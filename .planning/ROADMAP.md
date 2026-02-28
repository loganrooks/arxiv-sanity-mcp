# Roadmap: Dionysus Platform

**Created:** 2026-02-28
**Core Value:** A hardened workstation where scholarly tools can be developed, deployed, and accessed from any device — without experimentation creating chaos.

## Milestone 1: Platform Foundation (v1)

Transform Dionysus from an ad-hoc collection of processes into a secure, organized, multi-device research platform.

```
Phase 1 (Security) → Phase 2 (Cleanup) → Phase 3 (DevEnv) → Phase 4 (Services) → Phase 5 (Data) → Phase 6 (Multi-Device) → Phase 7 (Knowledge)
```

### Phase 1: Emergency Security Hardening

**Goal:** Eliminate all unauthenticated network exposure. Every service bound to localhost or Tailscale only.

**Requirements:** SEC-01, SEC-02, SEC-03, SEC-04, SEC-05, SEC-06

**Delivers:**
- VNC secured (password + localhost bind)
- nginx default site removed
- All services (PaddleOCR, uvicorn, SyncThing GUI) rebound to 127.0.0.1
- Plaintext git credentials eliminated
- File permissions verified

**Key risks:**
- VNC rebinding may break existing remote desktop workflow → verify Tailscale Serve TCP or SSH tunnel works first
- PaddleOCR Docker container may need rebuild to change bind address

**Needs sudo:** Yes (nginx removal, VNC config, UFW rules)

**Research needed:** None — all steps documented with exact commands in research

---

### Phase 2: Process Cleanup + Space Recovery

**Goal:** Recover ~53GB on /home (82% → ~65%), kill orphaned processes, fix broken system packages.

**Requirements:** CLN-01 through CLN-09

**Delivers:**
- 91 orphaned MCP processes killed, cron cleanup installed
- ~53GB disk space recovered (conda envs, HF models, pip cache, Tor Browser, stale dotfiles)
- Broken HWE kernel packages resolved
- .bashrc cleaned for Phase 3 tracking

**Key risks:**
- Deleting wrong HuggingFace models could break active projects → grep all project code first (research already did this)
- Kernel fix could go wrong → current running kernel (6.14.0) is unaffected, low risk

**Needs sudo:** Yes (kernel fix, potentially some cache dirs)

**User decisions during phase:**
- Review HuggingFace model deletion list before execution
- Confirm Whisper model retention (4.3GB) — depends on audiobookify usage

**Research needed:** None — sizes measured, commands documented

---

### Phase 3: Development Environment Modernization

**Goal:** Modern toolchain, version-controlled configs, reliable remote access from any device.

**Requirements:** DEV-01 through DEV-07

**Delivers:**
- Node.js 22 LTS with all projects verified
- uv as primary Python manager, conda reserved for GPU-only envs
- ~/dotfiles/ git repo managed by GNU Stow
- ~/.ssh/config with Tailscale hosts, multiplexing, keepalives
- tmux session persistence (disconnect/reconnect across devices)

**Key risks:**
- Node 22 could break TypeScript projects (zlibrary-mcp) → test before removing Node 18
- Stow symlink conflicts with existing files → backup originals first

**Needs sudo:** Yes (NodeSource install)

**Research needed:** Low — NodeSource, Stow, SSH config all well-documented standard procedures

---

### Phase 4: Service Infrastructure

**Goal:** Managed service lifecycle for all tools. Systemd user services + Docker Compose as the deployment spine.

**Requirements:** SVC-01 through SVC-07

**Delivers:**
- loginctl linger enabled (services survive SSH disconnect)
- First tool running as systemd user service (PHL410 annotation tool or similar)
- Docker Compose consolidating PaddleOCR + PostgreSQL + Redis
- Docker data-root on /data/docker/ (off root partition)
- Project template with deploy/ directory, .service file, Makefile deploy target
- Port registry at ~/.config/dionysus/

