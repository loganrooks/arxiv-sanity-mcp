---
type: pre-D-probe-findings
probe: P5
date: 2026-04-30
gsd_2_commit: 42ef05fbe
scope: |
  Three effective-state-emission surfaces in gsd-2: (1) `prefs` command, (2)
  `headless query`, (3) MCP tool catalog. Question: do they emit complete
  effective state, or are there silent drift gaps (docs say configurable, source
  shows defaulted-without-emission, hard-coded, or simply not surfaced)?
time_budget: ~75min spent (within 60-90min budget)
status: |
  Calibrated. Binding-evidence claim per surface: prefs/headless-query/MCP all
  examined at source level with file:line citations. Drift severity verdict
  delivered with explicit grounds; sub-areas left as "spot-check" labelled.
---

# P5 — Effective-state-emission probe findings

## §0 Summary

Drift detected across all three surfaces, severity moderate-leaning-severe (see §5
for calibration). The headline finding: **gsd-2 has no machine-readable surface
that emits its full effective state — preferences, active hooks, active skills,
isolation mode, model assignments, and extension registrations are loaded
internally for behavior gating but are not exposed via `prefs`, `headless query`,
or the MCP catalog.** The most acute drift is a documented capability that source
does not deliver: `docs/user-docs/configuration.md:12` claims `/gsd prefs status`
shows "current preference files, **merged values**, and skill resolution status,"
but the source handler (`commands-prefs-wizard.ts:241-269`) emits only file paths
and skill resolution counts — no merged values. For Phase D's decision-trace
first-target, this is load-bearing because reconstructing WHY decisions were
made over a project's lifetime requires reading the runtime configuration that
shaped those decisions, and that runtime configuration is largely silent at the
emission surfaces the skill would naturally consult. §7.9.3 (b) P5 failure-branch
sub-option (ii) — mild-to-moderate-drift-as-documented-caveat — is the
recommended call (see §6).

## §1 Method

### What I read (binding evidence)

- **Surface 1 (prefs):** Full read of `src/resources/extensions/gsd/preferences.ts`
  (638 lines) including `loadEffectiveGSDPreferences()`, mode/profile defaults,
  and the merge layering. Targeted read of `commands-prefs-wizard.ts:1-272`
  (covers `handlePrefs` and the `status` branch). Cross-checked
  `docs/user-docs/configuration.md:1-60`. Cross-referenced bootstrap/catalog
  registrations in `commands-bootstrap.ts:147` and `commands/catalog.ts:160`.
- **Surface 2 (headless query):** Full read of `src/headless-query.ts` (173 lines).
  Read of `src/headless-types.ts` (40 lines) for `HeadlessJsonResult` shape.
  Cross-checked `src/headless.ts:340-353` (query command dispatch) and
  `src/headless-events.ts:107-119` (`prefs` is registered as a quick-command).
  Read `GSDState` interface at `src/resources/extensions/gsd/types.ts:238-256`.
  Cross-checked prior precedent finding in
  `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md:88`.
- **Surface 3 (MCP):** Full read of `src/mcp-server.ts` (179 lines, the generic
  agent-tool transport). Targeted read of `packages/mcp-server/src/server.ts`
  (header + `readProjectState` + `gsd_progress`/`gsd_query`/`gsd_doctor`/
  `gsd_captures`/`gsd_knowledge` registrations, ~lines 1-260, 685-1080). Read of
  `packages/mcp-server/src/readers/state.ts:19-30` for `ProgressResult` shape.
  Read of `packages/mcp-server/src/workflow-tools.ts:606-642, 1352-1410,
  1790-1825` (tool name list + `gsd_milestone_status` impl + `gsd_journal_query`
  impl). Grep for any `gsd_prefs`/`gsd_skills`/`gsd_hooks`/`gsd_extensions`/
  `gsd_state` (none found).

### What I deliberately didn't read

- The full `commands-prefs-wizard.ts` (1835 lines) past line 300 — the wizard
  branches that don't touch `status` emission are out of scope for "what does
  prefs emit?" since they only mutate.
