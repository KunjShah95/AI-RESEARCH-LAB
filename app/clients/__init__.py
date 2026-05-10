"""Paper source clients"""

from app.clients.base import PaperSourceClient
from app.clients.arxiv import ArxivClient
from app.clients.semantic_scholar import SemanticScholarClient
from app.clients.pubmed import PubMedClient
from app.clients.crossref import CrossRefClient

__all__ = [
    "PaperSourceClient",
    "ArxivClient",
    "SemanticScholarClient",
    "PubMedClient",
    "CrossRefClient",
    "get_clients",
]


def get_clients() -> list[PaperSourceClient]:
    """Get all available paper source clients"""
    return [
        ArxivClient(),
        SemanticScholarClient(),
        PubMedClient(),
        CrossRefClient(),
    ]
