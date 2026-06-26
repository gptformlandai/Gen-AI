from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from hitl_incident_assistant.policy import assess_severity, boundary_for, clarification_questions, plan_actions
from hitl_incident_assistant.schemas import (
    ActionProposal,
    ApprovalDecision,
    ApprovalStatus,
    BoundaryDecision,
    IncidentReport,
    IncidentState,
    IncidentStatus,
    RiskLevel,
    Severity,
    WorkflowEvent,
)


class IncidentWorkflow:
    """Small deterministic workflow engine for long-lived incident handling."""

    def start(self, report: IncidentReport, incident_id: str | None = None) -> IncidentState:
        now = utc_now()
        state = IncidentState(
            incident_id=incident_id or f"inc-{uuid4().hex[:8]}",
            report=report,
            severity=Severity.sev4,
            status=IncidentStatus.monitoring,
            boundary=BoundaryDecision(requires_human=False, reason="Workflow just started."),
            created_at=now,
            updated_at=now,
        )
        add_event(state, "incident_started", "Incident workflow started.", {"requester": report.requester})
        self._triage_and_plan(state)
        return state

    def resume(
        self,
        state: IncidentState,
        approval_decisions: dict[str, ApprovalDecision] | None = None,
        actor: str = "human@example.com",
        observation: str = "",
    ) -> IncidentState:
        if approval_decisions:
            self._apply_human_decisions(state, approval_decisions, actor)
        if observation:
            self._record_observation(state, observation, actor)
        state.updated_at = utc_now()
        return state

    def _triage_and_plan(self, state: IncidentState) -> None:
        questions = clarification_questions(state.report)
        state.severity = assess_severity(state.report)
        if questions:
            state.status = IncidentStatus.needs_clarification
            state.boundary = boundary_for(state.report, [], questions)
            add_event(state, "clarification_required", "Workflow paused because the incident report is incomplete.")
            return

        state.actions = plan_actions(state.report, state.severity)
        state.total_estimated_latency_ms = sum(action.estimated_latency_ms for action in state.actions)

        # Safe diagnostics run before the approval gate; remediation remains pending.
        for action in state.actions:
            if action.risk == RiskLevel.safe:
                execute_action(action)
                add_event(state, "safe_action_executed", f"Executed safe action: {action.name}.")

        pending = state.pending_actions()
        state.boundary = boundary_for(state.report, state.actions, [])
        state.status = IncidentStatus.waiting_for_human if pending else IncidentStatus.monitoring
        add_event(
            state,
            "approval_gate" if pending else "monitoring_started",
            state.boundary.reason,
            {"pending_actions": ",".join(action.name for action in pending)},
        )
        self._record_latency_warning_if_needed(state)

    def _apply_human_decisions(
        self,
        state: IncidentState,
        approval_decisions: dict[str, ApprovalDecision],
        actor: str,
    ) -> None:
        for action in state.pending_actions():
            decision = approval_decisions.get(action.action_id, approval_decisions.get("all"))
            if decision == "approved":
                action.approval_status = ApprovalStatus.approved
                execute_action(action)
                add_event(
                    state,
                    "unsafe_action_approved",
                    f"{actor} approved and executed: {action.name}.",
                    {"action_id": action.action_id},
                )
            elif decision == "rejected":
                action.approval_status = ApprovalStatus.rejected
                action.result = f"Rejected by {actor}; action was not executed."
                add_event(
                    state,
                    "unsafe_action_rejected",
                    f"{actor} rejected: {action.name}.",
                    {"action_id": action.action_id},
                )

        if state.pending_actions():
            state.status = IncidentStatus.waiting_for_human
            state.boundary = boundary_for(state.report, state.actions, [])
        else:
            state.status = IncidentStatus.monitoring
            state.boundary = BoundaryDecision(
                requires_human=False,
                reason="All pending approval decisions have been recorded.",
            )
            add_event(state, "monitoring_started", "Workflow resumed into monitoring.")

    def _record_observation(self, state: IncidentState, observation: str, actor: str) -> None:
        add_event(state, "observation_recorded", observation, {"actor": actor})
        if any(term in observation.lower() for term in ("resolved", "stable", "recovered")):
            state.status = IncidentStatus.resolved
            state.boundary = BoundaryDecision(requires_human=False, reason="Human observation marked the incident stable or resolved.")
            add_event(state, "incident_resolved", "Incident marked resolved from follow-up observation.")

    def _record_latency_warning_if_needed(self, state: IncidentState) -> None:
        if state.total_estimated_latency_ms <= state.latency_budget_ms:
            return
        add_event(
            state,
            "latency_budget_exceeded",
            "Estimated workflow latency exceeds the operational budget.",
            {
                "estimated_ms": str(state.total_estimated_latency_ms),
                "budget_ms": str(state.latency_budget_ms),
            },
        )


def execute_action(action: ActionProposal) -> None:
    action.executed = True
    action.result = f"Simulated execution completed for {action.name}."


def add_event(
    state: IncidentState,
    event_type: str,
    message: str,
    metadata: dict[str, str] | None = None,
) -> None:
    state.events.append(
        WorkflowEvent(
            timestamp=utc_now(),
            event_type=event_type,
            message=message,
            metadata=metadata or {},
        )
    )


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()

