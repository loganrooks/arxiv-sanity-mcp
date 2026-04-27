---
type: audit-report
date: 2026-04-27
audit_spec: .planning/audits/2026-04-27-stage-1-artifacts-audit-spec.md
auditor: adversarial-auditor-xhigh (Claude Opus 4.7 at xhigh effort)
artifacts_audited: |
  - .planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md
  - .planning/gsd-2-uplift/DECISION-SPACE.md
  - .planning/gsd-2-uplift/INITIATIVE.md
  - .planning/deliberations/INDEX.md (2026-04-26 entry)
  - .planning/audits/2026-04-26-wave-5-exemplar-harvest.md (§10.14 forward-ref)
status: complete
---

# Audit report — Stage 1 deliverables of 2026-04-26 uplift initiative genesis session

## §0. Audit summary

The Stage 1 artifacts hold up reasonably well overall. They self-flag the closure-pressure-at-meta-layer pattern more honestly than the Wave 4 governance synthesis revision did, and the two-artifact split (dynamics log + decision-space distillation) appears to land its load. The most material findings cluster on the §1.1 confidence label, two specific phrasings that read as stronger commitments than the surrounding caveats acknowledge, and one numerical claim (`8 question-areas`) that survives unverified.

Top-line findings, severity-stratified:

**Important** (worth resolving before Stage 2 lands):
- **§1.1 confidence "high" appears mis-calibrated** given the deliberation log §B3 itself names the dispatch as having moved 4-6 times in-session; the artifacts' own discipline (§4.3) says churn is a confidence-instability signal that should be surfaced. (D5)
- **The "8 question-areas" claim** in §1.4 / INITIATIVE.md §5 is asserted in three places and enumerated in zero. A fresh-session subagent reading INITIATIVE.md §5 cold cannot reconstruct what the eighth question-area is. (D1, D6)
- **INITIATIVE.md §5 has no provisional caveat** on the 5-slice structure itself, even though DECISION-SPACE §1.4's confidence is "medium-low on specific slicing." That calibration does not propagate to the surface artifact subagents read first. (D3, D4)

**Quality** (reduce clarity / future-team usability without putting delivery at risk):
- The deliberation log §3 quotes the same Logan utterance as appears in §2; §3 acknowledges the duplication parenthetically but the structure still reads as if §3 reframes a quote the reader has already metabolized. (D2)
- §1.10's `~300-500 lines` self-description is now demonstrably wrong (DECISION-SPACE.md is 562 lines); minor self-honesty cost. (D5)
- The `~1000 lines` size claim for the deliberation log in §1.10 also overshoots (the log is 444 lines). The artifact under-sells its own brevity. (D5)
- INITIATIVE.md §4 inputs table labels Wave 5 outputs "low to medium" but the prose immediately following describes them in considerable substantive detail (α/β/γ/δ glosses), which appears to undercut the trust label. (D6)
- The deliberation log §A's table puts decision A2 "framing reframe" at confidence equivalent to the binding R2-base commitment without distinguishing that the reframe is described in DECISION-SPACE §1.2 as "high on the reframe; medium-low on the specific framing language" — that bifurcation does not survive the §A summary. (D2, D5)

**Methodological observations** (no specific remediation expected; recorded so future sessions can see them):
- The artifacts repeatedly reach for "load-bearing" as a label (15+ uses across DECISION-SPACE.md alone), which is itself one of the in-house rhetorical inflations the project has elsewhere flagged. The label survives where the argument is good; it survives equally where the argument is thin. (D3)
- The same-vendor framing-leakage caveat in §11 of this report applies; some findings I am tempted to mark "blocking" I am holding at "important" because I can produce the same prose Claude wrote and may be reading my own register sympathetically. (§11)

**Minor** (taste-adjacent or low-leverage; flagged not as fixes but as observations the team can drop):
- The metaquestion's sentence "If first-wave shifts this answer, direction reframes accordingly" is grammatically slightly off but is a quoted block; not worth fixing. (D7)
- The migration trigger in INITIATIVE.md §7 has no ownership/criterion for *who* decides the dedicated repo gets created. Open by design, but a future-Claude reading cold may treat the trigger as time-based when it is actually event-based. (D8)

The audit's overall read: Stage 1 is foundation that can carry Stage 2. The findings above are corrigible without rewriting the artifacts; most can be addressed by 1-2-line revisions or by adding a single explicit caveat in INITIATIVE.md §5.

## §1. D1 — Internal consistency across artifacts

### 1.1 Cross-references appear coherent

Every cross-reference I spot-checked resolves to the cited section. INITIATIVE.md §3.1 metaquestion phrasing is verbatim the same as DECISION-SPACE.md §1.7's proposed phrasing. §5 sequencing matches §1.4 + §1.6 + §2.3. The deliberation log §A decision-table maps decisions A1-A10 to DECISION-SPACE §1.1-§1.10 without gaps. INDEX.md's summary of the deliberation log is faithful to what the log actually contains.

**Severity:** none. Recording as "what works well" — internal consistency is non-trivial across 4 artifacts written in one session and the artifacts achieve it at the level of pointer integrity.

### 1.2 The "8 question-areas" claim is asserted but not enumerated

The figure "8 question-areas" appears in DECISION-SPACE.md:113, :125, :509 (§4.5 methodology entry), the deliberation log §1.4 row, §B5, and INITIATIVE.md:131. No artifact lists what the 8 are. Reverse-engineering from the slice content:

