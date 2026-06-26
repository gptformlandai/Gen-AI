from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class TraceRecorder:
    """Local trace sink that mirrors what would later feed OpenTelemetry."""

    def __init__(self, trace_dir: Path) -> None:
        self.trace_dir = trace_dir
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self.events: list[dict[str, Any]] = []

    def record(self, request_id: str, event: dict[str, Any]) -> None:
        self.events.append(event)
        path = self.trace_dir / f"{request_id}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    def tool_names(self) -> list[str]:
        return [event["tool_name"] for event in self.events if "tool_name" in event]

