---
slice: 1 (Mental model + mission + target user)
date: 2026-04-27
agent: codex GPT-5.5 high
status: complete
---

# Slice 1 output — Mental model + mission + target user

## (i) What I read

gsd-2 source / package metadata:

- `README.md:1-77` — top-level product claim, v2.78 highlights, installation, RTK note.
- `README.md:226-253` — v1-to-v2 comparison table.
- `README.md:281-353` — hierarchy, execution loop, auto mode, step mode.
- `README.md:356-490` — install/use/headless/two-terminal workflow and command table.
- `README.md:493-620` — managed artifacts, git strategy, verification, dashboard, reports, preferences, agent instructions.
- `VISION.md:1-37` — mission, audience, principles, relationship to GSD-1.
- `CHANGELOG.md:1-180` — latest release entries and unreleased status.
- `package.json:1-158` — package name/version/description, binaries, Node engine, scripts, dependencies.
- `src/loader.ts:1-246` — executable loader, fast help/version path, Node/git gates, environment setup, managed resources.
- `src/cli.ts:1-246`, `src/cli.ts:260-620`, `src/cli.ts:618-891` — CLI argument handling, graph/web/headless/auto/worktree/print/MCP/interactive branches.
- `src/help-text.ts:1-210` — CLI help/subcommand help for human and headless use.
- `src/cli-web-branch.ts:1-300` — parsed CLI flags and web-mode launch routing.
- `src/headless.ts:1-320` — headless orchestrator options and behavior.
- `src/mcp-server.ts:55-185` — native MCP server wrapper over registered tools.

gsd-2 workflow extension and artifact model:

- `src/resources/extensions/gsd/extension-manifest.json:1-32` — core extension manifest: commands, tools, hooks, shortcut.
- `src/resources/extensions/gsd/index.ts:1-37` — core `/gsd` command registration and bootstrap fallback.
- `src/resources/extensions/gsd/bootstrap/register-extension.ts:1-138` — registration of tools, hooks, shortcuts, worktree/exit commands, event listeners.
- `src/resources/extensions/gsd/commands/catalog.ts:1-260` — slash-command catalog and completions.
- `src/resources/extensions/gsd/commands/index.ts:1-20` — `/gsd` command handler registration.
- `src/resources/extensions/gsd/commands/dispatcher.ts:1-43` — handler dispatch chain for `/gsd`.
- `src/resources/extensions/gsd/commands/handlers/core.ts:1-260` — help/status/setup/model-facing command behavior.
- `src/resources/extensions/gsd/guided-flow.ts:1-76`, `src/resources/extensions/gsd/guided-flow.ts:1473-1668` — step-mode / smart-entry behavior.
- `src/resources/extensions/gsd/auto.ts:1-11`, `src/resources/extensions/gsd/auto.ts:355-390`, `src/resources/extensions/gsd/auto.ts:1888-1925` — auto-mode description, detached start, fresh session mechanics.
- `src/resources/extensions/gsd/auto-start.ts:336-420`, `src/resources/extensions/gsd/auto-start.ts:596-735` — auto bootstrap, discussion routing, survivor-branch handling.
- `src/resources/extensions/gsd/auto-dispatch.ts:1-180`, `src/resources/extensions/gsd/auto-dispatch.ts:420-450` — declarative dispatch table and reassessment gating.
- `src/resources/extensions/gsd/init-wizard.ts:1-345` — per-project setup wizard and `.gsd/` bootstrap.
- `src/resources/extensions/gsd/detection.ts:1-260` — project-state and ecosystem detection.
- `src/resources/extensions/gsd/paths.ts:1-220`, `src/resources/extensions/gsd/paths.ts:293-417` — `.gsd` path resolution and milestone/slice/task file naming.
- `src/resources/extensions/gsd/types.ts:1-220` — typed model of phases, roadmap, slice/task plans, summaries, verification.
- `src/resources/extensions/gsd/state.ts:1-220` — DB-primary state derivation with filesystem fallback.
- `src/resources/GSD-WORKFLOW.md:1-260` — manual bootstrap protocol and artifact format reference.

