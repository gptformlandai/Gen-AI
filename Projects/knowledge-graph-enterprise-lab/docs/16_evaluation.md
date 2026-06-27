# 16 Evaluation

## What It Is

Evaluation checks extraction, relationship extraction, query answers, GraphRAG grounding, and graph quality with golden test cases.

## Why It Matters

Graph quality decays unless you continuously test ingestion and answer behavior against expected cases.

## Where It Appears

- Eval cases: `data/eval/`
- Runner: `evaluation/evaluation_runner.py`
- Report: `evaluation/report_generator.py`
- Graph quality suite: `evaluation/graph_quality_eval.py`

## How To Run

```bash
kg-lab run-evals
```

## How To Extend

Add failed production questions as golden cases. Track precision, recall, answer grounding, and retrieval coverage over time.

## Common Mistakes

- Only testing happy-path queries.
- Not evaluating relationship direction.
- Scoring GraphRAG answers without checking citations.
