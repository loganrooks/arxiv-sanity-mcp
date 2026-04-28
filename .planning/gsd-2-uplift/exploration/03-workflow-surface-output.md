---
slice: 3 (Workflow surface + automation + testing)
date: 2026-04-28
agent: codex GPT-5.5 high
status: complete
---

# Slice 3 output - Workflow surface + automation + testing

## (i) What I read

Dispatching-project inputs:

- `.planning/gsd-2-uplift/orchestration/preamble.md:7-104` for role, aim, output discipline, calibration rules, forbidden reading, and required output structure.
- `.planning/gsd-2-uplift/orchestration/slice-03-workflow-surface.md:7-53` for slice scope, diagnostic questions, slice-specific forbidden reading, and output path.

gsd-2 README and user docs:

- `README.md:14-18`, `README.md:22`, `README.md:32-75`, `README.md:192-215`, `README.md:226-329`.
- `docs/user-docs/commands.md:1-380`.
- `docs/user-docs/hooks.md:1-152`.
- `docs/user-docs/configuration.md:301-420`.
- `CONTRIBUTING.md:104`, `CONTRIBUTING.md:319-341`.

gsd-2 command and CLI source:

- `package.json:1-24`, `package.json:47-102`.
- `src/resources/extensions/gsd/index.ts:18-35`.
- `src/resources/extensions/gsd/commands/index.ts:5-19`.
- `src/resources/extensions/gsd/commands-bootstrap.ts:254-262`.
- `src/resources/extensions/gsd/commands/catalog.ts:16-309`.
- `src/resources/extensions/gsd/commands/dispatcher.ts:10-23`.
- `src/resources/extensions/gsd/commands/handlers/core.ts:15-245`.
- `src/resources/extensions/gsd/commands/handlers/auto.ts:45-154`.
- `src/resources/extensions/gsd/commands/handlers/workflow.ts:65-603`.
- `src/resources/extensions/github-sync/index.ts:1-90`.
- `src/resources/extensions/bg-shell/bg-shell-command.ts:1-73`.
- `src/cli-web-branch.ts:7-102`, `src/cli-web-branch.ts:206-300`.
- `src/help-text.ts:1-201`.
- `src/cli.ts:76-91`, `src/cli.ts:146-157`, `src/cli.ts:218-260`.

gsd-2 automation, workflow, hook, and verification source:

