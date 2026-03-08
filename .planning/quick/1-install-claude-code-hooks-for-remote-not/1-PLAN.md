---
phase: quick-1
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - ~/.claude-notify.conf
  - ~/scripts/claude-notify.sh
  - ~/.claude/hooks/claude-notify.js
  - ~/.claude/settings.json
autonomous: true
requirements: [NOTIFY-01]

must_haves:
  truths:
    - "When Claude Code reaches an idle/permission/elicitation prompt on dionysus, the user's VS Code terminal on apollo receives a macOS notification via terminal bell"
    - "Optional ntfy.sh push notifications can be enabled for iPhone (orpheus) delivery by editing ~/.claude-notify.conf"
    - "Notifications are debounced to max 1 per 30 seconds per session to avoid spam"
    - "Hook failures never break Claude Code sessions (silent fail)"
  artifacts:
    - path: "~/.claude-notify.conf"
      provides: "Notification configuration (ntfy toggle, topic, bell toggle)"
      contains: "NTFY_ENABLED"
    - path: "~/scripts/claude-notify.sh"
      provides: "Central notification dispatcher (bell + ntfy)"
      min_lines: 20
    - path: "~/.claude/hooks/claude-notify.js"
      provides: "Claude Code Notification hook handler"
      min_lines: 40
    - path: "~/.claude/settings.json"
      provides: "Hook registration for Notification event"
      contains: "claude-notify.js"
  key_links:
    - from: "~/.claude/settings.json"
      to: "~/.claude/hooks/claude-notify.js"
      via: "hooks.Notification command entry"
      pattern: "claude-notify\\.js"
    - from: "~/.claude/hooks/claude-notify.js"
      to: "~/scripts/claude-notify.sh"
      via: "child_process.execFile call"
      pattern: "claude-notify\\.sh"
    - from: "~/scripts/claude-notify.sh"
      to: "~/.claude-notify.conf"
      via: "source config file"
      pattern: "claude-notify\\.conf"
---

<objective>
Install Claude Code notification hooks so that when any Claude Code session on dionysus reaches a point needing user attention (idle prompt, permission prompt, elicitation dialog), the user is notified on their macBook (via VS Code terminal bell forwarded to macOS notification center) and optionally on their iPhone (via ntfy.sh push notification).

Purpose: The user works remotely from apollo (MacBook) and orpheus (iPhone) via SSH/Tailscale. Claude Code sessions on dionysus can sit idle waiting for input with no way to alert the user. This hook solves that.
Output: Config file, shell dispatcher, Node.js hook script, settings.json updated.
</objective>

<execution_context>
@/home/rookslog/.claude/get-shit-done/workflows/execute-plan.md
@/home/rookslog/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@/home/rookslog/CLAUDE.md
@/home/rookslog/.claude/settings.json

<interfaces>
<!-- Existing hook pattern from gsd-context-monitor.js — follow this exact stdin/stdout JSON protocol -->

Hook stdin JSON shape (from Claude Code):
```json
{
  "session_id": "string",
  "cwd": "string",
  "hook_event_name": "Notification",
  "notification": {
    "type": "idle_prompt" | "permission_prompt" | "elicitation_dialog"
  }
}
```

