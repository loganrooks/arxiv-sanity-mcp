---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 02 extension-workflow
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 02 — Extension / Workflow

## 0. Scout Summary

- Source supports the current-artifact claim that "extension surface" is plural: I found standard Pi extensions, GSD ecosystem extensions, workflow plugins/templates, skills, shell hooks, and GSD post-unit/pre-dispatch hooks.
- Pi coding-agent extensions and GSD ecosystem extensions appear source-distinct: Pi uses `ExtensionAPI` and extension entry discovery/registry paths; GSD ecosystem extensions load project `.gsd/extensions/` through a `GSDExtensionAPI` wrapper and separate trust/ready handling.
- Workflow plugins are distinct from extension APIs and skills: they are markdown/YAML files discovered from bundled/global/project directories, grouped by modes, and dispatched through `/gsd workflow` handlers.
- `markdown-phase` and `yaml-step` are mechanically different in source. `markdown-phase` writes startup `STATE.json`/artifact/branch scaffolding and sends a prompt; `yaml-step` creates a run and drives `GRAPH.yaml` through `CustomWorkflowEngine`.
- Source supports the W2 claim that deterministic shell execution is not observed for markdown-phase executor-owned steps; deterministic shell execution appears in custom workflow verification for trusted YAML definitions.
- Skills have both Pi-level discovery (`packages/pi-coding-agent/src/core/skills.ts`) and GSD per-unit manifest/filtering/discovery surfaces (`skill-discovery.ts`, `skill-manifest.ts`).
- Hook/trust boundaries are not incidental: project ecosystem extensions are trust-gated; shell hooks use a trust marker; custom shell-command verification explicitly names the workflow-definition author as the trust boundary.
- Fresh delta around `src/resources/extensions/claude-code-cli/stream-adapter.ts` looks relevant to provider/tool-execution and permission behavior: current source defaults permission mode to `bypassPermissions`, auto-approves headless tool requests, preserves SDK tool-call/result blocks, and distinguishes abort from stream exhaustion. I did not adjudicate whether this changes uplift viability.
- Claims mapping four extension surfaces to R-strategy viability are not mechanical; they should remain high-adjudication synthesis claims.

## 1. Source Paths Inspected

- `src/extension-discovery.ts` — Pi extension entry discovery, package `pi.extensions`, fallback `index.ts`/`index.js`, installed-over-bundled shadowing.
- `src/extension-registry.ts` — extension manifest and registry shape, enable/disable semantics, manifest discovery.
- `src/resource-loader.ts` — bundled resource/extension sync and managed-resource manifest.
- `packages/pi-coding-agent/src/core/extensions/types.ts` — `ExtensionAPI` event and registration surface.
- `src/resources/extensions/gsd/ecosystem/loader.ts` — GSD ecosystem extension loader for `.gsd/extensions/`, trust gate, import path checks.
- `src/resources/extensions/gsd/ecosystem/gsd-extension-api.ts` — `GSDExtensionAPI` wrapper, `before_agent_start` interception, `getPhase`/`getActiveUnit`.
- `src/resources/extensions/gsd/bootstrap/register-extension.ts` and `bootstrap/register-hooks.ts` — GSD extension bootstrap and ecosystem handler chaining.
- `src/resources/extensions/gsd/workflow-plugins.ts` — workflow plugin discovery, modes, three-tier precedence, formatting.
- `src/resources/extensions/gsd/commands/handlers/workflow.ts` — mode-specific workflow dispatch.
- `src/resources/extensions/gsd/workflow-dispatch.ts` and `commands-workflow-templates.ts` — oneshot/markdown-phase prompt dispatch, `STATE.json`, artifact directory, branch creation.
- `src/resources/extensions/gsd/definition-loader.ts`, `custom-workflow-engine.ts`, `graph.ts`, `run-manager.ts`, `custom-verification.ts` — YAML definition parsing, `GRAPH.yaml` engine state, dependency/context behavior, shell-command verification.
- `src/resources/extensions/gsd/skill-discovery.ts`, `skill-manifest.ts`, `skill-catalog.ts`, `skill-health.ts` — GSD skill discovery, per-unit allowlists, health/introspection.
- `packages/pi-coding-agent/src/core/skills.ts` — Pi/agent skill discovery and validation rules.
- `src/resources/extensions/gsd/rule-registry.ts`, `post-unit-hooks.ts`, `preferences-types.ts` — GSD post-unit/pre-dispatch hook/rule surface.
- `packages/pi-coding-agent/src/core/settings-manager.ts`, `hooks-runner.ts` — Pi shell hook settings and trust/run behavior, sampled through rg and prior artifact claims.
- `src/resources/extensions/claude-code-cli/stream-adapter.ts`, `partial-builder.ts`, related tests by rg — Claude Code provider stream, permission, tool-call/result adaptation.
- Current artifacts read after source inventory: `03-workflow-surface-output.md`, `04-artifact-lifecycle-output.md`, `04-artifact-lifecycle-audit.md`, `w2-markdown-phase-engine-findings.md`, and extension/workflow/skills/hooks sections of `SYNTHESIS.md`.

