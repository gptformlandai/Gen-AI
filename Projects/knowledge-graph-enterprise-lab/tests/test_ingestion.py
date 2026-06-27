from kg_enterprise_lab.graph.graph_analysis import summarize_graph
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_ingestion_report, build_sample_graph, load_enterprise_sources


def test_ingestion_loads_realistic_enterprise_sources():
    sources = load_enterprise_sources()
    assert len(sources["services"]) >= 6
    assert sources["documents"][0].source_type == "markdown"


def test_build_sample_graph_has_core_domain_nodes():
    graph = build_sample_graph()
    assert graph.get_node("svc-provider-search").label == "Service"
    assert graph.get_node("topic-payment-events").label == "KafkaTopic"
    assert len(graph.relationships) > len(graph.nodes)


def test_ingestion_report_and_graph_summary_are_auditable():
    report = build_ingestion_report()
    assert report.node_count > 0
    assert report.relationship_count > 0
    assert all(stat.checksum for stat in report.source_stats)
    summary = summarize_graph(build_sample_graph())
    assert summary.node_labels["Service"] >= 6
    assert summary.relationship_types["DEPENDS_ON"] >= 1
