---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 03 release-practice
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 03 — Release / Practice

## 0. Scout Summary

- Source preflight confirms `/home/rookslog/workspace/projects/gsd-2-explore/` is a shallow clone: `git rev-parse --is-shallow-repository` returned `true`.
- Visible local history contains 2217 commits and 34 tags, with visible tags from `v2.36.0` dated 2026-03-20 through `v2.78.1` dated 2026-04-25. This supports "rapid in visible window" as a local-history observation, not a complete six-month claim.
- Formal release machinery exists in package scripts, GitHub workflows, changelog scripts, workflow templates, PR/contribution policy, and Keep-a-Changelog structure.
- Formal breaking-change/deprecation machinery exists: `CONTRIBUTING.md` asks for explicit breaking-change disclosure, the release workflow and changelog generator detect `BREAKING CHANGE` / `!`, and the API-breaking-change template stages survey/migrate/deprecate/release.
- Observed current changelog practice includes staged deprecation for MCP aliases in `[Unreleased]`, but also visible removals under `Fixed`/`Changed` sections.
- A local visible-history subject search found zero commit subjects matching `BREAKING CHANGE`, `breaking change`, or conventional `!:` breaking markers.
- The source workflow templates for release/hotfix/API breaking changes are agent-prompted Markdown workflows; gsd-2's own production release path is a GitHub Actions/script path.
- Current synthesis artifacts correctly flag machinery-vs-practice as load-bearing, but stable-pattern vs transition-state remains non-mechanical and needs high adjudication.

## 1. Commands Run

- `git -C /home/rookslog/workspace/projects/gsd-2-explore rev-parse --is-shallow-repository`
  - Result: `true`. History-derived negative findings are shallow-clone-bounded.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore log --oneline --decorate -30`
  - Result: latest 30 commits span 2026-04-26 to 2026-04-27 and include recent merges/fixes around worktree and safety handling.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore log --format=%h%x09%cs%x09%d%x09%s -30`
  - Result: same 30-commit window with dates; latest visible commit was `82bcf6b7` on 2026-04-27.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore log --oneline`
  - Result: command output had 2217 lines in this shallow clone.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore tag --list`
  - Result: 34 visible tags, `v2.36.0` through `v2.78.1`.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore for-each-ref --sort=creatordate --format='%(refname:short)%09%(creatordate:short)%09%(objectname:short)' refs/tags`
  - Result: tags date from 2026-03-20 through 2026-04-25.
- `rg -n "BREAKING CHANGE|!:\\s|Breaking changes|breaking change|Deprecated|Removed|deprecat|migrat|release|hotfix|changelog|version" /home/rookslog/workspace/projects/gsd-2-explore`
  - Result: broad source search found release scripts, changelog entries, workflow templates, deprecation references, migration code, and many version/migration hits.
- `find /home/rookslog/workspace/projects/gsd-2-explore/.github -maxdepth 4 -type f`
  - Result: found release/publish/CI/risk/version workflows plus issue/PR templates.
- `rg --files /home/rookslog/workspace/projects/gsd-2-explore | rg "(release|hotfix|changelog|version|bump|breaking|deprecat|migrat)"`
  - Result: found release/hotfix/API-breaking workflow templates, changelog scripts, migration files, release checklist template, and migration docs.
- `rg -n "BREAKING CHANGE|^### Breaking|!:" ...`
  - Result: formal machinery hits in `CONTRIBUTING.md`, workflow templates, and scripts; no `CHANGELOG.md` `### Breaking` section hit in this targeted command.
- `git -C /home/rookslog/workspace/projects/gsd-2-explore log --since="6 months ago" --pretty=format:%s | rg -i "^feat\\([^)]*\\)!:|^fix\\([^)]*\\)!:|BREAKING CHANGE|breaking change"`
  - Result: no matches, exit code 1.
