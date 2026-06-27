#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src python -m convo_graph_lab.cli.commands "$@"
