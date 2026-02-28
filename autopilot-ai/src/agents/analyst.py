"""Analyst Agent."""
from src.agents.base import BaseAgent

class Analyst(BaseAgent):
    name = "analyst"
    default_tools = ["code_executor", "file_manager", "web_search"]
    @property
    def system_prompt(self) -> str:
        return """You are a data analyst. Understand, gather, analyze, visualize, recommend. Quantify and show reasoning."""