- I also read citeable line ranges from `package.json`, `CHANGELOG.md`, `.github/workflows/*.yml`, release scripts, workflow templates, `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `preferences-types.ts`, and the three current exploration/synthesis artifacts named in the spec.

## 2. History Depth / Tag Caveats

The clone is shallow. `git rev-parse --is-shallow-repository` returned `true`, and no deepen/fetch was performed. Therefore:

- Commit-count and cadence observations are lower-bound / visible-window observations.
- Absence of older pre-deprecation evidence cannot be treated as evidence that no pre-deprecation ever existed.
- The 34 visible tags are locally available and date from 2026-03-20 to 2026-04-25, but tags before the shallow boundary inside a broader six-month window cannot be ruled out.
- The current slice artifact reports the same caveat: repository shallow, total visible commits `2217`, visible six-month command `2216`, and history truncated at the shallow boundary (`05-release-cadence-output.md:21-34`).

## 3. Machinery Evidence

Source-derived:

- Root package metadata shows current version `2.78.1` and release scripts: `release:changelog`, `release:bump`, and `release:update-changelog` (`/home/rookslog/workspace/projects/gsd-2-explore/package.json:1-4`, `:89-100`).
- `scripts/generate-changelog.mjs` finds the latest stable tag, gathers commits since that tag, parses conventional commits, detects `BREAKING CHANGE` or `!:`, maps breaking commits to a major bump, and emits JSON containing bump/changelog/release-notes data (`scripts/generate-changelog.mjs:14-35`, `:43-67`, `:93-127`, `:129-152`).
- `scripts/bump-version.mjs` updates the root package, workspace package versions, internal dependency references, platform package versions, `pkg/package.json`, and lockfiles (`scripts/bump-version.mjs:20-77`).
- `scripts/update-changelog.mjs` inserts an entry after `[Unreleased]` and updates comparison links (`scripts/update-changelog.mjs:33-58`).
- `CHANGELOG.md` explicitly uses a Keep a Changelog format and currently has `[Unreleased]` plus `### Deprecated` for MCP alias tools (`CHANGELOG.md:1-10`).
- `CONTRIBUTING.md` requires Conventional Commits and says public API, CLI behavior, config format, or file-structure changes must be called out explicitly, with migration guidance as needed (`CONTRIBUTING.md:36-43`, `:120-123`).
- `.github/PULL_REQUEST_TEMPLATE.md` includes a Breaking changes checkbox section (`.github/PULL_REQUEST_TEMPLATE.md:51-55`).
- `preferences-types.ts` states experimental features may change or be removed without a deprecation cycle while experimental (`src/resources/extensions/gsd/preferences-types.ts:277-287`).

Docs/template-derived:

- `prod-release.yml` is a manual `workflow_dispatch` production release with `fetch-depth: 0`, live tests, generated changelog/version, version bump, changelog update, release commit/tag, npm publish/latest promotion, GitHub Release creation, Discord announcement, Docker push, and optional back-merge PR (`.github/workflows/prod-release.yml:1-8`, `:25-29`, `:49-90`, `:92-176`).
- `dev-publish.yml` and `next-publish.yml` are manual publish workflows that stamp `dev`/`next` versions, build, smoke-test, publish to npm dist-tags, and verify installed packages (`.github/workflows/dev-publish.yml:1-15`, `:75-109`; `.github/workflows/next-publish.yml:1-13`, `:74-125`).
- `cleanup-dev-versions.yml` is scheduled weekly and removes stale `-dev.` versions older than `MAX_AGE_DAYS=30` (`.github/workflows/cleanup-dev-versions.yml:3-6`, `:21-57`).
- `version-check.yml` reads issue bodies for a reported GSD version, checks npm latest, comments upgrade instructions, and labels stale-version issues (`.github/workflows/version-check.yml:1-12`, `:31-38`, `:74-109`).
- The bundled `release` workflow template has prepare/bump/publish/announce phases, proposes semver bump using `BREAKING CHANGE:` / `!`, writes release artifacts, updates changelog, tags, pushes, verifies, and creates a GitHub Release (`workflow-templates/release.md:1-23`, `:31-48`, `:54-76`, `:82-117`).
- The bundled `hotfix` template is intentionally minimal: fix, test, commit, create PR, present to user (`workflow-templates/hotfix.md:11-20`, `:24-45`).
- The bundled `api-breaking-change` workflow has staged survey/migrate/deprecate/release phases, asks for caller mapping, migration guidance, deprecation warning, changelog/docs updates, and a major-version removal release (`workflow-templates/api-breaking-change.md:11-23`, `:31-54`, `:75-96`, `:98-115`).
- The bundled `changelog-gen` template categorizes commit prefixes, has a `Breaking` category, and writes/prints Keep-a-Changelog-style entries (`workflow-templates/changelog-gen.md:11-15`, `:19-40`, `:42-73`).

