"""Cytoscape-compatible JSON exporter."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.visualization import VisualizationEdge, VisualizationGraph, VisualizationNode


def export_cytoscape(graph: InMemoryGraphRepository, view: str = "full") -> VisualizationGraph:
    nodes = [
        VisualizationNode(id=node.id, label=node.label, name=node.name, properties=node.properties)
        for node in sorted(graph.nodes.values(), key=lambda item: item.id)
    ]
    edges = [
        VisualizationEdge(id=rel.id, source=rel.source_id, target=rel.target_id, type=rel.type, properties=rel.properties)
        for rel in sorted(graph.relationships.values(), key=lambda item: item.id)
    ]
    return VisualizationGraph(nodes=nodes, edges=edges, view=view)
