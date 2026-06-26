from __future__ import annotations

from workflow_triage_agent.schemas import (
    ActionPlan,
    ExecutionResult,
    PolicyContext,
    RequestClassification,
    TraceEvent,
    WorkflowResult,
)
from workflow_triage_agent.tools import PolicyLookupTool, TicketExecutionTool, ToolFailure
from workflow_triage_agent.workflow.state import TriageWorkflowState


def add_trace(state: TriageWorkflowState, node: str, message: str, data: dict | None = None) -> list[TraceEvent]:
    return [
        *state.get("trace", []),
        TraceEvent(node=node, message=message, data=data or {}),
    ]


def receive_request(state: TriageWorkflowState) -> TriageWorkflowState:
    request = state.get("request", "").strip()
    return {
        **state,
        "request": request,
        "status": "received",
        "policy_attempts": state.get("policy_attempts", 0),
        "max_policy_retries": state.get("max_policy_retries", 1),
        "errors": state.get("errors", []),
        "trace": add_trace(state, "receive_request", "Request received.", {"request": request}),
    }


def classify_request(state: TriageWorkflowState) -> TriageWorkflowState:
    request = state["request"].lower()

    if "admin access" in request or "grant" in request and "access" in request:
        classification = RequestClassification(
            category="admin_access",
            risk_level="high",
            approval_required=True,
            reason="Access elevation can affect production data and auditability.",
        )
    elif "delete" in request and "production" in request:
        classification = RequestClassification(
            category="production_delete",
            risk_level="high",
            approval_required=True,
            reason="Production deletion is destructive and requires approval.",
        )
    elif "billing" in request or "invoice" in request:
        classification = RequestClassification(
            category="billing",
            risk_level="medium",
            approval_required=False,
            reason="Billing requests route to finance operations.",
        )
    elif "incident" in request or "outage" in request:
        classification = RequestClassification(
            category="incident",
            risk_level="medium",
            approval_required=False,
            reason="Incident routing needs ownership but is not automatically destructive.",
        )
    elif len(request) < 20:
        classification = RequestClassification(
            category="manual_review",
            risk_level="medium",
            approval_required=True,
            reason="The request is too ambiguous for automatic execution.",
        )
    else:
        classification = RequestClassification(
            category="operations",
            risk_level="low",
            approval_required=False,
            reason="Routine operational request.",
        )

    return {
        **state,
        "classification": classification,
        "status": "classified",
        "trace": add_trace(
            state,
            "classify_request",
            "Request classified.",
            classification.model_dump(mode="json"),
        ),
    }


def lookup_policy(policy_tool: PolicyLookupTool):
    def _node(state: TriageWorkflowState) -> TriageWorkflowState:
        attempts = state.get("policy_attempts", 0) + 1
        classification = state["classification"]
        try:
            policy = policy_tool.lookup(classification.category, classification.risk_level)
        except ToolFailure as error:
            errors = [*state.get("errors", []), str(error)]
            route = "retry_policy" if attempts <= state.get("max_policy_retries", 1) else "recover_policy"
            return {
                **state,
                "policy_attempts": attempts,
                "errors": errors,
                "route": route,
                "trace": add_trace(
                    state,
                    "lookup_policy",
                    "Policy lookup failed.",
                    {"attempts": attempts, "route": route, "error": str(error)},
                ),
            }

        return {
            **state,
            "policy": policy,
            "policy_attempts": attempts,
            "status": "policy_loaded",
            "route": "draft_plan",
            "trace": add_trace(
                state,
                "lookup_policy",
                "Policy loaded.",
                {"attempts": attempts, **policy.model_dump(mode="json")},
            ),
        }

    return _node


def recover_policy(state: TriageWorkflowState) -> TriageWorkflowState:
    policy = PolicyContext(
        policy_id="POL-FALLBACK-REVIEW",
        summary="Fallback policy: require human approval and route through manual operations review.",
        requires_approval=True,
        source="fallback",
    )
    return {
        **state,
        "policy": policy,
        "status": "policy_recovered",
        "trace": add_trace(
            state,
            "recover_policy",
            "Fallback policy applied after tool failures.",
            policy.model_dump(mode="json"),
        ),
    }


def draft_plan(state: TriageWorkflowState) -> TriageWorkflowState:
    classification = state["classification"]
    policy = state["policy"]
    approval_required = classification.approval_required or policy.requires_approval
    assignee = {
        "admin_access": "Identity Operations",
        "production_delete": "Data Reliability",
        "incident": "Incident Command",
        "billing": "Finance Operations",
        "manual_review": "Operations Review",
    }.get(classification.category, "Platform Operations")

    plan = ActionPlan(
        title=f"Triage {classification.category.replace('_', ' ')} request",
        steps=[
            "Confirm request scope and requester identity.",
            f"Apply policy {policy.policy_id}: {policy.summary}",
            "Create a traceable work item with owner and next action.",
        ],
        assignee_team=assignee,
        approval_required=approval_required,
        risk_level=classification.risk_level,
    )
    route = "human_approval" if approval_required else "execute_action"
    return {
        **state,
        "plan": plan,
        "status": "plan_drafted",
        "route": route,
        "trace": add_trace(state, "draft_plan", "Action plan drafted.", plan.model_dump(mode="json")),
    }


def human_approval(state: TriageWorkflowState) -> TriageWorkflowState:
    decision = state.get("human_decision") or "pending"
    if decision == "approved":
        return {
            **state,
            "status": "approved",
            "route": "execute_action",
            "trace": add_trace(state, "human_approval", "Human approved the plan."),
        }
    if decision == "rejected":
        return {
            **state,
            "status": "rejected",
            "route": "finalize",
            "trace": add_trace(state, "human_approval", "Human rejected the plan."),
        }
    return {
        **state,
        "status": "pending_human_approval",
        "route": "finalize",
        "trace": add_trace(state, "human_approval", "Workflow paused for human approval."),
    }


def execute_action(execution_tool: TicketExecutionTool):
    def _node(state: TriageWorkflowState) -> TriageWorkflowState:
        plan = state["plan"]
        if plan.approval_required and state.get("status") != "approved":
            execution = ExecutionResult(
                executed=False,
                message="Blocked: high-risk plan did not receive human approval.",
            )
            status = "blocked"
        else:
            execution = execution_tool.execute(state["classification"].category, plan.title)
            status = "executed"
        return {
            **state,
            "execution": execution,
            "status": status,
            "trace": add_trace(
                state,
                "execute_action",
                "Execution step completed.",
                execution.model_dump(mode="json"),
            ),
        }

    return _node


def finalize(state: TriageWorkflowState) -> TriageWorkflowState:
    final_trace = add_trace(state, "finalize", "Workflow finalized.", {"status": state.get("status", "blocked")})
    result = WorkflowResult(
        request=state.get("request", ""),
        status=state.get("status", "blocked"),
        classification=state.get("classification"),
        policy=state.get("policy"),
        plan=state.get("plan"),
        execution=state.get("execution"),
        trace=final_trace,
        errors=state.get("errors", []),
    )
    return {
        **state,
        "final": result,
        "trace": final_trace,
    }


def route_after_policy_lookup(state: TriageWorkflowState) -> str:
    return state.get("route", "draft_plan")


def route_after_plan(state: TriageWorkflowState) -> str:
    return state.get("route", "execute_action")


def route_after_approval(state: TriageWorkflowState) -> str:
    return state.get("route", "finalize")