- The full `packages/mcp-server/src/workflow-tools.ts` (1950 lines) — confirmed
  all 29 workflow tool registrations by scanning the `WORKFLOW_TOOL_NAMES`
  enumeration and spot-checked a few; did not read every handler body.
- The `web/` UI services (e.g. `src/web/settings-service.ts:144` does
  `JSON.stringify({preferences, ...})`) — that's the desktop UI surface, not the
  CLI/MCP surfaces in scope.
- I did not run gsd-2 to observe runtime emission. All findings are
  source-citation-binding, not runtime-trace-binding.
- I did not check the VS Code extension surfaces (`vscode-extension/`).
- I did not check `gsd-orchestrator/` reference docs against current source —
  the prior precedent (`capabilities-production-fit-findings.md`) already
  established the orchestrator-docs source.

### Spot-check vs binding-evidence calibration

- **Surface 1 binding-evidence:** I traced the prefs subsystem from CLI command
  registration → `handlePrefs` dispatcher → `status` branch → emission output.
  All three of `loadEffectiveGSDPreferences`, `handlePrefs/status`, and the
  documented description in `configuration.md` were read directly. **Binding.**
- **Surface 2 binding-evidence:** I traced `gsd headless query` from
  `headless.ts:349-353` → `headless-query.ts:120-173` → its single emission
  point at `process.stdout.write(JSON.stringify(snapshot)+'\n')`. The full
  `QuerySnapshot` type was read. **Binding.**
- **Surface 3 binding-evidence:** I confirmed the README's own "6 read-only MCP
  tools" claim (`README.md:179`) matches exactly the registered tools in
  `server.ts`. I confirmed by name-grep that no `gsd_prefs` / `gsd_skills` /
  `gsd_hooks` / `gsd_extensions` / `gsd_state` MCP tool exists. **Binding for
  absence-claim**, since the registration list is enumerated and complete in
  one file.
- **Spot-check (not deeply traced):** I did not test whether
  `loadEffectiveGSDPreferences()` itself silently drops keys it can't parse;
  the prior `capabilities-production-fit-findings.md` already documented one
  docs/source drift in `git.isolation` team default (see §A.6 of that file),
  which suggests *internal* loading correctness can also drift from documented
  defaults. That's adjacent to my probe but not the emission question per se.

## §2 Surface 1: `prefs`

### Findings

- **What `prefs status` actually emits** (`commands-prefs-wizard.ts:241-269`,
  binding):
  ```
  GSD skill prefs — global <present|missing>: <path>; project <present|missing>: <path>
  Skills: <N> resolved, <M> unresolved
  Unresolved: <names>
  ```
  That is the entire output. It is text-formatted (not JSON), routed through
  `ctx.ui.notify`. It does NOT emit:
    - The merged effective preferences object
    - Active mode (solo/team) — even though source loads it
    - Active token_profile, models per phase, isolation, hooks, etc.
    - Profile/mode default layering — these are silent (see below)

- **Documentation drift** (`docs/user-docs/configuration.md:12`, binding):
  Doc claims `/gsd prefs status` shows "current preference files, **merged
  values**, and skill resolution status." Source emits only paths + skill
  counts. **The "merged values" claim is false against current source.**

- **Source/source drift between description fields** (`commands-bootstrap.ts:147`
  and `commands/catalog.ts:160`, binding): The in-source command catalogs
  describe `prefs status` as `"Show effective preferences"` — same false claim
  as user-docs. So the drift is doubled: in-source catalog descriptions
  promise behavior the in-source handler does not deliver.

- **Hidden default layering** (`preferences.ts:178-198`, binding): The merge
  pipeline is:
  ```
  global PREFERENCES.md
    → merged with project PREFERENCES.md (project wins per-key on scalars; arrays concat)
    → merged with token-profile defaults (lowest priority)
    → merged with mode (solo/team) defaults (lowest priority)
  ```
  An effective preference can be set by ANY of: explicit project, explicit
  global, profile defaults (`preferences-models.ts:resolveProfileDefaults`), or
  mode defaults (`MODE_DEFAULTS` in `preferences-types.ts`). A user reading
  their `PREFERENCES.md` file alone cannot determine the effective value for
  any field that was filled by profile or mode defaults.

