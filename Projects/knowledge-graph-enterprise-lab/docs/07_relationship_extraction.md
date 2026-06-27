# 07 Relationship Extraction

## What It Is

Relationship extraction detects edges like `CALLS`, `READS_FROM`, `PUBLISHES_TO`, and `MITIGATED_BY` from text.

## Why It Matters

Relationships are the reason the graph can answer multi-hop operational questions. Missing edges are often worse than missing documents.

## Where It Appears

- `extraction/relationship_extractor.py`
- `extraction/extraction_models.py`
- `tests/test_relationship_extraction.py`

## How To Run

```bash
python -m kg_enterprise_lab.examples.run_extraction_demo
```

## How To Extend

Add patterns for new relationship verbs, then map extracted names through `EntityResolver` before mutation.

## Common Mistakes

- Extracting relationships before entity resolution.
- Losing relationship direction.
- Not storing confidence and evidence text.
