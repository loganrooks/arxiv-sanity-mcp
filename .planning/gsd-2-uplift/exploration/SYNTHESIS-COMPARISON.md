---
type: paired-synthesis-comparison
date: 2026-04-28
synthesizers:
  - same-vendor: Claude Opus xhigh (.planning/gsd-2-uplift/exploration/SYNTHESIS.md; 609 lines)
  - cross-vendor: codex GPT-5.5 high (.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md; 207 lines)
comparison_author: Claude (Opus 4.7, xhigh effort) in-session-collaborative with Logan per D5a recommendation in `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md`
status: committed-with-audit-addendum (full §0-§6 landed; §7 audit addendum landed 2026-04-29 post-premise-bleed-audit per Logan disposition; §2.1 R4 disposition-timing + §5 axes await Logan adjudication at incubation per D5a)
inputs:
  - .planning/gsd-2-uplift/exploration/SYNTHESIS.md
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md
  - .planning/deliberations/2026-04-28-framing-widening.md
  - .planning/gsd-2-uplift/INITIATIVE.md
  - .planning/gsd-2-uplift/DECISION-SPACE.md
  - .planning/gsd-2-uplift/orchestration/synthesis-spec.md
  - .planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md
purpose: |
  Comparison artifact integrating both first-wave syntheses for incubation-checkpoint
  consumption per `synthesis-spec.md:185-188` + `DECISION-SPACE §2.3`. NOT a third
  synthesis — a convergence-and-divergence-aware integration that makes both
  syntheses navigable for Logan + Claude reading at incubation, surfaces convergent
  findings as robustness signal, divergent findings as deliberation input, and
  asymmetric coverage as completeness check.

  In-session-collaborative draft per D5a — Claude drafts; Logan adjudicates §2
  divergent findings + §5 integration. This comparison is not produced by an
  independent third synthesizer; the in-session-collaboration caveat in §6 applies.
read_order: |
  - For "what both syntheses converge on (highest-confidence inputs for incubation)":
    §1.
  - For "where the syntheses read the same evidence differently (Logan-adjudication
    territory)": §2.
  - For "what each synthesizer surfaced uniquely (asymmetric coverage / completeness
    signal)": §3.
  - For "what the paired-review process itself revealed (M1 in action)": §4.
  - For "the integrated read for incubation-checkpoint disposition (multi-axis:
    metaquestion / R-mix / context-anchoring / side-probe triggers)": §5.
  - For "what comparison can and cannot establish": §6.

  Per handoff §6.5 + DECISION-SPACE §2.3: incubation is **Logan-led + out of
  orchestration scope**. This comparison feeds incubation; it does not pre-decide
  incubation's questions.
---

# First-wave paired-synthesis comparison — gsd-2 uplift initiative

This document integrates the two first-wave syntheses landed 2026-04-28 — same-vendor `SYNTHESIS.md` (Claude Opus xhigh; 609 lines) and cross-vendor `SYNTHESIS-CROSS.md` (codex GPT-5.5 high; 207 lines) — into a paired-review integration for incubation-checkpoint per `DECISION-SPACE §2.3`. The shape preserves both syntheses (neither is modified per handoff §8.3); the comparison surfaces what reads the same evidence the same way (§1), what reads it differently (§2), what each surfaces alone (§3), and what the paired-review process itself revealed (§4). §5 integrates for incubation across four axes; §6 names limits.

If reading cold, follow the read-order in the frontmatter. Sections build on each other but each is self-contained enough to consult selectively.

## §0. Comparison summary

**What this comparison does for incubation.** Per `synthesis-spec.md:185-188` and `DECISION-SPACE §2.3`, incubation reads syntheses + comparison together to dispose: (a) does the metaquestion answer hold ("uplift-of-gsd-2 is the right shape"); (b) has the R1-R5 mix narrowed or shifted; (c) is direction-shifting evidence sufficient to re-disposition; (d) which deferred items (per `framing-widening §9`) are pre-vs-post critical path for second-wave-scoping. The comparison surfaces inputs to those dispositions; it does not dispose them.

**M1 paired-review framing.** Per `METHODOLOGY.md:104-115` + `DECISION-SPACE §1.13` (B3): cross-vendor reads catch substance more readily; same-vendor reads catch register more readily. The pairing is calibrated to test (i) whether substantive findings survive independent reading (convergent → robustness), (ii) whether interpretive register diverges in load-bearing ways (divergent → deliberation input), and (iii) whether either synthesizer missed material the other surfaced (asymmetric coverage → completeness signal). Per `synthesis-spec.md:172-189`, escalation to paired-synthesis was triggered (Trigger 4 fires per `SYNTHESIS.md §0`); this comparison is the escalation's downstream-utility artifact.

**Top-line takeaway.** Both syntheses converge on direction-holds-with-operating-frame-qualifications: the metaquestion answer ("uplift-of-gsd-2 is the right shape") persists, but the R-mix is narrower and more decomposed than `DECISION-SPACE §1.8`'s original R2-base + R2+R3 hybrid framing assumed. The substantive findings — Pi vendoring entanglement; extension-surface plurality (4 parallel subsystems); two-engine workflow architecture; release/breaking-change machinery-vs-practice gap; docs-vs-source drift class; telemetry/observability/security/trust centrality; B4 split holding; R3 under-evidenced; R2 viable with substantial caveats — converge across both syntheses (per §1).

The interpretive divergences are three-shaped (per §2):

1. **R4 weighting — substantive interpretive-disposition-timing divergence.** Codex declares operating-frame shift at synthesis stage: *"shifts the operating frame from 'R2 base unless infeasible' toward 'R2+R4 mix unless the needed surface requires core/Pi entanglement'"* (`SYNTHESIS-CROSS §0` OFS-1). Claude preserves R2 base + names R4-inclusion as a "net widening the operating frame should absorb" with explicit deferral to incubation: *"Whether this changes second-wave-scoping shape is incubation-checkpoint work"* (`SYNTHESIS §2.1` net read). **Load-bearing for incubation starting position** — codex's read has incubation operate under R2+R4-mix-as-already-shifted-frame; Claude's read has incubation evaluate whether-to-shift. Different disposition shapes. (Both name R4-elevation; the divergence is at the operating-frame disposition-timing level, not the inclusion level.)
2. **R5 framing — register divergence at common operational endpoint.** Codex *"no longer merely a cancellation bucket"* (`SYNTHESIS-CROSS §0` OS-2); Claude *"not first-wave-decidable; requires comparison frame"* (`SYNTHESIS §2.1` R5). Both converge operationally on deferring R5 evaluation pending the deferred competitor-landscape probe (`framing-widening §9` item 3); the divergence is read-not-disposition.
3. **Synthesis register/length — artifact-shape divergence.** Claude 609-line dense-deliberative with framing-widening vocabulary applied throughout + F1-F8 numbered findings stratification + §1.8 substrate-richness methodological observation + §2.5 design-shape candidates table. Codex 207-line compact-directive with operationally crisp §5 recommendations ("Pick a first second-wave target that tests the frame cheaply"; "Avoid starting with Pi seam refactoring or deterministic release engines"). Affects how incubation reads each.

Project-anchoring (six-context plurality) is interpretive at load-bearing position and is **Logan-disposed** at incubation per `framing-widening §3.3` + `SYNTHESIS §2.4` + `SYNTHESIS-CROSS §2.4`. Confidence: medium-high on direction-holds; medium-high on R4 as substantive-disposition-timing (not register); high on R5 as register-with-converged-operational-endpoint; medium on R-mix narrowing shape; medium-low on context-anchoring (synthesis cannot dispose).

**Scope.** This comparison integrates two landed syntheses. It does not re-synthesize from W1 evidence; the syntheses already integrate slice outputs + audits + side-investigations + framing-widening + DECISION-SPACE.md + INITIATIVE.md. The comparison's value-add is the paired-review integration for incubation-stage utility, not new substantive findings beyond what the syntheses carry.

**In-session collaboration caveat.** Per D5a, this comparison is drafted in-session (Claude-with-Logan) rather than by an independent third synthesizer. The M1 paired-review's full epistemic property — cross-vendor independence at integration stage — is partially honored: the two syntheses being compared are independent; the comparison itself is Claude-in-session. §6 expands this caveat.

---

## §1. Convergent findings

Findings both syntheses reach independently from the audited W1 evidence base. Per-finding format: claim → side-by-side citations → tight "Bears on §5.X axis" pointer (integration load lives in §5 multi-axis structure per `2026-04-28-comparison-drafting-decisions.md` DC3). **High-confidence inputs for incubation deliberation.**

### §1.1 Pi vendoring + clean-seam tension; ADR-010 proposed-not-implemented

- **Claim.** gsd-2 is a vendored modified Pi fork with substantial GSD-authored code embedded inside `pi-coding-agent` (~79 files per ADR-010); the proposed clean-seam refactor (`@gsd/agent-core`, `@gsd/agent-modes`) is `Status: Proposed`, not implemented; no reliable file-by-file provenance distinction without per-file source reading.
- **Same-vendor (Claude).** F1 in §0 stratification (operating-frame-shift; high confidence); §1.1 cross-slice pattern integration; §2.1 R1 evidence base.
- **Cross-vendor (codex).** §0 OFS-2 (operating-frame-shift; high confidence); §1.1 + §2.1 R1 caveat ("not cleanly 'GSD on top of Pi SDK'... vendored modified Pi fork plus GSD glue plus bundled extensions"); §2.1 R1 cost analysis.
- **Bears on.** §5.1 metaquestion integration (does direction hold given Pi-vendoring entanglement?) + §5.2 R1-R5 mix integration (R1 cost-model + whether R2 work targeting Pi-vendored internals counts as R2 or as R1-shaped).

### §1.2 Extension-surface plurality — at least four parallel subsystems

