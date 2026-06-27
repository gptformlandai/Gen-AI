from pathlib import Path

from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.modeling import build_graph_model_report
from convo_graph_lab.graph_engine.validator import validate_graph_definition
from convo_graph_lab.schema.models import NodeDefinition


def test_graph_compiles_with_no_errors_and_detects_cycle_info():
    settings = get_settings()
    graph, issues = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    assert graph.definition.start_node_id == "input"
    assert not [issue for issue in issues if issue.severity == "error"]
    assert any(issue.code == "cycle_detected" for issue in issues)
    assert validate_graph_definition(graph.definition)


def test_graph_model_report_and_node_config_validation():
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    report = build_graph_model_report(graph.definition)
    assert report.branching_node_ids
    assert report.pattern_coverage["clarification_loop"]
    broken = graph.definition.model_copy(
        update={
            "nodes": graph.definition.nodes + [NodeDefinition(id="bad_tool", type="ToolNode", name="Bad tool")],
            "edges": graph.definition.edges,
        }
    )
    issues = validate_graph_definition(broken)
    assert any(issue.code == "missing_tool_config" for issue in issues)
