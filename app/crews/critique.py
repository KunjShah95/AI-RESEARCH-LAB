"""Critique crew configuration"""

from crewai import Crew, Task
from app.agents import create_critic_agent


def create_critique_crew() -> Crew:
    """Create a dedicated critique crew for evaluating outputs"""
    critic = create_critic_agent()

    evaluation_task = Task(
        description="""
        Evaluate the following research output for quality and accuracy.
        
        Check:
        1. Source-grounding: Every claim has [Source: Title] citations
        2. Claim verification: Citations actually support the claims
        3. Completeness: All key aspects are covered
        4. Clarity: Findings are clearly explained
        5. Limitations: Limitations are acknowledged
        
        Provide a detailed evaluation with scores and feedback.
        """,
        expected_output="Evaluation report with scores and feedback",
        agent=critic,
    )

    return Crew(agents=[critic], tasks=[evaluation_task], verbose=True)
