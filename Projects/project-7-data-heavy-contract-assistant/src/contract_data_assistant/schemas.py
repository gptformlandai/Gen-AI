from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ElementKind = Literal["metadata", "section", "clause", "table", "table_row", "obligation"]


class RawDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    path: str
    text: str


class MetadataField(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    value: str


class Section(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    level: int
    title: str
    path: str
    text: str = ""


class Clause(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    section_id: str
    section_path: str
    text: str
    actor: str = ""


class Table(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    section_path: str
    headers: list[str]
    rows: list[dict[str, str]]


class Obligation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    actor: str
    action: str
    source_clause_id: str
    section_path: str


class ParsedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    title: str
    metadata: list[MetadataField]
    sections: list[Section]
    clauses: list[Clause]
    tables: list[Table]
    obligations: list[Obligation]


class IndexedElement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    document_id: str
    kind: ElementKind
    title: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


class SearchHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    element: IndexedElement
    score: float
    reason: str


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    citation_id: str
    document_id: str
    element_id: str
    kind: ElementKind
    title: str
    quote: str
    metadata: dict[str, str]


class AssistantAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    answer: str
    citations: list[Citation]
    confidence: Literal["high", "medium", "low"]


class EvaluationQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    question: str
    expected_docs: list[str]
    expected_terms: list[str]
    expected_kind: ElementKind


class EvaluationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str
    passed: bool
    citation_docs: list[str]
    citation_kinds: list[str]
    missing_terms: list[str]
    answer: str


class EvaluationSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total: int
    passed: int
    pass_rate: float
    rows: list[EvaluationRow]