gsd-2 user docs:

- `docs/user-docs/getting-started.md:1-180` — install prerequisites and first launch.
- `gitbook/getting-started/first-project.md:1-128` — first-project workflow and on-disk artifacts.
- `gitbook/core-concepts/auto-mode.md:1-216` — auto-mode overview, tool policy, runtime controls, diagnostics.
- `docs/user-docs/working-in-teams.md:1-132` — team mode and shared/local artifact boundary.

External docs:

- None. The README links to Pi SDK and RTK, but I did not need external documentation to answer this slice's mental-model questions.

## (ii) Calibrated findings

### Q1: What does gsd-2 do?

**Finding 1.1 — Advertised behavior:** gsd-2 presents itself as a standalone coding-agent CLI that can plan, execute, verify, commit, and advance through software work with less manual orchestration. **Confidence: high.** The README says v2 is a "standalone CLI" with direct access to the agent harness and claims it can clear context, inject files, manage git branches, track cost/tokens, detect stuck loops, recover from crashes, and auto-advance through a milestone (`README.md:14-18`). The package describes itself as "GSD — Get Shit Done coding agent" (`package.json:2-5`).

**Finding 1.2 — Entry points:** the primary executable entry point appears to be the `gsd` binary, with `gsd-cli` as another loader alias and `gsd-pi` mapped to the install script. **Confidence: high.** `package.json` maps `gsd` and `gsd-cli` to `dist/loader.js`, while `gsd-pi` points at `scripts/install.js` (`package.json:20-24`). The loader implements fast `--version` and `--help` behavior before heavy imports (`src/loader.ts:7-30`) and then imports `cli.js` after runtime/setup checks (`src/loader.ts:245-246`).

**Finding 1.3 — User-visible interaction modes:** source-observed interaction modes include an interactive terminal session, print/text/json/RPC/MCP modes, web mode, worktree mode, sessions, and headless automation. **Confidence: high.** CLI help lists `--mode <text|json|rpc|mcp>`, `--print`, `--continue`, `--worktree`, `--web`-adjacent subcommands, `auto`, `headless`, `graph`, and `sessions` (`src/help-text.ts:175-201`). The CLI routes `gsd headless` into `runHeadless()` (`src/cli.ts:424-434`), routes `gsd auto` to headless auto when invoked as a top-level subcommand (`src/cli.ts:457-462`), and starts an interactive `InteractiveMode` for normal TTY use (`src/cli.ts:753-891`).

**Finding 1.4 — Slash-command surface inside the agent session:** the central workflow surface is a `/gsd` command registered by a bundled extension. **Confidence: high.** The gsd extension manifest describes itself as the "Core GSD workflow engine" and provides commands including `gsd`, `kill`, `worktree`, and `exit` plus tools/hooks/shortcut (`src/resources/extensions/gsd/extension-manifest.json:1-32`). `registerGSDCommand()` registers the `gsd` command and delegates to `handleGSDCommand()` (`src/resources/extensions/gsd/commands/index.ts:5-18`), which dispatches to core, auto, parallel, workflow, and ops handlers (`src/resources/extensions/gsd/commands/dispatcher.ts:17-23`).

**Finding 1.5 — File-based interaction model:** gsd-2 uses `.gsd/` as the project-local workflow state and artifact tree. **Confidence: high.** The README says auto mode reads `.gsd/STATE.md` and dispatches based on disk state (`README.md:313-314`). `GSD-WORKFLOW.md` says all artifacts live in `.gsd/` and lists `STATE.md`, `DECISIONS.md`, `CODEBASE.md`, milestone roadmaps/context/research/summaries, slice plans/context/research/summaries/UAT, and task plans/summaries (`src/resources/GSD-WORKFLOW.md:40-66`). Source path helpers resolve the `.gsd` root, milestone directories, and canonical root files (`src/resources/extensions/gsd/paths.ts:293-417`).

