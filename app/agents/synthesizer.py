"""Synthesizer agent for CrewAI"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import settings


def create_synthesizer_agent() -> Agent:
    """Create the synthesis agent"""
    llm = None
    if settings.openai_api_key:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            api_key=settings.openai_api_key,
        )

    return Agent(
        role="Research Synthesizer",
        goal="Create coherent reports with inline citations. "
        "Ensure all claims are source-grounded and the report is well-structured.",
        backstory="""
        You are a research synthesizer who creates clear, well-structured reports.
        Every claim must include [Source: Title] citations. Structure outputs with:
        - Summary
        - Key Findings
        - Methodology
        - Limitations
        - Citations
        """,
        llm=llm,
        verbose=True,
        max_iter=10,
    )
