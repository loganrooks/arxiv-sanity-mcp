# Ecosystem Commentary: arxiv-sanity-mcp + arxiv-scan

> Written 2026-03-11 from a cross-project analysis session, **before Phase 04.1 execution**.
> Numbers in this document reflect pre-04.1 state (307 tests → now 357, 150 papers → now 154, 5 proposed tools → 9 shipped). Recommendations in §3-4 were implemented in Phase 04.1.
> Intended audience: future arxiv-sanity-mcp development sessions.

## Status as of 2026-04-26

*Added per governance audit synthesis G-B1. Covers §§5-7; §§3-4 are already annotated in the header above. External ecosystem claims in this document (tool counts, paper counts, arxiv-scan pipeline state) have not been re-verified after 2026-03-11.*

**§5 — Literature Review Feature Priorities:** Mostly shipped in v0.1. Multi-seed expansion and provenance tracking shipped in Phase 04.1 (`find_related_papers` accepts list of seeds). Watch-based monitoring with enriched deltas shipped in Phase 04.1/05. Cross-source relatedness (OpenAlex `related_works`) surfaced via MCP paper resource. BibTeX export and bulk triage remain open; profile description field and snapshots are v2 scope per REQUIREMENTS.md.

**§6 — Cross-Project Import Strategy:** Import strategy implemented in Phase 05 (05-01-PLAN.md). Import script ingested arxiv-scan papers (126 papers, not 150 — actual import used paper-index-data.json value scores), set triage states, created tension-vocabulary interest profile. The import served as Phase 05's validation dataset; MCP ranking was compared against human arxiv-scan triage decisions (doc 06 resolved). OpenAlex enrichment path established.

**§7 — MCP v1 Surface:** Closed by what shipped. v0.1 ships 13 tools (not the 5 proposed here), 4 resources (matching this §), 3 prompts (literature-review-session, daily-digest, triage-shortlist — not the 2 proposed here). Tool count exceeded the 5-10 heuristic cited at bottom of §7; MCP-07 in REQUIREMENTS.md has been reframed (governance audit synthesis commit 1) to "tool count justified by user-intent grouping" rather than numeric cap.

---

## 1. Foundation Audit: What It Got Right

The foundation audit (`.planning/foundation-audit/FINDINGS.md`) is genuinely rigorous work. Specific strengths:

- **Five-axis methodology** (evidence tracing, alternative evaluation, sensitivity analysis, inference chain integrity, category discipline) is reusable beyond this project. Each axis catches a different class of spec-drift.
- **I3 (category-based negative demotion)** was the most important finding. Demoting all cs.AI papers because one cs.AI paper was marked negative directly violated ADR-0001's explicit/implicit boundary. This was correctly identified as MEDIUM severity but functionally CRITICAL for a philosophy-focused researcher whose papers routinely span cs.AI, cs.CL, cs.MA, and philosophy categories.
- **Requirements extraction audit** establishing the "category error" pattern (hedging language → firm requirement) is methodology that transfers to any project where design docs feed implementation.
- **"Competently built to the wrong spec"** is exactly the right diagnosis. The code quality is high; the problem is that product decisions were embedded in implementation without user confirmation.

Quick Task 1 (completed 2026-03-11) already resolved I1, I3, and I4 based on audit findings. This is good execution.

---

## 2. Foundation Audit: What It Missed

