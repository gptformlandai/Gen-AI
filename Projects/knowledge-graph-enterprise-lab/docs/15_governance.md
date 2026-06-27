# 15 Governance

## What It Is

Governance controls query allowlists, risky traversal prevention, access-control placeholders, redaction, audit logging, confidence thresholds, human review, and ontology change review.

## Why It Matters

Knowledge graphs often contain sensitive system and ownership metadata. Production systems need guardrails before they expose broad traversal.

## Where It Appears

- `governance/query_policy.py`
- `governance/risk_checker.py`
- `governance/redaction.py`
- `governance/audit_logger.py`
- `governance/change_review.py`
- `query/graph_query_service.py`

## How To Run

```bash
kg-lab validate-ontology
kg-lab detect-duplicates
```

The main query service enforces intent allowlisting and traversal-depth policy before running handlers.

## How To Extend

Connect access checks to your identity provider, tag sensitive labels, and require approval for ontology or high-impact graph mutations.

## Common Mistakes

- Exposing unrestricted Cypher/SPARQL.
- Logging sensitive owner data without redaction.
- Auto-accepting low-confidence LLM extractions.
