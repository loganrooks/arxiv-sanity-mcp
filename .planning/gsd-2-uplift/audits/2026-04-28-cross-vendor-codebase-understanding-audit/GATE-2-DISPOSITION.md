---
type: gate-disposition
date: 2026-04-28
gate: 2
audit: 2026-04-28-cross-vendor-codebase-understanding-audit
decision: localized-qualifications
status: complete
---

# Gate 2 Disposition — Localized Qualifications

## 1. Decision

Classify Wave 2 result as **localized qualifications needed**.

Do not trigger constructive remap from Wave 2 alone. Do proceed to Wave 3 high meta-synthesis.

The current Claude-led investigation remains usable as an input, but not as an unqualified source of truth. Meta-synthesis should preserve the adjudicators' boundary corrections and decide how much these qualifications change trust in the original investigation.

## 2. Basis

All three Wave 2 adjudicators returned the same Gate 2 recommendation:

- Topology/runtime: `localized qualifications needed` (`wave-2/wave-2-adjudication-01-topology-runtime.md:112-114`).
- Extension/workflow: `localized qualifications needed` (`wave-2/wave-2-adjudication-02-extension-workflow.md:125-127`).
- Release/practice: `localized qualifications needed` (`wave-2/wave-2-adjudication-03-release-practice.md:132-134`).

No adjudicator reported a blocker, structural unreliability signal, or immediate constructive-remap trigger.

## 3. Domain Findings

### 3.1 Topology/runtime

Verdict: usable with localized qualifications.

The topology/runtime adjudicator found that the major source-backed claims survive: Pi packages are vendored and modified, ADR-010's clean seam is proposed-not-implemented, MCP/RPC/headless are distinct surfaces, and RTK/headless docs have real source tensions (`wave-2/wave-2-adjudication-01-topology-runtime.md:11-15`).

The main correction is boundary discipline: "vendored modified Pi fork" is acceptable only if it does not erase the root GSD CLI/glue layer, bundled GSD extension layer, standalone MCP/RPC packages, web/VS Code/daemon surfaces, and partial informal seams (`wave-2/wave-2-adjudication-01-topology-runtime.md:13-15`, `wave-2/wave-2-adjudication-01-topology-runtime.md:21-26`).

Carry-forward qualifications:

- Use "GSD CLI/application layer built around vendored, modified Pi-derived packages" rather than treating the whole repo as only a Pi fork (`wave-2/wave-2-adjudication-01-topology-runtime.md:36-40`).
- Preserve that ADR-010's package seam is absent, while informal runtime/extension seams exist (`wave-2/wave-2-adjudication-01-topology-runtime.md:47-51`).
- Keep in-process MCP, standalone MCP, RPC/headless, and TTY-gated `gsd auto` distinct (`wave-2/wave-2-adjudication-01-topology-runtime.md:58-62`).
- Treat RTK as a provisioning-vs-activation ambiguity rather than a flat docs/source contradiction (`wave-2/wave-2-adjudication-01-topology-runtime.md:69-73`).
- Treat web, VS Code, and daemon as additional runtime/integration surfaces; studio appears prototype-level from inspected evidence (`wave-2/wave-2-adjudication-01-topology-runtime.md:91-95`).

### 3.2 Extension/workflow

Verdict: usable with localized qualifications.

The extension/workflow adjudicator found that source supports plural extension-adjacent mechanisms, distinct workflow modes, and material trust boundaries. It does not support treating every mechanism as the same kind of "extension surface" or treating workflow-plugin viability as one uniform R2 claim (`wave-2/wave-2-adjudication-02-extension-workflow.md:11-17`).

Carry-forward qualifications:

- "Extension surface" must be a typed umbrella, not a silent semantic merger (`wave-2/wave-2-adjudication-02-extension-workflow.md:13-17`, `wave-2/wave-2-adjudication-02-extension-workflow.md:23-29`).
- Pi coding-agent extensions and GSD ecosystem extensions are source-distinct, but GSD ecosystem extensions wrap/delegate to the Pi API while adding GSD-specific timing/state (`wave-2/wave-2-adjudication-02-extension-workflow.md:24`, `wave-2/wave-2-adjudication-02-extension-workflow.md:50-53`).
- Workflow plugins, skills, hooks/rules, workflow MCP tools, and plugin importer should not be collapsed into one family (`wave-2/wave-2-adjudication-02-extension-workflow.md:25`, `wave-2/wave-2-adjudication-02-extension-workflow.md:61-64`).
- `markdown-phase` survives as prompt-dispatch with startup scaffolding, not executor-owned deterministic shell execution (`wave-2/wave-2-adjudication-02-extension-workflow.md:69-75`).
- `yaml-step` determinism applies to graph/control/verification layers, not prompt-authored step content (`wave-2/wave-2-adjudication-02-extension-workflow.md:83-86`).
- Trust/security exists across multiple layers and should not be presented as one uniform security model (`wave-2/wave-2-adjudication-02-extension-workflow.md:94-97`).

### 3.3 Release/practice

Verdict: usable with localized qualifications.

The release/practice adjudicator found that the main synthesis pattern survives: gsd-2 has substantial release and breaking-change machinery, while inspected practice evidence shows release communication often happening through changelog narrative and ordinary commit categories rather than formal `BREAKING CHANGE` markers. The key correction is scope: this is a shallow-history-bounded visible-window finding, not a complete-history or culture-level claim (`wave-2/wave-2-adjudication-03-release-practice.md:11-15`).

Carry-forward qualifications:

- Machinery/practice divergence is source-supported in the visible window, but stable-pattern vs transition-state remains unresolved (`wave-2/wave-2-adjudication-03-release-practice.md:21`).
- OAuth and `/gsd map-codebase` examples support "no visible local pre-deprecation found," not "no meaningful deprecation existed anywhere" (`wave-2/wave-2-adjudication-03-release-practice.md:22`, `wave-2/wave-2-adjudication-03-release-practice.md:48-51`).
- Absence of breaking markers is real in inspected local history, but enforcement/culture conclusions need PR, CI, and release-body evidence (`wave-2/wave-2-adjudication-03-release-practice.md:23`, `wave-2/wave-2-adjudication-03-release-practice.md:59-62`).
- Rapid cadence is visible; fork/extension maintenance risk requires surface-churn and diff sampling (`wave-2/wave-2-adjudication-03-release-practice.md:24`, `wave-2/wave-2-adjudication-03-release-practice.md:70-73`).
- Release/hotfix/API-breaking templates are product capability and doctrine evidence, not proof of actual gsd-2 maintainer release practice (`wave-2/wave-2-adjudication-03-release-practice.md:25`, `wave-2/wave-2-adjudication-03-release-practice.md:81-84`).
- Experimental deprecation waiver is source-real, but relevance depends on whether uplift relies on experimental-gated surfaces (`wave-2/wave-2-adjudication-03-release-practice.md:27`, `wave-2/wave-2-adjudication-03-release-practice.md:103-106`).

## 4. Why Not Constructive Remap

Constructive remap is not triggered because Wave 2 did not find multiple wrong or unsupported load-bearing synthesis claims across domains.

Instead, the adjudicators repeatedly found:

- claims generally survive,
- claims often survive only with qualification,
- stronger cultural, strategic, or stability readings require more evidence,
- mechanism existence should not be converted into strategic viability without typed boundaries.

This means the current investigation should be corrected and bounded, not discarded.

## 5. Wave 3 Instructions

Wave 3 meta-synthesis should answer:

1. Does the Claude-led investigation remain usable overall?
2. Which original synthesis claims survive cleanly?
3. Which claims survive only with Wave 2 qualifications?
4. Did any qualification materially change the trust level of the original synthesis?
5. Do the qualifications change the incubation checkpoint's decision posture?
6. Is any follow-up evidence needed before incubation?
7. Is constructive remap unnecessary, conditionally deferred, or now triggered?

Wave 3 must preserve:

- topology/runtime boundary discipline,
- typed extension-surface vocabulary,
- markdown-phase vs yaml-step determinism limits,
- shallow-history bounds on release/practice claims,
- distinction between mechanism existence and R-strategy viability.

## 6. Next Step

Write a Wave 3 meta-synthesis spec in `wave-3/`, then dispatch one high-reasoning meta-synthesis agent.
