---
type: agential-setup-audit
date: 2026-05-01
auditor: Claude Sonnet 4.5 (project-local explore-agent dispatch from Logan)
scope: How well-equipped is /home/rookslog/workspace/projects/arxiv-sanity-mcp/ for AI-assisted (Claude Code) development?
output_role: inventory + gap signals only — not interventions
not_covered: |
  Recommendations are intentionally absent. Whether and how to act on the gaps
  surfaced here is the orchestrator's call. This audit aims to make the
  decision space visible, not to pre-dispose it.
---

# Agential Development Setup Audit — arxiv-sanity-mcp

## §0. Summary at a glance

The project carries unusually heavy *doctrinal* infrastructure (paired audits, anti-pattern lists, deliberation discipline, methodology splits, ADR-citation rules) and unusually light *runtime/harness* infrastructure to enforce it. The doctrine documents exist, are coherent with each other, and are being honored at the human-driven layer (51 of 103 commits in the last 14 days are paired-audit / disposition / addendum work). Almost none of that doctrine is wired into hooks, slash commands, project-local agent definitions, or MCP-server access — it lives in flat Markdown that the orchestrator must remember to read.

Two patterns dominate the gap signals:

1. **Doctrine is enforced by Logan-the-orchestrator, not by the harness.** The hooks do generic GSD work (context warnings, conventional-commit checks, prompt-injection advisory) and one custom thing (postlude metadata stub, `downstream_live_wiring_not_shipped`). They do not surface project-specific anti-patterns, do not gate on closure-pressure language in agent output, do not auto-load doctrine load-points when triggers fire, and do not check ADR-against-current-work at deliberation boundaries — all of which AGENTS.md asks for.
2. **MCP and tooling are under-attached to the project.** Globally `serena`, `context7`, `philpapers`, `zlibrary`, `tavily`, `morphllm-fast-apply` are in `enabledMcpjsonServers`; locally none of them are loaded — `claude mcp list` shows only `sequential-thinking` plus four unauthenticated OAuth servers. The project has no `.mcp.json`. PostgreSQL is running locally and would be the obvious enrichment for a database-backed project; no MCP attachment exists. There is no philpapers/zlibrary attachment despite the substantive overlap with Logan's broader research-tool ecosystem.

What's working well: paired-audit cadence is real and consistent; AGENTS.md anti-pattern citations resolve correctly to LONG-ARC.md line numbers; the `adversarial-auditor-xhigh` and `trajectory-verifier` agent definitions are substantive (not stubs) and are being used regularly; the memory system is small but on-target (one entry caught a real audit-misframing failure mode and is the kind of correction that pays for itself); handoffs are dense and self-referential, which makes session-resumption reliable but also signals that *every* session pays a heavy onboarding cost in tokens.

The rest of this document inventories the pieces and surfaces gap signals without proposing interventions.

---

## §1. Project-local Claude config (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/`)

### Files (recursive)

```
.claude/
├── agents/                          (12 GSD-* agent definitions)
│   ├── gsd-codebase-mapper.md       16K
│   ├── gsd-debugger.md              38K
│   ├── gsd-executor.md              19K
│   ├── gsd-integration-checker.md   13K
│   ├── gsd-nyquist-auditor.md        5K
│   ├── gsd-phase-researcher.md      18K
│   ├── gsd-plan-checker.md          23K
│   ├── gsd-planner.md               43K
│   ├── gsd-project-researcher.md    16K
│   ├── gsd-research-synthesizer.md   7K
│   ├── gsd-roadmapper.md            17K
│   └── gsd-verifier.md              19K
├── commands/gsd/                    (32 slash-command stubs)
├── get-shit-done/                   (GSD framework v1.22.4 install)
│   ├── VERSION
│   ├── bin/gsd-tools.cjs            (CLI helper)
│   ├── references/                  (13 reference docs)
│   ├── templates/                   (24 templates + sub-dirs)
│   └── workflows/                   (~30 workflow scripts)
├── hooks/                           (3 GSD hooks)
│   ├── gsd-check-update.js          (background: npm view get-shit-done-cc)
│   ├── gsd-context-monitor.js       (PostToolUse: warns at 35%/25% remaining)
│   └── gsd-statusline.js            (statusline: model | task | dir | ctx-bar)
├── gsd-file-manifest.json           16K
├── package.json                     ({"type":"commonjs"})
├── scheduled_tasks.lock
├── settings.json                    (hook bindings)
└── settings.local.json              (2 permission allowances)
```

### Role of each piece

- **`agents/`** — 12 project-local copies of the global GSD agent set. Differ from `~/.claude/agents-disabled/` versions (e.g. `gsd-planner.md`, `gsd-executor.md`, `gsd-roadmapper.md` all show diffs). Several are project-only (no global counterpart): `gsd-codebase-mapper`, `gsd-debugger`, `gsd-integration-checker`, `gsd-nyquist-auditor`, `gsd-verifier`. **None** of these mention project-specific anti-patterns (closure pressure, single-reader framing, tournament narrowing, etc.) — they reference generic anti-patterns like "scavenger-hunt executors" and "horizontal layers". The project-specific anti-pattern list lives in `AGENTS.md:41-47` and `LONG-ARC.md:46-54`; the GSD agents are not wired to it.
- **`commands/gsd/`** — 32 slash-command stub files (`add-phase.md` through `verify-work.md`); each is a thin pointer to the matching workflow under `get-shit-done/workflows/`. These show up as `/gsd:*` in the command list. Project-local; not customized.
- **`get-shit-done/`** — Vendored GSD framework, version 1.22.4. The `references/` set carries durable conventions (git commit format, model-profile resolution, planning-config layout, verification patterns). The `templates/` set is the corpus the planner / executor / verifier write into.
- **`hooks/`** — Three hooks; only `gsd-context-monitor.js` runs on every PostToolUse (advisory message at 35% remaining, critical at 25%, debounced 5 calls). `gsd-check-update.js` fires once per session in the background. `gsd-statusline.js` powers the statusline (model, current task from todos file, dir, context bar with 16.5% autocompact buffer correction).
- **`gsd-file-manifest.json`** — GSD installer's tracking manifest (which files are vendored, their hashes).
- **`settings.json`** (project-local) — Wires SessionStart → `gsd-check-update.js` and PostToolUse → `gsd-context-monitor.js`. Nothing else. No `permissions`, no `enabledMcpjsonServers`, no `env`, no MCP entries. Path: `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/settings.json`.
- **`settings.local.json`** — Two narrow permission allowances: `Bash(mv ~/.claude/agents-disabled/gsdr-spike-runner.md ~/.claude/agents/)` and `Read(//home/rookslog/.claude/agents/**)`. Both relate to a one-time manual move of `gsdr-spike-runner` out of the disabled folder. Path: `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/settings.local.json`.
- **`scheduled_tasks.lock`** — Empty, present.
- **`package.json`** — Marks the dir as CommonJS for the hook scripts.

---

## §2. Settings.json — global + project-local + permissions

### Project-local `settings.json` (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/settings.json`)

```json
{
  "hooks": {
    "SessionStart": [{"hooks": [{"type": "command", "command": "node .claude/hooks/gsd-check-update.js"}]}],
    "PostToolUse":  [{"hooks": [{"type": "command", "command": "node .claude/hooks/gsd-context-monitor.js"}]}]
  }
}
```

