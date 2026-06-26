# Framework Selection Memo

## Recommendation

For a production version of this contract assistant, use:

- **LlamaIndex for the data plane**: parsing, document nodes, structured indices, metadata-aware retrieval, and citation-oriented query engines.
- **LangGraph for the control plane** when the workflow becomes multi-step: review queues, extraction retries, human approval, and remediation loops.

This project implements the first version locally so the mechanisms stay visible, but the architecture maps naturally to that split.

## Comparison

| Framework / runtime | Strength | Weakness | Fit for this project |
|---|---|---|---|
| LlamaIndex | Strong document ingestion, parsing, indexing, metadata filters, query engines | Less ideal as the only orchestration layer for complex approvals | Best fit for data-heavy parsing and retrieval |
| LangChain | Broad integration glue and simple chains | Can become too generic for document structure if used alone | Useful for model/tool calls, not the core data model |
| LangGraph | Explicit stateful workflows, retries, human review, recovery branches | Does not solve document parsing by itself | Best later when extraction and review become workflow-heavy |
| ADK | Agent runtime patterns and operational packaging | More runtime-oriented than data-model-oriented | Good comparison target, not first choice for document parsing |
| OpenAI Agents SDK | Tool-centric agent runtime with clean handoffs | The data indexing layer still needs design | Good for agentic workflows after the data layer is mature |

## Why Not Use Only A Chatbot

Contract questions often require exact structure:

- "Which table row has uptime below 99.9%?"
- "Who owns breach notification?"
- "What is the liability cap exception?"
- "Which clauses survive termination?"

Flattening all text into one prompt loses section IDs, row provenance, and obligation ownership. The assistant should first create structured data, then answer from it.

## Production Upgrade Path

1. Replace local markdown parsing with LlamaParse, Unstructured, or a custom PDF parser.
2. Store typed nodes in a document index with metadata filters.
3. Add table-specific retrieval and reranking.
4. Use LangGraph for human review of low-confidence extractions.
5. Use an agent runtime only after tools, state, and review boundaries are clear.