- **Claim.** gsd-2 has at least four parallel extension subsystems with separate APIs, discovery, and dispatch: (1) pi-coding-agent extensions; (2) GSD ecosystem extensions (`.gsd/extensions/` via `GSDExtensionAPI` wrapper); (3) workflow plugins (`workflow-plugins.ts` + 25 bundled templates; four execution modes); (4) skills (`skill-manifest.ts`/`skill-discovery.ts` with per-unit-type allowlists).
- **Same-vendor (Claude).** F2 in §0 stratification (high confidence); §1.3 cross-slice pattern; §2.1 R2 evidence base; §2.5 design-shape candidates table mapping to four-act plurality.
- **Cross-vendor (codex).** §0 OFS-1 ("R2 surfaces are substantive and product-load-bearing"); §1.3 ("Extension viability is real, but 'extension' is plural") with independent source spot-checks (`ecosystem/loader.ts:1-18, :45-95`; `ecosystem/gsd-extension-api.ts:1-10, :40-50`; `workflow-plugins.ts:1-14, :120-221`; `skill-manifest.ts:1-16, :25-43`); §3.3 resolution as surface plurality.
- **Bears on.** §5.2 R1-R5 mix integration (R2 viability decomposes by target subsystem; R-mix decisions should specify which subsystem any uplift work targets) + §5.4 side-probe triggers (temporal-stability probe across the four subsystems per `framing-widening §9` item 5).

### §1.3 Two-engine workflow architecture — markdown-phase prompt-dispatch vs yaml-step deterministic

- **Claim.** gsd-2's automation layer carries at least two architecturally distinct workflow engines: `markdown-phase` (prompt-dispatch; lightweight `STATE.json`; no executor-owned phase-advance writes; commands in markdown body are agent instructions, not executor steps), and `yaml-step` (graph-backed; deterministic `GRAPH.yaml` mutation; dependency-aware; structured `context_from`; shell-command verification via `spawnSync`).
- **Same-vendor (Claude).** F4 in §0 stratification (high confidence); §1.2 cross-slice pattern integration; §2.5 candidates table with W2-dive verification status per candidate.
- **Cross-vendor (codex).** §1.2 ("Agent-prompted workflow templates are not deterministic release engines") with independent source spot-checks at `commands-workflow-templates.ts:424-508` and `custom-workflow-engine.ts:90-226`; §2.1 R4 evidence base.
- **Bears on.** §5.2 R1-R5 mix integration (markdown-phase determinism boundary partitions which uplift candidates fit which engine + when to reframe as R4 orchestrate-from-outside vs R2 extension).

### §1.4 Release/breaking-change machinery-vs-practice gap (load-bearing direction-shifter)

- **Claim.** gsd-2 has elaborate breaking-change *machinery* (CONTRIBUTING signposting requirement; PR-template breaking-changes checkbox; bundled `api-breaking-change` workflow with staged deprecate-then-remove; semver detection in `generate-changelog.mjs` recognizing `BREAKING CHANGE:` / `!:`; Keep-a-Changelog format with Deprecated/Removed sections) but observed practice diverges (zero `BREAKING CHANGE`-marked commits in shallow 6-month window of ~2200 commits / 34 tags; recent removals like Anthropic OAuth in v2.70.0/v2.74.0 lack visible pre-deprecation in shallow window; experimental preferences explicitly waive deprecation cycle; rapid release cadence ~6.2 tags/visible-week, average tag-gap 0.160 weeks).
- **Same-vendor (Claude).** F3 in §0 stratification (medium-high confidence; "load-bearing direction-shifter for any R2/R3 strategy depending on stable extension surfaces"); §1.7 cross-slice pattern integration; §3.1 contradiction resolution at synthesis stage; D3 cross-finding flag from slice 5 audit §5 integrated here.
- **Cross-vendor (codex).** §0 OFS-3 ("Release and long-horizon machinery exists, but often as composable primitives, prompt-mediated workflow templates, or gsd-2's own repo practice rather than deterministic user-project release infrastructure"; medium-high confidence); §3.4 ("machinery exists but should not be treated as enforced culture"; recent rapid tag cadence makes the pattern direction-relevant).
- **Bears on.** §5.1 metaquestion integration (load-bearing direction-shifter; weakens R2 stability claims for specific surfaces) + §5.2 R-mix integration (R2 + R3 viability assessment for any work depending on stable extension surfaces) + §5.4 side-probe triggers (deeper-history sampling for Claude O3 unresolved-question — feature vs transition state). **Note carried into §5.1: the gap weakens-but-does-not-flip the metaquestion answer; both syntheses converge on direction-holds-with-qualifications.**

### §1.5 Docs-vs-source divergence as a recurring class

- **Claim.** README/docs frequently overstate or simplify behavior that source actually gates by preference, mode, or environment. Multiple cross-slice-verified instances: RTK gating (README claims provisioned managed RTK; source gates via `experimental.rtk` default-disabled per `cli.ts:167-178`); reassess-after-slice (README presents adaptive replanning; source defaults dedicated reassessment off); team-mode `git.isolation` (docs `"worktree"`; source `MODE_DEFAULTS.team.git.isolation = "none"`); boundary-map (GSD-WORKFLOW.md schema includes section; migrator at `migrate/writer.ts:140` skips per D004); CI/CD pipeline (docs imply automatic Dev→Test→Prod; workflow source is `workflow_dispatch`-gated); verification scope (README presents general "automated verification"; source narrows to `execute-task` units).
- **Same-vendor (Claude).** F5 in §0 stratification (high confidence — class, not single instance); §1.5 cross-slice pattern integration; §3.1-§3.5 contradictions; §3 "Pattern across §3.1-§3.5: the docs-vs-source-drift class".
- **Cross-vendor (codex).** §1.5 ("Documentation/source drift is recurrent but bounded, not catastrophic"; high confidence on recurrence, medium on severity); §3.1-§3.5 contradictions trace.
- **Bears on.** §5.2 R-mix integration (any R-strategy depending on docs-trust requires source verification before extension) + §4 methodological observations (synthesis confidence calibration on docs-anchored vs source-grounded claims).

### §1.6 R2 viable but with substantial caveats — both at medium-high confidence

- **Claim.** R2 (extension) is viable; the surface is richer than `DECISION-SPACE §1.8`'s framing assumed (per §1.2); but R2 work targeting Pi-vendored internals is functionally R1-shaped (per §1.1), markdown-phase plugins are prompt-dispatch only (per §1.3), and stability claims for any specific surface require source verification (per §1.4 + §1.5). R2 base persists as working hypothesis but with the mix narrower and more decomposed than originally assumed.
- **Same-vendor (Claude).** §2.1 R2 sub-section ("medium-high confidence; substantive evidence both supporting and qualifying"); F6 evidence-base integration.
- **Cross-vendor (codex).** §2.1 R2 sub-section ("viable but surface-specific, high confidence"); §0 OFS-1 ("R2+R4 mix unless the needed surface requires core/Pi entanglement").
- **Bears on.** §5.2 R1-R5 mix integration (R2-base persists as working hypothesis within widened R1-R5 space; R-strategy reclassification not licensed but mix narrows by subsystem). **Note: this is the convergent R2-viability finding; the divergence on R4-weighting in operating-frame-disposition-timing is at §2.1.**

### §1.7 Telemetry/observability/security/trust as central design surface

- **Claim.** Observability/security/trust is structurally central, not peripheral: worktree telemetry; journal (daily-rotated JSONL with 22 schema versions); forensics; doctor; debug sessions; metrics ledger; cost/budget controls; `/gsd export --html` reports; hook trust marker (`.pi/hooks.trusted`); write-gate state-machine; tool-policy `UnitContextManifest`; exec-sandbox with timeout/byte caps; secret scanning; destructive-command classifier; project-trust gating for ecosystem extensions.
- **Same-vendor (Claude).** F8 + F9 in §0 stratification (high confidence each); cross-slice watchlists across slices 1-5; capabilities probe §A.9 + §A.10 integrated.
- **Cross-vendor (codex).** §1.4 cross-slice pattern ("observability/security-heavy enough that uplift should use those surfaces, not bypass them") with explicit cross-slice citations; medium-high confidence.
- **Bears on.** §5.4 side-probe triggers (telemetry/observability as design-surface per `framing-widening §9` item 12 — whether design-shape candidates touching observability are in v1 scope or deferred).

### §1.8 B4 split held — slice 5 abstract long-horizon-relevance interpretation belongs at synthesis

- **Claim.** Slice 5 produced concrete-observable patterns (release cadence, breaking-change machinery, 17-feature inventory, prod/dev distinctions) and explicitly deferred abstract long-horizon-relevance interpretation to synthesis. Slice 5 audit §3 confirmed compliance; both syntheses integrated abstract interpretation at §2.3-§2.6 level using cross-slice context.
- **Same-vendor (Claude).** §2.6 dedicated B4-resolution section (split held; high confidence).
- **Cross-vendor (codex).** §2.6 dedicated B4-resolution section (split held; high confidence on split, medium on interpretation).
- **Bears on.** §5.1 metaquestion integration (long-horizon-relevance interpretation lives at synthesis-and-comparison level + concretizes for §5.3 six-context anchoring) + B4 pilot-disposition resolution: "split held; do not unsplit" per `DECISION-SPACE §1.14`.

### §1.9 R3 (upstream-PR-pipeline) is under-evidenced — both medium-low confidence

