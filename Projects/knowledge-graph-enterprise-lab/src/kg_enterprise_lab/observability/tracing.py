"""Tiny tracing utility used by CLI, API, and GraphRAG flows."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class Trace:
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    steps: list[str] = field(default_factory=list)

    def add(self, step: str) -> None:
        self.steps.append(step)
