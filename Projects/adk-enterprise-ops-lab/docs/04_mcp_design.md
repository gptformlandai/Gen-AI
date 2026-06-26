# MCP Design

## What It Is

The agent consumes mock MCP tools for service health, deployments, error rate, and on-call ownership. It also includes an example of exposing local ADK-style tools as MCP tools.

## Where It Appears

- `mcp/mock_mcp_server.py`
- `mcp/mcp_client.py`
- `mcp/mcp_toolset_config.py`
- `mcp/expose_adk_tools_server.py`

## Why It Matters

MCP separates operational capability boundaries from agent reasoning.

## Extend It

Replace `MockMcpClient` with ADK `MCPToolset` configuration and remote MCP server connection details.

