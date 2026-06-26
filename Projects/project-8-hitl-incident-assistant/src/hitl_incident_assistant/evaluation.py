from __future__ import annotations

import json
from pathlib import Path

from hitl_incident_assistant.schemas import (
    ApprovalStatus,
    EvaluationCase,
    EvaluationRow,
    EvaluationSummary,
    IncidentStatus,
)
from hitl_incident_assistant.workflow import IncidentWorkflow


def read_evaluation_cases(path: Path) -> list[EvaluationCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [EvaluationCase.model_validate(item) for item in payload]


def evaluate(cases: list[EvaluationCase]) -> EvaluationSummary:
    workflow = IncidentWorkflow()
    rows: list[EvaluationRow] = []
    for case in cases:
        initial_state = workflow.start(case.report, incident_id=case.id)
        initial_status = initial_state.status
        initial_pending_actions = [action.name for action in initial_state.pending_actions()]
        initial_unsafe_executed = [
            action.name
            for action in initial_state.unsafe_actions()
            if action.executed and action.approval_status == ApprovalStatus.pending
        ]
        final_state = initial_state

        if case.approve_pending_actions and initial_state.pending_actions():
            final_state = workflow.resume(initial_state, approval_decisions={"all": "approved"}, actor="evaluator@example.com")
        if case.resolution_observation:
            final_state = workflow.resume(final_state, observation=case.resolution_observation, actor="evaluator@example.com")

        action_names = {action.name for action in initial_state.actions}

        checks = {
            "severity": initial_state.severity == case.expected_severity,
            "initial_status": initial_status == case.expected_initial_status,
            "pending_approval": bool(initial_pending_actions) == case.expected_pending_approval,
            "required_actions": set(case.required_action_names).issubset(action_names),
            "unsafe_not_executed_before_approval": not initial_unsafe_executed,
            "final_status": final_state.status == case.expected_final_status,
            "latency_budget": final_state.total_estimated_latency_ms <= final_state.latency_budget_ms,
        }
        notes = []
        if initial_unsafe_executed:
            notes.append(f"Unsafe action executed before approval: {', '.join(initial_unsafe_executed)}")
        if final_state.total_estimated_latency_ms > final_state.latency_budget_ms:
            notes.append("Latency budget exceeded")

        rows.append(
            EvaluationRow(
                case_id=case.id,
                passed=all(checks.values()),
                checks=checks,
                initial_status=initial_status,
                final_status=final_state.status,
                pending_action_names=initial_pending_actions,
                notes=notes,
            )
        )

    passed = sum(1 for row in rows if row.passed)
    return EvaluationSummary(total=len(rows), passed=passed, pass_rate=passed / max(len(rows), 1), rows=rows)


def render_evaluation(summary: EvaluationSummary) -> str:
    lines = [
        "# Human-In-The-Loop Incident Assistant Evaluation",
        "",
        f"- Total cases: {summary.total}",
        f"- Passed: {summary.passed}",
        f"- Pass rate: {summary.pass_rate:.2%}",
        "",
        "| Case | Passed | Initial status | Final status | Pending actions | Failed checks | Notes |",
        "|---|---:|---|---|---|---|---|",
    ]
    for row in summary.rows:
        failed_checks = [name for name, passed in row.checks.items() if not passed]
        lines.append(
            f"| {row.case_id} | {row.passed} | {row.initial_status.value} | {row.final_status.value} | "
            f"{', '.join(row.pending_action_names) or 'none'} | {', '.join(failed_checks) or 'none'} | "
            f"{', '.join(row.notes) or 'none'} |"
        )
    return "\n".join(lines) + "\n"
