from __future__ import annotations

from hitl_incident_assistant.schemas import (
    ActionProposal,
    ApprovalStatus,
    BoundaryDecision,
    IncidentReport,
    RiskLevel,
    Severity,
)


SAFE_ACTION_LATENCY_MS = {
    "collect_diagnostics": 250,
    "notify_oncall": 120,
    "open_incident_channel": 90,
}

UNSAFE_ACTION_LATENCY_MS = {
    "rollback_deploy": 500,
    "restart_service": 420,
    "scale_capacity": 480,
    "post_status_page_update": 220,
}


def assess_severity(report: IncidentReport) -> Severity:
    text = report_text(report)
    if any(term in text for term in ("down", "cannot", "critical", "data loss", "checkout", "sign in")):
        return Severity.sev1
    if any(term in text for term in ("degraded", "timeout", "elevated", "latency", "stuck", "queue", "95 percent", "spike", "recovering")):
        return Severity.sev2
    if any(term in text for term in ("warning", "minor", "retry")):
        return Severity.sev3
    return Severity.sev4


def clarification_questions(report: IncidentReport) -> list[str]:
    questions: list[str] = []
    if not report.service.strip():
        questions.append("Which service or component is affected?")
    if not report.impact.strip():
        questions.append("What user or business impact is currently visible?")
    if not report.observed_signals:
        questions.append("Which observable signal supports the incident, such as latency, error rate, alert name, or queue depth?")
    return questions


def plan_actions(report: IncidentReport, severity: Severity) -> list[ActionProposal]:
    actions = [
        ActionProposal(
            action_id="act-001",
            name="collect_diagnostics",
            description=f"Collect logs, metrics, and recent deploy context for {report.service}.",
            risk=RiskLevel.safe,
            estimated_latency_ms=SAFE_ACTION_LATENCY_MS["collect_diagnostics"],
        )
    ]

    if severity in {Severity.sev1, Severity.sev2}:
        actions.extend(
            [
                ActionProposal(
                    action_id="act-002",
                    name="notify_oncall",
                    description=f"Notify the on-call owner for {report.service}.",
                    risk=RiskLevel.safe,
                    estimated_latency_ms=SAFE_ACTION_LATENCY_MS["notify_oncall"],
                ),
                ActionProposal(
                    action_id="act-003",
                    name="open_incident_channel",
                    description=f"Open a coordination channel for {report.service}.",
                    risk=RiskLevel.safe,
                    estimated_latency_ms=SAFE_ACTION_LATENCY_MS["open_incident_channel"],
                ),
            ]
        )

    text = report_text(report)
    unsafe_actions: list[tuple[str, str]] = []
    if any(term in text for term in ("deploy", "release", "rollback")):
        unsafe_actions.append(("rollback_deploy", "Rollback the most recent deployment after human approval."))
    if any(term in text for term in ("restart", "stuck", "heartbeat")):
        unsafe_actions.append(("restart_service", "Restart the affected service or worker after human approval."))
    if any(term in text for term in ("traffic spike", "high cpu", "95 percent", "capacity")):
        unsafe_actions.append(("scale_capacity", "Scale service capacity after human approval."))
    if severity == Severity.sev1 and any(term in text for term in ("customer", "customers", "unavailable", "cannot")):
        unsafe_actions.append(("post_status_page_update", "Post or update customer-facing incident communication after human approval."))

    next_id = 4
    for action_name, description in unsafe_actions:
        actions.append(
            ActionProposal(
                action_id=f"act-{next_id:03d}",
                name=action_name,
                description=description,
                risk=RiskLevel.approval_required,
                approval_status=ApprovalStatus.pending,
                estimated_latency_ms=UNSAFE_ACTION_LATENCY_MS[action_name],
            )
        )
        next_id += 1

    return actions


def boundary_for(report: IncidentReport, actions: list[ActionProposal], questions: list[str]) -> BoundaryDecision:
    if questions:
        return BoundaryDecision(
            requires_human=True,
            reason="Incident report is incomplete and needs human clarification.",
            clarification_questions=questions,
        )

    unsafe = [action.action_id for action in actions if action.approval_status == ApprovalStatus.pending]
    if unsafe:
        return BoundaryDecision(
            requires_human=True,
            reason="State-changing or customer-visible actions require human approval.",
            unsafe_action_ids=unsafe,
        )

    return BoundaryDecision(
        requires_human=False,
        reason="Only safe diagnostic or coordination actions are planned.",
    )


def report_text(report: IncidentReport) -> str:
    return " ".join(
        [
            report.summary,
            report.service,
            report.environment,
            report.impact,
            " ".join(report.observed_signals),
        ]
    ).lower()
