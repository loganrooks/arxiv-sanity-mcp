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

When creating or updating CONTEXT.md files for phase planning:

### Separate grounded decisions from inferences
- **Grounded**: Decision traceable to a specific passage in user-authored docs (01-11), an accepted ADR, or explicit user instruction. Cite the source.
- **Inferred**: Decision made by AI based on patterns, analogies, or judgment. Mark explicitly as `[inferred]` or `[chosen for now]` with reasoning.
- **Never** present an inference as if it were grounded.

### Do not close Open Questions without authority
- Items in `docs/10-open-questions.md` are **intentionally unresolved** by the user.
- An AI agent may **propose** an answer (mark as `[chosen for now]`) but must not silently adopt it as settled.
- Closing an Open Question requires: user confirmation, or a new ADR with explicit rationale.
- If implementation requires choosing an answer, document it as provisional and flag for user review.

### ADR citations must be specific
- When citing an ADR to justify a decision, quote the specific clause or principle that applies.
- Do not cite an ADR number alone as blanket authority for decisions the ADR does not address.
- Example: "ADR-0001 states 'multiple retrieval/ranking strategies must coexist' -- this means..." not just "per ADR-0001."

### No speculative product strategy
- CONTEXT.md files describe implementation decisions, not business models or monetization.
- Product strategy (pricing, donation models, growth) is out of scope unless the user introduces it.
