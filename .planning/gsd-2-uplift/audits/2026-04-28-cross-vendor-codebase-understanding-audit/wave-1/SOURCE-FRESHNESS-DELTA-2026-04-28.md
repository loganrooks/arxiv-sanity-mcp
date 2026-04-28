---
type: source-freshness-delta
date: 2026-04-28
audit: 2026-04-28-cross-vendor-codebase-understanding-audit
source_range: 82bcf6b71..bf1d8aad0
source_checkout: /home/rookslog/workspace/projects/gsd-2-explore
status: complete
reasoning_effort: medium
---

# Source Freshness Delta - 2026-04-28

## Scope

This delta scout inspected fetched git objects for `82bcf6b71..bf1d8aad0` without updating or checking out `/home/rookslog/workspace/projects/gsd-2-explore`.

Preflight source evidence:

- Local `HEAD` remains `82bcf6b71348bca835f386403763d3867725cbf1`.
- `origin/main` is `bf1d8aad0473809a58be4e7d7fd386ffa1581d8a`.
- Full range contains 10 commits: 2 merge commits and 8 non-merge commits.

## Commits Inspected

| Commit | Subject | Impact summary |
|---|---|---|
| `bf1d8aad0` | Merge pull request #5096 from jeremymcs/fix/always-allow-non-bash-tools | Merges Claude Code CLI permission persistence fix. |
| `1cec8ae38` | `test(claude-code-cli): cover empty permission suggestions fallback` | Adds test coverage for empty permission suggestions. |
| `a88baeae9` | `fix(claude-code-cli): persist Always Allow for non-Bash tools` | Adds fallback `updatedPermissions` for non-Bash tools with no SDK suggestions. |
| `a7b6e59b7` | Merge pull request #5087 from jeremymcs/fix/warp-auto-disconnect | Merges auto-mode/session lifecycle fix. |
| `c162c44bf` | `Fix agent_end session switch handoff` | Refines session transition handling during `agent_end`. |
| `e3bd04551` | `Fix session transition during agent_end` | Adds session-transition guards during `agent_end`. |
| `6d7e4ccb5` | `fix(agent-session): skip idle wait after agent_end` | Narrows idle-wait/session tail behavior. |
| `71114fccf` | `fix(agent-session): guard synthetic agent_end transitions` | Guards synthetic `agent_end` transition behavior. |
| `0f4fd902d` | `test(gsd): cover agent-end session resume persistence` | Adds persistence regression coverage. |
| `ebf7124a8` | `fix(gsd): preserve auto session handoff in terminals` | Introduces TTY-gated `gsd auto` headless redirect and lifecycle fix docs/tests. |

## Files Changed

`git diff --name-status 82bcf6b71..bf1d8aad0`:

| Status | Path | Domain relevance |
|---|---|---|
| A | `docs/dev/warp-auto-disconnect-findings.md` | Topology/runtime, release/practice context. |
| M | `packages/pi-coding-agent/src/core/agent-session-abort-order.test.ts` | Topology/runtime lifecycle tests. |
| M | `packages/pi-coding-agent/src/core/agent-session.ts` | Topology/runtime lifecycle behavior. |
| A | `src/cli-auto-routing.ts` | Topology/runtime CLI routing behavior. |
| M | `src/cli.ts` | Topology/runtime CLI routing behavior. |
| M | `src/resources/extensions/claude-code-cli/stream-adapter.ts` | Extension/workflow permission behavior. |
| M | `src/resources/extensions/claude-code-cli/tests/stream-adapter.test.ts` | Extension/workflow tests. |
| M | `src/tests/auto-mode-piped.test.ts` | Topology/runtime CLI routing tests. |
| M | `src/tests/auto-piped-io.test.ts` | Topology/runtime CLI routing tests. |

Range stat: 9 files changed, 729 insertions, 193 deletions.

## Domain Impact Table

| Scout domain | Impact classification | Judgment | Source evidence |
|---|---|---|---|
| Scout 01 topology/runtime | Small but concrete runtime freshness impact | Addendum enough; no full rerun recommended. | `bf1d8aad0:src/cli.ts:458-462` now routes `gsd auto` to headless only through `shouldRedirectAutoToHeadless`; `bf1d8aad0:src/cli-auto-routing.ts:1-8` defines that redirect as only `auto` plus non-TTY stdin or stdout. `bf1d8aad0:packages/pi-coding-agent/src/core/agent-session.ts:275-280`, `:441-455`, `:514-521`, and `:1608-1630` add lifecycle state and avoid aborting during `agent_end` session transitions. |
| Scout 02 extension/workflow | Material to the not-yet-completed domain, but not blocking this delta | Scout 02 should inspect fresh source. | `bf1d8aad0:src/resources/extensions/claude-code-cli/stream-adapter.ts:1094-1118` now persists "Always Allow" for non-Bash tools by adding a tool-name-only permission rule when suggestions are absent or empty. Tests cover missing and empty suggestions in `stream-adapter.test.ts`. |
| Scout 03 release/practice | Small freshness impact | Addendum enough; no full rerun recommended from this delta alone. | The range itself demonstrates continued rapid post-scout merge/fix activity: two merge commits and eight focused fix/test commits after `82bcf6b71`. It does not add release machinery, tags, changelog edits, breaking-change markers, or deprecation-policy changes. |

