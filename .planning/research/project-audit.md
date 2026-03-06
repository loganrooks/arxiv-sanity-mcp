# Domain Audit: Project Ecosystem (AUD-05)

**Audited:** 2026-03-05
**Scope:** All projects in ~/workspace/projects/, MCP server symlinks, running services
**Severity Scale:** HIGH (action needed Phase 3-4) | MEDIUM (should address) | LOW (cosmetic/minor)

## Executive Summary

- **Total projects:** 13 (vs. 11 listed in CLAUDE.md)
- **Total disk usage:** ~114.6 GB across all projects
- **Active projects (commit < 2 months):** 4 (scholardoc, get-shit-done-reflect, hermeneutic-workspace-plugin, zlibrary-mcp)
- **Maintenance/stale projects (commit 3+ months):** 7 (audiobookify, claude-enhanced, philo-rag-simple, robotic-psalms, semantic-calibre, bypy, philoso-roo)
- **Inactive/dormant projects (commit 9+ months):** 2 (mcp-vector-database, philograph-mcp)
- **Dominant disk consumer:** semantic-calibre at 112 GB (97.7% of total project disk)
- **MCP server symlinks:** 2 present (philo-rag-simple, zlibrary-mcp), 5 MCP servers listed in CLAUDE.md without symlinks (expected -- they use different runtime patterns)
- **Projects with dirty git state:** 10 of 13 (77%)
- **Running project services:** 1 (uvicorn on port 9001 for PHL410 annotation tool)

## Findings

### [MEDIUM] CLAUDE.md Project Table Outdated (13 actual vs 11 listed)

Two projects exist in ~/workspace/projects/ that are NOT listed in the CLAUDE.md project table:

| Unlisted Project | Lang | Size | Last Commit | Description |
|-----------------|------|------|-------------|-------------|
| get-shit-done-reflect | TypeScript | 79 MB | 20 min ago (active) | GSD framework fork/extension |
| hermeneutic-workspace-plugin | TypeScript | 3.5 MB | 4 days ago (active) | Obsidian plugin for hermeneutic workspace |

Both are actively developed. CLAUDE.md should be updated to include them.

**Remediation:** Update CLAUDE.md project table (Phase 4 or sooner).

### [MEDIUM] semantic-calibre Dominates Disk (112 GB)

- Total: 112 GB (97.7% of all project disk usage)
- Git history: 325 MB
- node_modules: 31 MB
- Remaining ~111.6 GB is build cache and source (Calibre fork with C++/Qt build artifacts)
- Status: Active, but last commit 3 months ago
- CLAUDE.md correctly documents "112GB with build cache"

**Remediation:** Consider moving build cache to /scratch or /data if not actively building (Phase 3 CLN-06).

### [MEDIUM] scholardoc Large Git History (134 MB .git, 106 uncommitted files)

- Total: 624 MB (git: 134 MB, .venv: 100 MB)
- 106 uncommitted files in working tree (highest of any project)
- Last commit: 59 minutes ago (very active)
- Branch: feature/01.1-01-foundation-types

This is expected for an active project with binary fixtures or test data, but 106 dirty files is worth investigating.

**Remediation:** Review scholardoc working directory for files that should be committed or gitignored.

### [MEDIUM] 10 Projects with Dirty Git State

| Project | Uncommitted Files | Branch | Last Commit |
|---------|-------------------|--------|-------------|
| scholardoc | 106 | feature/01.1-01-foundation-types | 59 min ago |
| claude-enhanced | 69 | feature/philpapers-mcp-server | 6 weeks ago |
| bypy | 12 | master | 4 months ago |
| robotic-psalms | 10 | feature/docker-and-bugfixes | 3 months ago |
| semantic-calibre | 7 | feature/phase4.2-research-projects | 3 months ago |
| zlibrary-mcp | 3 | master | 3 weeks ago |
| get-shit-done-reflect | 3 | gsd/phase-41-health-score-automation | 20 min ago |
| audiobookify | 2 | feature/v2.6.0-tui-enhancements | 3 months ago |
| philo-rag-simple | 1 | main | 3 months ago |

Only hermeneutic-workspace-plugin, mcp-vector-database, philograph-mcp, and philoso-roo have clean working trees.

**Remediation:** Each project should have its uncommitted changes resolved (committed, stashed, or discarded) as part of ecosystem maintenance. Not blocking but contributes to workspace entropy.

### [LOW] Dormant Projects (9+ months since last commit)

| Project | Last Commit | Status in CLAUDE.md |
|---------|-------------|---------------------|
| mcp-vector-database | 10 months ago (2025-05-05) | Inactive |
| philograph-mcp | 9 months ago (2025-06-10) | Inactive |
| philoso-roo | 10 months ago (2025-05-07) | Keep |

CLAUDE.md status labels are accurate for these projects.

### [LOW] bypy 36 Commits Behind Remote

bypy (upstream fork of kovidgoyal/bypy) is 36 commits behind remote. This is the build system for semantic-calibre.

**Remediation:** Pull upstream changes before next semantic-calibre build.

### [INFO] MCP Server Symlink Health

