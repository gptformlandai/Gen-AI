# Module 1 - GenAI Landscape And Mental Models

This is the evolving knowledge base for Module 1.

Covered so far:

- Topic 1.1.a: Foundation model vs instruct model vs reasoning-oriented model
- Topic 1.1.b: Assistant vs copilot vs workflow vs agent
- Topic 1.1.c: Hosted vs open-weight vs self-hosted model ecosystems
- Topic 1.1.d: Tokens, context windows, latency, throughput, and cost basics

---

## Topic 1.1: GenAI System Taxonomy and Vocabulary

**Topic time:** 4h

Subtopics in this topic:

- 1.1.a Foundation model vs instruct model vs reasoning-oriented model - 45m
- 1.1.b Assistant vs copilot vs workflow vs agent - 45m
- 1.1.c Hosted vs open-weight vs self-hosted model ecosystems - 60m
- 1.1.d Tokens, context windows, latency, throughput, and cost basics - 90m

Learning rule for this module file:

- We cover one subtopic at a time.
- We do not complete the full parent topic in a single pass.
- Each new subtopic is appended only after the previous one is understood.

---

## Subtopic 1.1.a: Foundation Model vs Instruct Model vs Reasoning-Oriented Model

### 1) The Intuition (Plain English)

These three labels describe different kinds of behavior, not three unrelated species of AI.

- A foundation model is the broad raw base.
- An instruct model is that base adapted to follow directions better.
- A reasoning-oriented model is optimized to stay coherent across longer chains of thought, multi-step decomposition, tool use, or harder decision sequences.

Simple mental model:

- Foundation model = general knowledge engine
- Instruct model = conversationally aligned task follower
- Reasoning-oriented model = more deliberate problem solver for complex tasks

Analogy:

Think of three versions of the same engineer.

- The foundation model is the engineer fresh out of school with lots of broad knowledge but not much structure in how to respond to business requests.
- The instruct model is the same engineer after being trained to answer stakeholders clearly, follow instructions, and stay on task.
- The reasoning-oriented model is the same engineer after learning how to break down ambiguous or difficult problems systematically over multiple steps.

Important intuition:

The jump from foundation to instruct is mostly about usability and alignment.
The jump from instruct to reasoning-oriented behavior is mostly about task difficulty, control of longer problem-solving chains, and better performance on multi-step decisions.

#### Clarification: What does "reasoning" mean in AI?

In AI, "reasoning" does not mean the model has human consciousness or true human-style understanding.

In practical system terms, reasoning means the model is better at:

- breaking a hard problem into smaller steps
- keeping track of intermediate conclusions
- comparing alternatives before answering
- choosing when to use a tool or more evidence
- avoiding shallow first-answer behavior on complex tasks

So when we call a model "reasoning-oriented," we usually mean it is more reliable on tasks like:

- multi-step diagnosis
- planning
- hypothesis comparison
- tool-using workflows
- long-form problem decomposition

The safest engineering interpretation is this:

Reasoning is observable as better multi-step task performance, not as proof that the model "thinks like a human."

#### Clarification: If the foundation model is raw, why is it still used at all?

You are right that most end users do not directly interact with a raw foundation model in production-facing applications.

But foundation models still matter for several reasons:

1. They are the base capability layer.

- Instruct models and reasoning-oriented variants are usually built on top of a strong foundation model.
- If the base model is weak, the tuned versions have a lower ceiling.

2. They are used by model builders and platform teams.

- alignment
- instruction tuning
- fine-tuning
- distillation
- evaluation research

3. They are useful in controlled backend settings.

Sometimes teams use base-style models for:

- offline experimentation
- synthetic data generation
- internal benchmarking
- research workflows
- specialized tuning pipelines

4. They help explain model behavior correctly.

If you do not understand the difference between base capability and instruction alignment, you will misdiagnose failures. You may think the model "does not know" something when the real issue is that it was not optimized to respond in a user-safe or instruction-following way.

So the correct mental model is not:

- foundation model = useless for practice

It is:

- foundation model = rarely the direct end-user interface, but still the base layer that makes the downstream instruct and reasoning systems possible.

### 2) Real-World Industry Scenarios

#### Scenario A: Internal policy assistant

- Product context: employees ask straightforward questions about benefits, leave, policy, and onboarding.
- Constraints: low hallucination tolerance, moderate latency sensitivity, clear formatting, predictable behavior.
- What good looks like in production: the system follows user requests reliably, formats answers well, and stays within policy boundaries.

Why this matters here:

- A raw foundation model is usually the wrong choice.
- An instruct model is usually the right default because the task is mostly about clear task following, not deep multi-step reasoning.

#### Scenario B: Multi-step incident triage or research workflow

- Product context: the system must examine logs, propose hypotheses, compare evidence, maybe call tools, and decide on the next action.
- Constraints: higher reasoning depth, better trajectory quality, stronger debugging trace needs, possibly higher latency tolerance.
- What good looks like in production: the system maintains coherence across multiple steps, does not collapse into shallow answers too early, and can justify intermediate decisions.

