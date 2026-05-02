# Plan: Trajectory from Audit-Arc-Complete to gsd-2-Uplift Extraction

**Plan author:** Claude (Opus 4.7), 2026-04-29, in-session-collaboration with Logan
**Plan status:** REVISED 2026-05-01 ((V′.a) Step 2 — methodology-fit response: spike-shape Phase D replaced with mapping-shape Phase D per 2026-04-30 §2.6 disposition; Phase E reshaped to test mapping-coherence; Phase F gate adjusted to mapping-coherence + intent-intervention-feasibility; §0.8 acknowledges methodology-fit response; §0.4 expanded with new standing-context references). Phases A, B, C complete; Phase D under (V′.a) replan with current evidence corpus marked interim per 2026-04-30 §2.8 + commit `43e652b`.
**Plan-self-audit status:** Phase A complete — `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md` (cross-vendor codex GPT-5.5 xhigh; 9 findings; 1A/6B/2C; revise-before-execute disposition). (V′.a) Step 3 plan-self-audit pending (scoped to question-shape-fit per 2026-04-30 §4 step 3; this revision is the artifact under audit). **Step 3 audit-spec drafting form: cross-vendor codex independent draft recommended** (per Step 2 self-review concern surfaced 2026-05-01 — audit-spec-itself-at-framing-inheritance-risk per 2026-04-30 §5.3 finding requires independence at scope-level, not just at execution-level; Claude-drafted-audit-spec-after-Logan-disposed-checks would re-import the failure-mode-signature). Logan disposes spec-drafting form before audit dispatch.
**Authoritative location:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (in-repo, version-controlled — the canonical execution authority and audit provenance). The `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` runtime copy is a working-draft mirror only; for any fresh-session execution, treat the in-repo copy as authority.

---

## Context (why this plan exists)

We just completed the v1-GSD premise-bleed audit-arc on SYNTHESIS-COMPARISON.md (cross-vendor codex Step-1 + same-vendor Claude xhigh independent Step-2 + main-thread DIFFERENTIAL.md + commit-with-addendum disposition + §7 addendum landed; commits b8db2a0 + fae9650 + a79e761). The comparison is now ready for §2.1 + §5 incubation adjudication.

Logan asked for an orchestrated trajectory from this point to the extraction of the gsd-2-uplift initiative into its own dedicated repo, with: quality gating, checkpoints, audit/review/verification at load-bearing junctures, framing-issue prevention, error-prevention (multiple kinds of erring), clear orchestration plan, clear artifact plan, clear commits (so backward-traceability of responsibility is preserved), and self-checkpoints via cross-vendor xhigh audits (or high where appropriate; leaning xhigh for big-picture / load-bearing decisions because *framing is itself a heavy load-bearing decision* — every frame excludes much from consideration, never neutrally, and a slightly mis-adjusted frame has tremendous downstream consequences).

The plan also needs to be **self-contained for context-clearing** — Logan plans to clear context before execution, so the plan must include onboarding for a fresh-context Claude.

The intended outcome: a trajectory that lands the gsd-2-uplift initiative in its own dedicated repo with full deliberation/audit/decision trail preserved, internal coherence intact, and arxiv-sanity-mcp's planning tree carrying clean trail-of-references back to the diagnostic loop (the spike-program-as-test-case relationship).

---

## §0. Onboarding (mandatory pre-reading + standing context)

**A fresh-context Claude executing this plan MUST read this section in full before doing anything else.** The discipline-set, horizon-stack, and methodological orientation here are load-bearing for every subsequent phase.

### §0.1 What this plan does and does not do

**Does:**
- Orchestrates a phased trajectory from incubation-checkpoint adjudication through extraction.
- Specifies quality gates at load-bearing decision points.
- Maps artifacts (what produces what, where it lands).
- Maps commits (atomic per logical unit, traceable backward).
- Specifies failure-mode handling for multiple kinds of erring.
- Carries onboarding context for fresh-session execution.

**Does not:**
- Pre-decide incubation dispositions (those are Logan-disposed per D5a in-session-collaboration discipline + framing-widening §3.3).
- Pre-decide first-second-wave-target shape (depends on incubation outcome).
- Pre-decide R-mix narrowing direction (depends on incubation + first-target evidence).
- Pre-decide context-anchoring (Logan-disposed per SYNTHESIS-COMPARISON.md §5.3).
- Specify the dedicated-repo's internal structure (forms in extraction phase based on what's being moved + how the disposition shaped the work).

### §0.2 The horizon stack — load-bearing for keeping bigger picture in foreground

**Long-horizon goal:** Long-horizon agential development substrate. Logan + Claude (or successor agents) being able to do deep, multi-month, intellectually-honest work together over years across many projects. gsd-2 is the current candidate substrate; whether and how to uplift it is the medium-horizon question.

**Medium-horizon goal:** Decide whether and how to uplift gsd-2 — a separate project at `~/workspace/projects/gsd-2-explore/` distinct from the current arxiv-sanity-mcp working directory. gsd-2 is a standalone agent application/runtime built around vendored Pi-derived packages with headless/RPC/MCP/state-machinery surfaces (NOT the v1-GSD pattern of workflow-markdown + skills + hooks layered onto a host runtime — that confusion is the source of the premise-bleed audit). Design space: R1-R5 (fork / extension / upstream-PR / orchestrate-without-modifying / replacement-informed-by) × six contexts (A solo-research / B small-team / C enterprise / D platform-team / E transition-as-event / F transition-as-stance) × four-act plurality (modify / configure / orchestrate-around / replace-informed-by).

**Short-horizon work:** Wave structure (D′): W1 cross-vendor codex slice exploration (5 slices) → W2 selective same-vendor audits → W3 paired synthesis (Claude SYNTHESIS.md 609 lines + codex SYNTHESIS-CROSS.md 207 lines) → SYNTHESIS-COMPARISON.md (in-session-collaborative integration) → premise-bleed audit-arc → §7 addendum landed → **incubation-checkpoint adjudication (NEXT)** → first-second-wave-target dispatch → stability test → extraction-readiness gate → extraction.

**Immediate task arc (this plan):** Trajectory from incubation-checkpoint to extraction. Each phase produces evidence about substrate-shape under spike-intensive conditions (per §0.3 below).

### §0.3 Test-case-vs-substrate relationship (the load-bearing clarification)

**arxiv-sanity-mcp is NOT the long-horizon goal.** It's a **spike-intensive test case** for whether the agential-development substrate can handle work where:

1. **Precedent is thin or absent.** No well-documented "right" stack/architecture to copy.
2. **Experimental design itself is load-bearing.** The wrong experiment forecloses optimal design routes; "fast enough" framings, premature comparative claims, and casual A/B reasoning silently destroy the design space.
3. **The work necessarily produces new knowledge.** You can't look up the answer; the answer comes out of the spike program, and the spike program's quality determines whether the answer is trustworthy.

This means **arxiv-sanity-mcp's value to the gsd-2-uplift initiative is diagnostic, not consumptive.** The spike program at `.planning/spikes/`, the foundation-audit, the deliberation discipline, the paired-review M1 property, the framing-widening discipline, the audit-of-audit discipline, the §7 addendum point-of-use foregrounding — these are all instances of *the substrate working under conditions where the substrate is what's being tested*.

**Implication for execution:** When deliberating about substrate-shape (gsd-2-uplift work), do not lose this test-case framing. arxiv-sanity-mcp's spike-program outputs are *evidence about substrate behavior*, not just project-specific decisions. Future sessions that confuse "the project" with "the substrate" lose the diagnostic loop.

### §0.4 Mandatory pre-reading (sequenced)

Read these in order before executing any phase. **Do not skip.** Each carries load-bearing standing context.

1. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/CLAUDE.md`** — project identity + accepted ADRs + architectural constraints + doctrine load-points. (Note: §0.3 above is currently NOT in CLAUDE.md; Phase B of this plan adds a load-point referencing the standing-context artifact.)
2. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/AGENTS.md`** — agent behavior rules + working posture + closure-pressure + comfort-language + performative-vs-operational openness disciplines.
3. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/LONG-ARC.md`** — anti-patterns + protected seams + doctrine-interaction-with-spike-program. (Note: this file lives under `.planning/`, not at repo root; corrected per Phase A audit F3.)
4. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/INITIATIVE.md`** — uplift initiative scoping + §7 migration trigger (load-bearing for Phase G move/stay table; the §7 text "DECISION-SPACE.md and the deliberation log stay in arxiv-sanity-mcp's `.planning/`" is the authoritative custody rule, not optional guidance).
5. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/DECISION-SPACE.md`** — accepted decisions + recommendations + open questions; §1.17 audit methodology; §2.3 incubation checkpoint specifics; §3 open questions deferred.
6. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/2026-04-28-framing-widening.md`** — R1-R5 design space; six-context plurality; four-act plurality; project-anchoring; §3.3 disposition-discipline; §9 deferred items log.
7. **`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md`** — full read of §0 + §2 + §5 + §6 + §7. The §7.1 reading-frame is **point-of-use active for §5 axes**.
8. **Audit folder:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/` — AUDIT-SPEC.md + FINDINGS.md + FINDINGS-STEP2.md + DIFFERENTIAL.md + DISPOSITION.md (full audit-arc trail).
9. **This plan's own audit-arc:** `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/` — PLAN-AUDIT.md + DISPOSITION.md (Phase A revise-before-execute applied; the reasoning trail showing why each F1-F9 revision exists in the plan as you read it).
10. **Cross-vendor codebase-understanding-audit's META-SYNTHESIS:** `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md` — primary grounding for "what gsd-2 actually is" (corrected frame vocabulary).
11. **`.planning/spikes/METHODOLOGY.md`** — six interpretive lenses + paired-review practice disciplines (A-F) + model-verification disciplines.
12. **`.planning/foundation-audit/METHODOLOGY.md`** — decision-review epistemic discipline; evidence tracing; alternative evaluation; sensitivity analysis; inference-chain integrity.
13. **`.planning/STATE.md`** — current state-of-play (will reflect plan-execution progress as phases complete).
14. **`.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md`** — Phase B output; test-case-vs-substrate framing as standing context (lifted from §0.3 here into a discoverable artifact). Load-bearing for keeping the diagnostic loop in foreground during mapping-shape Phase D.
15. **`.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md`** — substrate-vision standing context (2026-05-01). §1 corrected gsd-2-uplift project-shape (5-property: identity-preserving / pressure-respecting / pushes-limits-in-reasonable-ways / reasonable-objectives-discovered-through-exploration / anchored-against-concrete-test-cases). §2 pressure-not-destination relationship to harness-studio. §3 12 substrate-vision properties (the depth-spectrum mapping-shape Phase D evaluates). §4 scope-discipline (burden-of-proof-on-exclusion + four-category C1/C2/C3/C4 model + identity-distortion narrowness). §5 Phase D mapping purpose under this framing. **Load-bearing for mapping-shape Phase D scope-control** — §3 enumerates what gets mapped; §4 governs how candidate interventions get classified; §5 specifies what the mapping output looks like.
16. **`.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md`** — methodology-question-shape-mismatch finding (spike methodology applied to mapping question) + (V′.a) disposition + five frame-revisions trace + Logan-disposition scope clarification (§2.7) + calibration findings (§5: closure-pressure pattern recurrence + audit-discipline limits + Logan's correction about audit-load transfer). **Load-bearing for understanding why mapping-shape Phase D exists.**
17. **`.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md`** (forthcoming per (V′.a) Step 5; reference now so future-Claude executing post-Step-5 reads it) — standalone methodology-mismatch substrate-shape evidence artifact.

After reading: confirm internal model of (a) horizon-stack; (b) test-case-vs-substrate relationship; (c) §7.1 reading-frame; (d) audit-arc trail outcomes; (e) discipline-set per §0.5 below; (f) **mapping-vs-spike methodology distinction per §0.8 + 2026-04-30 deliberation §2.5**; (g) **substrate-vision 12-property set + four-category scope-confidence model per EXTERNAL-VISION-CONTEXT.md §3-§4 — these govern mapping-shape Phase D scope**.

### §0.5 Discipline reminders (load-bearing for execution)

**Note on self-containment (per Phase A audit F6 disposition):** The summaries below are the **execution authority** for these disciplines. Memory-file citations (`feedback_*`, `reference_*`) appear in parentheses as optional provenance pointers only — they are runtime-personalization artifacts that may not be available in a fresh session and are NOT mandatory pre-reading. **Execution does NOT depend on reading memory files.** The discipline content is fully captured in the bullets here. If a memory file is absent or stale, the bullet text governs.

**Framing-as-load-bearing.** Every frame excludes much from consideration, never neutrally. Slightly mis-adjusted frames have tremendous downstream consequences. Treat framing decisions (R-mix, context-anchoring, first-target-shape, axis-question shape) as heavy load-bearing decisions warranting cross-vendor xhigh audit per §2.

**M1 paired-review property.** Cross-vendor catches substance/vocabulary; same-vendor catches register/integration-grammar. Asymmetry is empirically more complex (per SYNTHESIS-COMPARISON.md §4.1). For premise-bleed and framing-leak, both vendor-positions are needed; either alone is structurally incomplete.

**D5a in-session-collaboration caveat.** Anything Claude drafts in the same session as Logan's framing carries inheritance from Logan's framing. Independent third-reader-validation is the structural correction; addendum-foregrounding (per §7.1) is the lighter mitigation; explicit Logan-adjudication is the discipline at load-bearing decisions.

**Disposition-discipline (per framing-widening §3.3).** Synthesis defers to incubation; comparison defers to incubation; audits surface signals + non-binding disposition signals but do not pre-decide; Logan disposes load-bearing decisions.

**Closure-pressure recurrence.** "Resolved enough to commit" framings, "fast enough" framings, "this seems right" framings — all close off the deliberation surface prematurely. Resist. Either actually resolve with evidence or explicitly mark open per `framing-widening §9` deferred-items pattern.

**Epistemic rigor (provenance: `feedback_epistemic_rigor`).** No premature conclusions. Comparative claims need comparative data. No "fast enough" framing. If unsure, name the uncertainty and what would resolve it.

**Traces over erasure (provenance: `feedback_methodology_and_philosophy`).** Preserve deliberation traces; render reasoning transparent; don't compress decisions into summary outcomes; cite verbatim; record dispositions with reasoning.

**Don't-modify-external-without-asking (provenance: `feedback_ask_before_modifying_external`).** `~/.claude/` is runtime; `~/workspace/projects/` is development. The in-repo plan copy at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` is the execution authority; the runtime mirror at `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` exists for `/loop` resume only. No writes outside arxiv-sanity-mcp without explicit Logan authorization (Phase G new-repo creation is the explicit exception, gated by Phase F).

