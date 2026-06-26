from __future__ import annotations

from enterprise_ops_lab.observability.metrics import MetricsRecorder


def record_metric(metrics: MetricsRecorder, name: str, value: int = 1) -> None:
    metrics.increment(name, value)

