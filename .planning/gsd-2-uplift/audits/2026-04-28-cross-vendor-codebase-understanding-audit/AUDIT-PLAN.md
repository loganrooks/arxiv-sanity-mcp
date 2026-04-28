---
type: cross-vendor-audit-plan
date: 2026-04-28
status: draft-for-disposition
target: gsd-2-uplift first-wave investigation and audits
scope: test whether the existing Claude-led investigation understood the gsd-2 codebase well enough to support downstream incubation decisions
location: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/
---

# Cross-Vendor Codebase-Understanding Audit Plan

## 1. Purpose

This audit tests whether the existing gsd-2 uplift investigation understood the `gsd-2` codebase well enough for its findings to support downstream incubation and second-wave scoping.

The immediate concern is not whether the current synthesis is plausible. The concern is whether it is source-grounded, complete enough on load-bearing surfaces, and calibrated about the difference between direct codebase evidence, docs-derived claims, and interpretive integration.

Primary audit question:

> Did the Claude-led exploration, audits, and synthesis materially misunderstand, overstate, or under-sample the `gsd-2` codebase in ways that would challenge their findings?

## 2. Audit Posture

This is a challenge audit before it is a constructive remap.

It is easier and cheaper to find load-bearing counterexamples to the current investigation than to construct a complete replacement model of the codebase. A single strong counterexample may be enough to reduce trust in the current synthesis if it lands on a load-bearing claim. A better full codebase model requires broader reconstruction and should be triggered only if the challenge audit shows the current understanding is materially unreliable.

Therefore this audit does not ask one agent to understand all of `gsd-2`. It asks bounded agents to understand specific source surfaces enough to test specific claims.

## 3. Reasoning-Tier Policy

Use reasoning effort based on task type:

- **Medium** for scouting and exploration tasks.
- **High** for load-bearing claim adjudication.
- **High** for final meta-synthesis.
- **No xhigh by default.** Escalate above high only if a later contradiction is both hard to resolve and decision-bearing.

Medium is sufficient for local source discovery and mechanical checks such as file existence, export presence, config gates, changelog markers, and source-path identification.

High is warranted when the task requires architectural judgment, subsystem boundary recognition, absence reasoning, docs/source divergence classification, or deciding whether a failed claim is merely local or structurally undermines the synthesis.

## 4. Existing Inputs Under Audit

Primary artifacts:

- `.planning/gsd-2-uplift/exploration/01-mental-model-output.md`
- `.planning/gsd-2-uplift/exploration/02-architecture-output.md`
- `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md`
- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md`
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md`
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md`
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md`
- `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md`
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md`
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md`

Context artifacts:

- `.planning/gsd-2-uplift/INITIATIVE.md`
- `.planning/gsd-2-uplift/DECISION-SPACE.md`
- `.planning/deliberations/2026-04-28-framing-widening.md`
- `.planning/gsd-2-uplift/orchestration/`

Source target:

- `/home/rookslog/workspace/projects/gsd-2-explore/`

## 5. Wave Structure

### Wave 1: Medium Scout Pass

Purpose: locate relevant source surfaces, pre-check simple claims, and nominate load-bearing claims for high adjudication.

Scouts do not produce broad conclusions about whether Claude understood the codebase. They produce source maps, obvious confirmations/refutations, suspicious omissions, and adjudication candidates.

#### Scout 1: Topology / Runtime

Scope:

- package layout
- CLI and runtime entrypoints
- headless mode
- MCP / RPC surfaces
- vendored Pi relationship
- clean-seam or package-boundary claims

Expected load: moderate. The scout should inspect package manifests, top-level source entrypoints, relevant README headings, and source paths discovered through targeted search. It should not attempt a full package-by-package architecture.

Output:

- `wave-1/wave-1-scout-01-topology-runtime.md`

Required output sections:

- source paths inspected
- simple claims confirmed/refuted
- claims needing high adjudication
- suspected omissions or conflations
- scope boundaries

#### Scout 2: Extension / Workflow

Scope:

- extension loaders and extension APIs
- workflow plugin system
- skills system
- hooks / trust boundaries
- `markdown-phase` vs `yaml-step`
- automation execution mode claims

Expected load: heaviest scout. Cap tightly: identify mechanisms and source paths, but do not fully judge architecture or viability.

Output:

- `wave-1/wave-1-scout-02-extension-workflow.md`

