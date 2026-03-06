# Domain Audit: Toolchain Inventory (AUD-07)

**Audited:** 2026-03-05
**Scope:** Node.js, Python, package managers, caches, conda environments, scripts, kernel state
**Severity Scale:** HIGH (action needed Phase 3-4) | MEDIUM (should address) | LOW (cosmetic/minor)

## Executive Summary

- **Node.js:** v18.19.1 (system install at /usr/bin/node) -- needs upgrade to v22 LTS
- **Python:** 3.13.5 (miniconda3), system Python 3.12.3 also present
- **Conda environments:** 5 (+ base), totaling 48 GB for all of miniconda3
- **Package manager caches:** 30.8 GB total (pip 5.5 GB + uv 25 GB + npm 275 MB)
- **No node version manager:** nvm/fnm not installed
- **Running kernel:** 6.14.0-36-generic (healthy)
- **Broken kernel packages:** 6.17.0-14 (headers and image in failed state)
- **Linger not enabled:** systemd user services will not persist across logout
- **Scripts directory:** 46 files including 155 MB Miniconda installer

## Findings

### [HIGH] Node.js 18.19.1 -- Needs Upgrade to v22 LTS

| Component | Version | Location |
|-----------|---------|----------|
| Node.js | v18.19.1 | /usr/bin/node |
| npm | 9.2.0 | /usr/bin/npm |
| npx | 9.2.0 | /usr/bin/npx |

Node.js 18 reaches end-of-life April 2025 (already past). Node.js 22 LTS is the current recommended version. All TypeScript projects (claude-enhanced, get-shit-done-reflect, hermeneutic-workspace-plugin, zlibrary-mcp) should be tested against Node 22 before upgrade.

No node version manager (nvm or fnm) is installed. System node is installed via apt (dpkg). Consider installing fnm for version management.

**Global npm packages:**
- @openai/codex@0.106.0 (installed via ~/.npm-global)

**Remediation:** Phase 4 DEV-01 -- upgrade to Node.js 22 LTS. Install fnm or nvm for version management.

### [HIGH] Package Manager Cache Overlap (30.8 GB)

| Cache | Size | Location |
|-------|------|----------|
| pip | 5.5 GB | ~/.cache/pip |
| uv | 25 GB | ~/.cache/uv |
| npm | 275 MB | ~/.npm |

**Total: 30.8 GB of package manager caches.**

pip and uv both cache Python packages. Since uv is the recommended modern Python package manager, the pip cache (5.5 GB) is largely redundant. The uv cache at 25 GB is substantial but expected for a system with many Python projects.

These caches are part of the broader ~/.cache issue (67 GB total). The 30.8 GB here accounts for roughly 46% of the cache directory.

**Remediation:** Phase 3 CLN-05 -- clear pip cache (`pip cache purge`), evaluate uv cache (`uv cache prune`), clear npm cache (`npm cache clean --force`).

### [HIGH] Broken HWE Kernel Packages (6.17.0-14)

The 6.17.0-14 kernel packages are in broken/failed install state:

| Package | Version | Status |
|---------|---------|--------|
| linux-generic-hwe-24.04 | 6.17.0-14.14~24.04.1 | iU (installed, Unpacked) |
| linux-headers-6.17.0-14-generic | 6.17.0-14.14~24.04.1 | iF (installed, Failed) |
| linux-headers-generic-hwe-24.04 | 6.17.0-14.14~24.04.1 | iU (installed, Unpacked) |
| linux-image-6.17.0-14-generic | 6.17.0-14.14~24.04.1 | iF (installed, Failed) |

The running kernel (6.14.0-36-generic) is healthy and unaffected. The 6.17.0-14 packages are from a failed HWE upgrade attempt. These broken packages prevent `apt upgrade` from completing cleanly.

**Remediation:** Phase 3 CLN-02 -- `sudo dpkg --remove --force-remove-reinstreq linux-headers-6.17.0-14-generic linux-image-6.17.0-14-generic && sudo apt --fix-broken install` (requires sudo/Codex CLI).

### [MEDIUM] 5 Conda Environments (48 GB total miniconda3)

