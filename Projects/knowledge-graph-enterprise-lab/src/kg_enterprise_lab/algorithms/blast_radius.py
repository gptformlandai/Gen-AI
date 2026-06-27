"""Blast radius and impacted owner calculation."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


DEPENDENCY_EDGE_TYPES = {"DEPENDS_ON", "CALLS", "READS_FROM", "WRITES_TO", "PUBLISHES_TO", "CONSUMES_FROM", "HAS_LINEAGE_TO"}


def blast_radius(graph: InMemoryGraphRepository, start_id: str, max_depth: int = 3) -> tuple[set[str], set[str]]:
    reverse_dependents, reverse_rels = graph.traverse(start_id, direction="in", relationship_types=DEPENDENCY_EDGE_TYPES, max_depth=max_depth)
    outbound_deps, outbound_rels = graph.traverse(start_id, direction="out", relationship_types=DEPENDENCY_EDGE_TYPES, max_depth=max_depth)
    return reverse_dependents | outbound_deps, reverse_rels | outbound_rels


def impacted_owners(graph: InMemoryGraphRepository, node_ids: set[str]) -> list[str]:
    teams: set[str] = set()
    owners: set[str] = set()
    for node_id in node_ids:
        for rel in graph.relationships_for_node(node_id, "out", {"OWNED_BY", "MAINTAINED_BY"}):
            target = graph.get_node(rel.target_id)
            if not target:
                continue
            if target.label == "Team":
                teams.add(target.name)
            elif target.label == "Owner":
                owners.add(target.name)
    return sorted(teams | owners)
