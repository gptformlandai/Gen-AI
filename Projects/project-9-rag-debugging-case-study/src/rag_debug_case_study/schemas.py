from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


FailureLayer = Literal["none", "retrieval", "synthesis", "refusal", "evaluation_coverage"]
RetrieverMode = Literal["baseline", "improved"]


class KnowledgeDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str
    title: str
    body: str
    tags: list[str] = Field(default_factory=list)


class EvaluationQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    question: str
    expected_doc_id: str
    expected_terms: list[str]
    category: str


class RetrievalHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str
    title: str
    score: float
    reason: str
    rank: int


class AssistantAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: RetrieverMode
    question: str
    answer: str
    confidence: Literal["high", "medium", "low"]
    citations: list[RetrievalHit]


class EvaluationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    question: str
    category: str
    passed: bool
    expected_doc_id: str
    actual_doc_id: str
    top3_doc_ids: list[str]
    missing_terms: list[str]
    failure_layer: FailureLayer
    answer: str


class EvaluationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: RetrieverMode
    total: int
    passed: int
    pass_rate: float
    top1_accuracy: float
    top3_recall: float
    term_coverage: float
    failure_counts: dict[str, int]
    rows: list[EvaluationRow]


class ComparisonSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    baseline: EvaluationSummary
    improved: EvaluationSummary
    pass_rate_delta: float
    top1_accuracy_delta: float
    top3_recall_delta: float

