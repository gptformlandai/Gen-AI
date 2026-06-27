from kg_enterprise_lab.algorithms.centrality import highest_dependency_centrality
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


def main() -> None:
    graph = build_sample_graph()
    print(highest_dependency_centrality(graph))


if __name__ == "__main__":
    main()
