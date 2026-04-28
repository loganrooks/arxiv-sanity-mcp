---
type: session-handoff
date: 2026-04-28
status: post-W1-parallel-dispatch + framing-widening artifact landed; W2 audits + tier-comparison agent pending
predecessor: .planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md
purpose: |
  Hand off the 2026-04-27 → 2026-04-28 session arc to fresh sessions.
  The arc covered: orchestration package authoring + cross-vendor audit
  + revisions + focused re-audit (2026-04-27); W1 slice 1 pilot dispatch
  + side-investigation (capabilities probe + W2 dive) (2026-04-27);
  framing-widening artifact authoring + slice prompt revisions
  (2026-04-28); W1 slices 2-5 parallel dispatch + outputs landed
  (2026-04-28); tier-comparison agent dispatched async (2026-04-28).

  W2 audits per audit-spec.md are pending and are the fresh session's
  primary work. The tier-comparison agent at .planning/deliberations/
  2026-04-28-tier-comparison-preliminary.md is in flight when this
  handoff is written — fresh session should check for landing.

  This handoff is written for fresh sessions to execute cold. Predecessor
  context restoration is helpful but not strictly required.
onboarding_read_order: |
  Read in this order if starting fresh:
  1. CLAUDE.md (project root) — auto-loaded; establishes project identity.
  2. AGENTS.md — agent behavior rules + project-specific anti-patterns.
  3. This handoff — full state of play and next-stage execution sequence.
  4. .planning/deliberations/2026-04-28-framing-widening.md — Part I + II;
     load-bearing for what "uplift" + "long-horizon" mean now (widened
     from DECISION-SPACE.md §1.8 + §3.6); deferred items log §9.
  5. .planning/gsd-2-uplift/INITIATIVE.md — initiative-staging artifact;
     goal as articulated; open framing questions (now widened).
  6. .planning/gsd-2-uplift/DECISION-SPACE.md — load-bearing decision
     reference; B1-B6 in §1.11-§1.16. Read alongside the framing-
     widening which widens but does not supersede.
  7. .planning/gsd-2-uplift/orchestration/OVERVIEW.md — wave structure +
     §4 pilot-gate criteria + §11 dispositions log + §7 pivot procedure.
  8. .planning/gsd-2-uplift/orchestration/audit-spec.md — W2 audit
     template; copy/substitute for each slice audit dispatch.
  9. .planning/gsd-2-uplift/orchestration/synthesis-spec.md — W3
     synthesis spec (after audits land); inputs include framing-widening
     artifact per recent revision.
  10. .planning/gsd-2-uplift/exploration/ — all W1 evidence:
      - 01-mental-model-output.md (slice 1 pilot, codex GPT-5.5 high).
      - 02-architecture-output.md (slice 2, codex GPT-5.5 high).
      - 03-workflow-surface-output.md (slice 3, with multi-engine subsidiary).
      - 04-artifact-lifecycle-output.md (slice 4, with extension-mechanism subsidiary).
      - 05-release-cadence-output.md (slice 5, shallow-clone preflight worked).
      - capabilities-production-fit-findings.md (W1 capabilities probe at medium).
      - w2-markdown-phase-engine-findings.md (W2 dive at medium).
  11. .planning/gsd-2-uplift/orchestration/cross-vendor-audit.md +
      cross-vendor-reaudit.md — orchestration-package audit history.
  12. .planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md
      §B — methodological observations B.1-B.5 (B.5 added 2026-04-27;
      this session adds a B.6 sub-pattern noted in §6 below).
  13. .planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md
      — predecessor; context for the genesis arc that produced
      DECISION-SPACE.md + INITIATIVE.md.

  Optional (selectively when relevant):
  - .planning/STATE.md — project state.
  - .planning/LONG-ARC.md — anti-patterns.
  - .planning/spikes/METHODOLOGY.md — M1 paired-review at line 112;
    forbidden-reading extension at line 117.
  - .planning/audits/2026-04-27-stage-1-artifacts-audit-report.md —
    Stage 1 audit findings (already integrated; reference only).