**Finding 1.6 — Supported operation sequence:** the core advertised sequence is milestone → slice → task, with tasks sized to one context window, and a loop of planning, execution, completion, reassessment, validation, and milestone completion. **Confidence: high for advertised sequence; medium for exact current defaults.** README defines the hierarchy (`README.md:281-291`) and the flow (`README.md:293-303`). `GSD-WORKFLOW.md` repeats the hierarchy and file formats (`src/resources/GSD-WORKFLOW.md:28-66`). The source has phase types for discussion, research, planning, execution, verification, summarizing, advancing, validation, completion, paused, and blocked states (`src/resources/extensions/gsd/types.ts:7-26`).

**Finding 1.7 — Source-observed setup sequence:** for a new project, gsd-2 detects project signals, may initialize git, asks solo/team mode, detects verification commands, collects preferences, bootstraps `.gsd/`, initializes the SQLite DB when possible, updates `.gitignore`, may commit an initialized git repo, generates `CODEBASE.md`, writes `STATE.md`, and prepares workflow MCP. **Confidence: high.** This sequence appears directly in `showProjectInit()` (`src/resources/extensions/gsd/init-wizard.ts:61-344`). The smart-entry path runs this init wizard when bootstrap artifacts are absent (`src/resources/extensions/gsd/guided-flow.ts:1502-1529`).

### Q2: What problem does gsd-2 solve?

**Finding 2.1 — Claimed pain point:** gsd-2 frames the problem as agent-workflow control rather than prompt-only guidance. **Confidence: high.** The README says original GSD was "fighting the tool" via prompts/slash commands, without control over context windows, sessions, or execution (`README.md:14-16`), and the v1 comparison lists missing context control, automation, crash recovery, observability, cost tracking, stuck detection, timeout supervision, and reporting (`README.md:226-253`).

**Finding 2.2 — Claimed solution:** gsd-2 claims to solve this by making GSD a TypeScript application controlling the agent session rather than a prompt framework. **Confidence: high.** The README explicitly says v2 is "not a prompt framework anymore" but a TypeScript application that controls the agent session (`README.md:235-253`). `VISION.md` similarly frames GSD-2 as "the orchestration layer between you and AI coding agents" for planning, execution, verification, and shipping (`VISION.md:1-4`).

**Finding 2.3 — Artifact set broadly matches the claimed pain:** the source and bundled docs include state, plans, summaries, decision registers, DB-backed state, crash locks/recovery, verification, cost/metrics, dashboards, logs, forensics, and MCP/tool surfaces; this appears directionally consistent with the README's "control/observability/recovery" framing. **Confidence: medium-high.** Examples include `.gsd` artifact formats (`src/resources/GSD-WORKFLOW.md:40-66`), DB-primary state derivation with filesystem fallback (`src/resources/extensions/gsd/state.ts:1-3`), crash/session handling in auto mode (`src/resources/extensions/gsd/auto-start.ts:353-363`, `src/resources/extensions/gsd/auto-start.ts:596-649`), query tools for DB state (`src/resources/extensions/gsd/bootstrap/query-tools.ts:7-33`), and status/dashboard commands (`src/resources/extensions/gsd/commands/handlers/core.ts:144-173`).

**Finding 2.4 — The implementation scope appears broader than "workflow loop" alone:** gsd-2 includes a coding-agent host layer, extension system, provider/model setup, MCP server mode, web mode, worktree management, memory/knowledge tools, remote questions, voice, and ecosystem extensions. **Confidence: medium-high.** The CLI exposes provider/session/interactive/headless/MCP/web branches (`src/cli.ts:143-246`, `src/cli.ts:344-461`, `src/cli.ts:618-891`), the extension bootstrap registers dynamic/db/journal/query/memory/exec tools and hooks (`src/resources/extensions/gsd/bootstrap/register-extension.ts:102-138`), and the `/gsd` catalog spans workflow, visibility, correction, setup, maintenance, extensions, MCP, and worktree commands (`src/resources/extensions/gsd/commands/catalog.ts:19-87`).

