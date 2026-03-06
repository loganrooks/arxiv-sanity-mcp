# Domain Audit: Network and Access (AUD-06)

**Audited:** 2026-03-05
**Scope:** Tailscale, SyncThing, tmux sessions, SSH configuration
**Severity Scale:** HIGH (action needed Phase 3-4) | MEDIUM (should address) | LOW (cosmetic/minor)

## Executive Summary

- **Tailscale peers:** 4 devices (dionysus, apollo, mitratampold, orpheus)
- **Tailscale health:** 1 warning (DNS servers unreachable)
- **SyncThing folders:** 9 configured (1 paused)
- **SyncThing peers:** 2 remote devices configured (APOLLO, LE2127), both currently disconnected
- **SyncThing uptime:** 93.9 days (started ~Dec 2, 2025)
- **Tmux sessions:** 19 total (HIGH: 11 stale claude-enhanced sessions from Dec-Jan)
- **SSH authorized keys:** 3 keys
- **SSH client config:** None (no ~/.ssh/config)

## Findings

### [HIGH] 19 Stale Tmux Sessions (11 claude-enhanced orphans)

19 tmux sessions exist, 11 of which are stale "claude-enhanced" sessions from December 2025 through January 2026:

| Session | Created | Status |
|---------|---------|--------|
| claude-enhanced | 2025-12-29 | Attached (group root) |
| claude-enhanced-5 | 2026-01-09 | Detached |
| claude-enhanced-6 | 2026-01-09 | Detached |
| claude-enhanced-7 | 2026-01-09 | Detached |
| claude-enhanced-8 | 2026-01-18 | Detached |
| claude-enhanced-9 | 2026-01-19 | Detached |
| claude-enhanced-10 | 2026-01-19 | Detached |
| claude-enhanced-11 | 2026-01-23 | Detached |
| claude-enhanced-12 | 2026-01-24 | Detached |
| claude-enhanced-13 | 2026-01-24 | Detached |
| claude-enhanced-14 | 2026-01-24 | Detached |
| claude-enhanced-15 | 2026-01-26 | Detached |

**Additional sessions (likely active/intentional):**

| Session | Created | Status |
|---------|---------|--------|
| 2 | 2026-01-08 | Attached |
| 3 | 2026-01-08 | Detached |
| crypt | 2026-01-08 | Attached |
| scholardoc | 2026-01-28 | Attached |
| zlibrary | 2026-01-28 | Attached |
| gsd | 2026-03-05 | Attached |
| dionysus | 2026-03-05 | Attached |

The 11 detached claude-enhanced-N sessions are orphaned from previous Claude Code development sessions. They consume memory and contribute to process clutter.

Cross-reference: process-audit.md also flags these sessions. Remediation: Phase 3 CLN-07 (orphan prevention).

**Remediation:** Kill stale tmux sessions (`tmux kill-session -t claude-enhanced-N`). Install session auto-cleanup (e.g., tmux plugin or cron job).

### [MEDIUM] Tailscale DNS Health Warning

```
Tailscale can't reach the configured DNS servers. Internet connectivity may be affected.
```

Tailscale is configured with custom DNS that may be unreachable. This is a known issue documented in the plan. Internet connectivity appears functional (all commands succeed), so this is a routing/fallback configuration issue rather than an outage.

**Remediation:** Review Tailscale admin console DNS settings. Ensure fallback DNS resolvers are configured. Phase 4 ACC-03.

### [MEDIUM] SyncThing Peers Disconnected

Both remote SyncThing peers (APOLLO and LE2127) show as disconnected:

| Device | Device ID (prefix) | Connected | Bytes In/Out |
|--------|-------------------|-----------|--------------|
| APOLLO | EFK2BM5- | No | 0/0 |
| LE2127 | 6K6DEOS- | No | 0/0 |

This matches the known issue from MEMORY.md: "Apollo and LE2127 are currently disconnected. SyncThing needs to be verified on Mac side."

All 9 folders are configured but cannot sync without connected peers. The dropbox folder is explicitly paused.

**Remediation:** Verify SyncThing is running on Apollo (Mac side). LE2127 may be intentionally offline. Phase 4 ACC-05.

### [MEDIUM] SyncThing GUI Bound to All Interfaces

The SyncThing GUI is bound to `[::]:8384` (all interfaces, IPv6 wildcard = equivalent to 0.0.0.0).

This is already flagged in the security audit (SEC-05). Here we document the functional state.

**guiAddressUsed:** `[::]:8384`
**Connection listeners:** `tcp://0.0.0.0:22000`, `quic://0.0.0.0:22000`

**Remediation:** Phase 3 SEC-05 — bind to 127.0.0.1:8384.

### [LOW] No SSH Client Config

No `~/.ssh/config` exists. SSH connections must be made with full arguments each time.

For a multi-device setup accessed via Tailscale, an SSH config with host aliases, ControlMaster, and keepalives would improve the workflow.

**Remediation:** Phase 4 ACC-03 — create SSH config with Tailscale host aliases.

