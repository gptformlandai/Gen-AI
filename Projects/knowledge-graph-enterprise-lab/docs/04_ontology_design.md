# 04 Ontology Design

## What It Is

An ontology defines allowed node classes, relationship types, required properties, cardinality rules, and evolution rules.

## Why It Matters

Without an ontology, the graph slowly fills with near-duplicate labels and ambiguous relationships. Validation keeps the graph queryable and trustworthy.

## Where It Appears

- `data/ontology/enterprise_ontology.yaml`
- `data/ontology/shacl_constraints.yaml`
- `ontology/ontology_models.py`
- `ontology/ontology_validator.py`

## How To Run

```bash
kg-lab validate-ontology
```

## How To Extend

Add a label or relationship to the ontology, update graph construction, then add a validation test. For production, use a reviewed migration process before writing changed ontology rules.

Relationship domain and range are enforced through `RelationshipShape`, so an edge such as `Service -OWNED_BY-> Database` fails validation.

## Common Mistakes

- Adding labels without asking what questions they support.
- Over-modeling every attribute as a node.
- Changing ontology rules without versioning.
