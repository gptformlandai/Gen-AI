from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MemoryRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    memory_id: str
    text: str
    tags: list[str] = Field(default_factory=list)
    service: str = ""
    created_at: str
    score: float = 0.0

