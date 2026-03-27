---
id: sig-2026-03-20-agent-acted-without-asking
type: signal
project: arxiv-mcp
tags: [agent-behavior, feedback, unauthorized-action, gsd-framework]
created: 2026-03-20T19:00:00Z
updated: 2026-03-20T19:00:00Z
durability: convention
status: active
severity: notable
signal_type: deviation
phase: spike-003
plan: n/a
polarity: negative
source: manual
occurrence_count: 1
related_signals: []
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## What Happened

Agent created a `deliberations/` directory in `~/.claude/get-shit-done-reflect/` and copied a file there without asking the user first. The actual GSD Reflect project repo lives at `~/workspace/projects/get-shit-done-reflect/` with its own `.planning/deliberations/` directory containing 20 existing deliberations. The agent didn't check for this and modified the wrong location.

## Context

User asked whether the deliberation should be migrated to the GSD Reflect repo. Agent checked `~/.claude/get-shit-done-reflect/` (the installed runtime), found no `.planning/` directory, and created one — without checking whether a separate development repo existed at `~/workspace/projects/`. The machine's CLAUDE.md documents the convention that all software projects live at `~/workspace/projects/`, and GSD Reflect's own CHANGELOG references it as a project. Agent should have checked or asked.

## Potential Cause

Agent treated `~/.claude/get-shit-done-reflect/` as the canonical location without considering that it might be a deployed/installed copy of a project that lives elsewhere. The distinction between "installed runtime" and "development repo" wasn't checked. Agent proceeded with a multi-step action (create dir, copy file, edit metadata) without confirming the approach — violating the principle of checking before taking actions that modify shared state.
