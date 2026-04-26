---
type: audit-package
status: ready-for-dispatch
date: 2026-04-25
purpose: Paired audit of v0.2 plan + VISION + LONG-ARC + METHODOLOGY before Phase 12 execution
---

# v0.2 Plan Paired Audit Package

## Why this exists

The v0.2 multi-lens substrate plan (committed 2026-04-25) was authored in a single session by a single reader (Claude Opus 4.7). The plan integrates ADR-0005 (architectural commit), v0.2-MILESTONE.md (scope spec), ROADMAP.md Phases 12-17 (phase details), REQUIREMENTS.md v0.2 codes (17 new), VISION.md (product identity), LONG-ARC.md (planning doctrine), and the extended `spikes/METHODOLOGY.md` (six new practice disciplines). All of these rest on each other; auditing them as separate documents misses the integration.

Per `spikes/METHODOLOGY.md` practice discipline A (paired review for framing claims), single-reader output should not drive Phase 12 execution on contestable framing without independent challenge. This package dispatches two parallel reviews:

| Review | Reader | Role | Effort |
|---|---|---|---|
| Cross-vendor primary | GPT-5.5 via codex CLI | independent reading; substance focus | high |
| Same-vendor adversarial | Claude Opus 4.7 (fresh session, via Agent tool) | argue against framing claims; register focus | high |

The cross-vendor reviewer tests whether an independent vendor reads the same coherence (or finds the same gaps) in the integrated plan. The same-vendor adversarial reviewer tests whether the in-house rhetorical patterns (closure pressure, prescriptive language overrunning diagnostic grounds, "load-bearing" / all-caps emphasis as argument-substitutes) survive a hostile read.

Two-axis disagreement is more informative than either alone.

## Scope

The audit reads — *as a single integrated artifact set* — these documents:

1. `.planning/milestones/v0.2-MILESTONE.md` (scope spec)
2. `.planning/ROADMAP.md` Phases 12-17 (phase details)
3. `.planning/REQUIREMENTS.md` v0.2 Requirements section (17 codes)
4. `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` (architectural commit)
5. `.planning/VISION.md` (product identity)
6. `.planning/LONG-ARC.md` (planning doctrine)
7. `.planning/spikes/METHODOLOGY.md` (practice-disciplines extension)

Reviewers may consult, but should not audit:

- `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` (gating audit; input)
- `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md` (journey artifact; context)
- `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md` (this session's handoff; orientation)

## Audit dimensions (both prompts apply these in order)

1. **LONG-ARC anti-pattern check.** Does the plan re-introduce tournament narrowing, accidental single-lens interface, silent defaults, ADR-violation-by-drift, closure pressure, embedding-model-as-load-bearing, or single-reader framing claims as authoritative?
2. **VISION coherence check.** Does v0.2 honor VISION's load-bearing claims (multi-lens substrate; research-practice operations beyond retrieval; longitudinal-memory; provenance/inspectability; lens trajectory)? Does it honor anti-vision (not paper chatbot, not RAG wrapper, not ranked-list-but-fancier, not arxiv-sanity-but-better)?
3. **LONG-ARC protected-seams check.** Does the plan preserve all named seams (lens extensibility, bundle-of-signals primitive, per-lens provenance, MCP surface lens-awareness, citation as first-class data, longitudinal state, inspectability, MCP-native operations)?
4. **METHODOLOGY practice-discipline check.** Does the plan apply paired-review discipline, calibrated language, pre-registration of empirical thresholds, model verification, pattern-watch?
5. **Critical-path realism check.** Is `12 → 13 → 16 → 17` realistic? Are 14 and 15 dependencies right? Is "~2 months" plausible given the dependency graph?
6. **Coverage check.** Does the plan miss anything that ADR-0005 commits or that VISION names as load-bearing?
7. **Risk completeness.** Are the named risks the actual risks? What's missing?

## How to dispatch

### Cross-vendor primary

```bash
codex exec --model gpt-5.5 -c model_reasoning_effort=high \
  --dangerously-bypass-approvals-and-sandbox \
  --cd /home/rookslog/workspace/projects/arxiv-sanity-mcp \
  "$(cat .planning/audits/2026-04-25-v0.2-paired-audit-package/cross-vendor-prompt.md)" \
  > .planning/audits/2026-04-25-v0.2-plan-audit-cross-vendor.md
```

### Same-vendor adversarial

Dispatch via Agent tool with `subagent_type: "general-purpose"` (not Explore — Explore lacks Write tool), `model: "opus"`, and the contents of `opus-adversarial-prompt.md` as the prompt. The agent writes its output to `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md`.

Both can run in parallel.

## After dispatch

When both reviews complete, synthesize at `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md`. Synthesis should:

- Adopt non-framing-claim findings immediately as plan revisions (with file/line cites).
- Flag framing-claim findings for further consideration.
- Identify convergent findings (both reviewers caught it) and divergent findings (only one caught it; characterize why).
- Propose plan-revision commits before Phase 12 execution begins.

## Provenance protocol

The 2026-04-25 spike paired review established the pattern that each reviewer's output is preserved on disk and the synthesis cites both rather than collapsing them into one verdict. Same protocol here. The two paired-review outputs are evidence; the synthesis is the actionable artifact.
