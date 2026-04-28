---
type: audit-spec-review
date: 2026-04-28
reviewer: GPT-5.5 xhigh
target: ./AUDIT-SPEC.md
status: complete
disposition: revise-before-dispatch
---

# AUDIT-SPEC.md Review

## Summary

The audit spec is aimed at the right failure mode: a bounded framing/register audit before Logan adjudicates `SYNTHESIS-COMPARISON.md` §2.1 and §5. It correctly distinguishes source/codebase-understanding from premise bleed, and it preserves Logan as disposition authority.

I would not dispatch it exactly as written. The core framing is sound, but several spec-level choices risk reproducing the same shared premise it is meant to detect.

## Findings

### 1. Material: Same-vendor baseline is risky for this exact audit

`AUDIT-SPEC.md` recommends a same-vendor adversarial-auditor as the baseline because the audit is register-shaped (`AUDIT-SPEC.md:83-97`). That would be persuasive for a generic register audit, but here the suspected failure is a **Claude + Logan shared-frame** failure: v1-GSD mental model bleeding into the initiative's premise.

The comparison artifact already observed that the paired-review asymmetry was mixed, not cleanly "same-vendor catches register / cross-vendor catches substance." It specifically notes that cross-vendor surfaced the framing-leakage caveat, while same-vendor preserved some context-anchored discipline but also missed that caveat (`SYNTHESIS-COMPARISON.md:242-250`).

Recommendation: switch the baseline to cross-vendor high, or define a two-step shape:

- same-vendor register scan to generate candidate findings;
- cross-vendor adjudication of Class B/C findings before comparison revision.

If only one auditor is used, cross-vendor is the safer default for this premise-bleed question.

### 2. Material: Excluding slice outputs prevents propagation proof

The spec excludes the five W1 slice outputs and W2 audits from scope (`AUDIT-SPEC.md:123-127`). That keeps the job bounded, but it weakens the audit's ability to answer its own propagation question.

The spec asks whether early framing propagated through slice prompts into synthesis/comparison (`AUDIT-SPEC.md:147-153`). To test propagation, the auditor needs at least targeted access to output sections where a prompt-level premise might have shaped what was found or omitted.

Recommendation: keep outputs out of full-read scope, but add a targeted sampling rule:

- if a prompt or framing artifact has a possible Class B/C premise-bleed instance, inspect the corresponding slice-output section to determine whether the premise actually propagated;
- cite the sampled output lines;
- do not re-audit the whole slice.

This preserves boundedness while making the propagation claim auditable.

### 3. Material: The lens is too vocabulary-weighted; add a negative-space check

The lens is strong on explicit v1-GSD vocabulary: patcher, skills, workflow markdown, hooks, command wrappers (`AUDIT-SPEC.md:72-80`, `AUDIT-SPEC.md:135-146`). But Logan's concern includes what was **not** said or challenged. Premise bleed may appear as absent first-class questions rather than visible bad vocabulary.

Example: an artifact might never say "patcher" or "skills bundle," but still under-weight session control, headless/RPC/MCP, runtime state, or effective-state emission as primary intervention surfaces.

Recommendation: add a required "negative-space check":

- Which runtime/application intervention surfaces are absent or late despite being source-central?
- Does the artifact's question order make skills/workflow markdown easy to see and runtime/application surfaces harder to see?
- Does the artifact treat R4 as an add-on despite headless/RPC/MCP being first-class GSD-2 surfaces?

Without this, the audit may under-detect premise bleed that operates through omission.

### 4. Material: The corrected-frame section imports imprecise replacement vocabulary

The spec's corrected-frame section is directionally right, but it introduces a few sloppy shorthands (`AUDIT-SPEC.md:61-70`):

- `--mode headless` should be `gsd headless`; `--mode rpc` and `--mode mcp` are the mode surfaces.
- "gsd-2 is a vendored modified Pi fork" should be bounded to the prior audit's phrasing: GSD-2 is a GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled, but the whole repo is broader than that fork.
- "core GSD is itself a Pi extension" should be stated as a source-backed architecture claim, not as an all-purpose shortcut for third-party extension viability.

