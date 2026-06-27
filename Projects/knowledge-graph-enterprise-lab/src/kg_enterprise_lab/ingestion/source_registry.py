"""Source registry tracks provenance for loaded records."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SourceRegistry:
    sources: dict[str, str] = field(default_factory=dict)

    def register(self, source_id: str, description: str) -> str:
        self.sources[source_id] = description
        return source_id

    def describe(self, source_id: str) -> str:
        return self.sources.get(source_id, source_id)
