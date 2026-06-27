"""Repository contract shared by local, Neo4j, and RDF-backed implementations."""

from __future__ import annotations

from typing import Protocol

from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.relationship import GraphRelationship


class GraphRepository(Protocol):
    def upsert_node(self, node: GraphNode) -> GraphNode: ...

    def upsert_relationship(self, relationship: GraphRelationship) -> GraphRelationship: ...

    def get_node(self, node_id: str) -> GraphNode | None: ...

    def find_nodes(self, label: str | None = None, name: str | None = None) -> list[GraphNode]: ...

    def neighbors(self, node_id: str, direction: str = "both", relationship_types: set[str] | None = None) -> list[GraphNode]: ...

    def relationships_for_node(self, node_id: str, direction: str = "both", relationship_types: set[str] | None = None) -> list[GraphRelationship]: ...
