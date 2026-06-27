from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.schemas.query import QueryRequest


def test_query_layer_answers_dependents_and_blast_radius():
    service = GraphQueryService(build_sample_graph())
    dependents = service.answer(QueryRequest(question="What services depend on provider-search-service?"))
    assert "mobile-app" in dependents.answer
    blast = service.answer(QueryRequest(question="Show blast radius for payments-api."))
    assert "claims-orchestrator" in blast.answer
    assert "notification-service" in blast.answer


def test_query_layer_finds_shortest_path():
    service = GraphQueryService(build_sample_graph())
    response = service.answer(QueryRequest(question="Find shortest path between mobile-app and provider-db."))
    assert "mobile-app" in response.answer
    assert "provider-db" in response.answer


def test_query_layer_rejects_risky_depth():
    service = GraphQueryService(build_sample_graph())
    response = service.answer(QueryRequest(question="Show blast radius for payments-api.", max_depth=99))
    assert response.confidence == 0.0
    assert "traversal policy" in response.answer
