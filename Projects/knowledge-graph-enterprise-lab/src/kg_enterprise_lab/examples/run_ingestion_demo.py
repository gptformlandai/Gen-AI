from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


def main() -> None:
    graph = build_sample_graph()
    print({"nodes": len(graph.nodes), "relationships": len(graph.relationships)})


if __name__ == "__main__":
    main()
