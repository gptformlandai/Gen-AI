# Project 4: Advanced RAG With Reranking And Guardrails

This project upgrades the Project 3 baseline RAG assistant with retrieval engineering and safety controls.

The goal is not to make a prettier answer. The goal is to improve the system by layer:

- rewrite the user query into multiple retrieval queries;
- retrieve more candidates;
- rerank candidates with query-intent features;
- apply safety and permission guardrails;
- compare advanced behavior against a baseline on the same evaluation set.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| Query rewriting or multi-query retrieval | `query_rewriting.py` creates query variants for ambiguous or under-specified search phrasing. |
| Reranking layer | `reranking.py` scores candidates using vector score, lexical overlap, topic intent, and phrase matches. |
| Guardrails or approval logic | `guardrails.py` blocks unsafe requests and role-restricted audit/admin requests. |
| Baseline vs advanced failure analysis | `evaluation.py` runs both systems and writes a side-by-side comparison. |
| Permission-aware or safety-aware refusal | `AdvancedRagAssistant` refuses unsafe requests and permission-restricted requests before answering. |

## Architecture

```text
question + user role
    |
    v
guardrail check
    |-- unsafe / unauthorized --> refusal
    |
    v
query rewriting
    |
    v
multi-query vector retrieval
    |
    v
candidate dedupe
    |
    v
reranking
    |
    v
evidence packet
    |
    v
grounded answer with citations
```

## What Improved Over Project 3

Project 3 had two visible failures:

- `eval-009`: unexpected refusal for analytics report export options.
- `eval-011`: missed retrieval for incident triage.

Project 4 fixes both by using query rewriting and reranking. It also adds guardrail scenarios that the baseline does not handle, such as employee access to audit-trail details.

## Run Locally

```bash
cd Projects/project-4-advanced-rag-reranking-guardrails
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Generate the corpus:

```bash
advanced-rag build-corpus --output data/corpus.jsonl --count 240
```

Ask a question:

```bash
advanced-rag ask \
  --corpus data/corpus.jsonl \
  --question "How should operators triage an incident?" \
  --role operator
```

Run comparison evaluation:

```bash
advanced-rag compare \
  --corpus data/corpus.jsonl \
  --questions data/evaluation_questions.json \
  --output docs/baseline_vs_advanced.md
```

## Tests

```bash
pytest
```

The implementation is deterministic and does not require an API key.
