# Project Template for Deployable Scholarly Tools

**Researched:** 2026-02-28

## Recommended Project Scaffold

A tool that can be both developed locally AND deployed as a persistent service.

```
~/workspace/projects/<tool-name>/
|-- pyproject.toml              # Project metadata, dependencies, scripts
|-- uv.lock                     # Locked dependencies (committed)
|-- .python-version             # Python version pin
|-- .env.example                # Template for environment variables
|-- Makefile                    # Dev and deploy commands
|-- <tool_name>/
|   |-- __init__.py
|   |-- api.py                  # FastAPI app with /health endpoint
|   |-- core.py                 # Business logic
|   |-- config.py               # Settings via pydantic-settings
|-- tests/
|   |-- test_core.py
|-- deploy/
|   |-- <tool-name>.service     # systemd user service file
|   |-- <tool-name>.env         # Production env vars (NOT committed, .gitignored)
```

## Key Files

### pyproject.toml
```toml
[project]
name = "tool-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic-settings>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "httpx>=0.27",  # for testing FastAPI
    "ruff>=0.8",
]

[project.scripts]
tool-name = "tool_name.api:main"

[tool.ruff]
line-length = 100
```

### Makefile
```makefile
.PHONY: dev install deploy logs status restart

# Development
dev:
	uv run uvicorn tool_name.api:app --host 127.0.0.1 --port 8000 --reload

install:
	uv sync

test:
	uv run pytest

# Deployment
deploy: install
	cp deploy/tool-name.service ~/.config/systemd/user/
	systemctl --user daemon-reload
	systemctl --user enable --now tool-name

restart:
	systemctl --user restart tool-name

status:
	systemctl --user status tool-name

logs:
	journalctl --user -u tool-name -f

stop:
	systemctl --user stop tool-name
	systemctl --user disable tool-name
```

### systemd Service File (deploy/tool-name.service)
```ini
[Unit]
Description=Tool Name - Scholarly Research Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/rookslog/workspace/projects/tool-name
ExecStart=/home/rookslog/workspace/projects/tool-name/.venv/bin/python -m uvicorn tool_name.api:app --host 127.0.0.1 --port 8000
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=/home/rookslog/.config/dionysus/tool-name.env
Restart=on-failure
RestartSec=5
StartLimitBurst=3
StartLimitIntervalSec=60

# Hardening (optional but recommended)
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/home/rookslog/workspace/projects/tool-name
ReadWritePaths=/data

[Install]
WantedBy=default.target
```

### API with Health Check (tool_name/api.py)
```python
"""Main API for tool-name."""
import uvicorn
from fastapi import FastAPI

from tool_name import __version__

app = FastAPI(title="Tool Name", version=__version__)


@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "service": "tool-name", "version": __version__}


# Add your routes here


def main():
    """Entry point for `tool-name` command."""
    uvicorn.run("tool_name.api:app", host="127.0.0.1", port=8000)
```

### Config via pydantic-settings (tool_name/config.py)
```python
"""Configuration loaded from environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Service configuration. Values come from environment or .env file."""

    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = "postgresql://localhost:5432/toolname"
    debug: bool = False

    class Config:
        env_prefix = "TOOLNAME_"


settings = Settings()
```

## Development vs Production Workflow

| Aspect | Dev Mode | Production (systemd) |
|--------|----------|---------------------|
| Start | `make dev` (uvicorn --reload) | `make deploy` then `make restart` |
| Code changes | Auto-reload | `make restart` (sub-second) |
| Logs | Terminal stdout | `make logs` (journalctl) |
| Port | Same (8000) | Same (8000) |
| Environment | `.env` in project dir | `~/.config/dionysus/tool-name.env` |
| Crash recovery | Manual restart | Automatic (Restart=on-failure) |
| Boot start | No | Yes (systemctl enable) |

## Environment File Convention

```
~/.config/dionysus/
|-- scholardoc.env
|-- philo-rag.env
|-- zlibrary-mcp.env
|-- ...
```

All env files: `chmod 600`, owned by rookslog, NOT in git.

## Port Registry

Maintain in a central location to prevent conflicts:

```
# ~/.config/dionysus/ports.conf
# Service            Port    Status
paddleocr            8765    docker
scholardoc           8000    systemd
philo-rag            8001    systemd
zlibrary-mcp         8002    systemd
annotation-tool      9001    systemd (migrate from ad-hoc)
postgresql           5432    docker
redis                6379    docker
```

## Sources

- uv project management: https://docs.astral.sh/uv/guides/projects/
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/
- systemd user services: https://wiki.archlinux.org/title/Systemd/User
- pydantic-settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
