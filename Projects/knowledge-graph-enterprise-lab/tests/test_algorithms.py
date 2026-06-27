from kg_enterprise_lab.algorithms.blast_radius import blast_radius
from kg_enterprise_lab.algorithms.centrality import highest_dependency_centrality
from kg_enterprise_lab.algorithms.connected_components import connected_components
from kg_enterprise_lab.algorithms.cycle_detection import detect_cycles
from kg_enterprise_lab.algorithms.pagerank import pagerank
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


def test_algorithms_cover_impact_and_criticality():
    graph = build_sample_graph()
    nodes, _ = blast_radius(graph, "svc-payments-api")
    assert "svc-mobile-app" in nodes
    assert highest_dependency_centrality(graph) is not None
    assert "svc-provider-search" in pagerank(graph, {"DEPENDS_ON", "CALLS"})
    assert connected_components(graph)
    assert isinstance(detect_cycles(graph), list)