agents_running: |
  Tier-comparison preliminary agent dispatched 2026-04-28 (Opus,
  general-purpose, async). Output expected at .planning/deliberations/
  2026-04-28-tier-comparison-preliminary.md (~150-200 lines). Status
  when this handoff was written: running. Fresh session should check
  for landing before W2 audit dispatch — the comparison may inform
  whether audits dispatch at xhigh (current spec) vs high (cost-saving
  if tier-comparison validates).
---

# Handoff — Post-W1 parallel dispatch + framing widening

This document is the durable record of the 2026-04-27 → 2026-04-28 session arc that began post-Stage-1 of the uplift initiative genesis and extended through orchestration package authoring, W1 dispatch (pilot + parallel + side-investigation), framing widening, and slice prompt revisions. It captures: (a) what landed; (b) what's pending; (c) the trajectory ahead; (d) lessons learned worth carrying forward; (e) what NOT to do; (f) cross-references.

If reading cold, follow the onboarding read-order in the frontmatter. Sections build on each other.

## 1. Where we are right now

**Date:** 2026-04-28 (session began 2026-04-27; handoff written 2026-04-28 after W1 slice outputs landed and tier-comparison agent dispatched).

**Branch:** `spike/001-volume-filtering` (substantial commits ahead of origin; not pushed).

**Active work:** gsd-2 uplift initiative — first-wave exploration W1 complete (slices 1-5 outputs landed). W2 audits per audit-spec.md are the primary pending work. Framing-widening artifact establishes a new operating frame (R1-R5 design space; six-context long-horizon plurality; plural significations of "uplift") that synthesis at W3 will integrate.

**Recent commits (2026-04-27 → 2026-04-28; chronological):**

Pre-handoff session arc landed:
- `52ee43c` — `docs(gsd-2-uplift): add cross-vendor pre-pilot audit of orchestration package`
- `6d1063b` — `docs(gsd-2-uplift): apply within-artifact revisions per cross-vendor audit + record preflight-failure as §B.5`
- `3681ada` — `docs(gsd-2-uplift): focused cross-vendor re-audit + addendum fixes; package clean to proceed to pilot`
- `e9d99dd` — `docs(gsd-2-uplift): W1 slice 1 pilot output + side-investigation evidence (capabilities probe + W2 dive)`
- `e34730a` — `docs(deliberations): record 2026-04-28 framing-widening + roadmap-derivation artifact`
- `26cae76` — `docs(gsd-2-uplift): apply slice prompt revisions + synthesis input update + STATE.md per framing-widening Part II §6`
- `d191095` — `docs(gsd-2-uplift): W1 slices 2-5 outputs (parallel cross-vendor dispatch at GPT-5.5 high)`

**Pending:**
- **W2 audits per audit-spec.md.** Slice 4 audit is mandatory (R2 viability load-bearing per `audit-spec.md:9`). Slices 2 and 5 audits warranted by load-bearing claims (vendoring + clean-seam ADR; release/workflow interleaving). Slice 3 audit borderline (corroborates W2 dive — possible skip). Working recommendation when this handoff was written: dispatch slices 2, 4, 5 audits in parallel via `adversarial-auditor-xhigh` subagent type; skip slice 3.
- **Tier-comparison agent landing.** Dispatched 2026-04-28; check `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` for landing. Once landed, may inform W2 audit tier (current spec audit-spec.md is xhigh; tier-comparison might justify high if cost-savings warranted).
- **W3 synthesis after audits.** Per synthesis-spec.md. Inputs now include framing-widening artifact (per recent revision to synthesis-spec.md `:36-50`).
- **Incubation checkpoint** per DECISION-SPACE §2.3 after W3.

## 2. The session's three arcs

This session arc covered three intertwined arcs. Understanding each is necessary to avoid mis-reading what landed.

### 2.1 Orchestration package + cross-vendor audit + revision arc (2026-04-27)

The orchestration package was authored 2026-04-27 (post-Stage-1). The session then:

1. Dispatched a cross-vendor (codex GPT-5.5 xhigh) audit of the orchestration package per Logan's escalation of the `OVERVIEW.md §2.5` recommended same-vendor pre-pilot audit. **Logan's call extended the spec from same-vendor to cross-vendor.** First audit verdict: **material → revise package then proceed.**

