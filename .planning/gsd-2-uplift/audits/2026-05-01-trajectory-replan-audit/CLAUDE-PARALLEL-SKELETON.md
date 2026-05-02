---
type: audit-spec-parallel-skeleton
date: 2026-05-01
status: parallel skeleton authored blind to codex output (P2 timing per Step 2 self-review Concern 1)
purpose: |
  Claude-side parallel skeleton of what Step 3 audit-spec WOULD look like
  if Claude had drafted it. Used for differential calibration against codex's
  independent draft (B-strong; cross-vendor codex GPT-5.5 xhigh).

  This artifact is NOT the audit-spec. The audit-spec is codex's output (per
  B-strong). This is Claude's parallel skeleton — read AFTER codex returns
  to surface where Claude-framing diverges from codex-framing. The divergence
  itself is signal about (V′.a) Step 2's framing-inheritance residuals.
audience: Logan disposes integrated audit-spec after differential
authored_under_constraint: |
  Authored 2026-05-01 in-session-collaboration with Logan after Step 2 +
  self-review revisions; same framing-inheritance risk as Step 2 + brief.
  Recorded as such; codex independence is the structural complement.
---

# Claude-side parallel skeleton — (V′.a) Step 3 audit-spec

This is what Claude (me) would have drafted as the audit-spec, blind to codex's output. **The codex AUDIT-SPEC.md is the authoritative draft Logan disposes; this skeleton exists for differential calibration.** Read after codex's spec lands; surface where Claude-framing-anchors-the-spec differently than codex-framing-anchors-the-spec.

## §1. Purpose (Claude-framing of why Step 3 exists)

The (V′.a) Step 3 plan-self-audit-2 catches framing-inheritance + recursive-failure-mode residuals in the trajectory-plan revision (commit `ffc0fb0`). Specifically: the revision was authored in-session-collaboration with Logan during the same 2026-05-01 turn-cluster that produced EXTERNAL-VISION-CONTEXT.md (12-property substrate-vision + four-category scope-confidence model + scope-discipline corrections). Both artifacts are subject to closure-pressure-into-elaboration pattern recurrence per 2026-04-30 §5.4 + 2026-05-01 EXTERNAL-VISION-CONTEXT.md §7.1; pattern survives /effort max + pattern-recognition-active; broke only on Logan-correction.

The Phase A audit precedent (2026-04-29; `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/`) was Claude-drafted at audit-spec level and audit-execution level. The audit fired correctly under its scope but did NOT catch the methodology-question-shape-mismatch finding that prompted (V′.a) — because the spec itself was scoped under the misframe. (V′.a) §0.8 + §1.4 + §1.5 + §1.6 are the methodology-fit response; Step 3 audits whether that response is sound.

**The Step 3 audit must be scoped to question-shape-fit + framing-inheritance-risk + recursive-failure-mode catch — explicitly, not nominally.** Lens-questions that fail to operationalize these scopes will reproduce the Phase A audit failure mode.

## §2. Scope (what's under audit)

