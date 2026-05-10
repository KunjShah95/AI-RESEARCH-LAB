"""Synthesis API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.engines import SynthesisEngine
from app.models.paper import Paper

router = APIRouter()
synthesis_engine = SynthesisEngine()


class SynthesisRequest(BaseModel):
    query: str
    papers: list[dict]


class SynthesisResponse(BaseModel):
    summary: str
    insights: list[dict]
    gaps: list[dict]
    recommendations: list[str]


@router.post("")
async def synthesize_papers(request: SynthesisRequest) -> SynthesisResponse:
    """Synthesize insights from papers"""
    if not request.papers:
        raise HTTPException(status_code=400, detail="No papers provided")

    papers = [Paper(**p) for p in request.papers]

    insights = synthesis_engine.synthesize_insights(papers, request.query)
    gaps = synthesis_engine.identify_research_gaps(papers, request.query)
    recommendations = synthesis_engine.generate_recommendations(insights, gaps)
    summary = synthesis_engine.generate_summary(papers, request.query)

    return SynthesisResponse(
        summary=summary,
        insights=[i.model_dump() for i in insights],
        gaps=[g.model_dump() for g in gaps],
        recommendations=recommendations,
    )
