from kg_enterprise_lab.extraction.entity_extractor import EntityExtractor
from kg_enterprise_lab.extraction.llm_extractor_placeholder import LLMExtractorPlaceholder
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph, load_documents
from kg_enterprise_lab.schemas.extraction import SourceDocument


def test_entity_extractor_finds_services_incidents_and_runbooks():
    graph = build_sample_graph()
    entities = EntityExtractor(graph).extract(load_documents()[0])
    ids = {entity.canonical_id for entity in entities}
    assert "svc-provider-search" in ids
    assert "INC-1001" in ids
    assert "runbook-provider-latency" in ids


def test_mock_llm_extractor_returns_schema_shaped_candidates():
    document = SourceDocument(id="doc-1", source_type="test", text="mobile-app calls provider-search-service after INC-1001.")
    extractor = LLMExtractorPlaceholder()
    batch = extractor.extract(document)
    assert "Extract enterprise knowledge graph" in extractor.build_prompt(document)
    assert any(entity.canonical_id == "svc-mobile-app" for entity in batch.entities)
    assert any(rel.relationship_type == "CALLS" for rel in batch.relationships)
