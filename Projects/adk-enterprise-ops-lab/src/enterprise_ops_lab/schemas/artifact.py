from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ArtifactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    path: str
    version: int
    content_type: str
    metadata: dict[str, str] = Field(default_factory=dict)

