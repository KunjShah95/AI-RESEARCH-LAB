"""Paper Writing API endpoints"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engines.paper_writer import PaperWriterEngine, PaperType, GeneratedPaper
from app.clients import get_clients

router = APIRouter()


class GeneratePaperRequest(BaseModel):
    topic: str
    paper_type: str
    paper_ids: Optional[List[str]] = None
    use_external_search: bool = False


class PaperGenerationResponse(BaseModel):
    paper: GeneratedPaper
    markdown: str


@router.post("/generate", response_model=PaperGenerationResponse)
async def generate_paper(request: GeneratePaperRequest):
    """Generate a complete research paper"""

    try:
        paper_type = PaperType(request.paper_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid paper type")

    writer_engine = PaperWriterEngine()
    papers = []

    if request.paper_ids:
        clients = get_clients()
        for paper_id in request.paper_ids:
            for client in clients:
                paper = client.get_paper(paper_id)
                if paper:
                    papers.append(paper)
                    break

    paper = await writer_engine.generate_paper(
        topic=request.topic,
        paper_type=paper_type,
        papers=papers,
        use_external_search=request.use_external_search,
    )

    markdown = writer_engine.export_to_markdown(paper)

    return PaperGenerationResponse(paper=paper, markdown=markdown)


@router.get("/types")
async def get_paper_types():
    """Get available paper types"""
    return {
        "types": [
            {"id": "literature_review", "name": "Literature Review"},
            {"id": "original_research", "name": "Original Research"},
            {"id": "survey", "name": "Survey Paper"},
            {"id": "position_paper", "name": "Position Paper"},
            {"id": "grant_proposal", "name": "Grant Proposal"},
            {"id": "method_paper", "name": "Method Paper"},
        ]
    }