Only the two GSD hooks listed in §1. No matchers, no permissions, no env, no MCP, no model defaults.

### Project-local `settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "Bash(mv ~/.claude/agents-disabled/gsdr-spike-runner.md ~/.claude/agents/)",
      "Read(//home/rookslog/.claude/agents/**)"
    ]
  }
}
```

Two narrowly-scoped allowances. `settings.local.json` is git-ignored by convention and these match a one-time manual op + a read of the global agents folder.

### Global `~/.claude/settings.json`

The global settings carry the heavier load. Highlights:

- **Permissions allowlist (~110 entries)** — generous Bash allowlist for routine tooling (Python/Node/Git/Docker/CUDA/etc.), broad Read/Edit/Write, MCP wildcards (`mcp__serena__*`, `mcp__sequential-thinking__*`, `mcp__context7__*`, `mcp__zlibrary__*`, `mcp__philpapers__*`).
- **Permissions deny (~20 entries)** — correctly scoped: `sudo:*`, `rm -rf ~`, `chmod 777`, `git push --force`, all `.env`/credential reads, `.git/**` writes, `__pycache__/**` edits.
- **Permissions ask (~15 entries)** — sensible: `curl http(s)://*` (network egress), `wget`, `nc`, `systemctl`, `git reset --hard`, edits to `.claude/settings.*` files.
- **`includeCoAuthoredBy: false`** — git commits don't get the `Co-Authored-By: Claude` trailer.
- **`enabledMcpjsonServers: ["serena", "sequential-thinking", "context7", "zlibrary"]`** — global default. Note: project-local `enabledMcpjsonServers` is `[]` (see §3) and the project's `hasTrustDialogAccepted: false` — meaning the project hasn't yet accepted the trust-dialog needed to inherit global MCP servers.
- **`effortLevel: "xhigh"`**, **`showThinkingSummaries: true`**, **`autoCompactEnabled: false`**, **`skipDangerousModePermissionPrompt: true`**, **`agentPushNotifEnabled: true`**, **`remoteControlAtStartup: true`**, **`spinnerTipsEnabled: true`**.
- **`statusLine`** → `bash /home/rookslog/.claude/statusline-command.sh`.
- **`env`**: `BASH_DEFAULT_TIMEOUT_MS=1800000`, `BASH_MAX_TIMEOUT_MS=7200000` (30min default, 2hr max).

### Global hooks (~/.claude/settings.json)

There are 5 SessionStart hooks, 1 Notification, 2 Stop, 2 PostToolUse, 3 PreToolUse. The substantive ones:

| Hook event | Script | Real work? |
|---|---|---|
| SessionStart | `gsdr-check-update.js` | yes — background `npm view get-shit-done-reflect version`, writes cache |
| SessionStart | `gsdr-version-check.js` | yes — compares project gsd-reflect version to installed, caches |
| SessionStart | `gsdr-ci-status.js` | yes — backgrounds CI status check |
| SessionStart | `gsdr-health-check.js` | yes — schedules a project-health re-check based on cache staleness |
| SessionStart | `gsd-session-state.sh` | **no-op for this project** — opt-in, requires `.planning/config.json:hooks.community=true` (this project has no `hooks` key) |
| Notification + Stop | `claude-notify.js` | yes — sends ntfy.sh push on attention-needed / stop; debounced 30s |
| Stop | `gsdr-postlude.js` | partial — appends `{ts, runtime, phase, postlude_fired:true, error_rate, direction_change, destructive_event, session_id}` to `.planning/measurement/session-meta-postlude/session-meta-postlude.jsonl`; `error_rate`/`direction_change`/`destructive_event` all read `not_computed_in_closeout_hook` / `downstream_live_wiring_not_shipped` (312 rows landed; the rows are stubs) |
| PostToolUse Bash\|Edit\|Write\|MultiEdit\|Agent\|Task | `gsdr-context-monitor.js` | yes — context warning at 35%/25% remaining (project also runs `gsd-context-monitor.js` at 35%/25% from project-local; the two are version-divergent variants doing the same thing) |
| PostToolUse Write\|Edit | `gsd-phase-boundary.sh` | **no-op for this project** — opt-in, `community: true` not set |
| PreToolUse Write\|Edit | `gsd-prompt-guard.js` | yes for `.planning/` writes — scans for prompt-injection patterns + invisible Unicode; advisory only (does not block) |
| PreToolUse Write\|Edit | `gsd-workflow-guard.js` | **no-op for this project** — opt-in, requires `hooks.workflow_guard: true` in `.planning/config.json`; not set |
| PreToolUse Bash | `gsd-validate-commit.sh` | **no-op for this project** — opt-in, requires `hooks.community: true`; not set |

**Net effect:** 4 of the 12 hooks listed are no-ops for this project because the project's `.planning/config.json` does not opt in to `community: true` or `workflow_guard: true`. The active hooks are: notification (push), context monitoring (the project gets *both* the project-local and global versions, which are slightly different threshold variants), session-start health/version/update background tasks, postlude metadata logging (stub fields), and prompt-injection scanning on `.planning/` writes.

**Are hooks doing real work?** Mostly yes — context monitoring, push notification, prompt-injection scanning are all real. But none of them are *project-specific*. The four most "project-aware" hooks (commit-format validation, phase-boundary STATE.md reminder, session-start STATE.md reminder, workflow-guard for direct edits) are gated behind opt-in flags and are silently disabled here. The postlude hook is wired but its "real" measurements (error_rate, direction_change, destructive_event) are explicitly TODO-marked in the data it writes.

---

## §3. MCP servers

### What's actually live in this project

Running `claude mcp list` in the project dir surfaces:

```
claude.ai Google Calendar  - ! Needs authentication
claude.ai Google Drive     - ! Needs authentication
claude.ai Gmail            - ! Needs authentication
claude.ai Canva            - ! Needs authentication
sequential-thinking        - ✓ Connected
```

Only `sequential-thinking` is operational. The four OAuth-based services are configured at global level but unauthenticated.

### What's configured but not loaded

- `~/.claude.json` top-level `mcpServers` defines only `sequential-thinking` as a local stdio MCP.
- `~/.claude/settings.json:enabledMcpjsonServers = ["serena", "sequential-thinking", "context7", "zlibrary"]` — these are *enabled* at the global level, but they require a `.mcp.json` at the project root to define their command/args (the typical pattern). Sister projects do this: `/home/rookslog/workspace/projects/scholardoc/.mcp.json` defines `serena` via `uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant`. This project has no `.mcp.json`.
- Project entry in `~/.claude.json:projects[...].enabledMcpjsonServers = []`, `disabledMcpjsonServers = []`, `hasTrustDialogAccepted = false`. The project hasn't completed the trust dialog, which is the gate for inheriting global MCP servers.
- Global `enabledMcpjsonServers` referenced from various sister projects: `serena`, `morphllm-fast-apply`, `philpapers`, `tavily`, `context7`, plus the four OAuth services. None are loaded here.

### Relevance gap

A research-discovery substrate inspired by arxiv-sanity sits squarely in Logan's broader scholarly-tool ecosystem:

- **`philpapers`** — Logan's own MCP server (mentioned in `~/CLAUDE.md` MCP list; appears in `~/.claude.json` as `mcp__philpapers__*` allowed). Direct relevance to arxiv-sanity-mcp's domain (papers). **Not loaded.**
- **`zlibrary`** — also Logan's. Less directly relevant to arxiv (open-access focus differs) but present in global allowlist. **Not loaded.**
- **`context7`** — third-party docs lookup. Generally useful for dependency-API exploration. **Not loaded.**
- **`serena`** — code-aware MCP for IDE assistants. Useful for codebase navigation. **Not loaded.**
- **`tavily`** — web search MCP. Could complement arXiv-paper recency / external-validation work. **Not loaded.**
- **PostgreSQL MCP** — none configured anywhere. The user's environment has PostgreSQL running on localhost. The project (per `CLAUDE.md`) has alembic migrations and a metadata-mirror pattern; database introspection during planning would be the obvious DB-side complement, but no postgres MCP is wired. The architecture is currently SQLite-only per Spike 001 / Spike 002 history (paths in `.planning/spikes/001-sqlite-vs-postgresql-scale/` and `002-backend-comparison/`), so postgres MCP wiring would only matter if the substrate moves to Postgres, which is one of the deliberation streams in `.planning/spikes/`.

The MCP attachment surface is the most under-utilized part of this project's setup relative to its stated scope.

---

## §4. Slash commands

### Project-local commands (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/commands/gsd/`)

32 commands, all GSD framework defaults:

```
add-phase, add-tests, add-todo, audit-milestone, check-todos, cleanup,
complete-milestone, debug, discuss-phase, execute-phase, health, help,
insert-phase, join-discord, list-phase-assumptions, map-codebase,
new-milestone, new-project, pause-work, plan-milestone-gaps,
plan-phase, progress, quick, reapply-patches, remove-phase,
research-phase, resume-work, set-profile, settings, update,
validate-phase, verify-work
```

Each is a thin frontmatter wrapper that delegates to the matching workflow file under `.claude/get-shit-done/workflows/`. None are customized for this project's discipline.

### Project-specific slash commands

**None.** The project has no commands for:

- dispatching a paired audit (cross-vendor codex + same-vendor adversarial-auditor-xhigh) — the dominant work pattern (51/103 commits in last 14 days)
- running an "ADR-against-current-work check at deliberation boundaries" (per AGENTS.md "ADR violation by gradual local-reasonable steps" counter-posture)
- ensuring an open question isn't being closed without authority (per AGENTS.md/CLAUDE.md "do not close Open Questions without authority")
- routing a doctrine-load-point trigger to the matching docs (per CLAUDE.md "Doctrine load-points")
- pattern-watching for closure-pressure language in agent output (per `LONG-ARC.md:51` and `spikes/METHODOLOGY.md` discipline D)

The `/gsdr:audit` skill (global, v1.19.10+dev) takes a 3-axis classification and dispatches `gsdr-auditor` (Sonnet) — but this isn't the project's paired-audit pattern, which is consistently `(cross-vendor codex GPT-5.5 high) ∥ (Claude Opus 4.7 adversarial-auditor-xhigh)`. The orchestration is currently done in-prompt-text, by hand, in each AUDIT-SPEC.md (5 of those exist in `.planning/gsd-2-uplift/audits/`).

---

## §5. Custom agents (project-local + global)

### Project-local agents (`.claude/agents/`)

12 GSD-framework-default agents listed in §1. None are project-customized (the diffs vs `~/.claude/agents-disabled/` are GSD version differences, not project-specific overrides). None reference `LONG-ARC.md`, `VISION.md`, or the project anti-pattern set.

### Global agents (`~/.claude/agents/`) directly relevant to this project's work pattern

- **`adversarial-auditor-xhigh.md`** — Same-vendor critical reviewer. Opus, xhigh effort. Used in 5 of the 7 `.planning/gsd-2-uplift/audits/*/AUDIT-SPEC.md` and named in 4 `.planning/audits/*` files. Substantive definition (60+ lines): prescribes 5-tier grounding hierarchy, `blocking`/`quality`/`taste` severity, `What-would-dissolve-the-finding` field, `Steelman residue` section, and explicit "you are subject to the same disciplines you apply" self-application clause. **This is the most heavily-used agent in the project.**
- **`gsdr-auditor.md`** — Sonnet, 3-axis-classification (subject × orientation × delegation) auditor. Receives a fully-formed task spec from `/gsdr:audit`. Has not been observed in the 7 audit specs — those all use `adversarial-auditor-xhigh` for same-vendor work.
- **`trajectory-verifier.md`** — Goal-backward verifier for trajectory-plan / deliberation-phase goal achievement. Designed for the gsd-2-uplift's `cheerful-forging-galaxy.md` trajectory plan and audit-arc / disposition / addendum patterns. Core principle: "Artifact production ≠ Goal achievement". Critical mindset: "Do NOT trust DISPOSITION.md / SUMMARY-section claims". Used for Phase B and Phase C verification per `2026-04-29-trajectory-plan-audit/.logs/codex-gpt55-xhigh.log` and the `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/`.
- **`knowledge-store.md`** — Reference spec for the GSD persistent knowledge store (`.planning/knowledge/`). Used as a reference, not a runner agent.
- **`gsdr-*` agents** — `advisor-researcher`, `artifact-sensor`, `assumptions-analyzer`, `ci-sensor`, `codebase-mapper`, `context-checker`, `debugger`, `git-sensor`, `integration-checker`, `log-sensor`, `nyquist-auditor`, `patch-sensor`, `reflector`, `signal-collector`, `signal-synthesizer`, `spike-runner`, `verifier`. Not directly observed in this project's audit-arc work; some may be invoked via `/gsdr:*` skills.

### Disabled agents (`~/.claude/agents-disabled/`)

14 GSD-framework agents (gsd-* and gsdr-*) sitting in the disabled folder. Globally disabled to avoid duplicating with project-local copies. The `gsdr-spike-runner.md` was moved out of disabled into `~/.claude/agents/` (the move is recorded as a permission allowance in `settings.local.json`).

---

## §6. Doctrine load-points — verification

`CLAUDE.md:30-36` lists 7 trigger → doc routings. Sampled and verified:

| Trigger | Cited docs | Exist? | Notes |
|---|---|---|---|
| Touching ranking, retrieval, or lens-architecture code | `LONG-ARC.md` (anti-patterns), `docs/adrs/ADR-0001`, `docs/adrs/ADR-0005` | yes — `.planning/LONG-ARC.md` (118 lines), `docs/adrs/ADR-0001-exploration-first.md`, `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` | bare `LONG-ARC.md` reference resolves only because LONG-ARC also lives at project root in convention; actual file is at `.planning/LONG-ARC.md` |
| Adding a new abstraction or signal type | `LONG-ARC.md` (protected seams), `VISION.md` (anti-vision section) | yes — protected-seams section is at `.planning/LONG-ARC.md:25-42` (heading `## Protected seams`); anti-vision section at `.planning/VISION.md:76-84` (heading `## Anti-vision — what we are not`) | line-anchor missing in CLAUDE.md but section names match |
| Touching MCP tool, resource, or prompt surfaces | `docs/adrs/ADR-0004`, `LONG-ARC.md` (MCP-native operations) | yes — `LONG-ARC.md:40` has the protected-seam "MCP-native operations" verbatim | resolves |
| Proposing changes to spike program structure or methodology | `.planning/spikes/METHODOLOGY.md`, `LONG-ARC.md` (doctrine-interaction-with-spike-program) | `spikes/METHODOLOGY.md` exists (190 lines); has practice-discipline sections A-F at `:104-167`. The "doctrine-interaction-with-spike-program" phrase doesn't grep-hit in LONG-ARC.md, but the conceptual content is present (section "Phase-Mapping" + sections discussing 005-008 chain) | semantic-match, not lexical-match |
| Editing `.planning/gsd-2-uplift/` artifacts | `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` | yes | resolves |

**Known minor issues:**

- The doctrine load-points use `LONG-ARC.md` and `VISION.md` as bare basenames without paths. The actual files are at `.planning/LONG-ARC.md` and `.planning/VISION.md`. New agents looking for these at the project root will not find them; convention search must include `.planning/`.
- `AGENTS.md:160` says: "When editing `LONG-ARC.md`, `VISION.md`, or the project root `CLAUDE.md` / `AGENTS.md`" — this implies LONG-ARC.md and VISION.md are at the project root. They're not. They are at `.planning/`.
- AGENTS.md anti-pattern citations like `(LONG-ARC.md:47)` resolve correctly: the anti-pattern bullet at LONG-ARC.md:47-53 matches the AGENTS.md text. Cite-back is consistent.
- `AGENTS.md:144` quotes `docs/adrs/ADR-0001-exploration-first.md:22` verbatim ("multiple retrieval and ranking strategies can coexist"); confirmed accurate.

---

## §7. AGENTS.md effectiveness

`AGENTS.md` (163 lines) covers:

- Mission (5 product values)
- "Do not do these things" (7 negations covering tags, dense retrieval, lexical retrieval, MCP-as-web-UI, paper-chat, license, hidden assumptions)
- Default working posture (5 items: keep design space open; prefer cheap defaults; preserve reversibility; record uncertainty explicitly; separate hypotheses from decisions)
- Project-specific anti-patterns to detect (7 patterns with verbatim cite-back to LONG-ARC.md:46-54)
- Required habits (mark commitment level; update right document; respect core constraints; prefer abstractions)
- Implementation bias (7 items)
- Pre-major-change checklist (6 questions)
- Definition of success (5 items)
- CONTEXT.md epistemic discipline (4 sub-disciplines: traceable vs derived; do-not-close-Open-Questions; ADR citations specific; no speculative product strategy)
- Deliberation boundaries (6 conditions for surface-and-propose)

### Concrete vs aspirational

Concrete and enforceable in principle:

- Status markers (Settled/Chosen-for-now/Hypothesis/Open) — actionable language test.
- "Update the right document" routing — checkable mechanically.
- ADR citations must quote the specific clause — checkable.
- Anti-pattern self-detection with cite-back — checkable.
- Deliberation-boundary triggers (e.g. "When modifying any accepted ADR's text, status, or scope") — well-defined.

Aspirational / unenforced by mechanism:

- "Calibrated language as default register" — culturally enforced; no lint-style detection.
- "Closure pressure at every layer" — flagged in pattern-watch but no automated detection.
- "Single-reader framing claims as authoritative" — counter-posture is paired review, but the dispatch is manual and ad-hoc per AUDIT-SPEC.md.
- "Tournament narrowing under disciplined framing" — pattern-watch only.

### Are they being respected per recent git history?

Last 30 commits are *entirely* in the `gsd-2-uplift/` thread (audit-arcs, dispositions, addenda, paired audits). Patterns visible in commit subjects:

- `audit` / `paired audit` / `cross-vendor` / `same-vendor` mentions in 51/103 commits over 14 days (~50%).
- "Phase D dispatch mid-arc — Step 6 + methodology + Option 4 + Option 5 + structural review" (`c0465a4`) — multi-option enumeration; no winner-pick.
- "Phase D mid-arc methodology-mismatch finding + (V'.a) trajectory-replan disposition" (`43e652b`) — pattern-watch caught a methodology mismatch mid-arc and triggered a replan rather than working around it. This is the AGENTS.md counter-posture for "When in doubt about whether a change qualifies, surface it" being honored.
- "G-3 follow-up — broaden doctrine-load-point trigger to cover STATE.md uplift-status edits" (`004a1a7`) — recursive doctrine maintenance: the doctrine load-point trigger itself was tightened based on an audit finding. Doctrine is being treated as living, not frozen.
- "EXTERNAL-VISION-CONTEXT.md + 12-property substrate-vision articulation + scope-discipline corrections" (`c1b098c`) — "scope-discipline corrections" suggests scope-creep was caught and named.

**Verdict:** AGENTS.md is being honored at a high level. The dominant work pattern — paired audit → disposition → addendum, with the `adversarial-auditor-xhigh` agent used consistently as the same-vendor reviewer — directly executes the M1 paired-review discipline that AGENTS.md and `LONG-ARC.md:53` ask for. The "calibrated language" discipline is harder to verify from commit messages alone, but the AUDIT-SPEC.md / DISPOSITION.md / VERIFICATION.md cadence visible in the audit folders is doing the work AGENTS.md asks for.

What's NOT happening: the doctrine load-points are not being *triggered* by the harness. They rely on Claude reading `CLAUDE.md` at session start and remembering them when triggers fire. That's a reliability ask of the model that the harness could shoulder but doesn't.

---

## §8. Memory system

Path: `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/memory/`

7 files (5 feedback, 1 reference, 1 index):

| File | Date | Theme |
|---|---|---|
| `MEMORY.md` | Apr 25 (6 days) | Index pointing at the others |
| `feedback_no_explore_for_audits.md` | Apr 25 (6 days) | Don't dispatch audits to default Explore agent without `model: "opus"` override; cost-test for known-quality model |
| `feedback_epistemic_rigor.md` | Mar 18 (44 days) | No premature conclusions; comparative claims need comparative data; no "fast enough" framing |
| `feedback_ask_before_modifying_external.md` | Mar 20 (42 days) | Don't modify `~/.claude/` runtime when development repo is at `~/workspace/projects/`; ask before cross-repo file ops |
| `feedback_methodology_and_philosophy.md` | Mar 26 (36 days) | Levinas/Said-Saying orientation: rigor as ethical response, traces over erasure, responsible positing, critique of premature closure; don't invoke philosophers by name in artifacts |
| `feedback_spike_process.md` | Mar 30 (32 days) | Formalize independent critique agents in spike workflow; separate designer/critic/executor; AI agent eval > AI list-review > pure metrics |
| `reference_spike_design.md` | Mar 26 (36 days) | Pointer to `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md` + deliberation constellation in `~/workspace/projects/get-shit-done-reflect/.planning/deliberations/` |

### Useful patterns

- **Feedback entries are origin-tracked** (e.g. `originSessionId: 4994da93-ebd1-4caf-bd5e-52ad12ab3122` in `feedback_no_explore_for_audits.md`) — preserves trace from session that produced the lesson.
- **Each feedback entry has a "How to apply" section** with concrete routing rules — not just complaints.
- **`feedback_no_explore_for_audits.md`** documents the most expensive feedback failure-mode caught: a Phase 3 property audit dispatched to default Explore (which read alembic migration 003 as current state, missing migration 005 dropping it) almost shipped a wrong roadmap framing; re-running with `model: "opus"` reversed the verdict. This is exactly the "single-reader framing claims as authoritative" anti-pattern in `LONG-ARC.md:53`.
- **Memory metadata** carries staleness warnings ("This memory is 36 days old. Memories are point-in-time observations…") — agents reading old feedback know to verify against current state. The 6-day-old entries are reasonably current; the 32-44-day ones predate v0.2 redirection and may need refresh.

### Gap signal

Memory has 7 entries total. The volume of audit/disposition work in the last 6 days (50+ commits in `gsd-2-uplift`) has produced multiple new methodological lessons (e.g. paired-vendor calibration discipline, attempt-1 codex hung on stdin discovery, recalibrating cross-vendor effort from xhigh→high per `2026-04-30-phase-d-entry-audit/AUDIT-SPEC.md`). None have landed in memory. The lesson-distillation pipeline appears to live in `DECISION-SPACE.md §1.17` ("lessons-distilled" sections) and audit POST-MORTEM.md files, rather than in the agent-readable memory at `~/.claude/projects/.../memory/`. Whether this is intentional (memory is for cross-project lessons, planning artifacts are for project-specific lessons) is not documented.

---

## §9. Audit / review infrastructure

### Agent definitions used

- `adversarial-auditor-xhigh` (global) — same-vendor reviewer. Used in 5 audit-specs and 4 standalone audits.
- `trajectory-verifier` (global) — goal-backward verifier for deliberation work.
- Cross-vendor: `codex-gpt55-high` and `codex-gpt55-xhigh` (the codex CLI dispatched as a Bash subprocess by the orchestrator; not a Claude Code agent).

### Cadence (last 14 days)

Looking at `.planning/gsd-2-uplift/audits/` (the active workstream):

| Date | Audit | Pattern |
|---|---|---|
| 2026-04-28 | `v1-gsd-mental-model-premise-bleed-audit` | Two-step conditional: codex GPT-5.5 high baseline; adversarial-auditor-xhigh same-vendor stress fires only if Step 1 returns Class-C candidates |
| 2026-04-28 | `cross-vendor-codebase-understanding-audit` | Cross-vendor only |
| 2026-04-29 | `incubation-checkpoint-audit` | Paired (cross-vendor codex GPT-5.5 + same-vendor adversarial-auditor-xhigh independent stress) per trajectory plan §2.4 row C + premise-bleed precedent |
| 2026-04-29 | `relationship-to-parent-audit` | Same-vendor adversarial only (Claude Opus, adversarial-auditor-xhigh agent type) |
| 2026-04-29 | `trajectory-plan-audit` | codex-gpt55-xhigh (cross-vendor) |
| 2026-04-30 | `phase-d-entry-audit` | Paired; same-vendor xhigh (Opus 4.7 adversarial-auditor-xhigh) + cross-vendor codex GPT-5.5 high (recalibrated from xhigh per Logan's calibration). Includes a documented attempt-1 failure where codex hung on stdin read for 37 minutes; root-cause documented at POST-MORTEM.md |
| 2026-05-01 | `trajectory-replan-audit` | codex GPT-5.5 xhigh (cross-vendor) |

The pattern holds through `.planning/audits/` (the v0.2 plan + governance audit cycle):

- 2026-04-25 v0.2 plan paired audit: codex high (cross-vendor) + Opus 4.7 high (same-vendor adversarial) + Opus 4.7 xhigh (rerun with adversarial-auditor-xhigh)
- 2026-04-26 governance paired audit: codex (cross-vendor) + Opus 4.7 xhigh (same-vendor adversarial-auditor-xhigh)

### Is paired-review at appropriate boundaries?

Yes — `AGENTS.md:151-162` specifies 6 deliberation-boundary triggers, and the `.planning/gsd-2-uplift/audits/` directory contains audits at most of those boundaries (Phase B entry, Phase C entry, Phase D entry, trajectory-replan, incubation-checkpoint). The paired-vendor pattern is consistently applied. The recent recalibration of cross-vendor effort from xhigh → high (per `2026-04-30-phase-d-entry-audit/POST-MORTEM.md` §7) shows the discipline is itself subject to revision when evidence accumulates — a sign the pattern-watch is working on the methodology too.

### Mechanical gaps

- **Audit dispatch is manual.** Each AUDIT-SPEC.md is hand-authored; the orchestrator types the prompt to invoke `adversarial-auditor-xhigh`, then separately dispatches the codex cross-vendor pass via Bash subprocess. The `/gsdr:audit` slash command exists but uses a different (3-axis) classification model and dispatches `gsdr-auditor` (Sonnet, not Opus xhigh). The project's actual paired-review pattern has no slash-command shortcut.
- **No automated paired-vendor reconciliation.** When both auditors finish, the orchestrator hand-writes a comparison artifact (`SYNTHESIS-COMPARISON.md`, `audit-findings-A.md` + `audit-findings-B.md` + manual differential).
- **No automated reading-frame contamination guard.** When dispatching the adversarial-auditor-xhigh, contamination from the cross-vendor output is prevented by manual prompt wording ("forbidden from reading [path]"). The 2026-04-25 v0.2 plan audit produced a `-xhigh-contaminated.md` and a `-xhigh.md` (independent) variant after the contaminated run was identified; the difference is documented in `2026-04-25-v0.2-plan-audit-comparison.md`.
- **Naming convention workaround.** Audit findings use `audit-findings-A.md` / `audit-findings-B.md` rather than `FINDINGS*.md` because `FINDINGS*` / `REPORT*` / `SUMMARY*` / `ANALYSIS*` basenames trigger Claude Code 2.1.123's `tengu_sub_nomdrep_q7k` regex and fail Write at the runtime layer (per `phase-d-entry-audit/AUDIT-SPEC.md`). This is a real, documented runtime workaround.

---

## §10. Friction points (`.planning/handoffs/`)

8 handoffs over 7 days (2026-04-25 → 2026-04-28). Each is dense (200-1500+ lines), self-referential, with a `predecessor` field. The patterns of friction visible:

### Recurring friction patterns mined from handoffs

1. **Recommendation flip-flopping in-session (`2026-04-27-post-stage-1-uplift-genesis-handoff.md`):**
   > "Pattern. Moving on a recommendation more than twice in a session signals unstable confidence. This session repeated harvest §10.9's earlier 4x flip-flop pattern with the cross-vendor dispatch."
   The user explicitly named this anti-pattern after observing 4x reversals on a single dispatch decision in a session.

2. **Closure pressure (rushing to dispatch) and opening pressure (always finding more to deliberate) — `2026-04-28-post-W1-and-framing-widening-handoff.md` §7.7:**
   > "Recurring failure mode: closure-pressure (rushing to dispatch); also opening-pressure (always finding more to deliberate). Both are dispositions Logan owns."
   Both are named as recurring; neither has a hook or check that catches them.

3. **Preflight setup forgotten before audit dispatch — `2026-04-28-post-W1...` §7.1:**
   > "Do NOT skip the gsd-2 setup preflight before dispatching audits. Per B.5 / B.6 pattern. The gsd-2 clone at `~/workspace/projects/gsd-2-explore/` is required for slice agents and auditors. Verify before dispatching."
   This is a "happens often enough to write it down" pattern.

4. **Auto-dispatching incubation-checkpoint or second-wave-scoping decisions Logan should own — `2026-04-28-post-W1...` §7.2:**
   > "Logan disposes. Per harvest §10.1 assumption #1 + DECISION-SPACE §0. The synthesis output flows to incubation-checkpoint deliberation; that deliberation is Logan-led, not Claude-auto."
   Recurring pattern of agent over-stepping into Logan-disposes territory.

5. **Synthesis collapsing back to a narrower frame — `2026-04-28-post-W1...` §7.3:**
   > "Do NOT collapse R1-R5 back to R1/R2/R3 in synthesis or downstream. The framing-widening explicitly preserves R4/R5 as named options."
   Tournament-narrowing anti-pattern (LONG-ARC.md:46) in micro form.

6. **Modifying read-only repo scope — `2026-04-28-post-W1...` §7.6:**
   > "Do NOT modify gsd-2 source. `~/workspace/projects/gsd-2-explore/` is a read-only target throughout this initiative."
   Cross-repo isolation.

7. **Auditor-misframing single-reader failure (memory `feedback_no_explore_for_audits.md`):**
   The Phase 3 property audit dispatched to default Explore agent with unverified model produced a wrong verdict by reading alembic migration 003 as current state, missing migration 005's drop. Caught by re-running with `model: "opus"`. The kind of failure mode the paired-review discipline exists to prevent.

8. **Onboarding cost is high and explicit — every handoff begins with a `onboarding_read_order` list of 7-13 documents. The `2026-04-28-post-W2-and-paired-synthesis-handoff.md` lists 13 read-order items, and the predecessor handoff itself is an additional document the new session may need to read. The reading-list size signals that fresh-session agents pay a substantial token cost just to reach the work surface.

### Friction patterns *not* mentioned but visible

- **The runtime keeps surfacing scheduling mismatches.** Handoffs reference codex hangs, cache invalidation issues, opt-in flags being unset, agent moves from disabled to active, and the `tengu_sub_nomdrep_q7k` Write-regex workaround. Each is small; cumulatively they suggest the harness isn't quite the right shape for the dispatch pattern the project relies on.
- **Doctrine maintenance is a substantial workstream of its own.** `004a1a7 docs(gsd-2-uplift): G-3 follow-up — broaden doctrine-load-point trigger to cover STATE.md uplift-status edits` shows a doctrine load-point trigger getting broadened mid-arc. The doctrine is alive, which is good; but the maintenance has no harness support — every change goes through CLAUDE.md / AGENTS.md hand-edit + paired-review.

---

## §11. Gap signals

These are surfaces where the agential setup is plausibly under-provisioned for what the project's doctrine asks for. No interventions proposed; the orchestrator will pick which (if any) of these are worth addressing.

### 11.1 No harness wiring of doctrine load-points

**Observed.** `CLAUDE.md:30-36` lists 7 trigger → doc routings ("touching ranking → LONG-ARC anti-patterns + ADR-0001 + ADR-0005"). These triggers fire by Claude reading CLAUDE.md at session start and remembering to apply the routing later. Nothing in the harness watches for the trigger and surfaces the docs.

**Mechanism that could exist.** A `PreToolUse` hook on Edit/Write that pattern-matches the file path or content keywords against the trigger set, and injects the matching doctrine docs as `additionalContext`. Conceptually similar to `gsd-prompt-guard.js` but routing forward instead of warning back.

**Why it might not exist.** The triggers are fuzzy ("touching ranking, retrieval, or lens-architecture code") and pattern-matching would produce false positives that train Claude to ignore the warning. The current model (Claude reads, Claude remembers) avoids the false-positive problem at the cost of relying on memory.

### 11.2 No automated detection of project-specific anti-patterns in agent output

**Observed.** AGENTS.md:41-47 lists 7 anti-patterns to detect. The counter-postures are ("name it; surface it to a deliberation rather than working around it"). Detection is the agent's job; there is no scanner.

The most-named ones in commits:

- closure pressure
- single-reader framing claims as authoritative
- tournament narrowing
- silent defaults
- ADR violation by gradual local-reasonable steps

**Mechanism that could exist.** A PostToolUse hook that scans agent output (assistant turns) for closure-pressure phrasings ("clearly", "obviously", "the obvious choice", "simply", "just", certain hedges-as-decoration, etc.) — could be regex-driven or call out to a smaller model. Same shape as `gsd-prompt-guard.js`.

**Why it might not exist.** Anti-pattern detection in natural-language output is hard to do well; false positives erode trust. The current model uses paired-review to catch these post-hoc.

### 11.3 No project MCP attachment file

**Observed.** No `.mcp.json` in the project root. `~/.claude.json:projects[arxiv-sanity-mcp].hasTrustDialogAccepted=false` and `enabledMcpjsonServers=[]`. The result is that `serena`, `context7`, `philpapers`, `zlibrary`, `tavily`, `morphllm-fast-apply` (all available globally) are not loaded for this project. Only `sequential-thinking` is live.

**Mechanism that could exist.** A `.mcp.json` matching the sister-project pattern (`scholardoc/.mcp.json`, `gsd-2-explore/.mcp.json`), enumerating relevant MCP servers. Plus accepting the trust dialog.

**Why it might not exist.** Possibly intentional minimalism; possibly oversight.

### 11.4 No PostgreSQL MCP

**Observed.** No postgres MCP exists in any of the project's MCP configs. PostgreSQL is running on localhost (`~/CLAUDE.md` "Running Services" table). The project is database-backed with alembic migrations; agents reading "current schema state" rely on grepping migration files (the `feedback_no_explore_for_audits.md` failure case).

**Mechanism that could exist.** Add a postgres MCP server to a project `.mcp.json` (e.g. `@modelcontextprotocol/server-postgres`) with a read-only connection to a local dev DB. Agents could then query `\d`, `\d+ tablename` directly instead of inferring from migrations.

**Why it might not exist.** The project is currently SQLite-only by spike conclusion; postgres is on the long-arc table but not committed. A postgres MCP would be premature if the architecture stays SQLite. SQLite MCP servers also exist (`@modelcontextprotocol/server-sqlite`); none configured either.

### 11.5 No dispatch-helper slash command for the project's paired-audit pattern

**Observed.** The project's dominant audit pattern is `(cross-vendor codex GPT-5.5 high) ∥ (Claude Opus 4.7 adversarial-auditor-xhigh)` with a hand-authored AUDIT-SPEC.md per audit (5 in `.planning/gsd-2-uplift/audits/` to date). The `/gsdr:audit` skill exists globally but uses a different (3-axis) shape and dispatches `gsdr-auditor` (Sonnet), not the project's actual pattern.

**Mechanism that could exist.** A project-local `/audit-paired` slash command that takes an artifact path + audit-frame and dispatches both the Bash codex subprocess and the `adversarial-auditor-xhigh` Task in one step, with anti-contamination prompting baked in.

**Why it might not exist.** The audit shape varies enough per audit (frame, lens-spec, recipient, attempt sequencing) that templating is non-trivial. The 5 existing AUDIT-SPECs differ in non-trivial ways.

### 11.6 Postlude metadata is wired but not yet measuring real signals

**Observed.** `gsdr-postlude.js` writes `~/.planning/measurement/session-meta-postlude/session-meta-postlude.jsonl` on every Stop event (312 rows landed). The interesting fields (`error_rate`, `direction_change`, `destructive_event`) all read `not_computed_in_closeout_hook` / `downstream_live_wiring_not_shipped`. The infrastructure exists; the measurements don't.

**Mechanism that could exist.** Wire in actual computation for these fields (transcript-driven post-hoc analysis, git-log diff inspection).

**Why it might not exist.** Likely WIP — explicitly named "downstream live wiring not shipped".

### 11.7 No automatic surfacing of `feedback_*` memory entries when triggers match

**Observed.** Memory has 7 entries (5 feedback, 1 reference, 1 index) at `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/memory/`. They auto-load at session start. There is no mechanism that re-surfaces a memory entry mid-session when its trigger conditions are met (e.g. resurfacing `feedback_no_explore_for_audits.md` when the agent is about to dispatch an audit to the default Explore agent).

**Mechanism that could exist.** A `PreToolUse` hook on Task that checks the agent's `description` / `model` field against memory entries' "How to apply" rules.

**Why it might not exist.** Hard to do precisely — the memory-application rules are stated in natural language ("if you are dispatching an audit") and would require either fuzzy matching or per-entry trigger-spec metadata.

### 11.8 No git-pre-commit discipline checks specific to the project

**Observed.** The active commit-validation hook (`gsd-validate-commit.sh`) is opt-in via `community: true`, which is unset. So conventional-commit format is not enforced. Recent commits do follow the `docs(gsd-2-uplift): ...` convention, suggesting cultural enforcement is working, but there's no mechanical check.

There are also no pre-commit checks specific to the project's discipline:

- "Did this commit modify CLAUDE.md/AGENTS.md/LONG-ARC.md/VISION.md? Surface and propose first?"
- "Did this commit close an Open Question without a new ADR?"
- "Did this commit add a new abstraction without ADR-0005-style 'shipped a second implementation' validation?"

**Mechanism that could exist.** Project-specific git-pre-commit hooks (in `.git/hooks/`) or a project-specific PreToolUse hook on Bash matching `^git[[:space:]]+commit` that blocks/warns on these conditions.

**Why it might not exist.** The discipline is already being enforced by hand (deliberation-boundary protocol from AGENTS.md:151-162). Adding mechanical checks risks false-positives that train Claude to bypass them.

### 11.9 GSD agents are not aware of the project's anti-pattern set

**Observed.** Project-local `gsd-planner`, `gsd-executor`, `gsd-verifier`, `gsd-roadmapper`, `gsd-debugger`, etc. mention generic anti-patterns ("scavenger hunt", "horizontal layers") but none reference the project's specific anti-pattern list (closure pressure, single-reader framing claims, tournament narrowing, etc.).

**Mechanism that could exist.** The project-local agent definitions in `.claude/agents/` could be customized to include cite-back to AGENTS.md:41-47 / LONG-ARC.md:46-54 in their working-posture prompts.

**Why it might not exist.** GSD agents are vendored from the framework; customization would diverge from upstream and complicate the vendoring update path. The current model (doctrine in CLAUDE.md/AGENTS.md, agents read these via auto-load) avoids the divergence problem at the cost of relying on each agent's memory-of-doctrine rather than embedded reminder.

### 11.10 LONG-ARC.md / VISION.md are not at the project root

**Observed.** `CLAUDE.md` and `AGENTS.md` reference `LONG-ARC.md` and `VISION.md` as bare basenames (e.g. `AGENTS.md:160` — "When editing `LONG-ARC.md`, `VISION.md`, or the project root `CLAUDE.md` / `AGENTS.md`"). The actual files are at `.planning/LONG-ARC.md` and `.planning/VISION.md`. Agents looking for them at the project root will not find them; they need to know to look in `.planning/`. PROJECT.md is also at `.planning/PROJECT.md`, not the project root, despite being part of CLAUDE.md's "New contributor" reading order ("PROJECT.md → VISION.md → LONG-ARC.md → ...").

**Mechanism that could exist.** Either (a) symlinks from project root to `.planning/` versions, (b) update the references to use full paths, or (c) the implicit convention "look in `.planning/` first" is documented somewhere agents reliably read.

**Why it might not exist.** The convention is likely understood; the friction is small enough that agents recover via grep. But for a fresh-session cold-read, the path mismatch is a real onboarding cost.

### 11.11 No instrumentation for the closure-pressure / opening-pressure reciprocal pair

**Observed.** Both anti-patterns are named in `2026-04-28-post-W1-and-framing-widening-handoff.md` §7.7 as recurring failure modes. Neither is instrumented. The user catches them by reading agent output; the agent does not catch itself.

**Mechanism that could exist.** A small classifier — possibly a Sonnet-4.5 sub-agent — that reads the last assistant turn on Stop and flags closure-pressure / opening-pressure phrasing. Output as `additionalContext` for the next turn or as a `.planning/measurement/` row.

**Why it might not exist.** Same false-positive concern as 11.2; also nontrivial to design without reading-the-room sensitivity.

### 11.12 Handoff cost is borne by the agent, not amortized

**Observed.** Each handoff lists 7-13 onboarding-read-order documents, plus optional documents. Fresh sessions pay this token cost in full. The `gsdr-postlude.js` writes session-end metadata but does not produce a session-summary that could replace partial handoff reading. The onboarding-read-order in handoff frontmatter is accurate but not delta-encoded against the predecessor handoff (it carries the full read-list each time, even if 80% overlaps).

**Mechanism that could exist.** A `gsd:resume-work` or `gsdr:resume-work` skill that reads only the latest handoff + STATE.md + the *delta* from the predecessor handoff. Or a session-summary auto-generated at Stop that becomes the cold-read artifact.

**Why it might not exist.** The current model (full handoff with explicit read-list) is robust against catastrophic context loss; a delta model would be faster but more fragile if the predecessor isn't read.

### 11.13 No project-local skill for "doctrine self-check before commit"

**Observed.** AGENTS.md:151-162 deliberation boundaries trigger surface-and-propose for 6 conditions (reshape spike/milestone/phase, modify ADR text/status/scope, introduce/remove top-level abstraction, change MCP surface, edit doctrine docs, close Open Question). The orchestrator has to remember these and self-check at commit time.

**Mechanism that could exist.** A `/doctrine-check` slash command that takes the staged diff and checks against the 6 triggers, prompting the orchestrator to confirm.

**Why it might not exist.** The 6 triggers are well-defined enough to mechanize; the cost of a self-check skill is low. Just hasn't been built.

### 11.14 Cross-project memory and signal-distillation pipeline split

**Observed.** Project memory at `~/.claude/projects/.../memory/` (7 entries, mostly Mar 2026). Cross-project signal-distillation appears to live in `~/workspace/projects/get-shit-done-reflect/.planning/deliberations/` (per `reference_spike_design.md`) and possibly in `~/.gsd/knowledge/`. Project-specific knowledge at `.planning/knowledge/signals/arxiv-mcp/` (10 signal files). Lesson-distillation also lives in `DECISION-SPACE.md §1.17` for the gsd-2-uplift workstream.

So lessons are written in 4 different places depending on cross-project relevance and timing. The fan-out is not documented in CLAUDE.md / AGENTS.md.

**Mechanism that could exist.** A clearer routing convention (which lessons go where), or a single skill (`/gsd:capture-lesson`) that prompts for scope and routes appropriately.

**Why it might not exist.** The routing is plausibly Logan-shaped and not yet stable enough to formalize.

---

## §12. What's working unusually well (for context)

Not all observations are gap-shaped. A few things are doing real work:

- **AGENTS.md anti-pattern citations resolve precisely** to LONG-ARC.md line numbers, and LONG-ARC.md → ADR-0001 / ADR-0005 citations also resolve. Doctrine is internally coherent at the textual level.
- **The `adversarial-auditor-xhigh` agent definition is substantive** — 60+ lines of specification, including a "Self-application" section that asks the auditor to apply its own disciplines to its output. The audit-finding template (What / Why it matters / Severity / Confidence / What would dissolve / Suggested direction) is detailed enough that audit outputs are comparable across runs.
- **The trajectory-verifier agent** has a "Critical mindset: Do NOT trust DISPOSITION.md / SUMMARY-section claims. Disposition records document what was *intended*; the artifact-level state is what *actually exists*." This is exactly the discipline the project's audit-arc structure depends on.
- **Memory entry `feedback_no_explore_for_audits.md`** is the kind of feedback that pays for itself many times over: it documents a specific failure mode (single-reader misframing of alembic migration state), the cost (almost-shipped wrong roadmap call), the fix (use `model: "opus"` for audit dispatches), and the cost-test (would a wrong verdict cost more than half a day of rework?). This is high-quality memory.
- **Audit-arc cadence is real.** 7 audits in `.planning/gsd-2-uplift/audits/` over 4 days, plus 8+ audits in `.planning/audits/` over the same 7-day window. Paired-vendor pattern is consistently applied where the deliberation-boundary discipline calls for it.
- **The GSD postlude's `runtime` field correctly distinguishes claude-code from codex-cli** (and falls back to file-presence detection if env vars are unset); the multi-runtime awareness is built-in even if the downstream measurement isn't yet wired.

---

## §13. Inventory tables for quick reference

### File index (project-local Claude config)

| Path | Role |
|---|---|
| `.claude/settings.json` | Hook bindings (SessionStart + PostToolUse only) |
| `.claude/settings.local.json` | 2 narrow permission allowances |
| `.claude/agents/*.md` | 12 GSD-default agents (no project customization) |
| `.claude/commands/gsd/*.md` | 32 GSD-default slash commands |
| `.claude/get-shit-done/` | Vendored GSD framework v1.22.4 |
| `.claude/hooks/gsd-check-update.js` | SessionStart background update check |
| `.claude/hooks/gsd-context-monitor.js` | PostToolUse 35%/25% context warning |
| `.claude/hooks/gsd-statusline.js` | Statusline (model \| task \| dir \| ctx-bar) |
| `.claude/gsd-file-manifest.json` | GSD installer file tracking |
| `.claude/scheduled_tasks.lock` | Empty lockfile |
| `.claude/package.json` | `{"type":"commonjs"}` for hooks |

### MCP surface

| Server | Configured at | Loaded for this project? | Relevance to project |
|---|---|---|---|
| sequential-thinking | global stdio | yes | general reasoning aid |
| serena | global enabledMcpjsonServers | no — no project `.mcp.json` | code navigation; useful |
| context7 | global enabledMcpjsonServers | no | docs lookup; useful |
| zlibrary | global enabledMcpjsonServers | no | scholarly docs; tangential |
| philpapers | global enabledMcpjsonServers (referenced) | no | direct domain match |
| tavily | global enabledMcpjsonServers (referenced) | no | web search; useful |
| morphllm-fast-apply | global enabledMcpjsonServers (referenced) | no | code edits; useful |
| (postgres / sqlite MCP) | none | n/a | database introspection; would address feedback_no_explore_for_audits failure mode |
| claude.ai Google Calendar / Drive / Gmail / Canva | global OAuth | needs auth | tangential |

### Hook activity (this project, this session)

| Hook | Active here? | Real work? |
|---|---|---|
| SessionStart `gsd-check-update.js` (project) | yes | npm version check |
| SessionStart `gsdr-check-update.js` (global) | yes | npm version check (different package) |
| SessionStart `gsdr-version-check.js` (global) | yes | project-vs-installed gsd-reflect version |
| SessionStart `gsdr-ci-status.js` (global) | yes | CI status fetch |
| SessionStart `gsdr-health-check.js` (global) | yes | project-health re-check scheduling |
| SessionStart `gsd-session-state.sh` (global) | no — opt-in not set | would inject STATE.md head |
| Notification `claude-notify.js` (global) | yes | ntfy.sh push |
| Stop `claude-notify.js` (global) | yes | ntfy.sh push on stop |
| Stop `gsdr-postlude.js` (global) | yes (partial) | metadata stub written; real measurements TODO |
| PostToolUse `gsdr-context-monitor.js` (global) | yes | warn at 35%/25% remaining |
| PostToolUse `gsd-context-monitor.js` (project) | yes | warn at threshold (variant) |
| PostToolUse `gsd-phase-boundary.sh` (global) | no — opt-in not set | would warn on `.planning/` writes |
| PreToolUse `gsd-prompt-guard.js` (global) | yes | prompt-injection scan on `.planning/` writes |
| PreToolUse `gsd-workflow-guard.js` (global) | no — opt-in not set | would warn on direct edits outside GSD workflows |
| PreToolUse `gsd-validate-commit.sh` (global) | no — opt-in not set | would enforce conventional-commit format |

---

## §14. Sources cited (for traceability)

Files referenced by this audit:

- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/CLAUDE.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/AGENTS.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/LONG-ARC.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/VISION.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/PROJECT.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/METHODOLOGY.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/foundation-audit/METHODOLOGY.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/config.json`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/measurement/session-meta-postlude/session-meta-postlude.jsonl`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/adrs/ADR-0001-exploration-first.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/settings.json`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/settings.local.json`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/hooks/*.js`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/agents/*.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.claude/commands/gsd/*.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-25-v0.2-plan-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-26-post-wave-2-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-26-post-wave-4-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/audits/*.md` (multiple)
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/*/AUDIT-SPEC.md` (5)
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/knowledge/signals/arxiv-mcp/*` (10)
- `/home/rookslog/.claude.json` (mcpServers + projects[arxiv-sanity-mcp])
- `/home/rookslog/.claude/settings.json`
- `/home/rookslog/.claude/agents/adversarial-auditor-xhigh.md`
- `/home/rookslog/.claude/agents/gsdr-auditor.md`
- `/home/rookslog/.claude/agents/trajectory-verifier.md`
- `/home/rookslog/.claude/agents/knowledge-store.md`
- `/home/rookslog/.claude/hooks/*.{js,sh}` (12 files)
- `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/memory/*.md` (7)
- `/home/rookslog/CLAUDE.md`
