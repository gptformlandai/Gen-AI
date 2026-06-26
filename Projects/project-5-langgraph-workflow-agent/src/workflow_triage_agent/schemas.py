from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RiskLevel = Literal["low", "medium", "high"]
WorkflowStatus = Literal[
    "received",
    "classified",
    "policy_loaded",
    "policy_recovered",
    "plan_drafted",
    "pending_human_approval",
    "approved",
    "rejected",
    "executed",
    "blocked",
]


class RequestClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str
    risk_level: RiskLevel
    approval_required: bool
    reason: str


class PolicyContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policy_id: str
    summary: str
    requires_approval: bool
    source: Literal["tool", "fallback"]


class ActionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    steps: list[str]
    assignee_team: str
    approval_required: bool
    risk_level: RiskLevel


class ExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    executed: bool
    message: str
    ticket_id: str = ""


class TraceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node: str
    message: str
    data: dict = Field(default_factory=dict)


class WorkflowResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request: str
    status: WorkflowStatus
    classification: RequestClassification | None = None
    policy: PolicyContext | None = None
    plan: ActionPlan | None = None
    execution: ExecutionResult | None = None
    trace: list[TraceEvent]
    errors: list[str] = Field(default_factory=list)
