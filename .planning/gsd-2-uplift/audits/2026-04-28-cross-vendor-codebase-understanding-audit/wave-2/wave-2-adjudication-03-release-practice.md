---
type: wave-2-adjudication
date: 2026-04-28
adjudicator: release-practice
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 03 — Release / Practice

## 0. Adjudication Summary

The current Claude investigation remains usable for the release/practice domain, with localized qualifications. The main synthesis pattern survives: gsd-2 has substantial release and breaking-change machinery, while the inspected practice evidence shows release communication often happening through changelog narrative and ordinary commit categories rather than formal `BREAKING CHANGE` markers. The important correction is scope: this is a shallow-history-bounded visible-window finding, not a complete-history or culture-level claim.

High-severity downstream correction: do not treat machinery as effective stability discipline without source-level verification of the specific uplift surface. Medium-severity correction: do not treat bundled release/hotfix/API-breaking templates as proof of the repo maintainers' own release practice; source shows the repo's production release path is GitHub Actions plus scripts.

## 1. Claim Verdict Table

| Claim family | Verdict | Severity | Confidence | One-line reason |
|---|---|---|---|---|
| Machinery-vs-practice: stable pattern vs transition state | Survives with qualification | high | medium-high | Machinery/practice divergence is source-supported in the visible window; stability vs transition remains unresolved. |
| Visible removals and meaningful deprecation | Survives with qualification | high | medium | OAuth and `/gsd map-codebase` support "no visible local pre-deprecation found," not "no meaningful deprecation existed anywhere." |
| Absent `BREAKING CHANGE` markers and convention-enforcement gap | Survives with qualification | medium-high | medium | Marker absence is real in inspected local history; enforcement/culture conclusions need PR, CI, and release-body evidence. |
| Rapid cadence and maintenance risk | Survives with qualification | medium | medium | Rapid cadence is strongly visible; material fork/extension risk needs surface-churn and diff sampling. |
| Bundled release/hotfix/API-breaking templates vs actual project practice | Survives with qualification | medium | high | Templates are product capability and project doctrine, but source does not prove maintainers use them for gsd-2 releases. |
| Release mechanics and product workflow interleaving | Survives with qualification | medium | medium | Interleaving is source-supported architecturally, but downstream importance depends on the uplift target surface. |
| Experimental deprecation waiver relevance | Survives with qualification | medium | high for source text, medium-low for relevance | The waiver is source-real; whether it affects uplift-relevant surfaces is not decidable yet. |

## 2. Detailed Adjudication

### 2.1 Machinery-vs-practice: stable pattern vs transition state

- Claim under audit: gsd-2 has release/breaking-change machinery, but observed practice diverges; decide whether this is a stable pattern or only a transition-state observation.
- Current artifact evidence: Scout 03 says formal machinery exists while practice interpretation remains open (`wave-1/wave-1-scout-03-release-practice.md:15-20`, `:57-90`, `:105-110`). Gate 1 explicitly warns not to turn shallow local history into a complete-history claim (`GATE-1-DISPOSITION.md:93-98`). Synthesis states the machinery-vs-practice pattern and leaves feature-vs-transition unresolved (`SYNTHESIS.md:131-148`, `:458-461`).
- Source/history evidence inspected: `package.json` exposes release scripts (`package.json:93-100`); `prod-release.yml` runs changelog generation, version bumping, changelog update, commit/tag, npm publish, GitHub Release, Discord, Docker, and back-merge PR steps (`.github/workflows/prod-release.yml:57-176`); `generate-changelog.mjs` parses conventional commits and maps `BREAKING CHANGE` / `!:` to a major bump (`scripts/generate-changelog.mjs:45-67`, `:93-125`); `CONTRIBUTING.md` requires explicit breaking-change disclosure (`CONTRIBUTING.md:120-122`); PR template has a breaking-changes checkbox (`.github/PULL_REQUEST_TEMPLATE.md:51-54`). Current local history remains shallow: `git rev-parse --is-shallow-repository` returned `true`; `git rev-list --count HEAD` and `git rev-list --count --since="6 months ago" HEAD` both returned `2227`, showing the requested six-month window is still truncated by visible history. `git log --since="6 months ago" --pretty=format:%s | rg -i "^feat\([^)]*\)!:|^fix\([^)]*\)!:|BREAKING CHANGE|breaking change|!:"` returned no matches.
- Reasoning: The existence of machinery is strong. The visible-window practice gap is also real: current release tooling can react to formal breaking markers, but inspected commit subjects do not use them. That supports the synthesis's warning against trusting machinery alone. It does not support the stronger claim that this is a stable maintainer culture or durable project pattern; shallow history and no PR/release-body inspection leave transition-state plausible.
- Verdict: Survives with qualification.
- Severity: high.
- Confidence: medium-high.
- Downstream correction or qualification: State "visible-window machinery/practice divergence" rather than "stable practice divergence" or "culture." For uplift, source-verify stability claims for the specific surface being extended.

