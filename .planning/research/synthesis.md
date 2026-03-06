# Agentic AI for the Scholarly Workstation: A Unified Reference (February 2026)

*Synthesis of three research reports on the agentic AI landscape, compiled for the Dionysus platform (Xeon W-2125, 32GB, GTX 1080 Ti) with Apollo (MacBook M4 Air) and Orpheus (iPhone), connected via Tailscale.*

---

## I. What happened this week and why it matters

The week of February 24–28, 2026 saw the densest cluster of AI agent releases in the field's history. The three most consequential for a philosophy researcher running a home server:

**Claude Code Remote Control** (Feb 24–25) lets you run an agentic session on Dionysus and interact from your iPhone or any browser. The session executes entirely on the server — your MCP servers, filesystem, and project configurations stay local. Only conversation flows through Anthropic's API via outbound HTTPS. A GitHub issue (#29479) confirms the exact chain working: MacBook → SSH (Tailscale) → headless Linux → tmux → Claude Code → Remote Control QR code → phone. If the network drops, it auto-reconnects within ~10 minutes.

**Obsidian Headless** (`obsidian-headless` v1.0.0, Feb 27) is an official Node.js CLI client for Obsidian Sync that eliminates the need to run the full Electron app on a server. `ob sync --continuous` creates a persistent sync daemon. This replaces the old Xvfb virtual framebuffer workaround (which consumed ~1–1.5GB RAM) with a lightweight process. On headless Ubuntu, use the `OBSIDIAN_AUTH_TOKEN` env var to bypass the D-Bus keychain issue.

**The MCP ecosystem** was donated to the Linux Foundation's Agentic AI Foundation (co-founded by Anthropic, Block, OpenAI; backed by Google, Microsoft, AWS, Cloudflare). It now has 97 million monthly SDK downloads and 10,000+ active servers with first-class support in Claude, ChatGPT, Cursor, Gemini, and VS Code. This institutional backing makes MCP durable infrastructure, not a single-vendor experiment.

Also this week: Cowork gained scheduled tasks and 21+ enterprise plugins (Feb 25), GitHub Copilot CLI reached GA with multi-model selection (Feb 25), Anthropic acquired Vercept for desktop automation (Feb 25), Perplexity launched its multi-model "Computer" orchestrator (Feb 26), Cursor shipped cloud-VM background agents (Feb 24), and GitHub shipped Enterprise AI Controls GA (Feb 26).

The broader February context: Claude Opus 4.6 launched Feb 5 (1M-token context, agent teams — 16 Opus agents wrote a C compiler in Rust that compiles the Linux kernel). Claude Sonnet 4.6 followed Feb 17 (72.5% on OSWorld). Google launched Gemini 3 (Feb 26). OpenAI shipped the Frontier platform (Feb 5). Claude Code itself now writes 4% of all GitHub commits and reached $2.5B annualized run rate.

---

## II. The agentic toolkit: What each tool actually is

### Claude Code: The deterministic development and research agent

Claude Code is a terminal-native, foreground AI assistant for deep, iterative work — code, system administration, research analysis. It manipulates local filesystems, manages Docker, refactors codebases, and processes documents. Its behavior is governed by `CLAUDE.md` files (project-specific rules and context) and extended by MCP servers that provide structured access to external tools.

**Key capabilities for your setup:**

The **headless mode** (`claude -p "prompt"`) runs non-interactively with JSON output, session resumption by ID, MCP server loading, tool access control, and max-turn limits. This is how you build automated pipelines — a cron job or file-watcher triggers Claude Code with a specific prompt.

**Remote Control** (`claude remote-control` or `/rc`) generates a session URL and QR code. Scan from the Claude iOS app or open in any browser for full bidirectional sync. The session runs on Dionysus; you get a window into it from anywhere. Currently requires **Max plan** ($100–200/month); Pro support coming.

