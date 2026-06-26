from __future__ import annotations

from uuid import uuid4

from enterprise_ops_lab.agents import artifact_report_agent, evaluator_agent, guardrail_agent, incident_triage_agent, memory_learning_agent, rag_runbook_agent, remediation_planner_agent
from enterprise_ops_lab.callbacks.lifecycle_callbacks import CallbackManager
from enterprise_ops_lab.config import Settings, get_settings
from enterprise_ops_lab.observability.logger import StructuredLogger
from enterprise_ops_lab.observability.metrics import MetricsRecorder
from enterprise_ops_lab.observability.tracing import TraceRecorder
from enterprise_ops_lab.schemas.incident import EvidenceItem, IncidentRequest, IncidentResponse, InvestigationTimelineItem, McpSummary
from enterprise_ops_lab.sessions.session_manager import InMemorySessionService
from enterprise_ops_lab.sessions import state_keys
from enterprise_ops_lab.tools import mcp_client_tools
from enterprise_ops_lab.workflows.escalation_checker import escalation_decision
from enterprise_ops_lab.workflows.human_approval import require_human_approval
from enterprise_ops_lab.workflows.loop_refinement import refine_hypothesis
from enterprise_ops_lab.workflows.parallel_diagnostics import run_parallel_diagnostics
from enterprise_ops_lab.workflows.router_workflow import route_intent
from enterprise_ops_lab.workflows.sequential_investigation import run_sequential_investigation