- `src/resources/extensions/gsd/auto.ts:1-11`, `src/resources/extensions/gsd/auto.ts:355-380`, `src/resources/extensions/gsd/auto.ts:1718-1769`.
- `src/resources/extensions/gsd/auto/loop.ts:1-155`, `src/resources/extensions/gsd/auto/loop.ts:210-719`.
- `src/resources/extensions/gsd/workflow-engine.ts:16-38`.
- `src/resources/extensions/gsd/engine-resolver.ts:1-56`.
- `src/resources/extensions/gsd/dev-workflow-engine.ts:1-109`.
- `src/resources/extensions/gsd/custom-workflow-engine.ts:1-244`.
- `src/resources/extensions/gsd/workflow-templates.ts:28-255`.
- `src/resources/extensions/gsd/uok/kernel.ts:45-117`.
- `src/resources/extensions/gsd/uok/flags.ts:4-39`.
- `src/resources/extensions/gsd/bootstrap/register-hooks.ts:65-607`.
- `src/resources/extensions/gsd/hook-emitter.ts:20-188`.
- `src/resources/extensions/gsd/post-unit-hooks.ts:1-86`.
- `packages/pi-coding-agent/src/core/settings-manager.ts:119-149`.
- `packages/pi-coding-agent/src/core/hooks-runner.ts:1-12`, `packages/pi-coding-agent/src/core/hooks-runner.ts:89-459`.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1293-1372`.
- `src/resources/extensions/gsd/verification-gate.ts:1-341`.
- `src/resources/extensions/gsd/auto-verification.ts:1-11`, `src/resources/extensions/gsd/auto-verification.ts:198-614`.
- `src/resources/extensions/gsd/custom-verification.ts:1-182`.
- `src/resources/extensions/gsd/commands-add-tests.ts:1-137`.

Machine-facing and external surface docs/source:

- `src/headless-query.ts:1-10`, `src/headless-query.ts:120-172`.
- `packages/rpc-client/README.md:1-104`.
- `src/rpc-mode.ts:727-762`.
- `packages/mcp-server/README.md:1-12`, `packages/mcp-server/README.md:76-217`.
- `.github/workflows/ci.yml:134-229`.

External docs:

- I did not read external RTK or Pi SDK repositories. The slice questions were answerable from gsd-2 source and gsd-2 docs.

## (ii) Calibrated findings

### Q1: What slash commands or CLI commands does gsd-2 expose?

**Top-level shape.** gsd-2 appears to expose one main slash-command namespace, `/gsd`, plus additional extension/session commands and a standalone `gsd` CLI. [high] The package declares CLI binaries `gsd` and `gsd-cli` pointing at `dist/loader.js`, plus `gsd-pi` pointing at `scripts/install.js` (`package.json:13-24`). The GSD extension registers the `/gsd` command and defers full setup until later initialization (`src/resources/extensions/gsd/index.ts:18-35`, `src/resources/extensions/gsd/commands/index.ts:5-19`, `src/resources/extensions/gsd/commands-bootstrap.ts:254-262`).

**The `/gsd` command family.** The docs list the main `/gsd` session commands as follows. [high]

| Purpose | Commands | What they consume / produce |
| --- | --- | --- |
| Main work loop | `/gsd`, `/gsd next`, `/gsd auto`, `/gsd quick`, `/gsd stop`, `/gsd pause` | These consume `.gsd` planning/runtime state and dispatch or control the work loop; `/gsd auto` can take options such as milestone, stop condition, or yolo mode in source (`docs/user-docs/commands.md:5-15`, `src/resources/extensions/gsd/commands/handlers/auto.ts:45-144`). |
| Steering and task intake | `/gsd steer`, `/gsd discuss`, `/gsd queue`, `/gsd capture`, `/gsd triage`, `/gsd dispatch` | These appear to manipulate or discuss project work items, queues, captures, and dispatches; source groups them in the top-level catalog and workflow handlers rather than as separate binaries (`docs/user-docs/commands.md:16-24`, `src/resources/extensions/gsd/commands/catalog.ts:19-87`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:492-603`). |
| Status, logs, and forensics | `/gsd status`, `/gsd widget`, `/gsd history`, `/gsd forensics`, `/gsd debug`, `/gsd logs`, `/gsd export`, `/gsd visualize` | These consume runtime state, history, logs, and graph/status data, and produce text output or UI output when a UI is available. `handleStatus` derives dashboard state; `handleVisualize` requires UI and otherwise tells the user to use text status (`docs/user-docs/commands.md:25-42`, `src/resources/extensions/gsd/commands/handlers/core.ts:144-201`). |
| Project setup/config/diagnostics | `/gsd prefs`, `/gsd mode`, `/gsd config`, `/gsd keys`, `/gsd doctor`, `/gsd inspect`, `/gsd init`, `/gsd setup`, `/gsd skill-health`, `/gsd hooks`, `/gsd run-hook`, `/gsd migrate` | These consume and update settings, keys, project initialization state, hooks configuration, or diagnostics surfaces (`docs/user-docs/commands.md:43-62`, `src/resources/extensions/gsd/commands/handlers/core.ts:204-245`). |
| Milestone/task state management | `/gsd new-milestone`, `/gsd skip`, `/gsd undo`, `/gsd undo-task`, `/gsd reset-slice`, `/gsd park`, `/gsd unpark`, `/gsd discard` | These operate on milestone/slice/task state and work parking queues (`docs/user-docs/commands.md:63-75`, `src/resources/extensions/gsd/commands/catalog.ts:19-87`). |
| Parallel orchestration | `/gsd parallel start/status/stop/pause/resume/merge` | These manage parallel execution groups and merge steps; the docs present them as a distinct orchestration surface (`docs/user-docs/commands.md:76-87`). |
| Workflow templates | `/gsd start`, `/gsd start resume`, `/gsd templates`, `/gsd templates info` | These consume bundled or installed workflow templates and produce initialized workflow state or template descriptions (`docs/user-docs/commands.md:89-97`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:492-603`). |
| Custom workflows | `/gsd workflow start/list/info/install/uninstall/validate/pause/resume/dispatch` | These consume workflow definitions from plugin directories, local paths, package references, or registry entries; `start` can create a run directory and start auto-mode for some modes (`docs/user-docs/commands.md:98-152`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:65-85`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:165-222`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:248-268`). |
| Extensions | `/gsd extensions list/info/install/update/uninstall/enable/disable/doctor/validate` | These manage extension lifecycle and validation (`docs/user-docs/commands.md:154-168`). |
| cmux | `/gsd cmux status/validate/doctor/adapter/queue/template` | These expose cmux-related bridge/status/template commands (`docs/user-docs/commands.md:169-179`). |
| GitHub sync | `/github-sync status/bootstrap` | This is a separate slash command that inspects or bootstraps GitHub issues/milestones/slices/tasks from GSD state (`docs/user-docs/commands.md:180-187`, `src/resources/extensions/github-sync/index.ts:18-39`, `src/resources/extensions/github-sync/index.ts:72-90`). |
| Worktrees | `/gsd git worktree ...`, `/gsd worktree ...` | These expose native git worktree wrappers and GSD worktree isolation commands, with docs distinguishing direct git-like worktree operations from GSD managed isolation commands (`docs/user-docs/commands.md:189-211`). |
| Remote control | `/gsd remote start/status/stop/test/send/poll/approve/reject/logs` | These expose Telegram-backed remote control, approval, and polling operations (`docs/user-docs/commands.md:213-227`). |

