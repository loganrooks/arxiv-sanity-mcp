---
type: w2-deep-dive
date: 2026-04-27
target: gsd-2 markdown-phase workflow engine
agent: codex GPT-5.5 medium (exploration mode)
status: complete
parent_probe: .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md
---

# W2 dive - markdown-phase workflow engine

## §0. Dive summary

Top-line: gsd-2's `markdown-phase` path appears to be a prompt-dispatch workflow with startup scaffolding, not a deterministic phase executor. **Confidence: high.**

Observed-in-source: `/gsd start` resolves a template, optionally creates an artifact directory, optionally creates a git branch, writes initial `STATE.json`, builds a `workflow-start` prompt with the raw markdown template, and sends it to the agent (`src/resources/extensions/gsd/commands-workflow-templates.ts:424-508`). The prompt tells the agent to follow phases and write artifacts (`src/resources/extensions/gsd/prompts/workflow-start.md:15-28`).

The executor does **not** appear to parse markdown command blocks and run them. Commands in `release.md` are instructions to the agent, not executor-owned shell steps. **Confidence: high.** The only deterministic shell execution I observed belongs to the separate `yaml-step` custom workflow verification policy, where `shell-command` verification runs through `spawnSync("sh", ["-c", ...])` (`src/resources/extensions/gsd/custom-verification.ts:144-182`).

State persistence differs by mode. `markdown-phase` writes a lightweight `STATE.json` under the artifact directory, but I did not observe source that advances phase status after each phase. `yaml-step` writes `.gsd/workflow-runs/<name>/<timestamp>/DEFINITION.yaml`, `GRAPH.yaml`, and optional `PARAMS.json`, then advances steps by mutating `GRAPH.yaml` (`src/resources/extensions/gsd/run-manager.ts:1-14`, `src/resources/extensions/gsd/custom-workflow-engine.ts:51-72`, `src/resources/extensions/gsd/custom-workflow-engine.ts:192-226`).

Programmatic invocation of GSD operations from markdown-phase templates appears unverified/refuted for direct execution: the template can ask the agent to run commands, but I did not observe an API where markdown phases call `/gsd pr-branch`, semver scripts, or other GSD tools directly. **Confidence: medium-high.**

## §1. State persistence

**Observed-in-source: markdown-phase state is `STATE.json` in the workflow artifact directory, if the template declares one.** The registry declares `release` as `mode: "markdown-phase"` with `artifact_dir: ".gsd/workflows/releases/"` and phases `prepare`, `bump`, `publish`, `announce` (`src/resources/extensions/gsd/workflow-templates/registry.json:213-220`). Startup creates a dated, numbered, slugged child directory under that artifact root (`src/resources/extensions/gsd/commands-workflow-templates.ts:424-432`), then writes state into that directory (`src/resources/extensions/gsd/commands-workflow-templates.ts:464-475`).

**Observed schema:** `WorkflowState` has `template`, `templateName`, `description`, `branch`, `phases`, `currentPhase`, `startedAt`, `updatedAt`, optional `completedAt`, and `artifactDir` (`src/resources/extensions/gsd/commands-workflow-templates.ts:74-93`). Each phase has `name`, `index`, and `status`, where status is only `"pending" | "active" | "completed"` (`src/resources/extensions/gsd/commands-workflow-templates.ts:76-80`). Initial write sets phase 0 active, other phases pending, `currentPhase: 0`, and timestamps (`src/resources/extensions/gsd/commands-workflow-templates.ts:106-122`).

**What survives restart:** `/gsd start resume` scans `.gsd/workflows/*/*/STATE.json`, parses each state file, and treats workflows without `completedAt` as in-progress (`src/resources/extensions/gsd/commands-workflow-templates.ts:126-159`). Resume chooses the most recently updated in-progress workflow, reports completed count/current active phase/branch/artifact path, reloads the template, and sends a resume-flavored `workflow-start` prompt (`src/resources/extensions/gsd/commands-workflow-templates.ts:196-245`).

**Important limit:** I did not observe source that updates `currentPhase`, changes a phase from active to completed, sets the next phase active, or writes `completedAt` for markdown-phase workflows. The inspected file defines initial state write and resume scanning, but the write helper is used at startup/plugin dispatch only (`src/resources/extensions/gsd/commands-workflow-templates.ts:466-475`, `src/resources/extensions/gsd/commands-workflow-templates.ts:632-642`). **Confidence: medium-high; this is an absence claim bounded to inspected workflow files and targeted search.**

