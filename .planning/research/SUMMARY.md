# Project Research Summary

**Project:** Dionysus Platform -- Scholarly Research Workstation
**Domain:** Personal infrastructure for a philosophy PhD researcher (3-device mesh, pipeline automation, knowledge management)
**Researched:** 2026-02-28
**Confidence:** HIGH (all findings verified against live system state)

---

## Executive Summary

The Dionysus workstation is a powerful but neglected Linux server (Xeon W-2125, 32GB RAM, GTX 1080 Ti) that runs a suite of scholarly research tools -- PDF extraction, OCR, RAG search, Z-Library access, audiobook conversion -- all connected via MCP servers to Claude Code. Four parallel research threads investigated how to transform this from an ad-hoc collection of processes into a reliable, secure, multi-device research platform. The findings converge on a single architectural vision: **systemd as the unifying control plane**, with clear storage tiers, automated pipelines, and secure network access via Tailscale.

The research uncovered two urgent problems that must be fixed before any construction begins. First, **VNC is running as root with no password on 0.0.0.0:5900** -- anyone on the local network can see and control the desktop. Second, **91 orphaned MCP processes are consuming 3.4 GB of RAM** due to a known Claude Code bug (#1935). These are not theoretical risks; they are active on the machine right now. Additionally, nginx is serving its default page on port 80 to all interfaces for no reason, and several services (PaddleOCR, uvicorn) are bound to 0.0.0.0 unnecessarily. A plaintext HuggingFace token sits in `~/.git-credentials`. The security posture must be hardened before exposing anything via Tailscale Serve.

The recommended approach proceeds in three phases: **stabilize** (security, cleanup, space recovery), **build** (systemd services, data architecture, pipeline orchestration with `just`), and **connect** (multi-device integration, Obsidian vault, phone pipeline). This ordering respects hard dependencies -- you cannot safely expose services until the network binding is fixed, you cannot build new infrastructure on a disk at 82% utilization, and you cannot connect devices until the services exist. The total estimated space recovery is ~53 GB on /home (82% down to ~65%), achieved by removing orphaned conda environments, unused HuggingFace models, the pip cache, and optionally Tor Browser. The unified stack is: systemd user services + Docker Compose (isolation-only) + Tailscale Serve (network) + journald (logging) + `just` (pipelines) + GNU Stow (dotfiles) + uv (Python) + Node 22 LTS.

---

## Key Findings

### From Service Deployment Research (STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md)

**Architecture:** Hybrid systemd-user + Docker. systemd handles Python/TS services that need fast restart and filesystem access. Docker handles only services requiring isolation: PaddleOCR (CUDA), PostgreSQL, Redis. Tailscale Serve provides HTTPS reverse proxy to the tailnet. journald handles all logging (500MB cap already configured).

**Core technologies:**
- **systemd user services**: Process lifecycle, auto-restart, boot persistence, journald integration. Already on the system.
- **Docker Compose**: Single compose file for PaddleOCR + PostgreSQL + Redis. Already installed (v2.40.3).
- **Tailscale Serve**: Reverse proxy with auto-HTTPS for `*.ts.net`. No Caddy/nginx needed.
- **uv**: Python package management replacing pip. Already partially in use via `uvx` for MCP servers.
- **Cron cleanup script**: Pragmatic fix for Claude Code MCP orphan leak (bug #1935).

**Table stakes:**
- Auto-restart on crash (systemd `Restart=on-failure`)
- Start on boot (systemd `enable` + `loginctl enable-linger`)
- Remote log access (journalctl over SSH)
- Service status overview (`systemctl --user list-units`)

**Key anti-features (do NOT build):**
- Kubernetes/k3s, Docker Swarm, Grafana/Prometheus, CI/CD pipelines, Ansible
- Do not Dockerize everything -- systemd for Python tools, Docker only for isolation

### From Multi-Device Research (multi-device.md)

**SSH:** Traditional SSH over Tailscale (not Tailscale SSH mode). ControlMaster multiplexing with `%C` hash paths. ForwardAgent for Dionysus only (git push from server). No `~/.ssh/config` exists yet -- must create.

**tmux:** TPM + tmux-resurrect + tmux-continuum for session persistence across reboots. Auto-attach on SSH login (`tmux new-session -A -s dev`). 3-4 named sessions: dev, uni, sys, bg.

**SyncThing:** 8 folders configured, but issues found: `academic-active` nested inside `courses` (double-sync risk), GUI bound to `0.0.0.0:8384` (security), `cleanoutDays: NaN` (bug), default Sync folder unused. Do NOT sync development repos (use git). Add inbox folder for phone recordings and Obsidian vault.

**Phone pipeline:** iCloud Drive relay through Apollo is the most frictionless path. iPhone saves to iCloud, Mac syncs to local FS, SyncThing sends to Dionysus. Mobius Sync (direct SyncThing to phone) is fallback but requires app to be open.

**Obsidian:** Sync ($4/mo) is the right choice for notes. Vault on Dionysus is receive-only via SyncThing for server-side processing. Obsidian is a view layer, NOT the data store. Pipelines write INTO the vault, never read from it.

### From Data Architecture Research (data-architecture.md)

**Directory structure:** Three storage tiers used inconsistently. Canonical scholarly data root at `/data/scholarly/` with clear separation: `raw/` (immutable inputs), `processed/` (generated outputs with metadata.json), `embeddings/` (experiments vs production), `vault/` (Obsidian-accessible layer). Code stays on /home, data on /data, temp processing on /scratch.

**Pipeline orchestration:** `just` (justfile) for command running + systemd path units for file-watch triggers. `just` is lighter than Prefect/Celery, more structured than shell scripts, with built-in `--list` and documentation. systemd path units use kernel inotify -- zero-daemon, integrates with journald.

**Embedding storage:** sqlite-vec for experiments (self-contained .db files, portable, deletable), pgvector for production (concurrent access, SQL joins). FAISS for in-memory notebook exploration. Philo-rag-simple already uses sqlite-vec.

**Obsidian vault design:** At `/data/scholarly/vault/`. User-authored notes alongside pipeline-generated markdown. No symlinks (Obsidian has documented issues). Frontmatter contains absolute paths to data files. Vault syncs to Apollo via SyncThing; large data stays on Dionysus.

**Data lifecycle:** Every generated output directory MUST have `metadata.json` with source, pipeline version, tool, params, and input hash. Weekly audit script flags stale experiments and missing metadata. Experiment embeddings get 90-day review flag. Raw inputs are permanent.

### From Dotfiles/DevEnv/Security Research (dotfiles-devenv-security.md)

**URGENT -- VNC security:** x11vnc running as root, no password, on `0.0.0.0:5900`. Fix: bind to localhost, add password, access via SSH tunnel or Tailscale Serve TCP.

**nginx removal:** Running on `0.0.0.0:80` with only the default site. No service uses it. Remove entirely.

**Git credentials:** Plaintext `store` helper + `.git-credentials` file with HuggingFace token. Remove store helper, delete credentials file, rely on `gh auth git-credential` for GitHub.

**Service binding audit:** VNC (CRITICAL), nginx (HIGH), uvicorn 9001 (MEDIUM), PaddleOCR 8765 (MEDIUM) all on 0.0.0.0. PostgreSQL and Redis correctly on 127.0.0.1.

**GNU Stow for dotfiles:** Simple symlink farm. Track .bashrc, .profile, .gitconfig, .tmux.conf, .ssh/config, .claude/CLAUDE.md. Do NOT track .env, SSH keys, .git-credentials, .claude.json.

**Node.js 22 LTS:** Current Node 18 is EOL (April 2025). Upgrade via NodeSource. Only global package is `@openai/codex`. 30% faster startup vs Node 20.

**Python: conda + uv, kill pip.** Keep conda for exactly 2 envs (ml-dev, audio) that need CUDA/ffmpeg. Use uv for everything else. Remove 3 orphaned conda envs (acadlib-dev, analysis, university) saving ~17 GB. Purge pip cache (5.5 GB).

**Cache cleanup (~53 GB reclaimable on /home):**
- Unreferenced HuggingFace models: ~13.5 GB
- Orphaned conda environments: ~17 GB
- pip cache: 5.5 GB
- Tor Browser (optional): 16 GB
- Thumbnails + misc: ~1 GB

**Broken kernel:** HWE 6.17.0-14 packages in broken state (iU/iF). System runs fine on 6.14.0. Standard dpkg force-remove fix, low risk.

---

## Cross-Domain Dependencies

The four research domains are deeply interconnected. The following dependency chains constrain phase ordering:

1. **Security before networking.** VNC and nginx must be fixed before Tailscale Serve exposes anything. Services must bind to 127.0.0.1 before they are reverse-proxied.

2. **Space recovery before building.** /home at 82% leaves insufficient room for new Node.js install, new conda/uv environments, or expanded project scaffolds. The ~53 GB recovery must happen early.

3. **systemd linger before services.** `loginctl enable-linger` is a one-command prerequisite for all systemd user services. Without it, services die when SSH disconnects.

4. **systemd services before Tailscale Serve.** Nothing to expose until services run reliably on localhost.

5. **systemd services before data pipelines.** The pipeline architecture (systemd path units triggering `just` recipes) depends on the systemd user service infrastructure being in place.

6. **Directory structure before pipelines.** Pipelines write to `/data/scholarly/processed/` and `/data/scholarly/embeddings/`. The canonical directory tree must exist first.

7. **SSH config before tmux plugins.** tmux session persistence matters most when SSH connections are reliable. SSH config with ControlMaster and keepalives should come first.

8. **Dotfiles cleanup before Stow.** .bashrc has duplicate aliases, dead paths, and stale entries. Clean it before capturing it in version control.

9. **Node upgrade before MCP server testing.** MCP servers run on Node. Upgrade first, then verify they work.

---

## Conflicts and Tensions

The research recommendations are largely compatible, but a few tensions exist:

1. **`just` vs Makefile.** The service deployment research uses Makefiles in the project template (ARCHITECTURE-project-template.md), while the data architecture research recommends `just` for pipeline orchestration. **Resolution:** Use both. Makefile for per-project dev/deploy commands (standard, expected by developers). `just` for cross-project pipeline orchestration at `~/scripts/pipelines/justfile`. They serve different scopes.

2. **Obsidian vault location.** Data architecture puts it at `/data/scholarly/vault/`. Multi-device research discusses it at `~/workspace/notes/obsidian-vault/`. **Resolution:** Use `/data/scholarly/vault/` as the canonical location (data belongs on /data, not /home). Create a symlink from workspace for convenience. The multi-device research's SyncThing path should point to the /data location.

3. **SyncThing GUI binding.** Multi-device research notes it should be `127.0.0.1:8384` or Tailscale IP only. Security research confirms the 0.0.0.0 binding is a problem. **Resolution:** Bind to `127.0.0.1:8384`, access via SSH tunnel. This is consistent with the "bind to localhost, use Tailscale for remote" pattern.

4. **File-watch: inotifywait vs systemd path units.** Multi-device research mentions `inotifywait` for the inbox watcher. Data architecture recommends systemd path units. **Resolution:** Use systemd path units. They are zero-daemon, integrate with journald, auto-restart on failure, and are already the recommended service management approach. inotifywait is the worse choice here -- it requires a running process with no built-in lifecycle management.

5. **Phone pipeline dependency on Apollo.** The iCloud relay approach requires the Mac to be running. This is a real constraint. **Resolution:** Accept the limitation for v1. Mobius Sync is the fallback for when Apollo is off. Document both paths.

---

## Decisions the User Must Make

These cannot be resolved by research alone:

1. **Obsidian Sync ($4/mo) or SyncThing relay?** Sync is clearly better for notes (content-level conflict resolution, native iOS). The question is whether $48/year is worth it. Recommendation: yes, for a PhD student whose workflow is note-centric.

2. **Remove Tor Browser (16 GB)?** Only the user knows if Tor access is needed for research. If occasionally needed, install the lightweight `tor` package instead of the full browser.

3. **Whisper model retention (4.3 GB)?** Depends on whether audiobookify is still actively used or just "Maintenance" status means it might be used again.

4. **Conda env `analysis` and `university` deletion (~16 GB)?** The .bashrc aliases pointing to these envs reference dead paths. Likely orphaned, but the user should verify no notebooks or scripts depend on them before deletion.

5. **HuggingFace model cleanup (~13.5 GB)?** The audit identified models not referenced by any git-tracked project. But notebooks, scratch scripts, or future experiments might reference them. The user should review the list before bulk deletion.

6. **Docker data-root migration timing.** Moving `/var/lib/docker/` to `/data/docker/` is a known TODO. It could happen during the space recovery phase or be deferred. It requires restarting Docker and potentially rebuilding images. Recommendation: do it during space recovery while we are already doing disruptive cleanup.

---

## Implications for Roadmap

Based on combined research across all 4 domains, the work organizes into 7 phases across 3 stages.

### Stage 1: Stabilize (Security + Cleanup)

#### Phase 1: Emergency Security Hardening
**Rationale:** The VNC exposure is an active attack surface. Nothing else matters until network security is sound.
**Delivers:** All services bound to localhost or Tailscale only. No unauthenticated network services.
**Tasks:**
- Fix VNC: bind to localhost, add password, or disable entirely
- Remove nginx (default page on 0.0.0.0:80, nothing uses it)
- Bind uvicorn (9001) and PaddleOCR (8765) to 127.0.0.1
- Fix SyncThing GUI binding (0.0.0.0:8384 to 127.0.0.1:8384)
- Remove plaintext git credential store, delete .git-credentials
- File permissions audit (~/.env, ~/.ssh/)
**Avoids:** Pitfall 3 (0.0.0.0 binding), Pitfall 4 (Docker iptables bypass)
**Research needed:** None -- all steps are documented with exact commands

#### Phase 2: Process Cleanup + Space Recovery
**Rationale:** 91 orphaned MCP processes waste 3.4 GB RAM. /home at 82% blocks new installs. Must clear the decks before building.
**Delivers:** ~53 GB recovered on /home (82% to ~65%). MCP leak stopped. Broken kernel fixed.
**Tasks:**
- Kill 91 orphaned MCP processes immediately
- Install cron-based MCP cleanup script (every 30 minutes)
- Remove orphaned conda envs (acadlib-dev + user-verified: analysis, university) -- ~17 GB
- Remove unreferenced HuggingFace models (user-verified) -- ~13.5 GB
- Purge pip cache -- 5.5 GB
- Prune uv cache -- 1-5 GB
- Remove Tor Browser if approved -- 16 GB
- Clear desktop thumbnails -- 0.5 GB
- Fix broken HWE kernel packages (dpkg force-remove)
- Clean .bashrc (dead aliases, duplicate PATHs, stale references)
- Remove stale dotdirs (.acadlib/, .gphoto/, .philosophy_tools/, .streamlit/, .copilot/)
**Avoids:** Pitfall 1 (MCP accumulation), Pitfall 7 (Docker data-root on root partition -- flag for later), Pitfall 9 (uv cache accumulation)
**Research needed:** None -- sizes measured, commands documented. User decisions required for Tor, conda envs, HF models.

### Stage 2: Build (Infrastructure + Pipelines)

#### Phase 3: Development Environment Modernization
**Rationale:** Node 18 is EOL. pip is redundant with uv. Dotfiles are untracked. Must modernize the toolchain before deploying services that depend on it.
**Delivers:** Node 22 LTS, uv-first Python workflow, version-controlled dotfiles, SSH config, tmux persistence.
**Tasks:**
- Upgrade Node.js 18 to 22 LTS via NodeSource
- Verify MCP servers and TypeScript projects work on Node 22
- Establish uv as primary Python manager (update project configs)
- Install GNU Stow, create ~/dotfiles/ with packages (shell, git, tmux, ssh, claude)
- Clean .bashrc before tracking (already done in Phase 2)
- Create ~/.ssh/config with Tailscale hosts, ControlMaster, keepalives
- Install TPM + tmux-resurrect + tmux-continuum
- Add tmux auto-attach to .bashrc for SSH sessions
**Avoids:** Pitfall 5 (systemd PATH issues -- absolute paths established here)
**Research needed:** LOW -- Node upgrade is standard, Stow is well-documented. SSH config details are fully specified in multi-device research.

#### Phase 4: Service Infrastructure
**Rationale:** With security fixed, space recovered, and toolchain modernized, the systemd + Docker foundation can be built. This is the spine of the platform.
**Delivers:** Managed service lifecycle for all tools. MCP cleanup automated. Docker services consolidated.
**Tasks:**
- Enable `loginctl enable-linger` (one command, unlocks everything)
- Create `~/.config/systemd/user/` directory structure
- Create `~/.config/dionysus/` for env files and port registry
- Migrate PHL410 annotation tool (port 9001) to systemd user service -- validates the pattern
- Create Docker Compose file consolidating PaddleOCR + PostgreSQL + Redis
- Migrate Docker data-root to /data/docker/ (if decided in Phase 2)
- Create project template scaffold (deploy/ directory with .service file, Makefile with deploy target)
- Add health check endpoints to existing services
**Avoids:** Pitfall 2 (linger not enabled), Pitfall 6 (Python buffered output -- PYTHONUNBUFFERED=1 in all service files), Pitfall 5 (PATH issues -- absolute paths to venv binaries)
**Research needed:** LOW -- patterns are fully documented in ARCHITECTURE.md and ARCHITECTURE-project-template.md. Docker data-root migration may need brief research.

#### Phase 5: Data Architecture + Pipeline Orchestration
**Rationale:** With services running, the data layer can be built. Directory structure must exist before pipelines can write to it.
**Delivers:** Canonical scholarly data directory on /data. First automated pipeline. `just` orchestration.
**Tasks:**
- Create `/data/scholarly/` directory tree (raw/, processed/, embeddings/, knowledge/, vault/)
- Create `/data/models/` and move HuggingFace cache (symlink back to ~/.cache/huggingface)
- Migrate existing data (university recordings, transcripts) to new structure
- Remove empty /data placeholders (corpora/, embeddings/, experiments/, datasets/)
- Create convenience symlink: /home/rookslog/workspace/data -> /data/scholarly
- Install `just`, create ~/scripts/pipelines/justfile
- Create first pipeline: audio transcription (transcribe recipe)
- Create systemd path unit for incoming audio (file-watch trigger)
- Create metadata.json template and convention docs
- Create weekly audit-scholarly-data.sh script
**Avoids:** Data sprawl (metadata.json convention prevents mystery directories)
**Research needed:** MEDIUM -- the justfile recipes reference faster-whisper and scholardoc, which need testing with actual tools. The directory structure is well-specified but migration of existing data needs care (SyncThing interactions).

### Stage 3: Connect (Multi-Device + Knowledge)

#### Phase 6: Network Exposure + Multi-Device
**Rationale:** Services exist and are secured. Now expose them to the tailnet and set up multi-device workflows.
**Delivers:** HTTPS access to services from Mac and phone. Phone-to-server audio pipeline.
**Tasks:**
- Configure Tailscale Serve for key services (scholardoc, PaddleOCR, any web UIs)
- Set up SyncThing inbox folder for phone-to-server file relay
- Configure iCloud Drive relay through Apollo (or Mobius Sync fallback)
- Clean up SyncThing (remove default folder, fix academic-active/courses overlap, fix cleanoutDays: NaN)
- Add .stignore files to all SyncThing folders
- Test end-to-end: record on phone -> iCloud -> Apollo -> SyncThing -> Dionysus -> transcription
**Avoids:** Pitfall 3 (services already bound to localhost from Phase 1), Pitfall 8 (Tailscale Serve sudo -- configure once with --bg)
**Research needed:** MEDIUM -- Tailscale Serve persistence across reboots needs testing. iCloud relay pipeline needs end-to-end validation. Apollo-side SyncThing setup is not fully specified.

#### Phase 7: Obsidian Integration + Knowledge Layer
**Rationale:** The vault depends on the data architecture (Phase 5) and multi-device sync (Phase 6) being in place. This is the capstone that makes processed data accessible for research.
**Delivers:** Obsidian vault as the human interface to the scholarly data layer. Processed outputs visible as notes.
**Tasks:**
- Create Obsidian vault at /data/scholarly/vault/ with recommended structure
- Set up Obsidian Sync (or SyncThing relay) for Mac and phone
- Configure Dionysus SyncThing folder for vault as receive-only
- Create vault note templates with frontmatter linking to data paths
- Create generate-vault-note.py to produce notes from processed outputs
- Install essential plugins (Dataview, Zotero Integration, Templater, Pandoc)
- Create embedding experimentation framework (just embed, just embed-promote)
- Migrate philo-rag-simple's index to /data/scholarly/embeddings/production/
**Research needed:** MEDIUM -- Obsidian's handling of pipeline-generated content needs testing. Zotero integration workflow needs validation. Vault size and SyncThing interaction need monitoring.

---

### Phase Ordering Rationale

```
Phase 1 (Security) -------> Phase 2 (Cleanup) -------> Phase 3 (DevEnv)
                                                              |
                                                              v
Phase 7 (Obsidian) <---- Phase 6 (Network) <---- Phase 5 (Data) <---- Phase 4 (Services)
```

- **Security is non-negotiable as Phase 1.** VNC with no password on 0.0.0.0 is an active vulnerability.
- **Cleanup before building** because you cannot install Node 22 or create new envs on a disk at 82%.
- **DevEnv before services** because service files reference Node and Python toolchains -- get those right first.
- **Services before data pipelines** because pipelines are triggered by systemd path units that depend on the systemd infrastructure.
- **Data architecture before Obsidian** because the vault writes into the directory structure built in Phase 5.
- **Network before Obsidian** because the vault syncs to Apollo via SyncThing (configured in Phase 6).

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 5 (Data Architecture):** Faster-whisper integration, scholardoc pipeline specifics, SyncThing migration interactions
- **Phase 6 (Network + Multi-Device):** Tailscale Serve reboot persistence, Apollo-side SyncThing configuration, iCloud relay setup
- **Phase 7 (Obsidian):** Plugin configuration, Zotero workflow, vault-as-view-layer pattern validation

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Security):** All fixes documented with exact commands
- **Phase 2 (Cleanup):** Space recovery is straightforward deletion with user confirmation
- **Phase 3 (DevEnv):** NodeSource, Stow, SSH config are all well-documented standard procedures
- **Phase 4 (Services):** systemd user services are thoroughly documented in ARCHITECTURE.md and the project template

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Security hardening | HIGH | All vulnerabilities confirmed via ss/ps/file inspection on live system |
| Space recovery | HIGH | All sizes measured via du -sh, model usage verified via grep |
| Service deployment | HIGH | systemd + Docker well-documented, verified on this exact system |
| Data architecture | HIGH for structure, MEDIUM for pipelines | Directory patterns sound; pipeline recipes need testing with actual tools |
| Multi-device | HIGH for SSH/tmux, MEDIUM for phone pipeline | SSH/tmux are established; iCloud relay needs end-to-end validation |
| Dotfiles/DevEnv | HIGH | Stow, NodeSource, uv are all standard, well-documented approaches |
| Obsidian integration | MEDIUM | Architecture is sound; symlink issues documented; vault-as-view-layer untested |

**Overall confidence:** HIGH -- research is grounded in direct system observation, official documentation, and established patterns. The MEDIUM-confidence areas (Obsidian, phone pipeline) are later phases with time to validate.

### Gaps to Address

- **Tailscale Serve persistence across reboots:** Does `--bg` survive Tailscale daemon restarts? Needs testing.
- **scholardoc OCR pipeline GPU access:** May need Docker for CUDA even though we prefer systemd. Needs investigation.
- **Apollo-side setup:** SyncThing folders, iCloud relay configuration, Obsidian installation -- all need Mac-side work not fully specified.
- **Docker data-root migration procedure:** Referenced as TODO but not fully researched. Standard procedure but needs coordination with running containers.
- **Conda env usage verification:** `analysis` and `university` envs assumed orphaned. User must verify.
- **Claude Code MCP + systemd interaction:** MCP servers use stdio, not network ports. They cannot be managed by systemd. The cleanup script is a workaround, not a fix.
- **Obsidian vault sizing:** How large the vault becomes with generated content, and whether SyncThing handles it well, is unknown until tested.

---

## Sources

### Primary (HIGH confidence)
- systemd user services: https://wiki.archlinux.org/title/Systemd/User
- systemd path units: https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html
- Docker Compose: https://docs.docker.com/compose/
- Tailscale Serve: https://tailscale.com/kb/1242/tailscale-serve
- OpenSSH ssh_config: https://man.openbsd.org/ssh_config
- Node.js release schedule: https://endoflife.date/nodejs
- NodeSource installation: https://nodesource.com/blog/Update-Node.js-versions-on-linux
- uv documentation: https://docs.astral.sh/uv/
- GNU Stow: https://www.gnu.org/software/stow/
- just task runner: https://github.com/casey/just
- sqlite-vec: https://github.com/asg017/sqlite-vec

### Secondary (MEDIUM confidence)
- Claude Code MCP bug #1935: https://github.com/anthropics/claude-code/issues/1935
- tmux-resurrect: https://github.com/tmux-plugins/tmux-resurrect
- tmux-continuum: https://github.com/tmux-plugins/tmux-continuum
- Obsidian Sync: https://obsidian.md/sync
- SyncThing .stignore: https://docs.syncthing.net/users/ignoring.html
- Mobius Sync FAQ: https://mobiussync.com/faq/

### Tertiary (LOW confidence -- needs validation)
- Obsidian symlink handling (community reports, not official docs)
- Tailscale Serve TCP for VNC (documented but untested on this system)
- iCloud Drive relay pattern (community practice, no official guide)

---
*Research completed: 2026-02-28*
*Ready for roadmap: yes*