**Other in-session commands.** gsd-2 also documents session management commands `/clear`, `/exit`, `/kill`, `/model`, `/login`, `/thinking`, and `/voice`; these appear to be broader runtime commands rather than GSD-project-specific commands. [high] The docs explicitly group them as "Session Management Commands" (`docs/user-docs/commands.md:229-239`). gsd-2 also exposes `/bg` for background shell jobs; the `/bg` command has UI behavior when an overlay is available and text-list behavior otherwise (`src/resources/extensions/bg-shell/bg-shell-command.ts:25-28`, `src/resources/extensions/bg-shell/bg-shell-command.ts:52-73`).

**CLI surface.** The standalone CLI exposes subcommands for `config`, `update`, `sessions`, `worktree`, `graph`, and `headless`, plus modes and aliases for interactive/headless/web/RPC/MCP/text execution. [high] Help text documents the subcommands and their examples (`src/help-text.ts:1-201`). The runtime also detects non-TTY invocation and suggests `--print`, `--web`, `--rpc`, `--mcp`, `--text`, `--headless`, or `gsd auto` rather than plain interactive startup (`src/cli.ts:76-91`). CLI flags include `--mode`, `--print`, `--continue`, `--no-session`, `--worktree`, `--web`, `--model`, `--extension`, and `--tools` (`src/cli-web-branch.ts:7-102`). The web aliases include `browser`, `web`, `server`, `serve`, and `webui` (`src/cli-web-branch.ts:206-300`).

**Headless and machine-query commands.** Headless mode is a documented CLI mode, with a special `gsd headless query` path that reads project state without asking an LLM. [high] The docs describe `gsd headless "prompt"` and options for JSON, model, continuation, timeout, and non-interactive use (`docs/user-docs/commands.md:279-321`). `headless query` is implemented as a deterministic project-state query path that "does not invoke the LLM" and supports JSON/tabular output over several entity types (`src/headless-query.ts:1-10`, `src/headless-query.ts:120-172`).

### Q2: Does gsd-2 provide automation, and if so what?

**Yes, gsd-2 provides automation beyond standard command invocation.** [high] The README describes a TypeScript application controlling an agent session, clearing context, injecting files, managing git branches, tracking cost/tokens, detecting stuck loops, recovering from errors, and auto-advancing through work (`README.md:14-18`, `README.md:226-253`). Source corroborates an auto-mode loop: `auto.ts` describes a state machine driven by `.gsd/` files, with fresh session dispatch per unit, rereading disk after `agent_end`, and injecting the next focused prompt (`src/resources/extensions/gsd/auto.ts:1-11`).

