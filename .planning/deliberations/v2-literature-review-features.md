# Deliberation: v2 Literature Review Feature Priorities

<!--
Deliberation template grounded in:
- Dewey's inquiry cycle (situation → problematization → hypothesis → test → warranted assertion)
- Toulmin's argument structure (claim, grounds, warrant, rebuttal)
- Lakatos's progressive vs degenerating programme shifts
- Peirce's fallibilism (no conclusion is permanently settled)

Lifecycle: open → concluded → adopted → evaluated → superseded
-->

**Date:** 2026-03-13
**Status:** Open
**Trigger:** During v1 milestone audit, Ecosystem Commentary §5 surfaced 5 literature review feature priorities not captured in v1 gap closure or v2 backlog. User wants to plan which belong in v2 milestone.
**Affects:** v2 milestone planning, REQUIREMENTS.md v2 section, ROADMAP.md
**Related:**
- `.planning/ECOSYSTEM-COMMENTARY.md` §5 (source of priorities)
- `.planning/v1-MILESTONE-AUDIT.md` (audit context where this arose)
- `docs/01-project-vision.md`, `docs/02-product-principles.md` (product values)
- ADR-0001 (exploration-first), ADR-0002 (metadata-first, lazy enrichment)

## Situation

v1 delivered a complete MCP-native discovery substrate: 11 tools, 4 resources, 3 prompts, 471 tests. The milestone audit found all 53 requirements satisfied with tech debt only. Two gap closure phases (7: MCP Surface Parity, 8: Infrastructure Fixes) are planned.

The Ecosystem Commentary §5 identified 5 literature review feature priorities from real arxiv-scan usage that go beyond v1 scope. These are genuine product enhancements — not gaps in what v1 promised, but capabilities that would make the tool significantly more useful for systematic literature review workflows. The user wants to capture these for v2 milestone planning.

### Evidence Base

| Source | What it shows | Corroborated? | Signal ID |
|--------|--------------|---------------|-----------|
| `mcp/tools/discovery.py:89-117` | `find_related_papers` accepts `list[str]`, deduplicates by score, but does not track which seed surfaced which result | Yes (code read) | informal |
| `db/models.py:151`, `enrichment/service.py:255` | OpenAlex `related_works` stored as JSONB on PaperEnrichment, displayed in CLI, but not surfaced as a discovery tool | Yes (grep) | informal |
| `db/models.py:338-358` | InterestProfile has no `description` field — only slug, name, is_archived, negative_weight, weights, timestamps | Yes (code read) | informal |
| `src/` grep for bibtex | No BibTeX export exists anywhere in the codebase | Yes (grep, 0 matches) | informal |
| Ecosystem Commentary §5 | Ordered feature priorities from cross-project analysis of real arxiv-scan usage patterns | Yes (document read) | informal |
| REQUIREMENTS.md v2 section | Current v2 scope: semantic search (SEMA-01 through SEMA-04), advanced enrichment (ADVN-01 through ADVN-04), advanced workflows (ADVW-01 through ADVW-03) | Yes (document read) | informal |

## Framing

**Core question:** Which §5 literature review features should be added to v2 requirements, how should they be grouped into phases, and what's the right sequencing relative to existing v2 items (semantic search, advanced enrichment, advanced workflows)?

**Adjacent questions:**
- Should v2 prioritize depth (semantic search making existing discovery better) or breadth (new discovery modalities like cross-source relatedness)?
- Do these features change the v2 milestone definition of done?
- Which features have dependencies on each other (e.g., cross-source relatedness needs enriched related_works which needs OpenAlex enrichment to be reliable first — Phase 8 fixes the schema mismatch)?

## Analysis

### The 5 Features Under Consideration

**1. Multi-seed expansion with provenance** (§5: Highest)
- Current state: `find_related_papers` supports multi-seed, deduplicates by highest score
- Gap: No tracking of which seed surfaced which result. Snowball sampling can't attribute discoveries.
- Implementation: Return `seed_arxiv_id` alongside each result in the MCP tool response. Requires changes to `find_related_papers` tool and `SearchService.find_related_papers`.
- Scope: Small — 1-2 files changed, schema of return value extended

