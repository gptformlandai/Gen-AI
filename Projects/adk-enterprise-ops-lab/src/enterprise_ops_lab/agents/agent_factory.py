from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from enterprise_ops_lab.config import Settings


@dataclass(frozen=True)
class LocalAgentSpec:
    """Local mirror of an ADK Agent/LlmAgent definition for tests and docs."""

    name: str
    model: str
    instruction: str
    tools: list[str] = field(default_factory=list)
    sub_agents: list[str] = field(default_factory=list)


def create_adk_or_local_agent(spec: LocalAgentSpec, sub_agents: list[Any] | None = None) -> Any:
    """Create a real google.adk.Agent when installed, otherwise return a local spec."""
    try:
        from google.adk import Agent  # type: ignore

        kwargs = {
            "name": spec.name,
            "model": spec.model,
            "instruction": spec.instruction,
            "tools": resolve_tool_functions(spec.tools),
        }
        if sub_agents:
            kwargs["sub_agents"] = sub_agents
        try:
            return Agent(**kwargs)
        except TypeError:
            kwargs.pop("sub_agents", None)
            return Agent(**kwargs)
    except Exception:
        return spec


def build_adk_or_local_agent_tree(settings: Settings) -> dict[str, Any]:
    """Build leaf agents first, then root with specialist sub-agents.

    This is the closest local/offline representation of an ADK multi-agent tree.
    When `google-adk` is unavailable, callers receive `LocalAgentSpec` objects.
    """
    specs = build_all_agent_specs(settings)
    built: dict[str, Any] = {}
    for name, spec in specs.items():
        if name == "root_incident_coordinator_agent":
            continue
        built[name] = create_adk_or_local_agent(spec)
    root_spec = specs["root_incident_coordinator_agent"]
    root_sub_agents = [built[name] for name in root_spec.sub_agents if name in built]
    built[root_spec.name] = create_adk_or_local_agent(root_spec, sub_agents=root_sub_agents)
    return built


def resolve_tool_functions(tool_names: list[str]) -> list[Callable]:
    from enterprise_ops_lab.tools import artifact_tools, evaluation_tools, guardrail_tools, incident_tools, memory_tools, mcp_client_tools, rag_tools, remediation_tools
    from enterprise_ops_lab.workflows.escalation_checker import escalation_decision
    from enterprise_ops_lab.workflows.human_approval import require_human_approval
    from enterprise_ops_lab.workflows.loop_refinement import refine_hypothesis
    from enterprise_ops_lab.workflows.parallel_diagnostics import run_parallel_diagnostics
    from enterprise_ops_lab.workflows.router_workflow import route_intent
    from enterprise_ops_lab.workflows.sequential_investigation import run_sequential_investigation

    mapping: dict[str, Callable] = {
        "guardrail.input_check": guardrail_tools.input_check,
        "guardrail.output_check": guardrail_tools.output_check,
        "guardrail.tool_call_check": guardrail_tools.tool_call_check,
        "triage.classify_intent": incident_tools.classify_intent,
        "triage.extract_incident": incident_tools.extract_incident_fields,
        "rag.search_runbooks": rag_tools.search_runbooks,
        "mcp.get_service_health": mcp_client_tools.get_service_health,
        "mcp.get_recent_deployments": mcp_client_tools.get_recent_deployments,
        "mcp.get_error_rate": mcp_client_tools.get_error_rate,
        "mcp.get_oncall_owner": mcp_client_tools.get_oncall_owner,
        "workflow.router": route_intent,
        "workflow.sequential_investigation": run_sequential_investigation,
        "workflow.parallel_diagnostics": run_parallel_diagnostics,
        "workflow.loop_refinement": refine_hypothesis,
        "workflow.human_approval": require_human_approval,
        "workflow.escalation_check": escalation_decision,
        "remediation.plan": remediation_tools.build_remediation_plan,
        "artifact.save_report": artifact_tools.save_report_artifact,
        "memory.add_resolution_note": memory_tools.add_resolution_note,
        "memory.search_resolution_notes": memory_tools.search_resolution_notes,
        "evaluation.evaluate_response": evaluation_tools.evaluate_response_quality,
    }
    return [mapping[name] for name in tool_names if name in mapping]


