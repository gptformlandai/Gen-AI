from __future__ import annotations

from pathlib import Path

from rag_debug_case_study.assistant import RagDebugAssistant
from rag_debug_case_study.evaluation import compare, read_questions
from rag_debug_case_study.sample_data import DOCUMENTS


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def test_baseline_has_known_retrieval_failure() -> None:
    answer = RagDebugAssistant(DOCUMENTS, mode="baseline").answer("How should operators triage an incident?")

    assert answer.citations
    assert answer.citations[0].doc_id != "incident_response"


def test_improved_fixes_known_retrieval_failure() -> None:
    answer = RagDebugAssistant(DOCUMENTS, mode="improved").answer("How should operators triage an incident?")

    assert answer.citations[0].doc_id == "incident_response"
    assert "severity" in answer.answer.lower()
    assert "incident commander" in answer.answer.lower()


def test_before_after_metrics_improve() -> None:
    comparison = compare(read_questions(DATA_DIR / "evaluation_questions.json"))

    assert comparison.baseline.pass_rate < comparison.improved.pass_rate
    assert comparison.improved.pass_rate >= 0.9
    assert comparison.improved.top1_accuracy > comparison.baseline.top1_accuracy


def test_diagnosis_identifies_retrieval_as_dominant_baseline_failure() -> None:
    comparison = compare(read_questions(DATA_DIR / "evaluation_questions.json"))

    assert comparison.baseline.failure_counts.get("retrieval", 0) >= 3
    assert comparison.improved.failure_counts.get("retrieval", 0) == 0


def test_answer_synthesizer_is_shared_between_modes() -> None:
    baseline = RagDebugAssistant(DOCUMENTS, mode="baseline").answer("How do users reset a forgotten password?")
    improved = RagDebugAssistant(DOCUMENTS, mode="improved").answer("How do users reset a forgotten password?")

    assert baseline.answer == improved.answer
    assert baseline.citations[0].doc_id == improved.citations[0].doc_id == "password_reset"
