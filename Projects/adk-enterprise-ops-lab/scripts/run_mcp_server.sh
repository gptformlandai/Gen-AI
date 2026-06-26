#!/usr/bin/env bash
set -euo pipefail
python -m enterprise_ops_lab.mcp.mock_mcp_server get_service_health --service payments-api

