---
slice: 5 (Concrete observable patterns: release cadence + breaking-change posture + features)
date: 2026-04-28
agent: codex GPT-5.5 high
status: complete
---

# Slice 5 output — Concrete observable patterns: release cadence + breaking-change posture + features

## (i) What I read

### gsd-2 git history and release metadata

- Git preflight commands in `/home/rookslog/workspace/projects/gsd-2-explore/`.
- `git log --since="6 months ago" --pretty=format:"%h %ai %s" | head -100`.
- `git tag --sort=-creatordate | head -30`.
- `git log --tags --pretty=format:"%h %ai %d %s" | head -30`.
- `git for-each-ref --sort=creatordate --format='%(refname:short) %(creatordate:iso8601) %(objectname:short) %(subject)' refs/tags`.
- Recent commit searches for deprecation/removal/breaking-change language.

Preflight raw output:

```text
$ git rev-parse --is-shallow-repository
true

$ git log --oneline | wc -l
2217

$ git log --since="6 months ago" --pretty=format:"%h" | wc -l
2216
```

Shallow-history caveat: the repository is shallow, total visible commits are `2217`, and commits in the six-month window are `2216`. History appears truncated at the shallow boundary; cadence numbers below are lower-bound/visible-history numbers. Dispatcher should deepen the clone and re-dispatch slice 5 if precise six-month cadence is needed.

Required Q1 raw output:

