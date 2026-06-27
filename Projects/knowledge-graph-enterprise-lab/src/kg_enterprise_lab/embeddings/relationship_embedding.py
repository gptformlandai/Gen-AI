"""Relationship text construction for embedding."""

from __future__ import annotations

from kg_enterprise_lab.schemas.relationship import GraphRelationship


def relationship_to_text(relationship: GraphRelationship) -> str:
    property_text = " ".join(str(value) for value in relationship.properties.values())
    return f"{relationship.source_id} {relationship.type} {relationship.target_id} {property_text}"
