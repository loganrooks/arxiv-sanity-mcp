---
type: wave-2-adjudicator-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: high
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-01-topology-runtime.md
domain: topology-runtime
---

# Wave 2 Adjudicator 01 Spec — Topology / Runtime

## Role

You are a high-reasoning claim adjudicator. Your job is to adjudicate selected topology/runtime claims against source and audit artifacts.

You are not doing a full constructive remap of `gsd-2`. You are deciding whether specific claims survive, survive with qualification, are unsupported, are wrong, or are not decidable from inspected evidence.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Expected source state:

- `main...origin/main`
- current known commit: `bf1d8aad0`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-01-topology-runtime.md`

## Required Reads

Read:

- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-1-DISPOSITION.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md`
- `.planning/gsd-2-uplift/exploration/02-architecture-output.md`
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections concerning Pi vendoring, clean seams, topology/runtime, MCP/RPC/headless, RTK, and docs/source divergence.

You may inspect nearby original slice/audit context as needed, but do not expand into release-practice or extension/workflow adjudication except where directly relevant to topology/runtime boundaries.

## Claims To Adjudicate

Adjudicate these claim families:

1. **Vendored modified Pi fork: correct phrasing and boundaries.**
   - Is "vendored modified Pi fork" accurate?
   - Does that phrase overcollapse layers that should remain separate?
   - What is source-backed vs ADR-derived?

2. **ADR-010 clean seam: proposed-not-implemented, plus partial seams.**
   - Is ADR-010 proposed-not-implemented?
   - Are `gsd-agent-core` / `gsd-agent-modes` absent?
   - Are there partial/informal seams that materially qualify "no clean seam"?

3. **MCP/RPC/headless topology.**
   - Are in-process MCP, standalone MCP package, RPC mode/client, headless, daemon, and `auto` routing correctly distinguished?
   - Does the current synthesis conflate any of them?
   - Incorporate the freshness addendum about TTY-gated `gsd auto` behavior.

4. **RTK docs/source divergence.**
   - Is this a true docs/source divergence, or a provisioning-vs-activation distinction?
   - What exact claim should downstream synthesis be allowed to make?

5. **Headless exit-code docs/source mismatch.**
   - Is the candidate mismatch real?
   - If real, is it material for gsd-2-uplift codebase-understanding claims?

6. **Peripheral vs relevant runtime surfaces.**
   - Are `daemon`, `web`, `studio`, and VS Code extension merely peripheral, or should current synthesis/topology claims qualify their omission?
   - Keep this bounded: do not map these packages fully.

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
adjudicator: topology-runtime
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 01 — Topology / Runtime

## 0. Adjudication Summary

<Short severity-stratified summary. State whether current Claude investigation remains usable for this domain.>

## 1. Claim Verdict Table

| Claim family | Verdict | Severity | Confidence | One-line reason |
|---|---|---|---|---|

## 2. Detailed Adjudication

### 2.1 <Claim family name>

- Claim under audit:
- Current artifact evidence:
- Source evidence inspected:
- Reasoning:
- Verdict:
- Severity:
- Confidence:
- Downstream correction or qualification:

## 3. Cross-Domain Flags

<Anything Wave 2 extension/workflow or release/practice adjudicators should know, without adjudicating their domains.>

## 4. Limits

<What you did not inspect; any unresolved evidence needs.>

## 5. Recommendation For Gate 2

One of:

- no material challenge in this domain
- localized qualifications needed
- material domain issue
- structural unreliability signal
```

## Quality Bar

- Cite source files and lines for source-backed claims.
- Cite audit artifacts by path and line when using scout/synthesis claims.
- Preserve the source freshness addendum.
- Do not infer full codebase architecture from README alone.
- Do not construct a new full architecture map.
