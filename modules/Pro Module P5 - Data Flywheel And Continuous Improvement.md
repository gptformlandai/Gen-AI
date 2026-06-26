# Pro Module P5 - Data Flywheel And Continuous Improvement

> **Module time:** 22h
> **Why this module matters:** The compounding advantage of a production GenAI system is its data loop, not its model. This module turns usage into an ever-improving asset and connects evaluation (Module 8) to optimization (Module 18).

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic P5.1** | **Capturing the right signals (8h)** | |
| P5.1.a | Logging prompts, contexts, outputs, traces, and outcomes safely | Done |
| P5.1.b | Implicit vs explicit feedback and their reliability | Done |
| P5.1.c | Privacy-safe capture: consent, redaction, and retention | Done |
| P5.1.d | Turning production failures into reproducible fixtures | Done |
| **Topic P5.2** | **From signals to growing eval sets (8h)** | |
| P5.2.a | Triaging and labeling captured data into golden sets | Done |
| P5.2.b | Hard-negative mining and edge-case curation | Done |
| P5.2.c | Detecting drift and growing coverage where the system is weak | Done |
| P5.2.d | Keeping eval sets trustworthy as they scale | Done |
| **Topic P5.3** | **Closing the loop with optimization (6h)** | |
| P5.3.a | When the loop justifies distillation or fine-tuning vs prompt/retrieval fixes | Done |
| P5.3.b | Synthetic data generation and curation pitfalls | Done |
| P5.3.c | Measuring whether the loop actually improved the system | Done |
| **Module checkpoint** | Data flywheel and continuous improvement synthesis | Done |

**Covered so far:**
- P5.1.a - Logging prompts, contexts, outputs, traces, and outcomes safely: trace envelope design, prompt/context/output capture, retrieval and tool lineage, model/prompt/config versions, outcome signals, redaction boundaries, storage tiers, access control, code sample, active recall, and interview-ready answer.
- P5.1.b - Implicit vs explicit feedback and their reliability: feedback taxonomy, thumbs up/down, corrections, retries, abandonment, dwell time, support escalation, noisy labels, bias, reliability scoring, aggregation, active recall, and interview-ready feedback strategy.
- P5.1.c - Privacy-safe capture: consent, redaction, and retention: privacy-by-design pipeline, capture eligibility, consent state, PII/PHI/PCI handling, redaction, tokenization, minimization, retention classes, deletion workflows, audit, active recall, and interview-ready privacy answer.
- P5.1.d - Turning production failures into reproducible fixtures: failure capture, replay bundles, fixture schema, dependency pinning, retrieval snapshots, tool mocks, expected behavior, regression tests, triage flow, active recall, and interview-ready fixture answer.
- P5.2.a - Triaging and labeling captured data into golden sets: triage queues, label taxonomy, gold/silver/bronze data tiers, labeling rubric, reviewer agreement, source-of-truth expected answers, coverage metadata, active recall, and interview-ready golden set design.
- P5.2.b - Hard-negative mining and edge-case curation: near-miss retrieval examples, confusing intents, adversarial but realistic inputs, slice coverage, contrastive examples, false positives, false negatives, active recall, and interview-ready hard-negative answer.
- P5.2.c - Detecting drift and growing coverage where the system is weak: traffic drift, retrieval drift, model behavior drift, data distribution changes, metric slices, alert thresholds, coverage gaps, weak-slice expansion, active recall, and interview-ready drift answer.
- P5.2.d - Keeping eval sets trustworthy as they scale: eval governance, deduplication, leakage control, label audits, versioning, frozen benchmark splits, freshness policy, ownership, retirement, active recall, and interview-ready eval integrity answer.
- P5.3.a - When the loop justifies distillation or fine-tuning vs prompt/retrieval fixes: optimization decision tree, root-cause alignment, prompt vs retrieval vs reranking vs fine-tuning vs distillation, ROI thresholds, data requirements, active recall, and interview-ready decision answer.
- P5.3.b - Synthetic data generation and curation pitfalls: synthetic data roles, generation recipes, diversity control, contamination risk, model self-confirmation, label hallucination, filtering, human review, active recall, and interview-ready synthetic data answer.
- P5.3.c - Measuring whether the loop actually improved the system: before/after evals, regression suites, online metrics, A/B tests, guardrails, statistical confidence, cost-quality tradeoffs, rollback criteria, active recall, and interview-ready measurement answer.
- Module checkpoint - Data flywheel and continuous improvement synthesis: privacy-safe capture pipeline, production failure to regression fixture loop, eval set growth strategy, optimization decision framework, improvement measurement plan, active recall, and senior-level flywheel defense.

---

## Topic P5.1: Capturing the Right Signals

> **Topic time:** 8h
> Focus: Capturing enough production evidence to improve the system while respecting privacy, security, consent, retention, and user trust.

A data flywheel starts with a brutal constraint:

```text
You cannot improve what you cannot observe.
You should not observe what you are not allowed to keep.
```

The goal is not to log everything forever.

The goal is to capture the right signals safely:

```text
what the user asked
what context the system used
what the model produced
which tools were called
what outcome happened
which version of the system was responsible
whether the result was good, bad, unsafe, slow, costly, or confusing
```

The central idea:

> A production GenAI trace is raw material. A privacy-safe, labeled, reproducible eval case is an asset.

The flywheel is the path between those two.

---

## Subtopic P5.1.a: Logging Prompts, Contexts, Outputs, Traces, and Outcomes Safely

> **Subtopic time:** 2h
> Outcome: You should be able to design a trace schema that supports debugging, eval creation, cost analysis, safety review, and replay without casually leaking sensitive data.

### Add to Knowledge Base

Basic logging says:

```text
request in
response out
```

GenAI logging needs more:

```text
prompt
retrieved context
tool calls
model configuration
output
citations
latency
cost
safety decisions
user feedback
business outcome
artifact versions
```

The mental model:

> A trace should let you explain why the system answered the way it did.

If a user reports a bad answer, you need to reconstruct:

```text
which prompt template ran
which model ran
which retrieval query ran
which chunks were retrieved
which tool calls happened
which policy checks passed
which answer was returned
which user-visible outcome followed
```

Without that, debugging becomes guesswork.

---

### 1. What to Capture

Capture at the right abstraction level.

| Layer | Useful Signals |
|---|---|
| Request | route, tenant, user role, locale, task type, risk tier |
| Prompt | prompt template ID, version, variables, rendered prompt hash |
| Retrieval | query, filters, top-k, scores, chunk IDs, doc versions, ACL versions |
| Context | context length, source IDs, citation candidates, redaction status |
| Model | model alias, provider, exact model version if available, decoding params |
| Tools | tool name, args hash, permission decision, output hash, status |
| Output | answer, schema validity, citations, refusal reason, safety labels |
| Outcome | user feedback, correction, retry, escalation, conversion, task success |
| Cost | input tokens, cached tokens, output tokens, tool cost, total estimated cost |
| Latency | retrieval, rerank, tool, model, gateway, end-to-end |
| Release | prompt/model/retrieval/config/policy/eval versions |

Do not capture raw sensitive content by default if a hash, reference, or redacted value is enough.

---

### 2. Safe Trace Envelope

Store traces in layers:

```text
metadata layer:
  broadly queryable, no raw sensitive text

redacted content layer:
  accessible to approved debugging/eval users

raw content layer:
  only if justified, encrypted, short retention, tightly controlled
```

This supports:

```text
analytics without raw data
debugging with redacted data
restricted replay when policy allows
```

Strong default:

```text
log identifiers and fingerprints first
log raw content only when there is an approved purpose
```

---

### 3. Trace Schema Example