**Can a later phase read prior phase state/artifacts?** There is no observed engine-mediated phase context injection for markdown-phase. The agent receives the artifact directory and execution rule "write all planning/summary documents there" (`src/resources/extensions/gsd/prompts/workflow-start.md:21-28`), so a later agent turn can read earlier files if it chooses. This is agent/file-system continuity, not a structured executor state handoff. **Confidence: high for prompt semantics; medium for actual agent behavior.**

## §2. Deterministic shell command execution

**Markdown-phase answer: prompt-only for command execution.** The startup path loads raw workflow markdown (`loadWorkflowTemplate` reads the template file and returns text; `src/resources/extensions/gsd/workflow-templates.ts:257-268`), injects it into `workflow-start`, and sends the resulting prompt to the agent via `pi.sendMessage` (`src/resources/extensions/gsd/commands-workflow-templates.ts:487-508`). The prompt says "Follow the workflow defined below" and "Execute each phase in order" (`src/resources/extensions/gsd/prompts/workflow-start.md:15-18`), but it does not describe a parser/executor for markdown code blocks.

**Release template commands are instructions, not executor steps.** `release.md` contains inline and fenced shell commands such as `git log <last_tag>..HEAD --oneline --no-merges`, `git status`, `git tag -a`, and `git push` (`src/resources/extensions/gsd/workflow-templates/release.md:31-40`, `src/resources/extensions/gsd/workflow-templates/release.md:64-86`). The markdown-phase dispatcher does not parse those blocks; it passes the whole template body into the prompt (`src/resources/extensions/gsd/commands-workflow-templates.ts:487-508`). **Confidence: high.**

**Separate yaml-step behavior:** `yaml-step` workflows can perform deterministic shell verification, not arbitrary command-step execution. The definition schema includes a `verify` union with `shell-command` (`src/resources/extensions/gsd/definition-loader.ts:22-26`), validates that shell-command has a non-empty command (`src/resources/extensions/gsd/definition-loader.ts:192-209`), and `custom-verification.ts` runs it via `spawnSync("sh", ["-c", rewrittenCommand])` in the run directory with a 30s timeout (`src/resources/extensions/gsd/custom-verification.ts:144-182`). Example: `test-backfill.yaml` sets `verify.policy: shell-command` and `command: "{{test_command}}"` (`src/resources/extensions/gsd/workflow-templates/test-backfill.yaml:56-58`).

**Calibration:** If "execute deterministic shell commands directly" means "the workflow engine parses markdown command blocks and runs them," the answer is **no observed support / effectively refuted for markdown-phase**. If it means "some workflow mode can run a configured shell command as verification," the answer is **yes for yaml-step verification only**. **Confidence: high.**

## §3. Artifact writes

**Where `PREPARE.md` and `RELEASE.md` come from:** they come from `release.md` instructions to the agent. Phase 1 says "Write `PREPARE.md` in the artifact directory" with proposed version, commit summary, and concerns (`src/resources/extensions/gsd/workflow-templates/release.md:42-48`). Phase 4 says "Write `RELEASE.md` in the artifact dir" with what shipped, links, and follow-ups (`src/resources/extensions/gsd/workflow-templates/release.md:113-116`).

**Executor writes:** for markdown-phase, the observed executor writes the artifact directory and `STATE.json`; it does not write `PREPARE.md`, `RELEASE.md`, changelog entries, or release notes. Directory creation is `mkdirSync(join(basePath, artifactDir), { recursive: true })` (`src/resources/extensions/gsd/commands-workflow-templates.ts:426-432`). State creation is `writeFileSync(statePath, JSON.stringify(state, null, 2) + "\n")` (`src/resources/extensions/gsd/commands-workflow-templates.ts:106-122`).

**Prompt-level artifact discipline:** `workflow-start` tells the agent: "If an artifact directory is specified, write all planning/summary documents there" (`src/resources/extensions/gsd/prompts/workflow-start.md:21-25`). That is an instruction to the agent, not a structured writer.