Why this matters here:

- A reasoning-oriented model may be worth the extra latency or cost.
- Using a cheaper instruct model may still work, but only if orchestration and verification are strong enough.

### 3) System View (Think like a systems engineer)

#### Inputs -> Transformations -> Outputs

- Inputs: task type, model choice, prompt structure, tool availability, evaluation target.
- Transformations:
  - classify whether the task is straightforward instruction-following or deeper multi-step reasoning
  - route to the most appropriate model family
  - optionally add retrieval or tools
  - verify output quality
- Outputs: direct answer, structured extraction, plan, decision, or tool-driven next action.

#### Observability

What we log and compare:

- model family chosen
- latency
- cost per request
- token usage
- quality on simple tasks vs multi-step tasks
- failure mode type: off-task behavior, shallow reasoning, formatting error, hallucination, tool misuse

#### Failure points

- Using a foundation model directly where user-facing behavior requires instruction following.
- Using an instruct model for tasks that need sustained multi-step reasoning without enough scaffolding.
- Assuming a reasoning-oriented model automatically fixes poor retrieval, poor tools, or poor orchestration.

### 4) System Design Flavor (practical and concise)

#### Key design question

Do we need better task following, or do we need better multi-step reasoning?

That question usually determines the right model class faster than brand comparisons do.

#### Tradeoffs

- Foundation vs instruct: instruct models are usually more usable for applications, but the foundation model matters underneath because it sets the base capability ceiling.
- Instruct vs reasoning-oriented: reasoning-oriented models can improve hard-task performance, but often cost more and take longer.
- Model strength vs system design: a stronger model helps, but it cannot fully compensate for bad retrieval, unclear task framing, or weak evaluation.

#### One scaling consideration

At scale, the wrong model class causes silent waste.

- If simple tasks are routed to expensive reasoning models, cost explodes.
- If complex tasks are routed to shallow instruct models, quality degrades and humans end up redoing the work.

### 5) Common Mistakes + Debugging

#### Mistake 1

- Symptom: outputs are awkward, off-format, or ignore user instructions.
- Likely cause: the system is too close to a raw foundation-style behavior and lacks instruction tuning or strong response constraints.
- First debugging step: compare the same task across an instruct model and the current model under identical prompt conditions.

#### Mistake 2

- Symptom: the system gives fast but shallow answers on hard multi-step tasks.
- Likely cause: an instruct model is being used for a reasoning-heavy task without enough scaffolding, decomposition, or model capability.
- First debugging step: inspect traces for premature answer generation and test whether decomposition or a reasoning-oriented model improves the trajectory.

#### Mistake 3

- Symptom: the team upgrades to a reasoning-oriented model but quality barely improves.
- Likely cause: the real bottleneck is retrieval quality, tool reliability, or workflow design rather than model reasoning depth.
- First debugging step: isolate one fixed task and compare evidence quality, tool success, and prompt clarity before blaming or praising the model class.

### 6) Active Recall (Spaced Repetition)

1. What is the simplest difference between a foundation model and an instruct model?
2. Why is an instruct model usually the safer default for user-facing applications?
3. What kind of task makes a reasoning-oriented model more justifiable?
4. Why can a stronger reasoning model still fail in a badly designed system?
5. What is the first question you should ask before choosing between instruct and reasoning-oriented behavior?

#### Active Recall Answers

1. A foundation model is the broad raw base, while an instruct model is adapted to follow user requests more reliably, safely, and clearly.
2. Because most user-facing applications need stable instruction-following behavior, cleaner formatting, and better alignment with human requests.
3. A task that requires multi-step decomposition, comparing alternatives, tool use, or sustained decision-making, such as incident analysis or research workflows.
4. Because the real bottleneck may be retrieval quality, tool reliability, prompt framing, or workflow design rather than raw model reasoning depth.
5. Ask: do we mainly need better task following, or do we mainly need better multi-step reasoning?

### 7) Practice

#### Mini-exercise

Classify the following tasks by default model need: foundation-style base capability, instruct-first, or reasoning-oriented-first.

- summarize a leave policy
- extract invoice fields into JSON
- compare three outage hypotheses using logs and retrieved runbooks
- answer a simple FAQ from a company handbook
- decide a sequence of actions for a support escalation workflow

For each one, write one sentence explaining why.

#### Mini-exercise Answers

- summarize a leave policy -> instruct-first
  Why: the task is mostly about following a user request clearly, staying grounded, and producing a readable answer.

- extract invoice fields into JSON -> instruct-first
  Why: this is mainly structured extraction and instruction-following, not deep multi-step reasoning.

- compare three outage hypotheses using logs and retrieved runbooks -> reasoning-oriented-first
  Why: the task requires comparing alternatives, holding intermediate conclusions, and making a better multi-step judgment.

- answer a simple FAQ from a company handbook -> instruct-first
  Why: this is a straightforward retrieval-plus-response task where stable instruction following matters more than deeper reasoning.

