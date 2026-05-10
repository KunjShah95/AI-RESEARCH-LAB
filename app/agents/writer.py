"""Writer Agent - drafts research papers"""

from crewai import Agent
from langchain_openai import ChatOpenAI


class WriterAgent:
    """Agent that drafts research paper content"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")

    def create_agent(self) -> Agent:
        return Agent(
            role="Research Paper Writer",
            goal="Generate well-structured, academically rigorous research paper content",
            backstory="""You are an expert academic writer with PhD-level knowledge in computer science.
            You specialize in writing comprehensive literature reviews, research papers, and surveys.
            Your writing is clear, precise, and properly cited.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )
