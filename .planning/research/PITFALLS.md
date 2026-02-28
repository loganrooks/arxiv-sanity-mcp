# Domain Pitfalls

**Domain:** Single-user workstation service deployment
**Researched:** 2026-02-28

## Critical Pitfalls

Mistakes that cause rewrites or major resource issues.

### Pitfall 1: MCP Server Process Accumulation (ACTIVE ON THIS MACHINE)
**What goes wrong:** Claude Code spawns MCP server processes (Python, Node.js) via stdio. When Claude Code exits, it fails to kill these child processes. They accumulate indefinitely.
**Why it happens:** Known bug in Claude Code (GitHub issue #1935, filed June 2025, still open as of February 2026). The MCP protocol specifies graceful shutdown, but Claude Code does not invoke cleanup handlers on exit.
**Consequences:** Observed right now on this machine: 91 orphaned processes consuming 3.4 GB of RAM. Each Claude Code session spawns ~6 MCP servers (sequential-thinking, serena, context7, tavily, philpapers, morphllm). Over weeks/months, hundreds accumulate.
**Prevention:**
- Cron job every 30 minutes to detect and kill orphaned MCP processes
- Detection: find MCP-related processes (serena, context7, sequential-thinking, etc.) whose parent is init (PID 1) or whose original Claude Code parent no longer exists
- Script must be careful NOT to kill MCP processes belonging to an active Claude Code session
**Detection:** `ps aux | grep -E 'serena|context7|tavily|philpapers|morphllm|sequential' | wc -l` -- anything above ~6 per active Claude Code session indicates orphans

### Pitfall 2: Linger Not Enabled = Services Die on Logout
**What goes wrong:** systemd user services are killed when the user's last session ends (SSH disconnect, logout). Without linger, all your carefully configured services stop the moment you close your laptop.
**Why it happens:** systemd defaults to cleaning up user services when no login session exists. This is the correct default for multi-user systems but wrong for a remote development server.
**Consequences:** Services stop randomly when SSH connections drop. Must manually restart everything after every disconnect.
**Prevention:** `sudo loginctl enable-linger rookslog` -- run once, persists across reboots. Verified that linger is currently NOT enabled on this machine (`Linger=no` observed).
**Detection:** `loginctl show-user rookslog | grep Linger` -- should show `Linger=yes`

### Pitfall 3: Binding to 0.0.0.0 Exposes Services to Local Network
**What goes wrong:** Services listening on all interfaces are accessible from the local network, not just Tailscale.
**Why it happens:** Many frameworks default to `0.0.0.0` for convenience. The PHL410 annotation tool (port 9001) and PaddleOCR (port 8765) are currently bound to `0.0.0.0`.
**Consequences:** Anyone on the same WiFi/ethernet network can access these services. Security risk, especially for services with no authentication.
**Prevention:** Always bind to `127.0.0.1`. Use Tailscale Serve for remote access. Docker: `ports: ["127.0.0.1:8765:8765"]`. Uvicorn: `--host 127.0.0.1`.
**Detection:** `ss -tlnp | grep '0.0.0.0'` -- shows services bound to all interfaces

## Moderate Pitfalls

### Pitfall 4: Docker iptables Firewall Bypass
**What goes wrong:** Docker manipulates iptables directly to expose container ports. If you publish a port without specifying an IP, Docker creates iptables rules that bypass UFW/firewalld, exposing the port to the world.
**Prevention:** Always use `127.0.0.1:hostport:containerport` in Docker port mappings. Never `hostport:containerport` alone.

### Pitfall 5: systemd User Service PATH Issues
**What goes wrong:** systemd user services run with a minimal environment. Conda environments, `uv`, `npm`, and other tools in custom paths are not found.
**Prevention:** Use absolute paths in `ExecStart=`. For Python: point to the venv's Python binary directly (`/path/to/.venv/bin/python`). For Node: use full path to the binary. Set `Environment=PATH=...` if needed.

### Pitfall 6: Python Buffered Output Hides Logs
**What goes wrong:** Python buffers stdout by default. When running under systemd, log lines don't appear in journald until the buffer fills (sometimes minutes or never).
**Prevention:** Always set `Environment=PYTHONUNBUFFERED=1` in systemd service files, or use `python -u`.

### Pitfall 7: Docker Data Root on Root Partition
**What goes wrong:** Docker stores images and container data on `/var/lib/docker/` which is on the root partition (55 GB, 70% used). Large images can fill root.
**Prevention:** This is already a known TODO: migrate Docker data-root to `/data/docker/`. Configure in `/etc/docker/daemon.json`: `{"data-root": "/data/docker"}`.
**Detection:** `du -sh /var/lib/docker/` -- check current usage

### Pitfall 8: Tailscale Serve Requires sudo
**What goes wrong:** `tailscale serve` commands require root/sudo access. Cannot be run from a non-root systemd user service or automated script without sudo configuration.
**Prevention:** Run Tailscale Serve configuration manually or via a setup script with sudo. The `--bg` flag makes it persistent so it only needs to be set once per service.

### Pitfall 9: uv Cache Accumulation
**What goes wrong:** Each `uvx` invocation (used by MCP servers) creates cached environments in `~/.cache/uv/`. The orphaned MCP processes each reference unique cache directories that persist after the process dies.
**Prevention:** Periodically clean uv cache: `uv cache clean`. Monitor with `du -sh ~/.cache/uv/`.
**Detection:** Multiple serena processes reference different cache paths (observed: `iEWFMXyg1OytdWvNO6H1U`, `5TFInB_5AgX-6Qg8HDOEb`, `zCVLTemzD_WBSM9z0L4rN`, etc.)

## Minor Pitfalls

### Pitfall 10: Port Conflicts Between Services
**What goes wrong:** Two services try to bind the same port. One fails silently or with an unclear error.
**Prevention:** Maintain a port registry (even a simple text file). Current known ports: 8765 (PaddleOCR), 9001 (PHL410), 9002 (annotation tool), 5432 (PostgreSQL), 6379 (Redis).

### Pitfall 11: Forgetting to Reload systemd After Editing Service Files
**What goes wrong:** Edit a .service file, run `systemctl --user restart <svc>`, old config is used.
**Prevention:** Always run `systemctl --user daemon-reload` after editing .service files, before restart.

### Pitfall 12: Docker Compose Version Mismatch
**What goes wrong:** Compose file uses features not available in installed version.
**Prevention:** Installed version is 2.40.3 (very recent). Use `version` key in compose file or omit it (modern practice). Avoid Compose V1 syntax.

### Pitfall 13: VS Code Server Process Accumulation
**What goes wrong:** Similar to MCP servers, VS Code Remote SSH spawns server processes that may not clean up properly. Currently 5+ VS Code server instances observed running.
**Prevention:** Periodic cleanup of old VS Code server processes. Consider using VS Code's built-in "Kill VS Code Server on Host" command.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| MCP Cleanup | Killing active session's MCP servers | Check if parent Claude Code PID still exists before killing |
| Enable Linger | None -- simple one-time command | Just do it |
| systemd Services | PATH issues, Python buffering | Use absolute paths, PYTHONUNBUFFERED=1 |
| Docker Compose | Port exposure, data-root space | 127.0.0.1 binding, migrate data-root first |
| Tailscale Serve | sudo requirement, path routing | Configure once with --bg, test from apollo |
| Project Template | Over-engineering the scaffold | Start simple, iterate after deploying 2-3 services |

## Sources

- MCP orphan bug: https://github.com/anthropics/claude-code/issues/1935
- Direct observation: 91 orphaned MCP processes, 3.4 GB RSS on this machine
- systemd user linger: https://wiki.archlinux.org/title/Systemd/User
- Docker iptables: https://docs.docker.com/network/packet-filtering-firewalls/
- Tailscale Serve: https://tailscale.com/kb/1242/tailscale-serve
