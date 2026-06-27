from kg_enterprise_lab.extraction.rule_based_extractor import RuleBasedExtractor
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph, load_documents


def main() -> None:
    graph = build_sample_graph()
    batch = RuleBasedExtractor(graph).extract(load_documents()[0])
    print({"entities": len(batch.entities), "relationships": len(batch.relationships)})


if __name__ == "__main__":
    main()
