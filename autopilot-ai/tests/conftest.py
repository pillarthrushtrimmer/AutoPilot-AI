import pytest
from src.core.engine import Engine, AgentConfig
from src.core.tools import ToolRegistry

@pytest.fixture
def config(): return AgentConfig(model="gpt-4o", max_iterations=3, verbose=False)

@pytest.fixture
def engine(config): return Engine(config)

@pytest.fixture
def tool_registry(): return ToolRegistry()
