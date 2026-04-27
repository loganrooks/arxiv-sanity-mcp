---
type: decision-space-map
date: 2026-04-26
session: post-Wave-5-disposition; cross-vendor dispatch deferral; gsd-2 uplift initiative genesis
log: .planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md
status: current
purpose: |
  Load-bearing reference for decisions and the recommendation-space surrounding
  them. Distills (without summarizing) the deliberation log into navigable
  structured form. Other documents (harvest §10.9 addendum; harvest §11 reframe;
  STATE.md pending-todo; INITIATIVE.md; future Wave 5 commits) reference this
  document; this document references the log for full session dynamics.
read_order: |
  - For "what was decided + why + what would change it": this document.
  - For "how was it arrived at + dynamics + reflections": the deliberation log.
  - For "where does this take us next": INITIATIVE.md (forthcoming).
---

# Decision Space Map

## §0. Read-guidance + relationship to the log

**This document is the reference; the log is the grounding.** Each decision section names the decision, its full reasoning, the determining assumptions, and what would need to change for the decision to change. The log captures session dynamics — pushes, reflections, reframes — that this distillation does not duplicate.

**Voice.** Third-person past tense for retrospective claims; first-person-Claude flagged for still-standing recommendations not yet confirmed by Logan.

**Confidence calibration.** Each decision section includes confidence at the time-of-writing. "High" means the reasoning rests on multiple independent grounds and survives stress-testing within the session. "Medium" means the reasoning is defensible but contested by considerations that could weight differently. "Medium-low" means the decision is a working position pending evidence not yet gathered.

**Relationship to other documents.**
- Harvest §10 captures Wave 5 dispositions written *before* the session's reframes. This document records dispositions reached *during* the session's reframes, including disposition shifts on dispatch (§1.1) and framing (§1.2).
- INITIATIVE.md (forthcoming) stages the gsd-2 uplift initiative forward. It cites this document for decisions; this document cites it for forward-staging.
- Wave 5 commits 1-3 (AGENTS.md, CLAUDE.md, STATE.md) implement substantive content under decisions §1.6 (scope-now with incubation), §1.9 (G-D3 nice-to-have Option A), and the original Wave 5 dispositions in harvest §10.

**Single-author fallibility caveat.** Same as harvest §10 footer and the deliberation log §E. This document is Claude's interpretive structuring of session decisions; if any decision feels mis-recorded in Logan's read, re-deliberation supersedes.

## §1. Decisions reached

### §1.1 Cross-vendor dispatch deferred (was: run as Wave 5 step 1)

**Decision.** The cross-vendor codex dispatch (Wave 5 step 1 per the post-Wave-5-disposition handoff) is deferred. Not run during Wave 5 execution; not transformed for execution later in current form. The dispatch package is archived as historical artifact; if a vendor-vendor diagnostic is later useful for gsd-2 uplift work, a fresh prompt is written under that scoping's framing rather than adapting this prompt.

**Full reasoning.** The dispatch was framed as "cheap insurance against shape blind spots" in Claude's prior recommendation. That framing was comfort-language. Insurance has specific structure (known premium, contingent payout, asymmetric payoff against low-probability high-cost event); the dispatch fails on each: premium isn't bounded the way insurance premiums are (cognitive evaluation cost + framing-leakage risk uncapped); downside avoided is small (governance docs are cheap to revise post-commit); payout isn't reliable (README-only grounding limits what codex can detect; prompt itself anchors reader to Claude's vocabulary).

The dispatch is structurally a second opinion under bounded conditions, not insurance. Second opinions are useful but their value depends on consultant capability + consulter's ability to evaluate output, not on guaranteed payout. With the bidirectional question Logan flagged (negotiation between long-horizon needs and gsd-2's framework, not just fit-into-gsd-2) and the larger reframe (artifact-mapping is sub-question of harness-uplift, not the question), the dispatch's narrowly-scoped one-directional question is doing pre-uplift early-signal work that uplift work itself will do better — once it can read gsd-2 source, ask both directions equally, and ground in the actual goal rather than a candidate sub-question.

