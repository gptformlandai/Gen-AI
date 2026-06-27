"""Graph neighborhood retrieval for GraphRAG."""

from __future__ import annotations

from collections import deque

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


class GraphRetriever:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.graph = graph

    def retrieve(
        self,
        anchor_ids: list[str],
        max_depth: int = 3,
        relationship_types: set[str] | None = None,
        max_nodes: int = 48,
    ) -> tuple[list[EvidenceChunk], set[str], set[str]]:
        relationship_types = relationship_types or OPERATIONAL_RETRIEVAL_EDGE_TYPES
        distances = self._distances(anchor_ids, max_depth, relationship_types, max_nodes)
        node_ids: set[str] = set(distances)
        relationship_ids: set[str] = set()
        for node_id in node_ids:
            for rel in self.graph.relationships_for_node(node_id, "both", relationship_types):
                if rel.source_id in node_ids and rel.target_id in node_ids:
                    relationship_ids.add(rel.id)
        evidence: list[EvidenceChunk] = []
        for node_id in sorted(node_ids):
            node = self.graph.get_node(node_id)
            if node:
                score = self._node_score(node.label, distances.get(node_id, max_depth))
                evidence.append(EvidenceChunk(id=f"graph-node-{node_id}", source="graph", text=f"{node.label} {node.name}: {node.properties}", node_ids=[node_id], score=score))
        for rel_id in sorted(relationship_ids):
            rel = self.graph.get_relationship(rel_id)
            if rel:
                evidence.append(EvidenceChunk(id=f"graph-rel-{rel_id}", source="graph", text=f"{rel.source_id} {rel.type} {rel.target_id}", relationship_ids=[rel_id], score=0.82))
        return evidence, node_ids, relationship_ids

    def _distances(self, anchor_ids: list[str], max_depth: int, relationship_types: set[str], max_nodes: int) -> dict[str, int]:
        distances: dict[str, int] = {}
        queue: deque[tuple[str, int]] = deque()
        for anchor_id in anchor_ids:
            if self.graph.get_node(anchor_id):
                distances[anchor_id] = 0
                queue.append((anchor_id, 0))
        while queue:
            node_id, depth = queue.popleft()
            if len(distances) >= max_nodes:
                break
            if depth >= max_depth:
                continue
            for neighbor in self.graph.neighbors(node_id, "both", relationship_types):
                if neighbor.id not in distances:
                    distances[neighbor.id] = depth + 1
                    queue.append((neighbor.id, depth + 1))
        return distances

    def _node_score(self, label: str, distance: int) -> float:
        label_bonus = {
            "Incident": 0.12,
            "Runbook": 0.1,
            "Database": 0.08,
            "Table": 0.06,
            "KafkaTopic": 0.05,
            "Service": 0.04,
        }.get(label, 0.0)
        return round(min(1.0, max(0.2, 1.0 - (distance * 0.12) + label_bonus)), 3)


OPERATIONAL_RETRIEVAL_EDGE_TYPES = {
    "DEPENDS_ON",
    "CALLS",
    "READS_FROM",
    "WRITES_TO",
    "PUBLISHES_TO",
    "CONSUMES_FROM",
    "HAS_INCIDENT",
    "DOCUMENTED_BY",
    "MITIGATED_BY",
    "IMPACTS",
    "HAS_LINEAGE_TO",
    "OWNED_BY",
    "MAINTAINED_BY",
}
