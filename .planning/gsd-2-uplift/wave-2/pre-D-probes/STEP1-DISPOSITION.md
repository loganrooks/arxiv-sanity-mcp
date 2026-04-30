---
type: phase-D-step-1-disposition
date: 2026-04-30
gsd_2_commit: 42ef05fbe
phase: trajectory plan §1.4 Phase D — first-second-wave-target dispatch + execution
sub-step: §7.10.4 Step 1 disposition (post-design-space-framing; pre-Step-2 practical decisions; pre-Step-3 mini-spec)
status: |
  Logan-disposed 2026-04-30 (/effort xhigh turn) accept-as-stated of Claude-surfaced
  recommendation across all four §6 axes of STEP1-design-space.md. This artifact
  records the disposition + Claude's reasoning + sensitivity map + acknowledged
  audit-priority risks for Phase D entry audit (per plan §2.4 row D paired)
  read at Step 5.
authoring_discipline: |
  Authored by Claude (Opus 4.7, /effort xhigh, in-session-collaboration with Logan)
  per trajectory plan §7.10.4 Step 1 → Step 2 transition. The disposition reasoning
  here is Claude's auditable surfacing per Logan-prompt "How would you dispose each
  axis and why? Be transparent in your reasoning, render it auditable, be ready to
  be challenged on all fronts" at /effort max turn 2026-04-30. Logan disposed
  accept-as-stated at /effort xhigh turn shortly after. The /effort max → /effort
  xhigh sequence is itself part of the auditable trail: Claude's surfacing was
  performed at maximum reasoning effort; Logan's accept-as-stated was given at
  xhigh after surfacing.

  D5a in-session-collaboration risk applies recursively to this disposition — both
  Claude's reasoning AND Logan's accept-as-stated are co-produced under shared
  framing. Phase D entry audit per plan §2.4 row D paired (same-vendor xhigh
  adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load)
  reads §7.10 + STEP1-design-space.md + this disposition artifact + Step 3 mini-spec
  together — structural correction. The Step 5 audit is where this co-produced
  disposition is third-reader-stress-tested.

ground:
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md (the artifact under disposition)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md (standing constraint)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md (gsd-2-internal primitive inventory)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7.10.4 + §7.10.5 (work-flow + executor checklist)
  - .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md §1.4 + §2.4 row D (Phase D goal + audit shape)
  - .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (test-case-vs-substrate; H5 anchor)
read_order: |
  - For "what was disposed and how": §1 dispositions table.
  - For "Claude's reasoning per axis": §2.A through §2.D (one section per axis).
  - For "principal challenges + defenses": §3 per-axis defense.
  - For "how dispositions would change under different factors": §4 sensitivity map.
  - For "audit-priority risks Claude is acknowledging": §5.
  - For "what Phase D entry audit (Step 5) reads": §6 cross-references.
---

# Phase D Step 1 — Disposition record

> **Standing clarification (added per Phase D entry audit F-PD-B5 disposition, applied 2026-04-30):** References to /effort max → /effort xhigh sequence in this corpus's provenance blocks (here at §0 + §5 #6, and at parallel locations in STEP2-practical-decisions.md, MINI-SPEC.md, STEP4-gates-and-L-tier.md frontmatters) are **procedural-traceability records, not disposition-authority claims**. Claude's surfacing was performed at maximum reasoning effort; Logan's accept-as-stated was given at xhigh after surfacing. This sequence preserves the auditable trail of what reasoning surface produced what artifact at what effort — it is evidence-of-deliberate-acceptance, NOT evidence-of-cleared-quality. The Phase D entry audit per plan §2.4 row D paired (same-vendor adversarial-auditor xhigh + cross-vendor codex GPT-5.5 high) is the structural correction; Logan's acceptance does not substitute for it.

This artifact records Logan's accept-as-stated disposition (2026-04-30 /effort xhigh) of Claude's recommended primary + comparator + gap-mapping discipline + out-of-scope-this-arc confirmations across all four §6 axes of STEP1-design-space.md, plus the auditable reasoning trail Claude surfaced at /effort max immediately prior.

## §1. Dispositions

