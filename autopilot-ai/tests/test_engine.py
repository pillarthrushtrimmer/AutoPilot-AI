from src.core.engine import AgentConfig, StepResult

def test_config_defaults():
    c = AgentConfig()
    assert c.model == "gpt-4o" and c.temperature == 0.7 and c.max_iterations == 10

def test_step_result():
    r = StepResult(1, "test", "ok", "content", ["web_search"])
    assert r.step_index == 1 and "web_search" in r.tools_used