- **Where `loadEffectiveGSDPreferences()` IS called** (binding from grep): 30+
  call-sites across `auto-post-unit.ts`, `dashboard-overlay.ts`, `doctor*.ts`,
  `auto-verification.ts`, `commands-cmux.ts`, `state.ts`, `guided-flow.ts`,
  `auto-worktree.ts`, `slice-cadence.ts`, `quick.ts`, `worktree-resolver.ts`,
  etc. — i.e., effective preferences shape behavior pervasively but are never
  emitted at any user-facing surface in JSON form (except indirectly through
  the web UI's `settings-service.ts:144`).

### Caveats

- I did not verify whether `validatePreferences()` (referenced from
  `preferences.ts:36`, body in `preferences-validation.ts`) silently drops
  unknown keys. If it does, that adds a *fourth* drift vector below the merge
  pipeline (parse-time silent-drop). Spot-check, not binding.
- The web UI does emit a JSON `{preferences, routingConfig, budgetAllocation,
  routingHistory, projectTotals}` payload (`src/web/settings-service.ts:144`,
  binding) — so the *capability* exists internally; it's just not surfaced
  through prefs/headless/MCP.

### Severity (Surface 1): **moderate**

Drift is real, documented, and load-bearing for any caller (skill, agent, human)
that needs to know the effective configuration. The fix-shape is small (emit
JSON of merged prefs at `prefs status` or add a flag). No actively misleading
emissions — the lie is one of *omission*.

## §3 Surface 2: `headless query`

### Findings

- **What `headless query` actually emits** (`headless-query.ts:93-111, 165-171`,
  binding): A single JSON line to stdout containing exactly:
  ```
  {
    state: GSDState,           // activeMilestone/Slice/Task, phase, blockers, nextAction, registry, progress
    next: { action, unitType?, unitId?, reason? },
    cost: { workers: [...], total: number }
  }
  ```
  `GSDState` (per `types.ts:238-256`) does NOT include preferences, hooks,
  skills, isolation mode, models, or extension registrations. The query CLI
  takes no arguments to select fields (`headless.ts:349-353`).

- **The implementation deliberately loads preferences but does not emit them**
  (`headless-query.ts:139-146`, binding):
  ```typescript
  const loaded = loadEffectiveGSDPreferences()
  const dispatch = await resolveDispatch({
    basePath, mid: ..., midTitle: ..., state, prefs: loaded?.preferences,
  })
  ```
  Preferences shape `next` (the resolved next-dispatch action), but the
  preferences themselves are dropped on the floor before stdout emission.

- **Documentation alignment is partial-truthful** (per
  `gsd-orchestrator/references/json-result.md:1-38`, cited in prior probe at
  `capabilities-production-fit-findings.md:88`): That reference describes
  `HeadlessJsonResult` (the *batch-mode `--output-format json`* shape), not
  `headless query`'s `QuerySnapshot`. They are different surfaces with
  different shapes. `HeadlessJsonResult` (binding from `headless-types.ts:20-39`)
  emits status, exitCode, sessionId, duration, cost (token-detailed), toolCalls,
  events, milestone, phase, nextAction, artifacts, commits — but again, no
  preferences, hooks, skills, extensions.

- **`prefs` IS a quick-command in headless** (`headless-events.ts:107-112`,
  binding): `gsd headless prefs` is dispatched the same way as the interactive
  `/gsd prefs`, so it runs `handlePrefs` and inherits Surface 1's drift.

### Caveats

- I did not test running `gsd headless query` against a real `.gsd/` project. A
  runtime trace would binding-confirm that nothing else slips into stdout.
  That said, the source emission point is a single `process.stdout.write` so
  the source-evidence is high-confidence.
- I did not check whether `state` (from `deriveState()`) might *partially*
  reflect preferences (e.g., if isolation mode shows up under `activeWorkspace`).
  Spot-check: `activeWorkspace` is a string field but I did not trace its
  population code path.

### Severity (Surface 2): **moderate**

Drift is "no surface where one should exist" rather than "surface lies." For a
CI/orchestrator/skill that needs effective state, the answer is "you can't get
it from `headless query` alone — you'd need to combine it with reading
`PREFERENCES.md` files and re-implementing the merge pipeline." The cost of
this drift is high for any skill that wants to be runtime-correct.

## §4 Surface 3: MCP tools

### Findings

- **The MCP tool catalog** (binding, enumerated):
  - **Session tools (6):** `gsd_execute`, `gsd_status`, `gsd_result`,
    `gsd_cancel`, `gsd_query`, `gsd_resolve_blocker`
  - **Interactive tools (2):** `ask_user_questions`, `secure_env_collect`
  - **Read-only tools (6+1):** `gsd_progress`, `gsd_roadmap`, `gsd_history`,
    `gsd_doctor`, `gsd_captures`, `gsd_knowledge`, `gsd_graph`
  - **Workflow tools (29):** decision/requirement save+update; milestone
    plan/complete/validate; slice plan/complete/replan/skip; task plan/complete;
    save_gate_result; reassess_roadmap; **`gsd_milestone_status`**,
    **`gsd_journal_query`**; memory tools (`gsd_capture_thought`,
    `gsd_memory_query`, `gsd_memory_graph`); plus aliases.
    (Source: `WORKFLOW_TOOL_NAMES` at `workflow-tools.ts:606-642`.)

- **NO MCP tool exposes effective preferences, active skills, active hooks,
  active extensions, or isolation mode** (binding from grep): No `gsd_prefs`,
  `gsd_skills`, `gsd_hooks`, `gsd_extensions`, or `gsd_state` tool exists.

- **The closest analogues do not cover effective state** (binding):
  - `gsd_progress` reads parsed STATE.md text → `ProgressResult`
    (`readers/state.ts:19-30`): activeMilestone/Slice/Task, phase, counts,
    blockers, nextAction. No prefs/hooks/skills.
  - `gsd_query` returns raw STATE.md, PROJECT.md, REQUIREMENTS.md text plus a
    milestone listing (`server.ts:196-249`). The `query` enum accepts
    `state|status|project|requirements|milestones` — nothing for prefs.
  - `gsd_milestone_status` is scoped to a single milestone
    (`workflow-tools.ts:1796-1809`).
  - `gsd_doctor` runs structural health checks on `.gsd/`
    (`server.ts:990-1005`); does not emit prefs (it only validates them
    internally per `doctor.ts:352-372`).

- **`gsd_progress` and `headless query` use *different* code paths to derive
  state** (binding):
  - `gsd_progress` parses STATE.md text via regex (`readers/state.ts`).
  - `headless query` calls `deriveState()` (the live state engine in
    `state.ts`).
  - These two surfaces can diverge if STATE.md is stale relative to the live
    engine. This is a *separate* drift vector — not directly an
    effective-state-emission gap, but it means there are two "state" surfaces
    that don't share an emission contract.

- **README claim is technically correct but understated** (`README.md:179`,
  binding): "MCP server — 6 read-only project state tools for external
  integrations." The count is right; the docs don't claim those 6 tools cover
  preferences. So Surface 3 has the *least* doc/source drift — but it has the
  most "missing surface" pressure: an external MCP client cannot ask gsd-2
  "what is your current effective state?" via any single tool.

### Caveats

- I did not deeply read all 29 workflow tool handler bodies; I read the type
  signatures and a sample. There could be a tool that emits prefs as a side
  effect of another operation, but the tool *names* don't suggest it and the
  ones I sampled do not.
- The MCP server is two server files: `src/mcp-server.ts` (generic
  agent-tool transport) and `packages/mcp-server/src/server.ts` (project-state
  tools). I read both; the former is just an SDK adapter and exposes whatever
  tools its caller passes in.
- I did not check whether any sub-package (e.g. `extensions/`) registers
  additional MCP tools at runtime. Spot-check — would require runtime trace.

### Severity (Surface 3): **moderate-to-severe** for the decision-trace use case

For Phase D's decision-trace first-target specifically, this is the most
load-bearing gap. An external skill/agent that wants to reconstruct decision
context must call MCP tools to introspect the project — and there is no MCP
tool for "show me your effective preferences/skills/hooks." The skill would
either need to (a) read `~/.gsd/PREFERENCES.md` and `.gsd/PREFERENCES.md`
directly and re-implement the merge pipeline, or (b) shell out to
`gsd headless query` and accept that its output excludes prefs.

## §5 Drift severity assessment

### Per-surface severity

| Surface | Severity | Confidence | Grounds |
|---------|----------|------------|---------|
| `prefs` (Surface 1) | **moderate** | high | Documented capability ("merged values") not delivered by source; concrete file:line citations on both sides. |
| `headless query` (Surface 2) | **moderate** | high | "No surface where one should exist" — preferences are loaded by the implementation, used internally, then dropped before emission. |
| MCP tools (Surface 3) | **moderate-to-severe** *for decision-trace use case* | high | No MCP tool emits effective preferences/skills/hooks. README understates by omission rather than overclaiming. |

### Cross-cutting observations

- **All three surfaces share the same root cause**: gsd-2's effective-state is
  computed via a sophisticated layered merge (project + global + profile +
  mode defaults), but only *the inputs* (the PREFERENCES.md files) are visible
  on disk. The *output* of the merge is a derived runtime construct that is
  never persisted or emitted to a stable interface.
- **The `web/settings-service.ts:144` payload proves the capability exists
  internally** — gsd-2 *can* serialize effective prefs to JSON; that surface
  is just bound to the desktop UI, not to CLI/headless/MCP.
- **The drift is consistent with prior W1/W2 findings** (e.g., the `git.isolation`
  team-default drift in `capabilities-production-fit-findings.md:120`; the
  RTK and reassess-after-slice drift in `01-mental-model-output.md:155-159`).
  This probe extends the docs/source-drift class to the *emission* layer
  specifically.

### What would change the call

- **Down to mild**: If a single-line patch (e.g., `--json` flag on `prefs status`
  or a `--include=prefs` flag on `headless query`) would close the gap, the
  *fix shape* is small even if the *current state* is moderate. I did not
  attempt to author such a patch, so this is a hypothesis.
- **Up to severe**: If the validation layer (`validatePreferences`) silently
  drops unknown keys, then there is *also* a parse-time drift below the merge
  pipeline — a user could write a key that looks valid (matches doc syntax),
  the validator could drop it, and no emission surface would surface this.
  I did not verify this; if it holds, the severity climbs to severe.
- **Up to severe**: If the `gsd_progress` (parsed-STATE.md) and `headless query`
  (`deriveState`) state surfaces can return materially different "active phase"
  or "active milestone" answers under common conditions, that is a separate
  state-coherence drift that would amplify the decision-trace skill's
  reliability concerns.

## §6 Implications for Phase D first-target

### §7.9.3 (b) P5 failure-branch trigger

**My recommendation: sub-option (ii) — mild-to-moderate-drift documented as
caveat; do NOT re-scope or re-evaluate Phase D wholesale.**

Reasoning:

1. The drift class is *omission*, not active misdirection. None of the three
   surfaces lies about gsd-2's runtime; they just don't tell the whole story.
   For a decision-trace skill, this is correctable by design (the skill itself
   can read `PREFERENCES.md` files directly, or use the in-process API
   `loadEffectiveGSDPreferences`).
2. The drift is *pre-existing* — it was visible in W1/W2 outputs (`git.isolation`,
   RTK, reassess-after-slice) and represents a known characteristic of gsd-2's
   surface design rather than a Phase-D-specific blocker.
3. The drift is *bounded* — I confirmed by enumeration (not just spot-check)
   that no MCP tool emits prefs, that `headless query`'s output schema is
   exactly `{state, next, cost}`, and that `prefs status`'s output is exactly
   the 1-2 lines documented in §2. The skill design can plan around a known
   surface shape.
4. The drift would *not* be fixed by re-scoping Phase D. The decision-trace
   skill needs effective state, and gsd-2's lack of emission surface for
   effective state is invariant under any Phase-D scope change. The right
   response is for the skill design to inherit the caveat: "to read effective
   state, do X (read files directly) instead of Y (call MCP tool)."

Consequences for Phase D Step 1 design-space framing:

- **Required caveat in skill design:** the decision-trace skill cannot rely on
  `headless query` or MCP `gsd_progress`/`gsd_query` to retrieve effective
  preferences, hooks, skills, or extensions. It must either read the on-disk
  files (`~/.gsd/PREFERENCES.md`, `.gsd/PREFERENCES.md`) and re-derive the
  merge, or invoke an in-process API path.
- **Soft requirement for skill design:** the skill should explicitly capture
  the *layer attribution* (was a value set by project, global, profile, or
  mode default?) since the merge pipeline doesn't surface this. Decision-trace
  reconstruction needs to know which layer set a value, not just the final
  value.
- **Possible Phase-D tributary:** the design could optionally consider whether
  Phase D should also propose (independent of decision-trace) a small surface
  patch — e.g., `gsd headless query --include=prefs` or `/gsd prefs status
  --json` — but this should be a separate item, not gating the decision-trace
  first-target.
- **Watch-out:** the `gsd_progress`-vs-`headless query` state-coherence drift
  (§4) is a *separate* class of risk that the decision-trace skill should
  also acknowledge — picking one path consistently rather than mixing them.

## §7 Open questions (flag for Phase D entry audit)

These are noticed-but-not-investigated; they deserve flagging at audit but
should not block §6's recommendation.

1. **Validation-layer silent-drop hypothesis** (severity-amplifier):
   `preferences-validation.ts` is referenced from `preferences.ts:36` but I
   did not read it. If `validatePreferences()` silently drops unknown keys,
   that's a fourth drift vector below the merge pipeline. Worth a 15-min spot
   check at Phase D entry audit.
2. **`gsd_progress` vs `headless query` state-coherence**: these two surfaces
   use different code paths to derive "current state." Under what conditions
   can they diverge? Worth a focused probe before committing the skill to one
   surface.
3. **Web UI emission as a counterexample**: `src/web/settings-service.ts:144`
   does the JSON serialization gsd-2 lacks at CLI/MCP. Is there a reason it
   wasn't lifted into a shared surface? (If it's a deliberate scoping
   decision, that's important context for whether to propose a tributary patch.)
4. **Active skills resolution surface**: skills are resolved per-call via
   `resolveAllSkillReferences` (`preferences-skills.ts`), but I did not check
   whether the resolution result is cached or recomputed. If recomputed,
   "what skills are active" is ambient rather than persisted; that has
   implications for decision-trace.
5. **Extension registration emission**: `register-extension.ts:102-138` (cited
   in prior W1/W2) registers tools/shortcuts/hooks/etc. dynamically. There
   does not appear to be an emission surface that says "extension X is
   currently registered with handlers Y, Z." For decision-trace over
   multi-year project lifetimes, knowing which extensions were active at a
   given decision is potentially load-bearing. Not investigated in this probe.
6. **`gsd_orchestrator/` references vs current source**: the orchestrator
   reference docs at `gsd-orchestrator/references/` were the source for prior
   probe's emission claims. They describe `HeadlessJsonResult` accurately as
   of that probe, but I did not re-verify against current source for *this*
   probe (binding evidence here came from `headless-types.ts` directly, which
   matched). If those references are versioned/lagging, they could be a
   third drift surface — but that's an orchestrator-docs question, not a P5
   finding.
7. **Runtime-trace verification**: all findings here are source-binding, not
   runtime-binding. A 30-minute pass running `gsd headless query`, `gsd prefs
   status`, and `tools/list` against an MCP client on a real `.gsd/` project
   would convert source-binding to runtime-binding. Recommended but not
   required to act on §6's recommendation.