Hook stdout JSON shape (optional, for additionalContext):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "Notification",
    "additionalContext": "string"
  }
}
```

Key patterns from existing hooks:
- 3-second stdin timeout guard (setTimeout -> process.exit(0))
- Silent fail in catch block (never block Claude Code)
- Uses require('fs'), require('child_process'), require('os'), require('path')
- Debounce state stored in /tmp/ files keyed by session_id

Existing settings.json hooks structure (to be extended, NOT replaced):
```json
{
  "hooks": {
    "SessionStart": [/* 4 existing entries — DO NOT MODIFY */],
    "PostToolUse": [/* 1 existing entry — DO NOT MODIFY */]
  }
}
```

The new "Notification" key must be ADDED alongside existing hooks.
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create config file and notification dispatcher script</name>
  <files>~/.claude-notify.conf, ~/scripts/claude-notify.sh</files>
  <action>
1. Create `~/.claude-notify.conf` with these defaults:
   ```
   # Claude Code notification config
   # Terminal bell — forwarded by VS Code Remote SSH to macOS notification center
   BELL_ENABLED=true
   # ntfy.sh push notifications — for iPhone/macOS ntfy app
   # To enable: set NTFY_ENABLED=true and choose a unique topic name
   NTFY_ENABLED=false
   NTFY_TOPIC=claude-dionysus-CHANGE-ME
   NTFY_SERVER=https://ntfy.sh
   ```

2. Create `~/scripts/claude-notify.sh` (chmod +x):
   - Accept arguments: `$1` = notification type (idle_prompt, permission_prompt, elicitation_dialog), `$2` = session context (optional, e.g. CWD basename)
   - Source `~/.claude-notify.conf` (exit silently if missing)
   - If BELL_ENABLED=true: `printf '\a'` to send terminal bell
   - If NTFY_ENABLED=true: send HTTP POST via curl to `$NTFY_SERVER/$NTFY_TOPIC`
     - Title: "Claude Code"
     - Message: human-readable, e.g. "Waiting for input (permission_prompt) in project-name"
     - Tags: "robot" (for ntfy emoji)
     - Priority: 3 (default) for idle_prompt, 4 (high) for permission_prompt
     - Use `curl -s -o /dev/null` with 5-second timeout to avoid hanging
   - Exit 0 always (never fail)

The script is the central dispatcher — the hook calls it, but it can also be called manually for testing (`~/scripts/claude-notify.sh idle_prompt my-project`).
  </action>
  <verify>
    <automated>bash -n ~/scripts/claude-notify.sh && test -f ~/.claude-notify.conf && echo "PASS: syntax ok, config exists"</automated>
  </verify>
  <done>Config file exists at ~/.claude-notify.conf with documented defaults. Shell script exists at ~/scripts/claude-notify.sh, is executable, passes bash syntax check, and can be run standalone for testing.</done>
</task>

<task type="auto">
  <name>Task 2: Create Node.js hook script and register in settings.json</name>
  <files>~/.claude/hooks/claude-notify.js, ~/.claude/settings.json</files>
  <action>
1. Create `~/.claude/hooks/claude-notify.js` following the EXACT pattern from gsd-context-monitor.js:
   - Shebang: `#!/usr/bin/env node`
   - 3-second stdin timeout guard: `const stdinTimeout = setTimeout(() => process.exit(0), 3000);`
   - Read all stdin, parse JSON
   - Extract: `session_id`, `cwd` (or process.cwd()), hook_event_name
   - The notification type comes from the stdin JSON. Check for `data.hook_event_name` — for the Notification event hook, the event name itself tells us it's a notification. The actual prompt type (idle, permission, elicitation) may be in subfields. Extract what's available; fall back to "attention needed" if specific type is not parseable.
   - **Debounce logic:**
     - State file: `/tmp/claude-notify-${session_id}.json` storing `{ lastNotify: timestamp_ms }`
     - If last notification was < 30000ms ago, exit silently
     - Update timestamp after sending notification
   - **Send notification:**
     - Derive project name from CWD: `path.basename(cwd)`
     - Call `~/scripts/claude-notify.sh` via `require('child_process').execFile`
     - Pass args: [notificationType, projectName]
     - Do NOT wait for completion — use fire-and-forget (spawn with detached + unref, or execFile with a short timeout and ignore errors)
   - **Output:** Write empty JSON `{}` to stdout (hook must produce valid JSON or nothing)
   - **Error handling:** Entire logic in try/catch, catch exits with 0 (never break Claude Code)

