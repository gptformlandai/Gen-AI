# Failure Analysis Report

## Baseline Failures Targeted

Project 3 exposed two important failures:

- `eval-009`: report export options were refused because the baseline retrieval score was too weak.
- `eval-011`: incident triage retrieved audit-trail content instead of incident-triage content.

## Advanced Fixes

- Query rewriting expands `export options` into `export analytics reports csv date range download`.
- Query rewriting expands `incident triage` into `operators classify incidents severity owner notify stakeholders`.
- Reranking boosts candidates whose topic profile matches the query intent.
- Guardrails refuse unsafe and unauthorized questions before retrieval.

## Remaining Risks

- The local embedding model is still a teaching scaffold, not a production semantic model.
- Rule-based rewrites can miss paraphrases outside the known patterns.
- Role checks are string-based and should connect to a real identity and authorization system in production.
- Reranking adds CPU cost and tuning complexity.
