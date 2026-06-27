"""Schemas for auditable ingestion reports."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceIngestionStats(BaseModel):
    source_name: str
    record_count: int
    checksum: str


class IngestionReport(BaseModel):
    source_stats: list[SourceIngestionStats] = Field(default_factory=list)
    document_count: int = 0
    node_count: int = 0
    relationship_count: int = 0
    warnings: list[str] = Field(default_factory=list)
