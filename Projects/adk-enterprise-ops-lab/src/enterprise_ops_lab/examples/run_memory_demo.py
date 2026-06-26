from __future__ import annotations

import json

from enterprise_ops_lab.agents.memory_learning_agent import recall, remember


if __name__ == "__main__":
    record = remember("Increasing consumer partitions fixed kafka lag.", service="kafka-consumers")
    hits = recall("consumer partitions lag", service="kafka-consumers")
    print(json.dumps({"stored": record, "hits": hits}, indent=2))