**Primary artifact:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` at commit `ffc0fb0` (842 lines).

**Secondary artifacts under audit:**
- The self-review trace embedded in the plan's final caveat block + commit `ffc0fb0` body (concerns 2-5 applied; 1+7 Logan-side; 6 no-op).
- The SPEC-DRAFTING-BRIEF.md authoring (commit `f6af0f1`) — meta-level: did the brief itself import Claude framing-inheritance into codex's task?
- The CLAUDE-PARALLEL-SKELETON.md (this artifact) — meta-meta: where do this skeleton's lens-questions diverge from codex's, and is the divergence diagnostic of Claude's framing-inheritance?

**Standing-context inputs (not under audit; informational):**
- 2026-04-30 deliberation (methodology-mismatch finding + (V′.a) disposition).
- EXTERNAL-VISION-CONTEXT.md (12 substrate-vision properties + scope-discipline; 2026-05-01 turn-cluster output).
- RELATIONSHIP-TO-PARENT.md (test-case-vs-substrate framing; Phase B output).
- Phase A audit precedent for audit-shape (PLAN-AUDIT.md + DISPOSITION.md).
- AUDIT-SPEC.md v2 precedent (premise-bleed audit folder).
- META-SYNTHESIS.md (cross-vendor codebase-understanding-audit; gsd-2 substrate vocabulary).

## §3. Audit execution form

- **Step-1 cross-vendor codex GPT-5.5 xhigh** — fires under this disposed spec. Output: FINDINGS.md.
- **Step-2 same-vendor adversarial-auditor xhigh independent mode** — fires under this disposed spec; does NOT read codex Step-1 output (independent stress per AUDIT-SPEC.md v2 §3.4 manual-discretion override). Output: FINDINGS-STEP2.md.
- **Main-thread Claude differential analysis** — DIFFERENTIAL.md after both. Per premise-bleed audit precedent: surfaces converging findings + diverging findings + per-vendor-position calibration.
- **Logan disposition** per AUDIT-SPEC.md v2 §8: commit-as-is / commit-with-addendum / revise-before-commit (where commit = the trajectory-plan-revision-as-finalized; revise = re-revise the plan before downstream phases).

**Paired-default per §2.3 of revised plan**, with Logan-discretion-to-downgrade-to-single-vendor under documented cost-bandwidth constraint (per Concern 5 self-review). Claude-side recommendation: **paired-default fires** for Step 3 specifically; Step 3's whole purpose is to catch what Phase A's single-vendor-Claude-drafted-spec failed to catch; downgrading to single-vendor at Step 3 reproduces Phase A's failure mode.

## §4. Lens-questions (Claude-framing)

Categories below mirror what Claude would have categorized. **Where this skeleton's categories or lens-questions are absent from codex's spec — that's signal Claude over-anchored on these. Where codex's categories are absent from this skeleton — that's signal Claude under-anchored on those.**

### §4.1 Question-shape-fit (mapping vs. spike)

**The lens (V′.a) demands.** If Step 3 doesn't catch question-shape-fit residuals, it has the same failure-mode signature as Phase A.

- **(Q-SF-1) Does Phase D §1.4 retain spike-converges-on-answer structure despite mapping label?** Specifically: §1.4 process step 10 says "Draft FINDINGS.md (the substrate-shape map) + DISPOSITION.md (Logan disposes)" — does this treat mapping as resolvable-by-Logan-disposition rather than iterative-theory-construction? Mapping-shape per §0.8 should be open-iteration-not-resolved-output.
- **(Q-SF-2) Could there be a third question-shape (NOT spike, NOT mapping)?** §0.8 commits to mapping-shape against the counter-claim "broader-scoped spikes would suffice" — but excludes other question-shapes (e.g., theory-construction-without-mapping; ethnographic substrate-shape characterization; speculative-design-anchored substrate-probing). Are alternatives genuinely considered or implicitly foreclosed?
- **(Q-SF-3) Does §0.8 spike-vs-mapping dichotomy oversimplify the question-space?** Hybrid shapes (mapping with spike-elements within; mapping that converges on actionable design-shape) may be the actual question-shape but get classified as one or the other.
- **(Q-SF-4) Does the four-axis structure cover the evidence-territory?** What if there's a fifth axis the four miss — e.g., "intent-revision-trace under accommodation evidence" (per Concern 3 self-review iteration-mechanics gesture); "harness-studio-pressure foreclosure-risk-trace"; "post-extraction substrate-evolution-trace."

### §4.2 Framing-inheritance-risk catch

- **(Q-FI-1) Does the revision treat its own framing-vocabulary as observed-fact?** "12 substrate-vision properties" + "C1/C2/C3/C4 model" + "burden-of-proof-on-exclusion" are inputs from EXTERNAL-VISION-CONTEXT.md, not facts. Where does the revision implicitly fact-treat them? Per §7.1 reading-frame-as-inputs-not-facts discipline.
- **(Q-FI-2) Does EXTERNAL-VISION-CONTEXT.md framing carry residuals the revision inherits?** EXTERNAL-VISION-CONTEXT.md §7.1 records closure-pressure recurrence during its own 2026-05-01 authoring. Residuals possible: (a) 12-property set may be over-articulated (artifact-of-elaborate-articulation-rather-than-actual-vision-distinction); (b) C1/C2/C3/C4 boundaries may be artifacts of conversation-shape; (c) burden-of-proof-on-exclusion may be load-bearing-in-conversation-but-not-load-bearing-as-substrate-discipline.
- **(Q-FI-3) Does the self-review process operate-or-perform?** Specifically: C4 self-corrects MOVE→DUPLICATE but doesn't address the underlying mechanism that produced the premature commit (structural-feel calls without sufficient evidence-load). Performative-vs-operational openness check per §0.6.
- **(Q-FI-4) Does closure-pressure-into-elaboration pattern recur in the revision itself?** Where in the 842-line plan are "resolved enough to commit" framings unresolved-by-evidence?
- **(Q-FI-5) D5a in-session-collaboration risk compounds across the chain (V′.a Step 1 → 2026-05-01 vision-articulation → Step 2 → self-review → SPEC-DRAFTING-BRIEF → this skeleton).** Each artifact inherits prior-artifact framing. Phase A audit was the prior independent break; nothing since 2026-04-29 has been independently-authored. Step 3 paired audit is the structural break.

### §4.3 Methodology-question-shape-mismatch (the new failure mode)

- **(Q-MM-1) Is the methodology-mismatch finding correctly diagnosed?** §0.8 challenges the counter-claim "broader-scoped spikes would suffice" — counter-counter is the spike methodology produces single-target-focus regardless of scope. Is the counter-counter sound? Is there a deeper diagnosis (e.g., the prior framing-error wasn't methodology-mismatch but vocabulary-mismatch — using gsd-2 surface vocabulary when the question was about practice-accommodation)?
- **(Q-MM-2) Does the iteration-mechanics gesture in §1.4 step 6+7 adequately operationalize the iteration?** Per Concern 3 self-review: under-specification claimed appropriate (mapping is theory-constructive; locking iteration shape is closure-pressure). Is the under-specification appropriate or hidden closure-pressure?
- **(Q-MM-3) Phase E mapping-coherence test — what does coherence MEAN at theory-construction stage?** §1.5 lists dimensions but doesn't compose them into the coherent/partially-coherent/incoherent disposition.
- **(Q-MM-4) Spikes-nest-inside-mapping discipline (§0.8) — what's the trigger for "this within-mapping question is genuinely a spike question"?** Without specified triggers, the discipline is performative.

### §4.4 Phase F gate criteria + Phase G dispositions

- **(Q-PF-1) Phase F criterion 2 (≥1 C1 path)** — what if zero C1 paths? §1.6 says "both findings warrant Phase D re-execution or (V′.b) consideration" — but doesn't specify when which.
- **(Q-PF-2) Phase F criterion 5 (methodology-mismatch finding integrated)** — operationalization risk: substrate-shape map could cite METHODOLOGY-MISMATCH-FINDING.md without operationally accounting for it.
- **(Q-PG-1) Phase G dispositions** — METHODOLOGY-MISMATCH-FINDING.md self-corrected to DUPLICATE; 2026-04-30 deliberation Per-deliberation-Logan-disposed. Are there OTHER artifact-dispositions similarly under-considered? (Specifically: SPEC-DRAFTING-BRIEF.md + CLAUDE-PARALLEL-SKELETON.md + Step 3 audit folder — all post-extraction dispositions are unspecified.)

### §4.5 Paired-audit-default-with-discretion

- **(Q-AD-1) Is paired-default-with-Logan-discretion-to-downgrade right?** Self-review C5 softening preserves escape-valve. Per 2026-04-30 §5.4: closure-pressure-pattern-survives-single-vendor risk. Is the softening legitimate cost-discipline or M1-strict-undersell-adjacent?
- **(Q-AD-2) Is the audit-spec for Step 3 (codex's spec + this skeleton) authored under conditions that re-import the failure mode?** Brief constrains codex; this skeleton constrains differential-comparison. Where do these constraints import Claude framing into supposedly-independent components?

### §4.6 Frame-revision-check ((V′.a) Step 4 mechanism)

- **(Q-FR-1) Is the frame-revision-check mechanism (§0.5 + §6.1 + §6.2 + §1.4 process steps 2/5/9) adequate for catching frame-revisions during Phase D execution?** Phase entry / mid-phase / output-draft check-points are specified — but check WHAT? The mechanism doesn't specify what triggers fire-frame-revision-check vs. continue-within-frame.
- **(Q-FR-2) Does the mechanism risk performative firing?** I.e., the check fires nominally ("we checked; it's still right") without operationally engaging frame-revision question.

### §4.7 Negative-space + meta

- **(Q-NS-1) What does the revision exclude from consideration?** Negative-space lens. Specifically: which intervention-intents from the project-portfolio (Property 12; cross-project portfolio-support) are NOT in S1-S8 sketch-set; which gsd-2 surfaces are NOT in axis-1 list (per META-SYNTHESIS); which arxiv-sanity-mcp practices are NOT in axis-2 list.
- **(Q-NS-2) What does the revision NOT say but should?** Missing dimensions.
- **(Q-Meta-1) Is there an implicit frame the revision treats as natural-not-imported?** Possibly: that mapping-shape is the right response (rather than e.g., "stop here; (V′.a) is the wrong replan and (V′.b) — return to incubation — was the right call").
- **(Q-Meta-2) Is the test-case-vs-substrate framing (RELATIONSHIP-TO-PARENT.md §1) preserved correctly in mapping-shape Phase D?** Phase D maps "arxiv-sanity-mcp practice" as evidence-channel — but is it the test-case-shape that matters, or could a different test-case have produced different evidence?

### §4.8 Differential-calibration meta-questions

These exist BECAUSE this skeleton is paired with codex's spec for differential.

- **(Q-DC-1) Where does this skeleton's lens-question categorization differ from codex's?** Convergence = M1 paired-review confirms; divergence = M1 paired-review surfaces vendor-position-asymmetry signal.
- **(Q-DC-2) Where does this skeleton miss lens-questions codex includes?** Claude-blind-spots surfaced.
- **(Q-DC-3) Where does this skeleton include lens-questions codex doesn't?** Claude-overweight-areas surfaced.

## §5. Classification scheme (per AUDIT-SPEC.md v2 precedent)

- **Class A — ACCEPT-AS-STATED.** Cosmetic / phrasing / non-load-bearing. No revision warranted.
- **Class B — ADDENDUM-TRACTABLE.** Substantive but addressable as addendum without trajectory-shape change. Logan-discretion: addendum or revise.
- **Class C — REVISE-BEFORE-COMMIT.** Load-bearing trajectory-shape concern. Revision precedes downstream phases.

Each finding includes: lens-question reference; evidence in artifact; classification; non-binding disposition signal (per AUDIT-SPEC.md §6.1 §5).

## §6. Output structure

Per AUDIT-SPEC.md v2 §6.1. Frontmatter: `type: trajectory-plan-audit-findings`; `audit_target: ffc0fb0 cheerful-forging-galaxy.md (V′.a) Step 2 + self-review`; `auditor: cross-vendor codex GPT-5.5 xhigh` (Step 1) / `same-vendor adversarial-auditor xhigh independent` (Step 2); `audit_spec: AUDIT-SPEC.md`.

Sections: §1 summary + headline-result; §2 per-finding details (lens-question + evidence + classification + disposition-signal); §3 cross-finding patterns; §4 negative-space report; §5 non-binding disposition signal (per-finding + overall).

## §7. Disposition pathway (per AUDIT-SPEC.md v2 §8)

1. Logan reads FINDINGS.md (Step 1) + FINDINGS-STEP2.md (Step 2) + DIFFERENTIAL.md.
2. Logan disposes:
   - Commit-as-is — Class A only or Logan reads B/C as not load-bearing.
   - Commit-with-addendum — Class B/C tractable as addendum; addendum drafted; commit follows.
   - Revise-before-commit — Class C affects load-bearing-claim shape; revision precedes downstream phases.
3. Disposition recorded at DISPOSITION.md (audit-folder local).

## §8. Cross-references

- `cheerful-forging-galaxy.md` at `ffc0fb0` (artifact under audit).
- `SPEC-DRAFTING-BRIEF.md` at `f6af0f1` (codex brief).
- `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` (methodology-mismatch finding).
- `EXTERNAL-VISION-CONTEXT.md` at `c1b098c` (12 properties + scope-discipline).
- `RELATIONSHIP-TO-PARENT.md` (test-case-vs-substrate framing).
- `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/` (Phase A precedent).
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` (v2 spec precedent).

---

*Skeleton authored 2026-05-01 by Claude (Opus 4.7) blind to codex AUDIT-SPEC.md draft (P2 timing per (V′.a) Step 2 self-review Concern 1). Subject to in-session-collaboration framing-inheritance from Step 2 + self-review + brief authoring; codex's spec is the structural complement. Differential-calibration analysis happens after both land + before audit dispatch. Logan disposes integrated spec.*
