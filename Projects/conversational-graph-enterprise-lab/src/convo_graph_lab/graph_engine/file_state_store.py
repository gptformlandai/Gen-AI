"""File-backed state store for local CLI resume across processes."""

from __future__ import annotations

import json
from pathlib import Path

from convo_graph_lab.graph_engine.state_store import InMemoryStateStore
from convo_graph_lab.schema.models import ConversationState, StateSnapshot


class FileStateStore(InMemoryStateStore):
    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, state: ConversationState) -> None:
        super().save(state)
        self._state_path(state.session_id).write_text(state.model_dump_json(indent=2), encoding="utf-8")
        snapshots = [snapshot.model_dump() for snapshot in self.snapshots.get(state.session_id, [])]
        self._snapshots_path(state.session_id).write_text(json.dumps(snapshots, indent=2), encoding="utf-8")

    def get(self, session_id: str) -> ConversationState | None:
        state = super().get(session_id)
        if state:
            return state
        path = self._state_path(session_id)
        if not path.exists():
            return None
        loaded = ConversationState(**json.loads(path.read_text(encoding="utf-8")))
        self.states[session_id] = loaded
        snapshots_path = self._snapshots_path(session_id)
        if snapshots_path.exists():
            self.snapshots[session_id] = [
                StateSnapshot(**item)
                for item in json.loads(snapshots_path.read_text(encoding="utf-8"))
            ]
        return loaded

    def snapshot(self, state: ConversationState, node_id: str) -> StateSnapshot:
        snapshot = super().snapshot(state, node_id)
        snapshots = [item.model_dump() for item in self.snapshots.get(state.session_id, [])]
        self._snapshots_path(state.session_id).write_text(json.dumps(snapshots, indent=2), encoding="utf-8")
        return snapshot

    def _state_path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.state.json"

    def _snapshots_path(self, session_id: str) -> Path:
        return self.root / f"{session_id}.snapshots.json"
