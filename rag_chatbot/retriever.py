"""Retrieval berbasis TF-IDF + cosine similarity (tanpa API tambahan)."""

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .loader import Chunk


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


class TfidfRetriever:
    def __init__(self, chunks: list[Chunk]):
        if not chunks:
            raise ValueError("chunks tidak boleh kosong")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks])

    def search(self, query: str, k: int = 3, min_score: float = 0.05) -> list[Hit]:
        """Kembalikan maksimal `k` chunk paling relevan dengan skor >= `min_score`."""
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).ravel()
        order = scores.argsort()[::-1][:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in order if scores[i] >= min_score]
