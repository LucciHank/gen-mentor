import re
import json
import ast
import logging
from typing import Dict, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


def _normalize_content_to_string(content: Any) -> str:
    """Convert provider-specific response content into a string."""
    if isinstance(content, str):
        return content
    if content is None:
        return ""
    if isinstance(content, list):
        parts = [_normalize_content_to_string(item).strip() for item in content]
        parts = [part for part in parts if part]
        if parts:
            return "\n".join(parts)
        return json.dumps(content, ensure_ascii=False)
    if isinstance(content, dict):
        for key in ("text", "content"):
            if key in content:
                normalized = _normalize_content_to_string(content[key]).strip()
                if normalized:
                    return normalized
        return json.dumps(content, ensure_ascii=False)
    return str(content)


def convert_json_output(output: str) -> Union[Dict[str, Any], list]:
    """
    Convert raw JSON output from the LLM into structured format.

    Args:
        output: The JSON output from the LLM
        
    Returns:
        Structured JSON output (dict or list)
    """
    output = _normalize_content_to_string(output).strip()
    
    # Cleanup common LLM artifacts
    # Remove markdown code blocks
    output = re.sub(r'^```(?:json)?\s*', '', output, flags=re.MULTILINE)
    output = re.sub(r'\s*```$', '', output, flags=re.MULTILINE)
    # Remove trailing commas before closing braces/brackets
    output = re.sub(r',\s*([}\]])', r'\1', output)
    # Replace single quotes with double quotes where safe
    output = re.sub(r"(\w+)(')(\w+)", r"\1\'\3", output)
    output = re.sub(r"(')([^']+)(')", r'"\2"', output)
    
    # Strategy 1: Direct JSON parse
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract first valid JSON object or array
    patterns = [
        (r'\{.*\}', re.DOTALL),  # Objects
        (r'\[.*\]', re.DOTALL),  # Arrays
    ]
    
    for pattern, flags in patterns:
        match = re.search(pattern, output, flags)
        if match:
            candidate = match.group(0).strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    
    # Strategy 3: ast.literal_eval fallback for Python-like syntax
    try:
        result = ast.literal_eval(output)
        if isinstance(result, (dict, list)):
            return result
    except (SyntaxError, ValueError):
        pass
    
    # Strategy 4: Extract all JSON patterns with regex matching
    bracket_stack = []
    start_pos = -1
    
    for i, char in enumerate(output):
        if char in '{[':
            if not bracket_stack:
                start_pos = i
            bracket_stack.append(char)
        elif char in '}]':
            if bracket_stack:
                opening = bracket_stack.pop()
                if (opening == '{' and char == '}') or (opening == '[' and char == ']'):
                    if not bracket_stack and start_pos != -1:
                        candidate = output[start_pos:i+1]
                        try:
                            return json.loads(candidate)
                        except json.JSONDecodeError:
                            try:
                                return ast.literal_eval(candidate)
                            except (SyntaxError, ValueError):
                                pass
    
    logger.error(f"{datetime.utcnow().isoformat()} Failed to parse JSON output, length={len(output)}")
    raise json.JSONDecodeError("No valid JSON found in response", output, 0)

def get_text_from_response(response):
    """Extract text from the response object."""
    if 'messages' in response:
        return _normalize_content_to_string(response['messages'][-1].content)
    if 'message' in response['choices'][0]:
        return _normalize_content_to_string(response['choices'][0]['message']['content'])
    return _normalize_content_to_string(response['choices'][0]['text'])

def extract_think_and_result(info):
    """Extract think and result content from the response info."""
    think_match = re.search(r"<think>(.*?)</think>", info, re.DOTALL)
    think_content = think_match.group(1).strip() if think_match else ''
    result_content = re.sub(r"<think>.*?</think>", "", info, flags=re.DOTALL).strip()
    return think_content, result_content


def preprocess_response(response, only_text=True, exclude_think=False, json_output=False, raise_errors=False):
    start_time = datetime.utcnow()
    
    try:
        if only_text or exclude_think or json_output:
            response = get_text_from_response(response)
            
        if exclude_think:
            think_content, result_content = extract_think_and_result(response)
            response = result_content
            
        if json_output:
            try:
                response = convert_json_output(response)
            except json.JSONDecodeError as e:
                logger.warning(
                    f"{start_time.isoformat()} JSON parsing failed: {str(e)}, "
                    f"response_length={len(response) if isinstance(response, str) else 'n/a'}"
                )
                response = {
                    "error": "Invalid JSON output",
                    "raw_content": response,
                    "parse_error": str(e)
                }
                if raise_errors:
                    raise e
    except Exception as e:
        logger.error(f"{start_time.isoformat()} Preprocessing failed: {str(e)}", exc_info=True)
        response = {
            "error": "Response preprocessing failed",
            "exception": str(e),
            "raw_content": response
        }
        if raise_errors:
            raise
            
    return response

