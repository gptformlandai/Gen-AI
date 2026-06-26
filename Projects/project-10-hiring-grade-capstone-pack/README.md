# Project 10: Hiring-Grade Capstone Asset Pack

This project packages the strongest work from the mini-project track into a reviewer-friendly case study.

The capstone story is **RAG Reliability Engineering**:

- Project 4 proves the production-oriented assistant: advanced RAG with query rewriting, reranking, citations, guardrails, and permission-aware refusal.
- Project 9 proves engineering diagnosis: a flawed retrieval baseline, layer-based root-cause analysis, one targeted intervention, and measurable before-vs-after gains.

## Problem

Support and operations teams need assistants that can answer from trusted knowledge, cite evidence, refuse unsafe or unauthorized requests, and improve when evaluation reveals failures.

The risk is not just hallucination. The system can fail because:

- retrieval ranks a distractor above the right document;
- the prompt is asked to answer from weak evidence;
- unsafe or restricted questions are answered instead of refused;
- improvements are made by intuition instead of measured diagnosis.

## System

The system combines:

- deterministic knowledge-base corpus;
- baseline RAG with citation traces;
- advanced retrieval with query rewriting and reranking;
- guardrails for unsafe and permission-restricted questions;
- evaluation harness with before-vs-after metrics;
- debugging case study that isolates the failing layer.

## Results

| Track | Before | After | Signal |
|---|---:|---:|---|
| Project 4 advanced RAG evaluation | 76.00% | 100.00% | Query rewriting, reranking, and guardrails fixed 6 failures. |
| Project 9 debugging evaluation | 58.33% | 100.00% | Retrieval failures fell from 5 to 0. |
| Project 9 top-1 retrieval accuracy | 58.33% | 100.00% | Candidate ranking was the root cause. |

## Asset Pack

| Required asset | File |
|---|---|
| Architecture diagram | `docs/architecture_diagram.md` |
| Failure analysis | `docs/failure_analysis.md` |
| Tradeoff justification memo | `docs/tradeoff_justification_memo.md` |
| Evaluation summary | `docs/evaluation_summary.md` |
| Interview walkthrough outline | `docs/interview_walkthrough.md` |
| Resume bullets | `docs/resume_bullets.md` |
| 3-minute demo narrative | `docs/demo_narrative.md` |
| FAQ | `docs/faq.md` |

## Run Local Validation

```bash
cd Projects/project-10-hiring-grade-capstone-pack
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
capstone-pack validate
pytest
```

The validator checks that the required asset files exist and include the expected hiring-signal sections.