| Gap | Severity | Detail |
|-----|----------|--------|
| **I2 ranking triple-counting underrated** | Should be CRITICAL | Category Jaccard is computed 3x across scorers: `score_category_overlap` (weight 0.15) + `score_seed_relation` (60% of 0.25 = 0.15) + `score_profile_match` (50% of 0.15 = 0.075). Effective category weight: **0.375** (intended: 0.15). For philosophy research, over-weighting category overlap penalizes cross-domain discovery — the most interesting papers come from unexpected categories. The audit noted this but rated it MEDIUM. |
| **"Seen" triage state dropped** | MEDIUM | WKFL-03 noted in audit but not elevated. "Seen but not triaged" vs "never encountered" is load-bearing for systematic literature review. Watch deltas can't distinguish "still thinking about this paper" from "never saw it." The absence-means-unseen design is fine for `unseen`, but there's no way to mark a paper as "encountered, decision pending." |
| **Over-fetch pagination break** | LOW | `_ranked_search` uses 3x over-fetch + re-rank + truncate. After re-ranking, cursor pagination tokens are meaningless — the next page fetches a different 3x window and re-ranks again, potentially surfacing papers that should have appeared on page 1. Should be documented as known limitation, not treated as working pagination. |
| **Test coverage quality unaudited** | LOW | 307 tests is an impressive count. But test quality for ranking correctness (do the right papers surface first?) and triage edge cases (state transitions, concurrent modifications) was not examined. Count ≠ coverage of important behaviors. |
| **CLAUDE.md stale** | LOW | Still says "Pre-implementation design phase. No source code exists." Four phases are complete with working code, tests, and CLI. This will confuse any agent (human or AI) starting a new session. |

---

## 3. Roadmap Resequencing Recommendation

### Current Sequence
Phase 4.1 (MCP v1) → Phase 5 (Content Normalization) → Phase 6 (MCP Integration)

### Problem
Content normalization blocks MCP validation. For literature review, metadata + abstracts + triage + ranking are the high-value loops. Full-text parsing is secondary and shouldn't delay real workflow validation. Phase 6 as designed assumes all services exist before MCP exposure — but the point of MCP-first (ADR-0004) is that agent workflows reveal what services need to exist.

### Recommended Sequence

**Phase 4.1: MCP v1** — Expose search, workflow, interest, enrichment as tools + resources. Ship the minimum viable MCP surface that enables a real literature review session.

**Phase 5: MCP validation + iteration** — Use MCP v1 with real agent workflows (the arxiv-scan continuation is the first real customer). Answer doc 06's open questions with evidence, not speculation:
- Which tool granularity works? (One `search` tool vs separate `search_papers`, `search_by_author`, `browse_recent`?)
- Which resources do agents actually read? (Paper metadata? Collection contents? Profile state?)
- What's missing? (Cross-collection comparison? Bulk triage? Export?)

**Phase 6: Content Normalization** — Add content variants and parsing. By this point, you know what content agents actually request, which backends matter, and what parsing quality is needed.

This resequencing treats MCP as the product surface (per ADR-0004), not as a wrapper applied after-the-fact.

---

## 4. Pre-MCP Fixes (Before Phase 4.1)

These should be done before shipping MCP v1 so the first real usage isn't undermined by known issues:

### 4A. Fix Ranking Triple-Counting
**File:** `src/arxiv_mcp/interest/ranking.py`

Remove redundant category Jaccard from `score_seed_relation` and `score_profile_match`. Score category overlap exactly once via `score_category_overlap`. The seed relation scorer should measure seed-specific signals (shared authors, citation links when available) without recomputing category similarity. The profile match scorer should aggregate profile-level signals without double-counting what the dedicated category scorer already provides.

Current effective weights:
```
category_overlap: 0.375 (intended 0.15)
author_match:     0.10 + 0.053 = 0.153
query_boost:      0.023
```

After fix, category overlap should be exactly 0.15, with the freed weight redistributed to seed-specific and profile-specific signals.

### 4B. Update CLAUDE.md
Reflect actual project state: 4 phases complete, working CLI, 307 tests, Quick Task 1 fixes applied. Remove "Pre-implementation design phase" language.

### 4C. Restore "Seen" Triage State
Add `seen` to the CHECK constraint in `TriageState`. This represents "encountered but no triage decision yet" — distinct from absence (never encountered) and from `shortlisted`/`dismissed` (decision made). Migration: add `seen` to the allowed values. Service: expose a `mark_seen` operation.

### 4D. Document Over-Fetch Pagination Limitation
Add a note in the search module or in an ADR that cursor pagination after re-ranking is approximate — page boundaries shift because each page independently over-fetches and re-ranks.

---

## 5. Literature Review Feature Priorities (for MCP Roadmap)