**Auto-memory** (via `/memory`) lets Claude save useful context automatically across sessions. **Subagents** spin up isolated Claude instances for specific subtasks, keeping the parent's context window clean — critical for long research sessions. **Parallel worktrees** let you run 3–5 Claude sessions simultaneously on different research tasks. **Skills as slash commands** turn recurring actions (format a citation, create a reading note, search a vault) into reusable patterns.

Boris Cherny, who created Claude Code, runs 5 instances in parallel tabs plus 5–10 on claude.ai/code, and shares this core insight: "The most important thing to get great results — **give Claude a way to verify its work.** If Claude has that feedback loop, it will 2–3x the quality." His team shares a single CLAUDE.md checked into git and uses subagents for common workflows (code-simplifier, verify-app).

**Security model:** CLAUDE.md behavioral rules → PreToolUse hooks (deterministic enforcement before tool execution) → settings.json deny lists (block specific bash commands, require human confirmation). This layered approach lets you grant filesystem access while blocking destructive operations.

**Pricing:** Pro ($20/month) gets Claude Code access. Max ($100–200/month) adds Remote Control and higher usage limits. API keys work for headless automation at pay-per-token rates (a 200-line analysis costs $0.02–$0.08 with Sonnet).

### OpenClaw: The autonomous background orchestrator

OpenClaw, Clawdbot, and Moltbot are the same project at different points in its naming history. Created by Peter Steinberger (Austrian developer, former PSPDFKit CEO), published as "Clawdbot" November 2025, renamed "Moltbot" January 27 after Anthropic's trademark complaint, became "OpenClaw" January 30. Hit ~200K GitHub stars. Steinberger announced joining OpenAI on February 14; the project is transferring to an open-source foundation.

OpenClaw is a **locally-running daemon** that connects to messaging platforms (WhatsApp, Telegram, Slack, Discord, Signal, iMessage) as its interface. Its architecture: a Node.js gateway service (WebSocket on port 18789) manages execution, state, tool dispatch, and channel routing. A model-agnostic "Pi Agent" connects to any LLM. A skills system (`SKILL.md` files with YAML frontmatter) extends capabilities. It maintains persistent memory via SQLite with vector embeddings, executes shell commands, controls browsers, and includes a "heartbeat" — waking every 30 minutes to check a `HEARTBEAT.md` checklist and take autonomous action unprompted.

**Where it excels for scholarship:** Asynchronous, long-running orchestration. Monitoring directories for new files, executing cron jobs, handling inbound audio recordings from a phone, scraping research databases while you're away from the keyboard. It's the always-on background process that Claude Code isn't designed to be.

**Where it's dangerous:** In February 2026, 341 malicious skills were found in ClawHub (12–20% of submitted skills were malicious), a CVE enabled remote command execution, credentials are stored in plaintext under `~/.openclaw/`. Cisco found skills performing data exfiltration. CrowdStrike released a removal pack. Google Cloud's VP of Security Engineering called it "an infostealer malware disguised as an AI personal assistant." The prompt injection surface is real — any data the agent reads can contain malicious instructions.

**Deployment recommendation:** If you use it at all, run it in an isolated Docker container, disable the `system.run` tool, vet every skill manually, execute under a dedicated non-privileged user account, and govern any shell access through an explicit allowlist. Or — and this is the pragmatic choice — use Claude Code's headless mode with cron/systemd for your automated pipelines instead, accepting slightly less "ambient intelligence" in exchange for a dramatically better security posture.

### Claude Cowork: The GUI agent (not for your server)

Cowork is Anthropic's desktop AI agent — Claude Code's capabilities wrapped in a GUI with an automatic filesystem sandbox. Released January 30 for macOS, Windows reached parity in February. Powered by Opus 4.6 with 1M-token context. Supports sub-agents, scheduled tasks (`/schedule`), 21+ plugins, and MCP connectors.

**Critical limitation: Cowork is not available on Linux.** An unofficial community package exists but runs without VM isolation — a significant security risk on a server. For Dionysus, Claude Code remains the right tool. Cowork is relevant for your Mac laptop when you want GUI-based agentic capabilities without touching the terminal.

