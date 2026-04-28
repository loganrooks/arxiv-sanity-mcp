---
type: capabilities-probe
date: 2026-04-27
agent: codex GPT-5.5 medium (exploration mode)
status: complete
---

# Capabilities probe — gsd-2 production-fitness

## §0. Probe summary

Top-line: gsd-2 visibly supports production/devops work in two separate ways: its own repo has concrete release CI, dev/next/latest publish workflows, semver/changelog scripts, Docker publishing, and rollback docs; its product surface also exposes milestones, headless automation, git/worktree isolation, workflow templates, hooks, MCP tools, telemetry, and team mode for user projects.

Direct release support appears strongest in bundled workflow templates (`release`, `hotfix`, `changelog-gen`) and in gsd-2's own GitHub Actions; direct release support inside the milestone abstraction is weaker: milestones are described as "shippable version" units, but I did not observe a fixed mapping to major/minor/patch/RC.

Pre-release support appears in gsd-2's own `@dev` and `@next` npm dist-tag workflows; I did not observe a user-project RC command, RC tag convention, or staged-rollout primitive beyond composing release templates, CI, hooks, and external pipeline steps.

CI/headless support is visible and structured: `gsd headless` has JSON/JSONL output, resumable sessions, exit codes, query mode, answer injection, event filtering, and a bare mode.

Most surprising finding: release/hotfix are first-class workflow templates, but they are separate from the milestone/slice/task planner rather than a semver-aware release layer on top of milestones.

## §A. Observation findings (source-cited; no judgment)

### §A.1 Versioning + release primitives

- **Package identity and current version:** gsd-2's package is `gsd-pi`, version `2.78.1`, with binaries `gsd`, `gsd-cli`, and `gsd-pi`. **Confidence: high.** (`package.json:1-24`)

- **Build/test/release scripts:** `package.json` exposes build/test scripts plus release-related scripts: `sync-pkg-version`, `sync-platform-versions`, `validate-pack`, `pipeline:version-stamp`, `release:changelog`, `release:bump`, and `release:update-changelog`; `prepublishOnly` runs sync, prepublish check, build, extension typecheck, and package validation. **Confidence: high.** (`package.json:47-101`)

- **Changelog format:** `CHANGELOG.md` states it follows Keep a Changelog and currently has `[Unreleased]`, `[2.78.1] - 2026-04-25`, and `[2.78.0] - 2026-04-25` sections. **Confidence: high.** (`CHANGELOG.md:1-18`)

- **Stable release script behavior:** `scripts/generate-changelog.mjs` finds the last stable tag matching `vX.Y.Z`, skips `-next` and `-dev`, parses conventional commits since that tag, sets bump type to `major` for breaking, `minor` for `feat`, else `patch`, and outputs JSON with `bumpType`, `newVersion`, `changelogEntry`, and `releaseNotes`. **Confidence: high.** (`scripts/generate-changelog.mjs:1-5`, `scripts/generate-changelog.mjs:14-27`, `scripts/generate-changelog.mjs:42-97`, `scripts/generate-changelog.mjs:116-152`)

- **Version bump script behavior:** `scripts/bump-version.mjs` requires an `X.Y.Z` argument, updates root `package.json`, workspace package versions and internal dependency references, syncs native/pkg package versions, and regenerates root and web package locks. **Confidence: high.** (`scripts/bump-version.mjs:1-17`, `scripts/bump-version.mjs:20-77`)

- **Pre-release stamping:** `scripts/version-stamp.mjs` uses `VERSION_CHANNEL` defaulting to `dev`, appends `-<channel>.<shortSha>` to the current package version, writes `package.json`, and regenerates `package-lock.json`. **Confidence: high.** (`scripts/version-stamp.mjs:9-23`)

- **Changelog update script:** `scripts/update-changelog.mjs` inserts a new `## [X.Y.Z] - YYYY-MM-DD` entry after `[Unreleased]` and updates comparison links if present. **Confidence: high.** (`scripts/update-changelog.mjs:1-7`, `scripts/update-changelog.mjs:21-58`)

- **Production release workflow:** `.github/workflows/prod-release.yml` is manually dispatched, uses the `prod` GitHub Environment, generates changelog/version, bumps version, validates package files, updates `CHANGELOG.md`, commits `release: v${RELEASE_VERSION}`, tags `v${RELEASE_VERSION}`, builds, publishes npm `@latest`, pushes commit/tag, creates a GitHub Release, optionally posts Discord, builds/pushes Docker `latest` and version tags, and opens a back-merge PR from `main` to `next` when needed. **Confidence: high.** (`.github/workflows/prod-release.yml:1-23`, `.github/workflows/prod-release.yml:57-90`, `.github/workflows/prod-release.yml:92-126`, `.github/workflows/prod-release.yml:127-176`)

- **Dev/next workflows:** `.github/workflows/dev-publish.yml` manually publishes a stamped `@dev` package from an input ref and verifies by globally installing the published package; `.github/workflows/next-publish.yml` does the same for `@next`. **Confidence: high.** (`.github/workflows/dev-publish.yml:1-18`, `.github/workflows/dev-publish.yml:75-108`, `.github/workflows/dev-publish.yml:110-158`; `.github/workflows/next-publish.yml:1-17`, `.github/workflows/next-publish.yml:74-99`, `.github/workflows/next-publish.yml:101-150`)

- **CI release branch signal:** CI runs on push to `main`, `dev`, `test`, and `hotfix/**`, and PRs to `main`, `dev`, and `test`. **Confidence: high.** (`.github/workflows/ci.yml:1-18`)

- **Shallow clone note:** The source checkout reports `rev-parse --is-shallow-repository = true`; I did not fetch. I only used local file contents plus a local tag/log glance, so deeper cadence/history claims are intentionally avoided. **Confidence: high for local checkout status.** (`probe command output from this run; no file citation available`)

### §A.2 Milestone / slice / task semantics — release-relevant fields