### 2.2 Visible removals and meaningful deprecation

- Claim under audit: OAuth and `/gsd map-codebase` removals show recent removals lacked meaningful deprecation.
- Current artifact evidence: Slice 5 says observed practice includes staged deprecation in some cases but OAuth removal and `/gsd map-codebase` removal lack visible pre-deprecation in the shallow read (`05-release-cadence-output.md:316-318`). The slice audit validates the OAuth hedge and says shallow truncation could hide earlier deprecation (`05-release-cadence-audit.md:63-67`). Scout 03 frames this as a high-adjudication claim because "meaningful" deprecation may appear in PRs, release bodies, runtime warnings, docs, or issue threads (`wave-1/wave-1-scout-03-release-practice.md:112-115`).
- Source/history evidence inspected: `CHANGELOG.md` records `/gsd map-codebase` removal under `2.74.0` `### Changed` (`CHANGELOG.md:552-557`) and Anthropic OAuth removal under `2.70.0` `### Fixed` (`CHANGELOG.md:769-778`). Runtime source says Anthropic OAuth was removed in v2.74.0 and self-heals stale OAuth credentials (`packages/pi-coding-agent/src/core/sdk.ts:476-503`). Visible commit search found `c2acb1fb4 2026-04-10 fix(pi-ai): remove Anthropic OAuth flow for TOS compliance` and `5e1a5d267 2026-04-14 refactor(gsd): remove /gsd map-codebase command`. In contrast, current MCP aliases have an explicit staged deprecation entry in `[Unreleased]` (`CHANGELOG.md:7-10`) and telemetry source says it is "Step 1 of a two-step deprecation" (`packages/mcp-server/src/alias-telemetry.ts:1-9`).
- Reasoning: The two examples support a narrower claim: the inspected local changelog and visible commit subjects do not show staged pre-deprecation before the removals, and they classify the changes under ordinary `Fixed` / `Changed` sections. They do not prove lack of meaningful user-facing deprecation because this pass did not inspect PR bodies, GitHub Release bodies, issue discussions, Actions annotations, npm deprecations, or external docs as users would encounter them. OAuth also has a compliance rationale, which may justify a different deprecation path.
- Verdict: Survives with qualification.
- Severity: high.
- Confidence: medium.
- Downstream correction or qualification: Use "no visible local pre-deprecation found for these examples" and do not upgrade it to "no meaningful deprecation" without PR/release/user-facing evidence.

### 2.3 Absent `BREAKING CHANGE` markers and convention-enforcement gap

