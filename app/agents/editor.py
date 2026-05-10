"""Editor Agent - refines and improves paper content"""

from crewai import Agent
from langchain_openai import ChatOpenAI


class EditorAgent:
    """Agent that edits and refines research papers"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4")

    def create_agent(self) -> Agent:
        return Agent(
            role="Research Paper Editor",
            goal="Improve clarity, flow, and academic tone of research papers",
            backstory="""You are a senior academic editor with 20 years of experience.
            You excel at refining academic writing, ensuring proper structure,
            and improving readability while maintaining technical accuracy.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
        )