- **Claim.** R3 viability is not first-wave-decidable. Local CONTRIBUTING.md is structurally rich (issue-first; ADR/RFC; conventional commits; extension-first principle); recent merge commits visible (PRs #5080-#5053 in last day of visible history); but slice 4 Q5 contribution-culture probe failed (`gh` API errors); maintainer responsiveness, review latency, external-contributor acceptance unverified at first-wave depth.
- **Same-vendor (Claude).** §2.1 R3 sub-section (medium-low; "probe was light by design; deeper investigation deferred"); §5.3 explicit recommendation to dispatch deep contribution-culture probe before R3-dependent design.
- **Cross-vendor (codex).** §2.1 R3 sub-section ("plausible but under-evidenced, medium-low confidence"); §0 OS-1 ("R3 is under-evidenced... live GitHub contribution probe failed"); §5 recommendation: "do not assume for load-bearing delivery."
- **Bears on.** §5.4 side-probe triggers (deferred contribution-culture deep probe per `DECISION-SPACE §1.15` B5 / `framing-widening §9` item 6 — pre-vs-post critical path for second-wave-scoping commits to R3-dependent design).

*(Note: the predecessor draft surfaced "tightly-interleaved release/workflow/artifact infrastructure" as a tenth convergent finding; per `2026-04-28-comparison-drafting-decisions.md` DC2, this is re-categorized as Claude-unique surfacing — `SYNTHESIS.md §1.4` carries it as a dedicated cross-slice pattern but codex `SYNTHESIS-CROSS.md` does not directly state the interleaving claim. Moves to §3 asymmetric coverage.)*

---

## §2. Divergent findings

*Sections marked **Logan-adjudication** in this section's items are the load-bearing decisions for incubation. The comparison surfaces both reads + the evidence behind each + what the divergence implies; Logan disposes which read incubation operates under. Sections marked **Surfacing-only** are recorded for completeness but converge operationally; no adjudication is required for incubation to proceed.*

Three divergence-types per `2026-04-28-comparison-drafting-decisions.md` DC4 typology: §2.1 substantive interpretive-disposition-timing (R4 weighting); §2.2 register divergence at common operational endpoint (R5 framing); §2.3 artifact-shape divergence (synthesis register/length).

### §2.1 R4 weighting — substantive interpretive-disposition-timing divergence — **Logan-adjudication**

- **The divergence.** Both syntheses elevate R4 (orchestrate-without-modifying) above its `DECISION-SPACE §1.8` original-framing-tier. The substantive divergence is **when** the operating-frame shift happens — at synthesis stage (codex) vs at incubation stage (Claude).
- **Codex read — synthesis-stage shift.** `SYNTHESIS-CROSS §0` OFS-1 reads as declarative-not-conditional: *"shifts the operating frame from 'R2 base unless infeasible' toward 'R2+R4 mix unless the needed surface requires core/Pi entanglement.'"* §2.1 R4 sub-section: *"strongly viable, medium-high confidence."* §2.5 design-shape candidates names R4 as *"Strong for release/RC/staging because existing release templates are prompt-mediated, not deterministic engines"*. §5 recommendation #3 elevates this to first-class checkpoint disposition: *"Treat R4 as first-class in the checkpoint. The evidence base repeatedly shows composable primitives and headless/machine surfaces; forcing these into R2 would be a silent-default narrowing."* The cumulative shape is: incubation-starting-position is R2+R4-mix-as-already-shifted-frame.
- **Claude read — synthesis-defers-shift-disposition.** `SYNTHESIS.md §2.1` net read on R-strategy mix: pre-decided in the operating frame is R2 base + primary; R1 as fallback. Both persist as working hypotheses. R4-inclusion is named as a "net widening the operating frame should absorb" but explicit deferral on shift-disposition: *"Whether this changes second-wave-scoping shape is incubation-checkpoint work."* The cumulative shape is: incubation-starting-position is R2-base-with-R4-net-widening-on-the-table-for-disposition; incubation evaluates whether-to-shift the operating frame.
- **What both agree on (zone of convergence).** R4 is no longer a cancellation bucket; R4 surfaces are substantive (headless, query, RPC, MCP, hooks, workflow templates per `framing-widening §1.4`); R4 is operationally relevant for release/RC/staging where existing release templates are prompt-mediated rather than deterministic engines (per §1.3 + §1.4 of this document). Both reach R4-elevation; the divergence is purely about disposition-timing.
- **Why the divergence is substantive, not register.** The two reads produce **different starting positions for incubation**. Codex's read has incubation operating *under* a shifted frame (R2+R4-mix); the question becomes "given this shifted frame, what's the first second-wave target." Claude's read has incubation *evaluating* whether to shift; the question becomes "should the operating frame shift, and on what evidence." Same downstream R-mix outcomes are reachable from either starting position, but the deliberation shape differs and the downstream commits differ in their evidence-load.
- **Possible reasons for the divergence (interpretive).** (i) Same-vendor reads catch register more readily and may default to register-preserving framing for already-stated operating-frame commitments per `METHODOLOGY.md` M1; cross-vendor reads catch substance more readily and may not register the "synthesis-defers-disposition" methodological discipline. (ii) The framing-widening §3.3 + §10 anti-patterns ground may have read more strongly into Claude's synthesis (deferring shift-disposition to incubation) than codex's (which absorbed framing-widening §1 R-strategy mix but read §3.3 disposition-discipline less deeply). (iii) Codex's brevity (207 lines vs 609) may reflect a directive register that compresses conditional structure into declarative form. None of these explanations is verifiable without re-running the syntheses; surfacing them as plausible accounts for the comparison author's transparency, not as adjudications.
- **Implication for incubation (Logan-adjudication).** Two operationally distinguishable starting positions:
  - **(a) Operate-under-shifted-frame.** Incubation enters with R2+R4-mix as the operating frame. First second-wave target selection asks "which of the four extension/configuration/orchestration surfaces (per `SYNTHESIS-CROSS §5` recommendation #2) carries the cheapest viable test." R4 is first-class; R2-targeting-Pi-vendored-internals is partitioned out by §1.1 + §1.6.
  - **(b) Evaluate-whether-to-shift.** Incubation enters with R2-base-+-R4-net-widening on the table. First second-wave target selection asks "given the convergent findings + Logan's six-context anchoring (per §5.3), does the operating frame shift, and on what evidence." R4 is on-the-table; the shift is contingent on the context-anchoring + first-target-shape.
  - Logan disposes which read incubation operates under. The disposition is load-bearing because it shapes second-wave-scoping question structure, not just R-mix decomposition.
- **Salient situational parameters that might modify this adjudication.** (i) If Logan reads the codex declaration as "premature-collapse-of-disposition-discipline" (per `framing-widening §3.3` "no synthesis pre-decides incubation"), Claude's read holds and the operating frame remains under-shift-evaluation. (ii) If Logan reads the codex declaration as "evidence-already-licensed-the-shift" (the four-extension-subsystems plurality + R4 surface substantiveness make R2-base-as-default a silent-default narrowing), codex's read holds and the operating frame is shifted. (iii) If incubation's pre-vs-post critical-path partitioning per `framing-widening §9` produces context-anchoring before R-mix narrowing (per `SYNTHESIS §2.4` + `SYNTHESIS-CROSS §2.4` recommendation), the disposition-timing question may resolve at context-anchoring rather than at synthesis-vs-incubation.
- **Confidence on the comparison-author's framing of this divergence.** Medium-high. The substantive-not-register characterization is grounded in the verbatim contrast (declarative-vs-explicitly-deferred). The plausibility of the three reason-accounts is medium; verifying them would require re-running the syntheses with controlled framing-conditions, which is not in scope for this comparison.

### §2.2 R5 framing — register divergence at common operational endpoint — **Surfacing-only**

- **The divergence.** Both syntheses elevate R5 (replacement-informed-by) above its `DECISION-SPACE §1.8` original "cancellation bucket" framing. The divergence is **how** each surfaces the elevation.
- **Codex read.** `SYNTHESIS-CROSS §0` OS-2: *"R5 is not demanded by first-wave evidence, but it is no longer merely a cancellation bucket. If incubation decides the needed target is Context F-heavy or non-coding/product-lifecycle-heavy, gsd-2 may be better used as a reference plus external orchestrated component than as the object modified."* Confidence: medium. §2.1 R5 sub-section: *"open option, not first-wave recommendation, medium confidence... It should not be collapsed to 'cancel'; it could mean 'use gsd-2 as a reference and maybe component, build a sibling for the missing semantics.'"* §5 recommendation #6: *"If R5 becomes live, dispatch a competitor/sibling-harness landscape probe before design."*
- **Claude read.** `SYNTHESIS.md §2.1` R5 sub-section: not first-wave-decidable; requires comparison frame. R5 disposition awaits the deferred competitor-landscape probe (`framing-widening §9` item 3) + Logan's context-anchoring read.
- **Operational endpoint.** Both converge on: (i) R5 is not first-wave-recommended; (ii) R5 is not collapsed to cancellation; (iii) R5 evaluation requires the deferred competitor-landscape probe before design; (iv) R5 becomes live conditional on context-anchoring (Context F-heavy or non-coding/product-lifecycle per codex; Logan's read per Claude). Same operational endpoint; same downstream side-probe trigger; same context-anchoring conditional.
- **Why surfacing-only.** Codex's "no longer merely a cancellation bucket" is more declaratively elevational; Claude's "requires comparison frame" is more methodologically conditional. The reads converge operationally so the divergence does not require Logan adjudication to proceed; incubation reads R5 the same way under either read.
- **Possible reasons for the register divergence (interpretive, optional reading).** Symmetric to §2.1: same-vendor caught the methodological-conditional shape; cross-vendor caught the substantive-elevation shape. Together they triangulate "elevated-but-conditional" more reliably than either alone — an instance of M1 paired-review's intended epistemic property in action (per §4.2 below).
- **Implication for incubation.** Carries to §5.4 side-probe triggers as: deferred competitor-landscape probe is a pre-vs-post critical-path question for second-wave-scoping commits to R5-dependent design.

### §2.3 Synthesis register/length — artifact-shape divergence — **Surfacing-only**

- **The divergence.** Claude 609-line dense-deliberative; codex 207-line compact-directive. ~3× length ratio with structurally different shapes.
- **Claude shape.** Framing-widening vocabulary applied throughout (R1-R5 mix, six-context plurality, four-act plurality, framing-widening §3.3 disposition-discipline). F1-F8 numbered findings stratification at §0 with explicit confidence levels per finding. §1.8 substrate-richness methodological observation surfaces a second-order observation about the evidence base. §2.5 design-shape candidates table maps to four-act plurality with W2-dive-verification status per candidate. §1.4 cross-slice pattern integration surfaces release/workflow/artifact infrastructure tight-interleaving (carried to §3.1 of this document). §3 contradictions trace the docs-vs-source-drift class with synthesis-stage resolutions per contradiction. §5.3 deeper-history sampling recommendation. The cumulative register is dense-deliberative with strong methodological-discipline-foregrounding.
- **Codex shape.** Operationally crisp §5 recommendations: *"Pick a first second-wave target that tests the frame cheaply. Good candidates: effective-state visibility; a release metadata/checklist artifact linked to milestones; a Context A/F long-arc decision trace skill/workflow; or a headless orchestration recipe. Avoid starting with Pi seam refactoring or deterministic release engines."* §0 stratification by operating-frame-shift / operating-frame-confirm / open-at-synthesis-stage. §2.1 R-strategy assessments more compact per strategy. §6 "cross-vendor framing-leakage caveat" foregrounds the framing-widening's R1-R5/six-context as inputs-not-observed-facts. The cumulative register is compact-directive with first-target-selection-foregrounding.
- **Why surfacing-only.** No adjudication required: Logan reads each on its own terms during incubation. The divergence is structurally informative for incubation reading-experience, not deliberation-input.
- **Implication for incubation reading-experience.** (i) Claude's synthesis takes longer to read but exposes more conditional-structure scaffolding and more methodological-discipline grounding; useful for "how should incubation deliberate." (ii) Codex's synthesis reads faster and produces more concrete first-target candidates; useful for "what should incubation deliberate about first." (iii) The two together form a useful pairing: codex compresses to actionable shape; Claude expands to deliberative shape. (iv) For Logan time-budget at incubation: codex §5 + this comparison §5 may carry the operational load; Claude §0 + §2.5 + §3 may carry the methodological load; full re-read of either is not strictly required for incubation if the comparison's §1 + §5 axes hold up.
- **Caveat.** Length-ratio interpretation is loose. Codex's compactness is partly due to (a) cross-vendor independence constraint not requiring re-narration of dispatching-project's framing vocabulary; (b) same-vendor's tendency to mirror the dispatching-project's register-density per `METHODOLOGY.md` M1. The artifact-shape divergence reflects vendor-specific register tendencies more than substantive deliberation difference; readers should treat both shapes as legitimate synthesis-shapes for the same evidence base.

---

## §3. Asymmetric coverage

*Findings or observations one synthesis surfaces that the other does not directly state. Asymmetric coverage is a completeness signal — not divergence (both syntheses had access to the same audited evidence base; either could in principle have surfaced the missed item). Per `2026-04-28-comparison-drafting-decisions.md` DC2, an item qualifies for §3 if it appears load-bearing in one synthesis and is not directly stated in the other (paraphrase + nearby reach is acceptable; verbatim restatement is not required).*

### §3.1 Claude-unique: tightly-interleaved release/workflow/artifact infrastructure

- **The surfacing.** `SYNTHESIS.md §1.4` carries as a dedicated cross-slice pattern: release/workflow/artifact infrastructure interleaves tightly enough that release engineering, workflow templates, and artifact lifecycle cannot be cleanly partitioned for uplift work. Concrete cross-slice instances per `SYNTHESIS.md §1.4`: (i) workflow plugins include release-template-shaped instances (api-breaking-change, hotfix); (ii) `generate-changelog.mjs` reads from artifact directories produced by milestone/slice/task lifecycle; (iii) release templates are markdown-phase plugins (per §1.3 of this document); (iv) breaking-change machinery (§1.4 of this document) operates partly through PR-template hooks, partly through CONTRIBUTING signposting, partly through workflow-plugin templates, partly through `BREAKING CHANGE:` semver-detection in release scripts.
- **What codex surfaces nearby but does not directly state.** `SYNTHESIS-CROSS §1.2` distinguishes markdown-phase prompt-dispatch from yaml-step deterministic; `SYNTHESIS-CROSS §3.4` notes machinery-vs-practice gap; `SYNTHESIS-CROSS §1.3` decomposes extension surface plurality. Codex reaches the components but does not integrate them into the "tight-interleaving precludes clean partitioning" claim.
- **Why this matters for incubation.** Bears on §5.2 R-mix decisions: any R2/R3/R4 work targeting release machinery cannot specify "extend the release engine" without specifying which subsystem (workflow plugin, release template, semver detection, artifact lifecycle, PR-template hook) is the actual extension target. Bears on §5.4 side-probe triggers: a release-shape probe that tests one subsystem in isolation may produce misleading viability signal because the subsystems compose in production.
- **Confidence.** Medium. Claude's interleaving claim is grounded in cross-slice integration; codex's component-decomposition is grounded in source spot-checks. Both are valid; the interleaving claim is the integrative read. Whether incubation should treat it as binding depends on whether release machinery is in-scope for first-second-wave-target.

### §3.2 Claude-unique: substrate-richness as methodological observation

- **The surfacing.** `SYNTHESIS.md §1.8` (referenced from §0 as a methodological observation): the gsd-2 evidence base is substrate-rich enough that synthesis stratification needs explicit confidence-per-finding (F1-F8 with confidence labels) rather than uniform-confidence claims, because the evidence supports different findings to different depths. This is a second-order observation about the evidence-base shape, not a first-order finding.
- **What codex surfaces nearby.** `SYNTHESIS-CROSS §6` confidence-and-limits stratifies by claim-type (high on source-verifiable structural; medium-high on cross-slice patterns; medium-or-medium-low on operating-frame implications). The stratification is substantively similar but presented as confidence-on-claims-this-synthesis-makes rather than as substrate-richness-licenses-stratified-confidence.
- **Why this matters for incubation.** Bears on §4 methodological observations (M1 in action) more than on §5 incubation-axes: the substrate-richness observation is calibration metadata for how to read both syntheses, not a finding about gsd-2.
- **Confidence.** Medium. The observation is well-grounded; the divergence is whether it's surfaced as a methodological observation (Claude) or absorbed into confidence-stratification (codex). Either approach is legitimate.

### §3.3 Codex-unique: explicit cross-vendor framing-leakage caveat

- **The surfacing.** `SYNTHESIS-CROSS §6` final bullet: *"Cross-vendor framing-leakage caveat: I am cross-vendor relative to the same-vendor synthesis, but I am still reading through the dispatching project's framing-widening vocabulary. The R1-R5 and six-context frames are useful inputs, not observed facts in gsd-2. Where they overfit the evidence, incubation should loosen them rather than treat this synthesis as authority."*
- **What Claude surfaces nearby.** Claude's `SYNTHESIS.md` carries framing-widening vocabulary throughout but does not explicitly flag framing-leakage as a methodological caveat. The closest analogue is Claude's deferral-of-shift-disposition pattern (§2.1 of this document), which preserves disposition-discipline but does not directly address whether the framing vocabulary itself is over-fitted.
- **Why this matters for incubation.** Bears on §4 methodological observations and on §5.3 six-context anchoring: codex's caveat is a check against treating R1-R5 / six-context as observed facts in gsd-2 rather than as deliberation-frames Logan brought in. Important for incubation if Logan revises the framing-widening (per `framing-widening §9` deferred items 16-17 around frame-revision triggers) — both syntheses should then be re-read with the revised frame, and the revision is licit per codex's caveat.
- **Confidence.** High. Codex's caveat is substantively important and methodologically clean. Claude could-have-but-did-not surface this; surfacing it cross-vendor is exactly the M1 paired-review property at work (cross-vendor catches the same-vendor's methodological blindspot).

### §3.4 Codex-unique: explicit "do not collapse R5 to cancel" framing

- **The surfacing.** `SYNTHESIS-CROSS §0` OS-2 + §2.1 R5: *"It should not be collapsed to 'cancel'; it could mean 'use gsd-2 as a reference and maybe component, build a sibling for the missing semantics.'"*
- **What Claude surfaces nearby.** Claude's `SYNTHESIS.md §2.1` R5 surfaces R5 as not-first-wave-decidable but does not explicitly carry the "use gsd-2 as a reference and maybe component, build a sibling" reframe. The reframe is operationally available under Claude's read but is not explicitly named.
- **Why this matters for incubation.** Bears on §5.2 R-mix integration + §5.4 side-probe triggers: the explicit reframe makes R5's content concrete (reference-plus-sibling-with-missing-semantics) rather than abstract (replacement-informed-by). Useful for incubation when evaluating whether R5 becomes live.
- **Confidence.** Medium-high. Codex's reframe is substantively useful; treating it as binding would over-commit (it's one shape of R5; other shapes exist). Best handled by incubation as one concrete option within R5.

