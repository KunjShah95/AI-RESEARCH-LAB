"""LangGraph state definitions"""

from typing import TypedDict, Optional


class ResearchState(TypedDict):
    """State for the research workflow"""

    query: str
    source: Optional[str]
    papers: list[dict]
    research_notes: str
    critique_notes: str
    final_report: str
    routing: str
    retries: int


class DebateState(TypedDict):
    """State for the debate workflow"""

    thesis: str
    proponent_arguments: str
    critic_arguments: str
    methodology_evaluation: str
    final_verdict: str
    vote_pro: int
    vote_con: int
    confidence: float


class SynthesisState(TypedDict):
    """State for the synthesis workflow"""

    papers: list[dict]
    insights: list[dict]
    gaps: list[dict]
    recommendations: list[str]
    summary: str