```text
$ git log --since="6 months ago" --pretty=format:"%h %ai %s" | head -100
82bcf6b7 2026-04-27 09:50:47 -0500 Merge pull request #5080 from jeremymcs/fix/headless-auto-cwd-anchor
8cd352fd 2026-04-27 09:35:12 -0500 test(gsd): restore cwd before temp repo cleanup
7cfa24af 2026-04-27 09:19:28 -0500 fix(gsd): anchor cwd without cwd guard
4aff417e 2026-04-27 09:10:00 -0500 fix(gsd): anchor cwd at project root in mergeAndExit (closes #5079)
0fdacd52 2026-04-27 00:33:45 -0500 Merge pull request #5062 from jeremymcs/fix/worktree-path-injection
fabecd48 2026-04-27 00:10:21 -0500 fix(gsd): harden worktree dispatch cwd handling
de73fb43 2026-04-26 23:53:41 -0500 fix(gsd): stop dispatch on cwd anchor failures
e42fc0fc 2026-04-26 23:33:49 -0500 test(gsd): cover worktree path injection
ca7a0bc1 2026-04-26 23:24:24 -0500 fix(gsd): anchor subagent dispatch to canonical worktree path
8a893322 2026-04-26 22:22:39 -0500 Merge pull request #5060 from jeremymcs/chore/expose-bundled-skills
325aae48 2026-04-26 22:13:56 -0500 Merge pull request #5055 from jeremymcs/feat/worktree-tui-commands
3980eb93 2026-04-26 22:07:59 -0500 test(gsd): tidy bundled skill trigger regressions
f6b3faa0 2026-04-26 22:06:55 -0500 Merge pull request #5058 from jeremymcs/fix/safety-harness-bash-evidence-race
1c6ebe3c 2026-04-26 22:02:05 -0500 chore(gsd): expose 11 previously-invisible bundled skills to system prompt
17fce646 2026-04-26 21:49:12 -0500 fix(gsd): harden worktree dirty handling
da7dd56e 2026-04-26 21:38:18 -0500 fix(safety): persist bash evidence at tool_call to close mid-unit re-dispatch race (#5056)
4e1d63db 2026-04-26 21:33:58 -0500 fix: clarify worktree clean retention reasons
04099eec 2026-04-26 21:21:18 -0500 fix: clarify worktree merge cleanup failures
9c7ef21b 2026-04-26 21:08:38 -0500 docs(gsd): document worktree tui commands
ca1f6daf 2026-04-26 21:01:52 -0500 Merge pull request #5053 from jeremymcs/chore/welcome-screen-mcp-row
2361ceeb 2026-04-26 21:00:03 -0500 feat(gsd): add worktree {list,merge,clean,remove} commands to TUI dispatcher
585e6ff4 2026-04-26 20:28:05 -0500 chore(welcome-screen): surface MCP server count in banner, suppress google_search deprecation
9d08d820 2026-04-26 20:03:26 -0500 Merge pull request #5036 from TommyC81/fix/5015-windows-home-dir
939b75e4 2026-04-26 20:03:01 -0500 Merge pull request #5045 from jeremymcs/feat/5003-ollama-timeout-env
cd22f0c0 2026-04-26 20:02:33 -0500 Merge pull request #5046 from jeremymcs/fix/4991-ollama-prefix-shadowing
780a8220 2026-04-26 20:02:17 -0500 Merge pull request #5042 from jeremymcs/fix/5017-windows-dep0190
f857a68b 2026-04-26 20:01:53 -0500 Merge pull request #5043 from jeremymcs/fix/4946-types-semver
2bf4caa2 2026-04-26 20:00:54 -0500 Merge pull request #5047 from jeremymcs/claude/research-agents-tasks-RyNx3
16f025a0 2026-04-26 20:00:33 -0500 Merge pull request #5051 from jeremymcs/fix/worktree-root-normalization
36a959ca 2026-04-26 19:50:06 -0500 fix(gsd): preserve inspected empty subagent inputs
cf9927a1 2026-04-26 19:49:42 -0500 fix(gsd): normalize auto worktree loop roots
bdc71391 2026-04-26 19:19:15 -0500 Tighten planning-dispatch stale caller shim
85588a69 2026-04-26 19:03:40 -0500 Fail closed on missing planning dispatch agents
02a7aca0 2026-04-26 18:50:13 -0500 Enforce planning dispatch agent allowlist
2e4e36a2 2026-04-26 18:44:23 -0500 Merge branch 'main' of https://github.com/gsd-build/gsd-2 into HEAD
759eab71 2026-04-26 18:35:56 -0500 fix: gate planning subagent dispatch
f6d51492 2026-04-26 18:32:13 -0500 fix(gsd): normalize worktree project roots
566bf768 2026-04-26 17:18:53 -0500 fix(gsd): restore prompt contract CI
6dcb8738 2026-04-26 17:04:25 -0500 test ollama timeout clamp edge cases
ebcd166b 2026-04-26 16:59:31 -0500 docs(gsd): document reactive execution defaults
d4ef437f 2026-04-26 16:53:45 -0500 fix(ollama): clamp timeout env timer values
be6fc9d3 2026-04-26 16:39:09 -0500 fix(ollama): correct context window for cloud / long-variant models
4b4ab00f 2026-04-26 21:37:55 +0000 feat(unit-manifest): introduce planning-dispatch mode for slice plan/complete
dd4bb494 2026-04-26 21:37:35 +0000 feat(auto-prompts): surface manifest skills via recommendations + auto-match
e16dcc63 2026-04-26 21:37:23 +0000 feat(auto-dispatch): default reactive-execute on at >=3 ready tasks
38316089 2026-04-26 21:37:09 +0000 feat(subagent): add dispatch telemetry and stronger prompt guidelines
6132d408 2026-04-26 16:34:35 -0500 feat(ollama): configurable probe/request timeouts via env vars
f4e576cc 2026-04-26 21:12:03 +0000 Revert "docs(agents): surface bundled agents and skills as first-class guidance"
fbde6a5c 2026-04-26 16:02:42 -0500 test: fix dep0190 regression file urls
a365eeee 2026-04-26 16:00:45 -0500 fix(extensions): drop semver dep, replace with inline isVersionGreater
3051c02b 2026-04-26 20:52:10 +0000 docs(agents): surface bundled agents and skills as first-class guidance
d8f01545 2026-04-26 15:50:48 -0500 fix(windows): avoid DEP0190 in Claude CLI binary probes
84a383f5 2026-04-26 15:11:23 -0500 Merge pull request #5041 from jeremymcs/fix/5024-prevent-self-merge
e1fd1e3a 2026-04-26 15:08:07 -0500 Merge pull request #5040 from jeremymcs/fix/5033-artifact-guard-external-gsd
8b4f7ba8 2026-04-26 15:05:56 -0500 Merge pull request #5011 from mastertyko/codex/fix-4652-infra-git-errors
01d9871f 2026-04-26 15:05:12 -0500 Merge pull request #4968 from mastertyko/codex/fix-4770-dangling-xml-params
49723ef0 2026-04-26 15:04:33 -0500 Merge pull request #4970 from imxv/feat/mcp-client-global-config
13426f8c 2026-04-26 15:01:14 -0500 fix(gsd): normalize self-merge ref guard
a5770ac9 2026-04-26 14:58:01 -0500 fix(gsd): guard milestone message scan
de50f8ac 2026-04-26 14:56:20 -0500 Merge pull request #5038 from mastertyko/codex/fix-5037-slice-parallel-headless
4edc3d4d 2026-04-26 14:37:52 -0500 fix(gsd): refuse self-merge when integration branch == milestone branch (#5024)
2ddcbdbc 2026-04-26 14:37:42 -0500 fix(gsd): bind milestone-tagged commits when .gsd/ is gitignored (#5033)
41edad04 2026-04-26 14:10:15 -0500 Merge pull request #5007 from jeremymcs/feat/min-request-interval-ms
77a76eb6 2026-04-26 22:34:53 +0400 refactor(gsd): migrate remaining files to getHomeDir() + harden forensics redaction
96a29b5d 2026-04-26 13:34:43 -0500 test: isolate auto-loop fixture paths
dc384642 2026-04-26 20:24:31 +0200 fix(gsd): run slice workers through headless auto
8bc82005 2026-04-26 21:26:15 +0400 fix(gsd): resolve home directory correctly on Windows (#5015)
957f129c 2026-04-26 12:02:23 -0500 test: tighten init prefs routing assertions
ce3b287e 2026-04-26 11:52:15 -0500 test(gsd): harden prefs wizard assertions
1b5e03f2 2026-04-26 11:42:07 -0500 test(gsd): cover min request interval prefs wizard
0515e2a0 2026-04-26 11:10:32 -0500 Merge pull request #4748 from jeremymcs/fix/4740-web-terminal-create-errors
cd488f1d 2026-04-26 11:07:58 -0500 Merge pull request #4990 from jeremymcs/ci/dev-publish-reachability-verify
83559893 2026-04-26 11:07:08 -0500 Merge pull request #5021 from jeremymcs/fix/5019-cache-busters
4dd01472 2026-04-26 11:06:37 -0500 Merge pull request #5030 from jeremymcs/perf/5027-compaction-cache-breakpoint
a400838a 2026-04-26 11:05:57 -0500 Merge pull request #5026 from jeremymcs/feat/5023-token-telemetry
4280909f 2026-04-26 11:05:23 -0500 Merge pull request #5032 from jeremymcs/chore/5031-mcp-alias-telemetry
8ebb13ee 2026-04-26 11:04:46 -0500 Merge pull request #5029 from jeremymcs/perf/5022-startup-optimization
25f7eb55 2026-04-26 10:53:09 -0500 Merge pull request #4753 from jeremymcs/test/4737-web-vscode-coverage
0d7f1db5 2026-04-26 10:49:21 -0500 fix(startup): address PR review feedback
df1c33c8 2026-04-26 10:39:10 -0500 test(pi-ai): cover anthropic cache breakpoint edge cases
057d2f96 2026-04-26 10:32:15 -0500 Address PR feedback for startup optimization
7425c5f8 2026-04-26 10:25:23 -0500 test(pi-ai): cover cache breakpoint edge cases
a78118e1 2026-04-26 10:21:11 -0500 fix startup review follow-ups
d7b0204a 2026-04-26 10:18:14 -0500 chore(mcp-server): instrument 11 gsd_* alias tools with usage telemetry (#5031)
e2971796 2026-04-26 10:09:49 -0500 perf(pi-ai): cache breakpoint after compaction summary boundary (#5027)
61c12669 2026-04-26 09:43:59 -0500 chore: remove copyright headers from startup changes
3deceae7 2026-04-26 09:40:13 -0500 perf(startup): reduce GSD launch overhead
4e30afb6 2026-04-26 09:14:28 -0500 docs: document token telemetry
b4d4725a 2026-04-26 09:07:36 -0500 feat(pi-coding-agent): opt-in per-call token telemetry (#5023)
1b88e5ae 2026-04-26 08:39:43 -0500 fix(pi-coding-agent,gsd): preserve Anthropic prompt cache (#5019)
1a43b86e 2026-04-26 07:41:53 -0500 Merge pull request #5014 from mastertyko/codex/fix-internal-error-classifier
e9e7da02 2026-04-26 07:39:31 -0500 Merge pull request #4269 from jeremymcs/fix/4258-compaction-phases
75d9e96e 2026-04-26 10:58:19 +0200 fix(gsd): classify stream internal errors as transient
a0bb0589 2026-04-26 06:13:27 +0200 fix(gsd): preserve infrastructure git add failures
f5746dab 2026-04-25 22:25:38 -0500 docs(gsd): clarify min request interval normalization
73bc4d2f 2026-04-25 22:13:37 -0500 fix(auto): stamp request interval at dispatch
c206e9fb 2026-04-25 22:01:04 -0500 Merge pull request #4952 from gsd-build/fix/4950-shutdown-gate
eca600ff 2026-04-25 21:59:14 -0500 Merge pull request #5006 from mastertyko/codex/fix-image-paste-submit
50ced577 2026-04-25 21:56:06 -0500 test(gsd): fix min request interval preference merge assertion
24c25092 2026-04-25 21:40:53 -0500 fix(web): guard shutdown gate process handlers

$ git tag --sort=-creatordate | head -30
v2.78.1
v2.78.0
v2.77.0
v2.76.0
v2.75.0
v2.74.0
v2.73.1
v2.72.0
v2.70.1
v2.70.0
v2.69.0
v2.68.1
v2.68.0
v2.67.0
v2.66.1
v2.64.0
v2.63.0
v2.62.1
v2.62.0
v2.59.1
v2.58.0
v2.56.0
v2.55.0
v2.54.0
v2.53.0
v2.51.0
v2.50.0
v2.46.1
v2.46.0
v2.45.0

$ git log --tags --pretty=format:"%h %ai %d %s" | head -30
43d1bfa9 2026-04-25 23:25:44 +0000  (tag: v2.78.1) release: v2.78.1
852826ce 2026-04-25 18:00:07 -0500  Merge pull request #5001 from jeremymcs/fix/4997-followup-windows-native-detection
20cf27f4 2026-04-25 17:46:00 -0500  fix(claude-code-cli): catch-all candidate iteration + auth-status fallback
aeeb2ca0 2026-04-25 17:25:47 -0500  Merge pull request #4999 from jeremymcs/fix/4997-2-78-0-removed-claude-code-subscription
3d175972 2026-04-25 17:15:40 -0500  docs(claude-code-cli): document readiness helpers
69d7c4ca 2026-04-25 17:02:22 -0500  fix(claude-code-cli): restore Claude subscription detection on Windows
20f86fe1 2026-04-25 15:26:46 -0500  Merge pull request #4994 from jeremymcs/docs/v2.78-readme
fdbff602 2026-04-25 15:15:02 -0500  docs: refresh commands and model-routing guides for 2.78
36e5e686 2026-04-25 15:14:51 -0500  docs(readme): update for v2.78 release
8db73c43 2026-04-25 20:04:28 +0000  (tag: v2.78.0) release: v2.78.0
cfd69e71 2026-04-25 14:04:08 -0500  Merge pull request #4768 from Solvely-Colin/Solvely/fix-4699-complete-milestone-self-diff
3ac29e5e 2026-04-25 13:58:04 -0500  Merge pull request #4988 from jeremymcs/fix/empty-turn-cc-cli-tool-block-shape
6dc5b842 2026-04-25 13:47:39 -0500  test(gsd): canonicalize server tool use fixture
a9ac36a8 2026-04-25 13:37:03 -0500  fix(gsd): match canonical tool-block types in empty-turn recovery
1594b263 2026-04-25 12:13:36 -0500  Merge pull request #4981 from jeremymcs/fix/git-process-safety-audit
a091aad0 2026-04-25 11:58:01 -0500  fix(test): use real temp basePath in dispatch-rule depth-mark test
2f718266 2026-04-25 11:56:32 -0500  fix(gsd): harden git process recovery
e0c1416e 2026-04-25 11:41:40 -0500  Merge upstream/main and consolidate isDeterministicPolicyError
debc4f9d 2026-04-25 11:33:31 -0500  fix(git): clarify TOCTOU ancestry guard and throttle slice persist
528496f7 2026-04-25 10:59:31 -0500  Merge pull request #4953 from gsd-build/fix/4950-quality-gates-cleanup
3724983c 2026-04-25 10:56:04 -0500  Merge pull request #4954 from jeremymcs/fix/4950-uok-gate-runner
ee655af4 2026-04-25 10:55:34 -0500  Merge pull request #4969 from mastertyko/codex/fix-4927-gpt55-xhigh-capability
fb6374a5 2026-04-25 10:55:12 -0500  Merge pull request #4955 from jeremymcs/fix/4950-bootstrap-write-gate
3c141ec5 2026-04-25 10:54:52 -0500  Merge pull request #4956 from jeremymcs/claude/analyze-write-gates-jZ5LH
b0879622 2026-04-25 10:54:29 -0500  Merge pull request #4268 from jeremymcs/fix/4259-pre-exec-notification
8c657e2c 2026-04-25 10:52:04 -0500  Merge pull request #4975 from jeremymcs/fix/auto-discuss-milestone-deadlock
71809253 2026-04-25 10:51:40 -0500  Merge pull request #4978 from jeremymcs/fix/4974-state-machine-edge-cases
42fd64f6 2026-04-25 10:51:17 -0500  fix(git): harden stash and slice recovery safety
d5082930 2026-04-25 11:27:57 -0400  chore: add npm run verify:pr to mirror CI build job locally (#4979)
5f61c499 2026-04-25 10:26:44 -0500  fix(git): repair integration regressions in safety audit
```

