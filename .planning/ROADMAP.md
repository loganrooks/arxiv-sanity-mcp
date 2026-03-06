# Roadmap: Dionysus Research Platform

**Created:** 2026-03-05
**Supersedes:** Previous roadmap (2026-02-28, never started)
**Core Value:** A three-node experimental research platform where scholarly tools can be developed, deployed, experimented with, and accessed fluidly.

## Milestone 1: Platform Genesis

Transform Dionysus from a fragmented, unstable workstation into a stable research platform with multi-device access, a knowledge base foundation, and the infrastructure for experimentation — through iterative cycles of diagnosis, research, and implementation.

```
Phase 1 (Audit) → Phase 2 (Research) → Phase 3 (Stabilize) → Phase 4 (Foundation) → Phase 5 (Workflow Research) → Phase 6 (Experiment Infra) → Phase 7 (First Workflow)
 ─── diagnosis ───   ─── research ───   ─── implementation ──────────────────────   ──── research ────   ──── implementation ──────────────────────
```

---

### Phase 1: Deep System Audit

**Goal:** Map the actual state of Dionysus comprehensively. Replace assumptions with verified facts.

**Requirements:** AUD-01 through AUD-08

**Delivers:**
- Complete storage breakdown (all partitions, all directories >1GB)
- Process/service inventory with orphan identification
- Security posture assessment (network bindings, credentials, permissions)
- GPU/CUDA state documentation
- Project ecosystem health check (14+ projects)
- Consolidated system map document

**Key approach:**
- Parallel subagents for independent audit domains (storage, processes, security, GPU, projects, network)
- Produce machine-readable findings that subsequent phases can reference
- Compare findings against synthesis.md and critical-audit.md claims

**Needs sudo:** No (read-only audit)

**Research needed:** None — this is the research

---

### Phase 2: Tool & Strategy Research

**Goal:** Hands-on evaluation of key tools against the actual system. Verify synthesis claims. Produce confirmed-working recommendations.

**Requirements:** RSC-01 through RSC-10

**Delivers:**
- Remote Control tested and documented (or ruled out with reasons)
- Obsidian Headless evaluated with minimal vault
- mosh evaluated for mobile access
- Agent parallelization and context-file patterns extracted from community
- OpenClaw security/utility assessment (likely: skip it)
- Multi-model decision framework (Claude vs Codex vs Gemini)
- Scholarly workflow reference implementations surveyed
- Tool evaluation document with actionable recommendations

**Key approach:**
- Fetch and analyze the 6 external research sources provided at project inception
- Test tools on the actual system, not just read docs
- Subagents for independent research threads
- Cross-reference findings against critical-audit.md verification criteria

**Needs sudo:** Possibly (mosh install)

**Research needed:** This IS the research phase

---

### Phase 3: Critical Stabilization

**Goal:** Fix everything dangerous or broken. The prerequisite for deploying any agent infrastructure.

**Requirements:** SEC-01 through SEC-07, CLN-01 through CLN-07

**Delivers:**
- Zero 0.0.0.0 network bindings (except SSH)
- No plaintext credentials anywhere on disk
- ~/.cache cleaned (potentially recovering 40-60GB)
- Broken kernel packages resolved
- Docker data-root on /data (off root partition)
- /home below 70% utilization
- Orphaned process prevention

**Key risks:**
- Docker data-root migration requires stopping all containers — schedule downtime
- Kernel fix could go wrong — but running kernel (6.14.0) is unaffected
- Cache cleanup needs careful identification of what's safe to remove

**Needs sudo:** Yes — use Codex CLI for privileged operations

**Research needed:** None — informed by Phase 1 findings

---

### Phase 4: Platform Foundation

**Goal:** Multi-device access, knowledge base, and development environment working end-to-end.

**Requirements:** ACC-01 through ACC-05, KNW-01 through KNW-05, DEV-01 through DEV-04

**Delivers:**
- Three-node network topology working: Dionysus ↔ Apollo ↔ Orpheus
- mosh + tmux + Remote Control for seamless device switching
- Obsidian vault syncing across all three devices via Obsidian Sync
- obsidian-mcp giving Claude Code read/write access to the vault
- Vault-root CLAUDE.md encoding philosophical framework and conventions
- Node.js 22, rationalized Python environments, dotfiles in git
- systemd user services ready for deployment