- decide a sequence of actions for a support escalation workflow -> reasoning-oriented-first
  Why: the system must plan over multiple steps and choose a sensible next action path rather than return one direct answer.

#### Capstone-style system design question

You are designing a support platform with two user flows:

- Flow A: answer common support questions from documentation
- Flow B: investigate recurring incidents by inspecting logs, proposing hypotheses, and escalating the right next action

Which flow should default to an instruct model, which might justify a reasoning-oriented model, and why would a raw foundation model usually stay behind the scenes rather than face the user directly?

#### Capstone-style Answer Outline

- Flow A should default to an instruct model.
  Why: answering common support questions is mainly about clear task following, helpful formatting, grounded retrieval use, and predictable user-facing behavior.

- Flow B may justify a reasoning-oriented model.
  Why: incident investigation requires comparing evidence, maintaining a multi-step hypothesis chain, possibly using tools, and deciding a next action rather than just producing a direct answer.

- A raw foundation model usually stays behind the scenes because end-user systems need alignment, safe behavior, and reliable instruction following.
  The foundation model still matters as the base capability layer underneath tuned instruct or reasoning-oriented variants.

### 8) Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect task-to-model routing.

Why:

The most common failure here is not that the model is universally weak. It is that the wrong class of model is assigned to the wrong class of task, which shows up as unnecessary cost, shallow reasoning, or poor instruction following.

### 9) Curiosity Bridge (Mandatory Ending)

Now that the model-class difference is clearer, the next question is not about models at all.

The next subtopic asks what kind of system you are actually building: assistant, copilot, workflow, or agent. That distinction often matters more than the model brand name.

---

## Subtopic 1.1.b: Assistant vs Copilot vs Workflow vs Agent

### 1) The Intuition (Plain English)

These four words are often mixed together, but they describe different system roles.

- An assistant mainly answers or helps when the user asks.
- A copilot helps inside an existing task flow, usually alongside a human.
- A workflow executes a predefined sequence of steps.
- An agent chooses its next action dynamically to reach a goal.

Simple mental model:

- Assistant = answers and helps
- Copilot = collaborates while you work
- Workflow = follows a defined path
- Agent = chooses the path

Analogy:

Think of air travel.

- An assistant is the airport help desk answering your questions.
- A copilot is the flight-support system helping the pilot during flight operations.
- A workflow is the standard boarding process with fixed stages.
- An agent is the operations controller dynamically rerouting flights and staff based on changing conditions.

The most important distinction is not “which one sounds smarter.”
It is “how much decision-making freedom should this system be allowed to have?”

If you get that wrong, the whole design becomes either too rigid or too chaotic.

#### Clarification: Why do people confuse these terms so often?

Because all four can use the same underlying LLMs, tools, retrieval, and UI patterns.

From the outside, they may all look like “chat with AI.”

But from a systems perspective, they differ in:

- how many decisions are predefined
- how much autonomy the model has
- whether the human stays in the loop continuously
- whether the system is mostly responding, assisting, executing, or deciding

That is why naming the system correctly matters before choosing architecture.

### 2) Real-World Industry Scenarios

#### Scenario A: IDE coding helper

- Product context: a developer writes code, asks questions, gets inline suggestions, explanations, refactors, and test help.
- Constraints: low interruption tolerance, high usefulness pressure, human remains actively in control, suggestions must be reversible.
- What good looks like in production: the system behaves as a copilot, stays context-aware, helps during the task, and does not act autonomously on risky changes.

Why this matters here:

- Calling this an “agent” by default is usually misleading.
- The human is still the primary operator.
- The AI is assisting inside an existing workflow.

#### Scenario B: Invoice processing pipeline

- Product context: invoices arrive, fields are extracted, anomalies are checked, records are routed, and exceptions go to human review.
- Constraints: repeatability, auditability, predictable latency, strong control boundaries.
- What good looks like in production: the system behaves mostly as a workflow with a few LLM-powered steps, not as a free-moving agent.

Why this matters here:

- Most business automation is workflow-first.
- The model may classify or extract, but the path is still predefined.

#### Scenario C: Incident response coordinator

- Product context: the system gathers logs, checks runbooks, compares likely causes, asks for missing evidence, and recommends or triggers next steps.
- Constraints: ambiguity, changing state, tool use, stronger reasoning demand, need for approval boundaries.
- What good looks like in production: the system may justify limited agentic behavior because the next step depends on what is discovered during execution.

Why this matters here:

- This is closer to a real agent problem because the path is not fully known in advance.
- But even here, autonomy should be bounded and observable.

### 3) System View (Think like a systems engineer)

#### Inputs -> Transformations -> Outputs

- Inputs: user goal, task state, available tools, business rules, approval rules, retrieved context.
- Transformations:
  - classify whether the system is only answering, assisting, executing a known sequence, or dynamically choosing actions
  - determine how much control stays with the human
  - apply retrieval, tools, prompts, or orchestration accordingly
  - produce a response, suggestion, workflow step, or next-action decision
- Outputs: answer, recommendation, structured result, executed step, or delegated next action.

#### Observability

What we log and inspect:

