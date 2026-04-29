---
type: premise-bleed-audit-spec
date: 2026-04-28 (initial draft); 2026-04-28 (revised post-cross-vendor-review)
status: revised-for-dispatch (post-cross-vendor-review; awaiting Logan final-call before auditor dispatch)
target: gsd-2-uplift framing artifacts (INITIATIVE.md, DECISION-SPACE.md, SYNTHESIS.md, SYNTHESIS-CROSS.md, SYNTHESIS-COMPARISON.md, framing-widening) + load-bearing slice prompts + targeted slice-output sampling under hard cap
scope: bounded premise-bleed lens audit before §2.1 + §5 incubation adjudication on SYNTHESIS-COMPARISON.md
location: .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/
revision_history: |
  - v1 (2026-04-28 ~11:42): initial draft.
  - v2 (2026-04-28 post-review): revised per cross-vendor (GPT-5.5 xhigh) review at AUDIT-SPEC-REVIEW.md and adjudication trace at .planning/deliberations/2026-04-28-audit-spec-review-deliberation.md §5-§6, distilled to DECISION-SPACE.md §1.17. Material changes: vendor selection (same-vendor → two-step conditional cross-vendor + same-vendor stress on Class C); method (added required negative-space check); scope (slice-output targeted sampling under hard cap; prior-audit grounding inputs allowed; narrow source-reading fallback allowed); lens vocabulary (vetted-replacement language with citations); output (rename "Recommendation shape" → "Non-binding disposition signal" + per-option justification); cost (full/targeted/scan-only read budget + conditional add-ons).
purpose: |
  Logan registered a premise-correction concern at 2026-04-28: he had been thinking
  of gsd-2 much more like original GSD (intervention surface made of workflow markdown,
  skills, hooks, command wrappers, host-runtime conventions inside Codex/Claude Code),
  but now understands gsd-2 is much more materially a standalone agent application/
  runtime built around Pi, with its own session control, headless/RPC/MCP surfaces,
  extension systems, workflow engines, state machinery, and release/runtime complexity.

  This audit checks whether that older v1-GSD mental model shaped the gsd-2-uplift
  initiative's framing in ways that — if uncorrected — would distort §2.1 + §5
  incubation dispositions. Specifically: over-weighting skills/workflow-markdown/
  patcher language; under-weighting runtime/application-level intervention surfaces
  (headless/RPC/MCP/Pi-session/state-control).

  This is **not** a re-audit of the codebase-understanding (that work was already
  done at `audits/2026-04-28-cross-vendor-codebase-understanding-audit/`). The
  question here is register/framing, not substance: did the artifacts inherit a
  v1-GSD-shaped vocabulary that made some surfaces visible and others less visible?
related_audit: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/ (substance-checked the codebase-understanding; outputs serve as primary grounding for this audit per §4 scope)
methodology_ground: METHODOLOGY.md M1 (paired-review register-vs-substance asymmetry — empirically more complex per SYNTHESIS-COMPARISON.md §4.1); LONG-ARC.md anti-patterns (closure pressure; framing-leakage); framing-widening §3.3 disposition-discipline; SYNTHESIS-COMPARISON.md §4.4 (framing-import drift surfaced as initiative-maturity signal)
decision_reference: .planning/gsd-2-uplift/DECISION-SPACE.md §1.17 (load-bearing audit-methodology decision; this spec implements §1.17)
deliberation_log: .planning/deliberations/2026-04-28-audit-spec-review-deliberation.md (full review-and-response trace)
---

# v1-GSD Mental-Model Premise-Bleed Audit Spec (revised)

## §0. Read-guidance

This document is the **revised spec** for an audit awaiting dispatch. v1 was reviewed at AUDIT-SPEC-REVIEW.md; this v2 implements the adjudications recorded at the deliberation log §5 + §6 and DECISION-SPACE.md §1.17.

**For "what the audit asks"**: §2 lens definition; §4 specific surfaces.
**For "how the auditor should work"**: §5 method (per-step + negative-space + grounding-input usage); §6 output shape.
**For "why this audit, not codebase re-audit"**: §1 motivation.
**For "what changed from v1"**: frontmatter `revision_history` + this section.
**For "what changes if Logan revises"**: §9 conditional structure.
**For "what was the deliberation that produced these decisions"**: deliberation log + DECISION-SPACE.md §1.17.

## §1. Why this audit (not the codebase-understanding audit)

The earlier `2026-04-28-cross-vendor-codebase-understanding-audit/` tested whether the Claude-led investigation **understood the gsd-2 codebase** well enough — substance audit. Its target was claim-grounding, source-verifiability, surface-coverage.

This audit tests something orthogonal: whether the **framing vocabulary** Logan and Claude carried into the initiative shaped what the artifacts looked at and how they articulated findings. The substance can be source-grounded **and** the framing can still under-weight load-bearing surfaces because those surfaces never made it into the question-set.