```json
{
  "trace_id": "tr_123",
  "session_id": "sess_456",
  "tenant_id": "tenant_a",
  "route": "support_rag_answer",
  "risk_tier": "medium",
  "consent_state": "analytics_and_quality",
  "prompt": {
    "template_id": "support_rag_v7",
    "rendered_hash": "sha256:abc",
    "variables_redacted": true
  },
  "retrieval": {
    "query_hash": "sha256:def",
    "top_k": 8,
    "chunks": [
      {"doc_id": "refund_policy", "chunk_id": "c12", "doc_version": "42", "score": 0.82}
    ]
  },
  "model": {
    "alias": "balanced",
    "provider": "provider_a",
    "config_version": "model_route_2026_06"
  },
  "output": {
    "answer_hash": "sha256:ghi",
    "schema_valid": true,
    "citation_count": 2,
    "safety_label": "allowed"
  },
  "outcome": {
    "thumb": "down",
    "retry_count": 1,
    "escalated_to_human": true,
    "task_success": false
  },
  "usage": {
    "input_tokens": 4200,
    "output_tokens": 420,
    "estimated_cost_usd": 0.019
  }
}
```

This trace is useful even if raw text is stored elsewhere or not stored at all.

---

### 4. Outcome Signals Matter

A perfect trace without outcome is incomplete.

You need to know:

```text
Did the user accept the answer?
Did they ask again?
Did they correct it?
Did they escalate?
Did the downstream task complete?
Did the answer violate policy?
Did it save time?
Did it create a support ticket?
```

The flywheel depends on outcome.

Otherwise you collect data but do not know what it means.

---

### 5. Code Sample: Safe Trace Builder

```python
import hashlib
import json
from typing import Any


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def build_trace(
    trace_id: str,
    tenant_id: str,
    route: str,
    prompt_text: str,
    retrieved_chunks: list[dict],
    answer_text: str,
    usage: dict,
    outcome: dict,
) -> dict:
    return {
        "trace_id": trace_id,
        "tenant_id": tenant_id,
        "route": route,
        "prompt_hash": sha256_text(prompt_text),
        "retrieval_fingerprint": sha256_text(stable_json(retrieved_chunks)),
        "answer_hash": sha256_text(answer_text),
        "chunk_refs": [
            {
                "doc_id": chunk["doc_id"],
                "chunk_id": chunk["chunk_id"],
                "version": chunk["version"],
            }
            for chunk in retrieved_chunks
        ],
        "usage": usage,
        "outcome": outcome,
    }
```

The point:

```text
log useful references and hashes
avoid raw content unless policy allows it
```

---

### 6. Practical Interview Question

> What would you log from a production RAG assistant so failures can become eval cases?

### Strong Answer

I would log a structured trace, not just prompt and answer text. The trace should include tenant, route, task type, risk tier, prompt template and version, model alias and config, retrieval query fingerprint, top-k chunk IDs, document versions, ACL versions, reranker scores, tool calls, output schema validity, citations, safety labels, token usage, latency breakdown, cost, and outcome signals like retry, correction, thumbs down, escalation, or task completion.

For privacy, I would separate metadata, redacted content, and raw content. Most analytics should work from metadata and hashes. Raw prompts or outputs should only be stored when consent and policy allow it, with encryption, short retention, access controls, and audit logs. The goal is to make a bad production answer reproducible without turning the trace store into a sensitive-data dump.

### Active Recall

1. Why is logging only prompt and answer not enough?
2. What retrieval fields make a RAG answer reproducible?
3. Why should traces include prompt/model/config versions?
4. What is the difference between metadata, redacted content, and raw content layers?
5. Which outcome signals are useful for eval-set growth?

Final takeaway:

> Good traces are the seed of the data flywheel. Safe traces are the only kind that should survive production.

---

## Subtopic P5.1.b: Implicit vs Explicit Feedback and Their Reliability

> **Subtopic time:** 2h
> Outcome: You should be able to explain which feedback signals are trustworthy, which are noisy, and how to combine them without fooling yourself.

### Add to Knowledge Base

Feedback tells the system whether behavior worked.

There are two broad types:

```text
explicit feedback:
  the user directly rates or corrects the answer

implicit feedback:
  the user's behavior suggests whether the answer helped
```

The mental model:

> Feedback is evidence, not truth.

Every signal has bias.

The flywheel gets stronger when it knows how much to trust each signal.

---

### 1. Explicit Feedback

Examples:

```text
thumbs up
thumbs down
star rating
written comment
user correction
expert review
human label
support agent disposition
```

Strengths:

```text
direct
easy to interpret
good for triage
useful for qualitative diagnosis
```

Weaknesses:

```text
low response rate
selection bias
angry users overrepresented
happy silent users underrepresented
ambiguous thumbs down
users may rate tone instead of correctness
```

A thumbs down means:

```text
something went wrong for the user
```

It does not automatically mean:

```text
retrieval failed
model failed
prompt failed
```

You still need diagnosis.

---

### 2. Implicit Feedback

Examples:

```text
user retries same question
user reformulates question
user copies answer
user clicks citation
user abandons session
user escalates to human
user completes workflow
user accepts generated edit
user reverts generated edit
user spends long time reading
support ticket reopened
```

Strengths:

```text
high volume
available even without ratings
closer to real behavior
good for detecting friction
```

Weaknesses:

```text
ambiguous
correlated with UX
can be affected by user skill
can reward persuasive but wrong answers
can punish correct but complex answers
```

Example:

```text
user copied answer
```

Could mean:

```text
answer was useful
```

Or:

```text
user copied it to complain elsewhere
```

Implicit signals need aggregation and context.

---

### 3. Feedback Reliability Ladder

From weakest to strongest:

```text
page dwell time
copy/click behavior
thumbs up/down
free-text user comment
user correction
expert label
ground-truth business outcome
reproducible failure fixture with expected answer
```

But even ground truth can be complicated.

For example:

```text
conversion happened
```

does not always mean:

```text
answer was accurate or safe
```

Product success and answer correctness are related, not identical.

---

### 4. Reliability Scoring

Assign confidence to signals.

Example:

| Signal | Reliability | Notes |
|---|---:|---|
| thumbs down only | 0.35 | useful triage, weak diagnosis |
| thumbs down plus correction | 0.65 | stronger, still user-supplied |
| expert label | 0.90 | strong if rubric is clear |
| human escalation resolved as wrong answer | 0.85 | strong operational evidence |
| user retry within 30 seconds | 0.45 | suggests friction |
| citation clicked | 0.30 | engagement, not correctness |
| task completed | 0.70 | strong for product success, not full correctness |

Use feedback for:

```text
triage
sampling
prioritization
eval case candidates
weak-slice detection
online monitoring
```

Do not use raw noisy feedback as training data without review.

---

### 5. Code Sample: Feedback Aggregation

```python
SIGNAL_WEIGHTS = {
    "thumb_down": -0.35,
    "thumb_up": 0.25,
    "retry_same_intent": -0.30,
    "human_escalation": -0.55,
    "user_correction": -0.70,
    "task_completed": 0.60,
    "expert_accept": 0.90,
    "expert_reject": -0.90,
}


def feedback_score(signals: list[str]) -> float:
    score = sum(SIGNAL_WEIGHTS.get(signal, 0.0) for signal in signals)
    return max(-1.0, min(1.0, score))


examples = [
    ["thumb_down", "retry_same_intent"],
    ["thumb_up", "task_completed"],
    ["thumb_down", "user_correction", "human_escalation"],
]

for signals in examples:
    print(signals, feedback_score(signals))
```

This is not a universal scoring model.

It demonstrates that feedback should be interpreted as weighted evidence.

---

### 6. Practical Interview Question

> How would you use thumbs up/down and user behavior to improve a GenAI assistant?

### Strong Answer

