# Pro Module P2 - LLMOps And Deployment Lifecycle

> **Module time:** 26h
> **Why this module matters:** In real teams, the dangerous part is not writing a prompt, it is changing one in production without breaking users. This module is the release-engineering discipline that the canon's evaluation module hints at but does not fully operationalize.

---

## Quick Topic Index

| # | Subtopic | Status |
|---|----------|--------|
| **Topic P2.1** | **Versioning, registries, and reproducibility (8h)** | |
| P2.1.a | Versioning prompts, models, datasets, and eval sets together | Done |
| P2.1.b | Model and prompt registries: promotion stages and metadata | Done |
| P2.1.c | Reproducible runs: pinning model versions, seeds, and configs | Done |
| P2.1.d | Environment parity: dev, staging, and prod for GenAI systems | Done |
| **Topic P2.2** | **Safe deployment strategies (10h)** | |
| P2.2.a | Offline eval gates as a merge requirement | Done |
| P2.2.b | Canary, shadow (mirror), and blue-green deployments for LLM changes | Done |
| P2.2.c | Online A/B testing and guardrail metrics with statistical significance | Done |
| P2.2.d | Automated rollback triggers on quality, latency, cost, and safety regressions | Done |
| **Topic P2.3** | **CI/CD and operational maturity (8h)** | |
| P2.3.a | Building a prompt/model CI pipeline (lint, eval, regression, gate) | Done |
| P2.3.b | Feature flags and dynamic config for fast, reversible changes | Done |
| P2.3.c | Incident response runbooks for GenAI services | Done |
| P2.3.d | Change management and approval flows for high-risk model updates | Done |
| **Module checkpoint** | LLMOps and deployment lifecycle synthesis | Done |

**Covered so far:**
- P2.1.a - Versioning prompts, models, datasets, and eval sets together: artifact bundle mental model, prompt/model/dataset/eval coupling, semantic versions, immutable IDs, lineage, release manifests, traceability, rollback, diff review, failure modes, manifest example, lab, active recall, and interview answer.
- P2.1.b - Model and prompt registries: promotion stages and metadata: registry as control plane, artifact metadata, dev/staging/prod promotion, approval state, ownership, risk labels, lifecycle, registry schema, anti-patterns, lab, active recall, and interview answer.
- P2.1.c - Reproducible runs: pinning model versions, seeds, and configs: reproducibility contract, model/provider pinning, seeds and nondeterminism limits, decoding configs, tool/retrieval pins, environment capture, replay bundles, failure modes, reproducible run record, lab, active recall, and interview answer.
- P2.1.d - Environment parity: dev, staging, and prod for GenAI systems: parity mental model, data/prompt/model/config/tool/provider differences, fixture parity, secret isolation, staging traffic, environment drift, smoke tests, parity checklist, lab, active recall, and interview answer.
- P2.2.a - Offline eval gates as a merge requirement: eval gate mental model, merge-blocking thresholds, regression suites, slice metrics, golden fixtures, safety gates, statistical confidence, CI integration, gate result schema, lab, active recall, and interview answer.
- P2.2.b - Canary, shadow, and blue-green deployments for LLM changes: release strategy comparison, traffic splitting, mirrored evaluation, instant rollback, stateful conversation risks, guardrail metrics, staged rollout plans, lab, active recall, and interview answer.
- P2.2.c - Online A/B testing and guardrail metrics with statistical significance: experiment design, randomization unit, primary/guardrail metrics, sequential testing risks, sample size intuition, heterogeneous treatment effects, safety constraints, lab, active recall, and interview answer.
- P2.2.d - Automated rollback triggers on quality, latency, cost, and safety regressions: rollback as safety mechanism, threshold design, burn-rate alerts, model/prompt rollback, feature flag rollback, human approval boundaries, runbooks, lab, active recall, and interview answer.
- P2.3.a - Building a prompt/model CI pipeline: lint, eval, regression, gate: CI pipeline stages, prompt linting, schema tests, retrieval fixtures, eval execution, report generation, merge checks, code sample, lab, active recall, and interview answer.
- P2.3.b - Feature flags and dynamic config for fast, reversible changes: config control plane, routing flags, model tiers, prompt versions, kill switches, tenant targeting, auditability, rollback, lab, active recall, and interview answer.
- P2.3.c - Incident response runbooks for GenAI services: incident taxonomy, triage, mitigation, trace collection, rollback, customer comms, postmortem, runbook template, lab, active recall, and interview answer.
- P2.3.d - Change management and approval flows for high-risk model updates: risk-tiered change control, approval packets, separation of duties, audit trail, regulated workflows, emergency change path, lab, active recall, and interview answer.
- Module checkpoint - LLMOps and deployment lifecycle synthesis: eval-gated prompt deployment pipeline, canary/shadow/blue-green comparison, automated rollback thresholds, release manifest, production readiness checklist, checkpoint scenario, active recall, and interview-ready LLMOps defense.

---

## Topic P2.1: Versioning, Registries, and Reproducibility

> **Topic time:** 8h
> Focus: Making GenAI changes traceable, reviewable, reproducible, and rollback-safe by versioning every artifact that can affect behavior.

LLMOps starts with a blunt reality:

```text
If you cannot say exactly what changed, you cannot safely deploy, debug, or roll back.
```

In traditional software, code changes drive behavior.

In GenAI systems, behavior can change because of:

```text
prompt text
model version
model provider
temperature
tool schema
retrieval config
dataset version
eval set version
reranker version
policy config
output parser
feature flag
```

The central idea:

> GenAI release engineering treats prompts, models, datasets, evals, configs, and tools as one versioned behavioral system.

---

## Subtopic P2.1.a: Versioning Prompts, Models, Datasets, and Eval Sets Together

> **Subtopic time:** 2h
> Outcome: You should be able to explain why versioning a prompt alone is insufficient and design a release manifest that links prompt, model, dataset, eval, config, and policy versions.

