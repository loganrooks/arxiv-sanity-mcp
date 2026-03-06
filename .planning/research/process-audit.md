# Process and Service Audit

**Audited:** 2026-03-06T02:30:09Z
**Auditor:** Claude Code (automated)
**Scope:** All listening sockets, systemd services (system and user), Docker containers, cron jobs, tmux sessions, orphaned/stale processes

## Executive Summary

The system has **44 listening TCP sockets**, **46 system services**, **46 user services**, **1 Docker container** (PaddleOCR, running 7 weeks), **5 cron entries**, and **19 tmux sessions** (most stale from Dec 2025 - Jan 2026). There are **13 active Claude Code instances** consuming significant memory (~7.5GB combined RSS), plus **30+ total Claude-related processes** including MCP server children and VS Code extension instances. VS Code desktop and remote server processes account for another ~2.5GB. The system is heavily loaded with long-running development agent processes that have accumulated over weeks/months without cleanup.

Key concerns: stale tmux sessions holding orphaned Claude instances, Docker data-root on `/var/lib/docker` (root partition), and 158 orphaned ssh-agent processes.

## Findings

### Finding: 19 Stale Tmux Sessions

| Property | Value |
|----------|-------|
| Severity | HIGH |
| Category | maintenance |
| Current State | 19 tmux sessions, 14 from claude-enhanced group (Dec 29 2025 - Jan 26 2026), 5 others. Only 5 currently attached (2, crypt, dionysus, gsd, scholardoc). |
| Expected State | Active sessions only; stale sessions from weeks/months ago should be cleaned |
| Remediation | Phase 3: CLN-07 -- Kill stale tmux sessions and their child processes |
| Verified By | `tmux list-sessions` |

**Session Inventory:**

| Session | Created | Status | Group |
|---------|---------|--------|-------|
| 2 | 2026-01-08 04:00 | attached | -- |
| 3 | 2026-01-08 10:51 | detached | -- |
| claude-enhanced | 2025-12-29 16:32 | attached | claude-enhanced |
| claude-enhanced-5 | 2026-01-09 15:41 | detached | claude-enhanced |
| claude-enhanced-6 | 2026-01-09 16:46 | detached | claude-enhanced |
| claude-enhanced-7 | 2026-01-09 21:57 | detached | claude-enhanced |
| claude-enhanced-8 | 2026-01-18 21:51 | detached | claude-enhanced |
| claude-enhanced-9 | 2026-01-19 00:00 | detached | claude-enhanced |
| claude-enhanced-10 | 2026-01-19 00:00 | detached | claude-enhanced |
| claude-enhanced-11 | 2026-01-23 14:30 | detached | claude-enhanced |
| claude-enhanced-12 | 2026-01-24 01:26 | detached | claude-enhanced |
| claude-enhanced-13 | 2026-01-24 16:06 | detached | claude-enhanced |
| claude-enhanced-14 | 2026-01-24 16:06 | detached | claude-enhanced |
| claude-enhanced-15 | 2026-01-26 02:52 | detached | claude-enhanced |
| crypt | 2026-01-08 22:54 | attached | -- |
| dionysus | 2026-03-05 19:53 | attached | -- |
| gsd | 2026-03-05 18:49 | attached | -- |
| scholardoc | 2026-01-28 19:13 | attached | -- |
| zlibrary | 2026-01-28 21:14 | attached | -- |

10 of 19 sessions are detached and stale (all from the claude-enhanced group, plus session "3"). These likely hold orphaned Claude and shell processes consuming memory.

### Finding: 13+ Active Claude Code Instances

| Property | Value |
|----------|-------|
| Severity | HIGH |
| Category | performance |
| Current State | 13 claude CLI processes (330MB-680MB RSS each), 3 VS Code extension Claude instances, plus MCP server children and shell wrappers. ~30 total Claude-related processes. Combined RSS estimate: ~7.5GB |
| Expected State | 1-3 active Claude instances for current work |
| Remediation | Phase 3: CLN-07 -- Terminate stale Claude instances, establish session hygiene |
| Verified By | `ps aux \| grep claude` |

**Active Claude CLI Instances by Age:**

