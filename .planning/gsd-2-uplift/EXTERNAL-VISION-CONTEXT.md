---
type: standing-context
date: 2026-05-01
status: standing — load-bearing for gsd-2-uplift work + cross-references harness-studio
audience: future-Logan, future-Claude (in fresh sessions, including post-extraction sessions in the new repo), subagents dispatched on uplift work
parent_project: arxiv-sanity-mcp
relates_to:
  - ~/workspace/projects/gsd-2-uplift/.planning/INITIATIVE.md
  - .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (DUPLICATE; this side)
  - ~/workspace/projects/gsd-2-uplift/.planning/DECISION-SPACE.md
  - ~/workspace/projects/gsd-2-uplift/.planning/deliberations/2026-04-28-framing-widening.md
  - .planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md (DUPLICATE; this side)
  - ~/workspace/projects/harness-studio/docs/vision/problem-statement.md
  - ~/workspace/projects/harness-studio/docs/handoff/current.md
  - ~/workspace/projects/harness-studio/docs/deliberations/2026-05-01-gsd-2-substrate-transfer-and-pressure-clarification.md
  - ~/workspace/projects/paddock/PARKED.md
post_extraction_disposition: DUPLICATE — this artifact lives on both sides of the extraction with bidirectional cross-references; both copies updated to point at the other (per trajectory plan §1.7 RELATIONSHIP-TO-PARENT pattern, applied recursively to this artifact)
sibling_copy: ~/workspace/projects/gsd-2-uplift/.planning/EXTERNAL-VISION-CONTEXT.md
sync_discipline: |
  This is the arxiv-sanity-mcp side of the DUPLICATE pair. Substantive edits should
  land on both copies; verify pair-coherence by diffing against the sibling
  (gsd-2-uplift/.planning/EXTERNAL-VISION-CONTEXT.md) before committing.
extraction_log: .planning/extraction/EXTRACTION-LOG.md (§5)
extraction_completed: 2026-05-08
---

# External Vision Context — gsd-2-uplift's Relationship to harness-studio's Vision

This document records (i) what gsd-2-uplift specifically is as a project; (ii) the pressure-not-destination relationship to harness-studio's master-consultant operating-model vision; (iii) substrate-vision properties the eventual harness should embody (12 articulated 2026-05-01); (iv) scope-discipline for evaluating candidate interventions; (v) Phase D mapping purpose under this framing; (vi) test-case anchors and project-portfolio context; (vii) meta-disciplines surfaced through the conversation that produced this artifact.

It lifts the substrate-vision-articulation work done in the 2026-05-01 turn-cluster (post-(V′.a) trajectory-replan, pre-(V′.a) Step 2 trajectory-plan revision authoring) into a place future sessions can find and build on without losing the reasoning trail.

## §0. How to read this document

**Audience.** Future-Logan, future-Claude in fresh sessions, subagents dispatched on (V′.a) execution, future plan-revision auditors, post-extraction sessions in the dedicated gsd-2-uplift repo.

**What this document IS.** Standing-context for gsd-2-uplift work. Records the corrected understanding of what gsd-2-uplift is, what the harness-studio relationship is, what substrate-vision-properties the work serves, and the discipline for evaluating scope.

**What this document IS NOT.**
- Not the (V′.a) Step 2 trajectory-plan revision itself (authored separately).
- Not a methodology-mismatch artifact ((V′.a) Step 5 standalone).
- Not a vision-statement *for harness-studio* — that lives in `~/workspace/projects/harness-studio/`.
- Not a commitment that harness-studio's vision will be reached via gsd-2-uplift work — gsd-2-uplift is its own thing per §2.

**Single-author + in-session-collaboration fallibility caveat.** Same as DECISION-SPACE.md §0 + framing-widening §0 + RELATIONSHIP-TO-PARENT.md §1.1. Substantive corrections to my own framing happened *multiple times* during the conversation that produced this artifact (closure-pressure-into-elaboration pattern recurred per 2026-04-30 §5.4); the structural mitigation against framing-inheritance in this artifact is plan-self-audit in (V′.a) Step 3 + future review.

**Read-order.**
- For "what gsd-2-uplift is, simply": §1.
- For "how it relates to harness-studio": §2.
- For "what the substrate should eventually do": §3 (12 properties).
- For "how to think about scope": §4.
- For "how mapping-shape Phase D operates under this framing": §5.
- For "what projects this serves": §6.
- For "meta-disciplines surfaced": §7.
- For "what's deferred": §8.