**The basic automated loop is phase/slice/task oriented.** [high] The README's hierarchy is "Project -> Milestones -> Slices -> Tasks", and its loop is plan, execute, verify, complete, reassess, repeat (`README.md:281-303`). In source, the dev workflow engine wraps current auto-mode behind a workflow-engine interface, derives active milestone/slice/task state, resolves dispatch, and reconciles state (`src/resources/extensions/gsd/dev-workflow-engine.ts:1-109`).

**Auto-mode automates context loading and dispatch.** [high] README says auto-mode reads `.gsd/STATE.md`, determines the next unit, starts a fresh session for each unit, injects a focused prompt, waits for completion, rereads disk, and repeats (`README.md:305-329`). Source shows the startup path bootstraps an auto session, starts command polling, and begins `runAutoLoopWithUok` (`src/resources/extensions/gsd/auto.ts:1718-1769`). The loop itself is described as "derive -> dispatch -> guards -> runUnit -> finalize -> repeat" (`src/resources/extensions/gsd/auto/loop.ts:1-8`).

**Auto-mode includes guardrails and persisted runtime state.** [high] The loop persists stuck-loop state in `.gsd/runtime/stuck-state.json` and custom-verification retries in `.gsd/runtime/custom-verify-retries.json` (`src/resources/extensions/gsd/auto/loop.ts:44-141`). It also uses session locks, sidecar queues, dispatch guards, verification, and finalization logic around both custom and dev paths (`src/resources/extensions/gsd/auto/loop.ts:281-719`).

**Verification is automated after execution units, but not universally for every possible action.** [high] The post-unit verification module says it runs typecheck/lint/test commands, runtime error capture, dependency audits, optional auto-fix retries, and writes verification evidence JSON (`src/resources/extensions/gsd/auto-verification.ts:1-11`). Its main path only runs the standard gate for `execute-task`; validation milestones have a separate post-check path (`src/resources/extensions/gsd/auto-verification.ts:198-214`). That means the README-level claim that verification is automated is broadly supported, but the source shows it is scoped by unit type and policy. [medium-high]

**There are multiple workflow engines or dispatch shapes, not one single engine.** [high]

1. **Default/dev auto engine.** This appears to be the normal milestone/slice/task loop. The engine resolver maps `null` or `"dev"` to `DevWorkflowEngine` plus `DevExecutionPolicy` (`src/resources/extensions/gsd/engine-resolver.ts:1-56`). The dev engine derives state from GSD project files, resolves dispatch through auto-dispatch, and reconciles with the existing auto-mode path (`src/resources/extensions/gsd/dev-workflow-engine.ts:1-109`).

2. **Custom YAML graph engine.** A non-null engine name resolves to `CustomWorkflowEngine`, which expects an active run directory; the custom engine reads `GRAPH.yaml`, chooses the next eligible step, writes graph state, and reconciles completed/running steps back to disk (`src/resources/extensions/gsd/engine-resolver.ts:1-56`, `src/resources/extensions/gsd/custom-workflow-engine.ts:1-13`, `src/resources/extensions/gsd/custom-workflow-engine.ts:51-226`). It persists state in the workflow run directory rather than only the normal milestone/slice/task files. [high]

3. **Workflow-template/plugin dispatch modes.** Workflow templates declare one of `oneshot`, `yaml-step`, `markdown-phase`, or `auto-milestone` (`src/resources/extensions/gsd/workflow-templates.ts:28-32`). The workflow command handler dispatches those modes differently: `oneshot` calls one-shot dispatch, `yaml-step` creates a run and starts the custom engine, `markdown-phase` dispatches a markdown-phase plugin, and `auto-milestone` routes the user to `/gsd auto` or `/gsd start` behavior (`src/resources/extensions/gsd/commands/handlers/workflow.ts:165-222`). [high]

