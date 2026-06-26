# Evaluation

## What It Is

Golden response tests, tool trajectory tests, and RAG grounding tests.

## Where It Appears

- `data/eval/`
- `evals/evaluation_runner.py`
- `evals/golden_eval.py`
- `evals/trajectory_eval.py`
- `evals/rag_eval.py`

## Why It Matters

Agent behavior should be regression-tested before deployment.

## Add A Case

Add JSON to `data/eval/*.json`, then run:

```bash
python -m enterprise_ops_lab.evals.evaluation_runner
```

