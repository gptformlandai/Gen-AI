from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
import json


@dataclass
class Session:
    """Per-user transient context. Durable memories live elsewhere."""

    session_id: str
    user_id: str
    state: dict[str, object] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).replace(microsecond=0).isoformat())


class InMemorySessionService:
    """ADK session-service stand-in with optional local checkpointing."""

    def __init__(self, checkpoint_dir: Path | None = None) -> None:
        self.sessions: dict[str, Session] = {}
        self.checkpoint_dir = checkpoint_dir
        if checkpoint_dir:
            checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def get_or_create(self, session_id: str, user_id: str) -> Session:
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(session_id=session_id, user_id=user_id)
        return self.sessions[session_id]

    def update(self, session_id: str, key: str, value: object) -> None:
        self.sessions[session_id].state[key] = value
        self.save(session_id)

    def save(self, session_id: str) -> None:
        if not self.checkpoint_dir:
            return
        session = self.sessions[session_id]
        payload = {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "state": session.state,
            "created_at": session.created_at,
        }
        (self.checkpoint_dir / f"{session_id}.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