I would treat feedback as triage evidence, not direct truth. Explicit feedback like thumbs down, comments, and corrections is useful because it tells us where users noticed pain, but it has selection bias and may reflect tone, latency, UX, or expectation mismatch rather than answer correctness.

Implicit signals like retries, reformulations, citation clicks, abandonment, copy behavior, task completion, and human escalation give higher-volume behavioral evidence. They are useful for detecting friction and weak slices, but they are ambiguous.

I would combine signals into a prioritized review queue. High-confidence negative cases, such as thumbs down plus correction plus escalation, should be turned into labeled fixtures. Low-confidence signals should influence sampling, not training directly. Expert review and reproducible expected behavior should be required before adding cases to golden evals or fine-tuning data.

### Active Recall

1. Why is a thumbs down not a root cause?
2. Give three implicit feedback signals.
3. Why can task completion fail as a correctness signal?
4. What feedback is strong enough for golden eval creation?
5. Why should noisy feedback not become training data directly?

Final takeaway:

> Feedback is a compass, not a judge. It points you toward cases worth investigating.

---

## Subtopic P5.1.c: Privacy-Safe Capture - Consent, Redaction, and Retention

> **Subtopic time:** 2h
> Outcome: You should be able to design a data-capture pipeline that collects improvement signals while respecting consent, data minimization, redaction, access control, and deletion requirements.

### Add to Knowledge Base

The data flywheel is only valuable if users and regulators can trust it.

Privacy-safe capture means:

```text
collect only what you need
only when allowed
redact or transform sensitive fields
retain for the minimum useful period
control access
honor deletion
audit usage
```

The mental model:

> Production data is borrowed, not owned.

You need explicit rules for what can enter the flywheel.

---

### 1. Capture Eligibility

Before storing a trace for improvement, check:

```text
tenant policy
user consent
data category
region
contract terms
risk tier
purpose limitation
retention class
```

Example capture decisions:

| Data | Capture Decision |
|---|---|
| public docs question | store redacted trace, eligible for eval |
| enterprise private ticket | store metadata, redacted text only with tenant permission |
| healthcare note | strict PHI controls, often no raw content for training |
| payment details | do not store raw; tokenize or redact |
| secrets/API keys | detect and purge |
| child data | specialized policy, often disallow improvement capture |

The pipeline should reject data before it reaches broad stores.

---

### 2. Redaction and Transformation

Common sensitive classes:

```text
PII: names, emails, phone numbers, addresses, IDs
PHI: health information
PCI: payment card data
secrets: API keys, tokens, passwords
business confidential: contracts, strategy, customer data
regulated attributes: age, race, religion, disability, etc.
```

Redaction options:

```text
remove
mask
hash
tokenize
pseudonymize
generalize
replace with typed placeholder
```

Example:

```text
"Email Sarah at sarah@example.com about invoice INV-123"
```

Redacted:

```text
"Email [PERSON] at [EMAIL] about invoice [INVOICE_ID]"
```

For evals, typed placeholders are often better than deletion because they preserve task structure.

---

### 3. Retention Classes

Not all data should live equally long.

| Store | Example Retention |
|---|---|
| raw trace | hours to days, if stored at all |
| redacted trace | weeks to months |
| metadata metrics | longer, depending on policy |
| approved eval fixture | long-lived, versioned |
| training dataset | long-lived only after explicit approval |
| security incident evidence | retention per legal/security policy |

Long-lived eval cases should be:

```text
redacted
reviewed
licensed/allowed
purpose-tagged
versioned
deletion-aware
```

---

### 4. Access Control

Separate roles:

```text
operator:
  sees metadata and aggregate metrics

debugger:
  sees redacted traces for assigned incidents

labeler:
  sees approved labeling queue

security/privacy reviewer:
  can inspect sensitive handling

admin:
  manages policies and access
```

Every access to sensitive trace data should be:

```text
authenticated
authorized
logged
reviewable
time-bound where possible
```

The flywheel should not become a shadow data warehouse.

---

### 5. Code Sample: Capture Policy Check

```python
def capture_allowed(event: dict) -> tuple[bool, str]:
    if event["consent_state"] not in {"quality_improvement", "analytics_and_quality"}:
        return False, "missing_consent"
    if event["data_category"] in {"payment_card", "secret"}:
        return False, "disallowed_data_category"
    if event["tenant_policy"].get("allow_quality_capture") is not True:
        return False, "tenant_policy_denies"
    if event["region"] not in event["tenant_policy"].get("allowed_regions", []):
        return False, "region_not_allowed"
    return True, "allowed"
```

This is the entry gate.

The redaction pipeline comes after.

---

### 6. Practical Interview Question

> How would you collect production traces for eval creation without violating privacy expectations?

### Strong Answer

I would design capture as a policy-controlled pipeline. Every trace would first pass capture eligibility based on tenant policy, user consent, data category, region, risk tier, and purpose. I would minimize raw content capture and separate metadata, redacted content, and raw content stores. Most analytics and triage should work from metadata, hashes, and references.

Before a trace becomes an eval case, it should be redacted, reviewed, and tagged with allowed use. PII, PHI, PCI, secrets, and confidential data should be masked, tokenized, or excluded according to policy. Retention should differ by store: raw traces short-lived, redacted traces medium-lived, approved eval fixtures longer-lived and versioned. Access should be role-based and audited.

I would also support deletion workflows. If a user or tenant deletes data, derived artifacts need clear lineage so we can remove or re-review affected eval cases and training examples.

### Active Recall

1. What checks should happen before storing production data for improvement?
2. Why are typed placeholders useful in redacted eval cases?
3. Why should raw traces have shorter retention than approved fixtures?
4. What is purpose limitation?
5. Why does deletion require lineage?

Final takeaway:

> A data flywheel that ignores privacy is not an asset. It is future incident material.

---

## Subtopic P5.1.d: Turning Production Failures Into Reproducible Fixtures

> **Subtopic time:** 2h
> Outcome: You should be able to transform a production failure into a deterministic regression case that can be replayed in CI and used to prevent recurrence.

### Add to Knowledge Base

A production failure is a story.

A regression fixture is a testable artifact.

The flywheel works when you convert:

```text
"User got a bad answer yesterday"
```

into:

```text
input
context snapshot
tool mocks
expected behavior
evaluation rubric
versions
replay command
```

The mental model:

> A failure that cannot be replayed can easily return.

Reproducibility turns incidents into coverage.

---

### 1. What a Fixture Needs

A GenAI fixture should include:

```text
fixture_id
source_trace_id
failure_type
input
redacted conversation history
retrieval snapshot or source refs
tool call mocks
prompt/model/config versions
expected answer or expected properties
forbidden behaviors
grader/rubric
owner
created_at
privacy classification
```

For RAG:

```text
which documents should be retrieved
which evidence supports the answer
which evidence must not be used
expected citation behavior
```

For agents:

```text
expected tool sequence
tools not allowed
approval points
stop condition
```

For safety:

```text
expected refusal or safe completion
policy category
red-team tag
```

---

### 2. Fixture Types

| Failure | Fixture Type |
|---|---|
| wrong answer despite evidence | answer-quality regression |
| missing evidence | retrieval regression |
| bad citation | citation regression |
| tool called incorrectly | trajectory regression |
| unsafe output | safety regression |
| schema parse failure | structured-output regression |
| excessive cost | cost regression |
| timeout | latency regression |
| cross-tenant data exposure | security regression |

Different fixture types need different graders.

Do not force every failure into a single "answer equals string" test.

---

### 3. Replay Bundle

A replay bundle freezes dependencies:

```text
prompt version
model alias/version
retrieval corpus snapshot
embedding/reranker config
tool mock responses
feature flags
safety policy
gateway routing config
```

Why?

Because a failed answer may disappear if:

