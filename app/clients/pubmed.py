"""PubMed client - mock implementation"""

from typing import Optional
from app.clients.base import PaperSourceClient
from app.models.paper import PaperSearchResult, Paper, Author


class PubMedClient(PaperSourceClient):
    """PubMed API client - MOCK MODE"""

    def get_source_name(self) -> str:
        return "pubmed"

    def search(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> PaperSearchResult:
        """Mock search returning sample data"""
        query_title = query.title() if query else "Medical"
        mock_papers = [
            Paper(
                source="pubmed",
                external_id=f"PMID-{40000000 + i}",
                title=f"Medical Research Paper {i}: {query_title} in Healthcare",
                authors=[
                    Author(name="Dr. Carol White", affiliation="General Hospital"),
                    Author(name="Dr. David Brown", affiliation="Medical University"),
                ],
                abstract=f"Abstract: This study examines {query} in medical contexts. "
                f"Results indicate significant improvements in patient outcomes.",
                year=2023 - i,
                doi=f"10.1000/medicine.{i}",
                open_access=False,
                categories=["Medicine", "Healthcare"],
            )
            for i in range(min(max_results, 5))
        ]

        return PaperSearchResult(
            papers=mock_papers, total=len(mock_papers), query=query, source="pubmed"
        )

    def get_paper(self, paper_id: str) -> dict:
        """Mock get paper by PMID"""
        return Paper(
            source="pubmed",
            external_id=paper_id,
            title=f"Mock Medical Paper: {paper_id}",
            authors=[Author(name="Dr. Mock", affiliation="Mock Hospital")],
            abstract="This is a mock medical paper for testing.",
            year=2023,
            open_access=False,
        ).model_dump()
