"""Advanced Search API"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.engines.advanced_search import (
    AdvancedSearchEngine,
    SearchType,
)


router = APIRouter()
search_engine = AdvancedSearchEngine()


class SearchRequest(BaseModel):
    query: str
    search_type: str = "hybrid"
    max_results: int = 20


@router.post("/")
async def advanced_search(request: SearchRequest):
    """Perform advanced search"""
    try:
        search_type = SearchType(request.search_type)
    except ValueError:
        search_type = SearchType.HYBRID

    from app.clients import get_clients

    clients = get_clients()

    all_papers = []
    for client in clients:
        try:
            result = client.search(query=request.query, max_results=50)
            all_papers.extend(result.papers)
        except Exception:
            pass

    results = search_engine.search(
        query=request.query,
        papers=all_papers,
        search_type=search_type,
        max_results=request.max_results,
    )

    return {
        "query": request.query,
        "search_type": request.search_type,
        "results": [
            {
                "paper": r.paper,
                "score": r.score,
                "match_type": r.match_type,
                "highlights": r.highlights,
            }
            for r in results
        ],
        "total": len(results),
    }


@router.get("/autocomplete")
async def autocomplete(q: str = Query(..., min_length=1)):
    """Get autocomplete suggestions"""
    from app.clients import get_clients

    clients = get_clients()

    all_papers = []
    for client in clients:
        try:
            result = client.search(query=q, max_results=30)
            all_papers.extend(result.papers)
        except Exception:
            pass

    suggestions = search_engine.autocomplete(q, all_papers)

    return {"query": q, "suggestions": suggestions}


@router.get("/types")
async def get_search_types():
    """Get available search types"""
    return {
        "types": [
            {
                "id": "semantic",
                "name": "Semantic Search",
                "description": "AI-powered meaning-based search",
            },
            {
                "id": "keyword",
                "name": "Keyword Search",
                "description": "Traditional keyword matching",
            },
            {
                "id": "boolean",
                "name": "Boolean Search",
                "description": "AND, OR, NOT operators",
            },
            {
                "id": "hybrid",
                "name": "Hybrid Search",
                "description": "Combined semantic + keyword (recommended)",
            },
            {
                "id": "vector",
                "name": "Vector Search",
                "description": "Embedding-based similarity",
            },
        ]
    }
