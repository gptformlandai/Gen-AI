# Troubleshooting

## ADK Import Fails

Install optional dependency:

```bash
python -m pip install -e ".[adk]"
```

## FastAPI Import Fails

Install:

```bash
python -m pip install -e ".[api]"
```

## RAG Returns Weak Evidence

Check runbook metadata, chunk size, and query expansion. Add a `rag_grounding_cases.json` case.

## Tool Trajectory Eval Fails

Inspect `.traces/<request_id>.jsonl` and compare against `data/eval/trajectory_cases.json`.

## Artifact Missing

Check `OPS_LAB_ARTIFACT_DIR` and filesystem permissions.

