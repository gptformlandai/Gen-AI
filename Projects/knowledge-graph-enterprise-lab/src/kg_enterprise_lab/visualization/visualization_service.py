"""View-specific visualization service."""

from __future__ import annotations

from kg_enterprise_lab.algorithms.blast_radius import blast_radius
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.resolution.entity_resolver import EntityResolver
from kg_enterprise_lab.visualization.cytoscape_exporter import export_cytoscape
from kg_enterprise_lab.visualization.graphviz_exporter import export_dot
from kg_enterprise_lab.visualization.mermaid_exporter import export_mermaid


class VisualizationService:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.graph = graph
        self.resolver = EntityResolver(graph)

    def subgraph_for_view(self, view: str, anchor_name: str | None = None) -> InMemoryGraphRepository:
        if view == "full":
            return self.graph
        anchor_id = self.resolver.resolve_name(anchor_name or "provider-search-service")
        if not anchor_id:
            return self.graph
        if view == "blast-radius":
            node_ids, rel_ids = blast_radius(self.graph, anchor_id)
            return self.graph.subgraph(node_ids, rel_ids)
        if view == "lineage":
            node_ids, rel_ids = self.graph.traverse(anchor_id, "out", {"HAS_LINEAGE_TO", "CALLS", "READS_FROM", "WRITES_TO"}, 4)
            return self.graph.subgraph(node_ids, rel_ids)
        if view == "incident-correlation":
            node_ids, rel_ids = self.graph.traverse(anchor_id, "both", {"HAS_INCIDENT", "DOCUMENTED_BY", "MITIGATED_BY", "IMPACTS"}, 3)
            return self.graph.subgraph(node_ids, rel_ids)
        node_ids, rel_ids = self.graph.traverse(anchor_id, "both", max_depth=2)
        return self.graph.subgraph(node_ids, rel_ids)

    def export(self, fmt: str = "json", view: str = "full", anchor_name: str | None = None) -> str | dict:
        subgraph = self.subgraph_for_view(view, anchor_name)
        if fmt == "mermaid":
            return export_mermaid(subgraph, title=view)
        if fmt == "dot":
            return export_dot(subgraph)
        return export_cytoscape(subgraph, view=view).model_dump()