- Claim under audit: absence of `BREAKING CHANGE` markers shows a convention-enforcement gap, not merely no marker usage in the inspected window.
- Current artifact evidence: Scout 03 reports zero visible-history commit subjects matching `BREAKING CHANGE`, lower-case "breaking change," or conventional `!:` markers (`wave-1/wave-1-scout-03-release-practice.md:18`, `:42-45`, `:86-89`). Slice audit independently corroborates no `### Breaking Changes` section and no matching visible-history subject search (`05-release-cadence-audit.md:57-61`). Synthesis carries this as observed practice operating outside formal channels (`SYNTHESIS.md:37`, `:141-147`).
- Source/history evidence inspected: `CONTRIBUTING.md` says commit messages must follow Conventional Commits and claims the commit-msg hook and CI enforce that (`CONTRIBUTING.md:36-42`). The release workflow template says to propose `major` for `BREAKING CHANGE:` or `!` suffix (`src/resources/extensions/gsd/workflow-templates/release.md:36-40`). The changelog generator detects `BREAKING CHANGE` / `!:` and maps breaking changes to major version bumps (`scripts/generate-changelog.mjs:58-67`, `:96-125`). The local command `git log --since="6 months ago" --pretty=format:%s | rg -i "^feat\([^)]*\)!:|^fix\([^)]*\)!:|BREAKING CHANGE|breaking change|!:"` returned no matches. `rg` over `CHANGELOG.md` found incidental uses of "breaking" but no `### Breaking` heading; relevant explicit sections include `### Deprecated` and `### Removed` elsewhere (`CHANGELOG.md:9-10`, `:1675-1681`).
- Reasoning: The absence finding survives for inspected local history. It also weakens any claim that the formal breaking marker convention is the operative communication channel in this window. However, "convention-enforcement gap" is ambiguous. If it means "CI/commit-msg enforcement does not exist," I did not verify that. If it means "the release generator's breaking marker channel is not visibly used for the removals and commits inspected," the claim survives. There may simply have been no semver-major changes, or maintainers may treat narrative changelog categories as sufficient.
- Verdict: Survives with qualification.
- Severity: medium-high.
- Confidence: medium.
- Downstream correction or qualification: Phrase as "marker-usage gap in inspected visible history" or "formal breaking-marker channel not visibly used," not as a proven enforcement or culture gap.

### 2.4 Rapid cadence and maintenance risk

- Claim under audit: rapid visible cadence materially increases fork/extension maintenance risk.
- Current artifact evidence: Slice 5 reports shallow history, `2216` visible commits, 34 visible tags dated 2026-03-20 through 2026-04-25, and average visible tag gap `0.160` weeks (`05-release-cadence-output.md:21-34`, `:252-294`). The slice audit verifies the cadence math and the shallow hedging (`05-release-cadence-audit.md:21-43`, `:95-106`). Source freshness delta says the newer `82bcf6b71..bf1d8aad0` range adds 10 more commits and touches runtime/extension files but not release machinery (`SOURCE-FRESHNESS-DELTA-2026-04-28.md:17-22`, `:83-94`).
- Source/history evidence inspected: Current HEAD is `bf1d8aad0`. The repository is shallow. `git rev-list --count HEAD` and `git rev-list --count --since="6 months ago" HEAD` both returned `2227`. `git log --format=%h%x09%cs%x09%s -10` showed all latest ten commits on 2026-04-27. `git tag --merged HEAD` returned the same 34 release tags from `v2.36.0` through `v2.78.1`. The current local tag ref set also contains many older tags not merged into visible `HEAD`; therefore the "34 tags" claim should be read as merged-visible tags, not all local tag refs.
- Reasoning: The cadence is rapid enough that fork tracking and extension compatibility plausibly become nontrivial. But cadence alone is not a complete maintenance-risk measure. Risk depends on changed-surface churn, API compatibility, test coverage, extension boundaries, release size, and how often uplift-dependent files move. The freshest 10-commit delta did touch runtime/extension behavior, which is directionally relevant, but this pass did not sample release-to-release diffs or extension-surface churn.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: medium.
- Downstream correction or qualification: Use cadence as a maintenance-risk pressure, not as a decisive risk finding. Before committing to a fork/extension strategy, sample diffs across representative tags for the exact surfaces the uplift would depend on.

### 2.5 Bundled release/hotfix/API-breaking templates vs actual project practice