- **Hierarchy:** gsd-2 docs describe `Milestone -> Slice -> Task`; a milestone is a "shippable version (4-10 slices)" in `GSD-WORKFLOW.md`, while GitBook says a milestone can be an MVP, major release, or feature set. **Confidence: high for stated docs.** (`src/resources/GSD-WORKFLOW.md:28-37`; `gitbook/core-concepts/project-structure.md:5-20`)

- **Roadmap fields:** the `Roadmap` type has `title`, `vision`, `successCriteria`, `slices`, and `boundaryMap`; each slice entry has `id`, `title`, `risk`, `depends`, `done`, and `demo`. **Confidence: high for source schema.** (`src/resources/extensions/gsd/types.ts:29-53`)

- **Slice plan fields:** a `SlicePlan` carries `id`, `title`, `goal`, `demo`, `mustHaves`, `tasks`, and `filesLikelyTouched`; task entries carry `id`, `title`, `description`, `done`, `estimate`, optional `files`, and optional `verify`. **Confidence: high for source schema.** (`src/resources/extensions/gsd/types.ts:55-75`, `src/resources/extensions/gsd/types.ts:115-123`)

- **Verification result fields:** verification records include command, exit code, stdout/stderr, duration, discovery source, timestamp, optional runtime errors, and optional audit warnings. **Confidence: high for source schema.** (`src/resources/extensions/gsd/types.ts:77-113`)

- **Summary fields:** task/slice summary frontmatter tracks `provides`, `requires`, `affects`, `key_files`, `key_decisions`, `patterns_established`, `observability_surfaces`, `duration`, `verification_result`, `completed_at`, and `blocker_discovered`. **Confidence: high for source schema.** (`src/resources/extensions/gsd/types.ts:125-148`)

- **Roadmap markdown format:** `M###-ROADMAP.md` includes a milestone title, vision, success criteria, slices with `risk` and `depends`, and a required boundary map showing produces/consumes. **Confidence: high for docs format.** (`src/resources/GSD-WORKFLOW.md:70-128`)

- **Slice/task markdown format:** `S##-PLAN.md` includes goal, demo, must-haves, tasks, and files likely touched; `T##-PLAN.md` includes slice/milestone, goal, truths/artifacts/key links, steps, and context. **Confidence: high for docs format.** (`src/resources/GSD-WORKFLOW.md:129-192`)

- **No observed semver fields in core artifact schemas:** I did not observe `target_version`, `release_date`, `rc`, `channel`, or `semver` fields in the core `Roadmap`, `SlicePlan`, `TaskPlanEntry`, or `GSDState` types. **Confidence: medium-high.** (`src/resources/extensions/gsd/types.ts:29-75`, `src/resources/extensions/gsd/types.ts:115-123`, `src/resources/extensions/gsd/types.ts:238-256`)

### §A.3 Pre-release / RC / staging tooling

- **Own-repo pre-release channels:** gsd-2's own workflows publish stamped versions to npm dist-tags `@dev` and `@next`; the dev workflow defaults to `main`, while next defaults to `next`. **Confidence: high.** (`.github/workflows/dev-publish.yml:4-15`, `.github/workflows/dev-publish.yml:75-100`; `.github/workflows/next-publish.yml:3-13`, `.github/workflows/next-publish.yml:74-99`)

- **Own-repo prod promotion:** production release is manual, environment-gated, publishes npm `@latest`, creates GitHub Release, pushes Docker `latest` and version tags, and can back-merge `main` into `next`. **Confidence: high.** (`.github/workflows/prod-release.yml:1-23`, `.github/workflows/prod-release.yml:95-126`, `.github/workflows/prod-release.yml:145-176`)

- **CI/CD docs:** dev docs describe a Dev -> Test -> Prod promotion model using npm dist-tags, with install commands for `@dev`, `@next`, and `@latest`, plus rollback commands for npm and Docker. **Confidence: high for docs.** (`docs/dev/ci-cd-pipeline.md:3-22`, `docs/dev/ci-cd-pipeline.md:24-58`, `docs/dev/ci-cd-pipeline.md:123-137`)

- **User-project release template:** the bundled `release` workflow template has prepare/bump/publish/announce phases and mentions approval gates, version bump, changelog generation, tag creation, pipeline triggering, and release visibility verification. **Confidence: high.** (`src/resources/extensions/gsd/workflow-templates/release.md:1-23`, `src/resources/extensions/gsd/workflow-templates/release.md:27-117`)

- **No apparent RC-specific primitive:** I did not observe a user-facing `rc` command, RC tag convention, RC artifact schema, or staging-environment config in the release template or core milestone schemas. **Confidence: medium.** (`src/resources/extensions/gsd/workflow-templates/release.md:18-23`, `src/resources/extensions/gsd/types.ts:29-75`)

### §A.4 CI / headless / automation surfaces

- **Headless purpose and exit codes in source:** `src/headless.ts` says `gsd headless` runs `/gsd` subcommands without TUI by spawning RPC mode, auto-responding to UI requests, streaming progress to stderr, and using exit codes `0`, `1`, `10`, and `11`. **Confidence: high.** (`src/headless.ts:1-13`)

- **Headless options:** headless supports timeout, JSON/stream JSON output, model override, context file/stdin/text, auto chaining, verbose output, max restarts, supervised mode, response timeout, answers file, event filters, resume session, and bare mode. **Confidence: high.** (`src/headless.ts:66-84`, `src/headless.ts:147-231`)

- **Headless restart behavior:** `runHeadless` defaults max restarts to 3 and exits success/blocked immediately, otherwise restarts until max restarts unless interrupted. **Confidence: high.** (`src/headless.ts:238-259`)

- **CLI help:** help documents `--json`, `--output-format text|json|stream-json`, `--bare`, `--resume`, `--supervised`, `--answers`, `--events`, commands `auto`, `next`, `status`, `new-milestone`, `query`, and exit codes. **Confidence: high.** (`src/help-text.ts:117-169`)

