---
slice: 2 (Architecture + runtime + Pi SDK relationship)
date: 2026-04-28
agent: codex GPT-5.5 high
status: complete
---

# Slice 2 output - Architecture + runtime + Pi SDK relationship

## (i) What I read

gsd-2 source / README:

- `README.md:1-24` - package identity, npm install snippet, Pi SDK and RTK claims.
- `README.md:226-360` - v1/v2 runtime comparison, `.gsd` state-machine description, auto/step mode.
- `package.json:1-158` - package name/version, workspaces, bin entries, files list, `piConfig`, engines, scripts, dependencies, optional dependencies.
- `package-lock.json:1-80` - lockfile version, root package metadata, workspace/dependency/bin snapshot.
- `.npmignore:1-8` - npm pack note that `files` in `package.json` controls included files.
- `tsconfig.json:1-16` - TypeScript module/target/outDir/rootDir/include/exclude.
- `src/loader.ts:1-180` and `src/loader.ts:174-260` - startup loader, runtime checks, environment setup, resource discovery, workspace package linking, dynamic import of `cli.js`.
- `src/cli.ts:1-260`, `src/cli.ts:260-620`, and `src/cli.ts:618-820` - CLI modes, Pi package imports, RTK preference gate, graph/web/headless/auto/print/MCP/interactive paths.
- `src/resource-loader.ts:1-240` and `src/resource-loader.ts:240-520` - GSD resource sync and agent `node_modules` linking.
- `src/app-paths.ts:1-8` - GSD home, agent, sessions, auth, web PID paths.
- `src/runtime-checks.ts:1-45` - Node and git precondition helpers.
- `src/mcp-server.ts:1-178` - in-process MCP server for exposing active agent tools.
- `src/resources/extensions/gsd/extension-manifest.json:1-33` - core GSD extension manifest.
- `src/resources/extensions/gsd/index.ts:1-37` - GSD extension entrypoint.
- `src/resources/extensions/gsd/bootstrap/register-extension.ts:1-139` - GSD extension wiring of commands, tools, shortcuts, hooks, ecosystem handlers.
- `packages/*/package.json` - workspace package identities and dependencies: `daemon`, `mcp-server`, `native`, `pi-agent-core`, `pi-ai`, `pi-coding-agent`, `pi-tui`, `rpc-client`.
- `packages/pi-coding-agent/src/index.ts:1-220` - public exports for config, session, extension system, SDK factory, tools.
- `packages/pi-coding-agent/src/main.ts:1-220` - upstream-like Pi CLI entrypoint.
- `packages/pi-coding-agent/src/config.ts:1-220` - package detection, `PI_PACKAGE_DIR`, app/config directory derivation.
- `packages/pi-coding-agent/src/core/resource-loader.ts:1-460` - project context discovery, extension/skill/theme/prompt resource loader.
- `packages/pi-coding-agent/src/core/package-manager.ts:1-260` and `packages/pi-coding-agent/src/core/package-manager.ts:1588-1745` - resource source resolution and global/project resource directories.
- `packages/pi-coding-agent/src/core/sdk.ts:1-520` - `createAgentSession`, model/auth/session/resource/tool assembly.
- `packages/pi-coding-agent/src/core/system-prompt.ts:1-298` - system prompt construction and context/skill injection.
- `packages/pi-coding-agent/src/core/tools/index.ts:1-218` - built-in tool exports and active tool sets.
- `packages/pi-coding-agent/src/core/extensions/index.ts:1-186` and `packages/pi-coding-agent/src/core/extensions/types.ts:1-260,1288-1570` - extension API and typed contract surface.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:1-130,300-360` - extension runtime imports, virtual module aliases, original Pi package aliases.
- `packages/pi-agent-core/src/agent.ts:1-220` and `packages/pi-agent-core/src/agent-loop.ts:1-220` - core agent state/loop and LLM/tool-call boundary.
- `packages/native/src/index.ts:1-128`, `native/Cargo.toml:1-19`, and `native/crates/*` listing - Rust/N-API native module layout.
- `packages/mcp-server/README.md:1-220` and `packages/mcp-server/src/cli.ts:1-70` - standalone MCP server package and stdio entrypoint.
- `packages/rpc-client/README.md:1-125` - standalone RPC client package.
- `Dockerfile:1-20` and `docker/README.md:1-144` - container runtime and sandbox documentation.

gsd-2 docs:

- `docs/dev/architecture.md:1-176` - current architecture overview, bundled extensions/agents, native engine, dispatch pipeline, key modules.
- `docs/dev/ADR-010-pi-clean-seam-architecture.md:1-260` - proposed Pi clean-seam refactor and current vendoring/seam diagnosis.
- `docs/dev/FILE-SYSTEM-MAP.md:1-220` - subsystem labels and source-file map.
- `docs/user-docs/getting-started.md:1-200` - prerequisites and install instructions.
- `docs/user-docs/configuration.md:1-220` - preferences, MCP client config, environment variables, token telemetry.
- `docs/user-docs/hooks.md:1-151` - hook configuration and trust model.

External docs:

- None. The README references Pi SDK and RTK, but the local source and local docs were sufficient for this slice's architecture questions; I did not follow external links.

## (ii) Calibrated findings

### Q1: What is the runtime architecture?

**Finding 1.1 - runtime shape (high confidence):** gsd-2 appears to be a Node/TypeScript CLI package named `gsd-pi`, with `gsd` and `gsd-cli` bin entries pointing to `dist/loader.js`; `gsd-pi` itself points to `scripts/install.js` (`package.json:1-24`). The TypeScript project targets NodeNext/ES2022 and compiles `src` to `dist` (`tsconfig.json:1-16`).

**Finding 1.2 - runtime preconditions (high confidence):** the package declares Node `>=22.0.0` (`package.json:43-45`) and the loader enforces Node major 22 plus availability of `git` before importing heavier runtime code (`src/runtime-checks.ts:4-45`; `src/loader.ts:32-69`). User docs recommend Node 24 LTS and Git 2.20+ (`docs/user-docs/getting-started.md:7-15`).

**Finding 1.3 - startup composition (high confidence):** startup is intentionally split into `loader.ts` and `cli.ts`: `loader.ts` handles fast `--version`/`--help`, validates runtime dependencies, sets GSD/Pi environment variables, resolves bundled resources, links workspace packages, then dynamically imports `cli.js` (`src/loader.ts:7-30`, `src/loader.ts:71-89`, `src/loader.ts:142-164`, `src/loader.ts:174-245`). The architecture doc describes this as a two-file loader pattern so `PI_PACKAGE_DIR` is set before SDK code evaluates (`docs/dev/architecture.md:34-40`).

**Finding 1.4 - app data paths (high confidence):** the main GSD runtime root defaults to `~/.gsd`, with `~/.gsd/agent`, `~/.gsd/sessions`, `~/.gsd/agent/auth.json`, and web PID/preferences paths derived from it (`src/app-paths.ts:1-8`). The loader sets `GSD_CODING_AGENT_DIR` to the GSD agent dir and `GSD_PKG_ROOT` to the package root before importing the CLI (`src/loader.ts:109-115`).

**Finding 1.5 - language/runtime dependency graph (high confidence):** the root package builds a workspace of TypeScript packages (`packages/*`, `studio`, `extensions/*`) and build scripts compose `@gsd/native`, `@gsd/pi-tui`, `@gsd/pi-ai`, `@gsd/pi-agent-core`, `@gsd/pi-coding-agent`, `@gsd-build/rpc-client`, and `@gsd-build/mcp-server` before compiling the root (`package.json:14-19`, `package.json:47-57`). At runtime, `src/cli.ts` imports or dynamically imports `@gsd/pi-coding-agent` for `AuthStorage`, `DefaultResourceLoader`, `ModelRegistry`, `SettingsManager`, `SessionManager`, `createAgentSession`, `InteractiveMode`, `runPrintMode`, and `runRpcMode` (`src/cli.ts:1-6`, `src/cli.ts:34-40`, `src/cli.ts:491-501`).

**Finding 1.6 - LLM/agent loop substrate (high confidence):** `@gsd/pi-agent-core` owns the `Agent` class and core loop; it imports LLM provider abstractions and `streamSimple` from `@gsd/pi-ai` (`packages/pi-agent-core/src/agent.ts:6-17`) and the loop converts agent messages to provider messages at the LLM boundary (`packages/pi-agent-core/src/agent-loop.ts:1-13`, `packages/pi-agent-core/src/agent-loop.ts:216-220`).

**Finding 1.7 - native substrate (high confidence):** performance-sensitive functions are exposed through `@gsd/native`, a TypeScript wrapper over Rust/N-API modules for grep/glob/ps/highlight/ast/diff/text/html/image/fd/clipboard/parser/truncation (`packages/native/package.json:1-19`, `packages/native/src/index.ts:1-128`, `native/Cargo.toml:1-19`). The root package includes platform-specific optional engine packages (`package.json:145-153`).

**Finding 1.8 - RTK relationship (medium confidence):** RTK is a managed external binary, not a TypeScript library dependency. The install script names RTK version `0.33.1`, repository `rtk-ai/rtk`, supported platform archive names, skip env vars, and telemetry-disabled env (`scripts/install.js:153-164`, `scripts/install.js:268-403`; see also `src/rtk.ts:25-82`). At runtime, `src/cli.ts` gates RTK behind `preferences.experimental.rtk === true`; otherwise it sets `GSD_RTK_DISABLED=1` (`src/cli.ts:160-178`). Shell-command rewriting is wired through shared helpers used by GSD verification/custom command paths rather than the Pi agent core itself (`src/resources/extensions/gsd/preferences-types.ts:284-288`; `src/resources/extensions/gsd/verification-gate.ts:11`; `src/resources/extensions/gsd/custom-verification.ts:26`).

**Finding 1.9 - modes (high confidence):** gsd-2 supports interactive TUI, print/text/json, RPC, MCP, web, headless, and `auto` shorthand. `src/cli.ts` routes `--mode rpc`, `--mode mcp`, `--print`, `headless`, `auto`, `--web`, `web stop`, `sessions`, `worktree`, and `graph` through distinct branches (`src/cli.ts:76-90`, `src/cli.ts:221-294`, `src/cli.ts:331-355`, `src/cli.ts:424-462`, `src/cli.ts:618-720`, `src/cli.ts:753-820`).

**Finding 1.10 - sandbox semantics (medium confidence):** the ordinary CLI is not itself sandboxed by default in the code I read; it runs in the caller's project cwd with tool permissions and hooks controlled by settings/extensions. A separate Docker sandbox path exists: the root `Dockerfile` installs `gsd-pi` in `node:24-slim` with Git and `ENTRYPOINT ["gsd"]` (`Dockerfile:6-20`), while Docker docs describe Docker Sandbox/MicroVM isolation or Docker Compose container isolation as an optional way to prevent host filesystem access (`docker/README.md:1-4`, `docker/README.md:28-60`).

### Q2: What is gsd-2 vs Pi SDK vs RTK?

**Finding 2.1 - current Pi relationship is vendored, not a clean external dependency (high confidence):** gsd-2 vendors four Pi-derived packages under the `@gsd` scope: `@gsd/pi-agent-core`, `@gsd/pi-ai`, `@gsd/pi-tui`, and `@gsd/pi-coding-agent`; their package descriptions explicitly say "vendored from pi-mono" for the Pi packages (`packages/pi-agent-core/package.json:1-22`, `packages/pi-ai/package.json:1-44`, `packages/pi-tui/package.json:1-34`, `packages/pi-coding-agent/package.json:1-50`). The root package does not list `@mariozechner/pi-*` dependencies; it links workspace packages from `packages/*` (`package.json:14-19`, `src/loader.ts:174-199`).

**Finding 2.2 - root gsd-2 code starts above `@gsd/pi-coding-agent` (high confidence):** the top-level `src/cli.ts` is GSD-specific glue: it uses GSD app paths, onboarding, update checks, RTK bootstrap, web/headless/auto behavior, and imports Pi coding-agent classes/functions to create sessions and modes (`src/cli.ts:1-40`, `src/cli.ts:491-523`). `src/loader.ts` sets GSD branding/config/resource env vars before importing `cli.js` (`src/loader.ts:79-90`, `src/loader.ts:135-164`).

**Finding 2.3 - core GSD workflow logic lives mostly as a bundled Pi extension (high confidence):** `src/resources/extensions/gsd/extension-manifest.json` declares the core "GSD Workflow" extension, including provided tools, commands, hooks, and shortcuts (`src/resources/extensions/gsd/extension-manifest.json:1-33`). Its entrypoint registers `/gsd` first, then attempts full GSD bootstrap (`src/resources/extensions/gsd/index.ts:18-36`). Full bootstrap registers worktree/exit commands, dynamic/db/journal/query/memory/exec tools, shortcuts, cmux event listeners, hooks, and ecosystem extensions (`src/resources/extensions/gsd/bootstrap/register-extension.ts:70-139`).

**Finding 2.4 - Pi substrate includes the extension API used by GSD (high confidence):** `@gsd/pi-coding-agent` exports extension types and runtime functions such as `ExtensionAPI`, `ExtensionContext`, `discoverAndLoadExtensions`, `ExtensionRunner`, and wrapper helpers (`packages/pi-coding-agent/src/index.ts:50-169`). The extension type docs say extensions can subscribe to lifecycle events, register LLM-callable tools, register commands/shortcuts/flags, and use UI primitives (`packages/pi-coding-agent/src/core/extensions/types.ts:1-9`).

**Finding 2.5 - boundaries are materially entangled today (high confidence):** a gsd-2 ADR says the project vendors Pi packages by copying source into `/packages/`, and that "substantial original logic" has been written directly inside `pi-coding-agent`, with no reliable way to distinguish GSD files from Pi files without individual reading (`docs/dev/ADR-010-pi-clean-seam-architecture.md:10-30`). Source observations match this: `packages/pi-coding-agent/src/core/sdk.ts` owns GSD-facing session assembly and imports GSD-scoped Pi packages plus GSD-relevant helpers (`packages/pi-coding-agent/src/core/sdk.ts:41-54`, `packages/pi-coding-agent/src/core/sdk.ts:86-131`), while GSD root code imports that SDK as `@gsd/pi-coding-agent` (`src/cli.ts:1-6`, `src/cli.ts:491-501`).

**Finding 2.6 - not monkey-patching in the narrow sense, but not clean library use either (medium confidence):** I did not observe GSD monkey-patching Pi prototypes at runtime. The composition appears to be vendored package modification, environment-variable configuration (`PI_PACKAGE_DIR`, `GSD_CODING_AGENT_DIR`), extension registration, and module aliasing for extensions (`src/loader.ts:86-90`, `src/loader.ts:109-115`, `packages/pi-coding-agent/src/core/extensions/loader.ts:61-91`, `packages/pi-coding-agent/src/core/extensions/loader.ts:325-342`). This is cleaner than runtime monkey-patching but less separable than "gsd imports Pi as an external library."

**Finding 2.7 - original Pi package aliases are explicitly supported (high confidence):** the extension loader maps both `@gsd/pi-*` and original `@mariozechner/pi-*` specifiers to bundled modules, indicating compatibility with external Pi ecosystem imports while still resolving to gsd-2's vendored copies (`packages/pi-coding-agent/src/core/extensions/loader.ts:61-91`, `packages/pi-coding-agent/src/core/extensions/loader.ts:329-341`).

**Finding 2.8 - RTK sits beside Pi/GSD as shell-output compression tooling (medium confidence):** RTK is provisioned/downloaded separately by install/bootstrap code and used by GSD shell-command/verification paths; it is not part of the Pi SDK package graph and does not appear in `package.json` dependencies (`package.json:103-153`; `scripts/install.js:153-164`; `src/cli.ts:160-178`).

**Direction-shifting evidence (medium confidence):** if a downstream plan assumes a clean "GSD app on top of Pi SDK" boundary, current source suggests a modified/vendored Pi fork plus a GSD extension/app layer. The project itself has a proposed ADR to create a cleaner seam, but that ADR describes a future package structure (`@gsd/agent-core`, `@gsd/agent-modes`) rather than the current package tree I observed (`docs/dev/ADR-010-pi-clean-seam-architecture.md:43-75`, `docs/dev/ADR-010-pi-clean-seam-architecture.md:196-205`).

### Q3: What is the module / file structure?

**Finding 3.1 - brief tree view (high confidence):**

```text
gsd-2-explore/
  package.json, package-lock.json, tsconfig*.json
    npm workspace root for `gsd-pi`; Node >=22; root CLI bins and build/test scripts.
  src/
    root GSD CLI/bootstrap/web/headless/MCP glue; excludes `src/resources`, `src/tests`, `src/web` from main TS build.
    resources/
      bundled runtime resources copied/synced into `~/.gsd/agent`: GSD workflow doc, agents, extensions.
      extensions/gsd/
        core GSD workflow extension: commands, auto loop, state, preferences, hooks, tools, memory, worktree, verification.
      extensions/*
        supporting extensions such as async jobs, bg shell, browser tools, claude-code-cli, mcp-client, search, remote questions.
    web/
      service layer for browser/web mode.
  packages/
    pi-agent-core/
      vendored core agent loop/types.
    pi-ai/
      vendored multi-provider LLM API and provider/model registry.
    pi-tui/
      vendored terminal UI framework.
    pi-coding-agent/
      vendored coding-agent package plus extension system, session/mode/tool machinery used by GSD.
    native/
      TypeScript wrappers for Rust/N-API modules.
    mcp-server/
      publishable MCP stdio server exposing GSD session/workflow/read tools.
    rpc-client/
      publishable RPC client SDK for spawning/interacting with the GSD agent process.
    daemon/
      background daemon package for monitoring/Discord integration.
  native/
    Rust workspace and build scripts for native engine crates.
  web/
    Next.js frontend for web interface.
  studio/
    Electron/Vite studio app.
  vscode-extension/
    VS Code extension with chat/sidebar/RPC integration.
  docs/, gitbook/, mintlify-docs/
    user/developer docs in multiple publishing formats.
  docker/
    Docker sandbox and CI-builder assets.
  extensions/google-search/
    extracted workspace reference extension.
  gsd-orchestrator/
    skill-style orchestrator bundle.
  scripts/
    build, install, release, validation, test, RTK, and packaging scripts.
```

Citations: top-level directory listing; `package.json:14-19`; `package.json:20-38`; `tsconfig.json:14-16`; `docs/dev/architecture.md:5-26`; `docs/dev/architecture.md:54-108`; `docs/dev/FILE-SYSTEM-MAP.md:70-220`; `packages/*/package.json`; `native/Cargo.toml:1-19`.

**Finding 3.2 - entry points (high confidence):** primary CLI entry is `dist/loader.js` via package bins `gsd` and `gsd-cli` (`package.json:20-24`). `loader.ts` dynamically imports `./cli.js` after environment/resource setup (`src/loader.ts:245-246`). Separate package-level entry points include `gsd-mcp-server` in `packages/mcp-server` (`packages/mcp-server/package.json:28-30`; `packages/mcp-server/src/cli.ts:1-70`), `@gsd-build/rpc-client` as a library (`packages/rpc-client/package.json:19-27`; `packages/rpc-client/README.md:1-29`), and `gsd-daemon` (`packages/daemon/package.json:23-25`).

**Finding 3.3 - resource sync shape (high confidence):** bundled `src/resources` are copied/synced to `~/.gsd/agent` on launch, with manifest/content-hash tracking and stale-resource pruning (`src/resource-loader.ts:20-32`, `src/resource-loader.ts:247-275`, `src/resource-loader.ts:315-353`, `docs/dev/architecture.md:42-45`). The loader also computes `GSD_BUNDLED_EXTENSION_PATHS` by scanning bundled extensions and remapping them to the managed agent extension directory (`src/loader.ts:142-164`).

### Q4: How does gsd-2 ship?

**Finding 4.1 - primary shipping path is npm (high confidence):** the README and getting-started docs install with `npm install -g gsd-pi` or `npm install -g gsd-pi@latest` (`README.md:20`, `docs/user-docs/getting-started.md:44-48`). `package.json` names the package `gsd-pi` at version `2.78.1` and exposes `gsd`, `gsd-cli`, and `gsd-pi` bins (`package.json:1-24`).

**Finding 4.2 - package contents are explicit (high confidence):** npm publish contents are controlled by the `files` array: `dist`, `dist/web`, `packages`, `pkg`, `src/resources`, install scripts, workspace linking scripts, package metadata, and README (`package.json:25-38`). `.npmignore` says the `files` field determines included files and exists to prevent `.gitignore` from interfering with npm pack (`.npmignore:1-8`).

**Finding 4.3 - lockfile/package manager (high confidence):** the repo uses npm (`packageManager: "npm@10.9.3"`) and has a v3 `package-lock.json` matching the root package/workspaces/dependencies (`package.json:46`; `package-lock.json:1-16`).

**Finding 4.4 - installable as executable and as several libraries (high confidence):** root `gsd-pi` is executable-oriented through CLI bins (`package.json:20-24`). Several workspace packages are also publishable libraries/executables: `@gsd-build/mcp-server` has `main`, `types`, exports, and `gsd-mcp-server` bin (`packages/mcp-server/package.json:19-30`); `@gsd-build/rpc-client` is a standalone SDK with exports and no runtime dependencies (`packages/rpc-client/package.json:19-38`; `packages/rpc-client/README.md:1-10`); `@gsd/native` exposes subpath modules for native functions (`packages/native/package.json:19-92`).

**Finding 4.5 - native/platform distribution (medium confidence):** native Rust functionality is built from a Rust workspace under `native/` and surfaced via `@gsd/native` (`native/Cargo.toml:1-19`, `packages/native/src/index.ts:1-128`). Root optional dependencies include platform engine packages named `@gsd-build/engine-*`, suggesting prebuilt native engines are pulled when available (`package.json:145-153`).

**Finding 4.6 - Docker path exists but appears secondary (medium confidence):** the root Dockerfile builds a runtime image by installing `gsd-pi` globally and setting `ENTRYPOINT ["gsd"]` (`Dockerfile:6-20`). Docker docs describe sandbox/compose workflows as an isolated way to run auto mode, not the base installation path (`docker/README.md:1-4`, `docker/README.md:26-60`).

### Q5: Is there an agent-runtime contract?

**Finding 5.1 - yes, but it is plural and layered (high confidence):** gsd-2 defines several interaction contracts: a human-facing CLI/TUI contract (`gsd`, slash commands, `auto`, `headless`, modes), a Pi extension API contract, auto-loaded context files (`AGENTS.md`/`CLAUDE.md`), skills, MCP server surfaces, and RPC client protocol. These are not one single "agent-runtime contract" file; they are distributed through Pi resource loading, extension manifests/types, and CLI/MCP/RPC entry points.

**Finding 5.2 - auto-loaded instruction files (high confidence):** `DefaultResourceLoader` searches global agent dir and each cwd ancestor for `AGENTS.md` or `CLAUDE.md`, deduplicates them, and returns them as project context files (`packages/pi-coding-agent/src/core/resource-loader.ts:57-112`). The system prompt builder appends context files under `# Project Context` (`packages/pi-coding-agent/src/core/system-prompt.ts:130-137`, `packages/pi-coding-agent/src/core/system-prompt.ts:278-285`).

