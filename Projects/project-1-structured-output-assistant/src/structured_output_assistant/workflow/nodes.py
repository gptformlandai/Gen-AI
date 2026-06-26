from __future__ import annotations

from structured_output_assistant.llm import (
    RequirementsModel,
    contains_risky_request,
    looks_incomplete,
)
from structured_output_assistant.schemas import (
    AssistantRunResult,
    build_clarification_document,
    build_refusal_document,
)
from structured_output_assistant.validation import (
    format_validation_errors,
    parse_requirements_document,
)
from structured_output_assistant.workflow.state import RequirementsWorkflowState


def precheck_input(state: RequirementsWorkflowState) -> RequirementsWorkflowState:
    """Route obvious failures before spending model tokens.

    This demonstrates an important production habit: not every bad input should
    go to the model. Some cases are cheaper, safer, and clearer to handle with
    deterministic policy.
    """

    raw_request = state.get("raw_request", "").strip()
    if contains_risky_request(raw_request):
        return {
            **state,
            "raw_request": raw_request,
            "result": build_refusal_document(
                raw_request,
                "The request appears to involve credential theft, evasion, or unauthorized access.",
            ),
            "route": "finalize",
        }

    if looks_incomplete(raw_request):
        return {
            **state,
            "raw_request": raw_request,
            "result": build_clarification_document(
                raw_request,
                "The request is too vague to safely convert into implementation-ready requirements.",
            ),
            "route": "finalize",
        }

    return {**state, "raw_request": raw_request, "route": "generate"}


def generate_output(model: RequirementsModel):
    def _node(state: RequirementsWorkflowState) -> RequirementsWorkflowState:
        raw_output = model.generate(state["raw_request"])
        return {
            **state,
            "raw_output": raw_output,
            "attempts": state.get("attempts", 0) + 1,
            "validation_errors": [],
        }

    return _node


def validate_output(state: RequirementsWorkflowState) -> RequirementsWorkflowState:
    try:
        result = parse_requirements_document(state["raw_output"])
    except Exception as error:
        return {
            **state,
            "result": None,
            "validation_errors": format_validation_errors(error),
            "route": "repair",
        }

    return {
        **state,
        "result": result,
        "validation_errors": [],
        "route": "finalize",
    }


def repair_output(model: RequirementsModel):
    def _node(state: RequirementsWorkflowState) -> RequirementsWorkflowState:
        repaired_output = model.repair(
            user_request=state["raw_request"],
            previous_output=state.get("raw_output", ""),
            validation_errors=state.get("validation_errors", []),
        )
        return {
            **state,
            "raw_output": repaired_output,
            "attempts": state.get("attempts", 0) + 1,
        }

    return _node


def finalize(state: RequirementsWorkflowState) -> RequirementsWorkflowState:
    result = state.get("result")
    if result is None:
        final = AssistantRunResult(
            request=state.get("raw_request", ""),
            status="schema_error",
            attempts=state.get("attempts", 0),
            output=None,
            errors=state.get("validation_errors", []),
        )
    else:
        final = AssistantRunResult(
            request=state.get("raw_request", ""),
            status=result.status,
            attempts=state.get("attempts", 0),
            output=result,
            errors=[],
        )

    return {**state, "final": final}


def route_after_precheck(state: RequirementsWorkflowState) -> str:
    return state.get("route", "generate")


def route_after_validation(state: RequirementsWorkflowState) -> str:
    if state.get("route") == "finalize":
        return "finalize"

    if state.get("attempts", 0) <= state.get("max_retries", 1):
        return "repair"

    return "finalize"
