---
type: first-wave-synthesis-cross-vendor
date: 2026-04-28
agent: codex GPT-5.5 high (cross-vendor; paired with same-vendor SYNTHESIS.md)
inputs:
  - .planning/gsd-2-uplift/exploration/01-mental-model-output.md
  - .planning/gsd-2-uplift/exploration/02-architecture-output.md
  - .planning/gsd-2-uplift/exploration/03-workflow-surface-output.md
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md (with (vi) addendum)
  - .planning/gsd-2-uplift/exploration/05-release-cadence-output.md (with (vi) corrigenda)
  - .planning/gsd-2-uplift/exploration/02-architecture-audit.md
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md
  - .planning/gsd-2-uplift/exploration/05-release-cadence-audit.md
  - .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md
  - .planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md
  - .planning/deliberations/2026-04-28-framing-widening.md
  - .planning/gsd-2-uplift/INITIATIVE.md (§1, §3)
  - .planning/gsd-2-uplift/DECISION-SPACE.md (§1.7, §1.8, §1.11, §1.12, §3.4, §3.6)
status: complete
note: |
  Independent cross-vendor synthesis. The same-vendor SYNTHESIS.md was NOT read
  (forbidden per dispatch prompt) so this synthesis is reached independently.
---

# First-wave synthesis (cross-vendor) — gsd-2 characterization

## §0. Synthesis summary

Top-line findings, severity-stratified by their bearing on operating-frame-update decisions:

- **Operating-frame-shift findings:** R2 remains viable, but not as a single clean "extension" path. First-wave evidence supports a plural extension/configuration/orchestration picture: Pi extensions, GSD ecosystem extensions, workflow plugins, skills, hooks, headless/RPC/MCP, and agent-prompted templates each have different stability and execution semantics. This shifts the operating frame from "R2 base unless infeasible" toward "R2+R4 mix unless the needed surface requires core/Pi entanglement." Confidence: medium-high.
- **Operating-frame-shift findings:** gsd-2's current architecture is not cleanly "GSD on top of Pi SDK." It is a vendored modified Pi fork plus GSD glue plus bundled extensions. ADR-010's clean seam is proposed, not implemented; I spot-verified the ADR status and package tree (`gsd-2 docs/dev/ADR-010-pi-clean-seam-architecture.md:3`, `:12-29`, `:45-57`; `gsd-2 package.json:15-19`). This makes R1 costly and makes any R2/R3 work inside Pi-facing seams more fragile. Confidence: high.
- **Operating-frame-shift findings:** Release and long-horizon machinery exists, but often as composable primitives, prompt-mediated workflow templates, or gsd-2's own repo practice rather than deterministic user-project release infrastructure. This strengthens R4 and weakens any second-wave assumption that a semver/RC/release-train layer is already native. Confidence: medium-high.
- **Operating-frame-confirm findings:** gsd-2 is active, broad, and compatible with the goal's general domain: agent workflow control, `.gsd` state, milestone/slice/task artifacts, verification, worktrees, headless automation, hooks, extension systems, team mode, telemetry, and release templates all exist across the slices. Confidence: high.
- **Operating-frame-confirm findings:** The first-wave did not surface evidence that gsd-2's mission is so divergent that uplift would distort identity. gsd-2 presents itself as a coding-agent orchestration layer for planning, execution, verification, and shipping; that is directionally close to the initiative's harness question. Confidence: medium-high.
- **Open at synthesis stage:** R3 is under-evidenced. Local `CONTRIBUTING.md` shows extension-first policy, issue-first norms, ADR/RFC expectations, and PR discipline, but the live GitHub contribution probe failed. Confidence in R3 viability remains medium-low.
- **Open at synthesis stage:** R5 is not demanded by first-wave evidence, but it is no longer merely a cancellation bucket. If incubation decides the needed target is Context F-heavy or non-coding/product-lifecycle-heavy, gsd-2 may be better used as a reference plus external orchestrated component than as the object modified. Confidence: medium.

## §1. Cross-slice pattern integration

### §1.1 gsd-2 is a product-scale agent host, not a thin planning layer

- Contributing slice(s): slices 1, 2, 3, 4, 5; architecture audit.
- Pattern: Slice 1 describes a standalone coding-agent CLI with interactive/headless/MCP modes, `.gsd` state, and a broad command surface (`01-mental-model-output.md:64-76`, `:102-112`). Slice 2 expands that into a Node/TypeScript package with vendored Pi packages, native modules, loader/CLI composition, in-process MCP, and standalone MCP/RPC packages (`02-architecture-output.md:63-81`, `:83-101`, `:178-188`). Slice 3 shows the command/automation surface is wide: slash commands, headless query, multiple dispatch shapes, hooks, verification, and machine-facing transports (`03-workflow-surface-output.md:80-130`, `:132-154`). Slice 4 adds artifact lifecycle, extension registry, migration, external state migration, and install/update/versioning (`04-artifact-lifecycle-output.md:262-356`). Slice 5 adds release channels, release templates, API-breaking templates, DB-backed planning schemas, and observable rapid release practice (`05-release-cadence-output.md:250-386`).
- Pattern implication: first-wave should not be read as "can we add docs around a workflow convention?" The target is a large runtime/product. Any intervention that assumes a small surface will miss coupling and maintenance cost.
- Confidence: high.

### §1.2 Agent-prompted workflow templates are not deterministic release engines

- Contributing slice(s): slice 3, slice 5, capabilities probe, W2 markdown-phase dive.
- Pattern: Slice 3 distinguishes dev auto, YAML graph, markdown-phase, oneshot, auto-milestone, and UOK wrapper dispatch shapes (`03-workflow-surface-output.md:118-128`). Slice 5 inventories release and API-breaking-change templates as concrete artifacts (`05-release-cadence-output.md:334-378`). The capabilities probe first flagged that release/hotfix templates are separate from milestone semantics and that release support is composable rather than a semver-aware milestone layer (`capabilities-production-fit-findings.md:10-20`, `:250-272`, `:276-356`). The W2 dive source-verified that markdown-phase creates artifact dir/branch/STATE.json and sends a prompt to the agent; it does not parse and execute markdown shell blocks (`w2-markdown-phase-engine-findings.md:12-22`, `:36-54`, `:70-78`).
- Source spot-check: `commands-workflow-templates.ts` creates artifact dir, maybe a branch, writes workflow state, then calls `pi.sendMessage` with the loaded prompt (`gsd-2 src/resources/extensions/gsd/commands-workflow-templates.ts:424-508`). `workflow-start.md` instructs the agent to follow phases and write artifacts (`gsd-2 src/resources/extensions/gsd/prompts/workflow-start.md:15-28`). YAML-step custom workflows, by contrast, update `GRAPH.yaml` and can run shell-command verification (`gsd-2 src/resources/extensions/gsd/custom-workflow-engine.ts:90-226`; `custom-verification.ts:144-182`).
- Pattern implication: release/RC/staging uplift should not assume executor-owned release semantics unless built as new code or recast through YAML/custom workflow machinery. A prompt-mediated release template is useful but materially different from a deterministic release pipeline.
- Confidence: high for the source distinction; medium-high for strategic implication.

### §1.3 Extension viability is real, but "extension" is plural

- Contributing slice(s): slices 2, 4, 3; slice 4 audit/addendum; framing-widening.
- Pattern: Slice 2 shows the Pi extension API is load-bearing and core GSD itself is a bundled extension (`02-architecture-output.md:89-97`, `:180-188`). Slice 4 initially found manifest + entry module + registry + `/gsd extensions`; the audit found this was incomplete because ecosystem extensions, workflow plugins, and skills are separate subsystems. The addendum now says to treat gsd-2 as having at least four parallel extension surfaces (`04-artifact-lifecycle-output.md:296-330`, `:425-429`; `04-artifact-lifecycle-audit.md:53-65`, `:108-123`). Slice 3 adds hooks and command transports as additional extension/configuration-adjacent surfaces (`03-workflow-surface-output.md:132-144`, `:160-168`).
- Source spot-check: ecosystem extensions load from `.gsd/extensions` via a GSD-specific wrapper and trust gate (`gsd-2 src/resources/extensions/gsd/ecosystem/loader.ts:1-18`, `:45-95`; `ecosystem/gsd-extension-api.ts:1-10`, `:40-50`). Workflow plugins advertise project/global/bundled discovery and four modes (`gsd-2 src/resources/extensions/gsd/workflow-plugins.ts:1-14`, `:120-221`). Skills have per-unit allowlists and discovery under `.agents`/Claude skill roots (`gsd-2 src/resources/extensions/gsd/skill-manifest.ts:1-16`, `:25-43`; `skill-discovery.ts:15-23`, `:49-77`).
- Pattern implication: R2 should be decomposed by target surface. "Build an extension" might mean a Pi extension, GSD ecosystem extension, workflow plugin, skill, hook, MCP tool, or bundled extension PR. These have different trust, execution, packaging, and durability properties.
- Confidence: high for surface plurality; medium-high for downstream mix.

### §1.4 gsd-2 is observability/security-heavy enough that uplift should use those surfaces, not bypass them

- Contributing slice(s): slices 1, 2, 3, 4, 5; capabilities probe.
- Pattern: Each slice independently flags observability/security/trust as central: slice 1 sees diagnostics, cost/tokens, dashboards, logs, forensics, and security/trust watchlists (`01-mental-model-output.md:84-88`, `:153-161`); slice 2 sees hooks/security/trust, MCP, and auto-loaded instruction contracts (`02-architecture-output.md:178-188`, `:214-231`); slice 3 sees hooks, write gates, verification, debug/forensics, and trust boundaries (`03-workflow-surface-output.md:132-154`, `:178-194`); slice 4 sees debug logs, extension trust, session artifacts, registry files (`04-artifact-lifecycle-output.md:262-330`, `:408-418`); slice 5 sees telemetry/forensics, HTML reports, schema migrations, and release observability (`05-release-cadence-output.md:328-386`). The capabilities probe adds write gates, exec sandbox, destructive-command classifier, secret scanning, and key management (`capabilities-production-fit-findings.md:166-198`).
- Pattern implication: Second-wave candidates should ask "which existing observation/trust surface does this attach to?" before inventing parallel state. Bypassing these surfaces would repeat the project's silent-default anti-pattern.
- Confidence: medium-high.

### §1.5 Documentation/source drift is recurrent but bounded, not catastrophic

- Contributing slice(s): slices 1, 2, 3, 4, 5; audits; capabilities probe.
- Pattern: Repeated tensions include RTK README vs opt-in source (`01-mental-model-output.md:153-161`; `02-architecture-output.md:77-81`; `02-architecture-audit.md:42-49`), reassess-loop docs vs default gating (`01-mental-model-output.md:88`, `03-workflow-surface-output.md:194-200`), extension command completion vs dispatch (`04-artifact-lifecycle-output.md:408-423`), boundary map docs vs migrator skip (`04-artifact-lifecycle-output.md:282-294`, `:408-423`), team default docs vs source (`capabilities-production-fit-findings.md:114-128`; spot-check `gsd-2 src/resources/extensions/gsd/preferences-types.ts:68-90` vs `docs/user-docs/git-strategy.md:135-145`), and CI/CD docs vs manual workflow sources (`05-release-cadence-output.md:396-410`).
- Pattern implication: For R2/R4 work, effective-state checks and source-backed behavior verification are not optional. Documentation can guide, but runtime/source must arbitrate.
- Confidence: high for recurrence; medium for severity.

## §2. Operating-frame test results

### §2.1 R-strategy viability across R1-R5 (per framing-widening §1)

