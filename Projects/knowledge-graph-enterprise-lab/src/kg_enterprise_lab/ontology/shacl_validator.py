"""SHACL-style validation adapter.

This is intentionally lightweight: the production move is to send the same
ontology and generated RDF to a real SHACL engine such as pySHACL.
"""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.schemas.ontology import ValidationIssue


def validate_shacl_like(graph: InMemoryGraphRepository) -> list[ValidationIssue]:
    return OntologyValidator(default_ontology()).validate_graph(graph)
