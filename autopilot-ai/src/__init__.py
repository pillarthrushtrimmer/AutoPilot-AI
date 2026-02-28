"""AutoPilot AI — Open-source autonomous AI agent framework."""

__version__ = "1.0.0"

from src.core.engine import Engine, AgentConfig
from src.agents.base import BaseAgent, AgentResult
from src.agents.researcher import Researcher
from src.agents.coder import Coder
from src.agents.writer import Writer
from src.agents.analyst import Analyst
from src.agents.pipeline import Pipeline
from src.core.tools import tool

__all__ = [
    "Engine", "AgentConfig", "BaseAgent", "AgentResult",
    "Researcher", "Coder", "Writer", "Analyst", "Pipeline", "tool",
]

def Agent(model: str = "gpt-4o", **kwargs):
    """Shortcut to create a general-purpose agent."""
    from src.agents.base import GeneralAgent
    return GeneralAgent(task="", model=model, **kwargs)
