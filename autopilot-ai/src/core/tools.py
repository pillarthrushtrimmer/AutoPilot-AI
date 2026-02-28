"""AutoPilot AI — Tool Registry."""

from __future__ import annotations
import json, inspect, logging
from typing import Any, Callable, get_type_hints
from functools import wraps

logger = logging.getLogger(__name__)
_TOOL_REGISTRY: dict[str, "ToolDef"] = {}

class ToolDef:
    def __init__(self, name: str, description: str, func: Callable, parameters: dict):
        self.name, self.description, self.func, self.parameters = name, description, func, parameters

    def to_openai_schema(self) -> dict:
        return {"type": "function", "function": {"name": self.name, "description": self.description, "parameters": self.parameters}}

def tool(name: str, description: str):
    """Decorator to register a function as an agent tool."""
    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        hints = get_type_hints(func)
        type_map = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array", dict: "object"}
        props, req = {}, []
        for pn, p in sig.parameters.items():
            props[pn] = {"type": type_map.get(hints.get(pn, str), "string")}
            if p.default is inspect.Parameter.empty:
                req.append(pn)
        _TOOL_REGISTRY[name] = ToolDef(name, description, func, {"type": "object", "properties": props, "required": req})
        @wraps(func)
        def wrapper(*a, **kw): return func(*a, **kw)
        wrapper._tool_name = name
        return wrapper
    return decorator

class ToolRegistry:
    def get_schemas(self, names: list[str]) -> list[dict]:
        return [_TOOL_REGISTRY[n].to_openai_schema() for n in names if n in _TOOL_REGISTRY]

    async def execute(self, name: str, arguments: str) -> Any:
        if name not in _TOOL_REGISTRY:
            return f"Error: tool \'{name}\' not found"
        try:
            args = json.loads(arguments) if isinstance(arguments, str) else arguments
            result = _TOOL_REGISTRY[name].func(**args)
            if inspect.isawaitable(result): result = await result
            return result
        except Exception as e:
            logger.error(f"Tool \'{name}\' failed: {e}")
            return f"Error: {e}"
