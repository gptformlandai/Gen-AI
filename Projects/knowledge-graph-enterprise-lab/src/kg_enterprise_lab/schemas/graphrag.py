"""GraphRAG request, evidence, and answer schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GraphRAGRequest(BaseModel):
    question: str
    max_graph_depth: int = 3
    vector_top_k: int = 5


class EvidenceChunk(BaseModel):
    id: str
    text: str
    source: str
    score: float = 1.0
    node_ids: list[str] = Field(default_factory=list)
    relationship_ids: list[str] = Field(default_factory=list)


class GraphRAGTrace(BaseModel):
    intent: str
    linked_entities: list[str] = Field(default_factory=list)
    graph_steps: list[str] = Field(default_factory=list)
    vector_steps: list[str] = Field(default_factory=list)
    hybrid_steps: list[str] = Field(default_factory=list)
    guardrail_notes: list[str] = Field(default_factory=list)


class GraphRAGResponse(BaseModel):
    question: str
    answer: str
    evidence: list[EvidenceChunk] = Field(default_factory=list)
    trace: GraphRAGTrace
    confidence: float = 1.0
    grounded: bool = True