**Key risks:**
- Obsidian Headless is new (v1.0.0) — may have edge cases
- Node 22 upgrade could break TypeScript projects — test before removing old version
- Obsidian Sync requires new subscription ($4-8/month)

**Needs sudo:** Yes (Node install, loginctl linger)

**User decisions during phase:**
- Obsidian vault folder structure (proposed in KNW-01, user approves)
- Which dotfiles to track vs. leave unmanaged

---

### Phase 5: Workflow & Architecture Research

**Goal:** With a stable platform, research how to build scholarly workflows that serve the user's actual practice.

**Requirements:** WRK-01 through WRK-05 (provisional — refined after Phase 4)

**Delivers:**
- Evaluation of hermeneutic workspace architecture against current needs
- Survey of agent patterns for scholarly tasks
- Design document for first end-to-end workflow
- Experiment framework design for retrieval/embedding comparisons
- Skills and CLAUDE.md patterns extracted from reference implementations

**Key approach:**
- Revisit the hermeneutic workspace architecture with fresh eyes and a working platform
- The claude-enhanced deliberation methodology (provisional invariants, interweaving) informs design
- User workshops: walk through actual scholarly tasks and identify automation points

**Needs sudo:** No

**Research needed:** This IS the research phase

---

### Phase 6: Experimentation Infrastructure

**Goal:** GPU tooling, model management, experiment tracking — the environment for running experiments.

**Requirements:** EXP-01 through EXP-05 (provisional — refined after Phase 5)

**Delivers:**
- Verified GPU tooling (CUDA, PyTorch, compatible frameworks)
- /data/models/ with managed model cache
- Experiment tracking system
- Isolated experiment environments
- Documentation for running experiments

**Needs sudo:** Possibly (CUDA toolkit)

**Research needed:** Low — informed by Phase 2 and Phase 5 findings

---

### Phase 7: First Scholarly Workflow

**Goal:** Implement one end-to-end scholarly workflow, use it for real work, and evaluate.

**Requirements:** FLW-01 through FLW-04 (provisional — defined by Phase 5)

**Delivers:**
- One complete, working scholarly workflow
- Real-world usage on an actual task
- Evaluation document: what worked, what didn't, what to change
- Input for Milestone 2 planning

**Needs sudo:** No

**Research needed:** None — this is implementation informed by all prior phases

---

## Success Criteria

The platform is ready for Milestone 2 when:

1. **Stability**: No recurring system fragility issues. Machine enables work instead of fighting it.
2. **Access**: SSH from Apollo → Dionysus → tmux → resume. Remote Control from Orpheus → same session. Disconnect, reconnect, continue.
3. **Knowledge**: Obsidian vault syncing across three devices. Claude Code can read/write notes. Philosophical framework encoded in CLAUDE.md.
4. **Security**: `ss -tlnp | grep 0.0.0.0` returns only SSH. No plaintext credentials.
5. **Storage**: /home below 70%. Docker on /data. Clear separation: /home (code), /data (data), /scratch (temp).
6. **Development**: Modern toolchain (Node 22, rationalized Python). Dotfiles versioned. New projects scaffold cleanly.
7. **Experimentation**: GPU works, experiment tracking exists, can run a fine-tuning or embedding experiment without fighting the environment.
8. **Workflow**: At least one scholarly workflow working end-to-end and evaluated against real use.

---

## Milestone 2: Scholarly Infrastructure (Future)

*Defined after Milestone 1 completes. Scope informed by Phase 7 evaluation.*

Likely directions:
- Advanced scholarly workflows (close reading, research, writing, lecture processing)
- Background automation pipelines (PDF processing, audio transcription, literature discovery)
- Self-improving dialogical system (evolving the claude-enhanced vision)
- Cloud infrastructure evaluation
- Advanced experiment workflows (manifold embeddings, retrieval comparisons, fine-tuning)

---
*Roadmap created: 2026-03-05*
*Methodology: Iterative spiral — phases alternate between diagnosis/research and implementation*