## 2. Mechanism Inventory

1. **Pi coding-agent extensions**
   - Source path: `src/extension-discovery.ts`, `src/extension-registry.ts`, `packages/pi-coding-agent/src/core/extensions/types.ts`.
   - Role: code extension modules with manifests/registry metadata and an activation function receiving `ExtensionAPI`.
   - Evidence: `resolveExtensionEntries()` treats a package `pi` manifest as authoritative and otherwise falls back to index files (`src/extension-discovery.ts:9-17`, `18-52`); `ExtensionManifest` includes `provides` and `dependencies` (`src/extension-registry.ts:15-32`); `ExtensionAPI` includes event subscriptions and registration surfaces (`packages/pi-coding-agent/src/core/extensions/types.ts:1288-1350`).
   - Distinct/overlap: distinct API/runtime substrate; GSD itself builds on it.

2. **GSD ecosystem extensions**
   - Source path: `src/resources/extensions/gsd/ecosystem/loader.ts`, `gsd-extension-api.ts`, `bootstrap/register-hooks.ts`.
   - Role: project-local `.gsd/extensions/*.js|*.ts` extensions with GSD state context.
   - Evidence: loader says it discovers `.gsd/extensions/` and is isolated from Pi's loader chain (`loader.ts:1-4`); it trust-gates project loading (`loader.ts:85-95`), rejects realpath escapes (`loader.ts:140-158`), and passes a `GSDExtensionAPI` to default exports (`loader.ts:123-129`, `187-195`). Wrapper adds `getPhase`/`getActiveUnit` and intercepts `before_agent_start` (`gsd-extension-api.ts:40-45`, `144-156`, `224-227`).
   - Distinct/overlap: distinct from Pi extension loader, but delegates most methods back to Pi's `ExtensionAPI`.

3. **Workflow plugins/templates**
   - Source path: `src/resources/extensions/gsd/workflow-plugins.ts`, `workflow-templates.ts`, `commands/handlers/workflow.ts`, `commands-workflow-templates.ts`.
   - Role: markdown/YAML workflow definitions with discovery/dispatch modes.
   - Evidence: source enumerates `oneshot`, `yaml-step`, `markdown-phase`, `auto-milestone` modes (`workflow-plugins.ts:1-13`, `120-122`); project/global/legacy/bundled discovery is implemented (`workflow-plugins.ts:290-304`); dispatch branches by mode (`commands/handlers/workflow.ts:165-222`).
   - Distinct/overlap: distinct from code extensions and skills; runs through GSD command handlers and workflow engines.

4. **Markdown-phase workflow mode**
   - Source path: `workflow-dispatch.ts`, `commands-workflow-templates.ts`, markdown templates.
   - Role: phased prompt-dispatch workflow with artifact/branch/state scaffolding.
   - Evidence: `dispatchMarkdownPhase` builds a `workflow-start` prompt and calls `pi.sendMessage` (`workflow-dispatch.ts:78-105`); `dispatchMarkdownPhasePlugin` reads template markdown, may create artifact dir/branch, writes `STATE.json`, then notifies/sends prompt (`commands-workflow-templates.ts:558-650`).
   - Distinct/overlap: mechanically separate from `yaml-step`; executor-owned phase advancement was not observed in inspected paths.

5. **YAML-step custom workflow mode**
   - Source path: `definition-loader.ts`, `run-manager.ts`, `custom-workflow-engine.ts`, `custom-verification.ts`.
   - Role: graph-backed workflow run using frozen definitions and `GRAPH.yaml`.
   - Evidence: YAML schema uses `depends_on`, `context_from`, `verify`, and `iterate` (`definition-loader.ts:1-14`, `35-52`, `376-390`); `CustomWorkflowEngine` reads/writes `GRAPH.yaml`, dispatches eligible steps, and reconciles completion (`custom-workflow-engine.ts:1-13`, `51-72`, `90-115`, `192-215`); shell-command verification uses `spawnSync` with a trust warning (`custom-verification.ts:1-18`, `145-175`).
   - Distinct/overlap: same workflow plugin family as markdown-phase, different state/execution semantics.

