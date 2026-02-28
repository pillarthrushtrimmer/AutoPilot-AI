"""AutoPilot AI — Base Agent."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.core.engine import Engine, AgentConfig, TaskResult

@dataclass
class AgentResult:
    agent_name: str
    task: str
    output: str
    steps_count: int = 0
    duration_ms: float = 0.0

class BaseAgent(ABC):
    name: str = "base"
    description: str = ""
    default_tools: list[str] = []

    def __init__(self, task: str = "", model: str = "gpt-4o", **kwargs):
        self.task = task
        self.config = AgentConfig(model=model, system_prompt=self.system_prompt, tools=self.default_tools, **kwargs)
        self.engine = Engine(self.config)

    @property
    @abstractmethod
    def system_prompt(self) -> str: ...

    async def execute(self, task: str | None = None) -> AgentResult:
        task = task or self.task
        r: TaskResult = await self.engine.run(task)
        return AgentResult(self.name, task, r.output, len(r.steps), r.total_duration_ms)

    def run(self, task: str | None = None) -> str:
        import asyncio
        return asyncio.run(self.execute(task)).output

class GeneralAgent(BaseAgent):
    name = "general"
    default_tools = ["web_search", "file_manager", "code_executor"]
    @property
    def system_prompt(self) -> str:
        return "You are AutoPilot AI, a helpful assistant. Search the web, write code, manage files. Be concise and accurate."
