---
type: dispatch-post-mortem
date: 2026-04-30
status: complete
context: Phase D entry audit — first cross-vendor codex dispatch hung; clean kill; re-dispatch follows
---

# POST-MORTEM — Codex Cross-Vendor Audit Dispatch (Attempt 1)

## §0. Summary

First cross-vendor codex audit dispatch (attempt 1, dispatched 2026-04-30 03:35 by main-thread Claude per AUDIT-SPEC.md §0 contract) **hung indefinitely on stdin read; never made an API call; cost $0; clean kill at 04:14 (37 min wallclock idle).** Root cause: shell-pattern bug — backgrounded `codex exec` inherited a non-tty stdin handle and applied its `<stdin>`-block-append branch, blocking on EOF that never arrived. Fix mechanical: `</dev/null` to explicitly close stdin. Same-vendor adversarial-auditor audit (B) completed normally in 7 min during the cross-vendor hang window and produced 3A/3B/1C addendum-shape findings. No audit content lost.

Effort recalibration applied at re-dispatch: gpt-5.5 `xhigh` → `high` per Logan's calibration (codex `high` ≈ Opus 4.7 `xhigh` capability; codex `xhigh` is the expensive markup with diminishing returns). The original `xhigh` choice followed AUDIT-SPEC.md template precedent + trajectory plan §2.4 row D wording verbatim — itself a precedent-following failure mode the audit lenses were supposed to catch.

## §1. Causal chain

| Time (local) | Event | Evidence |
|---|---|---|
| 03:34 | AUDIT-SPEC.md drafted; both auditors prepared for parallel dispatch | `audit-findings-A.md`/`B.md` filenames specified per Phase B precedent for `tengu_sub_nomdrep_q7k` regex bypass |
| 03:35 | Codex spawn begins: bash wrapper PID 3953968 → node CLI PID 3953970 → codex binary PID 3953996. Helper-binary symlinks set up at `~/.codex/tmp/arg0/codex-arg0KKrLDh/` (apply_patch, codex-linux-sandbox, codex-execve-wrapper, applypatch). 0-byte `.lock` flock created. | `ls -la ~/.codex/tmp/arg0/codex-arg0KKrLDh/` shows 03:35 timestamp on dir + symlinks; `.lock` exists but empty |
| 03:35 | Codex emits to stdout: `Reading additional input from stdin...` Tee captures into `/tmp/codex-phase-d-entry-audit.log` (39 bytes, single line) | Log file contents preserved at `/tmp/codex-phase-d-entry-audit-attempt-1-hung.log` |
| 03:35 | Codex blocks on `read()` from fd 0 awaiting EOF. NO further work performed: no sqlite log init, no session-rollout file, no model-config validation, no API call | `process_uuid LIKE '%3953%'` returns zero rows in `~/.codex/logs_2.sqlite`; no file in `~/.codex/sessions/2026/04/30/` |
| 03:35-04:14 | 37 minutes of `S` (sleeping) state at 0% CPU, RSS 47MB. No state change. Same-vendor audit B completes independently at 03:41 | `ps -p 3953970 -o stat,etime,pcpu,pmem,rss` showed `Sl 37:08 0.0 0.1 47736` |
| 04:14 | Investigation triggered by Logan prompt re: time + cost. Findings: hung-not-running. Kill issued; bash wrapper + node CLI + codex binary all SIGTERMed | bash background task exit code 144 (SIGTERM-shape) |
| 04:14+ | Re-dispatch with `</dev/null` + `model_reasoning_effort=high` | (this commit) |

## §2. Root cause

Per `codex exec --help`:
> *"If not provided as an argument (or if `-` is used), instructions are read from stdin. If stdin is piped and a prompt is also provided, stdin is appended as a `<stdin>` block."*

Original dispatch shell-pattern:
```bash
codex exec --model gpt-5.5 -c model_reasoning_effort=xhigh \
  --sandbox workspace-write --skip-git-repo-check "PROMPT_HERE" 2>&1 | tee /tmp/codex-phase-d-entry-audit.log
```

