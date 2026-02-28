"""AutoPilot AI — Core Execution Engine."""

from __future__ import annotations
import asyncio, time
from dataclasses import dataclass, field
from typing import Any
from litellm import acompletion
from rich.console import Console
from rich.panel import Panel
from src.core.memory import MemoryManager
from src.core.planner import TaskPlanner, Step
from src.core.tools import ToolRegistry

console = Console()

@dataclass
class AgentConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 4096
    max_iterations: int = 10
    system_prompt: str = "You are a helpful AI assistant."
    tools: list[str] = field(default_factory=list)
    memory_enabled: bool = True
    verbose: bool = True

@dataclass
class StepResult:
    step_index: int
    description: str
    summary: str
    content: str
    tools_used: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

@dataclass
class TaskResult:
    task: str
    output: str
    steps: list[StepResult] = field(default_factory=list)
    total_duration_ms: float = 0.0

class Engine:
    """Core execution engine: Plan -> Execute -> Synthesize."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory = MemoryManager() if config.memory_enabled else None
        self.planner = TaskPlanner(model=config.model)
        self.tools = ToolRegistry()

    async def run(self, task: str) -> TaskResult:
        start = time.perf_counter()
        if self.config.verbose:
            console.print(Panel(task, title="\U0001f3af Task", border_style="cyan"))

        context = ""
        if self.memory:
            memories = await self.memory.recall(task, top_k=5)
            if memories:
                context = "\n".join(f"- {m}" for m in memories)

        plan = await self.planner.decompose(task, context)
        if self.config.verbose:
            console.print(f"[bold yellow]\U0001f4cb Plan:[/] {len(plan.steps)} steps")

        step_results: list[StepResult] = []
        for i, step in enumerate(plan.steps, 1):
            if self.config.verbose:
                console.print(f"\n[bold green]\u25b6 Step {i}:[/] {step.description}")
            s = time.perf_counter()
            result = await self._execute_step(i, step)
            result.duration_ms = (time.perf_counter() - s) * 1000
            step_results.append(result)
            if self.config.verbose:
                console.print(f"[dim]  \u2713 {result.summary[:120]} ({result.duration_ms:.0f}ms)[/dim]")

        output = await self._synthesize(task, step_results)
        if self.memory:
            await self.memory.store(task=task, result=output)

        total_ms = (time.perf_counter() - start) * 1000
        if self.config.verbose:
            console.print(Panel(output[:500], title="\u2705 Result", border_style="green"))
        return TaskResult(task=task, output=output, steps=step_results, total_duration_ms=total_ms)

    async def _execute_step(self, index: int, step: Step) -> StepResult:
        messages = [
            {"role": "system", "content": self.config.system_prompt},
            {"role": "user", "content": step.prompt},
        ]
        tool_schemas = self.tools.get_schemas(step.required_tools)
        tools_used: list[str] = []

        for _ in range(self.config.max_iterations):
            resp = await acompletion(
                model=self.config.model, messages=messages,
                tools=tool_schemas or None, temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            choice = resp.choices[0]
            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                messages.append(choice.message)
                for call in choice.message.tool_calls:
                    tools_used.append(call.function.name)
                    r = await self.tools.execute(call.function.name, call.function.arguments)
                    messages.append({"role": "tool", "tool_call_id": call.id, "content": str(r)[:4000]})
            else:
                c = choice.message.content or ""
                return StepResult(step_index=index, description=step.description,
                                  summary=c[:200].replace("\n", " "), content=c, tools_used=tools_used)
        return StepResult(step_index=index, description=step.description,
                          summary="Max iterations", content="", tools_used=tools_used)

    async def _synthesize(self, task: str, results: list[StepResult]) -> str:
        if len(results) == 1:
            return results[0].content
        combined = "\n\n---\n\n".join(f"### Step {r.step_index}: {r.description}\n{r.content}" for r in results)
        resp = await acompletion(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "Synthesize step results into one coherent answer."},
                {"role": "user", "content": f"Task: {task}\n\nResults:\n{combined}"},
            ], temperature=0.3,
        )
        return resp.choices[0].message.content or ""
