from __future__ import annotations

from enterprise_ops_lab.schemas.incident import EvidenceItem, McpSummary, RemediationPlan


def build_remediation_plan(service: str, symptoms: list[str], evidence: list[EvidenceItem], mcp: McpSummary, confidence_hint: float = 0.8) -> RemediationPlan:
    text = " ".join(item.quote.lower() for item in evidence)
    actions: list[str] = []
    root_cause = "Likely operational degradation requiring targeted investigation."
    rollback = False
    approval = False
    if "deployment" in symptoms or mcp.recent_deployments:
        root_cause = "Recent deployment correlates with degraded service metrics."
        actions.append("Compare metrics before and after the latest deployment.")
        if service in {"payments-api", "search-service"}:
            actions.append("Prepare rollback plan for the latest deployment.")
            rollback = True
            approval = True
    if "lag" in symptoms or "consumer" in text:
        root_cause = "Consumer capacity or partition imbalance is likely driving lag."
        actions.append("Increase partitions or consumer replicas after checking poison messages.")
    if "database" in symptoms or service == "shared-postgres":
        root_cause = "Database lock waits or slow queries are likely driving latency."
        actions.append("Inspect slow queries and lock waits before cancelling work.")
        approval = True
    if not actions:
        actions.append("Continue diagnostics and escalate to service owner.")
    confidence = min(0.98, confidence_hint + (0.05 if evidence else 0) + (0.05 if mcp.error_rate > 3 else 0))
    return RemediationPlan(
        likely_root_cause=root_cause,
        recommended_actions=actions,
        rollback_recommended=rollback,
        human_approval_required=approval,
        confidence=round(confidence, 2),
        escalation_reason="Human approval required for production-changing action." if approval else "",
    )

