from enterprise_ops_lab.agents.mcp_operations_agent import run as run_mcp
from enterprise_ops_lab.workflows.parallel_diagnostics import run_parallel_diagnostics
from enterprise_ops_lab.workflows.sequential_investigation import run_sequential_investigation


def test_workflows_produce_sequential_and_parallel_steps() -> None:
    mcp = run_mcp("shared-postgres")
    sequential = run_sequential_investigation("shared-postgres", ["database"], mcp)
    parallel = run_parallel_diagnostics("shared-postgres", ["database"])

    assert [step.step for step in sequential][:2] == ["check_service_health", "inspect_recent_deployments"]
    assert any(step.step == "database_branch" for step in parallel)

