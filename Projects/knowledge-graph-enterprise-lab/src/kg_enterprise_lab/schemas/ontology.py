"""Ontology and validation schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CardinalityRule(BaseModel):
    source_label: str
    relationship_type: str
    target_label: str | None = None
    min_count: int = 0
    max_count: int | None = None
    severity: str = "error"


class RelationshipShape(BaseModel):
    relationship_type: str
    source_labels: set[str] = Field(default_factory=set)
    target_labels: set[str] = Field(default_factory=set)
    severity: str = "error"


class OntologyDefinition(BaseModel):
    version: str = "1.0.0"
    node_labels: set[str] = Field(default_factory=set)
    relationship_types: set[str] = Field(default_factory=set)
    required_properties: dict[str, set[str]] = Field(default_factory=dict)
    cardinality_rules: list[CardinalityRule] = Field(default_factory=list)
    relationship_shapes: list[RelationshipShape] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    severity: str
    code: str
    message: str
    node_id: str | None = None
    relationship_id: str | None = None
