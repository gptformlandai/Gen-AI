from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.runner import GraphRunner


def main() -> None:
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    runner = GraphRunner(graph, settings=settings)
    first = runner.start("Escalate billing support to human", session_id="resume-demo")
    print(first.state.status)
    resumed = runner.resume("resume-demo", {"approved": True})
    print(resumed.state.status)


if __name__ == "__main__":
    main()