- **R1 fork.** Viability: viable but high-cost, medium-high confidence. gsd-2 is MIT-licensed in package metadata and source is available (`gsd-2 package.json:2-8`), so a fork is mechanically possible. But the source picture makes fork maintenance expensive: current package is broad (`02-architecture-output.md:103-176`), vendored Pi is entangled, ADR-010 says substantial GSD code is mixed into `pi-coding-agent` (`02-architecture-output.md:85-101`; `02-architecture-audit.md:26-39`), and visible release cadence is extremely rapid (`05-release-cadence-output.md:250-296`; `05-release-cadence-audit.md:21-44`). R1 should remain fallback for narrow patches or if R2/R4 fail, not become the base operating frame from first-wave evidence alone.
- **R2 extension.** Viability: viable but surface-specific, high confidence. Slice 4 plus audit/addendum is decisive that extension surfaces exist (`04-artifact-lifecycle-output.md:296-330`, `:425-429`; `04-artifact-lifecycle-audit.md:53-65`). Slice 2 shows the extension API is not peripheral because core GSD is implemented as an extension (`02-architecture-output.md:89-97`, `:180-188`). Source spot-checks confirm multiple extension mechanisms. However, R2 should be decomposed: skills and workflow plugins support different work than Pi/GSD ecosystem extensions; markdown-phase templates cannot be treated as deterministic engines.
- **R3 upstream-PR-pipeline.** Viability: plausible but under-evidenced, medium-low confidence. `CONTRIBUTING.md` asks for issues before features, RFC/ADR for architectural changes, clean branches, conventional commits, CI, breaking-change disclosure, and says GSD is extension-first (`gsd-2 CONTRIBUTING.md:7-18`, `:101-164`). Local git history shows many PR merge commits in slice 4's fallback observation (`04-artifact-lifecycle-output.md:149-259`). But the required live PR/issue probe failed (`04-artifact-lifecycle-output.md:386-398`), so maintainer responsiveness, review latency, and external-contributor acceptance are not established. R3 is useful where changes align with extension-first policy; it should not be assumed for load-bearing delivery.
- **R4 orchestrate-without-modifying.** Viability: strongly viable, medium-high confidence. Headless/query/RPC/MCP, JSON/JSONL output, hooks, effective preferences, workflow artifacts, and gsd-2's own release scripts make orchestration from outside plausible (`03-workflow-surface-output.md:102-104`, `:128-130`; `capabilities-production-fit-findings.md:78-112`, `:232-260`, `:276-356`). W2 dive strengthens this by showing some release-like workflows are naturally prompt/artifact orchestration rather than core modifications (`w2-markdown-phase-engine-findings.md:98-107`). R4 may be the cleanest shape for release coordination, effective-state checks, external CI recipes, and project-specific discipline.
- **R5 replacement-informed-by.** Viability: open option, not first-wave recommendation, medium confidence. First-wave does not show gsd-2 is identity-misaligned or unusable. It does show gsd-2 is large, opinionated, fast-moving, and Pi-entangled. If incubation anchors the desired harness to context needs beyond gsd-2's current center of gravity, especially non-coding product lifecycle or anticipatory multi-context transition, R5 should stay live. It should not be collapsed to "cancel"; it could mean "use gsd-2 as a reference and maybe component, build a sibling for the missing semantics."

### §2.2 §1.7 metaquestion — direction-shifting evidence summary

Evidence supporting "uplift-of-gsd-2 is the right shape":

- gsd-2's mission and scope are close enough: it is explicitly about coding-agent orchestration, planning, execution, verification, shipping, and workflow control (`01-mental-model-output.md:64-88`, `:102-112`).
- R2 surfaces are substantive and product-load-bearing; core GSD itself uses extension machinery (`02-architecture-output.md:89-97`; `04-artifact-lifecycle-output.md:296-330`, `:425-429`).
- R4 surfaces are substantial: headless, query, RPC, MCP, hooks, workflow templates, and release/headless primitives (`03-workflow-surface-output.md:102-130`; `05-release-cadence-output.md:336-386`; `capabilities-production-fit-findings.md:78-112`).
- gsd-2 already carries many long-horizon-adjacent primitives: artifact hierarchy, summaries, requirements, schema migrations, validation, team mode, worktrees, release/API-breaking templates, and telemetry (`05-release-cadence-output.md:320-386`).

Evidence challenging or narrowing "uplift-of-gsd-2 is the right shape":

- Current Pi/GSD seam is proposed-clean, not implemented-clean. Anything requiring internal session/runtime changes is entangled with vendored Pi (`02-architecture-output.md:85-101`; `02-architecture-audit.md:26-39`).
- Release/RC/staging support is more template/composable than native schema. Milestone-to-release mapping is not explicit; RC primitives were not observed (`capabilities-production-fit-findings.md:224-272`; `w2-markdown-phase-engine-findings.md:98-107`).
- Release cadence is very rapid in visible history and breaking-change communication has elaborate machinery but inconsistent convention-enforced practice (`05-release-cadence-output.md:250-318`; `05-release-cadence-audit.md:108-123`).
- Documentation/source drift recurs across behavior defaults and workflow claims; extension work needs live effective-state checks.

Synthesis read: direction does not flip to "do not engage gsd-2." It does shift away from a simple R2-base story. The incubation checkpoint should evaluate a mixed answer: "proceed if the first second-wave target can be built through R2/R4 surfaces without depending on clean Pi separation or deterministic release semantics; otherwise consider R5 or a narrow R1 spike." Confidence: medium-high.

### §2.3 Long-horizon framing — six-context plurality (per framing-widening §2)

