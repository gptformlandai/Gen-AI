"""Runtime graph container."""

from __future__ import annotations

from dataclasses import dataclass

from convo_graph_lab.schema.models import EdgeDefinition, GraphDefinition, NodeDefinition


@dataclass
class RuntimeGraph:
    definition: GraphDefinition
    nodes: dict[str, NodeDefinition]
    edges: list[EdgeDefinition]

    def get_node(self, node_id: str) -> NodeDefinition:
        return self.nodes[node_id]


def build_runtime_graph(definition: GraphDefinition) -> RuntimeGraph:
    return RuntimeGraph(definition=definition, nodes={node.id: node for node in definition.nodes}, edges=definition.edges)
