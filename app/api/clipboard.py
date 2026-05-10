"""Citation Clipboard API - quick citation copying"""

from typing import List
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.engines.citation_formatter import CitationFormatter, CitationStyle
from app.clients import get_clients


router = APIRouter()
citation_formatter = CitationFormatter()


class CitationCopyRequest(BaseModel):
    paper_ids: List[str]
    source: str
    style: str = "apa"


@router.get("/copy")
async def copy_citation(
    paper_id: str = Query(...), source: str = Query(...), style: str = Query("apa")
):
    """Get formatted citation for a paper"""

    try:
        citation_style = CitationStyle(style)
    except ValueError:
        citation_style = CitationStyle.APA

    clients = get_clients()
    client = next((c for c in clients if c.get_source_name() == source), None)

    if not client:
        return {"error": "Source not found"}

    paper = client.get_paper(paper_id)
    if not paper:
        return {"error": "Paper not found"}

    citation = citation_formatter.format_single(paper, citation_style)

    return {"citation": citation, "style": style, "paper_id": paper_id}


@router.post("/copy/batch")
async def copy_multiple_citations(request: CitationCopyRequest):
    """Get formatted citations for multiple papers"""

    try:
        citation_style = CitationStyle(request.style)
    except ValueError:
        citation_style = CitationStyle.APA

    clients = get_clients()
    client = next((c for c in clients if c.get_source_name() == request.source), None)

    if not client:
        return {"error": "Source not found"}

    citations = []
    for paper_id in request.paper_ids:
        paper = client.get_paper(paper_id)
        if paper:
            citation = citation_formatter.format_single(paper, citation_style)
            citations.append({"paper_id": paper_id, "citation": citation})

    return {"citations": citations, "style": request.style, "count": len(citations)}


@router.get("/styles")
async def get_citation_styles():
    """Get available citation styles"""
    return {
        "styles": [
            {"id": "apa", "name": "APA (7th Edition)"},
            {"id": "mla", "name": "MLA (9th Edition)"},
            {"id": "chicago", "name": "Chicago/Turabian"},
            {"id": "harvard", "name": "Harvard"},
            {"id": "ieee", "name": "IEEE"},
            {"id": "vancouver", "name": "Vancouver"},
            {"id": "turabian", "name": "Turabian"},
        ]
    }
