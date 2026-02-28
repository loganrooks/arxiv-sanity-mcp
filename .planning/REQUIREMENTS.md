# Requirements: Dionysus Platform

**Defined:** 2026-02-28
**Core Value:** A hardened workstation where scholarly tools can be developed, deployed, and accessed from any device — without experimentation creating chaos.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Security

- [ ] **SEC-01**: All network services bound to 127.0.0.1 or Tailscale IP only (no 0.0.0.0 bindings)
- [ ] **SEC-02**: VNC secured with password and bound to localhost (accessed via SSH tunnel or Tailscale)
- [ ] **SEC-03**: nginx default site removed (no service uses it)
- [ ] **SEC-04**: Git credential.helper=store removed; plaintext .git-credentials deleted; gh auth is sole credential source
- [ ] **SEC-05**: SyncThing GUI bound to 127.0.0.1:8384 (not 0.0.0.0)
- [ ] **SEC-06**: Sensitive files (.env, SSH keys) verified at 600 permissions

### Cleanup

- [ ] **CLN-01**: Orphaned MCP processes killed and cron-based cleanup installed (every 30 min)
- [ ] **CLN-02**: Orphaned conda environments removed (acadlib-dev, analysis, university — ~17GB)
- [ ] **CLN-03**: Unreferenced HuggingFace models removed (~13.5GB, user-verified list)
- [ ] **CLN-04**: pip cache purged (~5.5GB)
- [ ] **CLN-05**: Tor Browser removed (~16GB)
- [ ] **CLN-06**: Stale dotfiles/dirs removed (.acadlib, .gphoto, .philosophy_tools, .streamlit, backup files)
- [ ] **CLN-07**: Broken HWE kernel packages (6.17.0-14) resolved
- [ ] **CLN-08**: .bashrc cleaned (dead aliases, duplicate PATHs, stale references)
- [ ] **CLN-09**: /home utilization reduced from 82% to ~65% or below

### Development Environment

- [ ] **DEV-01**: Node.js upgraded to v22 LTS via NodeSource
- [ ] **DEV-02**: All MCP servers and TypeScript projects verified working on Node 22
- [ ] **DEV-03**: uv established as primary Python package manager; pip cache cleared; conda reserved for GPU/system-dep envs only
- [ ] **DEV-04**: Dotfiles tracked in git repo with GNU Stow (.bashrc, .gitconfig, .tmux.conf, .ssh/config, .claude/CLAUDE.md)
- [ ] **DEV-05**: SSH config created with Tailscale host aliases, ControlMaster multiplexing, keepalives
- [ ] **DEV-06**: tmux plugins installed (TPM, resurrect, continuum) with auto-attach on SSH login
- [ ] **DEV-07**: Session persistence works: disconnect SSH, reconnect from different device, resume tmux session

### Service Infrastructure

- [ ] **SVC-01**: loginctl linger enabled for rookslog (user services persist beyond SSH)
- [ ] **SVC-02**: systemd user service directory structure created (~/.config/systemd/user/)
- [ ] **SVC-03**: At least one existing tool migrated to systemd user service (validates pattern)
- [ ] **SVC-04**: Docker Compose file consolidating PaddleOCR + PostgreSQL + Redis
- [ ] **SVC-05**: Docker data-root migrated to /data/docker/ (off root partition)
- [ ] **SVC-06**: Project template/scaffold exists for deploying new tools as services
- [ ] **SVC-07**: Port registry and environment config at ~/.config/dionysus/

### Data Architecture

- [ ] **DAT-01**: Canonical scholarly data directory at /data/scholarly/ with raw/, processed/, embeddings/, knowledge/, vault/ subdirs
- [ ] **DAT-02**: HuggingFace model cache relocated to /data/models/ (symlinked from ~/.cache/huggingface)
- [ ] **DAT-03**: Existing scattered data consolidated into new structure
- [ ] **DAT-04**: `just` installed with pipeline justfile at ~/scripts/pipelines/
- [ ] **DAT-05**: First automated pipeline working: audio file → transcription → structured output
- [ ] **DAT-06**: systemd path unit triggers pipeline on new file arrival in inbox directory
- [ ] **DAT-07**: metadata.json convention established for all generated outputs

### Multi-Device

- [ ] **MDV-01**: SyncThing cleaned up (default folder removed, academic-active/courses overlap fixed, cleanoutDays NaN fixed)
- [ ] **MDV-02**: SyncThing inbox folder created for phone-to-server file relay
- [ ] **MDV-03**: Tailscale Serve configured for key services (HTTPS on *.ts.net)
- [ ] **MDV-04**: End-to-end test: record audio on phone → arrives on Dionysus → transcription runs
- [ ] **MDV-05**: Apollo-side SyncThing verified and inbox relay configured

