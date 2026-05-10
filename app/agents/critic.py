"""Critic agent for CrewAI"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from app.config import settings


def create_critic_agent() -> Agent:
    """Create the critic/verifier agent"""
    llm = None
    if settings.openai_api_key:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
            api_key=settings.openai_api_key,
        )

    return Agent(
        role="Critical Reviewer",
        goal="Verify all claims, identify errors, and ensure source-grounding. "
        "Flag any unverified or potentially hallucinated claims.",
        backstory="""
        You are a critical reviewer with a skeptical eye. Your job is to verify 
        that every claim has proper source citations and the citations actually 
        support the claim. Flag any issues clearly.
        """,
        llm=llm,
        verbose=True,
        max_iter=10,
    )