### §3.5 Codex-unique: stronger emphasis on first-target-selection methodology

- **The surfacing.** `SYNTHESIS-CROSS §5` recommendations #2 + #5: ask which surface carries the first concrete target before asking R-mix decomposition; pick a first second-wave target that tests the frame cheaply with concrete candidates (effective-state visibility; release metadata/checklist artifact; Context A/F long-arc decision trace skill/workflow; headless orchestration recipe). Concrete avoid-list: Pi seam refactoring; deterministic release engines.
- **What Claude surfaces nearby.** Claude's `SYNTHESIS.md §2.5` design-shape candidates table maps shapes to four-act plurality but does not as crisply foreground "test the frame cheaply" as the methodological selection-criterion. Claude's §5 (recommendations) is more deliberative than directive.
- **Why this matters for incubation.** Bears on §5.2 R-mix integration: codex's selection-methodology gives incubation an actionable shape for first-target choice. Claude's table gives more candidates; codex gives selection criterion. Together they triangulate.
- **Confidence.** High. Codex's directive shape is substantively useful at incubation. Claude's deliberative shape is methodologically appropriate for synthesis stage. Both are legitimate; incubation reads them together.

### §3.6 Codex-unique: explicit `prefs` / `headless query` / MCP tools probe candidate

- **The surfacing.** `SYNTHESIS-CROSS §4` open question #2 names the concrete probe: *"What resolves: source/run check of `prefs`, `headless query`, or MCP tools for complete effective settings."*
- **What Claude surfaces nearby.** Claude's `SYNTHESIS.md` surfaces effective-state-visibility as a candidate target but does not name `prefs`/`headless query`/MCP tools as the probe shape.
- **Why this matters.** Bears on §5.4 side-probe triggers: codex's named probe is concrete enough to dispatch; Claude's framing requires further specification before dispatch. Useful when incubation commits to first-target work.
- **Confidence.** High on the surfacing. Whether `prefs` etc. are the right probe shape is a downstream design question.

