from __future__ import annotations

import json
from pathlib import Path

from advanced_rag_assistant.chunking import chunk_documents
from advanced_rag_assistant.corpus import read_jsonl_documents
from advanced_rag_assistant.rag import AdvancedRagAssistant, BaselineRagAssistant
from advanced_rag_assistant.schemas import (
    ComparisonRow,
    ComparisonSummary,
    EvaluationQuestion,
    EvaluationResult,
    RagAnswer,
)
from advanced_rag_assistant.vector_store import InMemoryVectorStore


def read_evaluation_questions(path: Path) -> list[EvaluationQuestion]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [EvaluationQuestion.model_validate(item) for item in payload]


def build_store_from_corpus(path: Path) -> InMemoryVectorStore:
    documents = read_jsonl_documents(path)
    return InMemoryVectorStore.from_chunks(chunk_documents(documents))


def evaluate_answer(question: EvaluationQuestion, answer: RagAnswer) -> EvaluationResult:
    citation_topics = sorted({citation.metadata.get("topic", "") for citation in answer.citations})
    missing_terms = [
        term for term in question.expected_terms if term.lower() not in answer.answer.lower()
    ]

    if question.expected_status == "refused":
        passed = answer.status == "refused"
        category = "pass" if passed else "expected_refusal_failed"
    elif answer.status == "refused":
        passed = False
        category = "unexpected_refusal"
    elif not set(question.expected_topics) & set(citation_topics):
        passed = False
        category = "missed_retrieval"
    elif missing_terms:
        passed = False
        category = "weak_answer_synthesis"
    else:
        passed = True
        category = "pass"

    return EvaluationResult(
        status=answer.status,
        passed=passed,
        failure_category=category,
        citation_topics=citation_topics,
        missing_terms=missing_terms,
        answer=answer.answer,
    )


def compare_systems(
    baseline: BaselineRagAssistant,
    advanced: AdvancedRagAssistant,
    questions: list[EvaluationQuestion],
) -> ComparisonSummary:
    rows: list[ComparisonRow] = []
    for question in questions:
        baseline_result = evaluate_answer(
            question,
            baseline.answer(question.question, user_role=question.user_role),
        )
        advanced_result = evaluate_answer(
            question,
            advanced.answer(question.question, user_role=question.user_role),
        )
        rows.append(
            ComparisonRow(
                question_id=question.id,
                question=question.question,
                user_role=question.user_role,
                expected_status=question.expected_status,
                baseline=baseline_result,
                advanced=advanced_result,
                improved=not baseline_result.passed and advanced_result.passed,
            )
        )

    baseline_passed = sum(1 for row in rows if row.baseline.passed)
    advanced_passed = sum(1 for row in rows if row.advanced.passed)
    total = len(rows)
    return ComparisonSummary(
        total_questions=total,
        baseline_passed=baseline_passed,
        advanced_passed=advanced_passed,
        baseline_pass_rate=baseline_passed / max(total, 1),
        advanced_pass_rate=advanced_passed / max(total, 1),
        improved_count=sum(1 for row in rows if row.improved),
        rows=rows,
    )


def render_comparison(summary: ComparisonSummary) -> str:
    lines = [
        "# Baseline vs Advanced RAG Comparison",
        "",
        f"- Total questions: {summary.total_questions}",
        f"- Baseline passed: {summary.baseline_passed} ({summary.baseline_pass_rate:.2%})",
        f"- Advanced passed: {summary.advanced_passed} ({summary.advanced_pass_rate:.2%})",
        f"- Improved failures: {summary.improved_count}",
        "",
        "| Question | Role | Expected | Baseline | Advanced | Improved | Baseline category | Advanced category |",
        "|---|---|---|---:|---:|---:|---|---|",
    ]
    for row in summary.rows:
        lines.append(
            f"| {row.question_id} | {row.user_role} | {row.expected_status} | "
            f"{row.baseline.passed} | {row.advanced.passed} | {row.improved} | "
            f"{row.baseline.failure_category} | {row.advanced.failure_category} |"
        )

    lines.extend(
        [
            "",
            "## Before-vs-After Notes",
            "",
            "- `eval-009` improves because query rewriting adds terms from the report export document.",
            "- `eval-011` improves because incident-triage rewriting and reranking boost the incident runbook.",
            "- `eval-023` and `eval-024` show permission-aware refusal for employee access to audit/admin details.",
        ]
    )
    return "\n".join(lines) + "\n"
