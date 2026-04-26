---
type: deliberation
status: decided — implementation open
date: 2026-04-25
level: design-direction (project-level)
form: long-form narrative with explicit decision, options, open questions
follow_through: redirection committed; implementation pending Property audit
related:
  - ../spikes/reviews/2026-04-25-handoff-pressure-pass.md
  - ../spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md
  - ../spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md
  - ../handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md
  - ../spikes/004-embedding-model-evaluation/OPEN-QUESTIONS.md
  - ../../docs/adrs/0001-exploration-first-architecture.md
---

# Long-Arc and Multi-Lens Redirection

## What prompted this deliberation

After ~two weeks of methodology audit work — a deliberation, an independent review of it, a dimensional reframing addendum, a pressure pass on the spike-suite handoffs, a paired AI review (cross-vendor + Opus adversarial) of the pressure pass, and an operationalization audit that walked itself back from six recommendations to three — I had landed on a small-fixes answer: append a `007` override annotation, fix `008`'s asymmetric comparison surface, decide which profile-construction family `008` should use, then run `008`. The user pushed back hard:

> "I don't care about the cost, I want this done right, I want it to be the best possible research tool it can possibly be, which means we need to think about every little thing. We need to question whether the way we have framed this research, the way we have been asking questions, the way we have been designing experiments have foreclosed potentially better versions of this tool. We need to think of the long arc as well, where do we want to go? And whether what we are building now will put us in a better position to get closer to that."

That prompt did three things at once: refused the small-fixes frame, demanded foundations-questioning, and asked for long-arc orientation. The deliberation that followed produced the most substantive direction shift of the session.

## What the deliberation surfaced

### The implicit commitments of the spike program

The spike program 003-008 had been operating under six implicit commitments that, examined against ADR-0001, didn't hold up:

1. **Profiles are pre-built, not emergent.** Eight fixed BERTopic profiles from MiniLM clusters (Spike 001) were the only way to express researcher interest. The substrate hadn't been questioned at the root since 004 surfaced the issue.
2. **Retrieval is the central operation.** The whole stack was "given a profile, find papers." Other research-practice operations (orienting attention, tracking lineages, locating dissent, detecting paradigm shifts) were not surfaced in design.
3. **The agent is the unit of evaluation.** `008` measures whether an agent produces better research output for a stated bounded task. Longitudinal practice was not the evaluation surface.
4. **Embedding-model choice is the load-bearing architectural decision.** Most spike effort had gone into "which model wins," even though most actual tool-quality leverage probably lives upstream of embedding choice (query interpretation, profile elicitation, result presentation, interaction-loop design, trust calibration, provenance, explanation).
5. **Tournament narrowing is the discovery mechanism.** Each spike pruned the candidate set toward a winner.
6. **MiniLM is silent default.** Even after Spike 005's partial de-MiniLM-ification, MiniLM-derived profiles remained the *incumbent reference frame*. Challengers were measured against a frame the incumbent constructed.

The pattern under all six: the spike program had drifted toward winner-pick under tournament-narrowing despite ADR-0001's accepted commitment to exploration-first multi-lens architecture. The methodology had been disciplined; the substantive frame had drifted from the philosophical orientation. The drift was *invisible from inside the spike program* because every step looked reasonable.

### The audience correction

After the initial multi-lens reframe was sketched (using philosophy-overfitted examples like Levinas, phenomenology, and Continental aesthetics), the user issued a separate correction: the tool is for AI researchers primarily, not philosophy researchers. That correction sharpened — rather than weakened — the multi-lens case. AI research is intensely community-structured (specific labs, specific conferences, specific paper threads) in ways that make citation/community lenses, benchmark/dataset lenses, and methodological lenses substantially more load-bearing than they would be for slower fields. Topic-cluster representation flattens AI-research practice in particularly damaging ways: RLHF papers and constitutional-AI papers are topically similar but conversationally distinct; mechanistic-interpretability papers are topically similar but methodologically very diverse.

(The audience correction is its own deliberation: see `2026-04-25-audience-reframe-arxiv-ai.md`.)

### What the current framing has foreclosed

Specifically:

- **The multi-lens architecture itself**, by treating ADR-0001's coexistence commitment as aspirational rather than load-bearing.
- **The longitudinal-practice evaluation surface**, by committing to bounded-task evaluation as the function-in-use definition.
- **The deeper substrate question** — profile elicitation, taste capture, longitudinal memory — by treating profiles as fixed inputs to model evaluation rather than as the load-bearing decision.
- **The discursive-community register** for AI research, by treating citation networks as enrichment (Phase 6) rather than as a primary signal.

### The long-arc vision (AI-research register)

A best-possible-research-tool for an arxiv-AI researcher:

- Knows reading history at depth — not just what was retrieved but what was read, time-on-page, annotated, cited approvingly, dismissed.
- Recognizes argumentative / methodological style — what kinds of approaches you find compelling.
- Surfaces lateral connections — "this argument structurally resembles X in another community, which you read eight months ago."
- Tracks intellectual lineages — citation cascades, conceptual influence, paradigm trajectories.
- Respects discursive-community structure — RLHF vs DPO vs constitutional AI as distinct conversations, not a topic cluster.
- Makes operations legible — every recommendation comes with reasoning; provenance for every signal.
- Steerable — multiple lenses (semantic, citation/community, author, benchmark, methodological, temporal) the researcher selects between.
- Accountable to dissent — when you disagree with a recommendation, the disagreement becomes part of the model.
- Memory across sessions — what you cared about three weeks ago is still there.