### gsd-2 README / docs / source

- README.md:1-24, 30-77, 200-220, 248-303, 313-337, 391-440, 448-488, 493-513, 531-560, 568-621, 692-746, 842.
- CHANGELOG.md:1-45, 405-430, 520-555, 730-785, 2158-2167, 3018-3032.
- CONTRIBUTING.md:1-140.
- .github/PULL_REQUEST_TEMPLATE.md:1-65.
- package.json:1-158.
- .github/workflows/dev-publish.yml:1-158.
- .github/workflows/next-publish.yml:1-150.
- .github/workflows/prod-release.yml:1-176.
- .github/workflows/build-native.yml:120-190.
- .github/workflows/pipeline.yml:1-56.
- docs/dev/ci-cd-pipeline.md:1-196.
- docs/user-docs/commands.md:88-142, 270-399.
- docs/user-docs/auto-mode.md:1-100, 170-190, 250-265.
- docs/user-docs/git-strategy.md:1-45, 150-180.
- docs/user-docs/working-in-teams.md:1-110.
- docs/user-docs/parallel-orchestration.md:1-90, 120-135, 245-258.
- src/resources/extensions/gsd/paths.ts:1-220.
- src/resources/extensions/gsd/md-importer.ts:115-170, 290-360, 431-680.
- src/resources/extensions/gsd/gsd-db.ts:1-130, 300-430, 720-930, 1020-1075.
- src/resources/extensions/gsd/db-writer.ts:125-180, 285-360, 619-715.
- src/resources/extensions/gsd/workflow-templates/registry.json:1-250.
- src/resources/extensions/gsd/workflow-templates/release.md:1-117.
- src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:1-117.
- src/update-check.ts:1-255.
- packages/mcp-server/src/alias-telemetry.ts:1-30.
- packages/mcp-server/src/workflow-tools.ts:574-585, 1335-1715.
- src/resources/extensions/google-search/extension-manifest.json:1-13 and src/resources/extensions/google-search/index.ts:14-19.
- src/resources/extensions/gsd/commands-config.ts:59-68.
- src/resources/extensions/gsd/preferences-validation.ts:960-1020, 1138-1162.
- src/resources/extensions/gsd/bootstrap/system-context.ts:82-96.
- packages/pi-coding-agent/src/core/extensions/loader.ts:1051-1065.
- packages/pi-coding-agent/src/core/skills.ts:349-355.
- packages/pi-coding-agent/src/migrations.ts:199-267.
- packages/pi-coding-agent/src/core/sdk.ts:465-505.
- native/scripts/sync-platform-versions.cjs:1-52.
- scripts/bump-version.mjs:1-77.
- scripts/update-changelog.mjs:78-136.
- scripts/generate-changelog.mjs:137-260.
- scripts/version-stamp.mjs:1-23.

