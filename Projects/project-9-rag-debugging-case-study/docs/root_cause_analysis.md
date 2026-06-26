# Root-Cause Analysis

## Layer Diagnosis

| Layer | Finding |
|---|---|
| Retrieval | Baseline retrieval searches body text only and ranks by raw token overlap. It misses title intent, tags, synonyms, and morphology. |
| Prompt / synthesis | The answer synthesizer is stable when the expected document is retrieved. It is not the dominant failure source. |
| Model | No model call is used in this deterministic project, so model choice is not the relevant layer. |
| Tooling | No external tool failed. The local retrieval scoring policy is the faulty component. |
| Orchestration | The control flow is simple and deterministic; no retry or state transition caused the failures. |

## Root Cause

The baseline assumes that user wording and document wording will overlap directly. That assumption breaks for realistic queries:

- "triage" versus "alert response";
- "verified" versus "HMAC signature";
- "throttled" versus "HTTP 429";
- "remove account data" versus "retention period before deletion";
- "analytics export options" where the key intent is mostly in title and tags.

## Evidence From The Run

The expected document appeared somewhere in the top 3 for every question, but the baseline often ranked a distractor first. That points to candidate ranking quality, not corpus coverage.

The most visible example is:

- Question: "How should operators triage an incident?"
- Baseline rank 1: `admin_permissions`
- Expected document: `incident_response`
- Improved rank 1: `incident_response`

## Why The Fix Is Retrieval, Not Prompting

Changing the answer prompt would not help if the correct evidence is missing. The first repair should improve candidate ranking while leaving synthesis unchanged. That makes the before-vs-after comparison cleaner.
