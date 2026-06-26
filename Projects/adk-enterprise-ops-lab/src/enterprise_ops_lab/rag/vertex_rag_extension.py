from __future__ import annotations


class VertexRagExtensionPlaceholder:
    """Documents where Vertex AI RAG Engine or Vertex AI Search would plug in."""

    def search(self, query: str) -> list[dict[str, str]]:
        raise NotImplementedError(
            "Configure VERTEX_RAG_CORPUS or VERTEX_SEARCH_DATASTORE and replace LocalVectorStore with Vertex retrieval."
        )

