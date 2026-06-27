#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=src uvicorn kg_enterprise_lab.api.app:app --reload --host 127.0.0.1 --port 8000