6. **Skills**
   - Source path: `packages/pi-coding-agent/src/core/skills.ts`, `src/resources/extensions/gsd/skill-discovery.ts`, `skill-manifest.ts`.
   - Role: `SKILL.md` instruction bundles discovered from global/project/bundled directories, then filtered or surfaced to the model.
   - Evidence: Pi skills define ecosystem and project directories and validate frontmatter/name/description (`packages/pi-coding-agent/src/core/skills.ts:10-20`, `81-100`, `108-167`); GSD skill discovery watches `~/.agents/skills` and `~/.claude/skills` and formats newly discovered skills for prompt injection (`skill-discovery.ts:15-23`, `53-97`, `120-149`); per-unit manifests filter skills by unit type (`skill-manifest.ts:1-16`, `25-33`, `131-150`).
   - Distinct/overlap: distinct from workflow plugins and extensions; can influence agent behavior but is not code execution by itself.

7. **Hooks and rule hooks**
   - Source path: `packages/pi-coding-agent/src/core/settings-manager.ts`, `hooks-runner.ts`, `src/resources/extensions/gsd/rule-registry.ts`, `types.ts`.
   - Role: shell hooks plus GSD pre-dispatch/post-unit hook rules.
   - Evidence: GSD hook types include post-unit hook fields such as `after`, `prompt`, `max_cycles`, `artifact`, and `retry_on` (`types.ts:271-292`); `RuleRegistry` evaluates post-unit hooks with hook-on-hook prevention and configured trigger unit types (`rule-registry.ts:148-180`) and pre-dispatch hooks with modify/skip semantics (`rule-registry.ts:273-310`).
   - Distinct/overlap: shell hooks are Pi/runtime settings; GSD rule hooks are workflow/auto-mode prompt-dispatch logic.

8. **Claude Code CLI provider extension**
   - Source path: `src/resources/extensions/claude-code-cli/index.ts`, `stream-adapter.ts`, `partial-builder.ts`.
   - Role: provider integration that adapts Claude Agent SDK messages, tool calls/results, permission mode, and elicitation/UI.
   - Evidence: stream adapter resolves permission mode, sets tool allowlists/MCP wildcard entries, distinguishes abort from stream exhaustion, preserves tool-call blocks and SDK external results (`stream-adapter.ts:1173-1232`, `1272-1335`, `1453-1580`, `1588-1850`); partial builder maps SDK stream events to GSD deltas and strips MCP tool prefixes for renderer matching (`partial-builder.ts:26-63`, `166-300`).
   - Distinct/overlap: provider-extension surface, not a workflow system, but load-bearing for workflow automation when Claude Code is the model backend.