## §1. What gsd-2-uplift specifically is

**Project-shape definition (corrected 2026-05-01):**

> gsd-2-uplift is an **identity-preserving, pressure-respecting** uplift of gsd-2 that **pushes its limits in reasonable ways** toward a set of **reasonable objectives — discovered and refined through exploration**, **anchored against concrete test cases**, producing an **uplifted-gsd-2 that is itself useful for current project work** without committing to convergence on harness-studio's full vision.

Five active properties unpack this:

1. **Identity-preserving.** Modifications maintainable as patch-system; gsd-2's own identity (standalone-agent-runtime shape, substrate decisions, existing surfaces) preserved. Hard constraint — patches that destroy gsd-2's identity are out. Identity-distortion is narrow in practice (see §4.3): applies to sweeping ontological replacements (replacing the milestone/phase/task ontology; replacing the artifact-discipline; replacing the runtime model; forcing single-shape additions), not most feature-additions.

2. **Pressure-respecting.** Anti-foreclosure constraints from harness-studio's vision shape design choices (preserve portable artifacts; don't make gsd-2 a sovereign product ontology; preserve workflow-lane awareness). These constraints don't bridge gsd-2-uplift *to* harness-studio — they keep harness-studio's optionality from being foreclosed. Pressure-not-destination per §2.

3. **Pushing limits in reasonable ways.** Not minimalist. The uplift's purpose is to push what gsd-2 can do — within bounds. "Reasonable" is the discipline; "push" is the posture. Per Logan 2026-05-01: "always trying to perhaps push the limits in reasonable ways, that is what the uplift is for."

4. **Reasonable objectives, exploration-discovered.** Objectives aren't pre-committed against an imported vision. They're discovered through exploration (mapping-shape Phase D), refined as evidence accumulates, kept reasonable-not-aspirational. **Burden-of-proof rests on exclusion** (§4.1): default candidate-in-scope; exclusion requires demonstrated grounds.

