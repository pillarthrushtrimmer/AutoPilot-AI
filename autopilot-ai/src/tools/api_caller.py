"""API Caller Tool."""
import json, httpx
from src.core.tools import tool

@tool(name="api_caller", description="HTTP requests to APIs")
async def api_caller(method: str, url: str, body: str = "", headers: str = "") -> str:
    h = json.loads(headers) if headers else {}
    b = json.loads(body) if body else None
    async with httpx.AsyncClient(timeout=15) as c:
        try:
            r = await c.request(method.upper(), url, json=b, headers=h)
            return f"Status: {r.status_code}\n{r.text[:3000]}"
        except Exception as e: return f"Failed: {e}"
