---
type: premise-bleed-audit-disposition
date: 2026-04-29
disposition: commit-with-addendum (option (b) per AUDIT-SPEC.md §8)
disposed_by: Logan, post-DIFFERENTIAL.md review
applied_by: Claude (Opus 4.7), main thread
status: disposition-applied
spec: ./AUDIT-SPEC.md
---

# Disposition — v1-GSD Mental-Model Premise-Bleed Audit

## §0. What was disposed

Logan disposed **commit-with-addendum** (option (b) per AUDIT-SPEC.md §8.2) on `SYNTHESIS-COMPARISON.md` after reviewing the cross-vendor + same-vendor-independent paired audit findings + the main-thread differential analysis.

## §1. Audit arc summary

| Stage | Output | Headline |
|---|---|---|
| Spec | AUDIT-SPEC.md (v2 revised post-cross-vendor-review) | Two-step conditional w/ manual-escalation discretion at §3.4 |
| Step-1 | FINDINGS.md (codex GPT-5.5 high cross-vendor) | 6 instances; 1A/5B/0C; no auto-Step-2 trigger |
| Logan disposition (d) | manual escalation as INDEPENDENT same-vendor read | spec §3.4 manual-discretion override of differential default |
| Step-2 | FINDINGS-STEP2.md (Claude xhigh same-vendor independent) | 9 instances; 4A/3B/2C narrowly load-bearing |
| Differential | DIFFERENTIAL.md (Claude main-thread, post-hoc) | reconcilable; vendor-position-symmetric; recommendation: commit-with-addendum |
| Logan disposition | commit-with-addendum (option (b)) | this file |
| Application | SYNTHESIS-COMPARISON.md §7 addendum landed 2026-04-29 | reading-frame at §7.1 + carry-forward at §7.2 |

## §2. Why this disposition

Per Logan's decision (recorded against DIFFERENTIAL.md §5 recommendation):

1. **Two-auditor differential confirms audit design worked.** Cross-vendor caught vocabulary-import bleed (and confirmed self-correction); same-vendor caught integration-grammar-as-fact at meta-level (which cross-vendor was structurally less likely to see). Discounting Step-2's Class C findings because Step-1 didn't surface them would defeat the M1 paired-review property the audit was set up to exploit.

2. **Both Class C findings have a single low-cost dissolver.** Lift `SYNTHESIS-CROSS.md §6` framing-leakage caveat to point-of-use at SYNTHESIS-COMPARISON.md §5. This is structural: the §6 caveat machinery already exists; the addendum makes it active at the §5-axis-reading frame rather than only after §5 axes are read.

3. **The addendum also serves Step-1's findings.** Step-1's strongest findings (F2 + F3 = INITIATIVE/DECISION-SPACE under-naming + R2-base) are operationally widened by `framing-widening` but artifact text remains. The addendum records the carry-forward in one place rather than requiring readers to triangulate between artifacts.

4. **Commit-as-is would leave a real timing gap.** Future readers entering the comparison cold would read §5 first and §6 last; the residual would only materialize on a careful read order. The addendum makes the reading-frame point-of-use rather than terminal.

5. **Revise-before-commit is heavier than warranted.** Both auditors agree §5's axis-questions are right-shaped; only the *reading frame* needs explicit foregrounding. Revising §5 itself would touch axis-question shape (§5.1(b), §5.2(a)–(c), §5.3(a)–(c), §5.4(a)–(c)) — heavier than the evidence warrants and risks introducing new framing-as-fact patterns at point of revision. Step-2 itself does not recommend this path.

## §3. What was applied

### §3.1 SYNTHESIS-COMPARISON.md addendum

A new §7 ("Premise-bleed audit addendum (post-comparison-draft)") landed at the end of `SYNTHESIS-COMPARISON.md`, with four sub-sections:

- **§7.1 Reading-frame for §5 axes (point-of-use foregrounding).** Lifts SYNTHESIS-CROSS.md §6 framing-leakage caveat verbatim. Names three reading disciplines: inputs-not-observed-facts; loose-able-if-overfit (per `framing-widening §9` items 16-17 + §6.5 disposition-stop discipline); one-register-among-several (per META-SYNTHESIS §2 item 3 + §3 prohibited articulations).
- **§7.2 Artifact-side carry-forward.** Records INITIATIVE.md §3.2 (patcher/skills/hybrid) as historical staging vocabulary; DECISION-SPACE.md §1.8 (R2-base + R2+R3 hybrid) as pre-W1 working hypothesis operationally widened by `framing-widening §5`. Reading discipline for both: read in artifact-context-of-origin, not as current R-mix.
- **§7.3 What the audit did not surface.** Records: no vocabulary-import bleed survives to incubation-facing §5 axes; the comparison's §3.3 + §4.4 + §6.3 + §6.5 jointly constitute self-audit machinery; §2.1 R4 disposition-timing remains explicit Logan-adjudication.
- **§7.4 Cross-references.** AUDIT-SPEC.md, FINDINGS.md, FINDINGS-STEP2.md, DIFFERENTIAL.md, this DISPOSITION.md, DECISION-SPACE.md §1.17.

Frontmatter `status` updated from `draft-complete` to `committed-with-audit-addendum`. Date-stamp footer at end of §7.4 updated to record the addendum-landing date (2026-04-29) and disposition reasoning summary.

### §3.2 Coordination updates

