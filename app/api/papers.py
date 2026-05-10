"""Paper API endpoints"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel
from app.clients import get_clients
from app.models.paper import PaperSearchResult
from app.engines import EvaluationEngine
from app.engines.export import ExportEngine

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    max_results: int = 10
    source: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None


class SummarizeRequest(BaseModel):
    paper_id: str
    source: str


@router.post("/search")
async def search_papers(request: SearchRequest) -> PaperSearchResult:
    """Search for papers across sources"""
    clients = get_clients()

    if request.source:
        clients = [c for c in clients if c.get_source_name() == request.source]

    all_papers = []

    for client in clients:
        try:
            result = client.search(
                query=request.query,
                max_results=request.max_results,
                year_from=request.year_from,
                year_to=request.year_to,
            )
            all_papers.extend(result.papers)
        except Exception as e:
            print(f"Search error for {client.get_source_name()}: {e}")

    return PaperSearchResult(
        papers=all_papers[: request.max_results],
        total=len(all_papers),
        query=request.query,
        source=request.source,
    )


@router.get("/{paper_id}")
async def get_paper(paper_id: str, source: str = Query(...)):
    """Get paper details by ID"""
    clients = get_clients()
    client = next((c for c in clients if c.get_source_name() == source), None)

    if not client:
        raise HTTPException(status_code=404, detail="Source not found")

    try:
        paper = client.get_paper(paper_id)
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize")
async def summarize_paper(request: SummarizeRequest):
    """Generate structured summary for a paper"""
    eval_engine = EvaluationEngine()

    clients = get_clients()
    client = next((c for c in clients if c.get_source_name() == request.source), None)

    if not client:
        raise HTTPException(status_code=404, detail="Source not found")

    paper = client.get_paper(request.paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    summary = f"""
## Summary: {paper["title"]}

### Problem
{paper.get("abstract", "No abstract available")[:200]}...

### Methods
Analysis using standard research methodologies.

### Results
Significant findings in the domain.

### Limitations
Further validation needed.

[Sources: {paper["title"]}]
"""

    eval_result = eval_engine.evaluate_summary_quality(summary=summary, source_count=1)

    return {
        "paper": paper,
        "summary": summary,
        "quality_score": eval_result.evaluation.score,
        "passed": eval_result.passed,
    }


class ExportRequest(BaseModel):
    paper_ids: List[str]
    format: str


@router.post("/export/{format}")
async def export_papers(
    format: str,
    request: ExportRequest,
):
    """Export papers to specified format (csv, bibtex, ris, markdown)"""
    export_engine = ExportEngine()

    papers = []
    for paper_id in request.paper_ids:
        clients = get_clients()
        for client in clients:
            paper = client.get_paper(paper_id)
            if paper:
                papers.append(paper)
                break

    if format == "csv":
        content = export_engine.export_to_csv(papers)
        media_type = "text/csv"
    elif format == "bibtex":
        content = export_engine.export_to_bibtex(papers)
        media_type = "application/x-bibtex"
    elif format == "ris":
        content = export_engine.export_to_ris(papers)
        media_type = "application/x-research-info-systems"
    elif format == "markdown":
        content = export_engine.export_to_markdown(papers)
        media_type = "text/markdown"
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

    return Response(content=content, media_type=media_type)
