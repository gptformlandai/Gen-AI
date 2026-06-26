# Project 7: Data-Heavy Assistant And Framework Selection Memo

This project implements a **contract data assistant**.

The assistant parses semi-structured contract documents into typed sections, clauses, tables, and metadata. It then answers questions by retrieving from those structured elements instead of treating the document as generic chat context.

## Why This Is Data-Heavy

Contracts are not just long text. Important meaning is carried by:

- section hierarchy;
- clause numbers;
- tables with service levels and remedies;
- key-value metadata such as parties, effective date, and governing law;
- obligations with actors such as `Customer`, `Vendor`, or `Processor`;
- exceptions and cross-references.

A generic chatbot over raw text can miss table rows, merge sections, or lose which party owns an obligation. This project makes those structures explicit.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| Document ingestion and structure-aware parsing | `parser.py` extracts front matter, headings, clauses, tables, and obligations. |
| Retrieval/workflow path suited to data-heavy work | `index.py` builds a typed structured index over clauses, tables, and metadata. |
| Framework/runtime comparison | `docs/framework_selection_memo.md` compares LlamaIndex, LangChain, LangGraph, ADK, and OpenAI Agents SDK. |
| Evaluation plan for document-heavy failure modes | `docs/evaluation_plan.md` lists table, clause, metadata, and grounding failure modes. |
| Difficult documents and handling notes | `docs/difficult_documents.md` explains the sample contracts and parsing strategy. |

## Architecture

```text
contract markdown files
    |
    v
front matter + section parser
    |
    v
typed elements: metadata, clauses, tables, obligations
    |
    v
structured index
    |
    v
query intent routing
    |
    v
answer with citations
```

## Run Locally

```bash
cd Projects/project-7-data-heavy-contract-assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Generate sample contracts:

```bash
contract-data build-samples --output data/contracts
```

Ask a question:

```bash
contract-data ask \
  --docs data/contracts \
  --question "What is the liability cap in the MSA?"
```

Evaluate:

```bash
contract-data evaluate \
  --docs data/contracts \
  --output docs/evaluation_results.md
```

The checked-in sample run passes all 12 golden questions and writes:

- `docs/parsed_documents.json` for parser inspection;
- `docs/evaluation_results.md` for the structure-heavy evaluation summary.

## Tests

```bash
pytest
```

The implementation is deterministic and does not require an API key.
