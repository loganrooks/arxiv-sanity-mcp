# AGENTS.md

This file defines how agents should work in this repository during the bootstrap phase.

## Mission

Help build an MCP-native research discovery substrate inspired by arxiv-sanity, while preserving the most important product values:

- discovery over overload,
- explicit and steerable taste / interest modeling,
- fast browse / triage loops,
- recent-paper monitoring,
- and inspectable ranking and provenance.

## Do not do these things

Do **not**:

- assume tags are the final or canonical taste representation,
- assume dense retrieval is obviously the winner,
- assume lexical retrieval is obsolete,
- assume the first MCP interface should mirror a web UI,
- assume “paper chat” is the product,
- serve or redistribute full text without checking license / provenance implications,
- collapse open questions into hidden code assumptions.

## Default working posture

Unless an ADR says otherwise:

1. keep the design space open,
2. prefer cheap defaults,
3. preserve reversibility,
4. record uncertainty explicitly,
5. separate hypotheses from decisions.

## Project-specific anti-patterns to detect

Patterns this project has already drifted into once (the 005-008 spike chain is the canonical case). When you notice one, name it; surface it to a deliberation rather than working around it. Cite-back to `LONG-ARC.md` per pattern so duplication-drift between this section and the source is detectable on next-pass review.

- **Tournament narrowing under "disciplined" framing** (`LONG-ARC.md:47`). Sequentially pruning a candidate set toward a winner. Counter-posture: rank-and-deprioritize, not eliminate; multi-lens framing replaces winner-pick.
- **Single-lens "interface" by accident** (`LONG-ARC.md:48`). Shipping a lens abstraction alongside only one lens — the abstraction ends up shaped exactly to that lens. Counter-posture: validate abstractions by shipping a second implementation, per ADR-0005.
- **Silent defaults** (`LONG-ARC.md:49`). A reference frame becomes the implicit baseline that all alternatives are measured against, even when nothing argued for it being baseline. Counter-posture: name the reference frame explicitly; require challengers measured against multiple frames or task outcomes.
- **ADR violation by gradual local-reasonable steps** (`LONG-ARC.md:50`). Each step locally defensible; cumulative drift away from an accepted ADR. Counter-posture: run an ADR-against-current-work check at deliberation boundaries (see below); ADRs are read at planning time, not just at writing time.
- **Closure pressure at every layer** (`LONG-ARC.md:51`). Confident remedies, prescriptive language, calibrated language reserved for closing footnotes. Counter-posture: calibrated language as default register; flag confident-sounding remedies for paired review before adoption (see `METHODOLOGY.md:104-115`, M1).
- **Embedding-model choice as load-bearing decision** (`LONG-ARC.md:52`). Treating "which model wins" as the architectural commitment when most leverage lives upstream. Counter-posture: treat embedding-model selection as one lens-design decision among many.
- **Single-reader framing claims as authoritative** (`LONG-ARC.md:53`). Audit memos and framing critiques produced by one reader propagated as ground truth. Counter-posture: paired review for framing claims (cross-vendor + same-vendor); consult `METHODOLOGY.md` (M1 status: Hypothesis as of 2026-04-26 update at line 119).

## Required habits for agents

### 1. Mark your level of commitment
When proposing architecture or API changes, explicitly classify them as:

- Settled
- Chosen for now
- Hypothesis
- Open

### 2. Update the right document
- New durable decision -> add or update an ADR
- New experiment -> update `docs/08-evaluation-and-experiments.md` and/or use the experiment template
- New unresolved issue -> update `docs/10-open-questions.md`
- New external precedent or pattern -> update `docs/04-reference-designs.md`

### 3. Respect the core constraints
Always keep in mind:

- **Time semantics matter**: submission, update, and announcement are not the same thing.
- **License semantics matter**: metadata, full text, PDFs, source, and derived content have different reuse constraints.
- **Provenance matters**: store where every ranking signal, content artifact, or taste signal came from.
- **Cost matters**: do not require expensive embeddings or heavyweight infrastructure without a strong reason.
- **Explainability matters**: prefer systems that can explain why a paper was returned.

### 4. Prefer these abstractions
Use these terms unless there is a better reason not to:

- **paper**
- **content variant**
- **interest profile**
- **collection**
- **saved query**
- **watch**
- **triage state**
- **result set**
- **ranking explanation**

Avoid hardcoding the system around `tag -> papers` as the universal model.

## Default implementation bias

The default bias for early implementation should be:

- metadata mirror before heavy content mirroring,
- lexical baseline before semantic-only retrieval,
- candidate generation + reranking architecture,
- lazy enrichment over eager enrichment,
- small MCP surface with strong primitives,
- explicit workflow state for agents,
- local-first where feasible.

