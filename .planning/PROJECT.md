# Project: Dionysus Research Platform

**Created:** 2026-03-05
**Supersedes:** Previous "Dionysus Platform" project (2026-02-28, never started)
**Owner:** Logan Rooks — Philosophy PhD, building scholarly research tools

---

## Core Value

A three-node experimental research platform where scholarly tools can be developed, deployed, experimented with, and accessed fluidly — with the infrastructure decisions themselves informed by philosophical-technical inquiry.

## The Problem

Scholarly practice is fragmented across multiple platforms (Claude Projects, Claude Code, Gemini, manual PDF downloads, scattered notes) with no persistent knowledge base, no connected infrastructure, and a server that demands constant firefighting instead of enabling work. Significant design work exists across multiple projects (hermeneutic workspace architecture, claude-enhanced deliberations, scholardoc, synthesis research) but has never been unified or tested against the actual system.

**Primary pain point:** System fragility — caches filling up, services conflicting, processes orphaned, packages broken — time spent fighting the machine instead of doing research.

## The Vision

### Three-Node Network

| Node | Device | Role |
|------|--------|------|
| **Dionysus** | Xeon W-2125, 32GB, GTX 1080 Ti | Compute + storage + always-on services + background processing + experiment runtime |
| **Apollo** | MacBook M4 Air | Primary development + interactive research + Obsidian + VS Code + Claude Code |
| **Orpheus** | iPhone | Capture (notes, audio) + monitoring + Remote Control oversight + quick interactions |

Connected via Tailscale mesh. Each device is a node with a distinct function — not just access points to the server but participants in a research network.

### What the Platform Enables

1. **Scholarly workflows** — Close reading, research, writing, lecture prep, reading groups, film club talks. AI assistance that actually improves reading quality, not just speed.
2. **Tool development** — ScholardDoc, philo-rag, philograph, hermeneutic workspace, and tools not yet conceived.
3. **Frontier experimentation** — Embeddings, retrieval comparisons, fine-tuning, agent architectures, novel semantic approaches (manifold-based, Deleuzian), experimental models. At local scale now, cloud eventually.
4. **Knowledge accumulation** — Obsidian vault as the human interface to a growing, connected knowledge base. Notes, readings, transcripts, writings, cross-textual connections mapping both explicit and implicit relations.
5. **Multi-model AI orchestration** — Claude (Max), ChatGPT (Pro), Gemini used strategically. The choice of which tool for which task is itself a research question.
6. **Parallelized remote workflows** — Multiple agents working simultaneously, background processing, automated pipelines, accessible and monitorable from any device.

### What This Project Is NOT

- Not the individual projects (scholardoc, philo-rag, etc.) — it is the **platform** on which they run
- Not a one-time cleanup — ongoing infrastructure that evolves with use
- Not a fixed architecture to implement — an iterative, research-informed process where later phases are shaped by earlier discoveries
- Not purely technical — infrastructure decisions are informed by philosophical thinking (provisional invariants, interweaving as method, the insufficiency of naive RAG)

## Methodology

### Iterative Spiral, Not Waterfall

Each cycle: **Diagnose → Research → Plan → Implement → Evaluate**

Later phases are deliberately underspecified. They get defined as earlier phases reveal what's needed. The roadmap is a living document refined through use.

### Philosophical-Technical Interweaving

From the claude-enhanced deliberations:
- **PD-002**: Provisional invariants — determinations stable enough to act on, revisable when conditions warrant
- **PD-005**: RAG is insufficient — cannot serve as the sole architecture for a system supporting retroactive reinterpretation
- **PD-006**: Interweaving as method — technical and philosophical work are simultaneous movements, not separate tracks

These inform decisions at every level — from sync tool selection to reading workflow design.

## Existing Assets

| Asset | Location | Status | Role |
|-------|----------|--------|------|
| Synthesis research | `.planning/research/synthesis.md` | Complete (theoretical) | Tool landscape — needs system verification |
| Critical audit | `.planning/research/critical-audit.md` | Complete (theoretical) | Challenges all synthesis claims — verification criteria to test |
| Hermeneutic workspace | `~/workspace/projects/hermeneutic-workspace-plugin/` | Designed, not built | Starting point for scholarly workflows — needs evolution |
| Claude-enhanced deliberations | `~/workspace/projects/claude-enhanced/.serena/memories/` | 4 deliberations + checkpoints | Philosophical foundations for system design |
| ScholardDoc | `~/workspace/projects/scholardoc/` | Active development | Document processing pipeline |
| Philo-RAG | `~/workspace/projects/philo-rag-simple/` | Maintenance | RAG engine — may be rethought per PD-005 |
| PhiloGraph | `~/workspace/projects/philograph-mcp/` | Inactive | Knowledge graph MCP — potential integration |
| Semantic Calibre | `~/workspace/projects/semantic-calibre/` | Active | Calibre fork with semantic library management |