2. Logan flagged a **preflight failure**: gsd-2 was not cloned at `~/workspace/projects/gsd-2-explore/` per `OVERVIEW.md §2.1` setup commands when the audit dispatched. Recorded as methodological observation §B.5 in `2026-04-27-dispatch-readiness-deliberation.md` — sub-pattern of B.1 (skill-heuristic shallow-match): **strong-trigger (Logan said "do audit") bypassed precondition-check**.

3. Within-artifact revisions applied per audit findings (clear-cut findings: 1.1 R2/R1 leak; 2.1 closure-pressure default; 2.3 W2 skip-criteria inverted logic; 5.1 0${SLICE_NUM} bug; 5.2 stale §-references; 5.3 gh fallback; 5.4 shallow-clone preflight; 4.2 slice-4/5 deprecation overlap; 8.2 cancellation artifact). Interpretive findings (1.2 long-horizon vocabulary; 1.3 agential-development category; 1.4 leading questions; 2.2 hold disposition; 2.4 paired-synthesis broadening) also applied with auditor's own §10 caveat noted.

4. Focused cross-vendor re-audit dispatched on revised package + slices 1/4/5 with gsd-2 now present. Verdict: **addendum-needed, then proceed to pilot.** All 15 prior findings resolved (13 fully, 2 partially → 2 new minor findings: §4 "alphabetical" claim mismatch; slice-5 deepening conflicting with read-only target). Both fixed.

Net result: orchestration package clean to proceed at commit `3681ada`.

### 2.2 W1 slice 1 pilot + side-investigation arc (2026-04-27)

W1 slice 1 (mental-model) dispatched cross-vendor codex GPT-5.5 high per `OVERVIEW.md §3.2`. Output landed at `01-mental-model-output.md` (28KB; 162 lines dense). Quality: existence-first Q4 honored verbatim; calibration discipline throughout; all 4 watchlist areas fired (debug high; collaboration medium-high; telemetry medium-high; security medium); README/source divergences flagged concretely (RTK default; reassess-after-slice default).

**Mid-pilot, Logan opened a parallel substantive question** about gsd-2's production-fitness (milestone-vs-release mapping; patch concept; pre-release workflows; CI integration; team-coordination; startup-vs-enterprise leverage). This produced two side-investigations:

1. **Capabilities probe** (codex GPT-5.5 medium, 250K tokens, 46KB) — three-section discipline (§A observation / §B mapping / §C gap-anchored candidates) tightly held. Dispatch at medium per Logan's "use medium" instruction — the cheap-explorer pattern's first test. Discipline held; medium produced strong inventory + cleanly-separated candidate enumeration.

2. **W2 dive on markdown-phase workflow engine** (codex GPT-5.5 medium, 144K tokens, 22.7KB) — focused 7-question dive identifying the **two-engine architecture** (markdown-phase prompt-mediated; yaml-step graph-backed deterministic). Updated §C candidate viability: deterministic execution refuted for markdown-phase (§C.2); structured cross-references refuted (§C.1, §C.6); programmatic cherry-pick refuted (§C.3); RC/staging soak metadata refuted (§C.4).

Logan's wave-structure-on-large-targets framing emerged mid-flight: "we should've done this in waves, where we first do high level exploration identifying exploration targets to go further in depth in a second wave." The capabilities probe + W2 dive functionally enacted this even though dispatched as single-pass; agent's `§D` self-identified depth-targets enabled the W2 dive without Claude having to reconstruct them.

### 2.3 Framing-widening + W1 parallel arc (2026-04-28)

Logan's questions on 2026-04-27 / 2026-04-28 surfaced three narrowings in the existing framing:

- R1/R2/R3 hybrid (DECISION-SPACE §1.8) is too narrow — R4 (orchestrate-without-modifying) and R5 (replacement-informed-by) are real options not in the design space.
- "Long-horizon" (DECISION-SPACE §3.6) is plural — Logan's articulation in INITIATIVE.md `:38-45` references temporal-extent, release-cadence, release-engineering, complexity-scaling, and situation-stability dimensions; treating these as a single axis collapses distinctions Logan was preserving (especially: reactive scaling vs anticipatory scaling, named explicitly 2026-04-28).
- "Uplift" is plural — modify gsd-2 / configure / orchestrate-around / replace-informed-by are different acts with different evidence requirements and resource profiles.