Required output sections:

- mechanism inventory
- source paths per mechanism
- simple claims confirmed/refuted
- possible missing sibling mechanisms
- claims needing high adjudication
- scope boundaries

#### Scout 3: Release / Practice

Scope:

- release scripts
- changelog structure
- tag and commit history checks
- breaking-change markers
- GitHub workflows
- deprecation / migration policy evidence
- shallow-history caveats

Expected load: lighter but command-heavy. The scout should distinguish source-backed release machinery from observed release practice.

Output:

- `wave-1/wave-1-scout-03-release-practice.md`

Required output sections:

- commands run
- history depth / tag caveats
- machinery evidence
- practice evidence
- simple claims confirmed/refuted
- claims needing high adjudication

### Gate 1: Scout Disposition

After Wave 1, the orchestrator reviews scout outputs and chooses one of:

- **Proceed narrow:** only challenged load-bearing claims go to high adjudication.
- **Proceed broad sample:** scouts found complexity or omissions suggesting a wider sample is needed, but not enough to pause.
- **Pause and re-slice:** scouts reveal the current domain split is wrong or a source surface is too large for the planned adjudicators.
- **Trigger constructive remap planning:** scouts find enough structural unreliability that claim-checking alone is insufficient.

The Gate 1 disposition should be recorded in:

- `GATE-1-DISPOSITION.md`

## 6. Wave 2: High Claim-Adjudication Pass

Purpose: adjudicate load-bearing claims against source.

Default shape is three high-reasoning adjudicators aligned to the scout domains. If Gate 1 finds only a small number of issues, Wave 2 may collapse to one high adjudicator. The default preserves domain separation so no agent has to reason across the whole codebase.

Each adjudicator receives the relevant scout output, the current Claude artifacts for that domain, and exact claims selected by the orchestrator after Gate 1.

Each adjudicator should evaluate 6-10 claims unless Gate 1 narrows the set.

Required verdict labels:

- **Survives**
- **Survives with qualification**
- **Unsupported**
- **Wrong**
- **Not decidable from inspected evidence**

Each verdict must include:

- claim under audit
- source evidence inspected
- artifact evidence inspected
- reasoning
- severity for downstream gsd-2-uplift decisions
- confidence

#### Adjudicator A: Topology / Runtime Claims

Candidate claim families:

- `gsd-2` as vendored modified Pi fork
- ADR-010 / clean seam proposed-not-implemented
- package-boundary and runtime-entrypoint understanding
- CLI / headless / MCP / RPC surface claims
- docs/source divergences around runtime activation

Output:

- `wave-2/wave-2-adjudication-01-topology-runtime.md`

#### Adjudicator B: Extension / Workflow Claims

Candidate claim families:

- four extension surfaces or plural extension-surface claim
- pi-coding-agent extensions vs GSD ecosystem extensions
- workflow plugins vs skills vs hooks
- `markdown-phase` prompt-dispatch claim
- `yaml-step` deterministic graph mutation claim
- trust/security boundaries relevant to extension viability

Output:

- `wave-2/wave-2-adjudication-02-extension-workflow.md`

#### Adjudicator C: Release / Practice Claims

Candidate claim families:

- release cadence claims
- breaking-change machinery vs observed practice
- changelog marker absence
- shallow-history limitations
- release workflow template vs actual project release scripts
- whether docs/source/practice divergence is a pattern or a few cases

Output:

- `wave-2/wave-2-adjudication-03-release-practice.md`

### Gate 2: Adjudication Disposition

After Wave 2, the orchestrator classifies the results:

- **No material challenge:** current synthesis remains usable, perhaps with minor addenda.
- **Localized qualifications:** current synthesis usable only with specific corrections.
- **Structural unreliability:** current synthesis cannot support incubation without constructive remap.
- **Contradiction unresolved:** specific contradiction requires a resolver before meta-synthesis can be trusted.

The Gate 2 disposition should be recorded in:

- `GATE-2-DISPOSITION.md`

## 7. Wave 3: High Meta-Synthesis

Purpose: integrate scout and adjudication outputs into an audit conclusion about the Claude-led investigation.

Default shape: one high-reasoning synthesis agent.

The meta-synthesizer should not do broad fresh source exploration. It may inspect source only to resolve small citation ambiguities. Its job is integration.

Inputs:

- all Wave 1 scout reports
- all Wave 2 adjudication reports
- Gate 1 and Gate 2 dispositions
- existing `SYNTHESIS.md`
- relevant original slice outputs and audits

Output:

- `wave-3/META-SYNTHESIS.md`

Required questions:

- Which current synthesis claims survive?
- Which survive only with qualification?
- Which are unsupported or wrong?
- Are failures isolated, domain-local, or structural?
- Did W2 audits catch the material issues, or did they mostly ratify?
- Did the current synthesis distinguish source facts from interpretation cleanly?
- Does incubation need a constructive remap before relying on this investigation?

Conclusion labels:

- **Usable with no material changes**
- **Usable with addenda**
- **Partially unreliable; do not use specified claims**
- **Structurally unreliable; constructive remap required**

## 8. Optional Wave 4: Contradiction Resolver

Only dispatch if Gate 2 or Wave 3 finds material unresolved disagreement.

Purpose: adjudicate specific contradictions, not perform fresh broad audit.

Inputs:

- the contradictory scout/adjudication/meta-synthesis passages
- the exact disputed source files
- the exact disputed claims

Output:

- `wave-4/CONTRADICTION-RESOLUTION.md`

The resolver should answer only:

- what exactly is disputed
- which interpretation is best supported
- what evidence would still be needed
- whether the dispute changes the final meta-synthesis conclusion

## 9. Constructive Remap Trigger

A constructive remap is out of scope for this audit unless triggered.

Trigger it if any of the following hold:

- multiple load-bearing synthesis claims are wrong or unsupported across more than one domain
- scouts find major source surfaces absent from the original slice/audit/synthesis stack
- adjudicators find that the current artifact vocabulary conflates distinct subsystems
- release/practice or workflow/execution evidence materially changes R-strategy viability
- the meta-synthesis concludes that the current synthesis is structurally unreliable

If triggered, create a separate plan rather than expanding this audit silently.

Suggested artifact:

- `CONSTRUCTIVE-REMAP-TRIGGER.md`

## 10. Scale Controls

This audit should avoid becoming a full undocumented rewrite of the first-wave investigation.

Controls:

- scouts are medium-reasoning and non-adjudicative
- each high adjudicator gets a bounded claim list
- high adjudicators should not exceed 10 claims without explicit Gate 1 disposition
- meta-synthesis does not perform broad source exploration
- optional contradiction resolution is claim-specific
- constructive remap requires an explicit trigger artifact

## 11. Audit Quality Requirements

All audit outputs must:

- cite source files and lines when making source-backed claims
- distinguish docs-derived claims from source-derived claims
- state what was deliberately not inspected
- mark confidence on substantive findings
- avoid treating absence of evidence as evidence of absence unless the search scope is explicit and appropriate
- avoid assuming README, changelog, templates, and source are mutually consistent
- avoid converting "we found a challenge" into "we now have a better whole-codebase model"

## 12. Planned Files

Directory:

- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/`

Plan and gate artifacts:

- `AUDIT-PLAN.md`
- `GATE-1-DISPOSITION.md`
- `GATE-2-DISPOSITION.md`
- `CONSTRUCTIVE-REMAP-TRIGGER.md` if needed

Wave 1:

- `wave-1/SCOUT-01-TOPOLOGY-RUNTIME-SPEC.md`
- `wave-1/SCOUT-02-EXTENSION-WORKFLOW-SPEC.md`
- `wave-1/SCOUT-03-RELEASE-PRACTICE-SPEC.md`
- `wave-1/wave-1-scout-01-topology-runtime.md`
- `wave-1/wave-1-scout-02-extension-workflow.md`
- `wave-1/wave-1-scout-03-release-practice.md`

Wave 2:

- `wave-2/wave-2-adjudication-01-topology-runtime.md`
- `wave-2/wave-2-adjudication-02-extension-workflow.md`
- `wave-2/wave-2-adjudication-03-release-practice.md`

Wave 3:

- `wave-3/META-SYNTHESIS.md`

Optional Wave 4:

- `wave-4/CONTRADICTION-RESOLUTION.md`

## 13. Current Disposition

This plan records the audit design only. No scouts, adjudicators, synthesizers, or contradiction resolvers have been launched from this artifact yet.

Next step, if approved: dispatch the three medium Wave 1 scout tasks using the specs in `wave-1/`.
