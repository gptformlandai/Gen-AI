from __future__ import annotations

import json

from enterprise_ops_lab.tools.rag_tools import search_runbooks


if __name__ == "__main__":
    print(json.dumps(search_runbooks("payments-api high latency after deployment", service="payments-api"), indent=2))