```text
the document changed
the retriever changed
the provider model changed
the tool result changed
the prompt changed
```

You need to know whether the fix actually fixed the failure or the environment merely moved.

---

### 4. Code Sample: Fixture Skeleton

```json
{
  "fixture_id": "fx_support_refund_001",
  "source_trace_id": "tr_123",
  "failure_type": "unsupported_answer",
  "route": "support_rag_answer",
  "input": "Can I get a refund after 45 days?",
  "retrieval_snapshot": [
    {
      "doc_id": "refund_policy",
      "chunk_id": "c12",
      "version": "42",
      "text_redacted": "Refunds are available within [DAYS] days..."
    }
  ],
  "expected": {
    "must_state": ["refunds are not available after 30 days"],
    "must_cite": ["refund_policy:c12"],
    "must_not_state": ["refund approved"]
  },
  "grader": {
    "type": "rubric",
    "checks": ["groundedness", "citation_correctness", "policy_compliance"]
  },
  "privacy": {
    "classification": "redacted_public_policy",
    "allowed_use": ["eval", "regression"]
  }
}
```

This is now reusable.

The original bad trace was not.

---

### 5. Failure-to-Fixture Workflow

```text
1. Detect failure from user report, metric, feedback, or red-team run.
2. Pull trace and dependency metadata.
3. Classify failure type.
4. Redact and minimize content.
5. Freeze retrieval/tool/prompt/config snapshot.
6. Write expected behavior and forbidden behavior.
7. Choose grader.
8. Have reviewer approve fixture.
9. Add to regression suite.
10. Verify current system fails the fixture.
11. Fix system.
12. Verify system passes fixture and no existing suite regresses.
```

Step 10 is important.

If the current system does not fail the fixture, the fixture may not capture the original problem.

---

### 6. Practical Interview Question

> A user reports that your RAG assistant hallucinated a refund policy. How do you turn that into a regression test?

### Strong Answer

I would pull the production trace and capture the full dependency context: user input, redacted conversation, retrieved chunk IDs, document versions, reranker scores, prompt version, model alias, generation settings, policy version, and any tool outputs. Then I would classify the failure, such as unsupported answer, missing evidence, or citation error.

I would create a fixture with redacted input, a frozen retrieval snapshot or controlled source references, expected answer properties, required citations, forbidden claims, and a rubric grader for groundedness and citation correctness. I would verify that the current or reproduced failing system fails the fixture. Then the fixture becomes part of the regression suite so future prompt, retrieval, model, or reranker changes cannot reintroduce the same failure.

### Active Recall

1. What is the difference between a trace and a fixture?
2. Why should a fixture include tool mocks?
3. Why should you verify that the fixture fails before fixing?
4. What fixture type catches bad agent tool sequences?
5. What privacy fields should a fixture include?

Final takeaway:

> Production failures become valuable only when they become reproducible, reviewed, privacy-safe regression fixtures.

---

## Topic P5.2: From Signals to Growing Eval Sets

> **Topic time:** 8h
> Focus: Turning captured traces and feedback into trustworthy eval sets that grow where the system is weak, not just where data is easy to collect.

Raw production data is messy.

Eval sets must be curated.

The transformation looks like:

```text
trace -> candidate -> triage -> redaction -> label -> review -> fixture -> eval suite
```

The central idea:

> Eval growth should be targeted by failure risk and coverage gaps, not by random accumulation.

More cases are not automatically better.

Better coverage is better.

---

## Subtopic P5.2.a: Triaging and Labeling Captured Data Into Golden Sets

> **Subtopic time:** 2h
> Outcome: You should be able to design a triage and labeling process that turns production candidates into high-quality golden eval cases.

### Add to Knowledge Base

A golden set is a trusted eval set.

It contains cases with:

```text
clear input
clear expected behavior
clear rubric
reviewed labels
known source
versioned metadata
coverage tags
```

The mental model:

> Golden sets are not logs. They are reviewed behavioral requirements.

If a case enters the golden set, it becomes part of the system's contract.

---

### 1. Triage Queues

Create queues such as:

```text
high-risk failure
high-volume failure
new intent
low-confidence success
retrieval miss
bad citation
safety issue
tool failure
edge case
candidate for training
candidate for eval only
```

Prioritize by:

```text
user impact
frequency
risk
business value
novelty
coverage gap
reproducibility
```

Do not label everything.

Label the cases that teach the system something.

---

### 2. Label Taxonomy

Use consistent labels:

```text
task_type
domain
intent
risk_tier
failure_type
expected_behavior_type
required_evidence
forbidden_behavior
user_segment
language
modality
difficulty
```

Example failure labels:

```text
retrieval_miss
irrelevant_context
bad_rerank
unsupported_answer
incorrect_citation
tool_argument_error
unsafe_compliance
schema_invalid
over_refusal
under_refusal
latency_timeout
cost_explosion
```

Good labels make slice analysis possible.

Without labels, eval results become one blurry score.

---

### 3. Gold, Silver, Bronze

Not all data deserves the same trust.

```text
gold:
  expert-reviewed, stable, used for release gates

silver:
  reviewed or high-confidence labels, useful for monitoring and development

bronze:
  raw or weakly labeled candidates, useful for triage and mining
```

Use cases:

```text
gold -> CI gate
silver -> exploratory analysis, dashboards
bronze -> candidate pool
```

Never let bronze silently become training or release-gating data.

---

### 4. Labeling Rubric

A good rubric is specific.

Bad:

```text
Is the answer good?
```

Better:

```text
1. Does the answer directly address the user's question?
2. Is every factual claim supported by retrieved evidence?
3. Are citations correct and specific?
4. Does the answer avoid forbidden claims?
5. Does it follow the output schema?
6. Does it satisfy the relevant safety policy?
```

Rubrics should include examples of:

```text
pass
partial pass
fail
common ambiguous cases
```

This improves reviewer agreement.

---

### 5. Practical Interview Question

> How do production traces become a golden eval set?

### Strong Answer

I would not move traces directly into golden evals. I would first create candidate queues from high-signal events such as user corrections, repeated retries, human escalations, safety flags, retrieval misses, and high-impact routes. Each candidate would be privacy-screened and redacted before labeling.

Then reviewers would apply a rubric with labels for task type, intent, risk tier, failure type, expected behavior, required evidence, forbidden behavior, and coverage tags. High-confidence, reviewed cases become gold and can gate releases. Lower-confidence cases stay silver for monitoring or bronze for future triage.

I would track reviewer agreement and periodically audit labels. A golden set is a behavioral contract, so cases should be curated, versioned, owned, and reviewed rather than accumulated blindly.

### Active Recall

1. Why are production logs not golden evals?
2. What makes a case eligible for gold?
3. What is the purpose of silver and bronze data tiers?
4. Why do eval cases need coverage tags?
5. What makes a labeling rubric reliable?

Final takeaway:

> A golden set is not found in production. It is manufactured from production evidence through review, labeling, and governance.

---

## Subtopic P5.2.b: Hard-Negative Mining and Edge-Case Curation

> **Subtopic time:** 2h
> Outcome: You should be able to find and curate the cases most likely to expose retrieval, routing, prompting, and model weaknesses.

### Add to Knowledge Base

Easy examples make eval scores look good.

Hard examples make systems better.

Hard negatives are cases that look similar to correct cases but should produce a different answer, retrieval result, label, or action.

The mental model:

> Hard negatives teach the system the boundary between almost right and actually right.

Examples:

```text
"refund after 30 days" vs "refund after 45 days"
"admin can reset password" vs "user can reset own password"
"delete draft" vs "delete production record"
"policy for California" vs "policy for Canada"
```

These are where real systems fail.

---

### 1. Retrieval Hard Negatives

For RAG:

