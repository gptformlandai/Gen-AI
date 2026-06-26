# Failure Analysis

## Summary

The capstone exposes failures instead of hiding them. The main observed failures were retrieval misses and guardrail misses.

## Retrieval Failures

Project 9 showed that the flawed baseline had:

- pass rate: 58.33%;
- top-1 document accuracy: 58.33%;
- retrieval failures: 5.

The root cause was shallow lexical ranking over body text only. The expected document often appeared in the top 3, but a distractor ranked first.

Example:

- Question: "How should operators triage an incident?"
- Baseline rank 1: `admin_permissions`
- Expected document: `incident_response`
- Improved rank 1: `incident_response`

## Guardrails

Project 4 showed failures where the baseline answered questions that should have been refused, especially employee requests for audit/admin-sensitive details. The advanced assistant fixed those by checking user role and request type before retrieval and synthesis.

## Prompt And Synthesis

The answer layer worked when the right evidence reached it. That is why the remediation focused on retrieval and guardrails rather than prompt polish.

## Remaining Risks

- Small deterministic corpora can overstate quality.
- Hand-built synonym maps can overfit current tests.
- Guardrail coverage needs adversarial evaluation.
- Production retrieval should include larger corpora, noisy documents, and trace sampling.
- A real LLM answer layer would need hallucination and citation-faithfulness checks.

