from kg_enterprise_lab.evaluation.evaluation_runner import run_all_evaluations


def test_evaluation_runner_passes_golden_cases():
    reports = run_all_evaluations()
    assert {report.suite for report in reports} == {"entity_extraction", "relationship_extraction", "query", "graphrag", "graph_quality"}
    assert all(report.pass_rate == 1.0 for report in reports)