**Finding 2.5 — There are some self-presentation tensions:** the README's compact narrative sometimes describes behavior as unconditional or automatic where source appears to gate it by preference. **Confidence: medium.** For example, README says the loop includes "Reassess Roadmap" and describes adaptive replanning after each slice (`README.md:293-303`, `README.md:333-335`), but `auto-dispatch.ts` defaults `reassess_after_slice` to `false` unless explicitly enabled (`src/resources/extensions/gsd/auto-dispatch.ts:429-440`). This does not invalidate the mental model, but it means downstream slices should verify defaults rather than rely on README phrasing.

### Q3: Who is the target user?

**Finding 3.1 — Stated audience:** gsd-2 says it is for "anyone who codes with AI agents," including solo developers, open-source maintainers, and "vibe coders." **Confidence: high for stated audience.** `VISION.md` states this directly (`VISION.md:5-8`). The README's getting-started flow assumes someone has a project directory, can install Node/npm/Git, can choose/log into an LLM provider, and can run terminal commands (`README.md:356-389`; `docs/user-docs/getting-started.md:7-15`).

**Finding 3.2 — Practical expected knowledge:** the implementation appears to expect users to understand or tolerate terminal workflows, git repositories, LLM provider auth, project verification commands, and review of generated planning artifacts. **Confidence: medium-high.** The project-init wizard tells users GSD uses git for version control/isolation and asks whether to initialize git (`src/resources/extensions/gsd/init-wizard.ts:76-94`), asks solo/team mode (`src/resources/extensions/gsd/init-wizard.ts:101-127`), surfaces detected verification commands (`src/resources/extensions/gsd/init-wizard.ts:129-151`), and stores project preferences (`src/resources/extensions/gsd/init-wizard.ts:265-284`).

**Finding 3.3 — Solo use is a first-class path:** the default project preferences and setup wizard appear optimized for solo use by default. **Confidence: medium-high.** `DEFAULT_PREFS` sets `mode: "solo"`, `gitIsolation: "worktree"`, `tokenProfile: "balanced"`, and `autoPush: true` (`src/resources/extensions/gsd/init-wizard.ts:42-53`). The setup wizard presents "Solo" as recommended and describes it as "Just me — auto-push, squash merge, worktree isolation" (`src/resources/extensions/gsd/init-wizard.ts:101-117`).

**Finding 3.4 — Team use is also intended, but appears to require explicit setup and shared artifact conventions:** team mode is documented and partially reflected in source preferences, but it is not the default. **Confidence: medium-high.** The setup wizard offers "Team" mode and turns off `autoPush` when selected (`src/resources/extensions/gsd/init-wizard.ts:113-127`). The team doc says `mode: team` enables unique milestone IDs, push branches, and pre-merge checks, and distinguishes committed planning artifacts from local runtime state (`docs/user-docs/working-in-teams.md:7-49`).

**Finding 3.5 — The audience claim is grounded but broad:** implementation supports both lower-ceremony solo usage and higher-ceremony team workflows, but the breadth of commands and setup suggests the "anyone" claim is aspirational at the edges. **Confidence: medium.** The first-project guide starts with `gsd`, `/gsd`, `/gsd auto`, and `/gsd status` (`gitbook/getting-started/first-project.md:3-23`, `gitbook/getting-started/first-project.md:36-82`), while the full command catalog exposes many advanced surfaces including parallel, workflow, MCP, doctor, forensics, worktree, keys, extensions, and PR-branch commands (`src/resources/extensions/gsd/commands/catalog.ts:19-87`).

### Q4: Does gsd-2 present itself as agent-facing, human-facing, or both?

**Finding 4.1 — gsd-2 is human-facing in its primary CLI/TUI posture:** it opens an interactive agent session, shows wizards, dashboards, help, setup prompts, and human steering commands. **Confidence: high.** README instructs users to run `gsd`, then type `/gsd`, `/gsd auto`, `/gsd discuss`, `/gsd status`, and `/gsd queue` (`README.md:381-416`). Source starts `InteractiveMode` in normal TTY sessions (`src/cli.ts:753-891`), the smart-entry path shows confirmation/action prompts via `showNextAction()` (`src/resources/extensions/gsd/guided-flow.ts:1473-1668`), and the status command opens a dashboard overlay when UI is available (`src/resources/extensions/gsd/commands/handlers/core.ts:144-173`).

