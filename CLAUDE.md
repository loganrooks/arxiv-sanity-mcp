# CLAUDE.md

This file is auto-loaded as runtime context for agents working in this repository under the current Claude Code runtime. It defines project identity, accepted decisions, and routing pointers — not behavioral discipline (see `AGENTS.md`). The bias is toward stability of decisions already made and explicit pointers for decisions that need to be re-checked. For genuinely trivial tasks, use judgment. The current placement of doctrine load-points (§ "Doctrine load-points" below) is current-runtime-shaped; if the runtime or substrate changes, that section's location and shape are reviewable.

## What This Project Is

An MCP-native research discovery substrate inspired by arxiv-sanity. The goal is to help researchers and agents discover, triage, and monitor arXiv papers through MCP tools, resources, and prompts — not a "chat with papers" wrapper.

**Current status:** v0.1 shipped 2026-03-14 (10 phases complete, including 04.1; 13 MCP tools, 4 resources, 3 prompts; current pytest collection ~493 tests). v0.2 (multi-lens substrate) is the active milestone — Phases 12-17. See [STATE.md](.planning/STATE.md) for live state.

## Accepted ADRs (Settled Decisions)

- **ADR-0001 — Exploration-first architecture:** Multiple retrieval and ranking strategies can coexist (capability commitment per `docs/adrs/ADR-0001-exploration-first.md:22`, not a directive that every decision *must* engage multiple strategies); interest state is not reduced to tags; unresolved questions stay documented.
- **ADR-0002 — Metadata-first, lazy enrichment:** Ingest metadata eagerly, enrich lazily, embed selectively.
- **ADR-0003 — License and provenance first:** Track provenance for all content and ranking signals; respect reuse constraints per content type.
- **ADR-0004 — MCP as workflow substrate:** Design MCP layer for agent workflows (collections, saved queries, triage state), not as a thin search wrapper.

## Key Architectural Constraints

- **Do not prematurely commit** to a retrieval family, ranking stack, vector DB, or MCP surface shape (the negation is the point — early commitment is the failure mode).
- **Preferred abstractions:** paper, content variant, interest profile, collection, saved query, watch, triage state, result set, ranking explanation.
- **Treat tags as one signal among several**, not the canonical taste primitive; **treat dense retrieval as one lens among several**, not the default; **the product is discovery and triage**, not paper-chat. (Reframed from earlier negations; the underlying commitments are unchanged.)
- **Implementation bias:** metadata mirror → lexical baseline → workflow state → graph enrichments → selective semantic retrieval.
- **Stack trajectory:** Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). The maximalist Stack D (full local hybrid research platform — see `docs/05-architecture-hypotheses.md:118`) is foreclosed because it commits compute and complexity that v0.x has no evidence to justify; the trajectory remains open if v0.3+ evidence warrants reopening.

## Doctrine load-points

Read the listed document before editing or proposing changes that match the trigger. (Current Claude Code runtime placement; the routing-by-trigger shape itself is durable across runtimes, but specific load-points are reviewable when surfaces change.)

- **Touching ranking, retrieval, or lens-architecture code** → `LONG-ARC.md` (anti-patterns), `docs/adrs/ADR-0001`, `docs/adrs/ADR-0005`.
- **Adding a new abstraction or signal type** → `LONG-ARC.md` (protected seams), `VISION.md` (anti-vision section).
- **Touching MCP tool, resource, or prompt surfaces** → `docs/adrs/ADR-0004`, `LONG-ARC.md` (MCP-native operations).
- **Proposing rights-affecting changes** (license, redistribution, content storage) → `docs/adrs/ADR-0003`.
- **Proposing changes to enrichment cost or scheduling** → `docs/adrs/ADR-0002`.
- **Proposing changes to the spike program structure or methodology** → `.planning/spikes/METHODOLOGY.md`, `LONG-ARC.md` (doctrine-interaction-with-spike-program).

## Status Markers

Use these labels when proposing changes:
- **Settled** — accepted ADR
- **Chosen for now** — pragmatic temporary choice
- **Hypothesis** — promising but unevaluated
- **Open** — intentionally unresolved

## Document Structure

- `AGENTS.md` — Agent behavior rules and working posture
- `docs/01-11` — Numbered design documents (read in order)
- `docs/adrs/` — Architecture Decision Records
- `docs/templates/` — ADR and experiment templates
- `.planning/` — GSD project management (STATE.md, ROADMAP.md, REQUIREMENTS.md, phases/)
- `.planning/foundation-audit/` — Epistemic audit findings and methodology
- `.planning/ECOSYSTEM-COMMENTARY.md` — Cross-project analysis (arxiv-scan ↔ MCP)

When proposing changes: new durable decisions → ADR; new experiments → `docs/08`; new unresolved issues → `docs/10`; new external patterns → `docs/04`.

## Governance Read-Order Map

**New contributor:** `PROJECT.md` → `VISION.md` → `LONG-ARC.md` → `docs/adrs/` (ADRs 0001-0005) → `AGENTS.md` → `.planning/ROADMAP.md` → `.planning/REQUIREMENTS.md` → `.planning/STATE.md`

**Agent starting a session:** This file → `.planning/STATE.md` → relevant phase plan → `AGENTS.md` (if work touches agent-conduct issues)

**Epistemic / methodology questions:** `.planning/spikes/METHODOLOGY.md` (interpretive lenses + practice disciplines) and `.planning/foundation-audit/METHODOLOGY.md` (decision-review epistemic discipline) — see relationship note at top of each file for scope split

**Deliberation history:** `.planning/deliberations/INDEX.md`

## Roadmap Phases

Phase 1 (metadata substrate) → Phase 2 (workflow state) → Phase 3 (interest modeling) → Phase 4 (enrichment adapters) → Phase 04.1 (MCP v1) → Phase 5 (MCP validation) → Phase 6 (content normalization).

Sequencing discipline: shared objects first, workflow state second, enrichments third, MCP surface fourth, validate with real workflows fifth, content last.