| Axis | Disposition | Logan-disposition | Confidence |
|---|---|---|---|
| **1 — Primary candidate** | **§6.E** — Shape E (in-tree gsd-2 skill at `src/resources/skills/decision-trace/`); skill-only at Phase D, workflow template option deferred to Step 2 (default: Phase E) | accept-as-stated | medium (load-bearing judgment at "more control + open-source" reframing weight) |
| **2 — Comparator** | **§6.E.(i)** — parallel R4 comparator (Shape A: user-side `~/.agents/skills/decision-trace/SKILL.md`, single SKILL.md ≤500 lines + install) | accept-as-stated | medium-high |
| **3 — Gap-mapping discipline** | **§6.(a)** — at Step 1 as drafted in §3 of STEP1-design-space.md; Step 3 mini-spec deepens for E + A | accept-as-stated | high (standard pattern) |
| **4 — Out-of-scope-this-arc** | **§6.F + §6.G both confirmed OOS-this-arc** — F (hooks) reversibility-grounded exclusion, available for re-entry at Phase E+ if licensed; G (YAML workflow) composable with E later | accept-as-stated | medium-high |

**Logan-disposition turn:** /effort xhigh, 2026-04-30. Logan-prompt verbatim: *"accept as stated, try to leave an auditable trail of this reasoning as usual"*. Disposition is co-produced under the /effort max preceding turn (Claude's full reasoning surface) + /effort xhigh disposition turn (Logan's accept).

## §2. Claude's reasoning per axis (the surfacing under accept-as-stated)

### §2.A Axis 1 — Primary §6.E

**Position defended:** Shape E primary (in-tree gsd-2 skill at `src/resources/skills/decision-trace/`); skill-only at Phase D, workflow template option deferred.

**Reasoning chain:**

1. **The "more control + open-source" reframing rules out A-only as primary.** A's evidence yield is gsd-2-discovery (does `~/.agents/skills/` ecosystem compose with gsd-2 runtime?), not gsd-2-design (does the actual surface design support this work?). Defaulting to A under-uses direct intervention authority Logan-correction surfaced at 2026-04-30 /effort max. We have source access; not operating around an opaque substrate.

2. **The reframing does NOT argue for maximum invasiveness — F is too core-shape-changing for spike.** Hook primitives touch auto-prompts.ts + extension-validator + tool-use event handling + package.json schema; reversibility envelope exceeded. F also forces §7.3.b R3 contribution-culture probe (deferred). Spike-program METHODOLOGY argues reversibility ≥ medium.

3. **Between D and E, E is the cleaner test of the actual question.** D modifies a CONVENTION (`.gsd/DECISIONS.md` schema) — schema-versioning is a substrate-convention claim gsd-2 doesn't currently have for that file, bundling "convention is necessary" with "decision-trace works elegantly" so Phase E read can't separate them cleanly. E adds a NEW PRIMITIVE alongside existing 30+ skills with no convention-versioning claim. E's cost is lower (1 new skill ≤500 lines vs 4-5 modifications + 1 new + schema-versioning + multi-skill coordination). E preserves more reversibility (single artifact addition; no convention modification cascading). E's failure mode is "the new skill doesn't fire well" — clean, falsifiable, doesn't drag a separate convention claim.

4. **E's audit-priority risks are tractable at Step 2/3.** Skill-vs-workflow boundary risk: Step 2 disposes "skill-only Phase D; workflow template deferred to Phase E if licensed." Description keyword-space collision with `forensics`/`handoff`: Step 3 mini-spec carries description-discrimination work. Per-unit-type allowlist update: that IS substrate-shape-evidence Phase D should test — force the question.

5. **CLAUDE.md "Stack D foreclosed" pattern applies recursively at Phase D scoping.** "The maximalist Stack D... is foreclosed because it commits compute and complexity that v0.x has no evidence to justify; the trajectory remains open if v0.3+ evidence warrants reopening" — the project-level discipline applies to D's bundling: schema-versioning + new skill + 4-5 skill modifications. Trajectory remains open to D at Phase E if E's evidence licenses it. **(Per Phase D entry audit F-PD-B4 disposition, applied 2026-04-30: Item 5 is rhetorical reinforcement; the disposition rests on items 1-4. Phase D entry audit can disregard item 5 if it does not add ground beyond items 1-4 — the structural similarity between project-level Stack D foreclosure and Phase-D-scope Shape D bundling is real but the dispositional weight is shallow; the ground for Shape E over Shape D should be Phase-D-internal per items 1-4, not pattern-match from product trajectory.)**

### §2.B Axis 2 — Comparator §6.E.(i)

