---
type: deliberation-log (audit-dispositions + synthesis-readiness)
date: 2026-04-28
session: post-W2-audits-landed; pre-W3-synthesis-dispatch
predecessor:
  - .planning/deliberations/2026-04-28-framing-widening.md (operating-frame ground)
  - .planning/deliberations/2026-04-28-tier-comparison-preliminary.md (tier-comparison input)
  - .planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md (B1-B6 source; §B methodological observations)
ground:
  - .planning/gsd-2-uplift/orchestration/audit-spec.md (W2 audit template + dispatch criteria)
  - .planning/gsd-2-uplift/orchestration/synthesis-spec.md (W3 synthesis spec)
  - .planning/gsd-2-uplift/orchestration/OVERVIEW.md §4-§6, §11 (wave structure + dispositions log)
  - .planning/gsd-2-uplift/exploration/02-architecture-audit.md (slice 2 audit; clean → proceed)
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md (slice 4 audit; minor → addendum with material CG-1)
  - .planning/gsd-2-uplift/exploration/05-release-cadence-audit.md (slice 5 audit; minor → addendum with citation errors + cross-finding flag)
status: complete (decisions D1-D5 disposed; recording artifact for auditing)
purpose: |
  Capture the W2 audit dispositions + W3 synthesis-dispatch decisions reached
  in the 2026-04-28 post-audits session, with qualified justifications
  preserving conditional structure ("what would change each recommendation").
  This log is the auditable record of *why* each disposition was chosen;
  OVERVIEW.md §11.4 carries the disposition headlines (per audit-spec.md:18)
  and references this log for full reasoning.

  Five live decisions are recorded here:
  - D1: Slice 4 CG-1 disposition (in-place addendum)
  - D2: Slice 5 citation errors (in-place strikethrough-correct)
  - D3: Slice 5 cross-finding integration flag (leave for synthesis)
  - D4: §11.4 dispositions log update timing (batch)
  - D5: W3 synthesis dispatch shape (single same-vendor; dispatched subagent;
        post-synthesis trigger evaluation; expect Trigger 4 to fire)

  This log is dynamics-faithful. Decision distillation in OVERVIEW.md §11.4
  + audit-spec.md / synthesis-spec.md follow-on dispatch.

  Single-author artifact written by Claude (Opus 4.7, xhigh effort) at
  Logan's direction post-recommendation-map exchange. Subject to the same
  fallibility caveat as DECISION-SPACE.md §0 and predecessor logs.
read_order: |
  - For "what was decided + why + what would change it": this document.
  - For "the audit findings these dispositions act on": the three audit
    files in `ground:` above.
  - For "the spec these dispositions follow / depart from": audit-spec.md
    and synthesis-spec.md.
  - For "the framing-widened operating frame these dispositions inherit":
    2026-04-28-framing-widening.md.
---

# W2 audit dispositions + W3 synthesis-readiness — 2026-04-28

## §0. How to read this document

**Audience.** Future-Logan, future-Claude in fresh sessions, future-auditors of the W3 synthesis or incubation-checkpoint deliberation, possibly external readers if the gsd-2 uplift initiative gets sponsored or observed.

**What this document IS.** Auditable record of the five live decisions reached in the post-W2-audits-landed session. Each decision section names: (i) the decision; (ii) the disposition chosen; (iii) the substantive justification (not just "spec says X"); (iv) the assumptions; (v) what would change the recommendation under what conditions.

**What this document IS NOT.** Not the disposition log itself (OVERVIEW.md §11.4 is the canonical home per audit-spec.md `:18`). Not a substitute for reading the audit files. Not a synthesis preview (synthesis-stage work is downstream).

**Disposition discipline.** Logan disposed all five decisions after a recommendation map was produced; this log captures the recommendations + Logan's affirmation + the conditional flips. Per harvest §10.1 assumption #1 + DECISION-SPACE.md §0, Logan disposes substantive choices.

