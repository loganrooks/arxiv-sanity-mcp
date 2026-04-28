---
type: wave-2-adjudication
date: 2026-04-28
adjudicator: extension-workflow
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 02 — Extension / Workflow

## 0. Adjudication Summary

Current Claude investigation remains usable for this domain, but it needs localized terminology and determinism qualifications before Gate 2. The source supports plural extension-adjacent mechanisms, distinct workflow modes, and material trust boundaries; it does not support treating every mechanism as the same kind of "extension surface" or treating workflow-plugin viability as one uniform R2 claim.

High-severity qualification: "extension surface" should be a typed umbrella, not a silent semantic merger. Pi extensions, GSD ecosystem extensions, workflow plugins, skills, hooks/rules, workflow MCP tools, and the Claude Code CLI provider surface have different registration, execution, trust, and caller contracts.

Medium/high-severity qualification: `markdown-phase` is prompt dispatch with startup scaffolding, not executor-owned deterministic shell execution. `yaml-step` determinism is real for graph mutation, eligibility, context injection, and verification policy execution; step work still reaches the agent as prompt content.

## 1. Claim Verdict Table

| Claim family | Verdict | Severity | Confidence | One-line reason |
|---|---|---|---|---|
| Whether all identified mechanisms should be called extension surfaces | Survives with qualification | high | high | Mechanism plurality survives, but not all mechanisms are extension surfaces in the same sense. |
| Pi coding-agent extensions vs GSD ecosystem extensions | Survives with qualification | medium-high | high | They are source-distinct; GSD ecosystem extensions wrap/delegate to Pi API while intercepting GSD-specific state timing. |
| Workflow plugins vs skills vs hooks | Survives with qualification | medium-high | high | They are distinct mechanisms; workflow MCP tools and plugin importer are additional sibling surfaces worth naming. |
| `markdown-phase` prompt-dispatch limitations | Survives | high | high | Source dispatch writes scaffolding and sends a prompt; no inspected executor path parses markdown commands into shell steps. |
| `yaml-step` deterministic claims | Survives with qualification | high | high | Graph and verification layers are deterministic; prompt-authored step content is not executor-deterministic. |
| Hook/trust/security composition | Survives with qualification | medium-high | high | Trust boundaries and hook composition are source-present, but they are multiple mechanisms, not one security model. |
| Claude Code CLI provider/permission behavior as workflow automation surface | Survives with qualification | medium | medium-high | It materially affects Claude-backed workflow automation and trust, but it is a provider surface, not a workflow engine. |

## 2. Detailed Adjudication

### 2.1 Whether all identified mechanisms should be called extension surfaces

- Claim under audit: Current artifacts claim the "extension surface" is plural, and the spec asks whether Pi extensions, GSD ecosystem extensions, workflow plugins, skills, hooks/rules, and provider extensions all deserve the same semantic label.
- Current artifact evidence: Gate 1 explicitly warns this domain risks conflating distinct mechanisms into one "extension" concept (`GATE-1-DISPOSITION.md:36-42`) and instructs this adjudicator to separate mechanism existence, semantic grouping, and downstream strategy meaning (`GATE-1-DISPOSITION.md:99-107`). Scout 02 confirms a plural inventory while reserving semantic/R-strategy mapping (`wave-1/wave-1-scout-02-extension-workflow.md:13-21`, `:107-147`). Synthesis states "at least four parallel extension surfaces" (`SYNTHESIS.md:99-108`).
- Source evidence inspected: Pi extensions use manifest/registry/discovery and `ExtensionAPI` registration (`src/extension-discovery.ts:9-18`, `src/extension-registry.ts:15-32`, `packages/pi-coding-agent/src/core/extensions/types.ts:1285-1350`, `:1374-1555`). GSD ecosystem extensions load `.gsd/extensions/` with a separate wrapper and trust gate (`src/resources/extensions/gsd/ecosystem/loader.ts:1-4`, `:82-95`, `:123-129`). Workflow plugins are markdown/YAML files with modes and precedence (`src/resources/extensions/gsd/workflow-plugins.ts:1-14`, `:120-122`, `:290-304`). Skills are instruction bundles and allowlists, not code-extension modules (`packages/pi-coding-agent/src/core/skills.ts:10-20`, `src/resources/extensions/gsd/skill-manifest.ts:1-16`, `:131-150`). Hooks include shell-hook settings and GSD rule hooks (`packages/pi-coding-agent/src/core/settings-manager.ts:119-149`, `src/resources/extensions/gsd/rule-registry.ts:145-184`, `:270-315`).
- Reasoning: Source supports a broad extension-adjacent ecosystem, but the mechanisms are not same-kind. Pi/GSD ecosystem extensions are code-loading APIs. Workflow plugins are declarative/procedural workflow definitions. Skills are prompt/instruction resources. Hooks/rules are interception or prompt-dispatch modifiers. Provider extensions are runtime/model integration surfaces. Calling all of these simply "extension surfaces" is useful only if immediately typed.
- Verdict: Survives with qualification.
- Severity: high.
- Confidence: high.
- Downstream correction or qualification: Replace bare "extension surface" claims with typed labels: code extension API, GSD ecosystem extension, workflow plugin, skill/instruction resource, hook/rule interception layer, provider integration, and workflow MCP/machine surface where applicable. R2/R4 meaning must be assigned after this typing, not inferred from the word "extension."

