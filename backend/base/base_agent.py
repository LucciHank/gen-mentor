import logging
from typing import Any, Dict, Optional, Sequence

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.exceptions import (
    LangChainError,
    ConnectionError as LangChainConnectionError,
    TimeoutError as LangChainTimeoutError,
    RateLimitError as LangChainRateLimitError,
    APIError as LangChainAPIError
)

from utils.llm_output import preprocess_response
from langgraph.typing import InputT, OutputT, StateT

logger = logging.getLogger(__name__)
from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    JumpTo,
    ModelRequest,
    ModelResponse,
    OmitFromSchema,
    _InputAgentState,
    _OutputAgentState,
)

valid_agent_arg_list = [
    "middleware",
    "response_format",
    "state_schema",
    "context_schema",
    "checkpointer",
    "store",
    "interrupt_before",
    "interrupt_after",
    "debug",
    "name",
    "cache"
]


class BaseAgent:

    def __init__(
            self,
            model: BaseChatModel,
            system_prompt: Optional[str] = None,
            tools: Optional[list[Any]] = None,
            max_retries: int = 3,
            retry_min_wait: float = 1.0,
            retry_max_wait: float = 10.0,
            **kwargs
        ) -> None:
        """Initialize a base agent with JSON output and validation."""
        self._model = model
        self._system_prompt = system_prompt
        self._tools = tools
        self._agent_kwargs = {k: v for k, v in kwargs.items() if k in valid_agent_arg_list}
        self._agent = self._build_agent()
        self.exclude_think = kwargs.get("exclude_think", True)
        self.jsonalize_output = kwargs.get("jsonalize_output", True)
        self.max_retries = max_retries
        self.retry_min_wait = retry_min_wait
        self.retry_max_wait = retry_max_wait
        
        # Transient errors that should be retried
        self.retryable_errors = (
            LangChainConnectionError,
            LangChainTimeoutError,
            LangChainRateLimitError,
            LangChainAPIError,
        )

    def _build_agent(self):
        return create_agent(
            model=self._model,
            tools=self._tools,
            system_prompt=self._system_prompt,
            **self._agent_kwargs,
        )

    def set_prompts(self, system_prompt: Optional[str] = None, task_prompt: Optional[str] = None) -> None:
        """Set or update system/task prompts and rebuild the internal agent if needed."""
        if system_prompt is not None:
            self._system_prompt = system_prompt
        if task_prompt is not None:
            self._task_prompt = task_prompt
        self._agent = self._build_agent()

    def _build_prompt(self, variables: Dict[str, Any], task_prompt: Optional[str] = None) -> _InputAgentState:
        """Build chat messages for model call."""
        assert task_prompt is not None, "Either self._task_prompt or task_prompt must be provided."
        task_prompt = task_prompt
        formatted_task = task_prompt.format(**variables)  # type: ignore[union-attr]
        prompt = {
            "messages": [
                {"role": "user", "content": formatted_task}
            ]
        }
        return prompt

    def invoke(self, input_dict: dict, task_prompt: Optional[str] = None) -> Any:
        """Invoke the agent with the given input text.
        
        Includes retry logic with exponential backoff for transient LLM errors.
        """
        input_prompt = self._build_prompt(input_dict, task_prompt=task_prompt)
        
        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=self.retry_min_wait, max=self.retry_max_wait),
            retry=retry_if_exception_type(self.retryable_errors),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True
        )
        def _invoke_with_retry():
            try:
                return self._agent.invoke(input_prompt)
            except self.retryable_errors as e:
                logger.warning(f"Transient error during LLM call: {type(e).__name__}: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Non-retryable error during LLM call: {type(e).__name__}: {str(e)}")
                raise
        
        try:
            raw_output = _invoke_with_retry()
        except Exception as e:
            logger.error(f"LLM call failed after {self.max_retries} attempts: {type(e).__name__}: {str(e)}")
            raise
        
        output = preprocess_response(
            raw_output, only_text=True, exclude_think=self.exclude_think, json_output=self.jsonalize_output
        )
        return output
