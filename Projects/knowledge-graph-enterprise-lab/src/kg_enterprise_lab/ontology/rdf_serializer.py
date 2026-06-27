"""Map property graph data to RDF/Turtle triples."""

from __future__ import annotations

import re

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.graph.rdf_triple_store import InMemoryTripleStore


def rdf_safe(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", value.strip())
    return cleaned.strip("_") or "unknown"


def graph_to_triples(graph: InMemoryGraphRepository) -> InMemoryTripleStore:
    store = InMemoryTripleStore()
    for node in graph.nodes.values():
        subject = rdf_safe(node.id)
        store.add(subject, "type", rdf_safe(node.label))
        store.add(subject, "label", rdf_safe(node.name))
    for rel in graph.relationships.values():
        store.add(rdf_safe(rel.source_id), rdf_safe(rel.type), rdf_safe(rel.target_id))
    return store


def graph_to_turtle(graph: InMemoryGraphRepository) -> str:
    return graph_to_triples(graph).to_turtle()
