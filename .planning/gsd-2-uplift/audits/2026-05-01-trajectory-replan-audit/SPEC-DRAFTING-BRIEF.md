---
type: audit-spec-drafting-brief
date: 2026-05-01
status: prepared for cross-vendor codex GPT-5.5 xhigh independent draft (B-strong per (V′.a) Step 2 self-review Concern 1)
purpose: |
  Brief for cross-vendor codex (GPT-5.5 xhigh) to draft an AUDIT-SPEC.md
  for the (V'.a) Step 3 plan-self-audit-2 — independent of Claude's
  framing-inheritance from Step 2 authoring + 2026-05-01 vision-articulation
  turn-cluster.
audience: cross-vendor codex GPT-5.5 xhigh; Logan disposes the audit-spec output before audit dispatch
artifact_under_audit:
  path: .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md
  commit: ffc0fb0
  lines: 842
output:
  path: .planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/AUDIT-SPEC.md
  structure: AUDIT-SPEC.md v2 precedent at .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md
  scope: question-shape-fit (mapping vs. spike) + framing-inheritance-risk + recursive-failure-mode catch
ground_rules:
  - You are drafting an audit-spec, NOT executing the audit. Output is AUDIT-SPEC.md.
  - You are independent of Claude's framing-inheritance from Step 2. The whole point of B-strong is that you draft the spec without Claude having scoped it.
  - You may disagree with the artifact-under-audit's framing. Surface where you would.
  - You may identify lens-questions Claude would not have included. Surface them.
  - You may identify lens-questions Claude included that should be reframed. Surface that.
---

# Audit-spec-drafting brief for (V′.a) Step 3 plan-self-audit-2

## §1. Why you (cross-vendor codex) are drafting this spec, not Claude

This brief implements **B-strong** from a self-review applied to (V′.a) Step 2 trajectory-plan revision (Logan-disposed 2026-05-01). The self-review surfaced **Concern 1**: the audit-spec for Step 3 is itself at framing-inheritance risk per the 2026-04-30 §5.3 audit-discipline-limits finding ("if the audit is scoped under the same misframe as the artifact, it may not surface the misframe"). Recursive failure-mode shape:

> Phase A's audit-spec was Claude-drafted; that audit fired correctly under its scope but didn't catch the methodology-question-shape-mismatch in the original Phase D framing — because the spec itself was scoped under the misframe. (V′.a) exists to address that mismatch. If Step 3's audit-spec is also Claude-drafted, the same recursive failure-mode signature is preserved.

Structural fix: independence at scope-level, not just at execution-level. Cross-vendor codex (you) drafts the spec without Claude having scoped it. Logan disposes your spec. Audit (cross-vendor + same-vendor paired) then fires under that spec.

**You may write a fundamentally different audit-spec than Claude would have written.** That's the point.

## §2. Artifact under audit

**Primary artifact:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` at commit `ffc0fb0` (842 lines).

**Self-review trace (also under audit; per Step 2 final caveat).** The same commit includes self-review revisions applied 2026-05-01 (concerns 2-5 applied; concerns 1+7 are Logan-side actions; concern 6 no-op). The self-review trace is in the plan's final caveat block + commit message body. **Audit must read self-review as performatively-open vs. operationally-resolved per §0.6 performative-vs-operational openness — surfacing concerns is not the same as resolving them; check whether the applied self-review revisions actually address the concerns or merely paper over them.**

## §3. Standing-context inputs (READ-FIRST; load-bearing)

Mandatory pre-reading for spec-drafting (in this order):

1. **`.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md`** — full read. The methodology-question-shape-mismatch finding + (V′.a) disposition + five frame-revisions + Logan-disposition discipline scope (§2.7) + calibration findings (§5: closure-pressure pattern recurrence + audit-discipline limits + max-effort + Logan-correction breaking condition).

2. **`.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md`** — full read. §1 corrected gsd-2-uplift project-shape (5-property); §2 pressure-not-destination relationship to harness-studio; §3 12 substrate-vision properties (the depth-spectrum the mapping-shape Phase D evaluates); §4 scope-discipline (burden-of-proof-on-exclusion + four-category C1/C2/C3/C4 model + identity-distortion narrowness); §5 Phase D mapping purpose; §7 meta-disciplines surfaced (closure-pressure recurrence in 2026-05-01 turn-cluster).

3. **`.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md`** — full read. Test-case-vs-substrate framing standing context (Phase B output). arxiv-sanity-mcp's diagnostic-loop role.

4. **The artifact under audit** — `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` at `ffc0fb0` — full read. Special attention to: §0.8 methodology-fit acknowledgment; §1.4 Phase D mapping-shape (process steps + inputs + outputs + quality gate); §1.5 Phase E mapping-coherence test; §1.6 Phase F gate criteria; §0.5 frame-revision-check mechanism; §0.6 + §5.6 methodology-question-shape-mismatch row; §2.4 paired audit-discipline at D + E + Step 3; §1.7 Phase G artifact-by-artifact table; final caveat self-review trace.

5. **Phase A audit precedent** — `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md` (~30KB; the precedent for what a previous trajectory-plan audit produced) + `DISPOSITION.md` (~19KB; how Logan disposed Phase A findings). **Read these for spec-shape precedent BUT note that Phase A audit didn't catch the methodology-question-shape-mismatch that prompted (V′.a) — so the spec-precedent is not the authority for what to look for; it's the precedent for the spec's structural shape.**

6. **AUDIT-SPEC.md v2 precedent** — `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` — for AUDIT-SPEC structural template (sections, classification scheme, output structure expectations, disposition pathway). Replicate this structure in your AUDIT-SPEC.md output.

7. **Cross-vendor codebase-understanding-audit's META-SYNTHESIS** — `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md` — primary grounding for "what gsd-2 actually is" (corrected frame vocabulary). This is the substrate Phase D maps.

8. **Methodology grounding** — `.planning/spikes/METHODOLOGY.md` (six interpretive lenses + paired-review M1; the methodology that was applied to a question-shape it didn't fit per 2026-04-30 §3.5) + `.planning/foundation-audit/METHODOLOGY.md` (decision-review epistemic discipline).

## §4. What the audit-spec MUST cover (high-confidence required lens-questions)

**These are non-exhaustive minimum-required lens-questions.** You MUST include them in your spec. You SHOULD identify additional lens-questions Claude would not have thought of. Mark your additions as such so Logan can disposition-track which questions are precedent-adjusted vs. cross-vendor-original.

### §4.1 Question-shape-fit (the lens (V'.a) demands)

- **(Q-SF-1) Is the trajectory-plan revision still spike-shape masquerading as mapping?** Specifically: does Phase D §1.4's process steps, despite being labeled mapping-shape, retain spike-converges-on-answer structure? E.g., does the four-axis structure produce a single-target-equivalent output despite the mapping label? Does §1.4 step 10's "Draft FINDINGS.md (the substrate-shape map) + DISPOSITION.md (Logan disposes)" treat mapping as resolvable-by-Logan-disposition rather than iterative-theory-construction?
- **(Q-SF-2) Is mapping itself the right question-shape?** Could there be a third question-shape (NOT spike, NOT mapping) the revision missed? Per 2026-04-30 §3.5 counter-claim: spike methodology can be scoped flexibly; what we need may be broader-scoped spikes, not different methodology. Or another option entirely. Surface alternative question-shapes if any.
- **(Q-SF-3) Does the §0.8 methodology-fit acknowledgment hold up under independent reading?** Specifically: does the spike-shape vs. mapping-shape dichotomy oversimplify the question-space? Are there hybrid shapes the dichotomy excludes?
- **(Q-SF-4) Does the four-axis structure (gsd-2 surfaces × arxiv-sanity-mcp practice × intervention-intents × joint accommodation-evidence) cover the evidence-territory adequately?** What's missing? Should there be a fifth axis? Should two axes collapse?

### §4.2 Framing-inheritance-risk catch (the recursive failure-mode)

- **(Q-FI-1) Does the revision treat its own framing-vocabulary as observed-fact rather than as inputs?** Per the §7.1 reading-frame from SYNTHESIS-COMPARISON.md: claims like "12 substrate-vision properties" or "C1/C2/C3/C4 model" are inputs Logan + Claude brought in via EXTERNAL-VISION-CONTEXT.md, not facts about gsd-2 or about the substrate. Where does the revision implicitly treat them as facts?
- **(Q-FI-2) Does the EXTERNAL-VISION-CONTEXT.md framing import (12 properties + scope-discipline) carry residuals that the revision inherits?** Specifically: closure-pressure recurred during the 2026-05-01 turn-cluster that produced EXTERNAL-VISION-CONTEXT.md (per §7.1 of that artifact); broke only on Logan-correction. The artifact may have residual framing-pressure even after correction. The revision uses §3 + §4 + §5 of EXTERNAL-VISION-CONTEXT.md as load-bearing inputs. What residuals propagate?
- **(Q-FI-3) Does the revision's self-review process operate-or-perform?** The plan's final caveat traces self-review revisions C2-C5 applied + C1 + C7 Logan-side + C6 no-op. Per §0.6 performative-vs-operational openness: did surfacing-the-concerns address the underlying risk, or did it produce comfort-language that obscures unresolved risk? Specifically: C4 self-corrects MOVE→DUPLICATE, but the underlying mechanism that produced premature-commit (structural-feel calls without sufficient evidence) is unaddressed.
- **(Q-FI-4) Does the closure-pressure-into-elaboration pattern (per 2026-04-30 §5.4) recur in the revision itself?** Specifically: where in the 842-line plan are "resolved enough to commit" framings unresolved-by-evidence? The pattern survives /effort max + pattern-recognition-active per 2026-04-30 §5.4 + 2026-05-01 §7.1.
- **(Q-FI-5) Does the in-session-collaboration risk (D5a) compound across (V′.a) Step 1 + Step 2 + 2026-05-01 vision-articulation + this self-review?** Each artifact in the chain inherits Logan-co-framing from prior artifacts. The chain compounds without independent breaks (Phase A audit was the prior independent break; nothing since 2026-04-29).

### §4.3 Methodology-question-shape-mismatch (the new failure-mode)

- **(Q-MM-1) Is the methodology-question-shape-mismatch finding correctly diagnosed?** Per 2026-04-30 §3.5 + (V′.a) disposition. Counter-claim challenged in §0.8 of the revision: "spike methodology can be scoped flexibly; what we need is broader-scoped spikes." Is the counter-counter response (which §0.8 commits to) sound? Or does it produce a methodology-shape that's neither spike nor mapping but something the revision hasn't articulated?
- **(Q-MM-2) Does the revision adequately specify HOW mapping iterates?** The §1.4 step 6 + 7 iteration-mechanics gesture is acknowledged as "one possible shape" with frame-revision-check at step 5 firing if iteration-shape shifts. Is this under-specification appropriate (mapping is theory-constructive; locking iteration shape is closure-pressure) or hidden closure-pressure (under-specification is performative-openness)?
- **(Q-MM-3) Does Phase E's mapping-coherence test specify what coherence MEANS at theory-construction stage?** §1.5 lists coherence dimensions (fresh-session re-read; cross-axis consistency; cross-vendor read; theory-construction-quality lenses) but doesn't specify how these compose into a coherent/partially-coherent/incoherent disposition.

### §4.4 Phase F gate criteria + Phase G dispositions

- **(Q-PF-1) Does Phase F criterion 2 (≥1 C1 path) operationalize correctly?** What if the substrate-shape map produces zero C1 paths (substrate genuinely doesn't accommodate any intervention at low risk)? §1.6 says "both are findings warranting Phase D re-execution or (V′.b) consideration, not extraction" but doesn't specify when Phase D re-execution is the right response vs. (V′.b).
- **(Q-PF-2) Does the criterion 5 "methodology-mismatch finding integrated" requirement risk being satisfied superficially?** I.e., a substrate-shape map could cite METHODOLOGY-MISMATCH-FINDING.md without operationally accounting for it.
- **(Q-PG-1) Phase G artifact-by-artifact table dispositions (METHODOLOGY-MISMATCH-FINDING.md DUPLICATE; 2026-04-30 deliberation Per-deliberation-Logan-disposed): are these the right dispositions?** Self-review caught METHODOLOGY-MISMATCH-FINDING.md MOVE→DUPLICATE; are there OTHER artifact-dispositions that are similarly under-considered?

### §4.5 Paired-audit-default-with-discretion at Phase D + E + Step 3

- **(Q-AD-1) Is paired-default-with-Logan-discretion-to-downgrade the right formulation?** Self-review C5 softened from hard-default; but the softening preserves an escape-valve that may undermine the discipline's purpose (per 2026-04-30 §5.4: closure-pressure-pattern-survives-single-vendor risk). Is the softening a legitimate cost-discipline tradeoff or M1-strict-undersell-adjacent (per §0.6)?
- **(Q-AD-2) Is the audit-spec for Step 3 (this spec you are drafting) being authored under conditions that itself might re-import the failure mode?** I.e., even codex-drafted spec inherits some Claude-context (this brief). Where does this brief constrain your spec-drafting in ways that import Claude framing-inheritance? Surface where you depart from the brief if the brief itself feels misframed.

### §4.6 Negative-space and meta-questions

- **(Q-NS-1) What does the revision exclude from consideration?** Negative-space lens question per §0.5 framing-as-load-bearing discipline. Is the exclusion principled or accidental?
- **(Q-NS-2) What does the revision NOT say but should say?** What's missing.
- **(Q-Meta-1) Is there a frame the revision is operating under that it doesn't acknowledge?** Some implicit framing the revision treats as natural-not-imported.

### §4.7 Disposition-shape (per AUDIT-SPEC.md v2 precedent)

Findings classification: A (ACCEPT-AS-STATED) / B (ADDENDUM-TRACTABLE) / C (REVISE-BEFORE-COMMIT). Apply to each finding.

Disposition pathway: per AUDIT-SPEC.md §8 universal. Logan disposes commit-as-is / commit-with-addendum / revise-before-commit per finding-class.

## §5. Audit execution form (NOT spec-drafting; this informs your spec)

After your spec is disposed by Logan, the actual audit will fire as:
- **Cross-vendor codex GPT-5.5 xhigh** Step-1 (you, executing your own spec)
- **Same-vendor adversarial-auditor xhigh** Step-2 independent (Claude same-vendor; per §2.3 paired-default-with-Logan-discretion-to-downgrade — Logan may downgrade to single-vendor if cost-bandwidth binding)
- **Main-thread Claude differential analysis** (DIFFERENTIAL.md if paired)
- **Logan disposes per AUDIT-SPEC.md §8**

Specify in your AUDIT-SPEC.md the structural expectations for each audit pass + the expected DIFFERENTIAL.md shape.

## §6. Output expected

- **Path:** `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/AUDIT-SPEC.md`
- **Structure:** AUDIT-SPEC.md v2 precedent at `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` (sections — §1 purpose / §2 scope / §3 audit-execution-form / §4 lens-questions per category / §5 classification scheme / §6 output structure / §7 disposition pathway / §8 cross-references).
- **Length:** ~400-700 lines (Phase A precedent was ~600 lines; (V′.a) Step 3 spec may be longer because of the recursive-failure-mode catch + framing-inheritance-risk emphasis).

After your AUDIT-SPEC.md is written, Logan reviews + disposes the spec form. Optional: Claude drafts a parallel spec for differential calibration (Logan-discretion). Then audit fires.

## §7. Closing notes for codex

- **You are not just precedent-adjusting.** B-strong specifically asks for spec-drafting independent of Claude's framing. Where you would write a different spec than what Claude's spec would have looked like, write it.
- **Check the brief itself.** Where this brief constrains your spec in ways that re-import Claude framing-inheritance, surface that in your spec's §1 purpose section (or as a finding in your own spec's lens-questions about itself).
- **Surface where the underlying methodology question is still open.** The (V′.a) replan committed to mapping-shape; if your independent reading suggests mapping-shape is also wrong (or not the only option), surface that as a Class-C finding even though it would re-trigger the trajectory-replan cycle.
- **Don't assume Logan-disposition-of-this-spec is rubber-stamp.** The spec-disposition is itself a substantive Logan-call; structure your spec so Logan can disposition meaningfully (not just "looks comprehensive").

---

*Brief authored 2026-05-01 by Claude (Opus 4.7) per (V′.a) Step 2 self-review Concern 1 disposition. Logan-disposed: "lets go with your recommendations then" /effort xhigh. The brief itself is at framing-inheritance risk per the recursive failure-mode pattern; codex-side independence is the structural mitigation; flag departures-from-brief where your independent reading suggests them.*