**Artifact write semantics:** for `STATE.json`, startup is overwrite semantics through `writeFileSync` to a fixed `STATE.json` path inside a newly created run directory (`src/resources/extensions/gsd/commands-workflow-templates.ts:106-122`). For `PREPARE.md`, `RELEASE.md`, and similar template-named artifacts, I observed no structured fields, append mode, or overwrite policy in executor source. Semantics appear freeform Markdown as written by the agent from the template. **Confidence: high for executor state write; medium-high for absence of structured markdown artifact writer.**

## §4. Phase lifecycle

**Markdown-phase explicit phase states:** the typed state only permits `"pending"`, `"active"`, and `"completed"` (`src/resources/extensions/gsd/commands-workflow-templates.ts:76-80`). It also has `completedAt`, but no typed `failed`, `paused`, or `retried` phase status (`src/resources/extensions/gsd/commands-workflow-templates.ts:82-93`).

**Markdown-phase completion/advance:** I did not observe executor code that marks a markdown phase complete or advances `currentPhase`. The prompt says to execute phases in order and summarize after each phase; low/medium complexity workflows keep moving by default, while high complexity workflows confirm at phase transitions (`src/resources/extensions/gsd/prompts/workflow-start.md:15-28`). That makes phase completion primarily an agent/prompt convention, not an engine state-machine transition. **Confidence: medium-high.**

**Markdown-phase pause/resume:** there is a resume mechanism based on `STATE.json`: `/gsd start resume` finds in-progress workflow states and resends a resume prompt (`src/resources/extensions/gsd/commands-workflow-templates.ts:196-245`). Because I did not observe phase advancement writes, resumed phase accuracy depends on whether something updated `STATE.json`; source-observed startup alone leaves phase 0 active. **Confidence: medium-high.**

**Markdown-phase retry/failure:** no explicit markdown-phase retry or failed states observed. The template may tell the agent to fix failures, and general agent/tool behavior may retry operationally, but the markdown-phase state schema does not encode failed/retried. **Confidence: medium-high.**

**yaml-step lifecycle for contrast:** `GRAPH.yaml` step status is `"pending" | "active" | "complete" | "expanded"` (`src/resources/extensions/gsd/graph.ts:25-42`). `resolveDispatch` reuses an already active step, otherwise marks the next dependency-satisfied pending step active and writes `GRAPH.yaml` before dispatch (`src/resources/extensions/gsd/custom-workflow-engine.ts:96-189`). `reconcile` re-reads `GRAPH.yaml`, marks the completed step complete, writes it back, and returns `milestone-complete` if all steps are complete/expanded, otherwise `continue` (`src/resources/extensions/gsd/custom-workflow-engine.ts:192-226`).

**yaml-step pause/resume/retry:** `/gsd workflow pause` pauses a running custom workflow via `pauseAuto`; `/gsd workflow resume` starts auto again (`src/resources/extensions/gsd/commands/handlers/workflow.ts:448-473`). Pause persists `activeEngineId` and `activeRunDir` in `.gsd/runtime/paused-session.json` (`src/resources/extensions/gsd/auto.ts:1152-1175`), and fresh start restores custom workflow engine state from that metadata (`src/resources/extensions/gsd/auto.ts:1456-1479`). Default custom recovery is `retry` (`src/resources/extensions/gsd/custom-execution-policy.ts:57-64`), and shell-command verification returns `retry` on nonzero/timeout (`src/resources/extensions/gsd/custom-verification.ts:144-182`).

## §5. Programmatic invocation of GSD operations

**Markdown-phase:** I did not observe a mechanism for markdown-phase templates to programmatically invoke other GSD operations. The dispatcher does some built-in operations itself: artifact directory creation, branch creation unless isolation is none, an auto-commit attempt before branch switch, and prompt dispatch (`src/resources/extensions/gsd/commands-workflow-templates.ts:424-508`). After that, the markdown content is agent instructions.

**Example of prompt-mediated operation:** `full-project` is special-cased; when `.gsd/` is absent, startup sends a prompt telling the agent to run `/gsd init` and then `/gsd auto` (`src/resources/extensions/gsd/commands-workflow-templates.ts:397-421`). This is still natural-language/agent-mediated, not a direct call into the init/auto handlers.