## Scout 01 Freshness Judgment

Provisional judgment: **addendum enough**.

The Scout 01 topology map remains accurate in broad terms:

- Package/workspace topology did not change.
- No `gsd-agent-core` or `gsd-agent-modes` package was added.
- No MCP/RPC/headless package split was rewritten.
- The in-process MCP and standalone MCP distinction remains untouched by this range.

The stale or incomplete parts are narrow:

1. Scout 01 said `gsd auto` is a shorthand for headless. That is now only true when stdin or stdout is not a TTY. In `bf1d8aad0`, `src/cli.ts:458-462` calls `shouldRedirectAutoToHeadless(...)`, and `src/cli-auto-routing.ts:1-8` returns true only for subcommand `auto` with non-TTY stdin or stdout.
2. Scout 01 listed `AgentSession` as a shared abstraction but did not include the new session-handoff nuance. `bf1d8aad0:packages/pi-coding-agent/src/core/agent-session.ts:1608-1630` now distinguishes session transitions during `agent_end` from normal session switches: during `agent_end`, it waits for idle and suppresses abort; otherwise it preserves the existing abort-before-disconnect behavior.
3. The new dev note states the observed Warp issue, root-cause hypothesis, and implemented fix: `docs/dev/warp-auto-disconnect-findings.md:21-30` names auto-mode `agent_end` handoff plus unconditional `gsd auto` routing as the relevant risks; lines `47-54` describe the implemented lifecycle distinction and TTY-gated auto routing.

This is source-backed and precise enough for an append-only freshness note. It does not require rerunning the full topology/runtime scout unless downstream adjudication depends specifically on auto-mode foreground ownership or `AgentSession.newSession()` semantics.

## Scout 03 Freshness Judgment

Provisional judgment: **addendum enough**.

The release/practice report is not materially invalidated:

- Its "latest visible commit was `82bcf6b7`" observation is stale after fetch.
- The delta adds two merge commits and eight non-merge fix/test commits, reinforcing the rapid visible activity observation.
- The delta does not touch `CHANGELOG.md`, `.github/workflows/*`, release scripts, `CONTRIBUTING.md`, PR templates, version metadata, or tags.
- No commit subject in this range uses `BREAKING CHANGE` or conventional `!:` breaking markers.

No full Scout 03 rerun is recommended from this delta alone. A rerun would be warranted only if the audit needs complete current-release/tag state beyond the local fetched commit range.

## Scout 02 Freshness Note

Scout 02 is not yet completed, so there is no stale report to patch. It should inspect `bf1d8aad0` directly because the delta changes extension/workflow behavior in a user-visible permission surface:

- `stream-adapter.ts` now builds an `updatedPermissions` fallback for non-Bash tools without SDK suggestions.
- The intended behavior is documented in comments at `bf1d8aad0:src/resources/extensions/claude-code-cli/stream-adapter.ts:1094-1107`: without fallback permissions, "Always Allow" can silently fail to persist for tools whose input varies per call; a bare `{ toolName }` rule matches any input.

## Addenda Performed

Append-only source freshness addenda were added to:

- `wave-1-scout-01-topology-runtime.md`
- `wave-1-scout-03-release-practice.md`

No original scout body was rewritten.

## Rerun Recommendations

| Scout | Recommendation | Reason |
|---|---|---|
| Scout 01 topology/runtime | No full rerun from this delta alone. | Addendum captures the narrow `gsd auto` and `AgentSession` lifecycle changes. |
| Scout 02 extension/workflow | Run against `bf1d8aad0`. | No completed report exists, and the delta changes Claude Code CLI permission persistence. |
| Scout 03 release/practice | No full rerun from this delta alone. | Release machinery/policy surfaces are unchanged; only latest-commit freshness changed. |

## Caveats

- This was a delta scout, not a full rerun.
- I inspected fetched git objects for `bf1d8aad0` because the source working tree remained at `82bcf6b71`.
- I did not execute the gsd-2 test suite.
- I did not inspect GitHub PR bodies, release pages, or network sources.
