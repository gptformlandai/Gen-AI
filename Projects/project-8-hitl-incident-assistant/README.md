# Project 8: Long-Lived Human-In-The-Loop Incident Assistant

This project implements a **long-running incident assistant** with an explicit human-review boundary.

The assistant can triage an incident report, execute safe diagnostic actions, pause before unsafe production actions, persist state to disk, resume after approval or rejection, and record a durable event log.

## Why This Fits Project 8

Project 8 asks for a system that is multimodal, long-lived, or human-in-the-loop. This project chooses the **human-in-the-loop plus long-lived workflow** path.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| One clear human-review boundary | State-changing actions such as rollback, restart, scale, and status-page update require approval. |
| Long-lived state or resumable workflow | `storage.py` persists incident state as JSON and the CLI can resume by `incident_id`. |
| Failure-mode list for latency, ambiguity, and unsafe actions | `docs/failure_log.md` documents the specific failure modes and mitigations. |
| Evaluation rubric suited to chosen modality | `docs/evaluation_rubric.md` evaluates approval gates, resumability, ambiguity handling, and latency budgets. |
| System demo or workflow run-through | `hitl-incident demo` writes a pending, approved, and resolved workflow trace. |
| Operational boundary definition | `docs/operational_boundaries.md` defines what the assistant can and cannot do. |

## Architecture

```text
incident report
    |
    v
ambiguity check
    |-- incomplete report --> needs_clarification
    |
    v
severity assessment
    |
    v
action planner
    |
    |-- safe diagnostics ---------> execute immediately
    |
    |-- unsafe remediation -------> wait for human approval
    |
    v
persisted incident state + event log
    |
    v
resume after approval, rejection, or new observation
```

## Run Locally

```bash
cd Projects/project-8-hitl-incident-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Start an incident that pauses for approval:

```bash
hitl-incident start \
  --summary "Checkout is down after the latest production deploy" \
  --service checkout \
  --environment production \
  --impact "Customers cannot complete purchases" \
  --signal "HTTP 500 rate is 38 percent" \
  --requester "ops@example.com"
```

Approve all pending actions:

```bash
hitl-incident approve \
  --incident-id <incident_id> \
  --actor "incident-commander@example.com"
```

Generate the demo artifacts:

```bash
hitl-incident demo --output docs/demo_runthrough.md --state-dir docs/demo_states
```

Evaluate the workflow:

```bash
hitl-incident evaluate \
  --cases data/evaluation_cases.json \
  --output docs/evaluation_results.md
```

## Tests

```bash
pytest
```

The implementation is deterministic and does not require an API key.

