"""AutoPilot AI — Task Planner."""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from litellm import acompletion

@dataclass
class Step:
    description: str
    prompt: str
    required_tools: list[str] = field(default_factory=list)

@dataclass
class Plan:
    task: str
    steps: list[Step] = field(default_factory=list)

PLANNER_PROMPT = """You are a task planning expert. Decompose the task into 1-5 steps.
For each step: {"description": "...", "prompt": "...", "tools": ["web_search"|"browser"|"code_executor"|"file_manager"|"api_caller"]}
Respond with JSON: {"steps": [...]}"""

class TaskPlanner:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    async def decompose(self, task: str, context: str = "") -> Plan:
        msg = f"Task: {task}"
        if context:
            msg += f"\n\nContext:\n{context}"
        resp = await acompletion(
            model=self.model,
            messages=[{"role": "system", "content": PLANNER_PROMPT}, {"role": "user", "content": msg}],
            temperature=0.2, response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        steps = [Step(s["description"], s["prompt"], s.get("tools", [])) for s in data.get("steps", [])]
        if not steps:
            steps = [Step(task, task)]
        return Plan(task=task, steps=steps)
