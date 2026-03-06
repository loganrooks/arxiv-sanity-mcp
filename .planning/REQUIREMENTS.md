# Requirements: Dionysus Research Platform

**Defined:** 2026-03-05
**Supersedes:** Previous requirements (2026-02-28)
**Methodology:** Iterative spiral — early requirements are diagnostic and research-oriented; implementation requirements are informed by findings and refined as phases complete.

---

## Phase 1: Deep System Audit

**Goal:** Comprehensive understanding of the actual system state, not assumptions from prior sessions.

- [x] **AUD-01**: Storage audit — all partitions, all directories >1GB, with usage breakdown. Includes the uninvestigated ~/.cache (67GB), .local, .vscode, miniconda3, and any other large consumers.
- [x] **AUD-02**: Process and service inventory — all running processes, listening ports, systemd services (system and user), Docker containers, cron jobs. Identify orphans, conflicts, and resource waste.
- [x] **AUD-03**: Security posture assessment — all network bindings (0.0.0.0 vs localhost vs Tailscale), credential storage locations, file permissions on sensitive files, firewall rules, SSH configuration.
- [x] **AUD-04**: GPU and CUDA assessment — driver version, CUDA toolkit state, installed ML frameworks, what's currently using the GPU, whether CUDA 11.8 is limiting.
- [x] **AUD-05**: Project ecosystem state — for each project in ~/workspace/projects/, assess: git status, last commit date, active dependencies, running services, disk footprint.
- [x] **AUD-06**: Network and access assessment — Tailscale status, SyncThing state (connected peers, sync status, folder health), SSH configuration, existing tmux/screen sessions.
- [x] **AUD-07**: Installed toolchain inventory — Node.js version(s), Python version(s) and environments, package managers (npm, pip, uv, conda), their caches and overlap.
- [ ] **AUD-08**: Produce consolidated system map document at `.planning/research/system-audit.md`

**Deliverable:** A living system map that becomes the ground truth for all subsequent phases.

---

## Phase 2: Tool & Strategy Research

**Goal:** Hands-on evaluation of key tools and approaches against the actual system. Verify and challenge the synthesis research claims.

- [ ] **RSC-01**: Test Claude Code Remote Control — verify it works on this system (headless Ubuntu 24.04, tmux, Tailscale chain). Document setup steps, failure modes, reconnection behavior.
- [ ] **RSC-02**: Evaluate Obsidian Headless — install, test sync, measure resource usage. Verify the `OBSIDIAN_AUTH_TOKEN` D-Bus bypass. Test with a minimal vault before committing.
- [ ] **RSC-03**: Evaluate mosh — install, test from Apollo and Orpheus equivalents, compare to raw SSH for session resilience.
- [ ] **RSC-04**: Research agent parallelization patterns — fetch and analyze Boris Cherny's workflow (parallel Claude instances, subagent patterns, verification loops). Assess what's applicable to our setup.
- [ ] **RSC-05**: Research domain-expertise-in-context-files pattern — fetch and analyze Zack Shapiro and Nav Toor threads. Extract applicable patterns for scholarly CLAUDE.md and context files.
- [ ] **RSC-06**: Evaluate OpenClaw — assess security posture (audit findings: 341 malicious skills, CVE, plaintext credentials) vs. utility. Determine if Claude Code headless + cron/systemd fully replaces its use cases.
- [ ] **RSC-07**: Survey scholarly workflow implementations — examine claude-scholar (40+ skills), pedrohcgs/claude-code-my-workflow, and other reference implementations. Extract reusable patterns.
- [ ] **RSC-08**: Evaluate multi-model orchestration — when Claude vs Codex CLI vs Gemini? What tasks suit which model? Document decision framework.
- [ ] **RSC-09**: Research experiment tracking approaches — MLflow, Weights & Biases, simple filesystem-based tracking. What's appropriate at our scale?
- [ ] **RSC-10**: Produce research findings document at `.planning/research/tool-evaluation.md` with recommendations that inform Phases 3-4.

**Deliverable:** Verified, system-tested recommendations for the tool stack — not theoretical preferences but confirmed-working approaches.

---

## Phase 3: Critical Stabilization

**Goal:** Fix everything that's actively dangerous or broken. Informed by Phase 1 audit findings.

### Security (blocking — must complete before deploying agents)
- [ ] **SEC-01**: All network services bound to 127.0.0.1 or Tailscale IP only (no 0.0.0.0 bindings)
- [ ] **SEC-02**: VNC secured (password + localhost bind) or removed if unused
- [ ] **SEC-03**: Nginx default site removed
- [ ] **SEC-04**: Git credential.helper=store removed; plaintext .git-credentials deleted; gh auth as sole credential source
- [ ] **SEC-05**: SyncThing GUI bound to 127.0.0.1:8384
- [ ] **SEC-06**: Sensitive files (.env, SSH keys) verified at 600 permissions
- [ ] **SEC-07**: UFW rules reviewed and tightened per audit findings

