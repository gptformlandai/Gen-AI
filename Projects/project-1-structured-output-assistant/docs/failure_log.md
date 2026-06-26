# Failure Log

This log should be updated while testing real prompts. Project 1 requires at least five real issues, so we start with the first issues this design is built to expose.

| # | Issue | Why it matters | Mitigation |
|---|---|---|---|
| 1 | Vague requests can still produce confident-looking requirements. | The model may invent scope when the user did not provide enough detail. | Route incomplete inputs to `needs_clarification` before generation. |
| 2 | JSON wrapped in Markdown fences breaks naive parsers. | Many models return helpful-looking fenced JSON that downstream code cannot parse directly. | Strip fences and extract the first JSON object before Pydantic validation. |
| 3 | Hallucinated fields can slip into flexible schemas. | Extra keys can hide prompt drift and break consumers later. | Use `extra="forbid"` on all Pydantic models. |
| 4 | Missing acceptance criteria makes output less actionable. | Requirements without testable outcomes are hard to implement and evaluate. | Require acceptance criteria when status is `ready`. |
| 5 | Unsafe requests can look like normal feature requests. | A structured schema alone does not decide whether a request should be fulfilled. | Run a pre-generation safety check and return `refused` with a reason. |
| 6 | The first risky-term check missed inflected wording like `steals passwords`. | Exact string checks are brittle and can route unsafe requests to clarification instead of refusal. | Add common inflections now; later replace with a stronger policy classifier. |

## Open Follow-Ups

- Add latency and cost observations once the OpenAI-backed path is used.
- Add a small quality score beyond schema validity, such as acceptance-criteria completeness.
- Compare deterministic golden tests with live LLM output on the same prompt set.
