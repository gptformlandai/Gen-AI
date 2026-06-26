from __future__ import annotations

import re
from pathlib import Path

from contract_data_assistant.schemas import (
    Clause,
    MetadataField,
    Obligation,
    ParsedDocument,
    RawDocument,
    Section,
    Table,
)


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
OBLIGATION_PATTERN = re.compile(r"\b(Customer|Vendor|Processor|Controller)\s+shall\s+(.+)", re.I)


def load_raw_documents(directory: Path) -> list[RawDocument]:
    documents: list[RawDocument] = []
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        document_id = path.stem
        front_matter, _ = split_front_matter(text)
        document_id = front_matter.get("document_id", document_id)
        documents.append(RawDocument(document_id=document_id, path=str(path), text=text))
    return documents


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    metadata: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, parts[2].strip()


def parse_document(raw: RawDocument) -> ParsedDocument:
    metadata_dict, body = split_front_matter(raw.text)
    metadata = [MetadataField(key=key, value=value) for key, value in metadata_dict.items()]
    title = metadata_dict.get("title", raw.document_id)

    sections: list[Section] = []
    clauses: list[Clause] = []
    tables: list[Table] = []
    obligations: list[Obligation] = []
    section_stack: list[tuple[int, str]] = []
    current_section: Section | None = None
    pending_table: list[str] = []

    def flush_table() -> None:
        nonlocal pending_table
        if not pending_table or current_section is None:
            pending_table = []
            return
        table = parse_markdown_table(
            table_id=f"{raw.document_id}-table-{len(tables) + 1:03d}",
            section_path=current_section.path,
            lines=pending_table,
        )
        if table:
            tables.append(table)
        pending_table = []

    def add_clause(text: str) -> None:
        if current_section is None:
            return
        cleaned = " ".join(text.split())
        if not cleaned:
            return
        clause = Clause(
            id=f"{raw.document_id}-clause-{len(clauses) + 1:03d}",
            section_id=current_section.id,
            section_path=current_section.path,
            text=cleaned,
            actor=extract_actor(cleaned),
        )
        clauses.append(clause)
        current_section.text = f"{current_section.text} {cleaned}".strip()
        obligation = extract_obligation(clause)
        if obligation:
            obligations.append(obligation)

    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_table()
            continue

        heading = HEADING_PATTERN.match(stripped)
        if heading:
            flush_table()
            level = len(heading.group(1))
            heading_title = heading.group(2).strip()
            while section_stack and section_stack[-1][0] >= level:
                section_stack.pop()
            section_stack.append((level, heading_title))
            path = " > ".join(title for _, title in section_stack)
            current_section = Section(
                id=f"{raw.document_id}-section-{len(sections) + 1:03d}",
                level=level,
                title=heading_title,
                path=path,
            )
            sections.append(current_section)
            continue

        if stripped.startswith("|"):
            pending_table.append(stripped)
            continue

        flush_table()
        add_clause(stripped)

    flush_table()
    return ParsedDocument(
        document_id=raw.document_id,
        title=title,
        metadata=metadata,
        sections=sections,
        clauses=clauses,
        tables=tables,
        obligations=obligations,
    )


def parse_markdown_table(table_id: str, section_path: str, lines: list[str]) -> Table | None:
    if len(lines) < 3:
        return None
    headers = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return Table(id=table_id, section_path=section_path, headers=headers, rows=rows)


def extract_actor(text: str) -> str:
    match = OBLIGATION_PATTERN.search(text)
    return match.group(1).title() if match else ""


def extract_obligation(clause: Clause) -> Obligation | None:
    match = OBLIGATION_PATTERN.search(clause.text)
    if not match:
        return None
    return Obligation(
        id=f"{clause.id}-obligation",
        actor=match.group(1).title(),
        action=match.group(2).strip(),
        source_clause_id=clause.id,
        section_path=clause.section_path,
    )
