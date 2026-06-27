#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src python -m kg_enterprise_lab.cli.commands run-evals
