# Artifacts

## What It Is

Versioned markdown incident reports and metadata saved after investigation.

## Where It Appears

- `artifacts/artifact_service.py`
- `agents/artifact_report_agent.py`
- `tools/artifact_tools.py`

## Why It Matters

Incident reports are durable outputs, not conversational text.

## Extend It

Replace `LocalArtifactService` with a GCS-backed implementation and add retention policies.

