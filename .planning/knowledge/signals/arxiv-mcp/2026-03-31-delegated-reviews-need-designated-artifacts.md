---
id: sig-2026-03-31-delegated-reviews-need-designated-artifacts
type: signal
project: arxiv-mcp
tags: [agent-orchestration, review-workflows, artifact-discipline, external-reviews]
created: 2026-03-31T19:30:18Z
updated: 2026-03-31T19:30:18Z
durability: principle
status: active
severity: notable
signal_type: capability-gap
phase: spike-program
plan: design-next-spike-round
polarity: negative
source: manual
occurrence_count: 1
related_signals: []
runtime: codex-cli
model: gpt-5
gsd_version: 1.18.0+dev
---

## What Happened

During external review of the canonical next-round spike suite, a reusable review spec was created and used successfully with the local `claude` CLI. The review returned valuable findings, but only as ephemeral terminal output. It did not write to a designated artifact such as a named review document under `.planning/`, and the current review request pattern did not require it to do so.

The user identified this as a workflow gap: delegated or external reviews should default to writing into an explicit artifact rather than leaving their output only in terminal scrollback.

## Context

This arose while testing whether a common review task/spec could be used both for external model runs and for internal agents. The spec itself exists and is reusable, but the orchestration pattern still treats artifact output as optional. That weakens auditability, comparison across review passes, and future reuse in a dedicated review skill.

The problem is not that the review failed. The problem is that the workflow leaves durable review capture to ad hoc follow-up instead of making it the default contract.

## Potential Cause

The current GSD-style planning and review workflows are stronger on critique content than on critique persistence. They assume the orchestrator will summarize or translate useful review output afterward, but they do not yet encode a principle that review-producing agents and external model calls should write to a designated artifact by default.
