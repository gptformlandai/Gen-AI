from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Document(BaseModel):
    """A source document before chunking."""

    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    text: str = Field(min_length=20)
    metadata: dict[str, str] = Field(default_factory=dict)


class Chunk(BaseModel):
    """A retrievable text unit.

    In real RAG systems, chunk quality often matters more than the vector store
    choice. This model keeps the link back to the source document explicit.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    document_id: str
    title: str
    text: str = Field(min_length=5)
    chunk_index: int
    metadata: dict[str, str] = Field(default_factory=dict)


class SearchHit(BaseModel):
    """One ranked search result."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    title: str
    score: float
    text: str
    metadata: dict[str, str]


class LabeledQuery(BaseModel):
    """Evaluation query with topic labels and optional metadata filters."""

    model_config = ConfigDict(extra="forbid")

    id: str
    query: str
    relevant_topics: list[str]
    filters: dict[str, str] = Field(default_factory=dict)


class EvaluationRow(BaseModel):
    """One row in the exact-vs-ANN comparison table."""

    model_config = ConfigDict(extra="forbid")

    query_id: str
    query: str
    filters: dict[str, str]
    exact_hit: bool
    ann_hit: bool
    exact_top_chunk_id: str
    ann_top_chunk_id: str
    exact_top_topic: str
    ann_top_topic: str
    exact_top_score: float
    ann_top_score: float


class EvaluationSummary(BaseModel):
    """Aggregate retrieval metrics for a labeled query set."""

    model_config = ConfigDict(extra="forbid")

    total_queries: int
    exact_hit_rate: float
    ann_hit_rate: float
    rows: list[EvaluationRow]
