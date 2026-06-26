from __future__ import annotations

from dataclasses import dataclass

from workflow_triage_agent.schemas import ExecutionResult, PolicyContext


class ToolFailure(RuntimeError):
    """Raised by deterministic tools to exercise retry and recovery paths."""


@dataclass
class PolicyLookupTool:
    """Fake policy tool with configurable failures for workflow testing."""

    failures_before_success: int = 0

    def lookup(self, category: str, risk_level: str) -> PolicyContext:
        if self.failures_before_success > 0:
            self.failures_before_success -= 1
            raise ToolFailure("Policy service temporarily unavailable.")

        if category == "admin_access":
            return PolicyContext(
                policy_id="POL-ACCESS-002",
                summary="Temporary admin access requires manager approval, expiry, and audit logging.",
                requires_approval=True,
                source="tool",
            )
        if category == "production_delete":
            return PolicyContext(
                policy_id="POL-DATA-007",
                summary="Production deletion requires export verification, approval, and rollback plan.",
                requires_approval=True,
                source="tool",
            )
        if category == "incident":
            return PolicyContext(
                policy_id="POL-INC-001",
                summary="Incidents must be assigned an owner, severity, and stakeholder update channel.",
                requires_approval=risk_level == "high",
                source="tool",
            )
        if category == "billing":
            return PolicyContext(
                policy_id="POL-BILL-004",
                summary="Billing escalations route to finance operations with customer-safe notes.",
                requires_approval=False,
                source="tool",
            )
        return PolicyContext(
            policy_id="POL-OPS-DEFAULT",
            summary="Low-risk operational tasks can be routed to the owning team with traceable notes.",
            requires_approval=False,
            source="tool",
        )


class TicketExecutionTool:
    """Fake executor that creates a deterministic ticket result."""

    def execute(self, category: str, title: str) -> ExecutionResult:
        ticket_prefix = {
            "admin_access": "ACCESS",
            "production_delete": "DATA",
            "incident": "INC",
            "billing": "BILL",
        }.get(category, "OPS")
        return ExecutionResult(
            executed=True,
            message=f"Created execution ticket for: {title}",
            ticket_id=f"{ticket_prefix}-0001",
        )
