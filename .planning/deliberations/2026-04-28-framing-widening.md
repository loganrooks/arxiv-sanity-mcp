---
type: framing-widening + roadmap-derivation
date: 2026-04-28
session: post-W1-side-investigation; pre-W1-slices-2-5-dispatch
status: provisional; widens DECISION-SPACE.md without superseding it
ground: |
  - DECISION-SPACE.md (load-bearing decision reference; this artifact widens but does not supersede)
  - INITIATIVE.md (forward-staging; updated context shifts pointer to here for current operating frame)
  - 2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md (genesis-arc dynamics)
  - 2026-04-27-dispatch-readiness-deliberation.md (orchestration package + methodology observations)
  - .planning/gsd-2-uplift/exploration/01-mental-model-output.md (slice 1 pilot evidence)
  - .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md (W1 capabilities probe)
  - .planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md (W2 dive)
  - .planning/gsd-2-uplift/orchestration/cross-vendor-audit.md (orchestration audit)
  - .planning/gsd-2-uplift/orchestration/cross-vendor-reaudit.md (focused re-audit)
purpose: |
  Two-part artifact. Part I widens the framing under which the gsd-2 uplift initiative
  is being conducted: extends R1/R2/R3 to R1-R5; articulates "long-horizon development"
  as plural across six contexts including a transition-stance distinction; names plural
  significations of "uplift"; surfaces gaps Part II's roadmap should address. Part II
  derives short / medium / long-horizon work from Part I, names the deferred items log,
  and articulates what changes for slice prompts and W3 synthesis inputs.

  This artifact is the inferential bridge between (a) the framings that were operative
  when DECISION-SPACE.md and INITIATIVE.md were authored on 2026-04-26 and 2026-04-27,
  and (b) the operating frame that the side-investigations (capabilities probe + W2 dive)
  and Logan's prompts on 2026-04-27 / 2026-04-28 have made viable. It does not foreclose
  prior decisions (R1/R2/R3 hybrid persists as a live option within the widened R1-R5
  space; "long-horizon agential development" persists as a candidate framing within the
  plural-context space). It widens.

  Single-author artifact written by Claude (Opus 4.7, max effort) at Logan's direction
  post-substantive-deliberation. Subject to the same fallibility caveat as DECISION-SPACE.md
  §0 + predecessor logs. Stress-testing happens through Logan's read + future use; if any
  widening feels mis-articulated, re-deliberation supersedes.
read_order: |
  - For "what changed in our framing + why": Part I (§1-§5).
  - For "what work follows from the widened framing": Part II (§6-§9).
  - For "where each claim might be wrong": "Where this could be wrong" subsections distributed throughout.
  - For "what's the very next thing to do": §6.1 (slice prompt revisions) and §6.2 (slice 2-5 dispatch).
---

# Framing-widening + roadmap derivation — 2026-04-28

## §0. Why this artifact exists

Two days of side-investigation (capabilities probe at `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md`; W2 dive at `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md`) plus Logan's framing-pressure on 2026-04-27 / 2026-04-28 have made visible that the operating frame as of `INITIATIVE.md:50-52` and `DECISION-SPACE.md:232-262` is narrower in three ways than the substantive question warrants.

The narrowings are:

1. **R1/R2/R3 design space.** `DECISION-SPACE.md §1.8` named three upstream relationships — fork (R1), extension (R2), upstream-PR-pipeline (R3) — and proposed a hybrid favoring R2. There are at least two more strategies that don't appear in that decision space at all: orchestration-without-modifying (call it R4) and replacement-informed-by (R5). They aren't necessarily better; their absence-from-decision-space is the issue, because absence prevents weighing.

2. **Long-horizon plurality.** `DECISION-SPACE.md §3.6` flagged "whether 'long-horizon' is the right framing axis" as an open question, with `INITIATIVE.md:38-45` recording Logan's articulation referencing "multiple milestones / releases, [...] release workflows, prod, dev, integrate with the gsd-2 framework, [...] codebases become more complex, [...] salient determining conditions of the design situation change." That articulation references several distinct things at once — temporal extent (multi-year project lifespans), team-size (solo to larger), product-orientation (research-tool to consumer product), software-development-context (research-discipline vs. product-discipline), and stance-toward-future (reactive adaptation vs. anticipatory modularity). Treating these as a single axis ("long-horizon") collapses distinctions that Logan's 2026-04-28 messages explicitly preserved.

3. **Plural significations of "uplift".** The term has been used to denote at least four different things across the deliberation arc: modifying gsd-2 source (R1/R2/R3); configuring gsd-2 for our use (custom skills, hooks, prefs); building tooling around gsd-2 that serves us (orchestration scripts, custom commands); and replacing gsd-2 informed by what we learn from it (R5). These are not exclusive but are not the same act; treating "uplift" as singular has been smoothing-over distinctions that matter.

This artifact widens the framing across all three, then derives the work-shape that follows. It anchors per-claim to artifacts and gsd-2 source where the claims rest on observation.

The act of widening is itself an epistemic discipline. Per `2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` §B's methodological observations (recorded as DECISION-SPACE §4 entries), "non-exhaustive listings should stay non-exhaustive in practice"; this artifact extends the discipline to "decision spaces should not narrow without evidence."

**Where this could be wrong.** The widening claims directly above rest on (i) my interpretation of Logan's 2026-04-27 / 2026-04-28 prompts, (ii) my reading of capabilities probe + W2 dive evidence, (iii) my reading of `INITIATIVE.md:38-45` as ambiguous-across-multiple-axes rather than singular. Logan's read may differ on any of these. If Logan reads the existing R1/R2/R3 hybrid as adequately covering R4/R5 implicitly (e.g., "R2 extension naturally subsumes R4 orchestration when extension surfaces are absent"), or reads "long-horizon" as already-plural-implicitly via §3.6's framing-axis question, then the widening is performative. The honest test: do the widenings produce different downstream work-shape than the narrower framing would? §6 of Part II answers yes for slice-3 + slice-4 prompt revisions and for the deferred items log; if those revisions are valuable, the widening is operationally non-trivial.

---

# Part I — Framing widening

## §1. The R1-R5 design space

`DECISION-SPACE.md §1.8` (`DECISION-SPACE.md:232-262`) named three upstream relationships:

- **R1 fork**: take gsd-2 source, modify for our purposes. Highest maintenance burden (track upstream, resolve conflicts).
- **R2 extension**: build on top via gsd-2's extension primitives (extension manifest; workflow templates; skills; hooks; MCP tools). Cleaner separation; lower friction for adoption.
- **R3 upstream-PR-pipeline**: contribute features upstream. Lowest maintenance burden but no acceptance guarantee.

