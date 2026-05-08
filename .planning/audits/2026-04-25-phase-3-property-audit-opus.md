---
type: property-audit
status: complete
date: 2026-04-25
scope: Phase 3 (interest modeling) lens-extensibility audit
gates: v0.2 multi-lens roadmap commit (Option A vs B vs C)
provenance:
  reviewer: Explore agent
  model: opus (4.7) — explicit override
  parallel_to: 2026-04-25-phase-3-property-audit-provisional.md (superseded)
---

# Phase 3 Property Audit (Opus rerun) — 2026-04-25

## Verdict summary

| Property | Verdict |
|---|---|
| 1. Profile primitive lens-extensible | extensible |
| 2. MCP tool signatures lens-aware | coupled |
| 3. Storage per-lens abstracted | coupled |

## Property 1 — Profile primitive
**Verdict: extensible.** The `InterestSignal` ORM at `src/arxiv_mcp/db/models.py:366-412` stores `signal_type` as an unconstrained `String(32)` — the original CHECK was deliberately dropped by `alembic/versions/005_drop_signal_type_check.py:23-24` ("allowing new signal types without DB migrations"). Validation lives only in the application-level set `VALID_SIGNAL_TYPES` at `src/arxiv_mcp/interest/signals.py:11`, which is a one-line edit. There is no BERTopic/MiniLM coupling anywhere in `interest/`; scorers in `interest/ranking.py:89-351` operate on `category_list`, `authors_text`, and `submitted_date` only. `RankingPipeline.score_paper` (`interest/ranking.py:415-495`) dispatches via a fixed sequence of scorer calls, but uses `self.weights.get(...)` (`interest/ranking.py:440,447,470,476,482`), so a new SignalType + a new pure-function scorer can be appended without touching existing code paths.

- Already there: open `signal_type` column, JSONB `profile.weights` for per-lens weight overrides (`db/models.py:353`), pure-function scorer pattern, `RankerSnapshot.signal_types_applied` is dynamic (`models/interest.py:130`).
- Missing: scorer registry — pipeline branches in `interest/ranking.py:436-487` are hard-sequenced; new scorers require editing `score_paper`. `signal_value` is `String(256)` (`db/models.py:384`) which holds graph node IDs / tag strings fine but cannot hold prose excerpts as-is.
- Caveat: `ProfileContext` (`interest/ranking.py:52-68`) has named fields `seed_papers`/`followed_authors`/`negative_papers`/`query_slugs` — this *is* shaped around the four current types, so a citation-anchor signal needs a context field too (no migration, but a dataclass + loader edit at `interest/search_augment.py:274-287`).

## Property 2 — MCP tool signatures
**Verdict: coupled.** None of `search_papers`, `browse_recent`, `find_related_papers`, `get_paper` (`mcp/tools/discovery.py:24-186`) accept any `lens=` / `strategy=` parameter — `profile_slug` is the only steering knob and it routes only into `ProfileRankingService` (`mcp/tools/discovery.py:59-70`, `104-111`). The lens choice doesn't "happen" anywhere; it is implicit in the single `ProfileRankingService` over-fetch-and-rerank pipeline at `interest/search_augment.py:165-234`, which always calls a single `RankingPipeline` with one fixed scorer set. `find_related_papers` is the most rigid: it has no `profile_slug` at all and unconditionally delegates to `SearchService.find_related_papers` (`mcp/tools/discovery.py:140-143` → `search/service.py:151-176`), which is hard-wired to `build_related_query`'s tsvector logic.

- Already there: tools take `**kwargs` to a service layer that accepts arbitrary keyword passthrough (`interest/search_augment.py:96-135`); response already carries `RankerSnapshot` so per-lens telemetry has a slot (`models/interest.py:120-138`).
- Missing: tool surface itself. Adding `lens="citation_community"` requires editing every `discovery.py` tool signature plus the dispatch in `ProfileRankingService.search_papers` (currently has no lens branch — only `if profile_slug is None` at `interest/search_augment.py:124`). `find_related_papers` has no profile awareness and would need full retrofit.