2. Update `~/.claude/settings.json`:
   - READ the file first (mandatory before Write)
   - Parse JSON, add a NEW key `"Notification"` to the `hooks` object (do NOT modify SessionStart or PostToolUse)
   - The Notification entry:
     ```json
     "Notification": [
       {
         "hooks": [
           {
             "type": "command",
             "command": "node \"/home/rookslog/.claude/hooks/claude-notify.js\""
           }
         ]
       }
     ]
     ```
   - Write the updated settings.json back, preserving all existing content and formatting
  </action>
  <verify>
    <automated>node -c /home/rookslog/.claude/hooks/claude-notify.js && node -e "const s = require('/home/rookslog/.claude/settings.json'); if (!s.hooks.Notification) { process.exit(1); } console.log('PASS: hook registered')"</automated>
  </verify>
  <done>Hook script exists at ~/.claude/hooks/claude-notify.js, passes Node.js syntax check, follows the same stdin/stdout pattern as gsd-context-monitor.js. settings.json contains a Notification hook entry pointing to the script. All existing hooks (SessionStart, PostToolUse) are unchanged.</done>
</task>

<task type="auto">
  <name>Task 3: End-to-end smoke test</name>
  <files></files>
  <action>
Run a simulated end-to-end test of the notification pipeline:

1. **Test the shell script directly:**
   ```bash
   ~/scripts/claude-notify.sh idle_prompt test-project
   ```
   Verify it exits 0 (bell will fire but won't be visible in non-terminal context — that's fine).

2. **Test the Node.js hook with simulated stdin:**
   ```bash
   echo '{"session_id":"test-123","cwd":"/home/rookslog/workspace/projects/test","hook_event_name":"Notification"}' | node ~/.claude/hooks/claude-notify.js
   ```
   Verify it exits 0 and does not error.

3. **Test debounce — run the same command again immediately:**
   The second invocation within 30 seconds should exit silently without calling the shell script.

4. **Verify settings.json integrity:**
   ```bash
   node -e "const s = require('/home/rookslog/.claude/settings.json'); console.log('SessionStart hooks:', s.hooks.SessionStart.length); console.log('PostToolUse hooks:', s.hooks.PostToolUse.length); console.log('Notification hooks:', s.hooks.Notification.length);"
   ```
   Expected: SessionStart: 4, PostToolUse: 1, Notification: 1

5. **Clean up test debounce file:**
   ```bash
   rm -f /tmp/claude-notify-test-123.json
   ```

If any test fails, diagnose and fix the issue in the relevant file before marking done.
  </action>
  <verify>
    <automated>echo '{"session_id":"smoke-test","cwd":"/home/rookslog","hook_event_name":"Notification"}' | timeout 5 node /home/rookslog/.claude/hooks/claude-notify.js; EXIT=$?; rm -f /tmp/claude-notify-smoke-test.json; test $EXIT -eq 0 && echo "PASS: hook exits cleanly"</automated>
  </verify>
  <done>Shell script exits 0 when called directly. Node.js hook exits 0 when fed simulated stdin JSON. Debounce prevents duplicate notifications within 30 seconds. settings.json retains all 4 SessionStart hooks, 1 PostToolUse hook, and has the new Notification hook. No errors in any test.</done>
</task>

</tasks>

<verification>
1. `~/.claude-notify.conf` exists with BELL_ENABLED=true and NTFY_ENABLED=false defaults
2. `~/scripts/claude-notify.sh` is executable and passes `bash -n` syntax check
3. `~/.claude/hooks/claude-notify.js` passes `node -c` syntax check
4. `~/.claude/settings.json` has hooks.Notification array with 1 entry
5. All pre-existing hooks in settings.json are unchanged (SessionStart: 4, PostToolUse: 1)
6. Simulated hook invocation exits 0 without errors
7. No secrets are stored in any created file
</verification>

<success_criteria>
- Terminal bell fires when Claude Code triggers Notification hook (testable only in a real VS Code Remote SSH session — verified structurally here)
- ntfy.sh notifications are opt-in and disabled by default
- Debounce prevents notification spam (max 1 per 30s per session)
- Hook never breaks Claude Code (silent fail on all error paths)
- All existing hooks continue to function (no regressions in settings.json)
</success_criteria>

<output>
After completion, create `.planning/quick/1-install-claude-code-hooks-for-remote-not/1-SUMMARY.md`
</output>
