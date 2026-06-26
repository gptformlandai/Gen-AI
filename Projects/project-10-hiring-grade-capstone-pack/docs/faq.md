# FAQ

## Why not just use a larger model?

A larger model cannot reliably answer from evidence it did not retrieve. The observed failure was retrieval ranking, so the correct first fix was retrieval-layer remediation.

## Why not use prompt tuning first?

Prompt tuning can make answers sound better while hiding missing-evidence problems. The evaluation showed distractor documents ranking above the right source, so prompt tuning was not the root-cause fix.

## Why use deterministic local code instead of a hosted LLM?

The goal is to make the mechanism inspectable. Deterministic code makes failure diagnosis, tests, and before-vs-after metrics reproducible. A production version can replace the synthesizer and embeddings while preserving the evaluation harness.

## How would this scale to production?

I would add real embeddings, larger corpora, trace sampling, offline regression suites, online feedback, adversarial guardrail tests, latency budgets, and staged rollouts for retrieval changes.

## What would you improve next?

I would add noisy document ingestion, citation-faithfulness scoring, realistic role-policy data, latency measurement, and a larger held-out evaluation set to reduce overfitting risk.

## What is the most important lesson?

RAG quality is a system property. Retrieval, ranking, synthesis, guardrails, and evaluation all need separate evidence before choosing a fix.

