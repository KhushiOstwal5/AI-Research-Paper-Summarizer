import re
from typing import List

from app.config import settings
from app.services.embeddings import DocumentIndexer


class RAGChatEngine:
    def __init__(self):
        self.indexer = DocumentIndexer()
        self.chunks: List[str] = []

    def _split_text(self, text: str) -> List[str]:
        cleaned = re.sub(r"\s+", " ", text).strip()
        if not cleaned:
            return []

        words = cleaned.split()
        chunk_size = settings.max_chunk_length
        chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def build_from_text(self, text: str) -> None:
        self.chunks = self._split_text(text)
        self.indexer.fit(self.chunks)

    def answer(self, question: str) -> str:
        if not self.chunks:
            return "Upload a PDF and process it before asking questions."

        matches = self.indexer.search(question, top_k=3)
        if not matches:
            return "I could not find a strong match for that question in the uploaded paper. Try rephrasing it."

        context_parts = [match["text"] for match in matches]
        context = "\n\n".join(context_parts)

        return (
            "Based on the uploaded paper, the most relevant section suggests: "
            f"{context[:800]}"
        )