## Before you make a major change

Ask:

1. Does this preserve the soul of arxiv-sanity?
2. Does this reduce or increase irreversible commitment?
3. Can we evaluate it against a baseline?
4. What is the cost impact?
5. What is the legal / licensing impact?
6. What new provenance do we need to track?

## Definition of success for early agents

A successful early contribution is one that makes the project:

- more testable,
- more explainable,
- more modular,
- more license-aware,
- and more capable of comparing alternatives without repeated rewrites.

## CONTEXT.md epistemic discipline

When creating or updating CONTEXT.md files and other planning artifacts:

### Separate traceable claims from derived and interpretive ones
- **Source-traceable**: Claim directly restates a specific passage in user-authored docs (01-11), an accepted ADR, or an explicit user instruction. Cite the source.
- **Artifact-reported**: Claim directly reports what an inspected code path, experiment artifact, log, or checked-in output says. Keep scope narrow and name the artifact.
- **Derived**: Claim combines traceable items with a small, explicit inferential step. Mark it as `[derived]` and state the bridge.
- **Interpretive**: Claim depends on substantive framing, analogy, or explanatory judgment. Mark it as `[interpretive]` or `[chosen for now]` with reasoning.
- **Never** present a derived or interpretive claim as if it were source-traceable or artifact-reported.
- Avoid bare `grounded` as an epistemic label in new planning artifacts. It is too overloaded and too easily heard as "validated" or "settled."
- Older artifacts may still use the legacy `grounded / inferred` language. Treat it as historical terminology, not the preferred schema for new work.

### Do not close Open Questions without authority
- Items in `docs/10-open-questions.md` are **intentionally unresolved** by the user.
- An AI agent may **propose** an answer (mark as `[chosen for now]`) but must not silently adopt it as settled.
- Closing an Open Question requires: user confirmation, or a new ADR with explicit rationale.
- If implementation requires choosing an answer, document it as provisional and flag for user review.

### ADR citations must be specific
- When citing an ADR to justify a decision, quote the specific clause or principle that applies.
- Do not cite an ADR number alone as blanket authority for decisions the ADR does not address.
- Example (verbatim quote, with deliberate fidelity to ADR text): ADR-0001 states "multiple retrieval and ranking strategies can coexist" (`docs/adrs/ADR-0001-exploration-first.md:22`) — this is a capability commitment about the architecture (the design must support coexistence), not a directive that every project decision *must* engage multiple strategies. Compare to the inflated paraphrase "multiple retrieval/ranking strategies must coexist" — that paraphrase converts a permission into a directive and is therefore inaccurate, even though it sounds more authoritative. Earlier versions of this section misquoted ADR-0001 as "must coexist"; corrected per the discipline being taught.

### No speculative product strategy
- CONTEXT.md files describe implementation decisions, not business models or monetization.
- Product strategy (pricing, donation models, growth) is out of scope unless the user introduces it.

## Deliberation boundaries

Some change-types deserve a pause-and-surface step before proceeding — propose the change, name the alternatives, and wait for confirmation rather than auto-executing. The list below is conditional ("when X, do Y"), not absolute. When in doubt about whether a change qualifies, surface it; the cost of pausing is small.

When proposing a change that fits any of the items below, state: (i) the observed problem; (ii) the proposed change; (iii) why now; (iv) alternatives considered; (v) the expected write-set; (vi) verification plan.

- **When reshaping a spike, milestone, or phase plan structurally** (not minor edits) — surface and propose; do not restructure in place.
- **When modifying any accepted ADR's text, status, or scope** — surface and propose; ADRs are read at planning time and accepted via deliberation, not amended silently.
- **When introducing or removing a top-level abstraction** (lens type, signal type, workflow primitive) — surface and propose; check the abstraction against ADR-0005's "validate by shipping a second implementation" discipline.
- **When changing the MCP tool / resource / prompt surface in ways visible to existing callers** — surface and propose; backward-compat semantics are part of the surface contract.
- **When editing `LONG-ARC.md`, `VISION.md`, or the project root `CLAUDE.md` / `AGENTS.md`** — surface and propose; doctrine-layer changes warrant deliberation rather than in-place editing during routine work.
- **When closing an Open Question** (per `docs/10-open-questions.md`) without a new ADR or explicit user confirmation — do not close; mark `[chosen for now]` instead and flag for review.

Once v0.2 introduces the `Lens` interface, `signal_type` registry, and MCP-tool lens-awareness surfaces, those should be tracked as protected-seams subject to the change-control discipline above; the specific tracking mechanism (a list inline here, a dedicated artifact, or a harness-level mechanism) is to be decided when the surfaces ship. The list does not yet exist because the surfaces do not yet exist.
