"""Reviewer Agent - validates paper quality and citations"""

from crewai import Agent
from langchain_openai import ChatOpenAI


class ReviewerAgent:
    """Agent that reviews and validates research papers"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")

    def create_agent(self) -> Agent:
        return Agent(
            role="Research Paper Reviewer",
            goal="Validate paper quality, check citations, and ensure factual accuracy",
            backstory="""You are a peer reviewer for top-tier academic conferences.
            You are critical but fair, ensuring papers meet academic standards
            for methodology, citations, and claims.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )
