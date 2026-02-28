"""Web Search Tool."""
import os, httpx
from src.core.tools import tool

@tool(name="web_search", description="Search the web via SerpAPI or DuckDuckGo")
async def web_search(query: str, num_results: int = 5) -> str:
    key = os.getenv("SERPAPI_KEY")
    if key:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get("https://serpapi.com/search", params={"q": query, "api_key": key, "num": num_results, "engine": "google"})
            data = r.json()
        return "\n\n---\n\n".join(f"**{i[\"title\"]}**\n{i.get(\"snippet\",\"\")}\nURL: {i[\"link\"]}" for i in data.get("organic_results", [])[:num_results]) or "No results."
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_redirect": 1})
        data = r.json()
    return "\n\n".join(f"{i[\"Text\"]}" for i in data.get("RelatedTopics", [])[:num_results] if "Text" in i) or f"Results for: {query}"
