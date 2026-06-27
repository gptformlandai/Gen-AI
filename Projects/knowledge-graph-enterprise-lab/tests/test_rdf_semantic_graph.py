from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.ontology.rdf_serializer import graph_to_turtle
from kg_enterprise_lab.query.sparql_executor import execute_sparql_template
from kg_enterprise_lab.query.sparql_templates import get_sparql_template


def test_rdf_export_and_allowlisted_sparql_execution():
    graph = build_sample_graph()
    turtle = graph_to_turtle(graph)
    assert "ent:svc_provider_search ent:DEPENDS_ON ent:svc_provider_db" in turtle
    assert "SELECT ?service ?dependency" in get_sparql_template("service_dependencies")
    rows = execute_sparql_template(graph, "service_dependencies")
    assert {"service": "svc_provider_search", "dependency": "svc_provider_db", "predicate": "DEPENDS_ON"} in rows
