"""Debate crew configuration"""

from crewai import Crew, Task, Process, Agent
from langchain_openai import ChatOpenAI
from app.config import settings


def create_debate_crew() -> Crew:
    """Create the debate crew with adversarial roles"""

    llm = None
    if settings.openai_api_key:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.5,
            max_tokens=settings.llm_max_tokens,
            api_key=settings.openai_api_key,
        )

    proponent = Agent(
        role="Proponent",
        goal="Argue FOR the proposed approach/method. "
        "Find supporting evidence and highlight strengths.",
        backstory="""
        You argue in favor of the given approach. Present compelling arguments,
        cite supporting evidence, and address counter-arguments where possible.
        """,
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    critic = Agent(
        role="Critic",
        goal="Argue AGAINST the proposed approach/method. "
        "Find weaknesses, limitations, and counter-evidence.",
        backstory="""
        You provide critical analysis of the given approach. Identify weaknesses,
        cite counter-evidence, and highlight limitations.
        """,
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    methodologist = Agent(
        role="Methodologist",
        goal="Evaluate the methodology objectively. "
        "Assess rigor, validity, and reproducibility.",
        backstory="""
        You evaluate research methodology objectively. Assess study design,
        statistical rigor, reproducibility, and potential biases.
        """,
        llm=llm,
        verbose=True,
        max_iter=5,
    )

    proponent_task = Task(
        description="""
        Argue FOR the following thesis: {thesis}
        
        Present supporting arguments with citations. Address counter-arguments.
        """,
        expected_output="Proponent arguments with citations",
        agent=proponent,
    )

    critic_task = Task(
        description="""
        Argue AGAINST the following thesis: {thesis}
        
        Present counter-arguments with citations. Identify weaknesses.
        """,
        expected_output="Critic arguments with citations",
        agent=critic,
    )

    methodologist_task = Task(
        description="""
        Evaluate the methodology of the arguments presented.
        
        Assess: rigor, validity, reproducibility, potential biases.
        """,
        expected_output="Methodology evaluation",
        agent=methodologist,
        context=[proponent_task, critic_task],
    )

    synthesis_task = Task(
        description="""
        Synthesize the debate into a balanced conclusion.
        
        Summarize:
        - Key arguments for
        - Key arguments against
        - Methodology assessment
        - Final verdict with confidence level
        
        Include source citations throughout.
        """,
        expected_output="Debate synthesis with verdict",
        agent=methodologist,
        context=[proponent_task, critic_task, methodologist_task],
    )

    return Crew(
        agents=[proponent, critic, methodologist],
        tasks=[proponent_task, critic_task, methodologist_task, synthesis_task],
        process=Process.SEQUENTIAL,
        memory=True,
        verbose=True,
    )