## 4. Practice Evidence

- Visible local tags are frequent: 34 visible tags dated 2026-03-20 through 2026-04-25. This mechanically supports a rapid visible release/tag cadence claim, with shallow caveats.
- Latest visible local release tags include `v2.78.0` and `v2.78.1` both on 2026-04-25; `CHANGELOG.md` also has `2.78.1` and `2.78.0` entries dated 2026-04-25 (`CHANGELOG.md:12-18`).
- Visible recent commits are high-throughput and PR-heavy: the latest 30 include multiple merge commits and fixes from 2026-04-26/27.
- Targeted visible-history commit-subject search for `BREAKING CHANGE`, `breaking change`, or conventional `!:` markers returned no matches.
- Current changelog includes staged deprecation for MCP alias tools in `[Unreleased]`, including telemetry and future removal after zero usage (`CHANGELOG.md:7-10`).
- Current changelog also records `remove Anthropic OAuth flow for TOS compliance` under `2.70.0` `### Fixed`, not under a breaking/removal section (`CHANGELOG.md:769-778`).
- Current changelog records `remove /gsd map-codebase command` under `2.74.0` `### Changed` (`CHANGELOG.md:552-557`).
- The observed production release path in source is GitHub Actions plus scripts; the bundled release workflow template is a product workflow template and should not be treated as proof that gsd-2 maintainers use that template for gsd-2's own releases.

## 5. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source/history evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|
| Release cadence is rapid in the visible history window. | `SYNTHESIS.md:37`, `:144`; `05-release-cadence-output.md:250-257` | 34 visible tags from 2026-03-20 to 2026-04-25; 2217 visible commits; latest 30 commits span roughly one day. | Confirmed for visible local window only. | Yes, for significance and complete-window cadence. |
| The visible history window is shallow-clone-bounded. | `05-release-cadence-output.md:21-34`; `SYNTHESIS.md:59` | `git rev-parse --is-shallow-repository` returned `true`. | Confirmed. | No for fact; yes for implications. |
| Formal breaking-change machinery exists. | `SYNTHESIS.md:134-139`; `05-release-cadence-output.md:332-338`, `:374-380` | `CONTRIBUTING.md`, PR template, release template, API-breaking template, changelog generator, and scripts all have relevant machinery. | Confirmed. | No for existence; yes for effectiveness. |
| Observed commits/changelog entries do not use `BREAKING CHANGE` markers. | `SYNTHESIS.md:141-145`; `05-release-cadence-output.md:316-318` | Targeted visible-history subject search found no matches; `rg` found machinery hits but no `CHANGELOG.md` breaking section hit. | Confirmed for inspected local visible history. | Yes, because deeper history/GitHub release bodies were not inspected. |
| Recent removals appear without visible pre-deprecation in inspected window. | `SYNTHESIS.md:143`; `05-release-cadence-output.md:316` | OAuth removal is under `Fixed` in v2.70.0; `/gsd map-codebase` removal under `Changed` in v2.74.0. No local pre-deprecation was established in this pass. | Partially confirmed as "no visible pre-deprecation found"; not confirmed as no pre-deprecation existed. | Yes. |
| Release workflow templates are agent-prompted while actual project release scripts run elsewhere. | `SYNTHESIS.md:110-114`; `05-release-cadence-output.md:374-380` | Template is Markdown instruction file; production release workflow runs GitHub Actions and scripts directly. | Confirmed as surface distinction. | Yes, for broader workflow-engine implications. |
| Docs/source/practice divergence is recurring rather than isolated. | `SYNTHESIS.md:117-121`, `:131-148` | This pass only inspected release/practice examples and current synthesis claims. | Not mechanically adjudicated by this scout. | Yes. |
| Experimental preferences waive the deprecation cycle. | `SYNTHESIS.md:146`; `05-release-cadence-output.md:346` | `preferences-types.ts:277-287` explicitly says experimental features may change or be removed without deprecation cycle. | Confirmed. | No for text; yes for policy impact. |

## 6. Claims Needing High Adjudication

1. **Machinery-vs-practice is a stable pattern rather than a transition state.**
   - Why load-bearing: it affects whether extension-surface stability can be trusted.
   - Inspect: deeper git history, GitHub Releases, PR discussions for breaking/removal PRs, `CONTRIBUTING.md`, changelog, release scripts.
   - Non-mechanical because shallow history can catch an organization mid-transition, and pattern stability requires temporal sampling.

