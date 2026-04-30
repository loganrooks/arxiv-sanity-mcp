---
type: pre-D-probe-findings
probe: M2
date: 2026-04-30
gsd_2_commit: 42ef05fbe
scope: gsd-2 skill subsystem (primary), workflow templates and doctrine layer (light-touch); read-only structural snapshot
time_budget: ~75 min
status: calibrated
---

# M2 — Codebase Snapshot Findings

## §0 Summary

gsd-2's "skill subsystem" is the **Anthropic Agent Skills** standard (filesystem-based `SKILL.md` directories with YAML frontmatter), wired in via `packages/pi-coding-agent/src/core/skills.ts` (loader/discovery) plus a domain layer in `src/resources/extensions/gsd/skill-{manifest,discovery,catalog,health,telemetry}.ts`. Skills are markdown files; they are surfaced to the model in the system prompt and invoked via a `Skill` tool — the manifest is per-unit-type allowlist, not per-edit doctrine load-points. The `/gsdr:*` items in the user's available-skills list are **not skills** in this subsystem; they are Claude Code slash-commands at `~/.claude/commands/gsdr/*.md` (separate package: `get-shit-done-reflect` v1.19.10+dev), distinct from the gsd-2 codebase. The strongest existing-primitive overlaps with "decision-trace" semantics are: **`gsd:deliberate`** (full structured deliberation with predictions, evaluation loop, `.planning/deliberations/` artifact), **`gsd:audit`** (3-axis classification + obligation composition), **`spike-wrap-up` skill** (durable packaging of spike findings into project-local skills), and **`.gsd/DECISIONS.md`** (one-line decision log convention referenced by `design-an-interface`, `write-milestone-brief`, and the `spike` workflow). H3 (existing-primitives unmapped) is therefore the most consequential of the three Phase D opening hypotheses — `gsd:deliberate` is already doing much of what a "decision-trace skill" would do.

## §1 Method

### Read (binding evidence)
- `src/resources/extensions/gsd/skill-manifest.ts` (full)
- `src/resources/extensions/gsd/skill-discovery.ts` (full)
- `src/resources/extensions/gsd/skill-catalog.ts` (full)
- `packages/pi-coding-agent/src/core/skills.ts` (full)
- `src/resources/extensions/gsd/auto-prompts.ts` lines 700-820 (skill activation block construction)
- `src/resources/extensions/gsd/unit-context-manifest.ts` lines 1-80
- `src/resources/extensions/gsd/workflow-templates/spike.md` (full)
- `src/resources/skills/create-skill/SKILL.md` (full — doctrine for authoring)
- `src/resources/skills/{spike-wrap-up,forensics,handoff,decompose-into-slices,write-milestone-brief,review,create-workflow}/SKILL.md` (heads, 20-50 lines each)
- `~/.claude/commands/gsdr/{deliberate,reflect,spike,explore,audit,signal,collect-signals}.md` (full or substantial)
- `gsd-orchestrator/SKILL.md` (head)
- `docs/user-docs/skills.md` (full)
- `VISION.md` (full)
- `CONTRIBUTING.md` (grep: skill mentions)
- `README.md` (grep: skill mentions; not full read)
- `mintlify-docs/guides/skills.mdx`, `gitbook/features/skills.md` — listed but not read (assumed redundant with `docs/user-docs/skills.md`)

### Deliberately did not read
- `src/resources/extensions/gsd/skill-{health,telemetry}.ts` (telemetry/lifecycle — outside primary probe scope)
- `dist/` (build artifacts)
- `node_modules/`
- Skills outside the "plausibly overlapping with decision-trace" filter (e.g., `accessibility`, `core-web-vitals`, `tdd`, language-specific skills)
- `tests/skill-*.test.ts` (validation behavior likely matches the source)
- The 20+ `mcp-server/` package files
- Full `auto-prompts.ts` (3000+ lines; only the skill-activation segment is load-bearing here)

### Spot-check vs binding-evidence calibration
Where this report cites file:line, claims rest on the actual file content. Where it characterizes (e.g., "no doctrine-load-point analog"), I searched for trigger-pattern keywords (`grep -rn "before edit\|load.*before\|trigger.*read\|doctrine.*load"` across `src/resources/skills/` and `docs/user-docs/skills.md`) and found nothing matching the arxiv-sanity-mcp CLAUDE.md "before editing X load Y" shape — but I did not exhaustively read every skill body, so this is **negative evidence with bounded coverage**, not a proof. The closer analog (description-keyword similarity matching, `auto-prompts.ts:707-717`) is positively documented.

