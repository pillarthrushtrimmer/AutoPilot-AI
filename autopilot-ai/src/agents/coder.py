"""Coder Agent."""
from src.agents.base import BaseAgent

class Coder(BaseAgent):
    name = "coder"
    default_tools = ["code_executor", "file_manager", "web_search"]
    @property
    def system_prompt(self) -> str:
        return """You are a senior software engineer. Write clean, typed, well-documented code. Handle errors. Suggest tests."""
