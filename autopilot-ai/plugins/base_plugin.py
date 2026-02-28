"""Base Plugin."""
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    name: str = "base"
    @abstractmethod
    async def setup(self, config: dict) -> None: ...
    @abstractmethod
    def get_tools(self) -> list: ...
