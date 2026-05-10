"""Duplicate detection for papers"""

from typing import Optional
from app.models.paper import Paper


class DuplicateDetector:
    """Detect duplicate and related papers"""

    def find_duplicates(self, paper: Paper, existing_papers: list[Paper]) -> list[dict]:
        """Find potential duplicates"""
        duplicates = []

        for existing in existing_papers:
            score = self._calculate_similarity(paper, existing)
            if score > 0.7:
                duplicates.append(
                    {
                        "paper_id": str(existing.id),
                        "title": existing.title,
                        "similarity": round(score, 2),
                        "reason": self._get_similarity_reason(paper, existing),
                    }
                )

        return sorted(duplicates, key=lambda x: x["similarity"], reverse=True)

    def _calculate_similarity(self, paper1: Paper, paper2: Paper) -> float:
        """Calculate title similarity score"""
        title1 = (paper1.title or "").lower()
        title2 = (paper2.title or "").lower()

        words1 = set(title1.split())
        words2 = set(title2.split())

        if not words1 or not words2:
            return 0.0

        common_words = words1 & words2
        total_words = words1 | words2

        base_score = len(common_words) / len(total_words) if total_words else 0.0

        if paper1.doi and paper2.doi and paper1.doi == paper2.doi:
            return 1.0

        return base_score

    def _get_similarity_reason(self, paper1: Paper, paper2: Paper) -> str:
        """Explain why papers are similar"""
        if paper1.doi and paper2.doi and paper1.doi == paper2.doi:
            return "Same DOI"

        year1 = paper1.year or 0
        year2 = paper2.year or 0

        if year1 and year2 and abs(year1 - year2) <= 1:
            author_names1 = {a.name for a in paper1.authors}
            author_names2 = {a.name for a in paper2.authors}
            if author_names1 & author_names2:
                return "Same authors, similar publication year"

        return "Similar title"

    def check_preprint_published(self, paper: Paper) -> Optional[dict]:
        """Check if preprint has published version"""
        source_lower = (paper.source or "").lower()

        if "arxiv" in source_lower:
            return {
                "has_published": False,
                "suggestion": "Check CrossRef for published version",
                "arxiv_id": paper.external_id,
            }

        if "semantic_scholar" in source_lower:
            if paper.doi:
                return {
                    "has_published": True,
                    "doi": paper.doi,
                    "suggestion": "Preprint has DOI",
                }

        return None
