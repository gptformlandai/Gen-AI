from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Environment = Literal["dev", "staging", "production"]
RiskLevel = Literal["low", "medium", "high"]
WorkflowStatus = Literal["completed", "pending_approval", "blocked"]


class ChangeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str = Field(min_length=5)
    environment: Environment
    requester: str = "unknown@example.com"
    approved: bool = False


class MCPResource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uri: str
    name: str
    description: str
    content: dict


class MCPToolSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    risky: bool = False


class MCPToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_name: str
    ok: bool
    output: dict = Field(default_factory=dict)
    error: str = ""
    latency_ms: float = 0.0


class RiskAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_level: RiskLevel
    approval_required: bool
    reasons: list[str]


class ChangeTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str
    created: bool
    message: str


class BudgetEstimate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    estimated_tokens: int = 0
    estimated_cost_usd: float = 0.0
    mcp_request_count: int = 0
    measured_latency_ms: float = 0.0
    latency_budget_ms: float = 500.0
    request_budget: int = 4
    within_latency_budget: bool = True
    within_request_budget: bool = True


class TraceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step: str
    message: str
    data: dict = Field(default_factory=dict)


class WorkflowResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request: ChangeRequest
    status: WorkflowStatus
    risk: RiskAssessment | None = None
    ticket: ChangeTicket | None = None
    notification: dict | None = None
    budget: BudgetEstimate
    trace: list[TraceEvent]
    errors: list[str] = Field(default_factory=list)
