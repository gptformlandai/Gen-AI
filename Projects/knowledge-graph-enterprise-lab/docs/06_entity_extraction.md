# 06 Entity Extraction

## What It Is

Entity extraction finds graph entities in unstructured text, such as architecture notes and incident summaries.

## Why It Matters

Architecture docs contain relationships that may not exist in service catalogs. Extraction lets the graph learn from text while preserving confidence and source references.

## Where It Appears

- `extraction/entity_extractor.py`
- `extraction/rule_based_extractor.py`
- `extraction/llm_extractor_placeholder.py`

## How To Run

```bash
python -m kg_enterprise_lab.examples.run_extraction_demo
```

## How To Extend

Replace the placeholder with a schema-constrained LLM call, keep confidence scores, and send uncertain entities to human review.

## Common Mistakes

- Trusting raw LLM extraction without ontology validation.
- Dropping the source sentence.
- Treating aliases as new canonical entities.