Ordered by value for systematic literature review workflows:

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **Highest** | Multi-seed expansion with provenance | Snowball sampling: start with key papers, expand via `find_related_papers`, triage results, add new seeds, repeat. Currently `find_related_papers` takes a single seed; should support multiple with provenance tracking (which seed surfaced which result). This is the core discovery loop. |
| **High** | Cross-source relatedness surfacing | OpenAlex `related_works` is already stored via enrichment but not surfaced as a discovery tool. Critical for philosophy where the same concept uses different vocabulary across traditions (e.g., "epistemic reliability" in analytic philosophy vs "truth-conduciveness" in pragmatism). |
| **High** | Watch-based monitoring with enriched deltas | Agent checks watches periodically, auto-shortlists high-confidence papers (above ranking threshold), flags borderline for human review. The triage state + watch system already exists; this is about the MCP workflow that connects them. |
| **Medium** | Interest profile as scope document | Add a `description` field to profiles for human-readable scope statement. Add profile snapshots for reproducibility. Add profile comparison to track how research interests evolve over time. |
| **Medium** | BibTeX/citation export | Low implementation cost; arXiv metadata already contains the necessary fields. The export module exists in workflow but needs BibTeX format and MCP exposure. |
| **Lower** | Bulk triage operations | Import existing triage decisions (e.g., the 1,211 triaged papers from arxiv-scan). Mark multiple papers in one operation. Currently one-at-a-time via CLI. |

---

## 6. Cross-Project Data Flow: arxiv-scan → MCP

The arxiv-scan pipeline (`/scratch/arxiv-scan/`) has produced data that should bootstrap MCP usage:

| Data | Source | MCP Target | Notes |
|------|--------|------------|-------|
| 150 analyzed papers | `pipeline/reading/paper-analyses/*.json` | Paper metadata + triage states | Import as pre-triaged papers with value scores |
| 10 tension definitions | `pipeline/evaluation-guidelines.md` | Interest profile signals | Tensions as signal types for discovery targeting |
| Evaluation dimensions | `pipeline/evaluation-guidelines.md` | Future evaluation lens definitions | 6-dimensional rubric maps to structured assessment |
| Inter-rater reliability data | `pipeline/inter-rater-reliability-summary.md` | Calibration baselines | Known biases (kappa=0.278) inform confidence bounds |
| 1,211 triage decisions | `pipeline/triage/` | Bulk triage import | Validate MCP ranking against known decisions |
| Thematic synthesis | `pipeline/synthesis/thematic-*.md` | Profile descriptions | Natural language scope for interest profiles |
| False negative audit | `pipeline/excluded-paper-audit.md` | Ranking validation | 4 known false negatives to test ranking improvements |

### Import Strategy
Phase A (after MCP v1 ships): Write a one-time import script that:
1. Ingests the 150 papers via arXiv API (metadata substrate)
2. Sets triage states from paper-index value scores (shortlisted for ≥7, seen for ≤6)
3. Creates an interest profile from arxiv-scan's tension vocabulary
4. Enriches via OpenAlex for citation data
5. Runs ranking against imported papers to compare MCP ranking vs arxiv-scan human ranking

This gives the MCP its first real validation dataset.

---

## 7. Open Question: What Should MCP v1 Expose?

Based on the existing codebase and literature review needs, a minimal viable MCP surface:

### Tools (actions that change state)
- `search_papers` — Lexical search with optional profile-based re-ranking
- `triage_paper` — Set triage state (shortlisted/dismissed/read/cite-later/archived/seen)
- `add_to_collection` — Add paper to named collection
- `create_watch` — Monitor a saved query for new results
- `add_signal` — Add signal to interest profile (seed paper, followed author, etc.)

### Resources (read-only state)
- `paper://{arxiv_id}` — Paper metadata + triage state + enrichment
- `collection://{slug}` — Collection contents with triage states
- `profile://{slug}` — Interest profile with signals and weights
- `watch://{slug}/deltas` — New papers since last checkpoint

### Prompts (reusable workflows)
- `literature-review-session` — Guided workflow: search → triage → collect → expand
- `discovery-expansion` — Given seed papers, find related work across sources

This aligns with ADR-0004 (MCP as workflow substrate) and keeps tool count within the 5-10 range noted in MCP-07.