2. **Recent removals lacked meaningful user-facing deprecation.**
   - Why load-bearing: this is the strongest practice-side evidence against relying on staged deprecation.
   - Inspect: diffs/PRs/releases around `v2.70.0`, `v2.74.0`, OAuth removal, `/gsd map-codebase` removal, GitHub Release bodies.
   - Non-mechanical because "meaningful" deprecation can occur in PRs, release bodies, runtime warnings, docs, or issue threads.

3. **Zero `BREAKING CHANGE` markers means convention-enforcement gap, not just no major-breaking changes.**
   - Why load-bearing: the release generator's semver behavior depends on markers.
   - Inspect: commit subjects/bodies, merge commit bodies, release PRs, CI checks for conventional commits.
   - Non-mechanical because absence of markers must be interpreted against the actual semantic breakage of changes.

4. **Release cadence materially increases fork/extension maintenance risk.**
   - Why load-bearing: it affects R1/R2/R3 strategy costs.
   - Inspect: tag cadence over complete history, diff size per release, extension-surface churn, dependency/update compatibility windows.
   - Non-mechanical because high cadence can be either stabilizing or destabilizing depending on release size and compatibility practice.

5. **Bundled release/hotfix/API-breaking workflow templates reflect project practice.**
   - Why load-bearing: templates could indicate intended workflow culture, but gsd-2's own prod release uses scripts/workflows.
   - Inspect: actual `.gsd/workflows/` artifacts if available, PR/release history, maintainer docs, Actions logs.
   - Non-mechanical because templates are capabilities; actual use requires practice evidence.

6. **Release mechanics and product workflow are tightly interleaved in a way that should shape uplift design.**
   - Why load-bearing: synthesis uses this to warn against separating release cadence from workflow mechanics.
   - Inspect: workflow plugin registry, release templates, GitHub workflows, GSD milestone/report/update/check surfaces.
   - Non-mechanical because interleaving significance depends on proposed uplift act and target runtime surface.

7. **Contribution policy and observed practice diverge in culturally important ways.**
   - Why load-bearing: affects R3 upstream contribution strategy.
   - Inspect: `CONTRIBUTING.md`, PR template, merged PRs, maintainer review comments, rejected PRs, checks.
   - Non-mechanical because written policy and maintainer practice can diverge benignly or materially.

8. **Experimental deprecation waiver creates instability for uplift-relevant surfaces.**
   - Why load-bearing: uplift may depend on features currently considered experimental.
   - Inspect: which uplift-relevant features live under `experimental`, release notes for experimental changes, migration paths out of experimental.
   - Non-mechanical because the waiver's practical risk depends on which surfaces the uplift work would depend on.

## 7. Scope Boundaries

- I did not deepen, fetch, or otherwise modify the read-only source target.
- I did not inspect network GitHub Releases, Actions run history, npm registry state, PR discussions, or issue discussions.
- I did not do a full diff sample across tags; removals were checked through current changelog/source surfaces and visible local history searches.
- I did not adjudicate extension-surface taxonomy, runtime topology outside release surfaces, or maintainer receptiveness.
- I did not decide whether gsd-2 release discipline is good, bad, stable, unstable, or culturally coherent.
- I treated workflow templates as machinery/capability evidence, not as proof of actual maintainer release practice.

## 8. Scout Caveat

This is a medium-reasoning source/history scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2` release practice.

## Source Freshness Addendum — 2026-04-28

Provisional delta note for `82bcf6b71..bf1d8aad0`: the release/practice findings above are not materially invalidated, but the latest visible commit observation is stale after fetch.

- The fetched range contains 10 commits: two merge commits and eight focused fix/test commits.
- The changed files are concentrated in `AgentSession` auto-mode handoff behavior, `gsd auto` TTY-gated routing, and Claude Code CLI permission persistence tests/logic.
- The range does not touch `CHANGELOG.md`, release workflows, release scripts, contribution policy, PR templates, version metadata, or tags.
- No commit subject in the inspected range uses `BREAKING CHANGE` or a conventional `!:` breaking marker.

Delta judgment: addendum enough; no full Scout 03 rerun is recommended from this range alone unless the audit needs complete current release/tag state rather than local fetched-range freshness.