```text
query retrieves plausible but wrong chunk
query retrieves old policy instead of current policy
query retrieves same topic but wrong region/product/tier
query retrieves public doc when private tenant doc should win
query retrieves answer but citation rank is too low
```

Hard-negative evals should test:

```text
can retriever find the right chunk?
can reranker place it high enough?
can generator ignore tempting wrong context?
can citation logic cite the actual support?
```

---

### 2. Classification and Tool Hard Negatives

For intent classification:

```text
"cancel my subscription" vs "cancel the scheduled email"
"reset password" vs "reset MFA"
"refund status" vs "refund request"
```

For tools:

```text
lookup_order vs cancel_order
draft_email vs send_email
read_calendar vs create_event
estimate_cost vs approve_purchase
```

The point is to prevent near-intent confusion.

---

### 3. Edge-Case Sources

Mine edge cases from:

```text
user corrections
retrieval low confidence
retriever/generator disagreement
high similarity but different labels
semantic cache rejections
human escalation notes
outlier latency or cost traces
policy boundary cases
long-tail languages
new product releases
high-value customers
red-team exercises
```

Do not wait for edge cases to appear randomly.

Actively hunt them.

---

### 4. Code Sample: Mining Similar Questions With Different Labels

```python
def hard_negative_pairs(examples: list[dict], min_similarity: float = 0.85):
    pairs = []
    for i, left in enumerate(examples):
        for right in examples[i + 1:]:
            if left["label"] == right["label"]:
                continue
            if left["similarity_to"].get(right["id"], 0.0) >= min_similarity:
                pairs.append((left["id"], right["id"]))
    return pairs
```

This catches:

```text
semantically close
but label-different
```

Those cases are valuable for routing, classification, retrieval, and semantic caching.

---

### 5. Practical Interview Question

> How would you improve a RAG eval set that is too easy?

### Strong Answer

I would mine hard negatives and edge cases. First I would look for queries where retrieval found plausible but wrong chunks: same topic but wrong product, region, customer tier, policy version, or permission scope. Then I would add cases where the correct chunk exists but is ranked below distracting chunks.

I would also mine production traces with user corrections, repeated reformulations, human escalations, low reranker confidence, semantic-cache near misses, and citation errors. Each hard case would include expected evidence, tempting wrong evidence, required citations, and forbidden claims.

The goal is not to make the eval set adversarial in an unrealistic way. The goal is to represent realistic confusion boundaries that the production system must handle.

### Active Recall

1. What is a hard negative?
2. Why are same-topic wrong-region docs dangerous in RAG?
3. How can semantic cache rejections help mine hard negatives?
4. What is a tool hard negative?
5. Why are easy eval sets misleading?

Final takeaway:

> Hard negatives are where the flywheel becomes sharp. They teach the system not just what to do, but what not to confuse.

---

## Subtopic P5.2.c: Detecting Drift and Growing Coverage Where the System Is Weak

> **Subtopic time:** 2h
> Outcome: You should be able to detect when production traffic or system behavior changes and grow eval coverage in the slices where risk is increasing.

### Add to Knowledge Base

Drift means the world moved.

Or the system moved.

Common drift types:

```text
traffic drift:
  users ask different kinds of questions

data drift:
  source corpus changes

retrieval drift:
  retrieved chunks/scores change

model drift:
  provider behavior changes or model version changes

policy drift:
  safety/business rules change

outcome drift:
  success rate changes for a slice
```

The mental model:

> Drift is a coverage alarm. It tells you where yesterday's eval set may no longer protect tomorrow's system.

---

### 1. Drift Signals

Track by route and slice:

```text
new intents
intent distribution shift
language distribution shift
input length shift
retrieval score distribution shift
top documents changed
no-answer rate
citation coverage
tool failure rate
schema failure rate
human escalation rate
thumbs down rate
cost per session
latency distribution
```

Example:

```text
Spanish traffic grows from 3% to 18%
but golden eval has only 4 Spanish cases
```

That is a coverage gap.

---

### 2. Weak-Slice Expansion

When a slice regresses, add coverage.

Slice examples:

```text
language = Spanish
product = enterprise billing
tenant tier = regulated
intent = cancellation
document type = contract
route = agent_tool_action
input length > 20k tokens
risk tier = high
```

For each weak slice:

```text
sample production traces
redact
triage
label
add representative pass/fail cases
add hard negatives
add regression fixtures
track slice metrics separately
```

Do not only add global cases.

Drift is usually slice-specific.

---

### 3. Coverage Matrix

Maintain a matrix:

| Slice | Traffic Share | Eval Cases | Failure Rate | Action |
|---|---:|---:|---:|---|
| English public FAQ | 45% | 220 | 1.2% | stable |
| Spanish billing | 18% | 4 | 8.5% | expand urgently |
| Enterprise legal | 2% | 80 | 3.0% | maintain despite low volume |
| Mobile short queries | 20% | 40 | 2.1% | add edge cases |
| Long-document analysis | 5% | 12 | 7.0% | expand |

Coverage is not only proportional to traffic.

Risk matters.

Low-volume high-risk slices deserve strong coverage.

---

### 4. Code Sample: Coverage Gap Score

```python
def coverage_gap_score(traffic_share: float, failure_rate: float, risk_weight: float, eval_cases: int) -> float:
    coverage_penalty = 1 / max(eval_cases, 1)
    return traffic_share * (1 + failure_rate) * risk_weight * coverage_penalty


slices = [
    {"name": "spanish_billing", "traffic": 0.18, "fail": 0.085, "risk": 2.0, "cases": 4},
    {"name": "public_faq", "traffic": 0.45, "fail": 0.012, "risk": 0.7, "cases": 220},
]

for s in slices:
    print(s["name"], coverage_gap_score(s["traffic"], s["fail"], s["risk"], s["cases"]))
```

This is a simple prioritization heuristic.

The lesson:

```text
traffic + failure + risk + low coverage = expand evals
```

---

### 5. Practical Interview Question

> How do you know when your eval set is no longer representative?

### Strong Answer

I would compare production traffic and outcomes against eval coverage by slice. Signals include changes in intent distribution, language mix, input length, document types, top retrieved sources, retrieval scores, tool failure rates, no-answer rate, citation coverage, human escalation, user corrections, and cost or latency patterns.

If a slice grows in traffic, risk, or failure rate but has little eval coverage, the eval set is no longer protecting that area. I would sample production traces from that slice, redact and label them, add representative cases and hard negatives, and then report slice-level metrics in CI and online dashboards.

The key is that representativeness is not static. Eval sets must grow where production behavior changes and where failure impact is highest.

### Active Recall

1. Name five types of drift in GenAI systems.
2. Why is traffic share not the only coverage priority?
3. What is weak-slice expansion?
4. How can retrieval score drift reveal a problem?
5. Why should eval metrics be sliced?

Final takeaway:

> Drift does not only ask "is the model worse?" It asks "is our test coverage still aimed at the real system?"

---

## Subtopic P5.2.d: Keeping Eval Sets Trustworthy as They Scale

> **Subtopic time:** 2h
> Outcome: You should be able to govern eval sets so they remain accurate, non-leaky, representative, reviewable, and useful as they grow.

### Add to Knowledge Base

An eval set can decay.

It decays when:

```text
labels become stale
duplicates inflate scores
training data leaks into evals
expected answers no longer match policy
source docs change
low-quality labels accumulate
easy cases dominate
ownership disappears
```

The mental model:

> Eval sets are production artifacts. They need maintenance, ownership, and change control.

If the eval set is untrustworthy, every optimization built on it is suspect.

---

### 1. Eval Set Governance

Each eval set should have:

```text
owner
purpose
scope
data source
allowed use
privacy classification
labeling rubric
review cadence
version
change log
release-gate role
retirement policy
```