### Add to Knowledge Base

A prompt version by itself is not enough.

The same prompt can behave differently with:

```text
different model
different temperature
different retrieval config
different tool schema
different policy rules
different examples
different parser
different eval data
```

The central mental model:

> A GenAI release is an artifact bundle, not a single prompt string.

If a production answer regresses, you need to know:

```text
which prompt ran
which model ran
which retrieval config ran
which dataset/eval approved the change
which tool schema was exposed
which policy version was active
which feature flag routed the request
```

---

### 1. What Must Be Versioned

| Artifact | Why It Matters |
|---|---|
| prompt template | changes instruction contract |
| model/provider | changes capability and behavior |
| decoding config | changes determinism, creativity, length |
| dataset | changes what examples/evals mean |
| eval set | changes gate criteria |
| retriever config | changes evidence |
| tool schemas | changes available actions |
| output schema/parser | changes validation surface |
| safety policy | changes allowed behavior |
| feature flag config | changes routing |

Do not version only what engineers edit manually.

Version everything that can change output behavior.

---

### 2. Release Manifest

A release manifest is the source of truth for one deployed behavior.

Example:

```yaml
release_id: support-rag-2026-06-26.1
owner: genai-platform
risk_tier: medium
prompt:
  name: support_answer_prompt
  version: 3.4.1
model:
  provider: openai
  name: gpt-x
  version: pinned-2026-06
decoding:
  temperature: 0.2
  max_output_tokens: 600
retrieval:
  chunker_version: 2.1.0
  embedding_model: text-embed-v4
  vector_index: support_docs_2026_06_20
  top_k: 12
  reranker: reranker-v2.3
tools:
  schema_version: support_tools_1.8
policy:
  safety_policy_version: 2026-06-01
evals:
  eval_suite: support_rag_regression
  eval_set_version: 2026-06-24
  required_pass_rate: 0.92
rollout:
  strategy: canary
  initial_percentage: 5
```

This manifest lets you:

```text
review
deploy
reproduce
compare
rollback
audit
```

---

### 3. Versioning Mistakes

| Mistake | Why It Breaks |
|---|---|
| prompt stored only in code comments | cannot audit or rollback cleanly |
| eval set changes without version bump | old pass rate becomes meaningless |
| model alias not pinned | provider update changes behavior silently |
| tool schema unversioned | model output no longer matches tools |
| retrieval index untracked | answer changes without prompt change |
| no release manifest | incident review becomes archaeology |

---

### 4. Practical Interview Question

> A prompt change passed tests last week, but this week the same prompt produces worse answers. What could have changed, and how would versioning help?

### Strong Answer

I would not assume the prompt is the only variable. The model alias, decoding config, retrieval index, embedding model, reranker, tool schema, policy config, or eval set may have changed. I would require every deployed behavior to have a release manifest tying prompt, model, configs, datasets, evals, tools, and policies together. Then I can compare the current manifest against last week's manifest, reproduce both runs, identify the changed artifact, and roll back the behavior bundle rather than guessing.

### Active Recall

1. Why is a prompt version alone insufficient?
2. What artifacts should be in a GenAI release manifest?
3. Why should eval sets be versioned?
4. Why are model aliases risky?
5. What does a release manifest enable?

Final takeaway:

> Version the behavioral bundle, not just the prompt; production GenAI behavior is the product of prompt, model, data, retrieval, tools, policy, and config together.

---

## Subtopic P2.1.b: Model and Prompt Registries - Promotion Stages and Metadata

> **Subtopic time:** 2h
> Outcome: You should be able to design a registry that stores prompt/model artifacts, metadata, ownership, risk labels, evaluation status, and promotion stage.

### Add to Knowledge Base

A registry is a control plane for behavioral artifacts.

It answers:

```text
What artifacts exist?
Who owns them?
What stage are they in?
What evals passed?
What risks are attached?
Where are they deployed?
Can they be promoted?
Can they be rolled back?
```

The central mental model:

> A registry makes model and prompt changes reviewable assets instead of hidden strings and dashboard toggles.

---

### 1. Promotion Stages

Typical stages:

```text
draft
dev
candidate
staging
canary
production
deprecated
archived
blocked
```

Promotion should require evidence.

Example:

```text
draft -> candidate:
  owner and changelog present

candidate -> staging:
  offline eval gate passes

staging -> canary:
  approval and shadow results pass

canary -> production:
  online guardrails stable
```

---

### 2. Registry Metadata

Prompt metadata:

```text
prompt_id
version
owner
task
risk_tier
input schema
output schema
tool schema compatibility
retrieval dependency
eval suite
changelog
approval status
```

Model metadata:

```text
model_id
provider
version or digest
context window
cost
latency profile
supported tools/JSON modes
security/privacy constraints
approved task tiers
fallback tier
deprecation date
```

Registry metadata should be queryable.

You should be able to ask:

```text
Which production prompts use this model?
Which high-risk workflows use this policy?
Which artifacts failed eval gate?
What is the latest approved rollback target?
```

---

### 3. Registry Schema Sketch

```json
{
  "artifact_id": "support_answer_prompt",
  "artifact_type": "prompt",
  "version": "3.4.1",
  "stage": "canary",
  "owner": "support-ai",
  "risk_tier": "medium",
  "compatible_models": ["gpt-x:pinned-2026-06", "local-8b:v12"],
  "input_schema": "support_query_v2",
  "output_schema": "grounded_answer_v3",
  "eval_results": {
    "suite": "support_rag_regression",
    "version": "2026-06-24",
    "pass_rate": 0.94,
    "safety_failures": 0
  },
  "approvals": ["ml_lead", "support_owner"],
  "created_at": "2026-06-26T09:00:00Z"
}
```

---

### 4. Practical Interview Question

> Why do model and prompt registries matter if prompts already live in Git?

### Strong Answer