| Symlink | Target | Valid |
|---------|--------|-------|
| ~/mcp-servers/philo-rag-simple | ~/workspace/projects/philo-rag-simple | Yes |
| ~/mcp-servers/zlibrary-mcp | ~/workspace/projects/zlibrary-mcp | Yes |

CLAUDE.md lists 7 MCP servers: sequential-thinking, serena, context7, tavily, morphllm, philpapers, zlibrary. Only 2 have symlinks in ~/mcp-servers/. The others use npm/npx runtime patterns configured in ~/.claude.json, so missing symlinks are expected for those.

Note: philo-rag-simple has a symlink but is not in the MCP server list in CLAUDE.md. The philpapers MCP server is listed but may run from a different location (likely within claude-enhanced).

### [INFO] Running Project Services

Only one project service is currently running:

- **Uvicorn on port 9001** — PHL410 annotation tool
  - Running since Jan 16 (49 days)
  - Bound to 0.0.0.0 (flagged in security-audit, cross-reference SEC-01)
  - Using miniconda3 Python 3.13
  - Source: ~/workspace/writings/PHL410_CryptOfCogito/preprocess/scripts/annotation_tool
  - Note: This is a university coursework tool, not from ~/workspace/projects/

## Raw Data: Per-Project Table

| Project | Total | .git | node_modules | .venv | Branch | Last Commit | Dirty | CLAUDE.md Status | Lang |
|---------|-------|------|-------------|-------|--------|-------------|-------|------------------|------|
| audiobookify | 31M | 11M | -- | -- | feature/v2.6.0-tui-enhancements | 2025-12-17 | 2 | Maintenance | Python |
| bypy | 7.8M | 2.7M | -- | -- | master | 2025-11-02 | 12 | Upstream fork | Python |
| claude-enhanced | 112M | 6.4M | -- | -- | feature/philpapers-mcp-server | 2026-01-25 | 69 | Active | TypeScript |
| get-shit-done-reflect | 79M | 7.8M | 50M | -- | gsd/phase-41-health-score-automation | 2026-03-05 | 3 | **NOT LISTED** | TypeScript |
| hermeneutic-workspace-plugin | 3.5M | 916K | -- | -- | codex/mcp-recovery-bundle | 2026-03-01 | 0 | **NOT LISTED** | TypeScript |
| mcp-vector-database | 23M | 5.7M | -- | -- | main | 2025-05-05 | 0 | Inactive | Python |
| philograph-mcp | 752K | 320K | -- | -- | main | 2025-06-10 | 0 | Inactive | Python |
| philo-rag-simple | 6.0M | 1.5M | -- | -- | main | 2025-11-30 | 1 | Maintenance | Python |
| philoso-roo | 56M | 51M | -- | -- | main | 2025-05-07 | 0 | Keep | Python |
| robotic-psalms | 130M | 860K | -- | -- | feature/docker-and-bugfixes | 2025-12-01 | 10 | Maintenance | Python |
| scholardoc | 624M | 134M | -- | 100M | feature/01.1-01-foundation-types | 2026-03-05 | 106 | Active | Python |
| semantic-calibre | 112G | 325M | 31M | -- | feature/phase4.2-research-projects | 2025-12-17 | 7 | Active | C++/Qt |
| zlibrary-mcp | 733M | 136M | 101M | 435M | master | 2026-02-11 | 3 | Active | TS/Python |

**Total disk:** ~114.6 GB
**Projects with node_modules:** 3 (get-shit-done-reflect 50M, semantic-calibre 31M, zlibrary-mcp 101M = 182M total)
**Projects with .venv:** 2 (scholardoc 100M, zlibrary-mcp 435M = 535M total)

## Verification Against CLAUDE.md Claims

| Claim | Actual | Match |
|-------|--------|-------|
| "11 projects listed" | 13 actual projects | MISMATCH (get-shit-done-reflect, hermeneutic-workspace-plugin unlisted) |
| semantic-calibre "112GB with build cache" | 112 GB confirmed | MATCH |
| scholardoc status "Active" | Last commit 59 min ago, 106 dirty files | MATCH |
| zlibrary-mcp status "Active" | Last commit 3 weeks ago | MATCH |
| claude-enhanced status "Active" | Last commit 6 weeks ago | MATCH (borderline -- no commits in over a month) |
| mcp-vector-database status "Inactive" | No commits in 10 months | MATCH |
| philograph-mcp status "Inactive" | No commits in 9 months | MATCH |
| bypy "Upstream fork" | 36 commits behind upstream | MATCH |
| PaddleOCR "Docker container, healthy" | Not in ~/workspace/projects/ (Docker) | N/A (correct -- it's a Docker container, not a project) |
| "Runtime symlinks in ~/mcp-servers/" | 2 symlinks present, both valid | PARTIAL (only 2 of potentially more) |
| philoso-roo status "Keep" | No activity in 10 months, clean tree | MATCH |

---

*Audit completed: 2026-03-05*
*Feeds into: Phase 3 CLN-06 (disk reduction), Phase 4 (CLAUDE.md update), 01-04-PLAN (consolidated system map)*
