# Storage Audit

**Audited:** 2026-03-06
**Requirement:** AUD-01
**Domain:** Storage -- all partitions, directories >1GB, ~/.cache investigation
**Status:** Complete -- document only, no changes made

## Executive Summary

The Dionysus workstation has 4 mount points totaling ~2.3TB of raw capacity with 267GB used on /home (83%), 37GB on root (71%), 326GB on /data (19%), and /scratch nearly empty. The /home partition is the primary concern: 67GB in ~/.cache alone (huggingface 30GB, uv 25GB, pip 5.5GB, whisper 4.3GB), 16GB in .local/share/torbrowser, 12GB in .vscode/extensions, 112GB in semantic-calibre build artifacts, and 48GB across 5 conda environments. Approximately 80-100GB is recoverable through cache cleanup and selective pruning without impacting functionality, which would bring /home from 83% to ~55-60% utilization.

## Findings

### Finding 1: ~/.cache at 67GB (largest hidden directory)

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Category** | Storage / Hidden Directory Bloat |
| **Current State** | 67GB in ~/.cache with 4 major consumers: huggingface (30GB), uv (25GB), pip (5.5GB), whisper (4.3GB) |
| **Expected State** | <10GB after selective cleanup (keep active model caches, clear package caches) |
| **Remediation** | Phase 3 CLN-01: Clear pip/uv caches, prune unused huggingface models, evaluate whisper models |
| **Verified By** | `du -sh ~/.cache/*/` output captured below |

**Breakdown of ~/.cache:**

| Directory | Size | Safe to Clear? | Notes |
|-----------|------|---------------|-------|
| huggingface/ | 30G | Partial | Contains downloaded models; identify which are actively used |
| uv/ | 25G | Yes | Python package installer cache; fully rebuildable |
| pip/ | 5.5G | Yes | pip download cache; fully rebuildable |
| whisper/ | 4.3G | Partial | Whisper model files; check if audiobookify still needs them |
| datalab/ | 1.7G | Evaluate | Data processing cache from scholardoc pipeline |
| thumbnails/ | 531M | Yes | Desktop thumbnail cache; auto-regenerated |
| zlibrary-mcp/ | 158M | Evaluate | MCP server cache |
| vscode-cpptools/ | 156M | Yes | C++ IntelliSense cache for semantic-calibre; rebuilds on demand |
| torbrowser/ | 132M | Evaluate | Browser cache (separate from 16GB in .local) |
| doctr/ | 124M | Evaluate | OCR model cache |
| claude-cli-nodejs/ | 66M | Yes | Claude CLI Node.js cache; auto-downloads |
| (others) | <50M each | Low priority | tracker3 31M, typescript 12M, nvidia 7.3M, etc. |

**Estimated recoverable from ~/.cache:** ~37GB (uv 25G + pip 5.5G + thumbnails 531M + partial huggingface + whisper evaluation)

### Finding 2: /home Partition at 83% Utilization

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Category** | Storage / Partition Pressure |
| **Current State** | 267GB used of 343GB (83%), 59GB free on /home |
| **Expected State** | <70% utilization (~240GB used, 103GB free) per Phase 3 target |
| **Remediation** | Phase 3 CLN-01 (cache cleanup), CLN-05 (conda pruning), CLN-06 (project cleanup) |
| **Verified By** | `df -h /home` output: 83% used |

**Note:** The CLAUDE.md documents /home at 82% (~264GB). Actual measurement shows 83% (267GB), a 3GB increase since documentation was last updated. The trend is upward.

### Finding 3: .local/share/torbrowser at 16GB

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Storage / Application Data |
| **Current State** | 16GB in ~/.local/share/torbrowser |
| **Expected State** | Evaluate whether Tor Browser is actively used; if not, full removal saves 16GB |
| **Remediation** | Phase 3 CLN-01: Evaluate usage, remove if unused |
| **Verified By** | `du -sh ~/.local/share/torbrowser/` |