**Finding 5.3 - system prompt/tool contract (high confidence):** Pi's default system prompt tells the model it is operating inside "pi, a coding agent harness," lists active tools, includes guidelines tied to active tools, includes Pi docs pointers, appends skills when read/Skill access exists, and always includes current working directory (`packages/pi-coding-agent/src/core/system-prompt.ts:21-70`, `packages/pi-coding-agent/src/core/system-prompt.ts:168-297`).

**Finding 5.4 - built-in tool surface (high confidence):** default active tool names are read/bash/edit/write/lsp or hashline variants, while all built-ins include read, bash, edit, write, grep, find, ls, lsp, hashline_edit, and hashline_read (`packages/pi-coding-agent/src/core/sdk.ts:327-339`; `packages/pi-coding-agent/src/core/tools/index.ts:138-161`). MCP mode activates every registered tool before serving external clients (`src/cli.ts:693-710`).

**Finding 5.5 - slash/command surface (high confidence):** the core GSD extension manifest declares commands `gsd`, `kill`, `worktree`, and `exit` (`src/resources/extensions/gsd/extension-manifest.json:14`). The GSD extension entrypoint registers `/gsd` first even if full setup later fails (`src/resources/extensions/gsd/index.ts:18-36`), and full bootstrap registers additional GSD commands/tools/hooks/shortcuts (`src/resources/extensions/gsd/bootstrap/register-extension.ts:70-139`).

