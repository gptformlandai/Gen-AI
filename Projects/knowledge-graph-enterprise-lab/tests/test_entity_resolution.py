from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.resolution.duplicate_detector import detect_duplicates
from kg_enterprise_lab.resolution.entity_resolver import EntityResolver
from kg_enterprise_lab.resolution.merge_strategy import merge_duplicate_node


def test_entity_resolver_uses_aliases_and_detects_duplicates():
    graph = build_sample_graph()
    resolver = EntityResolver(graph)
    assert resolver.resolve_name("providers-svc") == "svc-provider-search"
    duplicates = detect_duplicates(graph)
    assert any({"svc-provider-search", "svc-provider-search-v2"} <= {left, right} for left, right, _ in duplicates)


def test_merge_duplicate_node_rebuilds_relationship_indexes():
    graph = build_sample_graph()
    assert merge_duplicate_node(graph, "svc-provider-search", "svc-provider-search-v2")
    assert graph.get_node("svc-provider-search-v2") is None
    assert all(rel.source_id != "svc-provider-search-v2" and rel.target_id != "svc-provider-search-v2" for rel in graph.relationships.values())
    assert graph.relationships_for_node("svc-provider-search", "both")