## Property 3 — Storage abstraction
**Verdict: coupled.** The `Paper` table indexes (`db/models.py:113-122`) are exclusively GIN-on-tsvector, GIN-on-category_list, and btree-on-dates/category — no pgvector, no embedding column, no edge table, no citation graph table anywhere in `db/models.py`. `PaperEnrichment` (`db/models.py:131-178`) does hold `cited_by_count`, `related_works`, `topics`, `fwci` as JSONB blobs, but a grep of `db/queries.py`, `search/service.py`, `search/ranking.py`, and `interest/ranking.py` returns zero references to those fields — they are write-once metadata, not retrieval-shaped (no index on `cited_by_count`, `related_works` is JSONB rather than a normalized edge table). `db/queries.py:32-237` is exclusively `tsvector @@ tsquery` plus `ts_rank_cd`; `SearchService` directly imports those builders (`search/service.py:16`) and the `(Paper, rank)` row tuple is baked into result shaping at `search/ranking.py:43-49`.

- Already there: `PaperEnrichment` JSONB rows contain the raw signal needed for a citation-co-citation lens; the multi-tier `processing_tier` column (`db/models.py:101-102`, `ProcessingTier.EMBEDDED = 3` at `db/models.py:50`) anticipates embedding lifecycle; `weights` JSONB on profile permits per-lens weight overrides without schema work.
- Missing: any vector index, any normalized citations/edge table, any abstract retrieval interface — `SearchService` is a single concrete class hard-bound to PG-FTS query builders. Result row shape `(Paper, rank)` (`search/ranking.py:43-44`) hard-codes the assumption of one numeric similarity score per paper.

## Implications for Option A/B/C
The evidence is split, not balanced: Property 1 is genuinely extensible (the work to enable a new signal type was already done in migration 005 + the JSONB weights column), but Properties 2 and 3 are coupled in ways no amount of profile-side work can paper over. Option A (full multi-lens, 3-4 mo) is overscoped — the profile primitive doesn't need rewriting. Option C (refactor + 1 lens, 1 mo) under-tests the abstraction: a single-lens "interface" risks shipping shaped exactly to the lens you happen to build, repeating the trap ADR-0001 names. **Option B is the load-bearing choice**: it's the only option that forces the tool surface (Property 2) and storage layer (Property 3) to actually serve two lens shapes — which is the only test that distinguishes "multi-lens substrate" from "renamed single-lens code." Concrete work Option B requires given current state: (a) lens parameter on the four discovery tools + dispatch in `ProfileRankingService`; (b) a scorer registry replacing the hard-sequenced calls in `RankingPipeline.score_paper`; (c) one citations edge table or normalized projection of `PaperEnrichment.related_works` plus a second query builder family parallel to `db/queries.py`; (d) abstract `SearchResult` to carry per-lens score components rather than a single `rank`.

## What I am not telling you
- Ingestion-side coupling not assessed: `enrichment/openalex.py`, `ingestion/`, the OAI-PMH path. A citation lens depends on `related_works` being populated at sufficient coverage, which this audit did not measure.
- MCP resources/prompts surface (`src/arxiv_mcp/mcp/prompts/*`, `mcp/resources/`) not audited — only `tools/discovery.py` and `tools/interest.py` were read. Lens choice may also need to surface as a resource template.
- Test coverage of the abstraction: the 403-test suite was not opened; I cannot say which seams are test-pinned vs. free to refactor. CLI surfaces (`interest/cli.py`, `search/cli.py`) also not audited for parallel coupling.

## Confidence calibration
- Property 1 (extensible): high confidence, cross-confirmed across three independent pieces of evidence — the dropped CHECK constraint (`alembic/versions/005_drop_signal_type_check.py:23-24`), the application-level `VALID_SIGNAL_TYPES` set (`signals.py:11`), and the JSONB `weights` column (`db/models.py:353`). The "partly" caveat about ProfileContext field naming is real but mechanical.
- Property 2 (coupled): high confidence, load-bearing on direct reading of all four tool signatures (`mcp/tools/discovery.py:24,76,117,158`) — no lens parameter anywhere is a complete-evidence claim, not a sampling claim. `find_related_papers` having no `profile_slug` at all is the strongest single signal.
- Property 3 (coupled): high confidence on storage shape (the `Paper.__table_args__` index list at `db/models.py:113-122` is exhaustive); medium confidence on the "write-only metadata" characterization of `PaperEnrichment` — based on a grep showing zero retrieval-side references, which is dispositive for *current* state but doesn't preclude trivial reuse.