**Finding 5.6 - extension API contract (high confidence):** the extension API supports registering LLM-callable tools, commands, shortcuts, providers, and event handlers, and gives UI primitives such as select/confirm/input/notify/widgets/editor (`packages/pi-coding-agent/src/core/extensions/types.ts:1-9`, `packages/pi-coding-agent/src/core/extensions/types.ts:111-242`, `packages/pi-coding-agent/src/core/extensions/types.ts:1288-1570`).

**Finding 5.7 - skills contract (high confidence):** skills are loaded from global ecosystem `~/.agents/skills`, project `.agents/skills` ancestor directories, and legacy config-dir skills, with skill discovery requiring direct `.md` files at roots or recursive `SKILL.md` under subdirectories (`packages/pi-coding-agent/src/core/skills.ts:10-27`, `packages/pi-coding-agent/src/core/skills.ts:153-250`, `packages/pi-coding-agent/src/core/package-manager.ts:1635-1718`).

**Finding 5.8 - MCP contracts (high confidence):** `gsd --mode mcp` starts an in-process MCP server exposing the active session's registered tools over stdin/stdout (`src/cli.ts:693-712`; `src/mcp-server.ts:57-78`, `src/mcp-server.ts:96-178`). A separate `@gsd-build/mcp-server` package exposes session/read, interactive, and workflow tools such as `gsd_execute`, `gsd_status`, `gsd_result`, `ask_user_questions`, and many workflow mutation tools (`packages/mcp-server/README.md:1-12`, `packages/mcp-server/README.md:76-127`, `packages/mcp-server/README.md:129-220`).

