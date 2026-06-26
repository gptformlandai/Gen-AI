from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from structured_output_assistant.schemas import RequirementsDocument


class OutputParseError(ValueError):
    """Raised when model output cannot be converted into a JSON object."""


def strip_markdown_fences(raw_output: str) -> str:
    """Handle the common LLM habit of wrapping JSON in Markdown fences."""

    stripped = raw_output.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", stripped, flags=re.DOTALL)
    return fenced.group(1).strip() if fenced else stripped


def extract_json_object(raw_output: str) -> str:
    """Extract the first JSON object from a model response.

    This is intentionally small and conservative. It supports the common case
    where the model adds a sentence before or after the JSON object, while still
    failing loudly when no object can be found.
    """

    candidate = strip_markdown_fences(raw_output)
    if candidate.startswith("{") and candidate.endswith("}"):
        return candidate

    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise OutputParseError("No JSON object found in model output.")
    return candidate[start : end + 1]


def parse_json_dict(raw_output: str) -> dict[str, Any]:
    try:
        parsed = json.loads(extract_json_object(raw_output))
    except json.JSONDecodeError as error:
        raise OutputParseError(f"Invalid JSON: {error}") from error

    if not isinstance(parsed, dict):
        raise OutputParseError("Model output must be a JSON object.")
    return parsed


def parse_requirements_document(raw_output: str) -> RequirementsDocument:
    return RequirementsDocument.model_validate(parse_json_dict(raw_output))


def format_validation_errors(error: Exception) -> list[str]:
    """Return compact validation messages suitable for repair prompts."""

    if isinstance(error, ValidationError):
        messages: list[str] = []
        for item in error.errors():
            location = ".".join(str(part) for part in item.get("loc", ()))
            messages.append(f"{location}: {item.get('msg')}")
        return messages
    return [str(error)]
