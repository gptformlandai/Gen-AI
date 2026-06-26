# Evaluation Plan For Structure-Heavy Data

## Evaluation Dimensions

| Dimension | What can fail | Test signal |
|---|---|---|
| Metadata extraction | Parties, effective date, or governing law missed | Query answer lacks expected metadata term |
| Section parsing | Clauses assigned to wrong section | Citation points to wrong section path |
| Table extraction | Header/row alignment breaks | SLA or remedy answer misses exact value |
| Obligation ownership | Wrong actor assigned to obligation | Answer names wrong party |
| Exception handling | Cap exceptions or exclusions missed | Answer omits exception phrase |
| Cross-document retrieval | Wrong document answers similar query | Citation document ID mismatches expected document |

## Evaluation Set

The local evaluation uses deterministic questions over three difficult sample documents:

- Master Services Agreement
- Data Processing Addendum
- Service Level Agreement

Each question has:

- expected document IDs;
- expected answer terms;
- expected structure type such as `clause`, `obligation`, `table_row`, or `metadata`.

## Success Criteria

- At least 80% of evaluation questions pass.
- Table questions cite table rows.
- Clause questions cite section paths.
- Metadata questions cite the metadata element rather than random prose.

## Remaining Risk

The sample documents are markdown-like. Real PDFs add OCR, page headers, repeated footers, merged cells, and scanned signatures. Those should be evaluated separately before production use.
