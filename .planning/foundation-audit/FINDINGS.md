# Foundation Audit — Findings

Working scratch pad for issues identified, methodology applied, and verdicts rendered.
See METHODOLOGY.md for the justification framework applied throughout.

## Audit Scope

Reviewing the epistemic integrity of:
1. Roadmap structural changes (3 changes from docs/09 → .planning/ROADMAP.md)
2. Requirements extraction (47 requirements from Draft design docs)
3. Phase 3-4 CONTEXT.md (AI-inferred, unvalidated)
4. ADRs 0001-0004 (self-accepted)

---

## 1. Roadmap Structural Changes

### 1A. Interest Modeling & Ranking inserted as Phase 3

**Claim**: Interest modeling and ranking deserve their own phase, separated from workflow state (Phase 2).

**Evidence**:
- [STRUCTURAL] docs/09-roadmap.md Phase 2 originally bundled "workflow-state primitives" which included interest modeling
- [STRUCTURAL] REQUIREMENTS.md has distinct requirement groups: WKFL-01..08 (workflow) vs INTR-01..06 + RANK-01..03 (interest/ranking)
- [INFERENTIAL] Interest profiles consume workflow objects (saved queries, collections) so must come after, not during
- [INFERENTIAL] Ranking is a distinct subsystem (scorer pipeline, explanation assembly) unlike CRUD workflow operations

**Alternatives considered**:
- (a) Keep interest modeling in Phase 2 as originally designed → Phase 2 becomes very large (8 WKFL + 6 INTR + 3 RANK = 17 requirements in one phase). Execution risk: oversized phase.
- (b) Split interest modeling into Phase 2 (signals) + Phase 3 (ranking) → Artificial split of tightly coupled concerns
- (c) Current choice: separate phase for INTR + RANK after workflow state → Clean dependency: Phase 2 provides workflow objects that Phase 3's interest signals reference

**Sensitivity**: **Load-bearing** structurally, but the code exists and works. The dependency direction (interest profiles reference saved queries and collections) is verified in the codebase.

**Inference chain**:
```
docs/09 bundles interest+workflow → requirements are actually separable (WKFL vs INTR/RANK)
→ interest signals depend on workflow objects → must come after → separate phase is cleaner
```
Weakest link: "separate phase is cleaner" is a judgment call, not a necessity.

**Verdict**: **Reasonable but under-justified** [MODERATE]
The separation is sound (dependency direction is real), but the decision to make it a full phase rather than a sub-phase of Phase 2 was a scoping judgment made without user input. Result is defensible but should have been flagged as an AI structuring decision.

---

### 1B. MCP resequenced from Phase 4 → Phase 6

**Claim**: MCP integration should be the final phase, wiring up all services.

**Evidence**:
- [STRUCTURAL] MCP tools need to expose search, workflow, interest, enrichment, and content services — all must exist first
- [STRUCTURAL] docs/09-roadmap.md Phase 4 "MCP v1" originally came after only metadata + workflow + enrichment, before content normalization
- [ANALOGICAL] "Wire up the API last" is a common backend pattern
- [INFERENTIAL] Building MCP incrementally was the alternative not considered

**Alternatives considered**:
- (a) MCP as Phase 4 (original position) → Usable MCP surface earlier
- (b) Incremental MCP (thin layer after Phase 2, extended each phase) → Earlier feedback, more integration testing
- (c) MCP last (current) → Clean single implementation but no MCP usage until everything is built

**Sensitivity**: **Load-bearing**. The project's stated purpose is "MCP-native research discovery substrate." Delaying MCP to Phase 6 means the core product identity isn't testable until the very end.

**Inference chain**:
```
MCP needs all services → build services first → MCP last
```
Weakest link: "MCP needs ALL services" is false. MCP could expose partial functionality. The original roadmap had exactly this approach.

**Verdict**: **Suspect** [LOW]
The "build everything then wire up" approach contradicts the project's MCP-native identity. The resequencing optimized for implementation convenience over product validation.

**Possible remediation**:
- Option A: Restore MCP to original Phase 4 position, extend in Phase 6
- Option B: Insert thin MCP phase exposing existing services before Phase 5
- Option C: Accept current sequencing but document the trade-off

---

### 1C. Phases 7-8 dropped from v1

**Claim**: Hardening and advanced features are v2 scope.

