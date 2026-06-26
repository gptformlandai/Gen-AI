from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Severity = Literal["sev1", "sev2", "sev3", "sev4"]
Intent = Literal[
    "investigate_incident",
    "search_runbook",
    "generate_report",
    "remember_resolution",
    "evaluate_trajectory",
    "show_tool_trace",
    "demonstrate_state_memory",
]


class IncidentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    user_id: str = "local-user"
    session_id: str = "local-session"
    request_id: str = ""
    debug: bool = False


class IncidentTriage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: Intent
    service: str
    severity: Severity
    symptoms: list[str] = Field(default_factory=list)
    suspected_domain: str = "unknown"
    confidence: float = 0.0
    needs_clarification: bool = False
    clarification_questions: list[str] = Field(default_factory=list)


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    title: str
    quote: str
    score: float
    metadata: dict[str, str] = Field(default_factory=dict)


class McpSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_health: str
    error_rate: float
    recent_deployments: list[str]
    oncall_owner: str


class InvestigationTimelineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step: str
    outcome: str
    latency_ms: int = 0
    evidence_refs: list[str] = Field(default_factory=list)


class RemediationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    likely_root_cause: str
    recommended_actions: list[str]
    rollback_recommended: bool = False
    human_approval_required: bool = False
    confidence: float
    escalation_reason: str = ""


class IncidentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    session_id: str
    routed_agent: str
    triage: IncidentTriage
    likely_root_cause: str
    evidence: list[EvidenceItem]
    runbook_references: list[str]
    mcp_data_summary: McpSummary
    investigation_timeline: list[InvestigationTimelineItem]
    hypothesis_refinements: list[str]
    recommended_remediation: RemediationPlan
    human_approval: dict[str, Any]
    escalation_decision: str
    artifact_path: str
    memory_note_id: str
    evaluation_summary: dict[str, Any]
    metrics_snapshot: dict[str, int]
    tool_trajectory: list[str]
    final_answer: str
