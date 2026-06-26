from __future__ import annotations

from time import perf_counter

from enterprise_ops_lab.observability.logger import StructuredLogger
from enterprise_ops_lab.observability.tracing import TraceRecorder


class CallbackManager:
    """ADK-style lifecycle callback facade for agents and tools."""

    def __init__(self, logger: StructuredLogger, tracer: TraceRecorder) -> None:
        self.logger = logger
        self.tracer = tracer
        self._starts: dict[str, float] = {}

    def before_agent(self, request_id: str, session_id: str, agent_name: str) -> None:
        self._starts[f"agent:{agent_name}"] = perf_counter()
        self._record(request_id, "before_agent", session_id=session_id, agent_name=agent_name)

    def after_agent(self, request_id: str, session_id: str, agent_name: str, outcome: str = "ok") -> None:
        latency = self._latency(f"agent:{agent_name}")
        self._record(request_id, "after_agent", session_id=session_id, agent_name=agent_name, outcome=outcome, latency_ms=latency)

    def before_tool(self, request_id: str, session_id: str, agent_name: str, tool_name: str) -> None:
        self._starts[f"tool:{tool_name}"] = perf_counter()
        self._record(request_id, "before_tool", session_id=session_id, agent_name=agent_name, tool_name=tool_name)

    def after_tool(self, request_id: str, session_id: str, agent_name: str, tool_name: str, outcome: str = "ok") -> None:
        latency = self._latency(f"tool:{tool_name}")
        self._record(request_id, "after_tool", session_id=session_id, agent_name=agent_name, tool_name=tool_name, outcome=outcome, latency_ms=latency)

    def error(self, request_id: str, session_id: str, agent_name: str, error: str) -> None:
        self._record(request_id, "error", session_id=session_id, agent_name=agent_name, outcome="error", error=error)

    def safety(self, request_id: str, session_id: str, agent_name: str, outcome: str, reason: str) -> None:
        self._record(request_id, "safety", session_id=session_id, agent_name=agent_name, outcome=outcome, reason=reason)

    def _latency(self, key: str) -> int:
        start = self._starts.pop(key, perf_counter())
        return int((perf_counter() - start) * 1000)

    def _record(self, request_id: str, event_type: str, **fields: object) -> None:
        event = self.logger.event(event_type, request_id=request_id, **fields)
        self.tracer.record(request_id, event)

