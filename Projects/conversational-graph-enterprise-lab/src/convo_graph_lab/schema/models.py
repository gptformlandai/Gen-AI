"""Typed contracts for graph definitions and execution."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class NodeStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    INTERRUPTED = "interrupted"
    WAITING = "waiting"
    TERMINAL = "terminal"


class ConversationTurn(BaseModel):
    role: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    session_id: str
    user_id: str = "anonymous"
    latest_input: str = ""
    slots: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    history: list[ConversationTurn] = Field(default_factory=list)
    short_term_memory: dict[str, Any] = Field(default_factory=dict)
    long_term_memory_refs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)

    def get_value(self, key: str, default: Any = None) -> Any:
        if key in self.slots:
            return self.slots[key]
        if key in self.variables:
            return self.variables[key]
        return getattr(self, key, default)

    def set_value(self, key: str, value: Any) -> None:
        if key in {"intent", "incident_id", "account_id", "approved"}:
            self.slots[key] = value
        else:
            self.variables[key] = value


class ConversationState(BaseModel):
    session_id: str
    graph_id: str
    current_node_id: str
    context: ConversationContext
    status: str = "running"
    step_count: int = 0
    visited_node_ids: list[str] = Field(default_factory=list)
    retry_counts: dict[str, int] = Field(default_factory=dict)
    interrupted_at: str | None = None


class StateSnapshot(BaseModel):
    id: str
    session_id: str
    node_id: str
    step_count: int
    status: str
    slots: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class NodeDefinition(BaseModel):
    id: str
    type: str
    name: str
    config: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EdgeDefinition(BaseModel):
    id: str
    source: str
    target: str
    condition: str = "always"
    priority: int = 100
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphDefinition(BaseModel):
    id: str
    name: str
    version: str = "1.0.0"
    start_node_id: str
    nodes: list[NodeDefinition]
    edges: list[EdgeDefinition]
    metadata: dict[str, Any] = Field(default_factory=dict)


class NodeResult(BaseModel):
    node_id: str
    status: NodeStatus
    output: str = ""
    updates: dict[str, Any] = Field(default_factory=dict)
    next_node_id: str | None = None
    error: str | None = None
    latency_ms: float = 0.0


class TraceEvent(BaseModel):
    session_id: str
    node_id: str
    node_type: str
    status: str
    selected_edge_id: str | None = None
    next_node_id: str | None = None
    input_snapshot: dict[str, Any] = Field(default_factory=dict)
    state_snapshot_id: str | None = None
    output: str = ""
    error: str | None = None
    latency_ms: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExecutionResult(BaseModel):
    state: ConversationState
    trace: list[TraceEvent]
    final_output: str
    path: list[str]


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class ToolSpec(BaseModel):
    name: str
    required_args: list[str] = Field(default_factory=list)
    optional_args: list[str] = Field(default_factory=list)
    description: str = ""


class GraphModelReport(BaseModel):
    graph_id: str
    node_count: int
    edge_count: int
    start_node_id: str
    terminal_node_ids: list[str]
    branching_node_ids: list[str]
    cycle_detected: bool
    node_type_counts: dict[str, int]
    pattern_coverage: dict[str, bool]


class MemoryRecord(BaseModel):
    id: str
    user_id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    score: float = 1.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EvalCase(BaseModel):
    id: str
    inputs: list[str]
    expected_path_contains: list[str] = Field(default_factory=list)
    expected_slots: dict[str, Any] = Field(default_factory=dict)


class EvalResult(BaseModel):
    case_id: str
    passed: bool
    score: float
    details: str


class EvalReport(BaseModel):
    suite: str
    results: list[EvalResult]
    pass_rate: float
