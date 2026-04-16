---
id: sig-2026-04-16-inter-milestone-exploration-gap
type: signal
project: arxiv-mcp
tags: [gsd-framework, milestone-lifecycle, inter-milestone-exploration, process-gap]
created: 2026-04-16T18:39:31Z
updated: 2026-04-16T18:39:31Z
durability: principle
status: active
severity: notable
signal_type: capability-gap
phase: spike-program
plan: between-milestones-structure
polarity: negative
source: manual
occurrence_count: 2
related_signals: [sig-2026-03-19-spike-framework-scope-gap]
runtime: codex-cli
model: gpt-5
gsd_version: 1.19.4
---

## What Happened

During review of the project's current planning state, a workflow gap became explicit: the `v0.1` milestone was completed but never formally archived, and spike-program work began immediately afterward because the spike findings were expected to determine the shape of the *next* milestone rather than fit cleanly inside the old one.

The current GSDR structure cleanly models in-milestone execution and individual spikes, but it does not appear to provide a first-class mode for **inter-milestone exploration**: a bounded period of research, spike chaining, and deliberation that exists after one milestone is complete and before the next milestone is committed.

## Context

This project is now in exactly that state:

- the main roadmap work for `v0.1` is complete and marked as such in `STATE.md`
- the milestone was not formally closed/archived
- spike work continued because the unresolved questions were not implementation tasks inside `v0.1`, but inputs needed to shape the next milestone

Without an explicit framework concept for this situation, the repo drifted into an in-between state:

- too complete to honestly treat as an active implementation milestone
- too consequential to treat as unstructured side work
- and too forward-looking to force into the old roadmap as an extra phase

The case for adding such a concept to GSDR is that it would let projects distinguish:

1. **milestone execution** — committed implementation work
2. **inter-milestone exploration** — inquiry that determines what should be committed next
3. **next milestone planning** — turning findings into a new roadmap

That distinction would reduce confusion about closure status, scope, and what kinds of artifacts or gates are appropriate at each step.

## Potential Cause

The framework currently has stronger support for two modes than for the transition between them:

- phase/milestone execution inside a committed roadmap
- standalone spikes as isolated experiments

What is under-modeled is the situation where multiple spikes, deliberations, and synthesis artifacts collectively function as a **research program between milestones**. In that situation, the missing framework concept leads to predictable symptoms:

- completed milestones remain formally open
- exploratory work gets half-attached to the old roadmap
- users and agents lose clarity about whether they are implementing, exploring, or planning
- and the eventual next milestone has to be inferred from ad hoc artifacts rather than produced through a supported transition
