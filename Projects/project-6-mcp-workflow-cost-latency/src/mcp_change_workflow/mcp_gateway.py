from __future__ import annotations

import time
from time import perf_counter

from mcp_change_workflow.schemas import (
    ChangeRequest,
    ChangeTicket,
    MCPResource,
    MCPToolResult,
    MCPToolSpec,
    RiskAssessment,
)


class LocalMCPGateway:
    """Local MCP capability boundary.

    The workflow calls this gateway by resource URI and tool name. That keeps
    business workflow code decoupled from the capability implementation, which
    is the practical interoperability lesson MCP is meant to teach.
    """

    def __init__(self, simulate_slow_risk_ms: int = 0) -> None:
        self.simulate_slow_risk_ms = simulate_slow_risk_ms
        self._resources = {
            "policy://change-management": MCPResource(
                uri="policy://change-management",
                name="Change Management Policy",
                description="Policy thresholds for change-ticket workflow.",
                content={
                    "production_requires_approval": True,
                    "destructive_actions_require_approval": True,
                    "low_risk_staging_auto_allowed": True,
                    "notify_on_production": True,
                    "destructive_terms": ["delete", "drop", "remove", "purge"],
                    "emergency_terms": ["outage", "incident", "emergency"],
                },
            )
        }
        self._tools = {
            "risk.assess_change": MCPToolSpec(
                name="risk.assess_change",
                description="Assess environment and summary to determine risk.",
            ),
            "ticket.create_change": MCPToolSpec(
                name="ticket.create_change",
                description="Create a change-management ticket.",
                risky=True,
            ),
            "notify.stakeholders": MCPToolSpec(
                name="notify.stakeholders",
                description="Notify stakeholders about a created change.",
            ),
        }

    def list_resources(self) -> list[MCPResource]:
        return list(self._resources.values())

    def list_tools(self) -> list[MCPToolSpec]:
        return list(self._tools.values())

    def read_resource(self, uri: str) -> MCPResource:
        if uri not in self._resources:
            raise KeyError(f"Unknown MCP resource: {uri}")
        return self._resources[uri]

    def call_tool(self, name: str, arguments: dict) -> MCPToolResult:
        if name not in self._tools:
            return MCPToolResult(tool_name=name, ok=False, error=f"Unknown MCP tool: {name}")

        started = perf_counter()
        try:
            if name == "risk.assess_change":
                output = self._risk_assess_change(arguments).model_dump(mode="json")
            elif name == "ticket.create_change":
                output = self._create_change_ticket(arguments).model_dump(mode="json")
            elif name == "notify.stakeholders":
                output = self._notify_stakeholders(arguments)
            else:
                raise KeyError(name)
            return MCPToolResult(
                tool_name=name,
                ok=True,
                output=output,
                latency_ms=round((perf_counter() - started) * 1000, 3),
            )
        except Exception as error:
            return MCPToolResult(
                tool_name=name,
                ok=False,
                error=str(error),
                latency_ms=round((perf_counter() - started) * 1000, 3),
            )

    def _risk_assess_change(self, arguments: dict) -> RiskAssessment:
        if self.simulate_slow_risk_ms:
            time.sleep(self.simulate_slow_risk_ms / 1000)

        request = ChangeRequest.model_validate(arguments)
        lower = request.summary.lower()
        reasons: list[str] = []

        destructive = any(term in lower for term in ("delete", "drop", "remove", "purge"))
        emergency = any(term in lower for term in ("outage", "incident", "emergency"))

        if request.environment == "production":
            reasons.append("Production environment increases blast radius.")
        if destructive:
            reasons.append("Summary contains destructive action terms.")
        if emergency:
            reasons.append("Emergency or incident wording requires stakeholder visibility.")

        if request.environment == "production" and destructive:
            risk_level = "high"
        elif request.environment == "production" or destructive or emergency:
            risk_level = "medium"
        else:
            risk_level = "low"

        return RiskAssessment(
            risk_level=risk_level,
            approval_required=risk_level == "high" or request.environment == "production",
            reasons=reasons or ["Routine low-risk change."],
        )

    def _create_change_ticket(self, arguments: dict) -> ChangeTicket:
        request = ChangeRequest.model_validate(
            {
                "summary": arguments["summary"],
                "environment": arguments["environment"],
                "requester": arguments.get("requester", "unknown@example.com"),
                "approved": arguments.get("approved", False),
            }
        )
        risk = arguments.get("risk_level", "low")

        if (request.environment == "production" or risk == "high") and not request.approved:
            raise PermissionError("Approval is required before creating this change ticket.")

        prefix = "PROD" if request.environment == "production" else "CHG"
        ticket_id = f"{prefix}-0001"
        return ChangeTicket(
            ticket_id=ticket_id,
            created=True,
            message=f"Created {ticket_id} for {request.summary}",
        )

    def _notify_stakeholders(self, arguments: dict) -> dict:
        ticket_id = arguments["ticket_id"]
        environment = arguments["environment"]
        risk_level = arguments["risk_level"]
        return {
            "sent": True,
            "channel": "change-management",
            "message": f"Notified stakeholders for {ticket_id} in {environment} risk={risk_level}",
        }