**B.6 surface caught and addressed.** This session's decisions sit on top of three predecessor specs (audit-spec.md, synthesis-spec.md, OVERVIEW.md) authored 2026-04-27. The B.6 risk per `2026-04-28-tier-comparison-preliminary.md §7` is "defaulted-spec-following when evidence has shifted." Logan's prompt — "what might be your recommended response... why or why not is this approach sufficient... make explicit any assumptions or salient factors" — explicitly invited substantive re-evaluation rather than spec-deference. Each decision below was re-evaluated against current evidence (audit findings; framing-widening; tier-comparison) before being disposed.

**Calibration register.** Calibrated language per LONG-ARC.md anti-pattern "Closure pressure at every layer": appears-to over is; first-wave-evidence-suggests over first-wave-proves; operating-frame over decided-for-future for provisional positions.

## §1. Premise — what's in scope here, and what's not

Six audits-landed-state decisions sit between W2 completion and W3 synthesis dispatch. **The decisions don't pre-decide R-strategy, context-anchoring, or any operating-frame question** — those flow from synthesis + incubation-checkpoint per `DECISION-SPACE §2.3`. What's in scope: disposition mechanics for each audit; §11.4 update; synthesis dispatch shape. Deferred to later: Logan-direct-read scheduling (best at pre-incubation per `OVERVIEW.md §10`); R1-R5 evaluation (synthesis-stage); Stage 1 audit quality findings (per `framing-widening §9` item 10; non-blocking).

**Largest single load-bearing call: D5 (synthesis dispatch shape).** Once synthesis dispatches, W3 inputs commit and revising costs a re-dispatch. D1-D4 (audit-disposition mechanics) are recoverable. This shapes the careful-justification weighting below: D5 gets the most depth.

## §2. The audit landings being disposed

For audit-trail completeness:

**Slice 2 — architecture (`02-architecture-audit.md`).** Verdict: **Clean → proceed**. Five source spot-checks all verified. ADR-010 vendoring claim (proposed-not-implemented; ~79 files of GSD-authored code in vendored Pi packages) verified verbatim. RTK gating divergence verified verbatim (`README.md:22` vs `src/cli.ts:167-178`). No framing-leakage. No critical or material findings.

