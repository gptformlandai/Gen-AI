"""Execution trace recorder."""

from __future__ import annotations

from dataclasses import dataclass, field

from convo_graph_lab.schema.models import TraceEvent


@dataclass
class TraceRecorder:
    events_by_session: dict[str, list[TraceEvent]] = field(default_factory=dict)

    def record(self, event: TraceEvent) -> None:
        self.events_by_session.setdefault(event.session_id, []).append(event)

    def get(self, session_id: str) -> list[TraceEvent]:
        return self.events_by_session.get(session_id, [])
