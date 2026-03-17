# Product Principles

**Status:** Draft  
**Date:** 2026-03-08

This document records the product virtues we should preserve and the new ones we should add.

## 1. Discovery over generic conversation

The project should primarily help users and agents:

- find papers,
- rank papers,
- expand from seeds,
- monitor changes,
- and triage efficiently.

Summaries, comparisons, and synthesis may exist, but they should support discovery workflows rather than define the product.

## 2. Explicit, steerable interest modeling

The original arxiv-sanity systems used libraries and tags to represent taste explicitly. That explicitness is a feature. [S25][S26]

The future system should preserve the principle, not necessarily the exact mechanism.

Possible explicit signal types include:

- manual tags,
- seed paper sets,
- saved queries,
- followed authors,
- provisional machine suggestions,
- project workspaces,
- temporary session interests,
- negative examples,
- and mixed explicit + learned profiles.

The invariant is:

> The user should be able to inspect, steer, confirm, reject, and override the system’s notion of what is interesting.

## 3. Recent-paper monitoring is first-class

arXiv is not just a static paper database. It is also a time-structured stream with submission, update, and announcement semantics. [S1][S4][S9]

That means the product must support:

- “what’s new,”
- “what changed,”
- recurring watches,
- and delta-oriented workflows.

## 4. Multiple kinds of relatedness are valuable

“Similar paper” is not one thing.

Useful variants include:

- lexical similarity,
- semantic similarity,
- co-citation / bibliographic coupling,
- citation neighborhood,
- topic overlap,
- author or lab adjacency,
- relevance to a specific interest profile.

A good system should expose or at least preserve room for multiple relatedness operators.

## 5. Inspectability is part of the product

arxiv-sanity stood out because it was not purely magical. The future system should keep that spirit.

A result should be explainable using structured signals such as:

- query match,
- seed relation,
- category / topic match,
- interest profile match,
- citation signal,
- popularity signal,
- and recency.

## 6. Workflow state matters more in MCP than in a website

A human browsing a site supplies a lot of implicit state:

- what they already saw,
- what they rejected,
- what they are working on right now.

An MCP server often needs that state explicitly.

So the product should expect to support objects like:

- collections,
- triage states,
- saved queries,
- watches,
- and checkpoints.

## 7. Cost-awareness is a design virtue, not a temporary constraint

We should assume from the start that good design means:

- not embedding everything eagerly,
- not parsing every PDF upfront,
- not requiring expensive hosted infrastructure,
- and not doing heavy enrichment before it clearly buys value.

The elegant system is the one that gets strong usefulness per unit of complexity and cost.

## 8. Rights, provenance, and compliance are core

Metadata, PDFs, source files, HTML, derived markdown, and graph enrichments all have different provenance and reuse semantics. arXiv explicitly permits broad reuse of metadata, but not general redistribution of full e-prints unless the paper’s license allows it. [S2][S7]

Therefore:

- every content artifact should record source and rights context,
- every ranking signal should record provenance,
- and hosted/public deployments should be stricter than private/local ones.

## 9. MCP is a workflow substrate, not just a transport

MCP gives us tools, resources, and prompts as separate surfaces. [S20][S21][S22][S23]

That means we should think in terms of:

- actions,
- canonical objects,
- and reusable workflows,

not just one large search endpoint.

## 10. Open questions should remain visible

Some decisions can be made now.
Many should remain open until we have evidence.

The docs, ADRs, and experiment plan should make that boundary obvious.
