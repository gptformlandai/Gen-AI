from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Document(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    text: str = Field(min_length=20)
    metadata: dict[str, str] = Field(default_factory=dict)


class Chunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    document_id: str
    title: str
    text: str = Field(min_length=5)
    chunk_index: int
    metadata: dict[str, str] = Field(default_factory=dict)


class SearchHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    title: str
    score: float
    text: str
    metadata: dict[str, str]


class Citation(BaseModel):
    """Traceable source reference for one answer claim."""

    model_config = ConfigDict(extra="forbid")

    citation_id: str
    document_id: str
    chunk_id: str
    title: str
    quote: str
    score: float
    metadata: dict[str, str]


class RagAnswer(BaseModel):
    """Stable answer contract for the RAG assistant."""

    model_config = ConfigDict(extra="forbid")

    question: str
    status: Literal["answered", "refused"]
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    refusal_reason: str = ""
    confidence: Literal["high", "medium", "low"]


class EvaluationQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    question: str
    expected_topics: list[str]
    expected_terms: list[str] = Field(default_factory=list)
    should_refuse: bool = False


class EvaluationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    question: str
    status: str
    passed: bool
    failure_category: str
    citation_topics: list[str]
    missing_terms: list[str]
    answer: str


class EvaluationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_questions: int
    passed: int
    failed: int
    pass_rate: float
    rows: list[EvaluationRow]


class TraceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event: str
    payload: dict
