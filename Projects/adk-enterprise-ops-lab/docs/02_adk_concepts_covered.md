# ADK Concepts Covered

| Concept | Project file |
|---|---|
| Agents / LlmAgent specs | `agents/agent_factory.py` |
| Root agent | `agents/root_incident_coordinator_agent.py` |
| Specialist sub-agents | `agents/*_agent.py` |
| Agent as tool pattern | agent modules expose `run()` functions |
| Function tools | `tools/*.py` |
| MCP tools | `mcp/`, `tools/mcp_client_tools.py` |
| Sessions | `sessions/session_manager.py` |
| Memory | `memory/memory_service.py` |
| Artifacts | `artifacts/artifact_service.py` |
| Workflows | `workflows/` |
| Callbacks | `callbacks/lifecycle_callbacks.py` |
| Evaluation | `evals/` |
| Observability | `observability/` |
| Guardrails | `guardrails/` |

## Extend It

Every concept has both a local implementation and a cloud replacement seam.

