---
type: premise-bleed-audit-spec
date: 2026-04-28
status: draft-for-disposition (awaiting Logan review before auditor dispatch)
target: gsd-2-uplift framing artifacts (INITIATIVE.md, DECISION-SPACE.md, SYNTHESIS.md, SYNTHESIS-CROSS.md, SYNTHESIS-COMPARISON.md, framing-widening) + load-bearing slice prompts
scope: bounded premise-bleed lens audit before §2.1 + §5 incubation adjudication on SYNTHESIS-COMPARISON.md
location: .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/
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
  (headless/RPC/MCP/Pi/session/state-control).

  This is **not** a re-audit of the codebase-understanding (that work was already
  done at `audits/2026-04-28-cross-vendor-codebase-understanding-audit/`). The
  question here is register/framing, not substance: did the artifacts inherit a
  v1-GSD-shaped vocabulary that made some surfaces visible and others less visible?
related_audit: .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/ (substance-checked the codebase-understanding; this audit checks framing)
methodology_ground: METHODOLOGY.md M1 (paired-review register-vs-substance asymmetry); LONG-ARC.md anti-patterns (closure pressure; framing-leakage); framing-widening §3.3 disposition-discipline; SYNTHESIS-COMPARISON.md §4.4 (framing-import drift surfaced as initiative-maturity signal)
---

# v1-GSD Mental-Model Premise-Bleed Audit Spec

## §0. Read-guidance

This document is the **spec for an audit that has not yet run**. Logan disposes whether to dispatch as-specified, revise the spec, or cancel.

**For "what the audit asks"**: §2 lens definition; §4 specific surfaces.
**For "how the auditor should work"**: §5 method; §6 output shape.
**For "why this audit, not codebase re-audit"**: §1 motivation.
**For "what changes if Logan revises"**: §9 conditional structure.

## §1. Why this audit (not the codebase-understanding audit)

The earlier `2026-04-28-cross-vendor-codebase-understanding-audit/` tested whether the Claude-led investigation **understood the gsd-2 codebase** well enough — substance audit. Its target was claim-grounding, source-verifiability, surface-coverage.

This audit tests something orthogonal: whether the **framing vocabulary** Logan and Claude carried into the initiative shaped what the artifacts looked at and how they articulated findings. The substance can be source-grounded **and** the framing can still under-weight load-bearing surfaces because those surfaces never made it into the question-set.