### §3.7 Symmetry note

- Both syntheses surface roughly equivalent substantive findings on Pi vendoring, extension plurality, two-engine architecture, breaking-change machinery-vs-practice, docs-vs-source drift, telemetry/observability/security centrality, and B4 split (§1.1-§1.5, §1.7-§1.8 of this document). The asymmetric coverage is concentrated in (a) Claude's integrative observations (§3.1 interleaving + §3.2 substrate-richness) and (b) codex's methodological caveats and operationalizations (§3.3 framing-leakage caveat + §3.4 R5-reframe + §3.5 first-target-methodology + §3.6 named probe). The asymmetry is **complementary, not contradictory**: same-vendor goes deep on cross-slice integration; cross-vendor goes wide on methodological framing + concrete operationalization. Consistent with M1 paired-review's intended epistemic property.

---

## §4. Methodological observations (M1 in action)

*Per `METHODOLOGY.md:104-115` + `DECISION-SPACE §1.13` (B3): cross-vendor reads catch substance more readily; same-vendor reads catch register more readily. This section records what the paired-review process itself revealed during this comparison drafting — not findings about gsd-2, but findings about the synthesis methodology.*

### §4.1 M1 paired-review property — observed-as-claimed

- **What was claimed.** Same-vendor catches register more readily; cross-vendor catches substance more readily.
- **What was observed.** Mixed. Some claimed-properties held; some inverted; one new property emerged.
  - **Held — register vs substance asymmetry.** §3.3 framing-leakage caveat is methodological-register Claude could-have-but-did-not surface; codex did surface it. Consistent with cross-vendor catching same-vendor's methodological blindspot. §2.3 length/register divergence is consistent with same-vendor mirroring dispatching-project register-density.
  - **Inverted — methodological-discipline preservation.** §2.1 R4 disposition-timing: Claude (same-vendor) preserved the framing-widening §3.3 disposition-discipline (synthesis defers shift-disposition to incubation); codex (cross-vendor) compressed to declarative shape. This inverts the claimed asymmetry — same-vendor caught the substantive methodological-discipline; cross-vendor missed it. Plausible explanation: same-vendor read framing-widening more deeply because it operates within the same dispatching-project context; cross-vendor read framing-widening as inputs-not-observed-facts (per §3.3 caveat) and may have been less attentive to the §3.3 disposition-discipline as a binding methodological commitment.
  - **Emerged — complementary asymmetric coverage.** §3.1-§3.6 show same-vendor going deep on cross-slice integration (§3.1 interleaving; §3.2 substrate-richness) and cross-vendor going wide on methodological caveats + concrete operationalization (§3.3-§3.6). This is a third pattern beyond "register vs substance" — depth-vs-breadth of integration shape, plausibly explained by same-vendor's deeper context-immersion vs cross-vendor's framing-leakage-resistance.
- **Implication for future paired-synthesis use.** The M1 claim should be refined to: "cross-vendor and same-vendor reads catch *different* substantive and methodological patterns; the asymmetry is empirically more complex than register-vs-substance and is plausibly mediated by context-immersion-depth." Future paired-synthesis dispatches should preserve cross-vendor independence (per `synthesis-spec.md`) but should not over-commit to "same-vendor=register / cross-vendor=substance" as a clean asymmetry. The observed pattern is more like: same-vendor goes deeper on context-anchored deliberative methodology; cross-vendor goes wider on framing-resistant operational methodology. Both are useful; both can miss what the other catches.
- **Confidence.** Medium. n=1 paired-synthesis observation; the inverted asymmetry on §2.1 may not generalize. Worth recording as a calibration data point, not as a claim about the methodology.

### §4.2 Convergent findings as robustness signal — observed-as-claimed