Git is good for code review and history, but a registry adds operational state and metadata: stage, owner, risk tier, eval status, compatible models, active deployments, approvals, rollback targets, and deprecation. The registry connects artifact identity to release operations. A prompt can live in Git, but the registry says whether that prompt version is approved for staging, canary, or production and under which model/config/eval evidence.

### Active Recall

1. What does a registry control?
2. Name common promotion stages.
3. What metadata belongs on a prompt artifact?
4. What metadata belongs on a model artifact?
5. Why is stage separate from version?

Final takeaway:

> A registry turns prompts and models into governed deployment artifacts with ownership, metadata, stage, approvals, eval evidence, and rollback identity.

---

## Subtopic P2.1.c: Reproducible Runs - Pinning Model Versions, Seeds, and Configs

> **Subtopic time:** 2h
> Outcome: You should be able to design a run record that makes GenAI behavior replayable enough for debugging, evals, audit, and incident response.

### Add to Knowledge Base

Reproducibility in GenAI is not perfect determinism.

Even with the same inputs, providers and GPU kernels may produce small variation.

But production systems still need reproducible-enough runs.

The central mental model:

> Reproducibility means capturing enough context to explain, replay, compare, and debug behavior.

---

### 1. What to Pin

```text
model provider
model version or digest
prompt version
system/developer messages
tool schema version
retrieval index version
retrieved chunk IDs
reranker version
decoding parameters
random seed when supported
output schema version
policy version
feature flags
environment
code commit SHA
```

If it can change output, pin it or record it.

---

### 2. Seeds and Nondeterminism

Seeds help, but they do not solve everything.

Nondeterminism can come from:

```text
provider model updates
sampling
floating-point kernels
parallel execution
retrieval index changes
tool data changes
time-dependent prompts
feature flags
external APIs
```

For high-stakes evals:

```text
use low temperature
pin model/version
freeze retrieval corpus
record retrieved context
use deterministic parsers
repeat runs when needed
compare distributions, not one sample only
```

---

### 3. Run Record

```json
{
  "run_id": "run_123",
  "release_id": "support-rag-2026-06-26.1",
  "code_commit": "abc123",
  "model": {"provider": "openai", "name": "gpt-x", "version": "pinned-2026-06"},
  "prompt_version": "3.4.1",
  "decoding": {"temperature": 0.2, "seed": 42, "max_tokens": 600},
  "retrieval": {
    "index_version": "support_docs_2026_06_20",
    "chunk_ids": ["c101", "c205"],
    "reranker_version": "2.3"
  },
  "tool_schema_version": "support_tools_1.8",
  "policy_version": "2026-06-01",
  "feature_flags": {"new_refusal_policy": true},
  "environment": "staging"
}
```

---

### 4. Practical Interview Question

> An eval passed in CI but failed in staging. How would reproducible run records help?

### Strong Answer

I would compare the CI run record with the staging run record. I would check model version, prompt version, decoding parameters, retrieval index, retrieved chunk IDs, tool schema, policy version, feature flags, and code commit. If the eval failed because staging used a different retrieval index or model alias, the run record exposes it. If all artifacts match, then I would investigate nondeterminism, environment differences, or external tool data.

### Active Recall

1. Why is GenAI reproducibility harder than normal code reproducibility?
2. What should a run record include?
3. Why are seeds insufficient alone?
4. Why record retrieved chunk IDs?
5. Why pin model versions?

Final takeaway:

> Reproducibility is not a promise that every token is identical; it is a disciplined record of every artifact and config needed to replay, compare, and explain behavior.

---

## Subtopic P2.1.d: Environment Parity - Dev, Staging, and Prod for GenAI Systems

> **Subtopic time:** 2h
> Outcome: You should be able to explain how dev/staging/prod drift breaks GenAI releases and design parity checks that catch environment-specific failures.

### Add to Knowledge Base

Environment parity means:

```text
the same release behaves the same way across dev, staging, and production unless differences are intentional, documented, and tested
```

GenAI environment drift can hide in:

```text
model aliases
retrieval indexes
feature flags
tool mocks
policy configs
secret scopes
rate limits
provider regions
tenant data
eval fixtures
output schemas
```

The central mental model:

> Staging is only useful if it fails like production.

---

### 1. Parity Dimensions

| Dimension | Drift Example |
|---|---|
| model | staging uses older model alias |
| prompt/config | feature flag differs |
| retrieval | staging index is stale |
| tools | dev uses mocks, prod uses live APIs |
| policy | prod safety policy stricter |
| data | staging lacks tenant permissions |
| latency | staging has no production load |
| secrets | prod access denied due to different scope |

Parity does not require identical data.

It requires representative behavior and explicit differences.

---

### 2. Parity Checklist

```text
[ ] Same release manifest can deploy to each environment.
[ ] Environment-specific values are isolated in config.
[ ] Model versions are pinned or differences documented.
[ ] Retrieval index versions are visible.
[ ] Tool mocks match live schemas and error modes.
[ ] Policy versions are visible.
[ ] Feature flags are exported and auditable.
[ ] Staging has representative fixtures.
[ ] Smoke tests cover retrieval, tools, schemas, and safety.
[ ] Load tests simulate production latency pressure.
```

---

### 3. Practical Interview Question

> A prompt works in staging but fails in production. What environment differences would you inspect?

### Strong Answer

I would compare release manifests and run records across environments. I would inspect model aliases, prompt versions, feature flags, retrieval index versions, tool schemas, policy configs, secrets, tenant permissions, rate limits, and data shape. I would also check whether staging used mocks that did not reproduce production tool errors or latency. The fix is to make environment differences explicit, versioned, and covered by smoke tests and representative fixtures.

### Active Recall

1. What is environment parity?
2. Why can staging lie?
3. Name five GenAI-specific drift sources.
4. Why are tool mocks dangerous?
5. What should a parity smoke test cover?

