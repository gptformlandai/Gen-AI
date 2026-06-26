from __future__ import annotations

import json
from pathlib import Path

from baseline_rag_assistant.chunking import chunk_documents
from baseline_rag_assistant.evaluation import (
    evaluate_questions,
    read_evaluation_questions,
)
from baseline_rag_assistant.rag import BaselineRagAssistant
from baseline_rag_assistant.sample_data import build_sample_documents
from baseline_rag_assistant.tracing import JsonlTraceLogger
from baseline_rag_assistant.vector_store import InMemoryVectorStore


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_test_assistant() -> BaselineRagAssistant:
    documents = build_sample_documents(count=240)
    chunks = chunk_documents(documents)
    store = InMemoryVectorStore.from_chunks(chunks)
    return BaselineRagAssistant(store)


def test_rag_answer_returns_citations() -> None:
    assistant = build_test_assistant()
    result = assistant.answer("How do users reset a forgotten password?")

    assert result.status == "answered"
    assert result.citations
    assert result.citations[0].metadata["topic"] == "password_reset"
    assert "[S1]" in result.answer


def test_rag_refuses_when_evidence_is_insufficient() -> None:
    assistant = build_test_assistant()
    result = assistant.answer("What is the stock price of Apple tomorrow?")

    assert result.status == "refused"
    assert result.citations == []


def test_trace_logger_writes_jsonl(tmp_path: Path) -> None:
    assistant = build_test_assistant()
    trace_path = tmp_path / "trace.jsonl"
    assistant.answer(
        "What metrics are visible in the support ticket dashboard?",
        trace_logger=JsonlTraceLogger(trace_path),
    )

    lines = trace_path.read_text(encoding="utf-8").strip().splitlines()
    events = [json.loads(line)["event"] for line in lines]

    assert "retrieval" in events
    assert "answer_finalized" in events


def test_evaluation_question_set_has_required_size() -> None:
    questions = read_evaluation_questions(DATA_DIR / "evaluation_questions.json")

    assert 20 <= len(questions) <= 25


def test_evaluation_reveals_pass_fail_outcomes() -> None:
    assistant = build_test_assistant()
    questions = read_evaluation_questions(DATA_DIR / "evaluation_questions.json")
    summary = evaluate_questions(assistant, questions)

    assert summary.total_questions == len(questions)
    assert summary.pass_rate >= 0.75
    assert all(row.failure_category for row in summary.rows)


def test_answer_uses_cited_quote_text() -> None:
    assistant = build_test_assistant()
    result = assistant.answer("What does the CSV reconciliation workflow do with mismatches?")

    assert result.status == "answered"
    assert result.citations[0].quote in result.answer
