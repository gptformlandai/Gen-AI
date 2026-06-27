FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data

RUN python -m pip install --no-cache-dir -e ".[api]"

EXPOSE 8010
CMD ["uvicorn", "convo_graph_lab.api.app:app", "--host", "0.0.0.0", "--port", "8010"]
