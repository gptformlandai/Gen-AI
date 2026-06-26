from __future__ import annotations

from enterprise_ops_lab.schemas.incident import InvestigationTimelineItem


def run_parallel_diagnostics(service: str, symptoms: list[str]) -> list[InvestigationTimelineItem]:
    """Parallel fan-out/gather simulation for independent diagnostic branches."""
    branches = [
        ("logs_branch", f"Scanned structured logs for {service}."),
        ("metrics_branch", f"Checked latency, saturation, and error metrics for {service}."),
        ("dependency_branch", f"Checked dependency health for {service}."),
    ]
    if "database" in symptoms:
        branches.append(("database_branch", "Checked slow queries, lock waits, and pool saturation."))
    if "lag" in symptoms:
        branches.append(("streaming_branch", "Checked partition lag, rebalances, and dead-letter queue volume."))
    return [InvestigationTimelineItem(step=name, outcome=outcome, latency_ms=140) for name, outcome in branches]

