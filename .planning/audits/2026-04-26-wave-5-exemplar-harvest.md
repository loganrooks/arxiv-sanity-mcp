---
type: governance-exemplar-harvest
date: 2026-04-26
wave: 5
status: dispositioned 2026-04-26 — see §10 for the disposition record (Logan accepted dispositions as Claude recommended; full reasoning, assumptions, citation honesty, and "where my reasoning may be wrong" notes preserved per Wave 4 §2.5 pattern)
predecessor_artifacts:
  - .planning/audits/2026-04-26-governance-audit-synthesis.md (revised at 80cda50)
  - .planning/handoffs/2026-04-26-post-wave-4-handoff.md
inputs_provided_by_logan_2026-04-26:
  - "Architecting Autonomous Efficacy" — research doc on CLAUDE.md/AGENTS.md best practices
  - Karpathy-inspired terse CLAUDE.md exemplar (behavioral, 4-section)
  - gsd-modifier AGENTS.md exemplar (auditability/reviewability-heavy)
  - Logan-raised question: how to integrate LONG-ARC.md / VISION.md protocols into runtime governance
  - Gemini deep-research doc "Architecting a Mid-Horizon Automated Patcher" at .planning/research/gemini-deep-research/automating-long-term-planning-with-gsd-2.md (provided after harvest §1-§9 was drafted; framing-misaligned per Logan's read but gsd-2 mechanism descriptions verified by gsd-2 README)
  - gsd-2 README (verifies Pi SDK, RTK, worktree isolation, AGENTS.md auto-load, .gsd/ artifact set)
purpose: |
  Harvest distinguishing patterns from three exemplars; map them onto the
  arxiv-sanity-mcp governance set; propose dispositions for G-D1..G-D4 plus
  Logan's new LONG-ARC/VISION-integration question. Output is intended as
  input to a governance-synthesis revision (Wave 5 commit phase), not as
  the commits themselves. Single-author; subject to the same fallibility
  caveat as the prior synthesis (G-S synthesis §2.5 footer).
calibration_note: |
  The "Architecting Autonomous Efficacy" research doc mixes solid principles
  with quantified specifics that read as confident framing rather than
  empirically-grounded measurement (e.g., "exactly 25%/20%/15% PluginEval
  weights," "approximately 50,000 tokens before quality drop," "93%
  permission-prompt approval rate"). I treat the principles as directional
  and useful; I do not adopt the specific numbers as binding without
  independent verification. The Karpathy-style and gsd-modifier exemplars
  have observable provenance and are easier to ground.

  Calibration note added 2026-04-26 (post-disposition): I made two specific
  errors during deliberation that are recorded explicitly in §10 so a future
  reader can audit my judgment. (i) I called arXiv IDs 2604.03447 and
  2602.07609 "future-dated" when today is 2026-04-26 (April 26, 2026) and
  YYMM.NNNNN format makes 2604.xxxxx current-month — Logan caught this. The
  papers themselves remain unverified by me but the future-dating argument
  was wrong. (ii) I called RTK and Pi SDK "invented/confabulated" when both
  are real per the gsd-2 README — RTK at github.com/rtk-ai/rtk and Pi SDK
  at github.com/badlogic/pi-mono. The Gemini doc's gsd-2 mechanism
  descriptions are largely accurate; its framing of the question is
  misaligned (it answered "how to architect a code-patcher built on gsd-2"
  rather than "how to extend gsd-2 with VISION/LONG-ARC support").
---

# Wave 5 Exemplar Harvest — CLAUDE.md / AGENTS.md governance redesign

## 0. Document scope and what this is not

This document is the harvest analysis input to a Wave 5 governance-synthesis revision. It does **not** itself constitute a synthesis revision, and its proposals are not committed until Logan dispositions them in the same shape as the Wave 4 G-B-tier dispositions (synthesis §2.5).

**Disposition status (added 2026-04-26):** Logan dispositioned all ten items as recommended. The full disposition record — including the up-front shared assumptions Claude carried, citation-honesty observations per item, the recommendation-churn observation (Claude moved on the paired-audit recommendation across multiple turns), and the cross-cutting meta-concerns — is recorded at §10. §11 contains the candidate-uplift-primitives soft note that §10 dispositioned. Inline `**Disposition (2026-04-26):**` markers appear at the end of each `§4.x` and at §5.5; they point forward to §10 for full reasoning so §4 and §5 preserve the original proposal-stage content intact.

What this document does:

- Catalogues the three exemplars Logan provided.
- Extracts distinguishing patterns from each, with explicit calibration where claims look confident-but-unsubstantiated.
- Maps patterns onto the current `CLAUDE.md` / `AGENTS.md` state and the deferred-pending-exemplar items (G-D1, G-D2, G-D3, G-D4).
- Addresses Logan's new question: how do `LONG-ARC.md` and `VISION.md` become runtime guardrails for agents working in the repo?
- Proposes dispositions in the same `shape (a) / (b) / (c)` form as prior synthesis revisions, with explicit "where my reasoning may be wrong" notes.

What this document does **not** do:

- Rewrite `CLAUDE.md` or `AGENTS.md`. Those edits land at Wave 5 commit phase, after Logan's dispositions.
- Override Wave 4's already-committed G-A-tier or G-B-tier decisions.
- Re-litigate Wave 1 / Wave 3 plan-revision dispositions.
- Treat the research doc's prescriptions as binding. Some are useful; some are over-prescriptive for a single-developer project; some have hallmarks of AI-confabulated specifics.

## 1. Exemplars catalogued

### 1.1 "Architecting Autonomous Efficacy" (research doc)

**Posture:** Industry-survey style; heavy on prescriptions; assumes enterprise-scale multi-agent swarms.

**Distinguishing claims worth harvesting (treated as directional):**

- **Context rot is real and architecturally addressable.** Per-session scope to atomic-feature-or-bug, not long-running monolithic conversations. Re-anchor via persistent files at session start.
- **Token budgeting by layer.** Global-constitution / tenant-policy / user-memory / retrieved-artifacts / session-scratch — each with target budgets. (Specific token numbers offered are illustrative; the layered-discipline principle is what carries.)
- **Hierarchical scoping with deterministic priority.** Managed > CLI > Project > User > Plugin. Plugin-scope is permission-restricted to mitigate supply-chain risk.
- **`@include` directive for modular policy with anti-cyclic caching.** Prevents monolithic-file bloat; preserves composability.
- **Reversibility-weighted risk assessment.** Bias toward inherently reversible tools; quarantine irreversible operations behind explicit approval; do not rely on alert-fatigued human approval prompts as the sole safety surface.
- **Absolute literalism for Opus 4.7.** Replace negative ("don't do X") with positive declarative framing ("do Y in the following circumstances"). Front-load file paths. State acceptance criteria explicitly — do not rely on the model inferring that "implement X" means "with tests."
- **Effort-tier discipline.** Reserve `xhigh` for architectural reasoning and final verification; standard execution at `high`; cheap operations at `medium`.
- **Anti-patterns: `OVER_CONSTRAINED`, `BLOATED_SKILL`, `MISSING_TRIGGER`, `DEAD_CROSS_REF`.** OVER_CONSTRAINED specifically: more than ~15 instances of MUST/ALWAYS/NEVER in a single file paralyzes the model. (Specific threshold offered as illustrative; the underlying principle that absolutes-without-judgment-room degrade reasoning is plausible and supported by Anthropic's own prompting guidance against "negative constraint stacking.")

**Distinguishing claims to discount or treat with caution:**

- The named "PluginEval" framework with precise scoring weights — I cannot verify this exists as described.
- Specific quantified thresholds ("50,000 tokens before quality drop," "93% permission approval rate," "1.0 to 1.35x more tokens after tokenizer change"). These read as confident framing rather than measurement. Treat as illustrative.
- The "Tier 1/2/3/4 model routing" prescription is reasonable but the specific tier assignments offered are taste, not method.

**Net contribution:** Reinforces principles already present in the project's own `LONG-ARC.md` and `METHODOLOGY.md` (silent-default avoidance, calibrated language as default register, paired review for framing claims). Adds the **positive-declarative-framing** discipline as a concrete operational lever for Opus 4.7 contexts that the current docs do not name.

### 1.2 Karpathy-inspired CLAUDE.md exemplar

**Posture:** Terse; behavioral; project-agnostic; ~50 lines.

**Distinguishing patterns:**

- **Tradeoff acknowledged in the preamble.** "These guidelines bias toward caution over speed. For trivial tasks, use judgment." This is a calibrated meta-instruction that prevents the file from becoming an OVER_CONSTRAINED checklist.
- **Four behavioral sections, each with a one-sentence summary in bold.** Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution. The summary lines are the cognitive load; the bullets under each are elaboration.
- **Self-evaluation criteria at the foot.** "These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes." The file states how to know it is working — a feedback loop the agent can self-check against.
- **Negative framing used sparingly and pragmatically.** "Don't assume. Don't hide confusion. Surface tradeoffs." These are short and behavioral, not policy directives. The file does not stack absolutes.
- **No project-specific content.** The Karpathy file is a behavioral baseline; it expects to be merged with project-specific instructions, which it states explicitly.

**Net contribution:** Provides a tested template for the **behavioral discipline** layer of the governance set. The current `CLAUDE.md` does not have a clean behavioral-discipline layer separate from project-context; behavioral discipline is implicit in `AGENTS.md` but mixed with substantive policy. The Karpathy posture suggests cleaner separation: behavioral discipline in one place, behavioral discipline only, terse.

### 1.3 gsd-modifier AGENTS.md exemplar

**Posture:** Dense; project-specific; auditability-and-reviewability-heavy; ~150 lines across 11 sections.

**Distinguishing patterns:**

- **"Scope" section opens with explicit non-claims** ("treat this repo as the modifier project, not as a host product repo"; "do not import `prix-guesser` product-planning horizons as if they govern this repo"). The file actively guards against frame contamination from neighboring projects.
- **"Source Of Truth" section enumerates surfaces by category** (shipped/runtime, development-support, migration/provenance, carried origin audit). Each surface listed by exact path. An agent reading this knows exactly what counts as authoritative source vs derived artifact vs carried context.
- **"Live Control Surface" makes authority explicit and time-indexed.** "Do not treat generated runtime output or carried origin context as authority when it diverges from the live source and handoff surfaces." This is a precedence rule for resolving conflicts between artifacts.
- **"Working Rules" captures load-bearing project-specific patterns** (bootstrap and verification are load-bearing; portability via placeholders; install-profile-claim discipline). These are not generic best practices; they are this-project's known difficulty patterns.
- **"Workflow Rules" enforces propose-before-act for ambiguous/architectural changes** with an explicit checklist of what to state before approval ("the observed problem, the proposed change, why that change is appropriate, alternatives considered, the expected write set, the verification plan"). Also: "do not silently flatten" — and then enumerates the four flattenings to avoid (source vs materialized, observed vs inferred, planned vs improvised, accepted boundary vs ambient follow-up).
- **"Contract Propagation" treats local diffs as triggers for propagation analysis.** Names the producer/consumer/carrier/mirror/output chain explicitly. Lists the repo's contract-checking tools by command.
- **"Auditability And Review" section** — this is the section Logan called out as load-bearing. It demands "code, docs, plans, and rationale that can survive adversarial rereading without hidden chat context." Distinguishes "transparency" from "verbatim chain-of-thought dump." Lists explicit reviewable distinctions: observed vs inference, decision vs open question, source vs materialized verification, durable artifact vs disposable byproduct.
- **"Delegation And Review" requires explicit disposition** of delegated work as `accept`/`revise`/`park`/`reject`. Forbids performative delegation after the critical work is already done.
- **"Commit Hygiene" enforces Conventional Commits with scope** and lists separate-commit categories (shipped/runtime vs contract vs docs vs measurement) with explicit anti-bundling.
- **"Verification" section ends with a default verification stack** of exact commands. No room for the agent to invent its own verification.

**Net contribution:** Provides a tested template for the **substantive-policy-with-auditability** layer of the governance set. The current `AGENTS.md` has the CONTEXT.md epistemic discipline section (lines 110–137) that gestures in this direction, but does not enumerate distinctions, does not have a "do not silently flatten" formulation, does not enumerate protected seams, does not have a propose-before-act workflow rule, and does not have a default verification stack.

## 2. Patterns harvested by source — at-a-glance

| Pattern | Research doc | Karpathy | gsd-modifier | Action for Wave 5 |
|---|---|---|---|---|
| Calibrated tradeoff in preamble | — | yes | — | Adopt for behavioral layer |
| Token budgeting by layer | yes | — | implicit | Note as principle; do not commit to specific budgets |
| Positive-declarative framing | yes | yes | yes | Adopt; rewrite negatives where feasible |
| Source-of-truth enumeration by category | — | — | yes | Adopt for AGENTS.md |
| Live control-surface precedence rule | — | — | yes | Adopt for AGENTS.md |
| Propose-before-act for ambiguous changes | implicit | implicit | yes | Adopt for AGENTS.md |
| "Do not silently flatten" formulation | — | — | yes | Adopt for AGENTS.md |
| Reviewable distinctions explicit | — | — | yes | Adopt; project-specific tailoring |
| Delegation disposition (accept/revise/park/reject) | implicit | — | yes | Adopt; aligns with M1 paired-review discipline |
| Conventional Commits with scope | — | — | yes | Adopt as documentation; commit history already mostly conforms |
| Default verification stack | yes | yes | yes | Adopt; project has `pytest` + `ruff` + `pyright` baselines |
| Anti-pattern self-check | yes | — | — | Adopt — anti-patterns harvested from LONG-ARC + audit cycle |
| Effort-tier discipline | yes | — | — | Note; defer formal codification — current usage is ad hoc but working |
| `@include` directive | yes | — | — | Defer — current file count is small enough to not need modularization |

## 3. Mapping onto current `CLAUDE.md` and `AGENTS.md`

### 3.1 Current `CLAUDE.md` audit (project root)

The current file is ~80 lines and structured as: project identity (4 lines) → accepted ADRs (5 lines) → key architectural constraints (5 lines) → status markers (5 lines) → document structure (8 lines) → governance read-order map (8 lines) → roadmap phases (3 lines).

Strengths the exemplars validate:

- The governance read-order map (added in Wave 4 commit `c31e21a`) matches the gsd-modifier "Source Of Truth" enumeration spirit — different surfaces, same auditability function.
- The "Status Markers" section (Settled / Chosen for now / Hypothesis / Open) is the project's own contribution to the calibrated-language discipline; it has no analog in the exemplars but is consistent with their posture.
- The accepted-ADR list is short, named, and pointer-out — not redundant with the ADR text itself.

Weaknesses the exemplars surface:

- **No calibrated tradeoff in the preamble.** The file opens with "This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository." Compared to Karpathy's "These guidelines bias toward caution over speed. For trivial tasks, use judgment," the current opening reads as a label rather than a meta-instruction.
- **No behavioral-discipline content.** Behavioral discipline (assume vs ask, surgical changes, goal-driven verification) is entirely in `AGENTS.md` — but `AGENTS.md` is not auto-loaded into runtime context. Agents whose context only includes `CLAUDE.md` get no behavioral instruction at session start.
- **G-D4: "Stack trajectory: ... Not Stack D" is opaque without `docs/05` context.** Confirmed in §3.3 below.
- **Negative framing dominates "Key Architectural Constraints."** Three of four bullets are "Do not..." constructions. Per Opus 4.7 absolute-literalism guidance, positive declarative framing reads more reliably.

### 3.2 Current `AGENTS.md` audit (project root)

The current file is ~140 lines and structured as: mission → "do not do these things" (negative list) → default working posture → required habits (4 numbered) → default implementation bias → "before you make a major change" (6 questions) → definition of success → CONTEXT.md epistemic discipline (4 sub-sections).

Strengths the exemplars validate:

- The CONTEXT.md epistemic discipline section is already excellent and aligns with the gsd-modifier "Auditability And Review" intent — it enumerates distinctions (source-traceable vs artifact-reported vs derived vs interpretive) and prescribes labeling.
- Required Habit #1 (mark commitment level) is the calibrated-language discipline operationalized.
- Required Habit #2 (update the right document) is a precedence/routing rule similar to gsd-modifier's "Source Of Truth" pattern.

Weaknesses the exemplars surface:

- **G-D2: ADR-citation example misquotes ADR-0001.** Confirmed in §3.4 below.
- **No project-specific "Working Rules" section** capturing this project's known difficulty patterns. The LONG-ARC anti-patterns and the 005-008 spike-chain drift are project-specific load-bearing patterns; they live only in `LONG-ARC.md`, not in agent-facing posture instruction.
- **No propose-before-act workflow rule.** "Required habits" list says to mark commitment and update docs but does not say "for ambiguous/architectural/policy-bearing changes, propose before editing." The Wave 4 governance synthesis G-A3 fix (ADR-doctrine pass with verbatim re-checks) was needed precisely because this discipline is informal.
- **No "do not silently flatten" formulation.** The flattenings the project keeps falling into are different from gsd-modifier's, but the formulation is reusable.
- **No "Known difficulty patterns" / anti-pattern section.** This is G-D1 directly.
- **No default verification stack.** Project has `pytest`, `ruff`, `pyright` (and the test/tool counts that Wave 4's G-A2 commit pinned to ~493 tests / 13 tools). No file lists what the agent should run before claiming a task complete.
- **"Do not do these things" opens with seven negatives.** Per absolute-literalism guidance, positive reframing of at least the actionable items would help (the philosophical "do not assume tags are canonical" remains a useful negation; the operational ones can be reframed).

### 3.3 G-D4 — Stack-trajectory line

`CLAUDE.md:24` reads: `**Stack trajectory:** Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). Not Stack D.`

`docs/05-architecture-hypotheses.md` defines:

- Stack A — metadata + lexical + graph
- Stack B — metadata + lexical + selective local semantic
- Stack C — metadata + lexical + external API enrichments
- Stack D — full local hybrid research platform (the maximalist option)

The recommendation in `docs/05:140` is: "The best opening move is probably **Stack A moving toward Stack B**, not Stack D."

The CLAUDE.md line paraphrases `docs/05:140` faithfully but elides the source. An agent without `docs/05` context reads "Not Stack D" as a flat foreclosure with no context. Synthesis SV C1 self-labels this as "trivial but real."

### 3.4 G-D2 — AGENTS.md ADR-citation example

`AGENTS.md:130` (the ADR-citation discipline example): `Example: "ADR-0001 states 'multiple retrieval/ranking strategies must coexist' -- this means..."`

`ADR-0001` decision body (line 22): `multiple retrieval and ranking strategies can coexist`

Two divergences:

1. **`must` → `can`.** The example inflates a permission/affordance ("can") into a directive ("must"). This is precisely the kind of paraphrase inflation the discipline-section-as-a-whole warns against.
2. **`retrieval and ranking` → `retrieval/ranking`.** Cosmetic; not a fidelity issue.

The first divergence is the load-bearing one. The example teaching the discipline of accurate ADR-citation contains the inflation pattern the discipline forbids.

## 4. Substantive recommendations for G-D1..G-D4

Each item is offered in `shape (a) / (b) / (c)` form, with a single recommended shape and a "where my reasoning may be wrong" note.

### 4.1 G-D1 — `AGENTS.md` "Known difficulty patterns" section

**Recommended shape (a):** Add a new section to `AGENTS.md` titled "Project-specific anti-patterns to detect" that harvests the LONG-ARC anti-patterns plus the closure-pressure-at-every-layer pattern from the audit cycle. Each pattern stated in the form `pattern → counter-posture` (positive declarative framing). Total length target: ~30 lines, ~7 patterns.

Patterns to include (drawn from `LONG-ARC.md:42-54`, the audit-cycle deliberations, and the 005-008 lesson):

- Tournament narrowing under "disciplined" framing → rank-and-deprioritize, not eliminate; multi-lens framing replaces winner-pick.
- Single-lens "interface" by accident → validate abstractions by shipping a second implementation, per ADR-0005.
- Silent defaults → name the reference frame explicitly; require challengers measured against multiple frames or task outcomes.
- ADR violation by gradual local-reasonable steps → run an ADR-against-current-work check at deliberation boundaries; ADRs are read at planning time, not just at writing time.
- Closure pressure at every layer → calibrated language as default register; flag confident remedies for paired review before adoption.
- Embedding-model choice as load-bearing decision → treat embedding-model selection as one lens-design decision among many; most leverage lives upstream (query interpretation, profile elicitation, presentation).
- Single-reader framing claims as authoritative → paired review for framing claims (cross-vendor + same-vendor); consult `METHODOLOGY.md`.

**Alternative shape (b):** Same content, but place it in `LONG-ARC.md` only and cite from `AGENTS.md`. Keeps `AGENTS.md` short; relies on agents reading `LONG-ARC.md` when relevant. Risk: the agent that needs the anti-pattern most is the one that has not read `LONG-ARC.md`.

**Alternative shape (c):** Place a short summary list (3 patterns max) in `AGENTS.md` and full enumeration in `LONG-ARC.md`. Compromise; the choice of which 3 is itself a contestable judgment.

**Recommendation: (a).** Doubling the surface count is acceptable cost; runtime context (what an agent actually sees) is the load-bearing surface.

**Where my reasoning may be wrong:** If this section grows past ~30 lines, it crosses into the BLOATED_SKILL anti-pattern territory and OVER_CONSTRAINED if too many absolutes accumulate. Need to write it tight.

**Disposition (2026-04-26):** shape (a) **with refinement** — verbatim cite-back to `LONG-ARC.md:46-54` per pattern, so duplication-drift between AGENTS.md and LONG-ARC.md is detectable on next-pass review. Full reasoning, assumptions, and "where my reasoning may be wrong" recorded at §10.2.

### 4.2 G-D2 — `AGENTS.md` ADR-citation example fix

**Recommended shape (a):** Replace the example with a verbatim quote from ADR-0001's decision body, plus a brief note acknowledging the discipline applies to all ADR citations including this one's.

Proposed replacement text:

> Example (verbatim quote, with deliberate fidelity to the ADR text):
> ADR-0001 states "multiple retrieval and ranking strategies can coexist" — this is a capability commitment about the architecture (the design must support coexistence), not a directive that every project decision *must* engage multiple strategies. Compare to the inflated paraphrase "multiple retrieval/ranking strategies must coexist" — that paraphrase converts a permission into a directive and is therefore inaccurate, even though it sounds more authoritative.

This both fixes the misquote and uses the misquote-vs-correct-quote contrast as the teaching example. The discipline being taught now has a concrete instance of the failure mode it forbids.

**Alternative shape (b):** Just fix the quote (drop the inflation analysis). Cleaner; loses the teaching opportunity.

**Alternative shape (c):** Use a different ADR for the example (e.g., ADR-0003's "no redistribution of full text without rights verification"). Sidesteps the meta-issue but misses the chance to acknowledge the prior failure.

**Recommendation: (a).** The audit's symbolic concern (the document teaching accurate citation contains an inflation) deserves a meta-acknowledgment, not a silent fix.

**Where my reasoning may be wrong:** Shape (a) makes the example a paragraph rather than one line, which adds reading cost. If terseness matters more than meta-acknowledgment, (b) is fine. The shape choice is taste.

**Disposition (2026-04-26):** shape (a) — verbatim quote + misquote-vs-correct contrast as teaching example. Full reasoning at §10.3.

### 4.3 G-D3 — `CLAUDE.md` restructuring

**Recommended shape (a):** Targeted additions to current structure, not wholesale rewrite. Specifically:

1. **Replace the bare opening line** with a calibrated-tradeoff preamble (Karpathy-pattern):
   > This file is auto-loaded as runtime context for agents working in this repository. It defines project identity, accepted decisions, and routing pointers — not behavioral discipline (see `AGENTS.md`). The bias is toward stability of decisions already made and explicit pointers for decisions that need to be re-checked. For genuinely trivial tasks, use judgment.

2. **Add a short "Doctrine load-points" section** (4–6 lines) listing trigger conditions for reading `LONG-ARC.md` / `VISION.md` / specific ADRs. This is the LONG-ARC/VISION integration mechanism (see §5).

3. **Reframe "Key Architectural Constraints" negatives to positive declaratives where feasible.** "Do not prematurely commit to a retrieval family" stays as-is (the negation is the point). "Do not assume tags are canonical / dense retrieval is winner / paper chat is product" can be reframed as "Treat tags as one signal among several, not the canonical taste primitive; treat dense retrieval as one lens among several, not the default; the product is discovery and triage, not paper-chat" — same content, positive register.

4. **Fix G-D4** (Stack trajectory line) — see §4.4.

5. **Leave the rest as-is** (governance read-order map is good; status markers section is good; ADR list is good).

Total CLAUDE.md size target after edits: ~110 lines (from ~80). Net addition: ~30 lines, mostly the doctrine load-points section and the preamble.

**Alternative shape (b):** Karpathy-style minimalism — strip CLAUDE.md to ~30 lines (project identity + ADR list + read-order map only); push everything else to `AGENTS.md`. Cleaner runtime cost but moves the literalism-friendly framing further from agent context.

**Alternative shape (c):** Status quo + only G-D4 fix. Safest; lowest cost; foregoes the Karpathy-tradeoff-preamble and doctrine-load-points improvements.

**Recommendation: (a).** Targeted additions preserve the Wave 4 commits (G-A2, G-S1) that already shaped the file; adds the literalism-friendly preamble and the LONG-ARC/VISION integration without a wholesale rewrite that would itself be a closure-pressure move.

**Where my reasoning may be wrong:** ~110 lines is large for a runtime-loaded file. If empirical evidence emerges that token cost is a concrete problem, (b) becomes attractive. I do not currently have that evidence.

**Disposition (2026-04-26):** shape (a) **full split, lean keep nice-to-have** — add load-points section (mandatory if α adopted) + G-D4 fix (mandatory) + calibrated preamble + positive-declarative reframing of "Key Architectural Constraints" (nice-to-have, kept). Tension between "current Claude Code primary auto-load" and "post-migration gsd-2 fallback" resolved toward keep-nice-to-have because additions are durable Karpathy patterns and migration timing is "soon but tentative" not "imminent." Full reasoning + tension acknowledgment + recommendation-stability note at §10.4.

### 4.4 G-D4 — `CLAUDE.md` "Stack trajectory: Not Stack D" line

**Recommended shape (a):** Replace the bare "Not Stack D" suffix with an explicit pointer and a one-line gloss:

> **Stack trajectory:** Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). The maximalist Stack D (full local hybrid research platform — see `docs/05-architecture-hypotheses.md:118`) is foreclosed because it commits compute and complexity that v0.x has no evidence to justify; the trajectory remains open if v0.3+ evidence warrants reopening.

**Alternative shape (b):** Drop the "Not Stack D" line entirely. The positive trajectory is the actionable content; foreclosing-by-name without context is the silent-default pattern. Synthesis SV C1's secondary recommendation.

**Alternative shape (c):** Move the Stack-A-to-B trajectory line into the "Doctrine load-points" section as `Touching ranking/retrieval architecture → read docs/05`. Defers the gloss to the source doc.

**Recommendation: (a).** The Stack-A-to-B trajectory is a load-bearing project commitment that should stay surfaced in CLAUDE.md; the foreclosure is only meaningful with the gloss.

**Where my reasoning may be wrong:** SV C1 itself self-labels as "trivial but real." If the Wave 5 budget is tight, (b) is the cheap fix. (a) costs ~2 lines; the gain is a runtime-readable rationale.

**Disposition (2026-04-26):** shape (a) **with verification step** — re-check Stack-D foreclosure status against ADR-0005 before pinning the gloss, since ADR-0005 may have shifted v0.2's compute/complexity ambition in ways the gloss should reflect. Full reasoning at §10.5.

## 5. LONG-ARC.md / VISION.md integration — the new question Logan raised

The current state: `CLAUDE.md` lists ADRs and architectural constraints; `AGENTS.md` has the CONTEXT.md epistemic discipline; neither file has a *protocol* for when the agent must read `LONG-ARC.md` or `VISION.md` before acting. The 005-008 spike chain drift (the canonical example of doctrine-violation-by-locally-reasonable-steps) is what this integration is meant to prevent recurrence of.

I propose four integration shapes; they are not mutually exclusive. The harvest's recommendation is a combination — α + β + γ — with δ deferred unless evidence warrants.

### 5.1 Shape α — Doctrine load-points map (in `CLAUDE.md`)

A short section in `CLAUDE.md` that names trigger conditions and the document the agent must read before acting on that trigger.

Proposed content (~8 lines):

> **Doctrine load-points** (read the listed document before editing or proposing changes that match the trigger):
> - Touching ranking, retrieval, or lens-architecture code → `LONG-ARC.md` (anti-patterns), `docs/adrs/ADR-0001`, `docs/adrs/ADR-0005`.
> - Adding a new abstraction or signal type → `LONG-ARC.md` (protected seams), `VISION.md` (anti-vision section).
> - Touching MCP tool, resource, or prompt surfaces → `docs/adrs/ADR-0004`, `LONG-ARC.md` (MCP-native operations).
> - Proposing rights-affecting changes (license, redistribution, content storage) → `docs/adrs/ADR-0003`.
> - Proposing changes to enrichment cost or scheduling → `docs/adrs/ADR-0002`.
> - Proposing changes to the spike program structure or methodology → `.planning/spikes/METHODOLOGY.md`, `LONG-ARC.md` (doctrine-interaction-with-spike-program).

This is the file-routing analogue of the gsd-modifier "Source Of Truth" enumeration — it tells the agent where authority lives for which kinds of decision.

### 5.2 Shape β — Anti-pattern self-check (in `AGENTS.md`)

The "Project-specific anti-patterns to detect" section proposed in §4.1 (G-D1) is the operational form of this. The agent self-checks against the LONG-ARC anti-patterns before declaring substantive work complete. Format: `pattern → counter-posture`, positive declarative.

### 5.3 Shape γ — Deliberation-boundary protocol (in `AGENTS.md`)

A new "Deliberation boundaries" section in `AGENTS.md` listing change-types that should pause-and-surface rather than proceed-and-commit. Inspired by gsd-modifier's "for ambiguous, architectural, policy-bearing, or contract-carrying changes, do not edit files or commit until the proposed change has been explained and the user gives explicit approval."

Proposed boundaries to enumerate:

- Reshaping a spike, milestone, or phase plan structurally (not minor edits).
- Modifying any accepted ADR's text, status, or scope.
- Introducing or removing a top-level abstraction (lens type, signal type, workflow primitive).
- Changing the MCP tool/resource/prompt surface in ways visible to existing callers.
- Editing `LONG-ARC.md`, `VISION.md`, or the project root `CLAUDE.md` / `AGENTS.md`.
- Closing an Open Question without a new ADR or explicit Logan confirmation.

For each: state the observed problem, the proposed change, why now, alternatives considered, expected write set, verification plan — gsd-modifier's checklist.

### 5.4 Shape δ — Protected-seams change-control list (deferred)

A list of specific code surfaces that require explicit Logan approval to modify (e.g., the `Lens` interface once shipped, the `signal_type` registry, ADR text). Useful but premature — the surfaces it would protect are mostly v0.2+ work that has not yet been authored. Re-evaluate after Phase 12 plan-1 lands.

### 5.5 Recommended combination

**Adopt α + β + γ in Wave 5; defer δ to v0.2 implementation phase.**

The combination addresses the three risks the audit cycle identified:

- **Routing risk** (the agent does not know which doctrine governs the change it is making) → α resolves.
- **Drift risk** (the agent does locally-reasonable work that violates LONG-ARC anti-patterns) → β resolves.
- **Surfacing risk** (the agent does not pause-and-surface at moments that warrant deliberation) → γ resolves.

**Where my reasoning may be wrong:**

- α + β + γ together add ~50 lines across two files. If aggregated absolute-count crosses ~15, the OVER_CONSTRAINED anti-pattern starts to bite. Drafting must be careful — favor "do Y in circumstance Z" rather than "always Y" / "never X."
- γ overlaps with the project's existing "for ambiguous changes, propose first" implicit norm. Making it explicit is the value; over-listing the boundaries is the risk.
- The combination presumes the agent reads both files. If `AGENTS.md` is not loaded into runtime context (only `CLAUDE.md` is auto-loaded), β and γ benefit only the agent that explicitly reads `AGENTS.md`. A pointer from `CLAUDE.md` to `AGENTS.md` for behavioral discipline is part of the proposed §4.3 shape (a) preamble.

**Disposition (2026-04-26):** **α + β + γ + δ-as-pointer-note.** δ remains deferred for placeholder content (no fabrication of v0.2-surfaces-not-yet-authored) but a 2-sentence forward-looking pointer-note is added to the AGENTS.md γ section signaling intent: "Once v0.2 introduces the Lens interface, signal_type registry, and MCP-tool lens-awareness surfaces, those should be added to a protected-seams change-control list per the discipline above. The list does not yet exist because the surfaces do not yet exist." Full reasoning at §10.6.

## 6. Where these recommendations could collectively be wrong

Per the M1 discipline (paired review for framing claims) and the explicit acknowledgment in the prior governance synthesis (§2.5 footer) that single-author synthesis is fallible, this section names the cross-cutting risks to the harvest as a whole.

1. **The exemplars carry their own contexts that may not transfer.** The Karpathy posture is project-agnostic and behavioral; harvesting it for a behavioral preamble is direct. The gsd-modifier posture is built around a specific repo's contract-carrying surfaces; harvesting "auditability and review" is direct, but harvesting "Contract Propagation" specifics (named verification scripts) does not transfer — arxiv-sanity-mcp does not have an analogous contract-checker library. I have only harvested the transferable patterns; the non-transferable specifics are noted but not adopted.

2. **The research doc's prescriptions may anchor more than they should.** I have explicitly flagged the quantified specifics as illustrative-not-binding, but the framing categories the doc uses (token-budgeting layers, effort tiers, anti-pattern names like OVER_CONSTRAINED) may still bias the harvest. A skeptical re-reader should ask: does the OVER_CONSTRAINED concern actually apply at the proposed surface count, or is the threshold imported from the doc without independent grounding?

3. **The LONG-ARC/VISION integration shapes (α/β/γ/δ) are my construction.** Logan asked the question; I produced four shapes; I recommend a combination. Logan's actual best answer might be a shape I did not name — e.g., a single-document consolidation, or a workflow-tool integration (the gsd-2 uplift initiative is explicitly the long-horizon home for some of this; pulling it forward into Wave 5 might be premature).

4. **The "fix it in CLAUDE.md vs AGENTS.md vs both" decisions are taste.** Each item could be argued differently. The chosen split (CLAUDE.md = identity + routing, AGENTS.md = behavioral + protocol) is consistent and defensible but not the only defensible split.

5. **Closure pressure recurs at the meta-layer.** Producing a tidy harvest with four shapes per item and a single recommended combination is itself the closure-pressure pattern the audit cycle keeps surfacing. I have tried to keep the alternatives genuinely live and the recommendations marked as recommendations, not commitments. If a recommended shape feels obviously right on first read, that is a signal to slow down, not a signal to commit.

## 7. Proposed Wave 5 commit sequence (post-disposition)

This is the dispositioned commit sequence. All ten items in §10 are accepted by Logan; the sequence reflects shape (a) for G-D1..G-D4, α + β + γ + δ-pointer-note for LONG-ARC/VISION integration, mirror-Wave-4 sequencing, Q1/Q4/Q16-separate, and cross-vendor-codex-paired-audit-on-§5+§11.

**Pre-Wave-5 step 1: governance synthesis pointer.** Add a short subsection to `.planning/audits/2026-04-26-governance-audit-synthesis.md` §4 (Deferred pending exemplar review) noting that G-D items have been dispositioned per this harvest's §10. Single commit. Mirrors the `80cda50` Wave 4 disposition-recording commit pattern.

**Pre-Wave-5 step 2: cross-vendor codex dispatch on §5 + §11.** ~30-min focused dispatch. Scope question: "do these α/β/γ patterns map onto gsd-2's existing artifact vocabulary (PROJECT.md / DECISIONS.md / KNOWLEDGE.md / RUNTIME.md / STATE.md / ROADMAP.md), or do they require new artifact classes that gsd-2 doesn't currently have?" Output: brief comparison artifact at `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`. If the cross-vendor read surfaces a fifth shape or vocabulary mismatch, integrate before the commits. If not, proceed with confidence.

**Pre-Wave-5 step 3: create Gemini reading-notes.** ~10-line artifact at `.planning/research/gemini-deep-research/READING-NOTES.md` flagging the gsd-2-mechanism-accuracy + framing-misalignment + LLM-eval-specifics-unverified facts about the Gemini doc. Prevents future sessions from picking up the doc cold.

**Wave 5 commit 1 (`docs(governance)`):** AGENTS.md substantive expansion — adds "Project-specific anti-patterns to detect" (G-D1 shape (a) with cite-back), fixes ADR-citation example (G-D2 shape (a) with misquote-vs-correct teaching), adds "Deliberation boundaries" section (γ) with δ-pointer-note, reframes "Do not do these things" to positive declarative where feasible. Target size after: ~250 lines (from ~140).

**Wave 5 commit 2 (`docs(governance)`):** CLAUDE.md targeted additions — adds calibrated-tradeoff preamble (Karpathy-pattern), "Doctrine load-points" section (α), reframes "Key Architectural Constraints" negatives to positive declaratives where feasible, fixes "Stack trajectory: Not Stack D" line (G-D4 shape (a)) after re-verifying foreclosure status against ADR-0005. G-D3 shape (a) overall. Target size after: ~110 lines (from ~80).

**Wave 5 commit 3 (`docs(governance)`):** STATE.md update — frontmatter currency; pending-todos collapse Wave 5 items; session-continuity points to next handoff if appropriate.

**Wave 5 commit 4 (`docs(research)` — separate scope):** Gemini doc reading-notes file at `.planning/research/gemini-deep-research/READING-NOTES.md`. Separate commit because it's a research-context artifact, not a governance-doc edit.

Four commits is the upper bound. Pre-Wave-5 cross-vendor dispatch may add a fifth (the comparison artifact) but only if it surfaces something requiring action.

**Verification before each commit:**

- AGENTS.md commit: re-read ADR-0001 to confirm the verbatim quote in the example (`docs/adrs/ADR-0001-exploration-first.md:22`). Re-read `LONG-ARC.md:42-54` to confirm anti-pattern fidelity. Re-read `.planning/spikes/METHODOLOGY.md:112` to confirm M1 description. Run `wc -l AGENTS.md` and confirm not bloated past ~250 lines.
- CLAUDE.md commit: re-read `docs/05-architecture-hypotheses.md:118-140` to confirm Stack-D gloss is faithful. Re-read ADR-0005 to confirm Stack-D foreclosure status hasn't shifted post-redirection. Run `wc -l CLAUDE.md` and confirm not bloated past ~120 lines.
- STATE.md commit: re-read prior STATE.md frontmatter to confirm currency-update pattern is consistent. Verify test count (~493) and tool count (13) hasn't shifted (unlikely; v0.2 implementation hasn't started).

**Execution discipline:** Per Wave 4 precedent and handoff §9 fresh-session discipline, Wave 5 commits should land in a fresh session — not this one — with a self-contained briefing referencing this harvest's §10 dispositions. The cross-vendor dispatch and Gemini reading-notes file can be produced in this session or the next, at Logan's discretion.

## 8. Open questions for Logan (post-disposition)

All ten substantive dispositions are accepted per §10. What remains are execution-step choices:

1. **When to run the cross-vendor codex dispatch** — now (this session, immediately) or after the synthesis pointer commit. **Default recommendation:** after the synthesis pointer commit, so the cross-vendor read sees the dispositioned harvest as ground truth. Logan's call.
2. **Whether to fold the Gemini reading-notes commit into Wave 5 commit sequence or treat as standalone.** **Default recommendation:** standalone (Wave 5 commit 4 above) since it's a research-context artifact. Defensible either way.
3. **Migration timing for G-D3 nice-to-have** — if gsd-2 migration is happening in days rather than weeks, drop the calibrated preamble and positive-declarative reframing. **Default recommendation:** keep nice-to-have unless migration is imminent in days.
4. **Q1/Q4/Q16 validation timing** — orthogonal to Wave 5; can happen in parallel. **Status:** unchanged from §10.8.

## 9. Cross-references

- Governance synthesis (with G-D items deferred-pending-exemplar): `.planning/audits/2026-04-26-governance-audit-synthesis.md`
- Post-Wave-4 handoff (Wave 5 expectations): `.planning/handoffs/2026-04-26-post-wave-4-handoff.md` (§7 Wave 5 sequencing, §13 path-a)
- LONG-ARC anti-patterns (source for §4.1 + §5.2): `.planning/LONG-ARC.md:42-54`
- VISION anti-vision (source for §5.1 add-new-abstraction load-point): `.planning/VISION.md:76-84`
- METHODOLOGY (source for paired-review and calibrated-language disciplines): `.planning/spikes/METHODOLOGY.md`
- Stack A/B/C/D definitions (source for §4.4): `docs/05-architecture-hypotheses.md:59-140`
- ADR-0001 verbatim text (source for §4.2): `docs/adrs/ADR-0001-exploration-first.md:22`
- ADR-0005 multi-lens substrate (source for §4.1 anti-pattern fidelity + §4.4 Stack-D verification): `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
- Karpathy-style and gsd-modifier exemplars: provided by Logan in conversation 2026-04-26; not committed to repo
- "Architecting Autonomous Efficacy" research doc: provided by Logan in conversation 2026-04-26; not committed to repo
- Gemini deep-research doc: `.planning/research/gemini-deep-research/automating-long-term-planning-with-gsd-2.md` (committed); reading-notes pending at `.planning/research/gemini-deep-research/READING-NOTES.md` (Wave 5 commit 4)
- gsd-2 README: provided by Logan in conversation 2026-04-26 (verifiable at github.com/gsd-build/gsd-2); ground truth for §10.4 (post-migration AGENTS.md auto-load), §10.6 (gsd-2 artifact set), §11 (uplift soft note)

## 10. Logan dispositions 2026-04-26 — full reasoning, assumptions, citation honesty, and meta-concerns

This section records the disposition step. It mirrors the Wave 4 governance-synthesis §2.5 pattern: dispositions with reasoning + explicit assumptions + "where my reasoning may be wrong" sections, plus a cross-cutting concerns subsection. Per Logan's instruction ("include everything, even the assumptions, cross-cutting concerns and the 'where I might be wrong' etc."), the up-front shared assumptions (§10.1), citation-trust hierarchy (§10.11), recommendation-churn observation (§10.12), and where-I-most-welcome-pushback (§10.13) are all preserved here, not collapsed into the per-item sections.

Provenance: dispositions proposed by Claude (Opus 4.7, max effort) over multiple turns 2026-04-26; Logan reviewed across two explicit justification rounds (round 1 after initial harvest §1-§9; round 2 after the package shifted under Logan's framing corrections about gsd-2 mid-horizon timing and the Gemini doc's framing misalignment) and accepted dispositions as recommended in the final consolidated form. Single-author; subject to the same fallibility caveat as Wave 4's §2.5 footer.

### 10.0 Disposition status

All ten items accepted as recommended in the final consolidated form. None diverged from Claude's recommendation; all involved refinement from Claude's first-pass proposals across multiple turns of correction (see §10.12 recommendation-churn observation).

### 10.1 Up-front shared assumptions

Stated once and applied across all per-item dispositions. If any of these turn out wrong, the corresponding dispositions warrant re-review.

1. **Logan disposition, not agent disposition.** Future Wave-N work in this project assumes Logan is the disposition step. If this changes (e.g., Logan delegates dispositioning), several recommendations rebalance — particularly the M1-paired-review-substituted-by-Logan-as-second-reader argument (§10.9).
2. **Most future arxiv-sanity-mcp work involves agents** in some form (Logan+agent, agent-only). The runtime-instruction layer (CLAUDE.md / AGENTS.md content) is justified by this. If Logan intends to do v0.2 implementation himself with agents minimal, much of the runtime-instruction layer is over-engineered.
3. **gsd-2 migration is "soon" but not "now."** Per Logan's reframe ("mid-horizon basically means right after this... but it is no where near a complete and thus accurate inventory" of intervention surfaces), Wave 5 design tentatively lets uplift considerations inform marginal-cost-low decisions but does not bind to gsd-2 specifics. Migration timing affects G-D3 nice-to-have value (§10.4) and the G-D1 placement argument (§10.2).
4. **The gsd-2 README is the highest-trust source on gsd-2 itself.** It's verifiable, public, and provided by Logan. Where it disagrees with the Gemini doc, README wins. Where it disagrees with handoff §6's intervention-surfaces inventory, README wins. The Gemini doc's gsd-2 mechanism descriptions are largely accurate per README; its overall question-framing is misaligned with Logan's actual question.
5. **My calibration on this work has been imperfect.** I over-corrected twice (binding Wave 5 to handoff §6's mappings; calling RTK / Pi SDK / current-month arXiv IDs "confabulated" when they're real). I've factored this into how confidently I hold each recommendation below — mid-confidence recommendations are flagged as such.

### 10.2 G-D1 — `AGENTS.md` "Known difficulty patterns" section

**Disposition:** shape (a) — new section in AGENTS.md titled "Project-specific anti-patterns to detect" with ~7 patterns drawn from `LONG-ARC.md:42-54` plus the closure-pressure-at-every-layer pattern from the audit cycle. **Refinement:** verbatim cite-back per pattern (e.g., parenthetical `(LONG-ARC.md:46, "silent defaults")`) so duplication-drift is detectable on next-pass review.

**Assumptions:**

1. Operational question is "where does the agent encounter the pattern at decision time." Under current Claude Code, CLAUDE.md auto-loads; AGENTS.md is convention-loaded by name. Under post-migration gsd-2, AGENTS.md auto-loads at user and project level (gsd-2 README "Agent Instructions": "Pi core loads AGENTS.md automatically (with CLAUDE.md as a fallback)"). So putting the anti-patterns in AGENTS.md is correct under both runtimes.
2. The 005-008 spike chain drift is the canonical case proving the patterns are observed-in-this-project, not imported from outside.
3. Verbatim cite-back is cheap (a few characters per pattern) and the duplication-drift mitigation it enables is worth the cost.

**Reasoning:**

- Shape (b) (just point from AGENTS.md to LONG-ARC.md) reproduces the failure mode the section is meant to prevent — relying on the agent to know it should look elsewhere.
- Shape (c) (split 3-and-7) introduces a contestable ranking I can't ground; the patterns interrelate.
- The duplication-drift risk between AGENTS.md and LONG-ARC.md is real but cheap to mitigate via cite-back. If LONG-ARC.md is updated and AGENTS.md drifts, the cite-back pattern lets a careful reader notice on next-pass review.
- The README's AGENTS.md auto-load behavior post-migration strengthens the in-AGENTS.md placement argument.

**Where my reasoning may be wrong:**

- If AGENTS.md should remain a thin generic-bootstrap file, the right home for project-specific anti-patterns is a new file (e.g., `.planning/AGENT-WORKING-RULES.md`) and AGENTS.md just points to it. I don't think that's the better tradeoff under either runtime, but it's defensible.
- The README's AGENTS.md auto-load is a Pi SDK behavior; I'm assuming Pi's auto-load semantics will be preserved in gsd-2's continuing development. Reasonable but not guaranteed.
- The ~30-line target may be too tight or too loose. If the section grows past ~30 lines it crosses into BLOATED_SKILL territory; if too short, it fails to capture the pattern's nuance. Drafting will need to balance.

**Citation honesty:**

- I'm citing **LONG-ARC.md:42-54** as the source of the anti-patterns. This is project-internal canon that codifies this project's actual lessons learned (per the post-Wave-2 deliberations and the explicit 005-008 cycle that prompted LONG-ARC.md's creation). Load-bearing not because "the doc says so" but because the patterns named are observed-in-this-project, not imported from outside. Real grounding.
- I'm citing the **gsd-2 README's "Agent Instructions" section** as ground truth about runtime auto-loading. Verifiable; high-trust.
- I am **not** citing the research doc's anti-patterns claims as authority; the research doc's anti-patterns content is generic and adds nothing the project-internal canon doesn't already have. The OVER_CONSTRAINED principle is plausible from general LLM behavior; the specific ~15-absolutes threshold is unverified and treated as illustrative.

### 10.3 G-D2 — `AGENTS.md` ADR-citation example fix

**Disposition:** shape (a) — verbatim quote from ADR-0001 + misquote-vs-correct contrast as teaching example.

**Assumptions:**

1. The audit's symbolic concern is real: a discipline-section that demonstrates the discipline by violating it is a credibility wound.
2. Two sentences instead of one is acceptable cost; the teaching value is direct.
3. The specific failure mode (paraphrase inflation: permission → directive) is exactly the kind of error agents make routinely; showing failure-vs-correct contrast is more memorable than abstract discipline.

**Reasoning:**

- Silent-fix (shape b) closes the wound but leaves no record that the discipline is self-correcting.
- Using-a-different-ADR (shape c) sidesteps without acknowledgment.
- Shape (a) treats the prior failure as a learnable moment, consistent with the discipline rather than ornamental to it.
- The verbatim text from ADR-0001 (`docs/adrs/ADR-0001-exploration-first.md:22`) is "multiple retrieval and ranking strategies can coexist" — verified by direct read, not by trust in the synthesis.

**Where my reasoning may be wrong:**

- If shape (a) reads preachy or self-congratulatory, shape (a-lite) is fine — fix the quote silently with a one-line footnote ("Earlier version misquoted ADR-0001 as 'must coexist'; corrected per the discipline being taught"). The teaching value is the only thing lost; substantive correctness is preserved.
- I'm not being asked to assess whether the original AGENTS.md author *intended* "must" or made an error of phrasing. Either way, the fix is the same; the meta-acknowledgment doesn't depend on intent.

**Citation honesty:**

- I verified the ADR-0001 quote directly from the file in this session. Not relying on the synthesis's claim about it. The synthesis itself flagged this as deferred-pending-exemplar; the synthesis's recommendation is therefore not the grounding here.
- I am **not** citing "the synthesis recommends shape (a)" because the synthesis explicitly punts G-D items to exemplar harvest (this document) — citing it back would be circular.

### 10.4 G-D3 — `CLAUDE.md` restructuring

**Disposition:** shape (a) **full split, lean keep nice-to-have**. Mandatory: doctrine load-points section (~8 lines, contingent on §10.6 α adoption — which is adopted) + G-D4 fix (~2 lines). Nice-to-have, kept: calibrated-tradeoff preamble (Karpathy-pattern, ~3 lines) + positive-declarative reframing of "Key Architectural Constraints" (~3 lines, just rewriting existing content).

**Assumptions:**

1. Under **current** Claude Code runtime, CLAUDE.md is auto-loaded; it's the primary surface. Nice-to-have additions are worth doing for the current-period weeks where Claude Code is the runtime.
2. Under **post-migration** gsd-2, CLAUDE.md becomes fallback (gsd-2 README: "Pi core loads AGENTS.md automatically (with CLAUDE.md as a fallback)"). AGENTS.md takes over as primary auto-load.
3. Migration timing is "soon but tentative" not "imminent in days." If migration is in days, drop nice-to-have. If migration is in weeks-to-months, nice-to-have is worth ~10 lines.
4. The nice-to-have additions are durable in either runtime — calibrated-tradeoff preamble is a Karpathy pattern that survives any uplift redo; positive-declarative reframing is just rewriting existing content into a friendlier register.

**Reasoning:**

- Shape (b) (Karpathy-minimalism, strip CLAUDE.md heavily) is harder to justify when the file is already short (~80 lines). Karpathy-minimalism is the right posture when the file has bloated; CLAUDE.md hasn't.
- Shape (c) (status quo + only G-D4) is safest but skips the LONG-ARC/VISION integration mechanism (α load-points map) — most valuable addition in §5.
- Wave 4's commits `c31e21a` (governance read-order map) and `8c6220e` (CLAUDE.md minimal currency) already shaped the file. Wholesale rewrite would discard recent shaping work; targeted additions preserve it.

**Recommendation-stability note (per §10.12 recommendation-churn observation):** During deliberation I shifted on this item — initially "shape (a) split mandatory + nice-to-have," then briefly "mandatory only" (over-pivoting toward gsd-2-as-future-state when Logan reframed gsd-2 as imminent), then back to "lean keep nice-to-have" after Logan's "tentatively, not binding" correction. The final disposition reflects under-current-Claude-Code-runtime-CLAUDE.md-is-still-primary reasoning. If Logan's read on migration timing changes to "days not weeks," disposition shifts to mandatory-only.

**Where my reasoning may be wrong:**

- If gsd-2 migration is happening in days not weeks, drop nice-to-have. Logan's call on timing.
- If Logan found the Karpathy preamble specifically compelling, "lean keep" understates the conviction; reframe as "keep with conviction."
- ~110 lines is large for a runtime-loaded file. If empirical evidence emerges that token cost is a concrete problem, shape (b) becomes attractive. I do not currently have that evidence.

**Citation honesty:**

- gsd-2 README "Agent Instructions" section is high-trust; the AGENTS.md / CLAUDE.md auto-load semantics are verifiable.
- I am **not** citing the research doc's "Opus 4.7 absolute literalism" claim as authority for positive-declarative reframing. The positive-vs-negative framing principle is plausible from general LLM behavior; the specific Opus-4.7-literalism degree claimed in the research doc is unverifiable. Acting on the principle, not on the specific claim.
- I'm citing project history (Wave 4 commits `c31e21a` and `8c6220e`) verifiable in git log. Fair grounding for "wholesale rewrite would discard recent shaping work."

### 10.5 G-D4 — `CLAUDE.md` "Stack trajectory: Not Stack D" line

**Disposition:** shape (a) — gloss with definition + pointer. **With verification step:** re-check Stack-D foreclosure status against ADR-0005 before pinning the gloss; ADR-0005 may have shifted v0.2's compute/complexity ambition in ways that change the foreclosure rationale.

**Assumptions:**

1. Stack A → B is a load-bearing project commitment, surfaced in `PROJECT.md:109`, `PROJECT.md:129` (Key Decisions table), `ROADMAP.md`, and deliberations. Removing it from CLAUDE.md (shape b) loses an actual decision.
2. Bare "Not Stack D" is the silent-default pattern at the doctrine layer (per `LONG-ARC.md:48` "Silent defaults"). Adding the gloss is the minimal compliant fix.
3. ADR-0005-era thinking may differ from pre-redirection thinking; the gloss should reflect ADR-0005 status, not pure pre-redirection status.

**Reasoning:**

- Stack D = "full local hybrid research platform" defined at `docs/05-architecture-hypotheses.md:118`. Verified by direct grep in this session, not by trust in the synthesis.
- The recommendation in `docs/05:140` is "Stack A moving toward Stack B, not Stack D" — the CLAUDE.md line paraphrases this faithfully but elides the source.
- Shape (b) (drop the line) is cheaper but loses the actual decision; shape (c) (move to doctrine load-points) is over-architected for one line.
- The verification step (re-check against ADR-0005) is grounded in: ADR-0005's v0.2 multi-lens substrate may have shifted what counts as "compute and complexity v0.x has no evidence to justify." If Stack D's foreclosure rationale has changed, the gloss should reflect post-redirection foreclosure-or-reopening.

**Where my reasoning may be wrong:**

- ADR-0005 verification might surface that Stack-D foreclosure status has shifted. If so, the gloss reflects post-redirection thinking, not pre-redirection.
- "Cost and complexity that v0.x has no evidence to justify" is my paraphrase of why D is foreclosed; `docs/05` may have a more specific reason worth using verbatim.
- SV C1 itself self-labels as "trivial but real." If the Wave 5 budget is tight, shape (b) is the cheap fix. (a) costs ~2 lines.

**Citation honesty:**

- `docs/05-architecture-hypotheses.md:118-140` verified by direct grep in this session. Real grounding.
- The synthesis's SV-author self-label "trivial but real" (governance synthesis §G-D4) is taken at face value as evidence the SV-author saw it as a small fix, not as authority for fixing it. Grounding for fixing at all is: project explicitly committed (via LONG-ARC.md anti-patterns) to detecting silent defaults at the doctrine layer; removing one is consistent with that commitment.
- I am **not** treating handoff §6 or the Gemini doc as authority on Stack-D status. Both are silent on it.

### 10.6 LONG-ARC.md / VISION.md integration

**Disposition:** **α + β + γ + δ-as-pointer-note.**

- α (doctrine load-points map) → CLAUDE.md, ~8 lines.
- β (anti-pattern self-check) → AGENTS.md (this is G-D1's section, dual-purpose).
- γ (deliberation-boundary protocol) → AGENTS.md, ~15 lines, with conditional language ("when X, do Y") not absolute.
- δ-as-pointer-note → AGENTS.md γ section, ~2 sentences signaling intent: "Once v0.2 introduces the Lens interface, signal_type registry, and MCP-tool lens-awareness surfaces, those should be added to a protected-seams change-control list per the discipline above. The list does not yet exist because the surfaces do not yet exist."

**Refinement from harvest §5.5 recommendation:** The original §5.5 recommendation was "α+β+γ; defer δ unless evidence warrants." The disposition adds δ-as-pointer-note (not δ-as-content). Rationale for the refinement: codifying the *pattern* of protected-seams change-control with an explicit "list does not yet exist" pointer is durable; it survives any uplift redo and signals intent without fabricating placeholder content. Two sentences. Cheap insurance.

**Assumptions:**

1. The 005-008 spike chain drift evidences the drift risk (β) is real and high-severity even when low-probability per session. Project-internal evidence, not imported worry.
2. The propose-before-act discipline (γ) is a tested pattern from the gsd-modifier exemplar; the practice is sound even if the specific boundary list is contestable.
3. The README's gsd-2 artifact set (PROJECT.md / DECISIONS.md / KNOWLEDGE.md / RUNTIME.md / STATE.md / ROADMAP.md plus per-milestone CONTEXT/RESEARCH/PLAN/SUMMARY/UAT) does not natively include a routing-by-trigger map analogous to α — so α is genuinely additive content, not duplication of what gsd-2 will provide.
4. δ-as-content is fabrication (v0.2 surfaces don't exist yet); δ-as-pointer-note is durable signaling.

**Reasoning, by risk:**

- **Routing risk** (α): high probability per session, low severity per incident — agent does work in slight wrong direction; usually correctable. Cost ~8 lines. **Adopt.**
- **Drift risk** (β): medium probability, high severity — what 005-008 was; takes weeks to detect. Cost ~30 lines (this is G-D1's section). **Adopt.**
- **Surfacing risk** (γ): medium probability, medium severity. Cost ~15 lines. The boundary list is contestable but the practice is sound. **Adopt with caution about list contestability.**
- **Change-control risk** (δ): low probability, very high severity (breaking a load-bearing surface). Cost-as-content is high (v0.2 surfaces don't exist yet); cost-as-pointer-note is ~2 lines. **Adopt as pointer-note; defer content until v0.2 ships.**

**Cross-cutting concern:** aggregate absolute-count across α+β+γ. The OVER_CONSTRAINED principle (research doc) is plausible from general LLM behavior; the specific ~15-absolutes threshold is unverified. Mitigation: write each item as conditional ("when X, do Y") rather than absolute ("ALWAYS do Y") wherever possible. Counting bullets is wrong metric; counting absolutes is the metric.

**Where my reasoning may be wrong:**

- α/β/γ/δ is my construction. A fifth shape may exist. The cross-vendor codex dispatch (per §10.9) is partly insurance against shape blind spots in my own framing.
- δ's pointer-note may itself be over-engineered. If Logan would rather just defer δ entirely (no pointer-note), that's defensible — pointer-note costs ~2 lines and signals durable intent, but the cost-benefit isn't overwhelming.
- The combination presumes the agent reads both files. If only CLAUDE.md is auto-loaded (current Claude Code) and the agent doesn't proactively read AGENTS.md, β and γ benefit only the agent that explicitly reads AGENTS.md. The §4.3-shape-(a) preamble adds a CLAUDE.md→AGENTS.md pointer to mitigate.

**Citation honesty:**

- I'm citing the **observed project history** (005-008 drift documented in deliberations and audits) as the grounding for β. Real evidence, not internal garbage.
- I'm citing the **gsd-modifier exemplar's "do not silently flatten" formulation** as a concrete pattern that's worked in another project. Observable in the file Logan provided. Not authority — gsd-modifier is its own context — but a tested pattern.
- I'm **not** treating the research doc's anti-pattern taxonomy as authoritative; principle plausible, specific threshold unverified.
- I'm citing the **README's gsd-2 artifact set** to ground the claim that α adds genuinely new content rather than duplicating what gsd-2 provides. Verifiable.

### 10.7 Sequencing — mirror Wave 4

**Disposition:** harvest revision (this disposition record + synthesis pointer addendum) lands in this session; Wave 5 commits land in a fresh session per a self-contained briefing referencing this §10.

**Assumptions:**

1. Wave 4 pattern: dispositions worked through in xhigh session (`80cda50`), execution sub-agent dispatched in fresh session per self-contained briefing. Wave 5 mirrors this.
2. Fresh-session discipline (handoff §9) is documented but imperfectly observed; the principle stands that planning and execution mixed in the same session has documented bleed-through risk.
3. Wave 5 is 3-4 commits — small enough that sub-agent dispatch is overkill; **fresh session with Logan driving** is sufficient. Sub-agent was justified for Wave 4's 9 commits.

**Reasoning:**

- The harvest is the planning artifact. Once dispositioned, this document and the synthesis pointer are the entire planning step. Execution can be in fresh session.
- Cross-vendor codex dispatch on §5+§11 is also planning-adjacent (it informs Wave 5 phrasing). Can land in this session or fresh; either works.

**Where my reasoning may be wrong:**

- If Logan would rather get Wave 5 over with this session, the cost is one session's bias risk, which is small for a 3-4 commit governance change. Defensible.
- Wave 4 precedent is **one data point**; treating it as norm is the closure-pressure pattern. Honest framing: "we did this recently and it worked," not "this is how Wave-N is run."

**Citation honesty:**

- Handoff §9 fresh-session discipline is **soft preference**, not load-bearing rule. The Wave 2 case partially violated it and the synthesis was still adequate.
- Wave 4 precedent (commit `80cda50`) is one data point. Cited fairly as "we did this" not as authority.

### 10.8 Q1/Q4/Q16 validation — keep separate

**Disposition:** Q1/Q4/Q16 validation stays orthogonal to Wave 5; tracked in STATE.md Pending Validations table from Wave 4 commit `ee06cc1`.

**Assumptions:**

1. Q1/Q4/Q16 are foundation-audit closures pending **Logan's** validation of rationale recorded in `docs/10-open-questions.md` (lines 9, 31, 104). Work is: Logan reads three lines, decides if closure rationale is acceptable, confirms or reopens. **No agent work needed.**
2. Wave 5 is governance-document edits where agent work is the substance. Different work type.

**Reasoning:**

- Mixing them blurs the wave's scope. Wave 4's cleanness ("every commit was the same kind of work") was load-bearing for the wave's coherence.
- Tracker is already in STATE.md (Wave 4 commit `ee06cc1`). That's already the right home for follow-through.

**Where my reasoning may be wrong:**

- If Q1/Q4/Q16 validation reveals something that changes Wave 5 governance scope (e.g., Q1's signal-type validation changes how AGENTS.md should describe the profile primitive), they should be sequenced together. I don't expect this — closures are about retrospective rationale, not forward governance. Worth glancing at the three lines before Wave 5 commits.

**Citation honesty:**

- Pending Validations tracker verifiable in STATE.md. Project history I observed in this session's reads. Real grounding.

### 10.9 Paired audit — cross-vendor codex on §5 + §11, scoped vocabulary-mapping question

**Disposition:** cross-vendor codex (gpt-5.5) dispatch, ~30-min focused, scoped to §5 (LONG-ARC/VISION integration) and §11 (uplift soft note) only — not full harvest re-audit. Scope question: "do these α/β/γ patterns map onto gsd-2's existing artifact vocabulary (PROJECT.md / DECISIONS.md / KNOWLEDGE.md / RUNTIME.md / STATE.md), or do they require new artifact classes that gsd-2 doesn't currently have?" Output written to `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`.

**Disposition trace 2026-04-26:** Logan briefly considered overriding to "skip"; after Claude explained what the audit was for and what would be lost by skipping, Logan reversed and confirmed "let's still do it." Final disposition: do-it.

**Recommendation-churn observation (recorded explicitly per Logan's instruction to include "everything"):** I moved on this item across multiple turns. Initial recommendation: skip (M1 is at Hypothesis status; Logan disposition is the second-reader role; cost > benefit for taste-heavy work). Then briefly: do-it (multi-project blast radius via uplift propagation). Then back to skip (when Logan walked back the uplift-binding). Then back to do-it (when README facts made the diagnostic question concrete rather than aesthetic). The flip-flop is itself a signal worth recording: I do not have stable confidence on this item; the case is genuinely close and reasonable people would split.

**Assumptions (current disposition):**

1. With the README in hand, the diagnostic question is **concrete** rather than aesthetic. Before the README, asking "do these patterns generalize?" was abstract framing. With the README, asking "do these patterns map onto this specific listed artifact vocabulary?" is substantive artifact-matching. Cross-vendor reads handle artifact-matching well.
2. The Gemini doc precedent demonstrates that even sophisticated single-source reads can framing-mismatch on this topic (it answered "code-patcher on gsd-2" rather than "extend gsd-2 with VISION/LONG-ARC support"). A focused second read scoped to a concrete question helps catch shape mismatches before they bake into Wave 5 phrasing.
3. Cross-vendor codex is the right vendor: codex tends toward concrete artifact-mapping questions; same-vendor independent xhigh dispatch is less useful here because project framings already permeate same-vendor reasoning.

**Reasoning:**

- Cost: ~30 min dispatch + ~15 min comparison/integration. Manageable.
- Benefit: catches mapping mismatches between α/β/γ patterns and gsd-2 vocabulary before commits. If a fifth shape exists or the framework is mis-shaped, the dispatch surfaces it.
- Tight scoping prompt is the mitigation against noise-not-signal output. Provide README as ground truth; ask one diagnostic question.

**Where my reasoning may be wrong:**

- Cross-vendor dispatch may produce noise rather than signal if the second reader doesn't grasp the gsd-2-vocabulary-mapping question. Mitigation: tight scoping prompt with README and harvest §5+§11 attached.
- If the dispatch surfaces a fifth shape I missed, that delays Wave 5 commits. Acceptable cost in my view; the alternative is discovering the fifth shape post-commit when revision is more expensive.
- M1 discipline is at Hypothesis status (METHODOLOGY.md:112), reinforced by Wave 2 cycle but not confirmed. Invoking it as a discipline that "warrants" paired audit would overstate M1's epistemic standing. Honest framing: M1 is a discipline being tested; this would be its third test in conditions where the framing-claim load is medium-heavy. Not an authority claim.

**Citation honesty:**

- README's listed `.gsd/` artifact set as ground truth. Verifiable.
- Gemini doc as evidence of single-source framing-mismatch risk. Logan observed the mismatch; verifiable from the doc title and §6 content alone.
- M1 discipline cited honestly — Hypothesis status acknowledged, not promoted.
- Wave 4 precedent is one data point; not a discipline. Cited as "we did this," not as authority.

### 10.10 §11 candidate-uplift-primitives soft note + Gemini doc reading-notes

**Disposition (soft note):** include §11 — one paragraph at harvest footer with README-grounded facts about gsd-2's artifact set and the open mapping question. **No table.**

**Disposition (reading-notes):** create new ~10-line artifact at `.planning/research/gemini-deep-research/READING-NOTES.md` flagging: (i) gsd-2 mechanism descriptions in the doc are largely accurate per README; (ii) framing of the question is misaligned (code-patcher vs gsd-2-extension); (iii) LLM-evaluation specifics (TRACE rates, SAFi EMA decay 0.9) are unverified; (iv) treat as input-not-authority for any future gsd-2 design conversation.

**Assumptions:**

1. The README provides ground-truth facts about gsd-2's artifact set that *will* matter when uplift work begins. Recording them in the harvest footer is cheap; reconstructing later is wasteful.
2. The Gemini doc has provenance value (Logan ran it; gsd-2 mechanisms accurate per README) but framing misalignment risk. Without a reading note, future sessions may treat doc framing as authoritative.
3. Reading-notes is cheap insurance against future framing-mismatch propagation.

**Reasoning (soft note):**

- Earlier table-proposal was anchored to handoff §6's CR1-CR5 mappings, which Logan flagged as not authoritative and possibly mis-sourced. Building deliverable on §6 would propagate the misframing.
- Soft note records only what's verifiable from the README, plus the explicit "mapping is open" acknowledgment. No fabrication.

**Reasoning (reading-notes):**

- Doc accurately describes gsd-2 mechanisms (Pi SDK, RTK, worktree isolation, auto-loop pipeline, AGENTS.md auto-load, complexity routing) per README. Discounting the doc wholesale would be wrong.
- Framing misalignment is real per Logan's read; doc title "Architecting a Mid-Horizon Automated Patcher: Extending the GSD-2 Framework" reveals the misframing.
- LLM-eval specifics (TRACE arxiv:2604.03447, SAFi EMA 0.9) unverified. Today is 2026-04-26 (April 26, 2026); arxiv format YYMM.NNNNN means 2604.xxxxx is current-month, not future-dated. Whether these specific papers exist I cannot verify without web access.

**Where my reasoning may be wrong (soft note):**

- If Logan would rather the harvest *not* mention gsd-2 at all (keep Wave 5 strictly arxiv-sanity-mcp-internal), drop §11 entirely. Defensible argument: keeps Wave 5 cleanly scoped.

**Where my reasoning may be wrong (reading-notes):**

- Reading-notes itself may become stale if Logan re-runs research with sharper prompt. Mitigation: short reading-note with clear "as-of date 2026-04-26" so a re-run dated later supersedes cleanly.
- TRACE / SAFi specifics may be real; I'm flagging as unverified without claiming confabulated. If they're real and I'd flagged-as-confabulated, that would have been a calibration error of the same shape as my Pi-SDK / RTK / arxiv-date errors.

**Citation honesty (soft note):**

- All facts from README. High-trust, verifiable. Honest position is "the mapping is open; here are the facts."

**Citation honesty (reading-notes):**

- README is the verification source for gsd-2 mechanisms. High-trust.
- Self-corrective: reading-notes explicitly names what I got wrong about the doc earlier (date error; calling RTK and Pi SDK invented).
- TRACE / SAFi: honest stance is "unverified," not "confabulated." Same calibration discipline that should have been applied to RTK / Pi SDK from the start.

### 10.11 Citation trust hierarchy

What I'm grounding on, by trust level. An audit-discipline reader can use this to assess whether any per-item recommendation rests on weaker sources than I claim.

- **High-trust** (verifiable, provided by Logan or public, observable):
  - gsd-2 README (provided by Logan; verifiable at github.com/gsd-build/gsd-2)
  - Karpathy CLAUDE.md exemplar (provided by Logan)
  - gsd-modifier AGENTS.md exemplar (provided by Logan)
  - Current ADR-0001 / ADR-0005 / `docs/05` text in this repo
  - Current CLAUDE.md / AGENTS.md / LONG-ARC.md / VISION.md text in this repo
- **Medium-trust** (project-internal, codifies real observed experience):
  - LONG-ARC.md anti-patterns (codifies project's actual lessons; the 005-008 cycle is the ground truth)
  - CONTEXT.md epistemic discipline section in current AGENTS.md
  - Audit-cycle findings about closure pressure and silent defaults
- **Lower-trust** (real but limited or contextual):
  - M1 discipline (Hypothesis status; reinforced not confirmed by Wave 2 cycle)
  - Wave 4 precedent (one data point, not a discipline)
  - Gemini doc's gsd-2 mechanism descriptions (accurate per README but framed around wrong question)
  - Research doc's general framing principles (plausible but specific quantifications unverified)
- **Not-treating-as-authority**:
  - Handoff §6's CR1-CR5 intervention-surfaces inventory (per Logan's flag)
  - Research doc's specific quantified claims (PluginEval %s, OVER_CONSTRAINED ~15 threshold, "50,000 tokens before quality drop," "93% permission approval rate")
  - Gemini doc's TRACE / SAFi specifics (unverified — not "confabulated," but unverified)

### 10.12 Cross-cutting meta-concerns

Beyond the per-item where-might-be-wrong notes, these are concerns about the harvest as a whole.

1. **Recommendation churn observation.** I moved on the paired-audit recommendation across multiple turns (skip → do-it → skip → do-it). I also moved on G-D3 nice-to-have (keep → drop → keep). Logan's framing corrections were the proximate cause in both cases, but the underlying signal is: my confidence on these items is genuinely lower than on G-D1, G-D2, G-D4. Recording the churn explicitly so a future reader sees the recommendations were not stable arrivals.

2. **M1 Hypothesis caveat.** M1 (independent-dispatch sub-discipline) is at Hypothesis status. Citing it as "warranting" paired audit overstates its epistemic standing. The harvest invokes M1 in §10.9 and §6.5 as a worth-honoring discipline; not as a load-bearing rule.

3. **Framework-is-my-construction caveat.** α/β/γ/δ in §5 is my four-shape construction. Logan's actual best answer might be a shape I did not name. The cross-vendor codex dispatch (§10.9) is partly insurance against this.

4. **Closure-pressure-at-meta-layer risk.** Producing a tidy harvest with shape (a)/(b)/(c) per item and a single recommended combination is itself the closure-pressure pattern the audit cycle keeps surfacing. I have tried to keep alternatives genuinely live and recommendations marked as recommendations. If a recommended shape feels obviously right on first read, that is a signal to slow down — not a signal to commit.

5. **Single-author fallibility.** Same as Wave 4 §2.5 footer. Logan's disposition is the actual decision step; if any disposition becomes contested in execution, re-review.

6. **Calibration errors recorded explicitly.** Two specific errors during deliberation: (i) future-dated-arxiv-IDs claim was wrong (today is 2026-04-26; YYMM.NNNNN format makes 2604.xxxxx current-month, not future); (ii) RTK / Pi SDK called invented when both are real per README. The pattern: confident-quantification-without-traceable-source flagging led me to over-discount real items. Mitigation going forward: "unverified" rather than "confabulated" when I lack web access to verify.

7. **The "include everything" instruction is itself a constraint worth noting.** Per Logan's instruction "include everything, even the assumptions, cross-cutting concerns and the 'where I might be wrong' etc." — this section grew large because Logan asked for it, not because length-for-its-own-sake is the goal. Future readers should treat §10 as a comprehensive disposition record, not as a template suggesting all dispositions need to be this long.

### 10.13 Where I'd most welcome push-back

If Logan's disposition acceptance is firm and committed across the package, this section is preventive rather than active. If any disposition feels slightly off post-commit, the items below are where I'd revisit first.

- **Decision 5 (paired audit) — §10.9.** I moved on this each turn; current disposition is do-it (cross-vendor codex on §5+§11 only). If Logan finds the recommendation churn unhelpful, I can hold either position firmly. Both are defensible.
- **Decision 2 (the α/β/γ/δ framework) — §10.6.** It's my construction; the cross-vendor read is partly insurance against shape blind spots.
- **G-D3 nice-to-have keep-vs-drop — §10.4.** Depends on your read of migration timing in a way I can't infer. If "days," drop nice-to-have; if "weeks-to-months," lean keep.

The other items I'm more confident in.

## 11. Candidate uplift primitives — soft note (post-disposition footer)

Wave 5 outputs may be referenced when gsd-2 work begins. The α/β/γ patterns in §5 (doctrine load-points map; anti-pattern self-check; deliberation-boundary protocol) and the δ pointer-note describe shapes that *might* generalize as workflow primitives in an extended gsd-2.

However, **the mapping to gsd-2 is open**, and Wave 5 does not design for it. Two specific reasons:

1. **The Gemini deep-research doc's framing was misaligned** (it answered "how to architect a code-patcher built on gsd-2" rather than "how to extend gsd-2 with VISION/LONG-ARC support"). Treating the doc's CR1-CR5 mappings as work specifications would propagate the misframing.
2. **Handoff §6's CR1-CR5 intervention-surfaces inventory was sourced from current-GSD audit experience, not gsd-2**, per Logan's read; it is "no where near a complete and thus accurate inventory" of gsd-2's surfaces.

What is verifiable from the gsd-2 README:

- gsd-2 auto-loads `AGENTS.md` with `CLAUDE.md` as fallback at user and project levels.
- gsd-2's `.gsd/` artifact set has: `PROJECT.md`, `DECISIONS.md`, `KNOWLEDGE.md`, `RUNTIME.md`, `STATE.md`, `ROADMAP.md`, plus per-milestone `CONTEXT.md` / `RESEARCH.md` / `S0X-PLAN.md` / `T0X-PLAN.md` / `T0X-SUMMARY.md` / `S0X-UAT.md`.
- gsd-2 has a `/gsd migrate` tool for `.planning` → `.gsd` conversion (phases → slices, plans → tasks, milestones preserved).
- gsd-2 has no native artifact class for VISION.md or LONG-ARC.md.

The integration question (where do VISION.md / LONG-ARC.md / METHODOLOGY.md fit in gsd-2's vocabulary?) is open and is part of what the gsd-2 uplift initiative will address.

This soft note is for whoever picks up gsd-2 work — possibly Logan, possibly a fresh-session agent — so the verifiable facts and the open question are recorded once, not re-derived.

---

*Single-author harvest. Recommendations are recommendations; the disposition step is the actual decision step. §10 records the disposition step with full reasoning per Logan's instruction. Subject to the same fallibility caveat as the Wave 4 governance synthesis revision (synthesis §2.5 footer).*
