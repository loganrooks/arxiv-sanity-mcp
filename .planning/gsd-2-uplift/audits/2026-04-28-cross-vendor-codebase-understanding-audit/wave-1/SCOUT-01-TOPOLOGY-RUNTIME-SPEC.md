---
type: wave-1-scout-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: medium
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md
domain: topology-runtime
---

# Scout 01 Spec — Topology / Runtime

## Role

You are a medium-reasoning scout. Your job is to locate source surfaces and pre-check simple claims. You are not the final adjudicator.

You are testing whether the existing gsd-2 uplift investigation appears to have understood `gsd-2` topology and runtime surfaces well enough for later high-reasoning adjudication.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md`

## Reasoning Tier

Use medium reasoning. This is a scout pass, not a final architectural judgment.

Do not try to build a complete codebase model. Produce a bounded source map and nominate claims for high adjudication.

## Scope

Investigate:

- package layout and monorepo structure
- source entrypoints for CLI / TUI / headless modes
- MCP and RPC surfaces
- vendored Pi relationship
- package-boundary and clean-seam claims
- obvious docs/source divergences around runtime activation

Out of scope:

- detailed workflow plugin internals
- full extension-surface taxonomy
- release cadence / changelog practice
- broad product interpretation or R-strategy judgment

## Work Order

### Phase A: Source-first map

Before reading the current Claude synthesis, inspect the source target directly.

Suggested commands:

- `pwd`
- `git -C /home/rookslog/workspace/projects/gsd-2-explore status --short --branch`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 3 -type f -name 'package.json' | sort`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 2 -type d | sort`
- `rg -n "headless|mcp|rpc|PI_PACKAGE_DIR|GSD_CODING_AGENT_DIR|ADR-010|gsd-agent-core|gsd-agent-modes|cli|commander|yargs" /home/rookslog/workspace/projects/gsd-2-explore`

Use `nl -ba <file> | sed -n '<start>,<end>p'` or equivalent when you need stable line citations.

### Phase B: Claim pre-check

After the source-first map, read only the relevant current artifacts:

- `.planning/gsd-2-uplift/exploration/02-architecture-output.md`
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections that discuss topology/runtime/Pi/MCP/RPC

Pre-check simple claims mechanically where possible. For architectural claims, nominate them for high adjudication rather than deciding them yourself.

## Claims To Watch For

Watch especially for claims like:

- `gsd-2` is a vendored modified Pi fork.
- ADR-010 proposes a clean seam that is not implemented.
- There is no `gsd-agent-core` or `gsd-agent-modes` package.
- CLI/headless/MCP/RPC are distinct runtime surfaces.
- RTK or other runtime surfaces are docs-present but source-gated.
- README or docs overstate runtime defaults compared to source.

These are examples, not a closed checklist.

## Required Output

Write the output file with this structure:

```markdown
---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 01 topology-runtime
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 01 — Topology / Runtime

## 0. Scout Summary

<5-10 bullets: source surfaces found, obvious confirmations/refutations, and what needs high adjudication.>

## 1. Source Paths Inspected

<List files/directories inspected, with one-line purpose notes.>

## 2. Source-First Topology Map

<Bounded map of packages, entrypoints, and runtime surfaces. Mark docs-derived vs source-derived observations.>

## 3. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|

## 4. Claims Needing High Adjudication

<6-10 candidate claims at most. For each: why it is load-bearing, source paths to inspect, and what makes it non-mechanical.>

## 5. Suspected Omissions or Conflations

<Possible missing runtime surfaces, package-boundary conflations, or docs/source divergence classes.>

## 6. Scope Boundaries

<What you deliberately did not inspect.>

## 7. Scout Caveat

This is a medium-reasoning source scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2`.
```

## Quality Bar

- Cite source files and lines for source-backed claims.
- Keep conclusions modest.
- Do not infer codebase intent from README alone.
- Do not treat "found one challenge" as "the current synthesis is wrong overall."
- Do not perform broad fresh synthesis across all gsd-2 uplift artifacts.