| PID | Started | RSS (MB) | Command | TTY |
|-----|---------|----------|---------|-----|
| 886344 | 2025 (Dec) | 365 | claude -r | pts/9 |
| 749526 | Jan 15 | 324 | claude -r | pts/42 |
| 3820271 | Jan 28 | 285 | claude -r | pts/25 |
| 2580787 | Jan 09 | 521 | claude | pts/28 |
| 2736026 | Jan 18 | 565 | claude -r | -- (bg) |
| 1105490 | Feb 11 | 440 | claude --dangerously-skip-permissions -r | pts/76 |
| 2901731 | Feb 26 | 504 | claude -r | pts/52 |
| 3697484 | Mar 01 | 394 | claude -r --dangerously-skip-permissions | pts/77 |
| 1802652 | Today 19:49 | 499 | claude -r --dangerously-skip-permissions | pts/69 |
| 1843663 | Today 20:12 | 664 | claude -r --dangerously-skip-permissions | pts/62 |
| 1894629 | Today 20:31 | 467 | claude -r --dangerously-skip-permissions | pts/58 |
| 1903263 | Today 20:33 | 622 | claude --worktree npm-fix | pts/75 |
| 1942578 | Today 20:41 | 529 | claude -r --dangerously-skip-permissions | pts/70 |

Instances from 2025 and early January are almost certainly orphaned (2+ months old). The 5 instances from today are likely active work.

### Finding: 158 Orphaned ssh-agent Processes

| Property | Value |
|----------|-------|
| Severity | MEDIUM |
| Category | maintenance |
| Current State | 158 ssh-agent processes running -- likely one spawned per terminal/session without cleanup |
| Expected State | 1-2 ssh-agent processes (one per login session) |
| Remediation | Phase 3: CLN-07 -- Kill orphaned ssh-agents, fix session setup to reuse agent |
| Verified By | `ps aux \| awk '{print $11}' \| sort \| uniq -c \| sort -rn` |

### Finding: Multiple VS Code Server/Extension Host Processes

| Property | Value |
|----------|-------|
| Severity | LOW |
| Category | performance |
| Current State | 23 VS Code desktop processes (code), 18 vscode-server node processes, 13 /proc/self/exe utility processes. Multiple extension hosts with 250-980MB RSS each. |
| Expected State | Active VS Code instances only, with extension hosts for open workspaces |
| Remediation | Phase 3: CLN-07 -- Restart VS Code cleanly; consider reducing extension count |
| Verified By | `ps aux \| grep vscode`, `ps aux \| awk '{print $11}' \| sort \| uniq -c` |

### Finding: Docker Data-Root on Root Partition

| Property | Value |
|----------|-------|
| Severity | HIGH |
| Category | storage |
| Current State | Docker data-root at `/var/lib/docker` (root partition, 55GB total). Docker using 7.76GB images + 144MB containers + 4.05GB build cache = ~12GB on root. 6.02GB reclaimable from unused images. |
| Expected State | Docker data-root should be on /data or /home partition to avoid root partition pressure |
| Remediation | Phase 3: CLN-03 -- Migrate Docker data-root to /data/docker/ |
| Verified By | `docker info --format '{{.DockerRootDir}}'` and `docker system df` |

**Docker Disk Usage:**

| Type | Total | Active | Size | Reclaimable |
|------|-------|--------|------|-------------|
| Images | 3 | 1 | 7.76GB | 6.022GB (77%) |
| Containers | 1 | 1 | 144MB | 0B |
| Local Volumes | 0 | 0 | 0B | 0B |
| Build Cache | 54 | 0 | 4.047GB | 0B |

### Finding: Uvicorn on 0.0.0.0:9001 (Annotation Tool)

| Property | Value |
|----------|-------|
| Severity | MEDIUM |
| Category | security |
| Current State | Uvicorn (PHL410 annotation tool) listening on 0.0.0.0:9001 -- exposed to all interfaces. Spawned by a Claude shell snapshot from Jan 16. |
| Expected State | Should bind to 127.0.0.1:9001 (localhost only) or be stopped if not in active use |
| Remediation | Phase 3: SEC-01 -- Rebind to localhost or behind Tailscale |
| Verified By | `ss -tlnp` showing `0.0.0.0:9001` with uvicorn pid |

### Finding: Long-Running Shell Background Processes

