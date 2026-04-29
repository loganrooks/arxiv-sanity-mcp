---
type: audit-differential
date: 2026-04-29
authors:
  - main-thread Claude (Opus 4.7) — differential reconciliation
  - audit-findings-A.md — cross-vendor codex GPT-5.5 xhigh (Step-1)
  - audit-findings-B.md — same-vendor adversarial-auditor (Claude Opus 4.7 xhigh, independent mode) (Step-2)
status: complete
purpose: |
  Main-thread reconciliation of paired cross-vendor + same-vendor independent audit findings
  for the Phase C incubation-checkpoint audit. Per premise-bleed audit precedent (DECISION-SPACE.md
  §1.17 + lessons-distilled): paired Step-1 + Step-2 produces complementary findings rather than
  redundant. This DIFFERENTIAL.md surfaces convergence + divergence + complementary substrate +
  pattern observations, and produces a non-binding disposition signal for Logan adjudication.
inputs:
  - .planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/audit-findings-A.md (codex; 0A/5B/2C)
  - .planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/audit-findings-B.md (same-vendor; 4A/6B/2C)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md (artifact under audit)
  - .planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/AUDIT-SPEC.md (audit spec)
ground: |
  Premise-bleed audit precedent (DECISION-SPACE.md §1.17 lessons-distilled): cross-vendor +
  same-vendor pairing produces complementary findings — cross-vendor catches substantive-coherence
  residuals; same-vendor catches register-shaped residuals. Both vendor-positions needed for
  premise-bleed and framing-leak audits.
---

# Phase C Incubation-Checkpoint Audit — Main-Thread Differential

## §0. Summary

**Class breakdown across both auditors:**
- Cross-vendor codex (A): 0A / 5B / 2C (7 findings)
- Same-vendor adversarial-auditor (B): 4A / 6B / 2C (12 findings)
- Total: 4A / 11B / 4C (across paired)

**Convergent Class C findings (both auditors flag the same axis at Class C):**
1. **§7.4 substrate-shape-anchoring projection from test-case-anchoring** — converged at codex F-IC-A1 + same-vendor F-IC-1. Both auditors confirm §7.8 (i) was the right risk to flag; both extend the audit-priority surface beyond §7.8's articulation. **Class C in both.**

**Divergent Class C findings (one auditor reads as Class C; the other reads differently):**
2. **§7.1 (b) ↔ §7.3.a coherence (codex F-IC-A2 Class C):** codex finds internal incoherence — if §7.1 disposed (b) "evaluate-whether-to-shift," first-target should generate evidence ABOUT R4-shift; §7.3.a primarily-R2 decision-trace target's R4 evidence path is under-specified.
3. **§7.3.a reasoning bullet 4 inversion of RELATIONSHIP-TO-PARENT.md §2 failure-mode 1 (same-vendor F-IC-2 Class C):** same-vendor finds the reasoning-trace bullet "Decision-trace IS arxiv-sanity-mcp's binding constraint per RELATIONSHIP-TO-PARENT.md test-case-anchoring; substrate evidence will be coherent rather than fabricated" inverts the standing-context artifact's intended use.

