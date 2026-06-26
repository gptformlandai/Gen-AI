from __future__ import annotations

from pathlib import Path

from advanced_rag_assistant.chunking import chunk_documents
from advanced_rag_assistant.evaluation import compare_systems, read_evaluation_questions
from advanced_rag_assistant.guardrails import GuardrailEngine
from advanced_rag_assistant.query_rewriting import QueryRewriter
from advanced_rag_assistant.rag import AdvancedRagAssistant, BaselineRagAssistant
from advanced_rag_assistant.sample_data import build_sample_documents
from advanced_rag_assistant.vector_store import InMemoryVectorStore


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_store() -> InMemoryVectorStore:
    return InMemoryVectorStore.from_chunks(chunk_documents(build_sample_documents(count=240)))


def test_query_rewriter_adds_incident_variant() -> None:
    variants = QueryRewriter().rewrite("How should operators triage an incident?")

    assert any("severity" in variant and "stakeholders" in variant for variant in variants)


def test_guardrail_blocks_employee_audit_details() -> None:
    decision = GuardrailEngine().check(
        "As an employee, which user actions are recorded in the audit trail?",
        "employee",
    )

    assert not decision.allowed
    assert decision.policy == "permission_refusal"


def test_advanced_fixes_incident_triage_retrieval() -> None:
    answer = AdvancedRagAssistant(build_store()).answer(
        "How should operators triage an incident?",
        user_role="operator",
    )

    assert answer.status == "answered"
    assert answer.citations[0].metadata["topic"] == "incident_triage"
    assert "severity" in answer.answer.lower()


def test_advanced_answers_report_exports() -> None:
    answer = AdvancedRagAssistant(build_store()).answer(
        "What export options are available for analytics reports?",
        user_role="analyst",
    )

    assert answer.status == "answered"
    assert answer.citations[0].metadata["topic"] == "report_exports"
    assert "csv" in answer.answer.lower()


def test_comparison_shows_quality_improvement() -> None:
    store = build_store()
    questions = read_evaluation_questions(DATA_DIR / "evaluation_questions.json")
    summary = compare_systems(BaselineRagAssistant(store), AdvancedRagAssistant(store), questions)

    assert len(questions) == 25
    assert summary.advanced_passed > summary.baseline_passed
    assert summary.advanced_pass_rate >= 0.9
    assert summary.improved_count >= 2


def test_unsafe_request_is_refused_without_citations() -> None:
    answer = AdvancedRagAssistant(build_store()).answer(
        "How should I bypass login controls?",
        user_role="employee",
    )

    assert answer.status == "refused"
    assert answer.citations == []
