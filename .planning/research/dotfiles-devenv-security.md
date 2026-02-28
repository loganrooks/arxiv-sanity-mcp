# Research: Dotfiles Management, Development Environment & Security Hardening

**Domain:** Workstation infrastructure — configuration management, toolchain maintenance, security
**Researched:** 2026-02-28
**Overall confidence:** HIGH (most findings verified against current system state + official docs)

---

## Table of Contents

1. [Dotfiles Management](#1-dotfiles-management)
2. [Node.js Upgrade Path](#2-nodejs-upgrade-path)
3. [Python Environment Strategy](#3-python-environment-strategy)
4. [VS Code Extension Cleanup](#4-vs-code-extension-cleanup)
5. [Security Hardening](#5-security-hardening)
6. [Cache Cleanup](#6-cache-cleanup)
7. [Broken Kernel Fix](#7-broken-kernel-fix)
8. [Roadmap Implications](#8-roadmap-implications)

---

## 1. Dotfiles Management

### Recommendation: GNU Stow

**Why Stow over chezmoi, yadm, or bare git repo:**

| Tool | Approach | Complexity | Multi-machine | Best For |
|------|----------|-----------|---------------|----------|
| **GNU Stow** | Symlink farm | Minimal | Manual | Single machine, simplicity |
| chezmoi | File copy + templates | High | Excellent | Many diverse machines, secrets |
| yadm | Bare git wrapper | Medium | Good | Git-native users |
| Bare git repo | Manual bare repo | Medium | Manual | Maximum control |

**Decision rationale:** The user has one primary machine (Dionysus) with a potential Mac (Apollo) as secondary. chezmoi's power — templates, secret management, cross-OS adaptation — is overkill for this use case. GNU Stow is dead simple: files live in `~/dotfiles/`, symlinks point from `~/` into it. No new mental model needed. If the Mac needs different configs later, Stow can handle that with separate package directories.

yadm is a reasonable alternative but adds git-wrapping complexity for no real benefit — Stow + a regular git repo gives the same result with more transparency.

**Confidence:** HIGH — Stow is widely documented, actively maintained, and the standard recommendation for single-machine or low-machine-count setups.

### Files to Track

**Must track (core dotfiles):**

| File | Purpose | Notes |
|------|---------|-------|
| `.bashrc` | Shell config (187 lines) | Has stale aliases pointing to dead paths |
| `.profile` | Login shell PATH setup | Standard Ubuntu boilerplate |
| `.gitconfig` | Git identity, credential config | Currently has plaintext `store` helper |
| `.tmux.conf` | Session persistence config | Already well-configured |
| `.ssh/config` | Host aliases, multiplexing | Does not exist yet — must create |

**Should track (tool configs):**

| File | Purpose | Notes |
|------|---------|-------|
| `.claude/CLAUDE.md` | Claude Code global instructions | Already maintained |
| `.codex/config.toml` | Codex CLI config | Small, important |
| `.codex/instructions.md` | Codex CLI instructions | Small, important |

**Do NOT track:**

| Item | Why |
|------|-----|
| `.env` | Secrets — never version control |
| `.ssh/id_ed25519*` | Private keys — never version control |
| `.git-credentials` | Plaintext tokens — will be removed entirely |
| `.claude.json` | MCP server paths are machine-specific |
| `miniconda3/` | Too large, managed by conda itself |
| `.cache/` | Ephemeral, auto-rebuilds |

### Migration Path

```bash
# 1. Install stow
sudo apt install stow

# 2. Create dotfiles directory
mkdir -p ~/dotfiles

# 3. Move files into stow packages
# Package: shell
mkdir -p ~/dotfiles/shell
mv ~/.bashrc ~/dotfiles/shell/.bashrc
mv ~/.profile ~/dotfiles/shell/.profile

# Package: git
mkdir -p ~/dotfiles/git
mv ~/.gitconfig ~/dotfiles/git/.gitconfig

# Package: tmux
mkdir -p ~/dotfiles/tmux
mv ~/.tmux.conf ~/dotfiles/tmux/.tmux.conf

# Package: ssh (config only, not keys)
mkdir -p ~/dotfiles/ssh/.ssh
# Create the config file (doesn't exist yet)
touch ~/dotfiles/ssh/.ssh/config

# Package: claude
mkdir -p ~/dotfiles/claude/.claude
cp ~/.claude/CLAUDE.md ~/dotfiles/claude/.claude/CLAUDE.md

# 4. Stow everything
cd ~/dotfiles
stow shell git tmux ssh claude

# 5. Initialize git
cd ~/dotfiles
git init
git add -A
git commit -m "Initial dotfiles"

# 6. Push to GitHub (private repo)
gh repo create dotfiles --private --source=. --push
```

### .bashrc Cleanup Needed Before Tracking

The current `.bashrc` has issues that should be fixed before committing:

1. **Duplicate alias blocks** — Lines defining `phil-dev`, `phil-analysis`, etc. appear twice (exact duplicates)
2. **Dead path references** — `~/github/personal/philosophy-research-tools` does not exist, `~/workflows/analysis` does not exist, `~/workflows/university` does not exist
3. **Redundant PATH entries** — `~/.local/bin` appears twice, CUDA paths appear twice
4. **Stale `remote-services` reference** — `/home/rookslog/remote-services` path may not exist
5. **SSH agent block** — Good, but should be moved to `.profile` (login shell, runs once) rather than `.bashrc` (every subshell)

### Sources

- [GNU Stow dotfiles tutorial (2025)](https://www.penkin.me/development/tools/productivity/configuration/2025/10/20/my-dotfiles-setup-with-gnu-stow.html)
- [chezmoi comparison table](https://www.chezmoi.io/comparison-table/)
- [Dotfile management community discussion](https://biggo.com/news/202412191324_dotfile-management-tools-comparison)

---

## 2. Node.js Upgrade Path

### Recommendation: Node.js 22 LTS via NodeSource

**Current state:** Node.js 18.19.1 installed from Ubuntu apt (`nodejs/noble`), npm 9.2.0. Both severely outdated. Node 18 reached EOL April 2025.

**Target:** Node.js 22.x LTS (Active LTS through October 2025, Maintenance LTS through April 2027).

**Why v22 over v20:** Node 20 is already in Maintenance LTS (security fixes only). Node 22 is the current Active LTS — it gets bug fixes, performance improvements, and will be supported years longer. 30% faster startup than Node 20.

**Why NodeSource over nvm:** The user has a single-purpose server, not a development machine juggling multiple Node versions. nvm adds shell startup overhead, PATH complexity, and per-shell activation. NodeSource provides a clean system-wide install that replaces the outdated Ubuntu package. The only global npm package is `@openai/codex@0.106.0` — minimal reinstallation needed.

**Why not system apt:** Ubuntu 24.04 ships Node 18, which is EOL. The distro package will never upgrade to 22.

**Confidence:** HIGH — NodeSource is the official recommended installation method from Node.js documentation.

### Upgrade Steps

```bash
# 1. Record current global packages
npm list -g --depth=0 > /tmp/npm-globals.txt

# 2. Remove system nodejs
sudo apt remove nodejs nodejs-doc npm
sudo apt autoremove

# 3. Install NodeSource repo for Node 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install nodejs

# 4. Verify
node -v   # Should show v22.x.x
npm -v    # Should show 10.x.x

# 5. Reinstall global packages
npm install -g @openai/codex

# 6. Test existing projects
cd ~/workspace/projects/zlibrary-mcp && npm test
```

### Risk: Existing Projects

- **zlibrary-mcp (TypeScript):** Node 22 is fully compatible with TypeScript toolchains. No breaking changes expected from 18 to 22 for typical TypeScript projects.
- **MCP servers:** These run via Node — verify after upgrade by testing each MCP server connection from Claude Code.
- **Codex CLI:** `@openai/codex` should work on Node 22. Check release notes if issues arise.

### .npm-global Directory

The current `.bashrc` adds `$HOME/.npm-global/bin` to PATH. After NodeSource install, npm global packages go to `/usr/lib/node_modules` by default. Either:
- Keep the npm-global prefix: `npm config set prefix '~/.npm-global'` (recommended for non-root installs)
- Or switch to system-wide and remove the PATH entry

Recommendation: Keep `~/.npm-global` prefix. It avoids needing sudo for global installs.

### Sources

- [Node.js release schedule](https://endoflife.date/nodejs)
- [NodeSource installation guide](https://nodesource.com/blog/Update-Node.js-versions-on-linux)
- [Node.js 22 LTS announcement](https://nodesource.com/blog/Node.js-v22-Long-Term-Support-LTS)

---

## 3. Python Environment Strategy

### Recommendation: Conda for GPU/ML + uv for Everything Else. Eliminate pip.

**Current state:**

| Tool | Size | Purpose | Overlap |
|------|------|---------|---------|
| conda (miniconda3) | 48GB (5 envs) | ML, GPU packages | Also installing pure-Python packages |
| uv cache | 25GB | Fast package management | Overlaps with pip for same packages |
| pip cache | 5.5GB | Legacy package installs | Fully redundant with uv |

**Strategy:**

1. **Keep conda for exactly 2 environments:** `ml-dev` (12GB, GPU/CUDA packages) and `audio` (7.9GB, likely whisper/ffmpeg). These need binary packages that only conda provides well (CUDA libs, ffmpeg, etc.).

2. **Use uv for all new Python projects.** uv replaces pip, pip-tools, virtualenv, pipx, and pyenv. It is 10-100x faster and manages lockfiles. All new projects in `~/workspace/projects/` should use `uv init` and `uv sync`.

3. **Retire these conda environments:**
   - `acadlib-dev` (971MB) — acadlib is archived to `/data/archive/`. Delete the env.
   - `analysis` (8.3GB) — Check if anything uses it. The `.bashrc` alias `phil-analysis` points to a dead path (`~/workflows/analysis`). Likely orphaned.
   - `university` (7.9GB) — The `.bashrc` alias `phil-university` points to a dead path (`~/workflows/university`). Likely orphaned.

4. **Never use pip directly again.** uv is a drop-in replacement: `uv pip install` works in any environment including conda. The pip cache can be fully cleared.

**Confidence:** HIGH — uv has become the de facto standard for Python package management in 2025-2026. The conda-for-GPU + uv-for-everything-else pattern is widely recommended.

### Cleanup Steps

```bash
# 1. Remove orphaned conda environments
conda env remove -n acadlib-dev   # 971MB
conda env remove -n analysis      # 8.3GB (verify nothing uses it first)
conda env remove -n university    # 7.9GB (verify nothing uses it first)

# 2. Clean conda package cache
conda clean --all --yes           # Removes tarballs and unused packages

# 3. Clear pip cache entirely
pip cache purge                   # 5.5GB gone

# 4. Prune uv cache
uv cache prune                   # Removes unreferenced entries

# Expected savings: ~17GB from conda envs + 5.5GB pip + some uv pruning = ~23GB+
```

### Verification Before Deletion

Before removing `analysis` and `university` envs, check if any active project references them:

```bash
# Check which projects have conda env references
grep -r "analysis\|university" ~/workspace/projects/*/pyproject.toml ~/workspace/projects/*/.python-version 2>/dev/null
grep -r "conda activate analysis\|conda activate university" ~/workspace/projects/ 2>/dev/null | grep -v .git
```

If nothing references them, they are safe to remove.

### Per-Project Strategy Going Forward

| Project Type | Tool | Example |
|-------------|------|---------|
| GPU/ML workloads | conda env + uv pip | scholardoc OCR, whisper |
| Pure Python tools | uv venv + uv pip | zlibrary-mcp, philo-rag |
| Quick scripts | `uv run script.py` | One-off analysis scripts |
| CLI tools to install | `uv tool install` | Replaces pipx |

### Sources

- [uv documentation — caching](https://docs.astral.sh/uv/concepts/cache/)
- [conda + uv hybrid workflow](https://medium.com/@datagumshoe/using-uv-and-conda-together-effectively-a-fast-flexible-workflow-d046aff622f0)
- [Python package managers 2026 comparison](https://scopir.com/posts/best-python-package-managers-2026/)

---

## 4. VS Code Extension Cleanup

### Current State (Updated)

The earlier audit mentioned 94 extensions and 30+ Claude Code versions. Current state shows only **15 extensions** and **1 Claude Code version** — the previous cleanup session may have already addressed this, or VS Code has cleaned up old versions.

Current extensions (all appear necessary):
- `anthropic.claude-code` (1 version)
- `charliermarsh.ruff` (Python linter)
- `github.copilot-chat` (may not be needed — user uses Claude Code)
- `github.vscode-github-actions`
- `ms-python.*` (Python tooling — 4 extensions)
- `ms-vscode.c*` (C++ tooling — 4 extensions, needed for semantic-calibre)
- `ms-azuretools.vscode-containers` (Docker)

### Recommendation

1. **Remove `github.copilot-chat`** if not actively used. The user uses Claude Code as the primary AI assistant. Having Copilot installed alongside Claude Code creates ambiguity and the `.copilot/` directory consumes space.

2. **The old extension problem appears resolved.** No further action needed on bulk cleanup.

### Cleanup Commands

```bash
# Remove Copilot if not needed
code --uninstall-extension github.copilot-chat

# Remove stale Copilot dotdir
rm -rf ~/.copilot/

# List current extensions to verify
code --list-extensions
```

### VS Code Server Cache

The `.vscode-server/` directory is 2.8GB total (989MB extensions). This is reasonable for a remote development setup. The bulk is likely the VS Code Server binary and cached node modules. No aggressive cleanup recommended — it will regenerate.

**Confidence:** HIGH — direct filesystem inspection confirms current state.

---

## 5. Security Hardening

### 5.1 VNC: CRITICAL — Bind to Localhost

**Current state:** x11vnc running as root with `-nopw -noshm` on `0.0.0.0:5900`. This means:
- No password required
- Listening on ALL interfaces (LAN, any network)
- Running as root
- Anyone on the local network can connect and see/control the desktop

**The fix is straightforward:** Bind to localhost only, rely on Tailscale for remote access.

```
# Current (DANGEROUS):
x11vnc -display :1 -auth /run/user/1000/gdm/Xauthority -forever -shared -bg -nopw -noshm

# Fixed:
x11vnc -display :1 -auth /run/user/1000/gdm/Xauthority -forever -shared -bg -noshm \
  -localhost -rfbauth /home/rookslog/.vnc/passwd
```

**Implementation steps:**

```bash
# 1. Set a VNC password
x11vnc -storepasswd /home/rookslog/.vnc/passwd

# 2. Find how VNC is started (systemd unit, rc.local, crontab, etc.)
systemctl list-units | grep -i vnc
cat /etc/systemd/system/*vnc* 2>/dev/null
grep -r x11vnc /etc/systemd/ /etc/init.d/ /etc/rc.local 2>/dev/null

# 3. Update the startup command to add -localhost and -rfbauth
# 4. Restart the service

# 5. Access from Mac via Tailscale:
#    ssh -L 5900:localhost:5900 dionysus
#    Then connect VNC client to localhost:5900
```

**Alternative: Tailscale Serve for VNC.** Tailscale Serve can forward TCP to a local port, making VNC available only within the tailnet without SSH tunneling:

```bash
# Expose VNC on tailnet only (no SSH tunnel needed)
tailscale serve --bg tcp:5900
```

This is cleaner than SSH forwarding but requires Tailscale Serve to be enabled on the tailnet.

**Confidence:** HIGH — the VNC exposure is confirmed via `ps aux` and `ss -tlnp`.

### 5.2 nginx: Remove Entirely

**Current state:** nginx 1.24.0 running on `0.0.0.0:80` with only the `default` site enabled. It serves the default "Welcome to nginx!" page to anyone.

**Recommendation: Remove it.** There is no evidence of any service using nginx as a reverse proxy. PaddleOCR (port 8765) and uvicorn (port 9001) bind directly. If a reverse proxy is needed later, it can be reinstalled with proper configuration.

```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
sudo apt remove nginx nginx-common
sudo apt autoremove
```

If nginx is needed later for reverse-proxying services, reinstall with a proper config that binds to Tailscale IP or localhost only.

**Confidence:** HIGH — only the default site is enabled, no custom configuration exists.

### 5.3 Git Credentials: Remove `store`, Use `gh` Only

**Current state:** `.gitconfig` has both `credential.helper = store` (global, plaintext) and per-host `gh auth git-credential` overrides for github.com. The `.git-credentials` file contains a plaintext HuggingFace token.

**The per-host overrides for github.com already work correctly** — `gh auth git-credential` handles GitHub auth without storing plaintext tokens. The problem is the global `store` fallback and the existing `.git-credentials` file.

**Fix:**

```bash
# 1. Remove the global store helper
git config --global --unset credential.helper

# 2. Verify gh is still configured for GitHub
git config --global --get-regexp credential

# Should show only:
# credential.https://github.com.helper=
# credential.https://github.com.helper=!/usr/bin/gh auth git-credential
# credential.https://gist.github.com.helper=
# credential.https://gist.github.com.helper=!/usr/bin/gh auth git-credential

# 3. Check if anything needs the HuggingFace token
# The .git-credentials file has an HF token — verify if any project
# clones private HF repos. If not, delete the file.

# 4. Delete plaintext credentials file
rm ~/.git-credentials

# 5. If HF auth is needed, use huggingface-cli login instead
# (stores token in ~/.cache/huggingface/token with proper permissions)
huggingface-cli login
```

**Confidence:** HIGH — verified via `.gitconfig` contents and `.git-credentials` file.

### 5.4 Service Binding Audit

**Services currently on 0.0.0.0 (exposed to all interfaces):**

| Service | Port | Bind | Risk | Action |
|---------|------|------|------|--------|
| x11vnc | 5900 | 0.0.0.0 | **CRITICAL** — no password | Bind to localhost, add password |
| nginx | 80 | 0.0.0.0 | **HIGH** — default page | Remove entirely |
| SSH | 22 | 0.0.0.0 | LOW — key-only auth, fail2ban | Acceptable (SSH is already hardened) |
| uvicorn | 9001 | 0.0.0.0 | MEDIUM — annotation tool | Bind to localhost or Tailscale IP |
| PaddleOCR | 8765 | 0.0.0.0 | MEDIUM — Docker service | Bind to localhost in Docker config |

**Services correctly on localhost:**

| Service | Port | Status |
|---------|------|--------|
| PostgreSQL | 5432 | OK — 127.0.0.1 only |
| Redis | 6379 | OK — 127.0.0.1 only |
| VS Code servers | various | OK — 127.0.0.1 only |
| CUPS | 631 | OK — 127.0.0.1 only |

**Fix for uvicorn (port 9001):**

```bash
# Find how it's started
ps aux | grep uvicorn
# Change bind from 0.0.0.0:9001 to 127.0.0.1:9001
# In the start command: --host 127.0.0.1 instead of --host 0.0.0.0
```

**Fix for PaddleOCR Docker (port 8765):**

```bash
# In docker-compose.yml or docker run command, change:
#   -p 8765:8765     (binds to 0.0.0.0)
# To:
#   -p 127.0.0.1:8765:8765   (binds to localhost only)
```

### 5.5 File Permissions Audit

```bash
# Check for world-readable sensitive files
ls -la ~/.env                    # Should be 600
ls -la ~/.git-credentials        # Should not exist after cleanup
ls -la ~/.ssh/id_ed25519         # Should be 600 (currently correct)
ls -la ~/.ssh/id_ed25519_vm      # Should be 600

# Check for group/world-readable SSH dir
ls -la ~/.ssh/                   # Dir should be 700

# Fix if needed
chmod 600 ~/.env
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519*
```

### 5.6 Additional Security Items

**Tor SOCKS proxy on port 9050:** There is a service listening on `127.0.0.1:9050` — this is the Tor SOCKS proxy from the Tor Browser installation. Since it is localhost-only, it is not a network risk, but note that 16GB of Tor Browser in `.local/share/torbrowser/` consumes significant space. If not actively used, consider removing it (see Cache Cleanup section).

**Confidence:** HIGH for all security items — verified via direct system inspection (`ss -tlnp`, `ps aux`, file contents).

### Sources

- [x11vnc security documentation](https://github.com/LibVNC/x11vnc)
- [Tailscale Serve for TCP](https://tailscale.com/kb/1242/tailscale-serve/)
- [gh auth setup-git](https://cli.github.com/manual/gh_auth_setup-git)
- [Tailscale VNC guide](https://lukemillermakes.com/2022/04/20/vpn-remote-desktop-with-tailscale-and-x11vnc/)

---

## 6. Cache Cleanup

### Current .cache/ Breakdown (67GB total)

| Directory | Size | Status | Action |
|-----------|------|--------|--------|
| `huggingface/` | 30GB | Mixed used/unused | Audit and selectively delete |
| `uv/` | 25GB | Working cache | Prune safely |
| `pip/` | 5.5GB | Redundant (switching to uv) | Delete entirely |
| `whisper/` | 4.3GB | Active (audiobookify) | Keep if audiobookify is used |
| `datalab/` | 1.7GB | Unknown | Investigate — likely marker/surya related |
| `thumbnails/` | 531MB | Desktop thumbnails | Safe to delete, auto-rebuilds |
| `zlibrary-mcp/` | 158MB | Active project cache | Keep |
| `vscode-cpptools/` | 156MB | Active (semantic-calibre) | Keep |
| `torbrowser/` | 132MB | Tor Browser cache | Delete if removing Tor Browser |
| `doctr/` | 124MB | OCR models | Keep if scholardoc uses it |
| Everything else | <100MB | Various | Low priority |

### HuggingFace Model Audit (30GB)

**Models actively referenced by projects in ~/workspace/projects/:**

| Model | Size | Used By | Keep? |
|-------|------|---------|-------|
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 458MB | semantic-calibre | YES |
| `sentence-transformers/all-MiniLM-L6-v2` | 88MB | philo-rag-simple | YES |
| `microsoft/trocr-base-printed` | 1.3GB | scholardoc OCR evaluation | YES |
| `docling-project/docling-models` | 342MB | scholardoc | YES |
| `docling-project/docling-layout-heron` | 164MB | scholardoc | YES |
| `Systran/faster-whisper-large-v3` | 2.9GB | audiobookify/transcription | MAYBE |
| `Systran/faster-whisper-medium` | 1.5GB | audiobookify/transcription | MAYBE |

**Models NOT referenced by any active project (candidates for deletion):**

| Model | Size | Notes |
|-------|------|-------|
| `rednote-hilab/dots.ocr` | **5.7GB** | Experimental OCR, no project references |
| `microsoft/phi-2` | **5.2GB** | Language model, no project references |
| `stepfun-ai/GOT-OCR2_0` | 1.4GB | Experimental OCR, no project references |
| `juliozhao/DocLayout-YOLO-DocLayNet-from_scratch` | 154MB | Experimental layout detection |
| `juliozhao/DocLayout-YOLO-DocStructBench` | 39MB | Experimental layout detection |
| `juliozhao/DocLayout-YOLO-DocLayNet-Docsynth300K_pretrained` | 39MB | Experimental layout detection |
| `Mit1208/detr-resnet-50_finetuned_doclaynet` | 318MB | Experimental layout detection |
| `Aryn/deformable-detr-DocLayNet` | 158MB | Experimental layout detection |
| `cmarkea/detr-layout-detection` | 164MB | Experimental layout detection |
| `ds4sd/docling-layout-heron` | 164MB | Duplicate of docling-project version |
| `datalab-to/surya_layout` | 242MB | Experimental layout detection |
| `timm/resnet50.a1_in1k` | 98MB | Backbone model, likely unused alone |
| `bert-base-uncased` | 28KB | Only metadata cached (no model weights) |

**Potential savings from HF cleanup: ~13.5GB** (removing all unreferenced models)

### Cleanup Commands

```bash
# 1. Use huggingface-cli for safe model deletion
pip install -U "huggingface_hub[cli]"   # or: uv pip install "huggingface_hub[cli]"
huggingface-cli scan-cache              # Review what's cached
huggingface-cli delete-cache            # Interactive TUI for selection

# 2. Or delete specific models manually (safe — just cached downloads)
rm -rf ~/.cache/huggingface/hub/models--rednote-hilab--dots.ocr         # 5.7GB
rm -rf ~/.cache/huggingface/hub/models--microsoft--phi-2                # 5.2GB
rm -rf ~/.cache/huggingface/hub/models--stepfun-ai--GOT-OCR2_0         # 1.4GB
rm -rf ~/.cache/huggingface/hub/models--ds4sd--docling-layout-heron     # 164MB (duplicate)
# ... etc for other unreferenced models

# 3. Clear pip cache entirely (switching to uv)
pip cache purge                                                         # 5.5GB

# 4. Prune uv cache
uv cache prune                                                         # Removes unused entries

# 5. Clear desktop thumbnails
rm -rf ~/.cache/thumbnails/                                            # 531MB, auto-rebuilds

# 6. Clear Tor Browser cache (if removing Tor)
rm -rf ~/.cache/torbrowser/                                            # 132MB
```

### Whisper Model Decision

The whisper cache (4.3GB) contains `large-v3.pt` (2.9GB) and `medium.pt` (1.4GB). These are for `audiobookify` which is in "Maintenance" status. If audiobookify is not actively used, these can be deleted and will re-download if needed later. But since /home is at 82%, freeing 4.3GB is meaningful.

**Recommendation:** Keep for now, reassess after higher-impact cleanups.

### Tor Browser (16GB)

Located in `~/.local/share/torbrowser/` (16GB). This is a full Tor Browser installation. If it is not actively used for research, removing it frees significant space:

```bash
rm -rf ~/.local/share/torbrowser/   # 16GB
```

The Tor SOCKS proxy (port 9050) will also stop working. If Tor access is occasionally needed, it can be installed as a lighter-weight `tor` package without the full browser.

### Total Potential Space Recovery

| Action | Savings |
|--------|---------|
| Unreferenced HuggingFace models | ~13.5GB |
| pip cache purge | 5.5GB |
| Tor Browser removal | 16GB |
| Orphaned conda envs (acadlib-dev, analysis, university) | ~17GB |
| Desktop thumbnails | 0.5GB |
| uv cache prune | Unknown (likely 1-5GB) |
| **Total** | **~53GB+** |

This would take /home from 82% to roughly 65% — a healthy margin.

**Confidence:** HIGH — all sizes verified via direct `du -sh` inspection, model usage verified by grep across project source code.

---

## 7. Broken Kernel Fix

### Current State

The broken HWE kernel packages (6.17.0-14) have packages in three problematic states:
- `iU` (unpacked, not configured): `linux-generic-hwe-24.04`, `linux-headers-generic-hwe-24.04`
- `iF` (half-installed, failed): `linux-headers-6.17.0-14-generic`, `linux-image-6.17.0-14-generic`
- `ii` (properly installed): Several supporting packages

The system is currently running kernel `6.14.0-36-generic`, which is fine. The broken packages are not in use — they are a failed upgrade attempt.

### Fix Steps (Requires sudo — Use Codex CLI)

```bash
# Step 1: Force-remove the broken packages
sudo dpkg --remove --force-remove-reinstreq \
  linux-headers-6.17.0-14-generic \
  linux-image-6.17.0-14-generic

# Step 2: Fix broken dependencies
sudo apt --fix-broken install

# Step 3: Clean up remaining HWE packages if desired
sudo apt remove \
  linux-generic-hwe-24.04 \
  linux-headers-generic-hwe-24.04 \
  linux-image-generic-hwe-24.04 \
  linux-hwe-6.17-headers-6.17.0-14 \
  linux-hwe-6.17-tools-6.17.0-14 \
  linux-modules-6.17.0-14-generic \
  linux-modules-extra-6.17.0-14-generic \
  linux-tools-6.17.0-14-generic

# Step 4: Autoremove orphaned dependencies
sudo apt autoremove

# Step 5: Verify
dpkg -l | grep -i "6.17"    # Should show nothing
apt list --upgradable        # Should be clean
```

### Risk Assessment

- **LOW risk** — the system is running 6.14.0, not 6.17.0. The broken packages are not in use.
- The HWE kernel is for "Hardware Enablement" on LTS. Since the system works fine on 6.14.0, HWE is not needed.
- If HWE is wanted later, it can be reinstalled cleanly after the broken state is resolved.

### DKMS / NVIDIA Warning

After kernel package changes, verify that NVIDIA drivers are still functional:

```bash
nvidia-smi    # Should show GPU info without errors
```

If NVIDIA breaks, reinstall the driver module for the current kernel. But since we are not changing the running kernel (6.14.0), this should not be affected.

**Confidence:** HIGH — standard dpkg recovery procedure, verified package states via `dpkg -l`.

### Sources

- [Ubuntu broken package fix guide](https://oneuptime.com/blog/post/2026-01-15-fix-broken-packages-ubuntu/view)
- [dpkg force-remove-reinstreq documentation](https://discourse.ubuntu.com/t/how-to-fix-broken-packages/63132)

---

## 8. Roadmap Implications

### Suggested Phase Ordering for This Milestone

**Phase 1: Security Hardening (URGENT)**
Do this first because the VNC exposure is an active security risk.

Tasks:
1. Fix VNC binding (localhost + password)
2. Remove nginx
3. Fix git credential store (remove plaintext tokens)
4. Bind uvicorn and PaddleOCR to localhost
5. File permissions audit

**Phase 2: Broken State Fixes**
Remove blocking issues before building new things.

Tasks:
1. Fix broken HWE kernel packages
2. Clean `.bashrc` (remove dead aliases, duplicates, fix paths)
3. Remove stale dotdirs (`.acadlib/`, `.gphoto/`, `.philosophy_tools/`, `.streamlit/`, `.copilot/`)

**Phase 3: Space Recovery**
Reclaim disk space to create room for development work.

Tasks:
1. Remove unreferenced HuggingFace models (~13.5GB)
2. Remove orphaned conda environments (~17GB)
3. Purge pip cache (5.5GB)
4. Prune uv cache
5. Remove Tor Browser if not needed (16GB)
6. Clear thumbnails and other minor caches

**Phase 4: Development Environment Upgrade**
Modernize the toolchain.

Tasks:
1. Upgrade Node.js 18 to 22 LTS via NodeSource
2. Verify all MCP servers and projects work with Node 22
3. Establish uv as primary Python package manager
4. Document conda-only and uv-only project patterns

**Phase 5: Dotfiles Management**
Track and version-control configurations.

Tasks:
1. Install GNU Stow
2. Create `~/dotfiles/` with packages for shell, git, tmux, ssh, claude
3. Clean `.bashrc` content before tracking
4. Create `~/.ssh/config` with host aliases
5. Initialize git repo and push to GitHub (private)

### Phase Ordering Rationale

- **Security before everything** — the VNC exposure is a real attack surface
- **Broken state before building** — fix kernel and clean dead paths before adding dotfiles management
- **Space recovery before upgrades** — NodeSource install and new packages need room
- **Upgrades before dotfiles** — get the environment stable, THEN capture it in version control
- **Dotfiles last** — capture the clean, working state, not the messy current state

### Research Flags

- Phase 3 (Space Recovery): The HuggingFace model audit should be reviewed by the user — some "unreferenced" models may be used in notebooks or scripts not checked into git.
- Phase 4 (Node.js upgrade): Low risk but test MCP servers carefully. If any break, the fix is typically updating `node_modules` (`npm install`).
- Phase 5 (Dotfiles): Creating `~/.ssh/config` needs its own sub-research for proper Tailscale host aliases, multiplexing configuration, and keepalive settings. This is covered in the multi-device research file.

---

## Confidence Assessment

| Area | Confidence | Reason |
|------|------------|--------|
| Dotfiles (Stow) | HIGH | Well-documented, standard approach, verified no tools installed yet |
| Node.js upgrade | HIGH | Clear EOL timeline, NodeSource is official, current install from apt confirmed |
| Python strategy | HIGH | uv ecosystem well-established, conda env sizes and usage verified |
| VS Code cleanup | HIGH | Direct filesystem inspection shows problem largely resolved |
| Security hardening | HIGH | All vulnerabilities confirmed via ss/ps/file inspection |
| Cache cleanup | HIGH | All sizes measured, model usage traced via grep |
| Kernel fix | HIGH | Standard dpkg recovery, package states verified |

## Gaps to Address

- **SSH config creation** — Needs sub-research on Tailscale host naming, ProxyJump patterns, ControlMaster settings. Covered partially in multi-device research.
- **Docker data-root migration** — Not covered here (mentioned in PROJECT.md). Needs separate research on `/data/docker/` migration procedure.
- **Conda env usage verification** — `analysis` and `university` envs assumed orphaned based on dead `.bashrc` aliases. User should verify before deletion.
- **Whisper model decision** — Depends on whether audiobookify is still actively used. User decision.
