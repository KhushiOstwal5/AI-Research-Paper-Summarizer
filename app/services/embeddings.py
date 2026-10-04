from __future__ import annotations

from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentIndexer:
    def __init__(self, max_features: int = 2000):
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=max_features,
        )
        self.chunks: List[str] = []
        self.matrix = None

    def fit(self, chunks: List[str]) -> None:
        self.chunks = chunks
        if not chunks:
            self.matrix = np.empty((0, 0))
            return
        self.matrix = self.vectorizer.fit_transform(chunks)

    def search(self, query: str, top_k: int = 3):
        if not self.chunks or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.matrix).flatten()
        ranked_indices = similarities.argsort()[::-1][:top_k]

        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            if score <= 0:
                continue
            results.append({"index": int(idx), "score": score, "text": self.chunks[int(idx)]})
        return results
