"""Semantic Scholar client - mock implementation"""

from typing import Optional
from app.clients.base import PaperSourceClient
from app.models.paper import PaperSearchResult, Paper, Author


class SemanticScholarClient(PaperSourceClient):
    """Semantic Scholar API client - MOCK MODE"""

    def get_source_name(self) -> str:
        return "semantic_scholar"

    def search(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> PaperSearchResult:
        """Mock search returning sample data"""
        query_title = query.title() if query else "Research"
        mock_papers = [
            Paper(
                source="semantic_scholar",
                external_id=f"mock-s2-{i}",
                title=f"Sample Paper {i}: {query_title} Research",
                authors=[
                    Author(name="Alice Smith"),
                    Author(name="Bob Johnson"),
                ],
                abstract=f"This is a mock abstract for a paper about {query}. "
                f"It demonstrates the structure of search results.",
                year=2024 - i,
                doi=f"10.1234/mock.{i}",
                open_access=True,
                citations_count=100 - i * 10,
                categories=["cs.AI", "cs.LG"],
            )
            for i in range(min(max_results, 5))
        ]

        return PaperSearchResult(
            papers=mock_papers,
            total=len(mock_papers),
            query=query,
            source="semantic_scholar",
        )

    def get_paper(self, paper_id: str) -> dict:
        """Mock get paper by ID"""
        return Paper(
            source="semantic_scholar",
            external_id=paper_id,
            title=f"Mock Paper: {paper_id}",
            authors=[Author(name="Mock Author")],
            abstract="This is a mock paper for testing.",
            year=2024,
            open_access=True,
        ).model_dump()