**Key risks:**
- Docker data-root migration requires stopping all containers → schedule downtime
- systemd user services need correct PATH and env → use absolute paths to venv binaries

**Needs sudo:** Yes (loginctl linger, Docker config)

**Research needed:** Low — patterns fully documented in ARCHITECTURE.md. Docker data-root migration may need brief research.

---

### Phase 5: Data Architecture + Pipeline Orchestration

**Goal:** Canonical data directory on /data, first automated pipeline, `just` as the pipeline command runner.

**Requirements:** DAT-01 through DAT-07

**Delivers:**
- /data/scholarly/ directory tree (raw/, processed/, embeddings/, knowledge/, vault/)
- /data/models/ for ML model cache (HuggingFace symlinked)
- `just` installed with pipeline justfile
- First working pipeline: audio → transcription → structured output
- systemd path unit watching inbox directory for new files
- metadata.json convention for all generated outputs

**Key risks:**
- faster-whisper CUDA compatibility with CUDA 11.8 → needs testing
- SyncThing interactions during data migration → pause sync during moves

**Needs sudo:** No (all in user space and /data)

**Research needed:** Medium — pipeline tool integration (faster-whisper, scholardoc) needs testing with actual tools

---

### Phase 6: Network Exposure + Multi-Device Integration

**Goal:** Services accessible from Mac and phone via Tailscale. Phone-to-server audio pipeline working.

**Requirements:** MDV-01 through MDV-05

**Delivers:**
- Tailscale Serve exposing key services with HTTPS on *.ts.net
- SyncThing cleaned up and inbox folder configured
- Phone-to-server relay working (iCloud Drive through Apollo or Mobius Sync)
- Apollo-side SyncThing verified end-to-end

**Key risks:**
- Tailscale Serve persistence across reboots → needs testing
- iCloud relay depends on Apollo being online → Mobius Sync as fallback
- Apollo-side setup requires Mac access

**Needs sudo:** Yes (Tailscale Serve --bg)

**Research needed:** Medium — Tailscale Serve persistence, Apollo-side config, iCloud relay end-to-end validation

---

### Phase 7: Obsidian Integration + Knowledge Layer

**Goal:** Obsidian vault as the human interface to scholarly data. Processed outputs visible as notes. Embedding experimentation framework.

**Requirements:** KNW-01 through KNW-05

**Delivers:**
- Obsidian vault at /data/scholarly/vault/ with structured folders
- Vault syncs to Apollo (sync method decided during this phase)
- Pipeline outputs generate vault notes automatically
- Embedding experimentation: `just embed` / `just embed-promote`
- Essential plugins configured (Dataview, Templater, Pandoc)

**Key risks:**
- Vault size with generated content → monitor and set limits
- Obsidian plugin compatibility → test incrementally
- Sync method decision deferred → evaluate both options

**Needs sudo:** No

**Research needed:** Medium — Obsidian plugin workflow, vault-as-view-layer pattern validation, Zotero integration

---

## Success Criteria

The platform is "done" when:

1. **Security**: `ss -tlnp | grep 0.0.0.0` returns only SSH (port 22) — everything else is localhost or Tailscale IP
2. **Storage**: `/home` utilization below 70%, clear data separation between /home (code), /data (data), /scratch (temp)
3. **Services**: `systemctl --user list-units --type=service` shows managed scholarly tools, auto-restarting on failure
4. **Access**: Close laptop, open phone, `ssh dionysus` → `tmux attach` → resume exactly where you were
5. **Deployment**: New tool goes from code to running service in under 30 minutes using the project template
6. **Pipelines**: Drop an audio file in the inbox → transcription appears in /data/scholarly/processed/ with metadata.json
7. **Knowledge**: Open Obsidian on Mac → see processed outputs as navigable, linked notes

---
*Roadmap created: 2026-02-28*
*Last updated: 2026-02-28 after initial definition*
