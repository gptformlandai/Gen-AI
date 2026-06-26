from enterprise_ops_lab.artifacts.artifact_service import LocalArtifactService


def test_artifact_versioning(tmp_path) -> None:
    service = LocalArtifactService(tmp_path)
    one = service.save_markdown("incident_demo", "# One", {"service": "payments-api"})
    two = service.save_markdown("incident_demo", "# Two", {"service": "payments-api"})

    assert one.version == 1
    assert two.version == 2
    loaded, content = service.load("incident_demo")
    assert loaded.version == 2
    assert "# Two" in content

