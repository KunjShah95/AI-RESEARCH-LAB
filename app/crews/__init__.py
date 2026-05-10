"""CrewAI crew configurations"""

from app.crews.research import create_research_crew
from app.crews.critique import create_critique_crew
from app.crews.debate import create_debate_crew

__all__ = [
    "create_research_crew",
    "create_critique_crew",
    "create_debate_crew",
]
