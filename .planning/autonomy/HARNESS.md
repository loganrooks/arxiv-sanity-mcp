# Agentic harness — arxiv-sanity-mcp

**Status: built + tested 2026-05-29/30. Deny hook LIVE; Stop-contract hook built, not yet enabled.**
Purpose: make autonomous/looped Claude Code work *structurally* safe, not honor-system. Companion: [AUTONOMOUS-LOOP-SPEC.md](./AUTONOMOUS-LOOP-SPEC.md).

> `.claude/` is gitignored in this repo, so the **live** hooks are machine-local. This directory holds **committed reference copies** (`hooks/`) + the wiring instructions so the harness is reproducible on any clone/machine. The reference copy is the source of truth; if you edit the live hook, re-copy it here.

## 1. `PreToolUse` deny hook (Bash) — LIVE ✅

- **Live path:** `.claude/hooks/deny-destructive.js` · **reference copy:** `.planning/autonomy/hooks/deny-destructive.js`
- **What it blocks** (matched against the whole command string, so a banned verb hidden inside `bash -c "…"` / `python -c "…"` / a `&&;|` chain is still caught): `git reset --hard`, `git clean -f*`, `git checkout -- / .`, `git restore`, `git stash drop/pop/clear`, `git push --force/-f` (but **allows** `--force-with-lease`), `git branch -D`, `git rebase`, `git reflog delete/expire`, `git filter-branch/repo`, `git update-ref -d`, `rm -rf`/`-fr`, `rm -r …*`, and shell-metachar (`~` / `$VAR` / `*`) around a path in a destructive verb (the proven-by-incident tilde-expansion vector).
- **What it allows** (verified): `git status/add/commit/log`, `git push origin <branch>`, `git switch -c`, `git checkout <branch>` / `-b`, `gh pr merge`, plain `rm file`, read-only `python3 -c "…"`, `uv run pytest`, etc.
- **Mechanism:** reads the PreToolUse JSON on stdin; on a banned match writes a reason to stderr and exits `2` (Claude Code blocks the call). Fail-OPEN on parse errors (never bricks all Bash).
- **Test evidence:** `python3 /tmp/test_deny.py` → **30/30 cases pass** (16 block, 14 allow). Live wiring confirmed: `git branch -D __hooktest__` was intercepted with `[deny-destructive hook] BLOCKED — matched: git branch -D` (hot-reloaded, no restart needed).

This closes the single proven-by-incident gap (a CLAUDE.md ban does not stop execution; only a hook does). It fires regardless of permission/bypass mode.

**Known limitation (found live, required-before-full-autonomy):** the matcher is **substring-based, not command-position-aware**. A banned pattern quoted *inside* a non-executing argument — e.g. a `git commit -m "…blocks rm -rf…"` message, an `echo`, or a `grep` pattern — is a **false-positive block**. It errs safe (over-blocks, never under-blocks), so it's harmless for correctness, but for an autonomous loop it would fire constantly (commit messages routinely describe resets/removals). Fix before enabling full autonomy: match the banned verb only at a *command position* (string start, or after `;`/`&&`/`||`/`|`/`(`/`` ` ``/`$(`/`-c "`), not anywhere in the string. Until then: keep commit messages free of literal banned strings (write "recursive-force removal", not the literal command).

## 2. `Stop` completion-contract hook — BUILT, NOT ENABLED ⏸

- **Live path (when enabled):** `.claude/hooks/stop-contract.js` · **reference:** `.planning/autonomy/hooks/stop-contract.js`
- **Why off by default:** a `Stop` hook that refuses to end a turn would interfere with *normal* interactive turns. It is meant to be enabled **only for an autonomous run**, scoped by an active contract file.
- **How it works:** when `.planning/autonomy/active-contract.json` exists, the hook reads its `deliverables` checklist and **blocks stopping** until each is verified (mechanical checks: tests-pass marker, no-uncommitted-changes, queue-empty, etc.), OR an entry is explicitly dispositioned `halt`/`blocked` with evidence. No contract file → hook is a no-op (allows stop). This is the deterministic core; an LLM-evaluated variant (judging the transcript, per the /goal pattern) is a documented future extension — see the spec.
- **To enable for a run:** add a `Stop` hook to `.claude/settings.json` pointing at `stop-contract.js`, and write the run's `active-contract.json`. **Remove both when the run ends.**

## 3. Recreate on a fresh clone

```bash
mkdir -p .claude/hooks
cp .planning/autonomy/hooks/deny-destructive.js .claude/hooks/
# then add to .claude/settings.json hooks: a PreToolUse entry { "matcher":"Bash",
#   "hooks":[{"type":"command","command":"node .claude/hooks/deny-destructive.js"}] }
```
Verify with `python3 .planning/autonomy/hooks/test_deny.py` (or reconstruct from the case table above) before relying on it.

## 4. Not yet built (candidate follow-ups)

- `PreToolUse` Edit|Write guard for `.env` / `.git/**` / lockfiles (protect-sensitive-paths). Low effort, non-interfering.
- LLM-evaluated `Stop` hook (`type: prompt`/`agent`) that judges the transcript against the contract — the honest-done detector from the /goal field report. Higher effort; deterministic version above covers the mechanical floor.
- `PostToolUse` formatter/linter; `SessionStart(compact)` state re-injection.
