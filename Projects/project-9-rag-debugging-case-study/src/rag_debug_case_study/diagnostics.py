from __future__ import annotations

from rag_debug_case_study.schemas import AssistantAnswer, EvaluationQuestion, FailureLayer


def diagnose_failure(question: EvaluationQuestion, answer: AssistantAnswer, top3_doc_ids: list[str], missing_terms: list[str]) -> FailureLayer:
    if not missing_terms and answer.citations and answer.citations[0].doc_id == question.expected_doc_id:
        return "none"
    if not answer.citations:
        return "refusal"
    if question.expected_doc_id not in top3_doc_ids:
        return "retrieval"
    if answer.citations[0].doc_id != question.expected_doc_id:
        return "retrieval"
    if missing_terms:
        return "synthesis"
    return "evaluation_coverage"

