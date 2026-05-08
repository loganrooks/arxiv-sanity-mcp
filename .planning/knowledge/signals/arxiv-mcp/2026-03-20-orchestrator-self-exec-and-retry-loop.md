---
id: sig-2026-03-20-orchestrator-self-exec-and-retry-loop
type: signal
project: arxiv-mcp
tags: [delegation-failure, retry-without-diagnosis, orchestrator-discipline]
created: 2026-03-20T20:00:00Z
updated: 2026-03-20T20:00:00Z
durability: convention
status: active
severity: notable
signal_type: struggle
phase: spike-003
plan: W5 gap-filling
polarity: negative
source: manual
occurrence_count: 1
related_signals: []
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## What Happened

During Spike 003 gap-filling, the orchestrator ran 6 WebFetch calls directly to research batch pricing for API embedding services instead of delegating to a research agent. Four of those calls hit 403 errors on platform.openai.com, and the orchestrator retried the same domain with slightly different paths without stopping to diagnose why the requests were failing or adapting the approach.

## Context

The first API cost research (covering standard pricing for OpenAI, Cohere, Voyage, Google) was correctly delegated to a deep-research-agent and completed successfully. When the user asked a follow-up about batch pricing specifically, the orchestrator switched to running WebFetch directly — breaking the delegation pattern that had been working. The 403 errors on OpenAI's platform docs are likely due to bot detection or auth requirements, but no investigation was done.

## Potential Cause

1. **Delegation lapse**: The follow-up question felt "small enough" to handle inline rather than spawn an agent. This is a judgment error — the cost research agent had already established the research pattern and could have been continued via SendMessage, or a new focused agent spawned.

2. **Retry without diagnosis**: The 403 errors were treated as transient failures to retry rather than a signal to investigate (e.g., try a different domain, use WebSearch instead of WebFetch, check if the URL requires auth). The same error pattern repeated 4 times without adaptation.

3. **Pattern**: When an orchestrator starts doing tool calls that agents should be doing, it's usually because the orchestrator is optimizing for speed over reliability. The cost is wasted context window and undiagnosed failures.
