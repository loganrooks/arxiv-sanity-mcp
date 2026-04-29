---
gsd_state_version: 1.0
milestone: v0.2
milestone_name: multi-lens-substrate
status: planning
post_milestone_state: v0.2-active-planning
stopped_at: v1-GSD premise-bleed audit-spec arc revised-for-dispatch + awaiting Logan final-call before Step-1 cross-vendor codex auditor dispatch. SYNTHESIS-COMPARISON.md draft-complete remains the upstream artifact; audit feeds incubation-checkpoint disposition on it. Audit-spec arc: Claude drafted v1 (`.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md`); Logan commissioned cross-vendor GPT-5.5 xhigh review (`AUDIT-SPEC-REVIEW.md`; disposition revise-before-dispatch; 7 findings); Claude analyzed transparently then Claude-disposed per Logan authorization (`.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` §3 + §5 + §6); Logan post-disposition refinements F1 (manual-escalation discretion) + F4 (lookup mechanics + meta-discipline) + F6 (soft-cap-with-overflow + META-SYNTHESIS §2 typed-vocab cite + META-SYNTHESIS §3 prohibited-articulations integration) confirmed. Load-bearing decisions distilled to `DECISION-SPACE.md §1.17` (7-rule audit methodology). AUDIT-SPEC.md v2 revised (~30-50% rewrite). Audit shape: Step-1 cross-vendor codex GPT-5.5 high baseline; Step-2 same-vendor adversarial-auditor-xhigh stress + differential analysis fires by default on Class C return OR by Logan manual-escalation discretion. Hybrid grounding: prior-audit (META-SYNTHESIS / GATE-2 / Wave 2) primary + soft-cap ~5 source-reads with overflow protocol fallback. Negative-space check required. Vetted-replacement vocabulary lookup with citations. Non-binding disposition signal output shape. Next concrete step: Logan final-call review on AUDIT-SPEC.md v2 + DECISION-SPACE.md §1.17 + deliberation log §5; if approved, Step-1 cross-vendor codex auditor dispatch; FINDINGS.md feeds Logan disposition on SYNTHESIS-COMPARISON.md (commit-as-is / commit-with-addendum / revise-before-commit).
last_updated: "2026-04-29T01:30:00Z"
last_activity: 2026-04-28 — v1-GSD premise-bleed audit-spec arc landed. Logan registered premise-correction concern (v1-GSD mental-model bleed potentially under-weighting gsd-2 runtime-application surfaces); Claude drafted AUDIT-SPEC.md v1 + audit folder; Logan commissioned cross-vendor (GPT-5.5 xhigh) review at AUDIT-SPEC-REVIEW.md (7 findings; revise-before-dispatch); Claude rendered analysis transparent + per-finding adjudication trace at `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md`; Logan authorized Claude to write the disposition; load-bearing decisions distilled to DECISION-SPACE.md §1.17. Logan post-disposition follow-ups confirmed F1 (manual-escalation), F4 (lookup mechanics + meta-discipline), F6 (soft-cap-with-overflow universalization concern + META-SYNTHESIS verification → typed-vocab + prohibited-articulations integration). AUDIT-SPEC.md v2 revised across §2 (lens vocabulary) + §3 (vendor) + §4 (scope + grounding) + §5 (method + negative-space) + §6 (output rename + per-option justification) + §10 (read budget + conditional add-ons). All artifacts cross-referenced internally. Methodological observation: this review is itself an instance of cross-vendor catching what same-vendor missed (per deliberation log §4.4); refines M1 register-vs-substance asymmetry observation from SYNTHESIS-COMPARISON.md §4.1.
progress:
  total_phases: 11
  completed_phases: 11
  total_plans: 31
  completed_plans: 31
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-08)

**Core value:** Researchers and agents can discover, monitor, and triage arXiv papers through explicit, steerable interest modeling with inspectable results.
**Current focus:** v0.2 (multi-lens substrate) is the active milestone. Phases 12-17 are planned; implementation begins after gsd-2 uplift evaluation (see LONG-ARC.md and handoff). v0.1 is complete and frozen.