**Position defended:** Parallel R4 comparator (Shape A — user-side gsd-2 skill at `~/.agents/skills/decision-trace/`).

**Reasoning chain:**

1. **(i) preferred per §7.9.3 default heuristic** — parallel R4 gives clean contrast. A as user-side, E as in-tree, both about decision-trace skill semantics. Phase E reads "did A's user-side discovery fire well? Did E's in-tree integration fire well? Where do they diverge?" — exactly the contrast Phase E's go/no-go needs.

2. **(ii) effective-state-emission as R4 anchor inverts P5's actual finding.** P5 returned "moderate drift; sub-option (ii) caveat — do NOT re-scope Phase D wholesale." Using effective-state-emission as R4 anchor turns P5's finding into design-input rather than standing-constraint — category mistake. Cleaner to keep P5 as standing constraint per STEP1-design-space.md §1.4 and run A as parallel R4.

3. **(iii) deferred-to-Phase-E without evidence basis is unfounded.** Phase E's stability claim about "disposition holds across R-strategies" requires both R-strategies' evidence. Deferring R4 to Phase E means Phase E reads only R2 evidence and dispatches a separate R4 first-target — running two Phase D's serially when (i) gives both at once cheaply.

4. **A's cost is bounded:** single SKILL.md ≤500 lines + filesystem install. Cost-of-running-comparator < contrast-value.

### §2.C Axis 3 — Gap-mapping discipline §6.(a)

**Position defended:** Accept §3 candidate gap-mappings as Step 1 design-space framing; Step 3 mini-spec deepens for E + A.

**Reasoning chain:**

1. Gap-mapping at Step 1 is *bounded* (which existing primitives this candidate composes-with vs differentiates-from); at Step 3 mini-spec it's *deepened* (specific behavior boundaries, description keywords, allowlist entries, evidence sources).

2. Pure deferral to Step 3 loses Step 1 organizing logic — Logan can't compare candidates at design-space-framing layer if gap-mapping is absent until Step 3.

3. STEP1-design-space.md §4.5 audit-priority risk #6 explicitly acknowledges M2's primitive sampling bounds Step 1 gap-mapping — Step 3 refinement is the right pattern, and Phase D entry audit per plan §2.4 row D catches sampling gaps.

### §2.D Axis 4 — F + G out-of-scope-this-arc confirmations

**Position defended:** Confirm F + G both OOS-this-arc.

**F reasoning:**

1. Net-new core primitive in gsd-2; reversibility envelope exceeded.
2. Forces §7.3.b R3 contribution-culture probe re-disposition (Logan-disposed "not-fired-this-arc"); needs Phase D evidence first.
3. Exclusion is reversibility-grounded, not necessity-grounded. F re-enters at Phase E+ if licensed.

**G reasoning:**

1. G's evidence yield is engine-fit-for-reconstruction-shaped-work — narrow, Phase E or later question.
2. G composable with E later as evolution path: Phase D's E + Phase E's G if licensed.
3. G's R-strategy is R4-by-construction; doesn't add to E+A's R-contrast at Phase D.

## §3. Principal challenges + defenses (the auditable defense surface)

### §3.A Challenges to axis 1 (E primary)

| Challenge | Defense |
|---|---|
| "Why not D? Tests more surfaces." | D bundles schema-versioning convention claim with decision-trace skill claim — Phase E can't separate them cleanly. Foreclosure pattern from CLAUDE.md applies recursively: introducing complexity Phase D may not have evidence to justify. |
| "Why not D+E? Maximum coverage." | D+E exceeds default spike-sizing envelope per §7.10.4 + spike-program METHODOLOGY M4. Feature-complete-commitment masquerading as spike. Defer D to Phase E if E licenses. |
| "Why not A? Cheapest, most reversible — canonical spike." | **Honest hedge: this is the load-bearing judgment call.** A is canonical-spike-shape but evidence yield doesn't reach substrate-shape questions (gsd-2-discovery, not gsd-2-design). Under "more control + open-source" reframing: A under-uses direct intervention authority. Reading reframing as out-weighing canonical "spike means cheapest" by small margin; if Logan or auditors read reframing differently, axis 1 shifts to A. |
| "Why not F? Highest evidence yield." | F is correct-question-at-wrong-time. If correct shape, correct AFTER Phase D evidence shows decision-trace work needs edit-time triggers — evidence we don't have. Premature F commitment short-circuits discovery loop. |
| "Why not G? Tests substrate engine." | G's question is engine-fit-for-reconstruction-shaped-work — Phase E or later. Phase D's framing per §7.3.a is "decision-trace skill/workflow on skill subsystem"; G is mostly orthogonal. |
| "Working-branch R2 may drift toward commitment." | Real risk. Step 2 absorbs with explicit branch-lifetime budget (M1) + abort criteria. Spike-program METHODOLOGY supports bounded scope + abort triggers. |
| "M2's primitive sampling may have missed an in-tree `deliberate` analog." | M2 §3.B explicitly enumerated gsd-2 internal skills; no `deliberate`. Closest analog is `forensics` (failure-side reconstruction, auto-mode-failure-scope). E's gap-mapping vs forensics is explicit at STEP1-design-space.md §3.E. Phase D entry audit catches sample-coverage gaps. |