- **Structured result docs:** the orchestrator reference says `--output-format json` emits one `HeadlessJsonResult` to stdout at process exit with status, exitCode, sessionId, duration, cost, toolCalls, events, milestone, phase, nextAction, artifacts, and commits. **Confidence: high for docs.** (`gsd-orchestrator/references/json-result.md:1-38`)

- **Orchestrator command docs:** the headless command reference names `auto`, `next`, `new-milestone`, `dispatch <phase>`, `discuss`, `stop`, `pause`, `query`, `status`, `history`, `skip`, `undo`, `steer`, `queue`, `doctor`, `prefs`, and `knowledge`. **Confidence: high for docs.** (`gsd-orchestrator/references/commands.md:32-190`)

- **CI gates in gsd-2 repo:** CI includes docs prompt-injection scanning, secret scanning, `.gsd/` check, skill reference validation, test-required checks for PRs, build, typecheck extensions, validate package, workspace coverage, unit/package/coverage tests, and integration tests. **Confidence: high.** (`.github/workflows/ci.yml:71-132`, `.github/workflows/ci.yml:134-188`, `.github/workflows/ci.yml:189-229`)

### §A.5 Branch / worktree / git-strategy primitives for release work

- **Git strategy docs:** gsd-2 documents isolation modes `worktree`, `branch`, and `none`; worktree mode uses `.gsd/worktrees/<MID>/` and `milestone/<MID>` branches, then squash-merges to main and removes the worktree/branch on completion. **Confidence: high for docs.** (`docs/user-docs/git-strategy.md:1-18`, `docs/user-docs/git-strategy.md:90-124`)

- **Branch mode and none mode:** branch mode works in project root on `milestone/<MID>` and merges back to main; none mode commits directly on the current branch without branch isolation. **Confidence: high for docs.** (`docs/user-docs/git-strategy.md:21-31`, `docs/user-docs/git-strategy.md:47-49`)

- **Commit format:** docs say task commits use conventional commit format with a `GSD-Task:` trailer. **Confidence: high for docs; source also builds this shape.** (`docs/user-docs/git-strategy.md:76-88`; `src/resources/extensions/gsd/git-service.ts:139-179`)

- **Git preferences:** source defines `auto_push`, `push_branches`, `remote`, `snapshots`, `pre_merge_check`, `commit_type`, `main_branch`, `merge_strategy`, `isolation`, `manage_gitignore`, `worktree_post_create`, `auto_pr`, `pr_target_branch`, `absorb_snapshot_commits`, `collapse_cadence`, and `milestone_resquash`. **Confidence: high.** (`src/resources/extensions/gsd/git-service.ts:45-105`)

- **Slice-cadence merge:** `collapse_cadence: "slice"` squash-merges each validated slice to main; `milestone_resquash` can re-squash per-slice commits into one milestone commit. **Confidence: high for source behavior.** (`src/resources/extensions/gsd/git-service.ts:89-104`; `src/resources/extensions/gsd/slice-cadence.ts:1-20`, `src/resources/extensions/gsd/slice-cadence.ts:70-90`, `src/resources/extensions/gsd/slice-cadence.ts:196-208`)

- **Pre-merge checks:** `runPreMergeCheck` can skip, use a configured command, or auto-detect `npm test`; it rejects shell metacharacters in the configured command and runs via `execFileSync`. **Confidence: high.** (`src/resources/extensions/gsd/git-service.ts:882-944`)

- **Auto-push and PR creation:** on worktree merge, gsd-2 can push the integration branch when `auto_push` is true and can create a draft PR with `gh pr create` when `auto_pr` is true, targeting `pr_target_branch` or main. **Confidence: high.** (`src/resources/extensions/gsd/auto-worktree.ts:2261-2307`)

- **Workflow branch patterns:** source has branch regexes for `gsd/.../M###/S##`, `gsd/quick/`, and generic `gsd/<workflow>/...`; a comment in `git-service.ts` says workflow-template branches include hotfix, bugfix, spike, etc. **Confidence: medium-high.** (`src/resources/extensions/gsd/branch-patterns.ts:1-16`; `src/resources/extensions/gsd/git-service.ts:300`)

- **Hotfix path:** the CI workflow observes `hotfix/**` branches, and the bundled `hotfix` workflow template exists; I did not observe a core git-service hotfix branch creation convention beyond these. **Confidence: medium-high.** (`.github/workflows/ci.yml:4-18`; `src/resources/extensions/gsd/workflow-templates/hotfix.md:1-46`)

### §A.6 Team-mode features specifically for release coordination

- **Mode defaults in source:** `mode: team` defaults include `git.auto_push: false`, `git.push_branches: true`, `git.pre_merge_check: true`, `git.merge_strategy: "squash"`, `git.isolation: "none"` in `MODE_DEFAULTS`, and `unique_milestone_ids: true`. **Confidence: high for source defaults.** (`src/resources/extensions/gsd/preferences-types.ts:64-90`)

- **Init wizard behavior:** the init wizard defaults to solo/worktree/autoPush true; it asks Solo vs Team, describes Team as "Multiple contributors — branch-based, PR-friendly workflow", and turns off `autoPush` when team is selected. **Confidence: high.** (`src/resources/extensions/gsd/init-wizard.ts:42-53`, `src/resources/extensions/gsd/init-wizard.ts:101-127`)

- **Docs/source divergence note:** git strategy docs list team `git.isolation` as `"worktree"`, while `MODE_DEFAULTS` in source shows team `isolation: "none"`. **Confidence: high for observed divergence.** (`docs/user-docs/git-strategy.md:135-145`; `src/resources/extensions/gsd/preferences-types.ts:80-89`)

- **Shared/local artifact boundary:** team docs say committed artifacts include `.gsd/PREFERENCES.md`, `.gsd/PROJECT.md`, `.gsd/REQUIREMENTS.md`, `.gsd/DECISIONS.md`, and `.gsd/milestones/`; local artifacts include lock files, metrics, state cache, runtime records, worktrees, and activity logs. **Confidence: high for docs.** (`docs/user-docs/working-in-teams.md:23-49`)

