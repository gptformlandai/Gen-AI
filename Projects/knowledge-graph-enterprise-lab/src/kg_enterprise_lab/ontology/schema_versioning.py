"""Simple ontology version comparison helpers."""

from __future__ import annotations

from dataclasses import dataclass

from kg_enterprise_lab.schemas.ontology import OntologyDefinition


@dataclass(frozen=True)
class OntologyChange:
    category: str
    name: str
    change_type: str


def diff_ontologies(old: OntologyDefinition, new: OntologyDefinition) -> list[OntologyChange]:
    changes: list[OntologyChange] = []
    for label in sorted(new.node_labels - old.node_labels):
        changes.append(OntologyChange("node_label", label, "added"))
    for label in sorted(old.node_labels - new.node_labels):
        changes.append(OntologyChange("node_label", label, "removed"))
    for rel_type in sorted(new.relationship_types - old.relationship_types):
        changes.append(OntologyChange("relationship_type", rel_type, "added"))
    for rel_type in sorted(old.relationship_types - new.relationship_types):
        changes.append(OntologyChange("relationship_type", rel_type, "removed"))
    return changes
