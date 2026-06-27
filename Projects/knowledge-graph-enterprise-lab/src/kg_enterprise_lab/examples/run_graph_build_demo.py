from kg_enterprise_lab.config import get_settings
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


def main() -> None:
    settings = get_settings()
    graph = build_sample_graph(settings)
    graph.save_json(settings.graph_state_path)
    print(f"saved {settings.graph_state_path}")


if __name__ == "__main__":
    main()
