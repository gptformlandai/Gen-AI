from __future__ import annotations

from rag_debug_case_study.retrievers import BaselineRetriever, ImprovedRetriever
from rag_debug_case_study.schemas import AssistantAnswer, KnowledgeDocument, RetrieverMode
from rag_debug_case_study.text import tokenize


class RagDebugAssistant:
    """RAG assistant that keeps synthesis constant while retrievers vary."""

    def __init__(self, documents: list[KnowledgeDocument], mode: RetrieverMode) -> None:
        self.documents = {document.doc_id: document for document in documents}
        self.mode = mode
        self.retriever = BaselineRetriever(documents) if mode == "baseline" else ImprovedRetriever(documents)

    def answer(self, question: str, k: int = 3) -> AssistantAnswer:
        hits = self.retriever.search(question, k=k)
        if not hits:
            return AssistantAnswer(
                mode=self.mode,
                question=question,
                answer="I do not have enough retrieved evidence to answer.",
                confidence="low",
                citations=[],
            )

        primary = self.documents[hits[0].doc_id]
        answer = synthesize_from_document(question, primary)
        confidence = "high" if hits[0].score >= 5 else "medium"
        return AssistantAnswer(
            mode=self.mode,
            question=question,
            answer=answer,
            confidence=confidence,
            citations=hits,
        )


def synthesize_from_document(question: str, document: KnowledgeDocument) -> str:
    """Extractive synthesis: unchanged across baseline and improved runs."""
    sentences = split_sentences(document.body)
    if len(sentences) <= 3:
        return " ".join(sentences)
    query_tokens = set(tokenize(question, normalize=True))
    ranked = sorted(
        sentences,
        key=lambda sentence: len(query_tokens & set(tokenize(sentence, normalize=True))),
        reverse=True,
    )
    selected = [sentence for sentence in ranked[:2] if sentence]
    if not selected:
        selected = [document.body]
    return " ".join(selected)


def split_sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in text.replace("\n", " ").split(".") if sentence.strip()]