Final takeaway:

> Environment parity is release realism: staging must exercise the same models, configs, schemas, retrieval behavior, policies, and failure modes that production will use.

---

## Topic P2.2: Safe Deployment Strategies

> **Topic time:** 10h
> Focus: Moving GenAI changes toward production with eval gates, controlled exposure, online metrics, and automated rollback.

Safe deployment starts from one belief:

```text
Any prompt, model, retrieval, policy, or tool change can be a production behavior change.
```

The central idea:

> GenAI deployments need both offline evidence before merge and online guardrails after release.

---

## Subtopic P2.2.a: Offline Eval Gates as a Merge Requirement

> **Subtopic time:** 2.5h
> Outcome: You should be able to design CI merge gates that block unsafe prompt/model/config changes before they reach production.

### Add to Knowledge Base

An offline eval gate is a merge-blocking test suite for GenAI behavior.

It checks:

```text
does this change improve or preserve expected behavior on known cases?
does it regress important slices?
does it violate safety, schema, latency, or cost constraints?
```

The central mental model:

> If a prompt change can break users, it deserves a merge gate like code.

---

### 1. What an Eval Gate Tests

| Gate | Example |
|---|---|
| quality | answer correctness, groundedness, task success |
| safety | policy violations, unsafe completions |
| schema | JSON validity, required fields |
| retrieval | expected evidence found |
| tool use | correct tool and arguments |
| regression | old fixed bugs stay fixed |
| latency/cost | token and runtime budgets |
| slices | tenant/domain/language/risk category |

Gate thresholds should be explicit:

```text
overall pass rate >= 92 percent
critical safety failures = 0
schema validity >= 99 percent
unsupported claim rate <= 2 percent
no regression on P0 fixtures
cost increase <= 10 percent
```

---

### 2. Gate Result Schema

```json
{
  "change_id": "pr_842",
  "release_candidate": "support_prompt_3.5.0",
  "eval_suite": "support_regression_2026_06",
  "overall_pass_rate": 0.94,
  "critical_failures": 0,
  "schema_validity": 0.995,
  "unsupported_claim_rate": 0.012,
  "cost_delta": 0.06,
  "decision": "pass"
}
```

---

### 3. Code Sample: Merge Gate Decision

```python
def eval_gate(result: dict) -> tuple[bool, list[str]]:
    reasons = []
    if result["overall_pass_rate"] < 0.92:
        reasons.append("overall_pass_rate_below_threshold")
    if result["critical_failures"] > 0:
        reasons.append("critical_failures_present")
    if result["schema_validity"] < 0.99:
        reasons.append("schema_validity_below_threshold")
    if result["unsupported_claim_rate"] > 0.02:
        reasons.append("unsupported_claim_rate_too_high")
    if result["cost_delta"] > 0.10:
        reasons.append("cost_delta_too_high")
    return len(reasons) == 0, reasons
```

---

### 4. Practical Interview Question

> How do you prevent a prompt change from reaching production if it breaks known behavior?

### Strong Answer

I would require every prompt/model/config change to run an offline eval gate in CI before merge. The gate would use versioned eval sets and compare the candidate against the current production baseline on quality, safety, schema validity, retrieval grounding, tool-call correctness, latency, and cost. Critical safety failures or P0 regression fixtures should block merge regardless of aggregate score. The gate output should be a structured report attached to the PR, and the release manifest should record the eval suite and result that approved the artifact.

### Active Recall

1. What is an offline eval gate?
2. Why should evals block merge?
3. What is a P0 regression fixture?
4. Why are slice metrics important?
5. What should always block release?

Final takeaway:

> Offline eval gates turn prompt and model changes into reviewable software changes with measurable pass/fail criteria before users are exposed.

---

## Subtopic P2.2.b: Canary, Shadow, and Blue-Green Deployments for LLM Changes

> **Subtopic time:** 2.5h
> Outcome: You should be able to compare deployment strategies and choose the right rollout pattern for an LLM prompt/model/retrieval change.

### Add to Knowledge Base

Offline evals reduce risk.

They do not eliminate production risk.

Online deployment strategies control exposure.

The three core patterns:

```text
canary
shadow / mirror
blue-green
```

The central mental model:

> Canary exposes a few real users. Shadow observes real traffic without user impact. Blue-green swaps environments for fast cutover and rollback.

---

### 1. Canary

Canary sends a small percentage of real traffic to the new version.

Use when:

```text
offline eval passed
user impact is acceptable at small percentage
you need real-world feedback
rollout can be gradual
```

Watch:

```text
quality
latency
cost
safety
user feedback
tool errors
escalation rate
```

---

### 2. Shadow / Mirror

Shadow sends production inputs to the new version but does not show its outputs to users.

Use when:

```text
change is risky
you want real traffic distribution
you can afford duplicate inference cost
outputs can be evaluated offline
side effects are disabled
```

Important:

```text
shadow must not execute external side effects
shadow outputs must not reach users
shadow logs must respect privacy
```

---

### 3. Blue-Green

Blue-green keeps two environments:

```text
blue = current production
green = new candidate
```

Traffic switches from blue to green when ready.

Use when:

```text
you need fast cutover
rollback must be quick
infrastructure environments can be duplicated
state compatibility is managed
```

Watch-outs:

```text
conversation state compatibility
cache compatibility
index/schema compatibility
feature flags
tool side effects
```

---

### 4. Strategy Matrix

| Strategy | Best For | Main Risk |
|---|---|---|
| canary | gradual real-user rollout | small group sees bad behavior |
| shadow | high-risk behavior observation | extra cost and privacy/logging risk |
| blue-green | fast cutover/rollback | state and environment compatibility |

---

### 5. Practical Interview Question

> When would you use canary vs shadow vs blue-green for an LLM deployment?

### Strong Answer

