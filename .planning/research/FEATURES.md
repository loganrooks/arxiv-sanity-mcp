# Feature Landscape

**Domain:** Single-user workstation service deployment
**Researched:** 2026-02-28

## Table Stakes

Features that must work for the platform to be usable.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Auto-restart on crash | Services must recover without manual intervention | Low | systemd `Restart=on-failure` / Docker `restart: unless-stopped` |
| Start on boot | Remote workstation -- nobody logs in to start services | Low | systemd `enable` + linger / Docker restart policy |
| Log access | Must be able to diagnose issues remotely | Low | journald for systemd, `docker logs` for containers |
| Graceful stop/restart | Code changes need clean restart without data loss | Low | systemd `ExecStop` / Docker `stop_signal` |
| Service status overview | Quick check of what's running and healthy | Low | `systemctl --user list-units` / `docker compose ps` |
| Remote access via Tailscale | Must work from apollo (MacBook) and orpheus (iPhone) | Medium | Tailscale Serve with --bg flag |

## Differentiators

Features that make the platform significantly more useful than ad-hoc management.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| MCP orphan cleanup | Recover 3.4 GB+ RAM from leaked processes | Low | Cron script, immediate value |
| HTTPS via Tailscale Serve | Secure access without manual cert management | Low | Automatic with *.ts.net domains |
| Dev mode (edit-restart cycle) | Fast iteration: edit Python, `systemctl --user restart svc` | Low | No image rebuild, just restart |
| Health checks | Know when a service is actually responding, not just running | Medium | HTTP health endpoints + systemd watchdog or Docker healthcheck |
| Service dependency ordering | Start PostgreSQL before services that need it | Low | systemd `After=` / Docker `depends_on` |
| Unified project scaffold | Every new tool deploys the same way | Medium | Template with Makefile + service file + pyproject.toml |
| Per-service environment files | Credentials separate from code, per-service isolation | Low | systemd `EnvironmentFile=` / Docker `env_file` |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Kubernetes / k3s | Massive overkill for 5-10 services on one machine | systemd + Docker Compose |
| Container orchestration (Swarm) | Single machine, no clustering needed | Docker Compose is sufficient |
| Custom monitoring dashboard | Over-engineering for one user | `systemctl --user status` + journalctl |
| Grafana/Prometheus stack | 5-10 services do not need time-series monitoring | journald + health checks |
| nginx/Caddy reverse proxy | Extra software when Tailscale Serve does the job | Tailscale Serve |
| CI/CD pipeline | Single developer, local deploys | Makefile with `deploy` target |
| Dockerize everything | Slower dev iteration, unnecessary isolation for Python tools | systemd for Python, Docker only when isolation needed |
| Ansible/Puppet/Chef | One machine, one user, no fleet management | Shell scripts or Makefile |

## Feature Dependencies

```
loginctl enable-linger --> systemd user services work after logout
systemd user services --> service auto-restart, logging, boot start
Docker Compose --> container health checks, restart policies
Health check endpoints --> meaningful Docker/systemd health monitoring
Tailscale Serve --> remote HTTPS access (depends on services existing first)
MCP cleanup cron --> independent (can be done immediately)
```

## MVP Recommendation

Prioritize (immediate value, low effort):
1. **MCP cleanup script** -- recovers 3.4 GB now, prevents future accumulation
2. **Enable linger** -- one command, unlocks all systemd user services
3. **Migrate PHL410 annotation tool (port 9001) to systemd** -- validates the pattern
4. **Docker Compose for existing containers** -- consolidate PaddleOCR + databases

Defer:
- **Tailscale Serve**: Until there are services worth exposing remotely
- **Project template**: Until 2-3 services are deployed and patterns are clear
- **Tailscale Services (new feature)**: Overkill for current scale, revisit if multi-device

## Sources

- Direct system observation via `ps aux`, `ss -tlnp`, `docker ps`
- Tailscale Serve: https://tailscale.com/kb/1242/tailscale-serve
- systemd user services: https://wiki.archlinux.org/title/Systemd/User
