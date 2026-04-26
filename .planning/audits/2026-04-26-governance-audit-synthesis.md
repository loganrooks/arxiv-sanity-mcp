---
type: audit-synthesis
status: revised-2026-04-26-with-G-B-tier-dispositions
date: 2026-04-26 (revised same day)
target: governance-doc set (ADRs 0001-0004 + AGENTS + CLAUDE + REQUIREMENTS-outside-v0.2 + ROADMAP-outside-12-17 + STATE + foundation-audit + ECOSYSTEM-COMMENTARY)
inputs:
  - 2026-04-26-governance-audit-cross-vendor.md (primary)
  - 2026-04-26-governance-audit-opus-adversarial-xhigh.md (primary)
  - 2026-04-26-governance-audit-comparison.md (analysis)
weighting: |
  Both audits are weighted equally as primary inputs (both independently
  dispatched per M1; M1's Hypothesis status reinforced by the comparison's
  observed structural divergence + substance convergence).
purpose: |
  Convert governance-audit findings into concrete plan-revision proposals.
  Tiered by adoption disposition. Dispositions on AGENTS.md and CLAUDE.md
  substantive content are deferred pending exemplar review (Logan has
  noted exemplar AGENTS.md / CLAUDE.md from other projects to harvest
  principles from); the synthesis flags those rather than committing.
revision_note: |
  Original synthesis (committed 51abefc) was a draft pending Logan's
  dispositions on the four Adopt-with-shape items (G-B1..G-B4). This
  revision records those dispositions in a new §2.5.

  Provenance of the dispositions: proposed by Claude (opus-4-7, xhigh
  effort) in the post-Wave-3 onboarding session 2026-04-26, after
  reading the relevant source documents (ECOSYSTEM-COMMENTARY.md,
  REQUIREMENTS.md v2 sections, ADR-0005 in current state, governance
  comparison §3). Logan reviewed and accepted them with the explicit
  instruction to include everything — recommendations, explicit
  assumptions, reasoning, AND the "where my reasoning may be wrong"
  sections. §2.5 below records all of that.

  The original §2 "Adopt with Logan's call on shape" is preserved
  intact as the synthesis's original analysis with its original
  recommendations. §2.5 records the dispositions; one (G-B3) diverges
  from the original synthesis recommendation and the divergence is
  documented inline.

  Other deferred items (AGENTS/CLAUDE substantive edits in §4, gsd-2
  uplift items in §5) remain deferred pending exemplar review and the
  mid-horizon initiative respectively. This revision does not touch
  those.

  Sequencing impact: §8 Wave 4 commit list is updated to reflect the
  dispositioned shapes (commit 3 absorbs the G-B4 interim note to
  LONG-ARC; commit 5 reflects G-B1 shape-(a)-lite; commit 6 reflects
  G-B3 shape-(c)).
---

# Audit Synthesis — Governance-Doc Plan Revisions

## 0. Disposition summary (revised)

| Tier | Count | Action |
|---|---:|---|
| **Adopt now (commit-ready edits)** | 5 | Uncontested edits with multi-audit convergence; no exemplar-review dependency |
| **Adopt with shape (dispositioned 2026-04-26)** | 4 | Shape decisions recorded in §2.5; one (G-B3) diverges from original §2 recommendation |
| **Adopt at structural layer** | 3 | Structural changes to governance set (read-order map, audit closeout matrix, deliberation index) |
| **Deferred pending exemplar review** | 4 | AGENTS.md / CLAUDE.md substantive edits — wait for exemplar harvest |
| **Deferred to gsd-2 uplift initiative** | 2 | Issues whose right fix depends on the gsd-2 uplift design (e.g., per-phase ADR-against-plan audit operationalization) |
| **Drop / not adopting** | 3 | Findings that don't survive scrutiny or are taste-tier |

