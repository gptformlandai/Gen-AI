#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src python -m kg_enterprise_lab.cli.commands run-graphrag --question "${1:-Use GraphRAG to explain why provider-search-service may be slow.}"
