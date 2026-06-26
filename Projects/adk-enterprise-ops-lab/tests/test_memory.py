from enterprise_ops_lab.memory.memory_service import InMemoryMemoryService


def test_memory_add_and_search(tmp_path) -> None:
    memory = InMemoryMemoryService(tmp_path)
    memory.add("Increasing consumer partitions fixed kafka lag.", service="kafka-consumers", tags=["kafka"])

    hits = memory.search("consumer partitions lag", service="kafka-consumers")

    assert hits
    assert hits[0].service == "kafka-consumers"