**Finding 4.2 — gsd-2 is also agent-facing:** it registers tools, commands, hooks, prompt snippets/guidelines, and an MCP server surface for tool callers. **Confidence: high.** The extension manifest provides tools, commands, hooks, and shortcuts (`src/resources/extensions/gsd/extension-manifest.json:8-32`). Bootstrap registers DB/query/journal/memory/exec tools and hooks into Pi (`src/resources/extensions/gsd/bootstrap/register-extension.ts:102-138`). The MCP server exposes all registered agent-session tools over `tools/list` and executes them on `tools/call` (`src/mcp-server.ts:57-67`, `src/mcp-server.ts:96-177`).

**Finding 4.3 — The human/agent boundary appears operational rather than doctrinal:** gsd-2 mostly presents a human starting and steering a coding agent, while source mediates what the agent can see/do via prompts, tools, context injection, state files, and dispatch units. **Confidence: medium-high.** The README says GSD opens an interactive agent session (`README.md:389-394`) and that auto mode injects context into fresh sessions (`README.md:313-319`). Source comments for auto mode say each unit gets a fresh session and focused prompt (`src/resources/extensions/gsd/auto.ts:1-11`), and the actual unit path calls `newSession()` before dispatching work (`src/resources/extensions/gsd/auto.ts:1888-1909`).

**Finding 4.4 — Headless and MCP surfaces make gsd-2 machine-facing, not only TUI-facing:** this matters for downstream characterization because there are non-human-control surfaces in source. **Confidence: high.** `gsd headless` is documented for CI/scripts and can emit JSON/JSONL state/results (`README.md:417-440`; `src/help-text.ts:117-169`). `--mode mcp` activates every registered tool and starts an MCP server (`src/cli.ts:693-713`). `--mode rpc` starts RPC mode (`src/cli.ts:687-690`).

**Finding 4.5 — Agent-facing surfaces are not limited to "paper" prompt templates:** the system includes runtime write gates, DB tools, query tools, memory tools, exec tools, hooks, model routing, and workflow MCP preparation. **Confidence: medium-high.** The bootstrap registration list includes dynamic, DB, journal, query, memory, and exec tools plus shortcuts/hooks/ecosystem loaders (`src/resources/extensions/gsd/bootstrap/register-extension.ts:102-138`). Query tools explicitly tell the LLM to use `gsd_milestone_status` rather than direct SQLite access (`src/resources/extensions/gsd/bootstrap/query-tools.ts:7-33`).

### Q5: What is the current development status?

**Finding 5.1 — Current checked-out package version:** the checked-out package reports `2.78.1`. **Confidence: high.** `package.json` lists `"version": "2.78.1"` (`package.json:1-5`).

**Finding 5.2 — Last observed commit:** the shallow clone's latest commit is `82bcf6b7` dated `2026-04-27`, "Merge pull request #5080 from jeremymcs/fix/headless-auto-cwd-anchor." **Confidence: high for this local clone.** I observed this via `git log --oneline --date=short -n 12`; since this is command output rather than a file, treat it as local artifact-reported evidence from this run.

**Finding 5.3 — Release cadence at a glance appears active and rapid:** the changelog has an unreleased section plus releases `2.78.1` and `2.78.0` dated `2026-04-25`, and the README's latest section is "What's New in v2.78." **Confidence: high at-a-glance, without deeper cadence analysis.** See `CHANGELOG.md:7-18` and `README.md:30-77`.

**Finding 5.4 — Development status appears active rather than mature/stable-frozen:** recent changelog entries include many new features, fixes, and hardening items across auto, workflow, git, MCP, provider, web, and component surfaces. **Confidence: medium-high.** The `2.78.0` section lists added component-system, UnitContextManifest, extension framework, GPT-5.5 Codex support, workflow control-plane changes, and many fixes (`CHANGELOG.md:18-180`).

