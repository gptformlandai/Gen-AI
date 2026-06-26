from __future__ import annotations

from mcp_change_workflow.mcp_gateway import LocalMCPGateway
from mcp_change_workflow.schemas import ChangeRequest
from mcp_change_workflow.workflow import run_change_workflow


def test_mcp_gateway_exposes_resource_and_tools() -> None:
    gateway = LocalMCPGateway()

    resources = gateway.list_resources()
    tools = gateway.list_tools()

    assert resources[0].uri == "policy://change-management"
    assert {tool.name for tool in tools} >= {
        "risk.assess_change",
        "ticket.create_change",
        "notify.stakeholders",
    }


def test_low_risk_staging_change_completes() -> None:
    result = run_change_workflow(
        ChangeRequest(
            summary="Restart the staging support dashboard worker",
            environment="staging",
            requester="ops@example.com",
        )
    )

    assert result.status == "completed"
    assert result.ticket is not None
    assert result.ticket.created
    assert result.budget.mcp_request_count == 4


def test_high_risk_production_change_requires_approval() -> None:
    result = run_change_workflow(
        ChangeRequest(
            summary="Delete stale production records after export",
            environment="production",
            requester="ops@example.com",
        )
    )

    assert result.status == "pending_approval"
    assert result.risk is not None
    assert result.risk.approval_required
    assert result.ticket is None
    assert result.budget.mcp_request_count == 2


def test_approved_high_risk_change_creates_ticket() -> None:
    result = run_change_workflow(
        ChangeRequest(
            summary="Delete stale production records after export",
            environment="production",
            requester="ops@example.com",
            approved=True,
        )
    )

    assert result.status == "completed"
    assert result.ticket is not None
    assert result.ticket.ticket_id.startswith("PROD")
    assert result.notification is not None


def test_gateway_blocks_ticket_tool_without_approval() -> None:
    gateway = LocalMCPGateway()
    result = gateway.call_tool(
        "ticket.create_change",
        {
            "summary": "Delete stale production records after export",
            "environment": "production",
            "requester": "ops@example.com",
            "approved": False,
            "risk_level": "high",
        },
    )

    assert not result.ok
    assert "Approval is required" in result.error


def test_slow_risk_path_records_latency_budget_pressure() -> None:
    result = run_change_workflow(
        ChangeRequest(
            summary="Deploy production release with slow dependency scan",
            environment="production",
            requester="ops@example.com",
            approved=True,
        ),
        gateway=LocalMCPGateway(simulate_slow_risk_ms=80),
    )

    assert result.status == "completed"
    assert result.budget.measured_latency_ms >= 70
    assert result.budget.mcp_request_count == 4
