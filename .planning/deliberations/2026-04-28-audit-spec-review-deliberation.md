---
type: deliberation-log
date: 2026-04-28
session: post-comparison-draft + cross-vendor review of v1-GSD premise-bleed AUDIT-SPEC.md + revision-shape adjudication
status: adjudication-complete (Claude analysis §3; Claude-disposed per Logan authorization §5; revision-action table §6; awaiting Logan final-call before downstream actions — DECISION-SPACE.md §1.17 + revised AUDIT-SPEC.md)
ground: .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC-REVIEW.md (the cross-vendor review)
target_decision: .planning/gsd-2-uplift/DECISION-SPACE.md §1.17 (audit-methodology decision; section-number to be appended after §1.16)
related: .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md (the artifact under revision)
purpose: |
  Records the dynamics of the audit-spec-review-and-response cycle for the
  v1-GSD mental-model premise-bleed audit. Logan commissioned a cross-vendor
  GPT-5.5 xhigh review of Claude's draft AUDIT-SPEC.md. The review returned 7
  findings (4 Material / 2 Moderate / 1 Minor) with disposition
  "revise-before-dispatch." This log captures: the review's findings re-stated
  navigably (§2); Claude's per-finding analysis with assumptions, qualifications,
  and partial pushbacks rendered as transparently as possible (§3); cross-cutting
  observations on what the review demonstrates methodologically (§4); Logan's
  per-finding adjudication (§5, pending); resulting decisions on AUDIT-SPEC.md
  revisions (§6, derives from §5).

  Per the project's two-artifact pattern (DECISION-SPACE.md §1.10): this log
  carries the dynamics; DECISION-SPACE.md §1.17 carries the load-bearing
  decisions distilled from §5 + §6 of this log.
---

# Audit-spec review deliberation — v1-GSD premise-bleed audit

## §0. How to read

**For the review's findings**: §2 (re-stated tightly with line citations to AUDIT-SPEC-REVIEW.md).

**For Claude's analysis of the findings — the rendered-transparent reasoning Logan asked to record**: §3, organized per-finding with assumptions, qualifications, and partial pushbacks named explicitly.

**For cross-cutting methodological observations**: §4.

**For Logan's per-finding adjudication**: §5 (pending; placeholder structure ready for fill-in).

**For the resulting decisions on AUDIT-SPEC.md revisions**: §6 (derives from §5; populated after Logan adjudication).

**For cross-references**: §7.

**For the load-bearing decision form**: see DECISION-SPACE.md §1.17 (forthcoming; this log is its grounding).

## §1. Predecessor + scope

### §1.1 Predecessor

Claude drafted AUDIT-SPEC.md at 2026-04-28 ~11:42 (in-session response to Logan's premise-bleed concern; see SYNTHESIS-COMPARISON.md §4.4 + Logan's 2026-04-28 message registering the concern). Logan commissioned an independent cross-vendor review at GPT-5.5 xhigh; review landed at AUDIT-SPEC-REVIEW.md ~17:16. Disposition: **revise-before-dispatch**.

### §1.2 Scope of this log

- **In-scope.** The review's 7 findings; Claude's analysis; Logan's adjudication; resulting AUDIT-SPEC.md revision decisions; cross-cutting methodological observations.
- **Out-of-scope.** The premise-bleed audit's actual findings (those land at FINDINGS.md after the audit runs); §2.1 + §5 incubation adjudications on SYNTHESIS-COMPARISON.md (those are downstream); broader gsd-2-uplift initiative decisions outside audit methodology.

### §1.3 Why this matters

The audit-methodology decisions resulting from this deliberation shape:
- Whether the audit is single-step / two-step / three-step (vendor selection).
- What the audit can reach (slice-output sampling).
- How the audit detects bleed (vocabulary search + negative-space check).
- What grounding authority the audit rests on (prior-audit outputs / source-reading).
- How the audit's output is shaped (recommendation-shape vs disposition-signal).

