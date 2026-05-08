---
type: orchestrator-synthesis
status: revised — post-adversarial-review; for Logan disposition
date: 2026-05-01
audience: Logan (orchestrator-disposition)
supersedes: SYNTHESIS-DRAFT.md (this directory)
adversarial_review_input: audit-findings-A.md (this directory; 1 blocking + 11 quality + 1 absence-of-finding)
inputs:
  - CODEBASE-MAP.md (409 lines; same-dir; authored by gsd-codebase-mapper agent)
  - GSD-2-UPLIFT-MAP.md (594 lines; same-dir; authored by general-purpose Opus 4.7 1M-context agent)
  - AGENTIAL-SETUP-AUDIT.md (659 lines; same-dir; authored by Sonnet 4.5 explore-class agent)
  - GSD-2 external research (general-purpose agent + WebSearch + Bash)
  - Direct reads: CLAUDE.md, AGENTS.md, LONG-ARC.md, VISION.md, PROJECT.md, STATE.md, ROADMAP.md, RELATIONSHIP-TO-PARENT.md, ADR-0005
single_author_chain_caveat: |
  This synthesis was authored by Claude Opus 4.7 in a single session as orchestrator
  of four parallel investigations. The author of the synthesis is the same author
  who designed the four investigation specs. The four investigations are themselves
  single-author single-pass reads. Citations to upstream investigations (e.g.,
  "per CODEBASE-MAP §X") propagate single-reader claims; per LONG-ARC.md:61, factual
  claims sourced to investigations are checkable against the codebase / harness in
  seconds and should be re-verified before any disposition rests on them.
  This caveat applies to every numbered citation below.
revisions_from_draft: |
  Per audit-findings-A.md: §0.2 "thin" softened (F-1); §1.2 "blockers" reframed as
  "live risks under (V'.a) mitigation" (F-8); §0 obs 1 reconciled with §3.3 (F-10);
  §6.4 GSD-2 staging marked as test-case-stipulation-contingent (F-5); §8.1 split
  into ergonomic-config vs doctrine-layer-deliberation-boundary tiers (F-4 BLOCKING);
  I-4 Phase-12 scope-additions marked as candidate-for-Phase-12-plan-deliberation
  not pre-decisions (F-6); cost labels marked as `[chosen for now]` cost-vibes
  (F-7); §7/§8/§9 enumerations marked as bring-your-own-prioritization (F-9);
  §10/I-11 fifth option (e) "Defer all interventions; resume (V'.a) Step 3 as
  planned; revisit in 2 weeks" added (F-3); §11 reviewer-asks extended with
  methodology-fit (F-12). F-2 (option-space construction) addressed by softening
  reading (b) marker. F-11 (single-author chain) addressed by frontmatter caveat
  + per-citation marker convention.
logan_disposition: |
  2026-05-01 — extraction (the corrected disposition went past option (e) to
  extraction-of-uplift; this audit is one of the closure-pressure-recurrence-
  at-meta-level events that informed that disposition). Note added 2026-05-08
  during pre-extraction commit per the 2026-05-01 extraction-planning handoff
  (.planning/handoffs/2026-05-01-extraction-planning-handoff.md). Audit STAYS
  in arxiv-sanity-mcp; new repo cites by reference per .planning/extraction/
  EXTRACTION-LOG.md.
---

# Orchestrator Audit Synthesis — Final (Post-Adversarial-Review)

This synthesis is the revised output after adversarial review. It surfaces findings, brainstorms options, and proposes interventions scoped by milestone — but it does not dispose. Disposition is Logan's per the standing in-session-collaboration discipline (D5a; per RELATIONSHIP-TO-PARENT.md §1.1; per the disposition discipline in INITIATIVE.md §0).

**A "defer all interventions; resume (V'.a) Step 3; revisit in two weeks" option is a first-class disposition (per §10 reading e).** It is included not as a fallback but as a genuine candidate.

---

## §0. Executive frame (read first)

Three observations are load-bearing for everything that follows. Each carries a calibration note.

**1. The arxiv-sanity-mcp product is healthy as a v0.1 codebase but has not yet authored the Phase 12 plan that would translate ADR-0005's commitments into action.** The codebase shipped 2026-03-14 is single-implementation across the full surface — `grep -rn "lens|Lens" src/` returns zero matches, single-numeric `score` flows through `SearchResult` / pagination cursor / ranking pipeline (per CODEBASE-MAP §7; single-author Opus pass). The profile primitive (migration 005 + `InterestProfile.weights` JSONB at `db/models.py:353`) is intentionally extensible; everything downstream of it is not. **Calibration:** the codebase is no more or less ready than it was on 2026-04-25 when the property audit (`audits/2026-04-25-phase-3-property-audit-opus.md`) reached the same finding; nothing has regressed. What is missing is the Phase 12 plan that would translate readiness to action. Per ROADMAP, Phase 12 is 3 plans; planning it would resolve the readiness gap.

**2. The agential-development setup is asymmetrically thin relative to doctrinal density.** Doctrine is rich (CLAUDE.md, AGENTS.md, LONG-ARC.md, VISION.md, spike METHODOLOGY, foundation-audit METHODOLOGY, paired-review M1, 14-row failure-mode taxonomy in `cheerful-forging-galaxy.md` §0.6, framing-widening §9 17-item deferred items log, etc.). Harness is partly-working (12 hooks active, postlude landing 312 rows, prompt-injection scanner on `.planning/` writes, context monitor at 35%/25%, push notifications, statusline, vendored GSD framework v1.22.4) but not enforcing the project-specific disciplines: no `.mcp.json` (only `sequential-thinking` MCP loaded), no PostgreSQL/SQLite MCP despite database-backed architecture, no project-specific slash command for the dominant paired-audit pattern, project-local agents not customized to project anti-patterns, doctrine load-points fire only by Claude reading CLAUDE.md and remembering, postlude metadata stub-fielded (`error_rate` / `direction_change` / `destructive_event` all `downstream_live_wiring_not_shipped`), broken doctrine path references (CLAUDE.md cites `LONG-ARC.md` as bare basename; actual path is `.planning/LONG-ARC.md`). **Calibration:** the harness is doing real work; the gap is in *project-specific* enforcement, not generic enforcement.

