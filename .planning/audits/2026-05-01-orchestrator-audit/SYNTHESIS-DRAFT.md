---
type: orchestrator-synthesis
status: draft — for adversarial review
date: 2026-05-01
audience: Logan (orchestrator-disposition); reviewer (adversarial-auditor-xhigh)
inputs:
  - CODEBASE-MAP.md (409 lines, file: same dir)
  - GSD-2-UPLIFT-MAP.md (594 lines, file: same dir)
  - AGENTIAL-SETUP-AUDIT.md (659 lines, file: same dir)
  - GSD-2 external research (web search + repo inspection)
  - Direct reads: CLAUDE.md, AGENTS.md, LONG-ARC.md, VISION.md, PROJECT.md, STATE.md, ROADMAP.md, RELATIONSHIP-TO-PARENT.md, ADR-0005
single_author_caveat: |
  This synthesis was written by Claude Opus 4.7 in a single session as the orchestrator
  of four parallel investigations. The author of this synthesis is the same author
  who designed the four investigations, so the synthesis inherits framing from the
  investigation specs (an instance of the in-session-collaboration-risk that
  RELATIONSHIP-TO-PARENT.md §1.1 names). Adversarial review intended.
---

# Orchestrator Audit Synthesis — arxiv-sanity-mcp + gsd-2-uplift state

This synthesis is the output of a multi-prong audit dispatched 2026-05-01 in response to Logan's prompt:

> "I want you to plan and perform a full audit of this repo, where we are, where we are going, whether we are set up properly for agential development here, how we can uplift the repo and the setup even further, how we can make this the best possible product / service it can be, whether or not GSD-2 (has a GitHub page) would be useful at all for us. I want you to perhaps brainstorm some ideas, and then translate those ideas into concrete interventions into the current codebase as something we can formalize to either be integrated within this milestone or a future milestone. Perhaps some reviews on the quality of the code itself and how well prepared we are for where we perhaps are going. You should act as the orchestrator, delegating and synthesizing. I want you to identify any gaps as well. Also if you think GSD-2 would be appropriate and useful for this project, think about how we would potentially migrate over."

The synthesis structures findings, brainstorms, and concrete interventions. **It does not dispose** — disposition is Logan's per the standing in-session-collaboration discipline.

---

## §0. Executive frame (read first)

Three observations are load-bearing for everything that follows:

1. **The arxiv-sanity-mcp product is healthy as a v0.1 codebase but architecturally unprepared for v0.2.** The codebase shipped 2026-03-14 is single-implementation across the full surface — `grep -rn "lens|Lens" src/` returns zero matches. The profile primitive (migration 005) is intentionally extensible; everything downstream of it is not. ADR-0005 commits to ≥2 lens implementations as the validation discipline, but no v0.2 production code exists yet. Phases 12-17 are *planned*, not started.

2. **The agential-development setup is rich at the doctrinal layer (CLAUDE.md / AGENTS.md / LONG-ARC.md / VISION.md / spike METHODOLOGY / foundation-audit / paired-review / 14-row failure-mode taxonomy) and thin at the harness layer (no project `.mcp.json`, no project-specific slash commands for the dominant audit pattern, no automated anti-pattern detection, project-local agents not customized to project anti-patterns, broken doctrine path references).** The doctrine is enforced by Logan-the-orchestrator and by Claude reading CLAUDE.md and remembering — not by the harness.

