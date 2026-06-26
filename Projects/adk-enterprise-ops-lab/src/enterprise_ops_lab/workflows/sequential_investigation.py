from __future__ import annotations

from enterprise_ops_lab.schemas.incident import InvestigationTimelineItem, McpSummary


def run_sequential_investigation(service: str, symptoms: list[str], mcp: McpSummary) -> list[InvestigationTimelineItem]:
    """Sequential workflow: health, deploy, error-rate, owner."""
    return [
        InvestigationTimelineItem(step="check_service_health", outcome=f"{service} health is {mcp.service_health}", latency_ms=80),
        InvestigationTimelineItem(step="inspect_recent_deployments", outcome="; ".join(mcp.recent_deployments) or "No deployments found", latency_ms=95),
        InvestigationTimelineItem(step="measure_error_rate", outcome=f"Error rate is {mcp.error_rate} percent", latency_ms=70),
        InvestigationTimelineItem(step="identify_oncall", outcome=f"On-call owner is {mcp.oncall_owner}", latency_ms=30),
        InvestigationTimelineItem(step="map_symptoms", outcome=f"Symptoms considered: {', '.join(symptoms) or 'none'}", latency_ms=20),
    ]

