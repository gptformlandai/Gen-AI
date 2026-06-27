"""Schemas for entity and relationship extraction."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    id: str
    source_type: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractedEntity(BaseModel):
    canonical_id: str
    label: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    confidence: float = 1.0
    source_ref: str
    properties: dict[str, Any] = Field(default_factory=dict)


class ExtractedRelationship(BaseModel):
    source_name: str
    relationship_type: str
    target_name: str
    confidence: float = 1.0
    source_ref: str
    evidence: str = ""
    properties: dict[str, Any] = Field(default_factory=dict)


class ExtractionBatch(BaseModel):
    entities: list[ExtractedEntity] = Field(default_factory=list)
    relationships: list[ExtractedRelationship] = Field(default_factory=list)