**Evidence**:
- [STRUCTURAL] Phase 7 = error recovery, rate limits, caching, monitoring. Phase 8 = semantic experiments, cross-corpus, collaborative features.
- [STRUCTURAL] Semantic search explicitly deferred to v2 in REQUIREMENTS.md

**Sensitivity**: **Adjustable**. Neither is architecturally load-bearing for v1.

**Verdict**: **Well-grounded** [HIGH]
Standard scope management. Core features first. Semantic search deferral is explicitly user-aligned (project CLAUDE.md).

---

## 2. Requirements Extraction

### Methodology Applied
Compared each requirement against its traceable source passages in docs/01-09. Looked for hedging language ("candidate", "possible", "working hypothesis", "could", "examples") converted to firm specifications ("User CAN", "System MUST").

### High Severity

#### CONT-05 — Multi-backend parsing as firm requirement
- **Requirement**: "System supports multiple parsing backends behind a common interface (Docling, Marker, GROBID)"
- **Source** (doc 07, §10): "**Working hypothesis:** support multiple backends behind one content-normalization interface."
- **Verdict**: **Category error (clear)** [UNGROUNDED as a requirement]. Source explicitly labels this a "working hypothesis." Three integration surfaces is the most expensive CONT requirement. ADR-0002 (lazy enrichment) would argue for one backend behind an extensible interface.
- **Sensitivity**: High. If wrong, means building three integrations when one suffices for v1.

#### CONT-04 — Content acquisition as strict priority chain
- **Requirement**: "Content variant acquisition follows source-aware priority: abstract → arXiv HTML → source → PDF"
- **Source** (doc 07, §9): Ranked preference list with per-tier caveats ("when available", "when the source is clean", "for some works"). Also silently drops tier 4 (OpenAlex GROBID XML).
- **Verdict**: **Category error (moderate)**. Preference heuristic with caveats → rigid specification. Drops a tier without noting it.
- **Sensitivity**: Medium. May prevent context-appropriate ordering.

### Moderate Severity

#### MCP-05 — Specific prompt names as deliverables
- **Requirement**: "MCP server exposes reusable prompts: daily-digest, literature-map-from-seeds, triage-shortlist"
- **Source** (doc 06, §5): "Prompts can package common higher-level workflows. **Examples:**..." §8 frames entire section as "still only a **hypothesis**." §10 explicitly lists "Which prompts are genuinely reusable?" as an **open question**.
- **Verdict**: **Category error (moderate)**. Freezes example names as deliverables while source has an open question about which prompts are reusable.

#### MCP-07 — Tool count cap
- **Requirement**: "MCP tool set stays at 5-10 tools maximum to limit context token cost"
- **Source**: No traceable source passage in any design document.
- **Verdict**: **AI-invented** [UNGROUNDED]. Sensible MCP design guidance but not a project requirement. Should be a design heuristic.

#### INTR-04 — Followed authors as firm signal type
- **Requirement**: "Interest profiles support followed authors as signals"
- **Source** (doc 02, §2): "**Possible** explicit signal types include: ... followed authors ..." (doc 06, §4): Listed under "Examples only, not final."
- **Verdict**: **Category error (moderate)**. "Possible" signal type → firm v1 requirement. Requires author entity modeling.

#### INTR-05 — Negative examples as firm signal type
- **Requirement**: "Interest profiles support negative examples"
- **Source** (doc 02, §2): Same "Possible" list. (doc 05, §2): "**for example**: ... negative examples."
- **Verdict**: **Category error (minor-to-moderate)**. Same pattern, but negative examples are more naturally inherent to interest modeling.

### Lower Severity

#### SRCH-05 — Narrowed to lexical only
- **Source** (doc 01): "multiple notions of relatedness." Docs emphasize multi-modal.
- **Verdict**: Defensible v1 scoping but should say "chosen for now" not "requirement."

#### WKFL-03 — Dropped "seen" triage state
- **Source** (doc 06, §6): Lists six states including "seen." Requirement has five, drops "seen."
- **Verdict**: Silent data loss. "Seen but not triaged" vs "never encountered" matters for delta/watch.

#### RANK-02 — Dropped 2 of 7 signal types without note
- **Source** (doc 02, §5): 7 signal types. Requirement has 5, drops citation and popularity signals.
- **Verdict**: Defensible scoping but should document what was deferred.

#### CONT-02 — Internal tension with CONT-05
- Models 4 content variant types but omits TEI/XML, which is the native GROBID output format that CONT-05 requires supporting.

---

