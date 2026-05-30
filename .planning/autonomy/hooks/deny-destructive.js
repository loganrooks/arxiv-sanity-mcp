#!/usr/bin/env node
/**
 * PreToolUse deny hook — blocks destructive / irrecoverable Bash commands.
 *
 * Fires regardless of permission mode (this is the only proven-by-incident gap:
 * a natural-language ban in CLAUDE.md does NOT stop tool execution; only a hook does).
 * Blocks the operating-contract verb list PLUS the proven-by-incident vectors:
 * shell-metacharacters around a path in a destructive verb, and rm -rf in any form.
 *
 * Mechanism: read the PreToolUse JSON on stdin; if the Bash command matches a banned
 * pattern, write a reason to stderr and exit 2 (Claude Code treats exit 2 from a
 * PreToolUse hook as "block this tool call, show stderr to the model").
 * Fail-OPEN on parse errors (exit 0) so a malformed input never bricks all Bash.
 *
 * The destructive-verb patterns are matched against the WHOLE command string, so a
 * banned verb hidden inside `bash -c "..."` / `python -c "..."` / a `&&;|` chain is
 * still caught — without false-positiving on a legitimate read-only `python3 -c`.
 */
'use strict';

function readStdin() {
  try { return require('fs').readFileSync(0, 'utf8'); } catch (_) { return ''; }
}

let cmd = '';
let toolName = '';
try {
  const data = JSON.parse(readStdin() || '{}');
  toolName = data.tool_name || data.toolName || '';
  const ti = data.tool_input || data.toolInput || {};
  cmd = (ti && typeof ti === 'object' ? ti.command : '') || '';
} catch (_) {
  process.exit(0); // fail-open on bad input
}

if (toolName !== 'Bash' || !cmd) process.exit(0);

const BANNED = [
  [/\bgit\s+reset\s+--hard\b/, 'git reset --hard'],
  [/\bgit\s+clean\s+-[a-z]*f/, 'git clean -f*'],
  [/\bgit\s+checkout\s+(--(\s|$)|\.(\s|$)|HEAD\b[^\n]*--)/, 'git checkout -- / discard-tree'],
  [/\bgit\s+restore\b/, 'git restore'],
  [/\bgit\s+stash\s+(drop|pop|clear)\b/, 'git stash drop/pop/clear'],
  [/\bgit\s+push\b[^\n]*(--force(?!-with-lease)|\s-f(\s|$))/, 'git push --force/-f'],
  [/\bgit\s+branch\s+-[a-zA-Z]*D\b/, 'git branch -D'],
  [/\bgit\s+rebase\b/, 'git rebase'],
  [/\bgit\s+reflog\s+(delete|expire)\b/, 'git reflog delete/expire'],
  [/\bgit\s+filter-(branch|repo)\b/, 'git history rewrite (filter-branch/repo)'],
  [/\bgit\s+update-ref\s+-d\b/, 'git update-ref -d'],
  [/\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b/, 'rm -rf / -fr'],
  [/\brm\s+-[a-zA-Z]*r\b[^\n]*\*/, 'rm -r with a glob'],
];

// Extra guard: shell-metacharacter (~, $VAR, *) next to a path in a destructive verb.
const METACHAR_DESTRUCTIVE =
  /\b(rm\s+-|git\s+clean|git\s+checkout\s+--|git\s+restore)\b[^\n]*(~\/|\$\{?[A-Za-z_]|\s\*(\s|$))/;

let hit = null;
for (const [rx, name] of BANNED) { if (rx.test(cmd)) { hit = name; break; } }
if (!hit && METACHAR_DESTRUCTIVE.test(cmd)) hit = 'shell-metachar (~ / $VAR / *) around a path in a destructive command';

if (hit) {
  const reason =
    `[deny-destructive hook] BLOCKED — matched: ${hit}\n` +
    `Destructive/irrecoverable git or filesystem command. Operating contract requires explicit, ` +
    `specific human approval for this exact command (quote & expand every path first).\n` +
    `Command: ${cmd.slice(0, 400)}`;
  process.stderr.write(reason + '\n');
  process.exit(2); // block
}

process.exit(0); // allow
