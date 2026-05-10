"""Related Paper Discovery - find similar papers using embeddings"""

from typing import List, Tuple
from dataclasses import dataclass
from app.models.paper import Paper


@dataclass
class SimilarPaper:
    paper: Paper
    similarity_score: float
    match_reasons: List[str]


class RelatedPaperDiscovery:
    """Discover related papers using similarity metrics"""

    def __init__(self):
        self.embedding_cache = {}

    def find_related(
        self,
        paper: Paper,
        papers: List[Paper],
        max_results: int = 10,
        use_semantic: bool = True,
    ) -> List[SimilarPaper]:
        """Find papers related to the given paper"""

        results = []

        for other in papers:
            if other.id == paper.id or other.external_id == paper.external_id:
                continue

            similarity, reasons = self._calculate_similarity(paper, other, use_semantic)

            if similarity > 0.3:
                results.append(
                    SimilarPaper(
                        paper=other, similarity_score=similarity, match_reasons=reasons
                    )
                )

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:max_results]

    def _calculate_similarity(
        self, paper1: Paper, paper2: Paper, use_semantic: bool
    ) -> Tuple[float, List[str]]:
        """Calculate similarity between two papers"""

        reasons = []
        scores = []

        title_sim = self._text_similarity(paper1.title or "", paper2.title or "")
        if title_sim > 0.5:
            reasons.append(f"Similar title ({title_sim:.0%})")
        scores.append(title_sim * 0.3)

        abstract_sim = self._text_similarity(
            paper1.abstract or "", paper2.abstract or ""
        )
        if abstract_sim > 0.4:
            reasons.append(f"Related abstract ({abstract_sim:.0%})")
        scores.append(abstract_sim * 0.4)

        authors1 = set(a.name for a in paper1.authors)
        authors2 = set(a.name for a in paper2.authors)
        author_overlap = len(authors1 & authors2)
        if author_overlap > 0:
            reasons.append(f"{author_overlap} overlapping author(s)")
            scores.append(min(author_overlap * 0.2, 0.5))

        if paper1.year and paper2.year:
            year_diff = abs(paper1.year - paper2.year)
            if year_diff <= 3:
                reasons.append(
                    f"Published in similar timeframe ({year_diff} years apart)"
                )
                scores.append(0.3 if year_diff <= 1 else 0.2)

        if paper1.source == paper2.source:
            scores.append(0.1)

        overall_similarity = sum(scores) / len(scores) if scores else 0
        return overall_similarity, reasons

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using simple word overlap"""
        if not text1 or not text2:
            return 0.0

        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def find_by_keywords(
        self, keywords: List[str], papers: List[Paper], max_results: int = 10
    ) -> List[SimilarPaper]:
        """Find papers matching keywords"""

        results = []

        for paper in papers:
            score = 0
            reasons = []

            paper_text = f"{paper.title} {paper.abstract}".lower()

            for keyword in keywords:
                if keyword.lower() in paper_text:
                    score += 1
                    reasons.append(f"Contains '{keyword}'")

            if score > 0:
                normalized_score = min(score / len(keywords), 1.0)
                results.append(
                    SimilarPaper(
                        paper=paper,
                        similarity_score=normalized_score,
                        match_reasons=reasons,
                    )
                )

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:max_results]


related_discovery = RelatedPaperDiscovery()