**Slice 4 — artifact-lifecycle (`04-artifact-lifecycle-audit.md`).** Verdict: **Minor → addendum** (auditor's call); contains one severity-tagged "material" finding (CG-1) where the auditor explicitly resolved the material/addendum tension via the substantive trigger — "material → re-dispatch" applies when findings *change* synthesis-relevant claims; CG-1 *adds* (missed enumeration of three additional extension subsystems: ecosystem, workflow plugins, skills) without reversing. Source verification clean. No framing-leakage.

**Slice 5 — release-cadence (`05-release-cadence-audit.md`).** Verdict: **Minor → addendum**. Math reproduces exactly across 8 spot-checks. Three citation line-number errors in `scripts/generate-changelog.mjs` and `scripts/update-changelog.mjs` (content described correct in all three cases; only line numbers wrong). Cross-finding integration flag for synthesis (elaborate breaking-change *machinery* vs rapid-cadence *practice*; auditor flagged as synthesis-stage). No framing-leakage.

Slice 1 audit was not triggered (pilot disposition was already proceed-parallel; no re-audit warranted post-pilot). Slice 3 audit was skipped per the working recommendation adopted in this session (corroborates the W2 dive's two-engine finding which was already verified at re-audit time; per `audit-spec.md:10-18` skip criteria, slice 3 met all skip conditions and no in-scope omissions surfaced from the dispatching project's read).

## §3. Decisions

### §3.1 D1 — Slice 4 CG-1: in-place addendum using auditor's suggested paragraph

**Decision.** Append the auditor's suggested addendum paragraph (audit `:144-146`) to slice 4 file in-place at end, with explicit annotation that it is post-audit Claude-attributed. No re-dispatch; no separate addendum file; no Logan-direct-read-first.

**Substantive justification.**

The audit-spec.md `§6` categorical structure ties severity-tag to action: material → re-dispatch; minor → addendum. The auditor flagged CG-1 with severity "material" but disposed "addendum," resolving the apparent inconsistency by appealing to the *substantive* trigger at audit-spec.md `:140`: "Material findings → re-dispatch. Findings change synthesis-relevant claims." CG-1 *adds to* the slice's central claim ("gsd-2 has substantive extension surfaces") rather than reverses it; the four-surface enumeration *strengthens* R2/R4 viability under the framing-widening's R1-R5 design space rather than weakening R2-base.

The auditor's suggested paragraph is source-cited (`ecosystem/loader.ts:1-110`, `workflow-plugins.ts:1-60`, `skill-manifest.ts:1-60`), citation-grounded, one-paragraph-bounded. It names three subsystems with specific source files and characterization (ecosystem trust-gated isolated from pi loader chain; workflow plugins three-tier discovery with four execution modes; skills with per-unit-type allowlists). Synthesis at xhigh, reading both slice file and audit, has full enumeration available. In-place addendum (rather than separate file) keeps the slice file self-contained for future readers reaching it without audit context — they see the corrected enumeration directly.

Re-dispatch (option 2 in the recommendation map) would burn ~30-60 min wall-clock to land content the audit already provides at known citations. Logan-direct-read first (option 3) has more value than initially credited, but its primary payoff is at synthesis-output-review or pre-incubation per `OVERVIEW.md §10`, not at audit-disposition time.

**Assumptions (explicit).**

- **A1.** Synthesis at xhigh can integrate addendum content without losing load-bearing-ness of the four-surface enumeration. Grounded in `synthesis-spec.md §2.5` (design-shape candidates as part of synthesis output structure) which can hold the four-surface integration; depends on synthesis discipline holding.
- **A2.** The auditor's enumeration (ecosystem / workflow plugins / skills) is correct and comprehensive. Grounded in audit `:53-65` source citations; auditor explicitly verified each subsystem with named source files; high confidence.
- **A3.** Q2's miss is a depth-of-attention issue at high tier, not a prompt-shape issue. Grounded in `framing-widening §6.1` honest estimate (50% catch on Q2 multi-mechanism revisions) and tier-comparison §3.2 (high catches relationship-detection but not always full enumeration).

**Conditional flips (what would change the recommendation).**

- **Same-vendor sympathy bias on slice 4 is real and asymmetrically risky.** The auditor explicitly flagged §7 sympathy (audit `:155`: "I may be reading the slice's open-questions section as doing more work than it does"). The *enumeration* is source-grounded; the *disposition* is interpretive. **What would flip:** Logan's direct read of `ecosystem/loader.ts` + `workflow-plugins.ts` + `skill-manifest.ts` finding a *fifth* subsystem the auditor missed, OR finding that the auditor mis-categorized one of the four (e.g., skills are sub-mechanism of workflow plugins, not peer subsystem). Then auditor's enumeration is itself partial; re-dispatch with strengthened Q2 prompt becomes more defensible because we don't trust either slice or audit to be complete.
- **Q2 was the slice's most load-bearing diagnostic.** **What would flip:** if subsequent synthesis or incubation review surfaces a similar relationship-mapping miss in slice 2 or slice 5 (which audited clean), the pattern suggests systematic high-effort blind spot, and re-dispatch (with revised prompt for affected slice) would be warranted. Currently no pattern — slices 2 and 5 audits both came back clean on relationship-mapping.
- **Framing-widening §6.1 estimated 50% catch on Q2 revisions; audit confirms partial catch.** **What would flip:** if the framing-widening's R4 distinction needed empirical support that *only* slice 4 could provide via direct enumeration in slice file (e.g., for citation discoverability from framing-widening's own reasoning chain), addendum would be insufficient because it lives in audit not slice. Counter: the audit citations are themselves citable from framing-widening's downstream reasoning; nothing requires the four-surface enumeration to live in slice §-numbering specifically.

**What this decision does not decide.**

- Whether the four-surface enumeration shifts R2 viability vs R4 viability vs R5 viability (synthesis-stage).
- Whether the four-surface plurality bears on the framing-widening's four-act plurality of "uplift" (synthesis or incubation work).
- Whether other slices have similar enumeration gaps (slice 2 + slice 5 audits both clean; if subsequent reads surface gaps, re-evaluate).