## (ii) Calibrated findings

### Q1: Release cadence

**Finding 1.1 — visible commit count and lower-bound cadence (confidence: high).** The clone is shallow and appears to truncate the six-month history window. The visible six-month command returned `2216` commits; the first visible in-window commit is `2026-03-19 17:26:31 -0600`, and the latest is `2026-04-27 09:50:47 -0500`. Over that visible 38.642-day span, the visible-history density is `401.430 commits/week`. Spread across a nominal 183-day six-month window, `2216` commits gives a lower bound of `84.765 commits/week`; the true six-month count may be higher because the clone is shallow.

**Finding 1.2 — visible tags in the six-month window (confidence: high).** The visible tag list contains 34 tags dated `2026-03-20` through `2026-04-25`. All visible tags are within the six-month window; because the repository is shallow, tag count before `2026-03-20` in the six-month window cannot be ruled out from this clone alone.

**Finding 1.3 — gaps between visible tags (confidence: high for visible tags only).** Consecutive visible tag gaps, in weeks:

```text
v2.36.0 -> v2.39.0 gap_weeks=0.109
v2.39.0 -> v2.40.0 gap_weeks=0.013
v2.40.0 -> v2.43.0 gap_weeks=0.410
v2.43.0 -> v2.45.0 gap_weeks=0.212
v2.45.0 -> v2.46.0 gap_weeks=0.055
v2.46.0 -> v2.46.1 gap_weeks=0.008
v2.46.1 -> v2.50.0 gap_weeks=0.074
v2.50.0 -> v2.51.0 gap_weeks=0.061
v2.51.0 -> v2.53.0 gap_weeks=0.065
v2.53.0 -> v2.54.0 gap_weeks=0.072
v2.54.0 -> v2.55.0 gap_weeks=0.035
v2.55.0 -> v2.56.0 gap_weeks=0.004
v2.56.0 -> v2.58.0 gap_weeks=0.028
v2.58.0 -> v2.59.1 gap_weeks=0.904
v2.59.1 -> v2.62.0 gap_weeks=0.209
v2.62.0 -> v2.62.1 gap_weeks=0.026
v2.62.1 -> v2.63.0 gap_weeks=0.013
v2.63.0 -> v2.64.0 gap_weeks=0.133
v2.64.0 -> v2.66.1 gap_weeks=0.303
v2.66.1 -> v2.67.0 gap_weeks=0.172
v2.67.0 -> v2.68.0 gap_weeks=0.166
v2.68.0 -> v2.68.1 gap_weeks=0.012
v2.68.1 -> v2.69.0 gap_weeks=0.024
v2.69.0 -> v2.70.0 gap_weeks=0.019
v2.70.0 -> v2.70.1 gap_weeks=0.031
v2.70.1 -> v2.72.0 gap_weeks=0.291
v2.72.0 -> v2.73.1 gap_weeks=0.070
v2.73.1 -> v2.74.0 gap_weeks=0.137
v2.74.0 -> v2.75.0 gap_weeks=0.184
v2.75.0 -> v2.76.0 gap_weeks=0.515
v2.76.0 -> v2.77.0 gap_weeks=0.220
v2.77.0 -> v2.78.0 gap_weeks=0.677
v2.78.0 -> v2.78.1 gap_weeks=0.020
```

Summary for visible tags: `34` tags since `2025-10-28`; first visible tag `2026-03-20 01:26:46 +0000`; last visible tag `2026-04-25 23:25:44 +0000`; average gap across consecutive visible tags `0.160` weeks.

### Q2: Breaking-change posture (stated and observed)

**Finding 2.1 — stated contributor policy requires explicit signposting, not a fully numeric deprecation SLA (confidence: high).** CONTRIBUTING asks contributors to explicitly say when a PR changes public API, CLI behavior, config format, or file structure, and says breaking changes need extra scrutiny and may need migration guidance (`CONTRIBUTING.md:120-122`). The PR template also has an explicit "Breaking changes" checkbox with "No breaking changes" / "Yes - described above" options (`.github/PULL_REQUEST_TEMPLATE.md:51-54`). I did not observe a fixed release-count or time-based deprecation policy in the contributor docs I read.

**Finding 2.2 — release-note format includes Deprecated/Removed categories (confidence: high).** The root changelog says it is based on Keep a Changelog (`CHANGELOG.md:1-5`) and currently has an `[Unreleased]` `### Deprecated` entry for 11 MCP alias tools, including migration guidance to canonical names and a removal condition based on telemetry (`CHANGELOG.md:7-10`). Recent releases also use ordinary Added/Fixed/Changed headings, e.g. v2.78.0 (`CHANGELOG.md:18-45`), and older entries include `### Removed`, e.g. branch/isolation functions and preferences in v2.14.0-era history (`CHANGELOG.md:3022-3027`).

