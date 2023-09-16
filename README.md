[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Simple starter base for FastAPI

# Setup

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry shell
poetry install
make dev
```

# Generating migrations

```bash
alembic revision -m "create account table"
```