**No-explore-for-audits (provenance: `feedback_no_explore_for_audits`).** Default Explore agent is for code-search, not audit-grade analysis. Use Opus directly or explicit `model: "opus"` override. For audits at scale, use `adversarial-auditor-xhigh` or cross-vendor codex GPT-5.5 xhigh.

**Spike-process discipline (provenance: `feedback_spike_process` + `reference_spike_design`).** For spike-program decisions: separate designer/critic/executor roles; AI-agent evaluation > list-review > metrics; consult `reference_spike_design` checklist when designing experiments.

**Frame-revision-check ((V′.a) Step 4 mechanism, added 2026-04-30).** Each phase has explicit "is the question we're answering still right?" pauses, performed by Claude with surfacing to Logan, BEFORE within-frame elaboration. This is the structural mitigation against the closure-pressure-into-elaboration pattern documented 2026-04-30 §5.1 + recurring 2026-05-01: surface frame-revision question early, before elaborate within-frame work commits. Specific check-points (per §6.1 + §6.2):
- **Phase entry** (after reading inputs; before drafting outputs): "Is the question this phase exists to answer still the right question? Has the question-shape shifted since the prior phase? Is the methodology applied to this phase still right for the question-shape?"
- **Mid-Phase if observations diverge from priors** (or after a within-mapping observation that surfaces accommodation that the original phase scope didn't predict): "Are observations diverging from priors in a way that warrants pause-and-re-frame rather than continued within-frame elaboration?"
- **Phase output draft** (before commit): "Has the artifact drifted from the question-shape it was authored to answer? Have new frame-revision questions surfaced during construction?"

The check fires by Claude → surfaces to Logan if frame-revision is warranted → Logan disposes (continue within-frame / pause for frame-revision / restart phase under revised frame). Per 2026-04-30 §2.7: Logan-disposition here is for capturing user-intent on frame-revision direction, NOT for substrate-design-soundness audit-of-last-resort. Claude must do agent-side reasoning sufficient to commit to "within-frame OK" or "frame-revision needed" before defaulting to Logan.

### §0.6 Failure-mode taxonomy (kinds of erring to check against)

Different kinds of erring need different checks. The plan's quality gates target each. **§5.6 below** maps each row of this taxonomy to the phase(s) where it applies, the concrete check, and the disposition-owner.

| Kind | Description | Check |
|---|---|---|
| **Framing error** | Operating under wrong frame (e.g., v1-GSD bleed; integration-grammar-as-fact; reduced design space) | Cross-vendor xhigh audit at framing decisions; negative-space check (what's excluded?); §7.1 reading-frame application |
| **Premise-bleed** | Inheriting unexamined assumptions from prior framing into new artifacts | Same-vendor xhigh adversarial-auditor; vetted-replacement vocabulary lookup; META-SYNTHESIS prohibited articulations |
| **Closure-pressure** | "Resolved enough" framings that prematurely commit when evidence doesn't yet support commitment | Explicit name-the-uncertainty discipline; `framing-widening §9` deferred-items addition for genuinely open items |
| **Scope creep** | Phase produces work outside its scope; subsequent phases inherit creep | Per-phase scope check before commit; explicit out-of-scope rejection; spawn separate phase for valid-but-out-of-scope items |
| **Comparative-claims-without-comparative-data** | Claims like "X is better than Y" without comparative evidence | Per-claim evidence check; reject claims unsupported by comparative measurement |
| **False-confidence calibration** | Over-stating confidence; "high confidence" on under-evidenced claims | Per-finding confidence calibration check; downgrade where evidence-load doesn't justify |
| **Comfort-language** | Soft framings that obscure load-bearing claims; "we should consider" instead of "this is the disposition" | Active-voice + explicit-disposition discipline at decision artifacts |
| **Performative-vs-operational openness** | Naming options for the appearance of plurality; not actually preserving them as live options | Per-option evidence check; if option is unworkable, mark it; if option is live, keep operationally available |
| **Integration-grammar-as-fact** | Applying corrected framing as if it were observed-fact (the §7.1 residual the audit caught) | §7.1 reading-frame at application points; "inputs not facts" framing at point-of-use |
| **Skill-heuristic shallow-match** | Matching new context to similar-shaped prior context without checking actual fit | Explicit context-comparison check; spell out what's the same and what's different |
| **Strict-M1 undersell at recommendation stage** | Underselling cross-vendor or same-vendor recommendation because of M1 asymmetry-as-claimed; should use M1 asymmetry-as-empirically-more-complex | Recommendation calibration per SYNTHESIS-COMPARISON.md §4.1 |
| **Execution error** | Wrong tool, wrong file, wrong command — pure mechanics failure | Pre-execution verification; post-execution verification |
| **In-session-collaboration risk** | Claude-drafted artifacts carry Logan's framing inheritance | D5a caveat application; cross-vendor independent reads at load-bearing artifacts; ExitPlanMode discipline |
| **Methodology-question-shape mismatch (added 2026-04-30 per (V′.a))** | Methodology applied to a question-shape it doesn't fit (e.g., spike methodology applied to mapping question per 2026-04-30 §2.5 + §3.5) | Frame-revision-check at phase entry / mid-phase / phase output draft per (V′.a) Step 4; audit-spec lens-question "is the methodology still right for the question-shape?"; plan-self-audit at trajectory-plan revisions scoped to question-shape-fit |

### §0.7 Logan-disposed plan parameters (resolved 2026-04-29 items 1-5; item 6 added 2026-04-30 per (V′.a))

1. **Autonomy boundary.** Hybrid: autonomous within phases; pause at phase boundaries. Claude executes within a phase autonomously (drafting artifacts, dispatching audits, applying dispositions on lower-stakes items). Pauses at phase boundaries (between A→B, B→C, etc.) for Logan disposition before next phase begins. Preserves Logan-disposition discipline at load-bearing junctures while enabling within-phase momentum.

2. **Audit cadence.** Per-phase as §2.1 + §2.2 + §2.3 specify (default-fires + conditional-fires for cross-vendor / same-vendor / paired), AND **reasoning-level (xhigh vs high) judged per-audit based on shape/quality/kind** per §2.4 per-audit table. Logan's frame: "be smart and elegant about harnessing reasoning effectively." Some audits warrant xhigh; some are bounded enough that high suffices. §2.4 specifies the per-audit reasoning-level + the *principle* for the discrimination, so future-Claude (and Phase A audit) can pressure-test the assignments.

3. **Standing-context location.** Option (a): create `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (~80-120 lines articulating §0.3 in detail) + CLAUDE.md doctrine load-point referencing it. Auto-loads via CLAUDE.md; full-detail standing artifact for thorough articulation. (Phase B specifies operational shape.)

4. **Plan endpoint.** Phase H complete (extraction + integration verified). Plan stops when both repos are coherent post-extraction, all references work, EXTRACTION-LOG.md complete. Subsequent uplift design + build happens in new repo with its own plan/orchestration.

5. **Failure-mode-checks-per-phase.** Plan-default: checks relevant to that phase's load-bearing-ness (per §5.6 mapping table). Phase A plan-self-audit applies all §0.6 taxonomy checks (it's auditing the plan itself; comprehensive coverage warranted). Other phases apply the subset relevant to their load-bearing dimensions per §5.6. Logan-discretion to override per phase at execution time.

6. **(V′.a) trajectory-replan disposition (resolved 2026-04-30, Logan /effort xhigh).** Spike-shape Phase D was replaced with mapping-shape Phase D after the methodology-question-shape-mismatch finding crystallized (per `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` §2.5-§2.6). Phase E reshapes to test mapping-coherence; Phase F gate adjusts to mapping-coherence + intent-intervention-feasibility. Phase D current evidence corpus (per Phase D entry through 2026-04-30) is preserved as **interim work-product** (per 2026-04-30 §2.8 + commit `43e652b`), feeding into the replanned mapping-shape Phase D — NOT Phase D's final FINDINGS.md output. The plan-self-audit per (V′.a) Step 3 is scoped explicitly to question-shape-fit (mapping vs. spike) rather than the original Phase A audit's general "is this plan well-formed?" lens.

### §0.8 Methodology-fit acknowledgment (mapping-shape vs. spike-shape question)

**Spike methodology fits "does X work?" questions** under conditions where the right experiment isn't pre-known. Spike shape: pick target → experiment → does it work? → revise hypothesis. arxiv-sanity-mcp's spike program at `.planning/spikes/` uses this methodology where it fits.

**Substrate-design-accommodation is a different question-shape — a *mapping* question.** "Does this surface-set accommodate this practice?" Mapping shape: survey surfaces → compose mental model → check accommodation against intervention-intents → identify gaps → iterate model. Mapping is iterative and theory-constructive; it does not converge on a single experiment-resolved answer the way spikes do.

**The 2026-04-30 finding.** Five frame-revisions during Phase D's spike-shape execution (build pre-flight → test-shape → intervention-surface → multi-surface + intent-tangled → gsd-2-native-placement) all traced to a single source: spike methodology applied to a mapping question. Force-fitting produced the single-target-skill-shape misframe, the multi-surface omission, the intent-tangled blindness, and the gsd-2-native-placement miss. The fix is methodology-fit at trajectory-shape level, not within-frame elaboration. This trajectory revision IS that methodology-fit response.

**Implication for execution.**
- **Phase D under (V′.a) is mapping-shape, not spike-shape.** It produces a substrate-shape map across (a) gsd-2's intervention surfaces + their composition mechanics; (b) arxiv-sanity-mcp's actual practice as substrate-evidence-channel; (c) sketched intervention-intents per substrate-area (S1-S8 per 2026-04-30 §3.4); (d) joint accommodation-evidence at the surface × intent intersection.
- **Spike methodology remains valid for "does X work?" questions** that may arise within or alongside mapping work (e.g., probing whether a specific extension surface mechanically supports a specific intervention). Such spikes nest *inside* the mapping; they do not replace it.
- **Watch for spike→mapping contamination.** When a within-mapping question genuinely is "does X work?" — fire a bounded spike for it. When the question is "does this surface-set accommodate this practice?" — keep mapping. Conflating the two is the failure-mode this revision exists to address.

**Where this could be wrong.** Counter-claim: spike methodology can be scoped flexibly to do mapping work; what was needed was broader-scoped spikes, not different methodology. Counter-counter (per 2026-04-30 §3.5): the prior Phase D scope WAS spike-shaped (single-target with M1 abort triggers; theory-construction frame of EXECUTION-LOG.md §0; build → test → findings) and that scope produced single-surface focus. Calling broader-scoped work "spike" would be cosmetic re-labeling without addressing methodology-fit. (V′.a) Step 3 plan-self-audit is scoped to challenge this finding explicitly.

---

## §1. Trajectory shape (phases + gates)

The trajectory is **eight phases, A through H.** Each phase has: goal, inputs, outputs, quality gate, failure-branch, commit shape.

### §1.1 Phase A: Plan-self-audit (pre-execution)

**Goal:** Cross-vendor xhigh audit of THIS plan before execution begins. Catches framing errors in the plan itself; ensures the plan's discipline-set is applied consistently and the trajectory shape is well-formed.

**Why this phase exists:** This plan is itself a load-bearing framing decision. The §0.5 discipline ("framing is heavy load-bearing") applies recursively: the plan's framing of the trajectory itself warrants cross-vendor xhigh audit.

**Inputs:** This plan file. All §0.4 mandatory-pre-reading artifacts.

**Outputs:** `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md` (cross-vendor codex GPT-5.5 xhigh; 200-500 lines; same structure as premise-bleed audit's FINDINGS.md but lens-shifted to "is this trajectory plan well-formed").

**Lens for the audit:**
- Does the plan's horizon-stack hold? (Long → medium → short → immediate well-articulated; test-case-vs-substrate relationship preserved.)
- Does the plan's quality-gating discipline match the framing-as-load-bearing principle? (Cross-vendor audits at the right places; not over-engineered; not under-engineered.)
- Does the plan handle the failure-mode taxonomy (§0.6) actively, or only nominally?
- Does the plan preserve deliberation discipline (no pre-deciding incubation, scope creep, closure-pressure)?
- Does the plan's commit-map produce backward-traceable responsibility?
- Does the plan's onboarding section actually carry the load-bearing context for fresh-session execution?
- Negative-space check: what does the plan exclude from consideration? Is the exclusion principled or accidental?

**Quality gate:** Audit returns Class A only OR Logan disposes Class B/C items per AUDIT-SPEC.md §8 disposition pathway (commit-as-is / commit-with-addendum / revise-before-execute).

**Failure-branch:** If audit returns Class C items that change the trajectory shape, revise plan before execution. If Class B-only, addendum-shape correction. If Class A-only, proceed to Phase B.

**Plan-file authority resolution (per F1 disposition):** The plan file's authoritative location is `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (in-repo, version-controlled). The runtime copy at `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` is a working-draft mirror only and is NOT the execution authority. Phase A commit places the in-repo copy under version control alongside the audit folder; future revisions must update the in-repo copy and may optionally mirror to the runtime location for `/loop` resume convenience.

**Commit:** `docs(gsd-2-uplift): trajectory plan (in-repo) + Phase A plan-self-audit + revise-before-execute DISPOSITION` — in-repo plan copy at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` + audit folder (PLAN-AUDIT.md + DISPOSITION.md) + coordination updates (STATE.md + OVERVIEW.md).

### §1.2 Phase B: Standing-context artifact

**Goal:** Land the test-case-vs-substrate clarification (§0.3) as standing context, so future sessions don't re-confuse "the project" with "the substrate."

**Inputs:** §0.3 above. CLAUDE.md current state. INITIATIVE.md current state.

**Outputs (per Logan §0.7 Q3 disposition: Option (a)):**
1. `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` — new artifact, ~80-120 lines, articulating §0.3 test-case-vs-substrate relationship in detail. Sub-sections: (i) what arxiv-sanity-mcp is in the bigger picture (spike-intensive test case for substrate-shape, not the long-horizon goal); (ii) why this matters for execution (don't lose the diagnostic loop; don't confuse "the project" with "the substrate"); (iii) what this implies for migration (when extraction happens, the test-case-vs-substrate trail-of-references must be preserved on both sides); (iv) cross-references to INITIATIVE.md, framing-widening §3.3, the spike methodology relationship.
2. CLAUDE.md doctrine load-point addition: a new bullet under §"Doctrine load-points" — **"Touching gsd-2-uplift work or arxiv-sanity-mcp's diagnostic role as substrate-shape test case"** → `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (and, when post-extraction, the appropriate location in the new repo).

**Quality gate:** Same-vendor adversarial-auditor at **high** reasoning level (not xhigh — the artifact is bounded ~80-120 lines and the audit-task is register-leak detection on a clarification artifact; deep reasoning isn't what's being tested. Per §2.4 reasoning-level principle: "high suffices for bounded register checks.") Cross-vendor codex less appropriate here because cross-vendor doesn't share the framework being clarified — register-leak is a same-vendor strength.

**Why same-vendor here, not paired:** The clarification is *about* the relationship between arxiv-sanity-mcp and gsd-2-uplift; cross-vendor doesn't have the framework familiarity to detect register-leak. Adding cross-vendor would be M1 strict-undersell (per §0.6) — using paired discipline by default when the specific failure-mode is single-vendor-detectable.

**Failure-branch:** If audit surfaces framing-leak in the clarification artifact itself (recursive risk), revise. If audit surfaces wrong location (e.g., CLAUDE.md note belongs in INITIATIVE.md context instead), revise.

**Commit:** `docs(gsd-2-uplift): test-case-vs-substrate standing-context artifact + CLAUDE.md load-point`.

### §1.3 Phase C: Incubation-checkpoint adjudication on SYNTHESIS-COMPARISON.md

**Goal:** Logan-disposes the four §5 axes + §2.1 R4 disposition-timing per SYNTHESIS-COMPARISON.md and DECISION-SPACE.md §2.3 incubation checkpoint specifics. Produces operating-frame-disposition that dispatches Phase D first-target.

**Inputs:** SYNTHESIS-COMPARISON.md (with §7.1 reading-frame point-of-use active). Both syntheses (SYNTHESIS.md + SYNTHESIS-CROSS.md). Framing-widening. INITIATIVE.md. DECISION-SPACE.md. Audit-arc trail (FINDINGS + FINDINGS-STEP2 + DIFFERENTIAL + DISPOSITION).

**Adjudication axes (per SYNTHESIS-COMPARISON.md §5):**
- **§5.1 Metaquestion** — direction-holds-with-qualifications under what context-anchoring; whether qualification-load (release machinery-vs-practice gap, Pi vendoring entanglement, R3 under-evidenced) warrants re-evaluating direction.
- **§5.2 R-mix integration** — operating-frame disposition-timing per §2.1 (operate-under-shifted-R2+R4-mix vs evaluate-whether-to-shift); first-target-shape selection (which R2 subsystem carries cheapest viable test); R3-probe-fire-timing (pre-vs-post critical path).
- **§5.3 Six-context anchoring** — Logan-disposed which context is primary; stable-vs-anticipated-shifting; how anchoring shapes §5.1 + §5.2.
- **§5.4 Side-probes** — P1 contribution-culture / P2 temporal-stability / P3 competitor-landscape / P4 breaking-change / P5 effective-state-emission / P6 telemetry-as-design-surface; which fire pre-vs-post second-wave-scoping.
- **§5.5 Cross-axis composition** — recommended order: context-anchoring → metaquestion-under-anchoring → first-target-shape → R-mix decomposition for that target → pre-required side-probes.

**Process:** Per §0.5 disposition-discipline, this is Logan-led with Claude collaboration. Suggested operational form:
1. Claude pre-reads SYNTHESIS-COMPARISON.md §5 with §7.1 reading-frame applied.
2. Claude drafts axis-by-axis "what the comparison surfaces / what dissolves the question / what's load-bearing" — one section per axis. Not Claude-disposing; surfacing.
3. Logan reads + disposes per axis. Claude records dispositions verbatim.
4. Per §2.3 DECISION-SPACE: if shifts, re-disposition the initiative; record in DECISION-SPACE.md; update INITIATIVE.md.

**Outputs:**
- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` (~150-300 lines; per-axis disposition + reasoning + cross-references; Logan-disposed marked verbatim).
- DECISION-SPACE.md updates (new §1.18 or similar capturing load-bearing dispositions from incubation).
- INITIATIVE.md updates if direction-shifts (per §2.3 conditional).

**Quality gate:** Cross-vendor xhigh audit of INCUBATION-CHECKPOINT.md after Logan disposes. **Why cross-vendor:** Logan's dispositions inherit Logan-framing inheritance (D5a caveat applies); cross-vendor reading catches framing-application-as-fact at the dispositions themselves. Same-vendor independent stress fires on Class C trigger or Logan manual-discretion (per §1.17 7-rule methodology).

**Failure-branch:** If audit returns Class C items affecting dispositions, revise per disposition pathway. If incubation surfaces frame-revision (per `framing-widening §9` items 16-17), the comparison's findings re-read against revised framing (per §6.5 disposition-stop discipline) and incubation re-runs.

**Commit:** `docs(gsd-2-uplift): incubation-checkpoint adjudication + DECISION-SPACE.md updates + audit`.

### §1.4 Phase D: Mapping-shape substrate-shape evidence collection (REVISED 2026-04-30 per (V′.a))

**Goal:** Produce a **substrate-shape map** that surfaces, for each of the 12 substrate-vision properties (per EXTERNAL-VISION-CONTEXT.md §3), where current gsd-2 surface-mechanics meet, partially-meet, or do-not-meet the property under arxiv-sanity-mcp's actual practice — at multiple intervention depths (shallow / mid / deep). The map reclassifies candidate interventions across C1 (confirmed in-scope), C2 (plausibly in-scope, evidence-needed), C3 (aspirationally in-scope, deeper exploration warranted) per EXTERNAL-VISION-CONTEXT.md §4.2; it does NOT relocate items out of C4 (those stay anchored by harness-studio pressure, requiring vision-frame revision rather than mapping evidence).

**Why this phase exists (under (V′.a)):** Per §0.8 methodology-fit acknowledgment, substrate-design-accommodation is a mapping question, not a spike question. The map is the load-bearing evidence-product feeding Phase E (mapping-coherence test) and Phase F (extraction-readiness gate). Without it, extraction would happen against an unmapped substrate — high risk of the misfits surfaced 2026-04-30 (skill-shape gsd-2-native-placement misfit; substrate-mismatch between gsd-2 decision-DB and arxiv-sanity-mcp's actual decision-artifact conventions) re-occurring at design time.

**Inputs:**
- INCUBATION-CHECKPOINT.md disposition (Phase C — operating-frame).
- EXTERNAL-VISION-CONTEXT.md §3 (12 substrate-vision properties; mapping target).
- EXTERNAL-VISION-CONTEXT.md §4 (scope-discipline; burden-of-proof + four-category model + identity-distortion narrowness).
- EXTERNAL-VISION-CONTEXT.md §5 (Phase D mapping purpose specification).
- META-SYNTHESIS.md (cross-vendor codebase-understanding-audit; gsd-2 surface vocabulary + mechanics).
- 2026-04-30 deliberation §3.1-§3.4 (gsd-2-native-placement finding; substrate-mismatch finding; multi-surface evidence-need; intent-tangled-with-surface-choice).
- 2026-04-30 deliberation §3.4 sketched intervention-intents (S1-S8): S1 multi-modal decision-trail support / S2 layered audit-arc support / S3 methodology codification / S4 deliberation discipline / S5 decision reconstruction / S6 long-arc anti-pattern detection / S7 comprehension-across-time (Context A primary) / S8 modular-surfaces-that-stay-optional (Context F secondary).
- Phase D interim evidence corpus (per 2026-04-30 §2.8 + commit `43e652b`): EXECUTION-LOG.md §1.5 substrate-shape correction; M1 calibration; source-grounded P1/P3; investigation findings; gsd-2-native-placement misfit; substrate-mismatch finding. **Carried as inputs, not as final findings.**
- arxiv-sanity-mcp practice as substrate-evidence-channel: `.planning/deliberations/`, `docs/adrs/`, `.planning/handoffs/`, `git log`, `.planning/STATE.md`, audit folders, ADR-0005-style commitments, spike program outputs (the practice the substrate must accommodate).

**The mapping target — four axes:**

The substrate-shape map is a structured artifact populated across four axes:

1. **gsd-2 intervention surfaces + composition mechanics.** Surface set per META-SYNTHESIS: skills, hooks, workflow templates (markdown-phase + yaml-step engines), extensions, MCP tools, custom subcommands, decision-DB subsystem (`gsd_decision_save` / `.gsd/DECISIONS.md` / journal / activity / sessions), knowledge graph, per-unit-type allowlists, R4 external orchestration. Map records: what each surface is, what it composes with, what state it touches, what its identity-preservation envelope is (per EXTERNAL-VISION-CONTEXT.md §4.3).
2. **arxiv-sanity-mcp practice (substrate-evidence-channel).** What practice patterns arxiv-sanity-mcp actually uses (deep deliberation; audit-arcs; ADR-grounded decisions; multi-artifact decision-trails; handoff-bridged sessions; closure-pressure detection; framing-widening; M1 paired-review; spike methodology where it fits). Map records: what the practice is, what artifacts/conventions support it, what the substrate would need to accommodate.
3. **Sketched intervention-intents (S1-S8 per 2026-04-30 §3.4 + extensions).** What we'd want gsd-2 to do if it could. Each intent implicates multiple surfaces; intents are *sketches* and revisable as mapping evidence accumulates (per intent-tangled-with-surface-choice resolution in 2026-04-30 §3.4).
4. **Joint accommodation-evidence (surface × intent intersection).** For each (surface, intent) cell where mapping is informative: what's the shallow-depth accommodation (small extension, light hook, etc.); what's the mid-depth accommodation (decision-DB extension; new unit-types; workflow-template additions); what's the deep accommodation (vision-aware lifecycle; classification-driven workflow-selection; full progressive activation). What's the identity-preservation envelope at each depth? What's the harness-studio-pressure foreclosure-risk at each depth?

**The 12-property scope-control overlay.** For each of the 12 substrate-vision properties (per EXTERNAL-VISION-CONTEXT.md §3), the map records: at what depth (shallow / mid / deep) is the property pursuable under current gsd-2 surface-mechanics? What's the C1/C2/C3/C4 confidence per depth (per EXTERNAL-VISION-CONTEXT.md §4.2)? **Burden of proof rests on exclusion** (per §4.1): default depth is candidate-in-scope; downgrade requires demonstrated grounds.

**Process:**
1. Read inputs (per §0.4 mandatory pre-reading + Phase D interim corpus).
2. **Phase-entry frame-revision-check** (per §6.1 + §0.5 — the (V′.a) Step 4 mechanism): is the question we're answering still right? Is mapping the right shape? Surface to Logan if frame-revision is warranted.
3. Survey gsd-2 intervention surfaces + composition mechanics (axis 1). Read META-SYNTHESIS as primary grounding; supplement with source-archaeology where mechanics are unclear. Output: surface-mechanics inventory with identity-preservation envelope per surface.
4. Survey arxiv-sanity-mcp practice (axis 2). Inventory what practice patterns the substrate must accommodate (deliberation discipline; audit-arc patterns; multi-modal decision-trails; ADR-grounded commitments; handoff conventions; closure-pressure-pattern detection; M1 paired-review; spike methodology where it fits; offshoot pattern; etc.). Output: practice inventory with substrate-needs-per-practice.
5. **Mid-Phase frame-revision-check** (per §6.1 + §0.5): are observations diverging from priors? If new mapping-shape methodology questions surface, address them. If a within-mapping question genuinely shifts to "does X work?" shape, fire a bounded spike for it (per §0.8 spikes-nest-inside-mapping discipline).
6. Articulate sketched intervention-intents (axis 3). Start from S1-S8 per 2026-04-30 §3.4; add others surfaced during the survey. Cross-check against EXTERNAL-VISION-CONTEXT.md §3 12-property set — every property should have at least one representative intent in the sketched set, OR an explicit note about why no intent is sketched at this stage. **Iteration-mechanics gesture (intent-tangled-with-surface-choice per 2026-04-30 §3.4 + Hanson theory-laden-observation problem):** intent-sketches are revisable artifacts, not commitments. After axis-3 articulation passes, axes 1 + 2 inventories may surface accommodation-evidence (or its absence) that revises an intent's shape — e.g., a surface-mechanic absence may suggest the intent was under-specified for that surface; an arxiv-sanity-mcp practice pattern may reveal an intent the original S1-S8 list missed. When an axis-3 revision-trigger surfaces during axes-4 cell construction, record: (a) what was the prior intent-sketch; (b) what evidence triggered revision; (c) what the revised intent-sketch is; (d) whether revision warrants re-traversing earlier-completed cells under the new intent. **This iteration-shape gesture is one possible shape; Phase D execution may surface a different shape (e.g., revision-trigger should fire from intent-survey not surface-survey; or axes 3 + 4 should compose differently); frame-revision-check at process step 5 fires if the iteration-shape itself shifts.** The discipline is: the under-specification of iteration-mechanics here is intentional (mapping is theory-constructive; locking iteration shape prematurely is closure-pressure), not negligent.
7. Construct joint accommodation-evidence cells (axis 4). For each (surface, intent) cell that's informative, record shallow / mid / deep accommodation evidence + identity-preservation envelope + harness-studio-pressure foreclosure-risk. Cells that are uninformative (no plausible accommodation; not the surface for this intent) get explicitly marked as such (per performative-vs-operational openness discipline). When cell-construction surfaces intent-revision-triggers (per step 6 iteration-mechanics gesture), pause cell work, complete intent-revision, decide whether to re-traverse earlier cells, then resume.
8. Apply 12-property scope-control overlay. Per property × depth, classify as C1 / C2 / C3 / C4 with reasoning. Burden of proof on exclusion: default candidate-in-scope.
9. **Phase-output-draft frame-revision-check** (per §6.1 + §0.5): is the map well-formed? Has the question still got the right shape? Are there frame-revisions surfaced during construction that warrant pause-and-replan rather than commit?
10. Draft FINDINGS.md (the substrate-shape map) + DISPOSITION.md (Logan disposes).

**Outputs:**
- `.planning/gsd-2-uplift/wave-2/substrate-shape-map/SUBSTRATE-SHAPE-MAP.md` (mapping-shape Phase D's primary output; structured across four axes + 12-property overlay; ~600-1200 lines depending on map density). Replaces the wave-2/decision-trace/ skill-shape outputs as Phase D's final FINDINGS.md. **Budget-deviation-as-frame-revision-trigger:** if the map comes in meaningfully under (e.g., far-below 600 lines) or over (e.g., far-above 1200 lines), do NOT silently absorb. Underrun could mean (a) mapping-territory genuinely thinner than expected → substrate-shape evidence + readiness for Phase E early; OR (b) Phase D scope-truncation → closure-pressure recurrence. Overrun could mean (a) mapping-territory denser than expected → substrate-shape evidence + Phase D may need split; OR (b) scope-creep (e.g., intervention-intent sketch expanding into design-work). Different findings warrant different actions; phase-output-draft frame-revision-check (process step 9) is where the meta-question surfaces. Threshold deliberately unspecified — let executor-judgment fire on "feels meaningful," not on artificial precision (artificial precision would be closure-pressure-shaped).
- `.planning/gsd-2-uplift/wave-2/substrate-shape-map/INTERIM-CORPUS-INTEGRATION.md` (~150-300 lines; how the interim Phase D corpus from 2026-04-30 — gsd-2-native-placement misfit, substrate-mismatch finding, source-grounded P1/P3, investigation findings — gets carried into the map; what stays as evidence and what gets reclassified).
- `.planning/gsd-2-uplift/wave-2/substrate-shape-map/DISPOSITION.md` (~80-150 lines; Logan disposes the map; flags any properties / intents / cells warranting deeper exploration before Phase E).
- Audit folder with FINDINGS + DISPOSITION (cross-vendor xhigh + same-vendor xhigh paired per §2.4 update).

**Quality gate (cross-vendor xhigh + same-vendor xhigh paired):** The map carries high framing-load (mapping target shape itself is at framing-inheritance risk per 2026-04-30 §5.3 audit-discipline-limits finding). Paired discipline fires:
- **Cross-vendor xhigh** (codex GPT-5.5 xhigh): does the four-axis structure hold? Are there 12-property gaps the map missed? Is the C1/C2/C3/C4 classification well-evidenced? Negative-space check: what's NOT in the map that should be (excluded surfaces, omitted intents, missing accommodation cells)?
- **Same-vendor xhigh** (adversarial-auditor-xhigh independent mode): is the map drifting back into spike-shape framing? Is any "single-target accommodation" claim unsupported? Is integration-grammar-as-fact present at the map-claim level (treating mapping vocabulary as observed-fact rather than as inputs)?
- **Audit lens explicit:** "Is the map mapping-shape, or has it drifted toward spike-shape claims (single-target / converges-on-answer)?" + "Are the 12 properties + four-category scope-confidence model applied as scope-controls per EXTERNAL-VISION-CONTEXT.md §3-§4?" + "Has the closure-pressure-into-elaboration pattern surfaced new frame-revisions during mapping that warrant phase-restart rather than commit?"

**Failure-branch:**
- If audit surfaces frame-revision (the closure-pressure pattern recurred again): apply 2026-04-30 §5 calibration findings; either fix at point-of-bleed and re-audit, or pause to plan-self-audit-2 if the methodology-fit itself is in question.
- If audit surfaces "this is still spike-shape masquerading as mapping" — return to §0.8 methodology-fit reading + revise. Record explicitly per traces-over-erasure discipline.
- If interim Phase D corpus integration surfaces new evidence that shifts the mapping (e.g., gsd-2-native-placement finding generalizes beyond decision-trace): apply per §5.4 productive-curiosity pattern; expand mapping scope or surface for Logan-disposition.

**Phase-D-specific watch-flags (2026-04-30 calibration findings as live concerns):**
- **Closure-pressure-into-elaboration recurrence** (per 2026-04-30 §5.1; pattern surfaced multiple times during 2026-05-01 turn-cluster too). Watch for: "the mapping is resolved enough" framings absent evidence; elaborate within-frame work without frame-revision-check firing; "this surface obviously accommodates this intent" without joint-evidence.
- **In-session-collaboration risk on mapping target shape** (per 2026-04-30 §5.4; pattern recognition required Logan's pressure). Cross-vendor xhigh audit + same-vendor xhigh independent paired discipline (above) is structural mitigation. Logan-disposition is for user-intent capture (per 2026-04-30 §2.7 + §5.2), NOT for substrate-design-soundness audit-of-last-resort.
- **Audit-discipline limits** (per 2026-04-30 §5.3). Audit-spec must include "challenge intervention-surface choice" + "challenge methodology-fit" lens-questions explicitly — not just "is this artifact well-formed?". Embedded in audit-spec (above).

**Commit pattern:**
- (1) `docs(gsd-2-uplift): Phase D mapping-shape substrate-shape map + interim-corpus-integration` (the map + integration document together).
- (2) `docs(gsd-2-uplift): Phase D substrate-shape map audit + DISPOSITION` (audit folder + Logan disposition).
- (3) Coordination updates (STATE.md + OVERVIEW.md) per §6.2.

### §1.5 Phase E: Mapping-coherence + theory-construction quality test (REVISED 2026-04-30 per (V′.a))

**Goal:** Verify that the Phase D substrate-shape map is **coherent as a theory-construction artifact** — not "stable" in the spike-disposition sense. Mapping is iterative + theory-constructive; the relevant test is whether the map holds together as a coherent theory of the gsd-2 × arxiv-sanity-mcp × intervention-intents × accommodation-evidence territory, and whether the theory survives:
1. **Fresh-session re-read** (per §0.5 D5a caveat — does the map's structure + claims survive without Claude+Logan in-session-collaboration carrying it?).
2. **Internal cross-axis coherence** (do the four axes hang together; do (surface, intent) accommodation-cells sum to a coherent picture; do the 12-property classifications follow consistently from the underlying evidence; are there axis-internal contradictions?).
3. **Cross-vendor xhigh read** (does cross-vendor xhigh agree the map is well-formed; does it surface 12-property gaps or surface-omissions or intent-omissions that suggest the theory is incomplete in load-bearing ways?).
4. **Theory-construction-quality lenses** (per spike METHODOLOGY.md adapted to mapping: model-verification through evidence-traceability; framework-fit-lens; alternative-theory lens — could the same evidence support a different mapping shape and would that matter?).

**Inputs:** Phase D substrate-shape map (SUBSTRATE-SHAPE-MAP.md + INTERIM-CORPUS-INTEGRATION.md + DISPOSITION.md) + Phase D audit findings + DECISION-SPACE.md updates from Phase C + EXTERNAL-VISION-CONTEXT.md §3-§4 (the scope-control overlay the map applies).

**Process:**
1. Logan reads Phase D outputs in a fresh session (or after deliberate gap from Phase D session) — fresh-context coherence test.
2. **Internal cross-axis coherence audit:** main-thread Claude reads the map for axis-internal coherence + cross-axis consistency (e.g., does intent S5 "decision reconstruction" land at consistent depth-classification across the surfaces it implicates? Does property #4 "work-history multi-modal" map at consistent depths to the intents that operationalize it?).
3. **Cross-vendor xhigh audit (codex GPT-5.5 xhigh)** reads the map. Lens: "is the map a coherent theory of the territory; are there 12-property gaps; are there surface or intent omissions that suggest theory-incompleteness; does the C1/C2/C3 classification logic hold consistently across cells; is the burden-of-proof-on-exclusion discipline applied correctly per EXTERNAL-VISION-CONTEXT.md §4.1; is harness-studio-pressure foreclosure-risk surfaced where it applies?"
4. **Same-vendor xhigh adversarial-auditor (independent mode)** stress-tests the theory: "could the same evidence be marshaled into a different mapping shape — what would that look like, what would change about the conclusions; is integration-grammar-as-fact present at the map-claim level; has the closure-pressure-into-elaboration pattern produced any 'resolved enough' framings without evidence?"
5. Logan disposes: theory-coherent / partially-coherent / incoherent (with named axes/properties/intents requiring further mapping work).

**Outputs:**
- `.planning/gsd-2-uplift/MAPPING-COHERENCE-CHECK.md` (~100-200 lines; what theory-construction tests were applied; per-axis coherence findings; per-property coherence findings; cross-axis tensions surfaced; what would shift the call from coherent ↔ partially-coherent ↔ incoherent; Logan disposition).
- If partially-coherent: triggers targeted re-mapping (return to Phase D for specific axes/properties; do NOT restart whole-map work unless multiple axes are in question).
- If incoherent: triggers Phase D re-execution + (V′.b) consideration (return to incubation-level; map shape itself was wrong).

**Quality gate:** Theory-coherence call requires evidence-load justification. "Feels coherent" is closure-pressure (per §0.5); requires per-axis + per-property explicit coherence-evidence. Paired audit-discipline (cross-vendor + same-vendor) is the structural mitigation against the closure-pressure-pattern recurrence — particularly load-bearing here per 2026-04-30 §5.1 finding.

**Failure-branch:**
- **Partially-coherent (most likely outcome):** identify which axes/properties/intents are coherent vs. need further mapping. Coherent axes proceed to Phase F readiness consideration; incoherent axes loop back to Phase D for targeted re-mapping. Record which.
- **Incoherent:** map theory itself is misshapen. Loop back to question-shape disposition (potentially (V′.b) — replan trajectory shape itself if mapping methodology is itself wrong for the question).
- **New frame-revision surfaces during Phase E** (productive-curiosity per §5.4): record + propagate; do not silently absorb.

**Commit:** `docs(gsd-2-uplift): Phase E mapping-coherence check + audit + DISPOSITION`.

### §1.6 Phase F: Extraction-readiness gate (REVISED 2026-04-30 per (V′.a) — mapping-coherence + intent-intervention-feasibility)

**Goal:** Hard gate before extraction. Verifies that the conditions for extraction (per §0.3 test-case-vs-substrate analysis + §0.8 mapping-shape methodology-fit) are met.

**Gate criteria (all required; not Logan-discretion-bypassable except with explicit reasoning):**

1. **Mapping-coherent** (Phase E confirmed coherent, or partial-coherence with documented incoherent-axis-deferral plan). The substrate-shape map's four-axis structure holds together as a coherent theory of the territory; per-property C1/C2/C3 classifications are consistent; theory-construction-quality lenses passed.

2. **Intent-intervention feasibility surfaced for at least one C1-classified intervention path.** The map identifies at least one (intervention-intent × surface × depth) triplet at C1 confidence (per EXTERNAL-VISION-CONTEXT.md §4.2: "patches we can plausibly land based on current evidence") with named accommodation-evidence + identity-preservation envelope + harness-studio-pressure foreclosure-check. **This replaces the prior "first-target evidence in" criterion** — under mapping-shape, what gates extraction is "the map identifies feasible intervention paths," not "a single first-target was executed." (If zero C1 paths exist: the map either is incomplete OR the substrate genuinely cannot accommodate any intervention at low risk — both are findings warranting Phase D re-execution or (V′.b) consideration, not extraction.)

3. **Internal coherence + diagnostic-loop-preserving** — the gsd-2-uplift work has citations to its own internal artifacts (META-SYNTHESIS, substrate-shape map, INTERIM-CORPUS-INTEGRATION, audits, INITIATIVE, EXTERNAL-VISION-CONTEXT, RELATIONSHIP-TO-PARENT, METHODOLOGY-MISMATCH-FINDING) rather than depending heavily on arxiv-sanity-mcp-spike-program-references for its load-bearing claims. (If R5 disposed: heavier dependency may be appropriate; document.) Note: "internal coherence" here means the new-repo-content stands on its own internal logic, NOT that it has zero references back to arxiv-sanity-mcp; explicit references back for diagnostic evidence are expected and preserved (per §1.8 Phase H test phrasing). The diagnostic-loop relationship (arxiv-sanity-mcp practice as substrate-evidence-channel) must remain readable post-extraction.

4. **Repo-extraction triggers fired** — at least one of: (a) disposition explicitly commits to dedicated-uplift-repo as part of design (R1 fork; R5 sibling; R-mix per Phase C disposition); (b) substrate-shape mapping work has internal gravitational center independent of arxiv-sanity-mcp; (c) materially-competing-for-shared-resources signal (planning-tree confusion affecting spike work or arxiv-sanity-mcp implementation work); (d) the substrate-shape map identifies enough cross-project / portfolio-shape work (per Property 12 in EXTERNAL-VISION-CONTEXT.md §3) that staying within arxiv-sanity-mcp's planning tree distorts the work.

5. **Methodology-mismatch finding integrated** — the substrate-shape map + audit findings explicitly account for the 2026-04-30 methodology-mismatch finding (mapping-vs-spike question-shape distinction operationalized, not just nominally acknowledged). The METHODOLOGY-MISMATCH-FINDING.md artifact (per (V′.a) Step 5) is referenced from the map.

6. **No outstanding load-bearing-decisions block extraction** (per Logan disposition).

**Inputs:** All prior phase outputs + DECISION-SPACE.md + INITIATIVE.md + STATE.md current state.

**Process:**
1. Cross-vendor xhigh audit fires the gate criteria check (lens: "does this state warrant extraction; what's the strongest argument against; what's the weakest evidence supporting").
2. Logan disposes go-no-go.

**Outputs:**
- `.planning/gsd-2-uplift/EXTRACTION-READINESS.md` (~100-200 lines; gate-criteria check + audit findings + Logan disposition).

**Quality gate:** Audit must explicitly cover negative-space (what's NOT ready that might be load-bearing).

**Failure-branch:** If gate fails, identify specific criterion failed; loop to appropriate prior phase. (Common case: criterion 3 fails because the internal coherence still leans on spike-program-references; loop to Phase D to produce more internal evidence; or accept the dependency and document it for post-extraction handling.)

**Commit:** `docs(gsd-2-uplift): extraction-readiness gate + audit + disposition`.

### §1.7 Phase G: Extraction execution

**Goal:** Move the gsd-2-uplift initiative into its own repo. Mechanical phase, but with discipline around what moves vs what stays vs what gets cited-by-reference.

**Authoritative custody rule (per INITIATIVE.md §7 + Phase A audit F2 disposition):** INITIATIVE.md §7 establishes that **DECISION-SPACE.md and the deliberation log STAY in arxiv-sanity-mcp** because they record the genesis session of the initiative; **INITIATIVE.md and exploration outputs MIGRATE** to the new repo as initiative-scoping artifacts. The artifact-by-artifact table below operationalizes this rule. Any Logan-discretion deviation (e.g., duplicating DECISION-SPACE.md to both repos with bidirectional reference) must be explicit and recorded in EXTRACTION-LOG.md with reasoning.

**Artifact-by-artifact disposition table:**

| Artifact (current path in arxiv-sanity-mcp) | Disposition | Reasoning |
|---|---|---|
| `.planning/gsd-2-uplift/INITIATIVE.md` | **MOVE** | Initiative-scoping artifact (per INITIATIVE.md §7 explicit migration). Replace in arxiv-sanity-mcp with a thin pointer/genesis-marker artifact citing new-repo location. |
| `.planning/gsd-2-uplift/DECISION-SPACE.md` | **STAY** (per INITIATIVE.md §7) | Records arxiv-sanity-mcp's session that genesised the initiative. New repo gets its own decision-space starting from extraction-state if Logan disposes; this artifact remains canonical for the genesis trail. |
| `.planning/gsd-2-uplift/exploration/` (SYNTHESIS.md + SYNTHESIS-CROSS.md + SYNTHESIS-COMPARISON.md + INCUBATION-CHECKPOINT.md + STABILITY-CHECK.md + EXTRACTION-READINESS.md) | **MOVE** | Initiative-scoping exploration outputs (per INITIATIVE.md §7 explicit migration). |
| `.planning/gsd-2-uplift/audits/` (all uplift-scoped audit folders) | **MOVE** | Audits about uplift artifacts; their findings are about substrate-shape work. |
| `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` | **MOVE** | Initiative coordination record. |
| `.planning/gsd-2-uplift/wave-2/` (Phase D outputs — `decision-trace/` interim corpus + `substrate-shape-map/` mapping outputs) | **MOVE** | Substrate-shape mapping work product. The interim `decision-trace/` corpus moves alongside the final `substrate-shape-map/` outputs as carried-forward evidence (per Phase D INTERIM-CORPUS-INTEGRATION.md). |
| `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (Phase B output) | **DUPLICATE** (cite-by-reference) | This artifact is intrinsically about both sides of the relationship. arxiv-sanity-mcp keeps a copy referencing new-repo location for its diagnostic-loop trail; new repo keeps a copy referencing arxiv-sanity-mcp's spike program. Bidirectional reference; both copies updated to point at the other. |
| `.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md` (2026-05-01 standing-context artifact) | **DUPLICATE** (cite-by-reference) | Per the artifact's own frontmatter (`post_extraction_disposition: DUPLICATE`). Both sides keep a copy with bidirectional references to the other side and to harness-studio's sibling artifact. Vision-context is intrinsically cross-project (substrate-vision properties cross both gsd-2-uplift and the eventual harness-studio operating model); duplication preserves cross-project legibility. |
| `.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md` ((V′.a) Step 5 output) | **DUPLICATE** (cite-by-reference) | Self-correction from Step 2 (initially MOVE; revised on Step 2 self-review). The finding is intrinsically about both sides: (a) substrate-shape evidence (methodology-fit finding about substrate-design-evidence-collection) → matters in new repo; (b) diagnostic-loop record (the spike program at arxiv-sanity-mcp produced this finding through Phase D's misframe-and-recovery; the local-staying 2026-04-30 deliberation references it) → matters in arxiv-sanity-mcp. Same structural shape as RELATIONSHIP-TO-PARENT.md and EXTERNAL-VISION-CONTEXT.md (DUPLICATE precedent). Both copies updated to point at the other; sync-discipline note in both copies. |
| `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` | **Per-deliberation Logan-disposed** | Same heuristic as other uplift-substantive deliberations: records both arxiv-sanity-mcp's session-dynamic (the deliberation arc with five frame-revisions; Logan's correction; calibration findings about the substrate's behavior) AND substantive substrate-shape content (methodology-mismatch finding; (V′.a) disposition). Reasonable readings: STAY (recording of session-dynamic that arrived at substrate-shape conclusion; the diagnostic-loop record needs it local) OR MOVE (substrate-shape-substantive content that informs new-repo work). Logan disposes; EXTRACTION-LOG.md records reasoning. |
| `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (this plan) | **MOVE** (with arxiv-sanity-mcp citation kept) | Plan governs the extraction it just executed; lives in new repo as historical record. arxiv-sanity-mcp's EXTRACTION-LOG.md cites the plan's new-repo location. |
| `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` and similar genesis-recording deliberations | **STAY** (per INITIATIVE.md §7 deliberation-log retention) | Records arxiv-sanity-mcp's session-genesis. |
| Uplift-substantive deliberations from `.planning/deliberations/` (e.g., 2026-04-28-framing-widening, comparison-drafting, audit-spec-review) | **Per-deliberation Logan-disposed** | Default heuristic: if the deliberation primarily records arxiv-sanity-mcp's session-dynamic that arrived at an uplift conclusion → STAY; if it primarily records substrate-shape-substantive-content → MOVE. EXTRACTION-LOG.md records per-deliberation disposition + reasoning. |
| Uplift-related handoffs from `.planning/handoffs/` | **Per-handoff Logan-disposed** | Default heuristic: if the handoff bridges sessions for arxiv-sanity-mcp's stewardship of the initiative → STAY; if it bridges new-repo work in the future → MOVE. EXTRACTION-LOG.md records per-handoff disposition. |
| `.planning/spikes/` (spike program) | **STAY** | Diagnostic about substrate-shape but the spike work itself is arxiv-sanity-mcp-shaped (per §0.3). New repo cites by reference. |
| `.planning/foundation-audit/` | **STAY** | Project-side; about arxiv-sanity-mcp, not the substrate. |
| Methodology files (`.planning/spikes/METHODOLOGY.md`, `.planning/foundation-audit/METHODOLOGY.md`, `.planning/LONG-ARC.md`, `AGENTS.md`, `CLAUDE.md`) | **STAY (and reapply, not migrate)** | Current-runtime-shaped per CLAUDE.md. New repo authors its own CLAUDE.md/AGENTS.md/LONG-ARC.md (or analogous) reflecting its own runtime + identity. |

**What gets cited-by-reference from new repo to arxiv-sanity-mcp:**
- Spike-program outputs (as evidence about substrate behavior under arxiv-sanity-mcp-spike conditions).
- Foundation-audit findings (as project-side evidence the substrate had to handle).
- DECISION-SPACE.md (genesis decision-trail; new repo cites for "how the initiative arrived at its starting state").
- Genesis-recording deliberations and handoffs (per per-artifact disposition above).

**What gets cited-by-reference from arxiv-sanity-mcp to new repo:**
- INITIATIVE.md (replaced with thin pointer artifact at the same path; the pointer cites new-repo location and gives ~10 lines of "this initiative migrated on [date]; trail-of-references at [new repo path]; genesis record retained at DECISION-SPACE.md §X").
- exploration/ (replaced with similar pointer at the same path).
- audits/ (replaced with similar pointer; specific audit folder pointers if any are still cited from arxiv-sanity-mcp-side artifacts).
- This plan file (the trajectory/ pointer).
- RELATIONSHIP-TO-PARENT.md (kept locally + cites new-repo copy).

**Process:**
1. Create dedicated repo (per Logan-disposed location and structure).
2. Move artifacts per artifact-by-artifact table.
3. Establish trail-of-references on both sides.
4. Update CLAUDE.md + STATE.md + arxiv-sanity-mcp's load-points to reflect post-extraction state.
5. New repo authors its own CLAUDE.md (reapplied per current-runtime-shape) + AGENTS.md + LONG-ARC.md (or analogous).

**Outputs:**
- New repo (location Logan-disposed) with full uplift artifact tree.
- arxiv-sanity-mcp planning tree updated with trail-of-references and pointer artifacts at moved-from paths.
- `.planning/gsd-2-uplift/EXTRACTION-LOG.md` in arxiv-sanity-mcp (records what moved when; final disposition of each artifact; cross-repo commit identity per §4.2.1; ~150-300 lines).

**Quality gate:** Cross-vendor **high** audit of EXTRACTION-LOG.md + sample-check that new repo's load-bearing artifacts reference internal-only or properly-cited-back (no orphan references to arxiv-sanity-mcp-only paths in load-bearing claims; references-back for diagnostic evidence are explicit and traceable). Aligned with §2.4: mechanical-coherence (orphan-reference + missed-migration + cross-reference integrity) is bounded; xhigh would be over-engineered for this audit shape.

**Failure-branch:** If audit surfaces orphan references or broken cross-references, fix before commit. If audit surfaces missed migrations (artifact should have moved but didn't), apply.

**Commit pattern:**
- arxiv-sanity-mcp side: `docs(gsd-2-uplift): extract initiative to dedicated repo + trail-of-references + EXTRACTION-LOG.md`. Body MUST include the new-repo initial commit hash (added via follow-up commit if hash not yet known at primary commit time; see §4.2.1).
- New repo side: `chore(repo): initial population from arxiv-sanity-mcp gsd-2-uplift initiative` (or per new repo's commit conventions). Body MUST include the arxiv-sanity-mcp source commit hash that triggered extraction.

### §1.8 Phase H: Post-extraction integration

**Goal:** Verify both sides (new repo + arxiv-sanity-mcp) work coherently after extraction. Catch broken references, missed updates, lost context.

**Inputs:** Both repos in post-extraction state.

**Process:**
1. Fresh-context Claude reads new repo's CLAUDE.md + INITIATIVE.md + (any new-repo-local decision-state artifact, plus the cited-back DECISION-SPACE.md in arxiv-sanity-mcp for genesis trail); can it reconstruct the medium-horizon and short-horizon work **from new-repo-local artifacts, while following explicit references back to arxiv-sanity-mcp for diagnostic evidence** (spike-program outputs, foundation-audit findings, plan-audit trail, DECISION-SPACE.md genesis record)? (If yes: internal coherence holds with intact diagnostic-loop dependency. If no: what's missing — does the new repo need additional internal artifacts, or are the references-back miscalibrated?)
2. Fresh-context Claude reads arxiv-sanity-mcp's CLAUDE.md + STATE.md + Phase B's standing-context artifact; can it understand that gsd-2-uplift moved out + where to find it + what the diagnostic-loop relationship is + which artifacts stayed (DECISION-SPACE.md, deliberations, spike program) and why? (If yes: trail-of-references holds. If no: what's missing?)
3. Cross-vendor xhigh audit of integration: lens: "does each side preserve what it needs; does each side properly cite-by-reference what's now in the other; are there orphan references or context-loss patterns; does the references-back design (rather than independence) match §0.3 diagnostic-loop discipline?"

**Outputs:**
- `.planning/gsd-2-uplift/EXTRACTION-LOG.md` updated with Phase H verification results + final cross-repo commit identities (both sides' final commit hashes after Phase H corrections).
- New repo has any necessary corrections applied.

**Quality gate:** Both fresh-context tests pass (yes-and-yes, where "yes" means coherence-with-intact-references-back, NOT independence). Audit returns Class A only OR fixes applied for Class B/C.

**Failure-branch:** If either fresh-context test fails, identify gap and fill in the appropriate side. If audit surfaces deeper integration issues, may require re-running parts of Phase G.

**Commit pattern:** Both sides as needed; final commit messages reference EXTRACTION-LOG.md and include the paired commit hash from the other repo (per §4.2.1).

---

## §2. Quality-gating + audit cadence

### §2.1 What triggers cross-vendor audit (reasoning-level per §2.4)

**Default-fires (no Logan-discretion to skip):**
- Plan-self-audit (Phase A) + (V′.a) Step 3 plan-self-audit-2 (this revision under audit, scoped to question-shape-fit).
- Incubation-checkpoint adjudication output (Phase C — Logan dispositions inherit framing).
- **Substrate-shape map (Phase D under (V′.a))** — load-bearing for Phase E coherence test + Phase F gate; carries highest cross-cutting framing-load.
- **Mapping-coherence test (Phase E under (V′.a))** — load-bearing for go-no-go gate; theory-coherence stake.
- Extraction-readiness gate (Phase F — hard gate).
- Extraction execution audit (Phase G — orphan-reference + missed-migration check).
- Post-extraction integration (Phase H — coherence check).

**Conditional-fires (Logan-discretion):**
- Phase B standing-context artifact (only if Logan disposes the artifact carries framing-leak risk; same-vendor xhigh adversarial is the default for register-leak).
- Re-adjudication triggers (any phase that loops back fires fresh audit on the updated artifact).
- Within-mapping spike audits (when mapping-shape Phase D fires bounded spikes inside the mapping per §0.8 — those spikes get spike-program audit-discipline scaled to spike scope).

**What "cross-vendor xhigh" means operationally:**
- Cross-vendor: codex GPT-5.5 xhigh (per current cross-vendor pattern; substitute analogous if codex unavailable).
- xhigh effort: explicit reasoning-effort=xhigh override (or `model_reasoning_effort="high"` if xhigh not available; high is acceptable substitute per Logan's "high if appropriate" allowance).
- Output structure: per AUDIT-SPEC.md §6.1 (FINDINGS structure).

### §2.2 What triggers same-vendor adversarial audit (reasoning-level per §2.4)

**Default-fires:**
- Phase B standing-context artifact (register-leak detection).
- Independent-mode Step-2 stress on any cross-vendor audit Class C return (per AUDIT-SPEC.md §3.4 manual-discretion).

**Conditional-fires:**
- Logan manual-discretion at any decision point where shared-Claude+Logan-framing-inheritance is suspected.
- Integration-grammar-as-fact concern (the Step-2 same-vendor catch from premise-bleed audit).

**What "same-vendor adversarial-auditor-xhigh" means operationally:**
- Agent type: `adversarial-auditor-xhigh` (per existing infrastructure).
- Independent mode: do NOT read prior cross-vendor outputs (per AUDIT-SPEC.md §3.4 manual-discretion override pattern from premise-bleed audit).

### §2.3 What triggers paired (cross-vendor + same-vendor independent) audit

**Default-fires:**
- Phase A plan-self-audit MAY use paired discipline (Logan-discretion; depends on plan-load-bearing-ness Logan reads).
- Phase C incubation-checkpoint adjudication output MAY use paired discipline (Logan-discretion; depends on disposition-load-bearing-ness).
- **Phase D substrate-shape map (under (V′.a))** — paired-default (per §2.4 Phase D row + 2026-04-30 §5.3 audit-discipline-limits finding). Cross-vendor catches 12-property gaps + surface-omissions; same-vendor catches drift-back-to-spike-shape + integration-grammar-as-fact at map-claim level + closure-pressure-pattern resolutions-without-evidence. Logan-discretion to downgrade to single-vendor under cost-bandwidth constraint, with tradeoff explicit in DISPOSITION (downgrade reintroduces 2026-04-30 §5.4 closure-pressure-pattern-survives-single-vendor risk).
- **Phase E mapping-coherence test (under (V′.a))** — paired-default (per §2.4 Phase E row). Same rationale: theory-construction stage carries both vocabulary-import risk + integration-grammar-as-fact risk. Same Logan-discretion-to-downgrade as Phase D.
- **(V′.a) Step 3 plan-self-audit-2 (the revision under this section)** — paired-default; this revision IS the artifact at framing-inheritance risk per the 2026-04-30 §5.4 finding (max-effort + Logan-correction was the necessary condition to break the prior misframe; the revision must clear paired audit-discipline). **Audit-spec for Step 3 should be drafted independently** per Concern 1 disposition (cross-vendor codex independent spec-drafting recommended; Logan disposes spec-drafting form before audit dispatch).

**Pattern (per premise-bleed audit precedent):**
1. Cross-vendor codex Step-1 baseline.
2. Same-vendor adversarial-auditor-xhigh independent Step-2 (per §3.4 manual-discretion override of differential default).
3. Main-thread Claude differential analysis (DIFFERENTIAL.md).
4. Logan disposes per spec §8.

### §2.4 Per-audit reasoning-level table (xhigh vs high — Logan §0.7 Q2 disposition)

Per Logan's frame "be smart and elegant about harnessing reasoning effectively" — reasoning-level (xhigh vs high) is **judged per-audit based on the audit-task's shape, quality, and kind**, not blanketly applied. The principle:

**Audit reasoning-level scales with:**
- **Framing-load** of the artifact under audit (high framing-load → xhigh).
- **Cross-cutting reasoning required** (synthesizing across many artifacts → xhigh).
- **Decision-stake** (gate-passes, dispositions that shape downstream phases → xhigh).
- **Negative-space depth** (audit must reason about what's *absent* → xhigh).

**high suffices when:**
- **Mechanical-coherence** is what's being checked (orphan references, citation integrity, migration completeness).
- **Bounded register checks** on a small clarification artifact.
- **Fact-grounding** rather than architectural inference.
- The audit task is well-scoped and doesn't require synthesis across many artifacts.

**Per-phase audit reasoning-level assignments:**

| Phase | Audit | Vendor | Level | Reasoning-level rationale |
|---|---|---|---|---|
| A | Plan-self-audit | Cross-vendor codex GPT-5.5 | **xhigh** | This plan is itself a heavy framing decision affecting all 8 phases. Framing-load: highest in the trajectory. Cross-cutting: spans onboarding + trajectory + quality-gating + artifact map + commit map + failure-modes. Negative-space-depth: deep (what's the plan excluding from consideration?). xhigh warranted. |
| A | Plan-self-audit (paired Step-2) | Same-vendor adversarial-auditor | **xhigh** (Logan-discretion to fire) | Paired discipline at Logan-discretion. If fired, same-vendor catches integration-grammar-as-fact at meta-level (the §7-addendum-shaped residual we just exercised). xhigh because the residual is exactly register-shaped + meta-level. |
| B | Standing-context artifact audit | Same-vendor adversarial-auditor | **high** | Bounded artifact (~80-120 lines). Register-leak detection on a clarification artifact. Deep reasoning isn't what's being tested. high suffices. |
| C | Incubation-checkpoint audit | Cross-vendor codex GPT-5.5 | **xhigh** | Logan dispositions on §5 axes inherit Logan-framing inheritance. Decision-stake: shapes second-wave-target, which shapes substrate-shape evidence, which shapes extraction-readiness. Cross-cutting: integrates synthesis + comparison + framing-widening + audit-arc outcomes. xhigh warranted. |
| C | Incubation-checkpoint audit (paired Step-2) | Same-vendor adversarial-auditor | **xhigh** (Logan-discretion to fire) | If fired (recommended given premise-bleed audit precedent), catches integration-grammar-as-fact at the dispositions themselves. xhigh because dispositions carry framing-load. |
| D | Substrate-shape map audit (REVISED 2026-04-30 per (V′.a) — mapping-shape) | Cross-vendor codex GPT-5.5 | **xhigh** | Mapping-shape Phase D's substrate-shape map carries highest cross-cutting framing-load: 4 axes × 12 substrate-vision properties × multiple intervention-intents × multi-depth accommodation evidence × C1/C2/C3/C4 scope-classification overlay. Negative-space-depth deep ("what surfaces / intents / properties did the map miss?"). Decision-stake: feeds Phase E coherence test + Phase F gate. Aligned with §2.4 principle: "Cross-cutting reasoning required → xhigh." |
| D | Substrate-shape map audit (paired Step-2) | Same-vendor adversarial-auditor | **xhigh** (paired-default per (V′.a); Logan-discretion to downgrade to single-vendor xhigh under documented cost-bandwidth constraint, with paired-discipline tradeoff explicit in DISPOSITION) | Per 2026-04-30 §5.3 audit-discipline-limits finding: paired discipline catches different categories of failure (vocabulary-import vs. integration-grammar-as-fact). Phase D under (V′.a) carries three coexisting risks: vocabulary-import (mapping vocabulary fresh + framing-inheritance-risk), integration-grammar-as-fact (mapping vocabulary could be treated as observed-fact at map-claim level), and methodology-question-shape-mismatch (the new failure mode (V′.a) addresses). Same-vendor independent stress catches: map drifting back into spike-shape claims; integration-grammar-as-fact at the map-claim level; "resolved enough" framings without evidence. **Audit lens MUST include "challenge intervention-surface-set choice" + "challenge methodology-fit-of-mapping" lens-questions explicitly** per 2026-04-30 §5.3 finding (audit-spec-itself at framing-inheritance risk). **Discretion note:** if Logan downgrades to single-vendor under cost-bandwidth constraint, the closure-pressure-pattern recurrence risk from 2026-04-30 §5.4 (effort-level alone insufficient to break the pattern; max + structured-external-pressure was the breaking condition) becomes a known live risk; DISPOSITION must record this tradeoff. |
| E | Mapping-coherence test audit (REVISED 2026-04-30 per (V′.a)) | Cross-vendor codex GPT-5.5 | **xhigh** | Theory-coherence check: does the four-axis map hold together as a coherent theory; are 12-property gaps surfaced; does C1/C2/C3 logic apply consistently; is burden-of-proof-on-exclusion preserved? Cross-cutting reasoning across the entire map. Decision-stake: load-bearing for Phase F gate. xhigh warranted. |
| E | Mapping-coherence test (paired Step-2) | Same-vendor adversarial-auditor | **xhigh** (paired-default per (V′.a); Logan-discretion to downgrade to single-vendor xhigh under documented cost-bandwidth constraint, with paired-discipline tradeoff explicit in DISPOSITION) | Same rationale as Phase D paired audit: closure-pressure-pattern recurrence risk + integration-grammar-as-fact risk at theory-construction stage. Stress-tests: "could the same evidence be marshaled into a different mapping shape?" + "is the map closure-pressure-resolved without evidence at any cell?". Same Discretion-note as Phase D row: downgrade preserves cost but reintroduces 2026-04-30 §5.4 closure-pressure-pattern-survives-single-vendor risk; DISPOSITION must record. |
| F | Extraction-readiness gate audit | Cross-vendor codex GPT-5.5 | **xhigh** | Hard gate. Criterion-3 internal-coherence test requires deep cross-cutting reasoning ("does the work have its own gravitational center?"). Negative-space-depth: deep ("what's NOT ready that might be load-bearing?"). xhigh warranted. |
| G | Extraction execution audit | Cross-vendor codex GPT-5.5 | **high** | Mechanical-coherence: orphan-reference check + missed-migration check + cross-reference integrity. Bounded scope. Deep reasoning not required. high suffices. xhigh would be over-engineered. |
| H | Post-extraction integration audit | Cross-vendor codex GPT-5.5 | **xhigh** | Cross-cutting: reasons across two repos simultaneously; coherence-of-integration; trail-of-references on both sides. Decision-stake: this is the last gate before the trajectory is complete. xhigh warranted for final-state verification. |

**Note on M1 strict-undersell at recommendation stage (per §0.6 failure-mode taxonomy):** Don't add paired discipline by default to every audit "for safety." That's M1 strict-undersell — applying the strongest discipline blanketly when specific failure-modes are single-vendor-detectable. Phase B is single-vendor (same-vendor) because register-leak is what's being detected; Phase G is single-vendor (cross-vendor) because mechanical-coherence is what's being detected. Use paired discipline at Phase A, Phase C, **Phase D, and Phase E (the latter two added under (V′.a))** because those carry both vocabulary-import risk (cross-vendor catches) AND integration-grammar-as-fact risk (same-vendor catches). The premise-bleed audit precedent established this; the 2026-04-30 audit-discipline-limits finding (§5.3) extended it to Phase D + E given the closure-pressure-pattern recurrence + audit-scope-itself-at-framing-inheritance-risk evidence under mapping-shape methodology.

**Adversarial-auditor-xhigh agent vs reasoning level note:** The `adversarial-auditor-xhigh` Claude agent has "xhigh" in its name as the *agent-type identifier*. The reasoning-level is set per-dispatch via Anthropic SDK reasoning-effort parameter or analogous. When this plan says "same-vendor adversarial-auditor at high level," it means: agent-type=adversarial-auditor-xhigh, reasoning-effort=high. The agent's adversarial-discipline-prior + role-priming hold; just the reasoning depth is bounded.

### §2.5 Audit-output-disposition pathway

**Per AUDIT-SPEC.md §8 disposition pathway (universal across all audits in this plan):**
1. Logan reviews findings (summary + Class C + sample of Class A/B for calibration; differential if paired).
2. Logan disposes one of:
   - **Commit-as-is.** Class A only or Logan reads Class B/C as not load-bearing.
   - **Commit-with-addendum.** Class B/C tractable as addendum; addendum drafted; commit follows.
   - **Revise-before-commit.** Class C affects load-bearing-claim shape; revision precedes commit.
3. Disposition recorded at appropriate DISPOSITION.md (audit-folder local).

---

## §3. Artifact map

### §3.1 Where artifacts land

| Phase | Artifact | Location | Lines (target) |
|---|---|---|---|
| A | This plan + audit + DISPOSITION | **Authoritative:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (in-repo, version-controlled). **Mirror:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` (runtime working draft; not committed; for `/loop` resume only). **Audit folder:** `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md` + `DISPOSITION.md` | 800-1300 (plan) + 200-500 (audit) + 100-200 (DISPOSITION) |
| B | Standing-context artifact + CLAUDE.md load-point | `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (per §0.7 Q3 Option (a)) + CLAUDE.md doctrine-load-point addition (~3 lines under "Doctrine load-points") + audit folder | 80-120 (artifact) + ~3 (CLAUDE.md) + 100-200 (audit) |
| C | Incubation-checkpoint | `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` + DECISION-SPACE.md updates + audit folder | 150-300 (checkpoint) + ~30 (DECISION-SPACE updates) + 200-400 (audit) |
| D | Substrate-shape map (REVISED 2026-04-30 per (V′.a)) | `.planning/gsd-2-uplift/wave-2/substrate-shape-map/SUBSTRATE-SHAPE-MAP.md` + `INTERIM-CORPUS-INTEGRATION.md` + `DISPOSITION.md` + audit folder. Interim corpus at `.planning/gsd-2-uplift/wave-2/decision-trace/` carried as historical evidence. | 600-1200 (map) + 150-300 (integration) + 80-150 (DISPOSITION) + 400-700 (paired audit folder) |
| D-aux | Methodology-mismatch finding artifact ((V′.a) Step 5 standalone) | `.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md` | 200-400 (artifact) |
| E | Mapping-coherence check (REVISED 2026-04-30 per (V′.a)) | `.planning/gsd-2-uplift/MAPPING-COHERENCE-CHECK.md` + audit folder | 100-200 (check) + 400-700 (paired audit folder) |
| F | Extraction-readiness | `.planning/gsd-2-uplift/EXTRACTION-READINESS.md` + audit folder | 100-200 (readiness) + 200-400 (audit) |
| G | Extraction execution | New repo (location Logan-disposed) + `.planning/gsd-2-uplift/EXTRACTION-LOG.md` (arxiv-sanity-mcp side) + pointer artifacts at moved-from paths + audit folder | 150-300 (EXTRACTION-LOG) + ~10 lines per pointer artifact + TBD (depends on artifact set being moved) |
| H | Post-extraction integration | EXTRACTION-LOG.md updates with Phase H verification + final cross-repo commit identities + new repo corrections + audit folder | TBD |

### §3.2 Naming conventions

- **Audit folders:** `.planning/gsd-2-uplift/audits/YYYY-MM-DD-${descriptive-name}/` (per existing premise-bleed audit pattern).
- **Audit artifacts within folder:** AUDIT-SPEC.md / FINDINGS.md / FINDINGS-STEP2.md (if paired) / DIFFERENTIAL.md (if paired) / DISPOSITION.md.
- **Per-phase outputs:** `${phase-name-or-purpose}.md` (e.g., INCUBATION-CHECKPOINT.md, STABILITY-CHECK.md, EXTRACTION-READINESS.md, EXTRACTION-LOG.md).
- **Wave-2 outputs:** `.planning/gsd-2-uplift/wave-2/${slice-or-target-name}/` (per W1 pattern).
- **Trajectory plan:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (in-repo; this directory established by Phase A revise-before-execute disposition).

### §3.3 Cross-reference discipline

**Every artifact references:**
- Upstream artifact(s) it consumes (FROM).
- Downstream artifact(s) it feeds (TO).
- Decisions it implements (DECISION-SPACE.md §X.Y).
- Methodology it applies (METHODOLOGY.md / spike METHODOLOGY / etc.).
- Audit folder if applicable.

**Every load-bearing decision is traceable forward and backward.** This is what makes "responsibility traceable backward" possible (Logan's stated requirement).

---

## §4. Commit map

### §4.1 Commit grouping rules

**Atomic per logical unit:**
- One commit per phase output (with its audit) OR per coordination update (multi-phase coordination batched).
- Audit folders commit with their findings (per existing pattern).
- DECISION-SPACE.md updates commit with the decision they implement (per existing §1.17 pattern).
- STATE.md + OVERVIEW.md coordination updates commit together (per existing pattern).

**Suggested commit groups per phase (subject to working-tree state):**

| Phase | Suggested commit groups |
|---|---|
| A | (1) In-repo plan landing (`.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`) + plan-audit folder (PLAN-AUDIT.md + DISPOSITION.md). (2) Coordination updates (STATE.md + OVERVIEW.md). |
| B | (1) Standing-context artifact + CLAUDE.md load-point + audit. |
| C | (1) Incubation-checkpoint + audit folder. (2) DECISION-SPACE.md updates + INITIATIVE.md updates if shifts. (3) Coordination updates. |
| D | (1) Substrate-shape map (SUBSTRATE-SHAPE-MAP.md + INTERIM-CORPUS-INTEGRATION.md). (2) Substrate-shape map paired audit folder + DISPOSITION. (3) METHODOLOGY-MISMATCH-FINDING.md artifact ((V′.a) Step 5; may commit alongside (1) or as separate logical unit per Logan-discretion). (4) Coordination updates (STATE.md + OVERVIEW.md). |
| E | (1) Mapping-coherence check + paired audit folder + DISPOSITION. (2) Coordination updates. |
| F | (1) Extraction-readiness + audit + Logan disposition. |
| G | (1) Extraction-execution arxiv-sanity-mcp side: pointer artifacts at moved-from paths + EXTRACTION-LOG.md + trail-of-references. (2) Extraction-execution new repo side: initial population. (3) Cross-repo commit-identity follow-up commits per §4.2.1. |
| H | (1) Post-extraction integration audit + corrections (both sides) + EXTRACTION-LOG.md final-state update. |

### §4.2 Commit message conventions

**Per existing project pattern:**
```
docs(gsd-2-uplift): ${concise-description}

${body — what changed, why this matters, references to upstream/downstream}
```

For audit commits:
```
docs(gsd-2-uplift): ${audit-name} — ${headline-result}

${body — auditor + class breakdown + key findings + disposition pointer}
```

### §4.2.1 Cross-repo commit-identity rules (Phase G + Phase H)

**Per F8 disposition.** Extraction creates two git histories. Backward responsibility tracing requires cross-repo identity at every commit involved in the extraction. Rules:

1. **EXTRACTION-LOG.md MUST include**, at every revision (Phase G initial + Phase H final-state):
   - Source repo (arxiv-sanity-mcp) commit hash that the extraction was triggered from (the commit that produced the moved-from state).
   - Target repo (new repo) initial commit hash (the new repo's first commit containing the migrated artifacts).
   - Path-by-path move/stay/duplicate/reference disposition table (one row per artifact in the §1.7 artifact-by-artifact table) with old path + new path + disposition + per-disposition reasoning.
   - Final post-Phase-H commit hashes on both sides after corrections.
2. **Both sides' commit bodies MUST reference the paired commit hash from the other repo.** Where the paired hash is not yet known at primary-commit time (e.g., new-repo initial commit is created after arxiv-sanity-mcp side is committed), a follow-up commit MUST be added to record the paired hash. Pattern for follow-up:
   ```
   docs(gsd-2-uplift): record paired new-repo initial commit hash in EXTRACTION-LOG.md

   New repo's initial commit: <hash>. Cross-repo identity now complete; backward
   responsibility tracing intact across the extraction boundary.
   ```
3. **EXTRACTION-LOG.md serves as the cross-repo integrity ledger.** Phase H verification reads it to confirm both sides have paired hashes recorded; if any commit lacks its paired-hash, Phase H gate fails until follow-up commits land.

### §4.3 Working-tree-cleanliness checkpoints

**Mandatory clean-tree checkpoints:**
- Before Phase A starts (already clean post-current-arc).
- After each phase output commit (verify `git status` clean before proceeding).
- Before Phase G extraction execution (clean tree on both sides — for new repo, "clean tree" means uninitialized-or-fresh-init-commit-only state).
- After Phase H final integration commit.

If working tree dirty at a checkpoint, investigate (uncommitted plan revision; missed disposition update; etc.) and resolve before proceeding.

---

## §5. Failure-mode handling

### §5.1 If a gate doesn't pass

**Per-gate failure pattern:**
1. Identify which gate criterion failed (specific, evidence-grounded).
2. Identify which phase produced the failing artifact.
3. Loop back to that phase OR earlier phase if the failure traces upstream.
4. Record the loop-back trigger explicitly (in audit DISPOSITION.md and in coordination layer).
5. Re-execute affected phases.
6. Re-fire gate.

**Do not bypass gates with Logan-discretion** (except where explicit Logan-discretion is named in the gate-criteria — e.g., Phase F criterion 5 "no outstanding load-bearing-decisions block extraction" is Logan-disposed; criterion 3 internal-coherence is audit-disposed).

### §5.2 If new framing-bleed surfaces mid-execution

**Pattern:** A later-phase audit catches framing-bleed that earlier-phase audits missed. Treat as a revealed-residual, not as audit-failure.

1. Apply premise-bleed audit-arc pattern (similar to what we just did): cross-vendor + same-vendor-independent + differential + Logan-disposition.
2. Fix at point-of-bleed (likely an earlier phase artifact).
3. Re-run downstream phases as needed.
4. Update §0.6 failure-mode taxonomy if a new kind of erring is discovered.

### §5.3 If scope creep emerges

**Pattern:** A phase's execution starts producing work outside its scope.

1. Stop. Name the out-of-scope work explicitly.
2. Decide: is this valid work that should be its own phase, or is this distraction?
3. If valid: spawn a separate phase (or add to `framing-widening §9` deferred items log).
4. If distraction: drop and continue current phase scope.
5. Record the scope-creep-trigger and disposition.

### §5.4 If a phase produces unexpected new questions (productive curiosity)

**Pattern:** This is *not* failure. Spike-intensive work generates new questions that wasn't visible at design time. Per traces-over-erasure discipline (§0.5), preserve the question rather than silently dropping it.

1. Record the new question in `framing-widening §9` deferred items log (or analogous).
2. Decide: does answering this question affect current phase scope?
   - If yes: pause current phase, spawn investigation, return.
   - If no: defer to appropriate later phase or post-extraction work.
3. Do not pretend the question wasn't raised. Do not silently drop.

### §5.5 If Logan-discretion is required

**Pattern:** Some decisions are explicitly Logan-disposed (per §0.7 + per-phase Logan-disposition markers).

1. Surface the decision with all relevant evidence + non-binding-disposition-signal (per AUDIT-SPEC.md §6.1 §5 pattern: per-option reasoning).
2. Pause for Logan disposition.
3. Record disposition verbatim.
4. Continue.

If Logan unavailable mid-phase and the decision is truly Logan-disposed (not Claude-disposable), pause and record state for resumption (handoff pattern).

### §5.6 Failure-mode control matrix (per F4 disposition)

Maps each §0.6 failure-mode kind to: **phase(s) where it applies**, **concrete check** (where in the trajectory the check fires), **artifact where disposition is recorded**, and **owner** (Logan / auditor / executor) of the call.

| §0.6 failure mode | Phase(s) where applies | Concrete check | Recorded at | Owner |
|---|---|---|---|---|
| **Framing error** | A (plan framing); C (incubation framing); **D (mapping-target shape per (V′.a)); E (mapping-coherence theory shape per (V′.a))**; F (readiness framing) | Cross-vendor xhigh audit fires by default at A/C/D/E/F; **paired discipline (cross-vendor + same-vendor independent) default-fires at D and E per §2.4 + §2.3**; **frame-revision-check ((V′.a) Step 4) fires at phase entry / mid-phase / phase output draft per §6.1**; negative-space lens-question explicit in audit spec | Phase audit FINDINGS.md + DISPOSITION.md | auditor + Logan (disposes) |
| **Premise-bleed** | A; B; C; **D + E (under (V′.a))**; G (extraction prose carrying inheritance); H | Same-vendor adversarial-auditor (B default; A/C Logan-discretion paired; **D/E paired-default per (V′.a)**; G/H if Class C trigger from cross-vendor) | Phase audit FINDINGS-STEP2.md + DISPOSITION.md | auditor + Logan |
| **Closure-pressure** | All phases (recurrent — pattern-recurrence per 2026-04-30 §5.1 + 2026-05-01 turn-cluster recurrence) | Per-phase pre-commit check: "is any 'resolved enough' framing in this phase's output unresolved-by-evidence?"; explicit name-the-uncertainty discipline; `framing-widening §9` deferred-items addition for genuinely open items; **frame-revision-check at phase entry / mid-phase / phase output draft per (V′.a) Step 4 + §6.1** | Phase output (artifact body) + (if resolved-too-early) audit DISPOSITION.md re-open trigger | executor (in-phase) + auditor (post-phase) + Logan (final) |
| **Scope creep** | All phases — under (V′.a) particularly visible at Phase D where the mapping target shape itself is the scope (drift between sketches-of-intervention-intents vs. mapping-target-as-evidence-collection vs. operating-on-substrate is the scope-creep risk) | Per-phase pre-commit scope check (per §6.2 verification list); §5.3 handling pattern; **at Phase D under (V′.a): scope-pressure-watch for offshoot-pattern triggers (per EXTERNAL-VISION-CONTEXT.md §7.5) — when out-of-scope vision-content surfaces, carve to vision-repo rather than expand mapping scope** | Phase output (scope-statement section) + coordination layer (STATE.md note if creep landed) | executor (in-phase) + Logan (final disposition if creep is valid) |
| **Methodology-question-shape mismatch (added 2026-04-30 per (V′.a))** | All phases (recurrent risk; the load-bearing finding from 2026-04-30 §3.5) | Phase entry frame-revision-check asks: "is the methodology applied to this phase still right for the question-shape we're answering, or has the question-shape shifted?" Per-phase audit-spec includes explicit lens-question: "is the artifact under audit still the right shape for the question being answered?" Plan-self-audit at trajectory-plan revisions scoped explicitly to question-shape-fit | Phase output (frame-revision-check record) + audit FINDINGS.md (Class A/B/C as appropriate) | executor (raises) + auditor (surfaces) + Logan (disposes if methodology-shift warranted) |
| **Comparative-claims-without-comparative-data** | C (axis dispositions making cross-option comparisons); D (first-target findings); E (stability comparing Phase D evidence to Phase C disposition) | Per-claim evidence check (per audit lens); reject claims unsupported by comparative measurement; audit asks "what's the comparative data?" | Phase audit FINDINGS.md (Class B/C if claim unsupported) | auditor (surfaces) + Logan (disposes) |
| **False-confidence calibration** | A (plan claims); C (disposition claims); D (findings claims); F (gate claims); H (integration claims) | Per-finding confidence calibration check in audit spec; downgrade where evidence-load doesn't justify | Phase audit FINDINGS.md (Class A/B for over-confidence) + plan/output revision if Class C | auditor + Logan |
| **Comfort-language** | All phases producing prose (artifact bodies) | Active-voice + explicit-disposition discipline at decision artifacts; auditor lens explicitly checks "is any disposition softened to look optional that's actually load-bearing?" | Phase output + audit FINDINGS.md (Class A/B) | executor (in-phase) + auditor (post-phase) |
| **Performative-vs-operational openness** | A (claimed plurality in plan); C (axis dispositions naming options); F (criterion-4 trigger options) | Per-option evidence check: if option is unworkable, explicitly mark unworkable; if option is live, retain operationally | Phase output + audit FINDINGS.md | auditor + Logan |
| **Integration-grammar-as-fact** | A; C; G (cited frame language in extraction prose); H (integration prose) | §7.1 reading-frame application at point-of-use; "inputs not facts" framing; same-vendor adversarial-auditor catches at meta-level (premise-bleed audit precedent) | Phase audit FINDINGS-STEP2.md (same-vendor) + addendum-foregrounding if Class B/C | auditor (same-vendor) + Logan |
| **Skill-heuristic shallow-match** | All phases (especially when Claude reaches for prior-pattern templates) | Explicit context-comparison check: "what's the same as prior pattern; what's different"; per-phase pre-commit when reusing a pattern | Phase output (in body, when shallow-match risk is named) + audit if missed | executor (in-phase) + auditor (post-phase) |
| **Strict-M1 undersell at recommendation stage** | Audit recommendation stage (any phase with audit) | Recommendation calibration per SYNTHESIS-COMPARISON.md §4.1 (asymmetry empirically more complex); auditor's "non-binding disposition signal" must avoid blanket-paired or blanket-single-vendor reasoning | Audit FINDINGS.md non-binding disposition signal (§5 of audit) | auditor (calibrates) + Logan (disposes per §2.5) |
| **Execution error** | All phases (mechanics) | Pre-execution verification (per §6.1); post-execution verification (per §6.2); working-tree clean checkpoints (§4.3) | STATE.md / coordination layer if error landed; revert if needed | executor (catches) + Logan (escalation if non-recoverable) |
| **In-session-collaboration risk** | All phases where Claude drafts artifacts in-session with Logan | D5a caveat application: cross-vendor independent reads at load-bearing artifacts (A/C/E/F/H default cross-vendor audits); explicit Logan-adjudication at load-bearing decisions; addendum-foregrounding (per §7.1 pattern) where revision is heavier than warranted | Audit FINDINGS.md + plan/output revision or addendum + DISPOSITION.md | auditor (surfaces) + Logan (final disposition) |

---

## §6. Verification

### §6.1 Pre-execution verification

Before any phase begins:
- [ ] §0.4 mandatory pre-reading complete (fresh-context Claude must verify by re-reading and confirming internal model — including (f) mapping-vs-spike methodology distinction + (g) substrate-vision 12-property + four-category scope-confidence model per (V′.a) revisions).
- [ ] §0.5 discipline reminders internalized (including frame-revision-check (V′.a) Step 4 mechanism).
- [ ] §0.6 failure-mode taxonomy understood (including methodology-question-shape mismatch row); §5.6 control matrix reviewed for the upcoming phase.
- [ ] §0.7 Logan-disposed parameters acknowledged (including Q6 (V′.a) trajectory-replan disposition).
- [ ] §0.8 methodology-fit acknowledgment understood — particularly mapping-vs-spike question-shape distinction.
- [ ] Working tree clean.
- [ ] Current STATE.md reflects the actual state (no unsynced changes).
- [ ] **Phase-entry frame-revision-check fired:** "Is the question this phase exists to answer still right? Has question-shape shifted since prior phase? Is methodology applied to this phase still right for the question-shape?" Recorded in phase-output's frame-revision-check section.

### §6.2 Per-phase verification

Each phase verifies:
- [ ] Phase inputs are current (not stale; no upstream phase has shifted ground since this phase started).
- [ ] Phase scope is preserved (no scope creep per §5.3; offshoot-pattern triggers checked per §5.6 scope-creep row).
- [ ] **Mid-phase frame-revision-check fired** (if observations diverge from priors, or after within-mapping observations that surface accommodation the original scope didn't predict). Recorded.
- [ ] **Phase-output-draft frame-revision-check fired before commit:** "Has artifact drifted from question-shape it was authored to answer? Have new frame-revision questions surfaced during construction that warrant pause rather than commit?" Recorded.
- [ ] Phase quality gate fired and disposed.
- [ ] Phase outputs land at correct location per §3.1.
- [ ] Phase commits are atomic and traceable per §4.1.
- [ ] Working tree clean post-commit.
- [ ] Coordination layer (STATE.md + OVERVIEW.md) updated.
- [ ] Cross-references (§3.3) populated forward and backward.
- [ ] §5.6 failure-mode checks applicable to this phase have fired and been disposed.

### §6.3 Final-state verification (extraction completeness)

Post-extraction (Phase H complete):
- [ ] New repo internal coherence holds with intact references-back to arxiv-sanity-mcp (fresh-context test §1.8 process step 1; "yes" means coherent-with-references-back, NOT independent).
- [ ] arxiv-sanity-mcp trail-of-references holds (fresh-context test §1.8 process step 2).
- [ ] No orphan references on either side; explicit references-back are traceable and resolve correctly.
- [ ] Both repos have own STATE.md / equivalent reflecting post-extraction state.
- [ ] EXTRACTION-LOG.md complete and committed; cross-repo commit identities recorded per §4.2.1 (source commit + target initial commit + final-state both-side commits + path-by-path disposition table).
- [ ] All audit folders preserved (in whichever repo they belong per §1.7 artifact-by-artifact table).
- [ ] Pointer artifacts at moved-from paths in arxiv-sanity-mcp resolve to new-repo locations.

---

## §7. References + standing context

**Plan file (authoritative, in-repo):** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (committed; execution authority for fresh-session resume).

**Plan file (runtime working-draft mirror):** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` (not committed; useful for `/loop` resume convenience but execution must treat the in-repo copy as authority).

**Standing context (read in §0.4 order):**
- arxiv-sanity-mcp/CLAUDE.md
- arxiv-sanity-mcp/AGENTS.md
- arxiv-sanity-mcp/.planning/LONG-ARC.md
- .planning/gsd-2-uplift/INITIATIVE.md
- .planning/gsd-2-uplift/DECISION-SPACE.md
- .planning/deliberations/2026-04-28-framing-widening.md
- .planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md
- .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/ (full folder)
- .planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/ (this plan's own audit-arc; Phase A)
- .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md
- .planning/spikes/METHODOLOGY.md
- .planning/foundation-audit/METHODOLOGY.md
- .planning/STATE.md (current state-of-play)
- .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (Phase B output; test-case-vs-substrate framing)
- **`.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md`** (substrate-vision standing context; 12 properties + scope-discipline + Phase D mapping purpose; 2026-05-01 turn-cluster output)
- **`.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md`** (methodology-mismatch finding + (V′.a) disposition)
- `.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md` (forthcoming per (V′.a) Step 5)
- `.planning/gsd-2-uplift/audits/2026-04-30-phase-d-entry-audit/` ((V′.a) predecessor audit; the audit that fired Phase D entry but did not surface the methodology-mismatch — load-bearing as 2026-04-30 §5.3 evidence about audit-discipline limits)

**Methodology grounding:**
- `.planning/spikes/METHODOLOGY.md` M1 paired-review property (with empirical-complexity refinement per SYNTHESIS-COMPARISON.md §4.1).
- `.planning/LONG-ARC.md` anti-patterns (closure-pressure; framing-leakage).
- framing-widening §3.3 disposition-discipline.
- DECISION-SPACE.md §1.17 7-rule audit methodology.
- AUDIT-SPEC.md §6.1 audit-output structure (universal across audits in this plan).
- AUDIT-SPEC.md §8 disposition pathway (universal).

**Memory references (optional provenance pointers, NOT load-bearing for execution per §0.5 self-containment note):**

These are runtime-personalization artifacts that may not be available in a fresh session. Execution does not depend on reading them. They appear here only for traceability of where the §0.5 discipline summaries originated:

- feedback_epistemic_rigor.md
- feedback_ask_before_modifying_external.md
- feedback_methodology_and_philosophy.md
- feedback_spike_process.md
- feedback_no_explore_for_audits.md
- reference_spike_design.md

**Predecessor handoffs (for session-bridging if context loss):**
- 2026-04-28-post-W2-and-paired-synthesis-handoff.md (most recent uplift handoff).
- (Future: a handoff written at end of this plan's execution could capture extraction-state if needed.)

---

*Plan v1 drafted 2026-04-29 by Claude (Opus 4.7), main thread, in-session-collaboration with Logan. Revised 2026-04-29 post-Phase-A-audit per revise-before-execute disposition (F1-F9 applied; see audit folder DISPOSITION.md for per-finding revision trace). **Revised again 2026-05-01 per (V′.a) Step 2 — methodology-fit response to 2026-04-30 methodology-question-shape-mismatch finding** (per `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` §2.5-§2.6; (V′.a) Logan-disposed at /effort xhigh 2026-04-30): spike-shape Phase D replaced with mapping-shape Phase D; Phase E reshaped to test mapping-coherence; Phase F gate adjusted to mapping-coherence + intent-intervention-feasibility; §0.4 expanded with EXTERNAL-VISION-CONTEXT.md + 2026-04-30 deliberation + RELATIONSHIP-TO-PARENT.md + METHODOLOGY-MISMATCH-FINDING.md (forthcoming) + 2026-04-30 audit folder; §0.8 added (methodology-fit acknowledgment); §0.5 + §6.1 + §6.2 + §5.6 updated for frame-revision-check ((V′.a) Step 4 mechanism) + methodology-question-shape-mismatch failure mode; §2.1 + §2.3 + §2.4 + §3.1 + §4.1 + §1.7 updated for mapping-shape Phase D + E + (V′.a) Step 5 outputs + paired audit defaults at D and E. **Step 2 self-review revisions applied 2026-05-01** (Logan-disposed after Step 2 surfaced 7 concerns; recommendations 2-5 applied; recommendations 1 + 7 are Logan-side actions for Step 3 dispatch; recommendation 6 is no-op): §1.7 METHODOLOGY-MISMATCH-FINDING.md changed MOVE→DUPLICATE (self-correction from Step 2 premature commitment) + 2026-04-30 deliberation added to per-deliberation-Logan-disposed list; §2.3 + §2.4 paired-default-fires at D and E softened to paired-default-with-Logan-discretion-to-downgrade-under-cost-bandwidth-constraint; §1.4 step 6 + 7 + Outputs got iteration-mechanics gesture + budget-deviation-as-frame-revision-trigger; plan-status header notes Step 3 audit-spec drafting form (cross-vendor codex independent draft recommended) per Concern 1 disposition. Subject to same fallibility caveat as DECISION-SPACE.md §0 + EXTERNAL-VISION-CONTEXT.md §0. The in-session-collaboration risk applies to this revision (and to the self-review-revisions) as it does to all artifacts in this conversation arc; the (V′.a) Step 3 plan-self-audit-2 (scoped to question-shape-fit per 2026-04-30 §4 step 3; audit-spec independence per Concern 1 disposition) is the structural mitigation against framing-inheritance in both. The closure-pressure-into-elaboration pattern recurred during the 2026-05-01 turn-cluster that produced EXTERNAL-VISION-CONTEXT.md (per §7.1 of that artifact); future-Claude executing this plan should treat the pattern as a live risk under (V′.a), not a resolved one. **The self-review process itself (concerns surfaced + recommendations applied) is at framing-inheritance risk** — surfacing concerns can be performatively-open without operationally-resolving (per §0.6 performative-vs-operational openness); Step 3 paired audit reads both the revision AND the self-review trace as artifacts at risk.*
