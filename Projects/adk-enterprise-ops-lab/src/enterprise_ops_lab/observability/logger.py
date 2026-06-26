from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class StructuredLogger:
    """Tiny JSON logger used by callbacks, tools, workflows, and evaluation."""

    def __init__(self, log_path: Path | None = None) -> None:
        self.log_path = log_path
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def event(self, event_type: str, **fields: Any) -> dict[str, Any]:
        payload = {
            "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "event_type": event_type,
            **fields,
        }
        if self.log_path:
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True) + "\n")
        return payload

