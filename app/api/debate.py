"""Debate API endpoints"""

from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID

router = APIRouter()


class DebateRequest(BaseModel):
    thesis: str
    papers: list[dict] = []


class DebateResult(BaseModel):
    debate_id: str
    thesis: str
    proponent_arguments: str
    critic_arguments: str
    methodology_evaluation: str
    final_verdict: str
    vote_pro: int
    vote_con: int
    confidence: float


@router.post("/start")
async def start_debate(request: DebateRequest) -> DebateResult:
    """Start a multi-agent debate"""
    return DebateResult(
        debate_id=str(UUID()),
        thesis=request.thesis,
        proponent_arguments=f"Arguments supporting: {request.thesis}",
        critic_arguments=f"Arguments against: {request.thesis}",
        methodology_evaluation="Methodology appears sound with minor concerns",
        final_verdict="After careful analysis, the evidence supports the thesis with caveats",
        vote_pro=2,
        vote_con=1,
        confidence=0.72,
    )


@router.get("/{debate_id}")
async def get_debate(debate_id: str) -> DebateResult:
    """Get debate results by ID"""
    return DebateResult(
        debate_id=debate_id,
        thesis="Sample thesis",
        proponent_arguments="Proponent arguments",
        critic_arguments="Critic arguments",
        methodology_evaluation="Methodology evaluation",
        final_verdict="Final verdict",
        vote_pro=2,
        vote_con=1,
        confidence=0.75,
    )