## External Research Sources

To be investigated during early phases:
- Boris Cherny on Claude Code parallel workflows (X thread)
- Claude Code Remote Control docs
- OpenClaw getting started
- Zack Shapiro on domain-expertise-in-context-files (X thread)
- Nav Toor on Cowork context setup (X thread)
- Obsidian Headless sync documentation

## Constraints

| Constraint | Detail |
|-----------|--------|
| Hardware | Xeon W-2125 (4c/8t), 32GB RAM, GTX 1080 Ti (11GB, CUDA 11.8) |
| Root partition | 55G total, 70% used — must stay lean |
| /home | 343G, 82% used — needs cleanup |
| /data | 1.8T, 19% used — primary bulk storage target |
| /scratch | 92G, empty — temp processing |
| Budget | Claude Max + ChatGPT Pro + Gemini + Obsidian Sync (to add) |
| Access | Remote only via Tailscale — never physically at desktop |
| Scale | Local-first; cloud eventually |
| Time | Research time available |
| Sudo | Not available in Claude Code — use Codex CLI or manual for privileged operations |

## Known System Issues

- `~/.cache` 67GB — uninvestigated
- Broken HWE kernel packages (6.17.0-14)
- Docker data-root on root partition
- VNC on 0.0.0.0 without auth
- Nginx default site exposed
- Multiple VS Code server instances accumulating
- SyncThing peers (Apollo, LE2127) disconnected

## Subscriptions & Tools

| Service | Tier | Key Capabilities |
|---------|------|-----------------|
| Claude | Max | Claude Code, Remote Control, headless `-p` mode, subagents, 1M context |
| ChatGPT | Pro | Codex CLI (passwordless sudo on Dionysus), xhigh reasoning |
| Gemini | Access | Research, long-context analysis |
| Obsidian Sync | To add ($4-8/mo) | Three-device vault sync with conflict resolution |

## User Workflows

### Currently Active
- **Reading groups** (multiple) — reading schedules, guides, discussion questions
- **Philosophy film club** — research, 25-30 min philosophical talks, screening selection
- **Coursework** — syllabi, lecture recording/transcription, reading, notes, essays
- **Development** — building scholarly tools (scholardoc, etc.)
- **Research/writing** — essays, exploration, critique, understanding thinkers

### Desired
- AI-assisted close reading with genuine textual engagement (not shallow pretrained-bias analysis)
- Cross-textual, semantically-connected workspace
- Lecture note auto-expansion with context
- Phone capture (notes, audio) → automatic processing and organization
- Background processing of PDFs, audio, research queries
- Ideation scratchpad with rigorous AI-assisted exploration
- Holistic connection mapping across notes, readings, writings, transcripts, code
- Experiment infrastructure for embeddings, retrieval, fine-tuning, agent architectures
- Self-improving, dialogical system informed by philosophical and technical thinkers

### Volume Reality
- Raw material generation is currently **light/sporadic** — aspirational pipeline
- The infrastructure should make it *frictionless* to generate more, not just process existing volume
- Deep interactive sessions are the primary mode; background processing earns its keep later

## Key Decisions

| Decision | Status | Rationale |
|----------|--------|-----------|
| Agentic vision drives infrastructure | **Decided** | Cleanup/hardening serves the agentic future, not the reverse |
| Iterative spiral methodology | **Decided** | Diagnose → research → implement cycles, not waterfall |
| Platform scope (not individual tools) | **Decided** | This project builds the stage, not the performances |
| Multi-model strategy | **Open** | When Claude vs Codex vs Gemini — research question |
| Obsidian as knowledge hub | **Likely** | Headless CLI makes it viable on server; needs evaluation |
| OpenClaw adoption | **Skeptical** | Security concerns from audit; Claude headless may suffice |
| Hermeneutic workspace evolution | **Open** | Good starting point, needs improvement — specifics TBD |
| Cloud infrastructure timeline | **Deferred** | Local-first for now; cloud when local scale is insufficient |

---
*Last updated: 2026-03-05*
