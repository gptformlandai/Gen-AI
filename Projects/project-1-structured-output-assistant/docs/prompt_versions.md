# Prompt Versions

## v1

**Goal:** Ask the model to return JSON matching the requirements schema.

**Problem:** Prompt-only JSON instructions are fragile. They can produce Markdown fences, extra keys, or missing required fields.

## v2

**Goal:** Separate system and developer instructions, include the JSON schema, and validate with Pydantic.

**Change:** The assistant now has a strict role, a schema contract, status rules, and a repair path with validation errors.

**Why this is better:** This matches the two-layer defense from structured generation:

1. Tell the model exactly what shape to produce.
2. Verify the shape with code before returning it.

## v3 Candidate

Use provider-native structured output when available, such as OpenAI JSON schema mode, then keep Pydantic validation as an assertion and business-rule gate.
