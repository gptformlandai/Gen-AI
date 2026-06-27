# 20 Troubleshooting

## What It Is

Troubleshooting covers common local and production-style issues.

## Why It Matters

Knowledge graph systems fail through missing sources, duplicate IDs, invalid ontology rules, slow traversals, and ungrounded answers.

## Where It Appears

- CLI: `cli/commands.py`
- Validation: `ontology/ontology_validator.py`
- Governance: `governance/risk_checker.py`

## How To Run

```bash
kg-lab ingest-sample-data
kg-lab validate-ontology
kg-lab run-evals
```

## How To Extend

Add runbook entries for real incidents and failed eval cases.

## Common Mistakes

- Debugging GraphRAG before confirming entity linking.
- Assuming an empty answer means no relationship exists.
- Ignoring duplicate detection warnings.
