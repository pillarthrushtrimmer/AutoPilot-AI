"""Multi-Agent Pipeline."""

from __future__ import annotations
import asyncio, time
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from src.agents.base import BaseAgent, AgentResult

console = Console()

@dataclass
class PipelineResult:
    results: list[AgentResult]
    total_duration_ms: float

class Pipeline:
    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    async def execute_async(self) -> PipelineResult:
        start = time.perf_counter()
        results, context = [], ""
        console.print(Panel(f"{len(self.agents)} agents", title="\U0001f517 Pipeline", border_style="magenta"))
        for i, agent in enumerate(self.agents, 1):
            console.print(f"\n[bold magenta]\U0001f916 {i}/{len(self.agents)}:[/] {agent.name} — {agent.task}")
            full_task = agent.task + (f"\n\nContext:\n{context}" if context else "")
            r = await agent.execute(full_task)
            results.append(r)
            context = r.output[:3000]
        return PipelineResult(results, (time.perf_counter() - start) * 1000)

    def execute(self) -> list[AgentResult]:
        return asyncio.run(self.execute_async()).results