| Property | Value |
|----------|-------|
| Severity | LOW |
| Category | maintenance |
| Current State | Several Claude shell-snapshot spawned background processes still running: (1) annotation tool uvicorn on port 9001 since Jan 16, (2) python run.py on port 9002 since Jan 14, (3) SSH monitoring loop to VM since 2025. |
| Expected State | Background processes should be managed via systemd or cleaned up when no longer needed |
| Remediation | Phase 3: CLN-07 -- Audit and terminate stale background processes |
| Verified By | `ps aux \| grep claude \| grep shell-snapshots` |

## Raw Data

### All Listening TCP Sockets (44 total)

| Local Address | Port | Process | Notes |
|---------------|------|---------|-------|
| 127.0.0.1 | 4264 | code (pid=733011) | VS Code internal |
| 127.0.0.1 | 4379 | code (pid=1848728) | VS Code internal |
| 127.0.0.1 | 4889 | node (pid=1857044) | VS Code extension |
| 127.0.0.1 | 37771 | code-c3a26841a8 (pid=1997121) | VS Code server |
| 127.0.0.1 | 5453 | code (pid=1445249) | VS Code internal |
| 100.93.212.44 | 34825 | (system) | Tailscale service |
| 127.0.0.1 | 5432 | (system) | PostgreSQL -- GOOD: localhost only |
| **0.0.0.0** | **5900** | **(system)** | **VNC -- CRITICAL: all interfaces** |
| 127.0.0.1 | 5868 | node (pid=1484372) | VS Code extension |
| 127.0.0.1 | 6379 | (system) | Redis -- GOOD: localhost only |
| 127.0.0.1 | 56830 | code (pid=961761) | VS Code internal |
| 127.0.0.1 | 24287 | python (pid=2902130) | MCP server |
| 127.0.0.1 | 24285 | python (pid=1105816) | MCP server |
| 127.0.0.1 | 24282 | python (pid=750044) | MCP server |
| 127.0.0.1 | 24283 | python (pid=3820679) | MCP server |
| 127.0.0.1 | 24291 | python (pid=3697800) | MCP server |
| 127.0.0.1 | 16564 | node (pid=1856012) | VS Code extension host |
| **0.0.0.0** | **80** | **(system)** | **Nginx -- CRITICAL: all interfaces** |
| **0.0.0.0** | **22** | **(system)** | **SSH -- expected, all interfaces** |
| 127.0.0.1 | 631 | (system) | CUPS -- localhost only |
| 127.0.0.1 | 34994 | code (pid=731313) | VS Code internal |
| 127.0.0.53 | 53 | (system) | systemd-resolved |
| 127.0.0.1 | 19270 | code (pid=732300) | VS Code internal |
| 127.0.0.1 | 3404 | code (pid=731784) | VS Code internal |
| 127.0.0.1 | 36214 | node (pid=1819084) | VS Code extension host |
| 192.168.122.1 | 53 | (system) | libvirt DNS (virbr0) |
| 127.0.0.1 | 62212 | node (pid=1483528) | VS Code extension host |
| 127.0.0.1 | 41031 | code (pid=732300) | VS Code internal |
| **0.0.0.0** | **9001** | **uvicorn (pid=2366305)** | **Annotation tool -- MEDIUM: all interfaces** |
| 127.0.0.1 | 9050 | (system) | Tor SOCKS proxy -- localhost only |
| 127.0.0.1 | 9002 | python (pid=2888613) | Annotation tool (alt) -- localhost only |
| **0.0.0.0** | **8765** | **(system/docker)** | **PaddleOCR -- HIGH: all interfaces** |
| 127.0.0.1 | 42099 | code-c3a26841a8 (pid=1996919) | VS Code server |
| 127.0.0.1 | 58731 | code (pid=1444817) | VS Code internal |
| 127.0.0.54 | 53 | (system) | DNS resolver |
| 127.0.0.1 | 11414 | code (pid=1847988) | VS Code internal |
| *:22000 | 22000 | syncthing (pid=1641) | SyncThing data -- all interfaces |
| [::]:5900 | 5900 | (system) | VNC IPv6 -- CRITICAL |
| [::]:80 | 80 | (system) | Nginx IPv6 -- CRITICAL |
| [fd7a:...]:57309 | 57309 | (system) | Tailscale IPv6 |
| [::1]:631 | 631 | (system) | CUPS IPv6 -- localhost only |
| *:8384 | 8384 | syncthing (pid=1641) | SyncThing GUI -- CRITICAL: all interfaces |
| [::]:8765 | 8765 | (system/docker) | PaddleOCR IPv6 -- HIGH |
| [::1]:6379 | 6379 | (system) | Redis IPv6 -- localhost only |

