"""Compare API - paper diff view"""

from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.engines.diff import PaperDiffEngine, PaperDiff
from app.clients import get_clients


router = APIRouter()
diff_engine = PaperDiffEngine()


class CompareRequest(BaseModel):
    paper1_id: str
    paper1_source: str
    paper2_id: str
    paper2_source: str


@router.post("/", response_model=PaperDiff)
async def compare_papers(request: CompareRequest):
    """Compare two papers with detailed diff"""
    clients = get_clients()

    client1 = next(
        (c for c in clients if c.get_source_name() == request.paper1_source), None
    )
    client2 = next(
        (c for c in clients if c.get_source_name() == request.paper2_source), None
    )

    if not client1 or not client2:
        raise HTTPException(status_code=404, detail="Source not found")

    paper1 = client1.get_paper(request.paper1_id)
    paper2 = client2.get_paper(request.paper2_id)

    if not paper1 or not paper2:
        raise HTTPException(status_code=404, detail="Paper not found")

    from app.models.paper import Paper
    from datetime import datetime

    p1 = Paper(**{**paper1, "created_at": datetime.now()})
    p2 = Paper(**{**paper2, "created_at": datetime.now()})

    return diff_engine.compare_papers(p1, p2)


@router.get("/unified")
async def get_unified_diff(
    paper1_id: str = Query(...),
    paper1_source: str = Query(...),
    paper2_id: str = Query(...),
    paper2_source: str = Query(...),
):
    """Get unified diff format"""
    clients = get_clients()

    client1 = next((c for c in clients if c.get_source_name() == paper1_source), None)
    client2 = next((c for c in clients if c.get_source_name() == paper2_source), None)

    if not client1 or not client2:
        raise HTTPException(status_code=404, detail="Source not found")

    paper1 = client1.get_paper(paper1_id)
    paper2 = client2.get_paper(paper2_id)

    if not paper1 or not paper2:
        raise HTTPException(status_code=404, detail="Paper not found")

    diff = diff_engine.generate_unified_diff(
        paper1.get("abstract", ""),
        paper1.get("title", ""),
        paper2.get("abstract", ""),
        paper2.get("title", ""),
    )

    return {"diff": diff}


@router.post("/multiple")
async def compare_multiple_papers(paper_ids: List[str], source: str = "arxiv"):
    """Compare multiple papers"""
    clients = get_clients()
    client = next((c for c in clients if c.get_source_name() == source), None)

    if not client:
        raise HTTPException(status_code=404, detail="Source not found")

    papers = []
    for pid in paper_ids:
        paper = client.get_paper(pid)
        if paper:
            papers.append(paper)

    if len(papers) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 papers")

    from app.models.paper import Paper
    from datetime import datetime

    paper_models = [Paper(**{**p, "created_at": datetime.now()}) for p in papers]

    diffs = diff_engine.compare_multiple(paper_models)
    return {"comparisons": diffs}
