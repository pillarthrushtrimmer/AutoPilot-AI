# Contributing to AutoPilot AI

We love contributions! Here\'s how to get started.

## Development Setup

```

git clone https://github.com/jebo/autopilot-ai.git

cd autopilot-ai

pip install -e ".[dev]"

```

## Code Style

- We use **ruff** for linting and **mypy** for type checking
- Run `ruff check src/ tests/` before committing
- All functions should have type hints and docstrings

## Pull Requests

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit changes: `git commit -m "feat: add my feature"`
4. Push: `git push origin feat/my-feature`
5. Open a PR

## Issues

Bug reports and feature requests are welcome via GitHub Issues.
