"""Conversational graph execution engine."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

from convo_graph_lab.agents.agent_registry import AgentRegistry, default_agent_registry
from convo_graph_lab.config import Settings, get_settings
from convo_graph_lab.graph_engine.graph import RuntimeGraph
from convo_graph_lab.graph_engine.state_store import InMemoryStateStore
from convo_graph_lab.memory.memory_store import MemorySystem
from convo_graph_lab.nodes.factory import NodeFactory
from convo_graph_lab.observability.metrics import Metrics
from convo_graph_lab.observability.tracing import TraceRecorder
from convo_graph_lab.schema.models import ConversationContext, ConversationState, ExecutionResult, NodeResult, NodeStatus, TraceEvent
from convo_graph_lab.tools.registry import ToolRegistry, default_tool_registry
from convo_graph_lab.transitions.resolver import TransitionResolver


@dataclass
class RuntimeServices:
    memory: MemorySystem = field(default_factory=MemorySystem)
    tools: ToolRegistry = field(default_factory=default_tool_registry)
    agents: AgentRegistry = field(default_factory=default_agent_registry)
    metrics: Metrics = field(default_factory=Metrics)


class GraphRunner:
    def __init__(
        self,
        graph: RuntimeGraph,
        settings: Settings | None = None,
        state_store: InMemoryStateStore | None = None,
        services: RuntimeServices | None = None,
        trace_recorder: TraceRecorder | None = None,
    ) -> None:
        self.graph = graph
        self.settings = settings or get_settings()
        self.state_store = state_store or InMemoryStateStore()
        self.services = services or RuntimeServices()
        self.trace_recorder = trace_recorder or TraceRecorder()
        self.node_factory = NodeFactory()
        self.resolver = TransitionResolver(graph.edges)

    def start(self, user_input: str, user_id: str = "anonymous", session_id: str | None = None) -> ExecutionResult:
        session_id = session_id or uuid.uuid4().hex[:12]
        context = ConversationContext(session_id=session_id, user_id=user_id, latest_input=user_input)
        state = ConversationState(session_id=session_id, graph_id=self.graph.definition.id, current_node_id=self.graph.definition.start_node_id, context=context)
        return self.run_until_stop(state)

    def send_input(self, session_id: str, user_input: str) -> ExecutionResult:
        state = self.state_store.require(session_id)
        state.context.latest_input = user_input
        state.context.variables["awaiting_input"] = False
        if state.status in {"waiting", "interrupted", "complete"}:
            state.current_node_id = self.graph.definition.start_node_id
            state.status = "running"
        return self.run_until_stop(state)

    def resume(self, session_id: str, updates: dict[str, object] | None = None) -> ExecutionResult:
        state = self.state_store.require(session_id)
        for key, value in (updates or {}).items():
            state.context.set_value(key, value)
        state.context.variables["awaiting_approval"] = False
        state.status = "running"
        if state.interrupted_at:
            state.current_node_id = state.interrupted_at
        return self.run_until_stop(state)

    def run_until_stop(self, state: ConversationState) -> ExecutionResult:
        local_trace: list[TraceEvent] = []
        while state.status == "running" and state.step_count < self.settings.max_steps:
            event = self._execute_one(state)
            local_trace.append(event)
            self.trace_recorder.record(event)
            if state.status in {"waiting", "interrupted", "complete", "failed"}:
                break
        if state.step_count >= self.settings.max_steps and state.status == "running":
            state.status = "failed"
            state.context.errors.append("Maximum graph steps exceeded")
        self.state_store.save(state)
        return ExecutionResult(state=state, trace=local_trace, final_output=state.context.outputs[-1] if state.context.outputs else "", path=state.visited_node_ids)

    def _execute_one(self, state: ConversationState) -> TraceEvent:
        node_definition = self.graph.get_node(state.current_node_id)
        node = self.node_factory.create(node_definition)
        start = time.perf_counter()
        try:
            result = node.run(state, self.services)
        except Exception as exc:  # pragma: no cover - defensive production boundary
            result = NodeResult(node_id=node_definition.id, status=NodeStatus.FAILED, error=str(exc), updates={"node_failed": True, "confidence": 0.0})
        latency_ms = round((time.perf_counter() - start) * 1000, 3)
        result.latency_ms = latency_ms
        if latency_ms > self.settings.node_timeout_ms:
            result.status = NodeStatus.FAILED
            result.error = f"Node timeout after {latency_ms}ms"
            result.updates["node_timeout"] = True
            state.context.errors.append(result.error)
        self.services.metrics.increment(f"node.{node_definition.type}.executed")
        if result.status == NodeStatus.FAILED:
            self.services.metrics.increment(f"node.{node_definition.type}.failed")
        self.services.metrics.latency(f"node.{node_definition.id}.latency_ms", latency_ms)
        for key, value in result.updates.items():
            state.context.set_value(key, value)
        state.visited_node_ids.append(node_definition.id)
        state.step_count += 1
        snapshot = self.state_store.snapshot(state, node_definition.id)

        selected_edge_id = None
        next_node_id = result.next_node_id
        if result.status == NodeStatus.TERMINAL:
            state.status = "complete"
        elif result.status == NodeStatus.INTERRUPTED:
            state.status = "interrupted"
        elif result.status == NodeStatus.WAITING and state.context.get_value("awaiting_input"):
            state.status = "waiting"
        else:
            edge = self.resolver.resolve(node_definition.id, state.context)
            if edge:
                selected_edge_id = edge.id
                next_node_id = result.next_node_id or edge.target
                state.current_node_id = next_node_id
            else:
                state.status = "complete"

        if result.status == NodeStatus.FAILED and not next_node_id:
            state.status = "failed"

        return TraceEvent(
            session_id=state.session_id,
            node_id=node_definition.id,
            node_type=node_definition.type,
            status=result.status.value,
            selected_edge_id=selected_edge_id,
            next_node_id=next_node_id,
            input_snapshot={"slots": dict(state.context.slots), "variables": dict(state.context.variables)},
            state_snapshot_id=snapshot.id,
            output=result.output,
            error=result.error,
            latency_ms=latency_ms,
        )
