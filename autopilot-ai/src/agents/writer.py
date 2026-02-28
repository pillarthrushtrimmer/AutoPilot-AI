"""Writer Agent."""
from src.agents.base import BaseAgent

class Writer(BaseAgent):
    name = "writer"
    default_tools = ["web_search", "file_manager"]
    @property
    def system_prompt(self) -> str:
        return """You are a professional technical writer. Clear, structured, accurate, engaging. Use Markdown."""