**2. Cross-source relatedness surfacing** (§5: High)
- Current state: OpenAlex `related_works` stored as JSONB list of OpenAlex IDs on PaperEnrichment. Not queryable as a discovery mechanism.
- Gap: Can't say "show me what OpenAlex thinks is related to this paper" as a discovery path separate from lexical similarity.
- Implementation: New tool or mode in find_related_papers. Resolve OpenAlex IDs back to arXiv papers (reverse of current DOI-based resolution). May require new query paths.
- Scope: Medium — new service method, possibly new adapter method, MCP tool extension
- Dependency: Enrichment schema must work first (Phase 8)

**3. Watch-based monitoring with auto-shortlisting** (§5: High)
- Current state: Watches check for deltas. Triage is manual per-paper.
- Gap: High-confidence papers (above ranking threshold) could be auto-shortlisted, with borderline papers flagged for review.
- Implementation: Add ranking threshold to watch config. When `check_watch` runs, auto-triage results above threshold. Requires profile-ranked watch checks (Phase 7 wires ProfileRankingService into MCP first).
- Scope: Medium — watch service extension, config changes, MCP tool update
- Dependency: Phase 7 (MCP Surface Parity) must land first for profile-ranked search via MCP

**4. Interest profile as scope document** (§5: Medium)
- Current state: Profiles have name, signals, weights. No human-readable description.
- Gap: Can't explain what a profile is *for* in prose. No snapshots for reproducibility. No comparison over time.
- Implementation: Add `description` text field to InterestProfile. Profile snapshots as JSONB versioned records. Profile diff for evolution tracking.
- Scope: Description field is trivial (migration + model). Snapshots and comparison are medium.

**5. BibTeX/citation export** (§5: Medium)
- Current state: Export module exists for workflow state (JSON). No citation format export.
- Gap: Researchers need to cite papers. arXiv metadata has all the fields needed for BibTeX.
- Implementation: BibTeX formatter from Paper model. Export by collection, by triage state, by search results. MCP tool or resource.
- Scope: Small-medium — formatter function, export service method, MCP exposure

### Option A: Add all 5 to v2 as a "Discovery Enhancement" phase cluster

