"""Local metrics collector."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Metrics:
    counters: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    latencies_ms: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def latency(self, name: str, value: float) -> None:
        self.latencies_ms[name].append(value)

    def snapshot(self) -> dict[str, object]:
        return {
            "counters": dict(self.counters),
            "latencies_ms": {key: values for key, values in self.latencies_ms.items()},
        }
