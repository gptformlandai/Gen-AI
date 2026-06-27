"""Audit logger for graph reads, mutations, and GraphRAG decisions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class AuditLogger:
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event_type: str, actor: str = "local-user", **fields: Any) -> dict[str, Any]:
        event = {"timestamp": datetime.now(timezone.utc).isoformat(), "event_type": event_type, "actor": actor, **fields}
        self.events.append(event)
        return event

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.events, indent=2, sort_keys=True), encoding="utf-8")
        return path
