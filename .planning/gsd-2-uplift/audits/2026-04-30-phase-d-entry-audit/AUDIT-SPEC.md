---
type: audit-spec
date: 2026-04-30
status: dispatched
phase: D entry (trajectory plan)
artifact_under_audit: |
  Phase D entry corpus — read together as one unit:
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7.10 (negative-space survey)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md (5-candidate surfacing)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md (axis 1-4 dispositions + reasoning + sensitivity map)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md (H6/H7/M1/M3/M4)
  - .planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md (gate-3 amended per §7.9.3 (c) + §7.10 H4/H5/M5)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP4-gates-and-L-tier.md (gates 1+2+4 + L-tier sweep)
upstream_grounding:
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md (Step 0 P5 probe)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md (Step 0 M2 probe)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7 + §7.9 (Phase C dispositions + audit addendum that grounds §7.10)
  - .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (test-case-vs-substrate; H5 anchor)
  - .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md §1.4 + §2.4 row D (Phase D goal + audit shape)
audit_kind: paired (cross-vendor codex GPT-5.5 + same-vendor adversarial-auditor-xhigh independent stress) per trajectory plan §2.4 row D + premise-bleed precedent + Phase C precedent
reasoning_level: |
  Same-vendor: xhigh (Opus 4.7 adversarial-auditor-xhigh; completed attempt-1 in 7 min producing 3A/3B/1C addendum-shape).
  Cross-vendor: high (gpt-5.5 high). RECALIBRATED 2026-04-30 from xhigh per Logan's calibration (codex high ≈ Opus 4.7 xhigh capability; codex xhigh is expensive markup with diminishing returns vs high). Original xhigh choice followed AUDIT-SPEC template precedent + trajectory plan §2.4 row D wording verbatim — itself a precedent-following failure mode the audit lenses were supposed to catch. Re-dispatch parameters recorded at POST-MORTEM.md §7. Trajectory plan §2.4 row D amendment deferred to post-Phase-D evidence consideration.
dispatch_history:
  - attempt-1 (2026-04-30 03:35-04:14): cross-vendor codex hung on stdin read; never API-called; 37 min wallclock; $0 cost; clean kill. Same-vendor B unaffected, completed normally at 03:41. Root cause + fix recorded at POST-MORTEM.md.
  - attempt-2 (2026-04-30 04:15+): cross-vendor codex re-dispatched at gpt-5.5 high with </dev/null stdin closure.
m1_paired_review_rationale: paired per premise-bleed precedent + Phase C precedent — cross-vendor catches vocabulary-import / substantive divergence; same-vendor catches integration-grammar-as-fact / methodological-discipline-leak. The corpus is co-produced (Claude+Logan in-session); both vendor positions are needed
---

# AUDIT-SPEC.md — Phase D Entry Audit

## §0. Purpose

Phase D entry of the trajectory plan (`.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`) executes a 6-step work-flow per INCUBATION-CHECKPOINT.md §7.10.4 (Step 0 P5 + M2 probes → Step 1 design-space framing → Step 2 practical decisions → Step 3 mini-spec drafting → Step 4 gates + L-tier sweep → Step 5 audit → Step 6 Logan green-light + Phase D dispatch). This audit is Step 5 — paired structural correction for the corpus that emerged from Steps 0-4 before Phase D first-target work begins.

**Why this audit exists.** Phase D entry corpus is co-produced (Claude+Logan in-session-collaboration with /effort max + /effort xhigh effort levels). Per plan §0.5 D5a in-session-collaboration discipline + §7.10.6 D5a recursion acknowledgment: the corpus inherits Logan-framing inheritance. Same-vendor xhigh adversarial-auditor + cross-vendor codex GPT-5.5 xhigh paired discipline is the structural correction. The audit pressure-tests the corpus before Phase D first-target dispatch.

**Why paired.** Per premise-bleed audit precedent (DECISION-SPACE.md §1.17 lessons-distilled) + Phase C precedent: paired vendor produces complementary findings rather than redundant ones. Cross-vendor catches vocabulary-import / substantive divergence at design-shape; same-vendor catches integration-grammar-as-fact at meta-level (the §7.1 reading-frame residual recurring at design-framing stage; per §7.10.6 + §7.10.0 D5a recursion).

**Why xhigh both.** Per trajectory plan §2.4 row D design-shape:
- Framing-load: highest — first-target design-shape (E primary + A comparator) is the load-bearing decision Phase D acts on; affects Phase E + Phase F + Phase G inheritance.
- Cross-cutting reasoning: integrates 6 artifacts (§7.10 + STEP1-design-space + STEP1-DISPOSITION + STEP2 + MINI-SPEC + STEP4) plus 4 upstream grounding artifacts.
- Decision-stake: Phase D dispatch begins after this audit + Logan green-light; first-target work consumes M1 8-day budget.
- Negative-space depth: what is the corpus excluding from consideration?

