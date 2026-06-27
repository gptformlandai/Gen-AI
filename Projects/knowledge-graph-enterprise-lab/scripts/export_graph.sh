#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src python -m kg_enterprise_lab.cli.commands export-graph --format "${1:-json}" --view "${2:-full}"