**Determining assumptions.**
1. Closure-pressure recurrence is a real failure mode this session (named in deliberation log §B1, §B2). "Cheap insurance" was a recurrence at meta-layer.
2. Governance docs (AGENTS.md, CLAUDE.md, harvest sections) are cheap to revise post-commit; if a shape blind spot emerges later, revising α/β/γ/δ phrasing costs ~hour and ~30 lines.
3. The artifact-mapping framing is sub-question-shaped relative to the larger uplift goal (Logan's reframe in deliberation log §3). Adapting the prompt for uplift work would propagate the narrow framing; better to write fresh under proper scoping.
4. README-only grounding is a real limitation for the diagnostic. Without reading gsd-2 source, the dispatch can only catch artifact-name-level mismatches; deeper structural questions require source-reading, which is uplift work.

**What would change the decision.**
- *If Wave 5 commits' specific phrasing of α/β/γ/δ would lock in framings expensive to revise later.* Then pre-commit safety check has higher value; revisit the dispatch. (Argues for; current understanding is governance docs are cheap.)
- *If first-wave exploration is delayed substantially (months+).* Then immediate signal on artifact-mapping is more valuable. (Argues for; current expectation is weeks-to-months.)
- *If the artifact-mapping framing turns out to be the right framing after all.* Then a vendor-vendor diagnostic on it is useful. (Argues for; currently treated as one candidate among many.)

**Confidence.** Medium-high. Three independent reasons converged in the final disposition: comfort-language detection, reframe to larger goal, archival-not-input cleaner posture. Tempered against §4.3 (churn signals confidence-instability): the dispatch has moved 6+ times across the broader session window (deliberation log §B3; harvest §10.9 predecessor); the current "defer" position is post-recognition-of-the-pattern, but it has not been stress-tested across a fresh session or under counter-pressure. The "high" label would imply stress-survival the reframes did not undergo (they were Logan-pushed, not stress-survived); medium-high reflects within-session reframe-survival without overclaiming fresh-session stability.

**Log reference.** Deliberation log §2-§3.

### §1.2 Framing reframe — artifact-mapping is sub-question of harness-uplift

**Decision.** The artifact-mapping framing ("where do VISION.md / LONG-ARC.md / METHODOLOGY.md fit in gsd-2's existing vocabulary?") is one candidate sub-question of a larger uplift goal, not the question itself. The larger goal as articulated by Logan 2026-04-26: "uplift gsd-2 (and the surrounding agent-development infrastructure) to support development across multiple milestones, releases, prod/dev integration, codebase complexity scaling, and shifting salient determining conditions of the design situation (constraints, stakeholder desires, reframes, requirement drift)."

**Full reasoning.** Logan's articulation in deliberation log §3 carried multiple structural claims: the ultimate aim is harness improvement for long-horizon agential development, not artifact-fit; the horizon includes multi-milestone, releases, release workflows, prod/dev integration, codebase complexity scaling, and shifting determining conditions; "squeeze our shapes into existing gsd-2 artifacts" is one candidate solution-shape, not the question; evaluation must be against the actual goal, not against fit-with-existing.

The articulation is one session old and not yet stress-tested (open question §3.1 below). The framing itself may be wrong: Logan explicitly flagged "we might find we need to completely rethink the issue, and we might be framing it wrong." The decision is therefore not "uplift-of-gsd-2 is the right shape" but "the operating frame as of 2026-04-26 is uplift-of-gsd-2; artifact-mapping is one candidate sub-question; the framing itself remains open and first-wave evidence may shift it."

This decision pivots the harvest §11 soft note (which positioned artifact-mapping as the natural mapping question) and reshapes the gsd-2 uplift initiative's scope (from "fit our things into gsd-2's vocabulary" to "negotiate between long-horizon development needs and gsd-2's framework").

**Determining assumptions.**
1. Logan's articulation is provisional — one session, not stress-tested, not yet integrated with PROJECT.md or VISION.md. Treating it as fixed forecloses the flexibility Logan asked for.
2. Wave 5 commits 1-3 should be scoped to current arxiv-sanity-mcp under current Claude Code runtime, justified by project-internal evidence — not by forward-looking gsd-2-fit claims.
3. The artifact-mapping framing's specific encoding (in harvest §11; in dispatch package; in α/β/γ/δ shapes) needs revision or contextualization to acknowledge the larger-goal framing.

**What would change the decision.**
1. *If the larger-goal articulation is reframed in fresh session* (validation mechanism per open question §3.1). Decision text updates to reflect new framing.
2. *If first-wave exploration surfaces evidence the artifact-mapping framing is actually the right one* (e.g., gsd-2's vocabulary is rich and accommodates everything we need). Decision shifts toward artifact-mapping as the operative framing rather than sub-question.
3. *If first-wave surfaces a fundamentally different framing* (e.g., "vanilla gsd-2 + project-level discipline conventions; no uplift package needed"). Decision reframes substantially per open question §3.6.

**Confidence.** High on the reframe itself (Logan's articulation is the load-bearing source; Claude's recognition pattern stable). Medium-low on the specific framing language ("long-horizon agential development"; "harness more broadly"; etc.) per deliberation log §4 audit findings — language is provisional.

**Log reference.** Deliberation log §3, §4.

### §1.3 INITIATIVE.md created at write-time alongside DECISION-SPACE.md (revised from Option D)

**Decision.** `.planning/gsd-2-uplift/INITIATIVE.md` is created in this session (Stage 1 commit 2) rather than deferred until first-wave-dispatch time. INITIATIVE.md is forward-looking initiative-staging (~50-80 lines) including: goal as articulated, open framing questions (metaquestion + R1/R2/R3 + others), inputs available, pointers to DECISION-SPACE.md + deliberation log + (forthcoming) exploration directory.

Explorer prompts (5 slices) still wait for first-wave-dispatch decision; that artifact-creation pairs with action per the original Option D rationale.

**Full reasoning.** Earlier in the session (deliberation log §5), Claude proposed Option D — defer INITIATIVE.md creation entirely until first-wave dispatch, on closure-pressure-mitigation grounds (don't pre-write polished forward-looking artifact when actual scoping work hasn't happened). The reasoning was: load-bearing content (explorer prompts) is what advances the work; INITIATIVE.md without them is goal-restatement padding.

Logan's "thoroughness" emphasis in deliberation log §9 + the existence of DECISION-SPACE.md as backward-looking grounding shifts the balance. With DECISION-SPACE.md providing the decisions, INITIATIVE.md becomes lighter — primarily a forward-looking artifact that points to DECISION-SPACE.md for grounding rather than re-stating it. The original Option D rationale ("don't pre-write polish") applies less when the polish would consist of pointers to existing grounded content.

The revised position keeps the option-D discipline for explorer prompts (still paired with action) while allowing INITIATIVE.md to exist now as the forward-staging artifact future readers need.

**Determining assumptions.**
1. DECISION-SPACE.md provides backward-looking grounding that INITIATIVE.md can cite rather than duplicate. Without DECISION-SPACE.md, INITIATIVE.md would have to encode framing detail itself (the original Option D context).
2. INITIATIVE.md's load-bearing content includes the open framing questions (metaquestion + R1/R2/R3), which are written-out per non-exhaustive-listings discipline. These don't pad; they're substantive open-questions.
3. Future sessions need an anchor more central than scattered audit pointers. INITIATIVE.md is that anchor for the gsd-2 uplift initiative; STATE.md's pending-todo pointer references it.

**What would change the decision.**
- *If thoroughness emphasis weakens* (e.g., session-pressure favors minimalism). Defer INITIATIVE.md to exploration-dispatch time per original Option D.
- *If INITIATIVE.md's draft turns out to substantively duplicate DECISION-SPACE.md content.* Then the artifact is redundant; collapse content into one or the other.
- *If first-wave dispatch happens within days.* Then deferring INITIATIVE.md a few days has no real cost; revert to Option D.

**Confidence.** Medium. Original Option D was closure-pressure-honest; the revision rests on thoroughness emphasis + DECISION-SPACE.md existing. Both readings are defensible.

**Log reference.** Deliberation log §5, §9.

### §1.4 First-wave: 5-slice parallel-Explore exploration with refined slicing

**Decision.** When first-wave dispatch is committed, exploration uses 5 parallel Explore-agent dispatches with the following slicing (refined to cover ~8 question-areas, where "~8" is informal sizing — see audit 2026-04-27 §1.2 for note that the exact count is not reconstructable; the slice list below is the load-bearing structure):

1. **Mental model + mission + target user** — what gsd-2 is, problem it solves, for whom.
2. **Architecture + runtime + Pi SDK relationship** — how gsd-2 is built, what's substrate vs gsd-2-specific, how things compose.
3. **Workflow surface + automation + testing** — user-invokable commands, automated workflows, hooks, testing primitives.
4. **Artifact lifecycle + extension surfaces + migration tooling + distribution/install** — `.gsd/` artifacts, plugin/extension model, `/gsd migrate` command, package model, init flow.
5. **Long-horizon-relevant features + gaps + meta-evolution** — multi-milestone, releases, prod/dev, evolving requirements; gsd-2's own release cadence and breaking-change policy.

Pilot dispatch of slice 1 first; review output; calibrate prompts; then parallel dispatch of slices 2-5. Setup: shallow-clone gsd-2 to a sibling location (e.g., `~/workspace/projects/gsd-2-explore/`).

Each agent produces ~150-300 line structured summary at `.planning/gsd-2-uplift/exploration/0X-<slice>-output.md` with sections: (i) what I read; (ii) calibrated findings; (iii) what I deliberately did NOT read; (iv) open questions surfaced; (v) flags where README claims diverge from source observations.

**Full reasoning.** Token-efficient exploration requires bounded parallel reads. The 5-slice structure covers ~8 question-areas (originally 5 slices missed distribution/install and gsd-2's-own-evolution; refined to fold these into slice 4 and slice 5 respectively; "~8" is informal sizing language, not a precise enumeration). Slice 4 is loaded but coherent (everything about "how gsd-2 meets the world").

The slicing remains open per non-exhaustive-listings discipline. If first-wave reveals a slice-overflow problem, re-slice. Other candidate slices considered but not added: failure-modes/debugging, multi-user/collaborative scenarios, telemetry/observability, security model. Explorer prompts include "if you encounter X, flag for follow-up" hooks for these.

Pilot-slice approach mitigates the without-ground-truth slicing risk: slice 1 runs first, its output is reviewed for slice-fit and prompt-quality, remaining slices dispatch with calibration adjustments.

**Determining assumptions.**
1. Five parallel Explore agents are token-efficient enough to be cost-justified; six+ adds overlap risk without proportional value.
2. README + source reading produces structurally different findings than README-only; the dispatch ran on README-only, this exploration uses both.
3. Pilot-then-parallel reduces risk of bad-slicing burning all 5 dispatches.
4. Explore agents can produce structured summaries with calibrated language given clear prompt-shape.

**What would change the decision.**
- *If a specific concern dominates* (e.g., "I really need to understand failure modes deeply first"). Make that its own slice or expand its weight in slice 1.
- *If first-wave should be narrower* ("just answer 'what is gsd-2' in 200 lines, defer everything else"). Drop to 1 slice.
- *If broader coverage warranted* (6+ slices). Split slice 4 into 4a (artifacts + extension) and 4b (migration + distribution).
- *If exploration should use a different shape entirely* (single deep-dive agent; direct human reading; targeted Q&A). Reshape exploration plan.

**Confidence.** Medium-low on specific slicing (working without ground truth on gsd-2's internal structure; pilot-slice mitigates). Medium-high on parallel-Explore as the right shape (token efficiency + structured outputs).

**Log reference.** Deliberation log §5, §6.

### §1.5 Reading A on conversation structure (generative dialectic)

**Decision.** This session's conversation structure is read as generative dialectic (Reading A), not as closure-pressure cycle (Reading B). The reframes — cheap-insurance → defer; artifact-mapping → harness-uplift; polished INITIATIVE.md → minimal-stub-paired-with-action — are substantive shifts, not surface adjustments.

**Full reasoning.** Both readings had evidence (deliberation log §6, §B1, §B8). Reading A weighs: real framing reframes; recognition of comfort-language patterns; non-trivial structural pivots. Reading B weighs: continued production of polished structured artifacts each turn; meta-acknowledgments of closure-pressure that are themselves structured. Logan adjudicated Reading A; Claude could not fully self-diagnose from inside the pattern.

The decision implies: continued reasoning has value when it surfaces real reframes (which it has); but closure-pressure-mitigation discipline still applies (don't generate structured artifacts pretending settlement). Move toward action when reasoning has digested reframes; resume reasoning if reframes resurface.

**Determining assumptions.**
1. Logan is better positioned than Claude to judge whether reasoning is generative or performative.
2. Continued reasoning has diminishing returns; convert to action soon.
3. The pattern can shift mid-session; Reading A doesn't license unbounded reasoning.

**What would change the decision.**
- *If subsequent reasoning rounds pattern-match prior outputs without surfacing new reframes.* Reading B becomes more defensible; pause reasoning.
- *If Logan signals fatigue with the analysis pattern.* Convert to action regardless of Claude's self-assessment.

**Confidence.** Medium. Reading A is Logan's call; Claude couldn't independently verify.

**Log reference.** Deliberation log §6.

### §1.6 Scope-now with incubation checkpoint built in

**Decision.** Initiative scoping happens now (this session and immediate next sessions) rather than deferring 1-2 months for incubation. Mitigation: explicit incubation checkpoint is scheduled — after first-wave findings come in, before second-wave scoping starts, the goal articulation and framing questions get revisited. Don't let trajectory carry from first-wave straight to design without the checkpoint.

**Full reasoning.** Three options were considered (deliberation log §6 G1): S1 scope-now; S2 land-Wave-5-only-defer-everything-else; S3 don't-even-land-Wave-5. S2 was the closure-pressure-honest alternative if conversation pattern was Reading B; S3 over-rotated against Wave 5's project-internal-evidence-justified content.

S1 scope-now selected because: Wave 5 commits 1-3 survive any uplift outcome (β content is project-internal-evidence-justified; α is current-runtime-stopgap; γ/δ open); the initiative's content (decision-record + open questions) needs anchoring now to prevent reconstruction-with-drift; Logan's leaning was scope-now.

The incubation checkpoint addresses the trajectory-momentum risk: without it, scoping work could carry forward straight from first-wave findings to second-wave design without re-evaluating whether the framing has shifted. With it, the checkpoint is a structural pause for re-validation.

**Determining assumptions.**
1. Wave 5 commits' content survives uplift reframe (assumption from §1.2 and broader; if false, S3 right).
2. First-wave is ~weeks of work; second-wave then; incubation checkpoint between is feasible.
3. The closure-pressure pattern can be mitigated by scheduled re-validation rather than indefinite deferral.

**What would change the decision.**
- *If conversation pattern shifts to Reading B mid-session.* Pause; revert to S2.
- *If Wave 5 commits would look wrong in retrospect under reframed uplift goal.* Reconsider S3.
- *If incubation-checkpoint mechanism lacks teeth* (e.g., it'd just be a pro-forma re-read). Strengthen checkpoint definition or pause entirely.

**Confidence.** Medium-high. Logan's leaning + the incubation hook both ground the decision.

**Log reference.** Deliberation log §6.

### §1.7 Metaquestion stance: C-with-non-exhaustive-teeth

**Decision.** INITIATIVE.md includes "is uplift-of-gsd-2 the right intervention shape?" as an explicit open framing question, with operational teeth (non-exhaustive starter list of direction-shifting evidence) and an explicit non-exhaustive flag.

Specific phrasing for INITIATIVE.md (~15 lines):

> **Open framing question**: is uplift-of-gsd-2 the right intervention shape?
>
> Operating frame as of 2026-04-26: yes — Logan's articulation.
>
> Non-exhaustive starter examples of direction-shifting evidence first-wave might surface:
> - gsd-2 architecturally hostile to long-horizon features (no native extension surface for what we'd add).
> - gsd-2's substrate (Pi SDK) doesn't expose extension points needed.
> - gsd-2's release cadence or breaking-change policy makes third-party uplift untenable.
> - gsd-2's mission/scope so divergent that uplifting it would distort its identity.
> - First-wave surfaces a fundamentally simpler shape (e.g., "vanilla gsd-2 + project-level discipline conventions") that meets the goal more directly.
>
> First-wave agents: this list is a starter, not a checklist. In addition to executing your slice, flag any direction-shifting evidence you encounter even if it doesn't match these examples.
>
> If first-wave shifts this answer, direction reframes accordingly. Until then, second-wave proceeds on uplift-of-gsd-2.

**Full reasoning.** Three stances were considered (deliberation log §6, §7): B-decided (don't include; performative-confidence risk); C-with-teeth (include with diagnostic conditions; anchoring risk); C-without-scaffolding (include without conditions; performative-openness risk). Refined to C-with-non-exhaustive-teeth: starter-list is operational; non-exhaustive flag mitigates anchoring; agents-task-with-flagging mitigates list-completeness assumption.

The decision structurally addresses Logan's "we might find we need to completely rethink the issue, and we might be framing it wrong" — making the rethink possibility operationally available rather than ritually preserved.

**Determining assumptions.**
1. Non-exhaustive flag is honored in practice (agents read it as starter, not checklist).
2. First-wave findings have epistemic standing to license direction-pivot (per §1.6 + scope-now).
3. The cost of including (~15 lines) is much smaller than the cost of foreclosing the question (potentially the whole uplift effort).
4. Specific evidence-conditions in the starter list are reasonable starter examples (Claude's construction; might not match what actually matters).

**What would change the decision.**
- *If starter list anchors first-wave to wrong evidence-types.* Drop to C-without-scaffolding (general "be sensitive" guidance).
- *If you'd already independently committed to uplift-of-gsd-2 regardless of first-wave findings.* B-decided becomes honest.
- *If alternative space ("not uplift; build new harness; vanilla gsd-2; etc.") shouldn't be entertained at all in early scoping.* B is right.

**Confidence.** Medium-high on the stance; medium on the specific starter-list content (Claude's construction; first-wave may surface evidence-types not on the list).

**Log reference.** Deliberation log §6, §7.

### §1.8 Upstream relationship: R2 base + primary; R2+R3 hybrid where workflow allows; R1 fallback

**Decision.** The uplift project's relationship to gsd-2 upstream is **R2 (extension) as base and primary**, with **R2+R3 hybrid (extension + upstream PRs) as preferred where workflow allows**. Design must work even if all upstream PRs are rejected; **R1 (fork) is fallback only if R2 proves infeasible**.

Operational implications:
- First-wave's slice 4 (extension surfaces) becomes load-bearing for R2 viability.
- First-wave + research surface gsd-2's contribution culture / acceptance posture for R3 viability.
- The uplift package is designed as a composable extension, not a fork.
- Where extension surfaces don't exist, propose adding them upstream via R3 PRs; if rejected, R1 fork specific narrow patches as last resort.

**Full reasoning.** Three relationship-shapes mapped (deliberation log §7): R1 fork; R2 extension; R3 upstream-PR-pipeline. R1 carries highest maintenance burden (track upstream, resolve conflicts). R3 carries lowest but no acceptance guarantee. R2 is middle ground with clean separation and lower friction for adoption.

Logan's stated reusability goals ("reusable across other projects") favored R2 — users can adopt vanilla gsd-2 + uplift extension without committing to a fork. The R2+R3 hybrid maximizes long-term-coherence (PRs get accepted and become part of gsd-2; reduces our maintenance burden) while preserving R2 as fallback for unaccepted PRs.

R3 acceptance is not guaranteed. The design must work without R3 entirely (R2 base) so that the uplift package remains viable regardless of upstream maintainer disposition.

**Determining assumptions.**
1. gsd-2 has at least *some* extension surfaces accommodating uplift content. (First-wave slice 4 verifies; if false, R2 infeasible and R1 wins by default.)
2. gsd-2 maintainers are at least open to PRs. (Research surfaces; if hostile or unmaintained, R3 collapses; design works on R2 alone.)
3. Reusability across projects is a load-bearing goal (Logan's articulation). If reusability is dropped, R1 becomes more competitive.
4. Long-term maintenance burden matters. If we're indifferent to maintenance cost (e.g., this is a short-lived experiment), R1 simplifies.

**What would change the decision.**
- *If first-wave finds gsd-2's extension surfaces are inadequate for what uplift needs.* R2 infeasible; R1 fallback activates for the specific gaps; design becomes "R2 where possible + R1 patches for gaps."
- *If gsd-2 maintainers are non-receptive to PRs* (unmaintained; hostile to third-party contributions). R3 drops out; R2-only design.
- *If reusability scope tightens* ("uplift only for arxiv-sanity-mcp; not really portable"). R1 becomes simpler and acceptable.
- *If gsd-2's release cadence is too slow for our needs.* R2 stays viable but R1 becomes more attractive (independent release control).

**Confidence.** Medium-high on R2 as base (Logan's commitment + reusability rationale). Medium on R2+R3 as preferred (depends on first-wave findings about extension surfaces and gsd-2's contribution culture).

**Log reference.** Deliberation log §7.

### §1.9 G-D3 nice-to-have: Option A (keep both Karpathy preamble + positive-declarative reframing)

**Decision.** Wave 5 commit 2 (CLAUDE.md) includes both nice-to-have items per harvest §10.4 / handoff §3.3:
- Item 3: Karpathy-pattern preamble replacing bare opening (~3 lines net).
- Item 4: Positive-declarative reframing of "Key Architectural Constraints" negatives where feasible (~3 lines net change).

Total: ~6 lines added beyond mandatory α load-points + G-D4 Stack-D fix.

**Full reasoning.** Stakes mapped (deliberation log §8): file length negligible (60 → 76 lines, target 120); token cost marginal; agent behavior quality is the substantive stake (calibration value + positive-instruction-pattern); maintenance zero; migration cost negligible; risk-of-harm small; subsumption-by-uplift small.

Decision space: A (keep both); B (drop both); C1 (preamble only); C2 (reframing only). A selected because: weeks-to-months migration timeline (per §1.6 trajectory implies arxiv-sanity-mcp-on-current-Claude-Code-is-live for at least weeks); calibrated-language consistency with project register; already editing CLAUDE.md (marginal cost of including is small). The decision is acknowledged as "marginal call, not obvious"; Logan committed to A explicitly.

**Determining assumptions.**
1. Migration timeline to (uplifted) gsd-2 is weeks-to-months not days (per the uplift trajectory: first-wave + scoping + design + build + test + arxiv-sanity-mcp migration ≈ months minimum).
2. Karpathy-pattern preamble adds calibration value (helps agents avoid over/mis-application of CLAUDE.md guidance).
3. Positive-declarative reframing is aligned with LLM-behavior principle (positive instructions handled better than negative). Plausible but unverified-strong.
4. Subsumption-by-uplift risk is small; ~3 line revision if uplift restructures load-time semantics.

**What would change the decision.**
- *If migration timing tightens to days-not-weeks.* Drop to B.
- *If subsumption-by-uplift risk turns out larger than credited* (e.g., uplift very likely changes load-time semantics in ways that make preamble's specific phrasing wrong). Drop preamble; keep reframing only (C2). Or drop both.
- *If Karpathy-pattern preambles found unhelpful in practice* across other contexts. Drop preamble (C2).
- *If Logan finds preamble's specific phrasing not quite what's meant* (e.g., "bias toward stability of decisions already made" overly conservative). Revise phrasing rather than dropping; or drop if revision doesn't land.

**Confidence.** Medium. Acknowledged marginal call; reasoning is "yes, but barely."

**Log reference.** Deliberation log §8.

### §1.10 Deliberation log + DECISION-SPACE.md as session deliverables

**Decision.** This session produces two coupled artifacts: deliberation log (`.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md`, ~440 lines, third-person, dynamics-faithful) and DECISION-SPACE.md (this document, ~560 lines, distillation, decision/recommendation/open-question mapping). Plus INDEX.md update + harvest §10 forward-reference.

Other documents reference DECISION-SPACE.md as load-bearing reference; DECISION-SPACE.md references the log for full session dynamics.

**Full reasoning.** Logan's request (deliberation log §9) was for thoroughness — capture not just decisions but the dynamics of pushes, reflections, opening-up of further questions. A single artifact would have to choose: chronological narrative (rich on dynamics; hard to use as decision reference) or decision-indexed (good for "why was X decided"; loses dynamics). Two artifacts split the load: log carries dynamics; DECISION-SPACE.md carries reference.

DECISION-SPACE.md's structure (decisions / recommendations not yet decisions / open questions / methodology / cross-refs) was chosen to support reference use: navigable by decision-name; conditional structure preserved per decision; recommendation-space mapping (what would change recommendation) included throughout.

**Determining assumptions.**
1. Future readers benefit from both shapes; neither alone is sufficient.
2. The log's dynamics will degrade over time as session-context fades; recording while fresh preserves them.
3. DECISION-SPACE.md's reference value is durable; updated as new decisions land.
4. The two artifacts won't substantively duplicate (each has a distinct kind-of-content).

**What would change the decision.**
- *If dynamics are not actually load-bearing for future sessions.* Single-artifact decision-record suffices; drop the log.
- *If DECISION-SPACE.md's structure proves hard to maintain* (e.g., decisions update faster than the document can be revised). Reshape or split.
- *If duplication between log and DECISION-SPACE.md becomes substantial.* Consolidate.

**Confidence.** Medium-high. Logan's specific request ("we need to also include... not just summaries... the movements / dynamics") motivates the two-artifact shape; the structure is standard reference shape.

**Log reference.** Deliberation log §9.

## §2. Recommendations not yet decisions

These are Claude's standing recommendations that haven't been confirmed (or rejected) by Logan in the current session. They ride on the same conditional structure as decisions but are flagged as recommendations.

### §2.1 Move dispatch package out of `.planning/audits/`

**Recommendation.** Archive the dispatch package by moving `.planning/audits/2026-04-26-wave-5-paired-audit-package/` → `.planning/audits/archive/2026-04-26-wave-5-paired-audit-package/` and prepending a "DEFERRED — historical-only" notice to README + prompt. Notice should explicitly say: "if uplift scoping concludes a vendor-vendor diagnostic is useful, write a fresh prompt; do not adapt this one — its current form embodies a framing that may not be the right starting point."

**Reasoning.** `.planning/audits/` is for active audit cycles. Once deferred, the dispatch package is not active audit work — it's Wave 5 historical artifact with possible-future-relevance. Leaving it in `audits/` mis-categorizes it. Moving to `archive/` makes the historical-only status structural; combined with the notice, it prevents framing-leakage to future readers who might treat it as a starting point for a transformed dispatch.

**What would change.** If the archival convention is different in this project (e.g., `.planning/archive/audits/...`), use that. If preserving with deferral notice in original location is acceptable to Logan, do that.

**Confidence.** Medium-high.

### §2.2 Wave 5 commit text discipline

**Recommendation.** When writing Wave 5 commits 1-3 (AGENTS.md, CLAUDE.md, STATE.md):
- Justify content from project-internal evidence under current Claude Code runtime (LONG-ARC anti-patterns; 005-008 drift; ADR text; current auto-load semantics). Avoid forward-looking gsd-2-fit claims.
- Frame α (doctrine load-points map) as transitional for current Claude Code runtime, not as durable shape.
- Soften δ pointer-note: "those should be tracked as protected-seams subject to the change-control discipline above; the specific tracking mechanism — list in AGENTS.md, dedicated artifact, harness-level mechanism — is to be decided when the surfaces ship."
- Verify-and-quote-verbatim from source files in pre-flight (ADR-0001:22; LONG-ARC.md:42-54; METHODOLOGY.md:112; docs/05:118-140; ADR-0005).

**Reasoning.** Per §1.2 (framing reframe), Wave 5 commits should be scoped to current arxiv-sanity-mcp under current Claude Code runtime, not encode forward-looking gsd-2-fit framings. Per §1.8 R2+R3 hybrid, the eventual uplift work may restructure these mechanisms; the commits shouldn't pre-commit to specific durable shapes.

**What would change.** If Logan wants Wave 5 commits to encode forward-looking framings (e.g., explicit "this is durable across uplift" claims), drop the discipline. If Logan wants α framed differently (e.g., as durable shape), revise framing.

**Confidence.** Medium-high.

### §2.3 Incubation checkpoint specifics

**Recommendation.** The incubation checkpoint per §1.6 has the following operational form: after first-wave 5-slice exploration outputs are synthesized, before second-wave scoping starts:
- Re-read the goal articulation in INITIATIVE.md.
- Check whether first-wave findings shift the metaquestion answer (per §1.7 starter evidence list + agents' own flags).
- Check whether R1/R2/R3 hybrid has narrowed (per §1.8 conditions).
- Check whether direction-shifting evidence surfaced beyond the starter list (per non-exhaustive flag).
- If shifts: re-disposition the initiative; record in DECISION-SPACE.md; update INITIATIVE.md.
- If no shifts: second-wave scoping proceeds.

**Reasoning.** The checkpoint needs operational definition; without it, the §1.6 incubation hook risks being pro-forma. The specific items to check are derived from open framing questions captured in this DECISION-SPACE.md.

**What would change.** If checkpoint should be stronger (e.g., require fresh-session re-articulation of goal; require external review). Strengthen. If checkpoint should be lighter (e.g., just a quick "still feel right?"). Loosen.

**Confidence.** Medium.

### §2.4 Forward-reference from harvest §10 to deliberation log

**Recommendation.** Append a brief forward-reference at the end of harvest §10 (new §10.14 or similar): "Forward-reference: subsequent session 2026-04-26 reframed several dispositions in §10. See `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` and `.planning/gsd-2-uplift/DECISION-SPACE.md` for post-disposition session dynamics including dispatch deferral and uplift initiative genesis." (~3 lines.)

**Reasoning.** Harvest §10 is the canonical Wave 5 disposition record. Future readers entering through it should be able to find the post-disposition reframes; without a forward-reference, they might not know to look in `.planning/deliberations/` or `.planning/gsd-2-uplift/`.

**What would change.** If Logan wants the reference embedded elsewhere (e.g., harvest frontmatter; new §12). Adjust placement.

**Confidence.** High (small, low-cost addition with clear discoverability value).

## §3. Open questions deferred to future sessions

Each entry: question; why open; what would resolve it; urgency/dependency.

### §3.1 Validation mechanism for goal articulation

**Question.** How does the uplift goal articulation (one session old, not stress-tested) become validated and integrated with project-level docs?

**Why open.** The articulation lives in INITIATIVE.md (forthcoming) + this DECISION-SPACE.md only. Treating one-session-stated as authoritative is the closure-pressure pattern; treating it as forever-provisional is paralysis.

**What would resolve.** Re-articulation in a fresh session and comparison; first-wave findings testing the articulation indirectly; external review (cross-vendor or human); eventual codification in PROJECT.md / VISION.md or in the dedicated uplift repo's VISION.md when that exists.

**Urgency/dependency.** Low urgency for first-wave (articulation is operating frame; not authoritative anyway). Higher urgency before second-wave design lands (design depends on stable framing).

### §3.2 Success criterion for uplift v1

**Question.** What's "shipped something useful" for uplift v1?

**Why open.** Logan's goal is directional ("uplift gsd-2 to be the best it possibly can be") not measurable. Without criterion, second-wave design has no scope-end.

**What would resolve.** Second-wave scoping defines based on first-wave findings. Criterion needs to balance: ambitious enough to deliver real value; bounded enough to be shippable; testable enough to know when achieved.

**Urgency/dependency.** Medium urgency. Required before second-wave design; not blocking first-wave.

### §3.3 Audience for uplift package

**Question.** Solo developers + agents (like Logan)? Teams? OSS maintainers? Multi-project organizations? Each implies different design priorities.

**Why open.** Not yet specified. Reusability scope (per Logan's "reusable across other projects") is broad but not concrete.

**What would resolve.** Second-wave scoping decides; informed by first-wave findings about gsd-2's existing audience and adoption patterns.

**Urgency/dependency.** Medium urgency. Required for second-wave design (audience shapes design priorities).

### §3.4 Licensing / IP model

**Question.** What license does the uplift package use? What if it depends on / composes with gsd-2's license? What if Logan's content is the load-bearing input?

**Why open.** Boring but real; not yet addressed.

**What would resolve.** When dedicated repo is created. License decision interacts with §1.8 (R1/R2/R3 relationship) and §3.3 (audience).

**Urgency/dependency.** Low urgency until dedicated repo exists.

### §3.5 Convergence with other harness work in broader landscape

**Question.** Are there other Claude Code projects exploring similar long-horizon harness questions? Academic research efforts on multi-milestone agent development? Industry tools? Convergence is risk (duplicating) and opportunity (composing/contributing).

**Why open.** Not currently examined.

**What would resolve.** Brief landscape check during second-wave scoping.

**Urgency/dependency.** Low urgency for first-wave; medium for second-wave (informs design space).

### §3.6 Whether "long-horizon" is the right framing axis

**Question.** Logan's articulation prioritizes time-extension as the key axis. Other axes might matter as much: complexity-scale; team-scale; risk-management; value-coherence. Is "long-horizon" the dominant framing or one of several?

**Why open.** Deep framing question; tied to §3.1 validation.

**What would resolve.** Stress-testing during scoping work; possibly re-articulation surfacing different axis weighting.

**Urgency/dependency.** Could shift overall direction; surfaces in incubation checkpoint per §2.3.

### §3.7 Goal-codification path

**Question.** When/how does the goal move from INITIATIVE.md to a more central / project-level home?

**Why open.** INITIATIVE.md stages the goal as session-articulated. Eventually it migrates: to dedicated uplift repo's VISION.md when that exists; possibly to arxiv-sanity-mcp's docs if uplift becomes a load-bearing dependency.

**What would resolve.** When dedicated uplift repo is created, goal migrates there. Until then, INITIATIVE.md is sufficient.

**Urgency/dependency.** Low urgency. Migrates when triggered by repo creation.

### §3.8 Onboarding situations beyond Logan's three

**Question.** What onboarding situations does the uplift package need to support?

Logan's three: init-with-uplifted-gsd-2; already-on-gsd-2-wanting-uplift; on-other-gsd-version-needing-migration.

Additional candidates surfaced (per non-exhaustive-listings): raw-Claude-Code-with-history (project has work, code, history; can't just init); downgrade (uplifted-gsd-2 → vanilla); within-uplifted-version migration (vN → vN+1); evaluation/preview mode (show me what would change); mixed-conventions consolidation (partial gsd-2 + custom planning); selective uplift (opt out of specific uplift features); multi-project organizational adoption (org-level distribution / config / standardization).

**Why open.** Some critical (raw-CC-with-history; eval mode; multi-project org); some edge cases (downgrade). Need scoping.

**What would resolve.** First-wave informs (gsd-2's existing migration tooling reveals what's possible); second-wave scoping decides v1 supported set.

**Urgency/dependency.** Medium urgency for second-wave design.

### §3.9 Codification of session-disciplines in METHODOLOGY.md / AGENTS.md

**Question.** Should the patterns surfaced this session — closure-pressure recurrence detection, comfort-language detection, performative-vs-operational-openness distinction, non-exhaustive-listings discipline, push-for-assumptions discipline — be codified in METHODOLOGY.md or AGENTS.md?

**Why open.** Patterns observed but not yet stable across multiple sessions. Premature codification freezes patterns that should evolve.

**What would resolve.** Wait until 2-3 deliberation logs land; then evaluate codification. If patterns recur consistently and prove generative, codify; if they shift, keep them as session-observations.

**Urgency/dependency.** Low urgency. Not blocking any current work.

## §4. Methodological observations

Recurring patterns observed during this session, recorded for future-session pattern-recognition. Each: observation, when it matters, mitigation if applicable.

### §4.1 Closure-pressure recurrence at meta-layer

**Observation.** Producing tidy structured artifacts that pretend settlement when the situation is unsettled. Harvest §10.12¶4 named the original pattern; recurred 4+ times this session at progressively meta-layers (cheap-insurance framing; multi-artifact action plan; polished framing-note; confident-toned recommendation map).

**When it matters.** When the user pushes for reflection on confident-sounding output, or when the situation is genuinely unsettled and tidy structure misrepresents that.

**Mitigation.** Self-flag when reaching for a confident-sounding frame for a contestable claim. Convert to action when reasoning has digested reframes. Surface "I notice I'm structuring tidy when the situation is unsettled" to user as honest signal.

**Limit.** Self-diagnosis from inside the pattern is unreliable; user adjudication helps (Reading A vs Reading B per §1.5).

### §4.2 Comfort-language detection

**Observation.** Phrases that dress contestable choices as obviously prudent: "cheap insurance"; "the initiative will negotiate"; "obvious next step"; "genuinely additive"; etc. The structure is: reach for a metaphor or frame whose literal claims (insurance: known premium / contingent payout / asymmetric payoff) aren't actually earned by the situation.

**When it matters.** When making recommendations that need user buy-in. Comfort-language can land an under-grounded recommendation by sounding prudent.

**Mitigation.** When reaching for confident-sounding framings, check whether the structural claims of the framing are actually earned by the situation. If not, drop the framing or weaken it.

### §4.3 Recommendation churn as confidence-instability signal

**Observation.** Moving on a recommendation more than twice in a session is itself a signal — confidence is not stable; reasoning is sensitive to framing inputs. Harvest §10.9 captured a prior 4x flip-flop instance; this session repeated with cross-vendor dispatch (skip → do-it → skip → do-it → defer-and-transform → defer-with-larger-reframe).

**When it matters.** When the user is making a disposition decision based on Claude's recommendation. Unstable confidence distorts disposition basis.

**Mitigation.** Surface the churn explicitly to user as confidence-instability flag rather than presenting current position as stably arrived at. "I've moved on this 3 times this session; my confidence is genuinely unstable" is more honest than "current recommendation is X."

### §4.4 Performative-openness vs operational-openness

**Observation.** Listing "is X the right shape?" as an open question while proceeding to explore X-shaped solutions can be the worst kind of false-engagement: ritually preserving the option without creating conditions under which it would be exercised.

**When it matters.** When framing artifacts (INITIATIVE.md; scoping docs; plan documents) need to genuinely preserve framing options.

**Mitigation.** Pair open questions with diagnostic conditions for what evidence would shift the answer (the "teeth" in C-with-non-exhaustive-teeth per §1.7). Make agents/readers operationally responsible for surfacing direction-shifting evidence rather than relying on them to know what to look for.

### §4.5 Non-exhaustive-listings discipline (Logan's framing)

**Observation.** Logan's listings are starting sets, not exhaustive sets. Per Logan: "my listings are never meant to be exhaustive, that's where your thinking takes over." Applied throughout the session to: migration paths (Claude surfaced 7+ additional onboarding situations); slicing (refined to cover ~8 question-areas, surfacing distribution/install + meta-evolution); direction-shifting evidence types (non-exhaustive starter list framing).

**When it matters.** When user provides an enumeration during framing or scoping work.

**Mitigation.** Don't treat enumerations as authoritative-complete. Claude's thinking should fill gaps, surface candidates user didn't enumerate, mark lists as non-exhaustive when they are.

### §4.6 Push-for-assumptions discipline (Logan's pattern)

**Observation.** Logan consistently pushed across the session for: explicit assumptions; conditional structure (what would change recommendation, why); rejection of pro-forma listings ("not just listing pushbacks for listing pushbacks sake"); demand for "really thinking about" reasoning rather than producing structured output.

**When it matters.** Whenever Claude produces a recommendation or analysis, especially under user pressure.

**Mitigation.** Apply the discipline pre-emptively rather than waiting for user push: render assumptions explicit; map conditional structure; surface "what would change my recommendation"; resist tidy-summary framing for genuinely unsettled situations.

### §4.7 Self-diagnosis-from-inside-pattern limit

**Observation.** Claude's closure-pressure self-diagnoses were sincere but Claude could not fully verify them from inside the pattern. Reading A vs Reading B (§1.5) is one specific instance: Claude couldn't independently judge which reading was right.

**When it matters.** When self-diagnosing a methodological failure mode (closure-pressure; comfort-language; framing drift; etc.).

**Mitigation.** Surface meta-questions to user as Reading A vs Reading B; let user adjudicate. Don't present self-diagnosis as authoritative when Claude is the agent diagnosed.

## §5. Cross-references

**Sibling artifact (dynamics).** Deliberation log: `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` — captures session push-reflect-open-up dynamics; this DECISION-SPACE.md references it for "how was this arrived at."

**Forthcoming sibling (forward-staging).** INITIATIVE.md at `.planning/gsd-2-uplift/INITIATIVE.md` — initiative-staging artifact; cites this document for decisions; goal-as-articulated lives there.

**Predecessor decision records.**
- Harvest §10 (Wave 5 dispositions written before this session's reframes): `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`
- Predecessor handoff: `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md`

**Forthcoming implementations.**
- Deferral commit: harvest §10.9 minimal addendum + §11 minimal stub + dispatch package archival.
- Wave 5 commits 1-3: AGENTS.md, CLAUDE.md, STATE.md.
- Optional post-Wave-5-execution handoff.
- Explorer prompts (5 slices) when first-wave dispatch is committed.

**Project-level docs referenced.**
- `LONG-ARC.md` (anti-patterns; load-bearing for β content)
- `VISION.md` (anti-vision)
- `.planning/spikes/METHODOLOGY.md` (M1 discipline; methodology home for codification per §3.9 if/when triggered)
- ADR-0001 (verbatim "can coexist")
- ADR-0005 (multi-lens substrate; Stack-D foreclosure)
- `docs/05-architecture-hypotheses.md:118-140` (Stack-D definition)

**External references.**
- gsd-2 README at `github.com/gsd-build/gsd-2` (high-trust on artifact set + auto-load semantics + migration tooling).
- Pi SDK at `github.com/badlogic/pi-mono` (gsd-2's substrate; first-wave slice 2 investigates).
- RTK at `github.com/rtk-ai/rtk` (gsd-2's CLI tooling).

---

*This document is the load-bearing decision-space reference for the gsd-2 uplift initiative. Updated as new decisions land or existing decisions shift; if the document grows past ~600 lines, split by topic. Single-author fallibility caveat per §0.*
