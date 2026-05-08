# ADR-0001 — Exploration-first architecture

**Status:** Accepted  
**Date:** 2026-03-08

## Context

The project begins with major uncertainty around:

- retrieval family,
- ranking family,
- interest representation,
- workflow-state model,
- and MCP surface shape.

A premature hard commitment would likely make later experiments expensive or biased.

## Decision

We will structure the early system so that:

- multiple retrieval and ranking strategies can coexist,
- workflow-state features can be added without rewriting the core,
- interest state is not reduced to tags internally,
- and major unresolved questions remain documented until evidence justifies closure.

## Consequences

### Positive
- preserves optionality,
- reduces architectural churn later,
- encourages evidence-driven design.

### Negative
- requires discipline to avoid vague abstraction,
- some code may stay slightly more generic than a one-off implementation.

## Notes

This ADR is about **process and architecture posture**, not about avoiding implementation.
We still prefer small, concrete, useful increments.