### Finding 4: .vscode/extensions at 12GB

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Storage / Development Tools |
| **Current State** | 12GB in ~/.vscode/extensions/ (only directory under .vscode besides cli/ at 4KB) |
| **Expected State** | Audit installed extensions; remove unused ones to reduce to ~4-6GB |
| **Remediation** | Phase 3 CLN-01: Extension audit and pruning |
| **Verified By** | `du -sh ~/.vscode/*/` |

**Additional VS Code overhead:** .vscode-server at 2.8GB (Remote SSH extension host). Combined VS Code footprint: ~15GB.

### Finding 5: semantic-calibre at 112GB

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Storage / Project Build Artifacts |
| **Current State** | 112GB in ~/workspace/projects/semantic-calibre/ (includes build cache) |
| **Expected State** | Keep source, move/clear build cache to reduce to ~5-10GB source only |
| **Remediation** | Phase 3 CLN-06: Clean build artifacts, evaluate build cache strategy |
| **Verified By** | `du -sh ~/workspace/projects/semantic-calibre/` |

**Context:** This is a Calibre fork (C++/Qt). Build caches for C++ projects are large but rebuildable. The 112GB is ~42% of total /home usage.

### Finding 6: miniconda3 at 48GB Across 5 Environments

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Category** | Storage / Python Environments |
| **Current State** | 48GB total across 5 conda environments plus base |
| **Expected State** | Prune unused environments, clean conda caches to reduce to ~25-30GB |
| **Remediation** | Phase 3 CLN-05: Environment audit, identify orphans, conda clean |
| **Verified By** | `du -sh ~/miniconda3/envs/*/` |

**Per-environment breakdown:**

| Environment | Size | Status | Notes |
|-------------|------|--------|-------|
| ml-dev | 12G | Evaluate | Machine learning development; may overlap with analysis |
| analysis | 8.3G | Evaluate | Data analysis; check if distinct from ml-dev |
| university | 7.9G | Active | Coursework environment |
| audio | 7.9G | Evaluate | Audiobookify support; check if audiobookify is in maintenance mode |
| acadlib-dev | 971M | Candidate for removal | acadlib was archived to /data/archive/ |
| (base) | ~11G | Keep | Estimated from total minus envs (48G - 37G) |

**Orphan candidate:** `acadlib-dev` (971MB) -- acadlib project was archived per session memory. Likely safe to remove.

### Finding 7: ~/data Symlink to /data (Correct Configuration)

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **Category** | Storage / Configuration |
| **Current State** | ~/data is a symlink to /data mount point; /data is ext4 on /dev/sda1 (1.8TB HDD) |
| **Expected State** | Current state is correct |
| **Remediation** | None needed |
| **Verified By** | `ls -la ~/data` shows symlink; `mount \| grep data` confirms /dev/sda1 |

**Note:** `du -sh ~/data/` reports 326GB because it follows the symlink. This is NOT consuming /home space -- it is on the separate 1.8TB HDD. The 326GB is primarily /data/dropbox (319GB).

### Finding 8: /scratch Partition Nearly Empty (As Expected)

| Field | Value |
|-------|-------|
| **Severity** | INFO |
| **Category** | Storage / Partition Health |
| **Current State** | 88KB used of 92GB (1%) on /scratch |
| **Expected State** | Current state is correct -- /scratch is temp processing space |
| **Remediation** | None needed; weekly cron already cleans old files |
| **Verified By** | `df -h /scratch` |

### Finding 9: Root Partition at 71%

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Category** | Storage / Partition Health |
| **Current State** | 37GB used of 55GB (71%) on root / |
| **Expected State** | <80% -- currently acceptable but monitor |
| **Remediation** | Phase 3: Docker data-root migration to /data would free significant root space |
| **Verified By** | `df -h /` |