## 3. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|
| There are at least four extension-adjacent subsystems. | `SYNTHESIS.md` F2/§1.3; `04-artifact-lifecycle-output.md` addendum | Pi extensions (`extension-discovery.ts:9-17`, `extension-registry.ts:15-32`); GSD ecosystem extensions (`ecosystem/loader.ts:1-4`, `gsd-extension-api.ts:40-45`); workflow plugins (`workflow-plugins.ts:1-13`); skills (`skill-discovery.ts:15-23`, `skill-manifest.ts:1-16`). | Confirmed as a source inventory claim. Whether all count as "extensions" semantically is interpretive. | Yes, for semantic mapping and R-strategy implications. |
| Pi coding-agent extensions and GSD ecosystem extensions are distinct. | `SYNTHESIS.md` §1.3; `04-artifact-lifecycle-audit.md` CG-1 | Pi extensions use `ExtensionAPI` (`packages/pi-coding-agent/src/core/extensions/types.ts:1288-1350`); GSD ecosystem loader says it is isolated from Pi's loader chain and loads `.gsd/extensions/` (`ecosystem/loader.ts:1-4`, `82-95`); wrapper adds GSD state methods (`gsd-extension-api.ts:40-45`, `224-227`). | Mechanically confirmed. | Medium: lifecycle/compatibility consequences need adjudication. |
| Workflow plugins are distinct from extension APIs and skills. | `SYNTHESIS.md` §1.3; `04-artifact-lifecycle-output.md` addendum | Workflow plugins are `.yaml/.yml/.md` files with modes and project/global/bundled discovery (`workflow-plugins.ts:226-253`, `290-304`); dispatch is through workflow command handler (`commands/handlers/workflow.ts:165-222`). | Confirmed mechanically. | Yes, for whether they should be treated as R2 extension surface or workflow/config surface. |
| Skills have their own discovery and manifest system. | `SYNTHESIS.md` §1.3; `04-artifact-lifecycle-output.md` addendum | Pi skill discovery/validation is in `packages/pi-coding-agent/src/core/skills.ts:10-20`, `81-100`, `160-167`; GSD dynamic skill discovery is in `skill-discovery.ts:15-23`, `53-97`; per-unit allowlist is in `skill-manifest.ts:25-33`, `131-150`. | Confirmed. | Low/medium: relationship to extension strategy is interpretive. |
| `markdown-phase` is prompt-dispatch rather than deterministic executor-owned shell execution. | `w2-markdown-phase-engine-findings.md` §0-§2; `SYNTHESIS.md` F4/§1.2 | `dispatchMarkdownPhase` builds a prompt and sends it via `pi.sendMessage` (`workflow-dispatch.ts:78-105`); markdown-phase plugin dispatch reads markdown and writes startup scaffolding (`commands-workflow-templates.ts:558-650`). I did not observe source that parses markdown command blocks and runs them. | Confirmed within inspected paths; absence claim remains bounded. | Medium: complete proof over repo would require broader search/runtime test. |
| `yaml-step` uses graph-backed deterministic mutation and structured dependency/context behavior. | `w2-markdown-phase-engine-findings.md` §4/§7; `SYNTHESIS.md` F4 | `CustomWorkflowEngine` reads/writes `GRAPH.yaml` and marks steps active/complete (`custom-workflow-engine.ts:51-72`, `90-115`, `192-215`); YAML definitions include dependencies/context (`definition-loader.ts:35-52`, `376-390`). | Confirmed. | Medium: "deterministic" beyond graph mutation and verification behavior should be adjudicated carefully. |
| `shell-command` verification exists for YAML/custom workflows. | `w2-markdown-phase-engine-findings.md` §2; `SYNTHESIS.md` §1.2 | `VerifyPolicy` includes `shell-command` (`definition-loader.ts:22-26`), validation requires a command (`definition-loader.ts:192-209`), and handler runs `spawnSync("sh", ["-c", ...])` with timeout (`custom-verification.ts:145-175`). | Confirmed. | Low for existence; high for security/viability implications. |
| Extension/trust/security boundaries matter. | `SYNTHESIS.md` F9; `04-artifact-lifecycle-output.md` watchlist | Ecosystem extensions skip untrusted projects (`ecosystem/loader.ts:85-95`); shell-command verification names the workflow-definition author as trust boundary and same-process privileges (`custom-verification.ts:151-154`); rule hooks prevent hook-on-hook chains (`rule-registry.ts:161-168`). | Confirmed as source-present. | Yes, for full security model. |
| Claude Code CLI stream-adapter delta is relevant to workflow automation surfaces. | User instruction to pay attention to fresh delta; not a current synthesis claim I adjudicated. | Current source auto-approves headless/no-UI tool requests (`stream-adapter.ts:1642-1663`), sets allowed tools/MCP wildcards (`stream-adapter.ts:1291-1311`), distinguishes abort vs exhausted stream (`stream-adapter.ts:1173-1191`, `1837-1841`), and preserves SDK tool-call/results (`stream-adapter.ts:1453-1580`, `1800-1828`). | Confirmed as relevant surface; not adjudicated for product meaning. | Yes. |

## 4. Claims Needing High Adjudication

1. **Whether the four surfaces should all be called "extension surfaces."**
   - Load-bearing because R2 viability depends on what counts as extension versus configuration/workflow/prompt substrate.
   - Inspect: `extension-discovery.ts`, `ecosystem/loader.ts`, `workflow-plugins.ts`, `skill-discovery.ts`, `skill-manifest.ts`, CONTRIBUTING extension policy.
   - Non-mechanical because workflow plugins and skills are not code extension modules even though the audit spec explicitly put them in scope.

2. **Which subsystem is the right target for a given uplift act.**
   - Load-bearing because "R2 extension" could mean Pi code extension, GSD ecosystem extension, workflow plugin, skill, hook, or some combination.
   - Inspect: dispatch handlers, lifecycle docs, security/trust paths, workflow plugin modes.
   - Non-mechanical because it maps technical surfaces to project strategy.

