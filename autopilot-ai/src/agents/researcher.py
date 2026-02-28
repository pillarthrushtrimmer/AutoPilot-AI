"""Researcher Agent."""
from src.agents.base import BaseAgent

class Researcher(BaseAgent):
    name = "researcher"
    default_tools = ["web_search", "browser", "file_manager"]
    @property
    def system_prompt(self) -> str:
        return """You are a senior research analyst. Search 3-5 sources, analyze, synthesize, cite URLs. Prioritize primary sources."""