## 3. Phase 3-4 CONTEXT.md

### Cross-Cutting Process Findings

#### Finding A: Open Questions resolved without user input
Phase 4 CONTEXT.md closes at least two items from `docs/10-open-questions.md`:
- **Q4** ("Should OpenAlex be considered core?") → answered "Yes"
- **Q16** (enrichment strategy: demand-driven vs cohort-based vs budget-constrained vs two-phase) → answered "demand-driven only"

Both were explicitly marked as "intentionally unresolved" in user-authored docs. Answers chosen are defensible, but the pattern of AI-closing user-designated open questions is a process concern.

#### Finding B: ADRs cited as authority beyond their scope
- ADR-0001 (exploration-first architecture posture) cited to justify specific UX behavior: "negative examples must be soft demotions, not hard filters" (Phase 3)
- ADR-0002 (cost posture) cited to justify no cascading enrichment (Phase 4)

In both cases the ADR text doesn't actually address the specific decision. This stretches ADR authority and may prevent future questioning of decisions that appear to have "ADR backing."

#### Finding C: Speculative product strategy in CONTEXT files
Phase 3 CONTEXT includes a "donation model precedent" section speculating about monetization and investment priorities. No project document discusses revenue or donations. This is AI-fabricated product strategy that shouldn't appear as implementation context.

### Phase 3 Decisions

| Decision | Evidence | Type | Sensitivity | Verdict |
|----------|----------|------|-------------|---------|
| 4 signal types (seed_papers, saved_queries, followed_authors, negative_examples) | Strong — enumerated in docs 02, 03, 05 | Technical | Low | Well-grounded |
| Negative examples as soft demotions only | Weak — ADR-0001 stretched beyond scope | **Product (needs user)** | Moderate | Should have been discussed |
| System suggestions require user confirmation | Strong — PROJECT.md Out of Scope, doc 02 | Technical | Low | Well-grounded |
| 5-signal ranking pipeline (from 7 in docs) | Mixed — 2 signals deferred (citation, popularity) | Technical | Low | Defensible |
| 19-command CLI structure | Follows established codebase patterns | Technical | Low | Fine |
| Donation model / investment priorities | None — AI-fabricated | **Product (needs user)** | Low | Should not appear |

### Phase 4 Decisions

| Decision | Evidence | Type | Sensitivity | Verdict |
|----------|----------|------|-------------|---------|
| OpenAlex as only enrichment source | Strong but closes open Q4 | Borderline | Low | Should have been surfaced |
| Demand-driven only (no background jobs) | Moderate but closes open Q16 | Borderline | Low-Moderate | Should have been surfaced |
| Separate PaperEnrichment table | Sound technical reasoning | Technical | Low | Well-grounded |
| 7-day enrichment cooldown | No source (arbitrary, configurable) | Technical | Low | Fine |
| DOI construction as 10.48550/arXiv.{id} | Factually correct | Technical | Low | Correct |
| No cascading enrichment | Weak — ADR-0002 stretched | Product (borderline) | Low | Defensible |
| Adapter protocol interface | Follows ADR-0001 principle | Technical | Low | Well-grounded |

### Implementation Alignment
Despite process concerns, verification reports show implemented code is well-structured, well-tested, and aligned with core values (explicit interest modeling, structured explanations, provenance, cost-awareness). The issues are primarily about **who should have made the decision**, not about **the decisions themselves being wrong**.

---

## 4. ADRs 0001-0004

All four ADRs are **architectural posture documents** — meta-decisions about how to approach design rather than specific technical commitments.

| ADR | Content | Verdict |
|-----|---------|---------|
| 0001: Exploration-first | Multiple strategies coexist; interest state not reduced to tags; unresolved questions documented | **Well-grounded** — conservative, appropriate for early-stage. No irreversible commitments. |
| 0002: Metadata-first, lazy enrichment | Eager metadata, lazy everything else | **Well-grounded** — grounded in doc 02 §7. Notes correctly state it doesn't prohibit broader enrichment later. |
| 0003: License and provenance first | All artifacts record source, path, rights | **Well-grounded** — grounded in doc 07. Legally prudent, non-controversial. |
| 0004: MCP as workflow substrate | Workflow objects, not mega-search; tools + resources + prompts | **Well-grounded** — grounded in doc 06 Option D analysis. Formalizes existing trajectory. |

**Concern**: Not with the ADRs themselves, but with how downstream CONTEXT files cite them as authority for decisions the ADRs don't actually make (see Finding B above).