**Release/hotfix implications:** `release.md` can instruct the agent to run semver, git, tag, push, publish, and `gh release create` operations (`src/resources/extensions/gsd/workflow-templates/release.md:54-76`, `src/resources/extensions/gsd/workflow-templates/release.md:82-103`). `hotfix.md` can instruct the agent to commit, test, push, and create a PR (`src/resources/extensions/gsd/workflow-templates/hotfix.md:24-45`). I did not observe markdown-phase APIs for directly invoking `pr-branch` cherry-pick/backport logic or semver scripts. **Confidence: medium-high.**

**yaml-step:** yaml-step can programmatically execute shell-command verification, but step bodies remain prompts to the agent. The graph dispatch contract is `unitType`, `unitId`, and `prompt` (`src/resources/extensions/gsd/engine-types.ts:20-25`), and custom engine dispatch returns a prompt for a `custom-step` (`src/resources/extensions/gsd/custom-workflow-engine.ts:181-188`). **Confidence: high.**

## §6. Artifact references to milestone state

**Markdown-phase structured cross-reference mechanism:** I did not observe structured milestone/slice/task reference fields in markdown-phase `STATE.json`. Its schema tracks template metadata, description, branch, phase list, current phase, timestamps, and artifact dir (`src/resources/extensions/gsd/commands-workflow-templates.ts:82-93`).

**Template-level prose references:** `release.md` includes optional follow-up "Close any milestone linked to this release" (`src/resources/extensions/gsd/workflow-templates/release.md:108-112`) and asks `RELEASE.md` to capture links to release, changelog, and PRs (`src/resources/extensions/gsd/workflow-templates/release.md:113-116`). This supports prose/Markdown links, not an observed structured cross-reference mechanism. **Confidence: high.**

**yaml-step structured references are internal to workflow steps:** YAML definitions support `requires`, `produces`, `context_from`, `verify`, and `iterate` fields (`src/resources/extensions/gsd/definition-loader.ts:35-52`). `context_from` injects prior step artifacts into a later step's prompt by reading produced files from the run directory (`src/resources/extensions/gsd/context-injector.ts:24-100`). This is a structured step-artifact reference mechanism, but it is scoped to workflow step IDs/artifacts, not milestone IDs/slice IDs/task IDs. **Confidence: high.**

## §7. markdown-phase vs yaml-step distinction

**User-facing docs distinction:** docs describe `markdown-phase` as "Multi-phase with STATE.json + phase-approval gates" and `yaml-step` as "Full engine with GRAPH.yaml, iterate, and shell-verify" (`docs/user-docs/commands.md:98-109`). Bundled plugin docs list release/performance/etc. as `markdown-phase` and test-backfill/docs-sync/rename-symbol/env-audit as `yaml-step` (`docs/user-docs/commands.md:136-146`).

**Source distinction:** plugin discovery treats markdown files as markdown-phase by default and parses `<template_meta>` plus `<phases>` from the markdown body (`src/resources/extensions/gsd/workflow-plugins.ts:80-162`). YAML plugins are parsed from YAML and default to `yaml-step`, with phases derived from step IDs (`src/resources/extensions/gsd/workflow-plugins.ts:164-216`).

**Execution distinction:** markdown-phase dispatch creates optional artifact dir/branch/state and sends a `workflow-start` prompt (`src/resources/extensions/gsd/commands-workflow-templates.ts:556-670`). yaml-step dispatch creates `.gsd/workflow-runs/<name>/<timestamp>/`, freezes `DEFINITION.yaml`, initializes `GRAPH.yaml`, optionally writes `PARAMS.json`, sets active engine/run dir, and starts auto mode (`src/resources/extensions/gsd/run-manager.ts:1-14`, `src/resources/extensions/gsd/run-manager.ts:119-155`, `src/resources/extensions/gsd/commands/handlers/workflow.ts:181-197`).

**When each appears intended:** markdown-phase is for phased, human-readable procedural workflows with approval gates and agent-authored artifacts, such as release and performance audit. yaml-step is for graph-backed, resumable, dependency/iteration-oriented batch workflows with machine-checkable verification, such as test backfill and docs sync. **Confidence: high, sourced from docs plus source behavior.**

## §8. Implications for W1 §C candidates

- **§C.1 (release metadata linked to milestones): partially verified.** W1 assumed a workflow template can write a release artifact that references milestone IDs without changing the core milestone schema (`.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md:278-286`). This dive verifies that release artifacts can be agent-written under `.gsd/workflows/releases/...` (§1, §3), and that markdown/prose links to milestones are plausible (§6). It does **not** verify a structured cross-reference mechanism; markdown-phase `STATE.json` has no milestone/slice/task fields (§6). Verdict: viable as prose/Markdown artifact; unverified/refuted as structured linkage without additional schema.