**Finding 2.3 — bundled API-breaking workflow states a staged deprecate-then-remove process (confidence: high).** The `api-breaking-change` workflow template defines phases `survey`, `migrate`, `deprecate`, and `release` (`src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:18-23`). It asks for a `SURVEY.md` with old/new signatures, caller lists, migration difficulty, and "deprecate in release X, remove in release Y" timeline proposal (`src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:46-50`). It also says to add `@deprecated` annotations, runtime warnings where feasible, changelog `### Deprecated`, README/API-doc deprecation timeline, and major-version removal with prominent changelog documentation (`src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:79-96`, `src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:98-112`).

**Finding 2.4 — release tooling recognizes semver-major triggers, but observed tags stay in major version 2 in the visible window (confidence: high).** The release workflow template says to propose a `major` bump if a commit has a `BREAKING CHANGE:` footer or `!` suffix (`src/resources/extensions/gsd/workflow-templates/release.md:36-40`). The changelog generator also sets `hasBreaking` when a subject includes `BREAKING CHANGE` or `!:` and maps that to `major` (`scripts/generate-changelog.mjs:194-204`, `scripts/generate-changelog.mjs:230-260`). The visible tags are all `v2.x.y`, from `v2.36.0` through `v2.78.1`, per the tag output above.

**Finding 2.5 — in-code deprecation markers exist, but removal metadata varies by surface (confidence: high).** A filtered non-test/non-vendor search over `src` and `packages` returned deprecation-related markers in source, manifests, and workflow templates. Concrete examples:

- MCP alias telemetry says 11 alias `gsd_*` tools are in "Step 1 of a two-step deprecation"; it emits one JSONL record per invocation and says aliases can be removed after a long-enough zero-entry window (`packages/mcp-server/src/alias-telemetry.ts:1-9`, `packages/mcp-server/src/alias-telemetry.ts:11-30`).
- The MCP server registers alias tools such as `gsd_save_decision`, `gsd_update_requirement`, `gsd_save_requirement`, `gsd_task_plan`, `gsd_complete_slice`, `gsd_milestone_complete`, `gsd_milestone_validate`, `gsd_roadmap_reassess`, and `gsd_complete_task`, each logging alias usage before delegating to the canonical implementation (`packages/mcp-server/src/workflow-tools.ts:574-585`, `packages/mcp-server/src/workflow-tools.ts:1340-1450`, `packages/mcp-server/src/workflow-tools.ts:1503-1715`).
- The Google Search bundled extension is now a manifest-level "deprecated stub" with `deprecated: true` and no provided tools (`src/resources/extensions/google-search/extension-manifest.json:1-13`); its source comment says the notice is intentionally suppressed until the extracted package ships (`src/resources/extensions/google-search/index.ts:14-19`).
- `/gsd config` has a runtime warning that it is deprecated and "will be removed", but I did not see a version/date target in that warning (`src/resources/extensions/gsd/commands-config.ts:59-68`).
- `agent-instructions.md` has a runtime warning that the file is no longer loaded and should be migrated to `AGENTS.md` or `CLAUDE.md` (`src/resources/extensions/gsd/bootstrap/system-context.ts:82-96`), matching the README note (`README.md:621`).
- Preference validation warns that `git.commit_docs` and `git.merge_to_main` are deprecated and should be removed; these warnings do not include a removal version (`src/resources/extensions/gsd/preferences-validation.ts:982-1009`).
- Pi-facing code has `@deprecated` markers for `discoverAndLoadExtensions()` and `LoadSkillsOptions.agentDir` without an explicit removal release in the annotation (`packages/pi-coding-agent/src/core/extensions/loader.ts:1051-1065`, `packages/pi-coding-agent/src/core/skills.ts:349-355`).

**Finding 2.6 — observed practice includes both staged deprecation and removal-style changes without visible pre-deprecation evidence in the shallow history (confidence: medium).** The current unreleased MCP alias entry follows a staged telemetry/deprecation pattern (`CHANGELOG.md:7-10`; `packages/mcp-server/src/alias-telemetry.ts:1-9`). The `agent-instructions.md` change is signposted as "deprecate" in v2.36.0 (`CHANGELOG.md:2158-2167`) and has a source warning (`src/resources/extensions/gsd/bootstrap/system-context.ts:82-96`). By contrast, the visible changelog records `remove Anthropic OAuth flow for TOS compliance` under v2.70.0 `Fixed` (`CHANGELOG.md:769-778`), and the runtime source says OAuth support was removed in v2.74.0 and self-heals stale credentials (`packages/pi-coding-agent/src/core/sdk.ts:476-503`). I did not see, in this slice's read, a prior deprecation window for that OAuth removal. This claim is medium-confidence because the clone is shallow and I did not inspect GitHub releases outside the local clone.

**Finding 2.7 — visible commit/release messages do not consistently use explicit "breaking" wording for removals (confidence: medium).** A visible-history search for deprecation/removal language found commits such as `fix(pi-ai): remove Anthropic OAuth flow for TOS compliance`, `refactor(gsd): remove /gsd map-codebase command`, and `feat: deprecate agent-instructions.md in favor of AGENTS.md / CLAUDE.md`; I did not find a `BREAKING CHANGE` commit in the visible search results. The release template and changelog generator can detect breaking commits (`src/resources/extensions/gsd/workflow-templates/release.md:36-40`; `scripts/generate-changelog.mjs:194-204`), but recent observed removals appear signposted primarily as `fix`, `refactor`, or `Changed/Fixed` entries in the visible local artifacts (`CHANGELOG.md:554`, `CHANGELOG.md:777`).

### Q3: Multi-milestone / release-related artifacts

**Finding 3.1 — gsd-2 has a named `.gsd` artifact hierarchy for project, milestone, slice, and task records (confidence: high).** README lists root artifacts such as `PROJECT.md`, `DECISIONS.md`, `KNOWLEDGE.md`, `RUNTIME.md`, `STATE.md`; milestone artifacts `M001-ROADMAP.md`, `M001-CONTEXT.md`, `M001-RESEARCH.md`; slice/task artifacts `S01-PLAN.md`, `T01-PLAN.md`, `T01-SUMMARY.md`, and `S01-UAT.md` (`README.md:493-512`). Path builders encode `M001-ROADMAP.md`, `S01-PLAN.md`, and `T03-PLAN.md` naming (`src/resources/extensions/gsd/paths.ts:1-9`, `src/resources/extensions/gsd/paths.ts:141-164`).