Because this audit is about vocabulary precision, the spec should not replace one over-compressed mental model with another.

### 5. Moderate: Disposition authority and recommendation language conflict

The spec says disposition recommendations are out of scope and Logan disposes (`AUDIT-SPEC.md:81`). But the output template asks the auditor for a "Recommendation shape" choosing commit-as-is / commit-with-addendum / revise-before-commit (`AUDIT-SPEC.md:176-185`). It also says no revision suggestions (`AUDIT-SPEC.md:216-220`).

This is fixable, but it should be cleaned before dispatch.

Recommendation: rename "Recommendation shape" to "Non-binding disposition signal" and require the auditor to state why Logan might choose each plausible disposition. Keep actual disposition in `DISPOSITION.md` as the spec already says (`AUDIT-SPEC.md:241-250`).

### 6. Moderate: The no-source-reading rule needs an allowed grounding substitute

The spec says no gsd-2 source reading (`AUDIT-SPEC.md:154-160`) because this is not a substance audit. That is reasonable. But the corrected-frame lens rests on source-grounded claims, and the auditor needs a stable authority surface for those claims.

Recommendation: explicitly allow reading the prior codebase-understanding audit's final meta-synthesis and gate dispositions as grounding for corrected-frame facts, without reopening source. This prevents the auditor from treating `AUDIT-SPEC.md` itself as the sole authority for what GSD-2 is.

Suggested allowed inputs:

- `audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md`
- `audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-2-DISPOSITION.md`
- the relevant Wave 2 adjudication sections if a Class B/C finding depends on surface taxonomy.

### 7. Minor: Cost estimate is optimistic without an explicit read budget

The spec estimates 30-60 minutes for six primary artifacts plus two secondary artifact groups (`AUDIT-SPEC.md:267-274`). That is plausible only if the auditor is sampling, not full-reading.

Recommendation: add a read budget:

- full read: `INITIATIVE.md`, `SYNTHESIS-COMPARISON.md` §0/§2/§5/§6, `SYNTHESIS-CROSS.md` §0/§5/§6;
- targeted read: `DECISION-SPACE.md`, `SYNTHESIS.md`, `framing-widening.md`;
- scan only: orchestration preamble, slice prompts, synthesis/audit specs, unless a possible Class B/C chain is found.

## What Is Strong

The spec has several good controls:

- It correctly states that this is not a codebase re-audit (`AUDIT-SPEC.md:22-26`).
- It makes the v1-GSD vs corrected-GSD-2 lens explicit (`AUDIT-SPEC.md:51-80`).
- It distinguishes Class A/B/C severity in a way that maps to practical next steps (`AUDIT-SPEC.md:222-239`).
- It requires one bounded findings artifact and a separate disposition artifact (`AUDIT-SPEC.md:162-214`, `AUDIT-SPEC.md:241-250`).
- It keeps revision work out of the auditor's hands, which preserves the audit/disposition boundary (`AUDIT-SPEC.md:216-220`).

## Recommended Revision Before Dispatch

Revise the spec before launching the auditor:

1. Change baseline auditor to cross-vendor high, or add cross-vendor adjudication of any Class B/C same-vendor findings.
2. Add targeted slice-output sampling for propagation checks.
3. Add a negative-space check for omitted runtime/application surfaces.
4. Correct `gsd headless` / `--mode rpc` / `--mode mcp` and bound the Pi-fork shorthand.
5. Rename "Recommendation shape" to "Non-binding disposition signal."
6. Allow prior codebase-understanding audit outputs as corrected-frame grounding.
7. Add an explicit read budget so the job remains bounded.

With those revisions, the audit is well-justified and should run before Logan adjudicates `SYNTHESIS-COMPARISON.md` §2.1 and §5.

---

Signed: GPT-5.5 xhighm
