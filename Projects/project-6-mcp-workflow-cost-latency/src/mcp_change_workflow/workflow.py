from __future__ import annotations

import json

from mcp_change_workflow.budget import BudgetTracker
from mcp_change_workflow.mcp_gateway import LocalMCPGateway
from mcp_change_workflow.schemas import (
    ChangeRequest,
    ChangeTicket,
    RiskAssessment,
    TraceEvent,
    WorkflowResult,
)


def add_trace(trace: list[TraceEvent], step: str, message: str, data: dict | None = None) -> None:
    trace.append(TraceEvent(step=step, message=message, data=data or {}))


def run_change_workflow(
    request: ChangeRequest,
    gateway: LocalMCPGateway | None = None,
    budget: BudgetTracker | None = None,
) -> WorkflowResult:
    """Run the MCP-enabled change workflow."""

    mcp = gateway or LocalMCPGateway()
    tracker = budget or BudgetTracker()
    trace: list[TraceEvent] = []
    errors: list[str] = []

    add_trace(trace, "start", "Workflow started.", request.model_dump(mode="json"))

    policy = mcp.read_resource("policy://change-management")
    tracker.record_boundary_call(json.dumps(policy.model_dump(mode="json")))
    add_trace(trace, "mcp.resource.read", "Read change-management policy resource.", {"uri": policy.uri})

    risk_result = mcp.call_tool("risk.assess_change", request.model_dump(mode="json"))
    tracker.record_boundary_call(json.dumps(request.model_dump(mode="json")))
    if not risk_result.ok:
        errors.append(risk_result.error)
        return WorkflowResult(
            request=request,
            status="blocked",
            risk=None,
            ticket=None,
            notification=None,
            budget=tracker.snapshot(),
            trace=trace,
            errors=errors,
        )

    risk = RiskAssessment.model_validate(risk_result.output)
    add_trace(
        trace,
        "mcp.tool.risk",
        "Risk assessment completed.",
        {"risk": risk.model_dump(mode="json"), "latency_ms": risk_result.latency_ms},
    )

    if risk.approval_required and not request.approved:
        add_trace(
            trace,
            "approval.gate",
            "Workflow stopped before risky MCP ticket creation.",
            {"approval_required": True, "risk_level": risk.risk_level},
        )
        return WorkflowResult(
            request=request,
            status="pending_approval",
            risk=risk,
            ticket=None,
            notification=None,
            budget=tracker.snapshot(),
            trace=trace,
            errors=errors,
        )

    ticket_args = {**request.model_dump(mode="json"), "risk_level": risk.risk_level}
    ticket_result = mcp.call_tool("ticket.create_change", ticket_args)
    tracker.record_boundary_call(json.dumps(ticket_args))
    if not ticket_result.ok:
        errors.append(ticket_result.error)
        add_trace(trace, "mcp.tool.ticket", "Ticket creation failed.", {"error": ticket_result.error})
        return WorkflowResult(
            request=request,
            status="blocked",
            risk=risk,
            ticket=None,
            notification=None,
            budget=tracker.snapshot(),
            trace=trace,
            errors=errors,
        )

    ticket = ChangeTicket.model_validate(ticket_result.output)
    add_trace(
        trace,
        "mcp.tool.ticket",
        "Change ticket created.",
        {"ticket": ticket.model_dump(mode="json"), "latency_ms": ticket_result.latency_ms},
    )

    notify_args = {
        "ticket_id": ticket.ticket_id,
        "environment": request.environment,
        "risk_level": risk.risk_level,
    }
    notification_result = mcp.call_tool("notify.stakeholders", notify_args)
    tracker.record_boundary_call(json.dumps(notify_args))
    if not notification_result.ok:
        errors.append(notification_result.error)

    notification = notification_result.output if notification_result.ok else None
    add_trace(
        trace,
        "mcp.tool.notify",
        "Stakeholder notification completed." if notification_result.ok else "Stakeholder notification failed.",
        {"notification": notification, "latency_ms": notification_result.latency_ms},
    )

    return WorkflowResult(
        request=request,
        status="completed" if not errors else "blocked",
        risk=risk,
        ticket=ticket,
        notification=notification,
        budget=tracker.snapshot(),
        trace=trace,
        errors=errors,
    )