I would use shadow deployment when I want to test the new prompt/model against real traffic without user impact, especially for risky or uncertain changes. I would disable side effects and evaluate shadow outputs with offline or human review. I would use canary after offline gates pass and I am ready to expose a small percentage of real users while monitoring quality, safety, latency, cost, and escalation rate. I would use blue-green when I need a fast environment-level cutover and rollback, but I would verify conversation state, caches, indexes, and tool compatibility before switching.

### Active Recall

1. What is canary deployment?
2. What is shadow deployment?
3. What is blue-green deployment?
4. Why must shadow disable side effects?
5. What metrics should canary monitor?

Final takeaway:

> Safe LLM deployment chooses exposure level deliberately: shadow to observe, canary to learn with limited user impact, blue-green to cut over and roll back quickly.

---

## Subtopic P2.2.c: Online A/B Testing and Guardrail Metrics With Statistical Significance

> **Subtopic time:** 2.5h
> Outcome: You should be able to design online experiments that measure product improvement while protecting safety, latency, cost, and quality.

### Add to Knowledge Base

Online A/B testing answers:

```text
Does the new version improve real user outcomes?
```

Guardrail metrics answer:

```text
Does it harm anything we cannot afford to harm?
```

The central mental model:

> A/B tests optimize product outcomes only inside guardrail boundaries.

---

### 1. Experiment Design

Define:

```text
hypothesis
unit of randomization
control version
treatment version
primary metric
guardrail metrics
minimum detectable effect
sample size
duration
stop rules
slice analysis
```

Randomization unit matters:

```text
per request can contaminate conversation experience
per user/session is often safer
per tenant may be required for enterprise settings
```

---

### 2. Metrics

Primary metrics:

```text
task success
resolution rate
deflection rate
conversion
user satisfaction
human approval rate
```

Guardrail metrics:

```text
safety violation rate
unsupported claim rate
latency p95
cost per successful task
escalation rate
tool error rate
schema failure rate
complaint rate
```

Do not ship a lift in task success if safety or cost explodes.

---

### 3. Statistical Cautions

Watch for:

```text
small sample sizes
peeking too often
multiple comparisons
novelty effects
seasonality
tenant mix imbalance
survivorship bias
manual labels with drift
```

Do not declare victory from a tiny uplift on noisy metrics.

Use confidence intervals and predeclared stop rules.

---

### 4. Practical Interview Question

> Your new prompt improves thumbs-up rate by 2 percent but increases latency and safety escalations. Do you ship it?

### Strong Answer

Not automatically. I would check whether the thumbs-up lift is statistically significant, whether the randomization unit is valid, and whether the improvement holds across important slices. Then I would inspect guardrails: p95 latency, cost per successful task, safety escalation rate, unsupported claims, and tool errors. If safety escalations exceed threshold or latency violates SLO, I would not ship broadly even if the primary metric improves. I might revise the prompt, narrow rollout to safe slices, or run another canary with stricter gates.

### Active Recall

1. What is the difference between primary and guardrail metrics?
2. Why does randomization unit matter?
3. Why is peeking risky?
4. What is a minimum detectable effect?
5. Why can an A/B win still fail rollout?

Final takeaway:

> Online experiments are not "winner takes all"; the treatment must improve the primary metric while staying inside safety, latency, cost, and quality guardrails.

---

## Subtopic P2.2.d: Automated Rollback Triggers on Quality, Latency, Cost, and Safety Regressions

> **Subtopic time:** 2.5h
> Outcome: You should be able to define concrete rollback triggers that automatically stop or reverse bad GenAI deployments before incidents grow.

### Add to Knowledge Base

Rollback is not failure.

Rollback is part of safe release engineering.

The central mental model:

> If you can deploy dynamically, you must be able to undeploy dynamically.

Automated rollback protects against:

```text
quality regressions
safety spikes
latency violations
cost explosions
tool errors
schema failures
retrieval failures
unexpected refusals
```

---

### 1. Trigger Types

Quality:

```text
unsupported claim rate > 3 percent for 15 minutes
human override rate doubles baseline
task success drops 5 percent
```

Safety:

```text
critical policy violation > 0
PII leakage detector fires
unsafe tool call attempt rate exceeds threshold
```

Latency:

```text
p95 latency > 8s for 10 minutes
TTFT p95 increases 50 percent
timeout rate > 2 percent
```

Cost:

```text
cost per successful task rises 25 percent
output tokens/request doubles
fallback/retry rate exceeds budget
```

---

### 2. Rollback Actions

```text
disable feature flag
route back to prior prompt/model
reduce rollout percentage to 0
switch fallback provider
disable risky tool
fail closed for high-risk route
freeze deployment
page owner
open incident
```

Rollback should be tested.

If rollback requires manual archaeology, it will be too slow.

---

### 3. Practical Interview Question

> What automated rollback triggers would you define for a prompt/model release?

### Strong Answer

I would define triggers across quality, latency, cost, and safety. Examples: rollback immediately on any critical safety violation, PII leak, unauthorized tool call, or schema failure in a high-risk route. Roll back or pause canary if p95 latency exceeds SLO for a sustained window, timeout rate crosses threshold, cost per successful task rises beyond budget, unsupported claim rate exceeds baseline, human override rate spikes, or tool error rate increases. The rollback action should be automated through feature flags or registry stage changes, and the release manifest should identify the previous known-good artifact.

### Active Recall

1. Why is rollback part of release design?
2. Name quality rollback triggers.
3. Name safety rollback triggers.
4. Name latency rollback triggers.
5. Name cost rollback triggers.
6. Why should rollback use feature flags or registry stages?

Final takeaway:

> Automated rollback turns observability into protection: when measurable quality, latency, cost, or safety budgets burn too fast, the system reverts before users absorb the full blast radius.

---

## Topic P2.3: CI/CD and Operational Maturity

> **Topic time:** 8h
> Focus: Turning GenAI release practices into repeatable pipelines, reversible configuration, incident runbooks, and approval-controlled change management.

