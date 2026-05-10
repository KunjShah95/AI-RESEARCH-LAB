"""CrossRef client for metadata enrichment"""

from typing import Optional
from app.clients.base import PaperSourceClient
from app.models.paper import PaperSearchResult, Paper, Author


class CrossRefClient(PaperSourceClient):
    """CrossRef API client - MOCK MODE"""

    def get_source_name(self) -> str:
        return "crossref"

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
                source="crossref",
                external_id=f"10.1145/{3800000 + i}",
                title=f"CrossRef Paper {i}: {query_title} in Computing",
                authors=[
                    Author(name="Dr. Academic Researcher"),
                    Author(name="Prof. University Scientist"),
                    Author(name="Dr. Industry Expert"),
                ],
                abstract=f"This is a CrossRef indexed research paper about {query}. "
                f"It presents novel methodologies and empirical findings in the field.",
                year=2024 - i,
                doi=f"10.1145/{3800000 + i}",
                open_access=True,
                venue="ICSE 2024",
                citations_count=50 - i * 5,
            )
            for i in range(min(max_results, 4))
        ]

        return PaperSearchResult(
            papers=mock_papers, total=len(mock_papers), query=query, source="crossref"
        )

    def get_paper(self, paper_id: str) -> dict:
        """Get paper by DOI"""
        return Paper(
            source="crossref",
            external_id=paper_id,
            title=f"CrossRef Paper: {paper_id}",
            authors=[Author(name="Author Name")],
            abstract="CrossRef indexed research paper with DOI metadata.",
            year=2024,
            doi=paper_id,
            open_access=True,
            venue="Conference",
            citations_count=10,
        ).model_dump()
