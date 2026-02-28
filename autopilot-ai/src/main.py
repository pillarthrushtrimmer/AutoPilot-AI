"""AutoPilot AI — CLI."""
import asyncio
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from src.core.engine import Engine, AgentConfig

app = typer.Typer(name="autopilot", help="\U0001f916 AutoPilot AI", add_completion=False)
console = Console()

BANNER = """[bold cyan]
    _         _        ____  _ _       _
   / \\  _   _| |_ ___ |  _ \\(_) | ___ | |_
  / _ \\| | | | __/ _ \\| |_) | | |/ _ \\| __|
 / ___ \\ |_| | || (_) |  __/| | | (_) | |_
/_/   \\_\\__,_|\\__\\___/|_|   |_|_|\\___/ \\__|
[/bold cyan]
[dim]Open-source AI agent framework v1.0.0[/dim]
"""

@app.command()
def chat(model: str = typer.Option("gpt-4o")):
    """Interactive chat."""
    console.print(BANNER)
    engine = Engine(AgentConfig(model=model))
    while True:
        try: inp = Prompt.ask("\n[bold green]You[/]")
        except (KeyboardInterrupt, EOFError): console.print("\n[dim]Bye![/dim]"); break
        if inp.lower() in ("exit", "quit", "q"): break
        if not inp.strip(): continue
        r = asyncio.run(engine.run(inp))
        console.print(f"\n[bold cyan]\U0001f916:[/] {r.output}\n")

@app.command()
def run(task: str = typer.Argument(...), model: str = typer.Option("gpt-4o")):
    """Execute a task."""
    r = asyncio.run(Engine(AgentConfig(model=model)).run(task))
    console.print(Panel(r.output, title="Result", border_style="green"))

@app.command()
def serve(port: int = typer.Option(8000), model: str = typer.Option("gpt-4o")):
    """Start API server."""
    import uvicorn
    from src.api.app import create_app
    console.print(f"[bold green]\U0001f680 http://localhost:{port}[/]")
    uvicorn.run(create_app(model), host="0.0.0.0", port=port)

@app.command()
def version():
    console.print("[bold]AutoPilot AI[/] v1.0.0")

if __name__ == "__main__": app()
