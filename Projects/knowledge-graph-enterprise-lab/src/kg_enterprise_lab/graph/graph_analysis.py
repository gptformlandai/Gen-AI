"""Graph fundamentals helpers: summaries, neighborhoods, and subgraphs."""

from __future__ import annotations

from collections import Counter

from pydantic import BaseModel, Field

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


class GraphSummary(BaseModel):
    node_count: int
    relationship_count: int
    node_labels: dict[str, int] = Field(default_factory=dict)
    relationship_types: dict[str, int] = Field(default_factory=dict)
    orphan_node_ids: list[str] = Field(default_factory=list)
    density: float = 0.0


def summarize_graph(graph: InMemoryGraphRepository) -> GraphSummary:
    node_labels = Counter(node.label for node in graph.nodes.values())
    relationship_types = Counter(rel.type for rel in graph.relationships.values())
    orphan_node_ids = [
        node_id
        for node_id in graph.nodes
        if not graph.relationships_for_node(node_id, "both")
    ]
    possible_directed_edges = max(len(graph.nodes) * max(len(graph.nodes) - 1, 0), 1)
    density = round(len(graph.relationships) / possible_directed_edges, 5)
    return GraphSummary(
        node_count=len(graph.nodes),
        relationship_count=len(graph.relationships),
        node_labels=dict(sorted(node_labels.items())),
        relationship_types=dict(sorted(relationship_types.items())),
        orphan_node_ids=sorted(orphan_node_ids),
        density=density,
    )


def neighborhood_subgraph(
    graph: InMemoryGraphRepository,
    node_id: str,
    depth: int = 1,
    direction: str = "both",
    relationship_types: set[str] | None = None,
) -> InMemoryGraphRepository:
    node_ids, relationship_ids = graph.traverse(node_id, direction=direction, relationship_types=relationship_types, max_depth=depth)
    return graph.subgraph(node_ids, relationship_ids)
