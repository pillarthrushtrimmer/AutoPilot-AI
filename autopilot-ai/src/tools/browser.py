"""Browser Tool (Playwright)."""
from src.core.tools import tool

@tool(name="browser", description="Open URL and extract text")
async def browser(url: str, selector: str = "body") -> str:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return "playwright not installed"
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        page = await b.new_page()
        try:
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            return (await page.inner_text(selector))[:5000]
        except Exception as e: return f"Error: {e}"
        finally: await b.close()