- Slice 1: mental model, mission, target user (3 sub-items)
- Slice 2: architecture, runtime, Pi SDK relationship (3 sub-items)
- Slice 3: workflow surface, automation, testing (3 sub-items)
- Slice 4: artifact lifecycle, extension surfaces, migration tooling, distribution/install (4 sub-items)
- Slice 5: long-horizon-relevant features, gaps, meta-evolution (3 sub-items)

That is 16 sub-items, not 8. The §1.4 prose ("originally 5 slices missed distribution/install and gsd-2's-own-evolution; refined to fold these into slice 4 and slice 5 respectively") suggests "8" was meant as `5 original slices + 3 added concerns` or `5 slices + distribution/install + meta-evolution + something else` — but that arithmetic produces 7 or 8 depending on what counts. The number is durable in the artifacts but not reconstructable from the artifacts.

**Severity:** important (D1, D6). A fresh subagent reading INITIATIVE.md §5 to understand what to flag in their slice will not be able to verify what their slice covers from the "8 question-areas" framing.

**What would dissolve:** an enumeration in DECISION-SPACE §1.4 of the 8 question-areas, with mapping to which slice covers which. A 5-line table.

**What might be defensible about the artifact's choice:** the team may have intended "8 question-areas" as informal sizing language ("we explored 8-ish concerns") rather than precise enumeration. If so, soft language ("covering ~8 question-areas") would carry the same signal without inviting reconstruction.

**Confidence on finding:** high; the discrepancy is verifiable by counting.

### 1.3 The §A decision table compresses the §1.2 confidence bifurcation

Deliberation log §A row A2 lists "Framing reframe: artifact-mapping is sub-question of harness-uplift, not the question" without confidence distinction. DECISION-SPACE §1.2 actually splits confidence: "High on the reframe itself ... Medium-low on the specific framing language." That split is load-bearing because it is the difference between "the goal articulation is settled" and "the goal articulation needs work — see §3.1 validation mechanism."

**Severity:** quality (D2). The §A table is a summary index; readers consulting it as quick-reference may carry forward the simpler "framing reframe — A2" mental model without the bifurcation.

**What would dissolve:** a footnote in §A pointing readers at the per-decision confidence in DECISION-SPACE.md, or splitting A2 into A2a (reframe) + A2b (specific language).

**Confidence on finding:** medium-high; readers' actual use of the §A table depends on read patterns we cannot verify.

## §2. D2 — Decision capture faithfulness

### 2.1 §1.2 framing reframe — wording is faithful to the larger reframe

The §1.2 decision text and the verbatim quote in §1.65 (and INITIATIVE.md §1) match what the deliberation log §3 records as Logan's articulation. The "the framing itself may be wrong" honoring (§1.2 paragraph 2) preserves the "we might find we need to completely rethink the issue" element that the deliberation log §4 audit flagged as missing from the original draft framing-note. That is honest follow-through on a previously-flagged gap.

**Severity:** none — this works well; recording as strength.

### 2.2 §1.7 metaquestion C-with-non-exhaustive-teeth — the proposed phrasing is operationally meaningful

The starter list of 5 direction-shifting evidence types is concrete enough that a first-wave agent would recognize an instance if they saw one ("gsd-2 architecturally hostile to long-horizon features (no native extension surface for what we'd add)" is checkable in source). The "First-wave agents: this list is a starter, not a checklist" framing addresses the anchoring concern.

There is a residual risk worth naming: the starter list is constructed from inside the framing it is meant to test. Items 1-4 ("gsd-2 architecturally hostile"; "Pi SDK doesn't expose"; "release cadence too slow"; "mission divergent") all presuppose that the test is *fit between gsd-2-as-substrate and our long-horizon needs*. They do not surface evidence-types that would shift the question further upstream — e.g., "the long-horizon-development framing is itself the wrong axis" (which is open question §3.6) or "the goal articulation is wrong" (§3.1). The teeth bite *within* the operating frame, not at it.

That said, the artifacts honor the limit honestly: §1.7's confidence is medium on specific starter-list content, the non-exhaustive flag is explicit, and the question-types in §3.6 / §3.4 sit alongside §3.1. So the limit is named, not hidden.

**Severity:** quality (D2, D7). The operational teeth bite within-frame; cross-frame teeth are absent. This is defensible (within-frame teeth are still operational; cross-frame is what §3.4 / §3.6 do separately) but worth surfacing for first-wave subagents who read §3.1 cold and may interpret the starter list as exhaustive of "things that could shift direction."

**What would dissolve:** one sentence in §3.1 noting "see §3.4 / §3.6 for cross-frame direction-shifts; §3.1 starter list is within-frame."

**Confidence on finding:** medium; an alternative read is that within-frame teeth are exactly what §3.1 is for and cross-frame teeth would dilute its operational shape.

### 2.3 §1.8 R2 + R2+R3 hybrid — faithfully captures the commitment

The decision text matches Logan's quoted commitment in §7: "R2 base + primary; R2+R3 hybrid where workflow allows; design must work even if all upstream PRs rejected; R1 fallback." All four conditions are preserved. The change-conditions in §1.8 cover the foreseeable shifts.

**Severity:** none — strength.

### 2.4 §1.9 G-D3 nice-to-have Option A — calibration partially preserved

