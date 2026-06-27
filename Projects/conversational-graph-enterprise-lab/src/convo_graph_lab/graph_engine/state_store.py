"""In-memory session state store with resume support."""

from __future__ import annotations

from dataclasses import dataclass, field

from convo_graph_lab.schema.models import ConversationState, StateSnapshot


@dataclass
class InMemoryStateStore:
    states: dict[str, ConversationState] = field(default_factory=dict)
    snapshots: dict[str, list[StateSnapshot]] = field(default_factory=dict)

    def save(self, state: ConversationState) -> None:
        self.states[state.session_id] = state

    def get(self, session_id: str) -> ConversationState | None:
        return self.states.get(session_id)

    def require(self, session_id: str) -> ConversationState:
        state = self.get(session_id)
        if not state:
            raise KeyError(f"Unknown session: {session_id}")
        return state

    def snapshot(self, state: ConversationState, node_id: str) -> StateSnapshot:
        snapshot = StateSnapshot(
            id=f"{state.session_id}:{state.step_count}:{node_id}",
            session_id=state.session_id,
            node_id=node_id,
            step_count=state.step_count,
            status=state.status,
            slots=dict(state.context.slots),
            variables=dict(state.context.variables),
        )
        self.snapshots.setdefault(state.session_id, []).append(snapshot)
        return snapshot

    def get_snapshots(self, session_id: str) -> list[StateSnapshot]:
        return self.snapshots.get(session_id, [])
