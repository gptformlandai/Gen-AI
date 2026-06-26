from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ToolMetadata:
    name: str
    description: str
    category: str
    requires_approval: bool = False


class ToolRegistry:
    """Simple tool registry with metadata for governance and docs."""

    def __init__(self) -> None:
        self.tools: dict[str, Callable] = {}
        self.metadata: dict[str, ToolMetadata] = {}

    def register(self, name: str, fn: Callable, description: str, category: str, requires_approval: bool = False) -> None:
        self.tools[name] = fn
        self.metadata[name] = ToolMetadata(name, description, category, requires_approval)

    def get(self, name: str) -> Callable:
        return self.tools[name]

    def list_metadata(self) -> list[ToolMetadata]:
        return sorted(self.metadata.values(), key=lambda item: item.name)


def build_default_tool_registry() -> ToolRegistry:
    from enterprise_ops_lab.tools import artifact_tools, evaluation_tools, guardrail_tools, incident_tools, memory_tools, mcp_client_tools, rag_tools, remediation_tools
    from enterprise_ops_lab.workflows import loop_refinement, parallel_diagnostics, sequential_investigation
    from enterprise_ops_lab.workflows.escalation_checker import escalation_decision
    from enterprise_ops_lab.workflows.human_approval import require_human_approval
    from enterprise_ops_lab.workflows.router_workflow import route_intent

    registry = ToolRegistry()
    registry.register("guardrail.input_check", guardrail_tools.input_check, "Detect prompt injection and unsafe inputs.", "guardrail")
    registry.register("guardrail.output_check", guardrail_tools.output_check, "Validate response confidence and sensitive output.", "guardrail")
    registry.register("guardrail.tool_call_check", guardrail_tools.tool_call_check, "Block unsafe tool calls without approval.", "guardrail")
    registry.register("triage.classify_intent", incident_tools.classify_intent, "Classify enterprise operations intent.", "incident")
    registry.register("triage.extract_incident", incident_tools.extract_incident_fields, "Extract service, severity, symptoms, and domain.", "incident")
    registry.register("rag.search_runbooks", rag_tools.search_runbooks, "Search local runbooks with source grounding.", "rag")
    registry.register("mcp.get_service_health", mcp_client_tools.get_service_health, "Fetch service health through MCP.", "mcp")
    registry.register("mcp.get_recent_deployments", mcp_client_tools.get_recent_deployments, "Fetch deployments through MCP.", "mcp")
    registry.register("mcp.get_error_rate", mcp_client_tools.get_error_rate, "Fetch error rate through MCP.", "mcp")
    registry.register("mcp.get_oncall_owner", mcp_client_tools.get_oncall_owner, "Fetch on-call owner through MCP.", "mcp")
    registry.register("workflow.router", route_intent, "Route classified intent to a specialist agent.", "workflow")
    registry.register("workflow.sequential_investigation", sequential_investigation.run_sequential_investigation, "Run ordered incident diagnostics.", "workflow")
    registry.register("workflow.parallel_diagnostics", parallel_diagnostics.run_parallel_diagnostics, "Run parallel diagnostic fan-out branches.", "workflow")
    registry.register("workflow.loop_refinement", loop_refinement.refine_hypothesis, "Iteratively refine root-cause hypothesis.", "workflow")
    registry.register("workflow.human_approval", require_human_approval, "Simulate approval gate for risky operations.", "workflow", requires_approval=True)
    registry.register("workflow.escalation_check", escalation_decision, "Decide whether human escalation is required.", "workflow")
    registry.register("remediation.plan", remediation_tools.build_remediation_plan, "Generate a remediation plan.", "remediation")
    registry.register("artifact.save_report", artifact_tools.save_report_artifact, "Save markdown report artifact.", "artifact")
    registry.register("memory.add_resolution_note", memory_tools.add_resolution_note, "Store durable resolution note.", "memory")
    registry.register("memory.search_resolution_notes", memory_tools.search_resolution_notes, "Search durable memories.", "memory")
    registry.register("evaluation.evaluate_response", evaluation_tools.evaluate_response_quality, "Evaluate response and trajectory.", "evaluation")
    return registry