The `/gsdr:*` characterization rests on (a) the user's available-skills list explicitly tagging them `v1.19.10+dev` and (b) reading the actual command files at `~/.claude/commands/gsdr/`, which use Claude Code's slash-command frontmatter (`allowed-tools`, `argument-hint`) — not the SKILL.md/Agent-Skills schema gsd-2 uses internally.

## §2 Skill subsystem snapshot

### Manifest schema (file shape)

A skill is a directory containing a `SKILL.md` file with YAML frontmatter, validated per the Agent Skills standard at `packages/pi-coding-agent/src/core/skills.ts:81-95`:

```typescript
export interface SkillFrontmatter {
  name?: string;
  description?: string;
  "disable-model-invocation"?: boolean;
  [key: string]: unknown;
}
export interface Skill {
  name: string;
  description: string;
  filePath: string;
  baseDir: string;
  source: string;
  disableModelInvocation: boolean;
}
```

Validation rules (`skills.ts:112-151`):
- `name`: lowercase alphanumeric + hyphens, ≤64 chars, no leading/trailing/consecutive hyphens, must match parent directory name
- `description`: required, ≤1024 chars; missing description = skill silently dropped (`skills.ts:281-283`)
- Parent-directory match enforced — the directory name *is* the skill identity

Discovery rules (`skills.ts:166-251`):
- Direct `.md` children at the root of a skills directory
- Recursive `SKILL.md` under subdirectories (one level)
- Hidden files (`.*`) skipped; `node_modules` skipped; `.gitignore` honored

Skills can also be directories with `workflows/`, `references/`, `templates/`, `scripts/` subdirectories per the router pattern (`src/resources/skills/create-skill/SKILL.md:23-34`). Subdirectory contents are NOT auto-loaded — they are read on-demand by the SKILL.md instructions.

### Activation pattern

Three layers of activation are wired through `auto-prompts.ts`:

1. **Always-loaded catalog (system prompt injection).** All visible skills (those without `disable-model-invocation: true`) are stamped into the system prompt via `formatSkillsForPrompt` (`skills.ts:311-338`) as an `<available_skills>` XML block listing name + description + location. The model decides when to invoke the `Skill` tool.

2. **Per-unit-type allowlist (`skill-manifest.ts:33-123`).** A static `Record<string, string[]>` named `UNIT_TYPE_SKILL_MANIFEST` keyed by unit type (`research-milestone`, `plan-milestone`, `complete-milestone`, `validate-milestone`, `reassess-roadmap`, `research-slice`, `plan-slice`, `refine-slice`, `replan-slice`, `run-uat`). When a unit type matches, only listed skills survive into the prompt; unknown unit types fall through to "all skills" (wildcard, `:131-136`). `execute-task` is deliberately omitted from the manifest so it preserves wildcard fallback (`:119-122`). Strict mode (`GSD_SKILL_MANIFEST_STRICT=1`) warns on uninstalled-but-referenced skills (`:158-175`).

3. **User-preference layer (`auto-prompts.ts:707-797`).** Three preference categories drive invocation:
   - `always_use_skills` — explicit force-invoke (emits `<skill_activation>Call Skill({ skill: 'name' }).</skill_activation>`)
   - `prefer_skills` — invoke only when context tokens match skill name/description (`:707-717`, `skillMatchesContext`)
   - `skill_rules` — `when X then use/prefer/avoid Y` substring match against context tokens (`:736-751`)
   - Manifest also produces a separate `<skill_recommendations unit="...">` block (`:792-797`) that is **informational, not force-invoked** — surfaces per-unit-type defaults so the model can choose to invoke them.

The activation context is built from `milestoneId`, `milestoneTitle`, `sliceTitle`, `taskTitle`, `taskPlanContent`, plus extra context strings (`auto-prompts.ts:799-820+`).

### User-side discovery surface

Per `skills.ts:15-26, 421-433` and `skill-discovery.ts:15-17`, gsd-2 reads from three locations in priority order:

| Path | Scope | Source label |
|------|-------|--------------|
| `~/.agents/skills/` | Global (industry-standard, skills.sh ecosystem) | `user` |
| `.agents/skills/` (cwd-relative) | Project-local | `project` |
| `~/.gsd/agent/skills/` | Legacy (read-as-fallback until migration sentinel `.migrated-to-agents` exists) | `user` |

`skill-discovery.ts` *also* watches `~/.claude/skills/` as a secondary path (line 17 — `CLAUDE_SKILLS_DIR`). This watcher is the runtime-discovery path: it snapshots at auto-mode start and detects skills installed mid-session, injecting them into the system prompt as `<newly_discovered_skills>` (`:53-98`).

