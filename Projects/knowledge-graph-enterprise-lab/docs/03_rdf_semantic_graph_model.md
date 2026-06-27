# 03 RDF Semantic Graph Model

## What It Is

RDF represents knowledge as triples: subject, predicate, object. RDF adds URI semantics, RDFS/OWL vocabularies, and SPARQL queries.

## Why It Matters

RDF is useful when interoperability, vocabularies, semantic reasoning, or cross-organization data exchange matters more than property-rich traversal ergonomics.

## Where It Appears

- Turtle ontology: `data/ontology/enterprise_ontology.ttl`
- Local triple store: `graph/rdf_triple_store.py`
- Serializer: `ontology/rdf_serializer.py`
- SPARQL templates: `query/sparql_templates.py`
- Local SPARQL-style executor: `query/sparql_executor.py`

## How To Run

```bash
kg-lab export-graph --format ttl
kg-lab run-sparql --template service_dependencies
kg-lab query-graph --question "Compare RDF and property graph representation for this model."
```

## How To Extend

Map new labels to RDF classes and new relationship types to object properties. Load the exported Turtle into Fuseki, GraphDB, Neptune RDF, or another SPARQL endpoint.

## Common Mistakes

- Expecting RDF triples to behave like property graph edges with arbitrary nested properties.
- Skipping stable URIs.
- Mixing domain vocabulary changes with raw data ingestion.
