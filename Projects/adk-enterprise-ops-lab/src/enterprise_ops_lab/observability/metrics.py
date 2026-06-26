from __future__ import annotations

from collections import Counter


class MetricsRecorder:
    """In-memory counter set with an OpenTelemetry export placeholder."""

    def __init__(self) -> None:
        self.counters: Counter[str] = Counter()

    def increment(self, name: str, value: int = 1) -> None:
        self.counters[name] += value

    def snapshot(self) -> dict[str, int]:
        return dict(self.counters)

