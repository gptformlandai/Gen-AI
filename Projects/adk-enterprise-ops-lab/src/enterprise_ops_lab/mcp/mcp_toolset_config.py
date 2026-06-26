from __future__ import annotations


MCP_TOOLSET_CONFIG = {
    "transport": "stdio",
    "command": "python",
    "args": ["-m", "enterprise_ops_lab.mcp.mock_mcp_server"],
    "tools": ["get_service_health", "get_recent_deployments", "get_error_rate", "get_oncall_owner"],
    "timeout_ms": 1200,
}


ADK_MCP_TOOLSET_SNIPPET = """
from google.adk.tools.mcp_toolset import MCPToolset, StdioServerParameters

operations_mcp_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command="python",
        args=["-m", "enterprise_ops_lab.mcp.mock_mcp_server"],
    )
)
"""

