---
type: deliberation-log
date: 2026-04-30
session: post-Phase-D-build mid-arc — frame-revision arc + methodology-mismatch finding + (V'.a) trajectory-replan disposition
status: deliberation complete; (V'.a) trajectory-replan disposed by Logan 2026-04-30 /effort xhigh; pending execution per §4 steps 1-5
ground: |
  - `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` — trajectory plan to be revised under (V'.a)
  - `.planning/gsd-2-uplift/wave-2/decision-trace/EXECUTION-LOG.md` — Phase D evidence corpus (now marked interim)
  - `.planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md` — Phase D contract under single-target-spike framing (superseded by replan)
  - `.planning/gsd-2-uplift/audits/2026-04-30-phase-d-entry-audit/DISPOSITION.md` — paired audit-arc that fired Phase D entry but did not surface methodology-mismatch
  - `.planning/spikes/METHODOLOGY.md` — spike methodology identified as scope-mismatched for mapping-question
  - `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` — test-case-vs-substrate framing standing context
  - DECISION-SPACE.md §1.8 R2-base assumption (1) on extension-surface accommodation — load-bearing for what Phase D was supposed to test
purpose: |
  Records the deliberation arc from Phase D mid-arc build commit (`c0465a4` arxiv-
  sanity-mcp + `23b1ddc89` gsd-2-explore) through to the methodology-mismatch
  finding and (V'.a) trajectory-replan disposition. Captures:
  (a) The Option 4 build-pre-flight disposition (existing dist invoked via node;
      no install/link/rebuild/user-side state mod);
  (b) The five frame-revisions surfaced on Logan's direct prompting + their content;
  (c) The skill-shape gsd-2-native-placement misfit finding;
  (d) The multi-surface + intent-tangled reframe;
  (e) The methodology-question-mismatch finding as load-bearing source of the
      prior frame-revisions (spike methodology applied to mapping question);
  (f) Logan's correction about Logan-disposition-as-load-bearing-mitigation being
      irresponsible (transferring substrate-design audit-load to non-expert reader);
  (g) Claude's commitment to (V'.a) trajectory-replan with named residual risks
      and proposed structural mitigation (frame-revision-checks built into trajectory).
read_order: |
  - For "what was decided + how to execute": §2 decisions + §4 (V'.a) concrete steps.
  - For "the deliberation arc + dynamics": §1.
  - For "substantive findings": §3.
  - For "calibration findings (substrate-shape evidence)": §5.
  - For "where each claim might be wrong": "Where this could be wrong" subsections distributed throughout.
---

# Phase D mid-arc deliberation — methodology-mismatch + (V'.a) trajectory-replan

This document records the deliberation arc that ran 2026-04-30 from Phase D
mid-arc atomic commit through to (V'.a) trajectory-replan disposition. Five
frame-revisions surfaced on Logan's direct prompting; the fifth crystallized as
**methodology-question-mismatch** (spike methodology applied to mapping
question) — the load-bearing source of the prior four. Logan disposed (V'.a) at
xhigh; Claude committed to (V'.a) at max with named residual risks.

## §0. How to read this document

**Audience.** Future-Logan, future-Claude in fresh sessions, subagents
dispatched on (V'.a) execution, future plan-revision auditor.

**What this document IS.** Canonical record of the deliberation arc. Captures
dynamics + decisions + reasoning trails + calibration findings.

**What this document IS NOT.**
- Not the (V'.a) trajectory-plan revision itself — that is authored separately
  per §4 step 2.
- Not a methodology-mismatch artifact — that is authored separately per §4
  step 5.
- Not Phase D's FINDINGS.md — Phase D's current evidence corpus is now interim
  and will be incorporated into the replanned mapping-shape Phase D per §4 step 1.

**Single-author + in-session-collaboration fallibility caveat.** Same as
DECISION-SPACE.md §0 + framing-widening §0. This document is Claude's
interpretive structuring of session decisions written in-session-collaboration
with Logan. The (V'.a) plan-self-audit per §4 step 3 is the structural
mitigation against framing-inheritance in this deliberation.

## §1. The deliberation arc

### §1.1 Entry state

Predecessor commits:
- `c0465a4` arxiv-sanity-mcp — Phase D dispatch mid-arc Step 6 + methodology + Option 4 + Option 5 + structural review
- `23b1ddc89` gsd-2-explore — Shape E SKILL.md on `phase-d-decision-trace-spike` branch off `main@42ef05fbe`

Phase D was authored under spike-shape framing per MINI-SPEC.md (single-target
spike on decision-trace skill). Build phase complete; substrate-shape correction
§1.5 had landed (F-PD-A1 audit citation about resource-loader.ts mechanic was
verified non-existent); §3 subagent invocation evidence (channel a clean pass
on B1/B2/B4/B5/B5b/B5c) recorded; §0.7 hybrid autonomy boundary established
post §3 PROCEDURAL NOTE breach.

The session resumed post-compaction at this state. Pre-flight question for
live-LLM run was open: `npm install` mechanics had been surfaced as user-side
state-modifying via postinstall (`scripts/install.js:163-164` writes
`~/.gsd/agent/bin/rtk`).

### §1.2 Build pre-flight — Option 4 disposed

**Question.** How to make gsd-2 runnable for Phase D live observation without
crossing user-side state modification boundary unnecessarily.

Initial three options (pre-compaction):
1. `npm install --ignore-scripts` + `npm run build` — skips postinstall; risks workspace-link gap
2. Skip `npm install`; `npm run build` only — uses existing 2026-04-29 node_modules
3. Full `npm install` + `npm run build` — runs postinstall; writes `~/.gsd/agent/bin/rtk` (first-time user-side state)

**Frame-revision surfaced (1st).** On Logan asking "do you still stand by Option 2?" at /effort max + defense-against-critics framing, source-archaeology revealed:
- `dist/loader.js` exists and runs from source (`node dist/loader.js --version` → `2.78.1`)
- package.json + package-lock.json clean against HEAD
- Existing 2026-04-29 dist incorporates all source changes (Shape E SKILL.md is non-runtime data per substrate-shape correction §1.5)

**Option 4 surfaced.** Invoke gsd-2 via existing dist directly: `PATH=~/workspace/projects/gsd-2-explore/node_modules/.bin:$PATH node ~/workspace/projects/gsd-2-explore/dist/loader.js <args>` — zero install, link, rebuild, or user-side state mod. Strictly dominates Options 1-3 on blast-radius and equal on evidence-yield.

**Logan disposed Option 4** /effort xhigh ("i accept your recommendation").

### §1.3 Test-shape question — Shape α surfaced

**Question.** Given Option 4 pre-flight, what live-LLM observation surface efficiently covers channel-(b) substrate-shape evidence (P1-P5 + B5d distribution)?

Initial test-shape candidates A-D (Headless / Unit-type-bound interactive / Discovery verification / Hybrid). Recommended Shape D (hybrid C → A → B) at xhigh with residual uncertainties about: (1) gsd-2 skill-list diagnostic subcommand existence; (2) headless unit-type binding mechanism; (3) test-task plumbing for `<available_skills>` block.

**Logan disposed**: "Let's investigate the residuals."

**Investigation findings:**
- No top-level `gsd skills` subcommand
- `gsd headless query` returns no-LLM JSON snapshot but **requires `.gsd/`** in cwd
- `--bare` flag explicitly **strips user skills** — defeats test purpose
- **arxiv-sanity-mcp does NOT have `.gsd/`** (gsd-2 not initialized for this project)
- gsd-2-explore source repo also has NO `.gsd/` (doesn't dogfood itself)
- Per-unit-type allowlist applies via `skillFilter` predicate at `agent-session.ts:1045` calling `buildSystemPrompt(...)`; binds at queued-unit-execution time
- `auto-prompts.ts:40` imports `resolveSkillManifest` — confirms allowlist mechanism

**Frame-revision surfaced (2nd).** On Logan asking "What is the purpose of all this again?" at /effort xhigh, audit of the four-horizon stack against Phase E gate-question revealed:

> Phase E asks: "is the disposition + first-target evidence coherent and well-formed; does the disposition narrow the design space appropriately given the evidence."
>
> Phase F criterion 3: internal coherence test — work has its own gravitational center.
>
> **Neither gate strictly requires P2/P4 distribution evidence from live LLM observation.** The substrate-shape evidence already collected (substrate-shape correction §1.5 + M1 calibration finding + source-grounded P1/P3 + investigation findings) is substantial. P2/P4 evidence would be additional channel-(b) detail, not load-bearing for gates.

**Shape α surfaced.** Defer live-LLM to Phase E (where it would naturally fire if needed). Phase D produces FINDINGS.md from current evidence corpus + explicit deferred-conditional marker for P2/P4/B5d-distribution.

### §1.4 Frame-revision (3rd) — skill is the wrong intervention surface

**Logan's prompt:** "why are we intervening with skills? is that the best surface to intervene with in gsd-2?"

This question opened the surface-choice space that Phase C disposition had implicitly closed. gsd-2 has multiple intervention surfaces (skills, hooks, workflow templates / markdown-phase-engine, extensions, MCP tools, custom subcommands, decision-DB subsystem, knowledge graph, R4 external orchestration). Skill-shape was selected as Phase D first-target without explicit comparison against alternatives.

Surface-space analysis surfaced four within-frame options for engaging:
- (I) Continue skill-shape Phase D
- (II) Re-adjudicate first-target shape at Phase C re-entry
- (III) Run Phase D at minimal commitment + plan second target now
- (IV) Pause Phase D for fresh deliberation on intervention-surface choice

Recommended (II) at xhigh.

### §1.5 Frame-revision (4th) — gsd-2-native placement

**Logan's prompt:** "the question is more like, where should this live based on GSD-2 itself and its conventions"

**This sharpened the question from "which surface" to "by gsd-2's own conventions, where does decision-trace functionality belong?"**

Reading gsd-2 source as gsd-2 understands itself revealed:
- `gsd_decision_save` MCP tool + `.gsd/DECISIONS.md` — gsd-2's existing decision-DB primitive (writes)
- `gsd graph build / query` — companion-subcommand pattern (builds + reads)
- `gsd headless query` — read-existing-state pattern
- Forensics extension — reads gsd-2 state subsystems (journal/activity/sessions) → produces structured analysis. **Architectural analogue for decision-trace.**
- Skills — discipline-application surfaces; **NOT integrated with gsd-2's state subsystems**

**Finding crystallized:** decision-trace's gsd-2-native placement is **companion-tool to `gsd_decision_save`** (MCP tool / subcommand pattern, structurally analogous to `gsd graph query / gsd graph build`) OR **extension structurally analogous to forensics**. Skill-shape is misfit because skills are external-to-state discipline-application; decision-trace is internal-to-state reconstruction.

**The deeper observation:** arxiv-sanity-mcp does not use `gsd_decision_save` (no `.gsd/DECISIONS.md`); arxiv-sanity-mcp's actual decision-trail lives in `.planning/deliberations/` + ADRs + handoffs + git + audits + STATE.md. **The misfit between gsd-2's decision-DB substrate and arxiv-sanity-mcp's actual decision-artifact conventions IS substrate-shape evidence channel (b)** — gsd-2 may need to accommodate richer decision-trail substrates than `.gsd/DECISIONS.md` for uplift to serve arxiv-sanity-mcp's actual practice.

The skill-shape commitment was tacitly **R4 (orchestrate-without-modifying) disguised as R2 (extension)** — added markdown to user-side `~/.agents/skills/` rather than extending gsd-2's decision-DB primitive.

### §1.6 Frame-revision (5th) — multi-surface + intent-tangled

**Logan's prompt:** "I mean if you want to really ask 'which surface should we prototype against to learn about gsd-2.' I think it should be which surfaces, you cant just learn from one surface, but also this question is tangled up with what we want to do and how we want to intervene"

Two interlocked moves:

**Multi-surface plurality.** Single-surface evidence is structurally limited per LONG-ARC.md §53 single-reader-framing-claims-as-authoritative + framing-widening §1.3 R1-R5-as-composable-not-tournament. Different surfaces yield categorically different kinds of evidence. The joint pattern across surfaces is what's actually load-bearing for uplift design.

**Tangled-up-ness with intervention-intent.** Surface-evidence-needed depends on intervention-intent depends on capability-gap depends on substrate-shape evidence — circular per Hanson's theory-laden-observation problem at substrate-design level.

Phase-level options surfaced: (I) Phase C re-entry / (II) reshape Phase D in-flight / (III) sketch-corpus Phase D / (IV) pause + redesign. Then (V) Phase D FINDINGS.md as meta-finding + (V') = (V) + Logan-disposition on trajectory-level paths (V'.a/b/c).

Recommended (V') at max effort.

### §1.7 Logan's methodological correction

**Logan's response to (V'):**

> "I'll accept V' but also bringing things to my decision does not automatically resolve all your issues. I saw you using that defense against your manufactured critic. You need to have reasoned enough to make the recommendation strongly. I do not have expertise in this and to lay the responsibility on me is irresponsible."

**The correction.** (V')'s defense against Critic 4 (the recursive at-risk-for-same-pattern problem) was a manufactured-critic move. "Mitigation: surfacing-for-Logan-disposition" transferred the audit-load to a non-expert reader rather than solving the recursive risk. The Logan-disposition discipline was meant to address D5a in-session-collaboration risk by having a non-LLM reader catch *framing-pressure* (which Logan can audit because he's the user with framing-intent). It was NOT meant to be the audit-of-last-resort for substrate-design soundness.

**Where this could be wrong.** Logan-disposition has legitimate uses (capturing user-intent; auditing framing-pressure where Logan has standing). The correction isn't "never Logan-dispose"; it's "don't use Logan-disposition as substantive-audit-load-bearing-mitigation when you haven't done the agent-side reasoning to commit." Distinguishing the legitimate cases requires judgment per situation.

### §1.8 Methodology-mismatch finding crystallized + (V'.a) commitment

At /effort max with explicit defense-against-critics framing (this time properly self-imposed rather than performative), the five frame-revisions traced to a single source:

**Spike methodology applied to mapping question.**

The trajectory plan inherited spike structure (per `.planning/spikes/METHODOLOGY.md`) because spikes are arxiv-sanity-mcp's existing methodology. Spikes test "does X work?" under conditions where the right experiment isn't pre-known. Substrate-design-evidence-collection asks "does this surface-set accommodate this practice?" — a *mapping* question, not a *spike* question. **Force-fitting a mapping question into spike methodology produced the single-target-skill-shape misframe, the multi-surface omission, the intent-tangled blindness, and the gsd-2-native-placement miss.** All five frame-revisions trace to this single methodological mismatch.

This is a stronger finding than "frame-revision pattern" alone. It's **methodology-question-shape-mismatch** — spike methodology applied to a problem-shape it doesn't fit.

**(V'.a) trajectory-replan committed at max** with named residual risks (§3.5) and proposed structural mitigation (§4 step 4 — frame-revision-checks built into trajectory mechanics).

**Logan disposed (V'.a)** /effort xhigh ("I accept (V'.a) but lets perhaps record these decisions and this deliberation so I can compact").

## §2. Decisions reached

### §2.1 Build pre-flight: Option 4 (existing dist via node) accepted

Existing `dist/loader.js` invoked via node directly; no install / link / rebuild / user-side state mod. Verified viable: `node dist/loader.js --version` → `2.78.1`; package.json + lock clean against HEAD; existing dist incorporates all source-relevant changes; SKILL.md is runtime-data not compiled-into-dist per substrate-shape correction §1.5. Strictly dominates Options 1-3 on blast-radius; equal on evidence-yield. **Logan-disposed 2026-04-30.**

### §2.2 Test-shape: superseded by trajectory-replan

Shape α (defer live-LLM to Phase E) was the leading recommendation under the spike-shape framing. Under (V'.a) trajectory-replan, the test-shape question is itself reformulated — mapping-shape Phase D collects different evidence than spike-shape Phase D would have. Test-shape decisions made under spike framing are superseded; they are preserved here for trace.

### §2.3 Skill-shape gsd-2-native-placement: misfit identified (substantive finding)

Decision-trace's gsd-2-native placement is companion-tool to `gsd_decision_save` (MCP tool / subcommand pattern) or extension structurally analogous to forensics. Skill-shape was R4-disguised-as-R2. **Substantive finding** carried into the methodology-mismatch artifact per §4 step 5.

### §2.4 Multi-surface + intent-tangled scoping: required for substrate-design-evidence

Single-surface evidence is structurally limited; substrate-design-evidence requires joint-evidence across surfaces. Surface-choice is tangled with intervention-intent. **Substantive finding** carried into the trajectory-plan revision per §4 step 2.

### §2.5 Methodology-question-shape-mismatch: load-bearing finding

Spike methodology fits "does X work?" questions; substrate-design-accommodation is a "does this surface-set accommodate this practice?" question — mapping-shape, not spike-shape. The five frame-revisions trace to this mismatch as their source. **Load-bearing finding** driving (V'.a). Recorded in dedicated artifact per §4 step 5.

### §2.6 Trajectory-level disposition: (V'.a) replan

(V'.a) trajectory-replan committed by Claude at max effort + Logan-disposed at /effort xhigh 2026-04-30. Replaces single-target-spike Phase D with mapping-shape Phase D (substrate-shape map: gsd-2 surfaces × arxiv-sanity-mcp practice × intervention-intents × accommodation-evidence). Phase E reshapes to test mapping-coherence; Phase F gates on mapping-coherence + intent-intervention-feasibility. Plan-self-audit cycle scoped to question-shape-fit.

### §2.7 Logan-disposition discipline: scoped clarification

Logan-disposition is for capturing user-intent and auditing framing-pressure where Logan has standing as the user. Logan-disposition is **NOT** the audit-of-last-resort for substrate-design soundness; using it as such is irresponsible because it transfers audit-load to a non-expert reader. Agent-side reasoning must produce strong recommendations under the agent's own grounds; Logan can override but the audit-load stays agent-side.

**Codification candidate.** This clarification is a candidate for codification in `.planning/spikes/METHODOLOGY.md` or `AGENTS.md` (the "Definition of success for early agents" section) — pending Logan's judgment on placement. Tracked as pending in §4.

### §2.8 Phase D current evidence: interim, not final

Current Phase D evidence corpus (§3 subagent invocation; §1.5 substrate-shape correction; M1 calibration; source-grounded P1/P3; investigation findings; frame-revision arc; gsd-2-native-placement finding) is preserved as **interim Phase D output** — work-product input to the replanned mapping-shape Phase D, NOT Phase D's final FINDINGS.md under the misshapen scope.

## §3. Substantive findings

### §3.1 Skill-shape gsd-2-native-placement misfit

Decision-trace functionality is reconstruction-shaped read against gsd-2's existing state subsystems (`.gsd/DECISIONS.md`, `.gsd/journal/`, `.gsd/activity/`, sessions). By gsd-2's own conventions, this is structurally:
- Companion-tool to `gsd_decision_save` (write-side); analogous to `gsd graph query` companioning `gsd graph build`. Natural placement: **`gsd_decision_trace` MCP tool / subcommand** in the decision-DB subsystem.
- OR an extension structurally analogous to **forensics** — reads gsd-2 state, produces structured analysis.

The skill-shape commitment was tacitly **R4 (orchestrate-without-modifying) disguised as R2 (extension)**. The F-PD-A2 disposition language ("EXTENDS, DOES NOT DUPLICATE `gsd_decision_save`") was pointing at decision-DB extension; skill-shape was a workaround for decision-DB extension at the wrong layer.

**Where this could be wrong.** This finding rests on Claude's reading of gsd-2 source + the existing decision-DB primitive structure. Cross-vendor read of gsd-2 by an auditor unfamiliar with the original Phase D commitments might frame the placement question differently. (V'.a) plan-self-audit per §4 step 3 should challenge this finding explicitly.

### §3.2 The substrate-mismatch IS substrate-shape evidence

arxiv-sanity-mcp does NOT use `gsd_decision_save`. arxiv-sanity-mcp's actual decision-trail lives in:
- `.planning/deliberations/*.md`
- `docs/adrs/*.md`
- `.planning/handoffs/*.md`
- `git log`
- `.planning/STATE.md`
- ADR-0005-style architectural commitments
- Audit folders (`.planning/gsd-2-uplift/audits/*/`)

These are arxiv-sanity-mcp's native artifact conventions — not gsd-2's. **The misfit between gsd-2's decision-DB substrate and arxiv-sanity-mcp's actual decision-artifact conventions is load-bearing channel-(b) substrate-shape evidence.** It surfaces that gsd-2's decision-DB substrate is opinionated about decision-shape (per-decision-row); arxiv-sanity-mcp's actual decision-trail is artifact-richer and runs across multiple subsystems. Uplift design must address this misfit if gsd-2 is to serve arxiv-sanity-mcp's actual practice (per RELATIONSHIP-TO-PARENT.md §1 test-case-vs-substrate framing).

### §3.3 Multi-surface evidence-need

gsd-2 exposes multiple intervention surfaces (skills, hooks, workflow templates / markdown-phase-engine, extensions, MCP tools, custom subcommands, decision-DB subsystem, knowledge graph, R4 external orchestration). Each yields categorically different kinds of evidence (LLM-discipline-application vs. lifecycle-event vs. phase-type-registration vs. plugin-loading vs. deterministic-tool-composition vs. CLI-dispatch vs. state-extension vs. graph-vocabulary vs. external-orchestration). The joint pattern across surfaces is what's load-bearing for uplift design. Single-surface evidence is structurally insufficient.

### §3.4 Intent-tangled-with-surface-choice

Surface-evidence-needed depends on which surfaces we plan to intervene on, depends on what we want to do (intervention-intent), depends on what gsd-2 already supports vs. is missing, depends on substrate-shape evidence. Circular per Hanson's theory-laden-observation problem at substrate-design level. Resolution: **make intervention-intent explicit at sketch-level + collect evidence across the surfaces those sketches implicate + revise both intent and surface-priors as evidence accumulates** (post-falsificationist + theory-construction frame from §0 of EXECUTION-LOG.md, applied at trajectory-shape level).

Sketched intervention-intents from corpus (per RELATIONSHIP-TO-PARENT.md §1 + cheerful-forging-galaxy.md §0.2 + arxiv-sanity-mcp practice):
- S1 — Multi-modal decision-trail support
- S2 — Layered audit-arc support
- S3 — Methodology codification
- S4 — Deliberation discipline (closure-pressure detection / comfort-language / D5a / performative-vs-operational)
- S5 — Decision reconstruction (decision-trace's underlying intent)
- S6 — Long-arc anti-pattern detection
- S7 — Comprehension-across-time (Context A primary)
- S8 — Modular-surfaces-that-stay-optional (Context F secondary)

Each implicates multiple surfaces; the joint set is what mapping-shape Phase D probes.

### §3.5 Methodology-question-shape-mismatch (load-bearing)

The trajectory plan inherited spike structure because spikes are arxiv-sanity-mcp's existing methodology. Spikes test "does X work?" under conditions where the right experiment isn't pre-known. **Substrate-design-accommodation asks "does this surface-set accommodate this practice?" — a mapping question, not a spike question.** Mapping methodology is not the same as spike methodology:
- Spike: pick target → experiment → does it work? → revise hypothesis.
- Mapping: survey surfaces → compose mental model → check accommodation against intents → identify gaps → iterate model.

Force-fitting the mapping question into spike methodology produced the five frame-revisions surfaced in §1. The fix is methodology-fit at trajectory-shape level, not within-frame elaboration.

**Where this could be wrong.** Counter-claim: spike methodology can be scoped flexibly to do mapping work; what we need is broader-scoped spikes, not different methodology. Counter-counter: the current Phase D scope WAS spike-shaped (single-target with M1 abort triggers; theory-construction frame of §0; build → test → findings) and that scope produced single-surface focus. Calling broader-scoped work "spike" would be cosmetic re-labeling without addressing the methodology-fit. (V'.a) plan-self-audit per §4 step 3 should challenge this finding explicitly.

## §4. (V'.a) execution: concrete steps

These are committed. Logan-disposed disposition is execution-greenlight.

**Step 1 — Mark current Phase D evidence as interim.** EXECUTION-LOG.md updated with §4 marker indicating current corpus (§1-§3 + investigation findings) is interim work-product input to replanned mapping-shape Phase D, NOT final Phase D FINDINGS.md output. MINI-SPEC.md frontmatter updated with superseded-by-replan marker.

**Step 2 — Author trajectory-plan revision.** cheerful-forging-galaxy.md revised to:
- Replace single-target-spike Phase D with mapping-shape Phase D — produce substrate-shape map across (a) gsd-2's intervention surfaces + their composition mechanics; (b) arxiv-sanity-mcp's actual practice as substrate-evidence-channel; (c) sketched intervention-intents per substrate-area; (d) joint-evidence about accommodation at the surface × intent intersection.
- Reshape Phase E to stability-test the mapping's coherence + theory-construction quality.
- Adjust Phase F readiness gate to gate on mapping-coherence + intent-intervention-feasibility.
- Add §0 acknowledgment that spike methodology fits "does X work?" questions; substrate-design-accommodation is a mapping question; the trajectory-shape revision is the methodology-fit response.

**Step 3 — Plan-self-audit cycle scoped to question-shape-fit.** Per Phase A pattern. Cross-vendor xhigh audit explicitly scoped to: "does the revised trajectory shape fit the substrate-design-evidence-collection question (mapping vs. spike)?" + "are there remaining methodology-fit issues this revision misses?" + "is the methodology-mismatch finding correctly diagnosed?" — different lens than the original audit's general "is this plan well-formed?" scope.

**Step 4 — Build frame-revision-check into trajectory mechanics.** Each Phase has an explicit "is the question we're answering still right?" pause, performed by Claude with surfacing to Logan, BEFORE within-frame elaboration. This is the structural mitigation against the closure-pressure-into-elaboration pattern: surface frame-revision question early, before elaborate within-frame work commits. Specific check-points:
- Phase entry (after reading inputs; before drafting outputs)
- Mid-Phase if observations diverge from priors
- Phase output draft (before commit)

**Step 5 — Document methodology-mismatch finding as substrate-shape evidence artifact.** New artifact at `.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md` (or similar) capturing:
- The diagnosis: spike methodology applied to mapping question
- The five frame-revisions as evidence-of-mismatch
- The skill-shape gsd-2-native-placement misfit as one instantiation
- The substrate-mismatch (gsd-2 decision-DB vs. arxiv-sanity-mcp decision-artifact conventions) as substantive substrate-shape evidence
- Cross-references to deliberation log + EXECUTION-LOG.md + cheerful-forging-galaxy.md revision

**Step pending — Logan-disposition discipline scope clarification codification.** Per §2.7. Codify in `.planning/spikes/METHODOLOGY.md` or `AGENTS.md` that Logan-disposition is for user-intent capture + framing-pressure auditing where Logan has standing, NOT for substantive-audit-load-bearing where agent-side reasoning is the proper anchor. Tracked as pending; placement decided when the codification opportunity warrants (per existing codification-threshold pattern in DECISION-SPACE §3.9).

## §5. Calibration findings (substrate-shape evidence about the substrate)

### §5.1 Five frame-revisions on prompting

Empirically: 4-5 frame-revisions in this turn-cluster surfaced ONLY on Logan's direct prompting. Each was preceded by elaborate within-frame disposition by Claude. None surfaced from Claude's audit-loop or self-questioning.

Pattern timeline (this session):
1. Build pre-flight (assumed fresh build needed; Option 4 surfaced on max + defense-against-critics prompting)
2. Test-shape (assumed live-LLM needed for P2/P4; Shape α surfaced on "purpose of all this?" prompting)
3. Intervention-surface (assumed skill-shape was the question; broader surface-space surfaced on "best surface to intervene with?" prompting)
4. Multi-surface + intent-tangled (assumed single-surface evidence sufficient; multi-surface + intent-tangled surfaced on "which surfaces, tangled with intent" prompting)
5. gsd-2-native-placement (assumed skill is appropriate placement; gsd-2-native-placement surfaced on "where should this live based on GSD-2 itself" prompting)

**Substrate-shape evidence:** the closure-pressure-into-elaboration pattern survives:
- Cross-vendor xhigh audit (Phase D entry audit — fired but didn't catch methodology-mismatch)
- Same-vendor adversarial-auditor xhigh
- D5a awareness + addendum-foregrounding
- xhigh effort
- max effort
- Methodology codification (six-lens reading from `.planning/spikes/METHODOLOGY.md`)
- Premise-bleed audit-arc precedent (which had specifically calibrated for similar patterns)
- Direct prompting (surfaces frame-revisions but doesn't break the pattern internally)

The pattern only broke at /effort max with explicit defense-against-critics framing combined with Logan's correction about evading via Logan-disposition. Even max alone wasn't sufficient; max + correction was.

This is load-bearing substrate-shape evidence. Effort-level alone doesn't break closure-pressure under in-session-collaboration; structured external pressure (Logan's correction + defense-against-critics framing) does. Implication for uplift design: the substrate (Logan + Claude) needs mechanisms that surface frame-revision questions earlier than direct prompting at maximum effort. (V'.a) step 4 is one such mechanism (frame-revision-checks built into trajectory mechanics); broader codification candidates per §2.7 + §4 pending.

### §5.2 Logan-disposition-as-evasion correction

§1.7 captured Logan's correction. Calibration: Logan-disposition has been used in this session in two distinct ways:
- **Legitimate:** capturing Logan's user-intent on substantive disposition (pre-flight build, methodology disposition, structural review)
- **Evasive:** transferring agent-side audit-load to Logan when Claude was uncertain how to commit (the (V') Critic 4 defense)

The legitimate use rests on Logan having standing as the user with framing-intent. The evasive use rests on no real grounds — it's Claude's uncertainty disguised as discipline. Distinguishing requires per-situation judgment + honest agent-side reasoning before defaulting to "Logan disposes."

**Where this could be wrong.** Some Logan-disposition uses sit on the boundary — e.g., the trajectory-level options (V'.a/b/c) where I claimed no agent-side commitment. In this session at max effort I committed to (V'.a); at xhigh I had not. The judgment of when to commit vs. when to defer is itself fallible and depends on agent-side reasoning depth + confidence calibration. The discipline isn't a bright line; it's "do the agent-side reasoning sufficient to commit before defaulting to Logan-disposition" — which itself requires self-audit on whether sufficient reasoning has happened.

### §5.3 Audit-discipline limits

The 2026-04-30 phase-d-entry-audit fired (paired cross-vendor codex GPT-5.5 xhigh + same-vendor Claude adversarial-auditor xhigh) and produced 11 revisions to MINI-SPEC + DISPOSITION + skill-body. **Neither audit surfaced "skill-shape is the wrong intervention surface" or "spike methodology mis-fits this question."** Both audits were scoped to MINI-SPEC contents (skill-shape commitment was already baked-in). The audit-spec didn't include "challenge the intervention-surface choice" or "challenge the methodology fit."

**Calibration finding:** Cross-vendor + same-vendor paired discipline catches different categories of failure (substance vs. register; vocabulary-import vs. integration-grammar-as-fact) but does NOT automatically catch methodology-question-shape-mismatch unless explicitly scoped to. The audit-scope itself is at framing-inheritance risk; if the audit is scoped under the same misframe as the artifact, it may not surface the misframe.

Implication for (V'.a) step 3 plan-self-audit: scope explicitly to question-shape-fit + methodology-fit + intervention-surface-choice — not just general "is this plan well-formed?"

### §5.4 The pattern-recognition required Logan's pressure

The methodology-mismatch finding crystallized only at max effort + Logan's "lay the responsibility on me is irresponsible" correction. At xhigh I had reached (V') with manufactured-critic defense; at max with defense-against-critics + Logan's correction, I committed to (V'.a) with named residual risks.

**The pattern itself is substrate-shape evidence:** maximum-discipline configuration + Logan's structured external pressure + defense-against-critics framing was the necessary set of conditions to break closure-pressure-into-elaboration on this particular methodology-mismatch. Lower configurations (xhigh, max alone, defense-against-critics alone) were insufficient.

Implication: substrate-design must support maximum-discipline configuration + structured-external-pressure as routine, not exceptional. Without it, frame-misshapings persist undetected.

## §6. Cross-references

**Predecessor records:**
- Predecessor commit: `c0465a4` arxiv-sanity-mcp; `23b1ddc89` gsd-2-explore (Phase D mid-arc atomic commit)
- `.planning/gsd-2-uplift/wave-2/decision-trace/EXECUTION-LOG.md` §0-§3 + §1.5 substrate-shape correction
- `.planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md` (Phase D contract under spike framing)
- `.planning/gsd-2-uplift/audits/2026-04-30-phase-d-entry-audit/DISPOSITION.md` (paired audit-arc that didn't catch methodology-mismatch)
- `.planning/gsd-2-uplift/wave-2/decision-trace/TRAIL-2026-04-25-multi-lens-redirection.md` (subagent invocation evidence)

**Standing context:**
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` §1 (test-case-vs-substrate framing)
- `.planning/gsd-2-uplift/INITIATIVE.md` §1-§3 (uplift goal articulation + open framing questions)
- `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.8 (R2-base assumption (1) on extension-surface accommodation)
- `.planning/deliberations/2026-04-28-framing-widening.md` §1-§3 (R1-R5 design space + six-context plurality + project-anchoring)
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §5 + §7 (incubation axes + audit addendum)
- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` (Phase C disposition; first-target shape originally disposed)
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` §11.6 (Phase D orchestration history)

**Methodology grounding:**
- `.planning/spikes/METHODOLOGY.md` (spike methodology now identified as scope-mismatched for mapping-question)
- `.planning/foundation-audit/METHODOLOGY.md` (decision-review epistemic discipline)
- `.planning/LONG-ARC.md` §51 closure-pressure-at-every-layer + §53 single-reader-framing-claims-as-authoritative
- `AGENTS.md` "CONTEXT.md epistemic discipline" + "Deliberation boundaries"

**Forward-references (V'.a execution):**
- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (revision pending per §4 step 2)
- `.planning/gsd-2-uplift/audits/202X-XX-XX-trajectory-replan-audit/` (forthcoming per §4 step 3)
- `.planning/gsd-2-uplift/METHODOLOGY-MISMATCH-FINDING.md` (forthcoming per §4 step 5)
- Codification candidate (Logan-disposition scope clarification) per §2.7 + §4 pending

---

*Single-author + in-session-collaboration fallibility caveat. This document is
Claude's interpretive structuring of the deliberation arc. The (V'.a) plan-
self-audit per §4 step 3 is the structural mitigation against framing-
inheritance in this deliberation. If any decision feels mis-recorded in
Logan's read, re-deliberation supersedes.*