- system role assumed: assistant, copilot, workflow, or agent
- human approvals and overrides
- tool calls and execution path
- whether the route was deterministic or dynamic
- latency, cost, and failure points by step
- where the model made a decision vs where the system followed rules

#### Failure points

- Designing a workflow as an agent and losing predictability.
- Designing an agent as a workflow and losing adaptability.
- Calling a copilot an assistant and under-investing in task context.
- Giving an assistant unsafe action authority it should never have.

### 4) System Design Flavor (practical and concise)

#### Key design question

Is the next step known in advance, or must the system decide it dynamically?

That single question separates workflows from real agentic systems surprisingly often.

#### Tradeoffs

- Assistant vs copilot: assistants are simpler, but copilots are more context-aware within active work.
- Workflow vs agent: workflows are easier to test and audit, but agents can adapt better when paths are unknown.
- Human control vs autonomy: more autonomy may improve speed, but raises safety, debugging, and accountability costs.

#### One scaling consideration

At scale, false autonomy is expensive.

- If you over-label systems as agents, cost, unpredictability, and debugging burden rise.
- If you over-force workflow logic where reality is dynamic, humans end up manually compensating for rigidity.

### 5) Common Mistakes + Debugging

#### Mistake 1

- Symptom: the system behaves unpredictably and is hard to audit.
- Likely cause: a workflow problem was incorrectly designed as an agent problem.
- First debugging step: inspect whether the execution path should have been deterministic and identify which decisions could be converted into rules.

#### Mistake 2

- Symptom: the system feels dumb and brittle on dynamic tasks.
- Likely cause: an agent-like problem was forced into a rigid workflow with no room for conditional adaptation.
- First debugging step: inspect where failures occur because the next step depends on information discovered only during runtime.

#### Mistake 3

- Symptom: a so-called assistant accidentally performs risky actions or oversteps user intent.
- Likely cause: action authority and role boundaries were defined poorly.
- First debugging step: review tool permissions, approval gates, and which component is allowed to make execution decisions.

### 6) Active Recall (Spaced Repetition)

1. What is the simplest difference between a workflow and an agent?
2. Why is a coding helper usually better described as a copilot than a plain assistant?
3. What makes an assistant different from a copilot in system design terms?
4. Why is overusing the word “agent” harmful in architecture design?
5. What is the first question you should ask before deciding between workflow and agent?

#### Active Recall Answers

1. A workflow follows a predefined path, while an agent chooses the next step dynamically based on the evolving state.
2. Because it helps inside an active human task flow and collaborates with the user continuously rather than simply answering isolated questions.
3. An assistant mainly responds to requests, while a copilot is embedded into an ongoing task context and helps the human perform work step by step.
4. Because it encourages unnecessary autonomy, complexity, and unpredictability where a simpler workflow or assistant design would be safer and cheaper.
5. Ask: is the next step known in advance, or does the system need to decide it dynamically during execution?

### 7) Practice

#### Mini-exercise

Classify each use case as assistant, copilot, workflow, or agent.

- HR chatbot that answers policy questions with citations
- AI feature inside a CRM that drafts replies while sales reps work
- document ingestion pipeline that classifies, extracts, and routes files through fixed stages
- system that investigates incidents by checking logs, comparing hypotheses, and selecting the next tool to call
- support bot that answers simple questions but requires approval before refund actions

For each one, explain why the label fits better than the other three.

#### Mini-exercise Answers

- HR chatbot that answers policy questions with citations -> assistant
  Why: its primary role is to answer user questions directly, not collaborate inside an active task flow or choose a dynamic execution path.

- AI feature inside a CRM that drafts replies while sales reps work -> copilot
  Why: it supports a human inside an existing workflow and stays embedded in the user’s live task context.

- document ingestion pipeline that classifies, extracts, and routes files through fixed stages -> workflow
  Why: the sequence is predefined and repeatable even if some steps use LLMs internally.

- system that investigates incidents by checking logs, comparing hypotheses, and selecting the next tool to call -> agent
  Why: the next action depends on what is discovered during execution, so the path is not fully predetermined.

- support bot that answers simple questions but requires approval before refund actions -> assistant with guarded workflow steps
  Why: the answer behavior is assistant-like, but any risky action should move into an approval-bound workflow rather than full autonomous agency.

#### Capstone-style system design question

Design a customer support platform that must do four things: answer FAQ questions, help support reps draft responses, process routine ticket-routing steps, and investigate unusual incidents that require adaptive next steps. Which parts should be assistant behavior, which should be copilot behavior, which should be workflows, and which, if any, justify an agent?

#### Capstone-style Answer Outline

- FAQ question answering should be assistant behavior.
  Why: the job is mostly direct Q&A with retrieval and clear user-facing responses.

- helping support reps draft responses should be copilot behavior.
  Why: the system is assisting humans inside their ongoing work rather than acting alone.

- routine ticket-routing steps should be workflows.
  Why: fixed, auditable, repeatable paths are better than dynamic autonomy for predictable operations.