### §3.B Challenges to axis 2 ((i) parallel R4 = Shape A)

| Challenge | Defense |
|---|---|
| "Why not (ii)? Cheaper than running A in parallel." | (ii) makes P5 do double duty — once as drift-finding (its actual finding) and once as design-input. Category mistake. Keep P5 as standing constraint. |
| "Why not (iii)? Phase E can dispatch its own R4." | Defers contrast question without evidence basis. Phase E stability test reads Phase D evidence; if Phase D has only R2 evidence, the cross-R-strategy stability claim is unfounded. |

### §3.C Challenges to axis 3 ((a) Step 1 gap-mapping)

| Challenge | Defense |
|---|---|
| "M2-primitive-sampling-bounded means Step 1 gap-mapping is incomplete." | Acknowledged at STEP1-design-space.md §4.5 #6. Phase D entry audit catches; Step 3 deepens. Standard bounded-evidence design-framing pattern. |
| "Pure deferral to Step 3 would be cleaner." | Loses Step 1 organizing logic. Candidates aren't comparable at design-space layer if gap-mapping is absent. Step 1 surfacing-shape requires bounded gap-mapping per candidate. |

### §3.D Challenges to axis 4 (F + G out-of-scope)

| Challenge | Defense |
|---|---|
| "F is exactly the doctrine-load-point pattern RELATIONSHIP-TO-PARENT.md substrate-evidence channel surfaces." | True. But Phase D is a spike. If F is correct shape, correct AFTER Phase D evidence shows decision-trace work needs edit-time triggers. Honest hedge: if Logan reads Phase D as core-shape-test rather than skill-test, F-override is defensible — but that's a substantively different Phase D. |
| "G tests substrate engines; substrate-shape evidence." | True but narrow. Deterministic engine for reconstruction-shaped work is a specific question; Phase D's framing is broader (decision-trace skill/workflow on skill subsystem per §7.3.a). |

## §4. Sensitivity map — how dispositions would change under different factors

| If this factor shifts… | …primary candidate likely shifts to… | Reasoning |
|---|---|---|
| Reversibility outweighs control-and-access | **A** (R4 user-side); D+E defer to Phase E | Canonical "spike means cheapest" reading; defensible; under-uses access |
| P5 had returned severe drift (not moderate) | **Different first-target entirely** — fix emission surface first | P5 sub-option (i) re-scope trigger would have fired |
| M2 had found a gsd-2-internal `deliberate` skill | **D** or **E-as-router-over-deliberate** | Existing-primitive overlap shifts gap-mapping fundamentally |
| Anchor shifts from A+F-primary to B-primary (small-team) | **D** or **D+E** | Multi-user concerns weight schema-versioning argument higher |
| Logan re-opens §7.3.b R3 (contribution-culture probe) | **E + R5-conditional-upstream-PR within Phase D scope** | Significantly increases evidence yield; PR-step becomes Phase-D-internal |
| Logan disposes "Phase D is core-shape-test, not skill-test" | **F** (hooks) | Substantively different Phase D; reversibility envelope expands; abort criteria become primary discipline |
| Logan disposes "spike-sizing envelope can expand" | **D+E composition** | Removes cost ceiling that defers D; maximum substrate-shape coverage |
| Audit catches "more control + open-source" reading as over-shifting weight | Re-disposition to **A** | The reframing-as-organizing-logic risk per STEP1-design-space.md §4.5 #4 fires |

## §5. Audit-priority risks Claude is acknowledging in this disposition