Logan disposed: author the framing-widening artifact (Part I framing + Part II roadmap derivation; ~700 lines) at `.planning/deliberations/2026-04-28-framing-widening.md`. Apply slice 3 + slice 4 prompt revisions per Part II §6.1. Update synthesis-spec.md to add framing-widening artifact to inputs. Update INDEX.md + STATE.md.

W1 slices 2-5 then dispatched in parallel per `OVERVIEW.md §3.3` (cross-vendor codex GPT-5.5 high). All four landed within ~10 min. Quality at proceed-parallel level for all four:

- **Slice 2** (32KB): vendored Pi pattern; ADR-010 clean-seam; two-engine confirmed; RTK divergence (consistent with pilot).
- **Slice 3** (33KB): multi-engine subsidiary worked — explicit "There are multiple workflow engines or dispatch shapes, not one single engine [high]" with `engine-resolver.ts:1-56` citation.
- **Slice 4** (43KB; load-bearing for R2): substantive extension surfaces; core GSD itself implemented as an extension; gh fallback worked (Q5 reported "incomplete (gh probe failed)"); extension-mechanism subsidiary worked.
- **Slice 5** (46KB): shallow-clone preflight worked (2217 commits visible; truncated at shallow boundary; agent correctly didn't run git fetch); v2.x.y stable since v2.36.0; release/workflow tightly interleaved.

## 3. The framing-widening artifact (load-bearing for synthesis)

This is the most important artifact this session arc produced. **Read it carefully before W3 synthesis or any second-wave-scoping.**

`.planning/deliberations/2026-04-28-framing-widening.md` widens but does not supersede DECISION-SPACE.md.

### What it preserves (no change)
- §1.7 metaquestion ("is uplift-of-gsd-2 the right shape?") — preserved as meaningful question, with answer space widened.
- §1.11 first-wave aim ("characterize gsd-2 carefully enough that second-wave can decide whether/what to do") — preserved verbatim.
- §1.12 wave structure D′ — preserved.
- B1-B6 decisions — preserved.

### What it widens
- **§1.8 R1/R2/R3 hybrid → R1-R5 design space.** R4 (orchestrate-without-modifying) and R5 (replacement-informed-by) added explicitly. R2-base persists as working hypothesis within widened space.
- **§3.6 long-horizon-axis question → six-context plurality.** Solo-research-tool-over-years / Small-team-product / Larger-team-enterprise / Platform-team / Transition-as-event (reactive) / Transition-as-stance (anticipatory-scaling).
- **"Uplift" usage → four-act plurality.** Modify gsd-2 / configure / orchestrate-around / replace-informed-by.

### What it adds
- Project-anchoring framework (arxiv-sanity-mcp's context as primarily Solo-research with Context F secondary; flagged that uplift's reusability emphasis means anchoring should be plural across multiple onboarding situations).
- Deferred items log (Part II §9; 17 items across probes / methodology / audits / synthesis-stage / roadmap).

**Synthesis-spec.md was updated to include this artifact in W3 inputs** — see `.planning/gsd-2-uplift/orchestration/synthesis-spec.md:36-50`.

## 4. Next-stage execution sequence (W2 audits)

Fresh session should:

### 4.1 Check tier-comparison agent landing

Before dispatching audits:
- Check `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` for landing.
- If landed: read it. The tier-comparison's preliminary verdict may inform whether W2 audits dispatch at xhigh (current `audit-spec.md` spec) or whether high suffices for cost-savings. Audit-spec.md `:21` currently says "Effort: xhigh." If tier-comparison validates that xhigh is meaningfully stronger than high for synthesis-feeding work, keep xhigh. If tier-comparison shows the gap is smaller than expected, consider high as cost-savings — but **don't bypass the audit-spec discipline of recording the tier choice**; if changed, update audit-spec.md and explain in commit.
- If still running: proceed with audit dispatch at xhigh per current spec; integrate tier-comparison findings post-hoc (the preliminary's revision-trigger explicitly handles this).

### 4.2 Dispatch W2 audits per audit-spec.md

**Mandatory:** slice 4. **Recommended:** slice 2, slice 5. **Borderline (likely skip):** slice 3.

For each audit, instantiate `audit-spec.md` template by substituting `{N}` and `{slice-name}`. Dispatch via `adversarial-auditor-xhigh` subagent type within Claude Code. Pass the instantiated audit prompt as the subagent's prompt parameter.

Example dispatch shape (pseudo-code):
```
Agent({
  subagent_type: "adversarial-auditor-xhigh",
  description: "Audit of slice 4 output",
  prompt: <audit-spec.md template with {N}=4 and {slice-name}=artifact-lifecycle substituted>
})
```

The audit prompts should be substantively self-contained (template handles this). The auditor reads only:
- The slice output being audited.
- The slice prompt (slice spec + preamble.md).
- gsd-2 source.
- Other audit outputs (for cross-audit-pattern recognition; this is allowed per `audit-spec.md:46`).
- This handoff is forbidden reading for the auditor (per audit-spec.md `:37` "INITIATIVE.md, DECISION-SPACE.md, deliberation logs").

Audits can run in parallel (each is its own subagent). Total wall-clock: ~30-60 min per audit at xhigh.

### 4.3 Disposition each audit

Per `audit-spec.md §6`:
- **Clean → proceed.** No material findings; output stands.
- **Minor → addendum.** Flag in OVERVIEW.md §11.4; synthesis proceeds with addendum noted.
- **Material → re-dispatch.** Re-dispatch slice with strengthened prompt; integrate audit notes.
- **Critical → pause.** Surface to Logan; re-disposition.

Record disposition in `.planning/gsd-2-uplift/orchestration/OVERVIEW.md §11.4` per slice.

### 4.4 W3 synthesis after audits

After all audits dispose:
- Run W3 synthesis per `synthesis-spec.md`. Inputs include the framing-widening artifact at §5 of the input list.
- Synthesizer is same-vendor Claude Opus xhigh (per B3; `synthesis-spec.md:9-11`).
- Evaluate paired-synthesis escalation criterion at `synthesis-spec.md:165-182` (broadened to 4 triggers per cross-vendor audit revision).
- If escalation: dispatch cross-vendor codex synthesizer; produce `SYNTHESIS-COMPARISON.md`.

### 4.5 Incubation checkpoint

After synthesis: incubation checkpoint per `DECISION-SPACE §2.3`. Out of scope for this orchestration; Logan-disposed.

## 5. Direction-shifting evidence accumulated through W1 + side-investigation

Synthesis will integrate; flagging here for fresh-session orientation:

- **gsd-2's identity is "vendored-modified-Pi-fork + GSD app layer"**, not "GSD on top of Pi SDK as clean library." Per slice 2 Finding 2.5/2.6 + `docs/dev/ADR-010-pi-clean-seam-architecture.md`. Bears on R1 vs R2 viability: extension-against-vendored-Pi is fragile; ADR-010 proposes (but hasn't implemented) a clean-seam refactor.
- **gsd-2 has TWO workflow engines** (markdown-phase prompt-mediated; yaml-step graph-backed deterministic). Per slice 3 + W2 dive. Bears on §C candidate viability: deterministic intervention work needs yaml-step or core-additions, not markdown-phase.
- **Core GSD itself is implemented as an extension.** Per slice 4 Finding 2.7. Bears on R2 design: extensions are foundational composition mechanism; extension-system surface is mature.
- **Release mechanics + product workflow tightly interleaved.** Per slice 5 §iv. Bears on R2 design: release-touching extensions need to compose with milestone/slice/task state.
- **gsd-2 is in major-version-stability mode.** v2.36.0 → v2.78.1 all v2.x.y. Per slice 5. Bears on R2 timeline: v2 is reasonable build target; v3 break unlikely in our planning horizon.
- **gsd-2's docs sometimes overstate behavior relative to source defaults.** Multiple instances: RTK default; reassess-after-slice default; team git.isolation default; verification scope. Pattern across slices 1, 2, 3, 5. Bears on production-deployment of gsd-2: anyone using gsd-2 should verify effective preferences, not rely solely on README.

## 6. Lessons learned worth carrying forward

### 6.1 Methodological observation B.6 — defaulted-spec-following when evidence has shifted

**The pattern:** when a prior spec has been written and is "in front of" Claude, defaults are followed without re-evaluation even if the evidence base has shifted since the spec was written.

**Concrete instance this session:** Logan questioned model-tier choice on 2026-04-27 ("we can use GPT 5.5 medium for this") with the explicit deferral "I don't want to decide on the later [slices 2-5 tier] until we see what kind of work GPT 5.5 medium can do." Medium then exceeded expectations on capabilities probe + W2 dive. When dispatching slices 2-5 on 2026-04-28, Claude followed `OVERVIEW.md §3.1/§3.3` spec at high without re-raising the model-tier question. Logan's explicit calibration check ("when did you pick high instead of medium?") caught the defaulted decision.

**Sub-pattern of B.1/B.5:** B.1 is shallow-skill-trigger; B.5 is dispatching-before-precondition-check; B.6 is following-spec-without-re-evaluation-when-evidence-shifts. All share the structure: strong trigger (skill match / dispatch instruction / written spec) bypasses calibrated re-evaluation.

**Mitigation:** when a prior spec is followed, briefly note "spec says X; evidence since spec was written includes Y; I'm proceeding with X because [reason] / I'm proposing departure to Z because [reason]." This is a minor verbal discipline; the behavior change is to make the spec-follow choice explicit rather than defaulted.

**Recording venue:** when this handoff is committed, the framing-widening §9 deferred items (specifically items 7-8 methodology codification at threshold) gain a B.6 entry to consider for codification.

### 6.2 The cheap-explorer pattern is empirically validated for exploration-shape work

The capabilities probe + W2 dive at GPT-5.5 medium maintained calibration discipline + structured-section discipline on substantial material (250K + 144K tokens; 46KB + 22.7KB output). Three-section §A/§B/§C separation held. Citations grounded. The fear that medium would lose discipline didn't materialize.

**Where this confirms intuition:** for pure-exploration probes (find-things-and-cite-them; produce-structured-inventory), medium suffices.

**Where this is calibrated:** the W1 slices at high produced sharper architectural-relationship work than medium would have. Slice 2's vendoring + clean-seam findings; slice 3's engine-resolver dispatch detection; slice 4's extension-mechanism distinction. Medium would have caught these at inventory level; high caught them as relationships.

**Pending tier-comparison preliminary note** at `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` records this with audit revision-trigger.

### 6.3 The wave-structure-on-large-targets discipline

Logan's mid-flight observation: "the codebase was pretty large, maybe we should've done this in waves." The capabilities probe at single-pass medium effort functionally enacted W1 (survey identifying depth-targets in §D); the W2 dive on markdown-phase engine then explored those targets. The wave structure emerged after the fact rather than by design but worked.

**For future similar work:** when target is large enough that single-pass would go shallow uniformly, default to wave-structured: W1 high-level survey identifying depth-targets; W2 focused deep-dives at higher tier per-target if their work warrants; W3 synthesis. Total cost is often *lower* than single-pass-at-high because each wave's context is bounded.

**Codification deferred** per framing-widening §9 item 7 (methodology codification at threshold of ~3 samples).

### 6.4 The widening-when-pressed discipline

When Logan pressed on framing ("how are we understanding what it means to uplift?"), the right response was to widen explicitly via deliberation artifact rather than to fold the widening into slice prompt revisions or trust synthesis to do framing-application post-hoc. The framing-widening artifact at `.planning/deliberations/2026-04-28-framing-widening.md` carries the inferential chain that synthesis will read.

**Why this matters:** synthesis was supposed to evaluate the §1.7 metaquestion + §3.4 long-horizon-axis question (per `synthesis-spec.md §2.3 + §2.4`). If our framing was wrong-shaped, synthesis would have to fight against W1 evidence collected under the narrower framing. The framing-widening artifact aligns the framing with the evidence-base before synthesis runs.

**Counter-discipline:** widening-when-pressed must not become opening-pressure (always finding more to deliberate). The honest test: did the widening produce different downstream work? Yes — slice 3 + slice 4 prompt revisions; synthesis input list update; deferred items log structure. Operational consequences make the widening non-decorative.

### 6.5 The cross-vendor-audit pattern

Cross-vendor audit on the orchestration package (codex GPT-5.5 xhigh) caught real issues a same-vendor audit would have rationalized: explicit R2/R1 leak in slice-4 prompt; closure-pressure-by-default-tag in §4.1; inverted W2 skip-criteria logic; operational typos. The auditor's own §10 caveat ("may have read framing-leak aggressively") was honest calibration, not retraction.

**For future similar work:** cross-vendor audit on artifact production (prompts, deliberation notes, decision records) catches what same-vendor authors don't see. Same-vendor on cross-vendor outputs (W2 audits) catches register-issues + framing-leakage the cross-vendor reader couldn't catch (because the leaks were in the prompt). The pairing matters.

## 7. What NOT to do

### 7.1 Do NOT skip the gsd-2 setup preflight before dispatching audits

Per B.5 / B.6 pattern. The gsd-2 clone at `~/workspace/projects/gsd-2-explore/` is required for slice agents and auditors. Verify before dispatching:
```
ls -la ~/workspace/projects/gsd-2-explore/.git
gh repo view gsd-build/gsd-2 --json description
```

### 7.2 Do NOT auto-execute incubation-checkpoint or second-wave-scoping decisions

Logan disposes. Per harvest §10.1 assumption #1 + DECISION-SPACE §0. The synthesis output flows to incubation-checkpoint deliberation; that deliberation is Logan-led, not Claude-auto.

### 7.3 Do NOT collapse R1-R5 back to R1/R2/R3 in synthesis or downstream

The framing-widening explicitly preserves R4/R5 as named options. Synthesis should evaluate evidence against all five. If synthesis lands on R1+R2+R3 mix anyway, that's fine — but it should be by evidence-driven evaluation across R1-R5, not by implicit narrowing back to the older space.

### 7.4 Do NOT treat the framing-widening artifact as superseding DECISION-SPACE.md

It widens. B1-B6 decisions persist; R2-base persists as working hypothesis. The widening is "what's possible" not "what's decided." Synthesis can recommend a different working hypothesis; that's a synthesis-stage proposal subject to incubation-checkpoint disposition, not auto-adopted.

### 7.5 Do NOT bypass audit-spec.md discipline for slice 4

Slice 4 audit is mandatory per `audit-spec.md:9`. R2 viability is load-bearing per `DECISION-SPACE.md §1.8`. This is not a discretionary audit; cannot be skipped.

### 7.6 Do NOT modify gsd-2 source

`~/workspace/projects/gsd-2-explore/` is a read-only target throughout this initiative. The `OVERVIEW.md §2.1` setup discipline reserves `git fetch` operations to the dispatcher (Logan + this session); slice agents and auditors do not modify gsd-2.

### 7.7 Do NOT bypass disposition-discipline

Logan disposes substantive choices. Claude proposes options + recommendations; Logan picks. If a disposition feels obvious to Claude, surface as recommendation, not action. Recurring failure mode: closure-pressure (rushing to dispatch); also opening-pressure (always finding more to deliberate). Both are dispositions Logan owns.

## 8. Open questions / pending dispositions

### 8.1 Audit set: 4 slices, 3 slices, or 1 slice?

Working recommendation when this handoff was written: dispatch slices 2, 4, 5 audits; skip slice 3. Reasoning: slice 4 mandatory per spec; slice 2's vendoring + clean-seam findings load-bearing; slice 5's release/workflow interleaving load-bearing; slice 3's multi-engine finding corroborates W2 dive (already verified at re-audit time).

**Alternative dispositions:**
- Audit all 4 (most conservative; ~+30-60 min cost).
- Audit only slice 4 (cheapest; risks missing audit signal on novel claims in slices 2/5).
- Logan's call.

### 8.2 W2 audit tier (xhigh vs high)?

Current `audit-spec.md:21` spec: xhigh. Tier-comparison preliminary may inform whether high suffices. Don't change without explicit revision to audit-spec.md.

### 8.3 Whether to wait for tier-comparison agent before dispatching audits

Asynchronous; not blocking. Fresh session can check landing and dispatch in parallel. If tier-comparison verdict shifts audit-spec.md tier, re-dispatch with new tier.

### 8.4 Stage 1 audit deferred quality findings

Still pending per framing-widening §9 item 10 + STATE.md pending-todos. Address opportunistically; not blocking.

## 9. Cross-references

**Decision and operating-frame inputs.**
- `.planning/gsd-2-uplift/INITIATIVE.md` — initiative-staging.
- `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.11-§1.16 (B1-B6); §1.7 metaquestion; §1.8 R1/R2/R3 hybrid.
- `.planning/deliberations/2026-04-28-framing-widening.md` — Part I + Part II + §9 deferred items log.

**Orchestration package.**
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` — wave structure + §4 pilot-gate + §11 dispositions log + §7 pivot procedure.
- `.planning/gsd-2-uplift/orchestration/preamble.md` — common preamble; cross-slice watchlist.
- `.planning/gsd-2-uplift/orchestration/slice-01-mental-model.md` through `slice-05-release-cadence.md`.
- `.planning/gsd-2-uplift/orchestration/audit-spec.md` — W2 audit template.
- `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` — W3 synthesis spec.
- `.planning/gsd-2-uplift/orchestration/cross-vendor-audit.md` + `cross-vendor-reaudit.md` — orchestration audit history.

**W1 evidence.**
- `.planning/gsd-2-uplift/exploration/01-mental-model-output.md` (slice 1; high).
- `.planning/gsd-2-uplift/exploration/02-architecture-output.md` (slice 2; high).
- `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md` (slice 3; high).
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md` (slice 4; high).
- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md` (slice 5; high).
- `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md` (capabilities probe; medium).
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md` (W2 dive; medium).

**Deliberation logs.**
- `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` — genesis-arc.
- `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md` — orchestration package + B1-B6 + §B.1-§B.5 methodological observations.
- `.planning/deliberations/2026-04-28-framing-widening.md` — current operating frame.
- `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` — agent-authored async; check for landing.
- `.planning/deliberations/INDEX.md` — index for all dated deliberations.

**Predecessor handoffs.**
- `.planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md` — predecessor; Stage 1 → Stage 2.
- `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md` — further-predecessor; Wave 5 disposition + dispatch sequencing.
- `.planning/handoffs/2026-04-26-post-wave-4-handoff.md` — codex-CLI pitfall reminders (§9 of that handoff).

**Project doctrine referenced.**
- `CLAUDE.md` — project identity + accepted ADRs + doctrine load-points.
- `AGENTS.md` — project-specific anti-patterns to detect.
- `LONG-ARC.md` — anti-patterns at lines 42-54.
- `.planning/spikes/METHODOLOGY.md` — M1 paired-review at line 112; forbidden-reading extension at line 117.
- `.planning/foundation-audit/METHODOLOGY.md` — epistemic discipline.

**Source citations (selective; full per-finding citations in slice + probe outputs).**
- gsd-2 source at `~/workspace/projects/gsd-2-explore/`.
- Pi-vendored packages at `~/workspace/projects/gsd-2-explore/packages/`.
- Workflow engines at `src/resources/extensions/gsd/{workflow-engine,engine-resolver,dev-workflow-engine,custom-workflow-engine,commands-workflow-templates}.ts`.
- Extension surfaces at `src/{extension-registry,extension-discovery,extension-validator}.ts` + `packages/pi-coding-agent/src/core/extensions/`.
- Release tooling at `scripts/{generate-changelog,bump-version,version-stamp,update-changelog}.mjs` + `.github/workflows/{prod-release,dev-publish,next-publish,ci}.yml`.

---

*Single-author session handoff written 2026-04-28 by Claude (Opus 4.7, xhigh effort) at Logan's direction post-W1-parallel-dispatch + framing-widening. Subject to the same fallibility caveat as DECISION-SPACE.md §0 and predecessor handoffs. Stress-testing happens when fresh session reads + executes; if any direction reads mis-recorded, re-deliberation supersedes. The fresh session's primary work is W2 audits per §4.2 above.*
