from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Severity(str, Enum):
    sev1 = "sev1"
    sev2 = "sev2"
    sev3 = "sev3"
    sev4 = "sev4"


class IncidentStatus(str, Enum):
    needs_clarification = "needs_clarification"
    waiting_for_human = "waiting_for_human"
    monitoring = "monitoring"
    resolved = "resolved"


class ApprovalStatus(str, Enum):
    not_required = "not_required"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RiskLevel(str, Enum):
    safe = "safe"
    approval_required = "approval_required"


class IncidentReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    service: str = ""
    environment: str = "production"
    impact: str = ""
    observed_signals: list[str] = Field(default_factory=list)
    requester: str = "unknown@example.com"


class ActionProposal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: str
    name: str
    description: str
    risk: RiskLevel
    approval_status: ApprovalStatus = ApprovalStatus.not_required
    estimated_latency_ms: int
    executed: bool = False
    result: str = ""


class BoundaryDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    requires_human: bool
    reason: str
    unsafe_action_ids: list[str] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)


class WorkflowEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: str
    event_type: str
    message: str
    metadata: dict[str, str] = Field(default_factory=dict)


class IncidentState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_id: str
    report: IncidentReport
    severity: Severity
    status: IncidentStatus
    boundary: BoundaryDecision
    actions: list[ActionProposal] = Field(default_factory=list)
    events: list[WorkflowEvent] = Field(default_factory=list)
    created_at: str
    updated_at: str
    total_estimated_latency_ms: int = 0
    latency_budget_ms: int = 1500

    def pending_actions(self) -> list[ActionProposal]:
        return [action for action in self.actions if action.approval_status == ApprovalStatus.pending]

    def unsafe_actions(self) -> list[ActionProposal]:
        return [action for action in self.actions if action.risk == RiskLevel.approval_required]


class EvaluationCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    report: IncidentReport
    expected_severity: Severity
    expected_initial_status: IncidentStatus
    expected_pending_approval: bool
    required_action_names: list[str]
    approve_pending_actions: bool = False
    resolution_observation: str = ""
    expected_final_status: IncidentStatus


class EvaluationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    passed: bool
    checks: dict[str, bool]
    initial_status: IncidentStatus
    final_status: IncidentStatus
    pending_action_names: list[str]
    notes: list[str]


class EvaluationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int
    passed: int
    pass_rate: float
    rows: list[EvaluationRow]


ApprovalDecision = Literal["approved", "rejected"]

