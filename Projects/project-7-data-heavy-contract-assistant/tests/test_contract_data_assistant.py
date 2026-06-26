from __future__ import annotations

from pathlib import Path

from contract_data_assistant.assistant import ContractDataAssistant
from contract_data_assistant.evaluation import evaluate, read_evaluation_questions
from contract_data_assistant.index import StructuredContractIndex
from contract_data_assistant.parser import parse_document
from contract_data_assistant.sample_data import SAMPLE_DOCUMENTS
from contract_data_assistant.schemas import RawDocument


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def build_assistant() -> ContractDataAssistant:
    parsed = [
        parse_document(RawDocument(document_id=filename.removesuffix(".md"), path=filename, text=text))
        for filename, text in SAMPLE_DOCUMENTS.items()
    ]
    return ContractDataAssistant(StructuredContractIndex(parsed))


def test_parser_extracts_metadata_clauses_tables_and_obligations() -> None:
    parsed = parse_document(RawDocument(document_id="sla", path="sla.md", text=SAMPLE_DOCUMENTS["sla.md"]))

    assert parsed.metadata
    assert parsed.clauses
    assert parsed.tables
    assert parsed.tables[0].rows[1]["Service Credit"] == "10%"


def test_parser_extracts_obligation_actor() -> None:
    parsed = parse_document(RawDocument(document_id="msa", path="msa.md", text=SAMPLE_DOCUMENTS["msa.md"]))

    actors = {obligation.actor for obligation in parsed.obligations}
    assert "Vendor" in actors
    assert "Customer" in actors


def test_assistant_answers_table_question_with_table_row_citation() -> None:
    answer = build_assistant().answer("What uptime commitment has a 10 percent service credit?")

    assert answer.citations
    assert answer.citations[0].kind == "table_row"
    assert "99.5%" in answer.answer
    assert "10%" in answer.answer


def test_assistant_answers_metadata_question_with_metadata_citation() -> None:
    answer = build_assistant().answer("Which law governs the MSA?")

    assert answer.citations[0].kind == "metadata"
    assert answer.citations[0].document_id == "msa"
    assert "New York" in answer.answer


def test_assistant_answers_clause_question_with_section_path() -> None:
    answer = build_assistant().answer("What is the liability cap in the MSA?")

    assert answer.citations[0].kind == "clause"
    assert answer.citations[0].document_id == "msa"
    assert "12 months" in answer.answer


def test_evaluation_passes_expected_threshold() -> None:
    assistant = build_assistant()
    questions = read_evaluation_questions(DATA_DIR / "evaluation_questions.json")
    summary = evaluate(assistant, questions)

    assert summary.total == 12
    assert summary.pass_rate >= 0.8
