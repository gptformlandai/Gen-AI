from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.schemas.query import QueryRequest


def main() -> None:
    graph = build_sample_graph()
    response = GraphQueryService(graph).answer(QueryRequest(question="What services depend on provider-search-service?"))
    print(response.answer)


if __name__ == "__main__":
    main()