The `| tee` pipes codex's STDOUT to tee — it does NOT pipe anything INTO codex's stdin. But: when the Bash tool backgrounded this subshell via `run_in_background: true`, codex's stdin file descriptor (fd 0) was inherited from the harness's bash-task wrapper as a non-tty handle (likely the harness's task-stdin pseudoterminal or a kept-open pipe end from harness internals).

Codex's logic: *"stdin is non-tty → user is piping input → append it as `<stdin>` block to the prompt → block on `read()` until EOF."* No EOF ever arrived because nothing was actually writing to that fd.

The hang is reproducible: any `codex exec ... "PROMPT" 2>&1 | tee FILE` invocation under Claude Code's `run_in_background: true` will exhibit this if codex inherits a non-tty fd 0 from the harness.

## §3. Fix

**Mechanical:** add `</dev/null` to close stdin explicitly:

```bash
codex exec --model gpt-5.5 -c model_reasoning_effort=high \
  --sandbox workspace-write --skip-git-repo-check "PROMPT_HERE" </dev/null 2>&1 | tee /tmp/codex-phase-d-entry-audit-attempt-2.log
```

`</dev/null` redirects stdin from `/dev/null`, which returns immediate EOF on read. Codex sees the empty `<stdin>` block, ignores it, processes the prompt-arg only.

## §4. Effort recalibration (separate from the bug fix)

**Original:** `gpt-5.5 xhigh` per AUDIT-SPEC.md frontmatter (copied verbatim from incubation-checkpoint audit) + trajectory plan §2.4 row D specification ("xhigh both auditors").

**Recalibrated:** `gpt-5.5 high`.

**Reasoning** (Logan's calibration, applied at /effort xhigh turn 2026-04-30):
- Codex `xhigh` is the priciest tier with diminishing capability returns vs `high`.
- Codex `high` ≈ Opus 4.7 `xhigh` capability for these audit-shape tasks.
- Codex `medium` ≈ Opus 4.7 `xhigh` for some tasks (qualified equivalence).

Phase D entry audit is load-bearing; same-vendor audit B already came in at Opus xhigh; cross-vendor at codex high gives parity-not-asymmetry on the differential. Medium would be a gamble on this specific corpus (framing-leak detection benefits from depth); high captures the cost saving without sacrificing depth.

**The original `xhigh` choice was a precedent-following failure mode** — the audit lenses (specifically design-framing-quality / framing-leak detection) were exactly supposed to catch unexamined inheritance of past-audit framing. The audit was set up under that failure mode itself, in its model-effort-selection. Caught at Logan's prompt; corrected at re-dispatch.

**Trajectory plan §2.4 row D update implication:** the row's "xhigh both auditors" wording was written without the codex effort-tier-vs-cost calibration. Future cross-vendor codex audits should default to `high` (with `xhigh` reserved for explicitly-flagged extreme-framing-load tasks). Worth surfacing as a Phase D entry audit Class A finding *outside* the audit corpus itself (this post-mortem records it). Trajectory plan amendment deferred to post-Phase-D evidence consideration per plan §1.4 normal-amendment cadence.

## §5. Lessons (worth carrying forward)

1. **Never `codex exec` in background without `</dev/null`.** The fd-inheritance behavior under Claude Code's `run_in_background: true` is the silent failure surface. Add `</dev/null` to every backgrounded codex dispatch, even when the prompt is provided as argument.

2. **0% CPU + non-zero RSS + no log entries = blocked-on-syscall.** Strong signal to investigate stdin/lock/socket state, NOT to assume "still reasoning." Active codex reasoning shows non-zero CPU even between API turns (telemetry/sqlite writes). 37 min at 0% means the process never engaged.

3. **Past audit-folder examples don't transfer mechanically.** Logan likely dispatched prior codex audits from interactive shell where stdin was already a tty (no non-tty branch fires). The pattern in `audit-findings-A.md` frontmatters records the OUTCOME (model + reasoning level) but not the INVOCATION (shell pattern). Don't copy invocation patterns from precedent without verifying the runtime context matches.

4. **Cost calibration ≠ AUDIT-SPEC template inheritance.** `model_reasoning_effort` should be re-disposed per audit, not inherited from precedent verbatim. The trajectory plan §2.4 row reasoning-level table specifies WHY xhigh might be needed (framing-load + cross-cutting + decision-stake + negative-space-depth) — those criteria should fire per-audit, not be assumed invariant. Precedent-shaped inheritance is itself a closure-pressure surface.

5. **Same-vendor + cross-vendor parallel dispatch exposes asymmetric failure modes.** Same-vendor audit B completed normally in 7 min while cross-vendor A hung silently. Without independent investigation, the failure could have looked like "codex is just slow" until cost/time ratio surfaced it. Periodic process-health checks (CPU + RSS + log-file-growth) for long-running parallel dispatches would catch faster.

## §6. Salvageable artifacts (preserved for trail)

- `/tmp/codex-phase-d-entry-audit-attempt-1-hung.log` — 39 bytes, single line: "Reading additional input from stdin..." (the smoking gun).
- `~/.codex/tmp/arg0/codex-arg0KKrLDh/` — codex tmp dir intact with helper symlinks + 0-byte `.lock` file (NOT cleaned up by kill; flock dropped naturally on process death; safe to leave or delete).
- This POST-MORTEM.md.

**No audit content was generated by attempt 1; nothing to salvage from a content perspective.** Re-dispatch starts fresh.

## §7. Re-dispatch parameters (attempt 2)

- **Model:** gpt-5.5 (unchanged)
- **Reasoning effort:** `high` (recalibrated from `xhigh`)
- **Sandbox:** `workspace-write` (unchanged)
- **stdin:** `</dev/null` (NEW — bug fix)
- **Prompt:** identical to attempt 1 (preserves audit comparability with same-vendor audit B which read same AUDIT-SPEC.md)
- **Output destination:** `audit-findings-A.md` (unchanged)
- **Log destination:** `/tmp/codex-phase-d-entry-audit-attempt-2.log` (new file; preserves attempt-1 log)

## §8. Cross-references

- AUDIT-SPEC.md (this audit folder) — frontmatter to be updated reflecting effort recalibration.
- audit-findings-B.md (this audit folder) — completed during attempt-1 hang; unaffected.
- Phase D entry corpus (the 6 artifacts under audit) — unchanged.

---

*Post-mortem authored by Claude (Opus 4.7) 2026-04-30 04:15 in-session-collaboration with Logan, immediately following codex attempt-1 kill + investigation. Subject to same fallibility caveat as DECISION-SPACE.md §0; this record is procedural-traceability for Phase D entry audit folder, not Phase D substantive evidence.*
