---
type: wave-2-adjudicator-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: high
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-03-release-practice.md
domain: release-practice
---

# Wave 2 Adjudicator 03 Spec — Release / Practice

## Role

You are a high-reasoning claim adjudicator. Your job is to adjudicate selected release/practice claims against source, local history, and audit artifacts.

Preserve the shallow-history caveat. Do not silently convert local visible-history evidence into complete-history or culture-level claims.

You are not doing a full constructive remap of `gsd-2` release practice.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Expected source state:

- `main...origin/main`
- current known commit: `bf1d8aad0`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-03-release-practice.md`

## Required Reads

Read:

- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-1-DISPOSITION.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-03-release-practice.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md`
- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md`
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections concerning release cadence, breaking-change posture, machinery-vs-practice, and release/workflow interleaving.

You may inspect source scripts, workflows, changelog, local git history, and local tags. If you need network GitHub PR/release evidence or history deepening to decide a claim, do not silently assume it. Mark the claim not decidable from inspected evidence or state the scoped escalation needed.

## Claims To Adjudicate

Adjudicate these claim families:

1. **Machinery-vs-practice: stable pattern vs transition state.**
   - Does inspected evidence support "machinery exists but practice diverges"?
   - Does it support a stable pattern, or only a visible-window observation?

2. **Visible removals and meaningful deprecation.**
   - Do the OAuth and `/gsd map-codebase` examples support the current synthesis's claim?
   - What can and cannot be concluded without PR/release-body evidence?

3. **Absent `BREAKING CHANGE` markers and convention-enforcement gap.**
   - Does absence of markers in inspected local history show a gap, or only no marker usage in that window?
   - How should the release generator/conventional-commit machinery affect interpretation?

4. **Rapid cadence and maintenance risk.**
   - Does rapid visible cadence materially increase fork/extension maintenance risk?
   - What additional evidence would be needed to move from cadence to risk?

5. **Bundled release/hotfix/API-breaking templates vs actual project practice.**
   - Do templates reflect project practice, product capability, or both?
   - Does current synthesis overstate interleaving by conflating templates with the repo's own release process?

6. **Release mechanics and product workflow interleaving.**
   - Is the "release mechanics and product workflow are tightly interleaved" claim source-supported?
   - Does it matter for uplift design, or is it only an architectural observation?

7. **Experimental deprecation waiver relevance.**
   - Is the waiver source-real?
   - Does it affect surfaces likely relevant to uplift, or is that not decidable yet?

## Required Verdict Labels

For each claim family, use one:

- **Survives**
- **Survives with qualification**
- **Unsupported**
- **Wrong**
- **Not decidable from inspected evidence**

Also provide:

- severity for downstream gsd-2-uplift decisions: low / medium / high
- confidence: low / medium-low / medium / medium-high / high

## Output Structure

Write the target file with this structure:

```markdown
---
type: wave-2-adjudication
date: 2026-04-28
adjudicator: release-practice
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 03 — Release / Practice

## 0. Adjudication Summary

<Short severity-stratified summary. State whether current Claude investigation remains usable for this domain.>

## 1. Claim Verdict Table

| Claim family | Verdict | Severity | Confidence | One-line reason |
|---|---|---|---|---|

## 2. Detailed Adjudication

### 2.1 <Claim family name>

- Claim under audit:
- Current artifact evidence:
- Source/history evidence inspected:
- Reasoning:
- Verdict:
- Severity:
- Confidence:
- Downstream correction or qualification:

## 3. Evidence Needed But Not Gathered

<Network evidence, PR bodies, GitHub Release bodies, Actions logs, or history deepening needed for stronger claims.>

## 4. Cross-Domain Flags

<Anything Wave 2 topology/runtime or extension/workflow adjudicators should know, without adjudicating their domains.>

## 5. Limits

<What you did not inspect; preserve shallow-history caveat.>

## 6. Recommendation For Gate 2

One of:

- no material challenge in this domain
- localized qualifications needed
- material domain issue
- structural unreliability signal
```

## Quality Bar

- Cite source files and lines for source-backed claims.
- Cite local history commands/results when using history evidence.
- Cite audit artifacts by path and line when using scout/synthesis claims.
- Preserve shallow-history limits.
- Do not infer stable culture from local visible history alone.
- Do not treat workflow templates as proof of actual maintainer practice unless evidence connects them.