| Environment | Size | Purpose |
|-------------|------|---------|
| base | ~11 GB (48G total - 37G envs) | Default (Python 3.13.5) |
| ml-dev | 12 GB | Machine learning development |
| analysis | 8.3 GB | Data analysis |
| university | 7.9 GB | University coursework |
| audio | 7.9 GB | Audio processing (audiobookify) |
| acadlib-dev | 971 MB | Academic library development |

**Total miniconda3:** 48 GB

**Potential orphans:**
- **acadlib-dev:** The acadlib project was archived to /data/archive/ (per MEMORY.md). This environment may be orphaned (971 MB -- small but should be verified).
- **analysis:** No project directly maps to this environment. May be a general-purpose env.

**Remediation:** Phase 3 CLN-04 -- verify which conda environments are actively used. Remove orphaned environments.

### [MEDIUM] Linger Not Enabled for systemd User Services

```
Linger=no
```

Without linger, systemd user services (e.g., Obsidian Headless planned for Phase 4) will not persist after the user logs out. Since this is a headless server accessed remotely, user services must survive SSH disconnection.

**Remediation:** Phase 4 DEV-04 -- `sudo loginctl enable-linger rookslog` (requires sudo).

### [LOW] Miniconda3 Installer in ~/scripts/ (155 MB)

`Miniconda3-latest-Linux-x86_64.sh` (162 MB) is still in ~/scripts/. This is a one-time installer that has already been used.

**Remediation:** Delete installer to reclaim 155 MB.

### [LOW] pipx Has Stale Installation (superclaude)

pipx manages two packages:

| Package | Version | Python |
|---------|---------|--------|
| audiobookify | 2.3.0 | 3.12.3 |
| superclaude | 4.1.5 | 3.12.3 |

SuperClaude was removed from the project (per MEMORY.md: "SuperClaude removed, ~4.4k tokens/session saved"). The pipx installation remains.

**Remediation:** `pipx uninstall superclaude` to clean up.

### [LOW] Scripts Directory Needs Cleanup

~/scripts/ contains 46 files, many from initial system setup (Sep 2024-2025). Most are one-time setup scripts that are no longer needed:

**Cron-referenced (actively used):**
- `audit-workspace.sh` -- Weekly project git status report
- `audit-home.sh` -- Weekly home directory convention check

**Potentially useful:**
- `root-cleanup.sh` -- Root partition cleanup utility