### Knowledge Layer

- [ ] **KNW-01**: Obsidian vault created at /data/scholarly/vault/ with standard structure
- [ ] **KNW-02**: Vault syncs to Apollo (method TBD: Obsidian Sync or SyncThing)
- [ ] **KNW-03**: Pipeline-generated outputs appear as notes in vault (generate-vault-note tooling)
- [ ] **KNW-04**: Embedding experimentation framework: `just embed` creates isolated experiment, `just embed-promote` moves to production
- [ ] **KNW-05**: Essential Obsidian plugins installed (Dataview, Templater, Pandoc export)

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Canvas Integration

- **CAN-01**: Canvas API feasibility study completed
- **CAN-02**: Course materials auto-sync from Canvas to data directory
- **CAN-03**: Assignment deadlines integrated with note-taking workflow

### Advanced Pipelines

- **PIP-01**: Lecture recording → multi-format output (transcript, summary, connected readings, questions)
- **PIP-02**: Handwritten note scanning → OCR → structured integration
- **PIP-03**: Reading group workflow automation (reading paths, session notes, passage tracking)
- **PIP-04**: Writing project agents (automated close readings, thesis exploration, resource gathering)

### GPU Management

- **GPU-01**: Queue-based GPU scheduling for concurrent ML workloads
- **GPU-02**: Resource monitoring and allocation visibility

## Out of Scope

| Feature | Reason |
|---------|--------|
| Building individual scholarly tools | Separate GSD projects (scholardoc, lecture processor, etc.) |
| Kubernetes / container orchestration | Single-user, single-machine — systemd is sufficient |
| Grafana / Prometheus monitoring | Overkill for personal workstation; journald + scripts suffice |
| CI/CD pipelines | No deployment targets beyond local machine |
| Ansible / configuration management | Single machine; dotfiles + scripts cover this |
| Migrating away from Tailscale | Works well, no reason to change |
| Apollo-side software beyond SSH/SyncThing/Obsidian | Keep Mac minimal, Dionysus is the brain |
| Bare-metal disaster recovery automation | Dotfiles repo + git + documented setup covers 90% |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SEC-01 | Phase 1 | Pending |
| SEC-02 | Phase 1 | Pending |
| SEC-03 | Phase 1 | Pending |
| SEC-04 | Phase 1 | Pending |
| SEC-05 | Phase 1 | Pending |
| SEC-06 | Phase 1 | Pending |
| CLN-01 | Phase 2 | Pending |
| CLN-02 | Phase 2 | Pending |
| CLN-03 | Phase 2 | Pending |
| CLN-04 | Phase 2 | Pending |
| CLN-05 | Phase 2 | Pending |
| CLN-06 | Phase 2 | Pending |
| CLN-07 | Phase 2 | Pending |
| CLN-08 | Phase 2 | Pending |
| CLN-09 | Phase 2 | Pending |
| DEV-01 | Phase 3 | Pending |
| DEV-02 | Phase 3 | Pending |
| DEV-03 | Phase 3 | Pending |
| DEV-04 | Phase 3 | Pending |
| DEV-05 | Phase 3 | Pending |
| DEV-06 | Phase 3 | Pending |
| DEV-07 | Phase 3 | Pending |
| SVC-01 | Phase 4 | Pending |
| SVC-02 | Phase 4 | Pending |
| SVC-03 | Phase 4 | Pending |
| SVC-04 | Phase 4 | Pending |
| SVC-05 | Phase 4 | Pending |
| SVC-06 | Phase 4 | Pending |
| SVC-07 | Phase 4 | Pending |
| DAT-01 | Phase 5 | Pending |
| DAT-02 | Phase 5 | Pending |
| DAT-03 | Phase 5 | Pending |
| DAT-04 | Phase 5 | Pending |
| DAT-05 | Phase 5 | Pending |
| DAT-06 | Phase 5 | Pending |
| DAT-07 | Phase 5 | Pending |
| MDV-01 | Phase 6 | Pending |
| MDV-02 | Phase 6 | Pending |
| MDV-03 | Phase 6 | Pending |
| MDV-04 | Phase 6 | Pending |
| MDV-05 | Phase 6 | Pending |
| KNW-01 | Phase 7 | Pending |
| KNW-02 | Phase 7 | Pending |
| KNW-03 | Phase 7 | Pending |
| KNW-04 | Phase 7 | Pending |
| KNW-05 | Phase 7 | Pending |

**Coverage:**
- v1 requirements: 45 total
- Mapped to phases: 45
- Unmapped: 0

---
*Requirements defined: 2026-02-28*
*Last updated: 2026-02-28 after initial definition*