The decision proposed R2 as base + primary, with R2+R3 hybrid where workflow allows, R1 as fallback only if R2 proves infeasible. This is the "modify-gsd-2 strategies" family. The decision is anchored to assumption (1) "gsd-2 has at least *some* extension surfaces accommodating uplift content" (`DECISION-SPACE.md:249`).

### §1.1 R4 — orchestrate-without-modifying

**Definition.** Don't modify gsd-2 (no R1, no R2, no R3). Configure gsd-2 well for our use (preferences, custom skills under `~/.agents/skills/` or `.agents/skills/`, custom hooks per `docs/user-docs/hooks.md`); build orchestration tooling *around* gsd-2 that serves us (scripts that invoke `gsd headless`, parsers for `--output-format json` per `gsd-orchestrator/references/json-result.md:1-38`, custom MCP tools that compose with gsd-2's MCP server per `src/mcp-server.ts:57-67`). The gsd-2 surface remains unchanged; what changes is what's around it.

**Why this is real and distinct.** R4 is operationally distinct from R2 because R2 commits to writing extension code that runs *inside* gsd-2's extension framework (declared in `package.json` as `"gsd": { "extension": true }` per `src/extension-validator.ts:36-90`); R4 only configures gsd-2 from outside. R2 produces artifacts gsd-2 loads at runtime; R4 produces artifacts that *invoke* gsd-2 from external orchestrators. Per the W2 dive `w2-markdown-phase-engine-findings.md:70-78`, even gsd-2's own workflow templates can only invoke other GSD operations through agent-prompt mediation; this means a substantial range of "uplift" work that *might* be naturally R4-shaped (orchestrate gsd-2 from outside via headless mode + JSON parsing) wouldn't naturally fit R2.

**Why this matters.** A subset of the work the uplift initiative might produce is naturally R4 — particularly the work the capabilities probe surfaced as "composable from primitives" rather than "supported directly" (`capabilities-production-fit-findings.md:200-275`). RC/staging coordination, release-pipeline gating, multi-team release-train coordination — these are external orchestration over gsd-2's headless surface, not modifications to gsd-2 itself. If R1/R2/R3 are the only options on the table, this work is forced into a misfitting shape (R2 as "configuration extension" stretches the term; R1 as "fork to change behavior" is overkill).

**Where this could be wrong.** If "configure" reads to Logan as already covered by R2 (since custom skills and hooks load through gsd-2's extension framework, they ARE extensions), then R4 is a sub-shape of R2 rather than its own option. The honest distinction I'm drawing: R2 produces artifacts gsd-2 *integrates* (custom skill that registers as a skill; custom workflow plugin that registers as a workflow); R4 produces artifacts that *consume* gsd-2 (script that runs `gsd headless next` and parses output). The line between "configure-with-extensions" and "orchestrate-from-outside" is fuzzy; some specific work could go either way. But the fuzzy line is the reason to name R4 explicitly — to avoid implicit narrowing.

### §1.2 R5 — replacement-informed-by

**Definition.** Build something other than gsd-2, informed by gsd-2's design. The "informed-by" matters: this isn't a from-scratch alternative; it's a deliberate decision to take gsd-2's lessons (artifact discipline; phase types; workflow engines; safety primitives) and embody them in a different harness suited to a different context. R5 includes the cancellation possibility per B1 (`DECISION-SPACE.md:317-324`) but is broader: cancellation is "this isn't the right shape, do not proceed"; R5 is "this isn't the right shape *for us*; build a different shape that learns from gsd-2."

**Why this is real and distinct.** The cancellation possibility is currently framed as a binary — proceed with uplift, or cancel and re-disposition. R5 names a third path that some first-wave evidence might license: gsd-2 is well-designed but mis-aimed for our context; rather than fighting that mis-aim through R1/R2/R3, build a sibling harness aimed at our context, using gsd-2 as a design reference. Per `DECISION-SPACE.md §3.5` ("Convergence with other harness work in broader landscape"), this is already acknowledged as an open question; R5 names it as a strategic option rather than just an environmental factor.

**Why this matters now.** The capabilities probe found that gsd-2 is a substantial coding-agent application (`capabilities-production-fit-findings.md:11-20`) with its own opinions about phase types, artifact shapes, workflow engines, and team modes. If our context (long-horizon plurality discussed in §2 below) calls for opinions that diverge substantively from gsd-2's, R5 is the cleaner option than fighting through R1/R2/R3 to bend gsd-2 toward our context. Whether R5 is warranted is empirical (depends on how divergent our needs are from gsd-2's opinions); whether R5 is *a viable option* is the framing point.

**Where this could be wrong.** If R5 reads as "always available; doesn't need explicit naming," then I'm padding the design space. The argument for explicit naming: a deliberation that proceeds under R1/R2/R3 hybrid will find evidence that matches R1/R2/R3 because that's the lens it's looking through; R5 needs to be a peer option to be considered as a peer. This is the same epistemic discipline that motivated `DECISION-SPACE.md §3.6` to name the long-horizon-axis question even though "use long-horizon as the axis" was the operating frame.

### §1.3 R1-R5 as a composable space, not a tournament

The five options are not mutually exclusive. The realistic shape of any uplift outcome will mix them:

- **R2+R3** as proposed — extension is base; PRs go upstream where workflow allows.
- **R2+R4** — some uplift work is in-extension (custom skills, custom workflow plugins); some is external orchestration (release-pipeline scripts that invoke gsd-2 in headless mode).
- **R2+R3+R4** — all three; some changes go upstream, some live in our extensions, some live outside gsd-2.
- **R5+R4** — sibling harness for the parts gsd-2 doesn't fit; orchestration to compose gsd-2 with the sibling for the parts it does.
- **R1 narrow patches + R2 extension** — fork specific files where extension can't reach (per `DECISION-SPACE.md:240`); extension everywhere else.

The decision question is not "which one" but "in what proportions, with what dependencies, and with what reversibility." Some combinations are stable (R2+R3 mutually reinforcing); some are unstable (R1 narrow patches drift toward full fork over time without discipline); some are aspirational (R5 sibling-harness is much higher cost than the alternatives).

This composability shifts how the metaquestion (`DECISION-SPACE.md §1.7`) operates. The current metaquestion is "is uplift-of-gsd-2 the right shape?" with the operating frame "yes." Widened: "what mix of R1-R5, with what dependencies and proportions, fits our context?" The answer "yes, uplift-of-gsd-2" maps to "primarily R1+R2+R3 with some R4." The answer "no, not uplift" maps to "primarily R5+R4 with R3 contributions where appropriate." Intermediate mixes have intermediate metaquestion answers.

