"""Base client interface for paper sources"""

from abc import ABC, abstractmethod
from typing import Optional
from app.models.paper import PaperSearchResult


class PaperSourceClient(ABC):
    """Abstract base class for paper source clients"""

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> PaperSearchResult:
        """Search for papers matching query"""
        pass

    @abstractmethod
    def get_paper(self, paper_id: str) -> dict:
        """Get paper details by ID"""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the source name"""
        pass
