# Dionysus Platform

## What This Is

A personal scholarly research platform built on the Dionysus workstation (Xeon W-2125, 32GB, GTX 1080 Ti). The platform provides the infrastructure layer — security, service deployment, multi-device integration, data management, and development tooling — that enables building, deploying, and iteratively refining scholarly research tools. It serves one user (Logan Rooks, philosophy PhD) across three devices: Dionysus (server), Apollo (MacBook M4 Air), and Orpheus (iPhone).

## Core Value

A hardened, well-organized workstation where scholarly tools can be developed, deployed, and accessed from any device — and where experimentation with new tools and workflows doesn't create chaos.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

**Security & Hardening**
- [ ] All network services bound to localhost or Tailscale IP only (VNC, nginx, PaddleOCR)
- [ ] Git credential store replaced with secure credential helper (no plaintext tokens on disk)
- [ ] Firewall rules tightened to Tailscale-only for non-SSH services
- [ ] Stale/default services removed or properly configured (nginx default page)

**SSH & Remote Access**
- [ ] SSH config with host aliases, multiplexing, keepalives for all devices
- [ ] SSH agent auto-loads keys on login
- [ ] tmux configured as default session persistence layer (survive disconnects, resume from any device)

**Storage & Environment**
- [ ] Hidden directory audit and cleanup (~100GB in dotfiles: stale caches, orphaned envs, old extensions)
- [ ] Docker data-root migrated off root partition to /data/docker/
- [ ] Broken HWE kernel packages resolved
- [ ] Node.js upgraded to current LTS (v20 or v22)
- [ ] Python package manager strategy rationalized (uv vs pip vs conda overlap)
- [ ] Stale dotfiles and orphaned project configs removed

**Dotfiles & Configuration Management**
- [ ] Dotfiles tracked in git repo with symlink management (stow or similar)
- [ ] Covers: .bashrc, .gitconfig, .tmux.conf, .ssh/config, and key tool configs
- [ ] Restorable from fresh machine

**Multi-Device Integration**
- [ ] SyncThing verified end-to-end between Dionysus ↔ Apollo
- [ ] Apollo configured as shared workstation (local notes/writing + remote dev)
- [ ] Phone workflows supported: audio recording → Dionysus, quick notes, SSH, status checks
- [ ] Session persistence: close laptop, reopen on any device, resume exactly where you were

**Service Deployment Layer**
- [ ] Standard pattern for deploying scholarly tools as persistent services on Dionysus
- [ ] Service management: start, stop, logs, health checks, restart-on-boot
- [ ] Deployment works for both containerized (Docker) and direct (systemd) services
- [ ] Project template or scaffold for new tools that includes deployment config

**Development Environment**
- [ ] Frictionless path from experiment (notebook/script) to deployed service
- [ ] New projects scaffold into ~/workspace/projects/ with standard structure
- [ ] Conda environments rationalized: clear purpose per env, no orphans
- [ ] MCP server integration pattern documented for new tools

**Data & Pipeline Architecture**
- [ ] Directory structure for shared data (recordings, transcripts, notes, processed outputs)
- [ ] File-watch automation for routine pipelines (e.g., recording drops → transcription)
- [ ] Manual trigger path for experimental pipelines
- [ ] Clear separation: raw inputs / processed outputs / working storage
- [ ] Integration-ready for note-taking tools (Obsidian, others) — shared vault or sync pattern

### Out of Scope

- Building individual scholarly tools (scholardoc, lecture processor, reading group tool) — separate GSD projects
- Canvas API integration research — separate feasibility study after platform is stable
- GPU scheduling/partitioning — premature optimization; address when it becomes a bottleneck
- Apollo-side software installation beyond SSH/SyncThing config — keep Mac minimal
- Full disaster recovery / bare-metal restore automation — dotfiles + git + docs covers 90%
- Migrating away from Tailscale — it works, keep it

## Context

**Current state (2026-02-28):**
- Comprehensive home directory cleanup completed 2026-02-27 (48 → 20 top-level items)
- ~100GB hidden directory sprawl: .cache (67GB), .local (18GB), .vscode (11GB), miniconda3 (48GB)
- VNC exposed on 0.0.0.0:5900 with empty .vnc/ (no auth), nginx default on port 80
- No ~/.ssh/config despite remote-first workflow; SSH agent has no loaded keys
- Git credentials stored in plaintext via credential.helper=store
- Node.js 18 (EOL April 2025), npm 9.2.0 (severely outdated)
- 5 conda envs (48GB total), acadlib-dev orphaned; uv (25GB) + pip (5.5GB) caches overlap
- 94 VS Code extensions, ~30 old Claude Code versions accumulating
- 16GB Tor Browser in .local/share/, 30GB HuggingFace models (21 models, many experimental)
- fail2ban active, SSH properly hardened (key-only, AllowUsers), UFW active with DROP default
- SyncThing running but Apollo/LE2127 peers disconnected
- Broken HWE kernel package (6.17.0-14) — partial install
- Docker data-root on root partition (70% full)

**Existing project ecosystem:**
zlibrary-mcp → scholardoc → philo-rag-simple → philograph-mcp (pipeline vision)
Plus: semantic-calibre, audiobookify, PaddleOCR (Docker). All want to be "used regularly."

**User workflow pattern:**
- Split work between Mac (writing, notes, offline) and Dionysus (dev, GPU, long-running)
- Wants to shift more to Dionysus-centric: close laptop, continue from phone, long-running jobs
- Experimental mindset: tries new representations, embeddings, text navigation approaches
- Non-linear writing process: reading/listening → vague idea → explore → tools → write
- All four "chaos" vectors are active concerns: dead projects, data sprawl, config drift, lost context

## Constraints

- **Storage**: /home at 82% (62GB free), root at 70% (16GB free) — must reclaim before adding services
- **Single GPU**: GTX 1080 Ti shared by all ML workloads — no partitioning for now
- **Tailscale-only**: All remote access through Tailscale mesh — no public IP exposure
- **No sudo in Claude Code**: Kernel fix, Docker migration, systemd units need Codex CLI or manual intervention
- **SyncThing paths**: Some folders are SyncThing-managed — destructive ops on those paths risk sync corruption
- **Existing MCP servers**: 7+ configured in ~/.claude.json — changes must not break working integrations

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dotfiles in git + stow | Standard practice, enables restoration, version history | — Pending |
| tmux as session persistence | Already configured, lightweight, works from phone SSH | — Pending |
| Mixed deployment: Docker + systemd | Heavy services containerized, lightweight ones direct — pragmatic | — Pending |
| Both file-watch and manual pipeline triggers | Routine flows auto, experimental flows manual | — Pending |
| Dionysus-centric but Apollo shared | Mac handles offline notes/writing, syncs back; Dionysus is the brain | — Pending |
| Do it right over quick wins | User prefers solid architecture now over patching later | — Pending |

---
*Last updated: 2026-02-28 after project initialization*
