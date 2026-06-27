"""Ontology validation for graph entities and relationships."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.ontology import OntologyDefinition, ValidationIssue
from kg_enterprise_lab.schemas.relationship import GraphRelationship


class OntologyValidator:
    def __init__(self, ontology: OntologyDefinition) -> None:
        self.ontology = ontology

    def validate_node(self, node: GraphNode) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if node.label not in self.ontology.node_labels:
            issues.append(ValidationIssue(severity="error", code="unknown_label", message=f"Unknown label {node.label}", node_id=node.id))
        required = self.ontology.required_properties.get(node.label, set())
        missing = [prop for prop in required if prop not in node.properties and prop != "name"]
        for prop in missing:
            issues.append(ValidationIssue(severity="error", code="missing_property", message=f"{node.label} missing {prop}", node_id=node.id))
        return issues

    def validate_relationship(self, relationship: GraphRelationship, graph: InMemoryGraphRepository) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if relationship.type not in self.ontology.relationship_types:
            issues.append(
                ValidationIssue(severity="error", code="unknown_relationship", message=f"Unknown relationship {relationship.type}", relationship_id=relationship.id)
            )
        source = graph.get_node(relationship.source_id)
        target = graph.get_node(relationship.target_id)
        if not source:
            issues.append(ValidationIssue(severity="error", code="missing_source", message="Relationship source is missing", relationship_id=relationship.id))
        if not target:
            issues.append(ValidationIssue(severity="error", code="missing_target", message="Relationship target is missing", relationship_id=relationship.id))
        if source and target:
            issues.extend(self._validate_relationship_shape(relationship, source, target))
        return issues

    def _validate_relationship_shape(self, relationship: GraphRelationship, source: GraphNode, target: GraphNode) -> list[ValidationIssue]:
        shapes = [shape for shape in self.ontology.relationship_shapes if shape.relationship_type == relationship.type]
        if not shapes:
            return []
        for shape in shapes:
            source_ok = not shape.source_labels or source.label in shape.source_labels
            target_ok = not shape.target_labels or target.label in shape.target_labels
            if source_ok and target_ok:
                return []
        allowed = [
            f"{sorted(shape.source_labels)} -> {sorted(shape.target_labels)}"
            for shape in shapes
        ]
        return [
            ValidationIssue(
                severity=shapes[0].severity,
                code="relationship_shape",
                message=f"{relationship.type} cannot connect {source.label} to {target.label}; allowed: {'; '.join(allowed)}",
                relationship_id=relationship.id,
            )
        ]

    def validate_graph(self, graph: InMemoryGraphRepository) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for node in graph.nodes.values():
            issues.extend(self.validate_node(node))
        for relationship in graph.relationships.values():
            issues.extend(self.validate_relationship(relationship, graph))
        for rule in self.ontology.cardinality_rules:
            for node in graph.find_nodes(label=rule.source_label):
                rels = [
                    rel
                    for rel in graph.relationships_for_node(node.id, "out", {rule.relationship_type})
                    if not rule.target_label or (graph.get_node(rel.target_id) and graph.get_node(rel.target_id).label == rule.target_label)
                ]
                if len(rels) < rule.min_count:
                    issues.append(
                        ValidationIssue(
                            severity=rule.severity,
                            code="cardinality_min",
                            message=f"{node.name} requires at least {rule.min_count} {rule.relationship_type} relationship(s)",
                            node_id=node.id,
                        )
                    )
                if rule.max_count is not None and len(rels) > rule.max_count:
                    issues.append(
                        ValidationIssue(
                            severity=rule.severity,
                            code="cardinality_max",
                            message=f"{node.name} has too many {rule.relationship_type} relationships",
                            node_id=node.id,
                        )
                    )
        return issues
