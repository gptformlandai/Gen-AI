from __future__ import annotations

from enterprise_ops_lab.schemas.incident import InvestigationTimelineItem, McpSummary
from enterprise_ops_lab.workflows.parallel_diagnostics import run_parallel_diagnostics
from enterprise_ops_lab.workflows.sequential_investigation import run_sequential_investigation


def run(service: str, symptoms: list[str], mcp: McpSummary) -> list[InvestigationTimelineItem]:
    """Specialist workflow agent behavior."""
    return run_sequential_investigation(service, symptoms, mcp) + run_parallel_diagnostics(service, symptoms)

