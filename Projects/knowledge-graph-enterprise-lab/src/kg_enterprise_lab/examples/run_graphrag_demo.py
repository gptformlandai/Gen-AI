from kg_enterprise_lab.graphrag.graphrag_pipeline import GraphRAGPipeline
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest


def main() -> None:
    graph = build_sample_graph()
    response = GraphRAGPipeline(graph).run(GraphRAGRequest(question="Use GraphRAG to explain why provider-search-service may be slow."))
    print(response.answer)


if __name__ == "__main__":
    main()