- **Plan review workflow:** team docs describe a two-PR cycle: plan PR from `/gsd discuss`, review plan artifacts in GitHub, then code PR after `/gsd auto`; `/gsd discuss` does not auto-commit. **Confidence: high for docs.** (`docs/user-docs/working-in-teams.md:85-104`)

- **Slice discussion gate:** team docs say `phases.require_slice_discussion: true` pauses auto-mode when a slice is missing `CONTEXT` and requires `/gsd discuss`. **Confidence: high for docs; source has the preference field.** (`docs/user-docs/working-in-teams.md:105-115`; `src/resources/extensions/gsd/types.ts:347-355`)

- **Parallel team work:** team docs say multiple developers can run auto mode on different milestones, each with a worktree and `milestone/<MID>` branch, and milestone dependencies can be declared in `M00X-CONTEXT.md` frontmatter. **Confidence: high for docs.** (`docs/user-docs/working-in-teams.md:116-132`)

### §A.7 Hooks / events / extension primitives that release workflows could attach to

- **Extension manifest hook points:** the gsd extension manifest lists Pi-level hooks: `session_start`, `session_switch`, `bash_transform`, `session_fork`, `before_agent_start`, `agent_end`, `session_before_compact`, `session_shutdown`, `tool_call`, `tool_result`, `tool_execution_start`, `tool_execution_end`, `model_select`, and `before_provider_request`. **Confidence: high.** (`src/resources/extensions/gsd/extension-manifest.json:15-30`)

- **Hook registration:** `register-extension.ts` registers dynamic/db/journal/query/memory/exec tools, shortcuts, cmux events, hooks, and ecosystem extension loading as non-critical registrations. **Confidence: high.** (`src/resources/extensions/gsd/bootstrap/register-extension.ts:102-138`)

- **GSD post-unit/pre-dispatch hooks:** `PostUnitHookConfig` supports `name`, `after`, `prompt`, `max_cycles`, `model`, `artifact`, `retry_on`, `agent`, and `enabled`; post-unit hooks trigger after matching unit types and can be idempotent via artifact existence and retry via a retry artifact. **Confidence: high.** (`src/resources/extensions/gsd/types.ts:271-318`; `src/resources/extensions/gsd/rule-registry.ts:145-230`, `src/resources/extensions/gsd/rule-registry.ts:238-268`)

- **GSD pre-dispatch hooks:** pre-dispatch hooks are loaded from preferences, fire before matching unit types, and can proceed/skip/replace/modify prompts. **Confidence: high.** (`src/resources/extensions/gsd/rule-registry.ts:270-320`; `src/resources/extensions/gsd/preferences-validation.ts:494-551`)

