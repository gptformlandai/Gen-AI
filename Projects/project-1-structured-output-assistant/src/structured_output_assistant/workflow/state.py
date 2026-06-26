from __future__ import annotations

from typing import TypedDict

from structured_output_assistant.schemas import AssistantRunResult, RequirementsDocument


class RequirementsWorkflowState(TypedDict, total=False):
    """State passed between LangGraph nodes.

    Keeping this explicit is the main reason to use LangGraph here: generation,
    validation, repair, and finalization become inspectable steps instead of
    hidden control flow.
    """

    raw_request: str
    raw_output: str
    validation_errors: list[str]
    attempts: int
    max_retries: int
    result: RequirementsDocument
    final: AssistantRunResult
    route: str