Example:

```text
eval_set: support_rag_gold
purpose: release gate for support RAG answer quality
owner: support-ai-platform
allowed_use: eval only, no training
review_cadence: monthly
minimum_pass_rate: 94%
critical_slice_minimum: 98%
```

---

### 2. Leakage Control

Leakage means eval data contaminates training or prompt examples.

Leakage creates fake improvement.

Prevent leakage by:

```text
separating eval-only and training-allowed datasets
tracking source trace IDs
hashing examples for dedupe
blocking eval examples from fine-tuning data
reviewing prompt few-shot examples
versioning synthetic generation seeds and sources
```

Do not fine-tune on your release-gating gold set.

Keep a held-out set.

---

### 3. Deduplication and Balance

Duplicates can inflate metrics.

Example:

```text
50 near-identical password reset cases
2 cancellation policy cases
```

The aggregate score will overrepresent password reset.

Maintain:

```text
dedupe by exact text hash
dedupe by semantic similarity
cap per intent/source
slice weights
difficulty balance
risk-based sampling
```

Metrics should report:

```text
overall score
slice scores
weighted score
critical failure count
```

---

### 4. Label Audits

Labels drift too.

Audit:

```text
random sample of labels
disagreement between reviewers
cases with frequent model disagreement
cases near pass/fail threshold
cases affected by policy changes
cases affected by source-doc updates
```

Track:

```text
inter-reviewer agreement
label correction rate
stale label count
unknown/ambiguous cases
```

If label quality is weak, model optimization becomes noise chasing.

---

### 5. Practical Interview Question

> Your eval set grew from 500 to 50,000 cases. How do you keep it trustworthy?

### Strong Answer

I would treat the eval set as a governed artifact. It needs an owner, purpose, allowed use, privacy classification, version, change log, labeling rubric, review cadence, and release-gate role. I would separate gold, silver, and bronze tiers so raw production candidates do not silently become release-gating data.

I would control leakage by marking eval-only cases, tracking source IDs, deduping by hashes and semantic similarity, and preventing gold cases from entering fine-tuning or few-shot prompts. I would maintain slice balance so one high-volume easy intent does not dominate the score. I would audit labels regularly, track reviewer agreement, retire stale cases, and update expected answers when source docs or policies change.

At scale, the question is not just "how many eval cases do we have?" It is "can we still trust the score?"

### Active Recall

1. What is eval leakage?
2. Why should gold eval cases not be used for fine-tuning?
3. How do duplicates distort eval metrics?
4. What metadata should every eval set have?
5. Why do labels need audits?

Final takeaway:

> A growing eval set is only an advantage if its labels, coverage, privacy rights, and leakage boundaries stay trustworthy.

---

## Topic P5.3: Closing the Loop With Optimization

> **Topic time:** 6h
> Focus: Deciding which improvement lever to use, avoiding synthetic-data traps, and proving that the flywheel produced a real system improvement.

The flywheel is not complete when data is collected.

It is complete when data changes the system and the change is proven.

The improvement loop:

```text
production signal
-> triage
-> fixture/eval case
-> root-cause diagnosis
-> targeted fix
-> offline eval
-> online rollout
-> measurement
-> new signals
```

The central idea:

> The data flywheel should choose the cheapest effective fix, not automatically fine-tune a model.

Fine-tuning is sometimes right.

Often it is not.

---

## Subtopic P5.3.a: When the Loop Justifies Distillation or Fine-Tuning vs Prompt/Retrieval Fixes

> **Subtopic time:** 2h
> Outcome: You should be able to choose between prompt changes, retrieval fixes, reranking, routing, fine-tuning, and distillation based on the diagnosed failure pattern and available data.

### Add to Knowledge Base

Optimization should match root cause.

The bad habit:

```text
system failed -> fine-tune
```

The mature habit:

```text
system failed -> diagnose layer -> apply cheapest effective fix -> measure
```

The mental model:

> Fine-tuning changes model behavior. It does not repair missing evidence, bad permissions, broken tools, or unclear product requirements.

---

### 1. Fix Decision Table

| Failure Pattern | Best First Fix |
|---|---|
| correct evidence missing | retrieval/chunking/indexing/filtering |
| evidence retrieved but ranked low | reranker or retrieval tuning |
| evidence present but answer ignores it | prompt, context formatting, grounding checks |
| output schema invalid | schema prompting, constrained decoding, parser repair |
| wrong tool called | tool schema, router, approval gate, examples |
| too expensive | caching, routing, context compression, smaller model |
| style inconsistent | prompt or fine-tune if repeated at scale |
| domain terminology misunderstood | better retrieval examples or fine-tune if data is broad |
| small model should mimic expensive model | distillation |
| repeated task-specific reasoning pattern | fine-tune or distill after eval evidence |

Start with system fixes before model surgery.

---

### 2. When Prompt or Retrieval Fixes Are Enough

Use prompt fixes when:

```text
instructions are ambiguous
format is inconsistent
citations are not requested clearly
the model needs better step boundaries
tool-use policy is unclear
```

Use retrieval fixes when:

```text
correct evidence is missing
chunking is poor
metadata filters are wrong
hybrid search is needed
reranking would help
domain synonyms are not covered
```

Use routing fixes when:

```text
task is too hard for current model tier
high-risk tasks need premium route
simple tasks are over-served by expensive model
```

These are usually cheaper and easier to roll back than fine-tuning.

---

### 3. When Fine-Tuning Is Justified

Fine-tuning becomes plausible when:

```text
you have many reviewed examples
the failure is model behavior, not missing context
the desired behavior is stable
prompting has hit diminishing returns
retrieval is already strong
the task has repeated structure
you can evaluate regressions
the improvement justifies training and maintenance cost
```

Good fine-tuning candidates:

```text
domain-specific extraction
stable classification taxonomy
style/format consistency at scale
tool-call argument patterns
specialized reasoning pattern with many labels
```

Weak candidates:

```text
fast-changing facts
missing knowledge
private per-user data
unclear requirements
small number of examples
policy behavior likely to change
```

---

### 4. When Distillation Is Justified

Distillation means using a stronger model or process to train or guide a cheaper/faster model.

Use it when:

```text
premium model works but is too expensive or slow
task volume is high
behavior is stable
teacher outputs can be reviewed or filtered
student can meet quality bar
cost savings exceed training and evaluation cost
```

Distillation is a cost/latency optimization.

It is not a magic quality source.

Teacher mistakes can become student habits.

---

### 5. Practical Interview Question

> Production failures are accumulating. How do you decide whether to fine-tune?

### Strong Answer

I would first classify failures by layer. If the correct evidence is missing, I would fix retrieval, chunking, metadata, filters, or reranking. If evidence is present but unused, I would adjust prompt structure, context formatting, citation requirements, or groundedness checks. If the wrong model tier is being used, I would fix routing. If tool calls are wrong, I would improve tool schemas, examples, permission gates, or workflow control.

Fine-tuning becomes justified only when the failure pattern is truly model behavior, the desired behavior is stable, we have enough reviewed examples, cheaper fixes have plateaued, and we have evals to measure both improvement and regression. Distillation is justified when a premium model solves the task but cost or latency requires moving the behavior into a cheaper model.

I would not fine-tune to fix missing knowledge or broken orchestration. That is expensive misdiagnosis.

### Active Recall

1. Why does fine-tuning not fix missing evidence?
2. When is reranking a better fix than fine-tuning?
3. What data quality is needed before fine-tuning?
4. When is distillation mainly a cost optimization?
5. Why should prompt/retrieval fixes usually come first?

Final takeaway:

> The flywheel earns fine-tuning only after diagnosis shows repeated, stable model-behavior gaps with enough reviewed data and measurable ROI.

---