**Finding 5.9 - RPC contract (high confidence):** `@gsd-build/rpc-client` is a standalone SDK that spawns the agent process, handshakes with a v2 protocol, sends prompts/steering/follow-ups, receives typed events, and exposes session/model helpers (`packages/rpc-client/README.md:1-29`, `packages/rpc-client/README.md:31-120`).

**Finding 5.10 - hooks/security/trust contract (medium confidence):** GSD has Layer 0 shell-command hooks in settings, with project-scoped hooks requiring explicit trust via a marker file according to docs (`docs/user-docs/hooks.md:1-41`, `docs/user-docs/hooks.md:93-107`). The core extension manifest also declares numerous lifecycle hooks at the extension level (`src/resources/extensions/gsd/extension-manifest.json:15-30`). This is central enough to flag for cross-slice synthesis because hooks are both an agent contract and a security/trust surface.

## (iii) What I deliberately did NOT read

- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/audits/archive/`.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/INITIATIVE.md`.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/DECISION-SPACE.md`.
- I did not read other orchestration specs besides the common preamble and slice-2 spec. I only listed the exploration directory to determine whether this output file already existed; I did not read slice-1 output.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md`.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/research/gemini-deep-research/`.
- I did not read `~/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/`.
- I did not inspect gsd-2 release history beyond local README/changelog-adjacent snippets; release cadence is slice 5.
- I did not deeply audit user-facing command semantics, automation/test primitives, artifact formats, or migration behavior except where they directly revealed architecture/contract surfaces.
- I did not inspect external Pi SDK or RTK repositories. Local source and docs were enough to characterize current gsd-2 architecture for this slice without importing external framing.

## (iv) Open questions surfaced

- **Current vs proposed Pi seam (direction-shifting, high confidence):** The current source tree has no `packages/gsd-agent-core` or `packages/gsd-agent-modes`, while ADR-010 proposes those as the future clean seam (`docs/dev/ADR-010-pi-clean-seam-architecture.md:47-75`). Second wave should not assume that the proposed seam is implemented; it should treat "clean seam" as a planned or partially planned architecture unless verified in a newer source snapshot.

- **How much of `pi-coding-agent` is original Pi vs GSD-authored now? (high confidence that unresolved):** ADR-010 reports approximately 79 GSD-authored files inside `pi-coding-agent` and says the lack of distinction blocks updates (`docs/dev/ADR-010-pi-clean-seam-architecture.md:21-30`). This slice did not perform file-by-file provenance classification. A downstream intervention that touches Pi packages would need that map.

- **Which agent contract is load-bearing for downstream use? (medium confidence):** gsd-2 exposes multiple contracts: CLI/TUI, extension API, MCP server package, in-process MCP mode, RPC client, skills, `AGENTS.md`/`CLAUDE.md`, and hooks. Second wave should decide which contract it is evaluating rather than treating "the agent runtime contract" as singular (`src/cli.ts:76-90`, `packages/pi-coding-agent/src/core/extensions/types.ts:1-9`, `packages/mcp-server/README.md:1-12`, `packages/rpc-client/README.md:1-29`).

- **RTK default behavior needs source-level confirmation in active release (medium confidence):** README says GSD provisions managed RTK "to compress shell-command output" (`README.md:22`), but `src/cli.ts` says runtime RTK is opt-in via `experimental.rtk` and disabled by default (`src/cli.ts:167-176`). This may be a README register issue, a release transition artifact, or a distinction between provisioning and activation.

- **Security model appears central (medium confidence):** I saw explicit surfaces for hooks, project trust, URL blocking, secret collection, command allowlists, Docker sandboxing, and project-scoped hook trust (`docs/user-docs/hooks.md:93-107`; `docs/user-docs/configuration.md:155-165`; `packages/mcp-server/README.md:114-127`; `docker/README.md:1-4`). This is central enough for synthesis, but not fully analyzed in this architecture slice.

- **Telemetry/observability appears central (medium confidence):** README emphasizes worktree telemetry, token/cost ledgers, dashboards, forensics, and stuck detection (`README.md:32-39`, `README.md:67-75`, `README.md:331-335`). Configuration docs expose opt-in per-call token telemetry (`docs/user-docs/configuration.md:155-195`). This slice did not characterize the full observability model.

- **Debug/failure recovery appears central (medium confidence):** README and architecture docs mention crash recovery, stuck detection, forensics, doctor, recovery diagnostics, and lock files (`README.md:323-329`, `docs/dev/architecture.md:30-33`, `docs/dev/FILE-SYSTEM-MAP.md:26-27`, `docs/dev/FILE-SYSTEM-MAP.md:82-87`). This should be integrated by slices focused on operations/testing/failure modes.

- **Multi-user/collaboration is present but not scoped here (medium-low confidence):** README and docs reference working in teams, remote questions, Discord/Slack/Telegram routing, daemon, GitHub sync, and shared artifacts (`README.md:205-211`, `packages/daemon/package.json:1-35`, `docs/user-docs/configuration.md:79-153`). I did not determine whether this is central or mostly peripheral.

## (v) Flags where README claims diverge from source observations

- **RTK activation/register divergence (medium confidence):** README line 22 says GSD provisions a managed RTK binary "to compress shell-command output" and says `GSD_RTK_DISABLED=1` disables the integration (`README.md:22`). Source shows install/bootstrap can provision RTK, but runtime compression is opt-in via `preferences.experimental.rtk === true`; if the preference is not true, `src/cli.ts` sets `GSD_RTK_DISABLED=1` itself (`src/cli.ts:167-178`). This reads as a concrete README/source tension unless README is only describing availability/provisioning, not default activation.

- **No other README/source divergence observed within this slice's scope (medium confidence):** README's high-level claims that gsd-2 is a TypeScript application built on Pi SDK, manages `.gsd` state, creates fresh sessions, exposes MCP, uses worktrees, tracks costs, and has Docker docs are broadly supported by the local source/docs I inspected (`README.md:14-22`, `README.md:235-252`, `README.md:313-339`; `docs/dev/architecture.md:1-52`; `src/cli.ts:424-462`; `src/mcp-server.ts:57-78`; `packages/mcp-server/README.md:1-12`; `docker/README.md:1-4`).