The central idea:

> Mature LLMOps makes GenAI behavior changes as reviewable, testable, reversible, and auditable as code changes.

---

## Subtopic P2.3.a: Building a Prompt/Model CI Pipeline - Lint, Eval, Regression, Gate

> **Subtopic time:** 2h
> Outcome: You should be able to describe a CI pipeline that catches prompt/model regressions before merge.

### Add to Knowledge Base

Pipeline stages:

```text
lint
unit fixtures
schema validation
retrieval fixture tests
offline eval suite
safety evals
cost/latency budget check
regression comparison
approval gate
artifact registration
```

The central mental model:

> CI for GenAI tests behavior contracts, not just syntax.

---

### 1. Pipeline Example

```text
PR opened
-> prompt/config lint
-> render prompt snapshots
-> run golden fixtures
-> run eval suite
-> compare against production baseline
-> generate report
-> block or approve merge
-> register candidate artifact
```

Prompt lint can check:

```text
missing variables
unescaped braces
schema mismatch
forbidden secrets
ambiguous output instructions
missing refusal path
tool names out of date
```

---

### 2. Code Sample: CI Gate Skeleton

```python
def ci_decision(report: dict) -> str:
    blockers = []
    if report["prompt_lint_errors"] > 0:
        blockers.append("prompt_lint_errors")
    if report["schema_pass_rate"] < 0.99:
        blockers.append("schema_regression")
    if report["eval_pass_rate"] < report["required_pass_rate"]:
        blockers.append("eval_gate_failed")
    if report["critical_safety_failures"] > 0:
        blockers.append("critical_safety_failure")
    if report["cost_delta"] > 0.10:
        blockers.append("cost_budget_exceeded")

    return "pass" if not blockers else "block: " + ",".join(blockers)
```

---

### 3. Practical Interview Question

> What would a prompt/model CI pipeline include?

### Strong Answer

It would lint prompts and configs, render prompt snapshots, validate schemas, run golden fixtures, run offline eval suites, compare against the current production baseline, check safety regressions, check latency/cost budgets, produce a PR report, and block merge on critical failures. If the gate passes, the candidate artifact is registered with metadata, eval evidence, and promotion stage.

### Active Recall

1. What does prompt linting catch?
2. Why compare against production baseline?
3. What should block merge?
4. Why register artifacts after CI?
5. Why test rendered prompts?

Final takeaway:

> A GenAI CI pipeline makes behavior changes visible, testable, comparable, and merge-blocked before they become production incidents.

---

## Subtopic P2.3.b: Feature Flags and Dynamic Config for Fast, Reversible Changes

> **Subtopic time:** 2h
> Outcome: You should be able to design dynamic config and feature flags for fast rollout, rollback, routing, and emergency mitigation.

### Add to Knowledge Base

Feature flags let teams change behavior without redeploying code.

In GenAI systems, flags can control:

```text
prompt version
model route
retrieval top_k
reranker on/off
safety policy version
tool availability
fallback model
canary percentage
tenant targeting
output streaming
```

The central mental model:

> Dynamic config is the steering wheel; CI/evals decide whether the road is safe.

---

### 1. Flag Requirements

Good flags are:

```text
versioned
audited
owned
typed
validated
environment-scoped
tenant-targeted
quickly reversible
safe by default
```

Bad flags:

```text
stringly typed
unlogged
changed manually in prod
no owner
no expiration
no approval
```

---

### 2. Kill Switches

Every high-risk GenAI capability should have a kill switch.

Examples:

```text
disable refund tool
disable autonomous email send
disable new prompt version
disable fallback route
force safe refusal for risky route
route all traffic to previous model
```

Kill switches should be tested before they are needed.

---

### 3. Practical Interview Question

> Why are feature flags especially important for LLM systems?

### Strong Answer

LLM behavior can regress without a code deploy because prompts, models, policies, and routing configs change behavior. Feature flags make those changes reversible. They allow canaries, tenant targeting, fast rollback, kill switches for risky tools, dynamic model routing, and emergency mitigation. But flags must be typed, audited, owned, and connected to eval/approval workflows, otherwise they become hidden production changes.

### Active Recall

1. What can flags control in GenAI?
2. Why are kill switches important?
3. What makes a feature flag unsafe?
4. Why should flags be audited?
5. How do flags support canary rollout?

Final takeaway:

> Feature flags and dynamic config make GenAI behavior fast to change and fast to reverse, but only if every change is typed, audited, owned, and guarded by eval evidence.

---

## Subtopic P2.3.c: Incident Response Runbooks for GenAI Services

> **Subtopic time:** 2h
> Outcome: You should be able to write a runbook for GenAI incidents involving bad answers, safety failures, tool mistakes, latency/cost regressions, or deployment changes.

### Add to Knowledge Base

GenAI incidents can be:

```text
hallucinated answer
unsupported citation
prompt injection success
PII leak
unsafe output
wrong tool call
duplicate side effect
model outage
latency spike
cost spike
bad rollout
```

The central mental model:

> An incident runbook turns panic into ordered mitigation, evidence capture, rollback, and prevention.

---

### 1. Runbook Template

```text
1. Declare incident and owner.
2. Classify severity and blast radius.
3. Freeze risky rollouts.
4. Preserve traces and release manifests.
5. Mitigate: rollback, kill switch, fail closed, disable tool, route fallback.
6. Identify first failed layer.
7. Communicate to stakeholders.
8. Add regression fixture.
9. Fix targeted layer.
10. Review and update runbook.
```

---

### 2. GenAI-Specific Evidence

Collect:

```text
release manifest
run record
prompt version
model version
retrieved chunks
tool calls
policy decisions
output validation result
feature flags
eval gate report
rollout percentage
user-visible output
```

Avoid collecting raw secrets or unauthorized data in broad incident docs.

---

### 3. Practical Interview Question

