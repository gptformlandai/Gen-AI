from __future__ import annotations

from workflow_triage_agent.workflow import run_triage_workflow


def trace_nodes(result) -> list[str]:
    return [event.node for event in result.trace]


def test_low_risk_request_executes_without_human_approval() -> None:
    result = run_triage_workflow("Restart the support dashboard worker after business hours.")

    assert result.status == "executed"
    assert result.execution is not None
    assert result.execution.executed
    assert "human_approval" not in trace_nodes(result)


def test_high_risk_request_pauses_for_human_approval() -> None:
    result = run_triage_workflow("Grant temporary admin access to a reviewer for production records.")

    assert result.status == "pending_human_approval"
    assert result.plan is not None
    assert result.plan.approval_required
    assert result.execution is None
    assert "human_approval" in trace_nodes(result)


def test_high_risk_request_executes_after_approval() -> None:
    result = run_triage_workflow(
        "Grant temporary admin access to a reviewer for production records.",
        human_decision="approved",
    )

    assert result.status == "executed"
    assert result.execution is not None
    assert result.execution.ticket_id.startswith("ACCESS")


def test_high_risk_request_stops_when_rejected() -> None:
    result = run_triage_workflow(
        "Delete stale production records after export verification.",
        human_decision="rejected",
    )

    assert result.status == "rejected"
    assert result.execution is None


def test_policy_lookup_retries_then_succeeds() -> None:
    result = run_triage_workflow(
        "Route a billing escalation to finance operations.",
        simulate_policy_failures=1,
        max_policy_retries=1,
    )

    assert result.status == "executed"
    assert result.policy is not None
    assert result.policy.source == "tool"
    assert len(result.errors) == 1


def test_policy_lookup_recovers_after_persistent_failure() -> None:
    result = run_triage_workflow(
        "Simulate policy outage while routing a billing escalation.",
        simulate_policy_failures=2,
        max_policy_retries=1,
    )

    assert result.status == "pending_human_approval"
    assert result.policy is not None
    assert result.policy.source == "fallback"
    assert "recover_policy" in trace_nodes(result)
