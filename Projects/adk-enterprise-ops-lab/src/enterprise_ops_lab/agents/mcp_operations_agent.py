from __future__ import annotations

from enterprise_ops_lab.schemas.incident import McpSummary
from enterprise_ops_lab.tools import mcp_client_tools


def run(service: str) -> McpSummary:
    """Specialist MCP operations agent behavior."""
    health = mcp_client_tools.get_service_health(service)["data"]
    deployments = mcp_client_tools.get_recent_deployments(service)["data"]
    error_rate = mcp_client_tools.get_error_rate(service)["data"]
    oncall = mcp_client_tools.get_oncall_owner(service)["data"]
    return McpSummary(
        service_health=health["health"],
        error_rate=float(error_rate["error_rate"]),
        recent_deployments=list(deployments["deployments"]),
        oncall_owner=oncall["oncall_owner"],
    )