**Finding 5.5 — "Mature" should be used carefully:** the repository has extensive tests, docs, release history, and many reliability features, but the volume of recent fixes and new control-plane work suggests ongoing rapid evolution. **Confidence: medium.** `package.json` defines unit/integration/package/smoke/live test scripts (`package.json:63-101`), while recent changelog entries include state-machine hardening, write-gate fixes, crash recovery, worktree lifecycle, and MCP alias deprecations (`CHANGELOG.md:7-18`, `CHANGELOG.md:57-180`).

## (iii) What I deliberately did NOT read

- I did not read the dispatching project's forbidden prior-analysis artifacts: `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`, `.planning/audits/archive/`, `.planning/gsd-2-uplift/INITIATIVE.md`, `.planning/gsd-2-uplift/DECISION-SPACE.md`, other orchestration slice specs beyond `preamble.md` and `slice-01-mental-model.md`, `.planning/research/gemini-deep-research/`, or `.planning/deliberations/`.
- I did not read slice 2-5 specs except for their filenames appearing in an allowed directory listing before I re-focused on the permitted preamble and slice-1 spec.
- I did not inspect gsd-2 architecture docs in depth (`docs/dev/architecture.md`, Pi internals, ADRs) because architecture/runtime/Pi SDK relationship is slice 2 scope.
- I did not inspect release cadence deeply beyond package version, top changelog, README latest section, and local `git log -n 12`, because detailed cadence/pattern analysis is slice 5 scope.
- I did not inspect workflow-template internals, artifact lifecycle migration details, or distribution/package internals except where needed for entry points and visible behavior; those belong to slices 3-5.
- I did not follow external links to Pi SDK or RTK; source and README were sufficient for this slice's mental-model questions.

## (iv) Open questions surfaced

- **Direction-shifting evidence:** gsd-2 appears to be a full coding-agent application plus workflow engine, not just a planning-file convention or prompt package. **Confidence: medium-high.** Evidence includes CLI interactive/headless/MCP modes (`src/help-text.ts:175-201`), extension-registered tools/hooks (`src/resources/extensions/gsd/bootstrap/register-extension.ts:102-138`), and a broad command catalog (`src/resources/extensions/gsd/commands/catalog.ts:19-87`). If the dispatching project's characterization aim assumes a narrower artifact/template system, later slices should explicitly test that assumption.

- **Q4 boundary ambiguity:** I can answer "both human-facing and agent-facing" from source, but I did not find a compact doctrinal statement defining the boundary between human steering and agent autonomy. **Confidence: medium.** The README explains human commands and auto mode (`README.md:381-440`), while source implements agent tools/MCP/fresh-session dispatch (`src/mcp-server.ts:57-67`; `src/resources/extensions/gsd/auto.ts:1-11`), but the boundary is distributed across docs/source rather than stated once.

- **Default behavior needs second-wave verification:** some visible behaviors are advertised as part of the main loop, but source gates them by preferences or mode. **Confidence: medium.** Dedicated reassessment after slice completion is the clearest example (`README.md:293-303`, `README.md:333-335`; `src/resources/extensions/gsd/auto-dispatch.ts:429-440`). Slices 2-5 should distinguish capability, default, and opt-in behavior.

- **Cross-slice watchlist — failure modes/debugging appears central:** this is not just present; it appears repeatedly in README, docs, commands, and source. **Confidence: high.** Examples include crash recovery and stuck detection in README (`README.md:323-329`), diagnostic commands in auto-mode docs (`gitbook/core-concepts/auto-mode.md:190-216`), `/gsd doctor`, `/gsd debug`, `/gsd forensics`, `/gsd logs` in the command catalog (`src/resources/extensions/gsd/commands/catalog.ts:52-55`), and crash/session recovery in source (`src/resources/extensions/gsd/auto-start.ts:353-363`, `src/resources/extensions/gsd/auto-start.ts:629-649`).