### 2.2 Pi coding-agent extensions vs GSD ecosystem extensions

- Claim under audit: Pi coding-agent extensions and GSD ecosystem extensions are distinct source mechanisms; relationship may be wrapper/delegation, parallel subsystem, or something else.
- Current artifact evidence: Scout 02 says Pi extensions use `ExtensionAPI` and registry/discovery, while GSD ecosystem extensions load project `.gsd/extensions/` through `GSDExtensionAPI` (`wave-1/wave-1-scout-02-extension-workflow.md:13-15`, `:45-56`). Slice 4 addendum says the ecosystem layer resolves the `.pi/extensions` vs `.gsd/extensions` discrepancy (`04-artifact-lifecycle-output.md:425-429`).
- Source evidence inspected: Pi loader discovers trusted project-local `.pi/extensions`, global, installed, and configured extension paths (`packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1128`). GSD ecosystem loader says it is isolated from Pi's loader chain and loads `.gsd/extensions/` (`src/resources/extensions/gsd/ecosystem/loader.ts:1-4`, `:82-95`). `GSDExtensionAPI` extends `ExtensionAPI`, adds `getPhase`/`getActiveUnit`, delegates most methods to Pi, and intercepts only `before_agent_start` (`src/resources/extensions/gsd/ecosystem/gsd-extension-api.ts:40-45`, `:136-156`, `:166-227`). Bootstrap registers ecosystem loading as a non-critical GSD registration path (`src/resources/extensions/gsd/bootstrap/register-extension.ts:91-126`).
- Reasoning: They are distinct discovery/loading mechanisms with different project directories and timing semantics. They are not independent in capability terms: GSD ecosystem extensions mostly delegate back to the Pi `ExtensionAPI`, adding GSD state access and one event interception point.
- Verdict: Survives with qualification.
- Severity: medium-high.
- Confidence: high.
- Downstream correction or qualification: Describe the relationship as "parallel project-local loader plus GSD wrapper over Pi API," not as either fully independent subsystem or simple alias.

### 2.3 Workflow plugins vs skills vs hooks