> A prompt release caused unsupported answers for enterprise users. What does your runbook do?

### Strong Answer

First I would classify severity and freeze rollout. I would preserve traces, run records, release manifest, eval gate report, and affected outputs. If the issue is active, I would roll back via feature flag or registry to the previous known-good prompt/model bundle. Then I would identify the first failed layer: retrieval, prompt contract, model, parser, policy, or deployment config. I would add affected cases as regression fixtures, fix the layer, rerun eval gates, and only redeploy through canary with guardrails.

### Active Recall

1. Name five GenAI incident types.
2. What should be preserved during an incident?
3. Why freeze rollouts?
4. Why add regression fixtures?
5. What is the first mitigation for a bad release?

Final takeaway:

> GenAI incident response starts with containment and trace preservation, then moves from symptom to first failed layer, targeted fix, regression, and controlled redeploy.

---

## Subtopic P2.3.d: Change Management and Approval Flows for High-Risk Model Updates

> **Subtopic time:** 2h
> Outcome: You should be able to design approval workflows for model, prompt, policy, or tool changes that affect high-risk users or actions.

### Add to Knowledge Base

Not all GenAI changes deserve the same process.

Low-risk copy prompt:

```text
normal PR + eval gate
```

High-risk financial tool-routing model:

```text
eval gate + security review + product approval + staged rollout + rollback plan
```

The central mental model:

> Change management should scale with blast radius, risk, and reversibility.

---

### 1. High-Risk Change Examples

```text
model used for medical/legal/financial advice
prompt controlling tool calls
safety policy update
retrieval permission logic
autonomous action threshold
PII redaction change
model provider migration
fallback route for high-risk workflow
```

---

### 2. Approval Packet

```yaml
change_id: genai-change-913
risk_tier: high
artifact_versions:
  prompt: refund_router_2.1
  model: classifier_v5
  policy: refund_policy_2026_06
blast_radius:
  tenants: enterprise_all
  workflow: refund_approval
evidence:
  offline_eval: pass
  safety_eval: pass
  shadow_results: pass
rollback:
  previous_release: refund_router_2.0
  rollback_method: feature_flag
approvals:
  - ml_owner
  - product_owner
  - security_reviewer
```

---

### 3. Emergency Changes

Emergency changes need:

```text
fast path
explicit owner
time limit
post-hoc review
audit log
rollback plan
regression follow-up
```

Emergency should not mean undocumented.

---

### 4. Practical Interview Question

> How would you manage approval for a high-risk prompt/model update?

### Strong Answer

I would classify the change by risk and blast radius. For high-risk workflows, the change needs a structured approval packet containing artifact versions, expected behavior change, eval evidence, safety evidence, affected tenants/workflows, rollout plan, rollback target, and owner. Approvers should include the model/prompt owner, product owner, and security/compliance reviewer where appropriate. Deployment should use staged rollout and automated rollback triggers. Emergency changes can have a fast path, but they still need audit, expiration, post-hoc review, and regression follow-up.

### Active Recall

1. Why should approval scale by risk?
2. Name high-risk GenAI changes.
3. What belongs in an approval packet?
4. Why do emergency changes still need audit?
5. Who should approve high-risk changes?

Final takeaway:

> High-risk GenAI changes need evidence-backed approval, staged rollout, rollback plans, and auditability because they change operational behavior, not just text.

---

## Module P2 Checkpoint: LLMOps and Deployment Lifecycle Synthesis

### Module Checkpoint

By the end of Pro Module P2, you should be able to:

1. Design a deployment pipeline where a prompt change cannot reach prod without passing eval gates.
2. Explain canary vs shadow vs blue-green for an LLM system and when each fits.
3. Define concrete automated rollback triggers tied to measurable thresholds.

The target module sentence:

> "LLMOps makes GenAI behavior changes versioned, evaluated, promoted, monitored, and reversible."

---

### 1. Eval-Gated Prompt Deployment Pipeline

The pipeline:

```text
developer edits prompt/config
-> PR opens
-> prompt lint
-> rendered prompt snapshot
-> schema tests
-> golden fixtures
-> offline eval suite
-> safety evals
-> latency/cost budget check
-> baseline comparison
-> approval if risk requires
-> registry candidate
-> staging
-> shadow or canary
-> production promotion
```

Merge blockers:

```text
critical safety failure > 0
P0 regression fails
schema validity below threshold
unsupported claim rate above threshold
tool-call correctness below threshold
cost increase above budget
missing owner or release manifest
```

The mature phrase:

> A prompt change is not production-ready because it looks better in a chat window; it is production-ready when its artifact bundle passes versioned eval gates and rollout guardrails.

---

### 2. Canary vs Shadow vs Blue-Green

| Strategy | User Impact | Best Fit | Risk |
|---|---|---|---|
| shadow | none | observe real traffic safely | extra cost, no real user feedback |
| canary | limited | gradual exposure after offline pass | small group may see regressions |
| blue-green | full cutover | fast rollback/cutover | state/cache compatibility |

Decision:

```text
high uncertainty -> shadow
passed offline and needs live signal -> canary
environment-level swap needed -> blue-green
```

For LLM systems:

```text
shadow must disable side effects
canary must monitor quality/safety/cost/latency
blue-green must handle conversation state, cache, retrieval index, and tool compatibility
```

---

### 3. Automated Rollback Triggers

Concrete examples:

```text
critical safety violations > 0 in canary
PII leakage detector fires once
unsupported claim rate > 3 percent for 15 minutes
schema validity < 99 percent
tool-call error rate doubles baseline
p95 latency > 8 seconds for 10 minutes
timeout rate > 2 percent
cost per successful task increases > 25 percent
human escalation rate doubles baseline
user complaint rate exceeds threshold
```

Rollback actions:

```text
set canary percentage to 0
route to previous prompt/model bundle
disable risky tool
switch provider/model fallback
fail closed for high-risk route
open incident and page owner
```

