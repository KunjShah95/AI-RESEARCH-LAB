"""Researcher agent for CrewAI"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import settings


def create_researcher_agent() -> Agent:
    """Create the researcher agent"""
    llm = None
    if settings.openai_api_key:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            api_key=settings.openai_api_key,
        )

    return Agent(
        role="Senior Research Analyst",
        goal="Find accurate, up-to-date information with citations. "
        "Every claim must be source-grounded with [Source: Title] citations.",
        backstory="""
        You are a senior research analyst with expertise in finding and synthesizing 
        academic literature. You MUST cite sources as [Source: Title] for every claim.
        If you're uncertain about something, explicitly state the uncertainty.
        """,
        llm=llm,
        verbose=True,
        max_iter=10,
    )
