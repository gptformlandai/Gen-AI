from __future__ import annotations

import json

from enterprise_ops_lab.tools.artifact_tools import load_report_artifact, save_report_artifact


if __name__ == "__main__":
    saved = save_report_artifact("demo_report", "# Demo Report\n\nArtifact content.\n", metadata={"demo": "true"})
    loaded = load_report_artifact("demo_report")
    print(json.dumps({"saved": saved, "loaded": loaded}, indent=2))

