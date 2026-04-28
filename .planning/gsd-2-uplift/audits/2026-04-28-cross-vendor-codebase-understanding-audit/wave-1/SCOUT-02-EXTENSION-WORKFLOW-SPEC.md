---
type: wave-1-scout-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: medium
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-02-extension-workflow.md
domain: extension-workflow
---

# Scout 02 Spec — Extension / Workflow

## Role

You are a medium-reasoning scout. Your job is to locate source surfaces and pre-check simple claims. You are not the final adjudicator.

This is the heaviest scout pass. Keep it bounded: identify mechanisms, source paths, and obvious confirmations/refutations. Do not try to fully judge extension viability or workflow architecture.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-02-extension-workflow.md`

## Reasoning Tier

Use medium reasoning. This is a scout pass, not a final architectural judgment.

Do not decide whether R2 extension strategy is viable. Nominate the source claims that a high-reasoning adjudicator should test.

## Scope

Investigate:

- extension loaders and extension APIs
- workflow plugin system
- workflow template discovery and execution modes
- skills discovery / skill manifests
- hooks and trust boundaries where directly relevant
- `markdown-phase` vs `yaml-step`
- automation execution-mode claims

Out of scope:

- full runtime topology outside extension/workflow surfaces
- release cadence and commit-history practice
- deep contribution-culture analysis
- final R1/R2/R3/R4/R5 viability judgment

## Work Order

### Phase A: Source-first mechanism inventory

Before reading the current Claude synthesis, inspect the source target directly.

Suggested commands:

- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 4 -type f | rg "(extension|workflow|skill|hook|trust|template|phase|yaml|markdown)" | sort`
- `rg -n "ExtensionAPI|GSDExtensionAPI|extension|workflow plugin|workflow-plugin|workflow-template|skill|hook|trusted|markdown-phase|yaml-step|GRAPH.yaml|STATE.json|context_from|shell-command" /home/rookslog/workspace/projects/gsd-2-explore`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 5 -type f -path '*workflow*' | sort`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 5 -type f -path '*skill*' | sort`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 5 -type f -path '*extension*' | sort`

Use line-cited source snippets for claims you pre-check.

### Phase B: Claim pre-check

After the source-first inventory, read only the relevant current artifacts:

- `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md`
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections that discuss extension/workflow/skills/hooks

Pre-check simple claims mechanically where possible. For subsystem-boundary claims, nominate them for high adjudication.

## Claims To Watch For

Watch especially for claims like:

- There are at least four extension-adjacent subsystems.
- Pi coding-agent extensions and GSD ecosystem extensions are distinct.
- Workflow plugins are distinct from extension APIs and skills.
- Skills have their own discovery and manifest system.
- `markdown-phase` is prompt-dispatch rather than deterministic executor-owned shell execution.
- `yaml-step` uses graph-backed deterministic mutation and structured dependency/context behavior.
- Extension/trust/security boundaries matter for uplift viability.

These are examples, not a closed checklist.

## Required Output

Write the output file with this structure:

```markdown
---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 02 extension-workflow
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 02 — Extension / Workflow

## 0. Scout Summary

<5-10 bullets: mechanisms found, obvious confirmations/refutations, and what needs high adjudication.>

## 1. Source Paths Inspected

<List files/directories inspected, with one-line purpose notes.>

## 2. Mechanism Inventory

<Inventory extension/workflow/skill/hook mechanisms. For each: source path, apparent role, and whether it appears distinct or possibly overlapping.>

## 3. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|

## 4. Claims Needing High Adjudication

<6-10 candidate claims at most. For each: why it is load-bearing, source paths to inspect, and what makes it non-mechanical.>

## 5. Possible Missing Sibling Mechanisms

<Mechanisms current artifacts may have missed or conflated. Mark uncertainty.>

## 6. Scope Boundaries

<What you deliberately did not inspect.>

## 7. Scout Caveat

This is a medium-reasoning source scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2`.
```

## Quality Bar

- Cite source files and lines for source-backed claims.
- Keep subsystem-boundary conclusions tentative.
- Do not infer implementation behavior from workflow-template prose alone.
- Do not decide R2 viability.
- Do not perform broad fresh synthesis across all gsd-2 uplift artifacts.