Name collisions resolved first-wins with a collision diagnostic (`skills.ts:401-417`). Global beats project on collision (`docs/user-docs/skills.md:16`).

### Per-unit-type allowlist (the actual data)

Excerpt — manifest entries that constrain skills to specific unit types (full table at `skill-manifest.ts:33-123`):

| Unit type | Skills allowlisted |
|---|---|
| `research-milestone` | write-docs, write-milestone-brief, decompose-into-slices, grill-me, design-an-interface, api-design, observability |
| `plan-milestone` | write-milestone-brief, decompose-into-slices, design-an-interface, grill-me, write-docs, api-design, tdd, verify-before-complete |
| `complete-milestone` | verify-before-complete, write-docs, handoff, forensics, observability, security-review |
| `validate-milestone` | verify-before-complete, review, test, lint, security-review, accessibility, forensics, observability |
| `reassess-roadmap` | decompose-into-slices, grill-me, write-milestone-brief, write-docs, forensics |
| `run-uat` | verify-before-complete, test, review, accessibility |
| `execute-task` | (intentionally absent — wildcard fallback) |

This is a **shape-of-work allowlist**, not a "before-edit-X-load-Y" hook.

## §3 Existing primitives inventory

The `/gsdr:*` items in the available-skills list are **slash-commands** in `~/.claude/commands/gsdr/` (Claude Code's slash-command directory), packaged with `get-shit-done-reflect` v1.19.10+dev. They are **not** the gsd-2 internal skills (which live in `gsd-2-explore/src/resources/skills/`). I list both groups below since both are candidates for "existing primitives that may overlap with decision-trace."

### A. /gsdr:* slash-commands (separate package; what the user has installed)

| Primitive | Location (host) | What it does (1-3 lines) | Activation | Output shape |
|---|---|---|---|---|
| `/gsdr:deliberate` | `~/.claude/commands/gsdr/deliberate.md` | Structured deliberation with severe-testing (Mayo), warranted-assertibility (Dewey), falsifiable-prediction (Popper/Lakatos). Templates Trigger → Situation → Framing → Design Space → Predictions → Recommendation → Evaluation flow. Captures observation as signal (Step 1.5 gate). | User runs `/gsdr:deliberate "topic"` or with `--continue <slug>`; supports both fresh and resume modes; reads conversation context if no args | `.planning/deliberations/{slug}.md` with statuses `open` → `concluded` → `adopted` → `evaluated`; optional signal file in `~/.gsd/knowledge/signals/{project}/`; git commit per `commit_docs` setting |
| `/gsdr:reflect` | `~/.claude/commands/gsdr/reflect.md` | Routes to `get-shit-done-reflect/workflows/reflect.md`. Analyzes accumulated signals from KB, detects recurring patterns, distills lessons. Optional drift / cross-project / patterns-only modes. | User: `/gsdr:reflect [phase] [--all] [--drift] [--patterns-only]`; YOLO mode auto-approves HIGH confidence lessons | Lesson files (location not directly visible in command body — workflow-resident) |
| `/gsdr:audit` | `~/.claude/commands/gsdr/audit.md` | 3-axis (subject × orientation × delegation) audit dispatcher. Composes obligations from core (5 rules) + orientation + subject + cross-cutting (chain integrity / dispatch hygiene / framework invisibility). Inlines obligations into task spec (DC-2: copy, don't reference). Dispatches `gsdr-auditor` agent or `codex exec`. | User: `/gsdr:audit "topic"` with optional `--auto`, `--subject`, `--orientation`, `--delegation`, `--continue` | `.planning/audits/YYYY-MM-DD-{slug}/{slug}-task-spec.md` + `{slug}-output.md`; delegation log line in `.planning/delegation-log.jsonl` |
| `/gsdr:signal` | `~/.claude/commands/gsdr/signal.md` | Manual signal capture into `~/.gsd/knowledge/signals/{project}/{date}-{slug}.md` with v2_split provenance schema (`detected_by`/`written_by`). Auto-assigns severity, infers signal_type, dedup against index, volume check. | User: `/gsdr:signal "description" [--severity ...] [--type ...]` | KB signal file + index rebuild |
| `/gsdr:explore` | `~/.claude/commands/gsdr/explore.md` | Routes to `get-shit-done-reflect/workflows/explore.md`. Socratic ideation; routes outputs to notes / todos / seeds / research questions / requirements / new phases. | User: `/gsdr:explore [topic]` | Routed artifacts (notes/todos/seeds/etc.) |
| `/gsdr:spike` | `~/.claude/commands/gsdr/spike.md` | Routes to `get-shit-done-reflect/workflows/run-spike.md`. Translates design uncertainty into structured experiment with testable hypotheses; optional phase linkage. | User: `/gsdr:spike [question] [--phase N]` | Workflow-resident; spike artifacts presumably under `.planning/spikes/` |
| `/gsdr:collect-signals` | `~/.claude/commands/gsdr/collect-signals.md` | Routes to `get-shit-done-reflect/workflows/collect-signals.md`. Spawns parallel sensors (artifact, git) on a phase's execution artifacts, synthesizes signals to KB. Read-only retrospective. | User: `/gsdr:collect-signals <phase-number>` | KB signal files |

### B. gsd-2 internal SKILL.md skills (in the codebase under audit)

| Skill | Location | Behavior | Activation | Output shape |
|---|---|---|---|---|
| `spike-wrap-up` | `src/resources/skills/spike-wrap-up/SKILL.md` | Packages findings from a completed spike directory (`SCOPE.md`, `research/*.md`, `RECOMMENDATION.md`) into a **project-local skill** at `.claude/skills/<name>/SKILL.md`. Closes "throwaway spike → durable skill" loop. Refuses if recommendation has no reusable guidance. | Description-keyword match: "wrap up the spike", "package this as a skill", end of spike Phase 3 | Project-local SKILL.md file |
| `forensics` | `src/resources/skills/forensics/SKILL.md` | Post-mortem of failed auto-mode runs. Traces from symptom to root cause via `.gsd/activity/*.jsonl`, `.gsd/journal/`, `.gsd/metrics.json`, `.gsd/auto.lock`. Read-only. | Description-keyword match: "forensics", "post-mortem", "why did auto-mode fail", "trace the stuck loop" | GitHub-issue-ready report with file:line refs and proposed fix |
| `handoff` | `src/resources/skills/handoff/SKILL.md` | Mid-task handoff. Writes `continue.md` in active slice directory; ensures STATE.md and summary artifacts are current. | "hand off", "pause work", "I'll come back later" | `continue.md` (ephemeral pickup pointer) |
| `design-an-interface` | `src/resources/skills/design-an-interface/SKILL.md` | Captures decisions in `.gsd/DECISIONS.md` or active `S##-CONTEXT.md` with chosen shape and reason (Step 6 — file:line `:75-79`). | Description-keyword match | One-liner appended to `.gsd/DECISIONS.md`, plus interface design artifact |
| `write-milestone-brief` | `src/resources/skills/write-milestone-brief/SKILL.md` | Synthesizes conversation into `M###-CONTEXT.md`; appends architectural decisions to `.gsd/DECISIONS.md` (`:74`). | "turn this into a PRD", "draft a milestone brief" | `M###-CONTEXT.md` + DECISIONS.md append |
| `decompose-into-slices` | `src/resources/skills/decompose-into-slices/SKILL.md` | Breaks plan into vertical slices (tracer bullets). Produces `Slices` section of `M###-ROADMAP.md`. | "break this into slices", "decompose the plan" | Roadmap slices section |
| `review` | `src/resources/skills/review/SKILL.md` | Reviews diffs (staged/unstaged/commit/PR) for security/perf/bugs/quality. Read-only analysis. | "review", "check changes" | Structured feedback report |
| `verify-before-complete`, `grill-me`, `create-skill`, `create-workflow`, `write-docs`, `tdd`, `test`, `lint`, `observability`, `security-review`, `api-design`, `accessibility`, etc. | `src/resources/skills/*/SKILL.md` | Domain-specific skills (full list at §1 read inventory). | Description-keyword match + per-unit-type allowlist | Varies by skill |

### Most plausibly overlapping with decision-trace semantics

In rough order of overlap depth, by binding evidence:

1. **`/gsdr:deliberate` (decisive overlap).** It is *already* a structured decision-trace with: trigger taxonomy, severe-testing of factual claims (Step 2.5, Mayo), falsifiable predictions (Step 6, Popper), evaluation status lifecycle (`open` → `concluded` → `adopted` → `evaluated`), Toulmin-style option presentation (Step 5), pipeline-integration hooks to plan-phase / discuss-phase / reflect, and integration with the signal system. The artifact lives at `.planning/deliberations/{slug}.md`. The H3 hypothesis (existing primitives may already cover decision-trace) is strongly supported here — `gsd:deliberate` arguably *is* a decision-trace skill, just not labeled that way.
2. **`spike-wrap-up` skill (durability overlap).** Closes the loop from "decision was investigated via spike" → "durable artifact agents auto-load on similar future work." This is the *packaging* dimension of decision-trace — capturing the trace in a form that future sessions can find by description-keyword match.
3. **`/gsdr:audit`** (orthogonal but composable). Audit produces evidence-backed findings under composed obligations; an audit-output is itself a decision-relevant artifact. Less overlap with decision-*tracing* per se, but a decision-trace workflow might dispatch audits to populate the trace.
4. **`/gsdr:explore`, `/gsdr:spike`** — upstream of deliberation; they produce inputs that decisions consume. Marginal overlap with tracing itself; significant overlap with the "what gets traced" question.
5. **`.gsd/DECISIONS.md` convention** (lightweight overlap). One-line decision log appended to by `design-an-interface`, `write-milestone-brief`, and the spike workflow's wrap-up. Not a "trace" (no rationale chain), but it's the load-bearing existing convention for terse decision capture in gsd-2.

## §4 Skill-vs-workflow boundary

Two artifact families coexist:

**Skills** (`src/resources/skills/*/SKILL.md`):
- Markdown with YAML frontmatter; description-keyword matched and per-unit-type allowlisted
- Always loaded to system prompt (subject to manifest filter); model invokes via `Skill` tool
- Pure prompts — no executable steps the engine runs deterministically
- Author guidance: pure XML structure, no markdown headings, ≤500 lines (`create-skill/SKILL.md:42-54`)

**Workflow templates** (`src/resources/extensions/gsd/workflow-templates/`):
- Two file flavors:
  - `.md` files (e.g., `spike.md`, `bugfix.md`, `pr-review.md`, `refactor.md`) declare `mode: markdown-phase` in their `<template_meta>` block — these are **prompt-dispatched** (the engine reads phases as natural-language steps for the model)
  - `.yaml` files (e.g., `docs-sync.yaml`, `env-audit.yaml`, `rename-symbol.yaml`, `test-backfill.yaml`) declare `version: 1` and explicit `steps[]` — these are **deterministically dispatched** by the workflow engine (`custom-workflow-engine.ts`), with verification policies (`content-heuristic`, `shell-command`, `prompt-verify`, `human-review`)
- Per `create-workflow/SKILL.md` lines 5-37, the YAML schema enforces step IDs, dependency graph acyclicity, path-traversal guards, and parameter substitution

**Operational difference:**
- Skills are *capabilities the model invokes when it judges relevant*. They produce ad-hoc outputs.
- Markdown-phase workflows are *guided multi-phase tasks the model executes phase-by-phase*. The phases are prompts; the model decides *how* to execute each.
- YAML-step workflows are *deterministic step sequences the engine schedules*. The engine decides *when* each step runs based on dependency graph; the model only fills in the prompt body of each step.

**Which engine handles what:** the markdown-phase prompt-dispatch engine handles `.md` workflow templates and (transitively) every skill the model invokes; the deterministic engine handles `.yaml` workflow definitions. A skill *can* invoke a workflow (e.g., `/gsdr:spike` routes to a workflow file), and a workflow *can* invoke a skill (e.g., `spike.md` Phase 3 offers `spike-wrap-up`).

## §5 Doctrine-load-point analog (light-touch)

**Finding: gsd-2 has no direct analog to arxiv-sanity-mcp's "before editing X, load Y" trigger pattern.** The closest functional analogs are:

1. **Description-keyword similarity matching** (`auto-prompts.ts:707-717`). When the unit's context tokens (milestone/slice/task IDs and titles, plus extra context) match a skill's name or description, the skill is preferred / activated. This is *content*-driven, not *file-edit*-driven; it activates a skill but doesn't gate edits.
2. **Per-unit-type allowlist** (`skill-manifest.ts:33-123`). Constrains which skills are visible in the prompt for each lifecycle step (research/plan/validate). This is *unit-shape*-driven, again not edit-triggered.
3. **`always_use_skills` user preference** (`docs/user-docs/skills.md:99-114`). User declares "always load these skills" — equivalent to a static load-point but at user-config level, not triggered by editing a specific file.
4. **`skill_rules`** (`docs/user-docs/skills.md:108-114`). User-defined `when X then use/prefer/avoid Y` rules. The `when` is matched against context tokens — still not "before edit X" but the closest **rule-based** activation.

I did not find any pattern matching the form "if user touches file X, force-load doc Y." This is a negative finding with bounded coverage: I grep'd `"before edit\|load.*before\|trigger.*read\|doctrine.*load"` across `src/resources/skills/` and `docs/user-docs/skills.md` and found no hits matching the trigger-on-edit shape. I did not exhaustively read every skill body or every workflow template, so an unusual case could exist that this scan missed.

There is **no `AGENTS.md` or `CLAUDE.md` at the gsd-2 repo root** (verified by `find -maxdepth 2 -name AGENTS.md -o -name CLAUDE.md` — empty). `VISION.md` and `CONTRIBUTING.md` exist (read summary in §6). The `.gsd/` runtime directory is per-project, written by gsd-2 at runtime — the canonical doctrine surfaces are README + VISION + CONTRIBUTING + `docs/user-docs/`.

## §6 Doctrine layer (light-touch)

Where gsd-2 articulates opinions about how skills should work:

- **`VISION.md` (37 lines).** Three load-bearing claims for the skill subsystem: (1) **"Extension-first. If it can be an extension, it should be. Core stays lean. New capabilities belong in extensions, skills, and plugins unless they fundamentally require core integration"** (lines 9-11) — this is the architectural license for skills as the unit of capability extension. (2) **"Simplicity over abstraction"** with explicit rejection of "Enterprise patterns" (lines 13, 24-25). (3) **"Provider-agnostic"** (line 19) — skills follow the open Agent Skills standard precisely so they are portable across Claude Code, OpenAI Codex, Cursor, Copilot, Windsurf, etc. (`docs/user-docs/skills.md:5`).
- **`docs/user-docs/skills.md` (189 lines).** The user-facing reference. Documents directory locations, installation via `npx skills add`, the auto/suggest/off discovery modes, the preferences schema (`always_use_skills`, `prefer_skills`, `avoid_skills`, `skill_rules`, `skill_staleness_days`), the lifecycle (telemetry, health dashboard, staleness, heal-skill post-unit analysis). Key principle (line 188): **"skills are never auto-modified"** — research showed curated skills outperform auto-generated; human review is the gate.
- **`src/resources/skills/create-skill/SKILL.md` (175 lines).** The doctrine for *authoring* skills. Five essential principles: skills are prompts; SKILL.md is always loaded; router pattern for complex skills; pure XML structure (no markdown headings in body); progressive disclosure (≤500 lines, split to references/). Description-as-discoverability-signal is the most load-bearing claim for our purposes (cross-referenced in `spike-wrap-up:58`: "Description (frontmatter): one sentence, 120–1024 chars, keyword-rich. Must state when the agent should load it. Rewrite at least twice before settling.").
- **`README.md`** (only grep'd, not full read). Headlines include "Unified component system — skills, agents, pipelines, and marketplace are now one component model" (line 42), "Per-unit-type skill manifest resolver (#4779)" (line 46), "Skills overhaul — 30+ skill packs covering major frameworks, databases, and cloud platforms" (line 182).
- **`CONTRIBUTING.md`** — only one skill mention I caught: line 354, "Bug fixes must include a regression test that fails before the fix and passes after... See the `test-first-bugfix` skill." (Note: this skill is referenced but I did not verify it exists in the codebase under that name — could be aspirational or shipped under a different name.)

## §7 Implications for Phase D Step 1 design-space framing

### What shapes are licensed by the skill subsystem

The skill subsystem licenses (binding-evidence-supported) at least these artifact shapes for "decision-trace skill/workflow":

1. **Single SKILL.md skill** at `~/.agents/skills/decision-trace/SKILL.md` (or project-local `.agents/skills/decision-trace/SKILL.md`) — pure-prompt instructions the model invokes by description-keyword match.
2. **Router-pattern skill** at `~/.agents/skills/decision-trace/SKILL.md` + `workflows/`, `references/`, `templates/`, `scripts/` subdirectories. Allows progressive disclosure if decision-trace has multiple sub-flows (capture, audit, evaluate).
3. **Skill + markdown-phase workflow template pair.** Skill at `~/.agents/skills/decision-trace/SKILL.md` referencing a workflow template at `src/resources/extensions/gsd/workflow-templates/decision-trace.md` (host-side install) — phase-by-phase decision-trace dispatch handled by the prompt-dispatch engine.
4. **Skill + YAML deterministic workflow.** Same as 3 but with `decision-trace.yaml` — appropriate if the trace has explicit deterministic steps (e.g., write trace file → run audit → record predictions → schedule evaluation reminder) that benefit from engine-level dependency tracking and verification policies.
5. **Slash-command** at `~/.claude/commands/gsdr/decision-trace.md` (the `/gsdr:*` family). Same shape as `/gsdr:deliberate`. Carries `allowed-tools`, `argument-hint`, full workflow body inline. Note: this is **not in the gsd-2 codebase**; it is a Claude Code slash-command, packaged with `get-shit-done-reflect`.
6. **`.gsd/DECISIONS.md` extension.** Don't add a new artifact at all — extend the existing one-liner convention. Several existing skills already write to it; a "decision-trace" capability could be policy + tooling around populating, structuring, and reading that file.
7. **Hook-pattern (no source-of-truth analog found).** A "before-edit-X-load-Y" hook would be a *new* primitive in gsd-2 — there's no existing surface that fires on file edits. (Patches to `auto-prompts.ts` could simulate via context-token enrichment, but that's still token-driven, not edit-driven.)

### Existing-primitive overlaps suggest extension-vs-replacement-vs-orchestration

- **Replacement risk is high for shape 5 (slash-command):** `/gsdr:deliberate` already exists as a slash-command and already implements deliberation-with-predictions-and-evaluation. A new `/gsdr:decision-trace` slash-command would have to articulate why it doesn't simply extend `gsdr:deliberate`. **H3 verdict: existing primitives strongly cover this** — proposing shape 5 as new requires explicit gap-finding vs `/gsdr:deliberate`.
- **Extension is natural for shapes 1-4 (gsd-2 internal skills/workflows):** the gsd-2 codebase has the *capability slot* for a skill or workflow template, but no skill currently labeled "decision-trace." The closest is `spike-wrap-up` (decision-packaging) and `design-an-interface` (decision-capture-into-DECISIONS.md). A new `decision-trace` skill would compose with these rather than replace them.
- **Orchestration for shape 6 (DECISIONS.md):** the loosest, most composable shape — every existing decision-touching skill already writes there. A "decision-trace" capability could be a *thin orchestration layer* (richer schema, querying, cross-referencing) over the existing convention rather than a new artifact type.

### H2 R-strategy assessment per shape

R-strategies (per the gsd-2-uplift §7.10 framework — restating here from probe context, not from a binding source I read):
- **R2** = extend a gsd-2 surface in-tree
- **R4** = build outside gsd-2 (skill/workflow/slash-command lives elsewhere, doesn't modify gsd-2)
- **R5** = build elsewhere and *contribute upstream* later

| Candidate shape | R-strategy preliminary read | Reasoning |
|---|---|---|
| 1. Single SKILL.md (user-side `~/.agents/skills/decision-trace/`) | **R4-by-construction** | The skill lives in `~/.agents/skills/`, not in gsd-2's `src/resources/skills/`. gsd-2 discovers it at runtime; no codebase modification required. The H2 concern is correct here. |
| 1b. Single SKILL.md (in-tree at `src/resources/skills/decision-trace/`) | **R2** | Modifies gsd-2's bundled skills; ships with the next gsd-2 release. |
| 2. Router-pattern skill (user-side) | **R4-by-construction** | Same as 1 — directory-local. |
| 2b. Router-pattern skill (in-tree) | **R2** | Same as 1b. |
| 3. Skill + markdown workflow template (user-side workflow at `~/.gsd/workflows/`) | **R4-by-construction** for both halves | Workflow templates also have a user-side path (`~/.gsd/workflows/<name>.yaml` per `create-workflow/SKILL.md`). |
| 3b. Skill + markdown workflow (in-tree) | **R2** | Both halves modify gsd-2. |
| 4. YAML deterministic workflow (in-tree) | **R2** | Adds to `src/resources/extensions/gsd/workflow-templates/`; possibly registry update. |
| 4b. YAML workflow (user-side at `.gsd/workflows/<name>.yaml` project-local OR `~/.gsd/workflows/<name>.yaml` global) | **R4-by-construction** | Per `create-workflow/SKILL.md`, "Project plugins: `.gsd/workflows/<name>.yaml` (preferred — checked into repo). Global plugins: `~/.gsd/workflows/<name>.yaml`." |
| 5. Slash-command at `~/.claude/commands/gsdr/decision-trace.md` | **R4** with respect to gsd-2 (the `~/.claude/commands/gsdr/` location is not in gsd-2-explore at all) | But **R2 with respect to `get-shit-done-reflect`** — the slash-command's actual source is the `get-shit-done-reflect` repo, not gsd-2. **This is a decisive H2 finding: if the candidate shape is a slash-command, the relevant codebase is `get-shit-done-reflect`, not gsd-2.** That repo wasn't probed here. |
| 6. `.gsd/DECISIONS.md` policy/schema | **R2 (touches gsd-2 skills that write to it)** + **R5 (likely useful upstream)** | The convention already exists in gsd-2. Enriching it requires touching `design-an-interface`, `write-milestone-brief`, `spike` workflow — all in `src/resources/`. |
| 7. Hook (before-edit triggers) | **R2 (would require gsd-2 core changes)** | No existing hook surface; would need a new primitive in gsd-2 itself. Most invasive. |

**H2 verdict:** the original Phase D disposition (R2-shaped on the skill subsystem) is **plausible only for shapes 1b/2b/3b/4 — i.e., in-tree gsd-2 work.** For user-side / project-local shapes (1/2/3/4b) and the slash-command shape (5), R4-by-construction is more accurate. The skill subsystem's deliberate design — global location at `~/.agents/skills/`, project location at `.agents/skills/`, user-config-driven activation — *invites* R4-by-construction for most shapes. R2 only applies when the candidate ships *with gsd-2 itself*.

**H1 verdict:** the architectural shape is genuinely undefined — at least 7 shapes are licensed by the skill subsystem, plus the slash-command shape outside it. Phase D Step 1 needs to disambiguate which shape (or shapes) the candidate framework should evaluate.

## §8 Open questions

Things noticed but not investigated; flagging for Phase D entry audit:

1. **`get-shit-done-reflect` repo not probed.** All `/gsdr:*` slash-commands live there. If a candidate decision-trace shape is "extend `/gsdr:deliberate`" or "add `/gsdr:decision-trace`," the relevant codebase is `get-shit-done-reflect`, not gsd-2. M2 deliberately scoped to gsd-2 per the probe brief; an M3-equivalent of `get-shit-done-reflect` may be worth.
2. **Relationship between the gsd-2 internal `/gsd:*` commands and `get-shit-done-reflect`'s `/gsdr:*` commands.** Both exist in the user's available-skills list. The gsd-2 codebase contains `commands/` (e.g., `commands-bootstrap.ts`, `commands-handlers.ts`) referencing GSD-WORKFLOW.md. The relationship between `/gsd:audit-milestone` (gsd-2 internal) and `/gsdr:audit-milestone` (gsdr separate) was not investigated.
3. **`heal-skill` / skill-health subsystem** (`docs/user-docs/skills.md:184-188`, `src/resources/extensions/gsd/skill-health.ts`). Not read in detail. If a decision-trace skill is auto-evaluated via heal-skill, that's a relevant surface. Specifically: are there hooks for "skill X was used and produced bad outcome — flag for review"?
4. **`gsd:deliberate` predictions evaluation loop completeness.** The deliberate command documents `open` → `concluded` → `adopted` → `evaluated` lifecycle. Whether the actual `--continue <slug>` resume path fully implements evaluation (vs being aspirational) was not verified by reading the resume-mode code path of the workflow.
5. **`unit-context-manifest.ts` Phase 2-4 status.** The file's header (lines 14-26) describes a phased rollout — Phase 1 ships type+data+CI guard; Phase 2 introduces `composeSystemPromptForUnit()`, etc. Whether subsequent phases have landed and what the current composer-vs-direct-prompt split looks like was not investigated.
6. **`.gsd/DECISIONS.md` schema.** I confirmed the file is appended to by `design-an-interface`, `write-milestone-brief`, and the spike workflow's wrap-up offer. The actual line shape (one-liner per `write-milestone-brief:74`: `- YYYY-MM-DD [MID]: <decision> — <one-line rationale>`) was confirmed at one site; whether all writers use the same schema was not exhaustively checked.
7. **`mcp-server`'s `workflow-tools.ts`** (file mentioned `/gsdr:` per grep but not read). Could be a relevant surface if decision-trace is exposed via MCP tools. Out of probe scope, flagging.
8. **Skill staleness / lifecycle implications for decision-trace.** A "decision-trace" skill that captures past decisions could conflict with the staleness-based deprioritization (`skill_staleness_days`) — old decisions matter; old skills are deprioritized. Whether the gsd-2 design accommodates "evergreen" skills was not probed.
9. **`gsd-orchestrator/SKILL.md` is at the repo root, not in `src/resources/skills/`.** Suggests there may be other skill-shaped artifacts outside the main resources tree. Not exhaustively searched.
10. **`heal-skill` writes to `.gsd/skill-review-queue.md` for human review** (per `docs/user-docs/skills.md:184-188`). This is a "decision-relevant" artifact (skill modification proposals). Relationship to a hypothetical decision-trace surface was not investigated.