### System Health
- [ ] **CLN-01**: ~/.cache investigated and cleaned (67GB — identify what's safe to remove)
- [ ] **CLN-02**: Broken HWE kernel packages (6.17.0-14) resolved
- [ ] **CLN-03**: Docker data-root migrated to /data/docker/ (off root partition)
- [ ] **CLN-04**: Orphaned conda environments removed (audit-verified list)
- [ ] **CLN-05**: Stale caches cleaned (pip, uv, npm — audit-verified sizes)
- [ ] **CLN-06**: /home utilization reduced to ~65% or below
- [ ] **CLN-07**: Orphaned processes killed and prevention mechanism installed

**Requires sudo** — use Codex CLI or manual intervention.

---

## Phase 4: Platform Foundation

**Goal:** Multi-device access, knowledge base, and development environment — the stable base on which everything else runs.

### Multi-Device Access
- [ ] **ACC-01**: mosh installed and configured (if Phase 2 evaluation is positive)
- [ ] **ACC-02**: tmux configured with session persistence, plugins (resurrect, continuum)
- [ ] **ACC-03**: SSH config with Tailscale host aliases, ControlMaster multiplexing, keepalives
- [ ] **ACC-04**: Remote Control verified end-to-end: Dionysus → tmux → Claude Code → phone/browser
- [ ] **ACC-05**: Session persistence verified: disconnect from Apollo, reconnect from Orpheus, resume work

### Knowledge Base
- [ ] **KNW-01**: Obsidian vault architecture designed (folder structure, naming conventions, frontmatter schema)
- [ ] **KNW-02**: Obsidian Headless running as systemd user service with `loginctl enable-linger`
- [ ] **KNW-03**: Obsidian Sync configured for three-device mesh (Dionysus, Apollo, Orpheus)
- [ ] **KNW-04**: obsidian-mcp server connected to Claude Code (read, write, search vault)
- [ ] **KNW-05**: Vault-root CLAUDE.md written with philosophical framework, citation conventions, domain terminology

### Development Environment
- [ ] **DEV-01**: Node.js upgraded to v22 LTS; all MCP servers and TS projects verified
- [ ] **DEV-02**: Python environment strategy implemented (uv primary, conda for GPU-only)
- [ ] **DEV-03**: Dotfiles tracked in git repo with GNU Stow
- [ ] **DEV-04**: loginctl linger enabled; systemd user service directory prepared

**Requires sudo** for some items — use Codex CLI.

---

## Phase 5: Workflow & Architecture Research

**Goal:** With a stable platform, research how to build scholarly workflows. Evaluate existing approaches, design the first end-to-end workflow.

*Requirements for this phase will be defined after Phases 1-4 complete, informed by findings.*

Provisional scope:
- [ ] **WRK-01**: Evaluate hermeneutic workspace architecture against current needs — what to keep, what to evolve
- [ ] **WRK-02**: Design first end-to-end scholarly workflow (likely close reading or lecture processing)
- [ ] **WRK-03**: Research agent architecture for scholarly tasks (specialized readers, connection finders, etc.)
- [ ] **WRK-04**: Design experiment framework for retrieval/embedding comparisons
- [ ] **WRK-05**: Evaluate CLAUDE.md and skills patterns from claude-scholar and other reference implementations

---

## Phase 6: Experimentation Infrastructure

**Goal:** Set up the environment for running experiments — GPU tooling, model management, experiment tracking, notebook/script infrastructure.

*Requirements will be defined after Phase 5 research.*

Provisional scope:
- [ ] **EXP-01**: GPU tooling verified and documented (CUDA, PyTorch, frameworks)
- [ ] **EXP-02**: Model management — /data/models/ with HuggingFace symlink, cache policy
- [ ] **EXP-03**: Experiment tracking system deployed (method TBD from Phase 2 research)
- [ ] **EXP-04**: Notebook/script infrastructure for running experiments
- [ ] **EXP-05**: Environment isolation for experiments (separate from production tools)

---

## Phase 7: First Scholarly Workflow

**Goal:** Implement one end-to-end workflow, use it for real work, evaluate, iterate.

*Requirements will be defined after Phase 5-6.*

Provisional scope:
- [ ] **FLW-01**: One complete workflow implemented and tested
- [ ] **FLW-02**: Workflow used on a real task (reading group prep, film talk, lecture processing)
- [ ] **FLW-03**: Evaluation document produced — what worked, what didn't, what to change
- [ ] **FLW-04**: Roadmap for Milestone 2 informed by evaluation

---

## Out of Scope (This Milestone)

| Feature | Reason |
|---------|--------|
| Building individual scholarly tools | Separate projects (scholardoc, etc.) |
| Kubernetes / container orchestration | Single-user, single-machine |
| Full monitoring stack (Grafana/Prometheus) | Overkill; journald + scripts suffice |
| CI/CD pipelines | No deployment targets beyond local machine |
| Cloud infrastructure | Deferred to future milestone |
| Advanced pipeline automation | Depends on workflow research (Phase 5) |
| Canvas API integration | Deferred to Milestone 2 |

---

## Traceability

| Phase | Requirements | Focus |
|-------|-------------|-------|
| 1 | AUD-01 through AUD-08 | Diagnosis |
| 2 | RSC-01 through RSC-10 | Research |
| 3 | SEC-01–07, CLN-01–07 | Stabilization |
| 4 | ACC-01–05, KNW-01–05, DEV-01–04 | Foundation |
| 5 | WRK-01–05 (provisional) | Research |
| 6 | EXP-01–05 (provisional) | Experimentation |
| 7 | FLW-01–04 (provisional) | Implementation + Evaluation |

**Coverage:** 48 requirements (34 defined, 14 provisional)

---
*Requirements defined: 2026-03-05*
*Methodology note: Phases 5-7 requirements are provisional and will be refined after earlier phases complete.*
