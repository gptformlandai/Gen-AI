"""Node schemas for the enterprise property graph."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class GraphNode(BaseModel):
    id: str
    label: str
    name: str
    properties: dict[str, Any] = Field(default_factory=dict)
    aliases: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    @field_validator("id", "label", "name")
    @classmethod
    def require_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned

    def searchable_text(self) -> str:
        fields = [self.id, self.label, self.name, " ".join(self.aliases)]
        fields.extend(str(value) for value in self.properties.values() if isinstance(value, (str, int, float)))
        return " ".join(fields).lower()