- Claim under audit: Workflow plugins, skills, and hooks are distinct enough that synthesis should avoid treating them as one extension family; current synthesis may also be missing sibling mechanisms.
- Current artifact evidence: Slice 3 distinguishes workflow engines/templates, shell hooks, rule hooks, and skill behavior (`03-workflow-surface-output.md:118-130`, `:132-145`, `:146-156`). Scout 02 confirms workflow plugins, skills, hooks/rules, and provider behavior separately, and flags possible missing sibling mechanisms including MCP workflow tools and marketplace/plugin importer (`wave-1/wave-1-scout-02-extension-workflow.md:57-91`, `:149-156`).
- Source evidence inspected: Workflow plugins are discovered from bundled/global/project locations and grouped by mode (`src/resources/extensions/gsd/workflow-plugins.ts:1-14`, `:256-304`, `:319-340`), then dispatched by mode through workflow handlers (`src/resources/extensions/gsd/commands/handlers/workflow.ts:165-222`). Skills are discovered from `.agents`/Claude/ecosystem skill directories and filtered by unit type (`packages/pi-coding-agent/src/core/skills.ts:10-20`, `:160-167`; `src/resources/extensions/gsd/skill-discovery.ts:1-9`, `:53-97`; `src/resources/extensions/gsd/skill-manifest.ts:25-33`, `:131-150`). Shell hooks run configured commands with JSON stdin and block/modify semantics (`packages/pi-coding-agent/src/core/hooks-runner.ts:85-105`, `:126-228`), while GSD rule hooks evaluate post-unit and pre-dispatch prompt behavior (`src/resources/extensions/gsd/rule-registry.ts:145-184`, `:270-315`). Workflow MCP tools expose workflow read/mutation handlers over MCP (`packages/mcp-server/src/workflow-tools.ts:1-3`) and `workflow-mcp.ts` declares a workflow tool surface (`src/resources/extensions/gsd/workflow-mcp.ts:23-64`). Plugin importer separately discovers/selects/validates/imports marketplace components (`src/resources/extensions/gsd/plugin-importer.ts:1-14`, `:85-114`).
- Reasoning: Workflow plugins, skills, hooks, MCP workflow tools, and importer components differ in registration, invocation, and authority. They may compose in a workflow, but treating them as one extension family loses operationally important distinctions.
- Verdict: Survives with qualification.
- Severity: medium-high.
- Confidence: high.
- Downstream correction or qualification: Synthesis should mention workflow MCP tools and plugin importer as sibling extension/workflow-adjacent mechanisms if it is claiming subsystem completeness. It does not need a full topology remap for Gate 2.

### 2.4 `markdown-phase` prompt-dispatch limitations

- Claim under audit: Source supports that `markdown-phase` is prompt-dispatch, not deterministic executor-owned shell execution; absence claim must be bounded; limitation may affect R-strategy claims.
- Current artifact evidence: W2 markdown-phase dive says top-line that `markdown-phase` is prompt-dispatch with startup scaffolding, not deterministic phase executor (`w2-markdown-phase-engine-findings.md:12-23`), and explicitly bounds absence claims (`w2-markdown-phase-engine-findings.md:108-115`). Synthesis carries this into F4 and R2 implications (`SYNTHESIS.md:39-40`, `:90-97`, `:181-185`, `:330-342`).
- Source evidence inspected: `dispatchMarkdownPhase` builds a `workflow-start` prompt and calls `pi.sendMessage` (`src/resources/extensions/gsd/workflow-dispatch.ts:78-106`). Markdown plugin dispatch reads the template, creates artifact directory/branch, writes `STATE.json`, and sends the prompt (`src/resources/extensions/gsd/commands-workflow-templates.ts:556-670`). The workflow-start prompt instructs the agent to follow phases, write artifacts, commit, and verify (`src/resources/extensions/gsd/prompts/workflow-start.md:15-28`). `STATE.json` schema starts phase 0 active and is used for resume scanning (`src/resources/extensions/gsd/commands-workflow-templates.ts:76-123`, `:126-160`).
- Reasoning: The positive evidence for prompt-dispatch is direct. I did not find a markdown command-block parser or executor in the inspected dispatch paths; that absence remains bounded to these source paths and targeted searches. The limitation materially affects any claim that a `markdown-phase` release/hotfix/RC workflow can own deterministic shell or programmatic GSD operations.
- Verdict: Survives.
- Severity: high.
- Confidence: high.
- Downstream correction or qualification: Keep `markdown-phase` viable for agent-prompted procedural workflows, not deterministic executor-owned workflows. R2 candidates requiring deterministic shell/action ownership should be recast to `yaml-step`, code extension, or external orchestration.

### 2.5 `yaml-step` deterministic claims

