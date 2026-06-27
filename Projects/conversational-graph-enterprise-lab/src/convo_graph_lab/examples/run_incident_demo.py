from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.runner import GraphRunner


def main() -> None:
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    result = GraphRunner(graph, settings=settings).start("Investigate INC-1001 latency")
    print(result.final_output)


if __name__ == "__main__":
    main()
