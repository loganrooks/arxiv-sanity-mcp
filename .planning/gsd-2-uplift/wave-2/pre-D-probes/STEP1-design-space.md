---
type: phase-D-step-1-design-space-framing
date: 2026-04-30
gsd_2_commit: 42ef05fbe
phase: trajectory plan §1.4 Phase D — first-second-wave-target dispatch + execution
sub-step: §7.10.4 Step 1 — design-space framing (post-Step-0; pre-Step-2 practical decisions; pre-Step-3 mini-spec drafting)
status: surfacing — Logan-disposes one (or composition) at §6 to operationalize Step 2 + Step 3 mini-spec
authoring_discipline: |
  Drafted by Claude (Opus 4.7, xhigh effort, in-session-collaboration with Logan) per
  trajectory plan §7.10.4 Step 1. Surfacing-shape, NOT Claude-disposition: each
  candidate carries (i) architectural shape, (ii) R-strategy, (iii) existing
  gsd-2-internal-primitive gap-mapping, (iv) P5 effective-state caveat inheritance,
  (v) cheap-vs-informative tradeoff, (vi) Phase-E inheritance, (vii) per-candidate
  audit-priority risks. Logan-disposition recorded at §6 once given. The §7.10
  H/M/L tier framing is Claude-imported organizing structure; Phase D entry audit
  per plan §2.4 row D catches any tier-claim functioning as fact rather than
  organizing-frame.

  Drafting absorbed Logan-correction at /effort max turn (2026-04-30): gsdr
  (our fork of the original gsd; lives on Claude Code; opaque substrate) is a
  separate project from gsd-2 uplift. gsd-2 is a standalone runtime; open-source;
  we have direct intervention authority. Initial proposal's Shape B (slash-command
  at `~/.claude/commands/gsdr/decision-trace.md`) and Shape C (extend
  `/gsdr:deliberate`) were dropped as gsdr-shaped, not gsd-2-uplift-shaped.
  This artifact's 5-candidate set is properly gsd-2-shaped.

ground:
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md (Step 0 P5 probe; moderate drift; sub-option (ii) caveat)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md (Step 0 M2 probe; gsd-2 skill subsystem snapshot + existing-primitives inventory)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7 dispositions + §7.9 audit addendum + §7.10 negative-space survey (load-bearing)
  - .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (test-case-vs-substrate; load-bearing for H5 channel separation)
  - .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md §1.4 + §2.4 row D + §6.2 + §0.5 + §0.7
  - .planning/spikes/METHODOLOGY.md (six interpretive lenses + paired-review practice disciplines; load-bearing for spike-sizing M4)
  - .planning/deliberations/2026-04-28-framing-widening.md §1 R-mix + §2 six-context + §3.3 disposition-discipline
  - ~/workspace/projects/gsd-2-explore/ (gsd-2 source at commit 42ef05fbe; freshly pulled 2026-04-30)
read_order: |
  - For "what each candidate is + tradeoffs": §3.A through §3.G in any order; each is self-contained.
  - For "standing constraints across all candidates": §2.
  - For "comparator structure + recommended primary": §4 + §5.
  - For "Logan-disposition options": §6.
  - For "audit-priority risks at this Step 1 layer": §4.5 + §6 audit-priority list.
---

# Phase D Step 1 — Design-space framing for first-target

This artifact surfaces 5 candidate artifact shapes for the Phase D first-target ("Context A/F long-arc decision-trace skill/workflow on gsd-2's skill subsystem, possibly composing with workflow templates" per INCUBATION-CHECKPOINT.md §7.3.a + §7.3.c). It does NOT pre-decide which shape; per trajectory plan §0.7 hybrid autonomy + §7.10.4 Step 1, Logan disposes one (or composition) at §6 to operationalize Step 2 (practical decisions: H6 work-location / H7 staging / M1 budget / M3 auditor / M4 sizing) and Step 3 (mini-spec drafting per §7.9.3 (c) + §7.10 amendments).

## §0. Summary

**5 candidate shapes surfaced**, all gsd-2-side (gsdr-side shapes dropped per §1 below). All are R2 (in-tree gsd-2 working-branch) or R4 (user/project-side discoverable by gsd-2 at runtime) — none require upstream PR commitment within Phase D scope (R3 + R5 deferred per §7.3.b "not-fired-this-arc"; PR step is Phase E-conditional on Phase D evidence).

| # | Shape | R-strategy | Reversibility | gsd-2-internal-primitive gap |
|---|---|---|---|---|
| **A** | User-side gsd-2 skill at `~/.agents/skills/decision-trace/SKILL.md` (single or router) | R4-by-construction wrt gsd-2 | high (`rm -rf`) | Composes with `spike-wrap-up`'s durable-packaging dimension; orthogonal to existing skills |
| **D** | `.gsd/DECISIONS.md` schema/policy enrichment + thin orchestration over existing skills that already write to it | R2 in-tree on working-branch; R5-conditional if upstreamed at Phase E+ | medium (revert branch) | Direct extension of `design-an-interface`, `write-milestone-brief`, spike-wrap-up convergence point |
| **E** | In-tree gsd-2 skill at `src/resources/skills/decision-trace/SKILL.md` + (optional) markdown-phase workflow template | R2 in-tree on working-branch; R5-conditional if upstreamed | medium (revert branch) | New first-class skill alongside existing 30+ |
| **F** | Hook-pattern primitive ("before-edit-X-load-Y" trigger) | R2 in-tree, **core-shape change**; R5-mandatory eventually | low (most invasive) | New primitive; gsd-2 has no existing hook surface for edit-time triggers per M2 §5 |
| **G** | YAML deterministic workflow at `.gsd/workflows/decision-trace.yaml` (project-local) or `~/.gsd/workflows/decision-trace.yaml` (global) | R4-by-construction (user/project-side) | high | Composes with workflow-engine dependency-graph + verification-policies |

**Recommended primary emphasis (Logan-disposes per §6):** Shape D OR Shape E as primary (R2-in-tree-working-branch; the "more control + open-source" framing argues against under-using direct intervention authority); Shape A as comparator (satisfies §7.9.3 (a) R4 contrast requirement at Step 4 disposition); Shapes F + G enumerated for completeness but **out-of-scope-this-arc** (F too invasive for spike; G composable later if Phase D evidence licenses).

**Standing constraints across all candidates:** P5 effective-state caveat (skill must read `PREFERENCES.md` files directly or use in-process `loadEffectiveGSDPreferences` API; cannot rely on `headless query` / MCP `gsd_progress`/`gsd_query` / `prefs status` for effective preferences/skills/hooks/extensions); H5 substrate-vs-first-target channel separation (claims about "decision-trace skill works/doesn't work" must NOT auto-extend to "substrate handles this kind of work well/poorly"; cross-references to general substrate properties require explicit anchoring); §7.4 A+F-primary anchoring (skill design optimized for solo-research-over-years comprehension + transition-as-stance optionality).