**Likely stale (one-time setup scripts from initial system build):**
- `COMPLETE_SETUP.sh`, `CONDA_SETUP_SCRIPT.sh`, `IMMEDIATE_SETUP_SCRIPT.sh` -- Initial setup
- `FOUNDATION_IMPLEMENTATION.sh`, `FOUNDATION_VALIDATION.sh` -- Initial validation
- `STORAGE_TIERING_AUTOMATION.sh` -- Storage setup
- `setup-course.sh`, `setup_directories.sh` -- One-time directory setup
- `get-docker.sh` -- Docker installer (20 KB)
- `migrate_to_git.sh` -- One-time migration
- Various stub scripts (audio_backup_manager.py, batch_processor.py, etc.) -- placeholder scripts (~120 bytes each

**Remediation:** Review and archive stale scripts to /data/archive/scripts/ or remove.

## Raw Data

### Version Table

| Tool | Version | Location | Managed By |
|------|---------|----------|------------|
| Node.js | v18.19.1 | /usr/bin/node | apt (system) |
| npm | 9.2.0 | /usr/bin/npm | apt (system) |
| Python | 3.13.5 | ~/miniconda3/bin/python3 | conda |
| pip | 25.1 | ~/miniconda3/bin/pip | conda |
| uv | 0.8.22 | ~/.local/bin/uv | standalone |
| conda | (in PATH) | ~/miniconda3/bin/conda | miniconda |
| @openai/codex | 0.106.0 | ~/.npm-global | npm global |

### Cache Size Table

| Cache | Size | Location | Redundancy |
|-------|------|----------|------------|
| pip | 5.5 GB | ~/.cache/pip | Overlaps with uv |
| uv | 25 GB | ~/.cache/uv | Primary Python PM |
| npm | 275 MB | ~/.npm | Only Node PM cache |
| **Total** | **30.8 GB** | | |

### Conda Environment Table

| Environment | Size | Python | Last Used |
|-------------|------|--------|-----------|
| base | ~11 GB | 3.13.5 | Active (default) |
| ml-dev | 12 GB | ? | Unknown |
| analysis | 8.3 GB | ? | Unknown |
| university | 7.9 GB | ? | Active (coursework) |
| audio | 7.9 GB | ? | Maintenance (audiobookify) |
| acadlib-dev | 971 MB | ? | Likely orphaned (project archived) |

### Cron Jobs

| Schedule | Command | Script/Location |
|----------|---------|-----------------|
| Sun 00:00 | audit-workspace.sh | ~/scripts/audit-workspace.sh |
| Sun 00:05 | audit-home.sh | ~/scripts/audit-home.sh |
| Sun 03:00 | find /scratch -mtime +7 -delete | Inline |
| Sun 04:00 | docker system prune -f | Inline |
| Every 6hr | df / check >90% | Inline |

### Kernel State

| Version | Status | Notes |
|---------|--------|-------|
| 6.14.0-36-generic | Running, healthy | Current kernel |
| 6.17.0-14-generic | BROKEN (iF/iU) | Failed HWE upgrade, headers and image in failed state |

### Scripts Inventory (~/scripts/)

**Actively used (cron):**
- audit-workspace.sh (2.4 KB)
- audit-home.sh (3.0 KB)

**Utility scripts:**
- root-cleanup.sh (9.4 KB) -- root partition cleanup

**One-time setup scripts (likely stale):**
- COMPLETE_SETUP.sh (8.2 KB)
- CONDA_SETUP_SCRIPT.sh (6.3 KB)
- FOUNDATION_IMPLEMENTATION.sh (16 KB)
- FOUNDATION_VALIDATION.sh (9.6 KB)
- IMMEDIATE_SETUP_SCRIPT.sh (7.6 KB)
- STORAGE_TIERING_AUTOMATION.sh (4.7 KB)
- get-docker.sh (20 KB)
- setup-course.sh (5.6 KB)
- setup_directories.sh (2.5 KB)
- migrate_to_git.sh (2.4 KB)
- maintain-home-org.sh (3.0 KB)
- test-remote-access.sh (1.6 KB)

**Stub/placeholder scripts (~120 bytes each):**
- audio_backup_manager.py, batch_processor.py, directory_watcher.py
- encrypt_filenames.py, organize_transcriptions.py, plugin_adapter.py
- transcribe_lectures.py, transcribe_lectures_improved.py
- transcription_gui.py, web_validation_server.py

**Installers:**
- Miniconda3-latest-Linux-x86_64.sh (155 MB)

**Other:**
- codex-wave3-logs/ (directory)
- pipelines/ (directory)
- services/ (directory)
- setup/ (directory)
- tools/ (directory)

## Verification Against CLAUDE.md Claims

| Claim | Actual | Match |
|-------|--------|-------|
| "Broken HWE kernel package set (6.17.0-14)" | Confirmed: iF/iU status in dpkg | MATCH |
| "~/.cache/ is 67GB" | Cache pip+uv+npm = 30.8GB (partial) | PARTIAL (30.8GB of 67GB accounted for) |
| "CUDA 11.8" | Not tested in this audit (GPU audit is AUD-04) | N/A |
| Cron: "Sun 00:00 audit-workspace.sh" | Confirmed | MATCH |
| Cron: "Sun 00:05 audit-home.sh" | Confirmed | MATCH |
| Cron: "Sun 03:00 find /scratch..." | Confirmed | MATCH |
| Cron: "Sun 04:00 docker system prune" | Confirmed | MATCH |
| Cron: "Every 6hr df check" | Confirmed (*/6 schedule) | MATCH |

---

*Audit completed: 2026-03-05*
*Feeds into: Phase 3 CLN-02 (broken kernel), CLN-04 (conda cleanup), CLN-05 (cache cleanup), Phase 4 DEV-01 (Node upgrade), DEV-02 (Python strategy), DEV-04 (linger/systemd)*
