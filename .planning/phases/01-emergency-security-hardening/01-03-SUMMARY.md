---
phase: 01-emergency-security-hardening
plan: 03
subsystem: infra
tags: [audit, projects, network, tailscale, syncthing, tmux, nodejs, python, conda, toolchain]

# Dependency graph
requires:
  - phase: none
    provides: "First audit of these domains"
provides:
  - "Project ecosystem state for all 13 projects with disk/git breakdown"
  - "Network and access topology (Tailscale, SyncThing, tmux, SSH)"
  - "Installed toolchain inventory (Node 18, Python 3.13, 48GB conda, 30.8GB caches)"
affects: [01-04-PLAN, phase-3-stabilization, phase-4-foundation]

# Tech tracking
tech-stack:
  added: []
  patterns: [per-domain-audit-template, severity-tagged-findings]

key-files:
  created:
    - ".planning/research/project-audit.md"
    - ".planning/research/network-audit.md"
    - ".planning/research/toolchain-audit.md"
  modified: []

key-decisions:
  - "Classified 30.8GB cache overlap (pip+uv+npm) as HIGH priority for Phase 3 CLN-05"
  - "Identified acadlib-dev conda env as likely orphaned (project archived)"
  - "Documented Node.js 18.19.1 as past EOL, requiring Phase 4 DEV-01 upgrade"

patterns-established:
  - "Per-domain audit template: Executive Summary, Findings (severity-tagged), Raw Data, Verification Against CLAUDE.md"

requirements-completed: [AUD-05, AUD-06, AUD-07]

# Metrics
duration: 5min
completed: 2026-03-05
---

# Phase 01 Plan 03: Project/Network/Toolchain Audit Summary

**Full system inventory: 13 projects (112GB dominated by semantic-calibre), 19 stale tmux sessions, Node 18 EOL, 30.8GB cache overlap, broken HWE kernel confirmed**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-06T02:30:11Z
- **Completed:** 2026-03-06T02:35:27Z
- **Tasks:** 3
- **Files created:** 3

## Accomplishments
- Comprehensive project ecosystem audit covering all 13 projects with disk breakdown, git status, MCP symlink validation, and CLAUDE.md discrepancy identification (2 unlisted projects found)
- Network/access audit documenting 4 Tailscale peers, 9 SyncThing folders (both peers disconnected), 19 tmux sessions (11 stale), and SSH configuration
- Toolchain inventory: Node.js 18.19.1 (past EOL), Python 3.13.5 via conda, 5 conda environments (48GB total), 30.8GB package manager cache overlap, broken HWE kernel confirmed, linger=no

## Task Commits

Each task was committed atomically:

1. **Task 1: Project ecosystem audit (AUD-05)** - `15baa00` (feat)
2. **Task 2: Network and access audit (AUD-06)** - `d4de19c` (feat)
3. **Task 3: Toolchain inventory (AUD-07)** - `7854733` (feat)

## Files Created/Modified
- `.planning/research/project-audit.md` - Per-project table with disk, git, status for all 13 projects; identifies 2 unlisted in CLAUDE.md
- `.planning/research/network-audit.md` - Tailscale peers, SyncThing folders/peers, tmux sessions, SSH keys
- `.planning/research/toolchain-audit.md` - Node/Python versions, conda envs with sizes, cache quantification, kernel state, scripts inventory

## Decisions Made
- Classified the 30.8GB cache overlap (pip 5.5GB + uv 25GB) as HIGH priority for Phase 3 CLN-05, since pip is redundant when uv is the primary package manager
- Identified acadlib-dev conda environment (971MB) as likely orphaned since the acadlib project was archived to /data/archive/
- Node.js 18.19.1 is past end-of-life (April 2025), documented as HIGH priority for Phase 4 DEV-01

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

Minor: The SyncThing REST API `system/status` endpoint returned different keys than expected in the plan's script (no `startedAt` key). Adapted the query to use available keys. This did not affect the audit completeness -- uptime was captured via the `uptime` field (93.9 days).

## User Setup Required

None - no external service configuration required. This was a read-only audit.

## Next Phase Readiness
- All three audit domains complete and ready for consolidation in 01-04-PLAN (system map synthesis)
- Key Phase 3 inputs identified: broken kernel (CLN-02), cache cleanup (CLN-05), conda orphans (CLN-04), tmux cleanup (CLN-07)
- Key Phase 4 inputs identified: Node upgrade (DEV-01), Python strategy (DEV-02), linger (DEV-04), SSH config (ACC-03)
- No blockers for next plan

## Self-Check: PASSED

- All 3 created files verified on disk
- All 3 task commits verified in git history (15baa00, d4de19c, 7854733)

---
*Phase: 01-emergency-security-hardening*
*Completed: 2026-03-05*