### [INFO] SyncThing Folder Inventory

9 folders configured with varying device sharing:

| Folder ID | Label | Path | Type | Devices | Paused |
|-----------|-------|------|------|---------|--------|
| academic-active | Academic Active (2025-fall) | ~/workspace/university/courses/2025-fall | sendreceive | 3 | No |
| academic-notes | Academic Notes | ~/workspace/university/notes | sendreceive | 3 | No |
| academic-processing | Academic Processing (Incoming) | /scratch/lecture-processing/incoming | sendreceive | 3 | No |
| azymc-la4zx | writings | ~/workspace/writings | sendreceive | 2 | No |
| cavn9-d9bt7 | reading-groups | ~/workspace/university/reading-groups | sendreceive | 2 | No |
| courses | courses | ~/workspace/university/courses | sendreceive | 2 | No |
| default | Default Folder | ~/Sync | sendreceive | 1 | No |
| hktwt-tmkru | philosophy-film-club | ~/philosophy-film-club | sendreceive | 2 | No |
| zufol-bsxz2 | dropbox | /data/dropbox | receiveonly | 3 | Yes |

**Notes:**
- "default" folder (~/Sync) has only 1 device (local only) -- effectively unused
- "dropbox" is paused -- intentional per MEMORY.md
- "academic-processing" uses /scratch/ which is cleaned weekly by cron
- 3-device folders: academic-active, academic-notes, academic-processing, dropbox
- 2-device folders: writings, reading-groups, courses, philosophy-film-club

## Raw Data

### Tailscale Peer Table

| IP | Hostname | Owner | OS | Status | Connection |
|----|----------|-------|----|--------|------------|
| 100.93.212.44 | dionysus | logansrooks@ | linux | self | -- |
| 100.64.240.77 | apollo | logansrooks@ | macOS | active | direct 76.9.197.113:32521 |
| 100.92.243.32 | mitratampold | logansrooks@ | windows | offline | last seen 64 days ago |
| 100.107.206.108 | orpheus | logansrooks@ | iOS | -- | -- |

- Apollo: active with direct connection (tx 197MB, rx 592MB total)
- Mitratampold: Windows device, offline for 64 days
- Orpheus: iOS, status unclear (listed but no connection info)

### SSH Key Inventory

3 authorized keys in ~/.ssh/authorized_keys:

| # | Type | Comment |
|---|------|---------|
| 1 | ssh-ed25519 | logansrooks@gmail.com |
| 2 | ssh-ed25519 | logansrooks@gmail.com |
| 3 | ssh-ed25519 | logan-borrowed-laptop |

Note: Two keys with identical comments (logansrooks@gmail.com) -- likely Apollo and another device. "logan-borrowed-laptop" may be stale.

### Tmux Session Summary

- **Total sessions:** 19
- **Attached:** 6 (2, crypt, claude-enhanced, scholardoc, gsd, dionysus)
- **Detached:** 13 (3, claude-enhanced-5 through -15, zlibrary)
- **Stale (>30 days, detached):** 11 (claude-enhanced-5 through -15, plus session "3")
- **Oldest session:** claude-enhanced (2025-12-29, 66 days)

## Verification Against CLAUDE.md Claims

| Claim | Actual | Match |
|-------|--------|-------|
| Tailscale IP 100.93.212.44 | Confirmed | MATCH |
| "From laptop (apollo): VS Code Remote SSH + Claude Code" | Apollo active on Tailscale | MATCH |
| "From phone (orpheus): SSH terminal" | Orpheus listed but status unclear | PARTIAL |
| SyncThing syncs "university, writings, film-club to apollo" | All 3 folders configured, but peers disconnected | PARTIAL (config correct, sync not active) |
| SyncThing port 8384/22000 | 8384 (GUI) and 22000 (sync) both active | MATCH |

### Verification Against MEMORY.md SyncThing Table

| MEMORY.md Folder | Actual | Match |
|------------------|--------|-------|
| courses → ~/workspace/university/courses | Configured, 2 devices | MATCH |
| reading-groups → ~/workspace/university/reading-groups | Configured, 2 devices | MATCH |
| academic-active → ~/workspace/university/courses/2025-fall | Configured, 3 devices | MATCH |
| academic-notes → ~/workspace/university/notes | Configured, 3 devices | MATCH |
| writings → ~/workspace/writings | Configured, 2 devices | MATCH |
| philosophy-film-club → ~/philosophy-film-club | Configured, 2 devices | MATCH |
| dropbox → /data/dropbox | Configured, paused, 3 devices | MATCH |

MEMORY.md does not list 2 folders that exist: "academic-processing" (/scratch/lecture-processing/incoming) and "default" (~/Sync).

---

*Audit completed: 2026-03-05*
*Feeds into: Phase 3 SEC-05 (SyncThing GUI binding), Phase 3 CLN-07 (tmux cleanup), Phase 4 ACC-01 through ACC-05 (multi-device access)*