## Subtopic P5.3.b: Synthetic Data Generation and Curation Pitfalls

> **Subtopic time:** 2h
> Outcome: You should be able to use synthetic data as a targeted supplement while avoiding contamination, unrealistic examples, model self-confirmation, and label hallucination.

### Add to Knowledge Base

Synthetic data is generated data.

It can help with:

```text
coverage expansion
edge-case brainstorming
format variation
class balancing
rare intent simulation
hard-negative creation
teacher-student distillation
```

But it can also harm.

The mental model:

> Synthetic data is a proposal, not ground truth.

It needs curation.

---

### 1. Good Uses

Good synthetic data tasks:

```text
generate paraphrases of reviewed questions
generate hard negatives around known boundaries
generate test cases for schema robustness
generate multilingual variants for human review
generate rare but plausible support scenarios
generate teacher rationales for distillation, then filter
```

Synthetic data is strongest when anchored to real cases.

Example:

```text
real failure:
  user confused refund after 30 days vs 45 days

synthetic expansion:
  variants across products, regions, subscription types, and wording
```

Do not let the generator invent policy facts.

Anchor it to source documents.

---

### 2. Pitfalls

Common pitfalls:

```text
unrealistic user language
overly clean examples
labels generated without source evidence
teacher model hallucinations
duplicates and near-duplicates
overfitting to generator style
eval contamination
bias amplification
policy-inconsistent examples
synthetic examples dominating real examples
```

A synthetic eval set can make the system good at synthetic questions and bad at real users.

That is not improvement.

---

### 3. Curation Rules

Before using synthetic data:

```text
tie each example to a purpose
tag it as synthetic
store generator prompt/model/version
dedupe it
verify labels against source truth
sample for human review
limit synthetic share in gold evals
keep synthetic training separate from held-out real evals
test against real production slices
```

For high-risk domains:

```text
synthetic data can suggest cases
humans or trusted sources must confirm expected behavior
```

---

### 4. Code Sample: Synthetic Case Metadata

```json
{
  "example_id": "syn_refund_boundary_017",
  "source": "synthetic",
  "anchored_to_fixture": "fx_support_refund_001",
  "generator_model": "teacher_model_v3",
  "generator_prompt_version": "hard_negative_gen_v2",
  "human_reviewed": true,
  "allowed_use": ["development_eval", "training_candidate"],
  "not_allowed_use": ["release_gate_gold_without_review"],
  "coverage_tags": ["refund", "boundary_case", "subscription_plan"]
}
```

Synthetic provenance matters.

Without it, you cannot reason about contamination or trust.

---

### 5. Practical Interview Question

> Would you use synthetic data to improve a GenAI assistant?

### Strong Answer

Yes, but only as a targeted supplement. I would use synthetic data to expand around known real failures, create paraphrases, hard negatives, multilingual variants, and rare edge cases. I would anchor generation to real fixtures or source documents so the model does not invent facts.

I would tag every synthetic example with generator model, prompt version, source fixture, allowed use, and review status. I would dedupe examples, verify labels against source truth, and sample for human review. I would not let synthetic data dominate gold evals or contaminate held-out real production evals.

Synthetic data is useful for coverage, but it is not ground truth by default. The final proof still comes from curated evals and real production outcomes.

### Active Recall

1. Why is synthetic data not automatically ground truth?
2. What does it mean to anchor synthetic data?
3. Why can synthetic examples be too clean?
4. What metadata should synthetic examples include?
5. Why should held-out real evals stay separate?

Final takeaway:

> Synthetic data can widen the flywheel, but uncurated synthetic data can also teach the system a fake version of reality.

---

## Subtopic P5.3.c: Measuring Whether the Loop Actually Improved the System

> **Subtopic time:** 2h
> Outcome: You should be able to prove that a data flywheel improved quality, reliability, cost, or safety without hiding regressions behind a single aggregate score.

### Add to Knowledge Base

The flywheel is only real if it improves measured behavior.

Not:

```text
we collected 100k traces
we labeled 5k examples
we fine-tuned a model
```

But:

```text
retrieval failure rate dropped
grounded answer rate improved
cost per successful task improved
human escalation decreased
critical safety regressions stayed zero
weak-slice performance improved
```

The mental model:

> Improvement is a measured change in a meaningful metric under controlled comparison.

---

### 1. Measurement Stack

Use multiple layers:

```text
offline eval:
  fast, repeatable, controlled

shadow eval:
  production traffic replayed without affecting users

canary:
  small real-user exposure

A/B test:
  controlled online comparison

post-launch monitoring:
  continuous regression detection
```

Each layer catches different problems.

Offline evals catch known regressions.

Online tests catch user behavior changes.

Monitoring catches drift.

---

### 2. Metrics

Quality:

```text
task success rate
groundedness
citation correctness
schema validity
tool trajectory correctness
human acceptance
user correction rate
```

Safety:

```text
unsafe output rate
over-refusal rate
under-refusal rate
policy violation rate
secret exposure
cross-tenant leakage
```

Reliability:

```text
timeout rate
fallback rate
retry rate
availability
fixture pass rate
```

Cost/latency:

```text
cost per request
cost per session
cost per successful task
p50/p95 latency
token growth
cache hit rate
```

Coverage:

```text
slice pass rate
critical-case pass rate
new failure categories
drift alerts closed
```

---

### 3. Avoid Aggregate Score Traps

Aggregate improvement can hide slice regression.

Example:

```text
overall pass rate:
  91% -> 94%

Spanish billing slice:
  86% -> 72%
```

This is not an acceptable launch if Spanish billing matters.

Always check:

```text
critical slices
high-risk routes
long-tail languages
premium tenants
newly added regression fixtures
cost and latency guardrails
safety guardrails
```

---

### 4. Before/After Discipline

For every improvement, record:

```text
hypothesis
change made
target metric
guardrail metrics
eval set version
traffic slice
baseline result
post-change result
statistical confidence if online
decision
rollback plan
```

Example:

```text
hypothesis:
  reranker v3 will improve refund-policy groundedness without increasing p95 latency by more than 300ms

target:
  refund slice groundedness +5 points

guardrails:
  p95 latency <= baseline +300ms
  cost/request <= baseline +10%
  safety violations = 0 critical
```

This turns improvement into engineering.

---

### 5. Practical Interview Question

> How do you prove your data flywheel improved a RAG assistant?

### Strong Answer

I would compare a pinned baseline against the new system using versioned eval sets and production metrics. Offline, I would run the gold regression suite, weak-slice suites, hard negatives, safety cases, citation checks, schema checks, and cost/latency estimates. I would require no regression on critical cases and target improvement on the specific failure slice the change was designed to address.

Then I would use shadow traffic or canary rollout to measure real production behavior: task success, user corrections, human escalation, groundedness samples, cost per successful task, p95 latency, fallback rate, and safety violations. I would report results by slice because aggregate scores can hide regressions.

If the change improves target metrics but violates cost, latency, or safety guardrails, I would not ship it broadly. The flywheel is successful only if it produces measurable net improvement without unacceptable regression.

### Active Recall

1. Why is "we labeled more data" not proof of improvement?
2. What is the difference between offline eval and online A/B test?
3. Why must metrics be sliced?
4. What guardrails should accompany a quality improvement?
5. What should every improvement record include?

Final takeaway:

> A data flywheel is only real when captured evidence becomes measured, regression-safe improvement in production behavior.

---

## Module P5 Checkpoint: Data Flywheel and Continuous Improvement Synthesis

> **Checkpoint focus:** Design a privacy-safe capture pipeline, turn production failures into reusable evals, and choose the right optimization lever.

By the end of Pro Module P5, you should be able to:

1. Design a data-capture pipeline that respects privacy and produces reusable eval cases.
2. Explain how production failures become regression fixtures and grow coverage.
3. Decide when the flywheel justifies fine-tuning vs cheaper retrieval/prompt fixes.

---

### 1. The Big Picture

The full flywheel:

```text
production usage
-> safe trace capture
-> feedback and outcome signals
-> privacy filtering and redaction
-> triage queues
-> reviewed labels
-> fixtures and eval sets
-> root-cause diagnosis
-> targeted optimization
-> offline eval gates
-> online rollout
-> measurement
-> new production signals
```

The important idea:

> A data flywheel is not a logging pipeline. It is a learning system with privacy, evaluation, release, and measurement discipline.

If any link is weak, the flywheel breaks:

```text
no safe capture -> no usable data
no labels -> no evals
no fixtures -> failures recur
no diagnosis -> wrong fixes
no measurement -> fake improvement
no privacy controls -> governance failure
```

---

### 2. Privacy-Safe Capture Pipeline

Architecture:

```text
1. Application emits trace event.
2. Capture policy checks consent, tenant policy, data category, region, and purpose.
3. Sensitive content is redacted, tokenized, or excluded.
4. Metadata goes to analytics store.
5. Redacted content goes to review/eval candidate store.
6. Raw content, if allowed at all, goes to encrypted short-retention restricted store.
7. Outcome signals are joined later.
8. Candidate cases enter triage queues.
9. Approved cases become fixtures or eval examples.
10. Lineage links artifacts back to trace IDs and deletion obligations.
```

Key design principles:

```text
data minimization
purpose limitation
consent enforcement
role-based access
redaction before broad storage
short raw retention
lineage for deletion
audit logs
```

Interview sentence:

> I would rather have a smaller, privacy-safe, reviewable dataset than a huge trace lake nobody is allowed to use.

---

### 3. Production Failure to Regression Fixture

Flow:

```text
1. Detect failure through feedback, metric, user report, red-team run, or incident.
2. Pull trace and dependency metadata.
3. Classify root failure: retrieval, prompt, model, tool, safety, schema, latency, cost, or orchestration.
4. Redact and minimize content.
5. Freeze retrieval snapshot, prompt/model/config versions, tool mocks, and policy version.
6. Define expected behavior, required evidence, forbidden behavior, and grader.
7. Review and approve fixture.
8. Add fixture to regression suite.
9. Confirm failing system fails the fixture.
10. Apply fix.
11. Confirm new system passes fixture without regressing existing suites.
```

The conversion:

```text
bad production event -> reusable behavioral requirement
```

This is how the system accumulates scar tissue in a good way.

---

### 4. Growing Eval Coverage

Eval growth should be guided by:

```text
high-impact failures
high-volume failures
high-risk routes
drifted traffic slices
weak-slice metrics
hard negatives
new product behavior
human escalation themes
```

Not:

```text
whatever logs are easiest to label
```

Coverage questions:

```text
Which user intents are under-tested?
Which languages are under-tested?
Which tenants or risk tiers are under-tested?
Which retrieval boundaries are under-tested?
Which tool actions are under-tested?
Which failure types have no regression fixtures?
Which slices are high risk despite low traffic?
```

Good flywheels grow in the direction of weakness.

---

### 5. Fine-Tuning Decision Framework

Use this order:

```text
1. Is the requirement clear?
2. Is the failure reproducible?
3. Is the root cause known?
4. Can deterministic logic fix it?
5. Can retrieval/chunking/reranking fix it?
6. Can prompt/context/schema/tool design fix it?
7. Can routing to another existing model fix it?
8. Do we have enough reviewed examples?
9. Is the desired behavior stable?
10. Do evals prove fine-tuning/distillation improves the target without regressions?
```

Fine-tune when:

```text
repeated stable behavior gap
many reviewed examples
prompt/retrieval fixes plateaued
model behavior is the bottleneck
ROI justifies maintenance
regression evals are strong
```

Distill when:

```text
strong teacher works
cost/latency is too high
task is high-volume
student can meet quality threshold
teacher outputs are filtered and reviewed
```

Do not fine-tune when:

```text
evidence is missing
source data changes frequently
permissions are wrong
tools are broken
labels are noisy
requirements are unstable
you have no eval gate
```

---

### 6. Checkpoint Scenario

Scenario:

```text
An enterprise support assistant has a rising escalation rate in billing questions.
Users often downvote answers about annual-plan refunds.
The system sometimes cites monthly-plan policy for annual-plan questions.
```

Good flywheel response:

```text
1. Capture affected traces with privacy-safe metadata and redacted content.
2. Join outcome signals: downvotes, retries, escalations, corrections.
3. Triage as billing/refund/plan-boundary failures.
4. Build fixtures with annual vs monthly hard negatives.
5. Freeze retrieval snapshots and expected citations.
6. Diagnose root cause:
   - if annual policy chunk missing -> ingestion/chunking fix
   - if retrieved but ranked low -> reranker/search fix
   - if retrieved but ignored -> prompt/grounding fix
   - if repeated terminology misunderstanding remains -> consider fine-tune
7. Add cases to billing refund slice in eval.
8. Run offline eval and canary.
9. Measure escalation rate, groundedness, citation correctness, cost, and latency.
```

This is the mature answer because it does not jump to fine-tuning.

---

### 7. Interview-Ready Answer

> Design a data flywheel for a production GenAI assistant.

I would design the flywheel as a privacy-safe learning pipeline. The production system emits structured traces with route, tenant, task type, prompt/config versions, retrieval fingerprints, tool calls, model outputs, safety labels, cost, latency, and outcome signals. Before storage, each trace passes a capture policy for consent, tenant rules, data category, region, and purpose. Raw content is minimized, redacted, encrypted, and short-retention; approved redacted traces can enter triage.

From there, feedback and failures become candidate cases. Reviewers classify failures by layer, label task type, risk, expected behavior, required evidence, and forbidden behavior. High-quality reviewed cases become golden evals. Production failures become reproducible fixtures by freezing input, retrieval snapshots, tool mocks, prompt/model/config versions, expected behavior, and graders. This turns incidents into regression coverage.

The loop then chooses the cheapest effective fix. Retrieval failures get retrieval fixes. Context or citation failures get prompt/context/reranking fixes. Tool failures get schema or workflow fixes. Fine-tuning is justified only when the root cause is stable model behavior, we have enough reviewed examples, cheaper fixes have plateaued, and evals prove improvement without regressions. Distillation is justified when a strong teacher works but cost or latency demands a cheaper student.

Finally, I would prove the flywheel works with offline evals, shadow or canary tests, and online metrics by slice: task success, groundedness, citation correctness, safety, cost per successful task, p95 latency, escalation rate, and regression fixture pass rate.

---

### 8. Active Recall

1. What must a trace capture to become useful for eval creation?
2. Why is raw production data not automatically training data?
3. How do explicit and implicit feedback differ?
4. What makes a production failure reproducible?
5. What is the difference between gold, silver, and bronze datasets?
6. Why are hard negatives important?
7. What types of drift should trigger eval expansion?
8. How do you prevent eval leakage?
9. When is fine-tuning justified?
10. How do you prove the flywheel improved production behavior?

---

### 9. Final Checkpoint Summary

- One-line summary: A data flywheel turns safe production evidence into eval coverage, targeted fixes, and measured improvement.
- Three keywords: safe capture, regression fixtures, cheapest effective fix.
- One interview trap: saying "we will fine-tune on user logs" before discussing consent, redaction, labeling, eval leakage, and root-cause diagnosis.
- One memory trick: trace the failure, fixture the failure, fix the layer, measure the result.

Final takeaway:

> P5 is the module where GenAI quality becomes compounding. The model is not the moat by itself; the privacy-safe learning loop around the model is what gets stronger over time.
