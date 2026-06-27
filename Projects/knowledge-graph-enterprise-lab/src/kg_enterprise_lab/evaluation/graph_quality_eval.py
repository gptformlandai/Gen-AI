"""Graph quality evaluation for ontology, ownership, duplicates, and connectivity."""

from __future__ import annotations

from kg_enterprise_lab.algorithms.connected_components import connected_components
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.resolution.duplicate_detector import detect_duplicates
from kg_enterprise_lab.schemas.evaluation import EvalResult


def evaluate_graph_quality(graph: InMemoryGraphRepository) -> list[EvalResult]:
    issues = OntologyValidator(default_ontology()).validate_graph(graph)
    errors = [issue for issue in issues if issue.severity == "error"]
    services = graph.find_nodes(label="Service")
    owned_services = [
        service for service in services
        if graph.relationships_for_node(service.id, "out", {"OWNED_BY"})
    ]
    components = connected_components(graph)
    duplicates = detect_duplicates(graph)
    return [
        EvalResult(case_id="ontology_errors", passed=len(errors) == 0, score=1.0 if not errors else 0.0, details=f"errors={len(errors)}"),
        EvalResult(
            case_id="service_owner_coverage",
            passed=len(owned_services) == len(services),
            score=round(len(owned_services) / max(len(services), 1), 3),
            details=f"owned={len(owned_services)} total={len(services)}",
        ),
        EvalResult(
            case_id="duplicate_detection_signal",
            passed=any({"svc-provider-search", "svc-provider-search-v2"} <= {left, right} for left, right, _ in duplicates),
            score=1.0 if duplicates else 0.0,
            details=f"duplicates={duplicates}",
        ),
        EvalResult(
            case_id="connected_components",
            passed=len(components) <= 3,
            score=1.0 if len(components) <= 3 else 0.5,
            details=f"component_count={len(components)}",
        ),
    ]
