# CI Evaluation Gate

Recommended CI flow:

```bash
python -m pip install -e ".[dev]"
pytest
python -m enterprise_ops_lab.evals.evaluation_runner
```

Deployment should fail if:

- unit tests fail;
- golden pass rate drops below threshold;
- trajectory tests fail;
- RAG grounding tests fail;
- unsafe tool approval tests fail.

