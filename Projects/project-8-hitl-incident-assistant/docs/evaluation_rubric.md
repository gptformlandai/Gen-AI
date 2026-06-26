# Evaluation Rubric

This project evaluates long-lived human-in-the-loop behavior rather than single-turn answer quality.

| Dimension | Passing signal |
|---|---|
| Ambiguity handling | Incomplete reports enter `needs_clarification` and include concrete questions. |
| Human-review boundary | Unsafe actions enter `pending` and are not executed before approval. |
| Resumability | A persisted incident can be loaded and continued with approval, rejection, or observation. |
| Action planning | Required actions appear for the incident class, such as rollback after deploy or scale during capacity pressure. |
| Latency expectation | Estimated action latency remains within the configured workflow budget unless explicitly logged. |
| Event history | Each state transition writes an event with a timestamp and reason. |

## Scoring

Each evaluation case checks:

- expected severity;
- expected initial status;
- whether approval is pending;
- required action names;
- whether unsafe actions stayed unexecuted before approval;
- final status after approval when the case includes a resume step;
- latency budget compliance.

The project target is at least 85% of evaluation cases passing.

