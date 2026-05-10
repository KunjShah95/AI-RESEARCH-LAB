"""FAISS vector store for semantic search - MOCK MODE"""

import numpy as np


class VectorStore:
    """FAISS-based vector store for paper embeddings - MOCK"""

    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.embeddings = {}
        self.next_id = 0

    def add_paper(self, paper_id: str, text: str) -> int:
        """Add paper text to vector store"""
        embedding = np.random.randn(self.dimension).astype(np.float32)
        embedding = embedding / np.linalg.norm(embedding)

        paper_idx = self.next_id
        self.embeddings[paper_id] = embedding
        self.next_id += 1

        return paper_idx

    def search(self, query_text: str, top_k: int = 5) -> list[tuple[str, float]]:
        """Search for similar papers"""
        if not self.embeddings:
            return []

        query_embedding = np.random.randn(self.dimension).astype(np.float32)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)

        results = []
        for paper_id, embedding in self.embeddings.items():
            score = float(np.dot(query_embedding, embedding))
            results.append((paper_id, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def clear(self):
        """Clear all embeddings"""
        self.embeddings = {}
        self.next_id = 0
