"""Build answer subgraphs from retrieved evidence."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


def build_subgraph(graph: InMemoryGraphRepository, evidence: list[EvidenceChunk]) -> InMemoryGraphRepository:
    node_ids: set[str] = set()
    relationship_ids: set[str] = set()
    for chunk in evidence:
        node_ids.update(chunk.node_ids)
        relationship_ids.update(chunk.relationship_ids)
    return graph.subgraph(node_ids, relationship_ids if relationship_ids else None)
