"""GitHub Plugin."""
import os, httpx
from plugins.base_plugin import BasePlugin
from src.core.tools import tool

class GitHubPlugin(BasePlugin):
    name = "github"
    async def setup(self, config: dict) -> None: self.token = config.get("token", os.getenv("GITHUB_TOKEN", ""))
    def get_tools(self) -> list: return [github_create_issue, github_list_issues]

@tool(name="github_create_issue", description="Create a GitHub issue")
async def github_create_issue(repo: str, title: str, body: str = "") -> str:
    token = os.getenv("GITHUB_TOKEN", "")
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(f"https://api.github.com/repos/{repo}/issues", json={"title": title, "body": body},
                         headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"})
        if r.status_code == 201: d = r.json(); return f"Issue #{d[\"number\"]}: {d[\"html_url\"]}"
        return f"Failed ({r.status_code})"

@tool(name="github_list_issues", description="List open issues")
async def github_list_issues(repo: str) -> str:
    token = os.getenv("GITHUB_TOKEN", "")
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(f"https://api.github.com/repos/{repo}/issues", params={"state": "open", "per_page": 10},
                        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3+json"})
        issues = r.json()
        return "\n".join(f"#{i[\"number\"]} {i[\"title\"]}" for i in issues[:10]) if issues else "No issues"
