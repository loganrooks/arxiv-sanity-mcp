# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

An MCP-native research discovery substrate inspired by arxiv-sanity. The goal is to help researchers and agents discover, triage, and monitor arXiv papers through MCP tools, resources, and prompts — not a "chat with papers" wrapper.

**Current status:** Phases 1-5 + 04.1 complete. 403 tests passing, CLI operational, MCP server with 10 tools + 4 resources + 3 prompts. Validated with real data (126 imported papers, doc 06 resolved). Phase 6 (Content Normalization) is next.

## Accepted ADRs (Settled Decisions)

- **ADR-0001 — Exploration-first architecture:** Multiple retrieval/ranking strategies must coexist; interest state is not reduced to tags; unresolved questions stay documented.
- **ADR-0002 — Metadata-first, lazy enrichment:** Ingest metadata eagerly, enrich lazily, embed selectively.
- **ADR-0003 — License and provenance first:** Track provenance for all content and ranking signals; respect reuse constraints per content type.
- **ADR-0004 — MCP as workflow substrate:** Design MCP layer for agent workflows (collections, saved queries, triage state), not as a thin search wrapper.

## Key Architectural Constraints

- **Do not prematurely commit** to a retrieval family, ranking stack, vector DB, or MCP surface shape.
- **Preferred abstractions:** paper, content variant, interest profile, collection, saved query, watch, triage state, result set, ranking explanation.
- **Do not** assume tags are the canonical taste representation, dense retrieval is the winner, or "paper chat" is the product.
- **Implementation bias:** metadata mirror → lexical baseline → workflow state → graph enrichments → selective semantic retrieval.
- **Stack trajectory:** Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). Not Stack D.

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

## Roadmap Phases

Phase 1 (metadata substrate) → Phase 2 (workflow state) → Phase 3 (interest modeling) → Phase 4 (enrichment adapters) → Phase 04.1 (MCP v1) → Phase 5 (MCP validation) → Phase 6 (content normalization).

Sequencing discipline: shared objects first, workflow state second, enrichments third, MCP surface fourth, validate with real workflows fifth, content last.
