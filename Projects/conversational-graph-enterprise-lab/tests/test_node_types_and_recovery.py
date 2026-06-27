from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.runner import GraphRunner


def test_retry_and_fallback_path_for_tool_failure():
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    runner = GraphRunner(graph, settings=settings)
    result = runner.start("Search docs force_fail", session_id="retry-case")
    assert "retry_tool" in result.path
    assert "fallback" in result.path
    assert result.state.context.variables["fallback_used"] is True