- **Shell hook docs:** user docs describe shell hooks configured in settings with hook names including `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `SessionEnd`, `Stop`, `Notification`, `Blocked`, `PreCompact`, `PostCompact`, `PreCommit`, `PostCommit`, `PrePush`, `PostPush`, `PrePr`, `PostPr`, `PreMilestone`, `PostMilestone`, `PreUnit`, `PostUnit`, `PreVerify`, `PostVerify`, and `BudgetThreshold`. **Confidence: high for docs; I did not fully trace every shell hook implementation.** (`docs/user-docs/hooks.md:1-42`, `docs/user-docs/hooks.md:43-70`)

- **Shell hook control protocol:** docs say hooks receive JSON on stdin and may return JSON to block actions, rewrite commit messages, rewrite PR title/body, or override budget action. **Confidence: high for docs.** (`docs/user-docs/hooks.md:71-92`)

### §A.8 Extension / plugin / skill / command surfaces

- **Slash command catalog:** `/gsd` has top-level commands for auto/next/status/queue/quick/discuss/changelog/dispatch/history/undo/export/mode/prefs/keys/hooks/doctor/logs/debug/forensics/new-milestone/parallel/update/start/templates/extensions/workflow/ship/session-report/backlog/pr-branch/add-tests/scan/worktree and others. **Confidence: high.** (`src/resources/extensions/gsd/commands/catalog.ts:16-87`)

- **Workflow templates:** the workflow template registry supports modes `oneshot`, `yaml-step`, `markdown-phase`, and `auto-milestone`; template entries carry `name`, `description`, `file`, `mode`, `phases`, `triggers`, `artifact_dir`, `estimated_complexity`, and `requires_project`. **Confidence: high.** (`src/resources/extensions/gsd/workflow-templates.ts:26-49`)

- **Template discovery lifecycle:** templates can resolve by exact name, alias, prefix, or trigger matching; listing displays phases and complexity. **Confidence: high.** (`src/resources/extensions/gsd/workflow-templates.ts:82-143`, `src/resources/extensions/gsd/workflow-templates.ts:145-219`)

- **Bundled release/devops templates:** registry entries include `hotfix`, `changelog-gen`, `release`, `api-breaking-change`, `observability-setup`, and `ci-bootstrap`; `release` is `markdown-phase` with prepare/bump/publish/announce; `hotfix` is `markdown-phase` with fix/ship and `artifact_dir: null`. **Confidence: high.** (`src/resources/extensions/gsd/workflow-templates/registry.json:59-69`, `src/resources/extensions/gsd/workflow-templates/registry.json:103-113`, `src/resources/extensions/gsd/workflow-templates/registry.json:213-260`)

- **Custom workflow plugins:** docs say every workflow is discoverable via `/gsd workflow <name>`, can be project/global/bundled, and modes are oneshot, yaml-step, markdown-phase, and auto-milestone. **Confidence: high for docs.** (`docs/user-docs/commands.md:98-152`)

- **Workflow engine interface:** a pluggable `WorkflowEngine` has `engineId`, `deriveState`, `resolveDispatch`, `reconcile`, and `getDisplayMetadata`. **Confidence: high.** (`src/resources/extensions/gsd/workflow-engine.ts:16-38`)

- **Extension package validation:** external extension packages must declare `"gsd": { "extension": true }`, avoid reserved `gsd.*` IDs unless allowed, and avoid bundling `@gsd/*` host packages in dependencies/devDependencies. **Confidence: high.** (`src/extension-validator.ts:1-9`, `src/extension-validator.ts:36-90`, `src/extension-validator.ts:93-177`)

- **Ecosystem extension API:** gsd-2 wraps Pi's extension API to expose `getPhase()` and `getActiveUnit()`, captures `before_agent_start` handlers, and delegates tool/command/shortcut/flag/provider/event registration to Pi. **Confidence: high.** (`src/resources/extensions/gsd/ecosystem/gsd-extension-api.ts:38-45`, `src/resources/extensions/gsd/ecosystem/gsd-extension-api.ts:134-230`)

- **Skills:** GSD reads skills from `~/.agents/skills/` and project `.agents/skills/`, supports `skill_discovery` modes `auto`, `suggest`, `off`, supports skill preferences/rules, and tracks skill telemetry in `metrics.json`. **Confidence: high for docs.** (`docs/user-docs/skills.md:1-18`, `docs/user-docs/skills.md:85-123`, `docs/user-docs/skills.md:148-188`)

- **MCP tool surface:** native MCP server mode exposes all registered agent-session tools over `tools/list` and `tools/call`; workflow MCP lists GSD workflow tools such as `gsd_complete_milestone`, `gsd_complete_task`, `gsd_complete_slice`, `gsd_plan_milestone`, `gsd_plan_slice`, `gsd_reassess_roadmap`, `gsd_journal_query`, and related aliases. **Confidence: high.** (`src/mcp-server.ts:57-177`; `src/resources/extensions/gsd/workflow-mcp.ts:23-64`)

### §A.9 Telemetry / observability / cost / debugging surfaces

- **Metrics ledger:** metrics capture per-unit type/id/model/timestamps/tokens/cost/tool calls/message counts/api requests/context-window fields/tier/downgrade/skills/cache/compression and persist to `.gsd/metrics.json`. **Confidence: high.** (`src/resources/extensions/gsd/metrics.ts:1-14`, `src/resources/extensions/gsd/metrics.ts:30-77`, `src/resources/extensions/gsd/metrics.ts:130-240`)

- **Cost docs:** cost docs say every unit captures token counts, cost, duration, tool calls, and message counts, stored in `.gsd/metrics.json`; dashboard and `/gsd status` show real-time cost breakdown by phase/slice/model/project totals. **Confidence: high for docs.** (`docs/user-docs/cost-management.md:1-26`)

- **Budget controls:** docs describe `budget_ceiling`, enforcement modes `warn`, `pause`, `halt`, cost projections, and budget-pressure model downgrading. **Confidence: high for docs.** (`docs/user-docs/cost-management.md:27-83`)

- **Journal:** source writes daily-rotated JSONL events to `.gsd/journal/YYYY-MM-DD.jsonl`, grouped by flowId/seq with causedBy references; event types include dispatch, unit, guard, milestone, stuck, worktree, slice-merged, milestone-resquash, and subagent events. **Confidence: high.** (`src/resources/extensions/gsd/journal.ts:1-13`, `src/resources/extensions/gsd/journal.ts:31-84`, `src/resources/extensions/gsd/journal.ts:99-208`)

- **Worktree telemetry:** worktree telemetry emits created/merged/orphaned/auto-exit/sync/canonical-root/slice-merged/milestone-resquash events and summarizes orphan counts, merge durations, conflict counts, exit reasons, and related metrics. **Confidence: high.** (`src/resources/extensions/gsd/worktree-telemetry.ts:1-20`, `src/resources/extensions/gsd/worktree-telemetry.ts:40-207`, `src/resources/extensions/gsd/worktree-telemetry.ts:208-220`)

- **Forensics:** forensics scans activity logs, metrics, crash locks, doctor diagnostics, journal summary, and worktree telemetry; anomaly types include stuck loops, cost spikes, timeouts, missing artifacts, crashes, doctor issues, journal issues, worktree orphan, and unmerged exit. **Confidence: high.** (`src/resources/extensions/gsd/forensics.ts:1-9`, `src/resources/extensions/gsd/forensics.ts:40-119`, `src/resources/extensions/gsd/forensics.ts:734-790`)

- **Debug sessions:** `/gsd debug` creates persistent debug sessions under `.gsd/debug/sessions/<slug>.json`, with list/status/continue/diagnose modes. **Confidence: high for docs.** (`docs/user-docs/debug.md:1-31`, `docs/user-docs/debug.md:52-108`)

- **Command surfaces:** command catalog includes `status`, `visualize`, `history`, `rate`, `hooks`, `skill-health`, `doctor`, `logs`, `debug`, `forensics`, and `session-report`. **Confidence: high.** (`src/resources/extensions/gsd/commands/catalog.ts:25-55`, `src/resources/extensions/gsd/commands/catalog.ts:80-80`)

### §A.10 Security / sandboxing / runtime-policy surfaces

- **Unit tools policy:** auto-mode docs say each unit has a `UnitContextManifest` with `ToolsPolicy`; planning units can read broadly, write planning artifacts under `.gsd/`, run only read-only shell commands, and block unsafe writes/subagent dispatch with hard policy errors. **Confidence: high for docs.** (`docs/user-docs/auto-mode.md:31-36`)

- **Write gate:** source tracks write-gate state, pending gate IDs, read-only tool sets, safe shell regexes, and persists write-gate state under `.gsd/runtime/write-gate-state.json` by default. **Confidence: high.** (`src/resources/extensions/gsd/bootstrap/write-gate.ts:19-64`, `src/resources/extensions/gsd/bootstrap/write-gate.ts:69-118`, `src/resources/extensions/gsd/bootstrap/write-gate.ts:128-190`)

- **Exec sandbox:** `gsd_exec` sandbox runs bash/node/python scripts in subprocesses, persists stdout/stderr/meta under `.gsd/exec/`, returns only a digest, clamps timeouts, caps stdout/stderr bytes, and forwards only PATH/HOME plus allowlisted env vars. **Confidence: high.** (`src/resources/extensions/gsd/exec-sandbox.ts:1-9`, `src/resources/extensions/gsd/exec-sandbox.ts:16-65`, `src/resources/extensions/gsd/exec-sandbox.ts:67-151`)

- **Destructive command classifier:** safety code classifies destructive bash patterns such as recursive delete, force push, hard reset, git clean, SQL drop/truncate, chmod 777, and pipe-to-shell; comment says it classifies/logs but does not block. **Confidence: high.** (`src/resources/extensions/gsd/safety/destructive-guard.ts:1-8`, `src/resources/extensions/gsd/safety/destructive-guard.ts:16-48`)

- **Secret scanning:** CI runs `scripts/secret-scan.sh --diff origin/main`; the scanner detects multiple secret patterns and exits `1` on findings. **Confidence: high.** (`.github/workflows/ci.yml:92-103`; `scripts/secret-scan.mjs:11-27`, `scripts/secret-scan.mjs:141-184`)

- **Key manager:** `/gsd keys` uses `AuthStorage`, tracks provider key types, masks keys for display, and stores auth at `~/.gsd/agent/auth.json`. **Confidence: high.** (`src/resources/extensions/gsd/key-manager.ts:1-15`, `src/resources/extensions/gsd/key-manager.ts:80-136`, `src/resources/extensions/gsd/key-manager.ts:150-180`)

- **Hook trust model:** hook docs say project-local hooks are not executed unless explicitly trusted via `.pi/hooks.trusted`, while global hooks run because they are user-controlled. **Confidence: high for docs.** (`docs/user-docs/hooks.md:93-107`)

## §B. Workflow mapping (inference cited to §A; no recommendations)

### §B.1 Minor-release cycle

- **Supported/composable from primitives:** A team could map a minor release to a milestone because gsd-2 describes milestones as "shippable version" / MVP / major release / feature set and milestone artifacts carry vision, success criteria, slices, dependencies, demos, verification, summaries, and validation data (§A.2). **Confidence: medium-high.**

- **Execution mapping:** Work would likely flow through milestone discussion/planning/execution/validation using `/gsd auto`, headless `auto`/`next`, or MCP workflow tools, with verification commands and summaries attached to tasks/slices (§A.2, §A.4, §A.8). **Confidence: medium-high.**

- **Semver bump location:** Semver bumping appears outside core milestone fields: in gsd-2's own release scripts and in the bundled release workflow template's bump phase (§A.1, §A.3). **Confidence: high.**

- **CHANGELOG generation location:** Changelog generation appears in both gsd-2's own `generate-changelog/update-changelog` scripts and a `changelog-gen` oneshot template (§A.1, §A.8). **Confidence: high.**

- **Release artifact:** For a user project, the explicit release artifact appears to be workflow-template output under `.gsd/workflows/releases/`, including `PREPARE.md` and `RELEASE.md`; milestone output separately includes roadmap, plans, summaries, UAT, and reports (§A.2, §A.3, §A.8). **Confidence: medium-high.**

### §B.2 Patch / hotfix cycle

- **Supported directly as workflow template:** gsd-2 has a `hotfix` markdown-phase template with fix/ship phases, minimal ceremony, no planning artifacts, and no artifact directory (§A.8). **Confidence: high.**

- **CI branch support in own repo:** gsd-2's own CI runs on `hotfix/**` push branches (§A.1). **Confidence: high.**

- **Milestone fit:** Core milestones could represent a patch if a team chooses, but the hotfix template appears explicitly designed to avoid full milestone ceremony (§A.2, §A.8). **Confidence: medium-high.**

- **Branch/hotfix tooling:** I observed hotfix workflow/CI naming but not a core `hotfix/<name>` branch lifecycle or backport command in git-service (§A.5). **Confidence: medium.**

### §B.3 Pre-release / RC workflow

- **Supported directly in gsd-2's own repo for dev/next, not explicitly RC:** gsd-2's own workflows publish `@dev` and `@next` pre-release channels, while production uses environment approval and `@latest` (§A.3). **Confidence: high.**

- **Composable for user projects:** A user project could likely encode RC/soak steps in the release template's publish/verify phases, workflow plugins, pre/post hooks, or external CI, but I did not observe a named RC primitive (§A.3, §A.7, §A.8). **Confidence: medium.**

- **No apparent direct RC support:** No observed `rc` command, RC tag schema, or staged rollout field in milestone/release schemas (§A.2, §A.3). **Confidence: medium.**

### §B.4 CI-driven release pipeline

- **Supported directly for automation:** `gsd headless` supports CI/script execution, JSON/JSONL output, event filters, exit codes, query mode, answers, supervised mode, resume, and bare mode (§A.4). **Confidence: high.**

- **State inspection:** CI could use `gsd headless query` for state/next dispatch/cost without spawning an LLM, then run `next` or `auto` and gate on exit code/status (§A.4). **Confidence: high.**

- **Pipeline attachment:** CI can combine headless GSD with existing repo CI gates, release workflow templates, workflow plugins, and hooks (§A.1, §A.4, §A.7, §A.8). **Confidence: medium-high.**

- **Own repo example:** gsd-2 itself uses GitHub Actions for CI, manual dev/next/prod publishing, release generation, Docker publishing, and rollback docs, but those workflows are repo-specific GitHub Actions rather than a generic GSD command (§A.1, §A.3). **Confidence: high.**

### §B.5 Team coordination around a release

- **Supported artifacts:** Team mode supports shared planning artifacts and local runtime artifacts; plan/code PR split can coordinate release scope review before implementation (§A.6). **Confidence: high.**

- **Supported git controls:** Team settings can push branches, run pre-merge checks, create draft PRs, use unique milestone IDs, and run parallel milestones with dependencies (§A.5, §A.6). **Confidence: medium-high.**

- **Human coordination externality:** Slack/Discord remote questions exist as bundled tools, but I did not observe native calendar/standup/release train coordination, freeze-window, approver roster, or staged rollout ownership fields in core artifacts (§A.6, §A.8). **Confidence: medium.**

### §B.6 Milestone-to-release semantic mapping (the orchestration question)

- **No fixed semver mapping observed:** gsd-2 docs call a milestone a "shippable version" and give examples including MVP, major release, and feature set, but core schemas do not encode major/minor/patch/RC, target version, or release date (§A.2). **Confidence: high.**

- **Mapping appears open/conventional:** Because milestones can be MVP, major release, or feature set, and release workflow is a separate template, the relation between milestone and release appears team-defined rather than enforced 1:1 (§A.2, §A.3, §A.8). **Confidence: medium-high.**

- **One milestone spanning multiple minor releases:** I did not observe a source rule forbidding this, but the "shippable version" wording and squash-merge-at-milestone completion default suggest the default mental model is a milestone as a bounded shippable unit (§A.2, §A.5). **Confidence: medium-low.**

- **One minor release spanning multiple milestones:** I did not observe a source rule forbidding this; parallel milestones, milestone dependencies, and release workflow templates could be composed so a release gathers multiple completed milestones (§A.6, §A.8). **Confidence: medium-low.**

### §B.7 Visible mismatches

- **B.1 mismatch:** Minor-release planning can map to milestones, but semver bump, changelog, tag, publish, and release-note artifacts live in separate release scripts/templates rather than in milestone schemas. **Confidence: high.** (§B.1; §A.1, §A.2, §A.3)

- **B.2 mismatch:** Hotfix is directly available as a minimal workflow template, but I did not observe a complete hotfix branch/backport/promote lifecycle in core git strategy; CI observes `hotfix/**` only in gsd-2's own repo. **Confidence: medium-high.** (§B.2; §A.5, §A.8)

- **B.3 mismatch:** RC/staging/soak workflows are composable from dev/next channels, release templates, hooks, and CI, but there is no apparent user-project RC primitive or staged-rollout schema. **Confidence: medium.** (§B.3; §A.3, §A.7, §A.8)

- **B.4 mismatch:** Headless mode is CI-friendly, but CI-to-release orchestration appears external: gsd-2 offers primitives and its own GitHub Actions, not a generic release-pipeline command that owns environment promotion. **Confidence: medium.** (§B.4; §A.1, §A.4)

- **B.5 mismatch:** Team mode covers shared artifacts, plan review, branch/PR defaults, and dependencies, but release coordination items like release freeze, approvers, launch comms, and rollout ownership appear external to GSD artifacts. **Confidence: medium.** (§B.5; §A.6)

- **B.6 mismatch:** Milestone-to-release mapping is not explicit; no fixed 1:1, many:1, or 1:many rule is visible. **Confidence: high.** (§B.6; §A.2)

- **Cross-cutting mismatch:** Docs/source drift exists in at least one team default (`git.isolation`), so release/devops users would need to verify effective preferences rather than rely only on docs. **Confidence: high.** (§A.6)

## §C. Candidate intervention surfaces (heavily qualified; gap-anchored)

### §C.1 Candidate: release metadata artifact linked to milestones

- **Addresses:** §B.7 B.1 and B.6 mismatches.
- **Surface shape:** new artifact, likely under `.gsd/workflows/releases/` or milestone directory, not necessarily a core schema change.
- **Builds on:** release workflow artifact directory and `PREPARE.md`/`RELEASE.md` pattern (§A.3); milestone roadmap/summaries (§A.2); custom workflow plugin discovery (§A.8).
- **Architectural assumption:** assumes a workflow template can write a release artifact that references one or more milestone IDs without changing the core milestone schema.
- **Assumption verified?** Plausible-but-unverified. The release template says it writes `PREPARE.md` and `RELEASE.md`, but I did not trace markdown-phase executor write semantics.
- **Confidence:** medium — low architectural pressure, but viability depends on executor behavior and synthesis deciding whether artifact-only linkage is enough.
- **Caveat:** candidate; would need viability check against markdown-phase workflow state and artifact writes.

### §C.2 Candidate: semver-aware release workflow plugin

- **Addresses:** §B.7 B.1 mismatch.
- **Surface shape:** modification to existing `release` workflow template or new custom workflow plugin.
- **Builds on:** bundled `release` template phases (§A.3); workflow plugin modes/discovery (§A.8); own-repo semver/changelog scripts as precedent (§A.1).
- **Architectural assumption:** assumes markdown-phase workflows can execute deterministic shell steps or prompt agents to run existing project scripts while preserving approval gates.
- **Assumption verified?** Plausible-but-unverified. The template text describes shell/git steps, but I did not inspect the markdown-phase engine enough to confirm deterministic command hooks.
- **Confidence:** medium-low — candidate is well-aligned with existing surface, but implementation depth is unverified.
- **Caveat:** starting point for synthesis to evaluate; not a recommendation.

### §C.3 Candidate: hotfix branch/backport workflow plugin

- **Addresses:** §B.7 B.2 mismatch.
- **Surface shape:** new workflow template/plugin or enhancement to `hotfix.md`.
- **Builds on:** existing `hotfix` template (§A.8), CI `hotfix/**` branch precedent (§A.1), git-service branch/PR/pre-merge primitives (§A.5), and `pr-branch` filtered cherry-pick command (§A.5).
- **Architectural assumption:** assumes workflow templates can own branch naming and cherry-pick/backport instructions without core git-service additions.
- **Assumption verified?** Plausible-but-unverified. `pr-branch` proves filtered cherry-pick code exists, but not that hotfix workflows can invoke it programmatically.
- **Confidence:** medium-low — plausible gap fit; needs source check of workflow execution APIs.
- **Caveat:** candidate; would need viability check around branch operations and conflict handling.

### §C.4 Candidate: RC/staging workflow template

- **Addresses:** §B.7 B.3 mismatch.
- **Surface shape:** new bundled or custom `markdown-phase` workflow template.
- **Builds on:** release template prepare/bump/publish/announce gates (§A.3), workflow template registry modes (§A.8), hooks around PrePush/PrePr/PostVerify/BudgetThreshold (§A.7), and headless CI output (§A.4).
- **Architectural assumption:** assumes RC/staging can be represented as phased procedural state rather than a new milestone field.
- **Assumption verified?** Plausible-but-unverified. The template system supports markdown-phase workflows, but I did not confirm whether phase state can persist enough soak-test metadata.
- **Confidence:** medium — surface shape matches existing plugin vocabulary; operational semantics need validation.
- **Caveat:** candidate only; synthesis should test whether RC needs core release metadata rather than a template.

### §C.5 Candidate: generic release-pipeline headless recipe

- **Addresses:** §B.7 B.4 mismatch.
- **Surface shape:** new docs artifact, orchestrator skill/reference, or workflow plugin; not necessarily code.
- **Builds on:** `gsd headless` JSON/JSONL/exit codes/query/supervised/answers surfaces (§A.4), own-repo CI workflows (§A.1), and CI/CD docs rollback/promotion precedent (§A.3).
- **Architectural assumption:** assumes production CI owners want to compose GSD via shell/JQ rather than let GSD own environments.
- **Assumption verified?** Plausible-but-unverified. Headless docs explicitly target orchestrators, but user-project release-pipeline expectations were not surveyed.
- **Confidence:** medium — low-risk follow-up surface, but may be too documentation-shaped for downstream goals.
- **Caveat:** candidate; not a claim that documentation is sufficient.

### §C.6 Candidate: release coordination checklist artifact

- **Addresses:** §B.7 B.5 mismatch.
- **Surface shape:** new artifact in release workflow output, or markdown-phase template section.
- **Builds on:** release template `PREPARE.md` and `RELEASE.md` outputs (§A.3), team shared artifact boundary and plan PR workflow (§A.6), and hooks/remote questions (§A.7, §A.8).
- **Architectural assumption:** assumes coordination metadata can remain in checked-in Markdown artifacts rather than requiring integrations with Slack/calendar/incident systems.
- **Assumption verified?** Unverified. I did not inspect any release coordination artifact or external integration behavior beyond docs.
- **Confidence:** medium-low — addresses a visible gap but may duplicate team-external systems.
- **Caveat:** candidate for synthesis to evaluate, especially against actual team workflows.

### §C.7 Candidate: explicit milestone-release mapping note

- **Addresses:** §B.7 B.6 mismatch.
- **Surface shape:** new doc convention or optional field in release artifact; modification to core milestone schema would be a stronger variant.
- **Builds on:** milestone docs saying a milestone is a shippable version/major release/feature set (§A.2), release workflow artifacts (§A.3), and custom workflow plugins (§A.8).
- **Architectural assumption:** assumes the mapping should stay optional/team-defined rather than enforced by the milestone schema.
- **Assumption verified?** Unverified. Source shows no fixed mapping, but that does not verify intended future direction.
- **Confidence:** medium — useful as a characterization gap; any schema change would need deeper architecture review.
- **Caveat:** candidate; should not be read as a recommendation to add a field.

### §C.8 Candidate: preference-effective-state check in release workflows

- **Addresses:** §B.7 cross-cutting docs/source drift mismatch.
- **Surface shape:** release/hotfix workflow preflight step, hook, or headless `query`/`prefs` check.
- **Builds on:** preferences loading/mode defaults (§A.6), headless query/JSON outputs (§A.4), and release workflow prepare phase (§A.3).
- **Architectural assumption:** assumes release workflows can inspect effective preferences before doing git/release operations.
- **Assumption verified?** Plausible-but-unverified. Preferences are loadable in source, but I did not verify a stable command emits all effective preferences as JSON.
- **Confidence:** medium-low — motivated by observed drift, but implementation surface needs checking.
- **Caveat:** candidate for follow-up; not a design recommendation.

## §D. Open questions / probe limits

- I did not inspect the full markdown-phase/yaml-step workflow engines, so §C candidates that rely on workflow executor behavior are intentionally marked plausible-but-unverified.
- I did not fetch the shallow clone; release cadence/history claims are limited to checked-out files and local tags.
- I did not deep-read external Pi SDK or RTK docs.
- I did not fully trace every shell hook event implementation; hook docs are cited separately from source-observed GSD post-unit/pre-dispatch hooks.
- I did not test running `gsd headless`; findings are source/docs observations only.
- The most valuable next verification would be: how markdown-phase workflows persist state/artifacts, whether they can run deterministic shell commands, and whether effective preferences can be emitted machine-readably.
- A second valuable check would compare docs/source defaults for team/git behavior beyond the one observed `git.isolation` drift.

## §E. Probe self-disclosure

- I read gsd-2 source and docs under `/home/rookslog/workspace/projects/gsd-2-explore/`, including package metadata, release scripts, GitHub workflows, workflow templates, git/worktree code, headless code, hook/extension code, telemetry/debug/security surfaces, and selected user/dev docs.
- I read the permitted slice 1 pilot output at `.planning/gsd-2-uplift/exploration/01-mental-model-output.md` for orientation and cited its relevant line ranges only indirectly through current source citations; I did not duplicate its mental-model findings.
- I did not read the forbidden `.planning/audits/`, `INITIATIVE.md`, `DECISION-SPACE.md`, other orchestration specs, prior deep research, or deliberation logs.
- I encountered no forbidden material accidentally.
- The §A/§B/§C boundary was hardest around release templates: the templates themselves prescribe workflows, so I treated their text as §A observation, mapped usage in §B, and reserved only gap-anchored variants for §C.
