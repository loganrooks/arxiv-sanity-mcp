---
id: sig-2026-03-19-spike-framework-scope-gap
type: signal
project: arxiv-mcp
tags: [gsd-framework, spike-workflow, process-gap]
created: 2026-03-19T18:00:00Z
updated: 2026-03-19T18:00:00Z
durability: convention
status: active
---

## Observation

The spike execution framework (spike-execution.md) assumes contained experiments: one question, max 2 rounds, single agent spawn for Build → Run → Document. Spike 003 (strategy profiling) requires 5 waves across 7+ sessions with branch points that change subsequent wave design. The framework's "exploratory" type allows refining during execution but the structural constraint (2 rounds, one agent, Design → Build → Run → Document) doesn't accommodate iterative multi-wave investigation with inter-wave dependencies.

## Impact

Working outside the framework for Spike 003 — executing wave-by-wave with agent-based quality gates instead of human checkpoints, treating each wave as a sub-spike within the larger investigation.

## Recommendation

The spike framework could benefit from a "program" or "campaign" type for multi-wave exploratory investigations where findings from each wave inform the design of the next. This would formalize what Spikes 001-003 have already been doing in practice.

## Additional Gaps (same signal, expanded)

### Missing KB templates
The spike runner agent (`gsdr-spike-runner.md`) references `@/home/rookslog/.claude/agents/kb-templates/spike-design.md` and `spike-decision.md` — these files do not exist. The agent is built against templates that were never created.

### No spike program concept
The framework handles individual spikes (one question, one agent, one decision). There is no concept of a coordinated multi-spike investigation with:
- A shared ROADMAP across spikes
- Inter-spike dependencies
- Shared data assets (corpus, embeddings, enrichment)
- Progressive refinement where spike N's findings inform spike N+1's design
- Agent-based quality gates instead of human checkpoints

Spikes 001-003 in this project have been operating as a spike PROGRAM managed through an ad-hoc ROADMAP.md with no template and no framework support. The framework should formalize this pattern.

### Exploratory type vs exploratory execution
The "exploratory" spike type changes success criteria (learning goals, can refine) but NOT execution structure (still 2 rounds, single agent, Build → Run → Document). Multi-wave investigations need iterative execution with branch points between waves, not just flexible success criteria.
