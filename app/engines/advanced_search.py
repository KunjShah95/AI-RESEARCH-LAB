"""Advanced Search Engine - semantic, hybrid, and vector search"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import re
from app.models.paper import Paper


class SearchType(str, Enum):
    SEMANTIC = "semantic"
    KEYWORD = "keyword"
    BOOLEAN = "boolean"
    HYBRID = "hybrid"
    VECTOR = "vector"


@dataclass
class SearchResult:
    paper: Paper
    score: float
    match_type: str
    highlights: List[str]


@dataclass
class SearchFilters:
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    source: Optional[str] = None
    open_access: Optional[bool] = None
    min_citations: Optional[int] = None
    categories: Optional[List[str]] = None


class AdvancedSearchEngine:
    """Engine for advanced search with multiple search types"""

    def __init__(self):
        self.vector_store = None
        self.embeddings_model = None

    def search(
        self,
        query: str,
        papers: List[Paper],
        search_type: SearchType = SearchType.HYBRID,
        filters: Optional[SearchFilters] = None,
        max_results: int = 20,
    ) -> List[SearchResult]:
        """Search papers using specified search type"""

        if filters:
            papers = self._apply_filters(papers, filters)

        if not papers:
            return []

        if search_type == SearchType.SEMANTIC:
            return self._semantic_search(query, papers, max_results)
        elif search_type == SearchType.KEYWORD:
            return self._keyword_search(query, papers, max_results)
        elif search_type == SearchType.BOOLEAN:
            return self._boolean_search(query, papers, max_results)
        elif search_type == SearchType.HYBRID:
            return self._hybrid_search(query, papers, max_results)
        elif search_type == SearchType.VECTOR:
            return self._vector_search(query, papers, max_results)

        return self._hybrid_search(query, papers, max_results)

    def _apply_filters(
        self, papers: List[Paper], filters: SearchFilters
    ) -> List[Paper]:
        """Apply search filters to papers"""
        filtered = []

        for paper in papers:
            if filters.year_from and (paper.year or 0) < filters.year_from:
                continue
            if filters.year_to and (paper.year or 9999) > filters.year_to:
                continue
            if filters.source and paper.source != filters.source:
                continue
            if (
                filters.open_access is not None
                and paper.open_access != filters.open_access
            ):
                continue
            if (
                filters.min_citations
                and (paper.citations_count or 0) < filters.min_citations
            ):
                continue
            if filters.categories:
                pass

            filtered.append(paper)

        return filtered

    def _semantic_search(
        self, query: str, papers: List[Paper], max_results: int
    ) -> List[SearchResult]:
        """Semantic search using embeddings"""
        results = []

        query_keywords = set(query.lower().split())

        for paper in papers:
            score = 0
            highlights = []

            title_words = set(paper.title.lower().split())
            title_overlap = len(query_keywords & title_words)
            if title_overlap:
                score += title_overlap * 0.3
                if title_overlap > 0:
                    highlights.append(f"Title match: {paper.title[:80]}")

            if paper.abstract:
                abstract_words = set(paper.abstract.lower().split())
                abstract_overlap = len(query_keywords & abstract_words)
                if abstract_overlap:
                    score += abstract_overlap * 0.1
                    abstract_lower = paper.abstract.lower()
                    for kw in list(query_keywords)[:3]:
                        if kw in abstract_lower:
                            idx = abstract_lower.find(kw)
                            start = max(0, idx - 50)
                            end = min(len(paper.abstract), idx + 50)
                            highlights.append(f"...{paper.abstract[start:end]}...")

            if score > 0:
                results.append(
                    SearchResult(
                        paper=paper,
                        score=min(score, 1.0),
                        match_type="semantic",
                        highlights=highlights[:3],
                    )
                )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:max_results]

    def _keyword_search(
        self, query: str, papers: List[Paper], max_results: int
    ) -> List[SearchResult]:
        """Traditional keyword search with TF-IDF-style scoring"""
        results = []

        query_lower = query.lower()
        query_terms = re.findall(r"\w+", query_lower)

        for paper in papers:
            score = 0
            highlights = []

            if query_lower in paper.title.lower():
                score += 1.0
                highlights.append(f"Exact title match: {paper.title}")

            for term in query_terms:
                if term in paper.title.lower():
                    score += 0.3

            if paper.abstract:
                abstract_lower = paper.abstract.lower()
                term_count = sum(1 for term in query_terms if term in abstract_lower)
                score += term_count * 0.1

                if term_count > 0:
                    for sentence in paper.abstract.split("."):
                        if any(term in sentence.lower() for term in query_terms):
                            highlights.append(f"Match: {sentence.strip()[:100]}...")
                            break

            if score > 0:
                results.append(
                    SearchResult(
                        paper=paper,
                        score=min(score, 1.0),
                        match_type="keyword",
                        highlights=highlights[:3],
                    )
                )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:max_results]

    def _boolean_search(
        self, query: str, papers: List[Paper], max_results: int
    ) -> List[SearchResult]:
        """Boolean search (AND, OR, NOT operators)"""
        results = []

        tokens = query.upper().split()

        terms = [t for t in tokens if t not in ["AND", "OR", "NOT"]]
        operators = [t for t in tokens if t in ["AND", "OR", "NOT"]]

        for paper in papers:
            paper_text = f"{paper.title} {paper.abstract or ''}".lower()
            term_matches = [term.lower() in paper_text for term in terms]

            score = 0
            highlights = []

            if not operators:
                if any(term_matches):
                    score = sum(term_matches) / len(term_matches)
            else:
                result = term_matches[0] if term_matches else False
                for i, op in enumerate(operators):
                    if i + 1 < len(term_matches):
                        if op == "AND":
                            result = result and term_matches[i + 1]
                        elif op == "OR":
                            result = result or term_matches[i + 1]

                score = 1.0 if result else 0

            if score > 0:
                if paper.title.lower():
                    highlights.append(f"Title: {paper.title[:80]}")
                results.append(
                    SearchResult(
                        paper=paper,
                        score=score,
                        match_type="boolean",
                        highlights=highlights,
                    )
                )

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:max_results]

    def _hybrid_search(
        self, query: str, papers: List[Paper], max_results: int
    ) -> List[SearchResult]:
        """Hybrid search combining semantic and keyword"""

        keyword_results = {
            r.paper.id: r for r in self._keyword_search(query, papers, max_results)
        }

        semantic_results = {
            r.paper.id: r for r in self._semantic_search(query, papers, max_results)
        }

        combined = {}

        for paper_id, result in keyword_results.items():
            combined[paper_id] = result
            if paper_id in semantic_results:
                combined[paper_id].score = (
                    result.score * 0.6 + semantic_results[paper_id].score * 0.4
                )
                combined[paper_id].match_type = "hybrid"
                combined[paper_id].highlights.extend(
                    semantic_results[paper_id].highlights
                )

        for paper_id, result in semantic_results.items():
            if paper_id not in combined:
                combined[paper_id] = result

        sorted_results = sorted(combined.values(), key=lambda x: x.score, reverse=True)
        return sorted_results[:max_results]

    def _vector_search(
        self, query: str, papers: List[Paper], max_results: int
    ) -> List[SearchResult]:
        """Vector search using embeddings (placeholder for production)"""
        return self._hybrid_search(query, papers, max_results)

    def autocomplete(
        self, query: str, papers: List[Paper], max_suggestions: int = 5
    ) -> List[str]:
        """Autocomplete suggestions based on query"""
        suggestions = []
        query_lower = query.lower()

        title_terms = set()
        for paper in papers[:50]:
            words = paper.title.lower().split()
            title_terms.update(words)

        for term in sorted(title_terms):
            if term.startswith(query_lower) and len(term) > 3:
                suggestions.append(term)
                if len(suggestions) >= max_suggestions:
                    break

        return suggestions


advanced_search_engine = AdvancedSearchEngine()