§1.9 confidence is "Medium. Acknowledged marginal call; reasoning is 'yes, but barely.'" That language survives from the deliberation log §8 ("marginal call, not the obvious one. The reasoning is 'yes, but barely.'"). The calibration appears to land in DECISION-SPACE.md.

But INITIATIVE.md §3 / §5 / §6 do not mention the marginal-ness. The harvest §10.14 forward-reference characterizes G-D3 as "confirmed Option A given migration timing read of weeks-to-months" without the marginal flag. Future-Claude reading the harvest §10.14 cold will not encounter the marginal-call calibration — they will read the disposition as decided, full stop.

**Severity:** quality (D5). Calibration confined to DECISION-SPACE.md does not propagate to all the artifacts that reference the decision. The discipline LONG-ARC.md:51 articulates ("calibrated language as default register, not exceptional") would prefer the marginal flag travels with the decision-pointer.

**What would dissolve:** §10.14 says "Option A (acknowledged marginal call)" instead of just "Option A." Five characters.

**Confidence on finding:** high; verifiable by inspection.

## §3. D3 — Closure-pressure recurrence in the artifacts themselves

This is the highest-leverage dimension per the spec. The artifacts repeatedly self-flag the pattern (§B1 in the log; §4.1 in DECISION-SPACE.md). The audit's question is whether they exhibit it.

### 3.1 Where the artifacts honor the discipline

DECISION-SPACE §1.4 confidence is "medium-low on specific slicing" — calibrated honestly given the without-ground-truth situation. §1.5 Reading A confidence is "medium ... Logan's call; Claude couldn't independently verify" — appropriately honest. §1.9 "marginal call" honesty is preserved. §3 open questions are not pretending to closure. The deliberation log §B and §E are honest about the log's own fallibility.

These appear to land. The artifacts do not uniformly produce confident-sounding tidy structure dressed over unsettled situations.

### 3.2 Where the discipline appears to slip

**§1.1 confidence at "high" given the dispatch-deferral churn history.** The same artifact (DECISION-SPACE §4.3) defines recommendation churn as a confidence-instability signal: "Moving on a recommendation more than twice in a session is itself a signal — confidence is not stable." The deliberation log §B3 records the dispatch as having moved 4-6 times across the broader session window: "skip → do-it → skip → do-it → defer-and-transform → defer-with-larger-reframe." Harvest §10.9's flip-flop (skip → do-it → skip → do-it → final do-it) is the predecessor. The current "defer" disposition is the seventh position.

Yet §1.1 is labeled "High. Three independent reasons converged: comfort-language detection, reframe to larger goal, archival-not-input cleaner posture. Disposition stable across remaining session."

Two readings:
1. *Defensible:* "stable across remaining session" is accurate post-Phase-3 of *this* session; the prior flip-flopping was under different framings (comfort-insurance frame vs harness-uplift frame); once the harness-uplift frame landed, no further flip occurred. Three independent reasons did converge.
2. *Closure-pressure-recurrent:* the artifact's own discipline says churn is a signal that *the recommendation* is unstable, not that *the latest framing* is stable. The latest disposition has not been tested across a fresh session or under counter-pressure. "High" overstates what survived stress-testing: the reframes were Logan-pushed, not stress-survived.

I read the second more strongly. The §1.1 confidence label imports the very pattern §4.3 names. The label could be "Medium-high. Three independent reasons converged in the final disposition; the dispatch has moved 6+ times across the broader session-history (see §4.3); a fresh-session re-disposition would be informative."

**Severity:** important (D3, D5). This is the cleanest instance of a self-named discipline not propagating to the artifact's own surface.

**What would dissolve:** down-rate §1.1 confidence to medium-high or accompany "high" with explicit acknowledgment that the high label rests on within-session reframe-survival rather than fresh-session re-disposition.

**Confidence on finding:** medium-high; an alternative read (the closure-pressure pattern was *named* during the §2 reframe and the *recognition* itself is what licenses high confidence in the post-recognition position) is defensible. I do not find it dispositive.