**Finding 3.2 — the importer recognizes milestone/slice/task artifact classes by suffix (confidence: high).** The hierarchy artifact walker looks for milestone suffixes `ROADMAP`, `CONTEXT`, `RESEARCH`, `ASSESSMENT`; slice suffixes `PLAN`, `SUMMARY`, `RESEARCH`, `CONTEXT`, `ASSESSMENT`, `UAT`; and task suffixes `PLAN`, `SUMMARY`, `CONTINUE`, `CONTEXT`, `RESEARCH` (`src/resources/extensions/gsd/md-importer.ts:306-315`). It imports matching files into an `artifacts` record with `path`, `artifact_type`, `milestone_id`, `slice_id`, `task_id`, and `full_content` (`src/resources/extensions/gsd/md-importer.ts:431-449`).

**Finding 3.3 — requirements artifacts have a concrete status schema and regeneration path (confidence: high).** `REQUIREMENTS.md` parsing recognizes `## Active`, `## Validated`, `## Deferred`, and `## Out of Scope` sections and `### RXXX` requirement blocks with bullet fields (`src/resources/extensions/gsd/md-importer.ts:117-170`). The DB writer regenerates `REQUIREMENTS.md` grouped by status and emits fields including class, status, description, why, source, primary owner, supporting slices, validation, notes, plus traceability (`src/resources/extensions/gsd/db-writer.ts:125-180`). Requirement save/update functions write through DB and regenerate `.gsd/REQUIREMENTS.md` (`src/resources/extensions/gsd/db-writer.ts:285-360`, `src/resources/extensions/gsd/db-writer.ts:619-715`).

**Finding 3.4 — gsd-2 has database-backed milestone/slice/task schema with planning, verification, dependency, and replan fields (confidence: high).** The engine DB schema defines `milestones` with fields including `status`, `depends_on`, `vision`, `success_criteria`, `verification_*`, `definition_of_done`, `requirement_coverage`, and `boundary_map_markdown` (`src/resources/extensions/gsd/gsd-db.ts:338-357`). It defines `slices` with fields including `status`, `risk`, `depends`, `demo`, summary/UAT markdown, `goal`, `success_criteria`, `proof_level`, `integration_closure`, `observability_impact`, `sequence`, and sketch fields (`src/resources/extensions/gsd/gsd-db.ts:360-384`). It defines `tasks` with status, summary, verification, blocker/escalation, key files/decisions, planning files, verify command, inputs/expected output, and sequence fields (`src/resources/extensions/gsd/gsd-db.ts:387-421`).

**Finding 3.5 — version-aware migration exists in source (confidence: high).** The DB file uses `schema_version` rows and conditional migration blocks (`src/resources/extensions/gsd/gsd-db.ts:720-747`, `src/resources/extensions/gsd/gsd-db.ts:749-821`, `src/resources/extensions/gsd/gsd-db.ts:824-930`, `src/resources/extensions/gsd/gsd-db.ts:1065-1075`). The markdown migration path walks `.gsd/milestones`, parses roadmaps/plans, infers milestone status from summary/parked/checkbox state, and inserts milestones, slices, and tasks in order (`src/resources/extensions/gsd/md-importer.ts:494-590`, `src/resources/extensions/gsd/md-importer.ts:592-680`).

**Finding 3.6 — release-related artifacts and scripts are explicit (confidence: high).** The root has `CHANGELOG.md` with Keep a Changelog format (`CHANGELOG.md:1-5`), `package.json` version `2.78.1` and release scripts `release:changelog`, `release:bump`, and `release:update-changelog` (`package.json:1-4`, `package.json:94-100`). `scripts/bump-version.mjs` updates root and workspace package versions, syncs platform packages, and regenerates package-locks (`scripts/bump-version.mjs:1-77`). `scripts/update-changelog.mjs` inserts a changelog entry after `[Unreleased]` and updates comparison links (`scripts/update-changelog.mjs:78-136`). `scripts/generate-changelog.mjs` parses commits since the latest stable tag and outputs bump/changelog/release-notes data (`scripts/generate-changelog.mjs:137-260`).

**Finding 3.7 — bundled workflow templates include release and API-breaking-change artifact directories (confidence: high).** The workflow registry includes `release` with phases `prepare`, `bump`, `publish`, `announce` and artifact directory `.gsd/workflows/releases/` (`src/resources/extensions/gsd/workflow-templates/registry.json:213-223`). It includes `api-breaking-change` with phases `survey`, `migrate`, `deprecate`, `release` and artifact directory `.gsd/workflows/api-breaks/` (`src/resources/extensions/gsd/workflow-templates/registry.json:224-233`). The release template itself writes `PREPARE.md` and `RELEASE.md` into the release artifact directory (`src/resources/extensions/gsd/workflow-templates/release.md:42-48`, `src/resources/extensions/gsd/workflow-templates/release.md:113-117`).

### Q4: Prod / dev distinctions

**Finding 4.1 — release channels are represented with npm dist-tags and GitHub workflows (confidence: high).** The CI/CD doc describes `@dev`, `@next`, and `@latest` channels and their intended audiences (`docs/dev/ci-cd-pipeline.md:188-196`). Source workflows implement manual `Dev Publish` and `Next Publish` jobs that stamp versions using `VERSION_CHANNEL=dev` or `VERSION_CHANNEL=next` and publish with npm `--tag dev` / `--tag next` (`.github/workflows/dev-publish.yml:1-8`, `.github/workflows/dev-publish.yml:75-100`; `.github/workflows/next-publish.yml:1-5`, `.github/workflows/next-publish.yml:74-99`). `Prod Release` is manual, uses GitHub environment `prod`, bumps versions, updates changelog, tags, publishes npm `@latest`, creates a GitHub release, posts to Discord if configured, builds/pushes Docker images, and opens a back-merge PR if `next` is behind (`.github/workflows/prod-release.yml:1-5`, `.github/workflows/prod-release.yml:20-29`, `.github/workflows/prod-release.yml:57-125`, `.github/workflows/prod-release.yml:127-176`).

**Finding 4.2 — dev/pre-release versions are stamped with channel and short SHA (confidence: high).** `scripts/version-stamp.mjs` reads `VERSION_CHANNEL` or defaults to `dev`, then rewrites `package.json` to `${pkg.version}-${channel}.${shortSha}` and regenerates `package-lock.json` (`scripts/version-stamp.mjs:1-23`).

**Finding 4.3 — platform binary publishing distinguishes prerelease and stable tags (confidence: high).** Native build workflow detects `-next.` in the package version and publishes platform packages with `--tag next`; otherwise it publishes as stable/latest by default (`.github/workflows/build-native.yml:126-141`, `.github/workflows/build-native.yml:143-190`). Platform package versions are synced from root package version across five platform packages, while root optional dependencies intentionally keep range specifiers (`native/scripts/sync-platform-versions.cjs:1-52`).

