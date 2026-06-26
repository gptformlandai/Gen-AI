from __future__ import annotations

from structured_output_assistant.llm import RequirementsModel, RuleBasedRequirementsModel
from structured_output_assistant.schemas import AssistantRunResult
from structured_output_assistant.workflow.nodes import (
    finalize,
    generate_output,
    precheck_input,
    repair_output,
    route_after_precheck,
    route_after_validation,
    validate_output,
)
from structured_output_assistant.workflow.state import RequirementsWorkflowState


def build_requirements_graph(
    model: RequirementsModel | None = None,
    max_retries: int = 1,
):
    """Build the LangGraph workflow for Project 1.

    A single retry is intentional. If schema failures keep happening, that is a
    design signal, not something to hide behind endless retries.
    """

    try:
        from langgraph.graph import END, StateGraph
    except ImportError as error:
        raise RuntimeError(
            "LangGraph is not installed. Install project dependencies before building the graph."
        ) from error

    selected_model = model or RuleBasedRequirementsModel()

    workflow = StateGraph(RequirementsWorkflowState)
    workflow.add_node("precheck_input", precheck_input)
    workflow.add_node("generate_output", generate_output(selected_model))
    workflow.add_node("validate_output", validate_output)
    workflow.add_node("repair_output", repair_output(selected_model))
    workflow.add_node("finalize", finalize)

    workflow.set_entry_point("precheck_input")
    workflow.add_conditional_edges(
        "precheck_input",
        route_after_precheck,
        {
            "generate": "generate_output",
            "finalize": "finalize",
        },
    )
    workflow.add_edge("generate_output", "validate_output")
    workflow.add_conditional_edges(
        "validate_output",
        route_after_validation,
        {
            "repair": "repair_output",
            "finalize": "finalize",
        },
    )
    workflow.add_edge("repair_output", "validate_output")
    workflow.add_edge("finalize", END)

    return workflow.compile(), max_retries


def run_requirements_assistant(
    user_request: str,
    model: RequirementsModel | None = None,
    max_retries: int = 1,
) -> AssistantRunResult:
    graph, configured_retries = build_requirements_graph(model=model, max_retries=max_retries)
    final_state: RequirementsWorkflowState = graph.invoke(
        {
            "raw_request": user_request,
            "max_retries": configured_retries,
            "attempts": 0,
            "validation_errors": [],
        }
    )
    return final_state["final"]
