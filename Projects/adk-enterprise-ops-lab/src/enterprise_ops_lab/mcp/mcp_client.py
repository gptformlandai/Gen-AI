from __future__ import annotations

from enterprise_ops_lab.mcp.mock_mcp_server import handle_tool
from enterprise_ops_lab.schemas.tool_result import ToolResult


class MockMcpClient:
    """Local MCP client facade shaped like an ADK MCP toolset integration."""

    def __init__(self, timeout_ms: int = 1200) -> None:
        self.timeout_ms = timeout_ms

    def call(self, tool_name: str, service: str) -> ToolResult:
        try:
            data = handle_tool(tool_name, service)
            return ToolResult(tool_name=f"mcp.{tool_name}", ok=True, data=data, latency_ms=min(80, self.timeout_ms))
        except Exception as exc:
            return ToolResult(tool_name=f"mcp.{tool_name}", ok=False, error=str(exc), latency_ms=self.timeout_ms)

    def get_service_health(self, service: str) -> ToolResult:
        return self.call("get_service_health", service)

    def get_recent_deployments(self, service: str) -> ToolResult:
        return self.call("get_recent_deployments", service)

    def get_error_rate(self, service: str) -> ToolResult:
        return self.call("get_error_rate", service)

    def get_oncall_owner(self, service: str) -> ToolResult:
        return self.call("get_oncall_owner", service)