3. **Whether markdown-phase limitations materially weaken R2 viability.**
   - Load-bearing for release/hotfix/RC workflow candidates.
   - Inspect: `commands-workflow-templates.ts`, `workflow-dispatch.ts`, markdown templates, `workflow-start.md`, runtime tests if available.
   - Non-mechanical because prompt-mediated workflows may still be viable depending on target use case.

4. **Whether yaml-step is mature enough to carry deterministic uplift workflows.**
   - Load-bearing because it is the source-backed deterministic alternative to markdown-phase.
   - Inspect: `run-manager.ts`, `graph.ts`, `custom-workflow-engine.ts`, `custom-execution-policy.ts`, `custom-verification.ts`, integration tests.
   - Non-mechanical because source supports the mechanism, but maturity, UX, failure recovery, and adoption are broader claims.

5. **Whether `.pi/extensions` vs `.gsd/extensions` is a resolved distinction or a drift risk.**
   - Load-bearing for third-party extension authoring and documentation claims.
   - Inspect: Pi loader project-extension paths, GSD ecosystem loader, extension SDK docs, install/validate commands.
   - Non-mechanical because both paths exist, but the intended user-facing model and compatibility story require design interpretation.

6. **Whether the Claude Code CLI stream-adapter delta changes trust/automation claims.**
   - Load-bearing if automation depends on Claude Code provider behavior in headless or workflow modes.
   - Inspect: `stream-adapter.ts`, provider tests, agent-core `externalToolExecution` path, permission UI behavior.
   - Non-mechanical because the source shows behavior but not whether it is acceptable, regressive, or strategically relevant.

7. **Whether hook layers compose safely with extension/workflow layers.**
   - Load-bearing because hooks can modify/skip prompt dispatch and shell hooks can block/modify actions.
   - Inspect: `hooks-runner.ts`, `rule-registry.ts`, `register-hooks.ts`, preferences schemas, trust markers.
   - Non-mechanical because safety depends on runtime ordering, trust configuration, and user workflows.

8. **Whether current artifacts overstate "determinism" for yaml-step.**
   - Load-bearing because yaml-step still dispatches prompts to an agent; deterministic parts are graph mutation and verification, not necessarily step content generation.
   - Inspect: `engine-types.ts`, `custom-workflow-engine.ts`, `context-injector.ts`, `custom-verification.ts`, e2e tests.
   - Non-mechanical because determinism has multiple layers.

## 5. Possible Missing Sibling Mechanisms

- **MCP workflow tools**: I saw `packages/mcp-server/src/workflow-tools.ts` and `src/resources/extensions/gsd/workflow-mcp.ts` in inventory but did not trace them. They may be a sibling machine-facing workflow surface rather than merely an access path.
- **Marketplace/plugin importer**: Inventory shows `marketplace-discovery.ts` and `plugin-importer` tests with skills/agents/hooks. This may be a broader component ecosystem adjacent to skills/extensions.
- **Agents/subagents as components**: The `src/resources/extensions/subagent/` extension and plugin importer references to agents suggest another component type, but I did not inspect it.
- **Workflow MCP auto-prep / workflow projections / reconcile**: Source names suggest workflow-adjacent mechanisms beyond plugin discovery and engine dispatch. I did not inspect them because the medium-depth pass focused on named claims.
- **Web workflow action execution**: `web/lib/workflow-action-execution.ts` and integration tests may expose UI/web workflow controls. I only noted their existence.
- **UOK kernel wrapper**: Current artifacts describe it as a scheduler/wrapper path. I did not inspect it in this scout pass except through prior artifact claims.

## 6. Scope Boundaries

- I did not run gsd-2, start workflows, or execute extension loading at runtime.
- I did not inspect the full Pi extension loader implementation beyond API/discovery/registry-oriented paths and current-artifact references.
- I did not inspect all bundled templates, only the discovery/dispatch machinery and current-artifact claims about markdown/yaml modes.
- I did not inspect full contribution history, release cadence, package publication, or PR culture.
- I did not adjudicate R1/R2/R3/R4/R5 viability.
- I did not inspect all tests; tests were used by `rg` for orienting evidence only where they pointed to surfaces.
- I did not modify the read-only source target.

## 7. Scout Caveat

This is a medium-reasoning source scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2`.