**Net read on the divergence at §7.3.a.** Both auditors flag §7.3.a but at different layers: codex at *disposition-coherence* (the chosen target doesn't fit the chosen disposition-timing); same-vendor at *reasoning-trace D5a-leak* (the bullet justifying the target inverts the standing-context framing). The two findings are NOT contradictory — they prescribe different fixes:
- **Codex F-IC-A2** prescribes: §7.3.a should include explicit R4 contrast (headless/orchestration comparator, effective-state-emission integration, OR declared "R4 not tested by this first target" limit) — OR re-dispose §7.3.a toward R4/probe-shape if §7.1's evaluate-whether-to-shift is meant to be tested directly.
- **Same-vendor F-IC-2** prescribes: §7.3.a reasoning bullet 4 reframe or removal — disposition outcome (decision-trace skill/workflow) preserved; reasoning-trace cleansed of test-case-anchoring inheritance.

**Both auditors signal commit-with-addendum as the most-defensible disposition.** Codex hedges between commit-with-addendum and revise-before-commit (depending on whether Logan reads C findings as correctable by Phase D dispatch constraints or as requiring re-disposition); same-vendor explicitly favors commit-with-addendum (with §7.1-style point-of-use foregrounding pattern applied at disposition layer per SYNTHESIS-COMPARISON.md §7 precedent).

**My non-binding disposition signal (main-thread, after reading both):** **Commit-with-addendum** is the strongest signal. The convergent C1 + the two divergent C2's compose into one well-shaped addendum that addresses the underlying pattern (test-case-anchoring inheritance materializing in disposition-record reasoning + DECISION-SPACE.md determining-assumption + first-target reasoning bullet) plus the Phase D dispatch-readiness requirements codex catches. Detail at §3 below.

---

## §1. Convergence analysis

### §1.1 Convergent C1: §7.4 substrate-shape-anchoring projection

**Codex F-IC-A1 (Class C, high confidence).** Diagnosis: §7.4 disposition keeps "plural-context-anchoring" wording but operationally re-centers arxiv-sanity-mcp test-case via reasoning bullet 2 ("first-wave evidence is what we have"). Bullets (1) + (3) license the disposition without bullet (2)'s D5a-shaped move. Missing distinction between "Phase D diagnostic anchor" and "substrate-shape anchoring."

**Same-vendor F-IC-1 (Class C, medium-high confidence).** Diagnosis: convergent on §7.4 reasoning bullet 2 as the load-bearing leak. Same-vendor extension: the leak is *legitimated by stipulation* at DECISION-SPACE.md §1.18 determining-assumption #2 ("legitimately privileges arxiv-sanity-mcp's test-case anchoring... not D5a leak. Audit will challenge whether this holds") — inverts disposition-discipline (audit must overcome determining-assumption to dislodge a Logan disposition).

**Reconciliation.** Both auditors flag the same axis + same load-bearing reasoning-bullet. They surface complementary substrate:
- Codex catches the **substantive evidence-license shape**: bullet (2) is doing more work than its surface formulation.
- Same-vendor catches the **register-shape manifestation at meta-layer**: DECISION-SPACE.md §1.18 determining-assumption #2 formalizes the leak as a legitimating commitment.

**Combined fix shape.** Both auditors point at the same addendum target: §7.4 reasoning bullet 2 + DECISION-SPACE.md §1.18 determining-assumption #2 reframing. The §7.1-style point-of-use foregrounding pattern (per SYNTHESIS-COMPARISON.md §7.1 precedent) addresses both. Specifically:
- **§7.4 reasoning bullet 2 reframe**: lift the audit-priority risk from §7.4's closing paragraph into the reasoning trace itself; explicitly mark bullet 2 as the audit-priority surface, not as a positive evidence-license.
- **DECISION-SPACE.md §1.18 determining-assumption #2 reframe**: from "legitimately privileges... not D5a leak" to "is the audit-priority surface flagged at INCUBATION-CHECKPOINT.md §7.4; auditors assess whether the projection is principled or D5a-leak; this audit's findings (F-IC-A1 + F-IC-1) confirm the audit-priority risk surface and prescribe addendum-shape correction."

**Class call after reconciliation.** Confirmed C. The addendum is load-bearing for Phase E stability test (which reads disposition-stability against reasoning-trace anchors per trajectory plan §1.5).

### §1.2 Convergent §7.7 frame-revision-none-active disposition

**Codex F-IC-A5 (Class B, high confidence).** Diagnosis: "live-and-well-grounded" wording drifts from "no revision required before Phase D" toward "the integration grammar is well-grounded as a fact-like map." Repeats the §7.1 reading-frame's residual at a different layer.

**Same-vendor F-IC-3 (Class B, medium confidence).** Diagnosis: "no frame-revision triggers active" disposition without operational triggering condition is performative-vs-operational openness pattern (per trajectory plan §0.6 row).

**Reconciliation.** Both flag §7.7 at Class B with different vocabularies but the same residual:
- Codex: wording drifts toward fact-like map.
- Same-vendor: option preserved without operational trigger.

**Combined fix shape.** §7.7 rephrasing addresses both:
- "No frame-revision before Phase D; active stressors carried forward" (codex's prescription).
- Operational triggers articulated for when frame-revision would fire at Phase D / E / F (same-vendor's prescription).

**Class call after reconciliation.** Confirmed B. Addendum-shape; ~5-10 lines.

### §1.3 §7.8 audit-priority list coverage

**Codex coverage.** Converged-with: §7.8 (i)/(ii)/(iii)/(v)/(vi) confirmed real challenge surfaces. Extended-beyond: P2 post-D under-prioritization (F-IC-A4); user-side adoption-pattern probe missing (F-IC-A7); P5 failure branch missing (F-IC-A3). Mis-aligned: P2 read as more load-bearing than §7.8 implies.

**Same-vendor coverage.** Converged-with: (i) substrate-shape-anchoring projection + (vi) frame-revision-none-active. Extended-beyond: operational coupling of (i) at §7.3.a + DECISION-SPACE §1.18 layer; F-IC-3 / F-IC-4 / F-IC-5 / F-IC-6 / F-IC-7 / F-IC-8 across multiple axes. Mis-aligned: §7.8 (ii) §7.1 (b)-over-(a) — same-vendor reads (b) as adequately defensible; not the conservative-default-when-uncertain risk §7.8 ranks second.

**Net coverage assessment.** §7.8's ranked priorities track real surfaces but are individually-articulated; the audits surface that the underlying pattern is **system-level coupling** (F-IC-1 + F-IC-2 + F-IC-8 + F-IC-12 from same-vendor; F-IC-A1 + F-IC-A2 from codex) rather than separate audit-priority items. The §7.8 list is **calibration-grade as a risk taxonomy but under-couples the items as a system.**

---

## §2. Divergence analysis

### §2.1 Divergent C: §7.1 (b) ↔ §7.3.a coherence (codex C2 only)

**Codex F-IC-A2 (Class C, high confidence).** §7.1 says first-target generates evidence ABOUT R4-shift; §7.3.a selects primarily-R2 skill/workflow target. Internal incoherence: a primarily-R2 target does not automatically generate R4-shift evidence. R4 evidence route is present only indirectly (P5 pre-D parallel; possible workflow-template composition; later Phase E re-disposition).

**Same-vendor reads §7.1 (b) as defensible** (per F-IC-B headline + §4 calibration mis-alignment): "(b)-disposition is adequately defensible by Claude's transparency-disclosure (b is conservative-default-when-uncertain risk acknowledged but reversible to (a) at Phase E if Phase D evidence licenses; the disposition's reasoning trace is structurally sound)." Same-vendor's C2 (F-IC-2) targets §7.3.a reasoning bullet 4, NOT §7.1-vs-§7.3.a coherence.

**Why the divergence.** This is the **M1 paired-review property in action** at the divergence layer:
- **Cross-vendor strength:** catching substantive-coherence shape across dispositions. Codex reads "if (b), then evidence-about-shift; if R2 first-target, then evidence-about-R2-not-shift." Substantive incoherence detected via comparison §2.1 + §5.2.
- **Same-vendor strength:** reading the disposition shapes as preserving deliberation-discipline. Same-vendor reads (b) as the right disposition-discipline-honoring choice (synthesis defers shift-disposition to incubation; codex's declarative shape was potentially premature-collapse). Per comparison §4.1 M1-inversion observation, same-vendor caught this disposition-discipline at synthesis stage; reads it as preserved at disposition stage.

**Reconciliation.** Both reads are defensible; they're operating at different layers:
- Codex: dispatch-coherence (will Phase D evidence answer §7.1's question?).
- Same-vendor: disposition-coherence (does the disposition-set hold deliberation-discipline?).

**Combined fix shape — three options for Logan:**
- **(a) Add explicit R4 contrast at Phase D dispatch** (codex's preferred fix). Phase D first-target spec includes: (i) headless/orchestration comparator OR (ii) effective-state-emission integration as contrast with skill/workflow R2 path OR (iii) explicit declaration "R4 not tested by this first target — Phase E dispatches separate R4-shaped first-target if (b)→(a) re-disposition warranted." This addresses codex's coherence concern while preserving same-vendor's disposition-discipline read.
- **(b) Re-dispose §7.3.a toward R4/probe-shape** (codex's revise-before-commit branch). Replace decision-trace skill/workflow with effective-state-emission probe (P5) as first-target — generates R4-shift evidence directly. This addresses codex's coherence concern but loses A+F decision-trace fit and loses R2 skill subsystem viability test.
- **(c) Re-dispose §7.1 to (a) operate-under-shifted-frame** — concedes codex's read that R4 elevation is already evidence-licensed. This addresses codex's coherence by removing the evaluate-whether-to-shift constraint; same-vendor would read this as premature-collapse risk.

**Class call after reconciliation.** Codex reads C, same-vendor reads non-finding-or-B at this axis. Reconciliation: **Class C** is defensible because Phase D dispatch-readiness is load-bearing for Phase E stability test; if Phase D evidence doesn't bear on §7.1's question, the disposition record's evidence-load doesn't track the disposition's claim. **Recommended fix: (a) — add explicit R4 contrast at Phase D dispatch as addendum.** Preserves both auditors' concerns: codex's coherence is restored at the dispatch layer; same-vendor's disposition-discipline is preserved at the disposition layer.

### §2.2 Divergent C: §7.3.a reasoning bullet 4 inversion (same-vendor C2 only)

**Same-vendor F-IC-2 (Class C, medium-high to high confidence).** Diagnosis: §7.3.a reasoning bullet 4 ("Decision-trace IS arxiv-sanity-mcp's binding constraint per RELATIONSHIP-TO-PARENT.md test-case-anchoring; substrate evidence will be coherent rather than fabricated") inverts RELATIONSHIP-TO-PARENT.md §2 failure-mode 1's verbatim shape. The bullet activates the test-case-anchoring inheritance §7.4 audit-priority risk flagged.

**Codex flags §7.3.a but at a different surface.** Codex F-IC-A6 (Class B) targets §7.3.a as needing Phase D dispatch contract specification (artifact produced; skill behavior tested; F-discipline observable). Different concern; doesn't engage the reasoning bullet 4 inversion.

**Why the divergence.** Same-vendor strength manifested: register-shaped residuals at the dispositions themselves. Codex would have to read §7.3.a's reasoning trace AGAINST RELATIONSHIP-TO-PARENT.md §2 failure-mode-1 *prose* to catch it; same-vendor catches it because the move structurally rehearses the failure mode at the reasoning-trace layer. Per premise-bleed audit precedent: same-vendor catches integration-grammar-as-fact at meta-level; this is the same pattern at disposition layer.

**Combined fix shape.** Reframe or remove §7.3.a reasoning bullet 4. Disposition outcome (decision-trace skill/workflow) preserved on bullets 1 + 2 + 3 + 5 + 6.

**Class call after reconciliation.** Confirmed C (per same-vendor's call) because the reasoning-trace residual is load-bearing for Phase E (which reads disposition-stability against reasoning-trace anchors). Addendum-shape correction.

### §2.3 Divergent B-cluster (codex-unique substantive findings)

Codex catches several substantive findings same-vendor does not surface:
- **F-IC-A3 (P5 failure branch missing)** — what happens if pre-D P5 reveals docs-vs-source-drift severe enough to invalidate decision-trace assumptions? Disposition under-specifies.
- **F-IC-A4 (P2 post-D under-prioritization)** — comparison §5.4 says P2 trigger is "any R2 work targeting specific subsystem"; chosen target is R2-shaped on skill subsystem. Trigger met.
- **F-IC-A6 (Phase D dispatch contract missing)** — §7.3.a is directionally meaningful but not operationally dispatchable.
- **F-IC-A7 (user-side adoption-pattern probe missing from taxonomy)** — plural-context anchoring without probe that could test whether chosen contexts match plausible users.

**Pattern.** Codex's substantive strength manifested. Same-vendor was less attentive to the dispatch-readiness layer because it was more attentive to register-shape residuals at the disposition layer.

**Combined fix shape.** All four are addendum-shape additions to the checkpoint:
- §7.5 P5 failure branch defined (cheap; ~5 lines).
- §7.5 P2 challenge surface added to §7.8 OR P2 narrow pre-D spot-check (cheap; ~3 lines).
- §7.3.a Phase D dispatch contract specified (moderate; ~10-15 lines OR pointer to forthcoming Phase D mini-spec).
- §7.5 user-side adoption-pattern probe added to taxonomy as deferred or explicit-not-fired-with-reasoning (cheap; ~3 lines).

### §2.4 Divergent B-cluster (same-vendor-unique register findings)

Same-vendor catches several register findings codex does not surface:
- **F-IC-4 (§7.2 (β) steel-man under-engaged)** — audit-priority risk concedes (β) may be redundant with §7.3 first-target screening; reasoning trace doesn't engage.
- **F-IC-5 (§7.6 reasoning-trace post-hoc not ex-ante)** — cites "dispositions composed coherently" (post-hoc) rather than comparison §5.5 structural argument (ex-ante).
- **F-IC-6 (§7.3.c smuggled (a)-disposition under (b)-clothing)** — "the workflow template side could shift toward R4 if Phase D evidence licenses" pre-licenses sub-shifts beyond §7.1's (b)-vs-(a) re-disposition.
- **F-IC-7 (§7.5 P5 reasoning "any first-target" inconsistency)** — "useful diagnostic context for any first-target" violates §7.5's own dispositions of P2 / P4 / P6 post-D.
- **F-IC-8 (§7 disposition-record header rendered-transparency-as-ground)** — "Logan-disposition disposed... by accepting Claude's proposed-and-rendered-with-sensitivity-mapping position" embeds rendered-transparency as substantive ground.

**Pattern.** Same-vendor's register strength manifested. Codex was less attentive to reasoning-trace quality at the disposition layer because it was more attentive to dispatch-readiness substantive coherence.

**Combined fix shape.** All five are addendum-shape reframings of reasoning-trace prose:
- §7.2 reasoning trace engages the steel-man (~3 lines).
- §7.6 reasoning trace adds ex-ante structural argument from comparison §5.5 (~3-5 lines).
- §7.3.c clarifies whether sub-shift is part-of-§7.1-mechanism or independent (~2-3 lines).
- §7.5 P5 reasoning specifies the licensing argument distinct from "any first-target" (~3-5 lines).
- §7 disposition-record header reframes from "by accepting Claude's proposed... position" to "from option sets per §1.5/§2.5/etc., with audit as structural correction for D5a" (~3-5 lines).

### §2.5 Same-vendor cosmetic A-cluster

F-IC-9 / F-IC-10 / F-IC-11 / F-IC-12 are cosmetic wording-shape findings. F-IC-12 (frontmatter status field) inherits from F-IC-8's reframing. F-IC-9 / F-IC-10 / F-IC-11 are Logan-discretion fix-or-skip per low confidence.

---

## §3. Pattern observations + non-binding disposition signal

### §3.1 The convergent system-level pattern

Same-vendor's analysis at §3 of audit-findings-B identifies the convergent risk pattern: **F-IC-1 + F-IC-2 + F-IC-8 + F-IC-12 all point at one underlying issue — the disposition record carries register-shaped residuals that materialize the §7.4 audit-priority risk in the disposition's own reasoning-traces and metadata.** Codex's C-findings (F-IC-A1 + F-IC-A2) plus B-findings cluster fit alongside this pattern as substantive-coherence manifestations.

**Net read.** The disposition record's *outcomes* (the per-axis dispositions at §7.1-§7.7) are plausibly correct. The *reasoning traces + metadata* carry register-shaped + substantive-coherence residuals that materialize the §7.8 (i) audit-priority risk in concrete operational form.

### §3.2 Why commit-with-addendum is the strongest signal

Both auditors' headline + §5 explicitly favor commit-with-addendum (codex hedges with revise-before-commit; same-vendor explicitly favors addendum). The case for commit-with-addendum:

1. **Disposition outcomes preserved.** The dispositions at §7.1-§7.7 are defensible per per-axis analysis. Re-disposition would be heavy and the evidence supporting the dispositions remains.
2. **Addendum addresses the convergent pattern.** §7.1-style point-of-use foregrounding (per SYNTHESIS-COMPARISON.md §7 precedent) at the disposition-record layer addresses F-IC-1 + F-IC-2 + F-IC-8 + F-IC-12 + DECISION-SPACE.md §1.18 determining-assumption #2 reframing in one well-shaped section. Same shape that worked for the premise-bleed audit residual at synthesis stage.
3. **Substantive-coherence findings tractable as additions.** Codex's F-IC-A2 (R4 contrast at Phase D) + F-IC-A3 (P5 failure branch) + F-IC-A4 (P2 challenge surface) + F-IC-A6 (Phase D dispatch contract) + F-IC-A7 (user-adoption probe) are all addendum-shape additions, not re-dispositions.
4. **Class B reasoning-trace residuals tractable as small reframings.** Same-vendor's B-cluster (F-IC-3 / F-IC-4 / F-IC-5 / F-IC-6 / F-IC-7) are 3-5-line reframings each.
5. **Methodology continuity.** Premise-bleed audit precedent landed §7 reading-frame addendum at SYNTHESIS-COMPARISON.md; this audit lands a parallel §7.9 (or analogous) addendum at INCUBATION-CHECKPOINT.md. Same shape; transferable lesson.

### §3.3 The case for revise-before-commit (codex's stronger branch)

Codex hedges between commit-with-addendum and revise-before-commit. Revise-before-commit is defensible if Logan reads:
- **F-IC-A1 as Class C in the strong sense** — substrate-shape-anchoring needs to be re-disposed from "A+F substrate primary" to "A+F diagnostic-first under plural substrate anchoring." Per same-vendor's analysis, addendum can dissolve the Class C concern; per codex's analysis, the strong reading licenses revision.
- **F-IC-A2 internal incoherence as requiring §7.3.a re-disposition** — toward R4/probe-shape (effective-state-emission probe) if §7.1's evaluate-whether-to-shift is meant to be tested directly. This is the (b) option in my §2.1 reconciliation.

**Why revise-before-commit is harder to defend than commit-with-addendum.** The convergent risk pattern (per §3.1) is at the reasoning-trace layer, not the disposition-outcome layer. Revising the disposition outcomes adds disposition-shift cost without proportionate evidence-yield gain. Same-vendor's §4 steelman residue acknowledges that F-IC-1 + F-IC-2 *may* be over-strong on Class C; a softer reading lands at B with addendum still applicable.

### §3.4 The case for commit-as-is

Defensible if Logan reads §7.8 + DECISION-SPACE.md §1.18 + Phase E re-adjudication hooks as already covering the substantive risk surfaces, and Phase D planning is expected to specify decision-trace + P5 branches + R4 observables before execution.

**Why commit-as-is is harder to defend than commit-with-addendum.** Both auditors flag the C-findings as load-bearing for Phase E (which inherits the reasoning-trace anchors as standing context). Phase D dispatch readiness gaps (codex's B-cluster) need to be specified somewhere; if not in the checkpoint addendum, they need to be in a separate Phase D mini-spec. Either way, the work needs to be done; the question is whether to land it as addendum to the checkpoint or as a separate downstream artifact.

### §3.5 Recommended addendum shape (if Logan disposes commit-with-addendum)

Per SYNTHESIS-COMPARISON.md §7 precedent: append a §7.9 (or §8 / new section after §7) "Audit addendum (Phase C audit, post-disposition)" carrying:

**§7.9.1 Audit reading-frame at disposition layer (parallel to §7.1 reading-frame at synthesis layer).** Apply §7.1 point-of-use foregrounding to:
- §7.4 reasoning bullet 2 ("first-wave evidence is what we have") — read as audit-priority surface, not as positive evidence-license.
- §7.3.a reasoning bullet 4 ("Decision-trace IS arxiv-sanity-mcp's binding constraint... substrate evidence will be coherent rather than fabricated") — reframe or read as descriptive-not-licensing per same-vendor F-IC-2 analysis.
- §7 disposition-record header — reframe "by accepting Claude's proposed-and-rendered-with-sensitivity-mapping position" to "from option sets per §1.5/§2.5/etc.; audit fires as structural correction for D5a per trajectory plan §0.5; audit-applied disposition pathway per AUDIT-SPEC.md §8."
- Frontmatter status — same reframe.

**§7.9.2 DECISION-SPACE.md §1.18 determining-assumption #2 reframe.** "Substrate-shape-anchoring at this iteration legitimately privileges arxiv-sanity-mcp's test-case anchoring..." → "Substrate-shape-anchoring at this iteration is the audit-priority surface flagged at INCUBATION-CHECKPOINT.md §7.4. Audit (audit-findings-A.md F-IC-A1 + audit-findings-B.md F-IC-1) confirms the projection-from-test-case-to-substrate-shape carries D5a inheritance at reasoning bullet 2; the disposition outcome (A+F-primary plural) is licensed by bullets (1) + (3) without bullet (2)'s D5a-shaped move; the addendum at INCUBATION-CHECKPOINT.md §7.9 lifts the audit-priority surface into the reasoning trace." (Or analogous; Logan-disposed wording.)

**§7.9.3 Phase D dispatch additions per codex F-IC-A2 + F-IC-A3 + F-IC-A6.**
- R4 contrast requirement: Phase D first-target spec includes explicit R4 observable (headless/orchestration comparator OR effective-state-emission integration) OR declared "R4 not tested at first target — Phase E dispatches separate R4-shaped first-target if (b)→(a) re-disposition warranted."
- P5 failure branch: if pre-D P5 reveals docs-vs-source-drift severe enough to invalidate decision-trace assumptions, paths are: (i) pause first-target dispatch; (ii) re-scope target; (iii) proceed with explicit invalidation caveat. Logan-disposed at trigger-time.
- §7.3.a Phase D dispatch contract: forthcoming Phase D mini-spec OR addendum specification of artifact produced + skill behavior tested + workflow-template composition scope + successful decision-trace evidence + F-discipline observability.

**§7.9.4 §7.5 + §7.7 reasoning-trace additions.**
- §7.5 P2 challenge surface: added to §7.8 audit-priority list (cheap insurance) OR P2 narrow pre-D spot-check for skill subsystem only.
- §7.5 user-side adoption-pattern probe: added to probe taxonomy as deferred per framing-widening §9 item or explicit-not-fired-with-reasoning.
- §7.7 reframe from "live-and-well-grounded" to "active-non-revision: usable for Phase D, still under stress" per codex F-IC-A5; add operational triggers per same-vendor F-IC-3 (Phase D / E / F conditions under which frame-revision fires).

**§7.9.5 Same-vendor B-cluster reasoning-trace reframings.**
- §7.2 reasoning engages steel-man (per F-IC-4).
- §7.6 reasoning leads with comparison §5.5 ex-ante structural argument (per F-IC-5).
- §7.3.c clarifies workflow-template-side R-shift mechanism (per F-IC-6).
- §7.5 P5 reasoning specifies licensing argument distinct from "any first-target" (per F-IC-7).

**§7.9.6 Cross-references.** This audit folder; convergent C1 reconciliation; divergent C2 reconciliation per §2.1 + §2.2 above.

**Estimated addendum size.** ~80-120 lines. Substantial but bounded; mirrors SYNTHESIS-COMPARISON.md §7 audit addendum (~50 lines, smaller scope) at the disposition stage.

---

## §4. Pattern observations on M1 paired-review

Per premise-bleed audit precedent (DECISION-SPACE.md §1.17 lessons-distilled): paired cross-vendor + same-vendor pairing produces *complementary* findings rather than *redundant*. **This audit confirms the precedent.**

**Cross-vendor (codex) caught:** substantive-coherence between dispositions (F-IC-A2 §7.1 ↔ §7.3.a internal incoherence); dispatch-readiness gaps (F-IC-A3 / F-IC-A4 / F-IC-A6 / F-IC-A7); explicit-artifact contradictions (F-IC-A1 reasoning bullet 2 vs RELATIONSHIP-TO-PARENT.md plural-context discipline). Cross-vendor strength: substantive comparison across artifacts.

**Same-vendor caught:** register-shaped residuals at the dispositions themselves (F-IC-2 reasoning bullet 4 inversion; F-IC-8 disposition-record-header; F-IC-12 frontmatter); performative-vs-operational openness (F-IC-3 §7.7); steel-man under-engagement (F-IC-4 §7.2); reasoning-trace post-hoc-not-ex-ante (F-IC-5 §7.6); smuggled-shifts under disposition-clothing (F-IC-6 §7.3.c); framing-application-as-fact (F-IC-7 §7.5 P5). Same-vendor strength: register at meta-level + integration-grammar-as-fact at disposition stage.

**Convergent C1 (§7.4 substrate-shape-anchoring projection):** both vendor-positions caught the same axis at Class C, with complementary substrate (reasoning-bullet vs determining-assumption-layer). This is the M1 paired-review property in action: cross-vendor catches substance + same-vendor catches register at the same load-bearing axis with non-redundant evidence.

**Lesson for future audits.** Paired discipline at framing-load + decision-stake + cross-cutting + negative-space-depth audits remains warranted. Single-vendor (cross-vendor only OR same-vendor only) at this scale would have left half the audit-surface unexplored.

---

## §5. Disposition pathway

Per AUDIT-SPEC.md §8 (universal across audits in this trajectory plan):

1. **Logan reviews** audit-findings-A.md + audit-findings-B.md + this DIFFERENTIAL.md.
2. **Logan disposes** one of: commit-as-is / commit-with-addendum / revise-before-commit.
3. **Disposition recorded** at `DISPOSITION.md` in this audit folder.
4. **Disposition applied:**
   - Commit-as-is: no INCUBATION-CHECKPOINT.md or DECISION-SPACE.md §1.18 changes; commit Phase C atomic.
   - Commit-with-addendum: §7.9 addendum at INCUBATION-CHECKPOINT.md (per §3.5 above) + DECISION-SPACE.md §1.18 determining-assumption-2 reframe; commit Phase C atomic.
   - Revise-before-commit: re-disposition of affected axes (likely §7.4 + §7.3.a per F-IC-A1 + F-IC-A2 strong reading); Phase C cycle re-runs at affected axes; commit follows revision.

**Audit's non-binding signal (consolidated):** **Commit-with-addendum**, with the addendum shape per §3.5 above. Both auditors converge on this as the most-defensible path; revise-before-commit is defensible only under strong readings of F-IC-A1 / F-IC-A2; commit-as-is is defensible only if Logan reads the §7.8 list + §1.18 determining-assumption + Phase E re-adjudication hooks as already covering.

---

*Differential drafted 2026-04-29 by main-thread Claude (Opus 4.7) post-audit reading both audit-findings files. Per premise-bleed audit precedent, in-session-collaboration risk applies to differential analysis (Claude reading both audits); the differential's class-call reconciliations are Claude-shaped reads. Logan's disposition is binding; the DIFFERENTIAL.md surfaces for adjudication.*
