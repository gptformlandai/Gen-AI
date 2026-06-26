from __future__ import annotations

from workflow_triage_agent.schemas import WorkflowResult
from workflow_triage_agent.tools import PolicyLookupTool, TicketExecutionTool
from workflow_triage_agent.workflow.nodes import (
    classify_request,
    draft_plan,
    execute_action,
    finalize,
    human_approval,
    lookup_policy,
    receive_request,
    recover_policy,
    route_after_approval,
    route_after_plan,
    route_after_policy_lookup,
)
from workflow_triage_agent.workflow.state import TriageWorkflowState


def build_triage_graph(
    policy_tool: PolicyLookupTool | None = None,
    execution_tool: TicketExecutionTool | None = None,
):
    """Build the explicit LangGraph workflow."""

    try:
        from langgraph.graph import END, StateGraph
    except ImportError as error:
        raise RuntimeError("LangGraph is not installed. Install project dependencies first.") from error

    selected_policy_tool = policy_tool or PolicyLookupTool()
    selected_execution_tool = execution_tool or TicketExecutionTool()

    workflow = StateGraph(TriageWorkflowState)
    workflow.add_node("receive_request", receive_request)
    workflow.add_node("classify_request", classify_request)
    workflow.add_node("lookup_policy", lookup_policy(selected_policy_tool))
    workflow.add_node("recover_policy", recover_policy)
    workflow.add_node("draft_plan", draft_plan)
    workflow.add_node("human_approval", human_approval)
    workflow.add_node("execute_action", execute_action(selected_execution_tool))
    workflow.add_node("finalize", finalize)

    workflow.set_entry_point("receive_request")
    workflow.add_edge("receive_request", "classify_request")
    workflow.add_edge("classify_request", "lookup_policy")
    workflow.add_conditional_edges(
        "lookup_policy",
        route_after_policy_lookup,
        {
            "retry_policy": "lookup_policy",
            "recover_policy": "recover_policy",
            "draft_plan": "draft_plan",
        },
    )
    workflow.add_edge("recover_policy", "draft_plan")
    workflow.add_conditional_edges(
        "draft_plan",
        route_after_plan,
        {
            "human_approval": "human_approval",
            "execute_action": "execute_action",
        },
    )
    workflow.add_conditional_edges(
        "human_approval",
        route_after_approval,
        {
            "execute_action": "execute_action",
            "finalize": "finalize",
        },
    )
    workflow.add_edge("execute_action", "finalize")
    workflow.add_edge("finalize", END)
    return workflow.compile()


def run_triage_workflow(
    request: str,
    requester: str = "employee",
    human_decision: str = "",
    simulate_policy_failures: int = 0,
    max_policy_retries: int = 1,
) -> WorkflowResult:
    graph = build_triage_graph(policy_tool=PolicyLookupTool(simulate_policy_failures))
    final_state: TriageWorkflowState = graph.invoke(
        {
            "request": request,
            "requester": requester,
            "human_decision": human_decision,
            "max_policy_retries": max_policy_retries,
            "policy_attempts": 0,
            "errors": [],
            "trace": [],
        }
    )
    return final_state["final"]
