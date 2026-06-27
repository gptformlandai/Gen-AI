"""Database and event schema loader helpers."""

from __future__ import annotations


def normalize_table_name(table_id: str) -> str:
    return table_id.removeprefix("table-").replace("-", "_")


def normalize_schema_name(schema_id: str) -> str:
    return schema_id.removeprefix("schema-").replace("-", "_")