**Binding Summary:**
- **0.0.0.0 (all interfaces):** 5900 (VNC), 80 (nginx), 22 (SSH), 9001 (uvicorn), 8765 (PaddleOCR)
- **[::] (IPv6 all interfaces):** 5900, 80, 8765
- **\*:\* (all):** 22000 (SyncThing data), 8384 (SyncThing GUI)
- **127.0.0.1 (localhost):** 5432, 6379, 631, 9050, 9002, plus many VS Code/extension ports
- **100.93.212.44 (Tailscale only):** 34825
- **192.168.122.1 (virbr0):** 53

### System Services (46 running)

| Service | Description |
|---------|-------------|
| accounts-daemon.service | Accounts Service |
| avahi-daemon.service | Avahi mDNS/DNS-SD Stack |
| bluetooth.service | Bluetooth service |
| colord.service | Color Profiles |
| containerd.service | containerd container runtime |
| cron.service | Background program processing |
| cups-browsed.service | CUPS browsed |
| cups.service | CUPS Scheduler |
| dbus.service | D-Bus System Message Bus |
| docker.service | Docker Application Container Engine |
| fail2ban.service | Fail2Ban Service |
| fwupd.service | Firmware update daemon |
| gdm.service | GNOME Display Manager |
| gnome-remote-desktop.service | GNOME Remote Desktop |
| kerneloops.service | Kernel crash signatures |
| ModemManager.service | Modem Manager |
| NetworkManager.service | Network Manager |
| nginx.service | Nginx web server |
| nvidia-persistenced.service | NVIDIA Persistence Daemon |
| polkit.service | Authorization Manager |
| postgresql@16-main.service | PostgreSQL 16 |
| power-profiles-daemon.service | Power Profiles daemon |
| redis-server.service | Redis key-value store |
| rsyslog.service | System Logging |
| rtkit-daemon.service | RealtimeKit Scheduling |
| snap.canonical-livepatch.canonical-livepatchd.service | Canonical Livepatch |
| snapd.service | Snap Daemon |
| ssh.service | OpenSSH server |
| switcheroo-control.service | Switcheroo Control |
| syncthing@rookslog.service | SyncThing for rookslog |
| systemd-journald.service | Journal Service |
| systemd-logind.service | User Login Management |
| systemd-machined.service | VM/Container Registration |
| systemd-oomd.service | OOM Killer |
| systemd-resolved.service | DNS Resolution |
| systemd-timesyncd.service | Time Synchronization |
| systemd-udevd.service | Device Events |
| tailscaled.service | Tailscale node agent |
| tor@default.service | Tor anonymizing network |
| udisks2.service | Disk Manager |
| unattended-upgrades.service | Unattended Upgrades |
| upower.service | Power management |
| user@1000.service | User Manager for UID 1000 |
| virtlockd.service | libvirt locking daemon |
| virtlogd.service | libvirt logging daemon |
| wpa_supplicant.service | WPA supplicant |

**Notable services:**
- **fail2ban** -- running (security positive)
- **tor@default** -- running (explains port 9050 SOCKS proxy)
- **gnome-remote-desktop** -- running (potential VNC source)
- **nginx** -- running but likely unnecessary (default config, no reverse proxy use)
- **virtlockd/virtlogd** -- libvirt daemons running (from virbr0 network)

### User Services (46 running)

Primarily GNOME desktop services (session manager, keyring, settings daemons, IBus, PipeWire audio, tracker-miner, flatpak portals). These are expected for a GNOME desktop session and do not represent issues.

### Docker Containers

| Name | Image | Status | Ports | Created |
|------|-------|--------|-------|---------|
| paddleocr-server | paddleocr-server:latest | Up 7 weeks (healthy) | 0.0.0.0:8765->8765, [::]:8765->8765 | 2026-01-09 |

No stopped containers found. Only 1 container running.

### Cron Jobs (5 entries)

| Schedule | Command | Purpose |
|----------|---------|---------|
| Sun 03:00 | `find /scratch -type f -mtime +7 -delete` | Clean temp files older than 7 days |
| Sun 04:00 | `docker system prune -f --filter until=168h` | Clean Docker artifacts older than 7 days |
| Every 6hr | `df / --output=pcent` check >90% | Root partition space alert |
| Sun 00:00 | `audit-workspace.sh` | Weekly project git status report |
| Sun 00:05 | `audit-home.sh` | Weekly home directory convention check |