Total: 21 actionable items derived from 25 substantive findings in the comparison (12 strong-convergent → 11 actionable + 1 dropped; 9 single-audit → adjudicated; 1 substantive divergence → adopt SV's read; 3 self-discounted single-audit → drop or defer).

**Sequencing:** see §8 (updated to reflect dispositioned shapes). The Adopt-now items can land before the exemplar review. The deferred-pending-exemplar items wait. The deferred-to-gsd-2-uplift items wait for the mid-horizon initiative.

**Disposition revision summary table (G-B-tier):**

| Item | Original §2 recommendation | §2.5 disposition | Change |
|---|---|---|---|
| G-B1 | shape (a) full inline status table | shape (a)-lite — §-by-§ status, no per-recommendation table | **Narrow** |
| G-B2 | shape (a) minimal one-sentence reframe | shape (a) | None |
| G-B3 | shape (a) capability-with-illustrative ("e.g., SPECTER2 or equivalent") | shape (c) — strip names; record candidates in separate "Historical candidates" note | **Diverge** |
| G-B4 | shape (c) defer to gsd-2 uplift + one-line "operational-hook-pending" note | shape (c) + interim note made explicit about non-commitment of cadence | **Refine** |

## 1. Adopt now — commit-ready edits

These are concrete edits with multi-audit convergence in the comparison's CR1-CR5, with no dependence on exemplar review or gsd-2 uplift. Land in this audit cycle.

### G-A1. Refresh STATE.md to current and reconcile internal inconsistencies (CR4)

**Surface:** `.planning/STATE.md`

**Current state:** Frontmatter says v0.2 shape committed but detailed plan "still to be written" (lines 6-9) — but ROADMAP and v0.2-MILESTONE now have detailed Phases 12-17 with plans, dependencies, risks, success criteria. Velocity section says 23 plans completed (line 43); frontmatter says 31 (lines 13, 25). Session-continuity section says last session was 2026-04-16 (lines 222-226); frontmatter says last_updated 2026-04-25T20:00:00Z (line 8). "Pending Todos: None yet" (line 198) but pending items exist immediately below. "Phase 6 next" framings persist when Phase 6+ shipped months ago.

**Proposed structure:**
1. Tight current-state header: current milestone (v0.2), current activity (post-Wave 2 audit synthesis), last update (2026-04-26).
2. Clear "v0.1 historical metrics" section (separately legible from current activity).
3. Resolve 23-vs-31 plan-count discrepancy explicitly (one number is the v0.1 phase-plan total; one is the cumulative-plan total; document which is which).
4. Update session-continuity to current (2026-04-26 audit synthesis session).
5. Convert "Pending Todos: None yet" to actual pending items, or remove the line entirely.
6. Remove or annotate "Phase 6 next" framings.

**Reasoning:** Convergent finding (CV D4.1, D4.2, D4.3; SV E2). CLAUDE.md identifies STATE.md as the live-state record (CLAUDE.md:40-41 per SV's read); a live-state record cannot be internally inconsistent. Cost: 1-2 hours of focused editing. Blast radius: STATE.md only. No exemplar dependency.

### G-A2. Update CLAUDE.md (project-root) to current state — minimal version

**Surface:** `.planning/CLAUDE.md` (project root)

**Current state:** CLAUDE.md:9 says "Phases 1-5 + 04.1 complete. 403 tests passing, CLI operational, MCP server with 10 tools + 4 resources + 3 prompts. Validated with real data (126 imported papers, doc 06 resolved). Phase 6 (Content Normalization) is next." Per ROADMAP and CHANGELOG, v0.1 shipped (Phases 1-10 complete, including Phase 6); 13 tools (not 10); ~493 tests collected (not 403); v0.2 is active.

**Proposed minimal edit:** Update the "Current status" line only — to reflect v0.1 shipped, v0.2 active, current tool count (verified at edit time against tests), current test count (verified). Do not restructure the file in this commit. Restructuring is deferred-pending-exemplar-review (see §4).

**Why minimal:** the file's structural relationship to AGENTS.md (overlap, authority rule) is exemplar-review territory. The factual currency update is uncontested and cheap.

**Edit shape:**
> **Current status:** v0.1 shipped 2026-03-14 (10 phases complete, including 04.1; 13 MCP tools, 4 resources, 3 prompts; current pytest collection ~493 tests). v0.2 (multi-lens substrate) is the active milestone — Phases 12-17. See [STATE.md](.planning/STATE.md) for live state.

**Reasoning:** Convergent finding (CV D2.1, D3.1; SV D3). The structural fix waits; the currency fix doesn't. Cost: 5 minutes.

### G-A3. Doctrine pass: re-verify ADR citations against ADR text (CR1)

**Surface:** `.planning/LONG-ARC.md`, `.planning/VISION.md`, `.planning/milestones/v0.2-MILESTONE.md`, `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`

**Pattern:** Derivative documents cite ADR-0001 (and other ADRs) with stronger modal verbs than the source uses. Specific instances both audits identified:

- `LONG-ARC.md:46`: "Tournament narrowing... violates ADR-0001's coexistence intent" — paraphrase, not quotation
- `LONG-ARC.md:25`: "v0.2 has been architecturally committed via ADR-0005" — fine, just a pointer
- `MILESTONE.md:103`: "ADR-0001 — exploration-first architecture (binding for v0.2 implementation)" — "binding" is attribution, not in ADR-0001
- `ADR-0005:9`: "ADR-0001 commits the project to exploration-first architecture: 'multiple retrieval and ranking strategies can coexist' as a binding posture" — quotes the ADR but appends "as a binding posture" which is not in the ADR

**Proposed edits:**

`MILESTONE.md:103` — change to:
> ADR-0001 — exploration-first architecture (the architectural posture v0.2 is chosen to honor at the implementation layer)

`ADR-0005:9` — change to:
> ADR-0001 commits the project to exploration-first architecture: "multiple retrieval and ranking strategies can coexist." This ADR upgrades that capability claim to a delivery commitment — at least two shipped lens implementations — on the basis of the property audit's evidence that single-lens "interfaces" shape themselves around the lens that ships.

`LONG-ARC.md:46` — change to:
> Tournament narrowing... violates the coexistence posture ADR-0001 commits us to (capability claim about the architecture); LONG-ARC operationalizes it as a posture-to-honor at the implementation layer.

**Reasoning:** Convergent CR1 (CV D1.1, D1.3, D7.2, D8.1; SV A1, E3, D1). The team's own METHODOLOGY discipline D names rhetorical inflation as a pattern to watch. ADR-0005's structural fix (G-A3 second edit above) follows SV E3's recommendation: ADR-0005 owns the upgrade; ADR-0001 stands as warrant rather than as source.

**Note on AGENTS.md misquote:** SV D1 identified that AGENTS.md's own example (line 131) for "ADR citation must be specific" misquotes ADR-0001. **Deferred pending exemplar review** — AGENTS.md substantive content edits wait. See §4.

### G-A4. Foundation-audit closeout matrix (CR2)

**Surface:** `.planning/foundation-audit/FINDINGS.md` (extend with closeout-status section)

**Current state:** FINDINGS.md lists 12 issues + 6 implementation issues (I1-I6) marked MEDIUM-HIGH to LOW. STATE.md and Quick Task 1 records show several were resolved (I1, I3, I4, I6 via Quick Task 1; I5 partial via Phase 04.1). FINDINGS.md itself has no resolution annotations; reader cannot tell from FINDINGS.md which issues are open vs closed.

**Proposed addition (new section at bottom of FINDINGS.md):**

> ## Resolution status (added 2026-04-26 per governance audit synthesis)
>
> | Issue | Status | Resolution artifact |
> |---|---|---|
> | I1 (signal_type CHECK constraint) | RESOLVED | `.planning/quick/1-foundation-fixes-extensible-schemas-remo/1-SUMMARY.md` (alembic migration 005) |
> | I2 (flat scorer not multi-stage) | OPEN — preserved as design choice; revisit if multi-lens scoring requires multi-stage refactor | — |
> | I3 (negative demotion as implicit category inference) | RESOLVED | `.planning/quick/1-foundation-fixes-extensible-schemas-remo/1-SUMMARY.md` |
> | I4 (single enrichment record per paper) | RESOLVED | `.planning/quick/1-foundation-fixes-extensible-schemas-remo/1-SUMMARY.md` (composite enrichment PK) |
> | I5 (Open Question Q1, Q4, Q16 closures pending validation) | PARTIAL — see G-A5 (move to STATE.md tracker) | `docs/10-open-questions.md:8-11, 30-37, 103-118` |
> | I6 (OpenAlex email config missing) | RESOLVED | `.planning/quick/1-foundation-fixes-extensible-schemas-remo/1-SUMMARY.md` |
> | F1-F12 (process/documentation findings; see §3) | Mixed — see Quick Task 1 + Phase 04.1 summaries | Various |
>
> *This matrix was added retroactively per the 2026-04-26 governance audit synthesis. Future audits with cross-cutting findings should produce this matrix as part of their deliverable, not retroactively.*

**Reasoning:** Convergent CR2 (CV D5.2, D5.3; SV C3). Turns the audit document from a snapshot into a live tracker. Cost: ~30 minutes (researching each I-issue's resolution path). Logan may want to fill this in personally given the historical context.

### G-A5. Move Q1/Q4/Q16 pending-validation tracking from `docs/10` to STATE.md (CR2)

**Surface:** `.planning/STATE.md` (add follow-up section), `docs/10-open-questions.md` (annotate or cross-reference)

**Current state:** Q1, Q4, Q16 in `docs/10` are marked "resolved during implementation but pending user validation." No single live tracker says whether validation happened.

**Proposed:** Add to STATE.md a "Pending validations" section:
> ## Pending validations (carried over from foundation-audit)
> | Open Question | Closed by | Pending action | Status |
> |---|---|---|---|
> | Q1 (open question text) | Phase 3 implementation | Logan validates the closure rationale | PENDING |
> | Q4 (open question text) | Phase 4 implementation | Logan validates the closure rationale | PENDING |
> | Q16 (open question text) | Phase 04.1 implementation | Logan validates the closure rationale | PENDING |
>
> *Source: `.planning/foundation-audit/FINDINGS.md` finding I5; closures recorded in `docs/10-open-questions.md`.*

**Reasoning:** Convergent CR2 (CV D5.3; SV C3). Validation tracker belongs in the live-state document, not buried in `docs/10`. Cost: 15 minutes.

## 2. Adopt with Logan's call on shape

These have multi-audit convergence but Logan should pick the shape.

### G-B1. ECOSYSTEM-COMMENTARY status annotations (CR2 / row 5) — shape (a) inline status table or (b) explicit deprecation pointer

**Surface:** `.planning/ECOSYSTEM-COMMENTARY.md`

**Current state:** Document is dated 2026-03-11 (line 3) and honestly notes its number-staleness. But its §3-§7 recommendations don't distinguish implemented-vs-pending-vs-rejected. Reader cannot tell what's been done.

**Two shapes:**

**Shape (a) — inline status table at top of document:** Append a "Status as of 2026-04-26" section that walks each substantive recommendation (§3 resequencing, §4A-D pre-MCP fixes, §5 priorities, §6 import strategy, §7 MCP surface) and marks IMPLEMENTED / REJECTED / DEFERRED with file:line evidence. Keeps the document as live historical analysis with current annotations.

**Shape (b) — explicit deprecation pointer:** Add at top "This document is historical (2026-03-11). For current planning, see VISION.md, LONG-ARC.md, and ROADMAP.md. Recommendations from this document are reflected (or not) in those artifacts." Stops trying to keep ECOSYSTEM-COMMENTARY current.

**Recommendation:** Shape (a). Shape (b) abandons useful historical analysis. Shape (a) is ~30 minutes once and the document remains useful for understanding project history. Logan's call.

**Note:** This is also where CV D6.3 (external ecosystem currency claims) attaches — Logan may decide to add a separate "external ecosystem claims not re-verified after 2026-03-11" annotation.

### G-B2. ADR-0005 reframe of ADR-0001 commitment (CR5 / row 7) — already in G-A3 above; shape question is how aggressive

The G-A3 edit to ADR-0005:9 owns the stronger commitment. Logan could go further by adding a short "Why ADR-0001 alone isn't enough warrant" subsection to ADR-0005. **Two shapes:**

**Shape (a) — minimal:** Just the G-A3 edit (one sentence reframe in ADR-0005:9).

**Shape (b) — explicit subsection:** Add ~100-word subsection to ADR-0005's Context: "Relationship to ADR-0001. ADR-0001 says strategies can coexist (capability claim about architecture). This ADR upgrades to delivery (must coexist via shipped second implementation) on the basis of the property audit's evidence that single-lens 'interfaces' shape themselves around the lens that ships. The upgrade is this ADR's contribution, not ADR-0001's; this ADR cites ADR-0001 as the warrant for the original capability claim, not as the source of the delivery commitment."

**Recommendation:** Shape (a). The minimal reframe captures the substance; the explicit subsection is overkill given the v0.2 cycle's existing B2 disposition (ADR-0005 will get a "Considered and rejected" subsection anyway from the v0.2 synthesis Wave 3 commit). Logan's call — if Logan wants the explicit subsection, fold into the same v0.2 synthesis B2 commit.

### G-B3. v2-deferred technology-name reframe (row 11 — substantive divergence) — shape (a) capability-with-illustrative or (b) full removal

**Surface:** `.planning/REQUIREMENTS.md:141-153` (v2 Semantic Search and Advanced Enrichment sections)

**Current state:** SEMA-01 names SPECTER2 specifically; SEMA-02 names pgvector specifically; ADVN-01 names Semantic Scholar + SPECTER2 specifically. Per SV C2, this is the LONG-ARC anti-pattern "embedding-model choice as load-bearing decision" recurring at the requirements layer.

**Two shapes:**

**Shape (a) — capability-with-illustrative:** Reframe as capability requirements with named technologies as illustrative-only:
- SEMA-01: "System computes embeddings selectively for user-touched/saved papers (e.g., SPECTER2 or equivalent embedding model selected via lens-design analysis)"
- SEMA-02: "Semantic search via vector index (e.g., pgvector or equivalent) for embedded paper cohorts"
- ADVN-01: "Citation/recommendation adapter for an additional source (e.g., Semantic Scholar) — selection deferred to v3 lens-design"

**Shape (b) — full removal:** Strip the technology names entirely:
- SEMA-01: "System computes embeddings selectively for user-touched/saved papers; specific embedding model selected via lens-design analysis at v2 planning time"

**Recommendation:** Shape (a). Preserves the historical context of which technologies were the candidates at write-time while making clear the choice is deferred. Shape (b) is overcorrection (strips useful information). Logan's call.

### G-B4. Per-phase ADR-against-plan audit operationalization (SV D2 / row 13) — shape (a) document the practice or (b) propose the operational hook now

**Surface:** `.planning/LONG-ARC.md:96-103` ("What current planning must do") OR a new section in METHODOLOGY.md OR a deferral to gsd-2 uplift

**The finding:** LONG-ARC.md:101 says "Run an ADR-against-current-work audit at each deliberation boundary" — but no operational hook (when, who, what artifact). The 005-008 drift-against-ADR-0001 went uncaught for weeks because the discipline existed in spirit but not in mechanism.

**Three shapes:**

**Shape (a) — document the practice (lightweight):** Add to LONG-ARC.md:96-103 an operational sub-bullet: "Run an ADR-against-phase-plan audit at each phase-plan checkpoint, filing the artifact under `.planning/audits/<phase>-adr-audit.md`." Documents the practice; doesn't enforce.

**Shape (b) — propose the operational hook now:** Author a small ADR (ADR-0006: ADR-against-plan audit cadence) that specifies: when (before phase exit), who (independent reviewer; cross-vendor for high-stakes phases), what artifact (`.planning/audits/<phase>-adr-audit.md`), and the propagation discipline (audit findings must propagate into either phase plan, ADR amendment, or backlog before phase exit).

**Shape (c) — defer to gsd-2 uplift initiative:** This finding is precisely the kind of "long-horizon thinking integration" the gsd-2 uplift initiative is supposed to formalize. Defer to that initiative; the uplifted gsd-2 should bake ADR-against-plan audits into its phase-completion workflow as a project-agnostic capability.

**Recommendation:** Shape (c). The discipline is real and important; operationalizing it ad-hoc in arxiv-sanity-mcp now would create an arxiv-sanity-mcp-specific convention that the gsd-2 uplift would either supersede or fight. Better to let the uplift initiative design the operational hook as a project-agnostic capability. **In the meantime,** add a one-line note to LONG-ARC.md:96-103 — "ADR-against-plan audit cadence is operational-hook-pending; tracked for gsd-2 uplift integration." Keeps the gap visible without committing to a local solution. Logan's call on whether to additionally take shape (a) as an interim measure.

## 2.5. Dispositions on Adopt-with-shape items (recorded 2026-04-26)

This section records the dispositions on the four Adopt-with-shape items, including reasoning, explicit assumptions, and where-the-reasoning-may-be-wrong sections per Logan's instruction. Provenance: dispositions proposed by Claude (opus-4-7, xhigh effort) in the post-Wave-3 onboarding session 2026-04-26 after reading ECOSYSTEM-COMMENTARY.md, REQUIREMENTS.md v2 sections, ADR-0005 in current state, and the governance comparison §3. Logan reviewed and accepted them.

The original §2 above is preserved intact as the synthesis's original analysis with its original "Recommendation:" lines. §2.5 supplies the operative dispositions; one (G-B3) diverges from the original synthesis recommendation, and the divergence is documented inline.

### G-B1 — ECOSYSTEM-COMMENTARY status annotations: shape (a)-lite

**Disposition:** Add a `## Status as of 2026-04-26` section at the top of `.planning/ECOSYSTEM-COMMENTARY.md`, after the existing pre-04.1 note (lines 3-5), that does §-by-§ status (a few lines per §) — *not* the full per-recommendation table the original §2 shape (a) proposed.

**Assumptions:**

1. The doc still has load-bearing value as a rationale source. Evidence: `ROADMAP.md:142` cites `.planning/ECOSYSTEM-COMMENTARY.md §3` as the Phase-5/6 resequencing rationale. If we deprecate the doc, that citation becomes a pointer to a deprecated artifact.
2. Per-recommendation file:line citations (full §2 shape (a)) are bookkeeping that will go stale faster than the prose summary. The narrower §-by-§ status decays slower.
3. Shape (b) (deprecation pointer) loses information the author wrote about their own past thinking. The user's methodological orientation toward "traces over erasure" disfavors that move.

**Reasoning:**

- The doc's own top note (lines 3-5) **already** annotates §3-4 as implemented. The doc is partially status-annotated; the missing parts are §5-7. The original §2 framing (do the whole doc) over-scopes the actual gap.
- §5 (feature priorities): many shipped in v0.1 (multi-seed expansion, watch-based monitoring, etc.); some still open.
- §6 (cross-project import strategy): implemented in Phase 5.
- §7 (MCP v1 surface): closed by what shipped (13 tools, 4 resources, 3 prompts).
- Three short status paragraphs covering §5/§6/§7 do the work without committing to a maintenance burden.

**Diverges from §2 recommendation:** narrows the scope. §2 shape (a) is the full per-recommendation status table. §2.5 disposition is §-level status (briefer, slower-decaying). Cost differential: ~10-20 minutes either way; not large.

**Where my reasoning may be wrong:**

- If the doc is genuinely archaeological (no future reader will consult it for rationale), §2 shape (b) deprecation pointer is right and §2.5 is over-investing.
- I'm assuming `ROADMAP.md:142`'s single citation is evidence of load-bearing-ness; that's a single citation and may not be enough to establish the doc's value.
- The §-level status may itself go stale faster than I expect; if it does, future-me has to redo or remove it.

### G-B2 — ADR-0005 reframe of ADR-0001 commitment: shape (a)

**Disposition:** shape (a) — the minimal one-sentence reframe already in G-A3 (which lands in Wave 4 commit 3). No additional "Relationship to ADR-0001" subsection is added.

**Assumptions:**

1. ADR length matters for re-readability. ADRs that are scanned more get more attention; longer ADRs get less.
2. ADR-0005 is already gaining a "Considered and rejected" subsection (~150 words; landed at commit `9f19634` in Wave 3). Adding another subsection compounds the bloat.
3. Systematic interventions belong upstream (in templates / methodology), not in retrofits to a single ADR.

**Reasoning:**

- The substantive fix is "ADR-0005 owns the upgrade-from-capability-to-delivery; ADR-0001 stands as warrant rather than as source." G-A3's in-line edit at ADR-0005:9 does exactly this in the document's natural location (the Context section).
- A "Relationship to ADR-0001" subsection would elaborate but not add new substance.
- The pattern the audit caught (CR1: derivative documents inflate ADR modal verbs) is general. The right systematic intervention is in `docs/templates/` — require future ADRs that build on existing ADRs to include explicit relationship framing. That's an upstream fix that prevents recurrence; bloating ADR-0005 doesn't prevent recurrence in ADR-0006+.
- `docs/templates/` is in the comparison's joint blind spots (§5 item 2). It wasn't audited. If we want to follow this thread, that's a separate audit/edit cycle, not part of Wave 4.

**Where my reasoning may be wrong:**

- If the doctrine-relationship pattern needs to be modeled explicitly because future ADRs will build on this one, shape (b) is defensible. The template-fix path I'm leaning on may not happen in any reasonable timeframe; if it doesn't, the retrofit-via-subsection becomes more attractive.
- ADR length may matter less than I assume. Readers who care about doctrine will read carefully; the bloat concern may be aesthetic rather than functional.

### G-B3 — v2-deferred technology-name reframe: shape (c) (DIVERGES from §2 recommendation)

**Disposition:** Strip technology names from SEMA-01, SEMA-02, ADVN-01 (capability-only language). Add a separate "Historical candidates" note at the end of the v2 section recording that SPECTER2, pgvector, and Semantic Scholar were the candidates considered at write-time (2026-Q1).

**This diverges from the original §2 recommendation of shape (a).**

**Assumptions:**

1. Anchoring effects are real and this team is documented-susceptible. Evidence: the 005-008 spike chain let MiniLM become a silent default; the property audit (`.planning/audits/2026-04-25-phase-3-property-audit-opus.md`) and the multi-lens redirection deliberation are the trace of that failure.
2. Requirements docs get read at planning time; git history doesn't. What the requirement says has more weight than what the commit says.
3. Historical traces of "what was considered" have nonzero value for future planners, but should not be load-bearing on requirement language.

**Reasoning:**

- The audit finding (SV C2, adopted in synthesis comparison §3) frames this as the LONG-ARC anti-pattern "embedding-model choice as load-bearing decision" recurring at the requirements layer. That framing is the central justification for editing.
- §2 shape (a) — "e.g., SPECTER2 or equivalent" — does not actually defuse the anchoring. "e.g." is a hedge that preserves the privileged candidate. A future v2 planner reading SEMA-01 sees SPECTER2 first; their default is to start there; "or equivalent" gets noticed only if they're already thinking critically.
- The team has documented evidence (005-008) that they don't reliably think critically about silent defaults. Shape (a) is therefore a half-measure that pretends to address the anti-pattern while leaving the failure mode in place.
- §2 shape (b) (full removal) is honest but loses historical information.
- Shape (c) (capability + history-note) is honest about the requirement (it's a capability, technology-open) AND preserves the trace (the candidates considered are recorded as history, not as requirement). This is the trace-preserving move that doesn't anchor.
- Cost differential between (a) and (c): trivial. ~5 minutes either way.

**Why I diverge from the §2 recommendation:**

- §2 reasoning for (a) was that "(b) is overcorrection (strips useful information)." §2 did not consider shape (c).
- The shape (c) framing addresses both concerns (b)'s information-loss concern AND (a)'s anchoring concern, at no extra cost.

**Concrete edit shape:**

SEMA-01 becomes: "System computes embeddings selectively for user-touched/saved papers; specific embedding model selected via lens-design analysis at v2 planning time."

SEMA-02 becomes: "Semantic search via vector index for embedded paper cohorts; specific index implementation selected at v2 planning time."

ADVN-01 becomes: "Citation/recommendation adapter for an additional source beyond OpenAlex; specific source selected via lens-design analysis at v2 planning time."

After ADVN-04 (or at the end of the v2 section), add:

> **Historical candidates considered at write-time (2026-Q1):** SPECTER2 was the embedding-model candidate for SEMA-01; pgvector was the vector-index candidate for SEMA-02; Semantic Scholar was the additional-citation-source candidate for ADVN-01. Listed for context; not load-bearing on v2 planning. The technology choice is open per the LONG-ARC anti-pattern against treating embedding-model selection as architecturally load-bearing (`LONG-ARC.md:46-52`).

**Scope check:** apply only to SEMA-01, SEMA-02, ADVN-01 (the named instances of the anti-pattern). Don't touch SEMA-03/04 (already capability-only) or ADVN-02-04 (broader citation-graph candidates, not the documented embedding-model anti-pattern instance). ADVN-04's "GitHub stars" example is anti-pattern-adjacent and could be touched if a broader sweep is wanted; default scope is minimal (three requirement codes).

**Where my reasoning may be wrong:**

- My shape (c) is more work than (a) (minimally) and the anchoring concern may be overstated. The team has been more vigilant since the 005-008 cycle; shape (a) might be OK now.
- The "Historical candidates" note may itself become a silent default for future planners who read it as "these were the right answers, why are we questioning them?" That risk is mitigated by the explicit "Listed for context; not load-bearing" framing, but mitigation isn't elimination.
- I'm extrapolating from one documented failure (005-008 / MiniLM) to a general team-susceptibility-to-anchoring claim. One data point is weak evidence; the team may not actually be as susceptible as I'm framing.

### G-B4 — Per-phase ADR-against-plan audit operational hook: shape (c) with refined interim note

**Disposition:** shape (c) — defer the substantive operational design to the gsd-2 uplift. Add an interim note to LONG-ARC.md:96-103 that is explicit about the interim being honest non-commitment, not a fake discipline.

**Concrete interim note text:**

> Operational-hook status: pending. The audit cadence, ownership, and artifact format are tracked for the gsd-2 long-horizon-planning uplift to integrate as a project-agnostic workflow primitive. Until then, the discipline is self-imposed at deliberation boundaries; no specific cadence is committed.

**Assumptions:**

1. Self-discipline does not reliably operate audit cadences for this project. Evidence: the 005-008 drift took weeks to catch; the discipline existed in spirit but not in mechanism. The team's own diagnosis (LONG-ARC.md:46-52 anti-patterns; A7 mitigation in Wave 1) is that vigilance-over-mechanism recapitulates the failure.
2. gsd-2 uplift will eventually formalize this. Evidence: handoff §6 explicitly lists G-U1 (per-phase ADR-against-plan audit operational hook) as a target intervention surface for the uplift.
3. Honest "we have a gap; the long-term fix is in scope but not now" is better than fake "we have a discipline" — calibrated language as default register (LONG-ARC anti-pattern: closure pressure at every layer).

**Reasoning:**

- §2 shape (a) "document the practice" without operational hook is closure-pressure. It claims the discipline exists when the documented evidence is that the discipline doesn't reliably operate without a workflow primitive.
- §2 shape (b) "propose ADR-0006 now" commits to a local operational shape that will likely conflict with whatever the gsd-2 uplift designs. The handoff §6 framing of the uplift as project-agnostic means whatever ADR-0006 commits to may have to be unwound when the uplift designs differently.
- §2 shape (c) defers the substantive design but leaves the gap visible. Adding the interim note prevents the deferral from being silent.

**Refinement over §2's shape-(c) interim note:**

§2 proposed: "ADR-against-plan audit cadence is operational-hook-pending; tracked for gsd-2 uplift integration."

§2.5 proposes (above): "Operational-hook status: pending... Until then, the discipline is self-imposed at deliberation boundaries; no specific cadence is committed."

The §2.5 version is fully honest about the state — it explicitly says the discipline is self-imposed and no cadence is committed, rather than only flagging the operational-hook as pending. This matches the calibrated-language register the team's METHODOLOGY discipline D names.

**Risk being accepted:**

The gsd-2 uplift may take months. During that time, Phase 12-17 plans could be authored without the audit hook. Mitigation: A7 (already landed in Wave 1) operationalizes the anti-pattern watch at specific phase-boundary checkpoints (Phase 15 plan 3 + Phase 16 plan 1). That's narrower than a full ADR-against-plan audit, but it's not nothing. The remaining gap is ADR-0001/0002/0003/0004-against-plan checks at phase boundaries that don't already have A7 coverage.

**Where my reasoning may be wrong:**

- If gsd-2 uplift is much further off than the handoff implies, the cost of leaving the gap is higher and §2 shape (a) becomes more attractive as interim despite the closure-pressure concern.
- A7's coverage may be more limited than I'm framing — Phase 15 plan 3 + Phase 16 plan 1 are anti-pattern checkpoints specifically, not ADR-broadly checkpoints. The "remaining gap" may be larger than the wording above implies.
- The "self-discipline doesn't work" claim rests heavily on the 005-008 evidence. Different teams (and the same team after a bad outcome) may operate differently. The claim could be over-generalized.

### Cross-cutting: where these dispositions could be collectively wrong

- **All four dispositions assume the original synthesis (§§1-7) is broadly correct.** I did not audit the synthesis itself for whether its findings stand on the underlying audits. The single-author synthesis caveat in §10 applies to the original synthesis; I'm building on it, so any errors in §§1-7 propagate.
- **The dispositions assume Wave 4 will execute roughly as scoped.** If Wave 4 gets pre-empted (e.g., by exemplar harvest happening sooner than expected, or by gsd-2 uplift starting earlier), some dispositions may need re-revision.
- **The dispositions are single-author (Claude) plus user acceptance.** Logan accepted them but did not independently re-derive each. If Logan's acceptance was time-pressured rather than considered, dispositions may carry errors that paired review would catch. The discipline-A pattern (paired review for framing claims) was not applied to this dispositions set; if any disposition becomes contested in Wave 4 execution, paired re-read is the recommended remediation per the v0.2 synthesis §10.



Three structural changes to the governance set itself. Each is independent and could be done in any order.

### G-S1. Governance read-order map (CR3)

**Surface:** Either extension to `CLAUDE.md` Document Structure section (lines 34-44) OR a new file `.planning/READING-ORDER.md`

**The finding:** Governance set is large (15+ documents); no canonical read-order. New contributors / returning agents have no map. Per SV F1, recommended map structure:

> **For a new contributor:** PROJECT.md → VISION.md → LONG-ARC.md → ADRs (0001-0005) → AGENTS.md → ROADMAP.md → REQUIREMENTS.md → STATE.md
>
> **For an agent starting a session:** CLAUDE.md (this file) → STATE.md → relevant phase plan → AGENTS.md (if doing work that touches agent-conduct issues)
>
> **For epistemic / methodology questions:** `.planning/spikes/METHODOLOGY.md` (interpretive lenses + practice disciplines) and `.planning/foundation-audit/METHODOLOGY.md` (decision-review epistemic discipline). See [their relationship note below for scope split].
>
> **For deliberation history:** `.planning/deliberations/INDEX.md` (see G-S3).

**Recommendation:** Add to CLAUDE.md as a new section (5-7 lines). Keeps the entry point (CLAUDE.md is auto-loaded for agents) as the place where the map lives. If/when CLAUDE.md is restructured per exemplar review (§4), the map can move to a separate file.

### G-S2. Foundation-audit closeout matrix (already in G-A4)

This is structural in spirit but I've put the concrete edit in G-A4 (Adopt now). Same item, different framing.

### G-S3. Deliberation directory index

**Surface:** New file `.planning/deliberations/INDEX.md`

**The finding (SV F3):** `.planning/deliberations/` contains 14 markdown files. PROJECT.md:25 lists one as "primary active reference"; the other 13 are unindexed. New contributor / returning agent has no map for which deliberations are active vs superseded vs exploratory.

**Proposed:** A `deliberations/INDEX.md` listing each file with: date (from filename or frontmatter), title, status (active / produced-ADR / superseded / exploratory), one-line summary, and any ADR or phase plan it produced.

**Reasoning:** Cost: ~30 minutes. Yield: governance-set legibility improvement; deliberations become substrate rather than corpus.

### G-S4. Methodology-document relationship note

**Surface:** Both `.planning/foundation-audit/METHODOLOGY.md` and `.planning/spikes/METHODOLOGY.md`

**The finding (SV F2):** Two METHODOLOGY documents exist with non-trivial scope overlap; they are not in dialog with each other. Possible resolution: scope split (foundation-audit METHODOLOGY for decision-review; spikes METHODOLOGY for spike design and interpretation), but this is implicit.

**Proposed:** Add a one-paragraph "Relationship to [other METHODOLOGY]" note at the top of each, explaining the scope split and cross-referencing.

**Reasoning:** Cost: 15 minutes. Yield: makes the scope split explicit; agents/contributors learning methodology know which document to consult for what.

## 4. Deferred pending exemplar review

These are AGENTS.md / CLAUDE.md substantive content edits. Logan has noted exemplar AGENTS.md / CLAUDE.md files from other projects to harvest principles from. The right shape of these edits depends on what the harvest reveals.

### G-D1. AGENTS.md "Known difficulty patterns" section (SV A2)

**The finding:** AGENTS.md prescribes disciplines without enforcement mechanism / exit conditions / record of violations. Foundation-audit documented violations of those prescriptions; AGENTS.md was not updated in response.

**Possible directions:**
- Append a "Known difficulty patterns" section linking each prescription to documented violation patterns (foundation-audit citations)
- Add explicit revision-cadence note: "this document is updated when audit cycles surface violations"
- Move some prescriptions to a separate enforcement-rules document (if exemplars suggest this pattern)

**Why deferred:** the right structural pattern depends on what the exemplar AGENTS.md files do. Some projects co-locate prescriptions with enforcement; some separate them; some have explicit known-difficulty sections; some don't. Harvest informs.

### G-D2. AGENTS.md own ADR-citation example fix (SV D1)

**The finding:** AGENTS.md:131 example for "ADR citation must be specific" misquotes ADR-0001 ("must coexist" vs ADR's actual "can coexist").

**Possible directions:**
- Minimal fix: correct the example to match ADR-0001 text exactly
- Expand the example to demonstrate the discipline more clearly: "ADR-0001 states 'multiple retrieval and ranking strategies can coexist' — this means designing so they remain coexistable; it does not by itself prohibit shipping a single lens"
- Restructure the AGENTS.md citation-discipline section entirely (depends on exemplar review)

**Why deferred:** the minimal fix is uncontested and could land in Adopt-now if Logan wants. But it's small enough that bundling with the broader AGENTS.md restructuring (post-exemplar-review) is cleaner. Logan's call.

### G-D3. CLAUDE.md restructuring — minimal pointer or full content?

**The finding (CV D2.3, D2.1):** CLAUDE.md duplicates AGENTS.md content. CV recommends "make AGENTS.md canonical for agent conduct; make CLAUDE.md runtime-specific and minimal."

**Possible directions:**
- Demote CLAUDE.md to a thin pointer: "for agent conduct, see AGENTS.md; for live state, see STATE.md"
- Restructure CLAUDE.md as runtime-specific (claude-code session config, MCP integration notes) without duplicating AGENTS.md
- Keep CLAUDE.md as-is but prune the duplications

**Why deferred:** what counts as "runtime-specific" CLAUDE.md depends on what Logan's exemplar CLAUDE.md files do. Some projects put substantial content in CLAUDE.md (it's the auto-loaded context); some keep it minimal. Harvest informs.

### G-D4. CLAUDE.md "Stack trajectory: Not Stack D" silent-default fix (SV C1)

**The finding:** CLAUDE.md:24 reads "Stack trajectory: Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). Not Stack D." There's no definition of Stack D in CLAUDE.md; an agent reading this as runtime context sees a definite negation without context. SV C1 self-labels as "trivial but real."

**Possible directions:**
- Add a one-sentence Stack-D definition (or pointer to where it's defined)
- Remove the "Not Stack D" line entirely (the positive trajectory "A → B" is the actionable content)
- Restructure as part of broader CLAUDE.md restructuring (G-D3)

**Why deferred:** bundles cleanly with G-D3. Trivial in isolation; not worth a separate commit.

## 5. Deferred to gsd-2 uplift initiative

Two findings whose right operationalization depends on the gsd-2 uplift design.

### G-U1. Per-phase ADR-against-plan audit operational hook (SV D2)

See G-B4 above. Recommendation is shape (c) — defer to gsd-2 uplift.

### G-U2. Post-audit follow-through convention as a workflow primitive (CR2 generalization)

**The convergent risk:** prescriptive governance documents in this project don't have a documented update mechanism that triggers when audits surface violations or staleness. CR2 says a "post-audit follow-through" convention would address most of CR2's instances.

**Possible direction:** Bake post-audit follow-through into the gsd-2 uplift as a workflow primitive. When an audit produces findings, the uplift workflow surfaces those findings to the relevant prescriptive documents (AGENTS.md, CLAUDE.md, governance docs) as proposed-edits or backlog items. Without this, the convention has to be remembered each cycle — vigilance-over-mechanism (the same pattern A7 mitigates against in the v0.2 cycle).

**Why deferred:** ad-hoc local convention works for arxiv-sanity-mcp (we did the audit; we're synthesizing; we can self-impose post-audit follow-through). But for a project-agnostic uplift, this needs to be a workflow primitive, not a self-discipline. Better to design it once for the uplift and bake it in.

**Interim measure:** mark this synthesis itself as evidence that arxiv-sanity-mcp is using post-audit follow-through ad-hoc. Note in the gsd-2 uplift initiative that workflow-primitive operationalization is an outstanding requirement.

## 6. Drop / not adopting

### G-N1. ADRs 0001-0004 should enumerate alternatives (SV B1)

SV self-labels this as taste; the steelman is that posture-ADRs in their genre don't typically enumerate alternatives. ADRs 0001-0004's Notes sections already de-escalate the prescriptive register, and the alternatives in each case were essentially "the opposite of what we chose" (commit early; eager enrichment; ignore provenance; mega-search API). Adding alternatives now would be formality, not substance.

**Action:** Drop. ADRs 0001-0004 stand as-is.

### G-N2. ADR-0001 Context inheritance-rejection framing (SV B2)

SV self-labels Quality, Medium confidence, and notes "I'm reading some narrative coherence into the foundation that the team may not have perceived at the time of writing." The fix (add one sentence to ADR-0001's Notes connecting it to VISION.md positioning) is cheap but unrequested by the original ADR's audience.

**Action:** Drop unless Logan finds the framing useful. If Logan wants it, easy to add later.

### G-N3. ADRs 0002-0004 "common misuses" sections (CV D1.2)

CV recommends adding "common misuses" sections to ADRs 0002-0004 so downstream docs can't cite them for narrower decisions. The recommendation is fine but unnecessary at this point — there's no documented misuse pattern for ADRs 0002-0004 (the misuse pattern is on ADR-0001, addressed in G-A3). Adding "common misuses" without observed misuse is preemptive scope creep.

**Action:** Drop. Add later if specific misuse patterns surface.

## 7. Single-audit findings adjudicated

These are findings that appeared in only one audit; they need explicit disposition.

| Row | Finding | Adopt? | Disposition |
|---|---|---|---|
| 9 | Tool counts drift across surfaces | Yes | Bundled into G-A2 (CLAUDE.md update) |
| 10 | MCP-07 internally inconsistent (5-10 heuristic vs 13-tool test assertion) | Yes — small | Reframe MCP-07 in REQUIREMENTS.md as "tool count is justified and grouped by user intent" rather than numeric cap. **Adopt-now**, add to G-A1 commit. |
| 13 | Per-phase ADR-against-plan audit operationalization | See G-B4 (shape c) and G-U1 |
| 14 | "Not Stack D" silent default in CLAUDE.md | Defer to G-D4 (exemplar review) |
| 15 | AGENTS.md own example misquotes ADR-0001 | Defer to G-D2 (exemplar review) |
| 16 | ADR-0001 inheritance-rejection framing | Drop (G-N2) |
| 17 | ADRs 0002-0004 common-misuses sections | Drop (G-N3) |
| 18 | Status-marker discipline inconsistently used | Defer — bundles with exemplar review of AGENTS/CLAUDE which prescribe the markers |
| 19 | Phase 2 success criteria omits "seen" | Adopt small — add post-audit-correction note to ROADMAP.md Phase 2 success criteria; **bundles with G-A1 commit** |
| 20 | External ecosystem claims not verified | Note in G-B1 (ECOSYSTEM-COMMENTARY status annotation includes "external claims not re-verified after 2026-03-11") |
| 21 | VISION/LONG-ARC extend ADR-0003 coherently (positive) | No action; preserve |
| 22 | ROADMAP cites forbidden audit artifact (Property audit) as evidence for Option B | Adjust ROADMAP.md:8-10 — make ADR-0005 and the deliberation the primary live authority, with the property audit as evidence appendix. **Adopt-now**, add to G-A1 commit. |
| 23 | Two METHODOLOGY docs not in dialog | See G-S4 |
| 24 | Deliberation directory not indexed | See G-S3 |
| 25 | ADRs don't enumerate alternatives | Drop (G-N1) |

## 8. Sequencing — Wave 4 plan (governance-doc edits)

The v0.2 plan synthesis used 3 waves separated by the governance audit. This synthesis adds Wave 4 (governance-doc edits) and acknowledges the gsd-2 uplift initiative as a downstream wave.

### Wave 4 — governance-doc Adopt-now + with-shape edits (revised with dispositioned shapes)

Lands after the v0.2 synthesis Wave 3 commits land (Wave 3 touched ADR-0005, MILESTONE.md, LONG-ARC.md; Wave 3 commits 9f19634, 7614be3, 013625a are landed as of 2026-04-26). G-B-tier shapes are dispositioned per §2.5.

1. **Plan-revision commit 1 (STATE.md refresh):** G-A1 + row 19 (Phase 2 success criteria post-audit note) + row 22 (ROADMAP audit-citation reframe) + row 10 (MCP-07 reframe in REQUIREMENTS.md).
2. **Plan-revision commit 2 (CLAUDE.md minimal currency):** G-A2 only. Structural restructuring waits for exemplar review.
3. **Plan-revision commit 3 (ADR-doctrine pass + G-B4 interim note):** G-A3 — re-verify ADR citations against ADR text; touches LONG-ARC.md, MILESTONE.md, ADR-0005. Per §2.5 G-B2 disposition, G-A3's ADR-0005:9 reframe is the operative ADR-0001 reframe; no additional "Relationship to ADR-0001" subsection. Per §2.5 G-B4 disposition, also adds the interim note to LONG-ARC.md:96-103: "Operational-hook status: pending. The audit cadence, ownership, and artifact format are tracked for the gsd-2 long-horizon-planning uplift to integrate as a project-agnostic workflow primitive. Until then, the discipline is self-imposed at deliberation boundaries; no specific cadence is committed."
4. **Plan-revision commit 4 (foundation-audit closeout):** G-A4 + G-A5 — closeout matrix in FINDINGS.md; pending-validation tracker in STATE.md.
5. **Plan-revision commit 5 (ECOSYSTEM-COMMENTARY status):** G-B1 per §2.5 disposition — shape (a)-lite. Add `## Status as of 2026-04-26` section after the existing pre-04.1 note (lines 3-5) with §-by-§ status (a few lines per §) covering §5/§6/§7 specifically. NOT the full per-recommendation table.
6. **Plan-revision commit 6 (v2 tech-naming reframe):** G-B3 per §2.5 disposition — shape (c). Strip technology names from SEMA-01, SEMA-02, ADVN-01 (capability-only language). Add a separate "Historical candidates" note at the end of the v2 section recording SPECTER2/pgvector/Semantic Scholar as 2026-Q1 candidates considered. Concrete edit text in §2.5 G-B3.
7. **Plan-revision commit 7 (governance read-order map):** G-S1 (added to CLAUDE.md as a small section, even if CLAUDE.md restructuring is deferred).
8. **Plan-revision commit 8 (deliberation index):** G-S3.
9. **Plan-revision commit 9 (METHODOLOGY relationship note + M1 second-test annotation):** G-S4 + the §9 M1 annotation note.

### Wave 5 — exemplar AGENTS.md / CLAUDE.md harvest + deferred dispositions

After Logan provides exemplar AGENTS.md / CLAUDE.md from other projects:

10. **Exemplar harvest** — separate session; abstracts principles; produces a recommendations doc.
11. **Wave 4 synthesis revision** — like the v0.2 synthesis revision: incorporate exemplar findings; confirm AGENTS.md / CLAUDE.md dispositions (G-D1 through G-D4).
12. **Plan-revision commits** for AGENTS.md / CLAUDE.md restructuring per the revised dispositions.

### Wave 6+ — gsd-2 uplift initiative

Out of scope for this synthesis. Picks up G-U1, G-U2, and the broader gsd-2 uplift design (see handoff document for the full mid-horizon framing).

### Cross-wave: Wave 3 of v0.2 synthesis vs Wave 4 of governance synthesis — ordering

There's overlap: v0.2 synthesis Wave 3 touches ADR-0005 (B2 Considered-and-rejected subsection; per G-B2 above, possibly extended) and LONG-ARC.md (B1 semantic-lens non-decision; D2 explicit-confirmation seam). Governance synthesis Wave 4 also touches ADR-0005 (G-A3 reframe) and LONG-ARC.md (G-A3 doctrine pass).

**Recommended order:** v0.2 Wave 3 lands first (its commits are scoped to v0.2 plan revisions; lower entropy). Then governance Wave 4 lands. The v0.2 cycle's Wave 3 commits don't conflict with governance Wave 4's edits; they touch different parts of the documents.

## 9. M1 status update

Comparison §4 documented that this paired audit cycle's structural divergence + substance convergence pattern reinforces M1's Hypothesis status. M1 should remain `Hypothesis` (single comparison reinforces but does not confirm). Recommended action: add to M1's METHODOLOGY.md entry (which was added 020b5d1) a one-line note that the 2026-04-26 governance audit cycle is the second test case and reinforced the discipline; status remains Hypothesis until further cycles either reinforce or weaken.

**Edit shape (METHODOLOGY.md:112 extension):**
> *2026-04-26 update:* Second test of this discipline (governance-doc paired audit cycle, dispatched 2026-04-26 with M1's forbidden-reading list applied) produced the structural-divergence / substance-convergence pattern paired audits are supposed to produce — see `.planning/audits/2026-04-26-governance-audit-comparison.md` §4. Status remains Hypothesis pending further cycles.

**Sequencing:** add to Wave 4 commit 1 or as its own small commit at the end of Wave 4.

## 10. What this synthesis does not commit

- **Does not modify any audit-target document.** This is a synthesis; the actual edits are downstream commits.
- **Does not adjudicate the AGENTS.md / CLAUDE.md substantive structural questions.** Those are deferred pending exemplar review (§4).
- **Does not pre-empt the gsd-2 uplift initiative.** Two findings (G-U1, G-U2) are explicitly deferred to that initiative; other findings may also touch its scope.
- **Does not address joint blind spots** (comparison §5). Those are scope-acknowledgments, not actionable findings here.
- **Does not constitute a paired-review cycle on itself.** This synthesis is single-author. If any of its dispositions become contested, the discipline-A pattern recommends a paired re-read of the synthesis before commit. The fact that the v0.2 synthesis revision flipped multiple dispositions on re-read is evidence that single-author synthesis is fallible.
- **Does not commit Logan's call on the four Adopt-with-shape items.** Those need Logan's explicit disposition before Wave 4 commits land.
