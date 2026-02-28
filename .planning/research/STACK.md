# Technology Stack

**Project:** Dionysus Platform -- Service Deployment
**Researched:** 2026-02-28

## Recommended Stack

### Service Management (Primary)
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| systemd user services | 255 (installed) | Manage Python/TS services | Already on system, no extra deps, journald integration, auto-restart, socket activation |
| loginctl linger | -- | Allow services to run without login | Required for services to survive SSH logout |

### Container Management (Isolation)
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Docker | 29.0.2 (installed) | Run services needing isolation | Already installed, PaddleOCR already runs here |
| Docker Compose | 2.40.3 (installed) | Orchestrate multi-container services | Declarative config, health checks, restart policies, dependency ordering |

### Network Exposure
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Tailscale Serve | Current (installed) | Expose services to tailnet | Built-in reverse proxy, auto HTTPS for *.ts.net, no extra software |
| Tailscale | Current (installed) | VPN mesh | Already configured, 3 devices connected |

### Log Management
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| journald | 255 (installed) | Centralized logging | Already configured (500MB cap), integrates with systemd services natively |
| journalctl | 255 (installed) | Log querying | Filter by service, time, priority -- no extra tools needed |

### Python Tooling
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| uv | Current (installed) | Python project/venv management | Fast, already used for MCP servers (uvx), lockfile support |

### Process Cleanup
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| cron + kill script | -- | Clean orphaned MCP processes | Pragmatic workaround for Claude Code bug #1935 |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Service mgmt | systemd user | supervisord | Extra dependency, systemd already does everything needed |
| Service mgmt | systemd user | Docker for everything | Overhead for simple Python scripts, slower dev iteration (rebuild image vs restart service) |
| Service mgmt | systemd user | PM2 (Node) | Only handles Node/JS, adds dependency for no benefit |
| Reverse proxy | Tailscale Serve | Caddy | Extra software to install/maintain, Tailscale Serve handles the simple case |
| Reverse proxy | Tailscale Serve | nginx | Complex config, overkill for internal-only services |
| Reverse proxy | Tailscale Serve | Bind to Tailscale IP | No HTTPS, requires knowing IP, services must handle TLS |
| Containers | Docker | Podman | Docker already installed and working, PaddleOCR uses Docker |
| Logs | journald | Loki/Grafana | Massive overkill for single-user, 5-10 services |
| Logs | journald | Centralized log dir | Reinvents what journald already does, no structured querying |

## Key Commands

```bash
# Enable linger (run once, requires sudo)
sudo loginctl enable-linger rookslog

# Create user service directory
mkdir -p ~/.config/systemd/user/

# Example: manage a service
systemctl --user start scholardoc
systemctl --user stop scholardoc
systemctl --user restart scholardoc
systemctl --user status scholardoc
systemctl --user enable scholardoc  # auto-start on boot

# View logs for a service
journalctl --user -u scholardoc -f          # follow live
journalctl --user -u scholardoc --since today  # today's logs
journalctl --user -u scholardoc -n 100      # last 100 lines

# Tailscale Serve (persistent background)
sudo tailscale serve --bg --https=443 localhost:8000
sudo tailscale serve status
sudo tailscale serve --https=443 localhost:8000 off  # disable

# Docker Compose
docker compose -f ~/services/docker-compose.yml up -d
docker compose -f ~/services/docker-compose.yml logs -f
docker compose -f ~/services/docker-compose.yml ps
```

## Sources

- systemd 255 verified on this machine via `systemd --version`
- Docker 29.0.2 / Compose 2.40.3 verified via `docker --version` / `docker compose version`
- Tailscale Serve docs: https://tailscale.com/kb/1242/tailscale-serve
- Tailscale Services docs: https://tailscale.com/docs/features/tailscale-services
- journald config verified at /etc/systemd/journald.conf (500MB cap already set)
- Claude Code MCP issue: https://github.com/anthropics/claude-code/issues/1935
- systemd user services: https://wiki.archlinux.org/title/Systemd/User
