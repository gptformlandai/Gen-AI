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
    text: str
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


class RerankedHit(SearchHit):
    rerank_score: float
    retrieval_queries: list[str] = Field(default_factory=list)
    rerank_reason: str = ""


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    citation_id: str
    document_id: str
    chunk_id: str
    title: str
    quote: str
    score: float
    rerank_score: float
    metadata: dict[str, str]


class RagAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    user_role: str
    status: Literal["answered", "refused"]
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    refusal_reason: str = ""
    confidence: Literal["high", "medium", "low"]


class GuardrailDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed: bool
    reason: str
    policy: str


class EvaluationQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    question: str
    user_role: str = "employee"
    expected_topics: list[str]
    expected_terms: list[str] = Field(default_factory=list)
    expected_status: Literal["answered", "refused"]


class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    passed: bool
    failure_category: str
    citation_topics: list[str]
    missing_terms: list[str]
    answer: str


class ComparisonRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    question: str
    user_role: str
    expected_status: str
    baseline: EvaluationResult
    advanced: EvaluationResult
    improved: bool


class ComparisonSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_questions: int
    baseline_passed: int
    advanced_passed: int
    baseline_pass_rate: float
    advanced_pass_rate: float
    improved_count: int
    rows: list[ComparisonRow]