### §3.2 D2 — Slice 5 citation errors: in-place strikethrough-correct with corrigenda section

**Decision.** Strikethrough-correct the six citation occurrences in slice 5 (lines 244, 245, 304 (×2), 318, 332 (×2), 378 (×2)) with the auditor's corrected line numbers; add brief corrigenda section at end of slice file explaining the convention.

**Substantive justification.**

These are mechanical line-number errors where the auditor verified content correct (`scripts/generate-changelog.mjs:194-204` cited in slice; file is 152 lines; auditor found content at `:58, 66-67, 96, 118-125`). Three readers' situations to consider:

1. **Reader chasing slice citation post-audit-but-pre-synthesis:** hits dead line, has to re-derive. Bad.
2. **Synthesis reading slice + audit:** gets corrected via audit. Fine.
3. **Future reader reading slice without audit context** (e.g., post-archive): hits dead line. Bad.

In-place strikethrough-correct serves (1) and (3). Pure addendum-only serves only (2). Strikethrough preserves the original error (audit-trace per traces-over-erasure discipline; cf. memory `feedback_methodology_and_philosophy.md`); correction makes the citation chase work.

Single corrigenda section at end documents the strikethrough convention without bloating each in-place occurrence with explanation prose.

**Assumptions (explicit).**

- **B1.** Auditor's corrected line numbers are accurate. Auditor is xhigh + verified content; high confidence (`05-release-cadence-audit.md §1` spot-check 5).
- **B2.** In-place edits to slice files with attribution-annotation are project-aligned. No precedent forbidding it; `audit-spec.md §6` "addendum" disposition implicitly licenses post-audit slice-file additions; traces-over-erasure discipline supports strikethrough rather than silent edit.

**Conditional flips.**

- **Editing agent-produced artifacts breaks attribution chain.** Slice file's frontmatter says `agent: codex GPT-5.5 high`; in-place edits by Claude post-audit muddy attribution. **What would flip:** if Logan prefers strict "agent-produced artifacts are immutable" discipline (slice files become append-only after agent dispatch). Then addendum-section-at-end is right (preserves original verbatim; adds Claude-attributed corrigenda section). Cost: future readers chasing citations still hit dead lines mid-document; have to scroll to corrigenda. Counter-condition Logan affirmed: strikethrough-with-attribution reads as audit-trace, not artifact-mutation; the visual cue marks the post-hoc correction.
- **Three citation errors found in spot-check; comprehensive citation audit might find more.** **What would flip:** if Logan wants comprehensive citation-error scanning before synthesis, separate dispatch (light citation-audit subagent on all 5 slices). Counter: synthesis-time citation-failure cost is low (synthesis can verify content as it reads); marginal benefit doesn't justify the dispatch cost.

**What this decision does not decide.**

