"""Validated graph mutation helpers."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.relationship import GraphRelationship


def merge_node(graph: InMemoryGraphRepository, node_id: str, label: str, name: str, **properties: object) -> GraphNode:
    return graph.upsert_node(GraphNode(id=node_id, label=label, name=name, properties=dict(properties)))


def merge_relationship(graph: InMemoryGraphRepository, source_id: str, rel_type: str, target_id: str, **properties: object) -> GraphRelationship:
    return graph.upsert_relationship(GraphRelationship(source_id=source_id, type=rel_type, target_id=target_id, properties=dict(properties)))
