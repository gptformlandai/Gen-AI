"""Alias registry for canonical entity IDs."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AliasManager:
    aliases: dict[str, str] = field(default_factory=dict)

    def add_alias(self, alias: str, canonical_id: str) -> None:
        self.aliases[alias.lower().strip()] = canonical_id

    def resolve(self, value: str) -> str | None:
        return self.aliases.get(value.lower().strip())