1. **The "more control + open-source" reframing is doing load-bearing work in axis 1 reasoning.** If auditors read it as over-shifting weight (reversibility argues louder), E-primary shifts to A-primary. STEP1-design-space.md §4.5 #4 surfaces this exact risk.

2. **E-vs-D weighing may under-weight schema-versioning evidence yield.** D's substrate-shape coverage is broader. The "Stack D foreclosed pattern applies recursively" argument is a real principle but applying it at Phase D scoping is itself Claude-imported reading; defensible counter exists.

3. **(i) parallel R4 comparator picks A-as-comparator.** If Phase E reads "cleanly-paired contrast didn't actually surface useful divergence," (ii) or (iii) would have been better. Bounded judgment.

4. **F + G out-of-scope confirmations are reversibility-grounded.** If Phase E evidence supports F or G being needed, F/G's exclusion at Phase D will look wrong in retrospect. Reversibility-bounded judgment; defensible but not certain.

5. **D5a recursion at this disposition turn itself.** Disposition is co-produced — Claude's reasoning + Logan's accept-as-stated under shared in-session-collaboration framing. Phase D entry audit per plan §2.4 row D paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load) is the structural correction. Step 5 reads §7.10 + STEP1-design-space.md + this disposition + Step 3 mini-spec together.

6. **/effort max → /effort xhigh sequence is part of the auditable trail.** Claude's surfacing was performed at maximum reasoning effort; Logan's accept-as-stated was given at xhigh after surfacing. The accept happened under conditions where Logan had access to Claude's full reasoning surface; it was not a rubber-stamp under bounded reasoning. Auditor reads this as evidence-of-deliberate-acceptance, not evidence-of-cleared-quality (Logan's accept does not substitute for Phase D entry audit).

## §6. Cross-references

### Step 1 design-space framing artifact (under disposition)

- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md` — full 5-candidate surfacing; §6 disposition options table; this artifact records accept-as-stated.

### Step 0 outputs (load-bearing for Step 1 + this disposition)

- `.planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md` — P5 probe; sub-option (ii) caveat as standing constraint.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md` — gsd-2-internal primitive inventory; H3 finding.

### Standing context

- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.10.4 work-flow + §7.10.5 executor checklist.
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` §1 (test-case-vs-substrate; H5 anchor).
- `.planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/DISPOSITION.md` §8 (Phase D entry pre-mini-spec amendment).

### Trajectory plan governance

- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §1.4 Phase D goal + §2.4 row D audit shape (paired same-vendor + cross-vendor xhigh) + §0.5 disciplines + §0.7 hybrid autonomy.

### Logan-correction reference

- 2026-04-30 /effort max turn: gsdr (our fork of v1 gsd; lives on Claude Code) ≠ gsd-2 (standalone open-source runtime; direct intervention authority). gsdr-side shapes (B, C from initial proposal) dropped per substrate clarification. The "more control + open-source" reframing is the load-bearing organizing logic in axis 1 reasoning.

### Logan-disposition turn

- 2026-04-30 /effort xhigh turn: accept-as-stated of Claude's recommended primary + comparator + gap-mapping discipline + OOS confirmations across all four §6 axes. Logan-prompt verbatim: *"accept as stated, try to leave an auditable trail of this reasoning as usual"*.

### What Phase D entry audit (Step 5) reads

Per plan §2.4 row D paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load):

- INCUBATION-CHECKPOINT.md §7.10 (negative-space survey)
- STEP1-design-space.md (5-candidate surfacing)
- This disposition artifact (Logan-disposed dispositions + Claude reasoning + sensitivity map + acknowledged audit-priority risks)
- Step 2 outputs (practical decisions; not yet drafted)
- Step 3 mini-spec (not yet drafted)

The audit reads them together as one corpus — the structural correction for §7.10 D5a inheritance + Step 1 design-framing quality + this disposition's co-production risk + Step 3 mini-spec evidence-load calibration.

---

*Disposition record authored by Claude (Opus 4.7, /effort xhigh) 2026-04-30 immediately following Logan's accept-as-stated at /effort xhigh of Claude's recommendations surfaced at /effort max. The /effort max → /effort xhigh sequence preserves the reasoning surface that grounded the accept; both turns are part of the auditable trail. Subject to same fallibility caveat as STEP1-design-space.md, INCUBATION-CHECKPOINT.md §7.10, and DECISION-SPACE.md §0. Phase D entry audit per plan §2.4 row D is the structural correction for the co-production risk.*