## Current Position

Milestone: `v0.2` active (planning phase)
Implementation roadmap: Phases 12-17 authored; on hold pending gsd-2 uplift first-wave exploration + incubation checkpoint (see INITIATIVE.md §5 + DECISION-SPACE.md §2.3)
Status: W1 complete; W2 complete; W3 complete (paired-synthesis); SYNTHESIS-COMPARISON.md draft-complete (full §0-§6 landed in-session-collaborative per D5a). Post-comparison: v1-GSD premise-bleed audit-spec arc revised-for-dispatch (post-cross-vendor-review). AUDIT-SPEC.md v2 (`.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md`) implements DECISION-SPACE.md §1.17 7-rule methodology + Logan post-disposition refinements (F1 manual-escalation; F4 lookup mechanics + meta-discipline; F6 soft-cap-with-overflow + META-SYNTHESIS integration). Two-step conditional vendor (Step-1 cross-vendor codex baseline; Step-2 same-vendor adversarial-auditor-xhigh stress on Class C trigger or manual-escalation). Awaiting Logan final-call before Step-1 dispatch; FINDINGS.md feeds incubation-checkpoint disposition on SYNTHESIS-COMPARISON.md.
Active work: AUDIT-SPEC.md v2 revised-for-dispatch; pause for Logan final-call review on three artifacts: (1) AUDIT-SPEC.md v2 (~30-50% rewrite from v1; §2 vetted-replacement vocabulary lookup + META-SYNTHESIS §3 prohibited-articulations; §3 two-step conditional with manual-escalation discretion; §4 hybrid grounding with soft-cap-with-overflow; §5 negative-space check required; §6 non-binding disposition signal + per-option justification); (2) DECISION-SPACE.md §1.17 (load-bearing audit-methodology decision; 7 rules; ~140 lines); (3) deliberation log `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (§3 Claude transparent analysis; §5 per-finding adjudication trace with rationale + where-Logan-might-differ; §6 revision-action table). Post-final-call sequence: dispatch Step-1 cross-vendor codex auditor → receive FINDINGS.md → Logan dispositions commit-as-is / commit-with-addendum / revise-before-commit on SYNTHESIS-COMPARISON.md → execute disposition → record DISPOSITION.md → §2.1 + §5 incubation adjudication on (possibly revised) SYNTHESIS-COMPARISON.md.
Deferred items log: see `.planning/deliberations/2026-04-28-framing-widening.md §9` for the 17-item current state of deferred work (probes / methodology / audits / synthesis-stage / roadmap items). STATE.md "Pending todos" below lists project-level items outside the gsd-2 uplift initiative.
Last implementation activity: 2026-03-14 -- Phase 10 Plan 03 complete. 3 critical fixes (B-01, F-05, F-07), README corrected, friction report finalized with all 15 items resolved.

Progress: [██████████] 100% (31/31 plans) — v0.1 historical; v0.2 plans not yet tracked here

## v0.1 Historical Metrics

*These metrics are for the completed v0.1 milestone (Phases 1-10, shipped 2026-03-14). v0.2 velocity will be tracked separately once Phase 12 implementation begins.*

**Velocity:**
- Total v0.1 plans completed: 31 (phases 1-10 including Phase 04.1)
  - *Note: velocity table below shows 23 — that figure covers Phases 01-04 only (the phases with per-plan timing data). Plans 05-10 were tracked but not included in the avg/plan table. 31 is the correct total-plans-completed.*
- Average duration (Phases 01-04): 12.6 min
- Total execution time (Phases 01-04): 5.0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-metadata-substrate | 3 | 25 min | 8.3 min |
| 02-workflow-state | 3 | 21 min | 7.0 min |
| 03-interest-modeling-ranking | 3 | 23 min | 7.7 min |
| 04-enrichment-adapters | 2/2 | 16 min | 8.0 min |

| 04.1-MCP v1 | 3/3 | 19 min | 6.3 min |
| 05-MCP Validation | 3/3 | 39 min | 13.0 min |
| 06-Content Normalization | 4/4 | 130 min | 32.5 min |

**Recent Trend:**
- Last 5 plans: 06-02 (54 min), 06-03 (18 min), 06-04 (51 min), 07-01 (17 min), 07-02 (18 min)
- Trend: Consistent execution. All phases complete.

*Updated after each plan completion*
| Phase 06 P01 | 7 | 2 tasks | 10 files |
| Phase 06 P02 | 54 | 2 tasks | 7 files |
| Phase 06 P03 | 18 | 2 tasks | 9 files |
| Phase 06 P04 | 51 | 1 task | 3 files |
| Phase 07 P01 | 17 | 1 tasks | 5 files |
| Phase 07 P02 | 18 | 1 tasks | 3 files |
| Phase 08 P01 | 51 | 2 tasks | 11 files |
| Phase 08 P02 | 2 | 1 tasks | 0 files |
| Phase 09 P01 | 17 | 2 tasks | 45 files |
| Phase 09 P02 | 2 | 1 tasks | 1 files |
| Phase 09 P03 | 46 | 3 tasks | 4 files |
| Phase 10 P01 | 1 | 2 tasks | 1 files |
| Phase 10 P02 | 30 | 1 tasks | 3 files |
| Phase 10 P03 | 5 | 2 tasks | 4 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap: 6-phase structure derived from 47 requirements. Metadata substrate first, MCP surface last.
- Roadmap: Interest Modeling & Ranking grouped together (INTR + RANK) since interest profiles feed ranking explanations.
- Roadmap: Semantic search (SEMA) deferred to v2 per REQUIREMENTS.md.
- 01-01: Function-scoped async engine fixtures to avoid asyncpg event loop conflicts.
- 01-01: Hand-wrote Alembic migration 001 (not autogenerated) per research pitfall 5.
- 01-01: Created arxiv_mcp DB user with password auth for application connections.
- 01-02: arXivRaw as primary harvest format; JSON checkpoint file for incremental state.
- 01-02: ON CONFLICT upsert preserves processing_tier, promotion_reason, source, fetched_at.
- 01-02: python-dateutil added for arXiv RFC 2822 date format parsing.
- 01-03: Used websearch_to_tsquery for boolean search (supports AND/OR natural syntax).
- 01-03: Used plainto_tsquery with 'simple' config for author names (avoids stemming proper nouns).
- 01-03: Combined title AND + abstract OR tsquery for related papers (balanced precision/recall).
- 01-03: Browse recent uses max(date) subquery instead of current_date for deterministic tests.
- 01-03: Keyset cursor uses rank expression not label (PostgreSQL cannot reference SELECT aliases in WHERE).
- [Phase 01]: 01-02: arXivRaw as primary harvest format; JSON checkpoint file for incremental state
- [Phase 02]: 02-01: All 5 workflow ORM models in single db/models.py (shared Base, string forward references)
- [Phase 02]: 02-01: TriageState uses VARCHAR + CHECK constraint (not native ENUM) for migration simplicity
- [Phase 02]: 02-01: SavedQuery params as JSONB for schema-free evolution; watch columns on same table
- [Phase 02]: 02-02: CollectionPaperView as Pydantic BaseModel for PaginatedResponse generic compatibility
- [Phase 02]: 02-02: Query-based batch triage uses build_search_query with large page_size; processes in 500-paper chunks
- [Phase 02]: 02-03: Checkpoint+1 delta: check_watch uses checkpoint_date + 1 day as date_from for strictly-newer results
- [Phase 02]: 02-03: Post-process enrichment: WorkflowSearchService wraps SearchService with 2-query batch (no Phase 1 modification)
- [Phase 02]: 02-03: Last-write-wins for triage import conflict resolution; skip for collections/saved queries
- [Phase 02]: 02-03: Lazy workflow CLI import via try/except for forward compatibility
- [Phase 03]: 03-01: Single InterestSignal table with signal_type discriminator (not per-type tables) for uniform querying
- [Phase 03]: 03-01: Saved query signals use warn-not-error for non-existent queries (resilient to deleted queries)
- [Phase 03]: 03-01: Author name normalization via lowercase + whitespace collapse (exact match, not fuzzy)
- [Phase 03]: 03-01: Application-level duplicate check before DB constraint for descriptive error messages
- [Phase 03]: 03-02: Ranking types (SignalType, SignalScore, etc.) as Pydantic models in models/interest.py to break circular imports
- [Phase 03]: 03-02: Over-fetch multiplier of 3x for re-ranking compensation (page_size * 3 from base service)
- [Phase 03]: 03-02: Negative demotion uses multiplicative factor (1 - weight) on weighted_scores, never removes results
- [Phase 03]: 03-03: Suggestion threshold 3+ papers for author frequency, run_count >= 3 for query suggestions
- [Phase 03]: 03-03: All signal statuses (active/pending/dismissed) excluded from suggestion generation
- [Phase 03]: 03-03: CLI signal IDs use type:value format for confirm/dismiss (e.g., seed_paper:2301.00001)
- [Phase 03]: 03-03: Profile-ranked search displays inline per-result ranking explanations (not table format)
- [Phase 03]: 03-02: ProfileSearchResponse in interest/search_augment.py (not models/) to avoid circular import chain
- [Phase 04]: 04-01: respx mock fixture using context manager with base_url (not decorator pattern)
- [Phase 04]: 04-01: TopicInfo and ExternalIds strip URL prefixes via field_validator (short-form storage)
- [Phase 04]: 04-01: EnrichmentResult status via field completeness heuristic (SUCCESS if cited_by_count + fwci/topics)
- [Phase 04]: 04-01: RateLimiter uses time.monotonic + asyncio.sleep (simple, sufficient for 5 req/s)
- [Phase 04]: 04-02: pg_insert ON CONFLICT for enrichment upsert: full overwrite on success, status-only update on error
- [Phase 04]: 04-02: Paper.doi only set if currently null (never overwrite existing DOI)
- [Phase 04]: 04-02: Per-paper session scope in batch enrichment for partial failure resilience
- [Phase 04]: 04-02: MockAdapter pattern for service tests (implements protocol, predetermined results)
- [Phase quick-1]: Application-level validation for signal types instead of DB CHECK constraint (extensible without migration)
- [Phase quick-1]: Composite PK (arxiv_id, source_api) for multi-source enrichment records
- [Phase quick-1]: Direct ID matching only for negative demotion per ADR-0001 (no category inference)
- [Phase quick-1]: openalex_email setting for OpenAlex polite pool access
- [Phase 04.1]: 04.1-01: Category Jaccard removed from score_seed_relation (author-only) and score_profile_match (85% author + 15% query_boost)
- [Phase 04.1]: 04.1-01: 'seen' triage state uses existing mark_triage upsert path (no new service method)
- [Phase 04.1]: 04.1-01: Docstring assertion test pattern for documentation regression prevention
- [Phase 04.1]: 04.1-02: AppContext dataclass with all 7 services + engine/session_factory/settings for FastMCP lifespan DI
- [Phase 04.1]: 04.1-02: Tools return dict via model_dump(mode='json') for MCP transport compatibility
- [Phase 04.1]: 04.1-02: find_related_papers accepts str|list[str], deduplicates by highest score, excludes seed IDs
- [Phase 04.1]: 04.1-02: get_paper uses direct ORM select(Paper) query (not SearchService) for single-paper lookup
- [Phase 04.1]: 04.1-02: _get_app(ctx) helper pattern for extracting AppContext from MCP Context
- [Phase 04.1]: 04.1-03: All MCP tools use source='mcp' for audit trail provenance
- [Phase 04.1]: 04.1-03: add_to_collection auto-creates collection on ValueError (idempotent UX)
- [Phase 04.1]: 04.1-03: create_watch two-step: create_saved_query then promote_to_watch
- [Phase 04.1]: 04.1-03: Paper resource composes from 4 services (ORM + triage + enrichment + collections)
- [Phase 04.1]: 04.1-03: Resources return {"error": ...} dicts on not-found (consistent with tool pattern)
- [Phase 05]: 05-02: Prompts return concise workflow guidance (~1000-1500 chars), not paper content
- [Phase 05]: 05-02: triage_shortlist uses show_collection PaginatedResponse for live paper count
- [Phase 05]: 05-02: Each prompt is a single UserMessage (not multi-message sequences) for simplicity
- [Phase 05]: 05-01: Used followed_author signal type for tension vocabulary (tensions map to topical interest areas)
- [Phase 05]: 05-01: Paper-index-data.json value scores for triage mapping, NOT normalized_holistic
- [Phase 05]: 05-01: Excluded-audit papers default to 'seen' triage state (not in paper-index-data)
- [Phase 05]: 05-01: ON CONFLICT DO NOTHING for paper upsert idempotency
- [Phase 05]: 05-03: batch_add_signals uses partial-success semantics (continue on individual errors, report summary)
- [Phase 05]: 05-03: Result sets remain ephemeral in v1 (agents compensate via context window; persistence deferred to v2)
- [Phase 05]: 05-03: Option D (hybrid tools+resources+prompts) validated as correct MCP surface shape
- [Phase 05]: 05-03: All 5 doc 06 questions resolved with evidence from real MCP usage
- [Phase 05]: 05-03: Profile vs collection ordering is irrelevant (independent concepts at different workflow stages)
- [Phase 06]: 06-01: RightsChecker uses set-based license classification (PERMISSIVE vs PERSONAL_USE) with unknown/None as restrictive
- [Phase 06]: 06-01: Local mode always allows access with warning; hosted mode blocks non-permissive licenses (ADR-0003)
- [Phase 06]: 06-01: ContentVariant follows PaperEnrichment pattern: composite PK, FK to papers, CHECK constraint on variant_type
- [Phase 06]: 06-01: quality_warnings as JSONB in ORM and list[str] in Pydantic (natural serialization boundary)
- [Phase 06]: 06-02: ContentAdapter protocol mirrors EnrichmentAdapter: adapter_name property + async convert method
- [Phase 06]: 06-02: MarkerAdapter initializes PdfConverter once in __init__ (not per-call) via asyncio.to_thread
- [Phase 06]: 06-02: HTML fetcher uses HEAD-first check before GET to avoid bandwidth waste on 404 papers
- [Phase 06]: 06-02: ContentService reuses enrichment RateLimiter for consistent arXiv rate limiting
- [Phase 06]: 06-02: PDF temp file uses NamedTemporaryFile with delete=True for automatic cleanup
- [Phase 06]: 06-02: Variant storage uses pg_insert ON CONFLICT upsert (same pattern as enrichment)
- [Phase 06]: 06-03: get_content_variant validates variant before rights check (fail fast on invalid input)
- [Phase 06]: 06-03: Abstract variant skips rights check (always available per arXiv terms)
- [Phase 06]: 06-03: Rights enforcement at MCP tool layer via RightsChecker, not at service layer (ADR-0003)
- [Phase 06]: 06-03: Paper resource returns content_variants as lightweight metadata list (no full content)
- [Phase 06]: 06-03: Content CLI follows enrichment CLI pattern: _make_services helper, asyncio.run, Rich+JSON output
- [Phase 06]: 06-04: TRUNCATE CASCADE instead of drop+create for content test fixture cleanup (preserves asyncpg prepared statement cache)
- [Phase 07]: WorkflowSearchService as intermediate service (not on AppContext) -- only ProfileRankingService wraps it
- [Phase 07]: SuggestionCandidate serialized via dataclasses.asdict (not model_dump) -- dataclass not Pydantic
- [Phase 07]: ProfileRankingService as universal delegation target for discovery tools (handles both ranked and unranked paths internally)
- [Phase 07]: Always include ranking_explanation when profile_slug provided (no explain toggle) -- MCP returns structured data for agents
- [Phase 07]: find_related_papers not routed through ProfileRankingService -- flat list incompatible with ProfileSearchResponse
- [Phase 08]: 08-01: Shared fixtures (test_engine, test_session, TSVECTOR SQL, sample_paper_data) centralized in root conftest only; module conftest imports them
- [Phase 08]: 08-01: content/__init__.py stripped to docstring only (zero re-exports) per locked SC-4 decision
- [Phase 08]: 08-01: Subprocess-based import isolation testing for verifying lazy loading (avoids false passes from pre-loaded modules)
- [Phase 08]: 08-02: Database-only migration plan -- no source files modified, live DB migrated 004->008 via alembic upgrade head
- [Phase 09]: 09-01: PEP 639 SPDX string format for license (license = 'MIT') not legacy table format
- [Phase 09]: 09-01: Renamed enrichment/content local vars in server.py lifespan to avoid F811 shadowing with side-effect import names
- [Phase 09]: 09-01: Per-file-ignores for alembic F401 and cli.py E402 (intentional patterns)
- [Phase 09]: 09-02: README documents all 13 MCP tools grouped by domain, with user-facing quick-start and MCP server config
- [Phase 09]: 09-03: git subtree split to extract project from home directory monorepo into standalone GitHub repo
- [Phase 09]: 09-03: Content service integration tests deselected in CI (async DB+HTTP event loop hang; passes locally)
- [Phase 09]: 09-03: pytest-asyncio pinned to >=0.24,<1 for respx compatibility
- [Phase 10]: MCP server registered via claude mcp add-json --scope local (writes to ~/.claude.json alongside existing servers)
- [Phase 10]: DATABASE_URL passed explicitly in MCP env block (belt-and-suspenders with .env discovery via cwd)
- [Phase 10]: Absolute venv Python path used for MCP stdio command (not system python)
- [Phase 10]: IntegrityError catch at MCP tool layer (not service layer) for clean FK violation error messages
- [Phase 10]: F-07 fix via string replacement at tool layer rather than modifying SavedQueryService
- [Phase 10]: README split into Claude Code and Claude Desktop sections with validated configs

### Pending Todos

- **Draft `.planning/gsd-2-uplift/ORCHESTRATION.md`** (per decision B6) — wave-execution living plan. Content: per-slice prompts (5; cross-vendor codex GPT-5.5 high; minimum-viable-framing principle); pilot-gate criteria (what slice 1 output needs to look like for parallel proceed; re-slice trigger; approach-change trigger); W2 audit specs (slice 4 mandatory; others conditional per B2); W3 synthesis spec (same-vendor Claude xhigh; paired-synthesis escalation criterion per B3); setup checklist (clone location at `~/workspace/projects/gsd-2-explore/`; codex-CLI pitfall reminders per post-Wave-4 handoff §9 + archived dispatch package; output paths); failure-mode handling (codex hangs / sandbox issues / output truncation); mid-stream pivot protocol (per dispatch-readiness deliberation §9(d)); per-slice forbidden-reading-list (M1 extension at METHODOLOGY.md:117). See dispatch-readiness deliberation §9 for non-exhaustive starter of additional concerns. Estimated size: 300-500 lines.
- **Light orchestration-plan audit** before pilot dispatch (per dispatch-readiness deliberation §9(f)) — single same-vendor xhigh pass on ORCHESTRATION.md for closure-pressure-recurrence + framing-leak in prompts. Not full parallel audit.
- **Pilot dispatch of slice 1** (cross-vendor codex GPT-5.5 high) after orchestration audit. Disposition gate: review pilot output; calibrate prompts; decide proceed-parallel vs re-slice vs change approach. Possible escalation to Option C (paired exploration) if pilot reveals problems per B2 change-conditions; possible de-escalation to Option A (combined audit+synthesis) if pilot reveals cross-vendor reads gsd-2 well.
- **Parallel dispatch of slices 2-5** (cross-vendor) after pilot disposition.
- **Selective W2 audits** (same-vendor Claude xhigh; slice 4 always; others conditional per B2 selective-audit criteria).
- **W3 synthesis** (same-vendor Claude xhigh; paired-synthesis at W3 reserved as conditional escalation per B3).
- **Incubation checkpoint** per DECISION-SPACE §2.3. Re-evaluate goal articulation + R2/R3 hybrid + metaquestion. Mandatory; not pro-forma.
- Stage 1 audit findings (deferred quality + minor) — §A decision-table compression of §1.2 bifurcation; "Logan's framing" parenthetical in §4.5; §3 prefix vs §5.1 deliverables-vs-informing tension; R2-base contingency phrasing in INITIATIVE.md §2; "load-bearing" overuse + confidence-distribution tilt; cancellation procedure / re-articulation date / attention-budget vs v0.2. Address opportunistically; not blocking.
- Phase 12 plan 1 authoring (on hold pending gsd-2 uplift first-wave findings + incubation checkpoint; see LONG-ARC.md for sequencing)
- Q1/Q4/Q16 Logan validation (foundation-audit closures from Phase 04.1 / Quick Task 1; tracker in §"Pending Validations" below; orthogonal to uplift work)
- Codification of session-disciplines (closure-pressure recurrence; comfort-language; performative-vs-operational openness; non-exhaustive-listings; push-for-assumptions; **+ skill-heuristic shallow-match per dispatch-readiness §B.1; + strict-M1 undersell at recommendation stage per §B.2**) in METHODOLOGY.md or AGENTS.md — threshold 2-3 deliberation logs per DECISION-SPACE §3.9; current: 3 logs (2026-04-25 + 2026-04-26 + 2026-04-27). Threshold reached; codification candidate ready for evaluation when next opportunity warrants.
- Migration of `.planning/gsd-2-uplift/` artifacts to dedicated repo when that repo is created (per INITIATIVE.md §7 migration trigger).
- Two INDEX.md verification items addressed via PROJECT.md refresh (2026-04-26): local-gap-propagation reframed as GSDR-signal-system-scoped (not primary active reference); spike-epistemic-rigor symlink note added.

### Roadmap Evolution

- Phase 04.1 inserted after Phase 4: MCP v1 — expose existing services as MCP tools and resources (foundation audit finding 1B: MCP-native project identity requires earlier MCP validation)
- 2026-03-11: Roadmap resequenced per ecosystem analysis. Old Phase 5 (Content Normalization) → new Phase 6. Old Phase 6 (MCP Integration) absorbed into Phase 04.1 + new Phase 5 (MCP Validation). MCP requirements split: core tools (Phase 04.1), prompts/validation (Phase 5), content tool (Phase 6). Three new requirement categories added: PREMCP (pre-MCP fixes), MCPV (validation). Total requirements: 53 (was 47).
- 2026-03-11: Ecosystem commentary document written (.planning/ECOSYSTEM-COMMENTARY.md) analyzing cross-project data flows between arxiv-scan pipeline and MCP, identifying pre-MCP fix priorities, literature review feature priorities, and feedback loop design.

- Phase 9 added: Release Packaging (LICENSE, README, pyproject.toml, CHANGELOG, GitHub, CI, v0.1.0 tag)
- Phase 10 added: Agent Integration Test (real MCP server config, agent research session, setup docs from actual usage)

### Blockers/Concerns

- Phase 6: Docling vs Marker quality comparison for scholarly PDFs (math, citations, tables) needs Phase 6 experimentation.
- OpenAlex credit-based pricing tiers need research before committing to enrichment scheduling strategy.
- ~~Enrichment schema mismatch~~ RESOLVED (08-02): Live DB migrated to composite PK (arxiv_id, source_api) via alembic upgrade head.
- arXiv API URL must be HTTPS (fixed in 05-03); follow_redirects enabled as safety measure.

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 1 | Foundation fixes: extensible schemas, remove implicit demotion, epistemic discipline | 2026-03-11 | 27ae31f | [1-foundation-fixes](./quick/1-foundation-fixes-extensible-schemas-remo/) |

## Pending Validations (carried over from foundation-audit)

| Open Question | Closed by | Pending action | Status |
|---|---|---|---|
| Q1 — What is the right default notion of interest state? | Quick Task 1 (application-validated signal types, no DB constraint) | Logan validates the closure rationale | PENDING |
| Q4 — Which external enrichments are worth the dependency cost? | Quick Task 1 (OpenAlex as sole source; composite PK for multi-source extensibility) | Logan validates the closure rationale | PENDING |
| Q16 — What is the right processing intensity promotion strategy? | Quick Task 1 (demand-driven promotion only) | Logan validates the closure rationale | PENDING |

*Source: `.planning/foundation-audit/FINDINGS.md` finding I5; closures recorded in `docs/10-open-questions.md` (Q1 at line 9, Q4 at line 31, Q16 at line 104). Each marked "Resolved during implementation (pending user validation)."*

## Session Continuity

Last session: 2026-04-29T01:30:00Z
Stopped at: v1-GSD premise-bleed audit-spec arc revised-for-dispatch; AUDIT-SPEC.md v2 + DECISION-SPACE.md §1.17 + audit-spec-review deliberation log all landed; awaiting Logan final-call review before Step-1 cross-vendor codex auditor dispatch. Pre-audit-arc state preserved: SYNTHESIS-COMPARISON.md draft-complete (in-session-collaborative per D5a; full §0-§6 landed); §2.1 R4 disposition-timing + §5 axes are surfacing-shape awaiting incubation adjudication; v1-GSD premise-bleed audit feeds incubation-checkpoint disposition (commit-as-is / commit-with-addendum / revise-before-commit) before §2.1 + §5 adjudication proceeds. Audit shape: Step-1 cross-vendor codex GPT-5.5 high baseline + Step-2 same-vendor adversarial-auditor-xhigh stress on Class C trigger or Logan manual-escalation. Hybrid grounding with soft-cap ~5 source-reads + overflow protocol. Negative-space check required. Vetted-replacement vocabulary lookup + META-SYNTHESIS §3 prohibited-articulations integration.
Resume file: `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` (v2 revised-for-dispatch); `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC-REVIEW.md` (cross-vendor review unchanged); `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (full review-and-response trace; §3 transparent analysis; §5 per-finding adjudication; §6 revision-action table); `.planning/gsd-2-uplift/DECISION-SPACE.md §1.17` (load-bearing audit-methodology decision; 7 rules); `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` (the upstream artifact the audit feeds; §0-§6 draft-complete); `.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md` (predecessor session context); `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md` (primary grounding for premise-bleed audit per §4.2 hybrid).
Cross-references: load-bearing decision-space `.planning/gsd-2-uplift/DECISION-SPACE.md` (§1.11-§1.17); initiative-staging `.planning/gsd-2-uplift/INITIATIVE.md`; framing-widening operating-frame `.planning/deliberations/2026-04-28-framing-widening.md`; W2 disposition log `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` (D5a in-session-collaborative for comparison stage); comparison-drafting log `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` (DC0-DC4); audit-spec-review log `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (F1-F7 adjudications + post-disposition refinements); predecessor handoff `.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md`; further-predecessor handoff `.planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md`; orchestration overview `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` §11.4 (W2) + §11.5 (W3 + comparison) + §11.6.5 (audit-spec arc).
