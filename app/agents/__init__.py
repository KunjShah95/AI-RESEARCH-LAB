"""CrewAI agents"""

from app.agents.researcher import create_researcher_agent
from app.agents.critic import create_critic_agent
from app.agents.synthesizer import create_synthesizer_agent

__all__ = [
    "create_researcher_agent",
    "create_critic_agent",
    "create_synthesizer_agent",
]
