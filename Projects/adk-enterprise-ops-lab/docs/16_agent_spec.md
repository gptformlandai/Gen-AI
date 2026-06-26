# Agent Spec

| Agent | Responsibility | Tools |
|---|---|---|
| root_incident_coordinator_agent | Route and coordinate end-to-end incident flow | guardrail, triage |
| rag_runbook_agent | Retrieve runbook evidence | `rag.search_runbooks` |
| mcp_operations_agent | Fetch operational signals | `mcp.*` |
| incident_triage_agent | Extract structured incident fields | `triage.extract_incident` |
| investigation_workflow_agent | Run deterministic workflows | `workflow.*` |
| remediation_planner_agent | Build remediation plan | `remediation.plan` |
| artifact_report_agent | Save reports | `artifact.save_report` |
| memory_learning_agent | Store and search memories | `memory.*` |
| evaluator_agent | Run quality and trajectory checks | `evaluation.evaluate_response` |
| guardrail_agent | Enforce safety constraints | `guardrail.*` |

