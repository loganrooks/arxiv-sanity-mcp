# Multi-Device Integration & Session Persistence Research

**Domain:** Personal scholarly research platform (3-device mesh)
**Researched:** 2026-02-28
**Overall confidence:** HIGH

---

## 1. SSH Config for Tailscale Mesh

### Current State

- No `~/.ssh/config` exists despite remote-first workflow
- `~/.ssh/controlmasters/` directory exists (empty) -- someone started this but never finished
- Tailscale MagicDNS is enabled and working: `apollo` resolves to `100.64.240.77`, `orpheus` to `100.107.206.108`
- Tailscale suffix: `tail0528f0.ts.net`
- Traditional SSH (not Tailscale SSH) is in use -- standard sshd on port 22, key-based auth
- SSH agent has no loaded keys on login

### Recommendation: Traditional SSH over Tailscale (not Tailscale SSH)

**Use traditional SSH keys + Tailscale as the network layer.** Do not enable Tailscale SSH (`--ssh` mode). Rationale:

1. Tailscale SSH is designed for multi-user organizations managing fleet access via ACLs. For a single user across 3 personal devices, it adds complexity without benefit.
2. Traditional SSH gives full control over `~/.ssh/config`, agent forwarding, and ControlMaster -- all of which matter for this workflow.
3. The ControlMaster incompatibility with Tailscale SSH was fixed (issue #4920, June 2022), but avoiding the feature entirely means zero risk of edge cases.

### Recommended ~/.ssh/config (for Apollo -- the Mac)

This is the primary config that matters, since Apollo initiates most connections. Dionysus and Orpheus are destinations.

```ssh-config
# === Global Defaults ===
Host *
    # Keep connections alive through NAT/firewall
    ServerAliveInterval 30
    ServerAliveCountMax 3
    # Multiplex connections -- faster subsequent sessions
    ControlMaster auto
    ControlPath ~/.ssh/controlmasters/%C
    ControlPersist 10m
    # Security defaults
    IdentitiesOnly yes
    AddKeysToAgent yes
    # macOS keychain integration
    UseKeychain yes

# === Dionysus (Linux Server) ===
Host dionysus
    HostName dionysus
    User rookslog
    IdentityFile ~/.ssh/id_ed25519
    # Forward agent for git operations on server
    ForwardAgent yes
    # Increase for VS Code Remote SSH stability
    ServerAliveInterval 15

# === Dionysus via IP (fallback if MagicDNS fails) ===
Host dionysus-ip
    HostName 100.93.212.44
    User rookslog
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
    ServerAliveInterval 15

# === Orpheus (iPhone -- rarely a destination) ===
Host orpheus
    HostName orpheus
    User mobile
    IdentityFile ~/.ssh/id_ed25519
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `ControlPath %C` (hash) | Avoids path-length issues (108 char limit). `%C` = SHA1 of `%l%h%p%r`. |
| `ControlPersist 10m` | Keeps master socket alive 10 minutes after last session closes. Long enough for rapid reconnects, short enough to not leak. |
| `ServerAliveInterval 15` for Dionysus | VS Code Remote SSH benefits from aggressive keepalives. Tailscale connections are stable but the SSH layer can still timeout. |
| `ForwardAgent yes` only for Dionysus | Enables `git push` from server using Mac's SSH keys (for GitHub). Never forward agent to untrusted hosts. |
| `AddKeysToAgent yes` + `UseKeychain yes` | macOS-specific: loads keys into agent on first use, persists passphrase in Keychain across reboots. |
| `IdentitiesOnly yes` | Prevents SSH from trying every key in the agent -- sends only the specified IdentityFile. |
| MagicDNS hostnames | `dionysus` resolves via Tailscale MagicDNS. No need for IP addresses in normal operation. |

### SSH Config for Dionysus (the server)

Dionysus rarely initiates SSH, but should have config for completeness:

```ssh-config
Host *
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/controlmasters/%C
    ControlPersist 10m
    IdentitiesOnly yes
    AddKeysToAgent yes

Host apollo
    HostName apollo
    User logan
    IdentityFile ~/.ssh/id_ed25519
```

### SSH Agent Auto-Load

On Dionysus, add to `~/.bashrc` (or a file sourced by it):

```bash
# Auto-load SSH keys if agent is running but empty
if [ -z "$SSH_AUTH_SOCK" ]; then
    eval "$(ssh-agent -s)" > /dev/null
fi
if ! ssh-add -l &>/dev/null; then
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi
```

On Apollo, macOS handles this via `UseKeychain yes` + `AddKeysToAgent yes`.

### Confidence: HIGH
Sources: OpenSSH man pages, Tailscale official docs, verified MagicDNS resolution on this machine.

---

## 2. tmux Session Management

### Current State

- tmux 3.4 installed
- `.tmux.conf` exists with good basics: prefix remapped to `C-a`, mouse on, named session keybindings (`M-d` for dev, `M-u` for university, etc.)
- No plugin manager (TPM) installed
- No session persistence plugins (resurrect/continuum)
- No standard session layout defined

### Recommendation: Named Sessions + TPM + Resurrect/Continuum

The goal is: close laptop, SSH from phone, `tmux attach -t dev`, resume exactly where you were.

### Session Strategy

Use 3-4 named sessions with defined purposes:

| Session | Purpose | Typical Windows |
|---------|---------|-----------------|
| `dev` | Active project development | editor, shell, test runner, logs |
| `uni` | University/academic work | writing, reading notes, course materials |
| `sys` | System administration | htop, logs, docker, service management |
| `bg` | Background/long-running jobs | training, processing, builds |

**Do not** create sessions eagerly. Start `dev` always. Start others on demand. The keybindings in the existing `.tmux.conf` (prefix + `M-d`, `M-u`, etc.) already support this.

### Plugin Setup

Install TPM (Tmux Plugin Manager) and two essential plugins:

```bash
# Install TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Add to `.tmux.conf`:

```tmux
# Plugin Manager
set -g @plugin 'tmux-plugins/tpm'

# Session persistence across restarts
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'

# Resurrect config
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-strategy-nvim 'session'

# Continuum config -- auto-save every 15 min, auto-restore on tmux start
set -g @continuum-save-interval '15'
set -g @continuum-restore 'on'

# Initialize TPM (must be last line)
run '~/.tmux/plugins/tpm/tpm'
```

Then press `prefix + I` inside tmux to install plugins.

### What Resurrect Saves

- All sessions, windows, panes, and their order
- Current working directory per pane
- Pane layouts (including zoom state)
- Active/focused window and pane
- Running programs: vi, vim, nvim, man, less, more, tail, top, htop (default list)

### What Resurrect Does NOT Save

- Shell history per pane
- Scrollback buffer contents (unless `capture-pane-contents` is on)
- Environment variables
- Unsaved editor buffers

### Workflow: Device Switching

**Close laptop (Apollo):**
1. SSH connection drops
2. tmux sessions persist on Dionysus (they always do -- this is tmux's core feature)
3. Continuum auto-saves session state every 15 minutes

**Resume from phone (Orpheus):**
1. `ssh dionysus` (using Blink Shell or similar)
2. `tmux attach -t dev` or just `tmux a` to attach most recent

**Resume from laptop (Apollo):**
1. `ssh dionysus`
2. `tmux attach -t dev`

**After server reboot:**
1. Continuum auto-restores last saved state when tmux starts
2. `tmux attach -t dev` picks up where you left off (minus running processes)

### Auto-Start tmux on SSH Login

Add to `~/.bashrc` on Dionysus (at the end):

```bash
# Auto-attach to tmux on SSH login (not for local terminals or nested sessions)
if [ -n "$SSH_CONNECTION" ] && [ -z "$TMUX" ] && command -v tmux &>/dev/null; then
    # Attach to 'dev' session if it exists, otherwise create it
    tmux new-session -A -s dev
fi
```

The `-A` flag means: attach if exists, create if not. This ensures every SSH login drops you into tmux automatically.

### Phone-Specific Considerations

- **Blink Shell** (iOS): Best SSH/Mosh client for iPhone. Supports tmux natively, handles disconnects gracefully. ~$15 one-time purchase. Worth it for serious mobile SSH.
- **Prompt 3** (iOS): Alternative SSH client, good but Blink is better for tmux workflows.
- **Mosh** (optional): If Tailscale connections are unreliable on cellular, Mosh handles roaming/disconnects better than SSH. Install on Dionysus with `sudo apt install mosh`. But Tailscale already handles roaming well, so Mosh is likely unnecessary.

### Confidence: HIGH
tmux session persistence is well-established. Resurrect/Continuum are the standard plugins (2k+ GitHub stars each, actively maintained). The auto-attach pattern is widely used.

---

## 3. SyncThing Optimization

### Current State

SyncThing v1.27.2 running on Dionysus with 8 folders configured:

| Folder | Path | Devices | Status |
|--------|------|---------|--------|
| academic-active | ~/workspace/university/courses/2025-fall | APOLLO, DIONYSUS, LE2127 | Active |
| academic-notes | ~/workspace/university/notes | APOLLO, DIONYSUS, LE2127 | Active |
| academic-processing | /scratch/lecture-processing/incoming | APOLLO, DIONYSUS, LE2127 | Active |
| writings | ~/workspace/writings | APOLLO, DIONYSUS | Active |
| reading-groups | ~/workspace/university/reading-groups | APOLLO, DIONYSUS | Active |
| courses | ~/workspace/university/courses | APOLLO, DIONYSUS | Active |
| philosophy-film-club | ~/philosophy-film-club | APOLLO, DIONYSUS | Active |
| dropbox | /data/dropbox | APOLLO, DIONYSUS, LE2127 | **Paused** |
| default (Sync) | ~/Sync | DIONYSUS only | Unused |

**Issues identified:**
- `academic-active` (2025-fall subfolder) is nested inside `courses` -- potential double-sync
- `default` Sync folder is unused cruft
- `dropbox` is paused
- SyncThing GUI bound to `0.0.0.0:8384` -- security concern (should be Tailscale IP only)
- `cleanoutDays` set to `NaN` on some folders -- likely a bug
- Apollo and LE2127 peers currently disconnected

### Recommendations for Development Artifacts

**Do NOT sync development project directories via SyncThing.** Development repos contain:
- `node_modules/` (hundreds of MB)
- `.git/` directories (conflict-prone)
- Build artifacts, caches, virtual environments
- Lock files that conflict across platforms

The right tool for syncing code is **git**. All projects are already in git repos.

**What SHOULD be synced via SyncThing:**
- Documents/writings (already synced)
- Notes/academic materials (already synced)
- Obsidian vault (see section 5)
- An "inbox" folder for phone recordings (see section 4)
- Configuration snippets or reference materials

### .stignore Patterns

Every SyncThing folder should have a `.stignore` file. Recommended baseline:

```
// OS cruft
(?d).DS_Store
(?d)._*
(?d).Spotlight-V100
(?d).Trashes
(?d)Thumbs.db
(?d)desktop.ini

// Editor/IDE
.vscode/
.idea/
*.swp
*.swo
*~

// SyncThing internals
.stversions
.stfolder

// Development (if any code is ever in a synced folder)
node_modules/
__pycache__/
*.pyc
.git/
.env
venv/
.venv/
```

The `(?d)` prefix means "delete this file if it's blocking directory removal" -- appropriate for OS-generated junk.

### Cleanup Actions

1. **Remove the `default` Sync folder** -- it's unused
2. **Evaluate `academic-active` vs `courses` overlap** -- likely remove `academic-active` since `courses` already covers it, or restructure
3. **Fix SyncThing GUI binding** -- change from `0.0.0.0:8384` to `100.93.212.44:8384` (Tailscale IP) or `127.0.0.1:8384` + SSH tunnel
4. **Fix `cleanoutDays: NaN`** -- set to a valid number (e.g., 30)

### Confidence: HIGH
SyncThing behavior is well-documented and verified against the actual config on this machine.

---

## 4. Phone-to-Server Pipeline (Audio Recording)

### The Goal

Record audio on iPhone (lecture recordings, voice notes, reading reflections) and have it automatically appear on Dionysus for processing (transcription, etc.).

### Option Analysis

| Approach | Friction | Reliability | Background? | Cost |
|----------|----------|-------------|-------------|------|
| Mobius Sync (SyncThing iOS) | Medium | LOW | No (iOS limitation) | ~$5 one-time |
| Apple Shortcuts + SSH upload | High | LOW | No (requires tap to confirm) | Free |
| SyncThing on Apollo as relay | Low | HIGH | Yes (Mac runs SyncThing) | Free |
| Manual SCP/rsync from phone | High | HIGH | No | Free |
| iCloud Drive folder → Mac → SyncThing | Low | HIGH | Yes | Free (5GB iCloud) |

### Recommendation: iCloud Drive relay through Apollo

**The most frictionless path that actually works:**

1. **On iPhone:** Save audio recordings to an iCloud Drive folder (e.g., `iCloud Drive/inbox/`)
2. **On Apollo (Mac):** iCloud Drive syncs automatically. A SyncThing folder watches `~/Library/Mobile Documents/com~apple~CloudDocs/inbox/` (or a symlinked path)
3. **On Dionysus:** SyncThing receives the files into `/scratch/inbox/` or similar
4. **On Dionysus:** A file-watch service (inotifywait or similar) detects new files and triggers processing

**Why this beats the alternatives:**

- **Mobius Sync** cannot run in the background on iOS. It only syncs while the app is open. For audio recordings made in class, you'd have to remember to open Mobius Sync afterward. This defeats the purpose.
- **Apple Shortcuts SSH** requires tapping a confirmation alert on the lock screen. It cannot run truly unattended. It also has documented "Channel allocation error" issues over Tailscale.
- **The iCloud relay** is invisible: save file on phone, iCloud syncs to Mac automatically (even when Mac is sleeping with Power Nap), SyncThing picks it up from Mac and sends to Dionysus.

**Requirement:** Apollo must be running (lid open or Power Nap enabled) for this relay to work. If Apollo is offline for days, files queue in iCloud and sync when it comes back online.

### Alternative: Direct SyncThing with Mobius Sync

If the relay through Apollo is unacceptable (e.g., Mac is often off), Mobius Sync is the fallback. It works, but requires discipline:

1. Install Mobius Sync on iPhone (~$5 one-time)
2. Configure a send-only folder pointing at the recordings directory
3. Remember to open Mobius Sync after recording to trigger sync
4. Syncs directly to Dionysus over Tailscale

This is acceptable for "batch sync when I get home" but not for immediate/automatic processing.

### Server-Side Processing Setup

On Dionysus, use `inotifywait` (from `inotify-tools`) to watch the inbox:

```bash
# Simple watcher script (systemd service or tmux background)
inotifywait -m -e close_write /scratch/inbox/ |
while read dir event file; do
    # Route by file type
    case "$file" in
        *.m4a|*.mp3|*.wav)
            # Queue for transcription
            mv "/scratch/inbox/$file" /scratch/transcription-queue/
            ;;
        *.md|*.txt)
            # Move to notes processing
            mv "/scratch/inbox/$file" ~/workspace/writings/inbox/
            ;;
    esac
done
```

### Confidence: MEDIUM
The iCloud relay approach is well-established (many Obsidian users do this). Mobius Sync limitations are documented on their FAQ. The Apple Shortcuts SSH issues are documented in Tailscale's GitHub issues. However, the specific end-to-end pipeline has not been tested -- the individual components are reliable but integration needs validation.

---

## 5. Obsidian Integration

### The Decision: Obsidian Sync vs SyncThing vs Git

| Method | Cost | Conflict Resolution | iOS Support | Offline | Complexity |
|--------|------|---------------------|-------------|---------|------------|
| **Obsidian Sync** | $4/mo ($48/yr) | Excellent (diff-match-patch) | Native | Full | None |
| **SyncThing** | Free | File-level only (conflicts common) | Via Mobius Sync (flaky) | Full | Medium |
| **Git** | Free | Manual merge | Via Working Copy app | Full | High |
| **Remotely Save + WebDAV** | Free | Smart conflict handling | Native plugin | Full | Medium |
| **iCloud Drive** | Free | Poor (silent overwrites) | Native | Full | None |

### Recommendation: Obsidian Sync (if budget allows) or SyncThing relay

**First choice: Obsidian Sync at $4/month.** For a PhD student whose entire workflow revolves around notes, $48/year is trivially justified. It provides:

- Content-level conflict resolution (not just file-level) -- critical when editing the same note from Mac and phone
- Native iOS integration with no background-sync workarounds
- End-to-end encryption
- Version history (1 year on standard plan)
- Zero configuration

**Second choice: SyncThing relay through Apollo.** Same pattern as the audio pipeline:
- Vault lives on Apollo at `~/obsidian-vault/` (or wherever Obsidian stores it)
- SyncThing syncs vault to Dionysus at `~/workspace/notes/obsidian-vault/`
- iPhone accesses vault via iCloud Drive (Obsidian iOS can open iCloud vaults natively)
- This means Mac and phone sync via iCloud, Mac and server sync via SyncThing

The SyncThing approach works but has a known issue: SyncThing operates at the file level, not content level. If you edit the same note on two devices before sync completes, you get `.sync-conflict` files. Obsidian's SyncThing Integration plugin helps resolve these, but it's friction.

**Do NOT use git for vault sync.** Git requires manual commits and pushes. It's wrong for a note-taking tool where you want invisible sync. Git is for code, not thoughts.

### Vault Structure for Academic Work

```
obsidian-vault/
  daily/              # Daily notes (journal, log)
  literature/         # One note per source (book, paper, article)
  concepts/           # Philosophical concepts (one per note)
  projects/           # Research projects, papers in progress
  courses/            # Course-specific notes (can overlap with SyncThing university folder)
  templates/          # Note templates
  inbox/              # Quick capture, unsorted
  attachments/        # Images, PDFs referenced in notes
  .obsidian/          # Obsidian config (themes, plugins, hotkeys)
```

### Essential Plugins for Academic Philosophy

| Plugin | Purpose | Why |
|--------|---------|-----|
| **Zotero Integration** | Import citations, annotations, literature notes | Core of any academic workflow. Pulls highlights and annotations from Zotero PDFs directly into Obsidian. |
| **Dataview** | Query notes as a database | "Show all literature notes tagged #phenomenology published after 2020" -- essential for literature reviews. |
| **Pandoc Plugin** | Export to Word/PDF/LaTeX | Academic writing requires formatted output. Pandoc handles citations via citekeys. |
| **Templater** | Advanced templates | Create literature note templates that auto-fill from Zotero metadata. |
| **Calendar** | Navigate daily notes | Visual calendar for journal/daily note navigation. |
| **Excalidraw** | Visual thinking | Sketch argument structures, concept maps. Philosophy is spatial. |
| **Kanban** | Project tracking | Track paper/chapter progress without leaving Obsidian. |

### Plugins to Avoid

| Plugin | Why Avoid |
|--------|-----------|
| **Obsidian Git** | Adds git overhead to a note-taking tool. Use proper sync instead. |
| **Syncthing Integration** | Only needed if using SyncThing for vault sync (adds conflict resolution UI). Skip if using Obsidian Sync. |
| **Tasks** | Overkill for academic work. Kanban is simpler. |

### Vault Location Strategy

| Device | Location | Sync Method |
|--------|----------|-------------|
| Apollo (Mac) | `~/Documents/obsidian-vault/` | Obsidian Sync (or iCloud + SyncThing) |
| Orpheus (iPhone) | Obsidian app sandbox | Obsidian Sync (or iCloud) |
| Dionysus (server) | `~/workspace/notes/obsidian-vault/` | SyncThing from Apollo (for server-side processing/search) |

**Important:** Dionysus does not run Obsidian. It receives a copy of the vault via SyncThing for processing purposes (e.g., feeding notes into philo-rag-simple, building knowledge graphs with philograph-mcp). The vault on Dionysus should be a **receive-only** SyncThing folder to prevent accidental modification.

### Confidence: HIGH for Obsidian Sync recommendation, MEDIUM for SyncThing relay approach (conflict issues documented).

---

## 6. Offline Capability on Apollo (Mac)

### The Problem

When Apollo is disconnected from Tailscale (airplane, no wifi, coffee shop without internet), the user still needs to:
- Write and edit notes
- Work on papers/documents
- Review readings
- Capture ideas

When reconnected, changes must merge cleanly without data loss.

### What Works Offline by Default

| Activity | Tool | Offline? | Sync on Reconnect? |
|----------|------|----------|---------------------|
| Writing/notes | Obsidian | Yes (local vault) | Yes (Obsidian Sync or iCloud) |
| Writing papers | Any text editor | Yes (local files) | Yes (SyncThing resumes) |
| Reading PDFs | Zotero | Yes (local library) | N/A (Zotero syncs separately) |
| Code editing | VS Code (local) | Yes | Git push when online |
| Git operations | Local commits | Yes (commit, branch) | Push when online |

### What Does NOT Work Offline

| Activity | Why | Mitigation |
|----------|-----|------------|
| SSH to Dionysus | Requires Tailscale | Accept limitation. Use phone hotspot if urgent. |
| VS Code Remote SSH | Requires network | Work on local files instead. |
| Running GPU workloads | Server-only | Queue tasks before disconnecting. |
| Searching philo-rag | Server-side service | Local Obsidian search covers notes. |

### Sync Strategy: SyncThing Handles This

SyncThing is designed for intermittent connectivity. When Apollo reconnects:

1. SyncThing detects peer availability
2. Compares file indexes
3. Transfers changed files bidirectionally
4. If conflict (same file changed on both sides): creates `.sync-conflict` copy

**This is already how SyncThing works.** No special configuration needed for offline support.

### Conflict Prevention Best Practices

The best conflict resolution is conflict prevention:

1. **Partition work by device.** Edit documents on one device at a time. If writing a paper on Apollo, don't also edit it on Dionysus.
2. **Use Obsidian Sync for notes.** Its content-level merge handles simultaneous edits far better than file-level sync.
3. **Commit and push before disconnecting.** For code, `git push` before going offline ensures the server has the latest.
4. **SyncThing versioning is already configured.** Most folders have `simple` versioning with `keep: 5`. If a conflict destroys data, the previous version is in `.stversions/`.

### Offline Writing Workflow

For extended offline periods (flight, retreat):

1. Before disconnecting:
   - Ensure SyncThing is fully synced (check status bar or web UI)
   - `git push` any code changes
   - Note which tmux sessions have important state (they'll persist on Dionysus)
2. While offline:
   - Write in Obsidian (notes) or any editor (papers)
   - Commit code locally as usual
3. On reconnect:
   - SyncThing auto-syncs within seconds of peer discovery
   - `git push` code changes
   - `ssh dionysus` and `tmux attach` to resume server work

### Confidence: HIGH
SyncThing's offline/reconnect behavior is well-established and is the tool's core design principle.

---

## 7. Integration: How It All Fits Together

### Data Flow Architecture

```
ORPHEUS (iPhone)
  |
  | Audio recordings, quick notes
  | via iCloud Drive (automatic)
  v
APOLLO (MacBook M4 Air)
  |
  | iCloud <-> local filesystem
  | SyncThing <-> Dionysus
  | Obsidian Sync <-> all devices
  | SSH/tmux <-> Dionysus
  v
DIONYSUS (Linux Server)
  |
  | SyncThing receives: writings, university, vault, inbox
  | Processes: transcription, OCR, RAG indexing, knowledge graph
  | Serves: philo-rag, MCP servers, PaddleOCR
  | Persists: tmux sessions, long-running jobs
  v
  Results flow back via SyncThing or are accessed via SSH
```

### New SyncThing Folders to Add

| Folder | Path (Dionysus) | Path (Apollo) | Direction | Purpose |
|--------|-----------------|---------------|-----------|---------|
| inbox | /scratch/inbox/ | ~/inbox/ (via iCloud relay) | Apollo -> Dionysus | Phone recordings, quick captures |
| obsidian-vault | ~/workspace/notes/obsidian-vault/ | ~/Documents/obsidian-vault/ | Apollo -> Dionysus (receive-only) | Server-side processing of notes |

### Security Notes

1. **SyncThing GUI** is currently on `0.0.0.0:8384`. Bind to `127.0.0.1:8384` or `100.93.212.44:8384`.
2. **SSH agent forwarding** is safe within Tailscale mesh (all trusted devices) but should not be set globally.
3. **Obsidian Sync** uses E2E encryption by default. Vault contents are not readable by Obsidian's servers.

### Implementation Order

1. **SSH config** (5 min, zero risk, immediate benefit)
2. **tmux plugins** (15 min, zero risk, session persistence)
3. **SyncThing cleanup** (30 min, low risk, remove cruft)
4. **Obsidian vault setup** (1 hour, new tool, start small)
5. **Inbox/audio pipeline** (1-2 hours, requires Apollo-side setup)
6. **File-watch automation** (1 hour, Dionysus-side, can wait)

---

## 8. Tools & Costs Summary

| Tool | Cost | Already Installed? | Purpose |
|------|------|--------------------|---------|
| SSH + config | Free | Yes (needs config) | Remote access |
| tmux + TPM + plugins | Free | Partial (needs TPM) | Session persistence |
| SyncThing | Free | Yes | File sync |
| Obsidian | Free | No | Note-taking |
| Obsidian Sync | $4/mo | No | Cross-device note sync |
| Blink Shell (iOS) | ~$15 one-time | Unknown | SSH from phone |
| Mobius Sync (iOS) | ~$5 one-time | Unknown | SyncThing on phone (optional) |
| inotify-tools | Free | Check | File-watch automation |
| GNU Stow | Free | Check | Dotfiles management |

**Total recurring cost:** $4/month (Obsidian Sync only)
**Total one-time cost:** $0-20 (iOS apps, optional)

---

## Sources

### SSH & Tailscale
- [Tailscale SSH Documentation](https://tailscale.com/docs/features/tailscale-ssh)
- [SSH over Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale)
- [MagicDNS Documentation](https://tailscale.com/docs/features/magicdns)
- [ControlMaster + Tailscale SSH fix (Issue #4920)](https://github.com/tailscale/tailscale/issues/4920) -- resolved June 2022
- [OpenSSH ssh_config man page](https://man.openbsd.org/ssh_config)
- [SSH ControlMaster best practices](https://techbits.cc/controlmaster-ssh-config/)

### tmux
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum)
- [tmux session management for remote work](https://www.techtarget.com/searchsoftwarequality/tip/How-to-use-tmux-sessions-to-manage-remote-connections)

### SyncThing
- [SyncThing .stignore documentation](https://docs.syncthing.net/users/ignoring.html)
- [Comprehensive .stignore patterns](https://github.com/M-Mono/Syncthing-Ignore-Patterns)
- [SyncThing + Obsidian patterns](https://forum.syncthing.net/t/using-syncthing-for-syncing-markdown-files-obsidian/20808)

### Obsidian
- [Obsidian Sync](https://obsidian.md/sync)
- [Obsidian Sync vs SyncThing comparison](https://medium.com/@lennart.dde/a-comparison-of-syncthing-and-obsidian-sync-fd0c2376cc04)
- [Zotero + Obsidian academic workflow](https://medium.com/@alexandraphelan/an-updated-academic-workflow-zotero-obsidian-cffef080addd)
- [Remotely Save plugin](https://github.com/remotely-save/remotely-save)
- [Self-hosted LiveSync](https://github.com/vrtmrz/obsidian-livesync)

### Phone Pipeline
- [Mobius Sync FAQ](https://mobiussync.com/faq/)
- [Apple Shortcuts SSH limitations](https://discussions.apple.com/thread/254603731)
- [Tailscale SSH + Shortcuts channel allocation error](https://github.com/tailscale/tailscale/issues/12485)

### Dotfiles
- [GNU Stow for dotfiles](https://venthur.de/2021-12-19-managing-dotfiles-with-stow.html)
- [Stow dotfiles setup (2025)](https://www.penkin.me/development/tools/productivity/configuration/2025/10/20/my-dotfiles-setup-with-gnu-stow.html)
