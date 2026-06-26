from __future__ import annotations

from pathlib import Path

from hitl_incident_assistant.evaluation import evaluate, read_evaluation_cases
from hitl_incident_assistant.schemas import ApprovalStatus, IncidentReport, IncidentStatus, Severity
from hitl_incident_assistant.storage import IncidentStore
from hitl_incident_assistant.workflow import IncidentWorkflow


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_ambiguous_report_requests_clarification() -> None:
    state = IncidentWorkflow().start(IncidentReport(summary="Something is weird."))

    assert state.status == IncidentStatus.needs_clarification
    assert state.boundary.clarification_questions
    assert state.actions == []


def test_unsafe_production_actions_wait_for_human() -> None:
    state = IncidentWorkflow().start(
        IncidentReport(
            summary="Checkout is down after a production deploy.",
            service="checkout",
            environment="production",
            impact="Customers cannot buy.",
            observed_signals=["HTTP 500 rate is 40 percent"],
            requester="ops@example.com",
        )
    )

    pending_names = {action.name for action in state.pending_actions()}
    assert state.severity == Severity.sev1
    assert state.status == IncidentStatus.waiting_for_human
    assert "rollback_deploy" in pending_names
    assert all(not action.executed for action in state.pending_actions())


def test_approval_resumes_and_executes_pending_actions() -> None:
    workflow = IncidentWorkflow()
    state = workflow.start(
        IncidentReport(
            summary="Billing worker is stuck and needs restart.",
            service="billing-worker",
            environment="staging",
            impact="Invoices are delayed.",
            observed_signals=["queue depth rising"],
            requester="billing@example.com",
        )
    )

    resumed = workflow.resume(state, approval_decisions={"all": "approved"}, actor="lead@example.com")

    assert resumed.status == IncidentStatus.monitoring
    assert all(action.approval_status != ApprovalStatus.pending for action in resumed.actions)
    assert any(action.name == "restart_service" and action.executed for action in resumed.actions)


def test_rejection_records_decision_without_execution() -> None:
    workflow = IncidentWorkflow()
    state = workflow.start(
        IncidentReport(
            summary="Recommendation service has high CPU during a traffic spike.",
            service="recommendations",
            environment="production",
            impact="Homepage recommendations are intermittently unavailable.",
            observed_signals=["CPU is 95 percent"],
            requester="growth@example.com",
        )
    )

    resumed = workflow.resume(state, approval_decisions={"all": "rejected"}, actor="lead@example.com")
    scale = next(action for action in resumed.actions if action.name == "scale_capacity")

    assert resumed.status == IncidentStatus.monitoring
    assert scale.approval_status == ApprovalStatus.rejected
    assert not scale.executed


def test_state_can_be_persisted_and_loaded(tmp_path: Path) -> None:
    store = IncidentStore(tmp_path)
    state = IncidentWorkflow().start(
        IncidentReport(
            summary="Search latency is degraded.",
            service="search",
            environment="production",
            impact="Users see slow searches.",
            observed_signals=["p95 latency is 2400 ms"],
            requester="search@example.com",
        ),
        incident_id="inc-test-001",
    )

    store.save(state)
    loaded = store.load("inc-test-001")

    assert loaded.incident_id == state.incident_id
    assert loaded.events
    assert loaded.status == IncidentStatus.monitoring


def test_evaluation_passes_project_threshold() -> None:
    summary = evaluate(read_evaluation_cases(DATA_DIR / "evaluation_cases.json"))

    assert summary.total == 8
    assert summary.pass_rate >= 0.85