- **Cross-slice watchlist — multi-user/collaboration appears central enough to carry forward:** team mode, unique milestone IDs, shared artifacts, and multi-developer workflows are documented, but I did not inspect enforcement depth. **Confidence: medium-high.** See `docs/user-docs/working-in-teams.md:1-49` and `docs/user-docs/working-in-teams.md:85-132`, plus source init solo/team selection (`src/resources/extensions/gsd/init-wizard.ts:101-127`).

- **Cross-slice watchlist — telemetry/observability appears central:** cost, token metrics, dashboards, activity/debug logs, journal/query tools, and worktree telemetry show up across README, docs, source, and commands. **Confidence: medium-high.** README highlights cost and dashboard behavior (`README.md:331-339`, `README.md:543-557`), command catalog includes logs/history/session-report/status (`src/resources/extensions/gsd/commands/catalog.ts:25-27`, `src/resources/extensions/gsd/commands/catalog.ts:35-39`, `src/resources/extensions/gsd/commands/catalog.ts:52-55`), and query/journal/memory tools are registered (`src/resources/extensions/gsd/bootstrap/register-extension.ts:104-110`).

- **Cross-slice watchlist — security/trust model may be central:** I did not investigate this slice deeply, but runtime tool policies, write gates, secret handling, MCP transport checks, and git safety appear in the visible surface. **Confidence: medium.** Auto-mode docs describe runtime tool policy enforcement (`gitbook/core-concepts/auto-mode.md:71-76`), query tools warn against direct DB access (`src/resources/extensions/gsd/bootstrap/query-tools.ts:7-18`), and the changelog lists security and git-safety hardening (`CHANGELOG.md:67-75`, `CHANGELOG.md:121-133`).

- **Prompt clarity feedback:** slice 1 was mostly clear. The only calibration issue is that "mission + target user" can easily bleed into architecture/runtime because gsd-2's self-presentation ties mission to Pi SDK/session control. I handled that by citing entry points and behavior but avoiding Pi SDK internals. **Confidence: high.**

## (v) Flags where README claims diverge from source observations

- **README/source divergence: RTK default.** README says GSD "now provisions a managed RTK binary" and says `GSD_RTK_DISABLED=1` disables the integration (`README.md:22`). Source says RTK is opt-in via `experimental.rtk` and "Default: disabled"; if the preference is not true, it sets `GSD_RTK_DISABLED=1` (`src/cli.ts:160-178`). **Confidence: high that the README phrasing is at least incomplete relative to this source snapshot.**

- **README/source divergence: reassess-after-slice default.** README's main loop includes `Reassess Roadmap` after complete and says reassessment checks whether the roadmap still makes sense (`README.md:293-303`); it also says adaptive replanning happens after each slice completes (`README.md:333-335`). Source dispatch defaults dedicated `reassess-roadmap` to off unless `prefs.phases.reassess_after_slice` is true, with an inline comment explaining the default is false (`src/resources/extensions/gsd/auto-dispatch.ts:429-440`). **Confidence: high that README's simplified loop overstates the default dedicated reassessment step.**

- **README/source alignment: v2 is no longer only prompts.** README says v2 is a TypeScript application that controls the agent session (`README.md:235-253`), and source supports that broad claim through a compiled loader/CLI, bundled extension registration, auto-mode fresh sessions, and MCP/headless paths (`package.json:20-24`; `src/loader.ts:245-246`; `src/resources/extensions/gsd/index.ts:18-29`; `src/resources/extensions/gsd/auto.ts:1-11`; `src/cli.ts:424-461`; `src/cli.ts:693-713`). I did not observe a divergence here within this slice's scope. **Confidence: high.**

- **README/source alignment: `.gsd/` as state/artifact substrate.** README says auto mode reads `.gsd/STATE.md` and that preferences/artifacts live under `.gsd/` (`README.md:313-314`, `README.md:493-513`, `README.md:568-594`), and source path/artifact helpers plus bootstrap behavior match this (`src/resources/extensions/gsd/paths.ts:293-417`; `src/resources/extensions/gsd/init-wizard.ts:265-344`; `src/resources/GSD-WORKFLOW.md:40-66`). I did not observe a divergence here. **Confidence: high.**