**§4.5's "Logan's framing" parenthetical.** §4.5 names "Non-exhaustive-listings discipline (Logan's framing)" — this is descriptively accurate but the parenthetical functions as authority-grounding in a way the artifacts elsewhere flag. Per harvest §10.11: "Logan disposition" is the disposition step, not the discipline-source step. Phrasing the discipline as "Logan's framing" risks treating one-conversation-articulated as authoritative-discipline (the same risk §1.2 explicitly flags about goal articulation and §3.1 leaves open). It is one session old, like the goal.

**Severity:** quality (D3). The artifacts elsewhere model "treat one-session-articulated as provisional"; here a one-session-articulated discipline is named without that caveat.

**What would dissolve:** §4.5 noting that the discipline itself is observed-but-not-yet-codified (which §3.9 does separately); could be a single sentence linking the two.

**Confidence on finding:** medium; the §3.9 cross-reference does some of this work; a stricter reader would say the cross-reference should be inline.

**INITIATIVE.md §5 lacks the calibration §1.4 carries.** DECISION-SPACE §1.4 calibrates: medium-low on specific slicing; medium-high on parallel-Explore as the right shape. INITIATIVE.md §5 reads:

> Per DECISION-SPACE §1.4. Five-slice parallel-Explore dispatch with refined slicing covering 8 question-areas:
> 1. Mental model + mission + target user.
> 2. Architecture + runtime + Pi SDK relationship.
> ...
> Pilot dispatch slice 1 first; review output; calibrate; then parallel dispatch slices 2-5.

The slice list reads as a settled plan. The "covering 8 question-areas" reads as a fact. The pilot-slice mitigation reads as procedural prudence rather than as a hedge against the medium-low confidence on the slicing. The calibration label sits in DECISION-SPACE §1.4; it does not propagate to the artifact subagents read first.

**Severity:** important (D3, D4). This is the clearest closure-pressure-at-meta-layer instance: tidy structure (numbered slices) doing work that the underlying confidence cannot bear, with calibration confined to a sister artifact.

**What would dissolve:** one sentence in INITIATIVE.md §5: "The slicing rests on medium-low confidence (per DECISION-SPACE §1.4); the pilot-slice approach is the hedge. First-wave subagents may surface that the slicing is wrong-shaped; flag rather than work-around."

**Confidence on finding:** high; the propagation gap is verifiable.

### 3.3 Confidence distribution — does it cluster suspiciously?

DECISION-SPACE.md §1 confidence labels (all 14 in §1 + §2): high (3), medium-high (5), medium (4), medium-low (1), high-with-medium-low-bifurcation (1).

The distribution *appears* honestly stratified — about half the decisions sit at medium or below. But the cluster is at the upper end (8 of 14 are medium-high or high). Three of the highs are §1.1 (dispatch deferral), §2.4 (forward-reference), and §1.2's "reframe itself" half. §1.1's label is contestable per §3.2 above; §2.4 is "small low-cost addition with clear discoverability value" which is plausibly high; §1.2's reframe-itself is defensible because the reframe is what Logan articulated.

The distribution does not pathologically cluster, but it is not adversarially-rough either. A stress-tested distribution might have one or two medium-low entries beyond §1.4.

**Severity:** quality / methodological observation (D5). The distribution is honest enough to function but optimistic enough to invite calibration scrutiny.

**Confidence on finding:** low; this is closer to taste than ground. Recording for the team's awareness, not for revision.

## §4. D4 — Subagent handoff readiness

Imagining a fresh-session Explore subagent dispatched to first-wave slice 1 reading INITIATIVE.md cold:

### 4.1 Mitigations that appear to land

- §0 establishes "subagents dispatched for first-wave exploration" as audience explicitly.
- §1 marks the goal as "operating frame, not authoritative."
- §2 has the explicit "Operating-frame is provisional" header.
- §3 prefixes with "These are framing questions to inform first-wave exploration, not first-wave deliverables."
- §5.1 has subagent-specific guidance.
- §4 trust labels with footnote explaining "Low" means "calibrated skepticism, not ignore."

These mitigations do real work. A subagent reading the document linearly will encounter the operating-frame caveat before the slice list and will encounter §5.1's "treat §3 framing questions as informing-context, not deliverables" before they read their prompt.

### 4.2 Mitigations that may be insufficient

**The "harness" terminology gloss is in §1, but §3.1 starter list says "gsd-2 architecturally hostile" / "Pi SDK doesn't expose extension points" — both gsd-2-specific.** A subagent encountering §3.1 may read "harness" as gsd-2-specific despite the §1 gloss. The gsd-2-specific framing in §3.1 functions as anchoring counter-evidence to the §1 gloss.

**Severity:** quality (D4). Modest mitigation: §3.1 could note "uplift-of-gsd-2 here means the gsd-2-specific intervention; harness as defined in §1 is broader; first-wave evidence may surface that intervention should target the harness more broadly than gsd-2."

**§5 "covering 8 question-areas" reads as fact.** Per §3.2 above, this is the closure-pressure-at-meta-layer instance. A subagent reading §5 cold may treat the slice they are assigned as exhaustive coverage of their domain.

**Severity:** important (D3, D4). Already named.

**§3 questions as informing-context — risk of inverse misread.** §3 is prefaced as "framing questions to inform first-wave exploration, not first-wave deliverables." §5.1 reinforces: "Treat §3 framing questions as informing-context, not deliverables." A subagent who reads §3.1's "First-wave agents: this list is a starter, not a checklist. In addition to executing your slice, flag any direction-shifting evidence you encounter" may instead read this as a *secondary deliverable* — they execute their slice *and* flag direction-shifting evidence.

That second read is actually closer to what §5.1 wants: direction-shifting evidence flagging *is* a secondary task. The conflict is that §3 prefix says "not first-wave deliverables" while §5.1 + §3.1 effectively make it a secondary deliverable.

**Severity:** quality (D4). The two prescriptions are not contradictory but they are in tension. A clearer formulation: "answering §3 questions definitively is not your deliverable; flagging evidence relevant to them is."

**What would dissolve:** §3 prefix revises to "These are framing questions to inform first-wave exploration. Definitively answering them is second-wave work; flagging evidence relevant to them as you execute your slice is part of your output (per §5.1)."

**Confidence on finding:** medium; the existing prefix is workable, the revised prefix is clearer.

**"R2 base" in §2 as commitment vs contingent.** §2 reads:

> Upstream relationship: R2 (extension) as base + primary, contingent on first-wave finding gsd-2 has adequate extension surfaces (slice 4); R2+R3 hybrid (extension + upstream PRs) where workflow allows, contingent on gsd-2 maintainers being receptive to PRs; design must work even if all upstream PRs rejected; R1 (fork) as fallback only if R2 proves infeasible.

The "contingent on first-wave finding gsd-2 has adequate extension surfaces" qualifier is present but is buried mid-sentence. A subagent skimming §2 may read "R2 (extension) as base + primary" as the operative frame and miss the contingency.

This is partly addressed by §5.1's "do not auto-execute reframes; surface findings to Logan." But for slice 4 specifically (extension surfaces — the slice that *tests* R2 viability), the subagent should know their slice is the one that determines whether the operating frame survives. INITIATIVE.md does not flag this.

**Severity:** quality (D4). Modest mitigation: §5 slice-4 gloss could note "this slice is load-bearing for R2 viability per DECISION-SPACE §1.8 change-conditions."

**Confidence on finding:** medium; whether subagents would actually misread depends on first-wave prompt design (which is forthcoming).

## §5. D5 — Calibration honesty

Findings already covered above. Summarizing here:

- **§1.1 confidence "high"** — appears to import the closure-pressure pattern §4.3 names. Important. (§3.2)
- **§1.4 calibration not propagated to INITIATIVE.md §5** — the medium-low on specific slicing label does not surface where subagents read it. Important. (§3.2)
- **§1.9 marginal-call honesty preserved in DECISION-SPACE.md but lost in §10.14 forward-reference** — minor calibration leak. Quality. (§2.4)
- **§A decision table compresses §1.2 bifurcation** — quality. (§1.3)
- **§1.10 self-description (~300-500 lines, ~1000 lines) overshoots reality (562 / 444 lines)** — minor self-honesty miss; the artifacts under-deliver on size and over-claim. Quality.
- **Confidence distribution across §1 / §2** — does not pathologically cluster but tilts upper. Methodological observation. (§3.3)

The §0 read-guidance defines high / medium / medium-low precisely:

> "High" means the reasoning rests on multiple independent grounds and survives stress-testing within the session. "Medium" means the reasoning is defensible but contested by considerations that could weight differently. "Medium-low" means the decision is a working position pending evidence not yet gathered.

Most labels appear to honor this vocabulary. §1.1's "high" is the cleanest case where the definition is technically met (three independent grounds; stable across remaining session) but the underlying epistemic situation (6+ flip-flops; one session of stability) sits in tension with the spirit of the calibration scheme.

## §6. D6 — Citation discipline

### 6.1 Internal citations are largely load-bearing

LONG-ARC.md anti-patterns at lines 42-54: cited multiple times; verified content. The citation does work in §1.2 framing reframe + §4.1 closure-pressure recurrence. Genuine ground.

METHODOLOGY.md M1 at line 112: cited; M1 is at Hypothesis status per harvest §10.11 and the artifacts honor that — DECISION-SPACE does not over-credit M1. Honest.

ADR-0001 + ADR-0005: cited transitively for Wave 5 commit grounding (§2.2 recommendation); not directly load-bearing for Stage 1 decisions but referenced for the forthcoming commits. Appropriate.

Harvest §10 / §11: cited as predecessor; the §10.14 forward-reference closes the loop. Appropriate.

The 2026-04-25 recording-deliberations-extensively meta-deliberation is cited as policy precedent (deliberation log §9; INITIATIVE.md §8). Verifying — the meta-deliberation does establish the policy that this session's log instantiates. Honest grounding.

### 6.2 INITIATIVE.md §4 inputs table — trust labels and prose tension

The table:

| Input | Trust level | Use |
|---|---|---|
| Wave 5 outputs (α/β/γ/δ shapes per harvest §5 / §10.6; harvest §11 soft note; archived dispatch package) | low to medium (current-runtime-shaped; uplift-relevance is open) | Reference for what shapes Claude constructed during current-runtime governance work; not authoritative for uplift design. α = doctrine load-points map; β = anti-pattern self-check; γ = deliberation-boundary protocol; δ-pointer-note = forward-looking protected-seams change-control |

Two observations:

(a) The α/β/γ/δ glosses in the "Use" column substantively describe the shapes — for an input whose trust label is "low to medium" with "uplift-relevance is open," the gloss-level treatment is rich enough that a subagent reading this table may anchor to the α/β/γ/δ vocabulary as descriptive ground truth rather than as one Claude-construction subject to first-wave reframe. The trust label says "calibrated skepticism" but the prose does not skeptical-treat.

(b) The Gemini doc row says "mechanism-accurate; framing-misaligned" — this is honest, but a subagent reading "mechanism-accurate" may treat the mechanism descriptions as ground truth for gsd-2 mechanism, when the harvest's framing was that Gemini's *gsd-2 README descriptions* are accurate but the *interpretive lens around them* is misaligned. The distinction matters because subagents reading first-wave slice 4 (extension surfaces) may consult the Gemini doc for mechanism descriptions and propagate framing inadvertently.

**Severity:** quality (D6). Both observations are about under-skeptical prose under skeptical labels. The harvest §10.11 trust hierarchy makes this stratification explicit; the Stage 1 artifacts pick up the stratification mostly faithfully but the Wave 5 outputs row exhibits the prose-undermining-label tension.

**What would dissolve:** trim the α/β/γ/δ gloss in the "Use" column to a pointer ("see harvest §5 / §10.6"); the gloss is duplicative anyway. For Gemini, "mechanism descriptions accurate; framing on the uplift question misaligned" is more precise.

**Confidence on finding:** medium-high; this is the kind of finding where same-vendor reading risks reproducing-by-default the framings I am critiquing. I am holding this at quality not important.

### 6.3 The deliberation log §D cross-references — coverage check

§D lists predecessors (handoff, harvest, Gemini reading-notes, recording-deliberations meta), sibling distillation (DECISION-SPACE.md), forthcoming (INITIATIVE.md, deferral commit, Wave 5 commits, etc.), and project-level docs (LONG-ARC, VISION, METHODOLOGY, ADRs, docs/05).

Spot-check for omissions: the audit-cycle deliberations from 2026-04-25 (six siblings of the recording-deliberations meta) are not directly cited — only the recording-deliberations one. This is defensible (the recording-deliberations meta establishes the discipline; the others are not directly relevant to this session's work) but a fresh-session reader exploring "what other deliberations grounded the disciplines invoked here" would have to navigate via the recording-deliberations doc's frontmatter.

**Severity:** minor (D6). Coverage is adequate for the artifact's stated purpose.

**Confidence on finding:** medium; depends on whether future readers care about discipline-genealogy beyond the immediate predecessor.

## §7. D7 — Framing critique on the gsd-2 uplift initiative itself

### 7.1 The artifact-mapping → harness-uplift reframe

The reframe is a structural improvement insofar as it widens the question from "do our shapes map onto gsd-2's vocabulary?" to "what would make agential development more robust over longer horizons?" The widening is honest — the prior framing did pre-suppose gsd-2-as-target and same-vocabulary-as-medium.

However, the wider question may be *too* wide to operationally bind. "Long-horizon agential development" can absorb almost any improvement. §3.4 (is "long-horizon" the right framing axis) flags this — the artifacts honor the limit. But until first-wave work concretizes what "long-horizon" rules in / out, the operating frame is provisional in a way that risks under-constraining first-wave investigation.

Concretely: a first-wave Explore agent dispatched on slice 5 ("long-horizon-relevant features + gaps") has to choose what counts as "long-horizon-relevant." Without sharper criteria, the slice is a Rorschach.

**Severity:** quality (D7). The artifacts acknowledge this through §3.4 + §3.6 and through "operating frame" framing; the residual concern is whether first-wave evidence will *concretize* the framing or *defer* it further.

**What would dissolve:** the first-wave prompts (forthcoming) include a "what does long-horizon mean operationally for your slice?" sub-question. The Stage 1 artifacts cannot do this themselves; they can flag the need.

**Confidence on finding:** medium; this is more "concern to surface" than "finding requiring revision." Logan disposes whether to constrain or leave open.

### 7.2 Metaquestion C-with-non-exhaustive-teeth — operational vs ritual

The starter-list-with-non-exhaustive-flag-and-flagging-task structure does substantively more than ritual preservation. A subagent has clear instructions to surface direction-shifting evidence; the starter list is concrete enough to be checkable; the non-exhaustive flag is explicit.

The residual concern (§2.2 above) is that the starter list is within-frame. Cross-frame teeth are §3.4 / §3.6. A reader who treats §3.1 alone as the metaquestion mechanism may miss this; a reader who reads §3 as a whole sees it.

**Severity:** quality / methodological observation (D7). The mechanism does work; the within-frame/cross-frame split is not stated explicitly.

### 7.3 R2-base + R2+R3 hybrid — does it over-constrain?

The commitment is to *upstream relationship* (R2 / R3 / R1). The first-wave is supposed to surface evidence about *whether R2 is feasible* (slice 4) and *whether R3 is feasible* (gsd-2 contribution culture research). Decision text in §1.8 has explicit change-conditions — if first-wave shows R2 inadequate, R1 fallback activates.

The structure is closer to "R2 is the operating frame for design exploration; first-wave tests its validity" than to "R2 is committed regardless of first-wave evidence." That is consistent with the operating-frame discipline elsewhere.

The contingency wording in INITIATIVE.md §2 (per §4.2 above) is buried but is present. The change-conditions are spelled out in DECISION-SPACE §1.8.

**Severity:** none — appears to honor the operating-frame discipline. Recording as strength.

### 7.4 "Uplift gsd-2" as separate project + repo

The decision to spin out to a separate repo is in INITIATIVE.md §2 (Distribution shape) and §7 (Migration trigger). The reasoning given is "independent, valuable, reusable." The §3.3 onboarding situations + §3.5 reusability scope are open.

A counter-framing the artifacts do not explicitly entertain: "stay in arxiv-sanity-mcp `.planning/`; the uplift work is *for* arxiv-sanity-mcp; spinning out adds coordination cost." DECISION-SPACE.md does not list this as an open question and INITIATIVE.md §6 (NOT in scope) does not flag "should this be a separate project?" as an open question.

This is partially addressed by the metaquestion (§3.1 — "is uplift-of-gsd-2 the right intervention shape?") but that question is shape-of-intervention, not project-shape. A subagent reading cold may treat "separate project, separate repo" as settled when it actually rests on Logan's articulation that the package should be reusable across projects.

**Severity:** quality (D7). The "reusable across projects" goal is the operative ground for spin-out; if reusability scope tightens (per DECISION-SPACE §3.3), spin-out becomes contestable.

**What would dissolve:** add to §3 open framing questions: "Is separate-project-separate-repo the right distribution shape, or is this best done as project-internal infrastructure?"

**Confidence on finding:** medium; this may be a question already rendered implicit by §3.3 (audience) and §1.8 (R2 reusability). A stricter reader would say it deserves its own slot.

## §8. D8 — Anything missing

### 8.1 What happens if the uplift initiative is cancelled

INITIATIVE.md §6 (NOT in scope) and §7 (Migration trigger) cover the *forward* case (scoping continues; eventually migrates to dedicated repo). Neither addresses the *cancellation* case: if first-wave evidence + §3.1 metaquestion answer "no, uplift is not the right shape," what happens to the Stage 1 artifacts? Where do they live? Do they get marked superseded?

The deliberation log records the genesis; under cancellation, it remains as historical record. INITIATIVE.md and DECISION-SPACE.md would presumably get a "superseded" status. But the procedure is not codified.

**Severity:** quality (D8). Pro-forma at this stage but worth flagging because the metaquestion explicitly preserves cancellation-possibility.

**What would dissolve:** one paragraph in INITIATIVE.md §7 or new §6.x covering "If first-wave shifts the metaquestion answer to 'no': INITIATIVE.md and DECISION-SPACE.md gain a superseded-by-X status; the deliberation log remains as historical record; relevant content (e.g., specific patterns that proved valuable) migrates to wherever the new direction's home is."

**Confidence on finding:** medium; the team may regard this as future-Logan's problem, which is defensible; flagging anyway because the metaquestion's teeth depend on cancellation actually being executable.

### 8.2 Dispatch package archival path — recommendation, not decision

DECISION-SPACE §2.1 is a recommendation: archive the dispatch package by moving to `.planning/audits/archive/`. It is flagged as recommendation not decision, with confidence medium-high. This is honest — the archival has not yet happened; it is part of the forthcoming deferral commit.

The risk: the deferral commit is described in INITIATIVE.md §8 as "Forthcoming" without specifying *which* recommendation form lands. If Logan disposes a different archival path (e.g., leave in place with deferred notice), the §2.1 recommendation needs corresponding revision.

**Severity:** minor (D8). The recommendation/decision distinction is honored explicitly in the artifacts; this is more a future-state-coordination concern than a current-artifact gap.

**Confidence on finding:** low; this is operational and the team knows.

### 8.3 No mention of how this initiative interacts with active arxiv-sanity-mcp roadmap

Phase 12-17 (v0.2 multi-lens substrate per CLAUDE.md and STATE.md) is the active milestone. Stage 1 artifacts do not address: does the gsd-2 uplift initiative compete with v0.2 work for attention? What is the time/attention split? STATE.md (which Wave 5 commit 3 modifies) presumably will pin this, but Stage 1 artifacts do not pre-commit any answer.

The deliberation log §9 mentions "what might be forgotten ... AGENTS.md/CLAUDE.md cross-referencing initiative artifacts (no — same logic as Q5 from earlier)." That logic decides against project-level cross-referencing. But the question of *attention budget* between v0.2 and the uplift initiative is not explicitly addressed.

**Severity:** quality (D8). Forthcoming Wave 5 commit 3 (STATE.md) presumably handles; flagging because Stage 1 artifacts could include a one-line note in INITIATIVE.md §0 acknowledging "this initiative runs alongside v0.2 work; see STATE.md for attention split."

**Confidence on finding:** medium; depends on what Wave 5 commit 3 does.

### 8.4 No success / failure criterion for first-wave itself

§1.4 specifies first-wave shape (5 slices, parallel-Explore, ~150-300 lines per output, structured sections). It does not specify what makes first-wave *successful enough to proceed to second-wave* vs *requiring re-dispatch*. The incubation checkpoint per §2.3 is the gate, but its activation criteria are "if shifts: re-disposition; if no shifts: proceed." That assumes first-wave outputs are *good enough quality* to evaluate shifts on; it does not address the case where first-wave outputs are incomplete or shallow.

**Severity:** minor (D8). First-wave-quality criteria are typically codified in the dispatch prompts (forthcoming); flagging in case the team wants the criterion stated in INITIATIVE.md §5 too.

**Confidence on finding:** low; pragmatically the team knows quality when they see it.

### 8.5 Goal articulation has no fresh-session re-articulation date

DECISION-SPACE §3.1 says validation by "re-articulation in a fresh session and comparison; first-wave findings testing the articulation indirectly; external review." No timeline is given for re-articulation. The §1.6 incubation checkpoint timing is "after first-wave outputs synthesized" but the §3.1 validation is open-ended.

This is consistent with §3.1's "Low urgency for first-wave (articulation is operating frame; not authoritative anyway). Higher urgency before second-wave design lands." Honest about urgency. The risk: by the time second-wave design lands, the goal articulation may be 3+ months old and no one has re-articulated.

**Severity:** minor (D8). Pro-forma at Stage 1; flag if team wants to schedule re-articulation explicitly.

## §9. Cross-cutting observations

### 9.1 Convergent risk — calibration confined to DECISION-SPACE.md

Findings 2.4 (§10.14 omits marginal flag), 3.2 (§1 confidence labels do not propagate to INITIATIVE.md §5), 5 (calibration generally), and 6.2 (trust labels under-honored in prose) all point at the same underlying weakness: calibration lives in DECISION-SPACE.md but does not propagate consistently to the other artifacts that reference DECISION-SPACE.md decisions. LONG-ARC.md:51 articulates this exact discipline ("calibrated language as default register, not exceptional"). The Stage 1 artifacts honor it in DECISION-SPACE.md but inconsistently elsewhere.

This is one issue, not several. A single cross-artifact pass to propagate calibration to surface artifacts (INITIATIVE.md §5; harvest §10.14; INDEX.md summary) would address all four.

### 9.2 Convergent risk — within-frame teeth, cross-frame opacity

Findings 2.2 (§1.7 starter list within-frame) and 7.1-7.2 (long-horizon framing as Rorschach) point at: the artifacts have operational teeth *within* the operating frame but the cross-frame mechanism (§3.4 / §3.6) is structurally separate and not knit to the within-frame teeth. A subagent or future-Claude reading §3.1 cold may not notice they need to read §3.4 / §3.6 too.

This is also one issue. The teeth are operationally present but the architecture of teeth is not surfaced.

### 9.3 The artifacts' self-flag of closure-pressure-at-meta-layer is mostly load-bearing

§B in the log; §4.1 in DECISION-SPACE.md. These are not pro-forma — they document specific recurrences in specific phases of the session and they shape later sections (§1.5 Reading A; §1.4 medium-low confidence; §1.9 marginal-call honesty). The pattern-naming does work in the artifacts, not just sit there.

The two slips identified in §3.2 (§1.1 confidence; INITIATIVE.md §5 calibration) suggest the discipline is not fully internalized — the artifacts can name the pattern and still produce instances of it. That is consistent with the §B8 limit ("self-diagnosis from inside the pattern is unreliable") and with what same-vendor critical reading is supposed to catch.

### 9.4 The two-artifact split appears to land

Splitting dynamics (log) from decision-reference (DECISION-SPACE.md) is a real architectural improvement over the prior pattern of compressed-into-handoff capture. The log's narrative and the reference's structured form do different work for different readers. The split costs ~1000 lines combined but I do not see substantive duplication; each carries content the other does not.

The pattern is worth replicating. The deliberation log §9 already raises the codification question; §3.9 defers until 2-3 logs land. Reasonable.

## §10. What the audit could not verify

- **Faithfulness of dynamics-reconstruction.** The deliberation log is Claude's third-person reconstruction; without access to the original session transcript, the audit cannot verify whether specific phrasings (e.g., §2's "comfort-language detection") landed in-session or are post-hoc structuring. The single-author fallibility footer in §E names this honestly.
- **Whether first-wave subagents will actually misread.** §4.2 findings are speculative. The audit imagines a reader cold; actual reader behavior depends on first-wave prompts (forthcoming) and dispatch context.
- **Whether Logan's substantive reframes are correctly attributed to the right phase.** Several of the most consequential moves (Phase 2's comfort-language; Phase 3's larger reframe; Phase 4's framing-note self-audit) hinge on Logan's specific pushes. The log preserves direct quotes for the load-bearing pivots; the surrounding narrative is Claude's reconstruction. The audit cannot verify the reconstruction's psychological accuracy.
- **Whether the "8 question-areas" claim has a meaningful referent the audit missed.** I counted sub-items per slice; the figure does not match. There may be a higher-level grouping I did not reconstruct.
- **gsd-2 README facts cited transitively.** The audit did not re-verify gsd-2's `.gsd/` artifact set or auto-load semantics from source; relying on harvest §11's prior verification.
- **Whether the §1.1 "high" confidence is genuinely mis-calibrated or whether an alternative calibration vocabulary is in use.** Calibration is interpretive; the §0 vocabulary is precise enough to ground my critique but a different reader may calibrate differently.
- **Same-vendor framing-leakage.** The findings rest on observable artifact content; some critiques (especially §3.2 on §1.1 and §6.2 on inputs table) are exactly the kind where same-vendor sympathetic reading risks understating the issue. I have flagged where this concerns me. Cross-vendor reading would catch different things; this audit does not substitute.

