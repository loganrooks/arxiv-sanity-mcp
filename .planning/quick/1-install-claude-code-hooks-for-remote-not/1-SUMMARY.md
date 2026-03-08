---
phase: quick-1
plan: 01
subsystem: infra
tags: [hooks, notifications, ntfy, terminal-bell, claude-code]

# Dependency graph
requires: []
provides:
  - Claude Code Notification hook (idle/permission/elicitation alerts)
  - Terminal bell forwarding for macOS notification center via VS Code Remote SSH
  - Optional ntfy.sh push notification support for iPhone delivery
affects: []

# Tech tracking
tech-stack:
  added: [ntfy.sh (optional)]
  patterns: [claude-code-hook-stdin-json-protocol, debounce-via-tmp-state-files, fire-and-forget-child-process]

key-files:
  created:
    - ~/.claude-notify.conf
    - ~/scripts/claude-notify.sh
    - ~/.claude/hooks/claude-notify.js
  modified:
    - ~/.claude/settings.json

key-decisions:
  - "Terminal bell as primary notification mechanism (zero-dependency, works via VS Code Remote SSH)"
  - "ntfy.sh as opt-in secondary channel (disabled by default, no secrets committed)"
  - "30-second debounce per session to prevent notification spam"
  - "Fire-and-forget notification dispatch to never block Claude Code"

patterns-established:
  - "Notification hook pattern: stdin JSON -> debounce check -> shell dispatcher -> exit 0"
  - "Config file at ~/.claude-notify.conf sourced by shell scripts"

requirements-completed: [NOTIFY-01]

# Metrics
duration: 2min
completed: 2026-03-08
---

# Quick Task 1: Install Claude Code Notification Hooks Summary

**Terminal bell + optional ntfy.sh notifications for Claude Code idle/permission/elicitation prompts on dionysus, dispatched via debounced Node.js hook and shell script**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-08T21:39:49Z
- **Completed:** 2026-03-08T21:42:11Z
- **Tasks:** 3
- **Files created:** 3
- **Files modified:** 1

## Accomplishments
- Notification config file with documented defaults (bell on, ntfy off)
- Shell dispatcher script supporting terminal bell and ntfy.sh push notifications
- Node.js hook following exact gsd-context-monitor.js pattern (3s stdin timeout, debounce, silent fail)
- Notification hook registered in settings.json alongside existing SessionStart and PostToolUse hooks

## Task Commits

Note: All created/modified files live outside the .planning/ git scope (home directory dotfiles and scripts). Per-task git commits are not applicable since the repo only tracks .planning/ content.

1. **Task 1: Create config file and notification dispatcher script** - ~/.claude-notify.conf + ~/scripts/claude-notify.sh created
2. **Task 2: Create Node.js hook script and register in settings.json** - ~/.claude/hooks/claude-notify.js created, settings.json updated
3. **Task 3: End-to-end smoke test** - All tests passed (direct script, simulated hook, debounce, settings integrity)

## Files Created/Modified
- `~/.claude-notify.conf` - Notification config (bell toggle, ntfy toggle/topic/server)
- `~/scripts/claude-notify.sh` - Central notification dispatcher (bell + ntfy.sh)
- `~/.claude/hooks/claude-notify.js` - Claude Code Notification hook handler (debounced)
- `~/.claude/settings.json` - Added Notification hook entry (existing hooks unchanged)

## Decisions Made
- Used terminal bell (`printf '\a'`) as primary mechanism -- zero dependencies, forwarded by VS Code Remote SSH to macOS Notification Center automatically
- ntfy.sh disabled by default with placeholder topic name to avoid accidental notification leaks
- 30-second debounce window (per session, stored in /tmp/) balances responsiveness with spam prevention
- Fire-and-forget pattern for shell script execution (execFile with unref) to never block hook completion
- Empty JSON `{}` output from hook (valid protocol response, no additionalContext needed)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Home directory .gitignore excludes everything except .planning/, so per-task commits for the notification files were not possible within this repo. All files were created and verified in place; only the SUMMARY.md and STATE.md are committed to git.

## User Setup Required

**Optional: Enable ntfy.sh push notifications for iPhone (orpheus)**
1. Install ntfy app on iPhone
2. Edit `~/.claude-notify.conf`:
   - Set `NTFY_ENABLED=true`
   - Change `NTFY_TOPIC=` to a unique private topic name
3. Subscribe to that topic in the ntfy app
4. Test: `~/scripts/claude-notify.sh permission_prompt test-project`

No setup needed for terminal bell -- it works automatically via VS Code Remote SSH.

## Verification Results

| Check | Result |
|-------|--------|
| Config exists with correct defaults | PASS |
| Script executable + syntax check | PASS |
| Hook syntax check | PASS |
| Notification hook registered | PASS |
| Existing hooks unchanged (4+1) | PASS |
| Simulated invocation exits 0 | PASS |
| No secrets in files | PASS |

## Next Steps
- Terminal bell notifications will activate automatically on next Claude Code session
- To enable iPhone notifications, edit ~/.claude-notify.conf (see User Setup above)
- Consider adjusting DEBOUNCE_MS (30s default) if notification frequency needs tuning

## Self-Check: PASSED

All artifacts verified:
- ~/.claude-notify.conf: FOUND
- ~/scripts/claude-notify.sh: FOUND (executable)
- ~/.claude/hooks/claude-notify.js: FOUND
- ~/.claude/settings.json Notification hook: FOUND
- 1-SUMMARY.md: FOUND

---
*Quick Task: 1-install-claude-code-hooks-for-remote-not*
*Completed: 2026-03-08*
