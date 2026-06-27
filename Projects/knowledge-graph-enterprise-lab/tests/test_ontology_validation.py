from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.schemas.relationship import GraphRelationship


def test_ontology_validation_passes_sample_graph():
    graph = build_sample_graph()
    issues = OntologyValidator(default_ontology()).validate_graph(graph)
    assert [issue for issue in issues if issue.severity == "error"] == []


def test_ontology_validation_rejects_bad_relationship_shape():
    graph = build_sample_graph()
    graph.upsert_relationship(GraphRelationship(source_id="svc-provider-search", type="OWNED_BY", target_id="svc-provider-db"))
    issues = OntologyValidator(default_ontology()).validate_graph(graph)
    assert any(issue.code == "relationship_shape" for issue in issues)