- **What was claimed.** Convergent findings across independent reads are higher-confidence inputs because they survived independent reading of the audited evidence.
- **What was observed.** §1's nine convergent findings (§1.1-§1.9) all carry concordant confidence levels across both syntheses (high or medium-high; one medium-low both for §1.9 R3 under-evidenced). The independent source spot-checks codex performed (per `SYNTHESIS-CROSS §1.2-§1.3` source citations) reach the same source-grounded conclusions Claude reached via cross-slice integration. Robustness signal holds.
- **Caveat.** Convergence on findings does not validate the framing-widening vocabulary used to articulate them. Per §3.3 (codex's framing-leakage caveat): both syntheses share the dispatching-project's R1-R5 + six-context framing; convergence within that framing does not test the framing itself. Robustness applies to "given this framing, both reads agree on these findings"; it does not apply to "the framing is correct."
- **Implication for incubation.** Convergent findings (§1) are higher-confidence-within-framing; if Logan revises the framing at incubation (per `framing-widening §9` deferred items 16-17), the convergent findings should be re-read against the revised framing. Most are robust to framing revision (Pi vendoring entanglement, four-extension-subsystems plurality, two-engine architecture are source-grounded structural facts); some depend on framing (R-mix narrowing, R3 under-evidenced are framing-shaped articulations of evidence).

### §4.3 Tier-comparison expectations check — preliminary observation

- **What was tracked.** Per `2026-04-28-tier-comparison-preliminary-findings.md` (deliberation log on GPT-5.5 medium vs high tier comparison), the W1 dispatch tested cross-vendor at GPT-5.5 high tier and the W3 dispatch is a same-vendor Claude Opus xhigh + cross-vendor codex GPT-5.5 high pairing.
- **What was observed.** Codex GPT-5.5 high produced a structurally-clean 207-line synthesis with substantive findings, source spot-checks, and methodological caveats. The synthesis quality is consistent with the tier-comparison preliminary expectation that GPT-5.5 high is sufficient for synthesis-stage cross-vendor work. Length compactness is consistent with codex's directive register; substantive depth is preserved despite compactness.
- **Caveat.** Single-observation; insufficient for a tier-comparison conclusion. Worth recording as a calibration data point for future cross-vendor dispatches.
- **Implication.** Cross-vendor dispatch tier selection (GPT-5.5 high) is licit for synthesis-stage paired-review work based on this observation. Future dispatches at higher tiers (where available) might catch additional methodological-discipline patterns Claude caught at xhigh; this is speculation, not evidence.

### §4.4 Framing-import drift — methodological observation surfaced during this drafting

- **What was observed during drafting.** The comparison author (Claude, in-session) initially reasoned about §0 anti-pattern self-checks by importing arxiv-sanity-mcp's project-specific anti-pattern checklist (from `AGENTS.md`) as if it were generic governance discipline applicable to gsd-2-uplift comparison reasoning. Logan corrected this: arxiv-sanity-mcp's anti-patterns are project-specific; gsd-2-uplift inherits its anti-pattern grounds from `framing-widening §0+§10`, `DECISION-SPACE §4`, `LONG-ARC.md` (generic anti-patterns that survive cross-project), `handoff §8`, and `METHODOLOGY.md` M1, not from arxiv-sanity-mcp's `AGENTS.md`.
- **Why this matters for the comparison.** The drift is a methodological-leak from the host-project (arxiv-sanity-mcp) into the staged-initiative (gsd-2-uplift). This is a `framing-widening §10` anti-pattern instance: importing host-project specifics into the staged-initiative reasoning frame. Recorded in `2026-04-28-comparison-drafting-decisions.md §4` for traceability.
- **Implication for the gsd-2-uplift initiative.** Migration trigger per `INITIATIVE.md §7` (when dedicated repo is created) is approaching readiness: the initiative content has matured to the point where host-project framing-import is a recurring failure mode. This is signal-to-Logan, not a disposition; Logan disposes whether/when to migrate.
- **Implication for the comparison.** This comparison's grounds are: `framing-widening` (operating-frame ground), `DECISION-SPACE` (R-strategy + paired-review), `INITIATIVE` (initiative scope), `synthesis-spec` (paired-synthesis triggers + downstream-utility), `METHODOLOGY.md` (M1 + B-patterns), `LONG-ARC.md` (generic anti-patterns), and the predecessor handoff. NOT arxiv-sanity-mcp's `AGENTS.md` or other host-project specifics.

### §4.5 Synthesis stratification methodology — observed converged

- **What was observed.** Both syntheses stratify findings by confidence + by operating-frame-bearing (Claude F1-F8 stratification with confidence labels per finding; codex §0 OFS / OFC / Open-at-synthesis-stage stratification). Different stratification axes; converged on the methodological commitment that synthesis findings need stratification.
- **Implication for paired-synthesis methodology.** Stratification is a robust methodological commitment that survived independent reading. Future synthesis dispatches should expect stratification to be the norm; un-stratified syntheses should be re-stratified at comparison stage if dispatched.
- **Confidence.** High on the observation. Whether the specific stratification axes are optimal is a downstream methodological question (deferred per `framing-widening §9` if it appears).

---

## §5. Integration for incubation-checkpoint

*Per `synthesis-spec.md:185-188` + `DECISION-SPACE §2.3`, this section integrates the comparison's findings into incubation-checkpoint-shaped axes. Multi-axis (not single-axis) per `framing-widening §3.3` disposition-discipline + `2026-04-28-comparison-drafting-decisions.md` DC0: incubation disposes; the comparison surfaces the deliberation surface across four axes the synthesis-spec + framing-widening identify.*

*This section feeds incubation; it does not pre-decide incubation's questions. Sections marked **Logan-adjudication** are the binding incubation-stage decisions; sections marked **comparison-author surfaces** are calibration metadata.*

### §5.1 Metaquestion integration — does direction hold?

- **The metaquestion.** Per `INITIATIVE.md §1` + `framing-widening §1.7` + `DECISION-SPACE §1.7`: "is uplift-of-gsd-2 the right shape for the harness goal" (vs alternative shapes per R1-R5).
- **What the comparison surfaces.** Both syntheses converge: direction holds with operating-frame qualifications (per §1.1-§1.9). Substantive findings supporting direction-holds: Pi vendoring entanglement is real but not identity-misaligning (§1.1); extension-surface plurality demonstrates substantive R2 viability across multiple subsystems (§1.2 + §1.6); two-engine architecture distinguishes deterministic vs prompt-mediated work (§1.3); telemetry/observability/security centrality means uplift uses existing surfaces rather than bypasses them (§1.7); B4 split holds (§1.8). Substantive findings narrowing direction-holds: release/breaking-change machinery-vs-practice gap (§1.4 — load-bearing direction-shifter); docs-vs-source drift class (§1.5); R3 under-evidenced (§1.9).
- **Net read on the metaquestion.** The metaquestion answer ("uplift-of-gsd-2 is the right shape") persists at medium-high confidence. The qualifications narrow scope (R-mix decomposes by subsystem; surface-stability requires source verification; R3-dependent design awaits deeper probe) but do not flip direction. Per `SYNTHESIS-CROSS §2.2` synthesis read: *"direction does not flip to 'do not engage gsd-2.' It does shift away from a simple R2-base story."* Per `SYNTHESIS §0` net read: direction holds with operating-frame-qualifications.
- **What incubation should ask (Logan-adjudication).**
  - **(a) Is the direction-holds-with-qualifications net read sufficient for proceeding to second-wave-scoping**, or is the qualification-load (release machinery-vs-practice gap + Pi vendoring entanglement + R3 under-evidenced) heavy enough to warrant re-evaluating direction at synthesis-aware-incubation?
  - **(b) Does the §1.4 release/breaking-change machinery-vs-practice gap shift the metaquestion answer for any specific context (per §5.3) where release-discipline is load-bearing?** Both syntheses flag this as direction-shifter for stable-extension-surface work; whether it actually shifts depends on first-target-shape.
- **Salient parameters.** (i) If Logan's context-anchoring (§5.3) is Context A/F-primary, the qualifications are mostly tractable (extension surfaces are usable; release machinery less load-bearing for individual research/reflective use). (ii) If Logan's context-anchoring is Context B/C-primary, the qualifications become more load-bearing (release machinery-vs-practice gap, R3 contribution-receptivity, surface-stability all matter more for team/enterprise deployment). Direction may hold under (i) more strongly than under (ii); but the comparison surfaces this; incubation disposes.
- **Confidence.** Medium-high on direction-holds-with-qualifications. The qualifications are well-grounded; their load-bearing-ness depends on context-anchoring.

### §5.2 R1-R5 mix integration — has the mix narrowed or shifted?

- **What the comparison surfaces.** R1-R5 mix has narrowed and decomposed regardless of operating-frame-disposition-timing (§2.1). Per-strategy reads converged across both syntheses:
  - **R1 (fork).** Viable but high-cost (per §1.1 Pi vendoring entanglement); fallback for narrow patches; not first-wave operating frame. Both syntheses converge.
  - **R2 (extension).** Viable but surface-specific (per §1.6 + §1.2). Decomposes across Pi extensions / GSD ecosystem extensions / workflow plugins / skills / hooks / MCP tools — six R2-shaped surfaces, not one. R2-targeting-Pi-vendored-internals is functionally R1-shaped (per §1.1 + §1.6). Both syntheses converge.
  - **R3 (upstream-PR-pipeline).** Plausible but under-evidenced; requires deferred contribution-culture deep probe before R3-dependent design (per §1.9 + `framing-widening §9` item 6). Both syntheses converge.
  - **R4 (orchestrate-without-modifying).** Strongly viable; substantive surfaces (headless, query, RPC, MCP, hooks, workflow templates per §1.7); first-class for release/RC/staging where existing release templates are prompt-mediated rather than deterministic engines (per §1.3 + §1.4). **Disposition-timing divergent (§2.1).**
  - **R5 (replacement-informed-by).** Live optionality, not first-wave-recommendation; conditional on context-anchoring + competitor-landscape probe (per §2.2 + `framing-widening §9` item 3). Both syntheses converge operationally.
- **R-mix shape going into incubation.** R1 fallback / R2 base-decomposed-by-subsystem / R3 conditional-on-probe / R4 elevated-from-cancellation / R5 live-conditional-option. The pre-W1 framing in `DECISION-SPACE §1.8` ("R2-base + R2+R3 hybrid") has narrowed (R3 conditional rather than hybrid-default) and widened (R4 elevated from cancellation; R5 live).
- **What incubation should ask (Logan-adjudication).**
  - **(a) Per §2.1 — does incubation operate under the operating-frame-shifted R2+R4-mix (codex read) or evaluate-whether-to-shift from R2-base-with-R4-net-widening (Claude read)?** This is the binding §2.1 adjudication; it shapes deliberation-shape but converges on similar downstream R-mix outcomes.
  - **(b) Which R2 subsystem (Pi extensions / GSD ecosystem extensions / workflow plugins / skills / hooks / MCP tools) carries the cheapest viable first-second-wave-target?** Both syntheses recommend asking this before R-mix decomposition (per `SYNTHESIS-CROSS §5` recommendation #2; per `SYNTHESIS §2.5` design-shape candidates table).
  - **(c) When does the R3 deferred contribution-culture deep probe fire — pre-vs-post critical path for second-wave-scoping commits?** If first-target-shape requires R3 (e.g., upstream PR for ecosystem extension API stability), probe fires pre-design; if R3 is optional, probe can defer.
- **Salient parameters.** (i) If Logan disposes Operating-frame-shifted (codex read) at §2.1, R-mix questions reduce to "which R2/R4 subsystem first." (ii) If Logan disposes Evaluate-whether-to-shift (Claude read) at §2.1, R-mix questions include "should the operating frame shift on the §1 evidence." (iii) Either way, R3 + R5 dispositions remain conditional on side-probe completion (§5.4) + context-anchoring (§5.3).
- **Confidence.** High on R-mix narrowing-and-widening shape. Medium on which mix incubation operates under (depends on §2.1 adjudication + §5.3 context-anchoring).

### §5.3 Six-context anchoring — **Logan-disposed**

- **What the comparison surfaces.** Per `framing-widening §2-§3` + `SYNTHESIS §2.4` + `SYNTHESIS-CROSS §2.4`, six-context plurality (A solo-research / B small-team-product / C larger-enterprise / D platform-team / E transition-as-event / F transition-as-stance) anchoring is **Logan-disposed** at incubation. Both syntheses converge that this is outside synthesis scope; first-wave gsd-2 evidence is interpretively-compatible with multiple context-anchorings.
- **First-wave evidence on context-fit (per `SYNTHESIS-CROSS §2.3`).**
  - Context A (solo-research-tool over years): strongly supported. gsd-2's artifact hierarchy, summaries, decisions, state cache, continuation, verification, auto loop directly address continuity and comprehension.
  - Context B (small-team product): partially supported. Team mode, shared/local artifacts, plan/code PR workflow exist; release freeze, approvers, rollout ownership, RC/staging schema, external stakeholder review not clearly native.
  - Context C (larger enterprise): only gestured at. Security, telemetry, audit, CI, schema migrations exist; compliance-grade audit trails, release trains, regulatory workflows, org-level governance not established.
  - Context D (platform-team across org): source suggests gsd-2 itself has dev/next/latest channels, release workflows, update checks, extension tiers; user adoption patterns unknown.
  - Context E (transition-as-event): plausible but unproven. Solo/team mode + migration/external-state tooling suggest transition support; no evidence directly tests solo-to-team transition coherence.
  - Context F (transition-as-stance / anticipatory scaling): most relevant and most unsettled. gsd-2 has optional, progressive surfaces (team mode, workflows, extensions, hooks, headless, release templates); whether these compose into elegant optionality vs feature sprawl is incubation question.
- **Comparison-author surfaces (synthesis interpretive reads, not disposition).** Per `SYNTHESIS-CROSS §2.3`: *"long-horizon should remain plural. First-wave evidence supports Context A plus optional Context F/B adjacency more than it supports a single release-engineering or team-scaling axis. Confidence: medium."* Per `SYNTHESIS §2.4`: framing-widening's "primarily Context A with strong Context F secondary" is interpretively-consistent with first-wave evidence but not validated by first-wave evidence — requires Logan's read.
- **What incubation should ask (Logan-adjudication).**
  - **(a) Which context anchoring is primary?** Logan disposes from the framing-widening §3 plurality. Comparison-author observation: A-primary with F-secondary is the synthesis-stage default-plausible read; A/F-primary with B-adjacency is also plausible; B-primary or C-primary requires additional surface-stability + release-machinery evidence not currently in scope.
  - **(b) Is the anchoring stable-or-anticipated-shifting?** Per `framing-widening §2.6`, transition-as-stance (Context F) treats anchoring as anticipated-shifting; transition-as-event (Context E) treats it as stable-with-staged-shifts. Logan's read shapes whether the harness should be optimized for stable-anchoring vs anticipated-shifting.
  - **(c) How does context-anchoring shape §5.1 + §5.2 dispositions?** If A-primary: §1.4 release machinery less load-bearing; R-mix can lean R2-extension + R4-orchestration without heavy release-engineering. If A/F-primary: same as A-primary plus optionality-progressive-activation as a design discipline. If B-primary: §1.4 release machinery becomes load-bearing; R3 contribution-receptivity becomes load-bearing; surface-stability becomes load-bearing.
- **Salient parameters.** (i) Logan's actual project pipeline (per `CLAUDE.md` ecosystem) suggests A-primary + F-secondary as plausible; this is observation, not adjudication. (ii) The deferred competitor-landscape probe (§5.4) may shift R5-disposition under specific context-anchorings. (iii) Per `framing-widening §9` deferred items, several context-anchoring-related questions are explicitly deferred to incubation — this is one of them.
- **Confidence.** Comparison surfaces high-confidence on first-wave-evidence-context-fit (per codex §2.3 detailed); medium-low on which anchoring incubation should adopt (Logan-disposed; outside synthesis scope).

### §5.4 Side-probe triggers — pre-vs-post critical path for second-wave-scoping

- **What the comparison surfaces.** Per `framing-widening §9` deferred-items log + both syntheses' §4-§5, multiple side-probes are eligible to fire pre-second-wave-scoping or post-second-wave-scoping depending on first-target-shape. The comparison's job is to surface trigger-conditions; incubation disposes which fire when.
- **Side-probes surfaced.** (Per cross-reading of `framing-widening §9`, `SYNTHESIS §5`, `SYNTHESIS-CROSS §4-§5`.)
  - **(P1) Deferred contribution-culture deep probe** (per §1.9 + `framing-widening §9` item 6 + `DECISION-SPACE §1.15` B5). Trigger: first-target-shape requires R3 (upstream PR for ecosystem extension API stability or similar). Resolves: live GitHub PR/issue analysis, maintainer responsiveness, review latency, external-contributor acceptance.
  - **(P2) Temporal-stability probe across the four extension subsystems** (per §1.2 + `framing-widening §9` item 5). Trigger: any R2 work targeting a specific subsystem requires stability evidence beyond shallow window. Resolves: tag-diff sampling + changelog/GitHub release body review for the four subsystems.
  - **(P3) Deferred competitor-landscape probe** (per §2.2 + §3.4 + `framing-widening §9` item 3). Trigger: R5 becomes live (context-anchoring is Context F-heavy or non-coding/product-lifecycle-heavy per codex §0 OS-2; or Logan's context-anchoring read warrants competitor evaluation). Resolves: sibling-harness landscape, missing-semantics identification.
  - **(P4) Deeper-history sampling for breaking-change practice** (per §1.4 + `SYNTHESIS §3`). Trigger: any R2/R3 work targeting stable extension surfaces or release-coordination relies on breaking-change-practice claims beyond shallow window. Resolves: feature-vs-transition-state distinction; longer history window of `BREAKING CHANGE:` markers + removal events.
  - **(P5) Effective-state-emission probe (`prefs` / `headless query` / MCP tools)** (per §3.6). Trigger: docs-vs-source-drift class (§1.5) makes any R-strategy depending on docs-trust risky; effective-state-emission is a candidate first-target. Resolves: source/run check of `prefs`, `headless query`, or MCP tools for complete effective settings.
  - **(P6) Telemetry/observability/security as design-surface probe** (per §1.7 + `framing-widening §9` item 12). Trigger: design-shape candidates touching observability/security/trust surfaces require prior characterization of which existing surface attaches. Resolves: design-surface inventory + attachment analysis.
- **What incubation should ask (Logan-adjudication).**
  - **(a) Which side-probes fire pre-second-wave-scoping (before first-target-design commits)?** Comparison-author observation: P1 fires only if first-target-shape is R3-dependent; P2-P4 fire if first-target-shape is surface-stability-dependent; P5 fires if first-target-shape is effective-state-visibility (codex §5 candidate); P6 fires if first-target-shape touches observability/security; P3 fires if R5 becomes live.
  - **(b) Which side-probes fire post-second-wave-scoping (during second-wave execution)?** Probes not pre-required can defer to second-wave; this preserves first-wave-to-second-wave momentum without over-investing in probes that may not be load-bearing.
  - **(c) Are any side-probes parallel-eligible for cheap exploration?** P5 (effective-state probe) is structurally cheap (source/run check); could fire in parallel with first-target-shape selection. P3 (competitor-landscape) is more expensive but informs R5-disposition if R5 becomes live.
- **Salient parameters.** (i) First-target-shape selection (per §5.2 question (b)) determines which probes are pre-vs-post critical path. (ii) Context-anchoring (§5.3) determines whether release-machinery-load-bearing-ness raises P2 + P4 priority. (iii) Per `framing-widening §3.3` disposition-discipline: probes are not first-wave-decidable; they are incubation-or-second-wave-decidable.
- **Confidence.** High on probe-surface (well-grounded in §1 + §2 + `framing-widening §9`). Medium on probe-pre-vs-post-disposition (depends on first-target-shape + context-anchoring; Logan-disposed).

### §5.5 Cross-axis integration — how the four axes compose at incubation

- **Composition observation.** The four axes (§5.1 metaquestion / §5.2 R-mix / §5.3 context-anchoring / §5.4 side-probes) are not independent. Per the comparison's reading:
  - Context-anchoring (§5.3) is the most upstream axis: shapes whether §1.4 release machinery + §1.9 R3 + §1.2 surface-stability are load-bearing for the chosen context-mix.
  - Metaquestion (§5.1) flows from context-anchoring: direction-holds-with-qualifications net read holds across most context-anchorings; qualification-load varies by context.
  - R-mix (§5.2) flows from context-anchoring + first-target-shape: which R2 subsystem + whether R3/R5 become live depends on context + first-target.
  - Side-probes (§5.4) flow from first-target-shape + R-mix: which probes fire pre-vs-post depends on what the second-wave-scoping commits to.
- **Implication for incubation deliberation order.** Per both syntheses' §5 recommendations + this comparison's read, an efficient incubation ordering is: **(1) dispose context-anchoring (§5.3); (2) test metaquestion-direction-holds under that anchoring (§5.1); (3) select first-target-shape candidate (§5.2 question (b)); (4) decide R-mix decomposition for that target (§5.2 question (a) — §2.1 disposition-timing); (5) fire pre-required side-probes (§5.4).** This is a comparison-author surface, not a disposition; Logan disposes incubation deliberation order.
- **Comparison-author caveat.** Per `framing-widening §3.3`: incubation is Logan-led + out of orchestration scope. The comparison surfaces axis-composition; it does not pre-decide incubation deliberation order or the dispositions at each axis.

---

## §6. Confidence and limits

*What this comparison can and cannot establish, and how it should be read at incubation.*

### §6.1 What the comparison establishes

- **§1 convergent findings (high-to-medium-high confidence).** Nine findings reached independently by both syntheses from the audited W1 evidence base. Per §4.2: convergent findings carry robustness signal because they survived independent reading (cross-vendor codex did source spot-checks reaching the same conclusions Claude reached via cross-slice integration). High-confidence inputs for incubation deliberation, with the §4.2 caveat that convergence is within-framing (R1-R5 + six-context).
- **§2 divergent findings (substantive vs register characterization, medium-high confidence on characterization).** Three divergence-types identified: (i) §2.1 R4 weighting as substantive interpretive-disposition-timing divergence (Logan-adjudication required); (ii) §2.2 R5 framing as register divergence at common operational endpoint (surfacing-only); (iii) §2.3 synthesis register/length as artifact-shape divergence (surfacing-only). Comparison-author confidence on the typology is medium-high; the verbatim-contrast grounding is solid for §2.1.
- **§3 asymmetric coverage (complementary, not contradictory).** Six items where one synthesis surfaces what the other does not directly state; pattern is depth-vs-breadth rather than disagreement. Same-vendor goes deep on cross-slice integration (§3.1 interleaving + §3.2 substrate-richness); cross-vendor goes wide on methodological caveats + concrete operationalization (§3.3 framing-leakage caveat + §3.4 R5-reframe + §3.5 first-target-methodology + §3.6 named probe).
- **§4 methodological observations (medium confidence; n=1 paired-synthesis).** M1 paired-review property observed-as-claimed in some instances and inverted in others (§4.1); convergence-as-robustness signal held within-framing (§4.2); tier-comparison preliminary observation consistent with prior expectation (§4.3); framing-import drift surfaced as initiative-maturity signal (§4.4); stratification methodology converged across both syntheses (§4.5).
- **§5 incubation-checkpoint multi-axis structure (high on axis-composition; medium on dispositions).** Four-axis structure (metaquestion / R-mix / context-anchoring / side-probes) with cross-axis integration observation (§5.5). Comparison-author surfaces axis-composition; Logan-adjudication required at §5.1(b), §5.2(a)+(b)+(c), §5.3(a)+(b)+(c), §5.4(a)+(b)+(c).

### §6.2 What the comparison cannot establish

- **The dispositions themselves.** Per `framing-widening §3.3` + `DECISION-SPACE §2.3` + `synthesis-spec.md:185-188`: incubation is Logan-led + out of orchestration scope. The comparison surfaces deliberation surface; it does not pre-decide.
- **The framing-widening's correctness.** Per §3.3 + §4.2: convergent findings within R1-R5 + six-context framing do not validate the framing itself. Logan can revise the framing at incubation (per `framing-widening §9` deferred items 16-17) and the comparison's findings would need re-reading against the revised framing.
- **The context-anchoring (§5.3).** Both syntheses converge that this is outside synthesis scope; Logan-disposed. Comparison surfaces interpretive-compatibility with multiple anchorings; it does not establish which.
- **First-target-shape (§5.2 question (b)).** Comparison surfaces candidates per `SYNTHESIS-CROSS §5` (effective-state visibility; release metadata/checklist artifact; Context A/F long-arc decision trace skill/workflow; headless orchestration recipe) and `SYNTHESIS §2.5` design-shape candidates table. It does not select among them.
- **Side-probe pre-vs-post-disposition (§5.4).** Comparison surfaces probe-surface + trigger-conditions; it does not dispose which fire when.
- **Whether direction-shifting evidence is sufficient to flip metaquestion.** Both syntheses converge on direction-holds-with-qualifications; whether qualification-load is heavy enough to warrant re-evaluation under specific context-anchorings is Logan-disposed at §5.1(b).

### §6.3 In-session-collaboration caveat — D5a methodological note

- **What was authorized.** Per `2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` D5a: comparison-stage drafting is **in-session-collaborative** (Claude-with-Logan) rather than independent-third-synthesizer. The dispatch-to-third-synthesizer alternative was considered and not authorized at this stage.
- **What this preserves.** The two syntheses being compared (Claude `SYNTHESIS.md` + codex `SYNTHESIS-CROSS.md`) are independent — codex did not read `SYNTHESIS.md` per dispatch prompt (`SYNTHESIS-CROSS §0` note). Cross-vendor independence at synthesis stage is intact. The comparison artifact integrates them after the fact.
- **What this caveats.** The comparison itself is Claude-in-session. M1 paired-review's full epistemic property — cross-vendor independence at integration stage — is partially honored: integration is performed by one of the two synthesizers (Claude), not by an independent third synthesizer. Logan adjudication of §2.1 + §5 axes provides cross-checking but is not the same as a fully-independent third comparison.
- **Implication for reading the comparison.** The comparison's framing of divergences (especially §2.1 substantive-vs-register characterization) and asymmetric coverage (§3) reflect Claude's reading of both syntheses; an independent third synthesizer might characterize differently. Logan should weigh the comparison's typology choices as Claude-shaped reading, not as vendor-independent reading.
- **When this caveat matters most.** §2.1 R4 disposition-timing characterization is the highest-stakes Claude-shaped reading: characterizing it as substantive (rather than register) is a comparison-author choice. The `2026-04-28-comparison-drafting-decisions.md` DC4 preserves the conditional structure: if Logan reads the verbatim contrast differently, the typology can be revised without invalidating the rest of the comparison.
- **Mitigation via traceability.** All comparison-author choices are traceable: DC0-DC4 in `2026-04-28-comparison-drafting-decisions.md`; verbatim citations from both syntheses surfaced for all divergence claims; possible-reasons-for-divergence sections (§2.1, §2.2) explicitly marked interpretive. This reduces the in-session-collaboration risk: Logan can audit the typology + revise if needed.

### §6.4 First-wave evidence base — load-bearing limits

- **First-wave evidence is sufficient for incubation, insufficient for second-wave-design (per `SYNTHESIS-CROSS §6` + `SYNTHESIS §0`).** Both syntheses converge on this. Specifically: (i) R3 contribution-receptivity unverified (live PR/issue probe failed); (ii) Pi/GSD seam ADR-010 proposed-not-implemented; (iii) breaking-change practice partially shallow-window; (iv) extension-surface temporal-stability not characterized; (v) effective-state emission for divergent defaults not verified at runtime. Side-probes (§5.4) fill these gaps if-and-when first-target-shape requires them.
- **Audited evidence base traceability.** The W1 evidence base is `01-mental-model-output.md` through `05-release-cadence-output.md` + audits + side-investigations + `framing-widening` + `INITIATIVE.md` + `DECISION-SPACE.md`. Both syntheses cite this base; the comparison cites both syntheses + the deliberation log + handoff. The audit chain runs: slices → audits → syntheses → comparison → incubation.

### §6.5 Operational caveats for incubation reading

- **Read order at incubation.** Per `synthesis-spec.md:185-188` + handoff §6.5, incubation reads syntheses + comparison together. Suggested order: this comparison's §0 + §5 + §6 → both syntheses' §0 + §5 → drill into specific findings as deliberation requires. Full re-read of either synthesis is not strictly required if comparison's §1 + §5 axes hold up under Logan's read.
- **Frame revisions.** If Logan revises the framing-widening at incubation (per `framing-widening §9` deferred items 16-17), the comparison's §1 findings should be re-read against revised framing; structural facts (Pi vendoring, four extension subsystems, two-engine architecture) survive most revisions; framing-shaped articulations (R-mix narrowing shape, R3 under-evidenced framing) require re-articulation under revised frame.
- **Disposition-stop discipline.** Per handoff §8.7 + `framing-widening §3.3`: incubation disposes; the comparison does not. If the comparison's framing of §2.1 (substantive interpretive-disposition-timing) is read by Logan as already-pre-disposing the operating-frame question, the comparison should be revised, not the framing forced to fit. The comparison is fallibilist per `DECISION-SPACE.md §0`.
- **Second-wave-scoping start condition.** Per both syntheses + §5.4 of this comparison: second-wave-scoping starts after at least one context/R-target narrowing decision (per `SYNTHESIS-CROSS §6`) and after pre-required side-probes complete. The comparison does not specify which decisions are pre-required; that is incubation-disposed.

### §6.6 Confidence summary table

| Section | What it establishes | Confidence |
|---|---|---|
| §1 convergent findings | Nine findings reached independently | High-to-medium-high (within-framing) |
| §2.1 R4 weighting divergence | Substantive interpretive-disposition-timing | Medium-high on typology; Logan-adjudication on which read |
| §2.2 R5 framing divergence | Register at common operational endpoint | High on convergence; surfacing-only |
| §2.3 Synthesis register/length | Artifact-shape divergence | High; surfacing-only |
| §3 asymmetric coverage | Complementary depth-vs-breadth pattern | Medium-high on items; medium on pattern characterization |
| §4 methodological observations | M1 + n=1 calibration | Medium; n=1 paired-synthesis |
| §5.1 metaquestion | Direction-holds-with-qualifications | Medium-high (qualification-load context-dependent) |
| §5.2 R-mix integration | R-mix narrowed-and-widened shape | High on shape; medium on which-mix-incubation-operates-under |
| §5.3 context-anchoring | First-wave-evidence-context-fit | High on fit; medium-low on which-anchoring (Logan-disposed) |
| §5.4 side-probe triggers | Probe-surface + trigger-conditions | High on surface; medium on pre-vs-post-disposition |
| §5.5 cross-axis integration | Four-axis composition + suggested order | Medium-high; surfacing-only |
| §6 confidence + limits | What comparison can/cannot establish | High on the limits themselves |

---

## §7. Premise-bleed audit addendum (post-comparison-draft)

**What this addendum records.** A premise-bleed audit (cross-vendor codex GPT-5.5 high + same-vendor Claude xhigh independent) was conducted on this comparison and the upstream initiative artifacts before incubation adjudication on §2.1 + §5. Audit folder: `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/` (`AUDIT-SPEC.md` + `FINDINGS.md` + `FINDINGS-STEP2.md` + `DIFFERENTIAL.md` + `DISPOSITION.md`). Both reads converged that premise-bleed is largely localized to early staging artifacts and that the synthesis chain substantially corrected vocabulary-level bleed; both reads diverged on whether the integration grammar of §5 (R1-R5 / six-context / four-act) applied without explicit "inputs not observed facts" framing at point-of-use is itself narrowly load-bearing residual. This addendum records the load-bearing carry-forward.

### §7.1 Reading-frame for §5 axes (point-of-use foregrounding)

Per `SYNTHESIS-CROSS §6` framing-leakage caveat (`SYNTHESIS-CROSS.md:203`):

> *"The R1-R5 and six-context frames are useful inputs, not observed facts in gsd-2. Where they overfit the evidence, incubation should loosen them rather than treat this synthesis as authority."*

This caveat applies symmetrically to **all of §5** (metaquestion / R-mix / context-anchoring / side-probes / cross-axis integration). Read §5's axis-questions as:

- **Inputs Logan brought in via framing-widening**, not observed facts in gsd-2.
- **Loose-able if they overfit**: per `framing-widening §9` items 16-17, frame revision at incubation is a licit move; if a §5 axis-question is read as already-pre-disposing the deliberation-shape, the comparison should be revised, not the framing forced to fit (per §6.5 disposition-stop discipline).
- **One register among several**: per `META-SYNTHESIS §2 item 3` typed-extension vocabulary and `META-SYNTHESIS §3` prohibited articulations (at `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md`), the integration grammar should not be treated as same-kind observed-facts; surface selection precedes R-strategy assignment.

### §7.2 Artifact-side carry-forward (audit residuals not requiring §5 revision)

Two artifact-text residuals are operationally widened by `framing-widening` but text remains:

- **`INITIATIVE.md §3.2 candidate-design-shapes` ("patcher / skills / hybrid").** Was a starter list under v1-GSD framing; superseded by `SYNTHESIS.md §2.5` four-act mapping + this comparison's §5.2 R1-R5 decomposition. Read INITIATIVE.md §3.2 as historical staging vocabulary, not as candidate set.
- **`DECISION-SPACE.md §1.8` (R2-base + R2+R3 hybrid).** Operationally widened by `framing-widening §5` (`framing-widening.md:251`) to R1-R5 with R4 elevated and R3 conditional. Read §1.8 as the pre-W1 working hypothesis; current R-mix is at this comparison's §5.2.

### §7.3 What the audit did not surface

- No vocabulary-import bleed survives to this comparison's incubation-facing §5 axes.
- The §3.3 framing-leakage asymmetric-coverage observation + §4.4 framing-import drift observation + §6.3 D5a in-session-collaboration caveat + §6.5 frame-revision discipline jointly constitute the comparison's self-audit machinery.
- The §2.1 R4 disposition-timing divergence is already explicitly surfaced as Logan-adjudication; no premise-bleed conclusion changes its disposition.

### §7.4 Cross-references

- `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` (lens + method).
- `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/FINDINGS.md` (Step-1 cross-vendor codex GPT-5.5 high; 6 instances; 1A/5B/0C).
- `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/FINDINGS-STEP2.md` (Step-2 same-vendor Claude xhigh independent; 9 instances; 4A/3B/2C narrow).
- `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/DIFFERENTIAL.md` (post-hoc differential; reconciliation analysis; recommendation trace).
- `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/DISPOSITION.md` (Logan's disposition + reasoning).
- `DECISION-SPACE.md §1.17` (audit-methodology decision).

---

*[Draft complete 2026-04-28; §7 audit addendum landed 2026-04-29 (commit-with-addendum disposition per Logan, post-cross-vendor + same-vendor-independent premise-bleed audit). §0-§6 landed (in-session-collaborative per D5a); §2.1 R4 disposition-timing characterization + §5 axes are surfacing-shape, not adjudications — Logan adjudicates at incubation. Subject to the same fallibility caveat as `DECISION-SPACE.md §0`. Per handoff §6.5: this comparison feeds incubation; it does not pre-decide incubation's questions. The in-session-collaboration caveat (§6.3) applies to all comparison-author-shaped reading; §7.1 reading-frame applies to §5 axes at point-of-use.]*