---

### 4. Full Release Manifest Template

```yaml
release_id: support-rag-2026-06-26.1
change_type: prompt_model_config
risk_tier: medium
owner: support-ai
artifacts:
  prompt: support_answer_prompt@3.5.0
  model: gpt-x@pinned-2026-06
  retrieval: support_index@2026-06-20
  reranker: reranker@2.3
  tool_schema: support_tools@1.8
  policy: safety_policy@2026-06-01
eval_gate:
  suite: support_regression@2026-06-24
  result: pass
  pass_rate: 0.94
  critical_failures: 0
rollout:
  strategy: canary
  percent: 5
rollback:
  previous_release: support-rag-2026-06-18.2
  method: feature_flag
approvals:
  - ml_owner
  - product_owner
```

---

### 5. Production Readiness Checklist

```text
[ ] Release manifest created.
[ ] Prompt/model/config versions pinned.
[ ] Eval suite version recorded.
[ ] Offline gates passed.
[ ] Safety and schema gates passed.
[ ] Rollback target identified.
[ ] Feature flag route exists.
[ ] Canary/shadow/blue-green strategy selected.
[ ] Guardrail metrics configured.
[ ] Automated rollback thresholds configured.
[ ] Owner and on-call identified.
[ ] Incident runbook linked.
```

---

### 6. Checkpoint Interview Answer

If asked:

> How would you design LLMOps for safe prompt/model deployment?

Answer:

I would treat prompts, models, retrieval configs, tool schemas, policies, and eval sets as versioned deployment artifacts. Every production behavior should have a release manifest that links the artifact versions, owner, risk tier, eval evidence, rollout plan, and rollback target.

For a prompt change, I would require a CI gate before merge. The pipeline would lint the prompt, render prompt snapshots, validate schemas, run golden fixtures, run versioned offline evals, check safety and regression suites, compare against the production baseline, and enforce cost and latency budgets. Critical safety failures, P0 regressions, schema regressions, or budget violations would block merge.

After merge, I would promote through registry stages. For risky changes, I would use shadow deployment first to run the new version on real traffic without user impact or side effects. If shadow results look good, I would canary to a small percentage of users and monitor quality, safety, latency, cost, tool errors, escalation rate, and user feedback. Blue-green is useful when I need fast environment-level cutover and rollback, but I would verify conversation state, caches, retrieval indexes, and tool compatibility.

Finally, I would define automated rollback triggers. Examples include any critical safety violation, PII leak, unsupported claim rate above threshold, schema validity below threshold, p95 latency over SLO, timeout rate spike, cost per successful task increase, or tool error regression. Rollback should use feature flags or registry routing to return to the previous known-good artifact bundle quickly.

The key principle is that GenAI behavior changes should be versioned, evaluated, promoted, monitored, and reversible like serious production software.

---

### 7. Checkpoint Active Recall

Answer these without looking:

1. Why is changing a prompt a production deployment?
2. What belongs in a release manifest?
3. Why must eval sets be versioned?
4. What is a registry stage?
5. Why are model aliases dangerous?
6. What should a reproducible run record include?
7. Why can staging lie?
8. What does an offline eval gate test?
9. What should always block merge?
10. What is shadow deployment?
11. Why must shadow disable side effects?
12. What is canary deployment?
13. What is blue-green deployment?
14. What are primary online metrics?
15. What are guardrail metrics?
16. Why is statistical significance important?
17. Name five rollback triggers.
18. Why are feature flags important for LLMOps?
19. What belongs in a GenAI incident runbook?
20. What approval flow is needed for high-risk changes?

Expected answers:

1. It can change user-visible behavior, safety, tool use, cost, and quality.
2. Prompt, model, config, dataset, eval, retrieval, tools, policy, rollout, rollback, owner.
3. Changing evals changes the meaning of pass/fail.
4. Draft, candidate, staging, canary, production, deprecated, blocked.
5. Providers can update aliases and change behavior silently.
6. Model, prompt, config, retrieval, chunks, tools, policy, flags, environment, code commit.
7. Different data, flags, tools, policies, latency, and model aliases can hide failures.
8. Quality, safety, schema, retrieval, tools, latency, cost, regressions.
9. Critical safety failures, P0 regressions, schema failures, missing manifest.
10. Mirroring real traffic to a new version without showing output to users.
11. To avoid duplicate or unsafe real-world actions.
12. Sending a small percentage of real users to the new version.
13. Switching between old and new environments for fast rollback.
14. Task success, resolution, conversion, satisfaction.
15. Safety, latency, cost, unsupported claims, tool errors, schema failures.
16. To avoid shipping noise as improvement.
17. Safety violation, PII leak, latency SLO breach, cost spike, schema drop, tool error spike.
18. They make rollout, rollback, kill switches, and routing reversible.
19. Severity, owner, traces, release manifest, mitigation, rollback, comms, regression.
20. Risk-scoped approval with eval evidence, rollout plan, rollback target, and audit trail.

---

### 8. Final Module P2 Readiness Rubric

| Skill | Ready Signal |
|---|---|
| artifact versioning | can define a release manifest |
| registry design | can describe stages, metadata, approvals |
| reproducibility | can produce a run record for replay |
| parity | can identify dev/staging/prod drift |
| eval gates | can define merge-blocking thresholds |
| rollout strategy | can choose canary, shadow, or blue-green |
| online testing | can name primary and guardrail metrics |
| rollback | can define measurable rollback triggers |
| CI/CD | can design lint/eval/regression/gate pipeline |
| incident response | can write a GenAI runbook |
| high-risk approval | can design evidence-backed change management |

Final checkpoint sentence:

> A mature LLMOps engineer does not ask "Did the prompt seem better?" They ask "Which versioned artifact bundle changed, which eval gate approved it, how was it rolled out, what guardrails watched it, and how fast can we roll it back?"
