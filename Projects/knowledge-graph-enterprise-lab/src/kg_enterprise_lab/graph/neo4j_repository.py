"""Neo4j repository abstraction and Cypher generation helpers.

The local lab does not require Neo4j. This module shows the production seam:
replace ``InMemoryGraphRepository`` with this class after installing the
``neo4j`` optional dependency and setting credentials.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.relationship import GraphRelationship


def cypher_merge_node(node: GraphNode) -> tuple[str, dict[str, Any]]:
    query = f"MERGE (n:{node.label} {{id: $id}}) SET n.name = $name, n += $properties RETURN n"
    return query, {"id": node.id, "name": node.name, "properties": node.properties}


def cypher_merge_relationship(relationship: GraphRelationship) -> tuple[str, dict[str, Any]]:
    query = (
        "MATCH (s {id: $source_id}), (t {id: $target_id}) "
        f"MERGE (s)-[r:{relationship.type}]->(t) "
        "SET r.id = $id, r += $properties RETURN r"
    )
    return query, relationship.model_dump()


@dataclass
class Neo4jRepository:
    uri: str
    user: str
    password: str

    def connect(self) -> object:
        try:
            from neo4j import GraphDatabase  # type: ignore
        except ImportError as exc:
            raise RuntimeError("Install the graphdb extra to use Neo4j: pip install -e '.[graphdb]'") from exc
        return GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def planned_write_batch(self, nodes: list[GraphNode], relationships: list[GraphRelationship]) -> list[tuple[str, dict[str, Any]]]:
        statements = [cypher_merge_node(node) for node in nodes]
        statements.extend(cypher_merge_relationship(rel) for rel in relationships)
        return statements
