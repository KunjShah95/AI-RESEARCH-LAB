"""Research crew configuration"""

from crewai import Crew, Task, Process
from app.agents import (
    create_researcher_agent,
    create_critic_agent,
    create_synthesizer_agent,
)


def create_research_crew() -> Crew:
    """Create the research crew with sequential process"""
    researcher = create_researcher_agent()
    critic = create_critic_agent()
    synthesizer = create_synthesizer_agent()

    research_task = Task(
        description="""
        Research the following topic: {topic}
        
        Find relevant papers and extract key information including:
        - Paper titles and authors
        - Main findings and contributions
        - Methodology used
        - Limitations
        
        Always cite sources as [Source: Title] for every claim.
        """,
        expected_output="Research findings with source citations",
        agent=researcher,
    )

    critique_task = Task(
        description="""
        Review the research findings and verify all claims.
        
        Check that:
        - All claims have proper source citations
        - Citations actually support the claims
        - Any uncertain information is flagged
        
        Return verified findings with any issues noted.
        """,
        expected_output="Verified research findings",
        agent=critic,
        context=[research_task],
    )

    synthesis_task = Task(
        description="""
        Create a well-structured research report from the verified findings.
        
        Structure:
        - Executive Summary
        - Key Findings (with citations)
        - Methodology Overview
        - Limitations
        - References
        
        Every claim must include [Source: Title] citations.
        """,
        expected_output="Final research report with citations",
        agent=synthesizer,
        context=[research_task, critique_task],
        output_file="research_report.md",
    )

    return Crew(
        agents=[researcher, critic, synthesizer],
        tasks=[research_task, critique_task, synthesis_task],
        process=Process.SEQUENTIAL,
        memory=True,
        verbose=True,
    )