- Whether other slices have undetected citation errors (auditor's discipline is spot-check; only the three confirmed errors in slice 5 are corrected).
- Whether the cross-finding pattern the auditor flagged (machinery-vs-practice) is true (synthesis-stage interpretation).

### §3.3 D3 — Slice 5 cross-finding integration flag: leave for synthesis (auditor's call)

**Decision.** Do not surface the cross-finding integration flag (machinery-vs-practice across findings 2.6/2.7/4.5/4.6) earlier than synthesis. The flag is captured in audit `§5`; synthesis reads audits per `synthesis-spec.md:35`; flag enters synthesis-input chain naturally.

**Substantive justification.**

The audit-spec.md `§5` audit dimension explicitly directs auditor to flag synthesis-stage patterns when seen strongly: "if you see it strongly, flag." The auditor flagged it. The synthesis-spec.md `:35` mandates synthesizer reads audit outputs. So the flag is captured in the synthesis-input chain.

Surfacing the flag *outside* the audit (e.g., in OVERVIEW.md §11.4 as a synthesis-attention note) duplicates without adding signal. Updating slice 5 with the flag would collapse synthesis-stage interpretation back into slice-stage observation — exactly what B4 (slice 5 split per `DECISION-SPACE §1.14`) was preserving.

**Assumptions (explicit).**

- **C1.** Synthesizer at Claude Opus xhigh reads audit §5 dimension content with appropriate weight. The synthesis-spec doesn't mandate per-section emphasis but expects full audit read; plausible the synthesizer surfaces §5 cross-finding integration in synthesis output `§3` (slice contradictions).
- **C2.** The pattern is genuinely synthesis-stage (cross-finding integration), not slice-stage (in-slice observation). Auditor's read is grounded in §3.2 of audit (where they cite findings 2.6/2.7/4.5/4.6 as four contributing findings); high confidence.

**Conditional flips.**

- **Synthesis at xhigh is single-pass; flagging-within-a-flag may bury the pattern.** **What would flip:** if a prior synthesis showed weakness in audit-§5-integration, surfacing the flag as explicit "synthesis must address X" instruction in OVERVIEW.md §11.4 would warrant the duplication. Counter: no prior synthesis exists yet; default to spec discipline.
- **Cross-finding pattern is itself load-bearing for incubation-checkpoint** (bears on whether gsd-2's release-engineering machinery is *practiced* vs *staged*; bears on R-strategy assessment for any work touching release coordination). **What would flip:** if I thought synthesis was likely to miss the pattern entirely (e.g., synthesis instruction structure de-emphasizes cross-audit-integration), explicit surfacing would be safer. Counter: synthesis output structure at `synthesis-spec.md §1.1` (cross-slice patterns) and `§3` (slice contradictions) both naturally hold this; trust spec structure.

**What this decision does not decide.**

- Whether the machinery-vs-practice pattern is true (synthesis-stage).
- Whether the pattern bears on R-strategy assessment (synthesis or incubation work).

### §3.4 D4 — OVERVIEW.md §11.4 update timing: batch update post-disposition

**Decision.** Batch update §11.4 with all three audit dispositions in one inflection point, after D1-D3 are disposed. Per-slice entries with: target output path; verdict; disposition; addendum action; rationale (referencing this deliberation log for full reasoning).

**Substantive justification.**

§11.4 is the durable record of W2 audit dispositions per audit-spec.md `:18`. Per-disposition updates create churn for marginal benefit; defer-until-after-addenda is structurally backward (the disposition is the input to addendum work, not its output). Batch update at one inflection point is cleanest and gives a coherent §11.4 entry that captures all three slice dispositions in one place.

The shape per `OVERVIEW.md §4.7` (pilot disposition record): summary; disposition; rationale; calibration tweaks. Adapted for W2 audits: per-slice entry covers target output, audit verdict (clean/minor/material/critical), disposition, addendum action if any, recommendation rationale (with deliberation-log pointer).

**Assumptions (explicit).**

- **D1'.** Logan disposes D1-D3 in roughly one round (now confirmed in this session).
- **D2'.** §11.4 should not include synthesis-stage flags from audit §5 (those live in audit files; surfacing again in §11.4 is duplication; synthesis-spec.md handles synthesis-input chain).

**Conditional flips.**

- **Batch update means §11.4 lacks records during disposition window.** Brief but real. **What would flip:** if Logan wants §11.4 to track in-progress dispositions (not just disposed ones), per-disposition update with status ("disposing") is right. Counter: §11.4 records final dispositions, not work-in-progress; audit-spec doesn't mandate either.

**What this decision does not decide.**

- The §11.4 entry text itself (drafted at update-time per the spec).

### §3.5 D5 — W3 synthesis dispatch shape: single same-vendor; dispatched subagent; post-synthesis trigger evaluation

**Decision.** Dispatch single same-vendor synthesizer (Claude Opus xhigh, general-purpose subagent at max effort) per `synthesis-spec.md`. Inputs include the framing-widening artifact per `:45-50`. Post-synthesis: evaluate paired-synthesis escalation triggers per `synthesis-spec.md:172-189`. Pre-flag expectation: Trigger 4 (high-uncertainty interpretive claims at load-bearing positions) likely fires; if it does, escalate to paired-synthesis with cross-vendor codex synthesizer.

**Substantive justification (load-bearing decomposition).**

#### D5a — Synthesizer mode: dispatched subagent over in-session collaboration

`synthesis-spec.md:11` permits both. Dispatched subagent is right because:

- **Cleaner attribution** (single-author artifact at xhigh; current session has been deep in audit-disposition territory and carries cache-state anchored to that work).
- **Easier to pair with cross-vendor synthesizer if escalation triggers** (parallel structure).
- **Framing-widening artifact requires careful first-read;** fresh-session synthesizer reads it as new input rather than as "context I've been swimming in."
- **M1 paired-review discipline at synthesis stage** (per `METHODOLOGY.md:104-115`) is closer to honored when synthesis is its own dispatch than when session-collaborative.

In-session collaboration is more appropriate at *comparison* stage (if escalation fires) and at *incubation-checkpoint* stage (where Logan adjudication is load-bearing).

#### D5b — Paired-synthesis escalation: spec-following with pre-flagged expectation

`synthesis-spec.md:172-189` says: dispatch first synthesis; evaluate four triggers; escalate if any fires. Order is first-synthesize-then-evaluate. Following the spec but pre-flagging expectation:

Trigger 4: "high-uncertainty interpretive claims at load-bearing positions." Framing-widening's R1-R5 widening forces R-strategy evaluation; six-context plurality forces context-anchoring (which framing-widening §3.3 explicitly notes is interpretive — "Logan's read is binding"). So synthesis will *necessarily* carry interpretive claims at load-bearing positions. Trigger 4 is structurally likely to fire.

Pre-emptive escalation departs from spec and costs ~2x synthesis dispatch upfront. Spec-following dispatches single first; if Trigger 4 fires, escalates. Cost-of-escalating-when-warranted is paid once; cost-of-pre-emptively-escalating-when-not-needed is also ~2x. Net: spec-following is right because trigger evaluation is structural — if Trigger 4 fires, escalate; if not, save the cost.

Note B.6 is live here: synthesis-spec was authored 2026-04-27; framing-widening landed 2026-04-28. The synthesis-spec was *updated* to include framing-widening as input (per `synthesis-spec.md:45-50`), but the escalation triggers were not specifically re-evaluated against framing-widening's interpretive load. The triggers' calibration ("low — any one fires") is still right for this evidence base; the spec's reasoning (cost is real; sub-strict-M1 with audit catching what slips through is moderate-rigor) holds.

#### D5c — Synthesis dispatch readiness

All 5 slice outputs landed. Three audits disposed (after D1-D3). Slice 4 addendum + slice 5 corrections will land before synthesis dispatches. The synthesis-input dependency is satisfied. No specific gap blocks synthesis. Slice 1 audit not triggered (pilot disposed proceed-parallel); slice 3 audit skipped per audit-spec.md selective-audit criteria (corroborates W2 dive; no in-scope omissions surfaced).

**Assumptions (D5 collectively).**

- **E1.** Synthesizer at xhigh reading framing-widening + DECISION-SPACE.md + INITIATIVE.md + 5 slice outputs + 3 audits can produce a synthesis that meaningfully feeds incubation-checkpoint. `synthesis-spec.md` is built on this assumption.
- **E2.** B3's vendor split (W1 cross-vendor; W2 + W3 same-vendor) is the right split here. Tier-comparison preliminary §5 validates same-vendor xhigh for relationship-detection / interpretive-stage work.
- **E3.** Trigger 4 firing (likely) is a feature, not a bug. Escalation discipline is calibrated low precisely for this case.
- **E4.** General-purpose subagent at max effort is appropriate substrate for synthesis. No purpose-built "synthesis" subagent type exists; in-session collaboration is the alternative; general-purpose at max + synthesis-spec.md content + careful prompt yields equivalent quality with cleaner attribution.

**Conditional flips.**

- **Same-vendor synthesis carries framing-leak risk; pre-emptive paired-synthesis would mitigate.** **What would flip:** if I had specific evidence synthesis at same-vendor would systematically miss cross-vendor-perceptible patterns in this evidence set (e.g., a prior synthesis comparison showed substantive divergence). I don't — and spec's reasoning at `synthesis-spec.md:170` (cost is real; sub-strict-M1 with audit catching what slips through is moderate-rigor) still holds. **Counter-condition assumed:** audits at xhigh adversarial discipline already caught register-level framing concerns; first-synthesize-then-evaluate is sufficient rigor.
- **Logan-direct-read of gsd-2 before synthesis would ground-truth audits and slice findings.** **What would flip:** if Logan thinks the four-surface enumeration in slice 4 audit (high-confidence per auditor; high-stakes per R2 viability) requires Logan-eyes before synthesis to avoid synthesis building on shaky ground. Per `OVERVIEW.md §10`, "Highest benefit: pilot-review and pre-incubation stages" — pre-synthesis direct-read is mid-rank. **Counter-condition assumed:** pre-incubation direct-read has higher payoff than pre-synthesis (synthesis output is itself readable; ground-truthing post-synthesis is structurally easier than pre-synthesis).
- **Synthesis-spec output structure was authored 2026-04-27; framing-widening landed 2026-04-28; synthesis-spec output sections weren't restructured for R1-R5 / six-context plurality.** **What would flip:** if I expected synthesis-spec output structure to be inadequate for widened framing (e.g., need explicit R1-R5 mix recommendation section; need explicit context-anchoring section). Per `framing-widening §6.3` honest evaluation: "synthesis-spec.md's existing structure can absorb the widening as input-richer rather than structurally-different. If the synthesizer finds the existing structure inadequate, that itself would be a synthesis-stage finding flagged in synthesis output." **Counter-condition assumed:** synthesizer at xhigh, instructed to apply anti-pattern self-check (per `synthesis-spec.md:198`), can recognize and flag structure-inadequacy if it occurs.
- **Dispatched subagent (general-purpose at max) doesn't have purpose-built synthesizer subagent type; might lack synthesis-specific calibration.** **What would flip:** if a dedicated synthesis subagent existed; or if in-session collaboration would land cleaner artifact-production. **Counter-condition assumed:** general-purpose at max + careful prompt + synthesis-spec.md content yields equivalent quality with cleaner-attribution benefit; in-session is more appropriate at comparison/incubation stage.

**What this decision does not decide.**

- Synthesis content (synthesis output is the artifact).
- Whether escalation actually fires (post-synthesis evaluation).
- Whether Logan-direct-read happens at incubation-checkpoint stage (Logan disposes per `OVERVIEW §10`).
- Whether the cross-vendor synthesizer (if escalation fires) uses GPT-5.5 high or xhigh tier — defer to escalation-stage decision per B3.

## §4. Methodological note — B.6 surface caught and addressed

Logan's prompt structure in this session was a textbook B.6 catch:

1. After audits landed, Claude initially proposed dispatch of W2 audits and was about to default-follow audit-spec.md without re-evaluation. Logan's "do you have specs written for them?" caught the surface-level dispatch posture.
2. After clarification, Logan asked "do you think the template is sufficient yourself?" — explicit invitation to substantive evaluation rather than spec-deference. Three small clarifications were inlined at substitution time.
3. After audits ran and disposition options were proposed, Logan asked for "recommended response to each... why or why not... make explicit any assumptions or salient factors... possible pushback points... what would change your recommendation." This forced full conditional structure rather than spec-restated picks.

Each step caught a defaulted surface and forced substantive re-evaluation. Each step's catch was Logan's, not Claude's self-diagnosis.

The pattern matters for the broader B.6 codification deferred per `framing-widening §9` items 7-8 (methodology codification at threshold ~3 samples). This session is one sample; tier-comparison preliminary §7 named one (slices 2-5 dispatch defaulted to high without re-evaluation against medium evidence); the orchestration-package preflight failure per `2026-04-27-dispatch-readiness-deliberation.md §B.5` was one. Three-sample threshold reached for the defaulted-spec-following sub-pattern.

Mitigation observable in this session: each spec-aligned recommendation (D1, D2, D3, D5a-spec, D6-spec) carried explicit "why this is right" justification anchored to *current evidence* (audit findings; framing-widening; tier-comparison) rather than spec-text quotation. The fingerprint of substantive re-evaluation is *current-evidence anchoring*, not spec-rephrasing.

The deeper recurring meta-pattern across B.1 / B.5 / B.6: **strong trigger (skill match / dispatch instruction / written spec) bypasses calibrated re-evaluation**. The reliable correction has been Logan-adjudication. The discipline this codifies into is: when following any prior spec, briefly note "spec says X; evidence since spec was written includes Y; I'm proceeding with X because [reason] / proposing departure to Z because [reason]." Not an artifact-level discipline; a verbal-discipline-at-recommendation-stage.

## §5. What's next

Per the cross-decision dependency map:

1. **D1, D2, D3 → D4.** §11.4 batch update needs all dispositions disposed (now done).
2. **D4 → D5.** Synthesis dispatch is cleanest *after* §11.4 captures dispositions, so synthesizer reads consistent state.
3. **D5a (mode choice) is independent of D5b (escalation eval).**
4. **D5 → D6 (escalation eval) → potential cross-vendor dispatch → comparison artifact → incubation-checkpoint inputs.**

Concrete next actions (this session):

- Apply slice 4 addendum (D1).
- Apply slice 5 strikethrough corrections (D2).
- Update OVERVIEW.md §11.4 (D4).
- Update INDEX.md + STATE.md.
- Dispatch W3 synthesis (D5).
- Post-synthesis: evaluate Trigger 4. If fires, escalate to paired-synthesis.
- After synthesis (and comparison if paired): incubation-checkpoint per `DECISION-SPACE §2.3`. Logan-led; out of scope for this orchestration.

## §6. Cross-references

**Sibling artifacts (decisions / dynamics).**
- `.planning/gsd-2-uplift/DECISION-SPACE.md` — load-bearing decision reference; B1-B6 in §1.11-§1.16; §2.3 incubation-checkpoint.
- `.planning/deliberations/2026-04-28-framing-widening.md` — operating-frame ground (R1-R5 design space; six-context plurality; four-act plurality; project-anchoring framework); §9 deferred items log.
- `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` — tier-comparison input; §7 names B.6 sub-pattern.
- `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md` — orchestration package + B1-B6 + §B.1-§B.5 methodological observations.

**Audit inputs disposed by this log.**
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md` — clean → proceed.
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md` — minor → addendum (with material CG-1 disposed via substantive trigger).
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md` — minor → addendum (citation errors + cross-finding flag).

**Spec inputs.**
- `.planning/gsd-2-uplift/orchestration/audit-spec.md` — W2 audit template + dispatch criteria; `:18` for §11.4 disposition log; `:140` for material-trigger substance.
- `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` — W3 synthesis spec; `:45-50` for framing-widening as input; `:172-189` for paired-synthesis escalation triggers; `:170` for spec reasoning on default-single.
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` — §4-§6 wave structure; §10 Logan-direct-read prioritization; §11 dispositions log.

**Evidence inputs (W1).**
- `.planning/gsd-2-uplift/exploration/01-` through `05-*-output.md` — slice outputs at GPT-5.5 high.
- `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md` — capabilities probe at GPT-5.5 medium.
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md` — W2 dive at GPT-5.5 medium.

**Project doctrine referenced.**
- `LONG-ARC.md` — anti-patterns including closure-pressure-at-every-layer; this log resists that pressure by preserving conditional structure.
- `AGENTS.md` — project-specific anti-patterns; recommendation map applies anti-pattern self-check throughout.
- `CLAUDE.md` — project identity.
- `.planning/spikes/METHODOLOGY.md` — M1 paired-review discipline; B3 vendor split derives from it.

**Predecessor handoffs.**
- `.planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md` — predecessor; this session's onboarding artifact.

---

*Single-author deliberation log written 2026-04-28 by Claude (Opus 4.7, xhigh effort) at Logan's direction post-recommendation-map exchange. Subject to the same fallibility caveat as DECISION-SPACE.md §0 and predecessor logs. The log captures the recommendations + Logan's affirmation + the conditional flips. If any decision feels mis-recorded in Logan's read, re-deliberation supersedes this log.*
