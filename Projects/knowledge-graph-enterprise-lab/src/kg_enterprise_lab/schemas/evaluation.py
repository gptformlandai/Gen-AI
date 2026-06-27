"""Evaluation schemas for extraction, query, and GraphRAG checks."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvalCase(BaseModel):
    id: str
    question: str | None = None
    text: str | None = None
    must_include: list[str] = Field(default_factory=list)
    expected_entities: list[str] = Field(default_factory=list)
    expected_relationships: list[list[str]] = Field(default_factory=list)


class EvalResult(BaseModel):
    case_id: str
    passed: bool
    score: float
    details: str


class EvalReport(BaseModel):
    suite: str
    results: list[EvalResult]
    pass_rate: float