**Finding 4.4 — runtime/user modes distinguish solo/team, not exactly prod/dev (confidence: high).** Preferences define workflow modes `solo` and `team`; solo defaults include `auto_push: true`, `push_branches: false`, `pre_merge_check: "auto"`, `merge_strategy: "squash"`, `isolation: "none"`, `unique_milestone_ids: false`, while team defaults include `auto_push: false`, `push_branches: true`, `pre_merge_check: true`, `merge_strategy: "squash"`, `isolation: "none"`, `unique_milestone_ids: true` (`src/resources/extensions/gsd/preferences-types.ts:64-90`). Working-in-teams docs describe `mode: team` as enabling unique IDs, branch pushing, and pre-merge checks, and separate shared planning artifacts from local runtime files (`docs/user-docs/working-in-teams.md:7-21`, `docs/user-docs/working-in-teams.md:23-49`).

**Finding 4.5 — experimental features have explicit opt-in and looser deprecation guarantees (confidence: high).** Experimental preferences are described as disabled by default, explicitly enabled, and allowed to change or be removed without a deprecation cycle while experimental (`src/resources/extensions/gsd/preferences-types.ts:277-287`). Validation currently recognizes `experimental.rtk` as a boolean and warns on unknown experimental keys (`src/resources/extensions/gsd/preferences-validation.ts:1138-1162`).

**Finding 4.6 — developer/test commands are distinct from publish/release commands (confidence: high).** `package.json` includes dev/test commands such as `dev`, `gsd`, `gsd:web`, `test:unit`, `test:integration`, `test:live`, `test:coverage`, and release/publish commands such as `pipeline:version-stamp`, `release:*`, and `prepublishOnly` (`package.json:47-101`). The user-facing docs expose `gsd headless` for CI/cron/scripts and `gsd headless query` for machine-readable state without spawning an LLM session (`README.md:417-440`; `docs/user-docs/commands.md:279-360`).

### Q5: Multi-milestone / release-workflow / drift-handling feature inventory

Concrete feature inventory, without judging what time horizon these features support:

1. **Milestone/slice/task hierarchy.** README defines `Milestone -> Slice -> Task` with sizes and loop phases (`README.md:281-303`). Source paths build milestone, slice, and task file names (`src/resources/extensions/gsd/paths.ts:141-164`).

2. **Roadmap reassessment phase.** README describes reassessment after slice completion and says slices may be reordered, added, or removed before continuing (`README.md:333-335`). Auto-mode docs include `Reassess` in the loop (`docs/user-docs/auto-mode.md:11-23`).

3. **Milestone validation gate.** README says validation compares roadmap success criteria against actual results before sealing a milestone (`README.md:337`). Auto-mode docs repeat this as the `Validate Milestone` phase (`docs/user-docs/auto-mode.md:19-23`).

4. **Requirement contract artifact.** `REQUIREMENTS.md` has Active/Validated/Deferred/Out-of-Scope sections and requirement fields parsed into DB objects (`src/resources/extensions/gsd/md-importer.ts:117-170`), then regenerated with traceability and coverage summary (`src/resources/extensions/gsd/db-writer.ts:125-180`).

5. **Database schema for planning/progress/drift fields.** Milestone schema includes success criteria, verification fields, definition of done, requirement coverage, and boundary-map markdown (`src/resources/extensions/gsd/gsd-db.ts:338-357`). Slice/task schema includes dependencies, risk/demo, success/proof fields, sequence, replan, blockers, escalation, and verification fields (`src/resources/extensions/gsd/gsd-db.ts:360-421`, `src/resources/extensions/gsd/gsd-db.ts:860-930`).

6. **Markdown-to-DB migration.** The importer parses old project docs, recognizes hierarchy suffixes, infers statuses, and populates milestone/slice/task DB tables (`src/resources/extensions/gsd/md-importer.ts:306-360`, `src/resources/extensions/gsd/md-importer.ts:494-680`). README says migration maps phases to slices, plans to tasks, milestones to milestones, preserves completion state, consolidates research, previews before writing, and handles format variations (`README.md:254-277`).

7. **Git isolation and milestone merge behavior.** README describes milestone branches/worktrees, sequential slice commits, squash merge at milestone completion, and commit messages generated from task summaries (`README.md:321`, `README.md:514-531`). Git strategy docs enumerate `worktree`, `branch`, and `none` isolation modes plus automatic PR preferences (`docs/user-docs/git-strategy.md:1-31`, `docs/user-docs/git-strategy.md:150-180`).

8. **Parallel milestone orchestration.** Parallel docs describe separate worker processes, worktrees, branches, context windows, metrics, crash recovery, file-based IPC, dependency/file-overlap eligibility, budget tracking, and conflict-aware merge (`docs/user-docs/parallel-orchestration.md:1-25`, `docs/user-docs/parallel-orchestration.md:68-88`, `docs/user-docs/parallel-orchestration.md:120-135`, `docs/user-docs/parallel-orchestration.md:245-258`).

9. **Team workflow artifact sharing.** Team docs specify shared planning artifacts (`.gsd/PREFERENCES.md`, `PROJECT.md`, `REQUIREMENTS.md`, `DECISIONS.md`, `milestones/`) versus local runtime files, and describe a two-PR plan/code workflow (`docs/user-docs/working-in-teams.md:23-49`, `docs/user-docs/working-in-teams.md:85-103`).

10. **Headless mode for automation.** README and commands docs describe headless CI/script mode, `new-milestone --context ... --auto`, `next`, `query`, structured exit codes, timeout/restart flags, and JSON state snapshot schema (`README.md:417-440`; `docs/user-docs/commands.md:279-360`).

11. **Release workflow template.** The bundled release workflow has phases `prepare`, `bump`, `publish`, and `announce`; it proposes semver bump, writes `PREPARE.md`, updates changelog, commits/tags, pushes, verifies, creates a GitHub Release, and writes `RELEASE.md` (`src/resources/extensions/gsd/workflow-templates/release.md:1-117`).

12. **API-breaking-change workflow template.** The bundled API-breaking-change workflow has phases `survey`, `migrate`, `deprecate`, `release`; it asks for caller maps, migration pattern, timeline proposal, annotations/warnings, changelog/docs updates, and a final survey update (`src/resources/extensions/gsd/workflow-templates/api-breaking-change.md:1-117`).