- unusual incident investigation may justify bounded agent behavior.
  Why: the next action may depend on runtime evidence, but the agent should still operate within tool, policy, and approval boundaries.

### 8) Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect role boundaries and autonomy boundaries.

Why:

Many failures here happen because the system is doing the wrong kind of job, for example, a workflow disguised as an agent, or an assistant given action authority it should not have.

### 9) Curiosity Bridge (Mandatory Ending)

Now the system roles are clearer, but there is still another layer of confusion people run into.

Even after you know whether you are building an assistant, workflow, or agent, you still need to decide how you want to run the model itself: hosted, open-weight, or self-hosted. That deployment choice changes cost, control, privacy, and operational complexity.

---

## Subtopic 1.1.c: Hosted vs Open-Weight vs Self-Hosted Model Ecosystems

### 1) The Intuition (Plain English)

These three labels answer a very practical question: who owns and runs the model layer?

- Hosted means a model provider runs the inference infrastructure and you call it through an API.
- Open-weight means the model weights are available for you to obtain and run, subject to the model's license.
- Self-hosted means you run the model infrastructure yourself, usually on your own cloud account, cluster, or hardware.

The key thing people miss is this:

- hosted is a deployment choice
- open-weight is an availability and licensing characteristic
- self-hosted is an operational choice

So open-weight does not automatically mean self-hosted, and self-hosted usually relies on open-weight models.

Analogy:

Think of food service.

- Hosted is ordering from a restaurant delivery app. Someone else runs the kitchen.
- Open-weight is getting the recipe and ingredients list.
- Self-hosted is cooking in your own kitchen and managing the whole process yourself.

The more control you want, the more operational responsibility you accept.

#### Clarification: Why do people confuse open-weight with open-source?

Because many people hear "open" and assume full freedom.

But open-weight usually means the model parameters are accessible, not that every training detail, dataset, codebase, or commercial usage right is fully open.

As a systems engineer, you should separate these questions:

- Can I access the weights?
- Can I commercially use them under the license?
- Can I fine-tune and redistribute?
- Do I have the infra and operational skill to serve them reliably?

#### Clarification: Open-weight is not the same as temperature, top-p, or top-k controls

No. Open-weight does not mean the provider is giving you sampling controls like temperature, top-p, or top-k.

Those are inference-time decoding parameters.
They control how the model generates an answer for a specific request.

Open-weight refers to something deeper: access to the model's learned parameters themselves, which are the large numerical tensors produced during training.

Simple separation:

- model weights = what the model has learned
- temperature, top-p, top-k = how you ask the serving system to generate from that model at runtime
- model selection = which model endpoint or checkpoint you choose to call

So these are different layers of the stack.

| Layer | What it means | Example |
|---|---|---|
| Model artifact | The actual trained model parameters | Llama weights, Mistral weights |
| Serving / inference controls | Runtime generation knobs | temperature, top-p, top-k, max tokens |
| API routing choice | Which model or endpoint you invoke | choose GPT-4.1 vs a Llama deployment |

Why this distinction matters:

- A closed hosted API can still expose temperature and top-p even though the weights are not available to you.
- An open-weight model may be served through a simple endpoint that exposes only a few runtime controls.
- Self-hosting an open-weight model often gives you more flexibility over inference settings, batching, quantization, and serving stack design, but that flexibility comes from owning the serving layer, not from the phrase open-weight by itself.

Another way to think about it:

- open-weight answers: "Do I have access to the trained model itself?"
- temperature/top-p/top-k answer: "How should decoding behave for this request?"
- self-hosted answers: "Who runs the inference system?"

Example:

- If you call a hosted API for a closed model and set temperature to 0.2, you are controlling decoding, not accessing weights.
- If you download an open-weight model and run it on your own GPU, you have access to the weights.
- If you then expose an API on top of that model with temperature and top-p controls, those controls are part of your serving interface, not the definition of open-weight.

This is the clean mental model to keep:

- Open-weight is about model access.
- Hosted vs self-hosted is about deployment ownership.
- Temperature, top-p, and top-k are about output generation behavior at inference time.

### 2) Real-World Industry Scenarios

#### Scenario A: Startup building a customer support copilot fast

- Product context: a small team wants to launch quickly, validate product value, and avoid infrastructure complexity.
- Constraints: low engineering bandwidth, fast iteration, acceptable vendor dependency, moderate privacy requirements.
- What good looks like in production: the team uses hosted models first, ships quickly, measures value, and delays heavy infra decisions until they are justified.

Why this matters here:

- Hosted wins when speed matters more than deep control.
- Most early-stage teams should not start by running model infra themselves.

#### Scenario B: Enterprise document intelligence with tighter governance

- Product context: sensitive documents, compliance controls, approval-heavy environments, and stronger data residency requirements.
- Constraints: privacy, auditability, policy review, possible restrictions on external API exposure.
- What good looks like in production: the team evaluates open-weight and possibly self-hosted deployment to get stronger control over data handling and platform behavior.

Why this matters here:

- Control and compliance can justify more operational complexity.
- The right answer may still be hybrid rather than fully self-hosted.

