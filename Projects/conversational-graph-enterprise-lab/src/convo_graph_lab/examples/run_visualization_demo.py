from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.visualization.exporters import export_graph_mermaid


def main() -> None:
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    print(export_graph_mermaid(graph.definition))


if __name__ == "__main__":
    main()