**Where this could be wrong.** Composability claims are easier to assert than to validate; some compositions might be incoherent in practice (e.g., R5 sibling-harness while also doing R3 upstream PRs creates a divided maintenance attention). The honest claim is: at least some compositions are coherent; the design space includes not just "pick one" but "weigh combinations." The further claim — that this widening changes downstream work — rests on whether evidence-collection should track contributions to multiple R's at once. §6.2's slice prompt revisions are a small test of this; if revisions don't change because R1-R5 vs. R1/R2/R3 doesn't matter for slice agents, the widening is decoratively useful but not operationally necessary.

## §2. Long-horizon plurality

`INITIATIVE.md:38-45` quotes Logan's articulation of the goal. Re-reading it carefully, the articulation references:

- "multi-year horizons of development" (temporal-extent dimension)
- "across multiple milestones / releases" (release-cadence dimension)
- "release workflows, prod, dev, integrate with the gsd-2 framework" (release-engineering dimension)
- "codebases become more complex" (complexity-scaling dimension)
- "salient determining conditions of the design situation change (constraints, stakeholder desires, reframes, changing requirements)" (situation-stability dimension)

Five distinct dimensions get bundled under "long-horizon." `DECISION-SPACE.md §3.6` flagged this as an open question — "whether 'long-horizon' is the right framing axis" — but the question's framing presupposed there is a single axis to evaluate. If the bundled-five-dimensions reading is correct, the question is mis-posed: the framing axis isn't singular.

Logan's 2026-04-28 messages elaborated on this by naming distinct contexts where "long-horizon development" means meaningfully different things. I'll articulate six contexts here, anchored to Logan's framing and extended where I think the extensions are warranted.

### §2.1 Six contexts where "long-horizon development" means different things

**Context A — Solo-research-tool over years.** One developer; project lifespan measured in years; the binding constraint is that developer's understanding capacity (can they keep track of what they decided three years ago and why?); codebase complexity scaling matters because complexity erodes recall; requirement-drift handling matters because researcher's questions shift; no external stakeholders mean no release pressure but also no failure-of-failure (no users to disappoint); the failure mode is "abandoned because lost track of what mattered." gsd-2's planning-artifact discipline (milestone/slice/task with summaries and decisions per `01-mental-model-output.md:74-77` Finding 1.6 + 1.7) is most-clearly aimed here.

**Context B — Small-team consumer-facing product.** 3-15 developers; multi-year roadmap with shifting market signals; team-coordination across feature work + bug fixes + refactors; release-cadence matters because users notice it; breaking-change posture matters because users break; failure mode is "users churn or product becomes unmaintainable." gsd-2 has team-mode primitives (`capabilities-production-fit-findings.md:114-128`) but the release-coordination side is composable-not-supported per `capabilities-production-fit-findings.md:266-272`.

**Context C — Larger-team enterprise product.** 50+ engineers, multiple parallel release branches, regulatory compliance, structured RCAs, multi-tenant deployment. gsd-2's primitives (write-gate at `src/resources/extensions/gsd/bootstrap/write-gate.ts:19-64`; journal at `src/resources/extensions/gsd/journal.ts:31-84`; forensics at `src/resources/extensions/gsd/forensics.ts:40-119`; secret-scan at `scripts/secret-scan.mjs:11-27`) gesture toward this but the coordination-at-scale tooling isn't visibly present in source.

**Context D — Platform-team across organization.** gsd-2 itself becomes the tool that other teams adopt; cross-team consistency, version-pinning, governance. This is meta — long-horizon stewardship of a tool used long-horizon. Different demands than Contexts A-C.

**Context E — Transition-as-event.** Project starts as one shape (typically Context A or a deliberate experiment) and transitions to another (typically Context B or C). The Gmail-was-a-20%-project case. The harness demands include surviving the discontinuity (state machines don't break when team grows from 1 to 10; artifact discipline doesn't collapse when cadence shifts from monthly to weekly). This is reactive scaling — adapt-under-pressure.

**Context F — Transition-as-stance (anticipatory-scaling).** Project stays in one shape (typically research-tool or experiment) but designs for the *possibility* of transition without committing to it. Logan's 2026-04-28 distinction: research that "tries to keep the possibility of not just scaling, but scaling elegantly, efficiently etc. to meet additional demand along with easily adopting more complex product / software development workflows." The harness demands include enabling smooth transition (artifact patterns that compose from solo to team without rewrite; release-workflows that exist as primitives even when not used; modular surfaces that can be activated as needed). This is anticipatory scaling — design-for-options-without-committing.

### §2.2 Why this plurality matters operationally

These six contexts impose different demands on the harness. A few examples:

- Context A demands that artifact discipline survives years of single-developer drift; gsd-2's milestone/slice/task summaries (`src/resources/extensions/gsd/types.ts:125-148` summary fields) are aimed here.
- Context B demands release-coordination primitives (release branches, RC tags, deprecation cycles); gsd-2 has `release.md` template (`src/resources/extensions/gsd/workflow-templates/release.md`) but the coordination is markdown-phase prompt-mediated, not deterministic — see W2 dive `§2` `w2-markdown-phase-engine-findings.md:36-44`.
- Context C demands compliance-grade audit trails; gsd-2's journal is structured (`src/resources/extensions/gsd/journal.ts:99-208`) but I haven't seen evidence it's compliance-grade.
- Context D demands the harness itself be governed (versioning of gsd-2; deprecation policy of gsd-2's own surfaces); slice 5's planned breaking-change posture probe will surface this.
- Context E demands that the harness *survives* transition without rewrite — gsd-2 has team-mode but the transition between solo-mode and team-mode is unprobed.
- Context F demands that the harness *enables* transition without forcing it — primitives present but optional. This is the strongest demand because it means the harness must be designed for plurality across A-E.

The harness can be designed to span multiple contexts (gsd-2 visibly aspires to span A and B, with primitives gesturing at C). But spanning has limits. As Logan observed: no harness like gsd-2 can manage Facebook-scale platform development across decades. The honest scoping question is "where on the A-F spectrum should we expect gsd-2 (uplifted or not) to be load-bearing, and where should we recommend other tools or hybrid approaches?"

### §2.3 Three operational questions the plurality opens

The plurality opens questions that the singular "long-horizon axis" framing didn't:

1. **Where is gsd-2 currently load-bearing on this spectrum?** Empirical question; addressable by user-side adoption-pattern probe (deferred — see §9). Slice 4's contribution-culture probe (`slice-04-artifact-lifecycle.md:33-49`) gestures at this but is light by design.
2. **Where could gsd-2 be made load-bearing through R1-R5 work?** Counterfactual question; depends on which R's we choose and what evidence we have about extensibility from W2 dive (some) and slices 2-5 (forthcoming).
3. **Where on the spectrum does our project's actual long-horizon need sit?** Project-anchoring question; the connection to arxiv-sanity-mcp's actual goals. This is the question §3 below tries to anchor.

### §2.4 Where this plurality could be wrong

The six contexts above are my construction; Logan's articulation in `INITIATIVE.md:42` and 2026-04-28 messages license the plurality but don't foreclose specific contexts. If Logan's read is "five contexts: A through E; my anticipatory-scaling distinction is a sub-mode of E rather than its own context F," that's a defensible read. The honest ground for treating F as its own context: F is a *stance* maintained over time, not an event; the harness demand it imposes (design-for-options) is qualitatively different from E's demand (survive-discontinuity). But that's an interpretive call.

If the plurality reading is wrong and "long-horizon" really is a single axis (perhaps "duration-of-coherent-development-cycle"), then `DECISION-SPACE.md §3.6` reduces to a calibration question rather than a framing question, and §2 here is unnecessary. The argument for plurality: Logan's 2026-04-28 message explicitly differentiated reactive-scaling from anticipatory-scaling, and explicitly named "very different than a consumer facing product that is aimed to be monetized" as a distinct context. Treating these as a single axis collapses what Logan was preserving.

## §3. Project-anchoring — where does arxiv-sanity-mcp sit?

This is the question the framing arc has not yet answered. INITIATIVE.md `:50-58` records the operating frame as "uplift gsd-2 [...] toward the goal in §1" without anchoring to arxiv-sanity-mcp's specific context. The capabilities probe deliberately framed production-fitness in generic terms. Slices 1-5 are characterizing gsd-2 in the abstract.

But the gsd-2 uplift initiative is being conducted *here*, in arxiv-sanity-mcp's `.planning/`, with arxiv-sanity-mcp's STATE.md and disposition discipline. The honest question is: what does arxiv-sanity-mcp specifically need from a development harness, and how does that need map onto the six contexts in §2?

I want to be careful here. Logan's read is binding on this question — I can offer my interpretation but the actual project-anchoring is Logan's call. With that caveat:

### §3.1 My read of arxiv-sanity-mcp's context

Per `CLAUDE.md` ("An MCP-native research discovery substrate inspired by arxiv-sanity") and `STATE.md`-like progression (v0.1 shipped, v0.2 active, multi-phase roadmap), the project sits at:

- **Primary**: Context A (solo-research-tool over years). Logan is one developer; project lifespan is multi-year (v0.1 → v0.2 → ongoing); the binding constraint is comprehension across long stretches of work.
- **Secondary aspiration**: Context F (anticipatory-scaling). The project is being conducted with discipline (ADRs, audit trails, foundation-audit, METHODOLOGY.md) that wouldn't be necessary for pure-Context-A. The discipline preserves possibilities — that other researchers might adopt arxiv-sanity-mcp; that the project might transition to research-tool-published-as-MCP-server-adopted-by-others; that the architecture might support being extended by others.
- **Possibly-future**: Context E (transition-as-event) — if arxiv-sanity-mcp gains adoption, transition to Context B or D becomes possible. This is conditional and Logan-driven, not currently active.
- **Not present**: Context C (larger-team enterprise) — no evidence the project is aimed here.

This reading positions arxiv-sanity-mcp's actual harness need as primarily-A-with-strong-F. The "uplift gsd-2" question therefore translates: what does gsd-2 need to support primarily-A-with-strong-F well?

### §3.2 What this means for the "uplift toward what" question

Under this reading, the uplift's primary axis isn't release-engineering (gsd-2's release templates already cover the modest release-cadence Context A allows). Nor is it team-coordination (Context A is solo). The primary axes are:

- **Comprehension-across-time** (Context A's binding constraint). The artifact discipline gsd-2 has is the foundation; uplift might add to it (e.g., long-arc decision-trace artifacts that compose with milestone summaries).
- **Modular-surfaces-that-stay-optional** (Context F's binding constraint). gsd-2 has primitives that gesture at this (team mode toggle; workflow plugins that activate on demand); uplift might extend this (e.g., progressive activation of release-engineering surfaces when project transitions toward Context B or E).

This is a substantively different uplift target than "uplift gsd-2 to be production-grade for Context B/C teams." Both are valid uplift directions; the project-anchoring step says the former is the primary direction for arxiv-sanity-mcp's actual context. Other contexts remain in scope (Context F's anticipatory stance keeps the door open) but are not the binding constraints.

### §3.3 Where this could be wrong

Several places.

- **Logan's read of arxiv-sanity-mcp's context might differ.** The above is my interpretation from observation of CLAUDE.md, the project structure, and Logan's stated stewardship. Logan's intent for the project might prioritize different contexts. If Logan's actual read is "Context A primarily, with no Context F aspiration" (the project is solo-research and will stay so), the §3.2 conclusions narrow further and the F-related uplift work drops out. If Logan's read is "Context F primarily — explicit goal to make this a tool other researchers adopt with team-mode capability," then Context B becomes load-bearing and release-coordination work is in-scope.
- **Whether the "primary plus secondary aspiration" framing is even honest.** A project either has explicit plans for Context F or it doesn't; "aspiration" might be a way of having one's cake and eating it too (claim Context F to justify discipline, but not actually plan toward Context F transitions). The honest variant: aspiration without plan is a stance, not a roadmap; the harness demands it places are real but bounded.
- **Whether arxiv-sanity-mcp's context is decoupled from the gsd-2 uplift initiative's context.** A possibility I've been collapsing: maybe Logan wants the gsd-2 uplift initiative to serve a *broader* community than arxiv-sanity-mcp's specific context. If "uplift gsd-2 such that it serves long-horizon agential development for whoever uses it" is the goal — i.e., the uplift is for the gsd-2 community more broadly, not specifically for arxiv-sanity-mcp — then arxiv-sanity-mcp is one user-context among many, and project-anchoring is incomplete framing. This is consistent with `INITIATIVE.md:54-55` which lists "separate project, separate repo (independent, valuable, reusable)" and "supports multiple onboarding situations." Under this reading, project-anchoring should be plural: anchor to a *set* of representative user-contexts (Logan's three onboarding situations from `INITIATIVE.md:91-96` plus the additional ones in `DECISION-SPACE.md §3.8`), not just to arxiv-sanity-mcp.

This last point matters enough to elevate. Re-reading `INITIATIVE.md §3.3` ("What onboarding situations does the uplift package support?"), the question is open with three primary candidates plus additional ones flagged in `DECISION-SPACE.md §3.8`. The reusability emphasis in `DECISION-SPACE.md:251` ("Reusability across projects is a load-bearing goal") suggests the uplift initiative is not narrowly for arxiv-sanity-mcp. So my §3.1-§3.2 anchoring is partial; the full project-anchoring is to a *set* of contexts that includes arxiv-sanity-mcp plus other plausible adopters.

This widens the work: Part II's roadmap should treat user-context-plurality as a parameter, not assume arxiv-sanity-mcp is the only context.

## §4. Plural significations of "uplift"

`INITIATIVE.md §1` and `DECISION-SPACE.md §1.2` define "uplift gsd-2" implicitly as work-on-gsd-2-to-improve-it-for-long-horizon-development. The R1/R2/R3 hybrid suggests this is "modify-gsd-2 strategies."

But across the deliberation arc, "uplift" has been used to denote at least four different acts:

1. **Modify gsd-2 itself** (R1/R2/R3 family). The thing changes.
2. **Configure gsd-2 well for our use** (custom skills, hooks, prefs; no upstream changes). The thing stays the same; what we put around it changes.
3. **Build tooling around gsd-2 that serves us** (orchestration scripts, custom commands, parsers; sits outside gsd-2). The thing stays the same; we use it through additional layers.
4. **Replace gsd-2 informed by what we learn** (R5). The thing is set aside; a new thing is built that learns from the old.

These are different acts with different costs, reversibility, and downstream commitments. The current framing ("uplift" as singular) collapses them.

The plurality matters because:

- **Different Rs are appropriate for different acts.** (1) maps to R1/R2/R3. (2) and (3) are R4. (4) is R5. The R1-R5 widening in §1 above is the strategy-side; this is the act-side.
- **Different acts have different evidence requirements.** (1) requires evidence about gsd-2's extension surfaces and contribution culture (slice 4 work). (2) requires evidence about gsd-2's preference and skills systems (capabilities probe surfaced this). (3) requires evidence about gsd-2's headless and JSON output surfaces (capabilities probe surfaced this). (4) requires evidence about gsd-2's design decisions and where they don't fit our context (synthesis-stage work).
- **Different acts have different decision-points.** (1) requires the metaquestion "is uplift-of-gsd-2 right" to land "yes, modify-it." (2) and (3) are compatible with metaquestion "yes, modify it" *or* metaquestion "no, don't modify, just use it." (4) requires metaquestion "no, don't modify; build something better."

### §4.1 Composability among the four acts

Like R1-R5, the acts compose. A realistic uplift outcome will likely include some of (1) [extension or PR or fork-narrow-patch] + (2) [configure with custom skills/hooks/prefs] + (3) [orchestration tooling around gsd-2 for our specific workflows]. (4) is the alternative-path; (1)+(2)+(3) is the primary path under "yes, uplift-of-gsd-2."

The mix matters for resource allocation. If the uplift work is 70% (3) [orchestration around], 20% (2) [configuration], 10% (1) [extensions], the primary investment is in our project's specific workflow tooling, not in gsd-2 itself. If it's 70% (1) [extensions] and 30% the others, the primary investment is in gsd-2's surface area. These are different work-shapes warranting different resource plans.

### §4.2 Where this could be wrong

If the four acts collapse adequately into "configure-and-extend gsd-2" (encompassing 1+2 mostly, with 3 as an implementation detail of 2 and 4 as a fallback that doesn't merit its own naming), then the plurality is decorative. The argument for explicit naming: each act has a distinct decision-shape, evidence requirement, and resource profile. Treating them as one collapses operational distinctions that matter for planning.

If Logan's read is "the four acts are operationally indistinguishable from outside, and the uplift will produce whatever-mix-emerges-from-evidence," then the decomposition above is over-engineered. The argument for the decomposition: the resource and decision distinctions are pre-evidence; we should plan for the plural acts even before we know which mix the evidence will license.

## §5. Where the framing-widening preserves vs revises

To make the widening's relationship to existing artifacts clear:

**Preserves (no change):**
- `DECISION-SPACE.md §1.7` metaquestion ("is uplift-of-gsd-2 the right shape?") — preserved as a meaningful question, but with the answer space widened from {yes, no} to {primarily-modify, primarily-orchestrate-without-modifying, primarily-replace-informed-by, mixed} per §1.3 above.
- `DECISION-SPACE.md §1.11` first-wave aim ("characterize gsd-2 carefully enough that second-wave can decide whether/what to do") — preserved verbatim.
- `DECISION-SPACE.md §1.12` wave structure D′ — preserved.
- All B1-B6 decisions in `DECISION-SPACE.md §1.11-§1.16`.
- INITIATIVE.md goal articulation — preserved as one operating frame; this artifact widens what that articulation could mean.

**Widens (new shape; not contradiction):**
- `DECISION-SPACE.md §1.8` R1/R2/R3 hybrid → R1-R5 design space per §1 above. The R2-base recommendation persists as the working hypothesis within the R1-R5 space; widening allows other compositions to be considered as evidence warrants.
- `DECISION-SPACE.md §3.6` "long-horizon framing axis" question → six-context plurality per §2 above. The question persists as open; widening provides a structured space within which the open question can be answered (or which can itself be revised if six contexts isn't right).
- INITIATIVE.md "uplift" usage → four-act plurality per §4 above. The act-side complement of the strategy-side widening.

**Adds (new content):**
- Project-anchoring framework per §3.
- Connection between user-context-plurality (Logan's three onboarding situations + additional candidates) and the framing-widening.

**Where this could be wrong.** If Logan reads the widening as superseding rather than widening (e.g., "we no longer commit to R2-base; we're open to all five strategies equally"), the operating-frame implication is bigger than I intend. The honest claim: R2-base persists as the working hypothesis under §1.8; the widening lets evidence push toward other compositions if it appears, rather than forcing evidence into R2-shape. If the working hypothesis is dropped explicitly, that's a separate decision warranting its own deliberation; this artifact doesn't make that decision.

---

# Part II — Roadmap derivation

## §6. Short horizon (next 1-3 sessions)

The work that immediately follows from Part I is:

### §6.1 Slice prompt revisions

Based on (a) the W2 dive evidence about gsd-2's two-engine architecture, (b) the capabilities probe evidence about extension primitive plurality, and (c) the framing-widening above, two slice prompts warrant small revisions before slices 2-5 dispatch.

**Slice 3 (workflow surface) — Q2 revision.** Currently asks "Does gsd-2 provide automation, and if so what?" (`slice-03-workflow-surface.md:25-27`). The W2 dive found gsd-2 has two architecturally distinct workflow engines (markdown-phase and yaml-step) per `w2-markdown-phase-engine-findings.md:36-44`. A medium-effort slice agent might surface this through Q1 + Q2 together, but might not. The revision adds an explicit subsidiary asking about multiple-workflow-engines/dispatch-shapes without naming them, preserving existence-first discipline.

Proposed Q2 text:
> "Does gsd-2 provide automation, and if so what? **Specifically: are there multiple workflow engines or dispatch shapes within gsd-2's automation?** First establish whether gsd-2 automates anything beyond standard CLI command invocation. If yes: what kinds of dispatch / execution shapes exist (e.g., agent-prompted vs deterministic; phase-based vs graph-based; one-shot vs multi-phase)? Cite source for each shape. What gets automated and what is left to manual user invocation? If a meaningful human-vs-machine distinction surfaces in source, describe how it is drawn; if no such distinction is articulated, say so."

The added question in bold is the substantive change; the existing existence-first framing for human-vs-machine is preserved.

**Slice 4 (artifact lifecycle + extension surfaces) — Q2 addition.** Currently asks whether extension surfaces exist (`slice-04-artifact-lifecycle.md:27`). The capabilities probe surfaced multiple extension primitives — extension manifest, workflow templates, skills, MCP tools, ecosystem extensions (`capabilities-production-fit-findings.md:144-164`). Slice 4 Q2 in current form would catch these as a list; might miss the relationships (are they unified or distinct subsystems?).

Proposed Q2 addition (appended to existing question):
> "If multiple extension mechanisms appear (e.g., extension manifest vs workflow templates vs skills vs MCP tools), what are the relationships between them? Are they unified or distinct subsystems with different lifecycles? Cite source for each mechanism's registration / discovery / invocation."

This surfaces composition-vs-independence at slice level (descriptive) without requiring synthesis-stage judgment.

**Slices 1, 2, 5 — no changes.** Slice 1 is already done; slices 2 and 5 were marked clean-to-proceed by the focused re-audit (`cross-vendor-reaudit.md`). The framing-widening above doesn't add slice-prompt-level questions to them; the framing's effect on slice 5 is via synthesis-stage integration, not via additional slice-level questions.

**Where these revisions could be wrong.**
- If slice 3 in current form would naturally surface the two-engine distinction (e.g., because slice agent reads `workflow-templates.ts` and notices the mode field), the revision is redundant. My estimate: 60% current Q2 catches it, 40% it doesn't. Cost of revision: ~10 lines of prompt change. Cost of missing: synthesis has to reconstruct the distinction from inventory.
- If slice 4 in current form would naturally surface the extension-mechanism relationships (because slice agent reads `extension-manifest.json`, `workflow-plugins.ts`, `skills` docs and notices they share or differ), the addition is redundant. My estimate: 50% current catches relationships, 50% it doesn't.
- The revisions are conservative — they add subsidiaries rather than restructuring questions. If the widened framing actually warrants more substantial restructuring (e.g., a new Q6 in slice 3 for "is there progressive activation of release-engineering surfaces for Context F-style projects"), conservative revisions miss it. My read is conservative is right because deeper restructuring should be informed by slice 1 pilot evidence we already have, not by speculative framing-widening; and the framing-widening's Context F demand is more a synthesis-stage integration question than a slice-stage observation question.

### §6.2 Slices 2-5 dispatch

After §6.1 revisions, dispatch slices 2-5 in parallel per `OVERVIEW.md §3.3`. The W2 audits per `audit-spec.md` follow conditionally (slice 4 mandatory; others per the revised criteria in audit-spec.md `:10-18`).

Time estimate: 30-60 min wall-clock for parallel dispatch; 5-15 min per audit if dispatched.

### §6.3 W3 synthesis with widened inputs

When W3 synthesis runs per `synthesis-spec.md`, its inputs should include this artifact alongside DECISION-SPACE.md and INITIATIVE.md. The synthesis-spec.md currently lists:

```
3. **DECISION-SPACE.md** at `.planning/gsd-2-uplift/DECISION-SPACE.md`, specifically:
   - §1.7 (metaquestion C-with-non-exhaustive-teeth)
   - §1.8 (R2/R3 hybrid)
   - §1.11 (first-wave aim — characterize-for-decision)
   - §1.12 (wave structure D′)
   - §3.4 (long-horizon framing-axis question)
4. **INITIATIVE.md** at `.planning/gsd-2-uplift/INITIATIVE.md`, specifically:
   - §1 (goal articulation)
   - §3 (open framing questions)
```
(`synthesis-spec.md:36-44`)

Add to inputs:
- **`.planning/deliberations/2026-04-28-framing-widening.md`** specifically:
  - §1 (R1-R5 design space; widens DECISION-SPACE §1.8)
  - §2 (six-context long-horizon plurality; widens DECISION-SPACE §3.6)
  - §3 (project-anchoring framework)
  - §4 (plural significations of uplift)
  - §5 (preservation/revision boundary)

The synthesis output structure (`synthesis-spec.md:53-162`) doesn't need new sections — the existing §2.4 already covers "long-horizon framing-axis" and could be widened to address plurality; §2.5 covers "design-shape candidates" and could integrate the four-act plurality. The widening appears in synthesis as a richer integration framework, not as new sections.

This update should happen as part of §6.1 revisions (sibling to slice prompt revisions) or independently before W3 synthesis runs. I'd combine with §6.1 to avoid two revision passes.

**Where this could be wrong.** If synthesis-spec.md ends up needing structural revision (e.g., dedicated section for R1-R5 mix recommendation, or dedicated section for context-plurality-anchoring), the conservative input-list-only update misses it. My read: synthesis-spec.md's existing structure can absorb the widening as input-richer rather than structurally-different. If the synthesizer (Claude xhigh in W3) finds the existing structure inadequate, that itself would be a synthesis-stage finding flagged in the synthesis output; the structure can be revised in the next iteration.

## §7. Medium horizon (next 1-3 months)

Per the existing wave structure in `OVERVIEW.md §1`, after W1 + W2 + W3 lands the path is:

- **Incubation checkpoint per `DECISION-SPACE.md §2.3`.** Re-evaluates goal articulation, direction-shifting evidence, R1/R2/R3 hybrid (now R1-R5) viability, second-wave proceed/re-disposition decision.
- **Conditional second-wave-scoping per `DECISION-SPACE.md §1.6`.** If incubation says proceed: second-wave scopes the design phase. If incubation says re-disposition: deliberation note + revised operating frame.
- **Conditional cancellation per `DECISION-SPACE.md §1.11` B1.** If first-wave evidence + incubation surface that the operating frame is wrong-shaped, cancellation is a substantive output.

The framing-widening adds:

- **R5 disposition.** If first-wave evidence supports R5 (replacement-informed-by) being the right composition, second-wave-scoping has a different shape: design a sibling harness rather than design uplift extensions.
- **Context-plurality disposition.** If first-wave evidence supports a different context-mix than my §3.1 anchoring (e.g., Context F should be primary, not Context A), second-wave-scoping prioritizes different work.
- **Side-probe trigger evaluation.** Several side-probes are warranted but deferred (per §9 below). Incubation checkpoint should evaluate whether any side-probe is on the critical path for second-wave-scoping decisions; if yes, dispatch before second-wave; if no, defer further or drop.

The medium-horizon work is substantively unchanged in shape (W1 → W2 → W3 → checkpoint → second-wave); the widening affects the *content* of checkpoint deliberation and second-wave-scoping decisions.

## §8. Long horizon (1+ year considerations)

Most of the long-horizon work is already documented elsewhere; this section names it for completeness.

- **Migration of `.planning/gsd-2-uplift/` to a dedicated repo.** Per `INITIATIVE.md` frontmatter `migration_trigger`, when the dedicated repo is created. Not yet active; should not block on it.
- **Stage 1 audit deferred quality findings.** Per the post-Stage-1 handoff at `.planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md` and STATE.md pending-todos. Quality work that doesn't block first-wave dispatch.
- **Methodology codification of session-disciplines.** Tracked in `DECISION-SPACE.md §3.9` and `2026-04-27-dispatch-readiness-deliberation.md §B`. Threshold-based codification; not yet at threshold.
- **Production-fitness synthesis as durable artifact.** The capabilities probe + W2 dive material answers Logan's substantive production-fitness questions but isn't yet in a citable synthesis form. Optional follow-up if the conversational answer in this session's chat history needs to be made durable.

## §9. Deferred items log

Items that have been surfaced but not addressed; ordered by approximate priority for synthesis or later work.

### Probe / investigation deferrals

1. **W2 dive on `commands-pr-branch.ts`.** Per `w2-markdown-phase-engine-findings.md:112`. Validates §C.3 hotfix-backport candidate's programmatic-cherry-pick assumption. Triggered if R1-R5 deliberation lands on R2 with hotfix-coordination as a load-bearing intervention.
2. **W2 dive on effective-preferences emission.** Per `capabilities-production-fit-findings.md §D` and W2 dive `§9`. Validates §C.8 candidate. Triggered if the docs/source drift mitigation candidate becomes load-bearing.
3. **Competitor-landscape probe.** Per my prior message §3 gap analysis. Asks: what other agential development frameworks exist (Aider, OpenHands, Cline, Roo, etc.)? How does gsd-2 compare? Triggered if R5 (replacement-informed-by) becomes a serious option, or if the metaquestion needs comparison frame.
4. **Non-coding-workflow integration probe.** Per Logan's 2026-04-28 framing about consumer-facing products + product lifecycle management. Asks: what does gsd-2 offer for PRD-to-code workflows, incident response, UAT/stakeholder review? Triggered if Context B/C/E becomes load-bearing.
5. **Temporal-stability probe.** Per my prior gap analysis. Asks: which gsd-2 surfaces are stable enough to build R2 extensions on vs actively churning? Triggered before any R2 work that depends on specific surfaces.
6. **User-side adoption-pattern probe.** Per my prior gap analysis. Asks: who actually uses gsd-2, in what contexts, with what success patterns? gh issue/PR analysis; downstream adopter survey. Triggered if reusability scope (`DECISION-SPACE.md:251`) becomes a binding constraint.

### Methodology / codification deferrals

7. **Wave-structure-on-large-targets discipline.** Per Logan's 2026-04-27 framing and the in-flight capabilities probe → W2 dive pattern. The discipline: when target is large, default to W1 survey + W2 deep-dives + W3 synthesis rather than single-pass. Codify in `AGENTS.md` or `METHODOLOGY.md` after sample size (capabilities arc + slices 2-5 if they go through W2 audits = ~3 samples).
8. **Tier-the-model-to-the-task discipline.** Same source. The discipline: exploration tier → cheap; reasoning/synthesis → expensive. Codify per same threshold.
9. **Don't-dispatch-before-precondition-check discipline.** Per `2026-04-27-dispatch-readiness-deliberation.md §B.5`. Procedural mitigation: scan artifact's preconditions before dispatch. Already in the deliberation log; codification in AGENTS.md when methodology section becomes a defined surface.

### Audit / quality deferrals

10. **Stage 1 audit deferred quality findings.** §A decision-table compression of §1.2 bifurcation; "Logan's framing" parenthetical in §4.5; §3 prefix vs §5.1 deliverables-vs-informing tension; R2-base contingency phrasing; "load-bearing" overuse. Per `STATE.md` pending-todos.
11. **Cross-vendor audit / re-audit caveats integration.** Both audits flagged "may have read framing-leak aggressively" per their §10 caveats. Synthesis should weigh the audit findings against this caveat rather than treating audit as authoritative.

### Synthesis-stage deferrals

12. **Telemetry / observability as design-surface.** Capabilities probe inventoried; question is whether features compose as integrated story or as independent affordances. Synthesis-stage question.
13. **Security / trust model coherence.** Same shape — capabilities probe inventoried; design-coherence is synthesis-stage.
14. **Solo-to-team transition coherence.** Slice 1 + slice 4 will surface team-mode features; question is whether features compose toward smooth Context A → Context B/E transition. Synthesis-stage.
15. **Two-engine progressive activation.** W2 dive established markdown-phase / yaml-step distinction; synthesis-stage question is whether the distinction fits Context F's progressive-activation demand.

### Roadmap-related deferrals

16. **Migration of `.planning/gsd-2-uplift/` to dedicated repo.** Conditional on initiative graduating from staging.
17. **Production-fitness synthesis artifact.** Optional; convert capabilities-probe + W2-dive material into durable citable form.

This list expands as evidence and deliberation proceed. STATE.md should reference this artifact's §9 as the current source for deferred items related to the gsd-2 uplift initiative; STATE.md retains its own pending-todos for project-level work outside the initiative.

## §10. Where this artifact's recommendations could be wrong

Honest aggregation of where Part I + Part II might mislead.

### §10.1 Logan reads the widening as decoratively useful but not operationally needed

If Part II's slice prompt revisions (~15 lines of prompt change) and synthesis input list update are the only operational consequence of the widening, then the widening is doing 700+ lines of artifact work for what could have been a 30-minute slice prompt edit. The justification: the widening creates an artifact future synthesis reads from; without the artifact, synthesis has only the older narrower framings to integrate. Whether the artifact's reading-value is worth its authoring-cost is a judgment that depends on (i) whether synthesis actually reads it, (ii) whether the deferred items log gets used, (iii) whether the framing-widening surfaces second-wave-scoping considerations that wouldn't have been raised otherwise. I think the answer is yes on all three — the alternative (do widening implicitly via slice revisions only) doesn't preserve the inferential chain and rebuilds the framing context every session.

### §10.2 The R1-R5 widening over-states distinctions

If R4 collapses cleanly into R2 (because configuration-with-extensions IS extension), and R5 collapses cleanly into "cancellation per B1 + something else" (because replacement-informed-by isn't a meaningfully distinct strategy), the five-strategy framing is performatively richer than warranted. The argument for explicit naming: each has distinct decision shape and resource profile in the §1.1, §1.2 elaborations. The honest test: does §6.2 dispatch + §7 incubation actually use R4/R5 distinct from R1/R2/R3? If not, the distinctions are decorative. My estimate: R4 distinction will matter at synthesis (some uplift work is naturally R4-shaped); R5 distinction will matter at incubation (cancellation should be more nuanced than binary).

### §10.3 The six-context plurality over-fragments long-horizon

Six contexts is a lot. If the substantive distinction is just A (solo-research) vs B (small-team-product) with the others as gradations, then the six-fold framing is over-engineered. The argument for six: each has distinct harness demands (§2.2 elaboration). The honest test: does Part II's roadmap actually differentiate by context, or does it collapse to "primarily A, secondarily F"? §6 doesn't differentiate explicitly; §9 deferred items 4-6 (non-coding workflow; temporal stability; user adoption pattern) implicitly differentiate. Marginal evidence the six-fold framing is operational.

### §10.4 Project-anchoring is presumptuous

§3.1's reading of arxiv-sanity-mcp as "primarily Context A with strong Context F secondary" is my interpretation; Logan's read is binding. If Logan reads the project as already-Context-B (research tool aimed for community adoption with team-development plans), §3.2's conclusions narrow incorrectly toward Context A. If Logan reads it as pure-Context-A (no F aspiration), §3.2 over-stretches. I've tried to flag this in §3.3 but the structural risk is that downstream work reads §3.1-§3.2 as authoritative when it's interpretive. Logan should explicitly disposition §3 if it's wrong.

### §10.5 The act-side plurality (§4) collapses with the strategy-side (§1)

R1/R2/R3 already implicitly cover the "modify-gsd-2" act (=1); R4 covers (2) and (3); R5 covers (4). So the strategy-side and act-side might be saying the same thing twice. The argument for both: strategy describes upstream relationship; act describes the work-shape. R2 strategy can be done as act (1) [extension code modifying gsd-2's behavior] or act (2) [configuration via custom skills that happen to use the extension API but don't modify behavior]. The strategy/act distinction is real but admittedly subtle. If it's not load-bearing for downstream work, it's redundant.

### §10.6 The deferred items log will rot

§9 enumerates 17 items. Most lists like this become stale: items are addressed without being removed; new items are added without being prioritized; the list becomes a compost heap. The mitigation: STATE.md references this artifact's §9 (rather than duplicating); when an item is addressed, it gets moved out (struck-through or dated-and-archived). Whether this discipline holds is a meta-question about how the artifact is maintained.

### §10.7 The widening freezes the framing prematurely

If first-wave evidence + incubation reveal a different framing entirely (e.g., "this is fundamentally about agential-development skills as a Claude Code feature, not about gsd-2 uplift"), this artifact's widening becomes scaffolding to be discarded rather than built on. The argument for the widening anyway: even if the framing shifts dramatically, the act of widening preserves the inferential chain; future readers can see how the framing evolved.

## §11. Cross-references

**Sibling artifacts (decisions / dynamics).**
- `.planning/gsd-2-uplift/DECISION-SPACE.md` — load-bearing decision reference; this artifact widens but does not supersede.
- `.planning/gsd-2-uplift/INITIATIVE.md` — forward-staging artifact; this artifact joins the operating-frame inputs.

**Predecessor logs.**
- `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` — genesis-arc dynamics.
- `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md` — orchestration package + B1-B6 decisions + §B methodological observations.

**Evidence inputs (W1 work).**
- `.planning/gsd-2-uplift/exploration/01-mental-model-output.md` — slice 1 pilot.
- `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md` — capabilities probe.
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md` — W2 dive.

**Audit inputs.**
- `.planning/gsd-2-uplift/orchestration/cross-vendor-audit.md` — orchestration audit (material findings).
- `.planning/gsd-2-uplift/orchestration/cross-vendor-reaudit.md` — focused re-audit (clean to proceed).

**Project doctrine referenced.**
- `LONG-ARC.md` — anti-patterns including closure-pressure-at-every-layer; this artifact resists that pressure by widening.
- `AGENTS.md` — "Project-specific anti-patterns to detect" — referenced; the widening engages with the closure-pressure-at-meta-layer pattern.
- `CLAUDE.md` — project identity; arxiv-sanity-mcp's context per §3.1 is grounded here.
- `.planning/spikes/METHODOLOGY.md` and `.planning/foundation-audit/METHODOLOGY.md` — methodology disciplines.
- `INITIATIVE.md §3.3` and `DECISION-SPACE.md §3.8` — onboarding situation candidates relevant to §3.3 elaboration.

**Source citations to gsd-2.** Throughout this artifact; primary sources are gsd-2 README, VISION, CONTRIBUTING, plus source files at `src/resources/extensions/gsd/`, `src/cli.ts`, `src/headless.ts`, `src/mcp-server.ts`, and workflow-templates / scripts directories.

---

*Single-author framing-widening + roadmap-derivation artifact written 2026-04-28 by Claude (Opus 4.7, max effort) at Logan's direction post-substantive-deliberation across 2026-04-27 / 2026-04-28 messages. Subject to the same fallibility caveat as `DECISION-SPACE.md §0` and predecessor logs. The widening's value depends on whether it preserves the inferential chain for synthesis and incubation deliberation; if it doesn't get read or doesn't change downstream work, the cost was sunk for marginal benefit. Logan's read is binding on whether the widening was warranted.*