class EnterpriseOpsRunner:
    """Deterministic local runtime that mirrors the requested ADK agent trajectory."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.session_service = InMemorySessionService(self.settings.session_dir)
        self.logger = StructuredLogger(self.settings.trace_dir / "events.jsonl")
        self.tracer = TraceRecorder(self.settings.trace_dir)
        self.callbacks = CallbackManager(self.logger, self.tracer)
        self.metrics = MetricsRecorder()

    def run(self, request: IncidentRequest) -> IncidentResponse:
        request_id = request.request_id or f"req-{uuid4().hex[:8]}"
        session = self.session_service.get_or_create(request.session_id, request.user_id)
        history = list(session.state.get(state_keys.REQUEST_HISTORY, []))
        history.append({"request_id": request_id, "query": request.query})
        self.session_service.update(request.session_id, state_keys.REQUEST_HISTORY, history)
        trajectory: list[str] = []

        def agent_start(name: str) -> None:
            self.callbacks.before_agent(request_id, request.session_id, name)

        def agent_end(name: str) -> None:
            self.callbacks.after_agent(request_id, request.session_id, name)

        def call_tool(agent_name: str, tool_name: str, fn, *args, **kwargs):
            trajectory.append(tool_name)
            self.callbacks.before_tool(request_id, request.session_id, agent_name, tool_name)
            try:
                result = fn(*args, **kwargs)
                self.metrics.increment(f"tool.{tool_name}.ok")
                self.callbacks.after_tool(request_id, request.session_id, agent_name, tool_name)
                return result
            except Exception as exc:
                self.metrics.increment(f"tool.{tool_name}.error")
                self.callbacks.error(request_id, request.session_id, agent_name, str(exc))
                self.callbacks.after_tool(request_id, request.session_id, agent_name, tool_name, outcome="error")
                raise

        agent_start("guardrail_agent")
        guardrail = call_tool("guardrail_agent", "guardrail.input_check", guardrail_agent.check_input, request.query)
        self.callbacks.safety(request_id, request.session_id, "guardrail_agent", "allowed" if guardrail["ok"] else "blocked", guardrail["reason"])
        agent_end("guardrail_agent")
        if not guardrail["ok"]:
            raise ValueError(guardrail["reason"])

        agent_start("incident_triage_agent")
        triage = call_tool("incident_triage_agent", "triage.extract_incident", incident_triage_agent.run, guardrail["redacted_query"])
        agent_end("incident_triage_agent")

        routed_agent = call_tool("root_incident_coordinator_agent", "workflow.router", route_intent, triage.intent)

        agent_start("rag_runbook_agent")
        rag_payload = call_tool("rag_runbook_agent", "rag.search_runbooks", rag_runbook_agent.run, guardrail["redacted_query"], triage.service)
        evidence = [EvidenceItem.model_validate(item) for item in rag_payload["evidence"]]
        agent_end("rag_runbook_agent")

        agent_start("mcp_operations_agent")
        health = call_tool("mcp_operations_agent", "mcp.get_service_health", mcp_client_tools.get_service_health, triage.service)["data"]
        deployments = call_tool("mcp_operations_agent", "mcp.get_recent_deployments", mcp_client_tools.get_recent_deployments, triage.service)["data"]
        errors = call_tool("mcp_operations_agent", "mcp.get_error_rate", mcp_client_tools.get_error_rate, triage.service)["data"]
        oncall = call_tool("mcp_operations_agent", "mcp.get_oncall_owner", mcp_client_tools.get_oncall_owner, triage.service)["data"]
        mcp = McpSummary(
            service_health=health["health"],
            error_rate=float(errors["error_rate"]),
            recent_deployments=list(deployments["deployments"]),
            oncall_owner=oncall["oncall_owner"],
        )
        agent_end("mcp_operations_agent")

        agent_start("memory_learning_agent")
        memory_hits = call_tool("memory_learning_agent", "memory.search_resolution_notes", memory_learning_agent.recall, request.query, triage.service, str(self.settings.memory_dir))
        agent_end("memory_learning_agent")

        agent_start("investigation_workflow_agent")
        sequential = call_tool("investigation_workflow_agent", "workflow.sequential_investigation", run_sequential_investigation, triage.service, triage.symptoms, mcp)
        parallel = call_tool("investigation_workflow_agent", "workflow.parallel_diagnostics", run_parallel_diagnostics, triage.service, triage.symptoms)
        timeline = sequential + parallel
        agent_end("investigation_workflow_agent")

        agent_start("remediation_planner_agent")
        plan = call_tool("remediation_planner_agent", "remediation.plan", remediation_planner_agent.run, triage.service, triage.symptoms, evidence, mcp, triage.confidence)
        agent_end("remediation_planner_agent")

        evidence_terms = [item.title for item in evidence[:2]] + [mcp.service_health, *mcp.recent_deployments[:1]]
        hypothesis_refinements = call_tool("investigation_workflow_agent", "workflow.loop_refinement", refine_hypothesis, plan.likely_root_cause, evidence_terms)

        approval_action = "rollback_deployment" if plan.rollback_recommended else "diagnostic_read_only"
        tool_guard = call_tool("guardrail_agent", "guardrail.tool_call_check", guardrail_agent.check_tool, approval_action, False)
        human_approval = call_tool("investigation_workflow_agent", "workflow.human_approval", require_human_approval, approval_action, False)
        timeline.append(
            InvestigationTimelineItem(
                step="human_approval",
                outcome=human_approval["reason"],
                latency_ms=10,
                evidence_refs=[approval_action],
            )
        )

        escalation = call_tool("investigation_workflow_agent", "workflow.escalation_check", escalation_decision, plan.confidence, triage.severity, plan.human_approval_required, self.settings.confidence_threshold)
        final_answer = build_final_answer(triage.service, plan.likely_root_cause, plan.recommended_actions, rag_payload["sources"], memory_hits, mcp, evidence)
        output_guard = call_tool("guardrail_agent", "guardrail.output_check", guardrail_agent.check_output, final_answer, plan.confidence)
        self.callbacks.safety(request_id, request.session_id, "guardrail_agent", "allowed" if output_guard["ok"] else "blocked", output_guard["reason"])

        response_dict = {
            "request_id": request_id,
            "session_id": request.session_id,
            "routed_agent": routed_agent,
            "triage": triage.model_dump(mode="json"),
            "likely_root_cause": plan.likely_root_cause,
            "evidence": [item.model_dump(mode="json") for item in evidence],
            "runbook_references": rag_payload["sources"],
            "mcp_data_summary": mcp.model_dump(mode="json"),
            "investigation_timeline": [item.model_dump(mode="json") for item in timeline],
            "hypothesis_refinements": hypothesis_refinements,
            "recommended_remediation": plan.model_dump(mode="json"),
            "human_approval": {"tool_guard": tool_guard, "approval": human_approval},
            "escalation_decision": escalation,
            "artifact_path": "",
            "memory_note_id": "",
            "evaluation_summary": {},
            "metrics_snapshot": {},
            "tool_trajectory": trajectory,
            "final_answer": final_answer,
        }

        agent_start("artifact_report_agent")
        artifact = call_tool("artifact_report_agent", "artifact.save_report", artifact_report_agent.run, response_dict, str(self.settings.artifact_dir))
        response_dict["artifact_path"] = artifact["path"]
        agent_end("artifact_report_agent")

        agent_start("memory_learning_agent")
        memory_note = call_tool(
            "memory_learning_agent",
            "memory.add_resolution_note",
            memory_learning_agent.remember,
            f"{triage.service}: {plan.likely_root_cause}; actions: {'; '.join(plan.recommended_actions)}",
            triage.service,
            str(self.settings.memory_dir),
        )
        response_dict["memory_note_id"] = memory_note["memory_id"]
        agent_end("memory_learning_agent")

        agent_start("evaluator_agent")
        evaluation = call_tool(
            "evaluator_agent",
            "evaluation.evaluate_response",
            evaluator_agent.run,
            response_dict,
            ["latency" if "latency" in request.query.lower() else triage.service.split("-")[0]],
            ["rag.search_runbooks", "mcp.get_service_health", "artifact.save_report"],
        )
        response_dict["evaluation_summary"] = evaluation
        agent_end("evaluator_agent")

        self.metrics.increment("runner.completed")
        response_dict["metrics_snapshot"] = self.metrics.snapshot()
        response = IncidentResponse.model_validate(response_dict)
        self.session_service.update(request.session_id, state_keys.LAST_TRIAGE, triage.model_dump(mode="json"))
        self.session_service.update(request.session_id, state_keys.LAST_TOOL_TRAJECTORY, trajectory)
        self.session_service.update(request.session_id, state_keys.INVESTIGATION_CONTEXT, {"service": triage.service, "timeline": response_dict["investigation_timeline"]})
        self.session_service.update(request.session_id, state_keys.LAST_ARTIFACT, artifact["path"])
        return response


def build_final_answer(service: str, root_cause: str, actions: list[str], sources: list[str], memory_hits: list[dict], mcp: McpSummary, evidence: list[EvidenceItem]) -> str:
    memory_line = "No previous memory matched."
    if memory_hits:
        memory_line = f"Relevant memory: {memory_hits[0]['text']}"
    evidence_line = "No runbook excerpt available."
    if evidence:
        evidence_line = f"Top runbook evidence: {evidence[0].quote[:220]}"
    return (
        f"{service} investigation suggests: {root_cause} "
        f"MCP health is {mcp.service_health}; error rate is {mcp.error_rate} percent. "
        f"{evidence_line} "
        f"Recommended remediation: {'; '.join(actions)}. "
        f"Runbook sources: {', '.join(sources) or 'none'}. {memory_line}"
    )