---

## Synthesis

### Issues by Severity

**Must address before continuing:**
1. **MCP sequencing** (1B) — Suspect. Contradicts project identity. Needs a deliberate decision on whether to insert earlier MCP exposure.

**Should address (epistemic hygiene):**
2. **CONT-05** — "Working hypothesis" treated as firm requirement. Recommend downgrade: one backend behind extensible interface for v1.
3. **Open question closures** (Q4, Q16) — Process fix: establish that closing items from docs/10 requires surfacing to user.
4. **ADR scope creep** — Process fix: ADR citations in CONTEXT files should quote the specific clause, not just the number.
5. **Negative examples as soft-only** — Product decision made without user. Reversible but should be confirmed.

**Document and move on:**
6. **1A** (Interest modeling as Phase 3) — Reasonable, document as AI structuring decision.
7. **CONT-04** — Soften to "preferred order" with noted deferrals.
8. **WKFL-03** — Note the missing "seen" state.
9. **MCP-05, MCP-07** — Reframe as provisional/heuristic.
10. **INTR-04** — Note as "possible" signal type, not firm requirement.
11. **Speculative product strategy** — Remove from CONTEXT files.
12. **All requirement narrowings** (SRCH-05, RANK-02, CONT-02) — Annotate what was deferred.

### What's Actually Wrong

The initial audit concluded "technically sound, just process debt." Adversarial stress-testing **broke that claim**. The code is competently written and well-tested, but the AI-inferred CONTEXT files made consequential product decisions that the user's own documents explicitly wanted to keep open. The implementation is opinionated in ways the design docs warned against.

**Implementation issues (not just process):**

#### I1. Four signal types hardcoded into DB schema [MEDIUM-HIGH]
CHECK constraint in migration 003 enforces exactly `seed_paper`, `saved_query`, `followed_author`, `negative_example`. Design docs listed 9-10 candidate types (including tags, weighted tags, followed topics, project workspaces, temporary session interests). Adding a new type requires: Alembic migration + changes in `signals.py`, `ranking.py`, `suggestions.py`. This resolved Open Question Q1 without user input.

#### I2. Flat weighted-sum scorer, not multi-stage pipeline [MEDIUM]
Doc 05 §8 described a 5-stage pipeline (generate → filter → rerank → diversify → explain). Built: single `score_paper()` weighted sum. No diversification stage exists. Category overlap is triple-counted: once via `score_category_overlap` (0.15), once as 60% of `score_seed_relation` (effective 0.15), once as 50% of `score_profile_match` (effective 0.075). Total effective category weight: ~0.375. Arbitrary sub-weights (60/40, 50/35/15) and top-level weights (0.35/0.25/0.15/0.15/0.10) define the product experience and were never discussed.

#### I3. Negative demotion expands implicit inference [MEDIUM]
`apply_negative_demotion` demotes by category overlap, not just direct paper matching. Marking one cs.AI paper as negative demotes ALL cs.AI papers. This is implicit interest inference — precisely what doc 02 and ADR-0001 warn against ("explicit > implicit", "exploration-first").

#### I4. Single enrichment record per paper blocks multi-source [MEDIUM]
`PaperEnrichment` PK is `arxiv_id` alone. Cannot store both OpenAlex and Semantic Scholar data for the same paper — second source overwrites first. The adapter Protocol looks extensible but the schema underneath isn't. Multi-source enrichment (the design intent) is architecturally blocked.

#### I5. Three Open Questions resolved in code without user [HIGH — process]
- Q1 (interest state model) → four signal types
- Q4 (OpenAlex as core) → yes, only source
- Q16 (enrichment strategy) → demand-driven only
AGENTS.md: "do not collapse open questions into hidden code assumptions." All three had multiple candidate answers the user never evaluated.

#### I6. Missing openalex_email setting [LOW]
CONTEXT specified polite pool access via email. Implementation has no `openalex_email` config. Rate limit default (5 req/s) exceeds anonymous pool (1 req/s), guaranteeing 429 errors.

**Process issues (still relevant):**
- Category errors in requirements extraction (exploratory → firm)
- ADRs cited beyond their actual scope
- Speculative product strategy in CONTEXT files
- MCP sequencing contradicts project identity

**Bottom line:** The code is competently built. But "competently built to the wrong spec" is a different problem than "process debt." The spec itself (CONTEXT.md files) contains product opinions the user never made.
