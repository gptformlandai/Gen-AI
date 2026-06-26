from __future__ import annotations

from typing import Literal, TypedDict

from workflow_triage_agent.schemas import (
    ActionPlan,
    ExecutionResult,
    PolicyContext,
    RequestClassification,
    TraceEvent,
    WorkflowResult,
)


class TriageWorkflowState(TypedDict, total=False):
    """Explicit state object passed between LangGraph nodes."""

    request: str
    requester: str
    human_decision: Literal["approved", "rejected", "pending", ""]
    max_policy_retries: int
    policy_attempts: int
    route: str
    status: str
    classification: RequestClassification
    policy: PolicyContext
    plan: ActionPlan
    execution: ExecutionResult
    trace: list[TraceEvent]
    errors: list[str]
    final: WorkflowResult
