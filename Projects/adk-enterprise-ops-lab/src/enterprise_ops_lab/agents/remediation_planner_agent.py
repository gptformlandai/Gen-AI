from __future__ import annotations

from enterprise_ops_lab.schemas.incident import EvidenceItem, McpSummary, RemediationPlan
from enterprise_ops_lab.tools.remediation_tools import build_remediation_plan


def run(service: str, symptoms: list[str], evidence: list[EvidenceItem], mcp: McpSummary, confidence_hint: float = 0.8) -> RemediationPlan:
    """Specialist remediation planner behavior."""
    return build_remediation_plan(service, symptoms, evidence, mcp, confidence_hint)