First-wave concretizes the six-context plurality unevenly:

- **Context A (solo-research-tool over years):** strongly supported as a fit. gsd-2's artifact hierarchy, summaries, decisions, state cache, continuation, verification, and auto loop directly address continuity and comprehension (`01-mental-model-output.md:72-76`, `:114-124`; `04-artifact-lifecycle-output.md:262-294`; `05-release-cadence-output.md:320-334`).
- **Context B (small-team product):** partially supported. Team mode, shared/local artifacts, plan/code PR workflow, branch/worktree/PR surfaces, release templates, and API-breaking templates exist (`01-mental-model-output.md:96-100`; `05-release-cadence-output.md:336-386`; `capabilities-production-fit-findings.md:114-128`, `:242-260`). But release freeze, approvers, rollout ownership, RC/staging schema, and external stakeholder review are not clearly native (`capabilities-production-fit-findings.md:250-272`).
- **Context C (larger enterprise):** only gestured at. Security, telemetry, audit, CI, and schema migrations exist, but compliance-grade audit trails, release trains, regulatory workflows, and org-level governance were not established. Confidence: medium-low.
- **Context D (platform-team across org):** source suggests gsd-2 itself has dev/next/latest channels, release workflows, update checks, and extension tiers (`04-artifact-lifecycle-output.md:356-386`; `05-release-cadence-output.md:336-348`; `gsd-2 CONTRIBUTING.md:146-164`), but user adoption patterns are unknown.
- **Context E (transition-as-event):** plausible but unproven. Solo/team mode and migration/external-state tooling suggest transition support, but no evidence directly tests solo-to-team transition coherence (`04-artifact-lifecycle-output.md:330-356`; `capabilities-production-fit-findings.md:114-128`).
- **Context F (transition-as-stance / anticipatory scaling):** the most relevant and most unsettled. gsd-2 has optional, progressive surfaces (team mode, workflows, extensions, hooks, headless, release templates), but whether these compose into elegant optionality rather than feature sprawl is a synthesis/incubation question.

Synthesis read: "long-horizon" should remain plural. First-wave evidence supports Context A plus optional Context F/B adjacency more than it supports a single release-engineering or team-scaling axis. Confidence: medium.

### §2.4 Project-anchoring (per framing-widening §3)

Interpretive. First-wave gsd-2 evidence is compatible with the framing-widening's "arxiv-sanity-mcp as primarily Context A with strong Context F secondary," but it does not validate that project-anchoring. That remains Logan's read. What first-wave adds is a caution: if project anchoring is primarily A/F, R2/R4 work should emphasize comprehension-across-time, effective-state visibility, optional progressive activation, and reversible conventions rather than immediately building heavy Context B/C release machinery. Confidence: medium-low because the anchor is outside gsd-2 evidence.

### §2.5 §3.2 design-shape candidates (concrete intervention surfaces)

Using the four-act plurality:

- **Modify gsd-2 (R2/R3, maybe narrow R1):** best candidates are extension-surface improvements, workflow-plugin additions, skill packaging, effective-state emission if absent, and possibly upstream PRs that make existing surfaces more inspectable. Evidence: extension-first contribution policy (`gsd-2 CONTRIBUTING.md:140-164`), four extension surfaces, and command/automation surface.
- **Configure gsd-2 (R4-adjacent / sometimes R2):** custom skills, hooks, preferences, workflow templates, and project-local conventions. Strong for early Context A/F uplift because it is reversible and cheap. Evidence: skills, hooks, preferences, and mode defaults across slices 3-5.
- **Orchestrate around gsd-2 (R4):** CI/headless recipes, release-pipeline wrappers, effective-state checks, external dashboards, or scripts consuming headless JSON/query output. Strong for release/RC/staging because existing release templates are prompt-mediated, not deterministic engines.
- **Replace-informed-by (R5):** only if incubation decides the needed harness semantics are outside gsd-2's natural surfaces, especially cross-project governance, non-coding product lifecycle, or transition-stance mechanisms too deep for configuration.

Do not pre-decide among these. The first second-wave target should be chosen to test the cheapest viable act before committing to a deeper act. Confidence: medium-high.

### §2.6 B4 resolution — slice 5 split