#### Scenario C: High-volume retrieval and extraction platform

- Product context: millions of repetitive requests, cost pressure, predictable task shape, and strong optimization incentives.
- Constraints: inference cost, throughput, batching efficiency, latency SLOs.
- What good looks like in production: the team may adopt open-weight models and eventually self-host parts of the stack if traffic scale makes the economics favorable.

Why this matters here:

- At higher scale, per-request cost and infrastructure efficiency become first-class design concerns.

### 3) System View (Think like a systems engineer)

#### Inputs -> Transformations -> Outputs

- Inputs: product requirements, privacy constraints, latency targets, cost targets, traffic patterns, model quality needs, licensing limits, infra capability.
- Transformations:
  - choose whether model access is hosted, open-weight, self-hosted, or hybrid
  - route requests through provider APIs or internal inference infrastructure
  - apply fallback logic, observability, caching, and cost controls
  - monitor performance, quality, and operational risk
- Outputs: reliable model responses under the chosen control, cost, and compliance envelope.

#### Observability

What we log and inspect:

- provider, model, and deployment mode per request
- latency by stage: network, queue, inference, post-processing
- token usage and cost per request
- rate-limit events and provider errors
- GPU utilization, queue depth, and throughput for self-hosted paths
- fallback frequency across models or providers
- model version and rollout history

#### Failure points

- Hosted path: provider outage, quota exhaustion, rate limits, regional unavailability, sudden pricing changes.
- Open-weight path: licensing misunderstandings, poor model benchmarking, underestimated serving complexity.
- Self-hosted path: GPU instability, bad autoscaling, memory pressure, cold starts, weak observability, operational overload.

### 4) System Design Flavor (practical and concise)

#### Key design question

Who should own the inference layer for this product right now?

That question is usually more important than asking which model brand is best.

#### Tradeoffs

- Hosted vs self-hosted: hosted gives speed and simplicity, while self-hosted gives deeper control at the cost of much more operational burden.
- Hosted vs open-weight: hosted is easier to start with, while open-weight gives more portability and tuning freedom if the license and infra support it.
- Single provider vs hybrid: one provider is simpler, but multi-provider or hybrid setups improve resilience and negotiation power.

#### One scaling consideration

At 10x traffic, the bottleneck changes.

- Hosted systems start feeling provider cost, rate limits, and vendor concentration risk.
- Self-hosted systems start feeling GPU scheduling, batching strategy, observability depth, and capacity planning pressure.

### 5) Common Mistakes + Debugging

#### Mistake 1

- Symptom: the team assumes an open-weight model automatically means cheap and easy deployment.
- Likely cause: they confused model access with production serving complexity.
- First debugging step: separate model-license questions from inference-infrastructure questions and estimate the full serving path realistically.

#### Mistake 2

- Symptom: a team self-hosts too early and spends more time on infra than on product quality.
- Likely cause: self-hosting was chosen for prestige or perceived control rather than a measured business need.
- First debugging step: compare current quality, latency, and cost goals against a hosted baseline and calculate whether self-hosting is actually justified.

#### Mistake 3

- Symptom: a hosted deployment later becomes blocked by privacy, compliance, or residency constraints.
- Likely cause: data-handling requirements were not evaluated early enough.
- First debugging step: map the exact data path, including prompts, retrieved context, logs, and provider retention behavior.

### 6) Active Recall (Spaced Repetition)

1. What is the simplest difference between hosted and self-hosted model usage?
2. Why does open-weight not automatically mean self-hosted?
3. What kind of team usually benefits most from starting with hosted models?
4. What usually becomes more important at higher traffic volume: raw model branding or inference economics?
5. What is the first question you should ask before choosing between hosted and self-hosted?

#### Active Recall Answers

1. Hosted means a provider runs the inference stack for you, while self-hosted means you run the inference infrastructure yourself.
2. Because open-weight describes model availability and licensing, while self-hosted describes where and by whom the model is actually served.
3. A team that needs fast iteration, low operational burden, and quick time to market usually benefits most from hosted models first.
4. Inference economics, operational reliability, and control boundaries usually become more important at scale than model branding alone.
5. Ask: who should own the inference layer for this product right now, given our privacy, cost, latency, and operational constraints?

### 7) Practice

#### Mini-exercise

Choose the best default deployment approach for each use case: hosted, open-weight with managed serving, self-hosted, or hybrid.

- early-stage startup building a support assistant and validating product-market fit
- enterprise legal document assistant with strict data governance and region restrictions
- high-volume classification pipeline where request cost is starting to dominate margins
- internal research team experimenting with many models and benchmarking options quickly
- production system that needs a primary provider plus a fallback path during outages

For each one, explain why the choice fits better than the others.

#### Mini-exercise Answers

- early-stage startup building a support assistant and validating product-market fit -> hosted
  Why: the team should optimize for shipping speed, lower ops burden, and fast iteration before taking on inference infrastructure complexity.