- Claim under audit: bundled release/hotfix/API-breaking templates reflect actual project practice, product capability, or both; determine whether synthesis overstates interleaving by conflating templates with the repo's own release process.
- Current artifact evidence: Scout 03 distinguishes workflow templates from the repo's production release path and warns not to treat templates as proof that maintainers use them for gsd-2 releases (`wave-1/wave-1-scout-03-release-practice.md:76-90`, `:127-130`, `:154`). Synthesis says the release templates live in the workflow-plugin subsystem while gsd-2's own release uses CI scripts outside that subsystem (`SYNTHESIS.md:110-115`). Gate 1 identifies template-vs-practice as a release/practice claim family (`GATE-1-DISPOSITION.md:134-144`).
- Source/history evidence inspected: Workflow plugin discovery explicitly supports project, global, and bundled workflow definitions and declares `markdown-phase` as `STATE.json + phase gates` (`src/resources/extensions/gsd/workflow-plugins.ts:1-13`). The registry defines `release` as `markdown-phase` with `.gsd/workflows/releases/` artifacts and `api-breaking-change` as `markdown-phase` with `.gsd/workflows/api-breaks/` artifacts (`src/resources/extensions/gsd/workflow-templates/registry.json:213-233`). The release template itself instructs version bumping, changelog generation, tags, push, release pipeline, and GitHub Release creation (`src/resources/extensions/gsd/workflow-templates/release.md:11-23`, `:31-48`, `:54-76`, `:82-117`). The API-breaking template encodes staged survey/migrate/deprecate/release (`src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:11-23`, `:46-54`, `:75-96`, `:98-115`). The hotfix template is intentionally minimal (`src/resources/extensions/gsd/workflow-templates/hotfix.md:11-20`, `:24-45`). The repo's production release workflow is a manual GitHub Action using scripts directly (`.github/workflows/prod-release.yml:1-8`, `:57-176`), with dev/next publish also manual workflow-dispatch paths (`.github/workflows/dev-publish.yml:1-15`, `:75-109`; `.github/workflows/next-publish.yml:1-13`, `:74-127`).
- Reasoning: Templates are real product capability and encode project-recommended procedure. They are not, by themselves, proof of actual maintainer practice for the gsd-2 repository. The current synthesis is acceptable because it explicitly separates "templates live in workflow subsystem" from "own release uses CI scripts." Any downstream argument that "maintainers release gsd-2 through `/gsd workflow release`" would be unsupported by inspected evidence.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: high.
- Downstream correction or qualification: Treat templates as capability/doctrine evidence unless Actions logs, `.gsd/workflows/` artifacts, PRs, or maintainer docs connect them to actual gsd-2 release execution.

### 2.6 Release mechanics and product workflow interleaving

- Claim under audit: release mechanics and product workflow are tightly interleaved; decide whether this is source-supported and whether it matters for uplift design.
- Current artifact evidence: Slice 5 flags "release mechanics and product workflow are tightly interleaved" but defers interpretation to synthesis (`05-release-cadence-output.md:412`). Slice audit preserves that as direction-shifting evidence but says it is interpretive (`05-release-cadence-audit.md:108-128`). Synthesis carries the pattern and notes that own-release CI scripts run outside the workflow plugin system (`SYNTHESIS.md:110-115`).
- Source/history evidence inspected: Release-related capabilities exist in product workflow templates (`src/resources/extensions/gsd/workflow-templates/registry.json:213-233`), source release scripts (`package.json:93-100`; `scripts/generate-changelog.mjs:1-152`; `scripts/bump-version.mjs:20-77`; `scripts/update-changelog.mjs:33-58`), GitHub Actions (`.github/workflows/prod-release.yml:57-176`), and package-channel workflows (`.github/workflows/dev-publish.yml:75-109`; `.github/workflows/next-publish.yml:74-127`). Cleanup automation also exists for stale dev versions (`.github/workflows/cleanup-dev-versions.yml:3-6`, `:21-57`).
- Reasoning: Source supports interleaving in an architectural/product-surface sense: release workflows are part of the bundled workflow-plugin catalog, and release mechanics are embodied both as product templates and repo CI/scripts. The adjective "tightly" is interpretive. The synthesis does not collapse all paths into one engine; it correctly notes product templates and own-release scripts are separate. For uplift, this matters if the target design touches release coordination, workflow plugins, semver automation, CI/headless recipes, or API-breaking discipline. It is only background architecture if the uplift target is unrelated to release/workflow coordination.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: medium.
- Downstream correction or qualification: Keep "interleaving" as a design warning, not a universal architectural law. The needed intervention shape may be workflow-plugin, CI/script, headless orchestration, or documentation depending on the actual uplift target.