13. **Changelog generation and version bump scripts.** `scripts/generate-changelog.mjs` reads conventional commits since the last stable tag and computes bump/changelog/release-notes output (`scripts/generate-changelog.mjs:137-260`). `scripts/bump-version.mjs` updates root/workspace/platform/package-lock versions (`scripts/bump-version.mjs:1-77`). `scripts/update-changelog.mjs` inserts the entry under `[Unreleased]` and updates comparison links (`scripts/update-changelog.mjs:78-136`).

14. **Dev/next/prod release workflows.** Manual dev and next workflows stamp channel versions and verify installed packages (`.github/workflows/dev-publish.yml:1-8`, `.github/workflows/dev-publish.yml:75-158`; `.github/workflows/next-publish.yml:1-5`, `.github/workflows/next-publish.yml:74-150`). Prod workflow bumps, changelogs, tags, publishes npm, creates GitHub Release, builds Docker image, and opens a back-merge PR when applicable (`.github/workflows/prod-release.yml:57-176`).

15. **In-session update check.** `src/update-check.ts` fetches the latest npm version, caches checks for 24 hours, prints update banners, and can prompt to run `npm install -g gsd-pi@latest` or Bun equivalent (`src/update-check.ts:8-12`, `src/update-check.ts:52-76`, `src/update-check.ts:121-153`, `src/update-check.ts:156-255`).

16. **HTML milestone reports.** README says completed milestones generate self-contained HTML reports with summary, progress tree, slice dependency graph, cost/token charts, timeline, changelog, and knowledge sections; `index.html` shows progression metrics across milestones (`README.md:553-560`). Auto-mode docs also mention all-milestone export (`docs/user-docs/auto-mode.md:177-185`).

17. **Observability/forensics surfaces.** README v2.78 notes worktree telemetry events and a summarizer for orphan breakdowns, merge durations, conflict counts, exit reasons, and unmerged-exit metrics (`README.md:34-38`). It also lists `/gsd forensics`, `/gsd doctor`, `/gsd logs`, and `/gsd export --html` commands (`README.md:466-472`).

## (iii) What I deliberately did NOT read

- I did not read the dispatching project's prior gsd-2 framing artifacts, including `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`, `.planning/audits/archive/`, `.planning/gsd-2-uplift/INITIATIVE.md`, `.planning/gsd-2-uplift/DECISION-SPACE.md`, other slice outputs, prior cross-vendor analysis, or deliberation logs.
- I did not read slice outputs 01-04.
- I did not fetch, unshallow, deepen, or modify the gsd-2 clone.
- I did not inspect GitHub Releases through the network. Observed release practice is based on local git tags, local changelog, local workflows, and local source only.
- I did not evaluate whether the observed features are sufficient for any downstream time horizon, intervention shape, or adoption decision.

## (iv) Open questions surfaced

1. **Cadence precision requires a deeper clone.** The shallow boundary falls inside the requested six-month window, so visible cadence numbers are lower-bound or visible-window figures, not complete six-month history.

2. **Open question — interpretive; defer to synthesis.** Release cadence numbers by themselves require a comparison frame to be meaningful. This slice can report `2216` visible commits, `34` visible tags, and `0.160` average visible tag-gap weeks, but whether that pattern matters for downstream work is synthesis-level.

3. **Breaking-change practice needs release-note and diff sampling beyond this slice.** The source contains a stated staged API-breaking workflow, but visible recent removals are mixed across `Fixed`, `Changed`, `Removed`, and ordinary commit subjects. A follow-up could sample concrete diffs across selected tags (`v2.70.0`, `v2.74.0`, `v2.78.0`) and GitHub release bodies to determine how users would actually encounter breaking changes.

4. **Non-README docs/source divergence: pipeline automation language may be stale.** `docs/dev/ci-cd-pipeline.md` says merged PRs automatically move through Dev -> Test -> Prod (`docs/dev/ci-cd-pipeline.md:3-22`), but current workflow source says dev/prod publishing live in separate manual workflows (`.github/workflows/pipeline.yml:3-6`), and `dev-publish.yml`, `next-publish.yml`, and `prod-release.yml` are all `workflow_dispatch`-triggered (`.github/workflows/dev-publish.yml:8-15`; `.github/workflows/next-publish.yml:7-14`; `.github/workflows/prod-release.yml:7-8`). This is outside README-divergence framing but relevant to release-workflow observation.

5. **Cross-slice watchlist — telemetry/observability appears central, not incidental.** Worktree telemetry, forensics, doctor, logs, HTML reports, event logs, DB gate runs, and audit events appear in README/source (`README.md:34-38`, `README.md:466-472`; `src/resources/extensions/gsd/gsd-db.ts:496-547`). Synthesis should integrate observability as a central gsd-2 surface if other slices confirm it.

6. **Cross-slice watchlist — multi-user/collaboration appears central.** Team mode, shared artifacts, plan/code PR workflow, parallel milestones, per-worker IPC, and branch/worktree isolation are all directly documented (`docs/user-docs/working-in-teams.md:1-103`; `docs/user-docs/parallel-orchestration.md:1-88`). This slice did not evaluate collaboration semantics beyond concrete artifacts.

7. **Cross-slice watchlist — security/trust boundaries appear central enough for another slice to integrate.** Auto-mode tool policy says planning units can write only planning artifacts and cannot dispatch subagents except in `planning-dispatch`; writes outside allowed paths and unsafe bash commands are hard policy errors (`docs/user-docs/auto-mode.md:31-35`). CI includes secret/prompt-injection scanning in docs (`docs/dev/ci-cd-pipeline.md:78-99`). I did not inspect the full policy enforcement path.

8. **Potential direction-shifting evidence: release mechanics and product workflow are tightly interleaved.** Release templates, CI workflows, changelog tooling, GSD-managed milestone artifacts, worktree merge behavior, and in-session update checks are all present. This does not imply an intervention shape; it does mean a second-wave read that treats "release cadence" as separate from artifact/workflow mechanics may need to keep those surfaces linked.

## (v) Flags where README claims diverge from source observations

- No direct README-vs-source divergence observed in this slice's scope.
- Related non-README divergence: the CI/CD developer doc describes an automatic Dev -> Test -> Prod promotion pipeline (`docs/dev/ci-cd-pipeline.md:3-22`), while workflow source currently presents dev/prod publishing as separate manual workflows (`.github/workflows/pipeline.yml:3-6`) and dev/next/prod publish workflows use `workflow_dispatch` triggers (`.github/workflows/dev-publish.yml:8-15`; `.github/workflows/next-publish.yml:7-14`; `.github/workflows/prod-release.yml:7-8`).
