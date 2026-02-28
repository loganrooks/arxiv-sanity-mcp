# Architecture Patterns

**Domain:** Single-user workstation service deployment
**Researched:** 2026-02-28

## Recommended Architecture

```
                      Tailscale Network (private)
                              |
                     [Tailscale Serve]
                      HTTPS reverse proxy
                     (*.dionysus.ts.net)
                              |
                 +------------+------------+
                 |                         |
          [systemd user]           [Docker Compose]
          Python/TS services       Isolated services
                 |                         |
    +------+-----+-----+        +---------+---------+
    |      |     |      |       |         |         |
  scholar  philo zlibrary ...  PaddleOCR PostgreSQL Redis
  doc      RAG   MCP            (CUDA)
  :8000    :8001 :8002          :8765    :5432     :6379

          All on 127.0.0.1 (localhost only)
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| systemd user services | Manage Python/TS process lifecycle | journald (logs), filesystem (code) |
| Docker Compose | Manage containerized service lifecycle | Docker daemon, networks |
| Tailscale Serve | Reverse proxy + HTTPS termination | systemd services, Docker services |
| journald | Centralized log storage and querying | All systemd-managed services |
| Cron cleanup | Kill orphaned MCP processes | Process table |
| uv | Python dependency/venv management | Project directories |

### Data Flow

**Development workflow:**
1. Edit code in `~/workspace/projects/<tool>/`
2. `systemctl --user restart <tool>` (sub-second restart)
3. Test via `curl localhost:<port>/health`
4. Logs visible via `journalctl --user -u <tool> -f`

**Remote access workflow:**
1. Service runs on `127.0.0.1:<port>` on dionysus
2. Tailscale Serve forwards `https://dionysus.<tailnet>.ts.net/<path>` to `localhost:<port>`
3. apollo/orpheus accesses via Tailscale-encrypted connection
4. No port forwarding, no firewall rules, no manual cert management

**MCP server lifecycle (current, broken):**
1. Claude Code starts -> spawns MCP servers via stdio
2. Claude Code session ends -> processes NOT killed (bug #1935)
3. New session starts -> spawns MORE processes
4. Result: 91 orphaned processes, 3.4 GB wasted RAM

**MCP server lifecycle (proposed fix):**
1. Same as above (can't change Claude Code behavior)
2. Cron job every 30 minutes: find and kill orphaned MCP processes
3. Orphans detected by: process tree detached from any Claude Code parent

## Patterns to Follow

### Pattern 1: systemd User Service Unit File
**What:** A unit file for each Python/TS service
**When:** Any service that accesses local filesystem, uses conda/uv environments, needs fast restart
**Example:**
```ini
# ~/.config/systemd/user/scholardoc.service
[Unit]
Description=ScholarDoc PDF Processing Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/rookslog/workspace/projects/scholardoc
ExecStart=/home/rookslog/workspace/projects/scholardoc/.venv/bin/python -m uvicorn scholardoc.api:app --host 127.0.0.1 --port 8000
Environment=PYTHONUNBUFFERED=1
Restart=on-failure
RestartSec=5
StartLimitBurst=3
StartLimitIntervalSec=60

[Install]
WantedBy=default.target
```

### Pattern 2: Docker Compose for Isolated Services
**What:** A single compose file for services needing containerization
**When:** GPU access (CUDA), external database images, services with complex native dependencies
**Example:**
```yaml
# ~/services/docker-compose.yml
services:
  paddleocr:
    image: paddleocr-server:latest
    ports:
      - "127.0.0.1:8765:8765"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8765/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  postgres:
    image: postgres:16
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_password
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "127.0.0.1:6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### Pattern 3: Tailscale Serve Configuration
**What:** Expose localhost services to tailnet with HTTPS
**When:** Service needs to be accessed from apollo or orpheus
**Example:**
```bash
# Expose scholardoc API with HTTPS
sudo tailscale serve --bg --https=443 /scholardoc localhost:8000

# Expose PaddleOCR
sudo tailscale serve --bg --https=443 /ocr localhost:8765

# View current serve config
sudo tailscale serve status

# Access from apollo:
# https://dionysus.<tailnet>.ts.net/scholardoc
# https://dionysus.<tailnet>.ts.net/ocr
```

### Pattern 4: Health Check Endpoint
**What:** Every HTTP service exposes GET /health
**When:** Always -- required for Docker healthcheck and monitoring
**Example:**
```python
# In any FastAPI service
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok", "service": "scholardoc", "version": "0.1.0"}
```

### Pattern 5: Environment File Pattern
**What:** Per-service .env file, not in git, referenced by systemd/docker
**When:** Any service needing credentials or configuration
**Example:**
```ini
# ~/.config/dionysus/scholardoc.env
PADDLEOCR_URL=http://127.0.0.1:8765
DATABASE_URL=postgresql://localhost:5432/scholardoc
OPENAI_API_KEY=sk-...
```
Referenced in systemd:
```ini
[Service]
EnvironmentFile=/home/rookslog/.config/dionysus/%n.env
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Binding to 0.0.0.0
**What:** Services listening on all interfaces
**Why bad:** Exposes service to local network, bypasses Tailscale security
**Instead:** Always bind to `127.0.0.1`, use Tailscale Serve for remote access

### Anti-Pattern 2: Running services in tmux/screen sessions
**What:** Starting services in terminal multiplexer and leaving them
**Why bad:** No auto-restart on crash, no log rotation, no boot persistence, no health monitoring
**Instead:** systemd user service with `Restart=on-failure`

### Anti-Pattern 3: Dockerizing everything
**What:** Building Docker images for simple Python scripts
**Why bad:** Slow dev iteration (rebuild image on every change), complex for filesystem access, unnecessary overhead
**Instead:** Docker only for services needing isolation (CUDA, databases). systemd for everything else.

### Anti-Pattern 4: Per-service log files
**What:** Each service writes to its own log file in a custom directory
**Why bad:** Manual rotation, no centralized querying, disk space management
**Instead:** Let services write to stdout/stderr, let systemd/docker capture to journald

### Anti-Pattern 5: Storing secrets in service files
**What:** Putting API keys directly in .service files or docker-compose.yml
**Why bad:** Files may be committed to git, visible in `systemctl show`
**Instead:** Use `EnvironmentFile=` with chmod 600 .env files

## Scalability Considerations

| Concern | Now (5 services) | Later (10-15 services) | At Limit (20+) |
|---------|-------------------|------------------------|-----------------|
| Memory | 32 GB plenty | Monitor per-service RSS | May need to prioritize |
| CPU | Xeon W-2125 (4c/8t) | Fine for I/O-bound services | GPU services compete with CUDA |
| Ports | Manual assignment | Port registry in a config file | Consider Tailscale Serve path-based routing |
| Logs | journald 500 MB cap | Sufficient | May need to increase or add retention |
| Management | CLI commands | Still fine with systemctl | Consider a simple dashboard script |

## Sources

- systemd user services: https://wiki.archlinux.org/title/Systemd/User
- Docker Compose: https://docs.docker.com/compose/
- Tailscale Serve: https://tailscale.com/kb/1242/tailscale-serve
- FastAPI Docker deployment: https://fastapi.tiangolo.com/deployment/docker/
- Claude Code MCP bug: https://github.com/anthropics/claude-code/issues/1935