### 2.7 Experimental deprecation waiver relevance

- Claim under audit: the experimental deprecation waiver is source-real and affects uplift-relevant surfaces.
- Current artifact evidence: Scout 03 confirms the text exists but marks policy impact as high-adjudication (`wave-1/wave-1-scout-03-release-practice.md:68`, `:142-145`). Slice 5 reports experimental features are opt-in and may change or be removed without deprecation (`05-release-cadence-output.md:346`). Synthesis includes the waiver as part of the machinery-vs-practice pattern (`SYNTHESIS.md:146-147`).
- Source/history evidence inspected: `ExperimentalPreferences` says all features in the block are disabled by default, must be explicitly enabled, and may change or be removed without a deprecation cycle while experimental (`src/resources/extensions/gsd/preferences-types.ts:277-288`).
- Reasoning: The waiver is source-real and unambiguous. Its downstream relevance is not decidable from release/practice evidence alone because uplift-dependent surfaces have not been selected here. It matters if an uplift plan depends on experimental preferences or an experimental-gated runtime surface such as RTK. It does not automatically weaken all extension or release surfaces.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: high for source text, medium-low for relevance.
- Downstream correction or qualification: Before relying on a surface, classify whether it is experimental-gated. If yes, treat deprecation guarantees as weaker unless a later ADR or maintainer commitment narrows the waiver.

## 3. Evidence Needed But Not Gathered

- GitHub PR bodies and review discussions for the OAuth removal, `/gsd map-codebase` removal, MCP alias deprecation, and release commits.
- GitHub Release bodies for `v2.70.0`, `v2.74.0`, `v2.78.0`, and `v2.78.1`, plus whether release bodies contained stronger migration/deprecation language than `CHANGELOG.md`.
- Actions logs for prod/dev/next release runs to determine actual maintainer practice, approval gates, and whether workflow templates are ever involved.
- History deepening or a non-shallow clone if complete six-month cadence and complete negative evidence are needed.
- Representative tag-to-tag diff sampling for uplift-relevant surfaces, especially extension APIs, workflow plugin schema, headless/RPC/MCP surfaces, and experimental-gated features.
- CI/commit-hook inspection sufficient to decide whether Conventional Commit enforcement includes breaking-marker semantics or only generic commit-shape validation.

## 4. Cross-Domain Flags

- Extension/workflow adjudication should treat release, hotfix, and API-breaking workflows as `markdown-phase` product templates, not deterministic release executors by default (`src/resources/extensions/gsd/workflow-plugins.ts:8-11`; `src/resources/extensions/gsd/workflow-templates/registry.json:213-233`).
- Topology/runtime and extension/workflow adjudication should source-verify stability claims for specific surfaces. Release machinery does not by itself guarantee deprecation discipline on every runtime or extension surface.
- The source freshness delta did not touch release machinery or tags, but it did add runtime/extension changes after Scout 03; this reinforces activity pressure without changing release-practice evidence (`SOURCE-FRESHNESS-DELTA-2026-04-28.md:83-94`).
- Experimental preference gating is a cross-domain concern only when an uplift design depends on experimental features; release/practice evidence alone cannot identify that dependency.

## 5. Limits

- I did not deepen, unshallow, fetch, or otherwise modify `/home/rookslog/workspace/projects/gsd-2-explore/`.
- I did not use network evidence, GitHub PR bodies, GitHub Release pages, npm registry state, Actions logs, or issue discussions.
- I did not construct a full release-practice model for gsd-2.
- I did not sample full diffs across tags or decide which uplift surfaces are stable.
- Negative findings about missing pre-deprecation and missing `BREAKING CHANGE` markers are bounded by inspected local source and visible shallow history.

## 6. Recommendation For Gate 2

localized qualifications needed