- Claim under audit: Determine which `yaml-step` layers are deterministic and whether current synthesis overstates determinism.
- Current artifact evidence: W2 dive distinguishes `yaml-step` graph-backed state from `markdown-phase` prompt dispatch and says shell execution is verification-only (`w2-markdown-phase-engine-findings.md:20-23`, `:42-45`, `:64-79`, `:88-96`). Synthesis says `yaml-step` has deterministic `GRAPH.yaml` mutation, dependency tracking, structured `context_from`, and shell-command verification (`SYNTHESIS.md:39-40`, `:90-97`).
- Source evidence inspected: YAML definitions type steps with prompt, requires, produces, contextFrom, verify, and iterate (`src/resources/extensions/gsd/definition-loader.ts:35-52`, `:375-390`). Run creation freezes `DEFINITION.yaml`, initializes `GRAPH.yaml`, and optionally writes `PARAMS.json` (`src/resources/extensions/gsd/run-manager.ts:1-14`, `:119-155`). `CustomWorkflowEngine` reads/writes `GRAPH.yaml`, selects dependency-satisfied pending steps, marks active/complete, injects context, and reconciles completion (`src/resources/extensions/gsd/custom-workflow-engine.ts:51-72`, `:90-189`, `:192-225`). Graph dependency eligibility is explicit (`src/resources/extensions/gsd/graph.ts:154-175`). Context injection reads prior produced artifacts and prepends them to the prompt (`src/resources/extensions/gsd/context-injector.ts:24-43`, `:65-100`). `shell-command` verification is validated, then run with `spawnSync("sh", ["-c", ...])` and timeout (`src/resources/extensions/gsd/definition-loader.ts:192-209`; `src/resources/extensions/gsd/custom-verification.ts:144-182`). The step contract sent to the loop remains `unitType`, `unitId`, and `prompt` (`src/resources/extensions/gsd/engine-types.ts:20-25`).
- Reasoning: Deterministic layers: graph file mutation, dependency eligibility, run-directory initialization, context lookup/injection mechanics, and shell-command verification execution. Non-deterministic or agent-mediated layers: interpreting the step prompt, producing artifacts, and any task work not encoded as verification. Verification result gating is deterministic at policy level but depends on commands authored in trusted workflow definitions.
- Verdict: Survives with qualification.
- Severity: high.
- Confidence: high.
- Downstream correction or qualification: Current synthesis is acceptable if "deterministic" is read as applying to graph/control/verification layers. Add explicit caveat that `yaml-step` does not make prompt content or agent execution deterministic.

### 2.6 Hook/trust/security composition