def build_all_agent_specs(settings: Settings) -> dict[str, LocalAgentSpec]:
    from enterprise_ops_lab.prompts.artifact_report_prompt import ARTIFACT_REPORT_PROMPT
    from enterprise_ops_lab.prompts.evaluator_prompt import EVALUATOR_PROMPT
    from enterprise_ops_lab.prompts.guardrail_prompt import GUARDRAIL_PROMPT
    from enterprise_ops_lab.prompts.investigation_prompt import INVESTIGATION_PROMPT
    from enterprise_ops_lab.prompts.mcp_operations_prompt import MCP_OPERATIONS_PROMPT
    from enterprise_ops_lab.prompts.memory_prompt import MEMORY_PROMPT
    from enterprise_ops_lab.prompts.rag_runbook_prompt import RAG_RUNBOOK_PROMPT
    from enterprise_ops_lab.prompts.remediation_prompt import REMEDIATION_PROMPT
    from enterprise_ops_lab.prompts.root_prompt import ROOT_COORDINATOR_PROMPT
    from enterprise_ops_lab.prompts.triage_prompt import TRIAGE_PROMPT

    model = settings.model
    return {
        "root_incident_coordinator_agent": LocalAgentSpec(
            name="root_incident_coordinator_agent",
            model=model,
            instruction=ROOT_COORDINATOR_PROMPT,
            tools=["guardrail.input_check", "triage.classify_intent", "workflow.router"],
            sub_agents=[
                "rag_runbook_agent",
                "mcp_operations_agent",
                "incident_triage_agent",
                "investigation_workflow_agent",
                "remediation_planner_agent",
                "artifact_report_agent",
                "memory_learning_agent",
                "evaluator_agent",
                "guardrail_agent",
            ],
        ),
        "rag_runbook_agent": LocalAgentSpec("rag_runbook_agent", model, RAG_RUNBOOK_PROMPT, ["rag.search_runbooks"]),
        "mcp_operations_agent": LocalAgentSpec("mcp_operations_agent", model, MCP_OPERATIONS_PROMPT, ["mcp.get_service_health", "mcp.get_recent_deployments", "mcp.get_error_rate", "mcp.get_oncall_owner"]),
        "incident_triage_agent": LocalAgentSpec("incident_triage_agent", model, TRIAGE_PROMPT, ["triage.extract_incident"]),
        "investigation_workflow_agent": LocalAgentSpec(
            "investigation_workflow_agent",
            model,
            INVESTIGATION_PROMPT,
            [
                "workflow.sequential_investigation",
                "workflow.parallel_diagnostics",
                "workflow.loop_refinement",
                "workflow.human_approval",
                "workflow.escalation_check",
            ],
        ),
        "remediation_planner_agent": LocalAgentSpec("remediation_planner_agent", model, REMEDIATION_PROMPT, ["remediation.plan"]),
        "artifact_report_agent": LocalAgentSpec("artifact_report_agent", model, ARTIFACT_REPORT_PROMPT, ["artifact.save_report"]),
        "memory_learning_agent": LocalAgentSpec("memory_learning_agent", model, MEMORY_PROMPT, ["memory.add_resolution_note", "memory.search_resolution_notes"]),
        "evaluator_agent": LocalAgentSpec("evaluator_agent", model, EVALUATOR_PROMPT, ["evaluation.evaluate_response"]),
        "guardrail_agent": LocalAgentSpec("guardrail_agent", model, GUARDRAIL_PROMPT, ["guardrail.input_check", "guardrail.output_check", "guardrail.tool_call_check"]),
    }