- **Claim:** Group features 1-3 (discovery) into one phase and 4-5 (workflow) into another, sequenced after Phase 7-8 gap closure
- **Grounds:** These features directly serve the product's core value (discovery + triage for researchers). They build on v1's validated foundation rather than adding new infrastructure.
- **Warrant:** ADR-0004 says MCP is the workflow substrate. Features that make the MCP workflow more useful for real literature review are higher value than adding semantic search infrastructure that may not be needed yet (ADR-0001: exploration-first, don't prematurely commit).
- **Rebuttal:** Adding 5 features before semantic search delays the Stack A → B trajectory. Semantic search (SEMA-01 through SEMA-04) may be more transformative than incremental discovery improvements.
- **Qualifier:** Probably the right call for a philosophy researcher doing systematic literature review

### Option B: Cherry-pick the highest-value items, defer the rest

- **Claim:** Add only multi-seed provenance (#1) and cross-source relatedness (#2) to v2. Defer auto-shortlisting, profile descriptions, and BibTeX to v3 or backlog.
- **Grounds:** #1 is nearly free (small change). #2 unlocks a genuinely new discovery modality using data already stored. The others are nice-to-have workflow polish.
- **Warrant:** The product principle is "discovery over overload." #1 and #2 directly improve discovery. #3-5 improve workflow but don't unlock new discovery paths.
- **Rebuttal:** BibTeX export has outsized utility relative to its implementation cost. Excluding it feels like over-optimization.
- **Qualifier:** Presumably correct if implementation time is constrained

### Option C: Interleave with existing v2 items by dependency order

- **Claim:** Don't treat these as a separate cluster. Interleave them with SEMA/ADVN/ADVW phases based on dependencies and synergies.
- **Grounds:** Cross-source relatedness (#2) pairs naturally with ADVN-02 (broader citation graph). Auto-shortlisting (#3) becomes much more powerful with SEMA-04 (profile-driven recommendation). Profile descriptions (#4) pair with ADVW-01 (active learning suggestions).
- **Warrant:** Sequencing by synergy rather than origin creates more coherent phases than "§5 features" vs "existing v2 features."
- **Rebuttal:** Interleaving makes the v2 roadmap more complex and harder to scope. Risk of scope creep if every enhancement gets woven into every phase.
- **Qualifier:** Probably correct architecturally but adds planning overhead

## Tensions

1. **Discovery depth vs breadth:** Semantic search (SEMA) deepens existing retrieval. §5 features broaden discovery modalities. Both serve the product but pull in different directions.

2. **Stack trajectory vs product value:** The documented trajectory is Stack A → B (add selective semantic). But the highest-value next features may not require semantic search at all — they build on Stack A's graph enrichment and lexical foundation.

3. **Implementation cost vs user impact:** BibTeX export is trivially cheap but only matters at export time. Cross-source relatedness is moderate cost but could transform how related papers are discovered (vocabulary mismatch is a real problem for philosophy research).

4. **v2 scope discipline:** Adding 5 features to v2 alongside SEMA + ADVN + ADVW makes it a large milestone. The v1 milestone was already 53 requirements across 7+2 phases.

## Recommendation

**Current leaning:** Option A with scope discipline — add all 5 as formal v2 requirements, but sequence them early (before SEMA) since they build on v1 infrastructure and don't require new compute (no embeddings, no vector DB). Group as:
- Phase v2-1: Discovery Enhancement (multi-seed provenance, cross-source relatedness)
- Phase v2-2: Workflow Enhancement (profile descriptions, auto-shortlisting, BibTeX export)
- Then SEMA phases (which require pgvector, SPECTER2, GPU compute)

This follows ADR-0002's "metadata-first, lazy enrichment" — exhaust what you can do with metadata + graph before adding compute-heavy semantic retrieval.

**Open questions blocking conclusion:**
1. Does the user agree these belong in v2 vs being deferred further?
2. Should BibTeX move earlier (nearly free, high researcher utility)?
3. Does the user want to re-scope existing v2 items (SEMA, ADVN, ADVW) in light of these additions?

## Predictions

<!--
Predictions make the deliberation falsifiable (Lakatos). If adopted, what should we
observe? If we don't observe it, the deliberation's reasoning was flawed.
Record predictions BEFORE implementation so they can't be retrofitted.
-->

**If adopted, we predict:**

| ID | Prediction | Observable by | Falsified if |
|----|-----------|---------------|-------------|
| P1 | Multi-seed provenance will be the most-used new feature (agents attribute discoveries to seeds in every snowball session) | After v2-1 ships: check MCP usage logs for find_related_papers with provenance | Agents ignore provenance data and just use the flat result list |
| P2 | Cross-source relatedness will surface papers that lexical search misses (vocabulary mismatch problem) | After v2-1 ships: compare discovery sets from lexical vs graph-based relatedness | Graph-based relatedness returns a strict subset of lexical results |
| P3 | Sequencing §5 features before SEMA will not delay meaningful semantic search adoption | After v2-2 ships: assess whether SEMA is still the right next priority | User urgently needs semantic search and §5 features blocked it |
| P4 | BibTeX export will be requested in the first real research session after v2 ships | During first real usage session | User completes multiple research sessions without needing citation export |

## Decision Record

<!--
Filled when status moves to `concluded` or `adopted`.
Links the deliberation to the intervention that implements it.
-->

**Decision:** Pending — deliberation open for v2 milestone planning
**Decided:** —
**Implemented via:** not yet implemented
**Signals addressed:** None (triggered by ecosystem commentary review, not formal signals)

## Evaluation

<!--
Filled when status moves to `evaluated`.
-->

## Supersession

<!--
Filled when status moves to `superseded`.
-->
