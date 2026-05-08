---
id: sig-2026-03-20-deliberation-naming-convention
type: signal
project: arxiv-mcp
tags: [gsd-framework, deliberation, naming-convention, artifact-navigation]
created: 2026-03-20T17:30:00Z
updated: 2026-03-20T17:30:00Z
durability: convention
status: active
severity: notable
signal_type: custom
phase: spike-003
plan: n/a
polarity: negative
source: manual
occurrence_count: 1
related_signals: [sig-2026-03-20-premature-spike-decisions]
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## What Happened

Deliberation artifacts use topic-based filenames (`deployment-portability.md`, `v2-literature-review-features.md`, `spike-epistemic-rigor-and-framework-reflexivity.md`) with no temporal prefix. When listing a directory of deliberations, they sort alphabetically by topic name — which has no relationship to recency, importance, or logical ordering.

Signals already use `YYYY-MM-DD-slug.md` convention. Spike DESIGN/DECISION/FINDINGS files sit inside dated directories. Deliberations are the outlier — they lack temporal metadata in the filename.

## Context

With 3 deliberations in this project, navigation is trivial. But the pattern doesn't scale. A project with 10-15 deliberations (common for long-lived projects with multiple milestones) would present an opaque alphabetical list. The user noted that they remember deliberations by relative ordering ("the one we did after the spike review"), not by topic name. Agents scanning for "most recent deliberations" would need to open each file and parse the `Date:` field or frontmatter rather than reading the filename.

Current deliberation filenames in this project:
- `deployment-portability.md`
- `spike-epistemic-rigor-and-framework-reflexivity.md`
- `v2-literature-review-features.md`

With temporal prefix, these would sort by creation date:
- `2026-03-13-v2-literature-review-features.md`
- `2026-03-14-deployment-portability.md`
- `2026-03-20-spike-epistemic-rigor.md`

Additionally: deliberations lack structured frontmatter entirely (no `id`, `created`, `updated`, `author`, `model` fields). The deliberation template provides only inline markdown fields (`**Date:**`, `**Status:**`). This session's deliberation added YAML frontmatter as an experiment, but the template doesn't prescribe it.

## Potential Cause

The deliberation template was likely designed when projects had 1-2 deliberations. The naming convention wasn't a problem at that scale. As the artifact type matures and projects accumulate more deliberations, the lack of temporal ordering becomes a navigation problem for both humans and agents.

The broader pattern: signals, spikes, and phases all have structured naming/metadata conventions. Deliberations were designed as free-form documents with minimal structure. This may have been intentional (deliberations are exploratory, resist premature formalization) but the practical cost is poor navigability.