3. **The repo is currently hosting two distinct projects in tension.** `arxiv-sanity-mcp` (the product) is paused. `.planning/gsd-2-uplift/` (a methodology research initiative whose stated goal is to make the gsd-2 substrate "the best it possibly can be across longer and longer development horizons" — `INITIATIVE.md:42`) is consuming nearly all recent activity (50+ commits in 6 days). Phase 12 plan-1 authoring is **explicitly on hold** pending uplift findings (per STATE.md). The trajectory plan calls for the uplift to extract to its own repo at Phase G; that repo does not yet exist, and Phase G is gated on Phases D/E/F all completing (none have under the (V'.a) replan).

These three observations frame the question Logan posed: **what should we *do* about this state?**

---

## §1. Where we are

### §1.1 The product (arxiv-sanity-mcp)

| Dimension | State |
|---|---|
| Last code commit | 2026-03-14 (Phase 10 complete, v0.1.0 tag) |
| MCP surface | 13 tools, 4 resources, 3 prompts (per `src/arxiv_mcp/mcp/`) |
| Test count | 487 `def test_` matches across 51 files (CODEBASE-MAP §5) |
| Database | PostgreSQL via SQLAlchemy 2.0 async; 8 alembic migrations |
| Architecture | Single-lens-by-accident (no `Lens` abstraction in `src/`) — CODEBASE-MAP §7 |
| Active branch | `spike/001-volume-filtering` — but no spike-001 work since 2026-04-26; all commits since are gsd-2-uplift documentation |
| ADRs | 4 accepted (0001 exploration-first; 0002 metadata-first lazy enrichment; 0003 license + provenance; 0004 MCP as workflow substrate; 0005 multi-lens v0.2 substrate) |
| v0.2 phases | 12-17 authored in ROADMAP.md; 0/15 plans started |

### §1.2 The methodology research (gsd-2-uplift)

| Dimension | State |
|---|---|
| Initiative scope | `gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions` — substrate-shape itself part of investigation (per INITIATIVE.md:44) |
| Test-case framing | arxiv-sanity-mcp is *a* spike-intensive test case; framing is "stipulated, not observed" per RELATIONSHIP-TO-PARENT.md §1.1 |
| Current phase | Phase D under (V'.a) replan; mid-Step 3 (audit-spec drafting via cross-vendor codex; Claude parallel-skeleton authored blind for differential calibration) |
| Audits to date | 7 audit folders in `gsd-2-uplift/audits/` + 8+ in `.planning/audits/`; paired-vendor pattern dominant (cross-vendor codex GPT-5.5 ∥ same-vendor adversarial-auditor-xhigh) |
| Methodology artifacts | 14-row failure-mode taxonomy; framing-widening (R1-R5; six-context; four-act); premise-bleed audit-arc; B-strong protocol; point-of-use foregrounding; frame-revision-check; methodology-question-shape-mismatch; etc. |
| Migration plan | Phase G extracts artifacts to dedicated repo; 17-row artifact-by-artifact MOVE/STAY/DUPLICATE table |
| Dedicated repo | Does not exist yet |
| Documented blockers | Closure-pressure-into-elaboration recurrence (survives /effort max + paired audit + premise-bleed precedent); D5a in-session-collaboration risk compounding without independent break since Phase A audit (2026-04-29) |

### §1.3 The agential-development setup

| Surface | State |
|---|---|
| Project `.mcp.json` | None. Only `sequential-thinking` MCP loaded. Globally available (but unloaded here): serena, context7, philpapers, zlibrary, tavily, morphllm-fast-apply |
| PostgreSQL/SQLite MCP | None configured anywhere despite database-backed architecture |
| Project-local hooks | 2 (gsd-check-update, gsd-context-monitor); 4 of 12 active hooks are no-ops because `.planning/config.json` doesn't opt in to `community: true` / `workflow_guard: true` |
| Project-local slash commands | 32 GSD-default commands, none customized; **no command for the dominant paired-audit pattern** |
| Project-local custom agents | 12 GSD-default agents, none customized; none reference the project's 7 specific anti-patterns at LONG-ARC.md:46-54 |
| Doctrine load-points | 7 trigger→doc routings in CLAUDE.md, fired only by Claude-reads-and-remembers; no harness wiring |
| Postlude metadata | 312 rows landed; `error_rate` / `direction_change` / `destructive_event` all `downstream_live_wiring_not_shipped` |
| Memory entries | 7 (5 feedback + 1 reference + 1 index); `feedback_no_explore_for_audits.md` is high-value (caught a near-miss roadmap framing failure); 4 of 7 are 32-44 days old (predate v0.2 redirection) |
| Doctrine path references | LONG-ARC.md / VISION.md / PROJECT.md cited as bare basenames in CLAUDE.md and AGENTS.md, but live at `.planning/` — **broken references for fresh-session cold reads** |

### §1.4 The external GSD-2 tool

| Dimension | State |
|---|---|
| URL | https://github.com/gsd-build/gsd-2 |
| NPM | `gsd-pi` (install: `npm install -g gsd-pi@latest`) |
| Version | v2.78.1 (115 releases, 4,784 commits, ~7,000 stars) |
| Last activity | Active development; ~Apr 25, 2026 |
| Architecture | Standalone CLI built on Pi SDK with programmatic agent-harness control (NOT v1's slash-command framework) |
| State | SQLite DB authoritative; `.gsd/` markdown is projection |
| Distinguishing features | Worktree isolation, crash recovery, cost/token ledger, stuck detection, auto-advance through milestones, extension framework |
| Migration tool | `/gsd migrate [path]` parses v1 `.planning/` shape (works on this project's structure including decimal phases) |
| Logan's local copy | `/home/rookslog/workspace/projects/gsd-2-explore/` on `phase-d-decision-trace-spike` branch |
| GSDR (current) → GSD-2 | **No documented migration path**; GSDR is v1-line fork with extra capabilities (signal tracking, spike workflow, knowledge base, reflection, deliberate, audit, health-check) that GSD-2 does not yet have |

---

## §2. Where we are going

### §2.1 The stated long-arc (per VISION.md, LONG-ARC.md, ADR-0005)

**Product trajectory.** A multi-lens MCP-native research-discovery substrate for AI/CS/ML researchers, durable across years of practice. Multi-lens is the central architectural commitment (no single retrieval lens can serve practicing AI research). Bundle-of-signals profile primitive. Longitudinal memory across sessions. Per-lens provenance and explanation. Steerable, intersection-able, lens-disagreement-as-signal. v0.2 ships ≥2 lenses (semantic + citation/community) as the validation discipline for the abstraction.

**Substrate trajectory.** Per `gsd-2-uplift/INITIATIVE.md:42`, the goal is "to uplift GSD-2 to be the best it possibly can be across longer and longer development horizons." The initiative is staged at `.planning/gsd-2-uplift/` with explicit migration trigger to a dedicated repo (Phase G of trajectory plan).

### §2.2 The mismatch

The product trajectory and the substrate trajectory are sequenced. STATE.md:210:
> Phase 12 plan 1 authoring (on hold pending gsd-2 uplift first-wave findings + incubation checkpoint)

**The product is gated on the substrate evaluation completing.** The substrate evaluation is gated on its own Phase D mapping-shape execution (which is gated on the Step 3 audit-of-audit-of-the-trajectory-replan). The dependency chain runs through ~3-4 more (V'.a) sub-steps + Phase D + E + F before Phase G migration can fire, and only after that does product work resume.

This is the structural backdrop for everything in §3-§6.

### §2.3 What the product is set up to do well in v0.2 (architecture seam alignment)

- **Profile primitive** (lens-extensible by design — migration 005 + JSONB weights): the right shape for ADR-0005's bundle-of-signals.
- **Pluggable adapter pattern** for `EnrichmentAdapter` and `ContentAdapter` Protocols (`src/arxiv_mcp/enrichment/openalex.py:47-61`, `src/arxiv_mcp/content/adapters.py:23-47`): correct shape for what a `Lens` Protocol should look like.
- **Side-effect tool/resource/prompt registration via `mcp/server.py:96-102`**: a new lens-aware tool can be added as a new file with `@mcp.tool()` — no central registry to edit.
- **Composition-by-wrapping** (`ProfileRankingService` → `WorkflowSearchService` → `SearchService`): clean enough for a `LensDispatcher` to slide in as a fourth wrapping layer.

### §2.4 What the product needs to displace for v0.2 (architecture seam misalignment)

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
| `AppContext` 13-field dataclass — adding service requires editing dataclass + lifespan + every tool | `mcp/server.py:32-48` | 12 (adjacent) |
| CLI is a parallel surface that mirrors MCP — `lens=` must be added to both | `workflow/cli.py` (1130 lines) + `interest/cli.py` (617 lines) | 13 |

These are the concrete refactor targets. Phase 12 plan-1 authoring would be the place to scope them.

---

## §3. Quality of code & preparation for where we're going

### §3.1 Quality is high for v0.1's scope

The codebase is well-organized (8 packages with clean boundaries; no cross-package import smells beyond one documented inline-import at `enrichment/service.py:164` and one expected `interest → workflow` upward dependency). The MCP tool wiring is consistent (`AppContext` + `_get_app(ctx)` helper). Service test pattern is tight (real-DB for service tests, mocks for MCP tool tests + adapter tests). Test coverage is broad if not deep at integration boundaries (487 tests, no E2E system-level test, no migration tests).

`grep` of `TODO|FIXME|HACK|XXX` against `src/` returns **zero matches** — debt lives in `.planning/`, not in code, which is unusual and noteworthy.

### §3.2 Real load-bearing irregularities to know about

These are not blockers but should be known:

1. **`watch://{slug}/deltas` resource has a side-effect on read** (`mcp/resources/watch.py:24` → `workflow/watches.py:152-162`): reading the resource auto-advances `checkpoint_date` to today. MCP semantically treats resources as cacheable reads; this conflates "read deltas" with "checkpoint that I read them." A second read returns different results.
2. **Tests duplicate the tsvector trigger SQL from migration 001** (`tests/conftest.py:21-41` ↔ `alembic/versions/001_initial_schema.py:98-115`): if migration 001 changes, tests will silently use the old trigger.
3. **No migration tests** — tests build schema via `Base.metadata.create_all`, not `alembic upgrade head`. Buggy migrations or model/migration drift won't be caught.
4. **`get_paper` (tool) bypasses services** (`mcp/tools/discovery.py:165-169`) while `paper://` (resource) gives a richer composite. Asymmetry agents will trip on.
5. **`find_related_papers` has no profile awareness** (Property audit Property 2; CODEBASE-MAP §7). Surfaces a tool-level inconsistency in MCP UX.
6. **Marker (PDF→markdown) not in `pyproject.toml` deps** — silently degrades to "markdown not available" if not installed; no startup-time check (`content/adapters.py:64-88`).
7. **`add_to_collection` opportunistic create-on-missing** (`mcp/tools/workflow.py:54-65`) collapses two distinct `IntegrityError` cases into "Paper not found." Brittle.
8. **No telemetry / metrics layer** — `structlog` used in some services but not in discovery/workflow path or MCP server. No request-level observability.
9. **`ProcessingTier.EMBEDDED = 3`** dead — anticipatory slot for a future embedding lens (CODEBASE-MAP §8).
10. **`AppContext` is a struct, not a registry** — adding a service requires editing the dataclass + lifespan + every tool body. v0.2 will displace this.

### §3.3 Preparation for v0.2 — verdict

Mixed. The clean seams (profile primitive, adapter pattern, MCP registration via side-effect imports) are well-positioned for ADR-0005's commitments. The coupled seams (dispatcher, query builders, result shape, pagination, storage indexes) require concrete refactor work that **is what Phase 12 should plan**. There is no surprise here: the property audit (`audits/2026-04-25-phase-3-property-audit-opus.md`) and CODEBASE-MAP §7 converge on the same finding. **The codebase is no more or less ready than it was on 2026-04-25**; nothing about it has changed. What is missing is the Phase 12 plan that translates the readiness into action.

---

## §4. Agential development setup — gaps and what they imply

### §4.1 Gaps that are pure ergonomics (low-cost, high-impact)

The AGENTIAL-SETUP-AUDIT enumerates 14 gap signals. Several are pure ergonomics — fixing them costs hours, not days, and removes friction from every future session:

1. **No project `.mcp.json`.** Sister projects (`scholardoc/.mcp.json`, `gsd-2-explore/.mcp.json`) define MCP attachments. This project doesn't, and `hasTrustDialogAccepted: false`. **Fix:** add `.mcp.json` enabling serena (code nav), context7 (docs lookup), philpapers (domain-relevant), tavily (web search). Accept trust dialog.
2. **No PostgreSQL MCP** despite database-backed architecture. The `feedback_no_explore_for_audits.md` failure mode literally hinged on Explore reading migration 003 and missing migration 005's drop. A PostgreSQL MCP would let agents query `\d+ interest_signals` directly. **Fix:** add `@modelcontextprotocol/server-postgres` (read-only) to `.mcp.json`.
3. **Broken doctrine path references.** CLAUDE.md and AGENTS.md cite `LONG-ARC.md` / `VISION.md` / `PROJECT.md` as bare basenames; actual paths are `.planning/LONG-ARC.md` etc. **Fix:** either symlink to root, or update references to use full paths.
4. **`.planning/config.json` doesn't opt in to `community: true` / `workflow_guard: true`.** Four hooks (commit-format check, phase-boundary STATE.md reminder, session-start STATE.md reminder, workflow-guard) are silently no-ops. **Fix:** opt in if the disciplines are wanted; document the choice if not.
5. **Postlude metadata stub.** 312 rows landed with `error_rate` / `direction_change` / `destructive_event` all `downstream_live_wiring_not_shipped`. **Fix:** wire actual computation, OR document why deferred.

### §4.2 Gaps that need real engineering (medium-cost, high-impact)

6. **No project-local slash command for paired-audit pattern.** `(cross-vendor codex GPT-5.5) ∥ (Claude Opus 4.7 adversarial-auditor-xhigh)` is the dominant pattern (5 of 7 `gsd-2-uplift/audits/` + 4 of `.planning/audits/`). Each audit hand-orchestrates. **Fix:** build `/audit-paired` slash command. Caveat: the AUDIT-SPEC shape varies enough per audit that templating is non-trivial; a 5-spec sample (`.planning/gsd-2-uplift/audits/*/AUDIT-SPEC.md`) shows differences in lens-spec, recipient, attempt sequencing, anti-contamination prompting.
7. **No `/doctrine-check` slash command.** AGENTS.md:151-162 lists 6 deliberation-boundary triggers (reshape spike/milestone/phase, modify ADR text/status/scope, introduce/remove top-level abstraction, change MCP surface, edit doctrine docs, close Open Question). Mechanical check against staged diff is ~50 lines of bash + a prompt. **Fix:** build it.
8. **Project-local agents not aware of project anti-patterns.** All 12 GSD agents at `.claude/agents/` reference generic anti-patterns ("scavenger hunts", "horizontal layers"). None cite-back to AGENTS.md:41-47 / LONG-ARC.md:46-54 / the 7-pattern set. **Fix:** customize the 4-5 most-used agents (`gsd-planner`, `gsd-executor`, `gsd-verifier`, `gsd-codebase-mapper`, `gsd-roadmapper`) to include cite-backs. **Caveat:** vendoring update path complicates this; consider whether to fork or to provide a sidecar prompt-injection mechanism.
9. **No `PreToolUse` hook for doctrine load-points.** CLAUDE.md:30-36 lists 7 trigger→doc routings; nothing surfaces them automatically when triggers fire. **Fix:** small Node hook that pattern-matches file paths in Edit/Write tool calls and injects matching doctrine docs as `additionalContext`. **Caveat:** false positives could train Claude to ignore the warning.

### §4.3 Gaps that need careful design (high-cost, uncertain payoff)

10. **No automated detection of project-specific anti-patterns in agent output** (closure pressure, single-reader framing claims, tournament narrowing). A small classifier (Sonnet or smaller) could scan assistant turns for closure-pressure phrasings on Stop and flag. **Open question:** false positives are a real concern, and the discipline currently relies on paired-review post-hoc, which is high-quality but slow.
11. **No automatic resurfacing of memory entries when triggers match.** `feedback_no_explore_for_audits.md` warns against dispatching audits to default Explore — would benefit from auto-injection when an audit Task is about to fire. **Open question:** memory rules are stated in natural language; mechanical matching needs trigger-spec metadata per entry.
12. **Handoff cost not amortized.** Each handoff lists 7-13 onboarding-read-order documents in full; predecessor handoffs are not delta-encoded. **Possible fix:** `/gsd:resume-work` skill exists but doesn't read latest handoff + STATE.md + delta-from-predecessor. **Caveat:** delta model is more fragile if the predecessor isn't read.

### §4.4 What the gaps imply

The doctrine is impressively articulated and being honored at the human-orchestrator layer. The harness is barely doing the work the doctrine asks for. **The asymmetry is the main signal.** Closing it is the single largest agential-setup uplift available, and most of the work is mechanical (Type 11.1-11.4 in AGENTIAL-SETUP-AUDIT.md).

---

## §5. The meta-vs-product tension — observation

### §5.1 Two projects, one repo

This repo currently hosts two projects:

- **arxiv-sanity-mcp**: the product. v0.1 shipped; v0.2 architectural commitments accepted; Phase 12 plans pending. Last code commit 2026-03-14.
- **`.planning/gsd-2-uplift/`**: the methodology research. Initiative-staging, decision-space, audits, deliberations, trajectory plan, exploration outputs, wave-2 evidence corpus. Active branch (~50+ commits in 6 days).

### §5.2 The dependency chain

Per STATE.md:
- Phase 12 plan-1 authoring is **explicitly on hold** pending uplift findings
- Phase 12 plan-1 authoring is one of the smallest dependencies on the chain
- The uplift's own next milestone is Phase D mapping-shape execution
- Phase D mapping-shape execution is gated on (V'.a) Step 3 audit dispatch + disposition + Steps 4-5
- Phases E/F are downstream of Phase D
- Phase G (extraction to dedicated repo) is downstream of E/F passing

The product is gated on a chain that has been recursively elongating: each audit surfaces concerns that produce sub-steps; the methodology-mismatch finding mid-Phase-D required a complete trajectory replan. This is **not a criticism** — the work is producing real substrate-evidence (e.g., the skill-shape gsd-2-native-placement misfit per 2026-04-30 §3.1; substrate-mismatch as substrate-shape evidence per §3.2). It is an *observation about the structural dependency*.

### §5.3 What the artifacts themselves say about the tension

- `RELATIONSHIP-TO-PARENT.md §1.1`: the test-case-vs-substrate framing is "stipulated, not observed." It is a useful frame but loosenable per framing-widening §9 deferred-items pattern.
- `INITIATIVE.md §7`: migration trigger conditions exist; the dedicated repo doesn't yet.
- `EXTERNAL-VISION-CONTEXT.md §7.1`: closure-pressure-into-elaboration pattern recurred in the very turn-cluster that produced the corrective artifact (a documented failure of the discipline).
- `2026-04-30 §5.4`: the pattern survives /effort max + pattern-recognition-active + paired audit-discipline + premise-bleed audit precedent.
- Phase D entry paired audit fired but did **not** catch the methodology-question-shape-mismatch (per 2026-04-30 §5.3): "audit-spec didn't include 'challenge the intervention-surface choice' or 'challenge the methodology fit'."

### §5.4 What the tension implies for action

This is the load-bearing question for §6. Three readings, all defensible:

(a) **The uplift work is producing real substrate-evidence; pause-the-product is the cost of doing it right.** Honor the trajectory plan; let Phase D mapping-shape execute; let the dependency chain unwind.

(b) **The uplift recursion is a sign the methodology has overshot product reality.** Resume product work (Phase 12) and let the substrate-shape evidence emerge from concrete product work, not from meta-mapping.

(c) **The dependency is artificial.** Extract gsd-2-uplift to its own repo *now* (even though Phase G says wait). The uplift can continue at its own pace; product work can continue in parallel; the test-case-vs-substrate frame survives because the diagnostic loop is by-reference, not by-co-residence.

**These three readings have different costs and different irreversibility.** The synthesis in §6 surfaces concrete interventions that preserve optionality across them, with explicit notes about which reading they assume.

---

## §6. GSD-2 the tool — assessment

### §6.1 What GSD-2 actually is

GSD-2 (`github.com/gsd-build/gsd-2`, npm `gsd-pi`, v2.78.1) is a standalone CLI built on the Pi SDK with programmatic agent-harness control. The architecture is a deliberate departure from the v1 / GSDR slash-command-prompt-framework approach: v2 controls the agent runtime directly via TypeScript, dispatches fresh sessions per task with files injected at dispatch time, and stores state in a SQLite DB with `.gsd/` markdown as a projection.

Distinguishing capabilities relative to v1 / GSDR:
- Worktree isolation per task (no cross-task contamination)
- Atomic state writes
- Crash recovery
- Cost / token ledger
- Stuck detection
- Auto-advance through milestones
- Extension framework
- Multi-provider (Claude / GPT / others)

These directly address several of the failure modes documented in this project's `.planning/`:
- Closure-pressure / opening-pressure recurrence → fresh-session-per-task reduces accumulated context bias
- D5a in-session-collaboration risk compounding → fresh sessions break the chain
- Audit-of-audit recursion cost → programmatic dispatch can amortize
- The `tengu_sub_nomdrep_q7k` regex Write-path workaround → Pi SDK doesn't share Claude Code's runtime quirks

### §6.2 What GSD-2 does NOT have that GSDR does

GSDR (`get-shit-done-reflect-cc`, v1.19.10, Logan's fork) carries features GSD-2 does not yet have:
- Signal tracking (knowledge-base of accumulated lessons)
- Spike workflow (spike-runner + spike methodology integration)
- Persistent knowledge base (`~/.gsd/knowledge/`)
- Reflection (analyze accumulated signals; distill patterns into lessons)
- Audit (3-axis classification; dispatches `gsdr-auditor`)
- Deliberate (structured deliberation grounded in signals + philosophical principles)
- Health-check (workspace state validation)
- Upgrade-project (mini-onboarding for new features)

These are load-bearing for this project's discipline. The signal-tracking + spike-workflow + reflection trio is what produces the .planning/spikes/ + .planning/foundation-audit/ + .planning/deliberations/ infrastructure.

### §6.3 The migration question

Two questions are conflated in "should we adopt GSD-2":

(i) **Should this project adopt GSD-2 *the tool* now?**
- Pro: many of the documented failure modes in this project's `.planning/` are precisely what GSD-2's architecture addresses (worktree isolation, fresh-session dispatch, atomic writes, crash recovery, cost ledger).
- Pro: `/gsd migrate` exists and reads v1 `.planning/` shape; preview-before-write reduces migration risk.
- Pro: Logan already has `~/workspace/projects/gsd-2-explore/` cloned.
- Con: GSDR has signal-tracking / spike-workflow / reflection / deliberate that this project actively uses. Migrating to GSD-2 would lose these unless they're rebuilt as GSD-2 extensions or upstreamed.
- Con: `.planning/gsd-2-uplift/` is *itself* a methodology research initiative whose explicit goal is to refine what gsd-2 should be. Migrating now would adopt the substrate while it is being designed.
- Con: GSDR → GSD-2 has no documented migration path; this project would be the migration test case, which is high cost.

(ii) **Should the gsd-2-uplift initiative inform GSD-2's design (and / or absorb it)?**
- The trajectory plan §1.7 lists artifacts to MOVE to a dedicated repo at Phase G. The implied destination is something like `gsd-2-uplift` as a new repo with a clear path to becoming GSD-2 v2.79+ contributions or a parallel development line.
- The (V'.a) Step 5 deliverable is METHODOLOGY-MISMATCH-FINDING.md as standalone substrate-shape evidence — exactly the kind of artifact GSD-2's design process would benefit from.
- This reading suggests **gsd-2-uplift's outputs feed GSD-2's roadmap as findings, rather than this project adopting GSD-2 prematurely**.

### §6.4 Reading the combined evidence

The evidence supports a **staged adoption with parallel uplift**:

- **Now**: do not migrate. Adopt selected GSD-2 *capabilities* in the current setup where cheap (worktree isolation as a `git worktree` discipline; cost tracking via the postlude; etc.). Continue the gsd-2-uplift work as substrate-design research.
- **Phase G of trajectory plan (whenever it fires)**: extract gsd-2-uplift artifacts to a dedicated repo. That repo's relationship to GSD-2 is then explicit and negotiable — could be a parallel design line, could be GSD-2 extensions, could be a fork.
- **Post-Phase-G**: re-evaluate adoption. By then, the substrate-shape mapping work will have produced concrete recommendations about what GSD-2 should be; the GSDR features might be in GSD-2 (or be extensions); and the migration cost will be lower because the substrate-shape work has reduced surprise.

This staging assumes reading (a) or (c) in §5.4 — i.e., the uplift work continues. If reading (b) is preferred (resume product, let substrate-shape emerge from product work), the timing of the GSD-2 adoption question shifts.

---

## §7. Brainstormed ideas (raw list — not prioritized)

Surfacing the option space before scoping concrete interventions. Each idea is one sentence + cost/payoff vibe.

### Product-side (arxiv-sanity-mcp)

P1. Author Phase 12 plan-1 (Lens Abstraction Primitives) — even before uplift completes, on the basis that the architecture work is independently load-bearing. *Medium cost; resumes product work.*
P2. Refactor `AppContext` into a service registry (will be needed for v0.2 anyway). *Small cost; small benefit alone but composes with Phase 12.*
P3. Fix the `watch://{slug}/deltas` side-effect on read (separate "read deltas" from "checkpoint that I read them"). *Small cost; fixes documented MCP semantics violation.*
P4. Link `tests/conftest.py` trigger SQL to migration 001 (read from migration file or share via fixture). *Small cost; eliminates documented drift risk.*
P5. Add migration tests that run `alembic upgrade head` against a fresh DB and verify schema. *Small cost; closes a documented test-coverage gap.*
P6. Add coverage threshold + report (currently `pytest-cov` is in deps but no target). *Small cost; visibility.*
P7. Wire `structlog` through discovery / workflow / MCP server paths for observability. *Medium cost; foundation for production telemetry.*
P8. Fix `find_related_papers` profile-awareness — most prominent MCP-surface inconsistency. *Medium cost; could be a Phase 13 deliverable.*
P9. Remove `ProcessingTier.EMBEDDED = 3` (or activate it via Phase 14/15 work). *Trivial cost; small mental-model cleanup.*
P10. Drop or document the `confirm_suggestions_bulk` dead method. *Trivial cost; small cleanup.*
P11. Add Marker to `pyproject.toml` deps (or document why optional + add startup check). *Trivial cost; eliminates silent degradation.*
P12. Spike OpenAlex coverage for the existing 126 papers (precondition for Phase 14). *Small cost; prerequisite knowledge for citation lens.*
P13. Begin Phase 14 (Citation Graph Data Integration) in parallel with Phase 12 — per ROADMAP §"Execution Order" they're parallelizable. *Medium cost; resumes product work in two streams.*

### Agential-setup side

A1. Create `.mcp.json` enabling serena, context7, philpapers, tavily (and accept trust dialog). *Trivial cost; immediate ergonomic uplift for every session.*
A2. Add PostgreSQL MCP (read-only on local dev DB). *Small cost; addresses documented `feedback_no_explore_for_audits.md` failure mode.*
A3. Fix doctrine path references (LONG-ARC.md / VISION.md / PROJECT.md cited as bare basenames). Either symlink or update references. *Trivial cost; removes onboarding friction.*
A4. Opt into `community: true` / `workflow_guard: true` in `.planning/config.json` (or document why not). *Trivial cost; activates 4 dormant hooks.*
A5. Create `/audit-paired` slash command for the dominant audit pattern. *Medium cost; standardizes the 5+ AUDIT-SPECs that exist.*
A6. Create `/doctrine-check` slash command for the 6 AGENTS.md deliberation-boundary triggers. *Small cost; closes a self-check gap.*
A7. Customize 4-5 most-used project-local agents (gsd-planner, gsd-executor, gsd-verifier, gsd-codebase-mapper) to cite-back AGENTS.md anti-patterns. *Small cost; embeds discipline at agent level.*
A8. Build `PreToolUse` hook for doctrine load-points (path-pattern → doc-injection). *Medium cost; embeds CLAUDE.md routing in the harness.*
A9. Wire postlude metadata to compute real signals (transcript-driven post-hoc analysis). *Medium cost; activates 312 stub rows + every future row.*
A10. Build closure-pressure / opening-pressure classifier sub-agent (Sonnet, runs on Stop). *Higher cost; addresses §11.11 gap; false-positive risk.*
A11. Add per-memory-entry trigger metadata so memory entries can auto-resurface when triggers match. *Medium cost; addresses §11.7.*
A12. Refactor `/gsd:resume-work` to read latest handoff + STATE.md + delta-from-predecessor. *Medium cost; amortizes onboarding cost.*
A13. Document the lesson-distillation routing (which lessons go to memory vs `.planning/spikes/` vs `DECISION-SPACE.md` vs `~/.gsd/knowledge/`). *Small cost; reduces routing confusion.*
A14. Add `.git/hooks/pre-commit` checks for AGENTS.md deliberation triggers (e.g., diff includes ADR change → require explicit confirmation). *Medium cost; mechanical floor under discipline.*

### Meta-tension side

M1. Extract `.planning/gsd-2-uplift/` to a dedicated repo *now* (per Phase G migration plan, even though the gate isn't formally met). *Medium cost; resolves the structural tension; preserves the diagnostic loop by reference.*
M2. Continue trajectory as planned; the Phase D mapping-shape work is load-bearing. *Status quo; assumes reading (a) in §5.4.*
M3. Pause gsd-2-uplift; resume product work; substrate-shape evidence emerges from product work. *Reverses trajectory; assumes reading (b).*
M4. Timebox gsd-2-uplift Phase D to a specific outcome and date; resume product work in parallel. *Hybrid; preserves both.*
M5. Spike GSD-2 the tool's `/gsd migrate` against a copy of `.planning/` to assess migration cost without committing. *Small cost; informs §6 disposition.*

### GSD-2 adoption side

G1. Adopt GSD-2 features piecewise as disciplines rather than as tool migration (worktree isolation as `git worktree` per task; postlude cost-tracking). *Small cost; captures benefits without committing to migration.*
G2. Spike `/gsd migrate` against `.planning/` (M5 above). *Same as M5.*
G3. Defer adoption decision until Phase G of trajectory plan fires. *Status quo on this front.*
G4. Contribute the gsd-2-uplift methodology findings upstream to GSD-2 once Phase G extracts them. *Long-arc; depends on §6.4 staging.*

---

## §8. Concrete interventions, scoped by milestone

This section translates the brainstormed ideas into concrete proposals scoped to:

- **Now-or-immediate (this session or next)** — interventions with low cost and high payoff
- **Current milestone (v0.2)** — interventions to fold into Phase 12 plan-1 authoring (whenever that resumes)
- **Future milestone (v0.3 or later)** — interventions to defer
- **Cross-cutting (independent of milestone)** — interventions that don't fit a milestone but matter

### §8.1 Now-or-immediate (recommend doing without further deliberation)

These are pure ergonomic wins. Each is hours-of-work, not days.

**I-1. Create `.mcp.json` and fix doctrine path references.** Combines A1 + A3.
- Add `.mcp.json` at project root with `serena` (code nav), `context7` (docs lookup), `philpapers` (domain), `tavily` (web search). Use sister-project pattern (e.g., `scholardoc/.mcp.json`).
- Accept the trust dialog (`~/.claude.json:projects[arxiv-sanity-mcp].hasTrustDialogAccepted = true`).
- Fix CLAUDE.md and AGENTS.md to use full paths (`.planning/LONG-ARC.md`, `.planning/VISION.md`, `.planning/PROJECT.md`) OR symlink the planning files to root.
- Also: opt into `community: true` and `workflow_guard: true` in `.planning/config.json` if the disciplines are wanted (or document the choice).

**I-2. Add PostgreSQL MCP.** Combines A2.
- Add `@modelcontextprotocol/server-postgres` (or equivalent) to `.mcp.json` with read-only credentials on a local dev DB.
- Test that an agent can run `\d+ interest_signals` and confirm migration 005's drop of the CHECK constraint.
- This directly addresses the `feedback_no_explore_for_audits.md` failure mode that produced the most expensive recent audit miscalibration.

**I-3. Fix the documented load-bearing irregularities surfaced by CODEBASE-MAP §3.2.**
- Watch resource side-effect (P3): make `watch://{slug}/deltas` idempotent; add a separate `acknowledge_watch_checkpoint` tool/operation for the side-effect.
- Trigger SQL drift (P4): import migration 001's trigger SQL into `tests/conftest.py` rather than duplicating.
- Marker dep (P11): add to `pyproject.toml` as optional; add startup-time check that warns if invoked without it.
- Dead code (P9, P10): delete or activate.

These are bug-fix-class changes; they could be a single "Phase 11: Pre-v0.2 Hygiene" plan or just a small commit batch. **Small enough that a `/gsd:quick` or two would do it.**

### §8.2 Current milestone (fold into Phase 12 plan-1)

When Phase 12 plan-1 authoring resumes, these belong in scope:

**I-4. Phase 12 plan-1: Lens Abstraction Primitives (P1).** As ROADMAP.md already specifies. The CODEBASE-MAP §7 evidence makes this concrete:
- Define `Lens` Protocol following `EnrichmentAdapter` / `ContentAdapter` shape (`enrichment/openalex.py:47-61`, `content/adapters.py:23-47`).
- Build a scorer registry that replaces `RankingPipeline.score_paper`'s hard-sequenced if-tree (`interest/ranking.py:439-487`).
- Generalize `SearchResult` to carry `lens_scores: dict[str, float]` and `per_lens_explanations: dict[str, RankingExplanation]` as additive optional fields. Legacy `score` and `ranking_explanation` continue to mean composite over the active lens for backward compat.
- Generalize `ProfileContext` (the 9-field dataclass at `interest/ranking.py:52-68`) to a bag-of-typed-signals representation.
- Refactor `AppContext` into a service registry as part of this work (P2) — adding lenses repeatedly otherwise requires 3-place edits.
- All v0.1 tests pass without modification (per ROADMAP success criterion).

**I-5. Custom slash commands and agents specific to this project (A5, A6, A7).** Either as a separate dev-tooling plan or as Phase 12 prerequisite work:
- `/audit-paired` slash command for the dominant pattern.
- `/doctrine-check` slash command for AGENTS.md deliberation boundaries.
- Customize 4-5 project-local agents to cite-back AGENTS.md anti-patterns.

**I-6. Postlude wiring (A9).** Wire actual computation for `error_rate` / `direction_change` / `destructive_event`. This produces ongoing measurement that informs methodology adjustments. Not blocking Phase 12 but should land soon.

### §8.3 Future milestone (v0.3 or v0.2-late)

**I-7. Closure-pressure detection sub-agent (A10).** High-cost, uncertain payoff, false-positive risk. Defer until evidence accumulates that the manual-discipline alone is insufficient. *(Note: the gsd-2-uplift work is producing exactly that evidence; the deferral is reasonable until uplift completes.)*

**I-8. Memory entry auto-resurfacing (A11).** Requires per-entry trigger metadata; useful but not load-bearing.

**I-9. Handoff cost amortization (A12).** Useful but depends on the lesson-distillation routing being clearer first.

**I-10. Coverage threshold + report (P6), telemetry layer (P7), migration tests (P5).** Production-hardening work that becomes more relevant when v0.2 ships.

### §8.4 Cross-cutting (independent of milestone)

**I-11. Resolve the meta-vs-product tension.** This is the load-bearing decision Logan needs to make. Three readings (per §5.4 + §7 M1-M4):

(a) **Continue trajectory; product remains paused** until uplift completes. *Status quo; honors the gating in STATE.md.*

(b) **Pause uplift; resume product (Phase 12)**; substrate-shape evidence emerges from product work. *Inverts current sequencing.*

(c) **Extract gsd-2-uplift to dedicated repo NOW**, even though Phase G says wait. Both projects continue at their own pace; the diagnostic loop survives by reference per RELATIONSHIP-TO-PARENT.md §3. *Resolves structural tension; preserves both projects' velocity.*

(d) **Hybrid**: timebox gsd-2-uplift Phase D mapping-shape execution to a specific date / outcome (e.g., "produce substrate-shape map within 2 weeks or ship interim findings as Phase D output"). Resume Phase 12 plan-1 in parallel rather than serially. *Preserves both; adds explicit cost discipline to the uplift loop.*

**The synthesis cannot dispose this — it surfaces the option space.** §10 below records what evidence in the artifacts pertains to each reading.

**I-12. GSD-2 adoption staging (per §6.4).** Recommended posture:
- **Now**: do not migrate. Adopt selected GSD-2 *disciplines* (worktree-per-task discipline, cost tracking via postlude) without tool migration.
- **At Phase G of trajectory plan**: extract gsd-2-uplift to dedicated repo; that repo becomes either GSD-2 contributions, GSD-2 extensions, or a parallel design line.
- **Post-Phase-G**: re-evaluate full adoption with substrate-shape evidence in hand.

This recommendation is contingent on reading (a), (c), or (d) in I-11; reading (b) reorders.

**I-13. Spike `/gsd migrate` against a copy of `.planning/`** (M5/G2). Low-cost spike that informs I-12 disposition without committing to migration. Could be a half-day spike.

---

## §9. Identified gaps (synthesized across investigations)

A consolidated list, surfacing what was missed or under-provisioned across the four investigations:

### Code-level gaps

- **No abstraction over "kind of query"** — `db/queries.py` has three `build_*_query` functions all hardwired to tsvector + `ts_rank_cd`. Vector / graph queries need parallel modules.
- **No Lens abstraction in `src/`** — confirmed by `grep -rn "lens|Lens" src/` (zero matches). The architectural commitment in ADR-0005 has not yet been translated to code.
- **`AppContext` is a struct, not a registry** — adding services requires 3-place edits. Will need to change for v0.2.
- **Single-numeric score assumption** — flows through `SearchResult.score`, pagination cursor, ranking pipeline composite. Multi-lens result with `{semantic: 0.7, citation: 0.3}` cannot ride this pipe.
- **No telemetry / metrics layer** — `structlog` used in some services; not in discovery / workflow / MCP server paths.
- **Marker not in deps** — silent degradation; no startup-time check.
- **Migration tests absent** — schema built via `Base.metadata.create_all`, not `alembic upgrade head`.
- **Duplicate trigger SQL** — `tests/conftest.py` ↔ `alembic/versions/001_initial_schema.py`; drift risk.
- **Watch resource side-effect** — non-idempotent reads.
- **`get_paper` tool / `paper://` resource asymmetry** — composite vs single-row.
- **`find_related_papers` no profile awareness** — most prominent MCP-surface inconsistency.
- **CLI is a parallel surface to MCP** — any v0.2 surface change must be added to both.

### Agential-setup gaps

- **No project `.mcp.json`** — only `sequential-thinking` MCP loaded for this project despite globally-configured `serena`, `context7`, `philpapers`, `zlibrary`, `tavily`, `morphllm-fast-apply`.
- **No PostgreSQL/SQLite MCP** — directly addresses the documented `feedback_no_explore_for_audits.md` failure mode.
- **Broken doctrine path references** — LONG-ARC.md / VISION.md / PROJECT.md cited as bare basenames; live at `.planning/`.
- **4 of 12 hooks no-ops** — `community: true` / `workflow_guard: true` not opted into in `.planning/config.json`.
- **No project-specific slash command for paired-audit pattern** — dominant work pattern is hand-orchestrated.
- **Project-local agents not aware of project anti-patterns** — generic anti-pattern lists; no cite-back to AGENTS.md:41-47 / LONG-ARC.md:46-54.
- **No harness wiring of doctrine load-points** — CLAUDE.md routing fires only by Claude reading and remembering.
- **Postlude measurements stub-only** — `error_rate` / `direction_change` / `destructive_event` all `downstream_live_wiring_not_shipped`.
- **Memory entries not auto-resurfaced when triggers match** — `feedback_no_explore_for_audits.md` warning has to be remembered.
- **Lesson-distillation routing undocumented** — 4 different places lessons can land (memory, spikes, DECISION-SPACE, gsd-knowledge).
- **Handoff onboarding cost not delta-encoded** — fresh sessions pay full cost every time.
- **No git-pre-commit discipline checks** — conventional-commit format check is opt-in and not opted into; ADR-modification check is conceptual.

### Meta / process gaps

- **Phase numbering irregular** in `.planning/phases/` — two `05-*` directories; `04.1-*` alongside `04-*`. Onboarding confusion.
- **Vocabulary density** in gsd-2-uplift artifacts (`(V'.a)`, `M1`-`M5`, `R1`-`R5`, `C1`-`C4`, `S1`-`S8`, `B1`-`B6`, etc.) requires lookup to navigate.
- **Single-author + in-session-collaboration caveat** appended to most artifacts — accumulates into a thicket of self-doubt clauses; may be doing more than its share of the work the discipline intends.
- **Closure-pressure pattern recurrence** documented as surviving every layer of mitigation — surfaces a real limit of the current discipline.
- **No independent break in the in-session-collaboration chain** since Phase A audit (2026-04-29). The chain compounds: (V'.a) Step 1 → 2026-05-01 vision-articulation → Step 2 → self-review → SPEC-DRAFTING-BRIEF → CLAUDE-PARALLEL-SKELETON, all under Logan-co-framing.

---

## §10. What the artifacts say about disposition options (no recommendation)

### §10.1 Evidence pertaining to "fold uplift into existing milestone" (reading b)

- The methodology-mismatch finding produced two substantive substrate-shape findings as side-effects of spike work (per 2026-04-30 §3.1-§3.2): skill-shape gsd-2-native-placement misfit; substrate-mismatch IS substrate-shape evidence. These could inform Phase 14's citation-graph integration design.
- The 12 substrate-vision properties + scope-discipline (per EXTERNAL-VISION-CONTEXT.md §3-§4) are now articulated and committed.
- Phase 12 plan-1 authoring is explicitly on hold per STATE.md — resuming would require either the uplift completing OR explicit decision to decouple.

### §10.2 Evidence pertaining to "extract uplift to dedicated repo NOW" (reading c)

- Trajectory plan §1.7 has a 17-row artifact-by-artifact MOVE/STAY/DUPLICATE table — the disposition is already worked out.
- INITIATIVE.md §7 migration-trigger conditions exist and have been substantially developed.
- harness-studio (the larger vision repo) already exists at `~/workspace/projects/harness-studio/`.
- The offshoot pattern (Property 8 of EXTERNAL-VISION-CONTEXT.md) is demonstrated 2x.
- RELATIONSHIP-TO-PARENT.md §3 specifies the bidirectional reference pattern and Phase H verification — the diagnostic loop survives extraction.
- The dedicated repo trigger (per trajectory plan §1.6) includes "(b) substrate-shape mapping work has internal gravitational center independent of arxiv-sanity-mcp" and "(c) materially-competing-for-shared-resources signal" — both arguably apply now.

### §10.3 Evidence pertaining to "honor trajectory plan; complete Phase D under (V'.a)" (reading a)

- The closure-pressure-into-elaboration pattern is explicitly named as a live risk (per STATE.md `stopped_at:` field). Premature closure of the uplift work would instantiate the pattern.
- Phases D/E/F are pre-Phase-G gates per the plan; honoring them produces the substrate-shape map that informs the dedicated repo's shape.
- The (V'.a) Step 3 audit infrastructure (B-strong protocol; SPEC-DRAFTING-BRIEF + AUDIT-SPEC + CLAUDE-PARALLEL-SKELETON) is explicitly designed to break the framing-inheritance recursion that prior audits failed to break. Allowing Step 3 to dispatch and dispose tests whether the discipline can break the recursion.

### §10.4 Evidence pertaining to "hybrid: timebox uplift Phase D + resume product in parallel" (reading d)

- Phase 12 (Lens Abstraction Primitives) and Phase 14 (Citation Graph Data Integration) are parallelizable per ROADMAP §"Execution Order" — their dependencies do not require uplift completion.
- The uplift work's substrate-evidence channel does not require the product work be paused; product work can generate substrate-evidence in parallel (per §1.4 EXECUTION-LOG.md TRAIL example: 2026-04-25 multi-lens redirection deliberation was used as Phase D test-task — suggesting product deliberations *are* substrate-evidence sources already).
- Timeboxing is consistent with the budget-deviation-as-frame-revision-trigger discipline added to the trajectory plan during (V'.a) Step 2 self-review.

### §10.5 What the artifacts cannot say

The artifacts cannot recommend disposition because that is structurally Logan's per the in-session-collaboration discipline (D5a; per RELATIONSHIP-TO-PARENT.md §1.1; per the disposition discipline in INITIATIVE.md §0). They surface the evidence and let Logan dispose.

---

## §11. Single-author caveat (recursive)

This synthesis was authored by Claude Opus 4.7 in a single session. The author of the synthesis is the same author who designed the four parallel investigations whose outputs feed the synthesis. The investigation specs influenced what the investigators looked for; the synthesis inherits framing from the specs. This is the in-session-collaboration risk that RELATIONSHIP-TO-PARENT.md §1.1 names, applied recursively here.

The mitigation: this synthesis is to be reviewed by `adversarial-auditor-xhigh` (per the project's M1 discipline) **before** Logan disposes any of the proposed interventions. The reviewer is asked to focus on:

1. Whether §5's framing of the meta-vs-product tension overstates or understates either side.
2. Whether §8's intervention-scoping has hidden over-commitments (e.g., I-4 Phase 12 plan-1 may be larger than its ROADMAP entry suggests).
3. Whether §6's GSD-2 staging recommendation is shaped by inheritance from the gsd-2-uplift initiative's own framing.
4. Whether the absence of a "do nothing right now" option in §8 / §10 is itself a closure-pressure instance.

The synthesis is **draft until adversarial review lands and disposition is recorded.**

---

*Synthesis authored 2026-05-01 by Claude (Opus 4.7) as orchestrator output. Subject to single-author + in-session-collaboration fallibility caveat. To be reviewed by adversarial-auditor-xhigh before Logan disposition.*