Nav Toor's Cowork setup guide centers on **context files over prompts**: create a "Claude Context" folder with `about-me.md`, `brand-voice.md`, and `working-style.md`. "Stop thinking about better prompts and start thinking about better files." These compound over time — every week you refine them, outputs improve from generic to genuinely personalized.

### The broader competitive landscape

**Cursor** ($29.3B valuation, $1B ARR) runs agents on cloud VMs in parallel, triggerable from web, mobile, Slack, or GitHub. **Devin** ($20/month, down from $500) acquired Windsurf and is merging IDE + autonomous agent. **OpenAI Codex** has 1.5M+ weekly users and a macOS desktop app. **GitHub Copilot** (26M+ users) shipped CLI-native agents with multi-model selection (Claude, GPT, Gemini). **Perplexity Computer** treats multiple frontier models as specialized workers on a shared team.

The pattern across all of these: sub-agent architectures, MCP integration, SKILL.md/AGENTS.md portable instruction files, and multi-model selection are becoming universal standards.

---

## III. The three-layer architecture for Dionysus

### Layer 1: Synchronized knowledge base

Obsidian Headless runs as a systemd user service with `loginctl enable-linger`, keeping `~/vault/` in continuous sync:

```
iPhone (Obsidian iOS) ←→ Obsidian Sync Cloud ←→ Mac (Obsidian Desktop)
                                  ↕
                    Dionysus (ob sync --continuous)
```

```bash
# Installation
npm install -g obsidian-headless
export OBSIDIAN_AUTH_TOKEN="your-token"  # bypasses D-Bus keychain issue
ob sync-setup --vault "Research Vault" --device-name "Dionysus"
ob sync --continuous  # persistent sync daemon
```

The `obsidian-mcp` server (by StevenStavrakis, filesystem-based, no desktop app required) exposes read, write, search, and tag management to Claude Code. A `CLAUDE.md` at the vault root defines your conventions — wikilinks, YAML frontmatter, ISO dates, citation format, philosophical terminology, folder structure.

**Vault structure optimized for agent access:**

```
~/vault/
├── CLAUDE.md          # Rules: formatting, citations, philosophical framework
├── inbox/             # Drop zone — auto-processed by pipelines
├── processed/         # Agent-created structured notes
├── sources/           # Original PDFs
├── literature/        # Literature review notes (wiki-linked)
├── concepts/          # Philosophical concept notes
├── writing/           # Drafts and manuscripts
├── transcripts/       # Audio transcription outputs
├── film-club/         # Philosophy film club materials
└── daily/             # Daily notes and journals
```

**SyncThing vs. Obsidian Sync:** Report 2 recommends deprecating SyncThing for the active vault on the grounds that continuous background file modifications from agents cause race conditions. The counterargument: SyncThing is faster, free, and sufficient if only *one device* writes to the vault at a time. The practical approach is to use Obsidian Sync for the three-device mesh (it handles conflict resolution natively) and keep SyncThing for non-vault data transfers (audio files, bulk PDFs, general file sharing between Dionysus and Apollo).

### Layer 2: AI agent

