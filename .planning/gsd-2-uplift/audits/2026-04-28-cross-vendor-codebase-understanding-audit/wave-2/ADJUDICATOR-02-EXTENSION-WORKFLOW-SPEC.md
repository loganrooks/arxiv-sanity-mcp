---
type: wave-2-adjudicator-spec
date: 2026-04-28
status: ready-for-dispatch
reasoning_effort: high
target_output: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-02-extension-workflow.md
domain: extension-workflow
---

# Wave 2 Adjudicator 02 Spec — Extension / Workflow

## Role

You are a high-reasoning claim adjudicator. Your job is to adjudicate selected extension/workflow claims against source and audit artifacts.

This domain has the highest conflation risk. Keep separate:

- mechanism existence
- subsystem identity
- semantic label such as "extension surface"
- downstream R-strategy meaning

You are not doing a full constructive remap of `gsd-2`.

## Source Target

Read-only source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

Expected source state:

- `main...origin/main`
- current known commit: `bf1d8aad0`

Audit-session output target:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-2/wave-2-adjudication-02-extension-workflow.md`

## Required Reads

Read:

- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-1-DISPOSITION.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-02-extension-workflow.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md`
- `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md`
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` sections concerning extension surfaces, workflow engines, skills, hooks, trust/security, and R2/R4 implications.

You may inspect source tests and nearby docs as needed. Do not adjudicate release cadence or full topology except where needed to classify extension/workflow surfaces.

## Claims To Adjudicate

Adjudicate these claim families:

1. **Whether all identified mechanisms should be called extension surfaces.**
   - Pi extensions, GSD ecosystem extensions, workflow plugins, skills, hooks/rules, and provider extensions may all be relevant, but are they all "extension surfaces" in the same sense?

2. **Pi coding-agent extensions vs GSD ecosystem extensions.**
   - Are these actually distinct source mechanisms?
   - Is their relationship wrapper/delegation, parallel subsystem, or something else?

3. **Workflow plugins vs skills vs hooks.**
   - Are these distinct enough that synthesis should avoid treating them as one extension family?
   - Are there missing sibling mechanisms the current synthesis should mention?

4. **`markdown-phase` prompt-dispatch limitations.**
   - Does source support the claim that markdown-phase is prompt-dispatch, not deterministic executor-owned shell execution?
   - How bounded is the absence claim?
   - Does the limitation materially affect current synthesis/R-strategy claims?

5. **`yaml-step` deterministic claims.**
   - Which layers are deterministic: graph mutation, dependency eligibility, verification, shell command execution, prompt content, or something else?
   - Does current synthesis overstate determinism?

6. **Hook/trust/security composition.**
   - Are trust boundaries source-present and material?
   - Do hooks/rules compose with extension/workflow layers in ways that current synthesis missed or overstated?

7. **Claude Code CLI provider/permission behavior as workflow automation surface.**
   - Does fresh `stream-adapter.ts` behavior materially matter to workflow automation or trust claims?
   - Keep this as a domain relevance judgment, not a full provider audit.

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
adjudicator: extension-workflow
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 02 — Extension / Workflow

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

<Anything Wave 2 topology/runtime or release/practice adjudicators should know, without adjudicating their domains.>

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
- Do not equate "surface exists" with "surface is viable for uplift."
- Do not let "extension" become a silent umbrella term.
- Do not construct a full replacement workflow architecture.
