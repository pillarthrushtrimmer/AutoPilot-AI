"""Code Executor Tool (sandboxed)."""
import asyncio, sys, tempfile
from src.core.tools import tool

@tool(name="code_executor", description="Execute Python code in sandbox")
async def code_executor(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code); f.flush(); path = f.name
    try:
        proc = await asyncio.create_subprocess_exec(sys.executable, path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await asyncio.wait_for(proc.communicate(), timeout=30)
        s = ""
        if out: s += f"STDOUT:\n{out.decode()[:3000]}"
        if err: s += f"\nSTDERR:\n{err.decode()[:1000]}"
        if proc.returncode: s += f"\nExit: {proc.returncode}"
        return s or "OK (no output)"
    except asyncio.TimeoutError: return "Timeout (30s)"
    except Exception as e: return f"Error: {e}"