## §11. Single-author fallibility caveat

This audit is my (Claude Opus 4.7 at xhigh effort) interpretive read of the Stage 1 artifacts. Same caveat as harvest §10 footer, the Wave 4 governance synthesis revision, and the deliberation log §E: if findings are contested, re-evaluation supersedes this audit. The audit's job is to surface concerns to inform Logan's disposition; the disposition step is Logan's.

Same-vendor framing-leakage is non-trivial here. The artifacts use the project's in-house rhetorical patterns (calibrated-language register; operating-frame language; numbered-decisions structure) and so do I. Some findings I have flagged at "important" rather than "blocking" specifically because I cannot rule out that I am reading the artifacts sympathetically as a same-vendor reader. A cross-vendor reader would likely find: (a) some findings I called "important" are blocking; (b) some findings I missed entirely; (c) some findings I called "important" dissolve under a different framing register.

The audit's strongest findings are those grounded in within-artifact verifiable contradictions (the "8 question-areas" arithmetic; the size mis-statements; the calibration propagation gaps) rather than those grounded in interpretive judgment. The interpretive findings (§1.1 high confidence; within-frame teeth; trust label / prose tension) are weaker and more open to alternative readings.

The audit's overall posture: Stage 1 artifacts are foundation that Stage 2 work can build on. Findings are corrigible without rewriting; most can be addressed by 1-2-line revisions or single-paragraph additions. The team can dispose findings selectively — a credible Stage 2 launch does not require addressing all of them.
