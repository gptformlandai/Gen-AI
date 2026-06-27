"""Typed tool registry with deterministic enterprise mock tools."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from convo_graph_lab.schema.models import ToolCall, ToolResult, ToolSpec


ToolHandler = Callable[[dict[str, Any]], ToolResult]


@dataclass
class ToolRegistry:
    tools: dict[str, ToolHandler] = field(default_factory=dict)
    specs: dict[str, ToolSpec] = field(default_factory=dict)

    def register(self, name: str, handler: ToolHandler, spec: ToolSpec | None = None) -> None:
        self.tools[name] = handler
        self.specs[name] = spec or ToolSpec(name=name)

    def invoke(self, call: ToolCall) -> ToolResult:
        handler = self.tools.get(call.tool_name)
        if not handler:
            return ToolResult(tool_name=call.tool_name, success=False, error=f"Unknown tool: {call.tool_name}")
        spec = self.specs.get(call.tool_name, ToolSpec(name=call.tool_name))
        missing = [arg for arg in spec.required_args if call.arguments.get(arg) in {None, ""}]
        if missing:
            return ToolResult(tool_name=call.tool_name, success=False, error=f"Missing required tool args: {', '.join(missing)}")
        try:
            return handler(call.arguments)
        except Exception as exc:  # pragma: no cover - defensive production boundary
            return ToolResult(tool_name=call.tool_name, success=False, error=str(exc))


def default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("search_tool", search_tool, ToolSpec(name="search_tool", required_args=["query"], description="Search internal runbooks and docs."))
    registry.register("incident_lookup_tool", incident_lookup_tool, ToolSpec(name="incident_lookup_tool", required_args=["incident_id"], description="Lookup incident metadata."))
    registry.register("user_profile_tool", user_profile_tool, ToolSpec(name="user_profile_tool", optional_args=["user_id", "account_id"], description="Load enterprise user profile."))
    registry.register("graph_query_tool", graph_query_tool, ToolSpec(name="graph_query_tool", required_args=["query"], description="Run a dependency graph query."))
    return registry


def search_tool(arguments: dict[str, Any]) -> ToolResult:
    query = str(arguments.get("query", ""))
    if "force_fail" in query:
        return ToolResult(tool_name="search_tool", success=False, error="Simulated search failure")
    hits = [
        {"title": "Provider Search Latency Runbook", "snippet": "Check provider-db locks, topic lag, cache warmup."},
        {"title": "Conversation Graph Debugging", "snippet": "Inspect trace, selected edge, state snapshots, retry counts."},
    ]
    return ToolResult(tool_name="search_tool", success=True, output={"query": query, "hits": hits})


def incident_lookup_tool(arguments: dict[str, Any]) -> ToolResult:
    incident_id = str(arguments.get("incident_id") or "INC-1001")
    incidents = {
        "INC-1001": {
            "severity": "SEV2",
            "service": "provider-search-service",
            "owner": "Provider Platform",
            "summary": "Provider search latency caused by provider-db lock contention.",
        },
        "INC-1002": {
            "severity": "SEV1",
            "service": "payments-api",
            "owner": "Payments",
            "summary": "Payments timeout due to notification retry storm.",
        },
    }
    incident = incidents.get(incident_id)
    if not incident:
        return ToolResult(tool_name="incident_lookup_tool", success=False, error=f"Incident not found: {incident_id}")
    return ToolResult(tool_name="incident_lookup_tool", success=True, output={"incident_id": incident_id, **incident})


def user_profile_tool(arguments: dict[str, Any]) -> ToolResult:
    user_id = str(arguments.get("user_id") or arguments.get("account_id") or "anonymous")
    return ToolResult(
        tool_name="user_profile_tool",
        success=True,
        output={"user_id": user_id, "tier": "enterprise", "region": "us-east", "eligible_for_self_service": True},
    )


def graph_query_tool(arguments: dict[str, Any]) -> ToolResult:
    query = str(arguments.get("query", ""))
    return ToolResult(
        tool_name="graph_query_tool",
        success=True,
        output={
            "query": query,
            "answer": "provider-search-service depends on provider-db and is owned by Provider Platform.",
            "path": ["provider-search-service", "provider-db", "Provider Platform"],
        },
    )