**3. The repo is currently hosting two distinct projects.** `arxiv-sanity-mcp` (the product) is paused — last code commit 2026-03-14, Phase 12 plan-1 authoring **explicitly on hold per STATE.md:210** pending uplift findings. `.planning/gsd-2-uplift/` (a methodology research initiative whose stated goal is to make the gsd-2 substrate "the best it possibly can be across longer and longer development horizons" — INITIATIVE.md:42) is consuming nearly all recent activity (50+ commits in ~6 days). The trajectory plan calls for the uplift to extract to its own repo at Phase G; that repo does not yet exist, and Phase G is gated on Phases D/E/F (none complete under the (V'.a) replan).

These three frame the question Logan posed: **what should we *do* about this state?** The first-class answers include "nothing right now" (per §10 reading e).

---

## §1. Where we are

### §1.1 The product (arxiv-sanity-mcp)

Per CODEBASE-MAP and direct reads (single-author Opus pass; verifiable in seconds):

| Dimension | State |
|---|---|
| Last code commit | 2026-03-14 (Phase 10 complete, v0.1.0 tag) |
| MCP surface | 13 tools, 4 resources, 3 prompts (`src/arxiv_mcp/mcp/`) |
| Test count | 487 `def test_` matches across 51 files |
| Database | PostgreSQL via SQLAlchemy 2.0 async; 8 alembic migrations |
| Architecture | Single-lens-by-accident (no `Lens` abstraction in `src/`) |
| Active branch | `spike/001-volume-filtering` — recent commits all gsd-2-uplift documentation |
| ADRs | 4 accepted (0001 exploration-first; 0002 metadata-first lazy enrichment; 0003 license + provenance; 0004 MCP as workflow substrate; 0005 multi-lens v0.2 substrate) |
| v0.2 phases | 12-17 authored in ROADMAP.md; 0/15 plans started |

### §1.2 The methodology research (gsd-2-uplift)

Per GSD-2-UPLIFT-MAP (single-author Opus 4.7 1M-context pass; verifiable):

| Dimension | State |
|---|---|
| Initiative scope | `gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions` jointly (INITIATIVE.md:44) |
| Test-case framing | arxiv-sanity-mcp is *a* spike-intensive test case; **stipulated, not observed** per RELATIONSHIP-TO-PARENT.md §1.1 — loosenable per framing-widening §9 |
| Current phase | Phase D under (V'.a) replan; mid-Step 3 (audit-spec drafting via cross-vendor codex; Claude parallel-skeleton authored blind for differential calibration) |
| Audits to date | 7 audit folders in `gsd-2-uplift/audits/` + 8+ in `.planning/audits/`; paired-vendor pattern dominant |
| Methodology artifacts | 14-row failure-mode taxonomy; framing-widening (R1-R5; six-context; four-act); premise-bleed audit-arc; B-strong protocol; point-of-use foregrounding; frame-revision-check; methodology-question-shape-mismatch; etc. |
| Migration plan | Phase G extracts artifacts to dedicated repo; 17-row artifact-by-artifact MOVE/STAY/DUPLICATE table |
| Dedicated repo | Does not exist yet |
| Live risks under (V'.a) mitigation (NOT blockers) | Closure-pressure-into-elaboration recurrence (per STATE.md `stopped_at:` — "live risk under (V'.a), not resolved one"); D5a in-session-collaboration risk compounding without independent break since Phase A audit (2026-04-29). The (V'.a) Step 3 audit-of-audit infrastructure (B-strong protocol; SPEC-DRAFTING-BRIEF + AUDIT-SPEC + CLAUDE-PARALLEL-SKELETON) is the active framework addressing these. |

### §1.3 The agential-development setup

Per AGENTIAL-SETUP-AUDIT (Sonnet 4.5 explore-class pass; verifiable):

| Surface | State |
|---|---|
| Project `.mcp.json` | None. Only `sequential-thinking` MCP loaded. Globally available (unloaded here): serena, context7, philpapers, zlibrary, tavily, morphllm-fast-apply |
| PostgreSQL/SQLite MCP | None configured anywhere despite database-backed architecture |
| Project-local hooks | 2 (gsd-check-update, gsd-context-monitor); 4 of 12 active hooks are no-ops because `.planning/config.json` doesn't opt in to `community: true` / `workflow_guard: true` |
| Project-local slash commands | 32 GSD-default commands, none customized; **no command for the dominant paired-audit pattern** |
| Project-local custom agents | 12 GSD-default agents, none customized; none reference the 7 specific anti-patterns at LONG-ARC.md:46-54 |
| Doctrine load-points | 7 trigger→doc routings in CLAUDE.md, fired only by Claude-reads-and-remembers; no harness wiring |
| Postlude metadata | 312 rows landed; `error_rate` / `direction_change` / `destructive_event` all `downstream_live_wiring_not_shipped` |
| Memory entries | 7 (5 feedback + 1 reference + 1 index); `feedback_no_explore_for_audits.md` is high-value (caught a near-miss roadmap framing failure); 4 of 7 are 32-44 days old |
| Doctrine path references | LONG-ARC.md / VISION.md / PROJECT.md cited as bare basenames in CLAUDE.md and AGENTS.md, but live at `.planning/` — broken for fresh-session cold reads |

### §1.4 The external GSD-2 tool

Per GSD-2 external research (general-purpose agent + WebSearch + Bash; mature-repo verified):

| Dimension | State |
|---|---|
| URL | https://github.com/gsd-build/gsd-2 |
| NPM | `gsd-pi` (install: `npm install -g gsd-pi@latest`) |
| Version | v2.78.1 (115 releases, 4,784 commits, ~7,000 stars) |
| Architecture | Standalone CLI built on Pi SDK with programmatic agent-harness control (NOT v1's slash-command framework) |
| State storage | SQLite DB authoritative; `.gsd/` markdown is projection |
| Distinguishing features | Worktree isolation, crash recovery, cost/token ledger, stuck detection, auto-advance, extension framework |
| Migration tool | `/gsd migrate [path]` parses v1 `.planning/` shape; reads decimal phases |
| Logan's local copy | `/home/rookslog/workspace/projects/gsd-2-explore/` on `phase-d-decision-trace-spike` branch |
| GSDR (current) → GSD-2 | **No documented migration path**; GSDR (Logan's fork of v1) has signal tracking, spike workflow, knowledge base, reflection, deliberate, audit, health-check that GSD-2 does not yet have |

---

## §2. Where we are going (per stated commitments)

### §2.1 Product trajectory (per VISION.md, LONG-ARC.md, ADR-0005 — direct reads)

Multi-lens MCP-native research-discovery substrate for AI/CS/ML researchers, durable across years of practice. Multi-lens is the central architectural commitment ("no single retrieval lens can serve practicing AI research" — VISION.md:36). Bundle-of-signals profile primitive. Longitudinal memory across sessions. Per-lens provenance and explanation. Steerable, intersection-able, lens-disagreement-as-signal. v0.2 ships ≥2 lenses (semantic + citation/community) as the validation discipline for the abstraction (ADR-0005 §"Decision").

### §2.2 Substrate trajectory (per gsd-2-uplift artifacts; framing stipulated-not-observed)

Per `gsd-2-uplift/INITIATIVE.md:42`, the goal is to "uplift GSD-2 to be the best it possibly can be across longer and longer development horizons." Per EXTERNAL-VISION-CONTEXT.md:54, the project-shape is "an identity-preserving, pressure-respecting uplift of gsd-2 that pushes its limits in reasonable ways toward a set of reasonable objectives — discovered and refined through exploration, anchored against concrete test cases." The initiative is staged at `.planning/gsd-2-uplift/` with explicit migration trigger to a dedicated repo (Phase G of trajectory plan). **The test-case-vs-substrate framing (RELATIONSHIP-TO-PARENT.md §1) is itself stipulated, not observed (RELATIONSHIP-TO-PARENT.md §1.1).**

### §2.3 The sequencing tension

STATE.md:210:
> Phase 12 plan 1 authoring (on hold pending gsd-2 uplift first-wave findings + incubation checkpoint)

The product is gated on substrate evaluation. Substrate evaluation is gated on Phase D mapping-shape execution. Phase D mapping-shape is gated on (V'.a) Step 3 audit dispatch + disposition + Steps 4-5. Phases E/F are downstream. Phase G migration is downstream of E/F.

This sequencing is the load-bearing structural fact behind every disposition option in §6 below.

### §2.4 What v0.2 needs the codebase to displace

| Misalignment | Evidence | Phase to address |
|---|---|---|
| No `Lens` abstraction anywhere | `grep -rn "lens\|Lens" src/` → 0 matches | 12 |
| `SearchResult.score: float \| None` (single numeric) | `models/paper.py:141-145` | 12 |
| Pagination cursor's `sort_value` extractor assumes single numeric | `search/service.py:88, 95` | 12 |
| `RankingPipeline.score_paper` hard-sequences 5 scorer dispatches | `interest/ranking.py:439-487` | 12 |
| `ProfileContext` 9-field dataclass shaped to 4 current signal types | `interest/ranking.py:52-68` | 12 |
| `find_related_papers` no profile awareness, hardwired to tsvector | `mcp/tools/discovery.py:117-154`, `db/queries.py:181-237` | 13 |
| 8 indexes on `papers`, all tsvector / array / btree — no vector, no edge | `db/models.py:113-122` | 14 |
| `PaperEnrichment.related_works` JSONB never read by retrieval | `db/queries.py` (zero readers) | 14 |
| `AppContext` 13-field dataclass — adds-service ⇒ 3-place edits | `mcp/server.py:32-48` | (candidate scope addition for Phase 12 plan-1 deliberation; not pre-decided) |
| CLI is parallel surface to MCP | `workflow/cli.py` (1130) + `interest/cli.py` (617) | 13 |

These are the concrete refactor targets that Phase 12 plan-1 authoring would scope. **Whether `AppContext` and `ProfileContext` generalization belong in plan-1 specifically is an AGENTS.md:156 phase-scope-shape decision (deliberation boundary).**

---

## §3. Quality of code & preparation for v0.2

### §3.1 Quality is high for v0.1's scope

The codebase is well-organized (8 packages, clean boundaries, no cross-package import smells beyond one documented inline-import at `enrichment/service.py:164` and one expected `interest → workflow` upward dependency). MCP tool wiring is consistent. Service test pattern is tight (real-DB for service tests, mocks for MCP tool tests + adapter tests). Test coverage is broad if not deep at integration boundaries.

`grep -rn "TODO|FIXME|HACK|XXX"` against `src/` returns **zero matches** — debt lives in `.planning/`, not in code.

### §3.2 Real load-bearing irregularities to know about

(Per CODEBASE-MAP §3.2 and §8; single-author Opus pass; each verifiable in seconds)

1. **`watch://{slug}/deltas` resource has a side-effect on read** (`mcp/resources/watch.py:24` → `workflow/watches.py:152-162`): reading auto-advances `checkpoint_date`. MCP semantically treats resources as cacheable; this is non-idempotent.
2. **Tests duplicate the tsvector trigger SQL from migration 001** (`tests/conftest.py:21-41` ↔ `alembic/versions/001_initial_schema.py:98-115`): drift risk.
3. **No migration tests** — schema built via `Base.metadata.create_all`, not `alembic upgrade head`.
4. **`get_paper` tool / `paper://` resource asymmetry** (`mcp/tools/discovery.py:165-169` vs `mcp/resources/paper.py:21`).
5. **`find_related_papers` has no profile awareness** (Property audit Property 2; hardwired to `build_related_query`).
6. **Marker (PDF→markdown) not in `pyproject.toml` deps** (`content/adapters.py:64-88`); silent degradation.
7. **`add_to_collection` opportunistic create-on-missing** (`mcp/tools/workflow.py:54-65`); collapses two `IntegrityError` cases.
8. **No telemetry / metrics layer** for the discovery / workflow / MCP server paths.
9. **`ProcessingTier.EMBEDDED = 3`** is dead — anticipatory slot.
10. **`AppContext` is a struct, not a registry** — adding services requires 3-place edits.

### §3.3 Preparation verdict (reconciles §0 obs 1)

Mixed-but-as-expected. The clean seams (profile primitive, adapter pattern, MCP registration via side-effect imports) are well-positioned for ADR-0005's commitments. The coupled seams (dispatcher, query builders, result shape, pagination, storage indexes) require concrete refactor work that **is what Phase 12 plan-1 should plan**. **The codebase is no more or less ready than 2026-04-25** — nothing has changed; what's missing is the Phase 12 plan. Phase 12 plan-1 authoring is the gating action, not codebase work.

---

## §4. Agential-setup gaps (per AGENTIAL-SETUP-AUDIT)

The 14 gap signals from AGENTIAL-SETUP-AUDIT §11 partition into three classes by *operational shape* (NOT by claimed cost — cost labels are `[chosen for now]` cost-vibes pending operational disposition; per F-7).

### §4.1 Gaps that are pure config / file additions (no doctrine-layer edits)

(Mostly hours-not-days; verifiable by file-presence; do not modify CLAUDE.md / AGENTS.md / LONG-ARC.md)

- No project `.mcp.json`. Sister projects (`scholardoc/.mcp.json`, `gsd-2-explore/.mcp.json`) define MCP attachments.
- No PostgreSQL MCP despite database-backed architecture.
- `.planning/config.json` doesn't opt in to `community: true` / `workflow_guard: true` (4 hooks silently no-op).
- Postlude metadata stub-fielded.
- Memory entries stale (4 of 7 are 32-44 days old; predate v0.2 redirection).

### §4.2 Gaps that need real engineering (medium operational scope)

- No project-local slash command for paired-audit pattern. `(cross-vendor codex GPT-5.5) ∥ (Claude Opus 4.7 adversarial-auditor-xhigh)` is the dominant pattern (5 of 7 `gsd-2-uplift/audits/` + 4 of `.planning/audits/`); each hand-orchestrated.
- No `/doctrine-check` slash command for AGENTS.md:151-162's 6 deliberation-boundary triggers.
- Project-local agents not aware of project anti-patterns (LONG-ARC.md:46-54). **Note:** customizing vendored agents diverges from upstream and complicates GSD update path; consider sidecar prompt-injection mechanism instead of forking.
- No `PreToolUse` hook for doctrine load-points (CLAUDE.md routing not harness-wired).

### §4.3 Gaps that need careful design (uncertain payoff; false-positive risk; the discipline currently relies on paired-review post-hoc)

- No automated detection of project-specific anti-patterns in agent output (closure pressure, single-reader framing claims, tournament narrowing).
- No automatic resurfacing of memory entries when triggers match.
- Handoff cost not amortized (each handoff lists 7-13 onboarding-read-order documents in full).
- Lesson-distillation routing undocumented (4 places lessons can land).

### §4.4 Doctrine-layer gaps (AGENTS.md:160 deliberation-boundary territory — DO NOT auto-edit)

These are **not** "fix-and-go" items. Per AGENTS.md:160: "When editing `LONG-ARC.md`, `VISION.md`, or the project root `CLAUDE.md` / `AGENTS.md` — surface and propose; doctrine-layer changes warrant deliberation rather than in-place editing during routine work."

- **Broken doctrine path references.** CLAUDE.md and AGENTS.md cite `LONG-ARC.md` / `VISION.md` / `PROJECT.md` as bare basenames; actual paths are `.planning/`. Fixing requires editing CLAUDE.md and AGENTS.md (deliberation-boundary). Alternative: symlink `.planning/LONG-ARC.md` etc. to root (no doctrine-layer edit required, but introduces a different maintenance pattern). **Surface-and-propose, don't auto-edit.**
- **Doctrine load-point list at CLAUDE.md:30-36 may need broadening or tightening** as the project evolves. Each such change is AGENTS.md:160 territory.

### §4.5 What the gaps imply

The doctrine is impressively articulated and being honored at the human-orchestrator layer. The harness is doing real work but not project-specific work. **The asymmetry is a plausible focus area, but addressing it interacts with the doctrine-layer which itself triggers AGENTS.md:160.** Most of the §4.1 work is mechanical and reversible; the §4.4 work is not.

---

## §5. The meta-vs-product tension — observation

### §5.1 Two projects, one repo

- **arxiv-sanity-mcp**: the product. Last code commit 2026-03-14. Phase 12 plans pending.
- **`.planning/gsd-2-uplift/`**: the methodology research. ~50+ commits in 6 days.

### §5.2 The dependency chain

(Per STATE.md:210; verifiable)

Product gated on substrate evaluation → substrate evaluation gated on Phase D mapping-shape → Phase D gated on (V'.a) Step 3 audit + Steps 4-5 → Phases E/F downstream → Phase G migration downstream.

### §5.3 What the artifacts themselves say

(Citations are artifact-internal; the framings are stipulated-not-observed per RELATIONSHIP-TO-PARENT.md §1.1.)

- `EXTERNAL-VISION-CONTEXT.md §7.1`: closure-pressure-into-elaboration pattern recurred in the very turn-cluster that produced the corrective artifact (a documented failure of the discipline).
- `2026-04-30 §5.4`: the pattern survives /effort max + pattern-recognition-active + paired audit-discipline + premise-bleed audit precedent.
- Phase D entry paired audit fired but did not catch the methodology-question-shape-mismatch (per 2026-04-30 §5.3): "audit-spec didn't include 'challenge the intervention-surface choice' or 'challenge the methodology fit'."
- STATE.md `stopped_at:` field: the recurrence is "live risk under (V'.a), not resolved one."

### §5.4 What the tension implies for action — option space

**Five readings, all defensible.** The synthesis surfaces the option space; disposition is Logan's. Per F-2 of audit-findings-A.md: option (b) is included for completeness and is *not* artifact-grounded — it represents the inverse of the current sequencing without an artifact arguing for it.

(a) **Honor trajectory; product remains paused** until uplift completes. *Status quo; honors the gating in STATE.md. The (V'.a) Step 3 audit infrastructure is the active framework for the live-risk recurrences.*

(b) **Pause uplift; resume product (Phase 12)**; substrate-shape evidence emerges from product work. *Inverts current sequencing. Included for completeness; no artifact in the corpus argues for this disposition.*

(c) **Extract gsd-2-uplift to dedicated repo NOW**, even though Phase G says wait. Both projects continue at their own pace; the diagnostic loop survives by reference per RELATIONSHIP-TO-PARENT.md §3. *Resolves structural tension; preserves both projects' velocity.*

(d) **Hybrid**: timebox gsd-2-uplift Phase D mapping-shape execution to a specific date / outcome. Resume Phase 12 plan-1 in parallel rather than serially.

(e) **Defer all interventions; the audit's purpose was visibility, not action; resume (V'.a) Step 3 as planned; revisit in two weeks.** *This option includes "do not even act on the §4.1 ergonomic-config wins this week." The audit produces visibility into state; whether to act on the visibility now or after (V'.a) Step 3 disposes is a separate question. Per LONG-ARC.md:51 closure-pressure anti-pattern — choosing this option honors the discipline that "elaboration is the default; closure requires pause + Logan-correction."*

---

## §6. GSD-2 the tool — assessment (test-case-stipulation-contingent)

The §6.4 staging recommendation below rests on the test-case-vs-substrate framing (RELATIONSHIP-TO-PARENT.md §1.1), which is **stipulated, not observed**. If that stipulation loosens (per RELATIONSHIP-TO-PARENT.md §1.1's loosening conditions: "if evidence accumulates that the framing overfits — e.g., gsd-2-uplift first-target outputs surface that arxiv-sanity-mcp's diagnostic signals are unrepresentative"), the staging logic needs reconsideration.

### §6.1 What GSD-2 actually is

GSD-2 (`github.com/gsd-build/gsd-2`, npm `gsd-pi`, v2.78.1) — standalone CLI built on Pi SDK with programmatic agent-harness control. SQLite-DB-authoritative, markdown-projection. Worktree isolation per task, atomic state writes, crash recovery, cost / token ledger, stuck detection, auto-advance through milestones, extension framework, multi-provider.

(Substance question — capabilities list per §6.1 of GSD-2 research input; not independently verified by this synthesis.)

### §6.2 What GSD-2 does NOT have that GSDR does

GSDR (`get-shit-done-reflect-cc`, v1.19.10, Logan's fork) carries: signal tracking, spike workflow, persistent knowledge base (`~/.gsd/knowledge/`), reflection, audit (3-axis), deliberate, health-check, upgrade-project. The signal-tracking + spike-workflow + reflection trio is what produces the `.planning/spikes/` + `.planning/foundation-audit/` + `.planning/deliberations/` infrastructure this project actively uses.

### §6.3 Disambiguation — the tool vs the in-repo initiative

Two distinct things share the "gsd-2" name:

- **(A) GSD-2 the published tool** — `github.com/gsd-build/gsd-2`. Real, mature, active.
- **(B) `.planning/gsd-2-uplift/` in arxiv-sanity-mcp** — methodology research about whether and how to uplift gsd-2 as substrate. The artifact explicitly names the substrate as "gsd-2 + Claude Code runtime + dev tooling + organizational conventions" jointly. So the in-repo initiative is *about* (A), not a competing tool.

### §6.4 Migration question — staged adoption (contingent on test-case stipulation)

Two questions are conflated in "should we adopt GSD-2":

(i) **Should this project adopt GSD-2 *the tool* now?**
- Pro: GSD-2's architecture (worktree isolation, fresh-session dispatch, atomic writes, crash recovery, cost ledger) addresses some failure modes documented in `.planning/`.
- Pro: `/gsd migrate` exists and reads v1 `.planning/` shape.
- Con: GSDR has signal-tracking / spike-workflow / reflection / deliberate that this project actively uses. Migrating loses these unless rebuilt as GSD-2 extensions.
- Con: `.planning/gsd-2-uplift/` is *itself* designing what gsd-2 should be (subject to §1.1 stipulation). Migrating now adopts the substrate while it is being designed.
- Con: GSDR → GSD-2 has no documented migration path.

(ii) **Should the gsd-2-uplift initiative inform GSD-2's design (and / or absorb it)?**
- Trajectory plan §1.7 lists artifacts to MOVE to a dedicated repo at Phase G — implied destination is something like `gsd-2-uplift` as a new repo.
- (V'.a) Step 5 deliverable is METHODOLOGY-MISMATCH-FINDING.md as standalone substrate-shape evidence.
- Reading: gsd-2-uplift's outputs feed GSD-2's roadmap as findings, rather than this project adopting GSD-2 prematurely.

**Staging recommendation (contingent on §1.1 stipulation):**

- **Now**: do not migrate. Adopt selected GSD-2 *disciplines* in current setup where reversible (worktree-per-task as `git worktree` discipline; cost tracking via postlude). Continue gsd-2-uplift work as substrate-design research.
- **At Phase G of trajectory plan (when it fires)**: extract gsd-2-uplift artifacts to a dedicated repo. That repo's relationship to GSD-2 is then explicit and negotiable.
- **Post-Phase-G**: re-evaluate full adoption with substrate-shape evidence in hand.

**If the §1.1 stipulation loosens**, this staging needs reconsideration. **If reading (b) or (e) in §5.4 is preferred**, the timing of the GSD-2 question shifts.

---

## §7. Brainstormed options (bring-your-own-prioritization)

The list below is *inputs*, not a menu. The count is an artifact of how the brainstorm was structured, not a recommendation that 30 things should happen. The calibrated default is **pick zero or pick one**. Cost labels are `[chosen for now]` cost-vibes pending operational disposition (per F-7).

### Product-side (arxiv-sanity-mcp)

P1. Author Phase 12 plan-1 (Lens Abstraction Primitives). [Phase 12 work]
P2. Refactor `AppContext` into a service registry. [Candidate scope addition for Phase 12 plan-1 deliberation; AGENTS.md:156 territory]
P3. Fix `watch://{slug}/deltas` side-effect. [Hygiene]
P4. Link `tests/conftest.py` trigger SQL to migration 001. [Hygiene]
P5. Add migration tests. [Hygiene]
P6. Add coverage threshold + report. [Hygiene]
P7. Wire `structlog` through discovery / workflow / MCP server paths. [v0.2-late or v0.3]
P8. Fix `find_related_papers` profile-awareness. [Phase 13 candidate]
P9. Remove `ProcessingTier.EMBEDDED = 3` or activate it. [Trivial]
P10. Drop or document `confirm_suggestions_bulk` dead method. [Trivial]
P11. Add Marker to `pyproject.toml` deps + startup check. [Hygiene]
P12. Spike OpenAlex coverage for the existing 126 papers (precondition for Phase 14). [Phase 14 prerequisite]
P13. Begin Phase 14 in parallel with Phase 12 (per ROADMAP execution order). [If reading (d)]

### Agential-setup side (config / file-add only — no doctrine-layer edits)

A1. Create `.mcp.json` enabling serena, context7, philpapers, tavily. [Config]
A2. Add PostgreSQL MCP. [Config]
A3. Opt into `community: true` / `workflow_guard: true` (or document why not). [Config]
A4. Wire postlude actual-measurements computation. [Engineering]
A5. Refresh stale memory entries (4 of 7 are 32-44 days old). [Hygiene]

### Agential-setup side (engineering — slash commands, agents)

A6. Create `/audit-paired` slash command for the dominant audit pattern. [Engineering]
A7. Create `/doctrine-check` slash command for AGENTS.md:151-162's 6 triggers. [Engineering]
A8. Customize project-local agents to cite-back AGENTS.md anti-patterns (consider sidecar over fork). [Engineering]
A9. Build `PreToolUse` hook for doctrine load-points. [Engineering — false-positive risk]
A10. Build closure-pressure / opening-pressure classifier sub-agent. [Higher-cost; uncertain payoff; false-positive risk]
A11. Add per-memory-entry trigger metadata for auto-resurfacing. [Engineering]
A12. Refactor `/gsd:resume-work` to delta-encode handoffs. [Engineering]
A13. Document the lesson-distillation routing. [Doc]
A14. Add `.git/hooks/pre-commit` discipline checks. [Engineering]

### Agential-setup side (DOCTRINE-LAYER — AGENTS.md:160 surface-and-propose)

D1. Fix doctrine path references (LONG-ARC.md / VISION.md / PROJECT.md cited as bare basenames). Either symlink (config-only; preferred per F-4) or update CLAUDE.md / AGENTS.md (doctrine-layer; surface-and-propose).
D2. Broaden / tighten doctrine load-point list at CLAUDE.md:30-36 as project evolves. Each change is AGENTS.md:160.

### Meta-tension side

M1. Extract `.planning/gsd-2-uplift/` to dedicated repo *now*. [Reading c]
M2. Status quo. [Reading a or e]
M3. Pause gsd-2-uplift; resume product. [Reading b — included for completeness]
M4. Timebox uplift Phase D + parallel product. [Reading d]
M5. Spike `/gsd migrate` against `.planning/` to assess fit (informs §6 disposition). [Half-day]

### GSD-2 adoption side

G1. Adopt GSD-2 features piecewise as disciplines (worktree-per-task; cost tracking). [Without tool migration]
G2. Spike `/gsd migrate` (M5).
G3. Defer adoption decision until Phase G fires. [Status quo]
G4. Contribute gsd-2-uplift methodology findings upstream to GSD-2 once Phase G extracts them. [Long-arc]

---

## §8. Concrete interventions, scoped (and properly tiered per F-4)

Per audit-findings-A.md F-4 (BLOCKING): doctrine-layer edits cannot be in a "do without further deliberation" tier. Each tier below carries its discipline label.

### §8.1 Ergonomic config wins (NO doctrine-layer edits — surface to Logan but no AGENTS.md:160 trigger)

Each is reversible (file add or settings change) and does not modify CLAUDE.md / AGENTS.md / LONG-ARC.md / VISION.md. Logan disposes whether to act this week or after (V'.a) Step 3.

**I-1. Add `.mcp.json` at project root** (A1).
- Serena (code nav), context7 (docs lookup), philpapers (domain), tavily (web search).
- Use sister-project pattern (e.g., `scholardoc/.mcp.json`).
- Accept trust dialog (`~/.claude.json:projects[arxiv-sanity-mcp].hasTrustDialogAccepted = true`).

**I-2. Add PostgreSQL MCP** (A2).
- `@modelcontextprotocol/server-postgres` (read-only) on local dev DB.
- Directly addresses `feedback_no_explore_for_audits.md` failure mode.

**I-3. Opt into `community: true` / `workflow_guard: true` in `.planning/config.json`** (A3) — or document why not.
- Activates 4 dormant hooks.

**I-4. Symlink `.planning/LONG-ARC.md`, `.planning/VISION.md`, `.planning/PROJECT.md` to project root** (D1, config-only branch).
- Resolves broken doctrine path references *without* editing CLAUDE.md / AGENTS.md.
- Reversible (delete symlinks).
- Alternative D1 branch (updating CLAUDE.md / AGENTS.md to use full paths) IS doctrine-layer; see §8.4.

**I-5. Fix the load-bearing irregularities surfaced by CODEBASE-MAP §3.2** (P3, P4, P11, P9, P10).
- Watch resource side-effect (P3): make `watch://{slug}/deltas` idempotent.
- Trigger SQL drift (P4): import migration 001's trigger SQL into `tests/conftest.py`.
- Marker dep (P11): add to `pyproject.toml` as optional + startup check.
- Dead code (P9, P10): delete or activate.
- These are bug-fix-class; could be a single "Pre-v0.2 Hygiene" plan or `/gsd:quick`.

### §8.2 Phase 12 plan-1 candidates (AGENTS.md:156 phase-scope deliberation territory — surface-and-propose)

The Phase 12 plan-1 *authoring itself* is a deliberation-boundary moment. The items below are **candidates** for the plan, not pre-decisions.

**I-6. Phase 12 plan-1: Lens Abstraction Primitives** (P1) — as ROADMAP.md:272-274 specifies (3 plans; 5 success criteria). Concrete refactor targets per §2.4.

**I-7. Candidate scope additions for Phase 12 plan-1 deliberation** (P2 + ProfileContext generalization).
- AppContext registry refactor: argument is "adding lenses repeatedly otherwise requires 3-place edits." Could land as Phase 12 plan-1 or as Phase 11.5 hygiene.
- ProfileContext generalization to bag-of-typed-signals: closely tied to RankingPipeline scorer registry but not strictly necessary for the v0.1-tests-pass success criterion.
- **Logan disposes whether to scope these into plan-1 or split.**

**I-8. Custom slash commands and agents specific to this project** (A6, A7, A8) — could be a separate dev-tooling plan or Phase 12 prerequisite work.
- `/audit-paired`, `/doctrine-check`, project-anti-pattern cite-backs.

**I-9. Postlude wiring** (A4) — wire actual computation for measurement signals.

### §8.3 Future milestone (v0.3 or v0.2-late)

**I-10. Closure-pressure detection sub-agent** (A10) — defer until evidence accumulates that manual discipline alone is insufficient. The (V'.a) work *is* producing that evidence.

**I-11. Memory entry auto-resurfacing** (A11). 

**I-12. Handoff cost amortization** (A12) — depends on lesson-distillation routing being clearer first (A13).

**I-13. Coverage threshold + report (P6), telemetry layer (P7), migration tests (P5)** — production-hardening.

### §8.4 Doctrine-layer (AGENTS.md:160 surface-and-propose REQUIRED)

**I-14. Update CLAUDE.md / AGENTS.md to use full paths** (D1, doctrine-edit branch).
- Alternative to I-4 symlink.
- This is doctrine-layer and warrants explicit deliberation (per AGENTS.md:160).
- Suggested: surface-and-propose with (i) observed problem; (ii) proposed change; (iii) why now; (iv) alternatives considered (symlink per I-4); (v) expected write-set; (vi) verification plan.

**I-15. Broaden / tighten doctrine load-point list at CLAUDE.md:30-36 as project evolves** (D2).
- E.g., commit `004a1a7` already broadened the load-point trigger to cover STATE.md uplift-status edits.
- Each future change is AGENTS.md:160.

### §8.5 Cross-cutting — the meta-tension disposition (Logan-decides)

**I-16. Resolve §5.4's option (a) / (b) / (c) / (d) / (e).** This is the load-bearing decision Logan needs to make, or to explicitly defer per option (e).

**I-17. GSD-2 adoption staging** (per §6.4) — contingent on §1.1 test-case stipulation.

**I-18. Spike `/gsd migrate` against a copy of `.planning/`** (M5/G2) — half-day spike that informs I-17 disposition without committing.

---

## §9. Identified gaps (consolidated, single-author chain caveat applies)

(See SYNTHESIS-DRAFT §9 for the consolidated list. Findings are unchanged; the per-citation single-author marker applies — "per CODEBASE-MAP §X" = single-author Opus pass; "per AGENTIAL-SETUP-AUDIT §Y" = Sonnet 4.5 explore-class pass; verify before disposition rests on them.)

---

## §10. What the artifacts say about disposition options (per F-2 — option (b) marked)

### §10.1 Evidence pertaining to "fold uplift into existing milestone" (reading b)

**No artifact in the corpus argues for this disposition.** The closest artifact-grounded considerations:
- The methodology-mismatch finding produced two substantive substrate-shape findings as side-effects (per 2026-04-30 §3.1-§3.2) — but these emerged from spike work, not from product work.
- Phase 12 plan-1 is on hold per STATE.md — resuming requires an explicit decision that does not have artifact backing in the gsd-2-uplift corpus.

(Reading b is included in §5.4 for completeness, not because the corpus argues for it.)

### §10.2 Evidence pertaining to "extract uplift to dedicated repo NOW" (reading c)

- Trajectory plan §1.7 has a 17-row artifact-by-artifact MOVE/STAY/DUPLICATE table.
- INITIATIVE.md §7 migration-trigger conditions exist.
- harness-studio (the larger vision repo) already exists.
- The offshoot pattern (Property 8 of EXTERNAL-VISION-CONTEXT.md) is demonstrated 2x.
- RELATIONSHIP-TO-PARENT.md §3 specifies bidirectional reference + Phase H verification.
- Trajectory plan §1.6 trigger criteria (b) and (c) arguably apply now.

### §10.3 Evidence pertaining to "honor trajectory plan; complete Phase D under (V'.a)" (reading a)

- The closure-pressure-into-elaboration pattern is named as a live risk under (V'.a) mitigation. Premature closure of the uplift work would instantiate the pattern.
- Phases D/E/F are pre-Phase-G gates; honoring them produces the substrate-shape map.
- (V'.a) Step 3 audit infrastructure is explicitly designed to break framing-inheritance recursion.

### §10.4 Evidence pertaining to "hybrid: timebox + parallel" (reading d)

- Phase 12 and Phase 14 are parallelizable per ROADMAP §"Execution Order".
- The uplift work's substrate-evidence channel does not require product be paused; product deliberations *are* substrate-evidence sources (per §1.4 EXECUTION-LOG.md TRAIL).
- Timeboxing is consistent with the budget-deviation-as-frame-revision-trigger discipline added during (V'.a) Step 2 self-review.

### §10.5 Evidence pertaining to "defer all interventions; revisit in two weeks" (reading e)

- The audit's purpose was visibility (the user's prompt: "where we are, where we are going, whether we are set up properly"). Visibility does not entail action.
- The (V'.a) Step 3 audit-spec drafting is in flight; disposition there will inform what other interventions are appropriate.
- The synthesis itself is single-author + four single-author investigations + this synthesis-of-them = single-source-cubed (per F-11). Acting on the conclusions before independent verification is the failure mode the discipline exists to prevent.
- Per LONG-ARC.md:51 closure-pressure anti-pattern: the calibrated answer to "here are 18 interventions" is sometimes "act on zero of them this week."

### §10.6 What the artifacts cannot say

The artifacts cannot recommend disposition. That is structurally Logan's per the in-session-collaboration discipline (D5a; per RELATIONSHIP-TO-PARENT.md §1.1; per the disposition discipline in INITIATIVE.md §0).

---

## §11. Single-author chain caveat (revised per F-11)

This synthesis was authored by Claude Opus 4.7 in a single session. The author of the synthesis is the same author who designed the four parallel investigations. The four investigations are themselves single-author single-pass reads (CODEBASE-MAP and GSD-2-UPLIFT-MAP by Opus 4.7 1M-context; AGENTIAL-SETUP-AUDIT by Sonnet 4.5; GSD-2 external research by Sonnet 4.5).

Per LONG-ARC.md:61: "Single-reader factual claims need verification. 'X exists' or 'Y is current state' claims about the codebase are checkable in seconds; verify before propagating."

Inline citations in this synthesis carry the convention: `per CODEBASE-MAP §X` / `per AGENTIAL-SETUP-AUDIT §Y` — these are single-reader pointers. Every load-bearing claim is verifiable in seconds against the codebase or `.planning/` tree. Verify before any disposition rests on them.

The mitigation for the chain depth: this synthesis was reviewed by `adversarial-auditor-xhigh` (per the project's M1 discipline, fresh session, same vendor). The audit-findings-A.md output (340 lines, 1 blocking + 11 quality + 1 absence-of-finding) was incorporated into this revision. **The cross-vendor reviewer's role (substance verification of the four investigations) has not been executed for this audit — that is an additional verification layer Logan may want before disposing on substantive claims.**

The four reviewer-asks for adversarial review were:
1. ✅ Whether §5's framing of the meta-vs-product tension overstates or understates either side. (F-1, F-8, F-2 addressed)
2. ✅ Whether §8's intervention-scoping has hidden over-commitments. (F-4 BLOCKING + F-6 addressed)
3. ✅ Whether §6's GSD-2 staging recommendation is shaped by inheritance from gsd-2-uplift's framing. (F-5 addressed)
4. ✅ Whether the absence of a "do nothing right now" option is itself a closure-pressure instance. (F-3 addressed; reading (e) added)
5. (Per F-12): Whether the artifact applies intervention-design methodology where the question might be stop-and-look. (Acknowledged; reading (e) is the operational answer.)

---

## §12. Summary table for Logan disposition

| Item | Class | Reversibility | AGENTS.md:160? | Recommended pause-before-acting? |
|---|---|---|---|---|
| I-1 `.mcp.json` add | Config | High (delete file) | No | Standard surface-to-Logan |
| I-2 PostgreSQL MCP | Config | High | No | Standard surface-to-Logan |
| I-3 Opt-in to community/workflow_guard | Config | High (revert config.json) | No | Standard surface-to-Logan |
| I-4 Symlink doctrine files to root | Config | High (delete symlinks) | No (doesn't edit doctrine docs) | Standard surface-to-Logan |
| I-5 Hygiene fixes (P3, P4, P9, P10, P11) | Code | High (revert PR) | No | Standard surface-to-Logan |
| I-6 Phase 12 plan-1 authoring | Phase work | Low (creates plan artifact) | YES (AGENTS.md:156 phase-scope) | Surface-and-propose |
| I-7 P12 scope additions (AppContext / ProfileContext) | Phase scope | Low | YES (AGENTS.md:156) | Surface-and-propose |
| I-8 Custom slash commands + agents | Engineering | Medium | No (don't edit doctrine docs) | Standard surface-to-Logan |
| I-9 Postlude wiring | Engineering | Medium | No | Standard surface-to-Logan |
| I-10 Closure-pressure classifier | Engineering | Medium | No | Defer per §8.3 |
| I-14 Update CLAUDE.md / AGENTS.md paths | DOCTRINE | Medium | YES | Surface-and-propose REQUIRED |
| I-15 Broaden doctrine load-point list | DOCTRINE | Medium | YES | Surface-and-propose REQUIRED |
| I-16 Meta-tension disposition (a/b/c/d/e) | Decision | Variable | (Logan disposes) | (Logan disposes) |
| I-17 GSD-2 adoption staging | Decision | Variable | Contingent on §1.1 stipulation | (Logan disposes) |
| I-18 Spike `/gsd migrate` | Spike | High (read-only) | No | Standard surface-to-Logan |

**Legend:**
- "Standard surface-to-Logan": the Logan-disposes posture; surface the proposal, wait for explicit go.
- "Surface-and-propose REQUIRED": AGENTS.md:151-162 deliberation-boundary trigger.

**The "do nothing this week" disposition (option e) is consistent with all rows.**

---

*Synthesis revised 2026-05-01 by Claude (Opus 4.7) post-adversarial-review. Subject to single-author chain caveat (§11). To be reviewed by Logan; the option-space is Logan's to dispose. **Reading (e) "defer all interventions; revisit in two weeks" is a first-class disposition.**

*Cross-vendor reviewer dispatch (substance verification of the four investigations) is the additional verification layer Logan may want before disposing on substantive claims. Same-vendor adversarial review is complete (audit-findings-A.md).*
