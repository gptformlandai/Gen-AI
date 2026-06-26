from enterprise_ops_lab.agents.agent_factory import build_adk_or_local_agent_tree, build_all_agent_specs, resolve_tool_functions
from enterprise_ops_lab.config import Settings
from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.incident import IncidentRequest
from enterprise_ops_lab.sessions import state_keys
from enterprise_ops_lab.tools.tool_registry import build_default_tool_registry


def test_runtime_exercises_required_adk_concepts(tmp_path) -> None:
    settings = Settings(
        artifact_dir=tmp_path / "artifacts",
        trace_dir=tmp_path / "traces",
        session_dir=tmp_path / "sessions",
        memory_dir=tmp_path / "memory",
    )
    runner = EnterpriseOpsRunner(settings)

    response = runner.run(
        IncidentRequest(
            query="Investigate high latency in payments-api after last deployment.",
            session_id="coverage-session",
        )
    )

    trajectory = set(response.tool_trajectory)
    assert response.routed_agent == "investigation_workflow_agent"
    assert {"mcp.get_service_health", "mcp.get_recent_deployments", "mcp.get_error_rate", "mcp.get_oncall_owner"}.issubset(trajectory)
    assert {"workflow.router", "workflow.sequential_investigation", "workflow.parallel_diagnostics", "workflow.loop_refinement", "workflow.human_approval"}.issubset(trajectory)
    assert {"guardrail.input_check", "guardrail.output_check", "guardrail.tool_call_check"}.issubset(trajectory)
    assert response.hypothesis_refinements
    assert response.human_approval["approval"]["allowed"] is False
    assert response.artifact_path
    assert response.memory_note_id.startswith("mem-")
    assert response.metrics_snapshot["runner.completed"] == 1

    session = runner.session_service.get_or_create("coverage-session", "local-user")
    assert state_keys.REQUEST_HISTORY in session.state
    assert state_keys.LAST_TOOL_TRAJECTORY in session.state
    assert (settings.trace_dir / f"{response.request_id}.jsonl").exists()


def test_agent_specs_express_root_subagents_and_tools() -> None:
    specs = build_all_agent_specs(Settings())
    root = specs["root_incident_coordinator_agent"]

    assert "workflow.router" in root.tools
    assert "rag_runbook_agent" in root.sub_agents
    assert "mcp_operations_agent" in root.sub_agents
    assert "workflow.loop_refinement" in specs["investigation_workflow_agent"].tools
    assert resolve_tool_functions(["rag.search_runbooks", "workflow.router"])


def test_local_agent_tree_and_tool_registry_cover_workflow_surface() -> None:
    tree = build_adk_or_local_agent_tree(Settings())
    registry = build_default_tool_registry()
    tool_names = {item.name for item in registry.list_metadata()}

    assert "root_incident_coordinator_agent" in tree
    assert "workflow.router" in tool_names
    assert "workflow.parallel_diagnostics" in tool_names
    assert "workflow.loop_refinement" in tool_names
    assert "workflow.human_approval" in tool_names
