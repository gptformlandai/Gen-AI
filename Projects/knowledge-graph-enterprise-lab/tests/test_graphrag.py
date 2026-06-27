from kg_enterprise_lab.graphrag.graphrag_pipeline import GraphRAGPipeline
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest


def test_graphrag_answers_provider_latency_with_grounded_evidence():
    response = GraphRAGPipeline(build_sample_graph()).run(
        GraphRAGRequest(question="Use GraphRAG to explain why provider-search-service may be slow.")
    )
    assert "INC-1001" in response.answer
    assert "provider-db" in response.answer
    assert response.evidence
    assert response.trace.hybrid_steps
    assert any(chunk.source == "hybrid" for chunk in response.evidence)
    assert response.grounded
