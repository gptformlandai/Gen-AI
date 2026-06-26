# Project 9: Optimization Or Debugging Case Study

This project implements a **RAG debugging case study** based on the Project 3 baseline RAG assistant.

The intentionally flawed baseline uses shallow lexical retrieval over document bodies only. The debugging workflow diagnoses failures by layer, then applies one targeted intervention: a retrieval reranking layer with title, tag, synonym, and phrase features.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| Clear failure hypothesis | `docs/incident_writeup.md` states that failures are mostly retrieval-layer misses, not answer synthesis failures. |
| Layer-based diagnosis | `diagnostics.py` labels rows as retrieval, synthesis, refusal, or evaluation coverage failures. |
| Targeted intervention | `retrievers.py` adds one retrieval reranking layer while keeping the answer synthesizer unchanged. |
| Before-vs-after evaluation | `evaluation.py` compares baseline and improved metrics on the same question set. |
| Incident-style writeup | `docs/incident_writeup.md` summarizes impact, evidence, timeline, and remediation. |
| Root-cause analysis | `docs/root_cause_analysis.md` explains why baseline retrieval failed. |
| Metrics table | `rag-debug evaluate` writes `docs/before_after_metrics.md`. |
| Remediation note and risks | `docs/remediation_note.md` documents the intervention and remaining limits. |

## Architecture

```text
evaluation questions
    |
    v
baseline lexical retriever --------> answer synthesizer
    |                                      |
    v                                      v
baseline metrics                    row-level diagnosis

improved reranker -----------------> same answer synthesizer
    |                                      |
    v                                      v
improved metrics                    before-vs-after comparison
```

## Why This Is A Debugging Project

This project does not start by adding more model power. It first asks:

- Did retrieval find the expected document?
- If it did, did the answer include the required facts?
- Are failures clustered in one layer?
- Does a narrow intervention improve the metrics?

That is the difference between engineering diagnosis and random prompt tweaking.

## Run Locally

```bash
cd Projects/project-9-rag-debugging-case-study
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Ask with the baseline:

```bash
rag-debug ask \
  --mode baseline \
  --question "How should operators triage an incident?"
```

Ask with the improved retriever:

```bash
rag-debug ask \
  --mode improved \
  --question "How should operators triage an incident?"
```

Run before-vs-after evaluation:

```bash
rag-debug evaluate \
  --output docs/before_after_metrics.md \
  --failures-output docs/failure_cases.md
```

## Tests

```bash
pytest
```

The implementation is deterministic and does not require an API key.

