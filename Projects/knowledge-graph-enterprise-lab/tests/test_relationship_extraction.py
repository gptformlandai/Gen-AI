from kg_enterprise_lab.extraction.relationship_extractor import RelationshipExtractor
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.schemas.extraction import SourceDocument


def test_relationship_extractor_finds_calls_and_topic_edges():
    graph = build_sample_graph()
    text = "mobile-app calls provider-search-service. payments-api publishes kafka-topic-payment-events."
    rels = RelationshipExtractor(graph).extract(SourceDocument(id="t", source_type="test", text=text))
    found = {(rel.source_name, rel.relationship_type, rel.target_name) for rel in rels}
    assert ("mobile-app", "CALLS", "provider-search-service") in found
    assert ("payments-api", "PUBLISHES_TO", "kafka-topic-payment-events") in found
