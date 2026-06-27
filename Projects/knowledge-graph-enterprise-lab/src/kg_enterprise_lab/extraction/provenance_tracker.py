"""Track extraction source references."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProvenanceTracker:
    refs: dict[str, list[str]] = field(default_factory=dict)

    def add(self, entity_id: str, source_ref: str) -> None:
        self.refs.setdefault(entity_id, [])
        if source_ref not in self.refs[entity_id]:
            self.refs[entity_id].append(source_ref)
