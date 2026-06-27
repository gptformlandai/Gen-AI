# 08 Entity Resolution

## What It Is

Entity resolution maps aliases, fuzzy names, and duplicate records to canonical graph IDs.

## Why It Matters

Enterprise catalogs often contain `provider-search-service`, `provider search service`, and `providers-svc` as separate strings. Without resolution, queries miss data or double count services.

## Where It Appears

- `resolution/alias_manager.py`
- `resolution/duplicate_detector.py`
- `resolution/entity_resolver.py`
- `resolution/human_review_queue.py`

## How To Run

```bash
kg-lab detect-duplicates
```

## How To Extend

Add deterministic aliases first, then fuzzy matching, then human review for uncertain merges.

## Common Mistakes

- Auto-merging low-confidence duplicates.
- Ignoring ownership conflicts.
- Merging nodes without rewiring relationships.
