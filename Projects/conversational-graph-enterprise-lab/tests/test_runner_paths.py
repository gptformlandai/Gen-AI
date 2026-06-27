from convo_graph_lab.config import get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.file_state_store import FileStateStore
from convo_graph_lab.graph_engine.runner import GraphRunner
from convo_graph_lab.observability.debugger import build_debug_report


def make_runner():
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    return GraphRunner(graph, settings=settings)


def test_incident_flow_runs_tool_memory_decision_summary():
    runner = make_runner()
    result = runner.start("Investigate INC-1001 latency", user_id="u1", session_id="s1")
    assert result.state.status == "complete"
    assert result.state.context.slots["intent"] == "incident"
    assert result.state.context.slots["incident_id"] == "INC-1001"
    assert "incident_lookup" in result.path
    assert "memory_write" in result.path
    assert result.trace
    snapshots = runner.state_store.get_snapshots("s1")
    assert snapshots
    assert result.trace[0].state_snapshot_id == snapshots[0].id
    debug = build_debug_report(result.state, result.trace, snapshots)
    assert debug["detected_patterns"]["intent_detection_flow"]


def test_clarification_loop_waits_then_resumes_with_new_input():
    runner = make_runner()
    first = runner.start("help", user_id="u2", session_id="s2")
    assert first.state.status == "waiting"
    assert "clarify" in first.path
    assert "collect_slot" in first.path
    second = runner.send_input("s2", "account unlock user-101")
    assert second.state.status == "complete"
    assert second.state.context.slots["intent"] == "workflow"
    assert "workflow_agent" in second.path


def test_developer_tool_flow_and_metrics():
    runner = make_runner()
    result = runner.start("Search docs for provider-search-service timeout", user_id="u3", session_id="s3")
    assert result.state.status == "complete"
    assert "developer_agent" in result.path
    assert "search" in result.path
    assert runner.services.metrics.snapshot()["counters"]["node.ToolNode.executed"] >= 1


def test_human_handoff_interrupt_and_resume():
    runner = make_runner()
    first = runner.start("Escalate billing support to human", user_id="u4", session_id="s4")
    assert first.state.status == "interrupted"
    assert "human_approval" in first.path
    resumed = runner.resume("s4", {"approved": True})
    assert resumed.state.status == "complete"
    assert resumed.path[-1] == "end"


def test_file_state_store_supports_resume_across_runner_instances(tmp_path):
    settings = get_settings()
    graph, _ = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    first_runner = GraphRunner(graph, settings=settings, state_store=FileStateStore(tmp_path))
    first = first_runner.start("help", session_id="file-session")
    assert first.state.status == "waiting"
    second_runner = GraphRunner(graph, settings=settings, state_store=FileStateStore(tmp_path))
    second = second_runner.send_input("file-session", "account unlock user-101")
    assert second.state.status == "complete"
    assert second.state.context.slots["intent"] == "workflow"