5. **Anchored against concrete test cases.** Currently arxiv-sanity-mcp; eventually prix-guesser-shape and other concrete project work. *Not* anchored against vision-class abstractions (those are harness-studio's classification space).

**Output:** an uplifted-gsd-2, useful for Logan's actual project work, with the harness-studio pressure preserved as live context for harness-studio's separate eventual development.

## §2. Pressure-not-destination relationship to harness-studio

harness-studio (`~/workspace/projects/harness-studio/`) holds the master-consultant operating-model vision: a harness that lets a small operator-plus-agent system approximate the useful capabilities of a small expert product team. The vision is articulated in `docs/vision/problem-statement.md` and elaborated in `docs/handoff/current.md`'s layered-architecture hypothesis (operating-model / workflow-playbooks / expert-role-modules / execution-kernel / feedback-and-governance-loops).

**Relationship as of 2026-05-01:**

- gsd-2-uplift is **its own thing** (its own scope, destination, evaluation criteria).
- harness-studio is **a pressure**, not a destination. The pressure shapes gsd-2-uplift's design via anti-foreclosure constraints. It does not make gsd-2-uplift bridge *to* harness-studio.
- The deferred question — could uplifted gsd-2 eventually be utilized *by* harness-studio (as one execution kernel among possibly several) — is a **separate, later question**. Not gsd-2-uplift's current commitment.

**Update to harness-studio's 2026-04-24 framing.** harness-studio's `docs/deliberations/2026-04-24-bridge-harness-and-governance-seed.md` originally framed the predecessor uplift project (gsd-modifier) as a "bridge harness" with implicit graduation-to-harness-studio. Logan's 2026-05-01 clarification rejects that presupposition. The bridge-harness language is preserved in harness-studio's docs as historical record; the corrected framing is recorded in harness-studio's `docs/deliberations/2026-05-01-gsd-2-substrate-transfer-and-pressure-clarification.md` (sibling to this artifact).

**Substrate transfer.** When harness-studio was authored 2026-04-24, the bridge-harness role was held by gsd-modifier (work on the original v1-GSD). When gsd-2 (`~/workspace/projects/gsd-2-explore/`) emerged as a different substrate (2026-04-26+), the uplift target shifted; gsd-modifier's slot is now gsd-2-uplift's. But the substrate change came with the framing change: gsd-2-uplift is *not* a bridge-toward-harness-studio; it's its own pressure-respecting independent project.

**Reading direction.**
- For *vision-content* (master-consultant operating model, layered architecture, project-class plurality, candidate artifact families like OPERATING-MODEL.md / PRODUCT-THESIS.md / WORKFLOW-LANES.md / DECISION-LOG.md / FEEDBACK-LOOPS.md / RELEASE-PLAN.md / RISK-REGISTER.md / QUALITY-BAR.md): see harness-studio.
- For *gsd-2-uplift's project-shape and scope-discipline*: this artifact + INITIATIVE.md + DECISION-SPACE.md + framing-widening.

## §3. Substrate-vision properties (12)

The 12 properties below are *aspirational properties of the eventual substrate*. gsd-2-uplift can pursue each at varying depths (shallow / mid / deep) per Phase D mapping evidence; harness-studio's distinct contribution is the **meta-selection layer** (project-class classification + workflow-selection + operating-model-per-class + expert-role-module orchestration) that orchestrates these capabilities for different project classes.

**Per the burden-of-proof-on-exclusion discipline (§4.1)**, all 12 are candidate-in-scope for gsd-2-uplift. Exclusion requires demonstrated grounds, not preemptive narrowing.

**Origin:** The original 7 came from the 2026-05-01 turn-cluster opener (Claude's articulation of "what gsd-2 would ideally become"). Logan invited expansion (a/b/c/d) at /effort max; the corrected list reflects 4 unchanged + 3 modified + 4 added (+ 1 merge of two prior properties), settling at 12. Detailed reasoning in conversation history; this artifact records the committed set.

### Property 1 — Comprehension survives time

Decisions made three years ago are reconstructable in their reasoning-context, not just their outcomes — what was at stake, what alternatives were weighed, what evidence shifted the call, what would re-open it. The substrate carries this faithfully without requiring perfect recall from the human.

### Property 2 — Methodology (interpretive + practice + meta-disciplines) is operational, not aspirational

Disciplines like paired-review (M1), framing-widening, closure-pressure detection, comfort-language detection, traces-over-erasure aren't optional polish — they're routine practice the substrate makes easy enough to do every time. The substrate detects when they're being skipped or performed-rather-than-applied. Coverage spans: **interpretive disciplines** (six lenses per spike methodology); **practice disciplines** (paired-review, framing-widening, model-verification, etc.); **meta-disciplines** (offshoot pattern, frame-revision-check, burden-of-proof-on-exclusion, Logan-disposition scope discipline per 2026-04-30 §2.7).

### Property 3 — Frame-errors AND scope-errors surface early *(modified)*

The closure-pressure-into-elaboration pattern produces both frame-errors (commitment to a wrong frame; elaborate within-frame work) and scope-errors (out-of-scope vision distorting in-scope work). Both should surface structurally. **Frame-errors** caught via frame-revision-checks at phase boundaries (per (V′.a) Step 4). **Scope-errors** caught via scope-pressure detection that surfaces "this is starting to drift into out-of-scope territory; do we carve off?" before the drift distorts.

### Property 4 — Work-history multi-modal; no single artifact sovereign for any concern *(further-modified, absorbs anti-foreclosure)*

Decisions, visions, scope-events, methodology-events, monetization-evolution, practice-changes, release-cadence-state, feedback-loop-state — all stored portably across multiple coherent artifacts. Concerns can move between artifacts without information loss; the substrate avoids entrenching any single artifact as sovereign for any concern. This is the anti-foreclosure discipline operationalized at the storage layer (per harness-studio's `docs/deliberations/2026-04-24-bridge-harness-and-governance-seed.md` constraint list).

### Property 5 — Modular surfaces AND layered architecture stay optional *(merged from prior #5 + #11)*

Optionality at multiple scales, progressively activated per project classification. **Individual surfaces** (skills, hooks, workflow-templates, extensions, MCP tools) activate per project class + lifecycle stage. **Whole architectural layers** (operating-model, workflow-playbooks, expert-role-modules, execution-kernel, feedback-and-governance-loops, per harness-studio's working hypothesis) similarly activate per classification — solo-MCP-utility might use only execution-kernel + minimal feedback-loops; multi-game-platform-vision might use full stack. Both scales: add later without rewrite (anti-foreclosure across scales); remove later without breakage (downsizing-when-vision-narrows supported).

### Property 6 — Plural practices AND plural domains accommodated *(modified)*

The substrate accommodates **plural practices** (deep-deliberation + audit-arcs + ADR-grounded + handoff-bridged work as one practice; other practices viable too) AND **plural domains** (game / SaaS / social / scholarly tooling / philosophy/literature writing / research / etc.). Plurality across the six contexts (per framing-widening §2: A solo-research, B small-team, C enterprise, D platform, E transition-event, F transition-stance) is held as design-shape; domain-plurality adds an orthogonal axis.

### Property 7 — Spike-intensive (experimental-design-load-bearing) work first-class

Where precedent is thin and experimental design itself is load-bearing, the substrate's quality determines whether the work's outputs are trustworthy. arxiv-sanity-mcp is the diagnostic test case for this (per RELATIONSHIP-TO-PARENT.md §1). Generalizes: any work where designing the experiment correctly is itself the load-bearing question — not just spikes narrowly construed.

### Property 8 — Vision is first-class, regulative, and revisable; constraint-illumination + offshoot pattern supported *(added)*

The substrate carries vision as a canonical artifact (not mere project-summary or roadmap-target). Vision holds its **regulative-ideal** character: specifies something concrete enough to direct action *while always pointing beyond* whatever current materialization approaches it. The vision/materialization gap is held *open*, not closed (per Logan 2026-05-01: "A vision also signifies perhaps something concrete, but it also signifies something that exceeds whatever concrete materialization or implementation seems to approach it, like a mission, a core set of values, etc."). Vision is **revisable** between milestones / phases / events that warrant revisitation; vision-evolution is tracked as work-history (per Property 4).

The substrate supports vision-articulation, vision-tension-detection (where current work is straining against vision), vision-revision (when evidence licenses), vision-evolution-tracking (so future-Logan and future-agents can read which vision a past decision served).

The substrate also supports the **constraint-illumination** that vision provides: when new technological/material affordances arrive, vision is what makes those affordances load-bearing for the project rather than generic upgrades. The substrate helps read affordances *through* vision.

The vision-handling discipline includes the **offshoot pattern** as a supported response to scope-pressure: when out-of-scope vision starts distorting in-scope work, the substrate makes carving-off into a parked-context repo a routine workflow primitive. Two demonstrated instances (gsd-modifier→harness-studio 2026-04-24; prix-guesser→paddock 2026-04-25). The pattern is a candidate primitive worth codifying when methodology-codification threshold is hit (per DECISION-SPACE §3.9).

Cross-reference: Property 9 (project-class classification grounds vision-articulation; vision-evolution can trigger reclassification events).

### Property 9 — Project-class classification drives adaptive workflow-selection; meet-me-where-I-am AND push-me-beyond *(added)*

The substrate has an explicit **onboarding stage** that classifies the project across multiple axes:
- **project class** (research / game / SaaS / social / multi-game-platform / scholarly tooling / etc.)
- **team shape** (solo / small-team / transitioning)
- **lifecycle stage** (pre-MVP / MVP / beta / mature / late-stage)
- **material-constraint shape** (low-funding / medium-funding / high-funding-required)
- **ambition** (small-utility / monetizable-product / platform-vision / etc.)
- **expected maintenance / attention level**

Classification **drives workflow-selection** — different workflows, artifacts, review disciplines, release patterns activate per classification.

Two simultaneous postures: **meet-me-where-I-am** (configure appropriately for current state and ambition; don't impose maximum rigor on a small utility) AND **push-me-beyond** (when appropriate, surface higher visions, suggest more ambitious scope, prompt for what could be next; the master consultant doesn't just settle for the operator's stated state). The two postures are in tension; the substrate manages the tension contextually.

Classification is itself **revisable** — projects shift class (paddock-prix-guesser pivot was a reclassification event). The substrate supports re-classification + workflow-reselection as the project evolves.

Cross-reference: Property 8 (vision-articulation depends partly on knowing the class).

### Property 10 — Materialization-aware: monetization + deployability + others-can-use integrated as planning concerns *(added)*

Per-product-class × per-maturity-stage **monetization strategies** live as workflow primitives in the substrate's planning layer. Donations-with-transparency, beta-phase-small-donations, paid content packs, paid LAN versions, subscription, freemium, tip-jars, and other risk-free monetization shapes get integrated into planning from the start, not retrofitted late. Strategy depends on product class + expected maintenance/attention + future vision; strategies *evolve* as the product matures (and that evolution is tracked per Property 4).

The same integration applies to **deployability** and **others-can-use**: the substrate helps turn projects valuable to one operator into projects valuable + deployable + accessible to others. Distribution shape, packaging shape, onboarding-for-other-users shape, documentation shape, support shape — all in scope as workflow primitives, not last-phase concerns. Goal: turn-things-valuable-to-me into things-valuable-deployable-usable-to-others, generating money to offset opportunity cost in shapes appropriate to the product.

### Property 11 — Vendor-portable across model families and runtime environments *(added)*

The substrate works across model families (Anthropic / OpenAI / etc.) and runtime environments (Claude Code / Codex / etc.). Workflows, artifacts, and disciplines aren't tied to one vendor.

Load-bearing for: M1 paired-review property (cross-vendor + same-vendor pairing catches different categories of failure; vendor-plurality is required); MCP server surface (vendor-portability protocol); cross-vendor audit discipline (the audit-arcs in arxiv-sanity-mcp depend on this); harness-studio's stated portability across Codex and Claude.

Without this property, the substrate's design might drift toward single-vendor optimization (vendor-specific features that work great but break cross-vendor). With this property explicit, design choices preserve cross-vendor workability.

### Property 12 — Cross-project / portfolio support *(added)*

The substrate supports workflows across multiple projects in a portfolio. Artifacts, decisions, vision-evolution can be shared, referenced, or migrated across projects without losing context.

Demonstrated need:
- The offshoot pattern (Property 8) is itself a cross-project workflow.
- The pressure-respecting relationship between gsd-2-uplift and harness-studio is cross-project (one project respects another's vision-pressure without committing to convergence).
- Logan's project portfolio (arxiv-sanity-mcp, gsd-2-explore, harness-studio, paddock, prix-guesser, scholardoc/scholargt, AI-writing-philosophy, VIGIL, Z-Library MCP, etc.) has cross-project state-management needs.
- harness-studio's `docs/audits/project-portfolio-audit-seed.md` explicitly raised portfolio-perspective as substrate concern.

Distinct from: Property 6 (plural practices/domains — the substrate accommodating different shapes); Property 9 (classifying within a project); Property 8 (offshoot pattern is one cross-project workflow but portfolio-support is broader).

## §4. Scope-discipline

### §4.1 Burden of proof rests on exclusion

**Default: candidate-in-scope** unless we have demonstrated grounds for exclusion. The 12 properties of §3 are *all* candidate-in-scope for gsd-2-uplift at varying depths.

**Exclusion grounds** (require demonstration, not preemption):
- **Architectural blocker** — gsd-2's architecture genuinely cannot accommodate the intervention (rare; gsd-2 is mostly extension-friendly)
- **Identity-distortion shown concretely** — the intervention would distort gsd-2's identity in a sweeping way (see §4.3)
- **harness-studio-pressure foreclosure-risk with named risk** — the intervention would foreclose harness-studio's optionality in a specific, articulable way

Logan-disposition is appropriate when scope-exclusion *grounds* are unclear; not as audit-of-last-resort for substrate-design soundness (per 2026-04-30 §2.7).

### §4.2 Four-category scope-confidence model

Scope at any given moment is gradient-shaped, not binary. Items sit at:

- **C1 — Confirmed in-scope.** Patches we can plausibly land based on current evidence (small set; expands with Phase D mapping evidence).
- **C2 — Plausibly in-scope, evidence-needed.** Patches that *might* be feasible but require Phase D mapping evidence to confirm. **Most items at this stage sit here.**
- **C3 — Aspirationally in-scope, requires deeper exploration.** Patches that would address vision-properties more comprehensively but might cross identity-preservation lines or face accommodation-resistance from gsd-2. Notable set.
- **C4 — Out-of-scope by pressure-discipline.** **Narrow set.** Mostly applies to *design-disciplines* (don't entrench gsd-2 as sovereign; preserve portability) rather than *feature-categories*. Most actual feature-additions don't run into C4.

**Shift dynamics:**
- **C1 ↔ C2 ↔ C3** shift based on Phase D mapping evidence (and execution evidence in later phases). This is what mapping-shape Phase D is for.
- **C3 ↔ C4** shifts only via vision-frame revision (which happens via the offshoot pattern or substantive vision-deliberation, not via Phase D evidence).

### §4.3 Identity-distortion is genuinely narrow

**What gsd-2's identity consists of** (per cross-vendor codebase-understanding-audit's META-SYNTHESIS):
- Standalone agent application/runtime
- Vendored Pi-derived packages with headless/RPC/MCP/state-machinery surfaces
- Milestone/phase/task ontology
- Opinionated artifact discipline (PROJECT.md, ROADMAP.md, STATE.md, REQUIREMENTS.md, etc.)
- Skills system, hooks, workflow templates (markdown-phase + yaml-step engines)
- Extension manifest for ecosystem extensions
- MCP server surface
- Per-unit-type allowlists, decision-DB, journal/activity tracking, knowledge graph

**What would genuinely distort identity:**
- Replacing the milestone/phase/task ontology with a different ontology
- Removing the artifact-discipline (e.g., switching to database-UI persistence)
- Replacing the standalone-agent-runtime model
- Forcing a single workflow shape (contradicting gsd-2's extension/customization-friendly design)

**What does NOT distort identity** (despite prior framings implying it might):
- Adding a vision/mission mechanism that guides milestones (consistent with existing artifact-discipline)
- Extending the decision-DB substrate to recognize multi-modal trail (consistent with existing graph model)
- Adding workflow-lane primitives (consistent with extension-manifest pattern)
- Adding monetization-strategy artifacts (consistent with PROJECT.md / ROADMAP.md pattern)
- Most other feature-additions

The "identity-preservation" boundary applies to *sweeping ontological replacements*, not most feature-additions. Treat it as a narrow constraint, not a generic guard.

## §5. Phase D mapping purpose under this framing

Mapping-shape Phase D under (V′.a) generates evidence that **reclassifies items across C1-C2-C3** (per §4.2). It does NOT relocate items out of C4 (those stay anchored by harness-studio pressure, requiring vision-frame revision rather than mapping evidence to shift).

**Phase D output:** depth-classification per intervention candidate. For each of the 12 substrate-vision properties, Phase D mapping should generate evidence at multiple depths:
- **Shallow:** the safest patch (small extension, light hook, etc.) — typically C1-confirmable
- **Mid-depth:** more substantive intervention (decision-DB extension; new unit-types; workflow-template additions) — typically C2-pending-evidence
- **Deep:** structural addition (vision-aware lifecycle; classification-driven workflow-selection; full progressive activation) — typically C3-aspirational

**Phase E** stability-tests mapping coherence under fresh-context re-read + cross-vendor audit.

**Phase F** readiness-gate: does the proposed uplift-package design honor the four-category model? Does it land C1 contributions? Defer C2 with evidence-trigger? Commit/defer C3 with identity-risk Logan-disposition? Respect C4 absolutely?

## §6. Test-case anchors and project-portfolio context

**Current anchor for gsd-2-uplift bridge harness work:** arxiv-sanity-mcp (low-material-constraint research utility; deep-deliberation + audit-arcs practice; v0.1 shipped + v0.2 active).

**Next-most-likely anchor for post-extraction work:** prix-guesser (`loganrooks/prix-guesser` — active F1 game prototype; medium-material-constraint; MVP-being-built; mobile-first; viral-monetizable design).

**Deferred-noted anchors** (relevant to harness-studio's vision-horizon test-case-set; not active for gsd-2-uplift's current bridge-harness work):

| Project | Material-constraint shape | Lifecycle stage | Domain |
|---|---|---|---|
| paddock-vision (`~/workspace/projects/paddock/`) | high (platform requires sustained material support to materialize at vision-scale) | parked-canon (per `paddock/PARKED.md` 2026-04-25) | multi-game F1/motorsport platform |
| scholardoc / scholargt | medium-high (research platform; ongoing dev + likely material support) | hit-roadblocks-want-to-resume; multiple slightly-different versions | research / scholarly / humanities tooling (NotebookLM-like for philosophy/literature; PDF processing for complex works with explicit/implicit references) |
| AI-writing-philosophy | low (small bounded project) | not-yet-active | AI-generated-prose-quality discipline (teaching AIs to write philosophy/literature without AI-generated tics) |
| Z-Library MCP | low (MCP utility; small-donations support reference) | shipped/maintained | scholarly access utility |
| VIGIL | medium (Apollo/Tailscale app; ongoing dev) | per `harness-studio/docs/handoff/current.md` | personal-productivity + RL ADHD-coach |

The test-case anchors collectively span:
- **Resource-shape:** low → medium → high
- **Lifecycle stage:** shipped/maintained → MVP-active → prototype-stalled-want-to-resume → parked-canon → vision-only
- **Domain:** research utility, scholarly platform, AI-writing-discipline, F1 game, F1 platform, productivity/coaching

This is the **vision-horizon** test-case-set for harness-studio's eventual operating model. It is **NOT** the current test-case-set for gsd-2-uplift's bridge harness work — that stays at arxiv-sanity-mcp per (V′.a) execution discipline + extraction-priority signal.

## §7. Meta-disciplines surfaced through the conversation that produced this artifact

### §7.1 Closure-pressure-into-elaboration pattern recurred again

The pattern surfaced in 2026-04-30 §5.4 — agent commits to a frame, builds elaborate within-frame work, and only on Logan's prompting notices the frame was wrong — recurred multiple times during the 2026-05-01 turn-cluster that produced this artifact. Even at /effort max, even with explicit pattern-recognition active, the pattern re-fired. Each instance broke only on Logan-correction.

**Substrate-shape evidence:** the pattern is sufficiently load-bearing that effort-level alone doesn't break it; structured external pressure (Logan-correction + defense-against-critics framing) does. Confirms 2026-04-30 §5.4 finding under further evidence. Property 3 (frame-errors and scope-errors surface early) is the property the substrate would need to operationalize to break this pattern structurally rather than via Logan-correction.

### §7.2 Burden-of-proof-on-exclusion discipline (Logan-corrected)

When evaluating scope, **default candidate-in-scope** unless demonstrated grounds for exclusion exist. Initial framing tendency (preemptive narrowing) is a closure-pressure variant — committing to "this is out-of-scope" without demonstrating the exclusion-grounds. Corrected discipline: assume in-scope; require demonstrated grounds before excluding.

This connects to the vision-as-regulative-ideal framing (Property 8): vision-pressure should keep work pushing limits in reasonable ways. Treating materialization-feasibility as a *ceiling* (preemptively narrowing) is surrendering to materialization prematurely. The work happens in the tension between vision-pressure and materialization-pushback, not in pre-emptive surrender to materialization.

### §7.3 Identity-distortion as narrow constraint

The "identity-preservation" boundary I had been treating as broadly load-bearing turns out to be narrow in practice (§4.3). Most feature-additions don't run into it. Treating it as broad was another closure-pressure-shaped move (using a generic guard to preemptively narrow without demonstrating applicability per case).

### §7.4 Logan-disposition discipline scope (per 2026-04-30 §2.7)

Logan-disposition is for **user-intent capture** + **framing-pressure auditing where Logan has standing as user**. NOT audit-of-last-resort for substrate-design soundness. Agent-side reasoning must produce strong recommendations under the agent's own grounds; Logan can override but the audit-load stays agent-side.

Codification candidate: Logan-disposition discipline scope clarification belongs in `.planning/spikes/METHODOLOGY.md` or `AGENTS.md` per existing codification-threshold pattern.

### §7.5 Offshoot pattern as demonstrated discipline

Two demonstrated instances within 48 hours (gsd-modifier → harness-studio 2026-04-24; prix-guesser → paddock 2026-04-25). Pattern shape: when scope-pressure hits — when out-of-scope vision starts distorting in-scope work — carve the vision off into a parked-context repo. The offshoot is reference / vision / lab, not active execution. The working repo cites the offshoot for vision-context but doesn't execute against it.

Logan applied the pattern in real-time during the 2026-05-01 turn-cluster (extraction-priority signaling on (V′.a) execution: don't expand scope to absorb vision-additions; record-for-later instead). The pattern is *itself* a candidate workflow primitive for harness-studio's eventual operating model (Property 8 captures this).

## §8. Deferred questions

- **(a)** Could uplifted gsd-2 eventually be utilized *by* harness-studio's operating model (P1/P2/P3 paths from prior turn)? Separate, deferred question.
- **(b)** How does monetization-as-workflow-primitive get implemented? Vision-territory; harness-studio's eventual operating model layer.
- **(c)** Project-class classification flow operationalization. Vision-territory; harness-studio.
- **(d)** Cross-project / portfolio workflows (Property 12) operationalization depth-spectrum. Phase D mapping candidate.
- **(e)** Codification of Logan-disposition discipline scope clarification (per 2026-04-30 §2.7). Threshold-pending.
- **(f)** Codification of offshoot pattern as workflow primitive. Threshold-pending (two instances; needs three per existing pattern).
- **(g)** The "harness factory" eventual capability — meta-meta-level beyond harness-studio. Currently gestural; not articulated enough to be a substrate-property.

## §9. Cross-references

**Originating conversation:** 2026-05-01 turn-cluster (post-(V′.a) trajectory-replan; pre-(V′.a) Step 2 trajectory-plan revision authoring).

**Sibling standing-context:**
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` — test-case-vs-substrate framing (arxiv-sanity-mcp ↔ gsd-2-uplift's substrate-shape diagnostic role).

**gsd-2-uplift initiative artifacts:**
- `~/workspace/projects/gsd-2-uplift/.planning/INITIATIVE.md` — forward-staging; goal articulation; open framing questions; first-wave plan.
- `~/workspace/projects/gsd-2-uplift/.planning/DECISION-SPACE.md` — load-bearing decision reference.
- `~/workspace/projects/gsd-2-uplift/.planning/exploration/SYNTHESIS-COMPARISON.md` — paired-synthesis comparison; §7 audit addendum.
- `~/workspace/projects/gsd-2-uplift/.planning/trajectory/cheerful-forging-galaxy.md` — trajectory plan ((V′.a) Step 2 revision pending).
- `~/workspace/projects/gsd-2-uplift/.planning/wave-2/decision-trace/EXECUTION-LOG.md` — Phase D interim evidence corpus.

**Deliberation logs:**
- `.planning/deliberations/2026-04-28-framing-widening.md` — R1-R5 + six-context plurality + project-anchoring.
- `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` — methodology-mismatch finding + (V′.a) disposition.

**Audit folders:**
- `~/workspace/projects/gsd-2-uplift/.planning/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/` — premise-bleed audit-arc.
- `~/workspace/projects/gsd-2-uplift/.planning/audits/2026-04-29-trajectory-plan-audit/` — trajectory plan-self-audit.
- `~/workspace/projects/gsd-2-uplift/.planning/audits/2026-04-30-phase-d-entry-audit/` — Phase D entry audit (paired).

**External — harness-studio:**
- `~/workspace/projects/harness-studio/README.md` — purpose statement.
- `~/workspace/projects/harness-studio/docs/vision/problem-statement.md` — master-consultant vision.
- `~/workspace/projects/harness-studio/docs/handoff/current.md` — current state + layered architecture hypothesis + project-portfolio scope.
- `~/workspace/projects/harness-studio/docs/deliberations/2026-04-24-initial-harness-question.md` — initial framing.
- `~/workspace/projects/harness-studio/docs/deliberations/2026-04-24-bridge-harness-and-governance-seed.md` — bridge-harness pattern (now updated per pressure-not-destination clarification).
- `~/workspace/projects/harness-studio/docs/deliberations/2026-05-01-gsd-2-substrate-transfer-and-pressure-clarification.md` — substrate-transfer + pressure-clarification update (sibling to this artifact).

**External — paddock:**
- `~/workspace/projects/paddock/PARKED.md` — paddock parked-canon status (2026-04-25).
- `~/workspace/projects/paddock/discovery/01-vision.md` — F1-platform vision (parked).

**Methodology grounding:**
- `.planning/spikes/METHODOLOGY.md` — six interpretive lenses + paired-review practice disciplines (M1).
- `.planning/foundation-audit/METHODOLOGY.md` — decision-review epistemic discipline.
- `.planning/LONG-ARC.md` — anti-patterns + protected seams.

---

*Single-author + in-session-collaboration fallibility caveat. This artifact records substrate-vision-articulation work done 2026-05-01 in collaboration with Logan; subject to closure-pressure-pattern recurrence (per §7.1) and framing-inheritance per D5a. Future Phase E + Phase H audits + plan-self-audit per (V′.a) Step 3 provide structural mitigation. If any property feels mis-articulated in Logan's read, re-deliberation supersedes.*
