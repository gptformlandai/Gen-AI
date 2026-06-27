from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


def test_graph_repository_finds_neighbors_and_paths():
    graph = build_sample_graph()
    neighbors = {node.id for node in graph.neighbors("svc-provider-search")}
    assert "svc-provider-db" in neighbors
    path, rels = graph.shortest_path("svc-mobile-app", "table-providers", max_depth=5)
    assert path[0] == "svc-mobile-app"
    assert path[-1] == "table-providers"
    assert rels
