from __future__ import annotations

import json
from pathlib import Path

from baseline_rag_assistant.chunking import chunk_documents
from baseline_rag_assistant.corpus import read_jsonl_documents
from baseline_rag_assistant.rag import BaselineRagAssistant
from baseline_rag_assistant.schemas import EvaluationQuestion, EvaluationRow, EvaluationSummary, RagAnswer
from baseline_rag_assistant.vector_store import InMemoryVectorStore


def read_evaluation_questions(path: Path) -> list[EvaluationQuestion]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [EvaluationQuestion.model_validate(item) for item in payload]


def build_assistant_from_corpus(corpus_path: Path) -> BaselineRagAssistant:
    documents = read_jsonl_documents(corpus_path)
    chunks = chunk_documents(documents)
    store = InMemoryVectorStore.from_chunks(chunks)
    return BaselineRagAssistant(store)


def evaluate_answer(question: EvaluationQuestion, answer: RagAnswer) -> EvaluationRow:
    citation_topics = sorted({citation.metadata.get("topic", "") for citation in answer.citations})
    missing_terms = [
        term for term in question.expected_terms if term.lower() not in answer.answer.lower()
    ]

    if question.should_refuse:
        passed = answer.status == "refused"
        failure_category = "pass" if passed else "expected_refusal_failed"
    elif answer.status == "refused":
        passed = False
        failure_category = "unexpected_refusal"
    elif not set(question.expected_topics) & set(citation_topics):
        passed = False
        failure_category = "missed_retrieval"
    elif not answer.citations:
        passed = False
        failure_category = "wrong_grounding"
    elif missing_terms:
        passed = False
        failure_category = "weak_answer_synthesis"
    else:
        passed = True
        failure_category = "pass"

    return EvaluationRow(
        question_id=question.id,
        question=question.question,
        status=answer.status,
        passed=passed,
        failure_category=failure_category,
        citation_topics=citation_topics,
        missing_terms=missing_terms,
        answer=answer.answer,
    )


def evaluate_questions(
    assistant: BaselineRagAssistant,
    questions: list[EvaluationQuestion],
) -> EvaluationSummary:
    rows = [evaluate_answer(question, assistant.answer(question.question)) for question in questions]
    passed = sum(1 for row in rows if row.passed)
    total = len(rows)
    return EvaluationSummary(
        total_questions=total,
        passed=passed,
        failed=total - passed,
        pass_rate=passed / max(total, 1),
        rows=rows,
    )


def render_evaluation_sheet(summary: EvaluationSummary) -> str:
    lines = [
        "# Baseline RAG Evaluation Sheet",
        "",
        f"- Total questions: {summary.total_questions}",
        f"- Passed: {summary.passed}",
        f"- Failed: {summary.failed}",
        f"- Pass rate: {summary.pass_rate:.2%}",
        "",
        "| Question | Status | Passed | Failure category | Citation topics | Missing terms |",
        "|---|---|---:|---|---|---|",
    ]
    for row in summary.rows:
        lines.append(
            f"| {row.question_id} | {row.status} | {row.passed} | {row.failure_category} | "
            f"{', '.join(row.citation_topics) or 'none'} | {', '.join(row.missing_terms) or 'none'} |"
        )
    return "\n".join(lines) + "\n"


def render_citation_examples(answers: list[RagAnswer]) -> str:
    lines = ["# Citation Examples", ""]
    for answer in answers:
        if answer.status != "answered":
            continue
        lines.append(f"## {answer.question}")
        lines.append("")
        lines.append(answer.answer)
        lines.append("")
        for citation in answer.citations:
            lines.append(
                f"- [{citation.citation_id}] `{citation.document_id}` / `{citation.chunk_id}` "
                f"score={citation.score:.3f}: {citation.quote}"
            )
        lines.append("")
        if len(lines) > 45:
            break
    return "\n".join(lines)