**Concrete signal that motivates this audit** (from SYNTHESIS-COMPARISON.md §4.4 + Logan's 2026-04-28 message): INITIATIVE.md §3.2 explicitly names candidate design-shapes as "**Patcher / Skills / Hybrid**." That's v1-GSD vocabulary — it presupposes gsd-2 is a thin layer one applies a patcher or skills-bundle to, not a standalone runtime/application with headless/RPC/MCP/Pi-session surfaces as primary intervention candidates. If that vocabulary propagated through the slice prompts → slice outputs → audits → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON, the §2.1 R-mix and §5 R-strategy axes may carry under-weighting that the current paired-review didn't catch (because both syntheses share the dispatching-project's framing-widening vocabulary per cross-vendor's framing-leakage caveat at SYNTHESIS-CROSS §6).

**The audit's job is not to revise the framing.** It is to surface where premise-bleed appears, classify each appearance by load-bearing-ness for §2.1 + §5 dispositions, and produce a non-binding disposition signal (per §6); Logan disposes (per §8).

## §2. The lens

### §2.1 v1-GSD mental model (the prior frame)

GSD as intervention surface made of:
- Workflow markdown templates inside a host runtime (Codex, Claude Code).
- Skills (Claude Code skill manifests; per-unit allowlists).
- Hooks (host-runtime hooks; lifecycle integrations).
- Command wrappers (slash-commands; markdown command bodies as agent instructions).
- Host-runtime conventions (project-local config; trust gates layered on host runtime).
- Patcher tooling (modify-existing-installation pattern).

### §2.2 gsd-2 as it actually is (the corrected frame) — vetted-replacement vocabulary with citations

A standalone agent application/runtime, distinct from the host runtime. The auditor should treat the following as the corrected-frame vocabulary; citations point to grounding (per §4.2 grounding inputs). Where citations point to prior-audit outputs, the auditor consults those primary; falls back to source-reading per §4.2 only when prior-audit doesn't ground a specific claim.

**Key surfaces.**

- **Session control.** gsd-2 owns session lifecycle, not the host runtime. Source/grounding: META-SYNTHESIS or slice-2 architecture audit (auditor verifies path).
- **Headless surfaces.** `gsd headless` (subcommand-shaped, NOT `--mode headless`). Query subcommands; JSON/JSONL output. Cite slice-3 workflow-surface output + capabilities probe §A.4 / §A.8 for actual command shapes.
- **RPC surfaces.** RPC client; out-of-process control. The mode surfaces are `--mode rpc` (and `--mode mcp` for MCP server); `--mode` parameter applies to mode-shaped invocations specifically, not blanketly.
- **MCP surfaces.** In-process MCP via `--mode mcp`; standalone `@gsd-build/mcp-server` package.
- **Pi vendoring + Pi-extension API.** GSD-2 is a GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled per ADR-010, but the whole repo is broader than that fork. Avoid the over-compressed "gsd-2 is a vendored modified Pi fork" shorthand. Source: SYNTHESIS.md F1 + slice-2 architecture audit + ADR-010 (Status: Proposed).
- **State machinery.** `STATE.json`; `GRAPH.yaml`; daily-rotated journal with ~22 schema versions; metrics ledger; cost/budget controls. Source: SYNTHESIS.md F8 + slice-4 lifecycle output.
- **Workflow engines.** Two architecturally distinct: markdown-phase (prompt-dispatch) + yaml-step (deterministic graph-backed). Not just templates. Source: SYNTHESIS.md F4 + slice-3 + W2 markdown-phase dive.
- **Release/runtime complexity.** Semver detection; release templates; `generate-changelog.mjs`; `bump-version.mjs`; native modules; Rust components. Source: SYNTHESIS.md F3 + slice-5.
- **Extension systems.** Four parallel subsystems: pi-coding-agent extensions; GSD ecosystem extensions; workflow plugins; skills. Skills is *one of four*, not the primary surface. Source: SYNTHESIS.md F2 + slice-4 audit §2 CG-1 + (vi) addendum.
- **Architectural use of extension machinery.** Core GSD itself uses Pi extension machinery (source-backed claim per slice-4 audit §5 + SYNTHESIS.md F6); this is an architecture observation, not an all-purpose shortcut for third-party extension viability. The use-claim should remain qualified to its source-grounded scope.

### §2.3 Replacement vocabulary lookup

When the auditor encounters a v1-GSD-shaped phrasing in the audited artifacts and needs to articulate the corrected frame, the lookup table:

| If artifact says (or implies) | Replacement framing | Source-of-grounding |
|---|---|---|
| "patcher / skills / hybrid" as candidate intervention shapes; OR bare "extension surface" without typing | Per META-SYNTHESIS §2 item 3 typed vocabulary (canonical): "code extension API, GSD ecosystem extension, workflow plugin, skill/instruction resource, hook/rule interception layer, provider integration, and workflow MCP/machine surface where applicable." Mechanism existence does not itself decide R2/R4/R5 meaning; surface selection is typed before R-strategy assignment. | META-SYNTHESIS §2 item 3 (`wave-3/META-SYNTHESIS.md:38`); SYNTHESIS.md F2; slice-4 audit §2 |
| "harness as thin layer" | gsd-2 is a standalone application/runtime; "harness" framing per INITIATIVE.md §1 includes gsd-2 + host runtime + dev tooling, but gsd-2 carries first-class runtime surfaces | INITIATIVE.md §1 + SYNTHESIS.md F7 |
| "vendored modified Pi fork" (as whole-repo topology) | Per META-SYNTHESIS §2 item 1: "gsd-2 is a GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled, but the whole repo is broader than that fork." | META-SYNTHESIS §2 item 1 (`wave-3/META-SYNTHESIS.md:36`); SYNTHESIS.md F1 |
| "core GSD is itself a Pi extension" (as standalone claim) | "core GSD uses Pi extension machinery" (qualified architecture observation; not all-purpose shortcut for R2 viability) | slice-4 audit §5 + SYNTHESIS.md F6 |
| `--mode headless` | `gsd headless` (headless subcommand). Mode parameter surfaces are `--mode rpc` and `--mode mcp` per META-SYNTHESIS §2 item 2 carry-forward labels. | META-SYNTHESIS §2 item 2 (`wave-3/META-SYNTHESIS.md:37`); slice-3 workflow-surface; capabilities probe §A.4 |
| Skills framed as primary intervention surface | Skills is one of seven typed surfaces per META-SYNTHESIS §2 item 3 (above row). | META-SYNTHESIS §2 item 3 (`wave-3/META-SYNTHESIS.md:38`); SYNTHESIS.md F2 |

The auditor uses this lookup to stabilize corrected-frame articulation; verifies citations against prior-audit grounding (§4.2) or narrow source-reading fallback when needed.

**META-SYNTHESIS §3 prohibited articulations — complementary discipline reference.** META-SYNTHESIS §3 ("What Fails Or Is Unsupported") at `wave-3/META-SYNTHESIS.md:47-59` lists seven prohibited articulations the auditor consults alongside this lookup:
- Do not use "gsd-2 is a Pi fork" as whole-repo topology.
- Do not claim there are no seams of any kind (correct claim: ADR-010's clean package seam is absent; informal seams exist).
- Do not treat all extension-adjacent mechanisms as same-kind extension surfaces or as one security/trust model.
- Do not claim `markdown-phase` owns deterministic shell execution or programmatic phase advancement from inspected evidence.
- Do not upgrade shallow local history into complete release-history, maintainer-culture, or all-user-facing deprecation conclusions.
- Do not treat rapid cadence alone as decisive fork/extension risk; it is a pressure requiring surface-churn and diff sampling.
- Do not treat bundled workflow templates as evidence of actual gsd-2 maintainer release practice without Actions logs / artifacts / PRs / docs.

When auditing, prohibited-articulation findings cite META-SYNTHESIS §3 verbatim and apply the corresponding "do not" to the audited artifact's claim.

**Meta-discipline note.** The lookup is a **reference, not a substitute** for vocabulary-precision judgment. The auditor should read it as: "consult these vetted replacements when articulating corrected-frame language; carry the discipline of *not constructing new compressions on the fly* into any phrasing not covered by the lookup; if a phrase recurs in the audited artifacts that should plausibly be on the lookup but isn't, flag in FINDINGS §4 self-flagged-concerns rather than inventing replacement language." The lookup explicitly does not enumerate every possible v1-GSD-shaped phrasing; the meta-discipline ("be careful with vocabulary-precision; cite source-of-grounding when articulating corrected frame; do not invent compressions") applies to all phrasings, lookup-covered or not.

### §2.4 The audit lens

Where do the gsd-2-uplift framing artifacts:

- (a) Use v1-GSD vocabulary (patcher / skills-bundle / hybrid / "harness as thin layer") as primary?
- (b) Under-weight runtime-application surfaces (headless / RPC / MCP / Pi-session / state-control / two-engine-architecture / runtime application status)?
- (c) Treat skills as a primary intervention surface vs as one of four extension subsystems?
- (d) Treat workflow-markdown as the primary workflow vocabulary vs as one of two engine modes (markdown-phase) with the deterministic counterpart (yaml-step) under-discussed?
- (e) Use "harness" framing in ways that obscure gsd-2's standalone-runtime-application status?
- (f) Treat R2 (extension) as if it pre-supposes thin-layer extensibility, or as if it operates against runtime-application internals?
- (g) Under-weight R4 (orchestrate-without-modifying) target surfaces (the headless / RPC / MCP / query / hook / workflow-template surfaces)?

**Out of scope for this lens.** Substance claims about codebase facts (handled by the prior audit; results consumed as grounding per §4.2). Disposition recommendations (Logan disposes per §8). Re-exploration or new investigation.

**Coupling to method.** The lens questions (a)-(g) are operationalized in §5 method through (i) vocabulary scan, (ii) surface-weighting check, (iii) **negative-space check (required)**, (iv) question-shape check, (v) implication check. The negative-space check (per §5.2) tests for under-weighting via *omission* rather than vocabulary — a key methodological correction from v1.

## §3. Auditor selection — two-step conditional

### §3.1 Disposition

**Two-step conditional.** Step-1 cross-vendor codex GPT-5.5 high baseline pass under minimal lens-spec; Step-2 same-vendor adversarial-auditor-xhigh stress + differential analysis fires *only if* Step-1 returns Class C candidates. Pre-commit to floor + escalate on evidence (mirrors B2 selective-audit discipline at DECISION-SPACE.md §1.12).

### §3.2 Why this shape

- **Same-vendor-only is structurally incoherent for shared-frame failure.** Per SYNTHESIS-COMPARISON.md §4.1 inversion observation: M1's register-vs-substance asymmetry is empirically more complex than the original claim; cross-vendor surfaced the framing-leakage caveat same-vendor missed. Building a premise-bleed audit on a property the comparison itself documented as failing in this vendor pair is structurally incoherent.
- **Cross-vendor baseline is the structural floor.** The cross-vendor reader is the one who can detect shared Claude+Logan framing.
- **Same-vendor stress adds value only on Class C.** When cross-vendor surfaces Class C candidates Claude reading might re-classify or supplement. Below Class C, same-vendor stress likely catches register-shaped items below load-bearing-ness threshold; not worth the dispatch.
- **Conditional escalation matches existing project discipline.** Per B2's per-slice-W2-audit-disposition: pre-commit to floor + escalate on evidence.

### §3.3 Step-1: cross-vendor baseline

- **Auditor:** codex GPT-5.5 high.
- **Input:** the artifacts under audit (§4) + this spec's §2 lens definition + §4.2 grounding inputs + §5 method.
- **Output:** Step-1 FINDINGS section per §6 output shape (§6.1).
- **Forbidden-reading list:** see §3.5.

### §3.4 Step-2: same-vendor stress (conditional)

Fires by default if Step-1 returns one or more Class C candidates.

- **Auditor:** Claude same-vendor adversarial-auditor-xhigh.
- **Input:** Step-1 findings + the same artifacts under audit + this spec.
- **Output:** Step-2 FINDINGS section + differential analysis per §6 output shape (§6.2).
- **Differential analysis purpose.** Cross-vendor candidates same-vendor missed = highest-priority Class C-eligible (caught what same-vendor cannot). Same-vendor candidates cross-vendor missed = register-shaped catches that may still be valid (subtle in-house-vocabulary-leak codex doesn't recognize). Joint candidates = robustness-signaled.

**Manual-escalation discretion.** Logan can fire Step-2 manually for other reasons even if Step-1 doesn't return Class C. Examples: independent same-vendor read for cross-checking; calibration with prior audit experience; second-vendor read warranted by Step-1 findings that don't reach Class C but cluster in concerning ways; resource availability that makes Step-2 cheap to add. The Class-C trigger is the **default-firing-condition**, not the **only firing condition**. Logan retains escalation discretion per the project's general disposition-discipline (per DECISION-SPACE.md §1.17 + framing-widening §3.3).

### §3.5 Forbidden-reading list (both auditors)

- This conversation's transcript or any session-context.
- `.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md`.
- `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` (DC0-DC4 framing).
- `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (this audit's adjudication trace).
- `.planning/STATE.md`, `OVERVIEW.md` recent updates referring to comparison-drafting status.

The auditors read the artifacts under audit + this spec's lens definition + §4.2 grounding inputs. Not Claude's drafting context.

## §4. Artifacts under audit + grounding inputs

### §4.1 Artifacts under audit (in scope)

**Primary** (load-bearing for §2.1 + §5 incubation dispositions):

1. `.planning/gsd-2-uplift/INITIATIVE.md` — full read; §3.2 candidate-design-shapes and §1 "harness" framing are likely first-surface premise-bleed sites.
2. `.planning/gsd-2-uplift/DECISION-SPACE.md` — targeted read of §1.2 framing reframe; §1.7 metaquestion + starter list; §1.8 R2/R3 hybrid (R-mix language); §3.x open-question section.
3. `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` — targeted read of §0 stratification (F1-F8 framing); §1 cross-slice patterns; §2.1 R1-R5 viability; §2.5 design-shape candidates table.
4. `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` — full read of §0 stratification + §5 recommendations + §6 confidence; targeted read of §1 patterns + §2.1 R1-R5.
5. `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` — full read of §0 + §2 + §5 + §6; targeted read of §1 + §3 + §4.
6. `.planning/deliberations/2026-04-28-framing-widening.md` — targeted read of R1-R5 design space; six-context plurality; four-act plurality; project-anchoring; §9 deferred items log.

**Secondary** (read for premise-bleed in question-shape; do not re-audit substance):

7. `.planning/gsd-2-uplift/orchestration/preamble.md` and slice prompts (`slice-01-*.md` through `slice-05-*.md`) — scan only for question-set under-weighting of runtime-application surfaces.
8. `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` and `audit-spec.md` — scan only for synthesis question-shape carrying v1-GSD-shaped framing.

**Targeted-sampling allowed under hard cap** (per §5 method):

9. The 5 W1 slice outputs (`01-mental-model-output.md` through `05-release-cadence-output.md` + addenda/corrigenda) — sampled section-only when a Class B/C candidate appears in §4.1 items 1-8 and the auditor needs to test whether premise propagated. Hard cap: max 3-5 slice-output sections sampled per audit run total. Do not re-audit whole slices.

**Out of scope:**

- The 3 W2 audits (substance-audit-shaped; not relevant for premise-bleed; consumed as grounding per §4.2 if relevant).
- Full re-read of gsd-2 source code (no substance re-audit).

### §4.2 Grounding inputs — hybrid (prior-audit primary + narrow source-reading fallback)

The auditor needs stable authority for "what GSD-2 actually is" when applying the corrected frame (§2.2) and the negative-space check (§5.2). The grounding hybrid:

**Primary grounding** (consult first):

- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md`
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-2-DISPOSITION.md`
- Relevant Wave 2 adjudication sections from the same audit folder.

**Fallback grounding** (consult only when primary doesn't ground a specific claim):

- Narrow source-reading of gsd-2 source code (`/home/rookslog/workspace/projects/gsd-2-explore/`).
- **Soft default: ~5 file reads per audit run.** Auditor stays under by default.
- **Overflow protocol.** If auditor needs >5 reads to ground specific Class B/C findings, auditor flags + justifies in FINDINGS §4 self-flagged-concerns. Required justification: (i) the count exceeded; (ii) per additional read, why it was fact-grounding rather than architectural inference; (iii) which findings each additional read grounded. Logan disposes overflow per §8 (accept legitimate overflow / reclassify under-grounded findings / reject + discount findings).
- **Use only for fact-grounding** (e.g., verifying a command name, file path, schema field). Not for architectural inference.
- **Citation required** (file:line). The cited fact appears in the corresponding finding's justification.
- **Coverage expectation.** META-SYNTHESIS coverage of runtime-application surfaces is substantial (§1 explicit naming; §2 typed vocabulary; §5 R4 elevation). Source-reading fallback should fire *rarely*; expected typical reads <5; overflow is exceptional and justification-bounded.

**Method discipline.** Auditor consults primary grounding first; falls back to source-reading only when primary doesn't cover the specific claim. Does not re-construct GSD-2's architecture from scratch. The soft cap is an evidence-adaptive discipline marker (analogous to §3 conditional escalation): default low + explicit overflow protocol when justified.

## §5. Audit method

### §5.1 Pre-audit framing read

Auditor reads §2 (lens definition + corrected-frame vocabulary + replacement lookup) and §4 (artifacts + grounding inputs) before opening any audited artifact. The lens is the audit's anchor. The replacement vocabulary lookup (§2.3) is the auditor's stable reference for corrected-frame articulation.

### §5.2 Per-artifact pass

For each primary artifact (§4.1 items 1-6) and each secondary artifact (§4.1 items 7-8), the auditor performs five sub-steps:

1. **Vocabulary scan.** Search for v1-GSD-shaped vocabulary: "patcher," "skills-bundle," "hybrid," "harness" (in thin-layer sense), "wrappers around gsd-2," "skills + hooks + markdown" or similar enumerations that under-weight headless/RPC/MCP/Pi-session/state-control. Cite file:line.

2. **Surface-weighting check.** Where R-strategies are discussed (especially R1 / R2 / R4), check whether the discussion treats:
   - R2 as if extension targets are thin-layer config primarily, vs as if extension targets include runtime-application internals.
   - R4 as a fallback or low-priority option, vs as first-class for runtime-application surfaces (headless / RPC / MCP).
   - Skills / workflow-markdown as primary intervention surfaces vs as one-of-four extension subsystems.

3. **Negative-space check (required).** Test for under-weighting via *omission*. For each artifact, ask:
   - **(i)** Which runtime-application surfaces (per §2.2 corrected frame: headless / RPC / MCP / Pi-session / state machinery / two-engine architecture) are absent or late despite being source-central per §4.2 grounding?
   - **(ii)** Does the artifact's question order make skills / workflow-markdown easy to see and runtime-application surfaces harder to see?
   - **(iii)** Does the artifact treat R4 as add-on despite headless / RPC / MCP being first-class GSD-2 surfaces?
   
   Negative-space findings are recorded with the same structure as vocabulary-scan findings (per §6); justification cites the source-central surface that's absent + the grounding that establishes its source-centrality (per §4.2). This sub-step is *required*, not optional; coupling to §4.2 grounding is structural (the negative-space check rests on the grounding's stable reference frame).

4. **Question-shape check (for slice prompts and synthesis-spec).** Did the question-set ask about runtime-application surfaces with proportional weight, or did the question-set bias toward thin-layer surfaces?

5. **Propagation sampling (conditional).** When a Class B/C candidate appears in steps 1-4 above, optionally inspect the corresponding slice-output section (§4.1 item 9) to determine whether premise actually propagated. Cite verbatim. Do not re-audit whole slices. **Hard cap: max 3-5 slice-output sections sampled per audit run total.** Track the running count.

6. **Implication check.** Where the artifact draws implications for incubation / second-wave-scoping, does the implication-language reflect runtime-application reality, or thin-layer presupposition?

### §5.3 Cross-artifact pass

After per-artifact passes, the auditor checks for **propagation patterns**:

- Where v1-GSD vocabulary appears in INITIATIVE.md / DECISION-SPACE.md / framing-widening, does it propagate through slice prompts → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON?
- Where one artifact corrects v1-GSD framing (e.g., framing-widening §1 R1-R5 + §4 four-act plurality may already widen beyond v1-GSD), does the correction land in downstream artifacts?
- Where SYNTHESIS-COMPARISON.md §2.1 R4 weighting characterization sits relative to the lens — does it surface or obscure runtime-application surface-weighting?
- Where negative-space findings cluster across multiple artifacts (e.g., session-control / state-machinery / RPC under-weighted across INITIATIVE + SYNTHESIS + SYNTHESIS-COMPARISON), are they propagation chains or independent omissions?

### §5.4 No re-exploration

The audit does **not**:

- Read gsd-2 source code beyond the §4.2 narrow-source-reading fallback (max 5 file reads, fact-grounding only).
- Re-execute slice questions.
- Construct an alternative synthesis or comparison.
- Recommend specific revisions beyond classification (per §6 output shape).

### §5.5 Method for Step-2 (if fired)

If Step-2 same-vendor stress fires per §3.4, the same-vendor auditor:

- Reads Step-1 findings + the same audited artifacts + this spec.
- Re-runs §5.2 sub-steps 1-4 (vocabulary scan; surface-weighting; negative-space; question-shape) and §5.2 sub-step 6 (implication check) on each Class C-flagged artifact from Step-1.
- Records: (i) confirmations of Step-1 findings; (ii) re-classifications (e.g., Class B that should be Class C, or vice versa); (iii) net-new findings same-vendor reading surfaces; (iv) candidates Step-1 returned that same-vendor reading would dismiss.
- Differential analysis (per §6.2): cross-vendor-only / same-vendor-only / joint candidates per the §3.4 partition.

## §6. Output shape

The auditor produces **one document**: `FINDINGS.md` at the audit folder root. If Step-2 fires, the document carries Step-1 + Step-2 + differential sections; if Step-2 doesn't fire, the document carries Step-1 only.

### §6.1 Step-1 (cross-vendor baseline) FINDINGS structure

```
---
type: premise-bleed-audit-findings
date: <audit run date>
auditor_step1: codex GPT-5.5 high
spec: ./AUDIT-SPEC.md
target: <list of artifacts read>
status: step1-complete | both-steps-complete
---

# §0. Step-1 summary

- Total premise-bleed instances surfaced: N
- Classification breakdown:
  - Class A (cosmetic / wording-addendum): X
  - Class B (substantive but non-disposition-changing): Y
  - Class C (load-bearing for §2.1 / §5 dispositions): Z
- Top-line read: <2-3 sentences on whether premise-bleed is pervasive, localized, or absent>
- Step-2 escalation triggered: yes (Class C ≥ 1) | no (no Class C)

# §1. Per-instance findings

For each premise-bleed instance:

### Finding N
- **Artifact:** <file path>
- **Location:** <section + line numbers>
- **Quote:** "<verbatim excerpt>"
- **Lens-relevance:** <which §2.4 lens-question this hits: (a)-(g)> (and/or §5.2.3 negative-space sub-question (i)/(ii)/(iii))
- **Type:** vocabulary-scan | surface-weighting | negative-space | question-shape | implication
- **Classification:** Class A | Class B | Class C
- **Justification:** <why this instance fits the class; what would change the classification>
- **Grounding citation (if negative-space):** <prior-audit citation or fact-grounding source-read citation>
- **Disposition implication (Class C only):** <which incubation axis (§5.1 / §5.2 / §5.3 / §5.4) this affects + how>
- **Propagation sample (if applicable):** <slice-output section sampled per §5.2.5; verbatim citation; cumulative cap-tracking>

# §2. Cross-artifact propagation patterns

- Pattern 1: <description + propagation chain across artifacts>
- Pattern 2: <...>

# §3. Notable absences

Where the lens predicts premise-bleed should appear but doesn't (i.e., the artifact correctly weighted runtime-application surfaces). Inverse signal — useful for calibrating where the framing already self-corrected.

# §4. Step-1 confidence and limits

- Confidence on classification: <high / medium-high / medium / medium-low>
- Self-flagged concerns: <where the auditor isn't sure whether something is premise-bleed vs legitimate framing>
- Cross-vendor framing-leakage caveat: <where codex may not recognize subtle in-house framings; flag for Step-2 if fires>
- Slice-output sampling tally: <count of slice-output sections sampled, capped at 3-5 per §5.2.5>
- Source-reading tally: <count of source files read for fact-grounding, capped at 5 per §4.2>
- Out-of-scope: <items the auditor noticed but did not pursue per §5.4>

# §5. Non-binding disposition signal

Auditor states why Logan might choose each plausible disposition (per §8). Auditor does not pick one; Logan disposes.

- **Why Logan might choose commit-as-is:** <reasoning given findings>
- **Why Logan might choose commit-with-addendum:** <reasoning given findings>
- **Why Logan might choose revise-before-commit:** <reasoning given findings>
```

### §6.2 Step-2 (same-vendor stress) FINDINGS structure (if fired)

Appended to the Step-1 document if Step-2 fires:

```
# §6. Step-2 summary
- Same-vendor confirmations: N (Step-1 findings same-vendor agrees with)
- Same-vendor re-classifications: M (Step-1 findings same-vendor would re-class)
- Net-new same-vendor findings: P (cross-vendor missed)
- Same-vendor dismissals: Q (Step-1 findings same-vendor would dismiss)

# §7. Per-instance Step-2 findings
[same structure as §1, scoped to Step-2 candidates]

# §8. Differential analysis
- Cross-vendor-only candidates (same-vendor missed): <highest-priority Class C-eligible>
- Same-vendor-only candidates (cross-vendor missed): <register-shaped catches; calibrate carefully>
- Joint candidates: <robustness-signaled>

# §9. Step-2 confidence and limits
- M1 register-catch caveat: <where same-vendor may share v1-GSD framing-leak with Claude+Logan and cannot self-detect>
- Self-flagged concerns: <...>
- Out-of-scope: <...>

# §10. Updated non-binding disposition signal
- <revised reasoning per option given combined Step-1 + Step-2 evidence>
```

### §6.3 Output constraints

- **Length:** Step-1 only = 200-500 lines target. Step-1 + Step-2 = 350-700 lines. Beyond these, audit is over-scoped; flag instead of expanding.
- **No drafting suggestions** for revised wording (Logan + Claude handle revision post-disposition).
- **No reframe proposals** (out of scope).
- **Calibrated language**; cite verbatim; no paraphrase substitution for direct quotes.
- **Citation discipline:** every verbatim quote pairs with file:line; every grounding-cited claim pairs with prior-audit-citation or source-read-citation.

## §7. Classification rubric

**Class A — cosmetic / wording-addendum.**
- Vocabulary appears but doesn't shape the surrounding analysis.
- Could be revised by adding a footnote or 1-3 line clarification without changing downstream conclusions.
- Example shape: "patcher / skills / hybrid" appears in INITIATIVE.md §3.2 but the document also names "ground in what gsd-2 actually exposes (slice 4)" — the v1-GSD vocabulary is present but constrained by source-grounding requirement.

**Class B — substantive but non-disposition-changing.**
- Vocabulary or weighting shapes the analysis but the downstream conclusions remain valid under corrected framing.
- Could be revised by re-articulating the affected paragraphs without changing §2.1 / §5 dispositions.
- Example shape: an R-strategy section discusses R2 in thin-layer terms but the conclusion (R2 viable but with caveats) holds under runtime-application framing too.

**Class C — load-bearing for §2.1 / §5 dispositions.**
- Vocabulary or weighting shapes a conclusion that would change if the framing were corrected.
- Revision before §2.1 / §5 adjudication is warranted.
- Example shape: §5.2 R-mix integration treats R4 as elevated-from-cancellation primarily for release/RC/staging when under runtime-application framing R4 should be primary for headless/RPC/MCP surfaces independent of release-coordination — different incubation R-mix shape.

**Calibration discipline.** When uncertain between classes, the auditor names the uncertainty and lists what would resolve it. Do not over-classify Class C (false positives erode trust); do not under-classify (false negatives miss the audit's point). The auditor's confidence on each classification is recorded per-finding.

## §8. Disposition pathway (post-audit)

After auditor produces `FINDINGS.md`, the disposition pathway is:

1. **Logan reviews findings.** Reads the summary + Class C items + sample of Class A/B for calibration. If Step-2 fired, reads the differential analysis especially.
2. **Logan disposes** one of:
   - **(a) Commit-as-is.** Premise-bleed is absent or Class A only; SYNTHESIS-COMPARISON.md commits without revision.
   - **(b) Commit-with-addendum.** Class B/C items are tractable as a §7 addendum to SYNTHESIS-COMPARISON.md; Claude drafts addendum; commit follows.
   - **(c) Revise-before-commit.** Class C items affect §2.1 / §5 disposition shape; Claude revises affected sections; re-run alignment check; commit follows.
3. **Disposition recorded** at `DISPOSITION.md` in this audit folder. Records: what Logan disposed; reasoning; addendum shape (if (b)); revisions made (if (c)); cross-reference to comparison-drafting decisions log + DECISION-SPACE.md §1.17.

The auditor produces a non-binding disposition signal (per §6.1 §5 + §6.2 §10) that helps Logan see the per-option reasoning; Logan binds.

## §9. Conditional structure

**What would change this spec.**

- **If Logan reads the lens as wrongly-shaped** (e.g., the v1-GSD vs runtime-application binary is too coarse; the actual concern is finer-grained): revise §2 lens definition.
- **If Logan reads the auditor selection as wrong** (e.g., pre-commit two-step always; or cross-vendor-only single-step; or same-vendor with shared-frame caveat): revise §3 per the alternatives in DECISION-SPACE.md §1.17 "What would change the decision."
- **If Logan reads the artifact list as too narrow or too broad**: revise §4.1 per scope adjustment.
- **If Logan reads the grounding hybrid as risky** (e.g., source-reading creates substance-territory door): drop to prior-audit-only; revise §4.2.
- **If Logan reads the negative-space check as over-engineered**: relax §5.2.3 to optional; revise §2.4 coupling.
- **If Logan reads the vetted-replacement vocabulary as over-engineered**: drop §2.3 lookup; revise §2.2 to "be more careful" without explicit replacements.
- **If Logan reads the classification rubric as too coarse**: refine §7.

**What this spec does not foreclose.**

- Whether to expand to substance-audit if premise-bleed audit surfaces source-claim issues (it shouldn't, per scope, but if it does — those go to a substance follow-up, not this audit).
- Whether the SYNTHESIS-COMPARISON.md draft itself needs structural revision beyond §7 addendum (only if Class C items are pervasive enough that addendum-shape doesn't suffice).
- Whether to add a third audit step (e.g., independent third-synthesizer comparison) if Step-2 differential surfaces unresolvable register/substance conflicts.

## §10. Cost estimate (per F7 disposition)

### §10.1 Read budget per artifact

- **Full read.** INITIATIVE.md; SYNTHESIS-COMPARISON.md §0/§2/§5/§6; SYNTHESIS-CROSS.md §0/§5/§6.
- **Targeted read.** DECISION-SPACE.md (§1.2/§1.7/§1.8/§3); SYNTHESIS.md (§0/§1/§2.1/§2.5); framing-widening (§1/§2/§3/§4/§9).
- **Scan only.** orchestration preamble; slice prompts (`slice-01-*.md` through `slice-05-*.md`); synthesis-spec; audit-spec — unless propagation-sampling fires per §5.2.5.
- **Conditional sampling.** Slice outputs: only if a Class B/C candidate triggers per §5.2.5; max 3-5 sections; ~10-15 min per section sampled.
- **Conditional grounding.** Source-reading fallback per §4.2: only when prior-audit grounding doesn't cover a specific claim; max 5 file reads; ~5-10 min per file.

### §10.2 Time budget

- **Step-1 cross-vendor baseline:** ~1-1.5 hr wall-clock for codex GPT-5.5 high pass over the artifact set under the §10.1 read budget.
  - Plus ~10-15 min × N (max 3-5) if propagation-sampling fires.
  - Plus ~5-10 min × M (max 5) if source-reading fallback fires.
- **Step-2 same-vendor stress (conditional):** ~30-60 min Claude-xhigh pass + ~30 min differential analysis. Fires only if Step-1 returns Class C.
- **Logan disposition review:** ~15-30 min (more if Step-2 fired).
- **Post-disposition Claude work:** 0 lines (commit-as-is) / 50-150 lines addendum / 100-400 lines revisions.

### §10.3 Total time-to-§2.1+§5-adjudication

- **Lower bound** (Class A only; no escalation; no addendum): ~1.5-2 hr.
- **Mid-range** (Class B or B/C minor; escalation fires; addendum): ~2.5-3.5 hr.
- **Upper bound** (Class C pervasive; revision-before-commit): ~4-5 hr.

## §11. Cross-references

**Direct ground.**
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §4.4 (framing-import drift surfaced as initiative-maturity signal — antecedent observation that triggered this audit).
- `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` §4 (methodological note on arxiv-sanity-mcp framing-import drift).
- Logan 2026-04-28 message registering premise-correction concern (in-session conversation; see SYNTHESIS-COMPARISON.md §6.3 in-session-collaboration caveat for context).

**Decision + deliberation references.**
- `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.17 (load-bearing audit-methodology decision; this spec implements §1.17).
- `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (full review-and-response trace; §3 Claude analysis; §5 per-finding adjudications; §6 revision-action table).
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC-REVIEW.md` (cross-vendor review of v1 spec; basis for v2 revisions).

**Methodology ground.**
- METHODOLOGY.md M1 (paired-review register-vs-substance asymmetry — empirically more complex per SYNTHESIS-COMPARISON.md §4.1) at `:104-115`.
- LONG-ARC.md anti-patterns (closure pressure; framing-leakage).
- framing-widening §3.3 (disposition-discipline; synthesis defers to incubation).
- SYNTHESIS-COMPARISON.md §4.1 (M1 mixed observation — register/substance asymmetry empirically more complex than claimed).

**Adjacent audits.**
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/` — substance audit (codebase-understanding); orthogonal to this premise-bleed framing audit; outputs serve as primary grounding per §4.2.

**Initiative-staging.**
- `.planning/gsd-2-uplift/INITIATIVE.md` §7 migration trigger — initiative content is maturing toward dedicated-repo readiness; framing-import drift (§4.4) is one signal among others.

---

*Audit-spec v2 (revised) written 2026-04-28 by Claude (Opus 4.7) post-cross-vendor-review. Implements DECISION-SPACE.md §1.17 dispositions distilled from `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md`. Subject to the same fallibility caveat as DECISION-SPACE.md §0. Spec is revised-for-dispatch; awaits Logan final-call before auditor dispatch.*