## §1. Lens for the audit

**Primary lens — design-framing-quality challenge.** The audit's job is to challenge the design framing, not echo it. Design-framing-quality failures would look like:

- Candidate set incomplete (a 6th candidate exists beyond A/D/E/F/G that should have been surfaced; STEP1-design-space.md §4.5 #2 acknowledges sampling bound but doesn't claim completeness).
- R-strategy tagging miscoded (STEP1-design-space.md §4.5 #3 acknowledges M2-derived tagging may not survive audit-shaped re-read).
- "More control + open-source" reframing over-shifts weight at axis 1 (E vs A primary; STEP1-DISPOSITION.md §5 #1 + STEP1-design-space.md §4.5 #4 acknowledge this risk).
- Stack D foreclosure pattern misapplied recursively at Phase D scoping (the argument used to justify rejecting D in favor of E is itself Claude-imported; auditor reads whether it's principled or rationalizing the chosen path).
- E-vs-D weighing under-counts schema-versioning evidence yield (STEP1-DISPOSITION.md §5 #2 acknowledges this; auditor verifies if the under-count is recoverable or load-bearing).
- Reversibility argument over-weighted to justify F + G OOS confirmations (STEP1-DISPOSITION.md §5 #4 acknowledges; auditor checks if OOS is principled or convenience).

**Secondary lens — D5a in-session-collaboration leak detection.** The corpus is Claude-drafted with Logan-disposition. D5a leaks would look like:

- Substrate-shape projection from test-case-anchoring without explicit framing-discipline (RELATIONSHIP-TO-PARENT.md → MINI-SPEC.md inheritance; H5 channel separation drafted but discipline-shape, not built-in mechanism per MINI-SPEC §9 #4).
- Conservative-default-when-uncertain in axis 4 (F + G OOS-this-arc default; auditor verifies if (i) reversibility-grounded as STEP1-DISPOSITION claims OR (ii) default-conservative).
- /effort max → /effort xhigh sequence preserved as accept-conditions but functioning as accept-shape-laundering (Logan accept under /effort xhigh inherits framing surfaced at /effort max; auditor verifies the trail-as-recorded actually represents independent disposition vs framing-acceptance).
- §7.10 H/M/L tier framing imported from Claude organizing-structure (per §7.10.0 + §7.10.6 acknowledgments); auditor verifies tier-claims function as organizing-frame, not as observed taxonomy at meta-level.

**Tertiary lens — framing-leak detection (§7.1 reading-frame residual at design-framing stage).** The corpus cites R1-R5 / six-context / four-act / A+F-primary-anchoring vocabulary; framing-leak would look like:

- Treating R1-R5 as observed-fact about gsd-2 design-space rather than as inputs (the §7.1 residual that premise-bleed audit caught at synthesis stage; now potentially recurring at design-framing stage at MINI-SPEC §1.E + §1.A R-strategy claims).
- Treating "more control + open-source" reframing as observed-property of gsd-2 substrate rather than as Logan-imported organizing logic (STEP1-DISPOSITION §5 #1 acknowledges; auditor verifies discipline holds in dispositions themselves).
- Frame-revision-none-active operating context treated as neutral when it might be active-non-revision (STEP4 §1.3 user-adoption probe deferral confirmed; auditor verifies confirmation is principled vs default-conservative).
- A+F-primary anchoring carried into MINI-SPEC §5 F-discipline-observability section as if A+F is observed-fact for gsd-2 substrate vs Logan-imported anchoring choice.

**Quaternary lens — evidence-load calibration.** Does the corpus carry evidence-load that supports its claims?

- §4 success criteria items 1-6 jointly-too-strict risk (MINI-SPEC §9 #2 acknowledges).
- §6 falsifiers 1-9 channel-overlap risk (MINI-SPEC §9 #3 acknowledges).
- §7 channel-separation discipline as declared rule vs built-in mechanism (MINI-SPEC §9 #4 acknowledges).
- §8 M5 inline-discipline practical sustainability (MINI-SPEC §9 #5 acknowledges).
- M1 8-day hard limit calibration without prior-base-rate (STEP2 §3 #2 acknowledges).
- M3 paired-mode-precedent generalization from premise-bleed + Phase C audit-arcs (STEP2 §3 #6 acknowledges).
- Test-task selection (framing-widening deliberation) D5a inheritance (MINI-SPEC §9 #6 acknowledges; risk: skill validates Logan-framing rather than independently reconstructing).

**Negative-space lens (required, per DECISION-SPACE.md §1.17 audit-methodology rule 2).** What is the corpus *excluding* from consideration? The corpus surfaces audit-priority risks at multiple layers (STEP1-design-space §4.5; STEP1-DISPOSITION §5; STEP2 §3; MINI-SPEC §9; STEP4 §4). Auditor identifies exclusions beyond those:

- Are there decision-trace-relevant gsd-2 surfaces M2 didn't sample (heal-skill / skill-health subsystem per M2 §8 #3; `unit-context-manifest.ts` Phase 2-4 status per M2 §8 #5; `gsd_progress` vs `headless query` state-coherence drift per P5 §7 #2)?
- Are there alternative test-task selections (synthetic; non-Claude-co-produced; cross-project) that would produce evidence with less D5a inheritance than framing-widening?
- Are there H4 falsifiers (besides 1-9) that would license "decision-trace at Phase D was misframed entirely" rather than re-disposition within E/A axis?
- Are there L-tier reminders (besides L1-L8) that the §7.10 survey itself missed?

## §2. Methodology

Per AUDIT-SPEC.md §6.1 universal audit-output structure (premise-bleed + Phase C precedent):

1. **Read the artifact-under-audit corpus** (6 artifacts listed in §3 below) in any order; cross-references between artifacts are explicit.
2. **Read the upstream-grounding** (P5 + M2 probes; INCUBATION-CHECKPOINT §7 + §7.9; RELATIONSHIP-TO-PARENT; trajectory plan §1.4 + §2.4 row D + §0.5 + §0.7).
3. **Apply the four lenses** (design-framing-quality / D5a leak / framing-leak / evidence-load) systematically across the corpus.
4. **Apply negative-space lens** at the corpus as a whole and at each sub-artifact.
5. **Calibrate confidence** per finding (high / medium / low) and class per finding (Class A: addendum-shape; Class B: revision-shape; Class C: re-architect-shape).
6. **Produce non-binding disposition signal** per finding + overall.

**Independent mode (both auditors).** Per AUDIT-SPEC.md §3.4 manual-discretion pattern: each auditor reads ONLY the artifacts in §3 below. Do NOT read each other's findings before completing own audit; this preserves independence-of-finding and avoids cross-auditor-anchoring. Do NOT read prior audit folders (premise-bleed; trajectory-plan; relationship-to-parent; incubation-checkpoint) before completing own audit (reserve for differential or post-hoc verification).

**Cross-vendor + same-vendor as paired Step-1 + Step-2 (parallel, not sequential).** Per premise-bleed audit's lessons-distilled (DECISION-SPACE.md §1.17): paired Step-1 + Step-2 produces complementary findings, not redundant. This audit invokes both as Step-1 and Step-2 in parallel (independent dispatch); main-thread differential analysis post-hoc reconciles per premise-bleed precedent.

## §3. Inputs (required reading; sequenced)

1. **The corpus under audit (read in any order; cross-references explicit):**
   - `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.10 — negative-space survey (H1-H7, M1-M5, L1-L8, §7.10.4 work-flow, §7.10.5 checklist, §7.10.6 audit-priority acknowledgments).
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md` — 5 candidate shapes (A/D/E/F/G) + R-strategy + gap-mapping + audit-priority risks.
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md` — axis 1-4 Logan-dispositions + Claude reasoning + sensitivity map + acknowledged audit-priority risks.
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md` — H6/H7/M1/M3/M4 dispositions + per-decision reasoning.
   - `.planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md` — Phase D dispatch contract; gate-3 amended (§7.9.3 (c) + §7.10 H4/H5/M5).
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP4-gates-and-L-tier.md` — gates 1+2+4 dispositions + L-tier sweep + checklist completion.

2. **Upstream grounding (Step 0 evidence + standing context):**
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md` — gsd-2 effective-state emission gap; sub-option (ii) recommendation.
   - `.planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md` — gsd-2 skill subsystem snapshot; primitives inventory.
   - `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7 (Phase C dispositions per axis) + §7.9 (audit addendum that grounds §7.10).
   - `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (test-case-vs-substrate; H5 + M5 grounding).

3. **Trajectory plan governance:**
   - `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §1.4 (Phase D goal) + §2.4 row D (audit reasoning-level rationale) + §0.5 (disposition-discipline) + §0.6 (failure-mode taxonomy) + §0.7 (hybrid autonomy).

4. **Methodology grounding:**
   - `.planning/spikes/METHODOLOGY.md` (six interpretive lenses; paired-review practices; M1 paired-review property).
   - `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.17 (audit methodology) + §1.18 (Phase C dispositions).

**Optional reading (do NOT read in independent mode; reserve for differential or post-hoc verification only):**

- Premise-bleed audit folder (FINDINGS.md / FINDINGS-STEP2.md / DIFFERENTIAL.md / DISPOSITION.md).
- Trajectory-plan audit folder (PLAN-AUDIT.md / DISPOSITION.md).
- Incubation-checkpoint audit folder (audit-findings-A.md / audit-findings-B.md / DIFFERENTIAL.md / DISPOSITION.md / VERIFICATION.md).
- Relationship-to-parent audit folder (audit-findings-A.md / audit-findings-B.md / DISPOSITION.md / VERIFICATION.md).
- The other auditor's findings (when both auditors are dispatched in parallel; main-thread reads both for differential).

## §4. Output structure

Write findings to `audit-findings-A.md` (cross-vendor codex) + `audit-findings-B.md` (same-vendor adversarial-auditor) in this audit folder. Naming-convention rationale per Phase B precedent: `audit-findings*.md` bypasses Claude Code 2.1.123's `tengu_sub_nomdrep_q7k` regex.

**§0. Summary** — auditor identity + reasoning-level + class breakdown + headline + non-binding overall disposition signal.

**§1. Methodology applied** — what was read; what was excluded; mode (independent); time budget per artifact.

**§2. Findings** — per-finding entries with this structure:
  - **ID** (e.g., F-PD-A1 for cross-vendor codex; F-PD-B1 for same-vendor adversarial-auditor).
  - **Class** (A: addendum-shape / B: revision-shape / C: re-architect-shape).
  - **Confidence** (high / medium / low).
  - **Lens** (which of design-framing-quality / D5a leak / framing-leak / evidence-load / negative-space).
  - **Where** (which artifact(s) + which §).
  - **What** (the finding — what the audit observed).
  - **Why** (the reasoning chain).
  - **Suggested disposition** (non-binding signal — addendum / revision / re-architect / accept-as-is).

**§3. Negative-space catalogue** — what the corpus excludes from consideration that the audit identifies as load-bearing OR principally-excluded with justification.

**§4. Synthesis** — overall calibration: is the Phase D entry corpus dispatch-ready? what's the single biggest risk? what's the single strongest discipline-move that landed correctly?

**§5. Non-binding overall disposition signal** — one of:
- Accept-as-is (Class A only OR all Class B/C tractable as addendum without revision).
- Addendum-shape (Class B/C tractable but warrant explicit addendum at corpus or sub-artifact).
- Revise-before-dispatch (Class C affects design-framing shape; Phase D dispatch waits on revision).
- Re-architect (Class C affects work-flow shape; Step 1-4 work re-disposed before dispatch).

## §5. Time budget

- Cross-vendor codex GPT-5.5 xhigh: ~2-3 hours wall-clock (corpus is ~1500 lines + ~6000 lines of upstream grounding); reasoning-effort xhigh.
- Same-vendor adversarial-auditor-xhigh independent: ~2-3 hours wall-clock; xhigh effort.
- Main-thread differential analysis (post-audit): ~30 min.
- Logan disposition + Phase D dispatch decision: Logan-disposed after differential.

## §6. Cross-references

- AUDIT-SPEC.md universal §6.1 + §8 disposition pathway (per trajectory plan + DECISION-SPACE.md §1.17).
- Trajectory plan §2.4 row D (audit reasoning-level rationale).
- INCUBATION-CHECKPOINT.md §7.10.4 Step 5 (Phase D entry audit definition).
- Premise-bleed audit precedent (DECISION-SPACE.md §1.17 lessons-distilled).
- Phase C audit precedent (`.planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/`).

## §7. Disposition pathway (per AUDIT-SPEC.md §8 universal)

1. Logan reviews findings (summary + Class C + sample of Class A/B for calibration; differential).
2. Logan disposes one of:
   - **Accept-as-is.** Class A only OR Class B/C readable as not load-bearing for Phase D dispatch.
   - **Addendum-shape.** Class B/C tractable as addendum at corpus or sub-artifact; addendum drafted; Phase D dispatch follows.
   - **Revise-before-dispatch.** Class C affects design-framing shape; revision precedes Phase D dispatch.
   - **Re-architect.** Class C affects work-flow shape; Step 1-4 work re-disposed.
3. Disposition recorded at this audit folder's `DISPOSITION.md`.

---

*AUDIT-SPEC.md drafted by Claude (Opus 4.7, /effort xhigh) 2026-04-30 in-session-collaboration with Logan per trajectory plan §7.10.4 Step 5 + plan §2.4 row D paired audit shape. Independent mode + parallel dispatch per premise-bleed + Phase C precedent. Subject to same fallibility caveat as DECISION-SPACE.md §0; the audit IS the structural correction for the corpus's D5a inheritance.*
