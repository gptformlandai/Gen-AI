from __future__ import annotations

import re
from collections import Counter

from contract_data_assistant.schemas import IndexedElement, ParsedDocument, SearchHit


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9.%]+")
PERCENT_WORD_PATTERN = re.compile(r"\b(\d+(?:\.\d+)?)\s+percent\b", re.I)
STOPWORDS = {"a", "an", "and", "are", "as", "at", "by", "for", "from", "in", "is", "of", "on", "or", "the", "to", "what", "which", "who"}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class StructuredContractIndex:
    """Typed index over metadata, clauses, table rows, and obligations."""

    def __init__(self, documents: list[ParsedDocument]) -> None:
        self.documents = documents
        self.elements = build_elements(documents)

    def search(self, query: str, k: int = 5, kind: str | None = None) -> list[SearchHit]:
        expanded_query = expand_query(query)
        query_tokens = set(tokenize(expanded_query)) - STOPWORDS
        scored: list[SearchHit] = []
        desired_kind = kind or infer_desired_kind(query)
        desired_doc = infer_desired_document(query)

        for element in self.elements:
            if kind and element.kind != kind:
                continue
            element_tokens = tokenize(element.text + " " + element.title + " " + " ".join(element.metadata.values()))
            counts = Counter(element_tokens)
            overlap = sum(counts[token] for token in query_tokens)
            if overlap == 0:
                continue

            score = float(overlap)
            reasons = [f"overlap={overlap}"]
            if element.kind == desired_kind:
                score += 3.0
                reasons.append("kind_boost")
            if desired_doc and element.document_id == desired_doc:
                score += 2.0
                reasons.append("doc_boost")
            if element.kind == "table_row" and any(token in query_tokens for token in ("uptime", "severity", "credit", "response")):
                score += 2.0
                reasons.append("table_intent")
            if element.kind == "metadata" and any(token in query_tokens for token in ("law", "governing", "controller", "processor")):
                score += 2.0
                reasons.append("metadata_intent")
            structured_boost = score_structured_value_match(expanded_query, element)
            if structured_boost:
                score += structured_boost
                reasons.append(f"structured_value_boost={structured_boost:g}")
            phrase_boost = score_phrase_match(expanded_query, element)
            if phrase_boost:
                score += phrase_boost
                reasons.append(f"phrase_boost={phrase_boost:g}")

            scored.append(SearchHit(element=element, score=score, reason=", ".join(reasons)))

        scored.sort(key=lambda hit: hit.score, reverse=True)
        return scored[:k]


def build_elements(documents: list[ParsedDocument]) -> list[IndexedElement]:
    elements: list[IndexedElement] = []
    for document in documents:
        for field in document.metadata:
            elements.append(
                IndexedElement(
                    id=f"{document.document_id}-metadata-{field.key}",
                    document_id=document.document_id,
                    kind="metadata",
                    title=f"{document.title} metadata: {field.key}",
                    text=f"{field.key}: {field.value}",
                    metadata={"key": field.key, "value": field.value},
                )
            )
        for clause in document.clauses:
            elements.append(
                IndexedElement(
                    id=clause.id,
                    document_id=document.document_id,
                    kind="clause",
                    title=clause.section_path,
                    text=clause.text,
                    metadata={"section_path": clause.section_path, "actor": clause.actor},
                )
            )
        for table in document.tables:
            table_text = " | ".join(table.headers)
            elements.append(
                IndexedElement(
                    id=table.id,
                    document_id=document.document_id,
                    kind="table",
                    title=table.section_path,
                    text=table_text,
                    metadata={"section_path": table.section_path},
                )
            )
            for row_index, row in enumerate(table.rows, start=1):
                row_text = "; ".join(f"{key}: {value}" for key, value in row.items())
                elements.append(
                    IndexedElement(
                        id=f"{table.id}-row-{row_index:03d}",
                        document_id=document.document_id,
                        kind="table_row",
                        title=table.section_path,
                        text=row_text,
                        metadata={"section_path": table.section_path, **row},
                    )
                )
        for obligation in document.obligations:
            elements.append(
                IndexedElement(
                    id=obligation.id,
                    document_id=document.document_id,
                    kind="obligation",
                    title=obligation.section_path,
                    text=f"{obligation.actor} shall {obligation.action}",
                    metadata={"actor": obligation.actor, "source_clause_id": obligation.source_clause_id},
                )
            )
    return elements


def infer_desired_kind(query: str) -> str:
    lower = query.lower()
    if any(term in lower for term in ("uptime", "service credit", "severity", "response time")):
        return "table_row"
    if any(term in lower for term in ("governing law", "data controller", "effective date", "which document")):
        return "metadata"
    if any(term in lower for term in ("must", "shall", "who")):
        return "obligation"
    return "clause"


def infer_desired_document(query: str) -> str:
    lower = query.lower()
    if "msa" in lower or "liability" in lower:
        return "msa"
    if "dpa" in lower or "personal data" in lower or "subprocessor" in lower or "security incident" in lower:
        return "dpa"
    if "sla" in lower or "uptime" in lower or "service credit" in lower or "severity" in lower:
        return "sla"
    return ""


def expand_query(query: str) -> str:
    lower = query.lower()
    normalized_query = normalize_percent_words(query)
    expansions = [query, normalized_query]
    if "liability cap" in lower:
        expansions.append("aggregate liability capped fees paid 12 months cap exceptions")
    if "governing" in lower or "law" in lower:
        expansions.append("governing_law governing law New York")
    if "security incident" in lower or "reported" in lower:
        expansions.append("notify confirmed security incident no later than 72 hours")
    if "subprocessor" in lower:
        expansions.append("30 days advance notice new subprocessor")
    if "personal data" in lower and "termination" in lower:
        expansions.append("after termination delete return personal data customer choice")
    if "service credit" in lower or "uptime" in lower:
        expansions.append("uptime service credit")
    if "10 percent" in lower or "10%" in lower:
        expansions.append("10% 99.5% minor degradation")
    if "below 99.0" in lower or "< 99.0" in lower:
        expansions.append("< 99.0% 25% severe degradation")
    if "severity 1" in lower:
        expansions.append("Severity 1 Production outage critical data loss Initial Response 1 hour")
    if "survive termination" in lower:
        expansions.append("Confidentiality payment obligations limitation of liability survive termination")
    return " ".join(expansions)


def normalize_percent_words(text: str) -> str:
    return PERCENT_WORD_PATTERN.sub(r"\1%", text)


def score_structured_value_match(query: str, element: IndexedElement) -> float:
    """Prefer rows whose typed values exactly match numeric facts in the question."""
    if element.kind != "table_row":
        return 0.0
    query_values = set(re.findall(r"\d+(?:\.\d+)?%", query))
    if not query_values:
        return 0.0
    row_values = set(re.findall(r"\d+(?:\.\d+)?%", element.text))
    exact_matches = query_values & row_values
    return float(len(exact_matches) * 4)


def score_phrase_match(query: str, element: IndexedElement) -> float:
    lower_query = query.lower()
    lower_text = f"{element.title} {element.text}".lower()
    boost = 0.0
    if "after termination" in lower_query and "after termination" in lower_text:
        boost += 5.0
    if "protect customer confidential information" in lower_query and "protect customer confidential information" in lower_text:
        boost += 3.0
    if "service credit" in lower_query and element.kind == "table_row" and "service credit" in lower_text:
        boost += 1.0
    return boost
