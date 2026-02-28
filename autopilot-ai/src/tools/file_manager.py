"""File Manager Tool."""
from pathlib import Path
from src.core.tools import tool

WS = Path("./workspace")
WS.mkdir(exist_ok=True)

@tool(name="file_manager", description="Read, write, list, delete files")
def file_manager(action: str, path: str, content: str = "") -> str:
    t = WS / path
    if action == "read":
        return t.read_text()[:5000] if t.exists() else f"Not found: {path}"
    elif action == "write":
        t.parent.mkdir(parents=True, exist_ok=True); t.write_text(content)
        return f"Written {len(content)} chars to {path}"
    elif action == "append":
        t.parent.mkdir(parents=True, exist_ok=True)
        with open(t, "a") as f: f.write(content)
        return f"Appended {len(content)} chars"
    elif action == "list":
        base = t if t.is_dir() else WS
        return "\n".join(str(p.relative_to(WS)) for p in base.rglob("*") if p.is_file())[:2000] or "Empty"
    elif action == "delete":
        if t.exists(): t.unlink(); return f"Deleted {path}"
        return "Not found"
    return f"Unknown: {action}"