4. **UOK kernel wrapper.** Auto-mode is wrapped by a UOK scheduler/legacy contract layer. The UOK kernel labels paths as `uok-kernel`, `uok-legacy-wrapper`, or `uok-legacy-fallback`, writes parity events to `.gsd/runtime/uok-parity.jsonl`, and chooses kernel or legacy execution based on flags (`src/resources/extensions/gsd/uok/kernel.ts:45-117`). UOK flags default to enabled for several subfeatures unless fallback or overrides disable them (`src/resources/extensions/gsd/uok/flags.ts:4-39`). [medium-high] I read this as an execution wrapper/scheduler path around the loop, not as a separate user-facing workflow template.

**What is left manual?** [medium-high] Users still explicitly invoke start/control commands such as `/gsd auto`, `/gsd stop`, `/gsd pause`, `/gsd workflow start`, and workflow install/validate/list commands; source handlers route these commands rather than autonomously launching them without user command input (`src/resources/extensions/gsd/commands/handlers/auto.ts:45-154`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:65-85`). Some gates can pause or require correction rather than self-resolving everything; auto-verification can retry auto-fix but ultimately pauses on unresolved failure (`src/resources/extensions/gsd/auto-verification.ts:562-614`).

**Human-vs-machine distinction in automation.** [medium] I did not find a single source-level taxonomy that says "this engine is for humans" and "this engine is for machines." Instead, gsd-2 appears to distinguish command transports and runtime affordances: slash commands, headless CLI, RPC, MCP, and UI-aware behavior. Headless mode and MCP/RPC are explicit machine/external-client surfaces; slash commands and overlays are interactive surfaces. The automation engines themselves appear to be selected by workflow mode/state, not by whether a human or agent invoked them (`docs/user-docs/commands.md:279-372`, `packages/rpc-client/README.md:1-104`, `packages/mcp-server/README.md:1-12`, `packages/mcp-server/README.md:76-217`).

### Q3: What hooks does gsd-2 expose?

**gsd-2 exposes shell hooks configured in settings.** [high] The hooks docs say hooks are configured under `hooks` in `settings.json`; examples show `PreToolUse`, `PostToolUse`, and `Stop` entries with `command`, `match`, `timeout`, and `blocking` fields (`docs/user-docs/hooks.md:1-41`). The source settings type lists `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Notification`, `Stop`, `Blocked`, `SessionEnd`, `PreCommit`, `PostCommit`, `PrePush`, `PostPush`, `PrePR`, `PostPR`, `PreVerify`, `PostVerify`, `BudgetThreshold`, `MilestoneStart`, `MilestoneEnd`, `UnitStart`, `UnitEnd`, `PreCompact`, and `PostCompact` (`packages/pi-coding-agent/src/core/settings-manager.ts:119-149`).

**Shell hooks receive JSON on stdin and can block or modify action.** [high] The docs say hooks receive payload JSON on stdin and can emit JSON on stdout, including `allow`, `block`, and `modify` controls (`docs/user-docs/hooks.md:27-91`). Source implements collection from global and trusted project hooks, match filters over tool/command, command execution with `GSD_HOOK_EVENT` and `GSD_HOOK_SCOPE`, stdout JSON parsing, and blocking on non-zero exit when configured (`packages/pi-coding-agent/src/core/hooks-runner.ts:89-227`).

**Project hook execution has an explicit trust marker.** [high] Project hooks run only after the project has a `.pi/hooks.trusted` marker; global hooks always run. The docs present this as the trust boundary (`docs/user-docs/hooks.md:93-106`). Source likewise collects project hooks only when `hooks.trusted` is present and otherwise skips them (`packages/pi-coding-agent/src/core/hooks-runner.ts:89-105`).

**There is also an extension event/hook surface inside Pi/GSD.** [high] Extension context exposes subscription methods for events such as `session_start`, `session_switch`, `before_agent_start`, `agent_end`, `turn_end`, compaction, shutdown, tool call/result, model selection, provider request, and others (`packages/pi-coding-agent/src/core/extensions/types.ts:1293-1350`). The GSD extension registers many of those hooks: session start, before agent start, agent end, compaction checkpointing, tool-call guards, safety evidence, tool-result handling, discussion-log writes, and execution evidence (`src/resources/extensions/gsd/bootstrap/register-hooks.ts:65-607`).

**GSD-specific hook emission covers lifecycle, git, verification, budget, milestone, and unit events.** [high] `hook-emitter.ts` defines emission wrappers for notification, before/after commit, push, PR, verify, budget threshold, milestone start/end, and unit start/end (`src/resources/extensions/gsd/hook-emitter.ts:20-188`). The core hook runner provides corresponding handlers for those events plus compaction/session hooks (`packages/pi-coding-agent/src/core/hooks-runner.ts:297-459`).

**There is a post-unit/pre-dispatch rule-hook layer separate from shell hooks.** [medium-high] `post-unit-hooks.ts` is a facade over a rule registry and exposes `runPostUnitHooks`, `runPreDispatchHooks`, manual triggering, status, and state persistence (`src/resources/extensions/gsd/post-unit-hooks.ts:1-86`). I read this as a GSD-internal rule/hook layer used by auto-mode in addition to the general shell-hook runner. I did not read the full rule registry in this slice, so I am not characterizing all available built-in rules. [medium]

### Q4: What testing primitives exist?

**For users' projects, gsd-2 provides verification-command discovery and execution.** [high] `verification-gate.ts` says discovery order is preferences, task-plan verification commands, then package scripts (`src/resources/extensions/gsd/verification-gate.ts:1-4`). It recognizes `package.json` scripts such as `typecheck`, `lint`, and `test` (`src/resources/extensions/gsd/verification-gate.ts:39-47`), chooses the first non-empty configured source (`src/resources/extensions/gsd/verification-gate.ts:49-96`), sanitizes likely commands (`src/resources/extensions/gsd/verification-gate.ts:186-221`), and runs verification commands sequentially with structured results (`src/resources/extensions/gsd/verification-gate.ts:232-305`).

**Users can configure verification commands explicitly.** [high] Configuration docs expose `verification_commands`, including examples for npm, Python, Rust, and Go command sets (`docs/user-docs/configuration.md:404-420`). The same docs expose `reactive_execution`, `auto_supervisor`, UAT auto-dispatch, and skill discovery options near the verification settings (`docs/user-docs/configuration.md:316-402`).

**Post-unit verification includes runtime error and dependency checks, not just test commands.** [high] The verification gate scans background-shell/browser logs for recent runtime errors (`src/resources/extensions/gsd/verification-gate.ts:308-341`). Auto-verification also captures runtime errors and dependency-audit state, writes verification evidence JSON, emits verify-result events, and can invoke auto-fix retries before pausing on unresolved failures (`src/resources/extensions/gsd/auto-verification.ts:237-614`).

**Custom workflow steps can have custom verification policies.** [high] Custom verification supports `content-heuristic`, `shell-command`, `prompt-verify`, `human-review`, and no-policy cases (`src/resources/extensions/gsd/custom-verification.ts:1-18`). The content heuristic checks produced files, minimum sizes, required patterns, and path traversal; the shell-command policy runs a command with timeout and suspicious-command guards (`src/resources/extensions/gsd/custom-verification.ts:43-182`).

**There is a test-generation command for completed slices.** [medium-high] `commands-add-tests.ts` describes a command that generates tests for a completed slice using changed files, summaries, and detected test patterns (`src/resources/extensions/gsd/commands-add-tests.ts:1-6`). Source finds the last completed slice from `.gsd/.../SUMMARY.md`, detects local test patterns from config/test dirs/sample tests, and asks the agent to add tests (`src/resources/extensions/gsd/commands-add-tests.ts:17-137`). I did not trace whether this command is documented in the main command docs; it appears in the command catalog as `add-tests` (`src/resources/extensions/gsd/commands/catalog.ts:263-309`).

**gsd-2 itself is tested with npm scripts and CI jobs.** [high] `package.json` defines unit, integration, smoke, mutation, coverage, extension, hook, MCP, RPC, and PR-verification scripts (`package.json:63-76`, `package.json:93-101`). The CI build job runs core build, web build, extension typecheck, package validation, workspace coverage verification, unit tests, package tests, and coverage tests (`.github/workflows/ci.yml:134-187`). The integration job runs integration, hook, and smoke tests (`.github/workflows/ci.yml:189-229`). Contributing docs tell contributors to run `npm run verify:pr` and state that tests must execute code under test rather than merely grep source (`CONTRIBUTING.md:104`, `CONTRIBUTING.md:319-341`).

### Q5: Does gsd-2 distinguish user-facing from agent-facing surfaces?

**I did not find a single formal user-vs-agent taxonomy in source.** [medium-high] The command catalog, command docs, and handlers are organized by command purpose and transport rather than by "human-facing" versus "agent-facing" labels (`docs/user-docs/commands.md:1-380`, `src/resources/extensions/gsd/commands/catalog.ts:16-309`, `src/resources/extensions/gsd/commands/dispatcher.ts:10-23`).

**There is, however, a clear transport/runtime distinction.** [high] Human-interactive surfaces include slash commands, UI overlays, status widgets, visualizers, and session commands. Machine/external-client surfaces include headless CLI, deterministic `headless query`, RPC, and MCP. Headless docs explicitly target non-interactive mode (`docs/user-docs/commands.md:279-321`); `headless query` explicitly avoids LLM invocation (`src/headless-query.ts:1-10`); RPC exposes lifecycle, command, and event APIs for "external applications" (`packages/rpc-client/README.md:1-104`); MCP exposes project-state, session, prompt, shell, and workflow tools for MCP clients (`packages/mcp-server/README.md:1-12`, `packages/mcp-server/README.md:76-217`).

**Some commands adapt to UI availability rather than caller identity.** [high] `/gsd visualize` checks whether a UI is present and falls back to text status if not (`src/resources/extensions/gsd/commands/handlers/core.ts:179-201`). `/bg` similarly uses an overlay when UI is available and a text list otherwise (`src/resources/extensions/bg-shell/bg-shell-command.ts:52-73`). This suggests the user-facing/agent-facing distinction is often expressed as runtime capability (`hasUI`, headless, RPC, MCP) rather than a semantic split between humans and agents. [medium-high]

**Agent-facing surfaces are often files and prompts inside the work loop.** [medium-high] Auto-mode describes fresh-session dispatch with focused prompts and rereading disk state after agent completion (`src/resources/extensions/gsd/auto.ts:1-11`). The dev engine resolves dispatch from project state and the custom engine generates step prompts from `GRAPH.yaml` (`src/resources/extensions/gsd/dev-workflow-engine.ts:71-90`, `src/resources/extensions/gsd/custom-workflow-engine.ts:74-190`). I would characterize these as agent-facing execution surfaces, but gsd-2 source did not label them that way in the files I read. [medium]

## (iii) What I deliberately did NOT read

- I did not read `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`, `.planning/audits/archive/`, `.planning/gsd-2-uplift/INITIATIVE.md`, `.planning/gsd-2-uplift/DECISION-SPACE.md`, other orchestration files, `.planning/research/gemini-deep-research/`, or `.planning/deliberations/`.
- I did not read the slice 1 or slice 2 outputs: `.planning/gsd-2-uplift/exploration/01-mental-model-output.md` or `.planning/gsd-2-uplift/exploration/02-architecture-output.md`.
- I did not inspect release history, package distribution internals, migration artifacts, or full artifact-output surfaces except where commands and workflows required them.
- I did not read external RTK or Pi SDK repositories. I only used gsd-2 README/source/docs for this slice.
- I did not fully trace every command handler implementation. For Q1, I treated the command docs and command catalog as the exhaustive command surface, then sampled handlers for command behavior and artifacts where needed.

## (iv) Open questions surfaced

- **Command surface drift may be real.** [medium] Command definitions appear in docs, catalog, help text, lazy registration, handlers, and extension command modules. I saw enough duplicated command-surface material to suspect drift risk, but did not audit every command name against every handler. Relevant surfaces include the command docs (`docs/user-docs/commands.md:1-380`), command catalog (`src/resources/extensions/gsd/commands/catalog.ts:16-309`), and help handler (`src/resources/extensions/gsd/commands/handlers/core.ts:55-139`).

- **Workflow-engine boundaries deserve deeper reading.** [medium-high] The source clearly shows at least dev/default, custom YAML graph, workflow-template modes, and UOK wrapper paths (`src/resources/extensions/gsd/engine-resolver.ts:1-56`, `src/resources/extensions/gsd/workflow-templates.ts:28-32`, `src/resources/extensions/gsd/uok/kernel.ts:45-117`). I did not trace every persistence file, execution-policy decision, or migration path across those shapes. A second-wave reader should verify whether users experience these as coherent workflow variants or mostly as implementation layers behind `/gsd auto` and `/gsd workflow`.

- **Failure modes/debugging appear central enough for synthesis.** [high] The command surface includes `/gsd debug`, `/gsd forensics`, `/gsd doctor`, logs, stuck-state handling, and crash/recovery language (`docs/user-docs/commands.md:20-42`, `src/resources/extensions/gsd/auto/loop.ts:44-85`, `README.md:67-75`). This belongs on the cross-slice watchlist.

- **Telemetry/observability appear central enough for synthesis.** [high] README highlights worktree telemetry, forensics, cost and token tracking, budget intelligence, and history forensics (`README.md:32-38`, `README.md:73-75`). UOK writes parity events to `.gsd/runtime/uok-parity.jsonl` (`src/resources/extensions/gsd/uok/kernel.ts:52-117`). This belongs on the cross-slice watchlist.

- **Security/trust boundaries appear central enough for synthesis.** [high] Hook execution has a project trust marker (`docs/user-docs/hooks.md:93-106`, `packages/pi-coding-agent/src/core/hooks-runner.ts:89-105`). Tool-call hooks include state-write blocking, pending-gate checks, tool policy guards, and destructive-command warnings (`src/resources/extensions/gsd/bootstrap/register-hooks.ts:324-480`). This belongs on the cross-slice watchlist.

- **Multi-user/collaboration is present but not characterized here.** [medium] I saw team/worktree/parallel/remote/GitHub sync surfaces, but did not read enough to decide whether gsd-2 has true multi-user collaboration semantics or mostly orchestration around branches, issues, and remote approvals (`docs/user-docs/commands.md:76-87`, `docs/user-docs/commands.md:180-227`). This should be checked by synthesis if collaboration is load-bearing.

- **Direction-shifting evidence:** gsd-2's workflow surface appears broader than "a project-planning CLI." [medium-high] It exposes interactive commands, auto-mode, custom workflow templates, hooks, verification gates, headless/RPC/MCP transports, worktree isolation, remote control, and observability surfaces. If the dispatching project's characterization aim assumes a single narrow workflow layer, that aim may be under-shaped; the source suggests several overlapping runtime and automation surfaces that need to be separated before deciding whether to proceed.

## (v) Flags where README claims diverge from source observations

- **RTK default posture appears overstated in README.** README says GSD "now provisions a managed RTK runtime" and uses it in `bash`, `async_bash`, `bg_shell`, and verification flows (`README.md:22`). Source shows RTK bootstrap is skipped when `GSD_RTK_DISABLED` is set and otherwise requires `config.experimental.rtk` to be truthy; if the flag is absent, the bootstrap returns without provisioning (`src/cli.ts:160-178`). I read this as a README/source divergence unless `experimental.rtk` is enabled by default elsewhere that I did not inspect. [medium-high]

- **Automated verification is real, but README-level phrasing is broader than the source path I read.** README presents v2 as having "automated verification commands with retry/fix loops" (`README.md:250`) and describes the loop as verify-after-execute (`README.md:293-303`). Source supports automated verification and retry/fix behavior, but standard post-unit verification is explicitly scoped to `execute-task` units, with separate behavior for validation milestones and advisory handling for package/infra failures (`src/resources/extensions/gsd/auto-verification.ts:198-214`, `src/resources/extensions/gsd/auto-verification.ts:355-372`, `src/resources/extensions/gsd/auto-verification.ts:562-614`). I treat this as a scope narrowing rather than a hard contradiction. [high]

- **Roadmap reassessment docs appear potentially tensioned.** README presents reassessment as part of the automatic loop after completion (`README.md:293-303`), while configuration docs say slice-level reassessment requires `reassess_after_slice: true` and otherwise is skipped regardless of `skip_reassess` (`docs/user-docs/configuration.md:301-314`). I did not trace the current reassessment source in this slice, so this is a documentation tension to verify, not a confirmed source divergence. [medium]