**Concrete signal that motivates this audit** (from SYNTHESIS-COMPARISON.md §4.4 + Logan's 2026-04-28 message): INITIATIVE.md §3.2 explicitly names candidate design-shapes as "**Patcher / Skills / Hybrid**." That's v1-GSD vocabulary — it presupposes gsd-2 is a thin layer one applies a patcher or skills-bundle to, not a standalone runtime/application with headless/RPC/MCP/Pi-session surfaces as primary intervention candidates. If that vocabulary propagated through the slice prompts → slice outputs → audits → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON, the §2.1 R-mix and §5 R-strategy axes may carry under-weighting that the current paired-review didn't catch (because both syntheses share the dispatching-project's framing-widening vocabulary per cross-vendor's framing-leakage caveat at SYNTHESIS-CROSS §6).

**The audit's job is not to revise the framing.** It is to surface where premise-bleed appears, classify each appearance by load-bearing-ness for §2.1 + §5 dispositions, and let Logan decide what to do (commit-as-is / commit-with-addendum / revise-before-commit).

## §2. The lens

**v1-GSD mental model (the prior frame).** GSD as intervention surface made of:
- Workflow markdown templates inside a host runtime (Codex, Claude Code).
- Skills (Claude Code skill manifests; per-unit allowlists).
- Hooks (host-runtime hooks; lifecycle integrations).
- Command wrappers (slash-commands; markdown command bodies as agent instructions).
- Host-runtime conventions (project-local config; trust gates layered on host runtime).
- Patcher tooling (modify-existing-installation pattern).

**gsd-2 as it actually is (the corrected frame).** A standalone agent application/runtime built around Pi, with first-class:
- Session control (gsd-2 owns session lifecycle, not the host runtime).
- Headless surfaces (`--mode headless`; query subcommands; JSON/JSONL output).
- RPC surfaces (RPC client; out-of-process control).
- MCP surfaces (in-process MCP via `--mode mcp`; standalone `@gsd-build/mcp-server`).
- Pi vendoring + Pi-extension API (gsd-2 is a vendored modified Pi fork; core GSD is itself a Pi extension).
- State machinery (`STATE.json`; `GRAPH.yaml`; daily-rotated journal with ~22 schema versions; metrics ledger; cost/budget controls).
- Workflow engines (markdown-phase prompt-dispatch + yaml-step deterministic; not just templates).
- Release/runtime complexity (semver detection; release templates; `generate-changelog.mjs`; `bump-version.mjs`; native modules; Rust components).
- Extension systems (four parallel subsystems: pi-coding-agent extensions; GSD ecosystem extensions; workflow plugins; skills — the latter is *one of four*, not the primary surface).

**The audit lens.** Where do the gsd-2-uplift framing artifacts:
- (a) Use v1-GSD vocabulary (patcher / skills-bundle / hybrid / "harness as thin layer") as primary?
- (b) Under-weight runtime-application surfaces (headless / RPC / MCP / Pi-session / state-control / two-engine-architecture / runtime application status)?
- (c) Treat skills as a primary intervention surface vs as one of four extension subsystems?
- (d) Treat workflow-markdown as the primary workflow vocabulary vs as one of two engine modes (markdown-phase) with the deterministic counterpart (yaml-step) under-discussed?
- (e) Use "harness" framing in ways that obscure gsd-2's standalone-runtime-application status?
- (f) Treat R2 (extension) as if it pre-supposes thin-layer extensibility, or as if it operates against runtime-application internals?
- (g) Under-weight R4 (orchestrate-without-modifying) target surfaces (the headless / RPC / MCP / query / hook / workflow-template surfaces)?

**Out of scope for this lens.** Substance claims about codebase facts (handled by the prior audit). Disposition recommendations (Logan disposes). Re-exploration or new investigation.

## §3. Auditor selection

**Recommended: same-vendor adversarial-auditor-xhigh.**

Reasoning:
- The lens is **register-shaped**, not substance-shaped. Per METHODOLOGY.md M1 (and SYNTHESIS-COMPARISON.md §4.1's refined reading), same-vendor catches register more readily — exactly what's needed for vocabulary-leak detection.
- The lens requires understanding **both** "what v1-GSD looked like" AND "what gsd-2 actually is." Same-vendor with explicit lens-framing carries this better than cross-vendor (which would need to construct both frames from scratch).
- The auditor will operate under explicit forbidden-reading on this conversation's framing (per §5 below) to mitigate same-vendor framing-import.

**Alternative: cross-vendor codex GPT-5.5 high.**

When this becomes preferable:
- If Logan reads the same-vendor risk as load-bearing (Claude shares the v1-GSD framing-leak; same-vendor cannot detect it).
- If the audit returns conclusions with low confidence (escalate to cross-vendor for independent read).
- For escalation, **not baseline**, per the M1 register-catching property + cost trade-off.

**Forbidden-reading list (for either auditor).**
- This conversation's transcript or any session-context.
- `.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md`.
- `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` (DC0-DC4 framing).
- `.planning/STATE.md`, `OVERVIEW.md` recent updates referring to comparison-drafting status.

The auditor reads the artifacts under audit + the v1-GSD lens definition + this spec. Not Claude's drafting context.

## §4. Artifacts under audit (in scope)

Primary (load-bearing for §2.1 + §5 incubation dispositions):

1. `.planning/gsd-2-uplift/INITIATIVE.md` — full read; §3.2 candidate-design-shapes and §1 "harness" framing are likely first-surface premise-bleed sites.
2. `.planning/gsd-2-uplift/DECISION-SPACE.md` — §1.2 framing reframe; §1.7 metaquestion + starter list; §1.8 R2/R3 hybrid (R-mix language); §3.x open-question section.
3. `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` — §0 stratification (F1-F8 framing); §1 cross-slice patterns; §2.1 R1-R5 viability; §2.5 design-shape candidates table.
4. `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` — §0 stratification; §1 patterns; §2.1 R1-R5; §5 recommendations.
5. `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` — §0 summary; §1 convergent findings; §2 divergent findings (R4 weighting especially); §5 four-axis incubation integration.
6. `.planning/deliberations/2026-04-28-framing-widening.md` — R1-R5 design space; six-context plurality; four-act plurality; project-anchoring; §9 deferred items log.

Secondary (read for premise-bleed in question-shape; do not re-audit substance):

7. `.planning/gsd-2-uplift/orchestration/preamble.md` and slice prompts (`slice-01-*.md` through `slice-05-*.md`) — check whether question-set under-weights runtime-application surfaces.
8. `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` and `audit-spec.md` — check whether synthesis question-shape carries v1-GSD-shaped framing.

Out of scope:

- The 5 W1 slice outputs themselves (those report what slice questions asked; if slice questions carry premise-bleed, the slice outputs inherit it, but the leverage point for revision is the question-shape not the output).
- The 3 W2 audits (substance-audit-shaped; out of scope for premise-bleed).
- gsd-2 source code (no new source reading; this is not a substance audit).

## §5. Audit method

### §5.1 Pre-audit framing read

Auditor reads §2 of this spec (lens definition) and §4 of this spec (artifacts) before opening any artifact. The lens is the audit's anchor.

### §5.2 Per-artifact pass

For each primary artifact (§4 items 1-6) and each secondary artifact (§4 items 7-8):

1. **Vocabulary scan.** Search for v1-GSD-shaped vocabulary: "patcher," "skills-bundle," "hybrid," "harness" (in thin-layer sense), "wrappers around gsd-2," "skills + hooks + markdown" or similar enumerations that under-weight headless/RPC/MCP/Pi-session/state-control. Cite file:line.
2. **Surface-weighting check.** Where R-strategies are discussed (especially R1 / R2 / R4), check whether the discussion treats:
   - R2 as if extension targets are thin-layer config primarily, vs as if extension targets include runtime-application internals.
   - R4 as a fallback or low-priority option, vs as first-class for runtime-application surfaces (headless / RPC / MCP).
   - Skills / workflow-markdown as primary intervention surfaces vs as one-of-four extension subsystems.
3. **Question-shape check (for slice prompts and synthesis-spec).** Did the question-set ask about runtime-application surfaces with proportional weight, or did the question-set bias toward thin-layer surfaces?
4. **Implication check.** Where the artifact draws implications for incubation / second-wave-scoping, does the implication-language reflect runtime-application reality, or thin-layer presupposition?

### §5.3 Cross-artifact pass

After per-artifact passes, the auditor checks for **propagation patterns**:
- Where v1-GSD vocabulary appears in INITIATIVE.md / DECISION-SPACE.md / framing-widening, does it propagate through slice prompts → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON?
- Where one artifact corrects v1-GSD framing (e.g., framing-widening §1 R1-R5 + §4 four-act plurality may already widen beyond v1-GSD), does the correction land in downstream artifacts?
- Where SYNTHESIS-COMPARISON.md §2.1 R4 weighting characterization sits relative to the lens — does it surface or obscure runtime-application surface-weighting?

### §5.4 No re-exploration

The audit does **not**:
- Read gsd-2 source code.
- Re-execute slice questions.
- Construct an alternative synthesis or comparison.
- Recommend specific revisions beyond classification (per §6 output shape).

## §6. Output shape

The auditor produces **one document**: `FINDINGS.md` at the audit folder root. Structure:

```
---
type: premise-bleed-audit-findings
date: <audit run date>
auditor: <auditor identity + reasoning effort>
spec: ./AUDIT-SPEC.md
target: <list of artifacts read>
status: complete
---

# §0. Summary

- Total premise-bleed instances surfaced: N
- Classification breakdown:
  - Class A (cosmetic / wording-addendum): X
  - Class B (substantive but non-disposition-changing): Y
  - Class C (load-bearing for §2.1 / §5 dispositions): Z
- Top-line read: <2-3 sentences on whether premise-bleed is pervasive, localized, or absent>
- Recommendation shape: <commit-as-is / commit-with-addendum / revise-before-commit, with auditor's reasoning>

# §1. Per-instance findings

For each premise-bleed instance:

### Finding N
- **Artifact:** <file path>
- **Location:** <section + line numbers>
- **Quote:** "<verbatim excerpt>"
- **Lens-relevance:** <which §2 lens-question this hits: (a)-(g)>
- **Classification:** Class A | Class B | Class C
- **Justification:** <why this instance fits the class; what would change the classification>
- **Disposition implication (Class C only):** <which incubation axis (§5.1 / §5.2 / §5.3 / §5.4) this affects + how>

# §2. Cross-artifact propagation patterns

- Pattern 1: <description + propagation chain across artifacts>
- Pattern 2: <...>

# §3. Notable absences

Where the lens predicts premise-bleed should appear but doesn't (i.e., the artifact correctly weighted runtime-application surfaces). Inverse signal — useful for calibrating where the framing already self-corrected.

# §4. Confidence and limits

- Confidence on classification: <high / medium-high / medium / medium-low>
- Self-flagged concerns: <where the auditor isn't sure whether something is premise-bleed vs legitimate framing>
- M1 register-catch caveat (same-vendor only): <if same-vendor auditor, flag where Claude may share the framing-leak and the auditor cannot self-detect>
- Out-of-scope: <items the auditor noticed but did not pursue per §5.4>
```

**Constraints on output:**
- 200-500 lines target. Beyond 500 lines, audit is over-scoped; flag instead of expanding.
- No drafting suggestions for revised wording (Logan + Claude handle revision post-disposition).
- No reframe proposals (out of scope).
- Calibrated language; cite verbatim; no paraphrase substitution for direct quotes.

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

1. **Logan reviews findings.** Reads the summary + Class C items + sample of Class A/B for calibration.
2. **Logan disposes** one of:
   - **(a) Commit-as-is.** Premise-bleed is absent or Class A only; SYNTHESIS-COMPARISON.md commits without revision.
   - **(b) Commit-with-addendum.** Class B/C items are tractable as a §7 addendum to SYNTHESIS-COMPARISON.md; Claude drafts addendum; commit follows.
   - **(c) Revise-before-commit.** Class C items affect §2.1 / §5 disposition shape; Claude revises affected sections; re-run alignment check; commit follows.
3. **Disposition recorded** at `DISPOSITION.md` in this audit folder. Records: what Logan disposed; reasoning; addendum shape (if (b)); revisions made (if (c)); cross-reference to comparison-drafting decisions log.

## §9. Conditional structure

**What would change this spec.**

- **If Logan reads the lens as wrongly-shaped** (e.g., the v1-GSD vs runtime-application binary is too coarse; the actual concern is finer-grained): revise §2 lens definition.
- **If Logan reads the auditor selection as wrong** (e.g., cross-vendor codex preferred for independence): swap §3 recommendation; cross-vendor needs more lens-construction in the spec.
- **If Logan reads the artifact list as too narrow** (e.g., 5 W1 slice outputs should be in scope): expand §4 primary; expect ~doubling of audit time.
- **If Logan reads the artifact list as too broad** (e.g., framing-widening should be out-of-scope because it's already lens-aware): tighten §4.
- **If Logan reads the classification rubric as too coarse** (e.g., Class C needs sub-categories for incubation-axis-affected): refine §7.

**What this spec does not foreclose.**
- Whether to also dispatch a cross-vendor audit (Logan can choose to add post-Wave-1 if same-vendor finds substantial Class C items).
- Whether to expand to substance-audit if premise-bleed audit surfaces source-claim issues (it shouldn't, per scope, but if it does — those go to a substance follow-up, not this audit).
- Whether the SYNTHESIS-COMPARISON.md draft itself needs structural revision beyond §7 addendum (only if Class C items are pervasive enough that addendum-shape doesn't suffice).

## §10. Cost estimate

- **Auditor dispatch:** ~30-60 min wall-clock for same-vendor xhigh adversarial-auditor pass over 6 primary artifacts + 2 secondary; cross-vendor at GPT-5.5 high comparable.
- **Output:** 200-500 lines per §6 constraint.
- **Logan disposition:** ~15-30 min review of findings + disposition.
- **Post-disposition work** (Claude in-session): 0 lines (commit-as-is) / 50-150 lines addendum (commit-with-addendum) / 100-400 lines revisions (revise-before-commit).

**Total time-to-§2.1+§5-adjudication:** ~1-3 hours including Logan review + post-disposition work, depending on disposition shape.

## §11. Cross-references

**Direct ground.**
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §4.4 (framing-import drift surfaced as initiative-maturity signal — antecedent observation that triggered this audit).
- `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` §4 (methodological note on arxiv-sanity-mcp framing-import drift).
- Logan 2026-04-28 message registering premise-correction concern (in-session conversation; see SYNTHESIS-COMPARISON.md §6.3 in-session-collaboration caveat for context).

**Methodology ground.**
- METHODOLOGY.md M1 (paired-review register-vs-substance asymmetry) at `:104-115`.
- LONG-ARC.md anti-patterns (closure pressure; framing-leakage).
- framing-widening §3.3 (disposition-discipline; synthesis defers to incubation).
- SYNTHESIS-COMPARISON.md §4.1 (M1 mixed observation — register/substance asymmetry empirically more complex than claimed).

**Adjacent audits.**
- `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/` — substance-audit (codebase-understanding); this audit is the orthogonal framing audit.

**Initiative-staging.**
- `.planning/gsd-2-uplift/INITIATIVE.md` §7 migration trigger — initiative content is maturing toward dedicated-repo readiness; framing-import drift (§4.4) is one signal among others.

---

*Single-author audit-spec written 2026-04-28 by Claude (Opus 4.7) at Logan's direction post-comparison-draft-completion. Subject to the same fallibility caveat as DECISION-SPACE.md §0. Spec is draft-for-disposition; Logan reviews + revises + dispatches.*
