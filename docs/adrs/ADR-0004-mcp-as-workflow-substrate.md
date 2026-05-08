# ADR-0004 — MCP as workflow substrate, not just a wrapper

**Status:** Accepted  
**Date:** 2026-03-08

## Context

A naïve design would expose the existing web concepts as a search API and call it an MCP server.

But MCP supports tools, resources, and prompts, and agent workflows usually require more explicit state than a human website session.

## Decision

We will design the MCP layer as a workflow substrate.

Practically, this means:

- not forcing everything through one mega search tool,
- expecting explicit workflow objects such as collections, saved queries, or triage state,
- and planning for canonical resources and reusable prompts in addition to tools.

## Consequences

### Positive
- better fit for agent workflows,
- better long-term protocol design,
- avoids simple UI-to-MCP parameter translation.

### Negative
- requires more thought before freezing the public surface.

## Notes

This ADR does not say all workflow objects ship in v1.
It says the MCP design should anticipate them.
