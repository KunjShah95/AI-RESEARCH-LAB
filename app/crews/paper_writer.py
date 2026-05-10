"""Paper Writing Crew - coordinates writer, editor, reviewer"""

from crewai import Crew, Task, Process
from app.agents.writer import WriterAgent
from app.agents.editor import EditorAgent
from app.agents.reviewer import ReviewerAgent
from typing import List, Dict, Any


class PaperWriterCrew:
    """Crew for generating complete research papers"""

    def __init__(self):
        self.writer = WriterAgent().create_agent()
        self.editor = EditorAgent().create_agent()
        self.reviewer = ReviewerAgent().create_agent()

    def create_crew(
        self, topic: str, paper_type: str, papers: List[Dict[str, Any]]
    ) -> Crew:
        """Create crew for paper generation"""

        writing_task = Task(
            description=f"""Write a comprehensive research paper on '{topic}' of type '{paper_type}'.
            Use the following papers as source material:
            {papers}
            
            Structure the paper with proper academic sections including:
            Abstract, Introduction, Related Work, Methods, Results, Discussion, Conclusion, References.
            Ensure all claims are grounded in the source papers.""",
            agent=self.writer,
            expected_output="Draft research paper content in Markdown format",
        )

        editing_task = Task(
            description="""Refine the drafted paper for clarity, academic tone, and structure.
            Improve sentence flow and ensure consistent terminology.
            Maintain all technical accuracy while improving readability.""",
            agent=self.editor,
            expected_output="Edited research paper with improved clarity and structure",
        )

        review_task = Task(
            description="""Review the edited paper for:
            1. Citation accuracy - all claims should be properly cited
            2. Factual correctness - no hallucinated facts
            3. Academic rigor - methodology and conclusions are sound
            4. Completeness - all required sections present
            
            Provide a pass/fail verdict with specific feedback.""",
            agent=self.reviewer,
            expected_output="Review verdict with quality score and feedback",
        )

        return Crew(
            agents=[self.writer, self.editor, self.reviewer],
            tasks=[writing_task, editing_task, review_task],
            process=Process.sequential,
            verbose=True,
        )

    def generate(
        self, topic: str, paper_type: str, papers: List[Dict[str, Any]]
    ) -> str:
        """Generate paper using the crew"""
        crew = self.create_crew(topic, paper_type, papers)
        result = crew.kickoff()
        return str(result)
