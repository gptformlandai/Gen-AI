from __future__ import annotations

import json
from pathlib import Path

from baseline_rag_assistant.schemas import TraceEvent


class JsonlTraceLogger:
    """Tiny JSONL trace logger for observability practice."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.events: list[TraceEvent] = []
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("", encoding="utf-8")

    def log(self, event: str, payload: dict) -> None:
        trace_event = TraceEvent(event=event, payload=payload)
        self.events.append(trace_event)
        if self.path:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(trace_event.model_dump(mode="json"), sort_keys=True) + "\n")
