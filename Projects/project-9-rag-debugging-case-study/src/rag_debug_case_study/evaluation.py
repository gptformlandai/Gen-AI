from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from rag_debug_case_study.assistant import RagDebugAssistant
from rag_debug_case_study.diagnostics import diagnose_failure
from rag_debug_case_study.sample_data import DOCUMENTS
from rag_debug_case_study.schemas import ComparisonSummary, EvaluationQuestion, EvaluationRow, EvaluationSummary, RetrieverMode


def read_questions(path: Path) -> list[EvaluationQuestion]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [EvaluationQuestion.model_validate(item) for item in payload]


def evaluate(mode: RetrieverMode, questions: list[EvaluationQuestion]) -> EvaluationSummary:
    assistant = RagDebugAssistant(DOCUMENTS, mode=mode)
    rows: list[EvaluationRow] = []
    total_expected_terms = 0
    total_present_terms = 0

    for question in questions:
        answer = assistant.answer(question.question)
        top3_doc_ids = [citation.doc_id for citation in answer.citations[:3]]
        actual_doc_id = answer.citations[0].doc_id if answer.citations else ""
        missing_terms = [
            term for term in question.expected_terms if term.lower() not in answer.answer.lower()
        ]
        total_expected_terms += len(question.expected_terms)
        total_present_terms += len(question.expected_terms) - len(missing_terms)
        passed = actual_doc_id == question.expected_doc_id and not missing_terms
        failure_layer = diagnose_failure(question, answer, top3_doc_ids, missing_terms)
        rows.append(
            EvaluationRow(
                question_id=question.id,
                question=question.question,
                category=question.category,
                passed=passed,
                expected_doc_id=question.expected_doc_id,
                actual_doc_id=actual_doc_id,
                top3_doc_ids=top3_doc_ids,
                missing_terms=missing_terms,
                failure_layer=failure_layer,
                answer=answer.answer,
            )
        )

    passed = sum(row.passed for row in rows)
    top1 = sum(row.actual_doc_id == row.expected_doc_id for row in rows)
    top3 = sum(row.expected_doc_id in row.top3_doc_ids for row in rows)
    failure_counts = Counter(row.failure_layer for row in rows if row.failure_layer != "none")
    return EvaluationSummary(
        mode=mode,
        total=len(rows),
        passed=passed,
        pass_rate=passed / max(len(rows), 1),
        top1_accuracy=top1 / max(len(rows), 1),
        top3_recall=top3 / max(len(rows), 1),
        term_coverage=total_present_terms / max(total_expected_terms, 1),
        failure_counts=dict(sorted(failure_counts.items())),
        rows=rows,
    )


def compare(questions: list[EvaluationQuestion]) -> ComparisonSummary:
    baseline = evaluate("baseline", questions)
    improved = evaluate("improved", questions)
    return ComparisonSummary(
        baseline=baseline,
        improved=improved,
        pass_rate_delta=improved.pass_rate - baseline.pass_rate,
        top1_accuracy_delta=improved.top1_accuracy - baseline.top1_accuracy,
        top3_recall_delta=improved.top3_recall - baseline.top3_recall,
    )


def render_metrics(comparison: ComparisonSummary) -> str:
    lines = [
        "# Before-Vs-After Metrics",
        "",
        "| Metric | Baseline | Improved | Delta |",
        "|---|---:|---:|---:|",
        metric_row("Pass rate", comparison.baseline.pass_rate, comparison.improved.pass_rate),
        metric_row("Top-1 document accuracy", comparison.baseline.top1_accuracy, comparison.improved.top1_accuracy),
        metric_row("Top-3 document recall", comparison.baseline.top3_recall, comparison.improved.top3_recall),
        metric_row("Expected term coverage", comparison.baseline.term_coverage, comparison.improved.term_coverage),
        "",
        "## Failure Counts",
        "",
        "| Failure layer | Baseline | Improved |",
        "|---|---:|---:|",
    ]
    layers = sorted(set(comparison.baseline.failure_counts) | set(comparison.improved.failure_counts))
    if not layers:
        layers = ["none"]
    for layer in layers:
        lines.append(
            f"| {layer} | {comparison.baseline.failure_counts.get(layer, 0)} | "
            f"{comparison.improved.failure_counts.get(layer, 0)} |"
        )
    lines.extend(
        [
            "",
            "## Row Results",
            "",
            "| Question | Category | Baseline pass | Improved pass | Baseline doc | Improved doc |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    improved_rows = {row.question_id: row for row in comparison.improved.rows}
    for row in comparison.baseline.rows:
        improved = improved_rows[row.question_id]
        lines.append(
            f"| {row.question_id} | {row.category} | {row.passed} | {improved.passed} | "
            f"{row.actual_doc_id or 'none'} | {improved.actual_doc_id or 'none'} |"
        )
    return "\n".join(lines) + "\n"


def render_failures(comparison: ComparisonSummary) -> str:
    lines = [
        "# Failure Cases",
        "",
        "This file keeps the failed baseline rows visible so the improvement is traceable.",
        "",
        "| Question | Category | Expected doc | Baseline doc | Failure layer | Missing terms | Improved pass |",
        "|---|---|---|---|---|---|---:|",
    ]
    improved_rows = {row.question_id: row for row in comparison.improved.rows}
    for row in comparison.baseline.rows:
        if row.passed:
            continue
        improved = improved_rows[row.question_id]
        lines.append(
            f"| {row.question_id} | {row.category} | {row.expected_doc_id} | {row.actual_doc_id or 'none'} | "
            f"{row.failure_layer} | {', '.join(row.missing_terms) or 'none'} | {improved.passed} |"
        )
    return "\n".join(lines) + "\n"


def metric_row(name: str, baseline: float, improved: float) -> str:
    return f"| {name} | {baseline:.2%} | {improved:.2%} | {improved - baseline:+.2%} |"

