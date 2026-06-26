# Guardrails

## What It Is

Input, output, and tool-call checks for prompt injection, sensitive data leakage, unsafe operations, and confidence threshold escalation.

## Where It Appears

- `guardrails/`
- `tools/guardrail_tools.py`
- `agents/guardrail_agent.py`

## Why It Matters

Enterprise agents must fail safely when confidence is low or requested actions are unsafe.

## Extend It

Add policy-backed role checks, DLP scanning, and adversarial prompt-injection evals.