- **OVERVIEW.md §11.6.5** updated with audit-arc completion + disposition trail.
- **STATE.md** updated with new state (audit-arc complete; disposition applied; comparison ready for incubation per §5 axes with §7.1 reading-frame active).
- **DECISION-SPACE.md §1.17** updated with realized-outcome reference (the audit-methodology decision was implemented as designed; cross-vendor + same-vendor-independent + main-thread differential produced a tractable disposition surface).

## §4. Methodological notes

### §4.1 Spec §3.4 deviation: independent mode + main-thread differential

The spec §3.4 default Step-2 structure is differential (Step-2 reads Step-1 + same-artifacts + spec; produces appended differential analysis). Logan's §3.4 manual-escalation invocation overrode this to independent mode (Step-2 reads spec + same-artifacts; does NOT read Step-1; produces self-contained §6.1-shaped FINDINGS-STEP2.md). The differential was then performed in main thread (Claude, post-hoc).

**Tradeoffs of this override:**
- **Gain.** Both reads are independent of each other; the differential carries no anchoring contamination from one to the other. The vendor-position-symmetric structure is cleaner than the spec default's anchored structure for assessing vendor-position blind spots.
- **Loss.** The differential is performed by an in-session Claude instance (main thread) rather than by an independent third reader. This re-introduces in-session-collaboration risk analogous to the comparison's §6.3 D5a caveat. DIFFERENTIAL.md §7 names this explicitly.
- **Net.** Tradeoff is favorable for this audit's purpose: the principal differential signal (whether Step-2's Class C findings are real meta-level bleed or over-extension) is cleaner under independent-mode-with-main-thread-differential than it would have been under spec-default differential where Step-2 anchors on Step-1.

### §4.2 The two-auditor design's principal lesson

The audit's most useful structural finding is *not* any specific Class C item; it's the demonstration that the cross-vendor + same-vendor-xhigh pairing produced complementary findings rather than redundant findings. Cross-vendor caught vocabulary-import (where dispatching-project terminology leaks into artifacts). Same-vendor xhigh caught integration-grammar-as-fact (where the dispatching-project framework has been operationalized as the deliberation surface). Each catches what the other's vendor-position structurally cannot. This is the M1 paired-review property in action; the audit's evidence for it is independent of any specific finding.

For future audits where premise-bleed or framing-leak is a concern, this argues for retaining the cross-vendor + same-vendor-independent pairing as the discipline shape (with conditional escalation per spec §3.4 default OR manual-discretion).

### §4.3 Confidence on the disposition

- **High** that the §7 addendum dissolves both Class C findings as Step-2 specified (the "what dissolves" condition was identical for F6 and F9: lift the framing-leakage caveat to point-of-use; the addendum does this).
- **Medium-high** that no Class C residual remains after the addendum. Possible residuals: (i) a fully-independent third synthesizer might read the §7 addendum as still-not-foregrounded-enough; (ii) the in-session-collaboration caveat continues to apply. Both are tractable: (i) can be addressed by future independent third-reader if Logan reads further audit value as warranted; (ii) is a structural feature of synthesis-comparison work, not a defect specific to this addendum.
- **Medium** that incubation reading SYNTHESIS-COMPARISON.md §5 with the §7.1 reading-frame active will dissolve the practical residual. If incubation reads §5 mechanically (as observed-facts grammar) despite §7.1, the addendum has not fully dissolved the residual at point-of-use. The principal mitigation is Logan's awareness; the secondary mitigation is the addendum's explicit "inputs Logan brought in" framing.

## §5. What this disposition does NOT decide

- **The §2.1 R4 disposition-timing question** (operate-under-shifted-frame vs evaluate-whether-to-shift). This remains Logan-adjudicated at incubation per the comparison's §2.1 explicit Logan-adjudication marker. The audit found no premise-bleed reason to revise this characterization.
- **The §5 axis dispositions** (metaquestion narrowing, R-mix decomposition order, context-anchoring choice, side-probe pre-vs-post-firing). These remain Logan-disposed at incubation per the comparison's §5 explicit Logan-disposition markers.
- **Whether to revise INITIATIVE.md §3.2 or DECISION-SPACE.md §1.8 in place.** The addendum's §7.2 carry-forward records these as historical staging vocabulary; whether to revise the artifact text itself is separable from this audit and can be deferred to the dedicated-uplift-repo migration trigger (per INITIATIVE.md §7).
- **Whether to dispatch a third independent reader.** Logan can invoke this if the in-session-collaboration risk is read as load-bearing for incubation; this audit's disposition does not foreclose that option.

## §6. Cross-references

- AUDIT-SPEC.md (this audit's lens + method; v2 revised post-cross-vendor-review).
- AUDIT-SPEC-REVIEW.md (cross-vendor review of v1; basis for v2 revisions).
- FINDINGS.md (Step-1 cross-vendor codex GPT-5.5 high).
- FINDINGS-STEP2.md (Step-2 same-vendor Claude xhigh independent).
- DIFFERENTIAL.md (post-hoc differential; reconciliation analysis; recommendation trace).
- `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (audit-spec adjudication trace).
- `.planning/gsd-2-uplift/DECISION-SPACE.md §1.17` (audit-methodology decision; implemented by this audit).
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md §7` (addendum landed by this disposition).
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md §11.6.5` (audit-arc trail in initiative-orchestration record).

---

*Disposition recorded 2026-04-29 by Claude (Opus 4.7), main thread, in-session-collaboration with Logan. Subject to same fallibility caveat as DECISION-SPACE.md §0. The in-session-collaboration risk applies to this DISPOSITION.md as it does to DIFFERENTIAL.md and the §7 addendum; future audits or Logan re-review can revise.*