Claude Code runs on Dionysus, connected to MCP servers:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian", "/home/logan/vault"]
    },
    "zotero": {
      "command": "npx",
      "args": ["-y", "zotero-mcp"]
    },
    "scite": {
      "command": "npx",
      "args": ["-y", "scite-mcp"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

The MCP ecosystem for academic tools now includes connectors for **Zotero** (local + web API, updated Feb 26), **Scite** (Smart Citations covering 250M+ articles, launched Feb 26), **PubMed**, **Consensus**, **Semantic Scholar**, **OpenAlex**, and **Crossref**. Librarian Aaron Tay argued that Claude with MCP servers may match or exceed specialized academic AI tools, especially for humanities and philosophy where non-journal content (monographs, grey literature, archival sources) matters — content that Elicit and Undermind underindex.

For interactive work: SSH into Dionysus via Tailscale, reattach tmux, work directly. For mobile oversight: use Remote Control from phone. For deep research: use Plan Mode (Shift+Tab twice) for complex multi-step tasks.

### Layer 3: Automation pipelines

**Audio-to-vault pipeline** (the highest-value automation for your workflow):

```
iPhone records audio → SyncThing syncs .m4a to ~/vault/inbox/
  → inotifywait detects new file
  → Docker container runs Whisper (leveraging GTX 1080 Ti CUDA cores)
  → Raw timestamped transcript generated locally
  → Claude Code (-p flag) structures the transcript:
      extracts arguments, debate points, open questions, action items
  → obsidian-mcp writes structured note to ~/vault/transcripts/
      with backlinks to existing concept notes
```

```bash
#!/bin/bash
# watch-inbox.sh — file-watch trigger
inotifywait -m "$HOME/vault/inbox" -e create -e moved_to --format '%f' | \
while read filename; do
  case "$filename" in
    *.m4a|*.wav|*.mp3)
      # Local GPU transcription
      docker exec whisper whisper "/inbox/$filename" --output_format txt
      # Structured analysis via Claude Code headless
      claude -p "Read transcripts/${filename%.m4a}.txt. Extract: \
        (a) core philosophical arguments, (b) structural debate points, \
        (c) open questions, (d) action items. Create a structured note \
        in processed/ with wikilinks to existing concept notes." \
        --mcp-config ~/.claude/mcp-servers.json \
        --output-format json > "logs/${filename}.json"
      ;;
    *.pdf)
      # PDF processing pipeline
      claude -p "Read inbox/$filename. Extract main thesis, key arguments \
        with page refs, engagement with other thinkers, relevance to your \
        current research. Create structured note in literature/." \
        --mcp-config ~/.claude/mcp-servers.json \
        --output-format json > "logs/${filename}.json"
      ;;
  esac
done
```

**Scheduled literature discovery** (cron-driven):

A morning script queries PhilPapers/arXiv for new papers matching research keywords. A nightly script processes any PDFs added during the day through OCR and Claude-generated summaries. Claude Code's `-p` flag enables this: `claude -p "Summarize this PDF focusing on methodology and key arguments" --output-format json --allowedTools "Read,Write,Bash"`.

**Multi-viewpoint debate simulation** (manual trigger):

Spawn isolated sub-agents programmed with distinct philosophical positions (Kantian deontologist, utilitarian, virtue ethicist). They debate a premise you provide, governed by conversational rules that surface logical blind spots. The resulting transcript — with argument mapping and vulnerability analysis — saves directly to the vault. This provides multi-faceted critique of your own theses prior to peer review.

---

## IV. Security architecture

The reports converge on a strict security model with three dimensions:

### Network: Zero Trust via Tailscale

All services bound to localhost or Tailscale IP only. UFW configured to drop all incoming traffic by default, explicitly allowing only `tailscale0` and SSH (port 22). VNC (currently exposed on 0.0.0.0:5900 without auth), Nginx default page, and PaddleOCR must be locked down immediately. The current state — deploying any agent into an environment with plaintext Git credentials and unauthenticated VNC — is categorically unsafe.

### Agent permissions: Defense in Depth via CLAUDE.md

Three layers of enforcement for Claude Code:

1. **Behavioral rules** in CLAUDE.md: negative constraints ("NEVER commit .env files," "NEVER hardcode credentials," "NEVER delete without confirmation")
2. **PreToolUse hooks**: deterministic checks before tool execution — block reading `.env` files, prevent operations on SyncThing-managed paths without confirmation
3. **Permission settings** in `.claude/settings.json`: deny lists for destructive bash commands (`rm -rf`, `DROP TABLE`), requiring human approval

For OpenClaw (if used): disable `system.run`, run under dedicated non-privileged user, govern shell access via explicit allowlist, run in isolated Docker container.

### Data: Separation of concerns

Raw inputs (`inbox/`) → processed outputs (`processed/`, `literature/`, `transcripts/`) → working storage (`writing/`). Agents write to processed directories; raw inputs remain untouched. SyncThing handles bulk file transfer (audio, PDFs); Obsidian Sync handles the vault. No agent gets unrestricted sudo. Docker access goes through MCP intermediary, not raw socket.

---

## V. Remote access: Solving mobile volatility

The traditional SSH-from-phone experience is fragile — sessions die on network switches, screen locks, and cellular handoffs. The 2026 solution is a dual-layer approach:

**Mosh** (Mobile Shell) operates over UDP, allowing seamless roaming between IP addresses without dropping the connection. It buffers keystrokes locally to eliminate cellular typing latency.

**Tmux** runs on Dionysus and manages session state. If mosh disconnects due to prolonged signal loss, the terminal session — and any running Claude Code processes — continues executing.

**Claude Code Remote Control** adds a third layer on top: a synchronized web interface that survives disconnection independently of the terminal session. You can interact from the Claude iOS app while the underlying tmux session persists on the server.

The launch command from iPhone: `mosh dionysus -- tmux new-session -A -s dev`. Start a multi-hour literature analysis, lock the phone, return hours later to completed output in the same terminal pane.

---

## VI. Scholarly tools ecosystem

Several open-source reference implementations exist specifically for academic research with Claude Code:

**Galaxy-Dawn/claude-scholar** provides 40+ skills and 14 agents covering the full research lifecycle — ideation through paper writing, review response, and conference prep — with Zotero MCP integration.

**pedrohcgs/claude-code-my-workflow** from an Emory economist offers a production-tested template with multi-agent review, adversarial QA, and replication protocols: `/research-ideation` → `/interview-me` → `/lit-review` → `/data-analysis` → `/review-paper`.

For philosophy specifically: **PhilLit** facilitates reliable literature reviews while mitigating hallucination via curated vector stores. **papercli** handles low-context PDF processing (extract key contributions, methodologies, bibliographies via CLI flags, avoiding loading entire 50-page papers into context). **Undermind** excels at deep niche-topic searches — critical for continental philosophy's specialized vocabulary.

For writing: the emerging pattern is Claude Code with CLAUDE.md defining your conventions + voice dictation (SuperWhisper on Mac) + Claude asking structured interview questions to draw out your arguments + iterative editing passes where you retain authorial control. One developer documented writing 2,000 words in 90 minutes using this loop.

Zack Shapiro's "Claude-Native Law Firm" offers a transferable insight: **domain expertise encoded in context files beats specialized AI products.** He codifies professional judgment as reusable skills rather than generic prompts, and found that a well-configured generalist model outperforms purpose-built tools. This generalizes directly to philosophy — a CLAUDE.md encoding your knowledge of phenomenology, deconstruction, and continental theory will produce better results than any generic "academic AI."

---

## VII. Concrete revisions to the Dionysus PROJECT.md

Based on the synthesized findings, these are the specific changes warranted:

### Security & Hardening → Elevated to blocking priority

Move beyond IP binding. Implement strict UFW rules for `tailscale0` + SSH only. Purge plaintext Git credentials immediately. Kill VNC on 0.0.0.0. Before deploying any agent, establish the CLAUDE.md defense-in-depth model with PreToolUse hooks. This is the prerequisite for everything else.

### SSH & Remote Access → Augment with mosh + Remote Control

Add mosh to the SSH stack for UDP roaming resilience. Standardize on tmux for session persistence (already in the plan). Integrate Claude Code Remote Control as the primary phone interaction mode once available on Pro tier — this replaces fragile SSH pipes for synchronous agent work.

### Storage & Environment → Delegate to Claude Code

Stop manual cleanup. Initialize Claude Code with dotfiles-architect instructions to analyze and purge the 100GB hidden sprawl. Use the Docker Hub MCP to automate the Docker data-root migration to `/data/docker/`. Standardize on Node.js 22 LTS (required by OpenClaw, beneficial for Obsidian Headless). Let Claude Code untangle the pip/conda/uv overlap deterministically.

### Multi-Device Integration → Obsidian Headless replaces Xvfb

Deploy `obsidian-headless` with `ob sync --continuous` as a systemd user service. Use `OBSIDIAN_AUTH_TOKEN` to bypass the D-Bus keychain issue. This gives Dionysus the canonical vault state without the 1.5GB RAM overhead of the Xvfb approach. Keep SyncThing for non-vault file transfer (audio drops, bulk PDFs). Use Obsidian Sync for the three-device vault mesh.

### Service Deployment → Dual-agent architecture

Formalize the split: Claude Code for synchronous, foreground work (development, research sessions, system maintenance). Automated pipelines via Claude Code headless (`-p` flag) triggered by cron or inotifywait, managed as systemd services. If OpenClaw is adopted, deploy it strictly as a background orchestrator via systemd user unit, sandboxed, with `system.run` disabled.

### New section: Scholarly Pipelines

Add this to the active scope. The audio-to-vault pipeline (SyncThing drop → Whisper on GPU → Claude structuring → obsidian-mcp injection) is the highest-value automation. Scheduled literature discovery via cron is second. Both are achievable with Claude Code headless mode + MCP servers + systemd, without requiring OpenClaw.

### New section: CLAUDE.md as institutional knowledge

Invest in the vault-root `CLAUDE.md` as a compounding asset. After every correction, end with "Update your CLAUDE.md so you don't make that mistake again." Build skills as slash commands for recurring actions. Encode your philosophical framework, citation conventions, writing voice, and domain terminology. This is where Shapiro's insight applies: context files encoding your expertise will outperform any specialized tool.

### Pricing decision

**Immediate path:** Claude Pro ($20/month) + API key for headless automation. This gets you Claude Code, headless `-p` mode, and MCP servers — everything except Remote Control from phone.

**When Remote Control hits Pro:** Your full three-device workflow becomes available at $20/month.

**If you need Remote Control now:** Max plan at $100/month. Evaluate whether the phone-based oversight is worth 5x the cost given that you can SSH + tmux from a terminal app for free.

**Obsidian Sync:** Required for the headless architecture ($4–8/month depending on plan). Worth it to eliminate the Xvfb workaround and get native conflict resolution across three devices.

---

## VIII. What to build first

Given where Dionysus currently stands (cleanup just completed, security vulnerabilities still open, no agent infrastructure yet), the build order that minimizes risk while delivering value:

1. **Harden the network** — UFW rules, kill VNC, purge plaintext credentials, lock everything to Tailscale. This is a prerequisite for everything else and takes an afternoon.

2. **Deploy Obsidian Headless** — Install `obsidian-headless`, configure the systemd service, verify three-device sync. This gives you the canonical vault on the server with minimal risk.

3. **Set up Claude Code with CLAUDE.md** — Write the vault-root CLAUDE.md with your philosophical framework, citation conventions, and security rules. Configure the obsidian-mcp server. Start using Claude Code interactively via SSH + tmux for research sessions.

4. **Build the PDF processing pipeline** — inotifywait on `inbox/` triggering Claude Code headless. This is the simplest automation and immediately useful.

5. **Build the audio pipeline** — Whisper in Docker + Claude structuring. Requires the Docker data-root migration first (or enough space on root partition).

6. **Add scheduled literature discovery** — Cron-driven queries to PhilPapers/Semantic Scholar via MCP, with results landing as vault notes.

7. **Evaluate Remote Control** — Once available on Pro, or if you upgrade to Max, this completes the phone-based oversight loop.

Each step is independently valuable and builds on the previous one. You don't need OpenClaw for any of this — Claude Code headless + cron + systemd covers the automation layer with a far better security model.
