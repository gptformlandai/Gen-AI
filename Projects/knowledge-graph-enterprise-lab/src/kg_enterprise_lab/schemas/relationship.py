"""Relationship schemas for directed property graph edges."""

from __future__ import annotations

import hashlib
from typing import Any

from pydantic import BaseModel, Field, model_validator


class GraphRelationship(BaseModel):
    id: str = ""
    source_id: str
    target_id: str
    type: str
    properties: dict[str, Any] = Field(default_factory=dict)
    directed: bool = True
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def ensure_id(self) -> "GraphRelationship":
        if not self.id:
            raw = f"{self.source_id}|{self.type}|{self.target_id}|{self.directed}"
            self.id = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
        return self