## §1. Method + scope discipline

### §1.1 What this Step 1 artifact does

- Surfaces 5 candidate artifact shapes for the first-target.
- For each candidate: architecture / R-strategy / gap-mapping vs gsd-2-internal primitives / P5 caveat / cheap-vs-informative / Phase-E inheritance / audit-priority risks.
- Surfaces composition options across candidates (R-strategies compose per framing-widening §1.3).
- Recommends primary + comparator emphasis under "more control + open-source" reframing (Logan-disposes).
- Surfaces explicit Logan-disposition options at §6 + audit-priority risks at §4.5.

### §1.2 What this Step 1 artifact does NOT do

- Pre-decide which candidate shape (Logan-disposes per framing-widening §3.3 disposition-discipline + plan §0.7 hybrid autonomy).
- Operationalize Step 2 practical decisions (work-location / staging / budget / auditor / sizing — that's Step 2 work post-disposition).
- Draft the Step 3 mini-spec (depends on Step 2 disposition + Step 1 candidate selection).
- Probe `get-shit-done-reflect` (out of scope per Logan-disposition 2026-04-30 Axis 4: gsdr is separate project; Phase D is gsd-2-uplift-shaped).
- Map gsd-2-uplift Phase D against `/gsdr:*` slash-commands (substrate confusion per Logan-correction 2026-04-30; gsdr lives on Claude Code, gsd-2 has its own runtime).

### §1.3 Scope discipline — gsd-2-internal-primitive gap-mapping only

Per Logan-disposed Axis 3 (2026-04-30 /effort max): each candidate's gap-mapping is restricted to gsd-2-internal primitives (M2 §3.B inventory + Step-1-author-supplemented from M2 §1 read-list). NOT mapping vs `/gsdr:deliberate` or other gsdr-side primitives — wrong substrate.

**Inventory of gsd-2-internal primitives surfaced via Step 0 M2 (and consulted for gap-mapping):**

> **Inventory note (per Phase D entry audit F-PD-A2 + F-PD-B1 disposition, applied 2026-04-30):** The original inventory below was incomplete on two fronts: (1) the gsd-2-internal decision-DB substrate (`gsd_decision_save` MCP tool + canonical DECISIONS.md table-generator + db-writer pipeline) was not surfaced; and (2) the gsdr-adjacent prior-art comparator `/gsdr:deliberate` was silently dropped along with gsdr-side candidate-shapes. The drop conflated two distinct moves — dropping candidate-shapes (correct on R-strategy grounds: gsdr lives on Claude Code, gsd-2 has its own runtime) with dropping prior-art comparison (incorrect: coverage-question is independent of replacement-question). Both rows added below to restore the comparison-class without restoring the dropped candidate-shapes.

| Primitive | Source | Decision-trace-relevant dimension |
|---|---|---|
| `spike-wrap-up` skill | `src/resources/skills/spike-wrap-up/SKILL.md` | Durable packaging — captures spike findings into project-local skills (`.claude/skills/<name>/SKILL.md`); closes "throwaway → durable" loop |
| `design-an-interface` skill | `src/resources/skills/design-an-interface/SKILL.md:75-79` | Decision-capture — appends one-liner to `.gsd/DECISIONS.md` with chosen shape + reason (Step 6 of skill workflow) |
| `write-milestone-brief` skill | `src/resources/skills/write-milestone-brief/SKILL.md:74` | Synthesis — appends architectural decisions to `.gsd/DECISIONS.md` during milestone-brief composition |
| `forensics` skill | `src/resources/skills/forensics/SKILL.md` | Post-mortem reconstruction — traces failed auto-mode runs from symptom to root cause via `.gsd/activity/*.jsonl`, `.gsd/journal/`, `.gsd/metrics.json`; closest existing structural analog within gsd-2-internal skill subsystem |
| `handoff` skill | `src/resources/skills/handoff/SKILL.md` | Session-bridging — writes `continue.md` in active slice; ensures STATE.md current. Adjacent to decision-trace at the session-pickup boundary |
| `review` skill | `src/resources/skills/review/SKILL.md` | Diff-review — analyzes changes for security/perf/bugs/quality. Adjacent to decision-trace at "post-decision evaluation" boundary (analog to predictions-evaluation in deliberation patterns) |
| **`gsd_decision_save` MCP tool + DECISIONS.md canonical-table generator + db-writer pipeline** (added per F-PD-A2) | `packages/mcp-server/src/workflow-tools.ts:606-608, 1246-1255, 1401-1415` (MCP tool with structured fields: scope, decision, choice, rationale, revisable, when-context, made-by); `src/resources/GSD-WORKFLOW.md:234-260` (canonical table-shaped DECISIONS.md register definition); `src/resources/extensions/gsd/db-writer.ts:76-112, 455-489, 572-604` (canonical-table generator + saveDecisionToDb + dual-write structured memory record) | **gsd-2-internal decision-DB substrate.** Decision-trace skill must be evaluated against this existing structured primitive — DB-backed, MCP-exposed, canonical-table-generated. The earlier gap-mapping framed `.gsd/DECISIONS.md` as one-line append-only convention, missing the structured DB-shape that already exists. Shape D-style framing (schema enrichment) was thereby framed as more novel/heavier than gsd-2's actual surface warrants. Decision-trace overlaps with this primitive at WRITE side (existing) and extends at READ/RECONSTRUCT side (proposed). |
| `.gsd/DECISIONS.md` convention | Multiple writers above + canonical-table generator | **Substrate convention** — one-line append-only OR canonical-table-generated (per db-writer.ts:455-489). Earlier framing as "one-line append-only" only is incomplete; the canonical-table-generator emits structured tables. The existing convention is richer than initial gap-mapping surfaced. |
| Workflow templates: `bugfix.md`, `pr-review.md`, `refactor.md`, `spike.md` | `src/resources/extensions/gsd/workflow-templates/` | Markdown-phase prompt-dispatch templates; `spike.md` Phase 3 explicitly offers `spike-wrap-up`. Shape-comparison candidates if first-target is workflow-side |
| YAML deterministic workflows (`docs-sync.yaml`, `env-audit.yaml`, etc.) | `src/resources/extensions/gsd/workflow-templates/` | Engine-scheduled deterministic step sequences with verification policies; comparison shape if first-target is YAML-shaped |
| `.gsd/activity/*.jsonl`, `.gsd/journal/`, `.gsd/metrics.json` | gsd-2 runtime emission | Existing observable-state surfaces; decision-trace can READ these as evidence-source |
| **`/gsdr:deliberate` slash-command** (added per F-PD-B1; **prior-art-not-candidate-shape**) | gsdr-side at `~/.claude/commands/gsdr/deliberate.md` per M2 §0/§3 | **gsd-2-adjacent-runtime prior-art comparator.** M2 ranked as decisive structural overlap with decision-trace semantics — implementing trigger taxonomy + severe-testing + falsifiable predictions + evaluation-status lifecycle on `.planning/deliberations/` (the same artifact class). **EXCLUDED from candidate-shape set on R-strategy grounds** (gsdr lives on Claude Code; gsd-2 cannot consume its slash-commands at runtime; the *replacement* question is closed by acausal-runtime). **PRESERVED as prior-art comparator** because the *coverage* question is independent: the work the proposed decision-trace skill is supposed to handle already gets done by `/gsdr:deliberate` in adjacent runtime. RELATIONSHIP-TO-PARENT.md §1 frames substrate as "gsd-2 + Claude Code runtime + dev tooling + organizational conventions jointly" — adjacency-runtime is in-scope for substrate-shape evaluation, even if not in-scope for R-strategy candidate-shape selection. Phase D evidence on "decision-trace skill works" must be readable against this comparator at Phase E. |
| `~/.gsd/knowledge/signals/*` | gsdr-side (not gsd-2-side) per M2 | **EXCLUDED from gap-mapping at substrate level** — gsdr substrate, not gsd-2; not in either candidate-shape set or comparator set (no decision-trace-relevant overlap surfaced) |

The gap-mapping has two consequential layers: (1) the **`forensics` skill** as closest gsd-2-internal *skill-shape* analog (post-mortem reconstruction of past events from observable state); and (2) the **`gsd_decision_save` + DECISIONS.md canonical-table + db-writer** family as gsd-2-internal *decision-record-shape* substrate that decision-trace extends at READ side; and (3) the **`/gsdr:deliberate`** prior-art-not-candidate-shape comparator as adjacent-runtime evidence-base for whether the work-shape is novel-by-runtime-not-by-content. All candidate decision-trace shapes articulate gap vs `forensics` + `gsd_decision_save` family explicitly; differentiation vs `/gsdr:deliberate` is a Phase D evidence question (per MINI-SPEC §2.2 B5b/B5c rows added per disposition).

### §1.4 Standing-constraint carry-forward (from §7 dispositions + Step 0)

These constraints apply across all candidates uniformly:

- **A+F primary anchoring** (§7.4): skill design optimized for solo-research-over-years comprehension (A) + transition-as-stance optionality (F). NOT optimized for B (small-team) or C (enterprise) primary.
- **Reversibility** (§7.10.4 spike-sizing + spike-program METHODOLOGY): Phase D is a spike. Working-branch R2 is reversible (revert branch); R4 is reversible (`rm -rf`); upstream PR is NOT reversible at this scope. PR-step is Phase-E-conditional.
- **§7.9.3 (a) R4 contrast requirement**: Step 4 disposition must address — Logan disposes (i) parallel R4 comparator / (ii) effective-state-emission integration as comparator / (iii) explicit declaration that R4 not tested by this first-target. Default heuristic per §7.9.3: (i) or (ii) preferred.
- **§7.9.3 (c) Phase D dispatch contract** (mini-spec): each candidate must support Step 3 mini-spec draftability — artifact / skill behavior / workflow scope / decision-trace evidence definition / F-discipline observability + §7.10 amendments H4/H5/M5.
- **P5 effective-state caveat** (Step 0 P5 finding): skill cannot rely on `headless query` / MCP `gsd_progress`/`gsd_query` / `prefs status` for effective preferences/skills/hooks/extensions. Read `PREFERENCES.md` files directly (`~/.gsd/PREFERENCES.md` global + `.gsd/PREFERENCES.md` project; merge per `loadEffectiveGSDPreferences` semantics: project-wins-on-scalars, arrays-concat, plus profile-defaults and mode-defaults at lowest priority) OR use in-process `loadEffectiveGSDPreferences()` API. Layer attribution (which layer set a value) is load-bearing for decision-trace because runtime config shapes decision context.
- **H5 substrate-vs-first-target channel separation** (§7.10.1): claims about "decision-trace skill/workflow works/doesn't work" must NOT auto-extend to "gsd-2 substrate handles long-arc decision-trace work well/poorly." Cross-references to general substrate properties require explicit anchoring.
- **H4 falsification criteria** (§7.10.1): Step 3 mini-spec must specify what evidence would tell us decision-trace is the WRONG first-target (inverse of successful-evidence definition).
- **M5 per-decision test-case-vs-substrate rule** (§7.10.2): each implementation choice within Phase D must land on one side or the other (test-case-anchored: arxiv-sanity-mcp specific; substrate-anchored: gsd-2-general). Mini-spec carries the rule.

## §2. Standing constraints carried into all candidates

Re-articulated in compact form for Step 1 reading-frame; each candidate sub-section below applies these uniformly without re-statement.

1. **A+F-primary anchoring; B-adjacency preserved.** Plural-context per §7.4; not B-primary or C-primary.
2. **Reversibility ≥ medium for Phase D first-target.** Excludes upstream PR commitment within Phase D scope.
3. **P5 effective-state caveat operative.** Skill reads PREFERENCES.md or in-process API; not emission surfaces.
4. **§7.9.3 (a) R4 contrast at Step 4 disposition.** Required regardless of primary candidate.
5. **H5 channel separation.** Specific-evidence claims do not auto-extend to substrate-general claims.
6. **H4 falsification.** Step 3 mini-spec carries inverse-of-success criteria.
7. **M5 per-decision rule.** Test-case-vs-substrate categorization at each implementation choice.

## §3. Five candidate shapes

### §3.A Shape A — User-side gsd-2 skill at `~/.agents/skills/decision-trace/`

**Architectural shape.** Single SKILL.md file (or router pattern with `workflows/`, `references/`, `templates/`, `scripts/` subdirectories per `create-skill/SKILL.md:23-34`) at user-side discovery location `~/.agents/skills/decision-trace/SKILL.md`. Discovered by gsd-2 at runtime via `packages/pi-coding-agent/src/core/skills.ts:15-26, 421-433`. Activation via three-layer pattern (always-loaded catalog injection + per-unit-type allowlist + user-preference layer per M2 §2). The skill is a **prompt** — pure markdown with YAML frontmatter, ≤500 lines per `create-skill` doctrine, descriptions keyword-rich for discoverability.

**Integration surfaces.** None modified in gsd-2. Skill becomes available globally to any gsd-2 project that runs after install. Activation conditions written into the description (e.g., "Use when reconstructing why a past decision was made over multi-year project lifetimes").

**R-strategy.** **R4-by-construction wrt gsd-2.** No gsd-2 codebase modification; the skill lives in user-discovery space. R2 wrt the user's `~/.agents/skills/` ecosystem (skills.sh standard) — but that's not gsd-2-uplift-relevant.

**Existing gsd-2-internal-primitive gap-mapping.**
- vs `forensics`: `forensics` traces failed auto-mode runs from symptom to root cause; decision-trace traces *successful* decisions from outcome to rationale. **Differentiation:** forensics is symptom-driven (something went wrong); decision-trace is reconstruction-driven (which decision shaped this outcome). Composable: decision-trace can invoke forensics for failure-side analysis.
- vs `spike-wrap-up`: `spike-wrap-up` packages spike findings into durable project-local skills; decision-trace surfaces past decisions. **Differentiation:** spike-wrap-up is forward-looking (capture for future use); decision-trace is backward-looking (reconstruct from past).
- vs `design-an-interface` + `write-milestone-brief`: both append to `.gsd/DECISIONS.md` at decision-time; decision-trace reads + reconstructs at future-recall-time. **Differentiation:** capture (existing) vs reconstruction (new).
- vs `.gsd/DECISIONS.md` convention: skill READS the convention; doesn't replace it. **Composable.**
- vs `handoff`: `handoff` writes `continue.md` for session-pickup; decision-trace writes/reads decision-trail artifacts for cross-session reconstruction. **Adjacent at session-bridging boundary.**

**P5 caveat inheritance.** Skill prompt explicitly instructs the model to read `~/.gsd/PREFERENCES.md` + `.gsd/PREFERENCES.md` directly (or invoke `gsd doctor` if it surfaces effective state, per M2 spot-check). Layer attribution (project / global / profile / mode) preserved in trace artifact format.

**Cheap-vs-informative tradeoff.** Cheap (single SKILL.md ≤500 lines, no gsd-2 source modification, install via `cp -r`). Informative dimension: tests gsd-2's user-side skill discovery + activation pattern + description-keyword matching for decision-trace semantics. **Does NOT test:** gsd-2 internal contribution culture, skill manifest authoring as gsd-2 ships it, workflow-template integration, surface stability under gsd-2 release cadence.

**Phase-E inheritance.** Phase E reads: does the user-side skill activate when expected? Does description-keyword matching surface it appropriately? Do users (Logan + future-Claude) find the trace artifacts useful? **Limited evidence on substrate-shape questions** (skill manifest design, workflow integration); §7.4 substrate-shape-anchoring projection risk preserved at this candidate.

**Per-candidate audit-priority risks.**
- **R4-only-evidence under-specifies substrate-shape.** Phase E inherits "substrate handles user-side decision-trace skills well/poorly" but not "substrate handles in-tree decision-trace skills well/poorly." §7.9.3 (a) R4 contrast paradoxically inverts: this *is* the R4 path; comparator must be R2-shaped (Shape D, E, or F) for contrast to fire.
- **User-discovery is gsd-2-discovery-not-substrate-discovery.** A user-side skill discovered by gsd-2 doesn't test whether *gsd-2's design* is the substrate property of interest; it tests whether the user's `~/.agents/skills/` ecosystem composes with gsd-2 reasonably. Different question.
- **Description-keyword discoverability is brittle.** Per `create-skill` doctrine line 58: "Description... 120-1024 chars, keyword-rich. Must state when the agent should load it. Rewrite at least twice before settling." Decision-trace's keyword space ("decision," "trace," "rationale," "why," "past decisions," "long-arc," "reconstruction") may collide with deliberation/audit/forensics activation conditions. Step 3 mini-spec needs description-discrimination work.

### §3.D Shape D — `.gsd/DECISIONS.md` schema/policy enrichment + thin orchestration

**Architectural shape.** Three coordinated changes in gsd-2:
1. **Schema enrichment** of `.gsd/DECISIONS.md` from one-line append-only convention to structured (but still markdown-readable) entries with explicit fields: decision-id, date, milestone-id, slice-id (optional), task-id (optional), decision-summary, rationale, alternatives-considered, predictions, evaluation-trigger (optional). Schema versioned (front-matter `schema_version: 1.x`).
2. **Skill modifications**: `design-an-interface` + `write-milestone-brief` + `spike-wrap-up`'s wrap-up-offer + `spike.md` workflow Phase 3 — all updated to write structured entries matching the new schema. Pure additive (default to old shape if schema flag absent).
3. **New `decision-trace` skill** at `src/resources/skills/decision-trace/SKILL.md` (in-tree; thin orchestration) that READS `.gsd/DECISIONS.md` + cross-references to `.gsd/activity/*.jsonl`, `.gsd/journal/`, milestone summaries, slice context files; produces decision-trail reconstruction artifacts.

**Integration surfaces.** `.gsd/DECISIONS.md` (schema); existing decision-writing skills (modifications); new decision-trace skill (additive). All three changes ship together; partial commits make schema inconsistent.

**R-strategy.** **R2 in-tree on working-branch.** No upstream PR within Phase D. If Phase E evidence supports, R5-conditional upstream consideration (deferred per §7.3.b "R3-probe-fire-timing not-fired-this-arc"; PR step is Phase-E-conditional gating R3 probe re-disposition).

**Existing gsd-2-internal-primitive gap-mapping.**
- vs `.gsd/DECISIONS.md` convention: **direct extension.** Schema enrichment adds structure without breaking existing one-line entries (default-fallback handling). Existing writers are updated to write enriched entries; readers (the new decision-trace skill + future readers) consume both shapes.
- vs `design-an-interface` + `write-milestone-brief`: **modification, not replacement.** These skills continue to capture decisions; they now capture richer decisions. Differentiation preserved (interface design vs milestone brief vs spike wrap-up).
- vs `spike-wrap-up`: **modification + composition.** Spike-wrap-up offer-flow updated to write structured entries; decision-trace skill READS spike-wrap-up's artifacts as evidence-source.
- vs `forensics`: **complementary.** Forensics is symptom-driven post-mortem of failed auto-mode; decision-trace is reconstruction-driven recall of past decisions. Decision-trace skill MAY invoke forensics for the failure-side of the trace.
- vs workflow templates (`spike.md` Phase 3 offers `spike-wrap-up`): **integration point.** Spike workflow Phase 3 update writes structured entry to `.gsd/DECISIONS.md`.

**P5 caveat inheritance.** decision-trace skill's prompt instructs reading PREFERENCES.md directly + invoking `loadEffectiveGSDPreferences()` if available in-process (skill is a prompt; in-process API access depends on dispatch context). For runtime config layer attribution, decision-trace reads schema_version field + per-entry timestamps to reconstruct which preference layer was active when each decision was made.

**Cheap-vs-informative tradeoff.** Medium-cost (3 coordinated changes; schema versioning + 3-4 skill updates + 1 new skill; ~3-5 days of work). Informative dimension: tests gsd-2 *as-it-ships* — skill manifest authoring, in-tree skill integration, schema-versioning convention adoption, multi-skill coordination, `.gsd/DECISIONS.md` substrate evolution. **Does NOT test:** upstream PR receptivity (deferred), breaking-change practice on a real change (this would only become real on PR), surface stability of `.gsd/DECISIONS.md` convention upstream (Logan-side evidence only).

**Phase-E inheritance.** Phase E reads: does the schema enrichment compose elegantly with existing one-line convention (or feel grafted-on)? Do existing decision-writing skills produce richer entries naturally (or is it forced)? Does decision-trace reconstruction work at multi-year scale (when the schema_version changes between entries)? Does forensics composition surface useful failure-side context? **Strong evidence on substrate-shape questions** — this candidate stresses gsd-2's actual surface design.

**Per-candidate audit-priority risks.**
- **Working-branch R2 may drift toward commitment.** Per §7.10 H7 + spike-program reversibility: working-branch R2 is technically reversible but the longer the branch lives, the harder reversal becomes. Step 2 must set explicit branch-lifetime budget + abort criteria.
- **Schema-versioning is a substrate-convention claim.** Adding `schema_version: 1.x` to `.gsd/DECISIONS.md` proposes a versioning convention gsd-2 doesn't currently have for that file. Phase E read must distinguish "the convention is necessary" from "the convention got proposed by this Phase D and is unjustified beyond it."
- **Multi-skill coordination is a touchpoint-multiplier.** 4 skills modified + 1 added = 5 surfaces of change. Higher chance of inconsistency. Step 3 mini-spec must operationalize coordination discipline (single PR-equivalent commit; verification runs across all surfaces).
- **`.gsd/DECISIONS.md` is per-project, not per-substrate.** Each gsd-2 user has their own DECISIONS.md; decision-trace works per-project. The substrate-shape evidence is "gsd-2's per-project decision capture pattern handles structured schema well/poorly" — NOT "gsd-2 supports cross-project decision-trace" (which would require a different surface, possibly `~/.gsd/knowledge/decisions/` analog — not in gsd-2's current shape per M2).

### §3.E Shape E — In-tree gsd-2 skill + (optional) workflow template

**Architectural shape.** Two coordinated changes in gsd-2:
1. **New skill** at `src/resources/skills/decision-trace/SKILL.md` — in-tree, ships with gsd-2's bundled skills. Frontmatter: name (`decision-trace`), description (decision-trace activation conditions, keyword-rich), no `disable-model-invocation`. Body: pure-prompt instructions for decision-trace work (read DECISIONS.md / activity / journal / milestone summaries; produce reconstruction artifact at `.planning/decisions/<slug>.md` or analog).
2. **(Optional) workflow template** at `src/resources/extensions/gsd/workflow-templates/decision-trace.md` (markdown-phase prompt-dispatch). Multi-phase: Phase 1 scope (which decision(s) to trace) → Phase 2 evidence-gathering (read DECISIONS.md + cross-references) → Phase 3 reconstruction (synthesis with rationale chain) → Phase 4 evaluation (predictions check if applicable) → Phase 5 output (artifact write + DECISIONS.md back-reference).

**Integration surfaces.** New skill in `src/resources/skills/`; (optional) new workflow template in `src/resources/extensions/gsd/workflow-templates/`. May require entry in `unit-context-manifest` if per-unit-type allowlist applies (M2 §2 — would the skill be allowlisted for `research-milestone` / `complete-milestone` / `validate-milestone` / `reassess-roadmap`? Most plausibly all four).

**R-strategy.** **R2 in-tree on working-branch** (same as Shape D). PR-step Phase-E-conditional.

**Existing gsd-2-internal-primitive gap-mapping.**
- vs `forensics` (closest analog): forensics traces *failed* auto-mode runs; decision-trace traces *any* past decision (success or failure). **Differentiation:** scope is broader; not auto-mode-specific. Composable: decision-trace can invoke forensics for the auto-mode-failure subset.
- vs `spike-wrap-up`: spike-wrap-up packages spike findings into project-local skills; decision-trace reconstructs decision rationale from observable state. **Differentiation:** package-for-future vs reconstruct-from-past.
- vs `design-an-interface` / `write-milestone-brief`: those skills CAPTURE decisions at decision-time; decision-trace RECONSTRUCTS at recall-time. Decision-trace reads what those skills wrote. **Differentiation:** capture (existing) vs reconstruction (new). NOT modifying existing capture skills (that's Shape D).
- vs `.gsd/DECISIONS.md` convention: decision-trace READS the convention as-is (one-line append-only). Does NOT modify the convention (that's Shape D's territory). **Compatibility constraint:** Shape E works with existing one-line entries; doesn't require schema enrichment. (If both Shape D + Shape E: Shape E reads enriched schema; default-fallback to one-line.)
- vs workflow templates (`bugfix.md`, `pr-review.md`, `refactor.md`, `spike.md`): decision-trace.md (if implemented) is a peer template. **Differentiation:** decision-trace is reconstruction-shaped; bugfix/pr-review/refactor/spike are forward-action-shaped.

**P5 caveat inheritance.** Same as Shape A — skill prompt instructs reading PREFERENCES.md directly + per-entry timestamps for layer attribution. Workflow template (if implemented) carries the same instruction in Phase 2 evidence-gathering.

**Cheap-vs-informative tradeoff.** Cheap-to-medium (skill: 1 SKILL.md ≤500 lines + manifest entry; workflow template: optional, adds 2-3 days). Informative dimension: tests gsd-2's in-tree skill authoring discipline (frontmatter, description, structure), per-unit-type allowlist integration, workflow-template-vs-skill boundary (M2 §4). **Does NOT test:** `.gsd/DECISIONS.md` substrate evolution (that's Shape D's territory; Shape E reads the existing convention).

**Phase-E inheritance.** Phase E reads: does the new skill activate when expected (description-keyword matching for decision-trace semantics)? Does workflow-template composition (if implemented) feel natural alongside existing markdown-phase templates? Does the per-unit-type allowlist need extension for decision-trace (M2 §2 manifest doesn't currently include reassess-roadmap; if decision-trace primarily fires at reassess-roadmap, allowlist needs update)? **Medium evidence on substrate-shape questions** — tests skill design + workflow integration but not multi-skill coordination.

**Per-candidate audit-priority risks.**
- **Skill-vs-workflow boundary may force a Step 2 question prematurely.** If decision-trace is best-shaped as workflow (multi-phase reconstruction) but Step 1 candidate is skill-only, evidence yield is partial. Step 3 mini-spec must dispose skill-only vs skill+workflow.
- **Per-unit-type allowlist update is its own design decision.** decision-trace activates at which lifecycle steps? `complete-milestone` for trace-back-on-completion? `reassess-roadmap` for decision-recall during re-planning? Both? Allowlist update ≠ skill body ≠ workflow template — three coordinated changes if all apply.
- **In-tree skill description keyword-space collides with `forensics` and `handoff`.** "trace," "reconstruct," "recall," "history," "past" — overlap territory. Description-discrimination work at Step 3 mini-spec.
- **R5-conditional upstream surfaces R3-probe.** If Phase E evidence licenses upstream PR for the new skill (R5), the deferred R3 contribution-culture probe (per §7.3.b) MUST fire pre-PR. Phase E re-disposes §7.3.b if it fires.

### §3.F Shape F — Hook-pattern primitive (out-of-scope-this-arc; enumerated for completeness)

**Architectural shape.** New primitive in gsd-2 core: file-edit-time hooks that fire on user/agent edits to specific files, loading specified docs/skills before continuing. M2 §5 confirmed gsd-2 has NO existing hook surface for edit-time triggers; this is **net-new core primitive**.

Implementation sketch (NOT a Step 3 mini-spec — only enumeration):
- Hook registration: `package.json` `gsd.extension.true` + `gsd-hooks` config block specifying `before-edit-X-load-Y` triggers; OR new `~/.agents/hooks/` analog directory.
- Hook engine: gsd-2 core listens for tool-use events matching Edit/Write/MultiEdit on specified path patterns; fires hook before tool dispatch.
- Hook output: instructions inserted into model context (similar to skill activation but trigger-driven).

**Integration surfaces.** Net-new core surfaces in gsd-2; package.json schema extension; tool-use event listener; hook configuration; activation engine. **Most invasive of all candidates.**

**R-strategy.** **R2 in-tree, core-shape change.** No working-branch reversibility — the change touches gsd-2's auto-prompts.ts + tool-use-event-handling + extension-validator + package.json schema. **R5-mandatory eventually** (would not stay on a fork without upstream commitment).

**Existing gsd-2-internal-primitive gap-mapping.**
- vs all existing skills + workflows: hook-pattern is a **different activation mechanism** (trigger-driven vs context-token-driven). No existing gsd-2 primitive uses this activation shape. New primitive class.
- vs `auto-prompts.ts` description-keyword similarity matching (M2 §5): the closest existing analog is *content-driven* activation. Hooks are *event-driven*. Different mechanism.
- vs `~/.gsd/skill-rules` user-preference layer: skill_rules are static `when X then use/prefer/avoid Y` matched against context tokens — still token-driven. Hooks are tool-use-event-driven.

**P5 caveat inheritance.** Hook-defined load-instructions can directly invoke `loadEffectiveGSDPreferences()` since they fire in-process. Less brittle than skill-prompt-instructed reading.

**Cheap-vs-informative tradeoff.** Expensive (core-shape change; auto-prompts integration; tool-use event handling; package.json schema; hook engine). Informative dimension: would test gsd-2's core extension discipline + breaking-change practice + contribution culture (R3 probe forced) + extension-validator behavior. **Highest substrate-shape-evidence yield** but **highest cost + lowest reversibility.**

**Phase-E inheritance.** N/A under "out-of-scope-this-arc" disposition. If activated at later Phase (post-Phase-D-evidence-warrant), Phase E reads core-extension-feasibility evidence.

**Per-candidate audit-priority risks (for the out-of-scope disposition).**
- **Excluding F may be premature if the test-case-vs-substrate diagnostic loop favors edit-time triggers.** RELATIONSHIP-TO-PARENT.md §1 emphasizes substrate-evidence channel; arxiv-sanity-mcp's CLAUDE.md doctrine-load-points are exactly the pattern Shape F would propose for gsd-2. Excluding F means gsd-2 substrate evidence on this pattern doesn't accumulate from Phase D.
- **F's exclusion is reversibility-grounded, not necessity-grounded.** Step 1 doesn't claim hooks aren't needed; it claims hooks aren't *Phase-D-spike-shaped*. Future Phases (E, F, beyond-G) may activate F.
- **Logan-discretion to override exclusion exists.** If Logan reads Phase D as the right place to test core-extension-shape (because we have direct intervention authority + open-source reframing argues against under-using it), F re-enters. The §6 Logan-disposition options table lists F as out-of-scope-this-arc + Logan-discretion override.

### §3.G Shape G — YAML deterministic workflow (user/project-side)

**Architectural shape.** YAML deterministic workflow at `.gsd/workflows/decision-trace.yaml` (project-local, preferred per `create-workflow/SKILL.md`) OR `~/.gsd/workflows/decision-trace.yaml` (global). Schema per M2 §4 (version: 1; explicit `steps[]` with IDs, dependency graph, verification policies). Steps:
- `scope` — identify decision(s) to trace (user input or auto-detect from context)
- `gather` — collect evidence from `.gsd/DECISIONS.md` + activity + journal + milestone summaries (verification: content-heuristic; output exists)
- `reconstruct` — synthesize rationale chain + alternatives + predictions (verification: prompt-verify; LLM-graded structural completeness)
- `evaluate` — predictions-check if applicable (verification: shell-command on artifact existence)
- `output` — write artifact + DECISIONS.md back-reference (verification: file-exists)

**Integration surfaces.** None modified in gsd-2. Workflow runs via `custom-workflow-engine.ts`; user installs via filesystem placement.

**R-strategy.** **R4-by-construction** (user/project-side; no gsd-2 codebase modification).

**Existing gsd-2-internal-primitive gap-mapping.**
- vs YAML workflow templates already in gsd-2 (`docs-sync.yaml`, `env-audit.yaml`, etc.): peer-shape; same engine; same verification policies. **Differentiation:** content (decision-trace specific). Tests deterministic-engine for reconstruction-shaped work specifically.
- vs markdown-phase workflow templates (`bugfix.md`, `spike.md`, etc.): different engine (deterministic vs prompt-mediated). **Differentiation:** decision-trace as YAML tests "is reconstruction work better-shaped as deterministic steps or prompt-mediated phases?" Phase-E-evidence question.
- vs Shape A (user-side skill): different artifact type (workflow vs skill). Both R4. Compositional: skill could invoke workflow, or workflow could compose with skill.
- vs Shape D + E: different R-strategy. R4 vs R2.
- vs `.gsd/DECISIONS.md` convention: workflow READS as-is; Shape G doesn't modify the convention (that's Shape D's territory).

**P5 caveat inheritance.** Workflow steps run via the engine; can directly invoke `loadEffectiveGSDPreferences()` from within step bodies if exposed via engine context. Less brittle than skill-prompt instruction.

**Cheap-vs-informative tradeoff.** Cheap (1 YAML file ≤200 lines; install via filesystem placement). Informative dimension: tests gsd-2's deterministic-engine for reconstruction-shaped work + verification-policies for LLM-graded structural completeness + dependency-graph composition. **Does NOT test:** in-tree skill authoring, multi-skill coordination, schema convention evolution.

**Phase-E inheritance.** Phase E reads: does the deterministic engine handle reconstruction-shaped work elegantly (or is it too rigid for synthesis-style steps)? Do verification policies (prompt-verify in particular) catch incomplete reconstructions? Is the dependency graph + step IDs over-engineered for a 5-step reconstruction workflow? **Medium evidence on substrate-shape questions** — focused on engine behavior.

**Per-candidate audit-priority risks.**
- **YAML-shape may be wrong-fit for reconstruction work.** Deterministic engines work best when steps are mechanically definable; reconstruction is synthesis-shaped (model judgment, not deterministic). Phase E read may favor markdown-phase templates over YAML for this work — if so, Shape G's evidence yield is "YAML-engine-not-fit-here" rather than "reconstruction-works."
- **Composability with §7.4 anticipated-shifting (F-discipline)**: YAML workflows are static-ish (steps + dependencies pre-declared); F-discipline anticipates progressive activation. May not test F well.

## §4. Cross-candidate considerations

### §4.1 Composition possibilities

R-strategies compose per framing-widening §1.3. Step 1 surfaces compositions that are operationally coherent:

- **A + D**: user-side skill (A) + DECISIONS.md schema enrichment (D). R4 + R2 in-tree. The skill at `~/.agents/skills/` reads enriched DECISIONS.md. **Coherent**; tests both surfaces.
- **D + E**: schema enrichment (D) + new in-tree skill (E). Both R2 in-tree. The new skill consumes the enriched schema; existing skills updated to write it. **Coherent**; tightest substrate-shape coverage but highest coordination cost.
- **A + E**: user-side prototype (A) → in-tree promotion (E). R4 → R2 evolution path. **Coherent across phases** — A in Phase D, E in Phase E if A's evidence licenses.
- **A + G**: user-side skill + user-side YAML workflow. Both R4. Skill description references the workflow; workflow body invokes synthesis steps the skill describes. **Coherent**; tests both R4 surfaces.
- **D + E + G**: maximum coordination. Schema (D) + skill (E) + YAML workflow (G — but in-tree at `src/resources/extensions/gsd/workflow-templates/` rather than user-side, making it R2). **High coordination cost; highest substrate-shape coverage but exceeds spike-sizing envelope per §7.10.4 + spike-program METHODOLOGY.**

### §4.2 §7.9.3 (a) R4 contrast — how each composition satisfies

| Composition | R4 contrast satisfied via |
|---|---|
| A only | A *is* the R4 path — needs an R2 comparator (D, E, or F) to satisfy contrast |
| D only | D is R2 — needs an R4 comparator (A or G) |
| E only | E is R2 — needs an R4 comparator (A or G) |
| F only | F is R2 core-change — needs an R4 comparator (A or G) |
| G only | G is R4 — needs an R2 comparator (D, E, or F) |
| A + D | Built-in contrast (A=R4, D=R2) |
| D + E | Both R2 — needs an R4 comparator (A or G) added |
| A + E | Built-in contrast (A=R4, E=R2) |
| A + G | Both R4 — needs an R2 comparator (D, E, or F) added; OR Logan-disposes §7.9.3 (a)(iii) "R4 not tested by this first-target — Phase E dispatches separate R4-shaped first-target" (note: A+G ARE R4; (a)(iii) inverts to "R2 not tested — Phase E dispatches separate R2-shaped" which is reversal of original disposition spirit) |

Default heuristic per §7.9.3 (a): option (i) parallel R4 comparator OR (ii) effective-state-emission integration as R4 anchor preferred. The cleanest compositions for built-in contrast are **A + D**, **A + E**, **A + (D+E)**.

### §4.3 P5 effective-state caveat per composition

All compositions inherit the same P5 caveat (read PREFERENCES.md directly or use in-process API). Compositions with skill-only (A, E) instruct via prompt; compositions with YAML workflow (G) or hook (F) can invoke API directly. Compositions with schema enrichment (D) preserve layer-attribution evidence in the schema itself (timestamps + schema_version field).

### §4.4 H5 substrate-vs-first-target channel separation per composition

- **A only** + comparator: claims about "user-side skill discoverability" are first-target; substrate-shape claims require explicit anchoring beyond.
- **D + E**: tightest coupling between first-target and substrate (both modify gsd-2 directly). H5 discipline is hardest here — every claim must be carefully anchored. Per RELATIONSHIP-TO-PARENT.md §2 failure-mode 1, the test-case-anchoring → substrate-shape-anchoring projection is the audit-priority surface.
- **A + D**: cleaner channel separation — A tests user-side discovery (test-case-side); D tests in-tree convention evolution (substrate-side).

### §4.5 Audit-priority risks at this Step 1 layer

Per §7.10.6 audit-priority risks at the §7.10 layer + this Step 1's own layer:

1. **D5a recursion at Step 1 itself.** This artifact is Claude-drafted in-session-collaboration with Logan (§0.5 disposition-discipline applies recursively). Phase D entry audit per plan §2.4 row D paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load) reads §7.10 + Step 1 candidates + Logan's disposition + Step 3 mini-spec together — structural correction.
2. **Candidate-set completeness risk.** I surfaced 5 candidates drawing on M2's gsd-2-internal primitive inventory. M2 sampled 7+ skills and didn't read all 30+; M2's own §8 open question 1 flagged "non-exhaustive coverage." A 6th candidate I missed is possible; Phase D entry audit catches if so.
3. **R-strategy tagging is M2-derived; M2 was probe-shaped not audit-shaped.** R-strategy assignments per candidate use M2's framing. If an audit-shaped re-read of gsd-2 surfaces a different R-strategy taxonomy (e.g., R2-vs-R4 boundary fuzzier than M2's clean separation), candidate tags shift.
4. **"More control + open-source" reframing as Step 1 organizing logic.** §5 below recommends primary R2-in-tree; this is Logan's reframing applied to candidate weighting. If the reframing turns out to over-shift weight (e.g., reversibility argues louder than control-and-access), re-weight.
5. **Composition-table integration-grammar-as-fact risk.** §4.2 R4-contrast table presents compositions as if compositions are observed-facts of the candidate space. They're Claude's organizing structure. Phase D entry audit catches if any composition-claim functions as fact rather than option-surface.
6. **Each candidate's gap-mapping is bounded by M2's primitive sampling.** §3.X gap-mappings cite specific gsd-2 primitives; primitives outside M2's sample (e.g., 20+ skills not deeply read) may overlap. Step 3 mini-spec gap-mapping refinement.

## §5. Recommended primary + comparator emphasis (Logan-disposes per §6)

Per Logan-disposed framing (2026-04-30 /effort max):
- **"More control + open-source" reframing**: gsd-2 is open-source standalone runtime; we have direct intervention authority. Defaulting to R4-only would under-use that access.
- **Reversibility constraint**: Phase D is a spike (per §7.10.4 + spike-program METHODOLOGY). Working-branch R2 is reversible (revert branch); upstream PR is NOT reversible at Phase D scope.
- **Substrate-shape-evidence yield**: R2-in-tree generates evidence about gsd-2's surface design (skill manifest authoring, workflow integration, schema convention evolution) that R4 doesn't.

**Recommended primary**: Shape D OR Shape E (R2 in-tree on working-branch).
- **D leads** if Logan reads "extension of existing convention" as the cheaper, more-coherent-with-current-substrate path. Tests `.gsd/DECISIONS.md` evolution + multi-skill coordination + schema versioning convention.
- **E leads** if Logan reads "new first-class primitive" as the cleaner-new-surface-test path. Tests in-tree skill authoring + workflow-template-vs-skill boundary + per-unit-type allowlist integration.
- **D + E composition** is highest-coverage but exceeds spike-sizing envelope per §7.10.4 — defer one to Phase E.

**Recommended comparator**: Shape A (R4 user-side skill).
- Satisfies §7.9.3 (a) R4 contrast requirement at Step 4 disposition (option (i) parallel R4 comparator).
- Tests gsd-2's user-side discovery + activation pattern as a parallel surface.
- Cheap (single SKILL.md ≤500 lines + install).
- Composes with D or E without conflict.

**Recommended out-of-scope-this-arc**:
- Shape F (hook primitive — too invasive for spike; reversibility too low; would force §7.3.b R3-probe-fire-timing re-disposition).
- Shape G (YAML workflow — composable later if Phase D evidence licenses; testing engine fit is a Phase-E or later question).

**My weight of confidence on this recommendation: medium.** The reframing is real and load-bearing; reversibility-via-working-branch is preserved; substrate-shape evidence yield is highest at Shape D or E. **Steel-man counter:** if Phase D is supposed to be cheap-and-reversible-above-substrate-shape-evidence-yield, Shape A should be primary and Shapes D + E defer to Phase E. Defensible — spike-program METHODOLOGY emphasizes reversibility heavily. **My read: the "we have access; don't under-use it" argument outweighs "spike means cheapest" by a small margin under the reframing — but this is a Logan-disposable judgment call.**

## §6. Logan-disposition options

Logan disposes one (or composition) of these to operationalize Step 2 + Step 3.

### Primary candidate (one of)

- **§6.A — Shape A primary**: R4 user-side skill at `~/.agents/skills/decision-trace/`. Comparator: Shape D OR Shape E (R2 needed for §7.9.3 (a) contrast).
- **§6.D — Shape D primary**: `.gsd/DECISIONS.md` schema enrichment + in-tree decision-trace skill. Comparator: Shape A.
- **§6.E — Shape E primary**: in-tree decision-trace skill (+ optional workflow template) at `src/resources/skills/decision-trace/`. Comparator: Shape A.
- **§6.D+E — D + E composition**: schema enrichment + in-tree skill together. Comparator: Shape A. Higher cost; exceeds default spike-sizing — Logan-discretion to expand envelope or defer one to Phase E.
- **§6.F — Shape F primary**: hook-pattern primitive. **Out-of-scope-this-arc per §3.F default**; Logan-discretion override.
- **§6.G — Shape G primary**: YAML workflow. **Out-of-scope-this-arc per §3.G default**; Logan-discretion override.
- **§6.alt — Logan-disposed alternative**: shape not on the table; surface at §6 disposition with reasoning.

### Comparator (one of, conditional on primary)

Per §7.9.3 (a) R4 contrast — Logan disposes which:
- **(i) Parallel R4 comparator** (Shape A if primary is D/E/F; Shape D/E/F if primary is A/G) — preferred per §7.9.3 default heuristic.
- **(ii) Effective-state-emission integration as R4 anchor** — uses Step 0 P5 output as comparator surface; lighter than parallel candidate.
- **(iii) Explicit declaration** "R4 not tested by this first-target — Phase E dispatches separate R4-shaped first-target if (b)→(a) re-disposition warranted" — defensible if Logan disposes the §7.1 question is appropriately deferred to Phase E.

### Existing-primitive overlap discipline

- **(a) Step 1 candidates each carry explicit gap-mapping** (already in §3 above) — recommended; Logan accepts as drafted OR refines.
- **(b) Defer gap-mapping to Step 3 mini-spec** — Logan-discretion override.

### Out-of-scope-this-arc dispositions

- **F (hooks)**: confirm out-of-scope-this-arc (default) OR override (Logan-discretion to include).
- **G (YAML workflow)**: confirm out-of-scope-this-arc (default) OR override.

### Audit-priority risk acknowledgments

Per §4.5: D5a recursion + candidate-completeness + R-strategy-tagging-bounded + reframing-as-organizing-logic + composition-table-grammar + gap-mapping-bounded. Phase D entry audit per plan §2.4 row D reads this Step 1 + Logan-disposition + Step 3 mini-spec together as structural correction.

## §7. Cross-references

### Standing context (read alongside this Step 1)

- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7 dispositions; §7.9 audit addendum (gates 1+2+3+4); §7.10 negative-space survey (H1-H7 + M1-M5 + L1-L8 + §7.10.4 work-flow).
- `.planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/DISPOSITION.md` §8 Phase D entry pre-mini-spec amendment.
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` §1 + §2 (test-case-vs-substrate; failure-modes; H5 anchor).

### Step 0 outputs (load-bearing for Step 1)

- `.planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md` (P5 probe; sub-option (ii) caveat; standing constraint per §1.4).
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md` (M2 probe; primitives inventory; H1/H2/H3 evidence).

### Trajectory plan governance

- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §1.4 Phase D goal + §2.4 row D audit shape + §6.2 per-phase verification + §0.5 disciplines + §0.7 hybrid autonomy.

### Methodology grounding

- `.planning/spikes/METHODOLOGY.md` six interpretive lenses + paired-review practices A-F (load-bearing for spike-sizing M4 + Step 4 audit reasoning).
- `.planning/foundation-audit/METHODOLOGY.md` decision-review epistemic discipline.
- `.planning/deliberations/2026-04-28-framing-widening.md` §1 R-mix composition + §3.3 disposition-discipline + §9 deferred items (frame-revision availability if Phase D evidence licenses).

### Logan-correction reference

- 2026-04-30 /effort max turn: gsdr (our fork of v1 gsd; lives on Claude Code) ≠ gsd-2 (standalone open-source runtime; direct intervention authority). gsdr-side shapes (B, C from initial proposal) dropped per substrate clarification; Step 1 candidates are properly gsd-2-shaped. The "more control + open-source" reframing argues against under-using direct intervention authority via R4-only defaulting.

---

*Step 1 design-space framing artifact authored by Claude (Opus 4.7, xhigh effort) 2026-04-30 in-session-collaboration with Logan per trajectory plan §7.10.4 Step 1. Surfacing-shape, NOT Claude-disposition: Logan disposes at §6 to operationalize Step 2 + Step 3. The in-session-collaboration risk applies recursively to this artifact; the Phase D entry audit per plan §2.4 row D paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load) is the structural correction, reading §7.10 + Step 1 + Logan-disposition + Step 3 mini-spec together. Subject to same fallibility caveat as DECISION-SPACE.md §0.*
