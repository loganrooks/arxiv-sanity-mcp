---
type: wave-1-scout-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: medium
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-03-release-practice.md
domain: release-practice
---

# Scout 03 Spec — Release / Practice

## Role

You are a medium-reasoning scout. Your job is to locate source and history surfaces, pre-check simple claims, and flag which release/practice claims need high adjudication.

You are not the final adjudicator. Do not decide whether gsd-2's release discipline is good, bad, stable, unstable, or culturally coherent. Distinguish machinery from observed practice.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-03-release-practice.md`

## Reasoning Tier

Use medium reasoning. This is a command-heavy scout pass, not a final interpretive judgment.

## Scope

Investigate:

- changelog structure
- tag and commit-history availability
- breaking-change markers
- release scripts
- GitHub workflows
- workflow templates related to release / hotfix / breaking changes
- deprecation or migration policy evidence
- shallow-history caveats

Out of scope:

- extension-surface taxonomy
- runtime topology outside release surfaces
- final conclusion about whether machinery/practice divergence is a stable pattern
- maintainer receptiveness or contribution-culture deep probe

## Work Order

### Phase A: History and source preflight

Before reading the current Claude synthesis, inspect the source target directly.

Suggested commands:

- `git -C /home/rookslog/workspace/projects/gsd-2-explore rev-parse --is-shallow-repository`
- `git -C /home/rookslog/workspace/projects/gsd-2-explore log --oneline --decorate -30`
- `git -C /home/rookslog/workspace/projects/gsd-2-explore tag --list | tail -50`
- `rg -n "BREAKING CHANGE|!:\\s|Breaking changes|breaking change|Deprecated|Removed|deprecat|migrat|release|hotfix|changelog|version" /home/rookslog/workspace/projects/gsd-2-explore`
- `find /home/rookslog/workspace/projects/gsd-2-explore/.github -maxdepth 4 -type f | sort`
- `find /home/rookslog/workspace/projects/gsd-2-explore -maxdepth 5 -type f | rg "(release|hotfix|changelog|version|bump|breaking|deprecat|migrat)" | sort`

If the clone is shallow or tags/history are incomplete, do not deepen it yourself unless explicitly authorized by the orchestrator. Record the limitation and treat history-derived findings as lower-bound observations.

### Phase B: Claim pre-check

After the source/history preflight, read only the relevant current artifacts:

- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md`
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections that discuss release cadence, breaking-change posture, and machinery-vs-practice

Pre-check simple claims mechanically where possible. For pattern claims, nominate them for high adjudication.

## Claims To Watch For

Watch especially for claims like:

- release cadence is rapid in the visible history window
- the visible history window is shallow-clone-bounded
- formal breaking-change machinery exists
- observed commits/changelog entries do not use `BREAKING CHANGE` markers
- recent removals appear without visible pre-deprecation in the inspected window
- release workflow templates are agent-prompted while actual project release scripts run elsewhere
- docs/source/practice divergence is a recurring pattern rather than isolated examples

These are examples, not a closed checklist.

## Required Output

Write the output file with this structure:

```markdown
---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 03 release-practice
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 03 — Release / Practice

## 0. Scout Summary

<5-10 bullets: history availability, machinery/practice surfaces found, obvious confirmations/refutations, and what needs high adjudication.>

## 1. Commands Run

<List commands run and short result summaries. Include history-depth caveats.>

## 2. History Depth / Tag Caveats

<State whether clone is shallow, whether tags appear available, and what this means for cadence claims.>

## 3. Machinery Evidence

<Source/docs evidence for formal release, changelog, deprecation, migration, or breaking-change machinery. Mark source-derived vs docs/template-derived.>

## 4. Practice Evidence

<Commit/tag/changelog observations. Keep bounded to inspected window.>

## 5. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source/history evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|

## 6. Claims Needing High Adjudication

<6-10 candidate claims at most. For each: why it is load-bearing, source/history paths to inspect, and what makes it non-mechanical.>

## 7. Scope Boundaries

<What you deliberately did not inspect.>

## 8. Scout Caveat

This is a medium-reasoning source/history scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2` release practice.
```

## Quality Bar

- Cite source files and lines for source-backed claims.
- Report exact history-depth limitations.
- Do not overgeneralize from shallow history.
- Do not infer stable culture from one command sample.
- Do not treat release templates as proof of actual release practice without history evidence.