All 5 cron entries match CLAUDE.md documentation. Well-maintained.

### Top Memory Consumers

| PID | %MEM | RSS (MB) | Command |
|-----|------|----------|---------|
| 802595 | 3.0% | 956 | VS Code file watcher |
| 1417938 | 2.3% | 753 | Firefox content process |
| 1483528 | 2.3% | 741 | VS Code extension host |
| 1843663 | 2.0% | 664 | claude -r (today, current session) |
| 1903263 | 1.9% | 622 | claude --worktree npm-fix (today) |
| 1856012 | 1.9% | 611 | VS Code extension host |
| 1819084 | 1.7% | 565 | VS Code extension host |
| 2736026 | 1.7% | 565 | claude -r (Jan 18 -- stale) |
| 4024 | 1.6% | 532 | VS Code desktop (main) |
| 1942578 | 1.6% | 529 | claude -r (today) |
| 2580787 | 1.6% | 521 | claude (Jan 09 -- stale) |
| 2901731 | 1.5% | 504 | claude -r (Feb 26) |
| 1802652 | 1.5% | 499 | claude -r (today) |
| 1894629 | 1.4% | 467 | claude -r (today) |
| 1105490 | 1.3% | 440 | claude -r (Feb 11) |
| 1484372 | 1.3% | 434 | VS Code Pylance |
| 1857044 | 1.3% | 426 | VS Code Pylance |
| 3697484 | 1.2% | 394 | claude -r (Mar 01) |
| 1417650 | 1.2% | 384 | Firefox (main) |
| 886344 | 1.1% | 365 | claude -r (2025 -- stale) |
| 749526 | 1.0% | 324 | claude -r (Jan 15 -- stale) |
| 3820271 | 0.8% | 285 | claude -r (Jan 28 -- stale) |

### Process Count by Command (Top 30)

| Count | Command |
|-------|---------|
| 158 | ssh-agent |
| 40 | node |
| 38 | sh |
| 35 | npm |
| 25 | /bin/bash |
| 23 | /usr/share/code/code |
| 18 | vscode-server node |
| 17 | -bash |
| 13 | /proc/self/exe (VS Code utility) |
| 13 | claude |
| 10 | /usr/bin/bash |
| 10 | firefox |
| 9 | tmux |
| 9 | nginx: |
| 6 | mosh-server |
| 5 | /usr/bin/python3 |
| 5 | python3 |
| 5 | postgres: |
| 5 | uv |
| 4 | tailscaled |
| 4 | VS Code python-env-tools |
| 4 | QtWebEngineProcess |
| 4 | bash |
| 3 | node (standalone) |
| 3 | sort |
| 3 | sleep |

## Verification Against Research

| Claim (from research/CLAUDE.md) | Verified? | Actual State | Notes |
|---------------------------------|-----------|--------------|-------|
| 44 listening sockets | YES | 44 TCP listeners confirmed | Exact match with research |
| 19 stale tmux sessions | YES | 19 sessions total, 10 detached/stale | Session count matches; "stale" is more nuanced -- some attached sessions also old |
| Multiple stale Claude/VS Code processes | YES | 13 Claude CLI, 30+ total Claude-related, 23+ VS Code desktop processes | Worse than expected; some Claude instances from 2025 |
| PaddleOCR container healthy | YES | Up 7 weeks, healthy status | Exact match |
| 5 cron entries | YES | 5 entries confirmed | All match CLAUDE.md documentation |
| Docker data-root on / | YES | /var/lib/docker on root partition | ~12GB of Docker data on 55GB root |
| PostgreSQL localhost only | YES | 127.0.0.1:5432 | Correctly bound |
| Redis localhost only | YES | 127.0.0.1:6379 | Correctly bound |
| VNC on 0.0.0.0:5900 | YES | Confirmed | Security finding -- see security-audit.md |
| Uvicorn on 9001 | YES | 0.0.0.0:9001 | CLAUDE.md says "Running" but does not note it's bound to all interfaces |

---

*Audit complete: 2026-03-06T02:30Z*
*No system changes made -- document only*
