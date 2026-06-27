"""Resolve the next edge from a node."""

from __future__ import annotations

from convo_graph_lab.schema.models import ConversationContext, EdgeDefinition
from convo_graph_lab.transitions.conditions import evaluate_condition


class TransitionResolver:
    def __init__(self, edges: list[EdgeDefinition]) -> None:
        self.edges_by_source: dict[str, list[EdgeDefinition]] = {}
        for edge in edges:
            self.edges_by_source.setdefault(edge.source, []).append(edge)
        for source, source_edges in self.edges_by_source.items():
            self.edges_by_source[source] = sorted(source_edges, key=lambda edge: edge.priority)

    def resolve(self, source_node_id: str, context: ConversationContext) -> EdgeDefinition | None:
        default_edge: EdgeDefinition | None = None
        for edge in self.edges_by_source.get(source_node_id, []):
            if edge.condition == "default":
                default_edge = edge
                continue
            if evaluate_condition(edge.condition, context):
                return edge
        return default_edge
