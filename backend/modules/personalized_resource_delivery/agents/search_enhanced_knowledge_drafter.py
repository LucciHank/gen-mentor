from __future__ import annotations

import ast
import logging
from typing import Any, Mapping, Optional, List
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

from pydantic import BaseModel, field_validator

from base import BaseAgent
from base.search_rag import SearchRagManager, format_docs
from modules.personalized_resource_delivery.prompts.search_enhanced_knowledge_drafter import (
    search_enhanced_knowledge_drafter_system_prompt,
    search_enhanced_knowledge_drafter_task_prompt,
)
from modules.personalized_resource_delivery.schemas import KnowledgeDraft
from config.loader import default_config


class KnowledgeDraftPayload(BaseModel):
    learner_profile: Any
    learning_path: Any
    learning_session: Any
    knowledge_points: Any
    knowledge_point: Any
    external_resources: str | None = ""

    @field_validator("learner_profile", "learning_path", "learning_session", "knowledge_points", "knowledge_point")
    @classmethod
    def coerce_jsonish(cls, v: Any) -> Any:
        if isinstance(v, BaseModel):
            return v.model_dump()
        if isinstance(v, Mapping):
            return dict(v)
        if isinstance(v, str):
            return v.strip()
        return v


class SearchEnhancedKnowledgeDrafter(BaseAgent):

    name: str = "SearchEnhancedKnowledgeDrafter"

    def __init__(self, model: Any, *, search_rag_manager: Optional[SearchRagManager] = None, use_search: bool = True):
        super().__init__(model=model, system_prompt=search_enhanced_knowledge_drafter_system_prompt, jsonalize_output=True)
        self.use_search = use_search
        if search_rag_manager is not None:
            self.search_rag_manager = search_rag_manager
        elif use_search:
            self.search_rag_manager = SearchRagManager.from_config(default_config)
        else:
            self.search_rag_manager = None

    def draft(self, payload: KnowledgeDraftPayload | Mapping[str, Any] | str):
        if not isinstance(payload, KnowledgeDraftPayload):
            payload = KnowledgeDraftPayload.model_validate(payload)
        data = payload.model_dump()
        # Optionally enrich external resources using the search RAG manager
        if self.use_search and self.search_rag_manager is not None:
            session = data.get("learning_session") or {}
            session_title = str(session.get("title", "")).strip() or "learning_session"
            knowledge_point = data.get("knowledge_point") or {}
            knowledge_point_name = str(knowledge_point.get('name', '')).strip()
            query = f"{session_title} {knowledge_point_name}".strip()
            docs = self.search_rag_manager.invoke(query)
            context = format_docs(docs)
            if context:
                ext = data.get("external_resources") or ""
                data["external_resources"] = f"{ext}{context}"
        raw_output = self.invoke(data, task_prompt=search_enhanced_knowledge_drafter_task_prompt)
        validated_output = KnowledgeDraft.model_validate(raw_output)
        return validated_output.model_dump()

def draft_knowledge_point_with_llm(
    llm,
    learner_profile,
    learning_path,
    learning_session,
    knowledge_points,
    knowledge_point,
    use_search: bool = True,
    *,
    search_rag_manager: Optional[SearchRagManager] = None,
):
    """Draft a single knowledge point using the agent, optionally enriching with a SearchRagManager."""
    drafter = SearchEnhancedKnowledgeDrafter(llm, search_rag_manager=search_rag_manager, use_search=use_search)
    payload = {
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "learning_session": learning_session,
        "knowledge_points": knowledge_points,
        "knowledge_point": knowledge_point,
    }
    return drafter.draft(payload)


def draft_knowledge_points_with_llm(
    llm,
    learner_profile,
    learning_path,
    learning_session,
    knowledge_points,
    allow_parallel: bool = True,
    use_search: bool = True,
    max_workers: int = 8,
    *,
    search_rag_manager: Optional[SearchRagManager] = None,
):
    """Draft multiple knowledge points in parallel or sequentially using the agent."""
    if isinstance(learning_session, str):
        try:
            learning_session = ast.literal_eval(learning_session)
        except (SyntaxError, ValueError, TypeError) as e:
            logger.error(f"Invalid learning_session format: {str(e)}. Content: {learning_session[:100]}")
            raise ValueError(f"Invalid learning_session format: expected valid JSON/parseable string. Error: {str(e)}")
    if isinstance(knowledge_points, str):
        try:
            knowledge_points = ast.literal_eval(knowledge_points)
        except (SyntaxError, ValueError, TypeError) as e:
            logger.error(f"Invalid knowledge_points format: {str(e)}. Content: {knowledge_points[:100]}")
            raise ValueError(f"Invalid knowledge_points format: expected valid JSON/parseable string. Error: {str(e)}")
    if search_rag_manager is None and use_search:
        try:
            search_rag_manager = SearchRagManager.from_config(default_config)
        except Exception as e:
            logger.error(f"Failed to initialize SearchRagManager: {str(e)}")
            search_rag_manager = None
    def draft_one(kp):
        try:
            return draft_knowledge_point_with_llm(
                llm,
                learner_profile,
                learning_path,
                learning_session,
                knowledge_points,
                kp,
                use_search=use_search,
                search_rag_manager=search_rag_manager,
            )
        except Exception as e:
            kp_name = kp.get('name', 'unknown') if isinstance(kp, dict) else str(kp)
            logger.error(f"Failed to draft knowledge point '{kp_name}': {str(e)}", exc_info=True)
            return {
                "error": True,
                "error_message": str(e),
                "error_type": type(e).__name__,
                "knowledge_point": kp,
                "name": kp_name,
                "status": "failed"
            }

    if allow_parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Use list() to consume all results - exceptions are now handled inside draft_one
            return list(executor.map(draft_one, knowledge_points))
    else:
        results: List[Any] = []
        for kp in knowledge_points:
            results.append(draft_one(kp))
        return results


if __name__ == "__main__":
    from config.loader import default_config
    from base.llm_factory import LLMFactory
    import logging

    llm = LLMFactory.from_config(default_config.llm)
    search_rag_manager = SearchRagManager.from_config(default_config)
    logging.basicConfig(level=default_config.log_level)
    logger = logging.getLogger(__name__)

    learner_profile = {"name": "Alice", "level": "intermediate"}
    learning_path = {"title": "Data Science Basics"}
    learning_session = {"title": "Introduction to Pandas"}
    knowledge_points = [
        {"name": "Pandas DataFrames"},
        {"name": "Data Cleaning with Pandas"},
    ]

    drafts = draft_knowledge_points_with_llm(
        llm,
        learner_profile,
        learning_path,
        learning_session,
        knowledge_points,
        allow_parallel=True,
        use_search=True,
    )

    for draft in drafts:
        logger.info(f"Drafted Knowledge Point: {draft}")
