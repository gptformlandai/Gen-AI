from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.visualization.visualization_service import VisualizationService


def main() -> None:
    graph = build_sample_graph()
    print(VisualizationService(graph).export(fmt="mermaid", view="blast-radius", anchor_name="payments-api"))


if __name__ == "__main__":
    main()
