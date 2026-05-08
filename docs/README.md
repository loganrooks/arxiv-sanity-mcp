# Documentation Map

This is the initial documentation suite for the repository bootstrap.

It is designed for **human + agent** collaboration in the early phase of the project.

## Documents

### `01-project-vision.md`
The top-level product vision, goals, non-goals, user stories, and success criteria.

### `02-product-principles.md`
The product virtues we are trying to preserve from arxiv-sanity and the new virtues required for an MCP-native system.

### `03-design-space.md`
A broad map of the design space so we do not narrow too early.

### `04-reference-designs.md`
External systems and patterns worth learning from, without copying them blindly.

### `05-architecture-hypotheses.md`
Candidate architecture shapes and cost-aware stack options.

### `06-mcp-surface-options.md`
Different ways to think about the MCP interface before freezing a schema.

### `07-data-sources-content-rights.md`
Data-source roles, rights constraints, and content-normalization options.

### `08-evaluation-and-experiments.md`
How we will compare retrieval, recommendation, workflow, and extraction choices.

### `09-roadmap.md`
A phased path from repo bootstrap to a useful first system.

### `10-open-questions.md`
Explicit unresolved questions that should stay visible.

### `11-sources.md`
External references used to ground this initial documentation suite.

### `adrs/`
Small initial ADR set for process and constraint decisions that are strong enough to commit to now.

### `templates/`
Templates for future ADRs and experiments.

## Recommended reading order

1. `01-project-vision.md`
2. `02-product-principles.md`
3. `03-design-space.md`
4. `04-reference-designs.md`
5. `05-architecture-hypotheses.md`
6. `06-mcp-surface-options.md`
7. `07-data-sources-content-rights.md`
8. `08-evaluation-and-experiments.md`
9. `09-roadmap.md`
10. `10-open-questions.md`

## Why this suite is shaped this way

The point of this docs set is not to pretend we already know the right retrieval method, ranking stack, or user-state model.

The point is to give the repo:

- a clear product thesis,
- explicit constraints,
- a disciplined exploration process,
- and enough structure that agents can implement without silently foreclosing the design space.