This is *not* arxiv-sanity-but-better. It overlaps (paper substrate, retrieval, profile abstraction) but the long-arc tool has a different center of gravity: it lives in the researcher's practice over years, and most of its value is in operations that aren't simple retrieval.

## What was decided

**Concrete decision (user-confirmed 2026-04-25):**

- v0.2 will be **multi-lens.** ADR-0001 honored in implementation, not just design.
- **Citation/community lens is the load-bearing v0.2 addition** (the second lens beyond existing semantic). Reasons: AI research is intensely community-structured; citation graphs are particularly load-bearing for AI; this is the highest-leverage AI-specific addition the spike program neglected.
- **BERTopic profile primitive will be generalized to bundle-of-signals**, not replaced. BERTopic stays as one signal among many; behavior-derived, citation-anchor-derived, and researcher-curated-prose signals can be added in parallel without breaking changes.
- **Spike `008` will not run as a tournament.** It will be reshaped (or replaced) as part of a longitudinal pilot using multi-lens MCP. Decision deferred pending vision document.
- **Cost of redirection is acceptable.** No code is being torn up; the redirection is methodological. v0.1 (31/31 plans, MCP server, 403 tests) stays.

## Roadmap options

The roadmap commit between three options is not yet made. It's contingent on a Property audit of Phase 3 (interest modeling) implementation — see `Open questions` below.

| Option | Scope | Cost | Multi-lens fidelity |
|---|---|---|---|
| **A** | Full multi-lens substrate in v0.2 | 3-4 months engineering + spike work | Highest |
| **B** *(default lean)* | Refactor primitives + ship two lenses (existing semantic + new citation/community) | ~2 months | Validated by shipping a second lens |
| **C** | Refactor for extensibility, ship one lens, multi-lens validated in v0.3 | ~1 month | Honored at design level only |

Option B is preferred because **abstractions are most likely to be right when validated by a second implementation.** Option C risks the lens-extensibility abstraction being subtly wrong in ways that only become visible when adding the second lens — by which time consumers depend on it. Option A is too expensive for one milestone.

## Open questions

1. **Property audit of Phase 3 implementation.** Highest-leverage open item. Three properties:
   - Is the existing interest-profile primitive lens-extensible (bundle-of-signals shape) or BERTopic-coupled?
   - Are MCP tool signatures lens-aware (accept a `strategy=` parameter or equivalent), or do they assume single-lens?
   - Is storage committed to one similarity type, or already abstracted per-lens?
   The Option A/B/C choice is contingent on the audit answers.
2. **Vision document** (≤2-page constraint articulation; AI-research register; iteratable). Not yet written. Should set the criterion the spike program is judged against, replacing "which model retrieves best."
3. **Phase ordering.** Should Phase 6 (content normalization) and citation-graph data integration be pulled forward into v0.2 to support citation/community lens? Likely yes; needs explicit decision.
4. **Which third lens** after citation/community? Methodological (high AI-research leverage but needs taxonomy work) or benchmark/dataset (uniquely AI-specific, easier integration). Open.
5. **`008` fate.** Reshape as longitudinal pilot using multi-lens, or shelve, or run for partial signal. Pending vision document outcome.
6. **Profile-elicitation alternatives.** Behavior-derived, citation-anchor-derived, researcher-curated prose. Spike value high. When? Probably after v0.2 ships (so the bundle-of-signals primitive can be informed by what other signals look like) but a small upfront spike could de-risk the abstraction.
7. **MiniLM-entanglement remediation.** Spike 005 partially addressed it; carried forward by inertia since. The bundle-of-signals primitive lets us add non-MiniLM-derived signals without breaking — the question is which to add first and when.

## Status of follow-through

- **Direction committed.** ✓
- **Vision document written.** ✗ — not yet drafted.
- **Property audit performed.** ✗ — the immediate next concrete action.
- **Roadmap commit (A/B/C) made.** ✗ — contingent on audit.
- **v0.2 plan written.** ✗ — pending roadmap commit.
- **`008` fate decided.** ✗ — pending vision document.
- **Handoff written.** ✓ — see `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md`.

The redirection is decided but unrealized. The first concrete action that would manifest it is the Property audit.

## What this deliberation says about the project

Two meta-observations:

1. **ADR-0001 was binding all along; the spike program had quietly violated it.** The deliberation rediscovers, rather than invents, the architectural commitment. The two months of spike work narrowing toward `008` were operating outside the ADR's intent. This is worth preserving as a lesson: even disciplined-looking work can violate accepted ADRs if the violation is gradual and locally reasonable.

2. **The closure-pressure pattern recurs at every layer.** The original spike program narrowed toward a winner. The methodology audit work then exhibited the same pattern — confident remedies, prescriptive language, calibrated language as closing footnote. The redirection itself can fall into this pattern (six confidently-listed reorientation components walked back to a smaller set under assumption audit). Pattern-watch is needed at every level of work, not just the level being audited.

## What the form of this document tries to honor

This is the most consequential deliberation of the session, so the form is long: narrative of the prompt, the implicit-commitment audit, the audience correction's effect, the long-arc vision, the decision, the options, the open questions, and the follow-through honesty. The point is not to produce a verdict — the redirection was already accepted by the time this document was written — but to **preserve the journey** so future-self (Claude or Logan) can see *how* the conclusion was reached, *what* was foreclosed, and *what remains undone*.

The form fits because the redirection is a foundational shift; brevity here would lose the warrant for the shift.