These decisions are upstream of the §2.1 + §5 incubation adjudications (the audit's purpose is to surface premise-bleed before those adjudications). Mis-calibration here propagates into incubation. Hence load-bearing.

## §2. The 7 review findings (re-stated)

Re-stated tightly with line citations into AUDIT-SPEC-REVIEW.md. Full text and reasoning per finding lives in the review document; this section is for navigability.

### §2.1 Finding 1 (Material) — Same-vendor baseline is risky

`AUDIT-SPEC-REVIEW.md:20-31`. Same-vendor adversarial-auditor baseline cannot self-detect a Claude+Logan shared-frame failure (which is exactly the v1-GSD-bleed concern). Cites SYNTHESIS-COMPARISON.md §4.1 inversion observation as evidence the M1 register-vs-substance asymmetry is empirically more complex. Recommends switching baseline to cross-vendor high, OR two-step (same-vendor scan → cross-vendor adjudication of Class B/C).

### §2.2 Finding 2 (Material) — Excluding slice outputs prevents propagation proof

`AUDIT-SPEC-REVIEW.md:33-45`. The spec asks whether early framing propagated through slice prompts → synthesis (`AUDIT-SPEC.md:147-153`) but excludes slice outputs from scope (`AUDIT-SPEC.md:123-127`). Internal contradiction. Recommends targeted sampling (inspect slice-output sections only when Class B/C candidate appears upstream; cite verbatim; don't re-audit whole slices).

### §2.3 Finding 3 (Material) — Lens too vocabulary-weighted; add negative-space check

`AUDIT-SPEC-REVIEW.md:47-59`. Lens searches for v1-GSD vocabulary ("patcher", "skills", "hooks") but premise-bleed may operate through *omission* — artifact never says "patcher" but still under-weights session-control / headless / RPC / MCP / state-emission as primary intervention surfaces. Recommends required negative-space check: which runtime-application surfaces are absent or late despite being source-central?

### §2.4 Finding 4 (Material) — Corrected-frame imports imprecise replacement vocabulary

`AUDIT-SPEC-REVIEW.md:61-69`. Specific corrections:
- `--mode headless` → `gsd headless`; `--mode rpc` and `--mode mcp` are the mode surfaces.
- "vendored modified Pi fork" overstated; should be bounded to "GSD CLI/application layer built around vendored, modified Pi-derived packages."
- "core GSD is itself a Pi extension" should be source-backed claim, not all-purpose shortcut.

### §2.5 Finding 5 (Moderate) — Disposition authority + recommendation language conflict

`AUDIT-SPEC-REVIEW.md:71-77`. Spec says disposition is Logan's (`AUDIT-SPEC.md:81`) but output template asks auditor for "Recommendation shape" (`AUDIT-SPEC.md:176-185`); also says no revision suggestions (`AUDIT-SPEC.md:216-220`). Internal conflict. Recommends rename to "Non-binding disposition signal" with required justification per option.

### §2.6 Finding 6 (Moderate) — No-source-reading needs allowed grounding substitute

`AUDIT-SPEC-REVIEW.md:79-89`. Spec forbids gsd-2 source reading (`AUDIT-SPEC.md:154-160`) but the corrected-frame lens rests on source-grounded claims; auditor needs stable authority surface. Recommends allowing prior cross-vendor-codebase-understanding-audit's META-SYNTHESIS + GATE-2-DISPOSITION + relevant Wave 2 sections as grounding inputs.

### §2.7 Finding 7 (Minor) — Cost estimate optimistic; needs explicit read budget

`AUDIT-SPEC-REVIEW.md:91-99`. Spec estimate (30-60 min for 6 primary + 2 secondary) plausible only if sampling. Recommends explicit read budget per artifact (full / targeted / scan-only).

## §3. Claude's analysis (rendered transparent)

Per-finding analysis with assumptions, qualifications, and partial pushbacks made explicit.

### §3.1 Finding 1 — Strong agreement, with go-further-than-the-review recommendation

**Net read:** strong agreement; would extend the review's recommendation.

**Why agree.** Same-vendor catches register more readily, but cannot detect register the auditor *shares* with the audited artifact's author. v1-GSD-mental-model is exactly that case — Claude (spec author + comparison author) and Logan have shared exposure to v1-GSD vocabulary; same-vendor adversarial-auditor inherits that shared frame and cannot self-detect what it shares. The reviewer cites SYNTHESIS-COMPARISON.md §4.1's inversion observation, which is the right citation; my own paired-review analysis already documented that "same-vendor catches register" is empirically more complex than the M1 claim. Building the audit on a property the comparison itself documented as failing in this vendor pair is structurally incoherent.

**Why extend.** The reviewer offers two options: cross-vendor-only baseline OR two-step (same-vendor scan → cross-vendor adjudication). Both have residual problems:
- **Cross-vendor-only.** Codex doesn't natively know v1-GSD; the lens has to be constructed in the spec; the cross-vendor auditor reads under the spec's frame, not under independent grounding. Smaller version of same problem.
- **Two-step (same-vendor scan first).** Same-vendor cannot self-detect what it shares; the candidate list is filtered by the shared frame; cross-vendor adjudicates a narrower-than-it-should-be candidate set.

**My refined proposal:** three-step.
- **(i) Cross-vendor baseline pass** at GPT-5.5 high or xhigh. Codex generates independent first candidate list under a *minimal* lens-spec (just: "where do these artifacts under-weight runtime-application surfaces; cite verbatim"). Forbidden from reading the lens-rich version of the spec.
- **(ii) Same-vendor adversarial-auditor-xhigh second pass**, conditional on cross-vendor candidate list. Stress-tests cross-vendor candidates: does Claude reading the same artifacts under the same lens produce a different candidate set or different classifications?
- **(iii) Differential analysis.** Cross-vendor's candidates that same-vendor missed = highest-priority Class C-eligible (caught what same-vendor cannot). Same-vendor's candidates that cross-vendor missed = register-shaped catches that may still be valid (subtle in-house-vocabulary-leak codex doesn't recognize). Joint candidates = robustness-signaled.

**Cost trade-off.** Three-step ~2× the review's two-step (~1-2 hr cross-vendor + ~30-60 min same-vendor + ~30 min differential = ~2.5-3.5 hr total). For an audit specifically diagnosed as Claude+Logan shared-frame failure, the cost is justified.

**Salient situational factors.**
- (a) If premise-bleed is small-magnitude (probably-Class-A only), even cross-vendor-only is over-engineering.
- (b) If disposition-changing (Class C plausible), three-step is justified.
- (c) If incubation under wrong frame burns weeks of second-wave-scoping wrong, three-step is cheap.
- (d) If incubation under slightly-shifted starting position is correctable later, single-step cross-vendor is fine.

**Assumptions made explicit.**
- Treating v1-GSD-bleed as plausibly load-bearing for §2.1 (R4 disposition-timing — exactly where runtime-application weighting matters) and §5.2 (R-mix decomposition shape — depends on which surfaces are first-class).
- If Logan reads bleed as cosmetic, simpler audit shapes hold.

### §3.2 Finding 2 — Strong agreement with one qualifier

**Net read:** strong agreement.

**Why agree.** The spec's §1 motivation invokes propagation but §4 scope-bounds excluded slice outputs. Internal contradiction. Reviewer's targeted-sampling fix is the right resolution.

**Why originally excluded.** Worry about scope creep (slice outputs ~1437 lines combined) + audit-shape confusion (slice outputs were already audit-targeted in cross-vendor-codebase-understanding-audit; re-auditing risks substance-vs-register confusion). Both concerns real but neutralized by the reviewer's targeted-sampling fix.

**Qualifier.** Targeted-sampling rule needs a stop-condition. If propagation is investigated and the chain is "INITIATIVE.md → DECISION-SPACE.md → orchestration spec → slice prompt → slice output → audit → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON," sampling could cascade. Reviewer's recommendation says "do not re-audit the whole slice"; I'd add explicit cap: max 3-5 slice-output sections sampled per audit run. Hard cap prevents auditor walking into substance-audit territory.

**Salient situational factors.**
- (a) If Class B/C candidates appear at framing-widening / DECISION-SPACE / INITIATIVE level (upstream), propagation sampling fires for slice prompts + outputs.
- (b) If Class B/C appears only at SYNTHESIS-COMPARISON.md level (downstream), propagation sampling unnecessary (bleed didn't propagate; localized).
- (c) If no Class B/C candidates, no sampling fires.

### §3.3 Finding 3 — Strong agreement; this is the review's most important methodological catch

**Net read:** strong agreement; no qualification.

**Why agree.** Searching for v1-GSD vocabulary catches the *visible* form of premise-bleed. Reviewer correctly identifies that bleed can also operate through omission. This is exactly the failure mode the spec couldn't detect because the lens was searching for what was said, not for what was absent.

**Honest acknowledgment of methodological error in draft.** §2 lens-questions (a)-(g) include item (b) "under-weighting" and item (g) "under-weighting," but §5.2 audit method described "vocabulary scan" + "surface-weighting check" + "question-shape check" + "implication check" — none operationalized as negative-space queries. The lens-questions named the right targets; the method didn't operationalize how to find them. Reviewer's negative-space check shape ("which runtime-application surfaces are absent or late despite being source-central?") fixes this directly.

**Salient situational factor.** Negative-space checking requires the auditor to have a stable reference frame for "what surfaces are source-central enough that absence-is-meaningful." This couples to finding 6 (allowed grounding inputs) — without grounding-substitute, negative-space check rests on the auditor's own constructed model of what gsd-2 has, which reintroduces shared-frame risk.

### §3.4 Finding 4 — Agreement on principle; partial qualification on specifics

**Net read:** agreement on principle (audit about vocabulary precision should not replace one over-compressed mental model with another); qualification on specifics.

**Specifics analysis.**
- **`gsd headless` vs `--mode headless`.** Accept the correction provisionally; flag it. I wrote `--mode headless` from memory of slice-3 outputs; haven't verified. Reviewer corrected from prior-audit grounding (which couples to finding 6). **Salient factor:** if prior audit was wrong here, revision propagates wrong correction. Low-probability concern; accept correction with awareness.
- **"vendored modified Pi fork" overstated.** Strong agreement. Phrasing under-emphasizes that GSD-2 is a CLI/application *built around* vendored Pi-derived packages, not just-the-fork. Reviewer's tighter formulation more accurate. Note SYNTHESIS-CROSS.md §0 uses similar language; my spec inherited it; both imprecise in same direction.
- **"core GSD is itself a Pi extension" overstated.** Partial pushback. SYNTHESIS.md F6 + slice 4 audit §5 do source-back the claim that core GSD uses extension machinery; reviewer's correction ("source-backed architecture claim, not all-purpose shortcut") is right that I wrote it as if it were a load-bearing inference for R2 viability, but the underlying claim *is* source-grounded. Fix: qualify the *use* of the claim, not retreat from it.

**Where I'd push back partially.** Reviewer offers corrections without offering replacement language. For an audit about vocabulary precision, the spec should carry vetted replacement language, not just "be more careful." Otherwise the auditor inherits "be more careful" and constructs its own replacements (reintroduces original problem).

**My add.** When revising, include explicitly-vetted replacement vocabulary in §2 (lens definition), with citations to source-of-grounding (META-SYNTHESIS or specific source files). More work; load-bearing for finding 3 (negative-space check) which requires stable reference frame.

### §3.5 Finding 5 — Strong agreement, with framing nuance

**Net read:** strong agreement.

**Why agree.** Internal contradiction in spec: §6 output-template asks for "Recommendation shape" while §0 / §5.4 / §8 say disposition is Logan's and revision suggestions are out of scope. Reviewer's rename ("Non-binding disposition signal") with required per-option justification is the clean fix.

**Framing nuance.** The conflict crept in because I was imitating the codebase-understanding audit's GATE-1 / GATE-2 disposition shape, which has gates *internal to the audit*. For a single-pass premise-bleed audit, "Recommendation shape" is over-loaded — it conflates Logan-disposition (Logan owns) with auditor's read of which disposition is *plausible* (auditor can helpfully signal). Reviewer's rename captures this distinction.

### §3.6 Finding 6 — Agreement on principle; substantive partial pushback on specifics

**Net read:** agreement on principle (auditing premise-bleed under corrected frame requires *something* to ground the corrected frame; otherwise circularity); substantive partial pushback on specifics.

**Why agree on principle.** If auditor's only authority for "what GSD-2 is" is the spec itself, the spec carries the lens and the auditor inherits it. Reviewer's allowed-grounding-substitute is structurally needed.

**Substantive pushback on specifics.** Reviewer suggests three grounding inputs (META-SYNTHESIS / GATE-2-DISPOSITION / Wave 2 adjudications from cross-vendor-codebase-understanding-audit). Concern: that audit was *also* shaped by Claude+Logan's shared frame (Claude+Logan dispatched it; lens constructed in its AUDIT-PLAN.md). If it inherited even partial v1-GSD framing, its META-SYNTHESIS / GATE-2-DISPOSITION inherits it; using as grounding substitute *re-imports* shared-frame risk into the premise-bleed audit. Reviewer recommends grounding drawn from artifacts that may share the same potential bleed.

**Where I'd push back partially.** Before accepting these grounding inputs, want to verify that codebase-understanding audit was *itself* substantially cross-vendor-grounded (which it was — it was the cross-vendor audit) AND that its META-SYNTHESIS makes claims at the level needed (runtime-application surfaces, not just substance facts). If prior audit's META-SYNTHESIS asserts what GSD-2 is at substance level (package identity; vendored Pi packages; ADR-010 status), it's safer grounding than if it inherits same surface-weighting we're auditing.

**My alternative or addition.** Rather than adopting only prior audit's outputs as grounding, allow auditor to consult **gsd-2 source directly for narrow factual queries** when grounding a corrected-frame claim. Hard cap: max 5 file reads, only for fact-grounding (not architectural inference), citation required. Preserves no-substance-re-audit while giving auditor fall-back authority that doesn't re-import shared-frame risk.

**Salient situational factor.** If prior cross-vendor audit's META-SYNTHESIS is robust against v1-GSD-bleed (cross-vendor codex caught what same-vendor would miss), reviewer's grounding inputs are fine and source-reading isn't needed. If prior audit shares the bleed, source-reading provides independent check.

**Cost.** Adding "narrow source-reading allowed for fact-grounding only" adds ~5-10 minutes auditor time per fact-grounded claim. Modest.

### §3.7 Finding 7 — Agreement, with small caveat

**Net read:** agreement.

**Why agree.** §10 estimate sloppy. Assumed sampling-not-full-read but didn't say so. Reviewer's recommendation (full / targeted / scan-only per artifact) is the right discipline.

**Caveat.** Read-budget interacts with finding 2 (targeted slice-output sampling) — if propagation sampling fires, read budget expands. Spec should name this conditional explicitly: base read budget X; if propagation sampling fires, add Y per slice sampled (max 3-5 per finding 2's cap).

## §4. Cross-cutting observations

### §4.1 Most load-bearing finding

Finding 1 (auditor selection) is most load-bearing because it's structural — changes the audit's epistemic foundation. Findings 2, 3, 5, 7 are operational refinements. Findings 4, 6 are vocabulary/grounding precision. If only one finding could be addressed, it would be finding 1.

### §4.2 Internal coherence of the review

The review is internally consistent: findings 1 (vendor) + 3 (negative-space) + 6 (grounding) form a coherent triad — all address "what stable independent reference frame can the auditor anchor to." Finding 2 (slice-output sampling) addresses "what evidence base can the auditor reach without scope creep." Findings 4, 5, 7 are localized fixes. Review's structure mirrors my draft's structure (lens / method / scope / output) and addresses the right load points.

### §4.3 Where the review is silent

Doesn't address §9 conditional structure (meta-consideration; reasonable to leave alone). Doesn't propose alternative output shapes (frontmatter / FINDINGS.md format) — reasonable to leave alone since working. Doesn't address §8 disposition pathway — but finding 5 implicitly does (separates auditor's signal from Logan's disposition).

### §4.4 Methodological reflection — M1 cross-vendor catching what same-vendor missed

This review is itself an instance of M1 cross-vendor catching what same-vendor missed. Claude drafted the spec; review caught seven things. SYNTHESIS-COMPARISON.md §4.1 documented that M1's register-vs-substance asymmetry is empirically more complex; this review reinforces that — what cross-vendor caught is methodological-discipline (vendor selection; negative-space; vocabulary precision), which crosses register/substance. Logan was right to commission this review; the spec was substantially weaker than Claude assessed it to be at time of writing.

### §4.5 Downstream signal on §2.1 R4 disposition-timing typology

Reviewer's finding 1 cites SYNTHESIS-COMPARISON.md §4.1 specifically. Direct downstream signal: the comparison's M1-mixed observation is being treated as load-bearing methodological evidence by an independent reader. Small calibration on how much weight Claude's own §4.1 carries — Logan now has external corroboration that the M1 inversion observation isn't just Claude-interpretation but is operationally consequential.

### §4.6 Honest acknowledgment

The spec was structurally weaker than Claude drew it to be. Review is a substantively better-calibrated read of what this audit needs than the original draft was. Worth revising per all 7 findings before dispatch. Not worth defaulting to original draft on cost-saving grounds.

### §4.7 Operational scale of revision

Revised spec closer to major rewrite than minor patch. Finding 1 alone changes auditor selection; finding 3 changes method; finding 6 changes scope; finding 4 changes lens vocabulary. Estimated ~50-70% spec content survives unchanged; ~30-50% needs rewriting.

## §5. Per-finding adjudication

**Adjudication authorization.** Logan authorized Claude to perform the per-finding adjudication and write the disposition (2026-04-28 message: "can you perform the per-finding adjudication on the 7 findings? and write the disposition."). Per the in-session-collaboration discipline (analogous to SYNTHESIS-COMPARISON.md §6.3 caveat): Logan retains final-call-on-the-call before downstream actions land (DECISION-SPACE.md §1.17 + revised AUDIT-SPEC.md). Each disposition below includes "where Logan might choose differently" so the call remains auditable and revisable.

### §5.1 Finding 1 (auditor selection) — Disposition: cross-vendor baseline + conditional same-vendor stress

**Disposition.** Two-step conditional. **(Step 1)** Cross-vendor codex GPT-5.5 high baseline pass under minimal lens-spec; codex generates independent first candidate list; codex forbidden from reading the lens-rich version of the spec. **(Step 2 — conditional)** If cross-vendor returns any Class C candidates, fire same-vendor adversarial-auditor-xhigh stress pass over the same artifacts under the same lens; produce differential analysis (cross-vendor candidates same-vendor missed = highest-priority Class C-eligible; same-vendor candidates cross-vendor missed = register-shaped catches; joint candidates = robustness-signaled). If cross-vendor returns only Class A/B candidates, no stress pass — audit's purpose was satisfied at lower cost.

**Note.** Disposed by Claude per Logan's authorization. This is between the reviewer's two-step (always run both) and Claude's three-step (always run all three): same-vendor stress is conditional on cross-vendor returning Class C. Adapts cost to evidence.

**Rationale.**
- Same-vendor-only is structurally incoherent for shared-frame failure (per F1 reasoning + SYNTHESIS-COMPARISON.md §4.1). Eliminate.
- Cross-vendor-only baseline is the audit's structural floor — the cross-vendor reader is the one who can detect shared Claude+Logan framing.
- Same-vendor stress adds value only if cross-vendor surfaces something Claude reading might re-classify or supplement. If cross-vendor returns Class A only, same-vendor stress likely catches subtle register-shaped items but they're below load-bearing-ness threshold; not worth the dispatch.
- Conditional escalation matches the project's existing per-slice-W2-audit-disposition discipline (DECISION-SPACE.md §1.12 B2): pre-commit to floor + escalate on evidence.

**Where Logan might choose differently.**
- (a) If Logan reads bleed concern as cosmetic Class-A-only, drop to cross-vendor-only single-step (no conditional).
- (b) If Logan reads bleed as definitively load-bearing, force three-step (Claude's extension; same-vendor stress always runs) for higher robustness.
- (c) If Logan distrusts conditional dispositions (per DECISION-SPACE.md §1.12 "If you'd rather not maintain per-slice audit-disposition decisions"), pre-commit to two-step always.
- (d) Cost-binding alternative: cross-vendor-only single-step regardless of Class C return; revise post-hoc if findings warrant.

**Logan post-disposition confirmation (2026-04-28 follow-up).** Logan affirmed conditional shape — explicitly *not* pre-committing — with the noted reservation that "there might be other reasons why we might want to do a same-vendor adversarial audit." Resolved by adding **manual-escalation discretion** to AUDIT-SPEC.md §3.4: Class-C trigger is the default-firing-condition (not the only firing condition); Logan retains discretion to fire Step-2 manually for other reasons (independent cross-checking; prior-audit calibration; cluster-of-non-Class-C concerning patterns; cheap-to-add resource availability). Disposition shape unchanged at the conditional-default level; surface for manual escalation made explicit.

**Revision implication for AUDIT-SPEC.md.**
- §3 Auditor selection: rewrite to specify two-step-conditional shape (cross-vendor baseline; same-vendor stress on Class C); preserve forbidden-reading list scoped per step.
- §3.4 Step-2 (post-Logan-confirmation): add manual-escalation discretion note.
- §5 Audit method: split into Step-1 method (cross-vendor independent pass) + Step-2 method (same-vendor stress pass with cross-vendor candidate list as input + differential analysis).
- §6 Output shape: single FINDINGS.md if Step-1-only; two-section FINDINGS.md (Step-1 candidates + Step-2 differential) if escalated.
- §10 Cost estimate: ~1-1.5 hr Step-1; +30-60 min Step-2 if escalated; +30 min differential.

### §5.2 Finding 2 (slice-output sampling) — Disposition: accept + hard-cap

**Disposition.** Accept reviewer's targeted-sampling rule + Claude's hard-cap qualifier. Sampling rule: if a Class B/C candidate appears in a primary or secondary artifact (§4 of AUDIT-SPEC.md), inspect the corresponding slice-output section to determine whether premise actually propagated; cite verbatim; do not re-audit whole slices. Hard cap: max 3-5 slice-output sections sampled per audit run total.

**Note.** Disposed by Claude per Logan's authorization. Hard-cap added to prevent cascading sampling that walks audit into substance-territory.

**Rationale.**
- Reviewer's fix correctly resolves spec's internal contradiction (motivation invokes propagation; scope excluded slice outputs).
- Hard-cap is a small but real protection: without it, an over-eager auditor could sample 10+ sections chasing propagation chains, exceeding bounded-audit scope.
- 3-5 cap aligns with §6 output-shape constraint (200-500 line FINDINGS.md); more samples than that exceed output budget.

**Where Logan might choose differently.**
- (a) Drop hard-cap entirely if Logan trusts auditor's calibration on bounded sampling.
- (b) Tighter cap (max 2) if Logan prioritizes scope discipline over propagation completeness.
- (c) Replace cap with discretion-then-defer: auditor flags propagation chains exceeding 5 samples as "partial coverage; full-trace requires substance-audit follow-up" — surfaces gap rather than capping.

**Revision implication for AUDIT-SPEC.md.**
- §4 Scope: move slice outputs from "out of scope" to "targeted-sampling allowed under §5.2 method"; explicit hard-cap.
- §5.2 Per-artifact pass: add new sub-step "(5) Propagation sampling — fires only when Class B/C candidate appears upstream; max 3-5 slice-output sections per audit run; cite verbatim; do not re-audit."

### §5.3 Finding 3 (negative-space check) — Disposition: accept + couple to F6 grounding

**Disposition.** Accept reviewer's negative-space check as a required method step. Add as new §5.2 sub-step: for each artifact, ask (i) which runtime-application surfaces are absent or late despite being source-central (per F6 grounding); (ii) does artifact's question order make skills/workflow markdown easy to see and runtime-application surfaces harder to see; (iii) does artifact treat R4 as add-on despite headless/RPC/MCP being first-class GSD-2 surfaces. The negative-space check is *required*, not optional. Reference frame for "source-central surfaces" comes from F6 grounding inputs (per the coupling Claude's §3.3 flagged).

**Note.** Disposed by Claude per Logan's authorization. This is the review's most important methodological catch (per §4.1).

**Rationale.**
- Vocabulary-only lens catches what was *said*, not what was *omitted*. Premise-bleed via omission is exactly the failure mode Logan's premise-correction concern flagged.
- Acknowledged honestly in §3.3: spec's lens-questions named the right targets but method didn't operationalize how to find them. Reviewer's negative-space check fixes this directly.
- Couples to F6 because negative-space check requires a stable reference for "what surfaces are source-central enough that absence-is-meaningful." Without that reference, auditor constructs the model itself, which reintroduces shared-frame risk.

**Where Logan might choose differently.**
- (a) Accept as optional sub-step (auditor uses if relevant rather than required) — lower coverage but lighter audit.
- (b) Frame negative-space check at cross-artifact level only (§5.3 propagation pass) rather than per-artifact (§5.2) — focuses on systemic patterns over local instances.

**Revision implication for AUDIT-SPEC.md.**
- §5.2 Per-artifact pass: add new sub-step "(2.5) Negative-space check — required" with the three sub-questions verbatim.
- §2 Lens definition: cross-reference negative-space check + F6 grounding to make the coupling explicit.

### §5.4 Finding 4 (vocabulary corrections) — Disposition: accept all three + vetted-replacement extension

**Disposition.** Accept all three corrections + Claude's vetted-replacement-language extension. Specific actions:
- (a) `--mode headless` → `gsd headless`; `--mode rpc` and `--mode mcp` are the mode surfaces. Replace in §2 lens definition.
- (b) "vendored modified Pi fork" → "GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled, but the whole repo is broader than that fork." Replace in §2.
- (c) "core GSD is itself a Pi extension" → qualify use as source-backed architecture claim citing slice 4 audit §5 + SYNTHESIS.md F6; not all-purpose shortcut for third-party extension viability. Edit in §2 + any other §X references.
- (d) Vetted-replacement-language extension: §2 includes explicit replacement vocabulary for each corrected item, with citations to META-SYNTHESIS or specific source files (per F6 grounding inputs). The auditor inherits vetted vocabulary, not "be more careful."

**Note.** Disposed by Claude per Logan's authorization. (a) accepted with awareness that correction itself depends on prior-audit accuracy (low-probability concern). (c) accepted with Claude's nuance — qualify use, don't retreat from claim.

**Rationale.**
- Reviewer's meta-point (audit about vocabulary precision shouldn't replace one over-compressed model with another) is structurally correct.
- (a) corrects a Claude-inherited compression from slice-3 memory; verified via reviewer's prior-audit grounding.
- (b) corrects an inherited compression from SYNTHESIS-CROSS.md §0; both syntheses imprecise in same direction.
- (c) preserves source-grounded claim (slice 4 audit §5 + F6) but qualifies its rhetorical use.
- (d) Claude's vetted-replacement extension is necessary because "be more careful" alone reintroduces the original problem (auditor constructs replacements; inherits compression-shape).

**Where Logan might choose differently.**
- (a) Accept (a)+(b)+(c) without (d) (vetted-replacement) if Logan trusts auditor calibration on vocabulary precision under "be more careful" instruction alone — lighter spec; higher inheritance risk.
- (b) Reject (c)'s nuance if Logan reads "core GSD is itself a Pi extension" as substantively unverified — full retreat rather than use-qualification.
- (c) Defer (a)/(b)/(c) to post-audit if auditor's findings reveal additional vocabulary issues — combine corrections.

**Logan post-disposition confirmation (2026-04-28 follow-up).** Logan asked clarifying questions about the lookup-table mechanics ("how does that work? is it automated?") and proposed adding a meta-comment about "being careful." Resolved with both:
- **Lookup mechanics confirmed** (not automated; reference-not-substitution): the auditor reads §2.1 + §2.2 + §2.3 in pre-audit framing read; encounters v1-GSD-shaped phrasings while reading audited artifacts; consults the lookup to articulate the corrected framing in FINDINGS.md "Justification" sections; cites the corrected framing's source-of-grounding (per §4.2). The lookup yields consistency-across-FINDINGS.md (three findings citing the same v1-GSD-shaped phrasing articulate the corrected frame the same way) + audibility (Logan can audit the lookup-table calibration separately from auditing FINDINGS) + citation chain (each lookup row's grounding citation propagates to FINDINGS).
- **Meta-discipline note added** to AUDIT-SPEC.md §2.3: "The lookup is a reference, not a substitute for vocabulary-precision judgment. The auditor should... carry the discipline of *not constructing new compressions on the fly* into any phrasing not covered by the lookup; if a phrase recurs in the audited artifacts that should plausibly be on the lookup but isn't, flag in FINDINGS §4 self-flagged-concerns rather than inventing replacement language." Combines lookup-specificity with reviewer's "be careful" meta-instruction. Closes the gap where lookup doesn't enumerate every possible v1-GSD-shaped phrasing.

**Revision implication for AUDIT-SPEC.md.**
- §2 Lens definition: rewrite "gsd-2 as it actually is" subsection with vetted-replacement vocabulary + explicit citations per item; add sub-section "Replacement vocabulary lookup" listing each correction with source-of-grounding.
- §2.3 (post-Logan-confirmation): add meta-discipline note bridging lookup-coverage with general vocabulary-precision discipline for phrasings the lookup doesn't enumerate.

### §5.5 Finding 5 (recommendation-shape rename) — Disposition: accept rename + per-option justification

**Disposition.** Accept reviewer's rename: "Recommendation shape" → "Non-binding disposition signal." Add required per-option justification: auditor states *why* Logan might choose each plausible disposition (commit-as-is / commit-with-addendum / revise-before-commit) given the findings; auditor does not pick one. Actual disposition lives in DISPOSITION.md as spec already says (`AUDIT-SPEC.md:241-250`).

**Note.** Disposed by Claude per Logan's authorization. Clean fix; no qualifier needed.

**Rationale.**
- Reviewer correctly identified internal contradiction. Rename + justification-requirement separates auditor's signal (helpful: which dispositions are plausible given findings) from Logan's disposition (binding: which Logan chooses).
- Aligns with framing-widening §3.3 disposition-discipline — Claude/auditors surface; Logan disposes.

**Where Logan might choose differently.**
- (a) Drop the section entirely; auditor produces only findings, no disposition signal — minimal output; cleanest separation.
- (b) Keep "Recommendation shape" name + accept Logan-binding-not-auditor disclaimer in spec — minor cleanup without rename.

**Revision implication for AUDIT-SPEC.md.**
- §6 Output shape: rename "Recommendation shape:" to "Non-binding disposition signal:"; add format requirement for per-option justification (commit-as-is / commit-with-addendum / revise-before-commit, each with auditor's reasoning for why Logan might choose it).
- §0 / §5.4 / §8 cross-references: update references to align with rename.

### §5.6 Finding 6 (grounding inputs) — Disposition: accept reviewer + Claude's narrow-source-reading

**Disposition.** Both grounding sources allowed, in priority order. **(Primary)** Prior cross-vendor-codebase-understanding-audit outputs: META-SYNTHESIS.md, GATE-2-DISPOSITION.md, relevant Wave 2 adjudication sections — auditor reads as primary grounding for "what GSD-2 actually is." **(Secondary, fallback)** Narrow source-reading: max 5 gsd-2 source file reads per audit run; only for fact-grounding when prior-audit grounding doesn't cover a specific claim; citation required (file:line); not for architectural inference. Auditor uses prior-audit-first; falls back to source-reading only when prior-audit doesn't ground a needed claim.

**Note.** Disposed by Claude per Logan's authorization. Hybrid resolves Claude's §3.6 partial pushback (prior-audit may share v1-GSD bleed → use it but don't depend on it alone) without forcing source-re-audit (which would push into substance territory).

**Rationale.**
- Reviewer's principle is correct: auditor needs stable authority surface for corrected-frame claims.
- Reviewer's prior-audit-only inputs have residual shared-frame risk (Claude+Logan dispatched the codebase audit; lens construction inherited some framing).
- Source-reading-only is heavier (re-opens substance work) but fully independent.
- Hybrid (prior-audit-first + narrow-source-reading-fallback) gets best of both: leverages prior audit's substantial work; preserves independent fall-back when needed.
- Hard cap on source-reading (max 5; fact-grounding only) maintains scope discipline.

**Where Logan might choose differently.**
- (a) Reviewer's prior-audit-only (no source-reading) if Logan reads codebase audit as fully cross-vendor-grounded and trusts its META-SYNTHESIS as authoritative — simpler; faster.
- (b) Source-reading-only (no prior-audit) if Logan reads codebase audit as too potentially-shared-frame to ground premise-bleed audit — heavier but cleanest independence.
- (c) Tighter source-reading cap (max 2-3) if Logan prioritizes scope-discipline over independence-fallback.
- (d) Looser cap or no cap if Logan reads source-reading as more important than I do.

**Logan post-disposition follow-up — verification + soft-cap-with-overflow + META-SYNTHESIS integration (2026-04-28).** Logan pushed on three points: (i) (a-verify) pre-confirmation: read META-SYNTHESIS to verify coverage of runtime-application surfaces before locking hybrid; (ii) max-5 cap is universalizing without checking actual need — "should it be soft max 5 as guideline and then flexibility depending on the situation?"; (iii) what is the cap applied to specifically.

**META-SYNTHESIS verification result.** Coverage is substantial and proportional: §1 explicitly names plural runtime surfaces (CLI/TUI, headless/RPC, in-process MCP, standalone MCP, RPC client); §2 item 1 provides corrected "vendored modified Pi fork" replacement; §2 item 2 provides typed labels (`gsd --mode mcp` / `@gsd-build/mcp-server` / `gsd headless` / `--mode rpc`); §2 item 3 provides seven-category typed extension-surface vocabulary (richer than my four-subsystem framing); §3 lists seven prohibited articulations; §5 explicitly elevates R4 ("should remain explicit; headless/RPC/MCP and external orchestration surfaces should not be forced into R2 vocabulary"). META-SYNTHESIS does substantial runtime-application-surface foregrounding work the premise-bleed audit's negative-space check needs.

**Three refinements applied.**
- **Refinement 1: soft-cap-with-overflow** (replaces hard-cap-5). Default ~5 source-reads; overflow protocol requires auditor to flag + justify in FINDINGS §4 (count exceeded; per-read fact-grounding-vs-architectural-inference justification; findings grounded). Logan disposes overflow per §8 (accept / reclassify / reject). Evidence-adaptive shape (analogous to F1 conditional escalation); preserves discipline marker without hard ceiling.
- **Refinement 2: META-SYNTHESIS §2 item 3 typed vocabulary cited as canonical** in §2.3 lookup row 1 (replaces my four-subsystem framing). Seven-category typing is richer and pre-vetted. §2.3 row "vendored modified Pi fork" cites META-SYNTHESIS §2 item 1 carry-forward; row "`--mode headless`" cites META-SYNTHESIS §2 item 2 carry-forward labels.
- **Refinement 3: META-SYNTHESIS §3 prohibited articulations referenced** in §2.3 as complementary discipline list. Seven explicit "do not use" patterns the auditor cites verbatim when finding analogous claims in audited artifacts.

**The cap-applies-to clarification.** The soft-cap applies *only* to gsd-2 source-code file reads under the §4.2 fallback grounding clause. NOT to: reading audited artifacts (§10.1 read budget); reading prior-audit grounding inputs (§4.2 primary; auditor reads as needed); slice-output sampling (§5.2.5 has its own separate cap of 3-5 sections per audit run). Universalization concern resolved: the cap was specific scope-discipline marker for source-reading-as-substance-territory-door, not generic restriction.

**Revision implication for AUDIT-SPEC.md.**
- §4.2 Grounding: hard-cap-5 → soft-cap-with-overflow + Logan-disposition protocol; META-SYNTHESIS coverage expectation note (fallback fires rarely).
- §2.3 Lookup: cite META-SYNTHESIS §2 item 1/2/3 as canonical sources; add prohibited-articulations sub-section citing META-SYNTHESIS §3 with seven explicit patterns.
- §5 Audit method: cross-references to refined §4.2 + §2.3 stand.
- Cross-reference to F3 (negative-space check requires this grounding) + F4 (vetted replacement vocabulary cites these sources).

### §5.7 Finding 7 (read budget) — Disposition: accept + conditional-budget caveat

**Disposition.** Accept reviewer's read-budget shape with Claude's conditional-budget extension. **(Base budget)** Full read: INITIATIVE.md, SYNTHESIS-COMPARISON.md §0/§2/§5/§6, SYNTHESIS-CROSS.md §0/§5/§6. Targeted read: DECISION-SPACE.md, SYNTHESIS.md, framing-widening.md (specific sections per lens-relevance). Scan only: orchestration preamble, slice prompts, synthesis/audit specs (unless propagation-sampling fires per F2). **(Conditional add-on)** If propagation-sampling fires per F2, add ~10-15 min per slice-output section sampled (max 3-5 per F2 cap). **(Step-2 add-on)** If same-vendor stress pass fires per F1, add ~30-60 min for stress pass + ~30 min for differential analysis.

**Note.** Disposed by Claude per Logan's authorization. Conditional add-ons make the budget honest about scope-expansion paths.

**Rationale.**
- Reviewer's full/targeted/scan-only shape is the right discipline.
- Spec's original 30-60 min estimate was sloppy (assumed sampling-not-full-read but didn't say so).
- Conditional add-ons match the F1 + F2 conditional dispositions: total budget depends on what gets escalated.

**Where Logan might choose differently.**
- (a) Tighter base (drop SYNTHESIS-CROSS.md §0/§5/§6 to targeted-only) if Logan reads cross-vendor synthesis as less central than same-vendor — saves ~20-30 min.
- (b) Looser base (full-read DECISION-SPACE.md, SYNTHESIS.md) if Logan reads these as more central than my targeting suggests — adds ~30-60 min.
- (c) Drop conditional add-ons and use single base budget regardless of escalation — simpler but less honest about cost.

**Revision implication for AUDIT-SPEC.md.**
- §10 Cost estimate: rewrite with explicit per-artifact read-mode (full / targeted / scan-only) + conditional add-ons (propagation-sampling per F2; same-vendor stress per F1).

## §6. Resulting AUDIT-SPEC.md revision decisions

*Distilled from §5 per-finding adjudications. Each row maps an adjudication to concrete revision actions in AUDIT-SPEC.md. Subject to Logan's final-call-on-the-call before revisions land.*

| Finding | Adjudication | AUDIT-SPEC.md section affected | Concrete revision action |
|---|---|---|---|
| F1 (vendor) | Two-step conditional: cross-vendor baseline + same-vendor stress on Class C | §3, §5, §6, §10 | Rewrite §3 to specify two-step-conditional shape; split §5 into Step-1 + Step-2 method; §6 output-shape allows single or two-section FINDINGS.md per escalation; §10 cost estimate base + Step-2 add-on |
| F2 (slice sampling) | Accept reviewer's targeted-sampling + Claude's hard-cap (max 3-5 sections) | §4 (scope), §5.2 (method) | Move slice outputs from out-of-scope to targeted-sampling-allowed under §5.2; explicit hard-cap; new §5.2 sub-step "(5) Propagation sampling" |
| F3 (negative-space) | Accept reviewer's negative-space check; required not optional; couple to F6 grounding | §5.2 (method), §2 (lens cross-ref) | Add new §5.2 sub-step "(2.5) Negative-space check — required" with three sub-questions verbatim; §2 cross-references negative-space + F6 grounding coupling |
| F4 (vocabulary) | Accept all three corrections + Claude's vetted-replacement-language extension | §2 (lens) | Rewrite "gsd-2 as it actually is" sub-section with vetted-replacement vocabulary + explicit citations per item; add "Replacement vocabulary lookup" sub-section |
| F5 (rec-shape rename) | Accept rename to "Non-binding disposition signal" + per-option justification requirement | §6 (output), §0/§5.4/§8 (cross-refs) | Rename §6 "Recommendation shape:" → "Non-binding disposition signal:"; add per-option justification format; update cross-references |
| F6 (grounding) | Hybrid: prior-audit grounding (META-SYNTHESIS + GATE-2 + Wave 2) primary + narrow source-reading (max 5 reads, fact-grounding only) fallback | §4 (scope), §5 (method) | Split §4 out-of-scope into hard exclusions + conditional inclusions; add §5 sub-step on grounding-input usage; cross-reference to F3 + F4 |
| F7 (read budget) | Accept reviewer's full/targeted/scan-only + Claude's conditional add-ons (propagation per F2; Step-2 per F1) | §10 (cost) | Rewrite §10 with explicit per-artifact read-mode + conditional add-ons (~10-15 min per slice-output sampled; ~30-60 min for Step-2 stress; ~30 min for differential) |

**Cross-cutting revision implications.**

- **Spec scope of revision.** Estimated ~30-50% rewrite as predicted in §4.7 — finding 1 (vendor) restructures §3/§5/§6/§10; finding 4 (vocabulary) rewrites §2 lens definition; finding 6 (grounding) rewrites §4 scope; findings 2/3 add new method sub-steps; findings 5/7 are localized.
- **Spec coupling.** F1 (vendor) + F3 (negative-space) + F6 (grounding) form the triad Claude flagged in §4.2; revisions to these three should be cross-referenced internally so the auditor reads them as a coherent epistemic infrastructure.
- **Spec cost.** Revised audit-time budget (per F7 disposition): ~1-1.5 hr base (Step-1 cross-vendor only); +30-60 min if Step-2 fires (Class C in Step-1); +30 min differential if Step-2 ran; +10-15 min × N (max 3-5) per slice-output sampling fires. Total range: 1-3 hours depending on escalation.
- **Spec-revision authoring time.** Estimated ~45-90 min Claude-time to apply all 7 revisions + cross-link.
- **Spec-revision review.** After Claude revises, surface to Logan for review. If Logan disposes the revisions land, AUDIT-SPEC.md commits as a revision; deliberation log + DECISION-SPACE.md §1.17 commit alongside; auditor dispatch follows.

**Adjudication uncertainty notes (where Claude's call is least confident).**

- **F1 conditional escalation shape.** The "fire Step-2 only on Class C" condition is a judgment call. If Logan reads it as evidence-adaptive (good), accept. If Logan reads it as adding operational burden without clear payoff, simplify to cross-vendor-only single-step or pre-commit two-step.
- **F4 vetted-replacement extension.** Adding explicit replacement vocabulary in §2 is more work than reviewer recommended; if Logan reads "be more careful" as sufficient discipline, drop the extension.
- **F6 narrow source-reading hybrid.** Adding source-reading as fallback creates a small substance-territory door. If Logan distrusts that door, drop to prior-audit-grounding-only.

## §7. Cross-references

**Predecessor artifacts.**
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` — Claude's draft (the artifact under audit).
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC-REVIEW.md` — GPT-5.5 xhigh review (the review under deliberation).
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §4.1 — M1 paired-review property observation that the review cites; predecessor methodological observation.
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §4.4 — framing-import drift methodological observation that motivated the audit.

**Methodological ground.**
- METHODOLOGY.md M1 (paired-review register-vs-substance asymmetry) at `:104-115`.
- LONG-ARC.md anti-patterns (closure pressure; framing-leakage).
- DECISION-SPACE.md §1.10 — two-artifact pattern (deliberation log + decision reference) that this log instantiates.
- DECISION-SPACE.md §1.13 — vendor-scope discipline (cross-vendor for substance; same-vendor for register; paired escalation).

**Adjacent audits.**
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/` — substance audit (codebase-understanding); orthogonal to this premise-bleed framing audit; finding 6 references its META-SYNTHESIS + GATE-2 + Wave 2 outputs as proposed grounding inputs.

**Forthcoming.**
- `.planning/gsd-2-uplift/DECISION-SPACE.md §1.17` — load-bearing audit-methodology decision; distills §5 + §6 of this log.
- Revised `AUDIT-SPEC.md` — applies §6 revisions.
- `.planning/deliberations/INDEX.md` — adds entry for this log.
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/DISPOSITION.md` (post-audit) — records audit's actual disposition after FINDINGS.md lands.

---

*Two-artifact pattern per DECISION-SPACE.md §1.10: this log carries dynamics + Claude's transparent reasoning (§3) + Logan's adjudication trace (§5); DECISION-SPACE.md §1.17 carries the load-bearing decision distilled. Subject to the same fallibility caveat as DECISION-SPACE.md §0. §5 + §6 populate after Logan adjudicates.*
