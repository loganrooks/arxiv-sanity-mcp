---
id: sig-2026-03-30-explorer-reasoning-effort-high-at-most
type: signal
project: arxiv-mcp
tags: [agent-orchestration, explorer-agents, reasoning-effort, resource-discipline]
created: 2026-03-30T12:57:38Z
updated: 2026-03-30T12:57:38Z
durability: principle
status: active
severity: notable
signal_type: custom
phase: spike-program
plan: design-next-spike-round
polarity: neutral
source: manual
occurrence_count: 1
related_signals: []
runtime: codex-cli
model: gpt-5
gsd_version: 1.18.0+dev
---

## What Happened

During orchestration of the next spike-round work, exploration agents were being considered with elevated reasoning settings. The user clarified that exploration agents should not use `xhigh` reasoning. `High` is the upper bound for this class of work, and `medium` is often sufficient. For this project, the practical rule is: if an exploration agent needs elevated reasoning, use `high` at most.

## Context

This came up while structuring pre-spike analysis work and deciding how to delegate bounded exploratory subtasks. The distinction matters because exploration agents are typically used to gather bounded codebase or artifact context, not to carry the core interpretive or design burden. Overshooting reasoning effort on exploration work increases cost and latency without proportionate epistemic gain.

The correction is specifically about non-planning exploration work. It does not imply that all subagents should default to `medium`, nor that more demanding reasoning is never warranted elsewhere. It sets a ceiling for exploration agents and preserves `high` as the strongest acceptable setting in that lane.

## Potential Cause

The orchestration heuristics were optimizing for success probability and bounded delegation quality, but they lacked an explicit local rule about reasoning-effort ceilings by agent role. Without that role-specific constraint, it is easy to over-provision explorer reasoning effort "just to be safe," even when the task is better served by tighter, cheaper settings.
