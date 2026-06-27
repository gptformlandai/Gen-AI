from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.visualization.visualization_service import VisualizationService


def test_visualization_exports_mermaid_and_json():
    graph = build_sample_graph()
    service = VisualizationService(graph)
    mermaid = service.export(fmt="mermaid", view="blast-radius", anchor_name="payments-api")
    assert "flowchart" in mermaid
    assert "payments-api" in mermaid
    data = service.export(fmt="json", view="lineage", anchor_name="mobile-app")
    assert data["nodes"]
    assert data["edges"]
