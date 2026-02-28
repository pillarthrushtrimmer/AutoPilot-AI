from autopilot import Pipeline, Researcher, Coder, Writer
pipeline = Pipeline([
    Researcher(task="Research best Python async patterns"),
    Coder(task="Write an async web scraper"),
    Writer(task="Write README docs"),
])
for r in pipeline.execute():
    print(f"[{r.agent_name}] {r.output[:200]}")