- Claim under audit: Trust boundaries are source-present and material; hooks/rules compose with extension/workflow layers in ways synthesis may miss or overstate.
- Current artifact evidence: Scout 02 says trust boundaries are not incidental and names ecosystem trust, shell-command verification trust, and hook-on-hook prevention (`wave-1/wave-1-scout-02-extension-workflow.md:19-20`, `:81-85`, `:103-105`, `:139-142`). Synthesis F9 says security/trust model is structurally present and central (`SYNTHESIS.md:51-52`).
- Source evidence inspected: Pi project-local extensions load only trusted `.pi/extensions` paths (`packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1090`). GSD ecosystem extensions skip untrusted `.gsd/extensions` projects and reject realpath escapes (`src/resources/extensions/gsd/ecosystem/loader.ts:85-95`, `:140-158`). Shell hooks require project trust for project hooks and can block via exit code or parsed stdout (`packages/pi-coding-agent/src/core/hooks-runner.ts:85-105`, `:202-228`). Rule hooks prevent hook-on-hook chains and can skip/modify/replace pre-dispatch prompts (`src/resources/extensions/gsd/rule-registry.ts:161-184`, `:276-315`). `shell-command` verification names the workflow-definition author as the trust boundary and runs with GSD process privileges (`src/resources/extensions/gsd/custom-verification.ts:151-155`). Claude provider permissions also default/auto-approve in some modes (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1212-1231`, `:1642-1663`).
- Reasoning: Trust/security concerns are source-present at multiple layers. They compose because hooks can alter/block tool and prompt behavior, workflow definitions can run verification commands, ecosystem extensions are project code, and provider permissions can auto-approve tool use. But they are not one uniform trust boundary.
- Verdict: Survives with qualification.
- Severity: medium-high.
- Confidence: high.
- Downstream correction or qualification: Treat security/trust as cross-cutting across extension/workflow/provider layers. Do not infer that trust-gating one layer secures the others.

### 2.7 Claude Code CLI provider/permission behavior as workflow automation surface

- Claim under audit: Fresh `stream-adapter.ts` behavior may matter to workflow automation or trust claims, but should stay scoped to domain relevance.
- Current artifact evidence: Freshness delta says the source range changed Claude Code CLI permission persistence and Scout 02 should inspect fresh source (`SOURCE-FRESHNESS-DELTA-2026-04-28.md:56-62`, `:96-102`). Scout 02 reports the current source defaults permission behavior broadly, auto-approves headless tool requests, preserves tool-call/results, and distinguishes abort from exhaustion (`wave-1/wave-1-scout-02-extension-workflow.md:20`, `:87-91`, `:134-137`).
- Source evidence inspected: Non-Bash "Always Allow" without SDK suggestions now builds a tool-name-only fallback permission rule (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1094-1118`), with tests for missing and empty suggestions (`src/resources/extensions/claude-code-cli/tests/stream-adapter.test.ts:1612-1646`). Permission mode resolution returns `bypassPermissions` for headless and currently also by default (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1198-1231`). SDK options include broad allowed tools and MCP wildcard entries and set `allowDangerouslySkipPermissions` when bypassing (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1272-1338`). In no-UI/headless cases, the `canUseTool` fallback auto-allows tool requests (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1642-1663`). Tool-call/result preservation for external execution is explicit (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1453-1502`, `:1517-1581`), and generator exhaustion is classified as an error rather than success (`src/resources/extensions/claude-code-cli/stream-adapter.ts:1837-1841`).
- Reasoning: This is materially relevant when workflow automation runs through the Claude Code provider, because permissions decide whether agent-prompted or workflow-dispatched tool use blocks, auto-allows, persists, or reports correctly. It is not itself a workflow engine and should not be folded into workflow-plugin determinism.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: medium-high.
- Downstream correction or qualification: Keep provider permission behavior in trust/runtime qualifications for workflow automation, especially headless/auto-mode and MCP tool use. Do not use it to adjudicate full provider architecture or release practice.

## 3. Cross-Domain Flags

- Topology/runtime adjudicator: workflow MCP tools are a sibling machine-facing workflow automation surface, not just an extension/workflow implementation detail (`packages/mcp-server/src/workflow-tools.ts:1-3`; `src/resources/extensions/gsd/workflow-mcp.ts:23-64`).
- Topology/runtime adjudicator: Claude Code CLI permission mode and auto-approval behavior are runtime/provider facts relevant to headless and workflow automation, but this report does not adjudicate the full provider stack.
- Release/practice adjudicator: release/hotfix `markdown-phase` workflows are agent-prompted procedures, not executor-deterministic release engines. Any release-practice inference based on workflow templates should preserve that limitation.
- Release/practice adjudicator: extension stability claims should not be inferred from formal mechanism existence alone; trust and permission behavior affect whether those mechanisms are viable for third-party uplift.

## 4. Limits

- I verified the source checkout was `HEAD == origin/main == bf1d8aad0473809a58be4e7d7fd386ffa1581d8a` and did not modify `/home/rookslog/workspace/projects/gsd-2-explore/`.
- I did not run gsd-2, execute workflows, install extensions, or run tests. This is source and artifact adjudication.
- Absence claims about `markdown-phase` are bounded to inspected dispatch/template/workflow paths and targeted source searches, not a mathematical proof over every repository file.
- I did not perform a full security model or provider audit. Trust/security and Claude Code CLI behavior are adjudicated only for extension/workflow relevance.
- I did not construct a replacement workflow architecture or decide R1-R5 strategy. I only classified how source evidence qualifies current synthesis claims.

## 5. Recommendation For Gate 2

localized qualifications needed
