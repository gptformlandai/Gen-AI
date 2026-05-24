# Module 1 - GenAI Landscape And Mental Models

This is the evolving knowledge base for Module 1.

Covered so far:

- Topic 1.1.a: Foundation model vs instruct model vs reasoning-oriented model

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