The split held. Slice 5 mostly stayed concrete: release cadence, breaking-change posture, artifacts, prod/dev distinctions, and feature inventory. Its abstract interpretation was explicitly deferred (`05-release-cadence-output.md:396-410`). The audit's machinery-vs-practice flag is exactly synthesis-stage integration (`05-release-cadence-audit.md:108-123`; disposition D3 at `2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md:172-194`). Therefore B4's provisional split should be treated as validated enough for this wave.

Synthesis interpretation: slice 5 shows gsd-2 has rich long-horizon-adjacent features, but those features do not by themselves prove long-horizon adequacy. They need context-specific composition analysis, especially around release semantics, stable interfaces, and optionality. Confidence: high for split, medium for interpretation.

## §3. Slice contradictions

### §3.1 README-level reassessment vs source/config defaults

- Slice 1 says README presents reassessment as part of the loop, while source defaults dedicated `reassess_after_slice` off (`01-mental-model-output.md:74-88`).
- Slice 3 independently flags reassessment docs as tensioned and says it did not fully trace the source in that slice (`03-workflow-surface-output.md:194-200`).
- Slice 5 lists roadmap reassessment as a concrete long-horizon feature because README/auto docs include it (`05-release-cadence-output.md:354-358`).
- Resolution: capability exists, but default/execution semantics need source-level verification before any uplift relies on it. Treat "reassessment" as a capability, not guaranteed default behavior. Confidence: medium-high.

### §3.2 RTK provisioning vs activation

- Slices 1, 2, and 3 all flag README/source divergence: README implies managed RTK integration, while `cli.ts` gates runtime activation behind `experimental.rtk` and disables by default unless enabled (`01-mental-model-output.md:153-161`; `02-architecture-output.md:77-81`, `:232-236`; `03-workflow-surface-output.md:194-198`).
- Audit confirms the specific source/readme tension (`02-architecture-audit.md:42-49`).
- Source spot-check confirms opt-in gating (`gsd-2 src/cli.ts:160-178`).
- Resolution: distinguish install-time provisioning from runtime activation. The divergence is not central to uplift strategy, but it is a durable warning against relying on README defaults. Confidence: high.

### §3.3 Extension path discrepancy resolved into surface plurality

- Slice 4 initially flags `.gsd/extensions` vs `.pi/extensions` as an open project-local extension path discrepancy (`04-artifact-lifecycle-output.md:408-414`).
- Audit resolves this as evidence of two parallel project-local extension subsystems: Pi loader and GSD ecosystem loader (`04-artifact-lifecycle-audit.md:53-65`).
- Source spot-check confirms GSD ecosystem extensions load from `.gsd/extensions` through a separate wrapper and trust gate (`gsd-2 src/resources/extensions/gsd/ecosystem/loader.ts:45-95`; `ecosystem/gsd-extension-api.ts:1-10`).
- Resolution: not merely docs/source drift; it is a real subsystem distinction. Synthesis should carry it as extension-surface plurality. Confidence: high.

### §3.4 Release/breaking-change machinery vs practice

- Slice 5 shows machinery: PR template/contributor policy, changelog categories, API-breaking template, semver detection, alias telemetry, release scripts (`05-release-cadence-output.md:296-334`, `:336-386`).
- Slice 5 also shows practice tension: no fixed deprecation SLA, visible removals not consistently using explicit breaking wording, OAuth removal lacks visible pre-deprecation in shallow history (`05-release-cadence-output.md:296-318`).
- Audit says this integration belongs at synthesis stage and adds that recent rapid tag cadence makes the machinery-vs-practice pattern direction-relevant (`05-release-cadence-audit.md:108-123`).
- Resolution: machinery exists but should not be treated as enforced culture. Any uplift depending on stable third-party surfaces needs a temporal-stability probe, not just workflow-template inspection. Confidence: medium-high.

### §3.5 Team/default docs vs source preference defaults

- Capabilities probe finds docs say team `git.isolation` is `"worktree"` while source `MODE_DEFAULTS.team.git.isolation` is `"none"` (`capabilities-production-fit-findings.md:114-128`).
- Source spot-check confirms source default and doc table divergence (`gsd-2 src/resources/extensions/gsd/preferences-types.ts:68-90`; `docs/user-docs/git-strategy.md:135-145`).
- Resolution: team-mode claims should be treated as intended/available surfaces until effective-preference behavior is verified. This matters for Context B/E/F conclusions. Confidence: high.

## §4. Open questions surfaced