**Context:** CLAUDE.md documents root at 70% (~37G). Current measurement: 71% (37G). The broken HWE kernel packages may be consuming some root space. Docker images stored on root are a known pressure point.

## Raw Data

### Partition Overview

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2   55G   37G   16G  71% /
/dev/nvme0n1p4  343G  267G   59G  83% /home
/dev/sdb1        92G   88K   87G   1% /scratch
/dev/sda1       1.8T  326G  1.4T  19% /data
```

### Top-Level Home Breakdown (Visible Directories)

```
326G    /home/rookslog/data/          (symlink to /data -- NOT on /home partition)
116G    /home/rookslog/workspace/
48G     /home/rookslog/miniconda3/
3.0G    /home/rookslog/snap/
157M    /home/rookslog/scripts/
64M     /home/rookslog/nltk_data/
6.2M    /home/rookslog/Calibre Library/
4.3M    /home/rookslog/Downloads/
3.2M    /home/rookslog/Pictures/
2.0M    /home/rookslog/philosophy-film-club/
232K    /home/rookslog/docs/
8.0K    /home/rookslog/Sync/
4.0K    /home/rookslog/Videos/
4.0K    /home/rookslog/Templates/
4.0K    /home/rookslog/Public/
4.0K    /home/rookslog/Music/
4.0K    /home/rookslog/mcp-servers/
4.0K    /home/rookslog/Documents/
4.0K    /home/rookslog/Desktop/
```

### Hidden Directory Breakdown

```
67G     /home/rookslog/.cache
18G     /home/rookslog/.local
12G     /home/rookslog/.vscode
2.8G    /home/rookslog/.vscode-server
1.4G    /home/rookslog/.claude
650M    /home/rookslog/.config
275M    /home/rookslog/.npm
100M    /home/rookslog/.npm-global
94M     /home/rookslog/.EasyOCR
84M     /home/rookslog/.serena
3.3M    /home/rookslog/.codex
3.2M    /home/rookslog/.audiobookify
2.0M    /home/rookslog/.triton
740K    /home/rookslog/.git
424K    /home/rookslog/.planning
272K    /home/rookslog/.docker
248K    /home/rookslog/.dotnet
232K    /home/rookslog/.gsd
76K     /home/rookslog/.pki
56K     /home/rookslog/.acadlib
52K     /home/rookslog/.claude.json.backup
52K     /home/rookslog/.bash_history
48K     /home/rookslog/.claude.json
36K     /home/rookslog/.ssh
36K     /home/rookslog/.conda
32K     /home/rookslog/.pytest_cache
20K     /home/rookslog/.copilot
12K     /home/rookslog/.gnupg
8.0K    /home/rookslog/.streamlit
8.0K    /home/rookslog/.philosophy_tools
```

### ~/.cache Subdirectory Breakdown (67GB Total)

```
30G     /home/rookslog/.cache/huggingface/
25G     /home/rookslog/.cache/uv/
5.5G    /home/rookslog/.cache/pip/
4.3G    /home/rookslog/.cache/whisper/
1.7G    /home/rookslog/.cache/datalab/
531M    /home/rookslog/.cache/thumbnails/
158M    /home/rookslog/.cache/zlibrary-mcp/
156M    /home/rookslog/.cache/vscode-cpptools/
132M    /home/rookslog/.cache/torbrowser/
124M    /home/rookslog/.cache/doctr/
66M     /home/rookslog/.cache/claude-cli-nodejs/
31M     /home/rookslog/.cache/tracker3/
12M     /home/rookslog/.cache/typescript/
7.3M    /home/rookslog/.cache/nvidia/
4.4M    /home/rookslog/.cache/calibre/
2.5M    /home/rookslog/.cache/pip-audit/
2.3M    /home/rookslog/.cache/evolution/
680K    /home/rookslog/.cache/vlc/
424K    /home/rookslog/.cache/gstreamer-1.0/
216K    /home/rookslog/.cache/ibus/
176K    /home/rookslog/.cache/fontconfig/
144K    /home/rookslog/.cache/torch/
144K    /home/rookslog/.cache/matplotlib/
44K     /home/rookslog/.cache/ubuntu-pro/
40K     /home/rookslog/.cache/qtshadercache-x86_64-little_endian-lp64/
28K     /home/rookslog/.cache/pre-commit/
12K     /home/rookslog/.cache/update-manager-core/
12K     /home/rookslog/.cache/Microsoft/
12K     /home/rookslog/.cache/conda-anaconda-tos/
12K     /home/rookslog/.cache/calibre-ebook.com/
8.0K    /home/rookslog/.cache/ubuntu-report/
8.0K    /home/rookslog/.cache/pipx/
8.0K    /home/rookslog/.cache/libimobiledevice/
8.0K    /home/rookslog/.cache/gnome-desktop-thumbnailer/
8.0K    /home/rookslog/.cache/geeqie/
8.0K    /home/rookslog/.cache/conda/
8.0K    /home/rookslog/.cache/claude/
8.0K    /home/rookslog/.cache/chroma/
4.0K    /home/rookslog/.cache/obexd/
4.0K    /home/rookslog/.cache/ibus-table/
```

### ~/.local/share Breakdown

```
16G     /home/rookslog/.local/share/torbrowser/
1.8G    /home/rookslog/.local/share/claude/
159M    /home/rookslog/.local/share/Trash/
129M    /home/rookslog/.local/share/pipx/
364K    /home/rookslog/.local/share/nautilus/
160K    /home/rookslog/.local/share/evolution/
112K    /home/rookslog/.local/share/gvfs-metadata/
76K     /home/rookslog/.local/share/xorg/
28K     /home/rookslog/.local/share/CMakeTools/
20K     /home/rookslog/.local/share/calibre-ebook.com/
16K     /home/rookslog/.local/share/uv/
16K     /home/rookslog/.local/share/org.gnome.TextEditor/
12K     /home/rookslog/.local/share/keyrings/
12K     /home/rookslog/.local/share/gnome-shell/
12K     /home/rookslog/.local/share/geeqie/
8.0K    /home/rookslog/.local/share/vlc/
8.0K    /home/rookslog/.local/share/icc/
8.0K    /home/rookslog/.local/share/gthumb/
8.0K    /home/rookslog/.local/share/flatpak/
4.0K    /home/rookslog/.local/share/sounds/
4.0K    /home/rookslog/.local/share/nvim/
4.0K    /home/rookslog/.local/share/nano/
4.0K    /home/rookslog/.local/share/man/
4.0K    /home/rookslog/.local/share/ibus-table/
4.0K    /home/rookslog/.local/share/gnome-settings-daemon/
4.0K    /home/rookslog/.local/share/backgrounds/
4.0K    /home/rookslog/.local/share/applications/
```

### ~/.vscode Breakdown

```
12G     /home/rookslog/.vscode/extensions/
4.0K    /home/rookslog/.vscode/cli/
```

### Conda Per-Environment Sizes

```
12G     /home/rookslog/miniconda3/envs/ml-dev/
8.3G    /home/rookslog/miniconda3/envs/analysis/
7.9G    /home/rookslog/miniconda3/envs/university/
7.9G    /home/rookslog/miniconda3/envs/audio/
971M    /home/rookslog/miniconda3/envs/acadlib-dev/
```

### Workspace Per-Project Sizes

```
112G    /home/rookslog/workspace/projects/semantic-calibre/
731M    /home/rookslog/workspace/projects/zlibrary-mcp/
624M    /home/rookslog/workspace/projects/scholardoc/
130M    /home/rookslog/workspace/projects/robotic-psalms/
112M    /home/rookslog/workspace/projects/claude-enhanced/
79M     /home/rookslog/workspace/projects/get-shit-done-reflect/
56M     /home/rookslog/workspace/projects/philoso-roo/
31M     /home/rookslog/workspace/projects/audiobookify/
23M     /home/rookslog/workspace/projects/mcp-vector-database/
7.8M    /home/rookslog/workspace/projects/bypy/
6.0M    /home/rookslog/workspace/projects/philo-rag-simple/
3.5M    /home/rookslog/workspace/projects/hermeneutic-workspace-plugin/
752K    /home/rookslog/workspace/projects/philograph-mcp/
```

### ~/data Symlink and /data Mount

```
~/data -> /data (symlink)
/dev/sda1 on /data type ext4 (rw,noatime)
```

### /data Breakdown

```
319G    /data/dropbox/
3.1G    /data/backups/
2.7G    /data/university/
1.1G    /data/archive/
16K     /data/lost+found/
4.0K    /data/models/
4.0K    /data/experiments/
4.0K    /data/embeddings/
4.0K    /data/datasets/
4.0K    /data/corpora/
4.0K    /data/analysis-results/
```

### All Directories >1GB Under /home

| Size | Directory |
|------|-----------|
| 116G | ~/workspace/ |
| 67G | ~/.cache/ |
| 48G | ~/miniconda3/ |
| 18G | ~/.local/ |
| 12G | ~/.vscode/ |
| 3.0G | ~/snap/ |
| 2.8G | ~/.vscode-server/ |
| 1.4G | ~/.claude/ |

**Note:** ~/data/ (326G) excluded from this table -- it is a symlink to /data HDD, not consuming /home partition space.

**Total accounted on /home:** ~268GB (aligns with df reported 267GB used)

## Verification Against Research

| Claim (from CLAUDE.md / synthesis.md) | Actual | Status |
|---------------------------------------|--------|--------|
| ~/.cache is 67GB | 67GB confirmed | VERIFIED |
| /home at 82% (~264G) | 83% (267G) -- 3GB higher | DRIFT (minor upward) |
| Root at 70% (~37G) | 71% (37G) | VERIFIED (within rounding) |
| /scratch at ~0 | 88KB (1%) | VERIFIED |
| /data at 19% (~326G) | 19% (326G) | VERIFIED |
| semantic-calibre ~112GB with build cache | 112G confirmed | VERIFIED |
| huggingface ~30G in cache | 30G confirmed | VERIFIED |
| uv ~25G in cache | 25G confirmed | VERIFIED |
| pip ~5.5G in cache | 5.5G confirmed | VERIFIED |
| whisper ~4.3G in cache | 4.3G confirmed | VERIFIED |
| torbrowser ~16GB in .local | 16G confirmed | VERIFIED |
| .vscode extensions ~12GB | 12G confirmed | VERIFIED |
| miniconda3 ~48GB | 48G confirmed (5 envs + base) | VERIFIED |

**All research claims verified.** Only drift: /home utilization increased from 82% to 83% (3GB growth since last documentation update).

## Remediation Summary

| Finding | Severity | Estimated Recovery | Remediation Phase |
|---------|----------|-------------------|-------------------|
| ~/.cache bloat (67GB) | CRITICAL | ~37GB | Phase 3 CLN-01 |
| /home at 83% | HIGH | Target: <70% | Phase 3 CLN-01, CLN-05, CLN-06 |
| torbrowser 16GB | MEDIUM | Up to 16GB | Phase 3 CLN-01 |
| .vscode extensions 12GB | MEDIUM | ~6GB | Phase 3 CLN-01 |
| semantic-calibre 112GB | MEDIUM | ~100GB (build cache) | Phase 3 CLN-06 |
| miniconda3 48GB | MEDIUM | ~15-20GB | Phase 3 CLN-05 |
| Root at 71% | LOW | Docker migration | Phase 3 (Docker data-root to /data) |

**Total estimated recoverable:** 80-100GB on /home partition through cache cleanup, conda pruning, and build artifact removal.

---
*Audit completed: 2026-03-06*
*No system changes made -- document only*