- enterprise legal document assistant with strict data governance and region restrictions -> open-weight with managed serving or self-hosted, depending compliance depth
  Why: stronger control over data handling may be required, but the exact answer depends on whether the organization can operate the infra safely itself.

- high-volume classification pipeline where request cost is starting to dominate margins -> open-weight with managed serving or self-hosted
  Why: once traffic is large and task shape is stable, controlling inference economics becomes more valuable and can justify more operational ownership.

- internal research team experimenting with many models and benchmarking options quickly -> hosted or hybrid
  Why: broad experimentation is usually faster with hosted access, though hybrid setups may help if some open-weight models need side-by-side evaluation.

- production system that needs a primary provider plus a fallback path during outages -> hybrid
  Why: resilience improves when the system is not completely dependent on one serving path or one vendor.

#### Capstone-style system design question

You are designing an enterprise GenAI platform for three workloads: a general knowledge assistant, a sensitive contract-analysis system, and a high-volume document extraction service. For each workload, decide whether hosted, open-weight, self-hosted, or a hybrid approach is the best starting point, and explain how privacy, cost, and operational maturity change the answer.

#### Capstone-style Answer Outline

- The general knowledge assistant usually starts hosted.
  Why: speed, simplicity, and broad capability matter more than deep infrastructure control at the start.

- The sensitive contract-analysis system may justify open-weight plus stronger control, possibly self-hosted if compliance and residency needs are strict enough.
  Why: privacy and governance can outweigh the simplicity advantage of hosted APIs.

- The high-volume document extraction service may move toward open-weight or self-hosted serving as traffic grows.
  Why: predictable workloads and sustained volume make cost and throughput optimization more important.

- A hybrid platform is often the most realistic answer.
  Why: different workloads have different risk, cost, and control needs, so one deployment model is rarely optimal for everything.

### 8) Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect the inference ownership boundary and the actual request path.

Why:

Many production failures here come from misunderstanding where the model is really running, what dependencies are in the request path, and which privacy, rate-limit, or infrastructure bottleneck is actually in control.

### 9) Curiosity Bridge (Mandatory Ending)

Now the deployment ecosystem is clearer, but one more layer still decides whether the product feels viable in the real world.

Even a great hosted or self-hosted setup can fail if you do not understand token usage, context limits, latency, throughput, and cost. That is the next subtopic because those mechanics drive real production tradeoffs every day.

---

## Subtopic 1.1.d: Tokens, Context Windows, Latency, Throughput, and Cost Basics

### 1) The Intuition (Plain English)

This is the operations physics of GenAI systems.

- Tokens are the billable and computational units.
- Context window is the total token budget the model can consider in one request.
- Latency is how long one request takes.
- Throughput is how many requests (or tokens) the system can handle over time.
- Cost is the money spent to process input and output tokens, plus infrastructure overhead.

If model quality is your engine, these metrics are your fuel, road width, speed, traffic flow, and toll cost.

Analogy:

Think of a highway toll system.

- Tokens = number of vehicles passing through.
- Context window = maximum vehicles allowed in one lane segment.
- Latency = time one vehicle takes from entry to exit.
- Throughput = vehicles processed per minute.
- Cost = toll paid per vehicle.

You cannot optimize only one of these forever. If you push one too hard, another gets worse.

#### Core formulas you should remember

- total_tokens = input_tokens + output_tokens
- estimated_cost_per_request = (input_tokens * input_price_per_token) + (output_tokens * output_price_per_token)
- throughput_rps = completed_requests / second
- p95_latency = 95th percentile response time

### 2) Real-World Industry Scenarios

#### Scenario A: Customer support assistant spikes during business hours

- Product context: many short user queries, moderate answers, occasional retrieval augmentation.
- Constraints: low p95 latency target, stable UX, budget limits, spiky traffic.
- What good looks like in production: bounded prompts, cached context, predictable token usage, and autoscaling that keeps p95 within SLA.

Why this matters:

- Small token savings multiplied across high volume create major cost and latency improvements.

#### Scenario B: Legal document analysis with long context

- Product context: large contracts, clause comparison, citation-heavy outputs.
- Constraints: large context demand, slower responses acceptable, high accuracy and traceability required.
- What good looks like in production: chunking and retrieval reduce unnecessary full-context calls, while output length is constrained to control cost.

Why this matters:

- Large context windows solve some problems, but unbounded context growth can destroy cost and latency.

#### Scenario C: Internal analytics copilot serving many teams

- Product context: mixed workload from small queries to deep analysis requests.
- Constraints: shared quota, noisy-neighbor effects, variable output lengths.
- What good looks like in production: request classes with different limits, queue management, and cost guardrails per tenant.

Why this matters:

- Throughput and fairness become architecture concerns, not just model concerns.

### 3) System View (Think like a systems engineer)

#### Inputs -> Transformations -> Outputs

- Inputs: request text, retrieved context, system prompt, user tier, target model, output format needs.
- Transformations:
  - tokenize input
  - enforce context limits and trim or compress context
  - run inference with decoding limits
  - stream or return output
  - record token counts, latency, and cost metadata
