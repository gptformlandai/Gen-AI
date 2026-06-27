from convo_graph_lab.config import get_settings
from convo_graph_lab.evals.runner import run_evaluations
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.visualization.exporters import export_graph_json, export_graph_mermaid


def test_visualization_exports_graph_and_eval_passes():
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    mermaid = export_graph_mermaid(graph.definition)
    assert "flowchart" in mermaid
    graph_json = export_graph_json(graph.definition)
    assert graph_json["nodes"]
    report = run_evaluations(settings)
    assert report.pass_rate == 1.0
