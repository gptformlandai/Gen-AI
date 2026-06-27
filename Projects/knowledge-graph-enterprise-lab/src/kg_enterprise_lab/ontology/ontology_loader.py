"""Ontology loader with a no-dependency YAML fallback."""

from __future__ import annotations

from pathlib import Path

from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.schemas.ontology import CardinalityRule, OntologyDefinition, RelationshipShape


def load_ontology(path: Path | None = None) -> OntologyDefinition:
    if path is None or not path.exists():
        return default_ontology()
    try:
        import yaml  # type: ignore
    except ImportError:
        return default_ontology()
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    ontology = default_ontology()
    return ontology.model_copy(
        update={
            "version": str(payload.get("version", ontology.version)),
            "node_labels": set(payload.get("node_labels", ontology.node_labels)),
            "relationship_types": set(payload.get("relationship_types", ontology.relationship_types)),
            "required_properties": {key: set(value) for key, value in payload.get("required_properties", ontology.required_properties).items()},
            "cardinality_rules": _load_cardinality_rules(payload.get("cardinality_rules")) or ontology.cardinality_rules,
            "relationship_shapes": _load_relationship_shapes(payload.get("relationship_shapes")) or ontology.relationship_shapes,
        }
    )


def _load_cardinality_rules(raw: object) -> list[CardinalityRule]:
    if not isinstance(raw, dict):
        return []
    rules: list[CardinalityRule] = []
    for source_label, relationships in raw.items():
        if not isinstance(relationships, dict):
            continue
        for relationship_type, shape in relationships.items():
            if isinstance(shape, dict):
                rules.append(
                    CardinalityRule(
                        source_label=str(source_label),
                        relationship_type=str(relationship_type),
                        target_label=shape.get("target_label"),
                        min_count=int(shape.get("min", 0)),
                        max_count=shape.get("max"),
                    )
                )
    return rules


def _load_relationship_shapes(raw: object) -> list[RelationshipShape]:
    if not isinstance(raw, list):
        return []
    shapes: list[RelationshipShape] = []
    for item in raw:
        if isinstance(item, dict):
            shapes.append(
                RelationshipShape(
                    relationship_type=str(item["relationship_type"]),
                    source_labels=set(item.get("source_labels", [])),
                    target_labels=set(item.get("target_labels", [])),
                    severity=str(item.get("severity", "error")),
                )
            )
    return shapes
