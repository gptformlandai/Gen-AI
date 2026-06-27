"""Query planning and result schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str
    max_depth: int = 4
    include_explanation: bool = True


class QueryPlan(BaseModel):
    intent: str
    entity_name: str | None = None
    target_name: str | None = None
    template_name: str | None = None
    max_depth: int = 4


class PathResult(BaseModel):
    node_ids: list[str]
    relationship_ids: list[str] = Field(default_factory=list)
    score: float = 1.0


class QueryResponse(BaseModel):
    question: str
    intent: str
    answer: str
    node_ids: list[str] = Field(default_factory=list)
    relationship_ids: list[str] = Field(default_factory=list)
    paths: list[PathResult] = Field(default_factory=list)
    explanation: list[str] = Field(default_factory=list)
    confidence: float = 1.0