- Outputs: generated response plus observability and billing signals.

#### Observability

What we must track per request:

- input_tokens, output_tokens, total_tokens
- p50, p95, p99 latency
- time-to-first-token for streaming systems
- model, prompt version, retrieval payload size
- queue wait time vs inference time
- estimated and realized cost by request, user, and feature
- rate-limit errors, truncation events, timeout events

#### Failure points

- Context overflow: prompt + retrieved chunks exceed window and force truncation.
- Latency blow-up: oversized prompts or long outputs degrade p95.
- Throughput collapse: queue growth during spikes causes cascading timeouts.
- Cost drift: output length or retrieval payload silently grows over time.

### 4) System Design Flavor (practical and concise)

#### Key design question

What token budget and latency budget does each request class get?

Without class-based budgets, systems over-serve simple tasks and under-serve complex tasks.

#### Tradeoffs

- Larger context vs lower latency: more context can improve grounding but increases compute time.
- Longer outputs vs lower cost: richer answers cost more and can slow UX.
- Higher throughput vs tighter quality controls: aggressive concurrency helps capacity but can stress retrieval and guardrail checks.

#### One scaling consideration

At 10x traffic, global defaults fail.

You need per-route budgets, tenant-aware throttling, and degradation policies (for example, shorter outputs or smaller retrieval sets during peak load).

### 5) Common Mistakes + Debugging

#### Mistake 1

- Symptom: p95 latency rises gradually over weeks.
- Likely cause: prompt or retrieval payload bloat increased average input tokens.
- First debugging step: compare token histograms by prompt version and retrieval chunk count before and after regression.

#### Mistake 2

- Symptom: monthly spend exceeds forecast even though request volume is stable.
- Likely cause: output token growth from verbose prompting or missing output caps.
- First debugging step: inspect output token distribution and enforce max output tokens per route.

#### Mistake 3

- Symptom: intermittent failures during peak traffic.
- Likely cause: throughput bottleneck in queueing, model concurrency, or shared rate limits.
- First debugging step: separate queue wait time from inference time to identify where saturation begins.

### 6) Active Recall (Spaced Repetition)

1. What is the simplest formula for total tokens in one request?
2. Why can increasing context window usage hurt latency and cost?
3. What does p95 latency tell you that average latency can hide?
4. Why should teams measure queue wait time separately from inference time?
5. What is one common reason cost rises even when request count is flat?

#### Active Recall Answers

1. total_tokens = input_tokens + output_tokens.
2. More tokens require more compute and memory, which usually increases response time and token charges.
3. p95 shows tail behavior for slower requests, which better reflects real user pain than averages.
4. Because queue delay and model compute delay have different root causes and require different fixes.
5. Output tokens or retrieval payload size can grow silently, increasing per-request cost.

### 7) Practice

#### Mini-exercise

A support feature handles 1,000,000 requests per month.

- Current average per request: input 1,200 tokens, output 500 tokens
- New prompt design would reduce input by 20 percent but increase output by 10 percent

1. Compute old total tokens per request.
2. Compute new total tokens per request.
3. Decide whether this change is likely to help or hurt cost, assuming equal price per token for quick estimation.
4. Name one latency risk and one mitigation.

#### Mini-exercise Answers

1. Old total = 1,200 + 500 = 1,700 tokens.
2. New input = 1,200 * 0.8 = 960 tokens. New output = 500 * 1.1 = 550 tokens. New total = 960 + 550 = 1,510 tokens.
3. Likely helps cost in this simplified estimate because total tokens drop from 1,700 to 1,510 per request.
4. Latency risk: longer outputs can still increase generation time for some requests. Mitigation: set output caps and monitor p95 with route-level alerts.

#### Capstone-style system design question

Design token and latency guardrails for a three-tier GenAI product (free, pro, enterprise) where all tiers share the same base model but have different SLA and cost expectations. Define per-tier limits, what you will monitor, and what degradation strategy you apply under overload.

#### Capstone-style Answer Outline

- Free tier: strict token caps, smaller retrieval payload, relaxed latency SLA.
- Pro tier: moderate token caps, better retrieval depth, tighter latency SLA.
- Enterprise tier: highest limits with dedicated quotas and stronger isolation controls.
- Monitor: token distributions, p95 latency, queue depth, timeout rate, per-tenant spend.
- Overload strategy: reduce retrieval depth, reduce max output tokens, prioritize higher SLA tiers, and shed non-critical traffic gracefully.

### 8) Production Reality Check (Mandatory Ending)

If this fails in prod, what is the first thing we inspect?

We inspect per-route token distributions and the split between queue wait time and inference time.

Why:

Most real failures here come from budget drift (token growth) or saturation (queue and concurrency pressure), and those two signals identify root cause fastest.

### 9) Curiosity Bridge (Mandatory Ending)

Now you can reason about the core operating metrics of any GenAI call.

The next step is to connect these metrics to architecture choices in the full GenAI application anatomy: model layer, prompt layer, tool layer, and retrieval layer. That is where optimization becomes system design, not only prompt tuning.