# ADR-0005 — Multi-lens substrate for v0.2

**Status:** Accepted
**Date:** 2026-04-25
**Supersedes:** Implicit single-lens trajectory of the 005-008 spike program

## Context

ADR-0001 commits the project to exploration-first architecture: "multiple retrieval and ranking strategies can coexist" as a binding posture. From v0.1 onward, the spike program (005-008) drifted toward a tournament-narrowing frame ("which embedding model wins") that quietly violated this commitment — a drift made visible only by the 2026-04-25 paired-review and the multi-lens redirection deliberation. ADR-0001's coexistence claim had been treated as design aspiration rather than implementation requirement.

A Property audit of the Phase 3 (interest modeling) implementation, run at Opus 4.7 with explicit model override, produced these verdicts:

- **Profile primitive: extensible.** `signal_type` is unconstrained at the DB level (alembic migration 005 dropped the CHECK; validation lives only in `signals.py:11`). No BERTopic/MiniLM coupling in `interest/`. JSONB `weights` column on `interest_profiles` already accommodates per-lens weight overrides without schema work.
- **MCP tool signatures: coupled.** No `lens=` / `strategy=` parameter on any of the four discovery tools. `find_related_papers` has no profile awareness at all. `ProfileRankingService._load_profile_context` hardcodes which signals to load.
- **Storage: coupled.** Indexes are exclusively tsvector + GIN on `category_list`. No vector index, no normalized citation edge table. `PaperEnrichment.related_works` exists as JSONB but is never read by retrieval — write-once metadata, not retrieval-shaped.

(Audit at `.planning/audits/2026-04-25-phase-3-property-audit-opus.md`.)

The deliberation enumerated three roadmap options. Option A (full multi-lens substrate, 3-4 mo) is overscoped given Property 1's verdict — the profile primitive doesn't need rewriting. Option C (refactor + 1 lens, ~1 mo) under-tests the abstraction: a single-lens "interface" risks shipping shaped exactly to the lens you happen to build, repeating the trap ADR-0001 names. Only a second lens forces the tool surface (Property 2) and storage layer (Property 3) to actually serve two lens shapes.

## Decision

v0.2 ships a **multi-lens MCP substrate** with at least two lenses:

1. **Existing semantic lens** — the current TF-IDF + lexical + workflow-state stack, formalized as a registered lens with explicit per-lens scoring.
2. **Citation/community lens** — new lens deriving recommendations from citation graph traversal and co-citation neighborhoods. Highest-leverage AI-specific addition the spike program had neglected.

The substrate commits to:

- **`Lens` interface** — registered implementations producing `query(seed_or_profile, options) → ranked_results_with_provenance`. Plugin or module-level registry.
- **`lens=` parameter** on the four discovery MCP tools (`search_papers`, `browse_recent`, `find_related_papers`, `get_paper`). When `lens=` is omitted, behavior is single-lens semantic, preserving v0.1 response shape for backward compatibility. This default is a backward-compat decision flagged for sunset review after Phase 17 pilot signals are interpreted (LPILOT-03 milestone gate). "All available" was considered as a UX-richer default and deferred — `v0.1` callers expect single-lens response shape.

  Multi-value `lens=` (a list of lens names) without an explicit `mode=` parameter returns a per-lens result *dict* keyed by lens name: `{"semantic": [...results...], "citation_community": [...results...]}`. This is *not* fusion. Callers requesting fusion must pass `mode="fusion"` explicitly; callers requesting intersection or disagreement use Phase 16's dedicated operations. The per-lens-dict default honors ADR-0001's coexistence commitment at the API contract layer and the LONG-ARC anti-pattern against silent fusion-by-default (`LONG-ARC.md:46`, `:48`).
- **`ProfileRankingService` becomes a lens dispatcher** rather than a single hardcoded pipeline. `_load_profile_context` is generalized to dispatch by lens name.
- **Bundle-of-signals profile primitive** — BERTopic-derived signals coexist with citation-anchor, behavior-derived, and curated-prose signals via the existing open `signal_type` column. No primitive rewrite. Per-lens scorers added to `RankingPipeline` via a registry replacing the hard-sequenced calls in `score_paper`.
- **Citations storage** — either a normalized projection of `PaperEnrichment.related_works` into a queryable edges table, or a denormalization layer. To be decided in the v0.2 plan; it must be retrieval-shaped, not write-once metadata.
- **`SearchResult` shape generalized** — carries per-lens score components and per-lens explanations, not a single `rank`.
- **Lens disagreement and intersection as MCP-exposed operations** — not just fusion. Steering, set intersection, lens-disagreement-as-signal, per-paper explanation are first-class. Fusion (RRF as default if used) is one strategy among several, not the implicit default.

Cost target: ~2 months of engineering + spike work. The 005-008 spike chain is reshaped, not abandoned: tournament narrowing is parked; the semantic-lens spike work continues but as lens-design, not as winner-pick.

## Consequences

### Positive
- ADR-0001 honored at the implementation layer, not only at the design layer.
- Lens abstraction validated by a second implementation, reducing the risk of shipping a single-lens "interface" subtly shaped around the lens that happens to ship.
- The bundle-of-signals primitive opens the door to behavior-derived, citation-anchor-derived, and researcher-curated signals as future additions without breaking changes.
- `008`'s "function-in-use tournament" frame dissolves; the v0.2 architecture is no longer hostage to which embedding model wins.

### Negative
- v0.2 ships later than a single-lens refactor would (Option C's ~1 mo vs ~2 mo). This is the cost of validating the abstraction by use rather than by design.
- Citations storage adds operational surface (graph data integration; freshness; coverage). OpenAlex via `PaperEnrichment` is the candidate source, but coverage characterisation is outstanding.
- Storage-layer changes (citation edges, generalized result shape) cross more of the codebase than the profile-primitive work, so refactor blast-radius is moderate rather than minimal.

## Notes

This ADR commits the architectural shape but not the detailed phase plan. The v0.2 plan (separate artifact, GSD-style breakdown) covers task ordering, citation source choice (Semantic Scholar vs OpenAlex; depth; freshness), `SearchResult` migration strategy, the scorer registry shape, the lens-disagreement MCP surface design, and any required revision to phase ordering (e.g., whether Phase 6 content normalization should be pulled forward to support citation lens).

What this ADR explicitly does *not* commit:

- **Which third lens** comes after citation/community (methodological vs benchmark/dataset vs author/affiliation).
- **Fusion strategy** beyond "fusion is one option among steering / disagreement / intersection / explanation; RRF preferred if fusion is used."
- **Methodological-lens taxonomy** (curated vs classifier; what method-tags exist).
- **Profile-elicitation alternatives** (behavior-derived, citation-anchor-derived, curated-prose) — value high, timing open.
- **`008`'s fate.** Reshape as longitudinal pilot using multi-lens, shelve, or run for partial signal. Pending vision document.

The decision rests on the Opus property audit (verified against migration 005 by direct read). A first audit by a default Explore agent reached "Property 1 = coupled" by missing migration 005's drop of the CHECK constraint; that audit is preserved as `.planning/audits/2026-04-25-phase-3-property-audit-provisional.md` (status: superseded) and is not the basis for this decision.