- **Which extension surface is stable enough for R2?** Four-surface plurality helps viability but also creates selection risk. What resolves: temporal-stability probe over Pi extension API, ecosystem extension API, workflow plugins, and skills.
- **Can effective preferences be emitted machine-readably?** Multiple divergences make effective-state visibility a promising R4/R2 target. What resolves: source/run check of `prefs`, `headless query`, or MCP tools for complete effective settings.
- **What is real contribution receptivity?** Local `CONTRIBUTING.md` and merge commits are not enough. What resolves: live GitHub PR/issue analysis when network/auth allows, plus external-contributor sampling.
- **How coherent is solo-to-team transition?** Features exist, but composition is untested. What resolves: scenario walkthrough from solo Context A project to team Context B/E project using source/runtime, not docs alone.
- **What surfaces are actually user-stable?** Rapid releases and schema/version churn suggest surface stability differs by layer. What resolves: selected tag diff sampling plus changelog/GitHub release body review.
- **Does Context F require new semantics or just better composition?** First-wave cannot decide whether anticipatory scaling is satisfied by optional features. What resolves: incubation checkpoint anchored to Logan's actual target contexts, then a second-wave design spike.
- **Can release/RC semantics stay artifact-level?** Prompt-mediated release templates may be enough for Context A/F, insufficient for Context B/C. What resolves: scenario-specific release workflow spike.

## §5. Recommendations for incubation-checkpoint

- Re-read the goal articulation and explicitly choose the context mix before choosing the R mix. My synthesis read is Context A primary with Context F/B adjacency, but that is interpretive and Logan's read is binding.
- Do not ask "R2 or not?" as a binary. Ask which of the four extension/configuration/orchestration surfaces can carry the first concrete target, and only then whether R1/R3/R5 are needed.
- Treat R4 as first-class in the checkpoint. The evidence base repeatedly shows composable primitives and headless/machine surfaces; forcing these into R2 would be a silent-default narrowing.
- Require source/runtime verification before relying on any default behavior surfaced only in README or user docs. Specific checks: reassessment default, team-mode effective preferences, extension compatibility enforcement, and release workflow state advancement.
- If proceeding, pick a first second-wave target that tests the frame cheaply. Good candidates: effective-state visibility; a release metadata/checklist artifact linked to milestones; a Context A/F long-arc decision trace skill/workflow; or a headless orchestration recipe. Avoid starting with Pi seam refactoring or deterministic release engines unless incubation explicitly decides those are load-bearing.
- If R5 becomes live, dispatch a competitor/sibling-harness landscape probe before design. The current evidence says gsd-2 is useful and instructive, not that it must be the sole substrate.

## §6. Confidence and limits

- Confidence is high on source-verifiable structural claims: package identity, vendored Pi packages, ADR-010 proposed status, RTK opt-in gating, extension-surface plurality, markdown-phase prompt-dispatch semantics, shallow tag/commit facts, and release/API-breaking templates.
- Confidence is medium-high on cross-slice patterns: product-scale runtime, extension plurality, prompt-mediated release workflow limits, documentation/source drift, and machinery-vs-practice.
- Confidence is medium or medium-low on operating-frame implications: R4 weighting, Context A/F anchoring, R5 relevance, and whether release machinery is culturally reliable. These are interpretive.
- I did not read the forbidden same-vendor `SYNTHESIS.md`, Gemini deep-research directory, or named handoff. This preserves independence but means I did not compare against the same-vendor synthesis.
- I spot-verified selected source claims, not every citation in all slices. The audits already performed source verification for slices 2, 4, and 5; my independent checks focused on claims that change R-strategy or contradiction handling.
- First-wave evidence is sufficient for incubation to operate, but not sufficient for second-wave design to start without at least one context/R-target narrowing decision.
- Cross-vendor framing-leakage caveat: I am cross-vendor relative to the same-vendor synthesis, but I am still reading through the dispatching project's framing-widening vocabulary. The R1-R5 and six-context frames are useful inputs, not observed facts in gsd-2. Where they overfit the evidence, incubation should loosen them rather than treat this synthesis as authority.

## §7. Cross-vendor caveat

This is a cross-vendor (codex GPT-5.5 high) synthesis paired with `SYNTHESIS.md` (Claude Opus xhigh). I did not read `SYNTHESIS.md` to preserve independence. The downstream comparison artifact will integrate both syntheses for incubation-checkpoint.