- **§C.2 (semver-aware release workflow plugin): partially verified / deterministic-command assumption refuted for markdown-phase.** W1 assumed markdown-phase workflows can execute deterministic shell steps or prompt agents to run scripts (`.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md:288-296`). This dive refutes deterministic markdown command execution by the executor (§2). The existing release markdown can prompt an agent to run semver/git/changelog operations (§2, §5), and yaml-step can run deterministic shell verification (§2, §7), but markdown-phase itself is not a direct shell-step engine. Verdict: viable as agent-prompted workflow; not verified as deterministic executor-owned semver workflow unless recast to yaml-step or separate code.

- **§C.3 (hotfix branch/backport workflow plugin): partially verified / programmatic backport invocation unverified.** W1 assumed templates can own branch naming and cherry-pick/backport instructions without core git-service additions (`.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md:298-305`). This dive verifies markdown-phase startup can create a `gsd/<template>/<slug>` branch (§5) and hotfix can prompt the agent to test/commit/push/PR (§5). It does not verify that hotfix can programmatically call `pr-branch` cherry-pick/backport code (§5). Verdict: viable for prompt-mediated hotfix procedure; unverified/refuted for direct programmatic cherry-pick/backport invocation from markdown.

- **§C.4 (RC/staging workflow template): partially verified.** W1 assumed RC/staging can be represented as phased procedural state and that phase state may persist soak metadata (`.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md:308-316`). This dive verifies markdown-phase can represent phased procedural instructions and write agent-authored artifacts (§1, §3, §7). It weakens the phase-state assumption: `STATE.json` exists, but source-observed markdown-phase state does not appear to advance phases or carry structured soak metadata (§1, §4). Verdict: viable as prompt/artifact workflow; still unverified for durable structured RC/soak state without adding conventions or using yaml-step/custom state.

## §9. Open questions / dive limits

- I did not run gsd-2 or execute a sample markdown-phase workflow; findings are source-observed only.
- I did not inspect full auto-loop internals beyond custom workflow pause/resume and policy touchpoints. That was enough to distinguish markdown-phase from yaml-step, but not enough to characterize every auto-loop retry edge.
- I did not inspect `commands-pr-branch.ts` in this W2 dive because the question was whether markdown-phase workflows can invoke it programmatically. The inspected workflow dispatch path did not expose such invocation.
- I did not inspect all bundled markdown templates. I focused on `release.md`, `hotfix.md`, registry, plugin discovery, dispatch, prompts, and yaml-step contrast files.
- Absence claims are bounded: "I did not observe" means not found in the allowed focused source paths and targeted searches, not a proof over every repository file.

## §10. Self-disclosure

Read from dispatching project: W1 `capabilities-production-fit-findings.md` for §C assumptions and light orientation from `01-mental-model-output.md`.

Read from gsd-2 source: `workflow-templates.ts`, `workflow-templates/registry.json`, `workflow-templates/release.md`, `workflow-templates/hotfix.md`, `workflow-templates/test-backfill.yaml`, `workflow-templates/docs-sync.yaml`, `commands-workflow-templates.ts`, `workflow-dispatch.ts`, `workflow-plugins.ts`, `commands/handlers/workflow.ts`, `run-manager.ts`, `workflow-engine.ts`, `custom-workflow-engine.ts`, `custom-execution-policy.ts`, `custom-verification.ts`, `definition-loader.ts`, `graph.ts`, `context-injector.ts`, `engine-types.ts`, selected `auto.ts` pause/resume spans, `interrupted-session.ts`, and `docs/user-docs/commands.md`.

Skipped per prompt: `.planning/audits/`, `INITIATIVE.md`, `DECISION-SPACE.md`, orchestration directory, `.planning/research/`, `.planning/deliberations/`, and other slice outputs/audits beyond the allowed W1/pilot files.

Discipline: I separated docs-stated claims from source-observed behavior where they diverge or differ in confidence. The key high-confidence source observation is that markdown-phase dispatch sends prompt content to the agent, while yaml-step is the graph-backed engine with deterministic verification hooks.
