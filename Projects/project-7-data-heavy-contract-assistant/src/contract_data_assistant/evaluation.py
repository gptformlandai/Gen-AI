from __future__ import annotations

import json
from pathlib import Path

from contract_data_assistant.assistant import ContractDataAssistant
from contract_data_assistant.parser import load_raw_documents, parse_document
from contract_data_assistant.index import StructuredContractIndex
from contract_data_assistant.schemas import EvaluationQuestion, EvaluationRow, EvaluationSummary


def build_assistant_from_directory(directory: Path) -> ContractDataAssistant:
    parsed = [parse_document(raw) for raw in load_raw_documents(directory)]
    return ContractDataAssistant(StructuredContractIndex(parsed))


def read_evaluation_questions(path: Path) -> list[EvaluationQuestion]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [EvaluationQuestion.model_validate(item) for item in payload]


def evaluate(assistant: ContractDataAssistant, questions: list[EvaluationQuestion]) -> EvaluationSummary:
    rows: list[EvaluationRow] = []
    for question in questions:
        answer = assistant.answer(question.question)
        citation_docs = sorted({citation.document_id for citation in answer.citations})
        citation_kinds = sorted({citation.kind for citation in answer.citations})
        missing_terms = [
            term for term in question.expected_terms if term.lower() not in answer.answer.lower()
        ]
        passed = (
            bool(set(question.expected_docs) & set(citation_docs))
            and question.expected_kind in citation_kinds
            and not missing_terms
        )
        rows.append(
            EvaluationRow(
                question_id=question.id,
                passed=passed,
                citation_docs=citation_docs,
                citation_kinds=citation_kinds,
                missing_terms=missing_terms,
                answer=answer.answer,
            )
        )
    passed_count = sum(1 for row in rows if row.passed)
    return EvaluationSummary(
        total=len(rows),
        passed=passed_count,
        pass_rate=passed_count / max(len(rows), 1),
        rows=rows,
    )


def render_evaluation(summary: EvaluationSummary) -> str:
    lines = [
        "# Data-Heavy Assistant Evaluation Results",
        "",
        f"- Total questions: {summary.total}",
        f"- Passed: {summary.passed}",
        f"- Pass rate: {summary.pass_rate:.2%}",
        "",
        "| Question | Passed | Citation docs | Citation kinds | Missing terms |",
        "|---|---:|---|---|---|",
    ]
    for row in summary.rows:
        lines.append(
            f"| {row.question_id} | {row.passed} | {', '.join(row.citation_docs) or 'none'} | "
            f"{', '.join(row.citation_kinds) or 'none'} | {', '.join(row.missing_terms) or 'none'} |"
        )
    return "\n".join(lines) + "\n"
