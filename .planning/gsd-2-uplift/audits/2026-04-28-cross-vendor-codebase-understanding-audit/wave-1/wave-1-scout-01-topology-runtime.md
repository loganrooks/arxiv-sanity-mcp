---
type: wave-1-scout-output
date: 2026-04-28
scout: Scout 01 topology-runtime
reasoning_effort: medium
status: complete
---

# Wave 1 Scout 01 — Topology / Runtime

## 0. Scout Summary

- Source target is a clean `main...origin/main` checkout at `/home/rookslog/workspace/projects/gsd-2-explore`; I treated it as read-only.
- Source-derived: the npm workspace root is `gsd-pi`, with `packages/*`, `studio`, and `extensions/*` workspaces and root `gsd`/`gsd-cli` bins pointing to `dist/loader.js` (`package.json:2`, `package.json:15-24`).
- Source-derived: current package tree has `daemon`, `mcp-server`, `native`, `pi-agent-core`, `pi-ai`, `pi-coding-agent`, `pi-tui`, and `rpc-client`; I did not find `packages/gsd-agent-core` or `packages/gsd-agent-modes` in the current tree.
- Source-derived: CLI/runtime activation is split across `src/loader.ts` and `src/cli.ts`; the loader sets Pi/GSD environment variables before dynamic-importing the CLI (`src/loader.ts:79-90`, `src/loader.ts:109-119`).
- Source-derived: runtime surfaces are plural: interactive TUI, print/text/json, `--mode rpc`, `--mode mcp`, web mode, `headless`, `auto` shorthand, standalone MCP package, standalone RPC client package, and daemon package (`src/cli.ts:76-90`, `src/cli.ts:424-462`, `src/cli.ts:685-720`; `packages/mcp-server/package.json:28-30`; `packages/rpc-client/package.json:20-27`; `packages/daemon/package.json:23-25`).
- Source-derived: `gsd headless` is not merely a docs label; it has a dedicated orchestrator that spawns/uses RPC mode, parses headless flags, and auto-responds to extension UI requests (`src/headless.ts:1-7`, `src/headless.ts:66-84`, `src/headless.ts:147-220`).
- Source-derived/docs-confirmed: Pi relationship is vendored and modified. Pi package descriptions say "vendored from pi-mono" (`packages/pi-coding-agent/package.json:2-5`; `packages/pi-agent-core/package.json:1-4`), and ADR-010 states vendored Pi source plus substantial GSD-authored logic inside `pi-coding-agent` (`docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`).
- Source-derived/docs-divergence candidate: RTK is provisioned and path/telemetry env is applied broadly, but runtime bootstrap in `src/cli.ts` says RTK is opt-in via `preferences.experimental.rtk`; README language reads more activated-by-default than the source branch I inspected (`README.md:22`; `src/cli.ts:160-178`; `src/rtk-shared.ts:70-73`).
- Current architecture output and audit appear mechanically accurate on the simple topology/runtime claims I checked. Claims about what this means for intervention strategy remain synthesis/adjudication work, not scout work.

## 1. Source Paths Inspected

- `/home/rookslog/workspace/projects/gsd-2-explore/package.json` - workspace root identity, bins, build scripts, dependencies, `piConfig`.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/*/package.json` - package identities, vendored package descriptions, linkable package metadata, package-level bins.
- `/home/rookslog/workspace/projects/gsd-2-explore/src/loader.ts` - startup loader, `PI_PACKAGE_DIR`, `GSD_CODING_AGENT_DIR`, RTK env application, workspace package linking.
- `/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts` - primary runtime router for graph, web, headless, auto, print, RPC, MCP, and interactive branches.
- `/home/rookslog/workspace/projects/gsd-2-explore/src/headless.ts` and nearby `headless-*` files - headless orchestrator shape and flags.
- `/home/rookslog/workspace/projects/gsd-2-explore/src/mcp-server.ts` - in-process MCP transport used by `gsd --mode mcp`.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/mcp-server/src/cli.ts` and `packages/mcp-server/README.md` - standalone stdio MCP server package.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/rpc-client/README.md` and `packages/rpc-client/src/index.ts` - standalone RPC client surface.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/main.ts`, `src/modes/index.ts`, and `src/core/agent-session.ts` - Pi coding-agent entrypoint, mode exports, shared AgentSession abstraction.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/config.ts` - Pi package-dir override behavior.
- `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/core/extensions/loader.ts` - aliasing between `@gsd/pi-*` and original `@mariozechner/pi-*` package specifiers.
- `/home/rookslog/workspace/projects/gsd-2-explore/docs/dev/ADR-010-pi-clean-seam-architecture.md` - docs-derived proposed clean-seam structure and current vendoring diagnosis.
- `/home/rookslog/workspace/projects/gsd-2-explore/README.md` and selected docs under `docs/`, `gitbook/`, and `mintlify-docs/` - docs/runtime language, with attention to RTK/headless/MCP/RPC claims.
- Current artifacts read after source-first pass: `.planning/gsd-2-uplift/exploration/02-architecture-output.md`, `.planning/gsd-2-uplift/exploration/02-architecture-audit.md`, and relevant topology/runtime sections of `.planning/gsd-2-uplift/exploration/SYNTHESIS.md`.

## 2. Source-First Topology Map

Source-derived package/layout map:

```text
gsd-2-explore/
  package.json
    npm workspace root named gsd-pi; workspaces packages/*, studio, extensions/*.
    bins: gsd, gsd-cli -> dist/loader.js; gsd-pi -> scripts/install.js.
  src/
    loader.ts       startup gate, env setup, package linking, dynamic import of cli.ts
    cli.ts          runtime router for graph/web/headless/auto/print/RPC/MCP/interactive
    headless*.ts    headless orchestrator, query, context, UI, event, answer surfaces
    mcp-server.ts   in-process MCP server for active session tools
    resources/      bundled GSD extensions, skills, workflow resources
  packages/
    pi-agent-core/      vendored Pi core agent loop/types
    pi-ai/              vendored Pi LLM/provider layer
    pi-tui/             vendored Pi terminal UI
    pi-coding-agent/    vendored Pi coding-agent package with modes, session, tools, extension runtime
    native/             TS package for native engine bindings
    rpc-client/         standalone @gsd-build/rpc-client package
    mcp-server/         standalone @gsd-build/mcp-server package
    daemon/             background daemon package using rpc-client
  native/               Rust workspace/build support for native engine
  web/                  Next.js web UI
  studio/               Electron/Vite studio app
  vscode-extension/     VS Code extension
  docs/, gitbook/, mintlify-docs/
  docker/, scripts/, gsd-orchestrator/
```

Source-derived entrypoint map:

- Root package exposes `gsd` and `gsd-cli` as `dist/loader.js`, and `gsd-pi` as `scripts/install.js` (`package.json:20-24`).
- `loader.ts` handles fast `--version`/`--help`, validates runtime prerequisites, sets `PI_PACKAGE_DIR`, `GSD_CODING_AGENT_DIR`, `GSD_PKG_ROOT`, `GSD_VERSION`, `GSD_BIN_PATH`, `GSD_WORKFLOW_PATH`, and `GSD_BUNDLED_EXTENSION_PATHS`, then dynamic-imports CLI code after env setup (`src/loader.ts:7-30`, `src/loader.ts:86-90`, `src/loader.ts:109-119`, `src/loader.ts:135-164`).
- `loader.ts` discovers `packages/*/package.json` entries with `gsd.linkable === true` and symlinks/copies them into `node_modules` under declared `scope`/`name` (`src/loader.ts:174-203`, `src/loader.ts:205-218`).
- `src/cli.ts` imports/dynamically imports `@gsd/pi-coding-agent` and assembles GSD runtime behavior around it (`src/cli.ts:1-6`, `src/cli.ts:34-40`, `src/cli.ts:491-501`).
- `packages/pi-coding-agent/src/main.ts` remains a Pi coding-agent CLI entrypoint that calls `main(process.argv.slice(2))` after provider setup (`packages/pi-coding-agent/src/main.ts:1-18`).

Source-derived runtime surface map:

- Interactive TUI: after setup, `src/cli.ts` constructs session/resource/model state and enters interactive mode (`src/cli.ts:753-820`).
- Print/text/json/RPC/MCP branch: `isPrintMode` is true for `--print` or any explicit `--mode`; it creates a session, then routes `mode === "rpc"` to `runRpcMode`, `mode === "mcp"` to `startMcpServer`, otherwise to `runPrintMode` (`src/cli.ts:143-145`, `src/cli.ts:621-720`).
- Headless branch: `gsd headless` initializes resources and calls `runHeadless(parseHeadlessArgs(process.argv))`; `gsd auto` is a shorthand for headless auto (`src/cli.ts:424-462`).
- Headless implementation: `src/headless.ts` describes the orchestrator as running `/gsd` subcommands by spawning a child process in RPC mode, auto-responding to extension UI, and streaming progress; it exposes flags for timeout, JSON/output format, model, context, auto, answers, supervised mode, resume, and bare mode (`src/headless.ts:1-7`, `src/headless.ts:66-84`, `src/headless.ts:147-220`).
- In-process MCP: `gsd --mode mcp` activates every registered tool before serving and calls `startMcpServer({ tools: session.agent.state.tools ?? [] })` (`src/cli.ts:693-710`); `src/mcp-server.ts` registers `tools/list` and `tools/call` over stdio (`src/mcp-server.ts:57-78`, `src/mcp-server.ts:96-178`).
- Standalone MCP package: `@gsd-build/mcp-server` exposes `gsd-mcp-server` (`packages/mcp-server/package.json:28-30`) and README says it exposes session/read tools, interactive tools, and headless-safe workflow tools (`packages/mcp-server/README.md:1-12`).
- RPC package: `@gsd-build/rpc-client` exports a standalone client SDK for spawning the agent process, v2 handshake, prompt/steer/follow-up, and event consumption (`packages/rpc-client/README.md:1-29`, `packages/rpc-client/src/index.ts:1-10`).
- Daemon package: `@gsd-build/daemon` exposes `gsd-daemon` and depends on `@gsd-build/rpc-client`, suggesting another runtime integration surface but not one I deeply inspected (`packages/daemon/package.json:23-35`).

Docs-derived / source-checked Pi relationship:

- Package descriptions for `@gsd/pi-agent-core`, `@gsd/pi-ai`, `@gsd/pi-tui`, and `@gsd/pi-coding-agent` explicitly say "vendored from pi-mono" (`packages/pi-agent-core/package.json:1-4`; `packages/pi-ai/package.json:1-4`; `packages/pi-tui/package.json:1-4`; `packages/pi-coding-agent/package.json:1-5`).
- ADR-010 states GSD vendors four Pi packages by copying source into `/packages/`, chose vendoring to modify upstream packages freely, and has substantial GSD-authored logic mixed into `pi-coding-agent` with no reliable distinction short of individual reading (`docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`).
- ADR-010 proposes new `gsd-agent-core/` and `gsd-agent-modes/` packages, but current `packages/` listing does not include those names (`docs/dev/ADR-010-pi-clean-seam-architecture.md:43-57`; source directory listing).
- Pi config/rebranding uses an environment override: `loader.ts` sets `PI_PACKAGE_DIR` before importing the Pi SDK (`src/loader.ts:86-90`), and `packages/pi-coding-agent/src/config.ts` honors `process.env.PI_PACKAGE_DIR` in package-dir resolution (`packages/pi-coding-agent/src/config.ts:82-91`).
- Extension loader aliases both `@gsd/pi-*` and `@mariozechner/pi-*` to bundled/vendored modules, which is a coupling/compatibility surface for Pi-ecosystem extensions (`packages/pi-coding-agent/src/core/extensions/loader.ts:61-91`, `packages/pi-coding-agent/src/core/extensions/loader.ts:325-342`).

Docs/source divergence candidates:

- RTK: README says GSD provisions managed RTK "to compress shell-command output" and `GSD_RTK_DISABLED=1` disables it (`README.md:22`). Source applies RTK path/telemetry env in loader (`src/loader.ts:117-119`) and shared helper (`src/rtk-shared.ts:70-73`), but runtime bootstrap explicitly says RTK is opt-in via `experimental.rtk` and sets `GSD_RTK_DISABLED=1` when the preference is not true (`src/cli.ts:160-178`). This is a real candidate divergence or at least a provisioning-vs-activation ambiguity.
- Headless exit-code docs may deserve a later precise check: `src/headless.ts` declares exit codes `0`, `1`, `10`, `11` (`src/headless.ts:8-12`), while README text I saw says structured codes `0`, `1`, `2` (`README.md:438`). I did not adjudicate whether README is stale, simplified, or referring to older behavior.

## 3. Simple Claims Confirmed / Refuted

| Claim | Current artifact source | Source evidence | Scout verdict | Needs high adjudication? |
|---|---|---|---|---|
| `gsd-2` is a vendored modified Pi fork. | `02-architecture-output.md:85-101`; `02-architecture-audit.md:116-137`; `SYNTHESIS.md:83-88` | Pi package descriptions say "vendored from pi-mono" (`packages/pi-coding-agent/package.json:2-5`; `packages/pi-agent-core/package.json:1-4`). ADR-010 says source is copied into `/packages/` and modified with GSD-authored logic inside `pi-coding-agent` (`docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`). | Mechanically confirmed at scout level, with "modified" grounded mainly in ADR-010 plus current package layout. | Yes, for implications of "fork" vs "vendored packages plus GSD layer"; no, for basic vendoring fact. |
| ADR-010 proposes a clean seam that is not implemented. | `02-architecture-output.md:101`; `02-architecture-audit.md:34-40`; `SYNTHESIS.md:33-34` | ADR-010 status is Proposed (`docs/dev/ADR-010-pi-clean-seam-architecture.md:1-4`) and proposes `gsd-agent-core/` and `gsd-agent-modes/` (`docs/dev/ADR-010-pi-clean-seam-architecture.md:43-57`). Current `packages/` listing lacks those packages. | Confirmed mechanically. | No for package absence/status; yes for how much of the seam is partially approximated elsewhere. |
| There is no `gsd-agent-core` or `gsd-agent-modes` package. | `02-architecture-audit.md:34-40`; `SYNTHESIS.md:33-34` | `find ... -name package.json` returned package.json files for `daemon`, `mcp-server`, `native`, `pi-agent-core`, `pi-ai`, `pi-coding-agent`, `pi-tui`, `rpc-client`, but none for `gsd-agent-core` or `gsd-agent-modes`; `ls packages` likewise did not include them. | Confirmed in current source tree. | No. |
| CLI/headless/MCP/RPC are distinct runtime surfaces. | `02-architecture-output.md:79`, `02-architecture-output.md:194-196`; `SYNTHESIS.md:47-48` | `src/cli.ts` routes `headless` separately (`src/cli.ts:424-433`), `auto` to headless (`src/cli.ts:457-462`), `--mode rpc` to `runRpcMode` (`src/cli.ts:685-690`), and `--mode mcp` to `startMcpServer` (`src/cli.ts:693-712`). Standalone MCP/RPC packages also exist (`packages/mcp-server/package.json:28-30`; `packages/rpc-client/package.json:20-27`). | Confirmed. | Low; high adjudication only if deciding which surface is load-bearing for uplift. |
| RTK is docs-present but source-gated. | `02-architecture-output.md:77`, `02-architecture-output.md:232-234`; `02-architecture-audit.md:42-50`; `SYNTHESIS.md:41` | README says RTK is provisioned to compress shell output (`README.md:22`). `src/cli.ts` says RTK is opt-in via `experimental.rtk`; default disabled; sets `GSD_RTK_DISABLED=1` when not enabled (`src/cli.ts:160-178`). | Confirmed as a real source/docs tension or provisioning-vs-activation ambiguity. | Yes, if downstream work depends on RTK default behavior. |
| README/docs overstate runtime defaults compared to source. | `SYNTHESIS.md:117-121`; `02-architecture-output.md:232-236` | RTK is the strongest checked example. Possible headless exit-code mismatch: source declares `0/1/10/11` (`src/headless.ts:8-12`) while README says `0/1/2` (`README.md:438`). I did not exhaustively validate the broader docs-vs-source class. | Partially confirmed for RTK; candidate additional mismatch for headless exit codes. | Yes, for the recurring-class claim beyond these instances. |
| There is an in-process MCP mode plus a standalone MCP package. | `02-architecture-output.md:194`; `02-architecture-audit.md:52-58`; `SYNTHESIS.md:47-48` | `src/cli.ts` calls `startMcpServer` for `mode === "mcp"` (`src/cli.ts:693-710`); `src/mcp-server.ts` implements stdio MCP for active tools (`src/mcp-server.ts:57-78`, `src/mcp-server.ts:96-178`). `@gsd-build/mcp-server` exposes `gsd-mcp-server` and its own tool surfaces (`packages/mcp-server/package.json:28-30`; `packages/mcp-server/README.md:1-12`). | Confirmed. | No for existence; yes for contract equivalence/differences. |
| The `gsd.linkable` convention ties workspace packages to runtime module resolution. | `02-architecture-audit.md:72-77`, `02-architecture-audit.md:147-151`; `SYNTHESIS.md:86` | `loader.ts` scans `packages/*/package.json`, requires `gsd.linkable === true`, then symlinks/copies packages into scoped `node_modules` names (`src/loader.ts:174-218`). Pi packages and build packages declare `gsd.linkable` in package metadata (`packages/pi-coding-agent/package.json:6-10`; `packages/mcp-server/package.json:6-10`). | Confirmed. | No for mechanism; yes for its strategic meaning. |

## 4. Claims Needing High Adjudication

1. **How to phrase "vendored modified Pi fork" without overcollapsing layers.** Load-bearing because it shapes R1/R2/R3/R4 strategy. Inspect `docs/dev/ADR-010-pi-clean-seam-architecture.md`, `packages/pi-coding-agent/src/`, root `src/`, and extension resources. Non-mechanical because "fork" can mean source topology, governance posture, or practical maintenance burden.

2. **Whether current source has any partial clean seam despite missing ADR-010 packages.** Load-bearing because uplift could target an existing informal seam even if ADR-010 is not implemented. Inspect `src/cli.ts`, `src/resources/extensions/gsd/`, `packages/pi-coding-agent/src/core/sdk.ts`, and extension APIs. Non-mechanical because absence of packages does not prove absence of stable boundaries.

3. **Which MCP surface is relevant to downstream uplift: in-process `--mode mcp` or standalone `@gsd-build/mcp-server`.** Load-bearing because they expose different tool populations and startup/session models. Inspect `src/mcp-server.ts`, `packages/mcp-server/src/server.ts`, `packages/mcp-server/src/workflow-tools.ts`, and `packages/mcp-server/README.md`. Non-mechanical because "MCP support" is plural.

4. **Whether RPC/headless is a better orchestration seam than extension APIs for some uplift work.** Load-bearing because headless uses RPC and supports automation flags; R4-vs-R2 mapping depends on it. Inspect `src/headless.ts`, `src/headless-query.ts`, `packages/rpc-client/src/`, and workflow/plugin callers. Non-mechanical because it depends on workload shape, not just existence of APIs.

5. **RTK documentation interpretation: provisioning claim vs activation claim.** Load-bearing if runtime performance/compression assumptions enter the uplift plan. Inspect `README.md`, `scripts/install.js`, `src/cli.ts`, `src/rtk.ts`, `src/rtk-shared.ts`, and preference schema/tests. Non-mechanical because README may be describing installed availability while source describes runtime activation.

6. **Headless exit-code docs/source mismatch candidate.** Load-bearing for CI/orchestration users if they branch on blocked/cancelled codes. Inspect `src/headless.ts`, `src/headless-events.ts`, `docs/user-docs/commands.md`, `README.md`, and tests. Non-mechanical until all docs and historical behavior are checked.

7. **Stability of Pi extension aliases for external Pi ecosystem compatibility.** Load-bearing for an R2 strategy that hopes to write upstream-Pi-compatible extensions. Inspect `packages/pi-coding-agent/src/core/extensions/loader.ts`, extension validator docs/tests, and package exports. Non-mechanical because alias existence does not guarantee behavioral equivalence with upstream Pi.

8. **Whether `daemon`, `web`, `studio`, and VS Code extension are peripheral or meaningful runtime surfaces.** Load-bearing if "runtime topology" is used to decide integration points beyond CLI/headless/MCP/RPC. Inspect each package/app entrypoint and docs. Non-mechanical because centrality depends on actual use, not package presence.

## 5. Suspected Omissions or Conflations

- **MCP conflation risk:** "MCP" can mean root in-process `gsd --mode mcp`, standalone `@gsd-build/mcp-server`, or MCP client functionality inside bundled extensions. The current architecture output distinguishes the first two; later synthesis should keep them separate.
- **RPC conflation risk:** root `--mode rpc`, `@gsd-build/rpc-client`, and `headless` are connected but not identical. Headless is an orchestrator using RPC; rpc-client is an external SDK; `runRpcMode` is the internal server mode.
- **Pi/GSD package-boundary risk:** package names under `@gsd/pi-*` can sound like clean GSD-owned abstractions, but package descriptions and ADR-010 identify them as vendored Pi-derived packages.
- **Clean-seam status risk:** ADR-010's proposed package names are easy to carry forward as if implemented. Current source tree does not have those packages.
- **RTK default risk:** README language can be read as "enabled by default"; source says runtime compression is preference-gated. Treat RTK behavior as source-verified per active release, not README-inferred.
- **Docs-runtime exit-code risk:** headless exit codes may have stale docs. The scout found enough to nominate this, not enough to fully audit every doc surface.
- **Runtime root/rebrand subtlety:** `PI_PACKAGE_DIR` points to a shim/package-dir path and Pi config code honors the env override. This suggests rebranding uses an intended Pi package-dir hook, not only ad hoc GSD patching.
- **Daemon/app surfaces under-covered:** current topology/runtime discussions emphasize CLI/headless/MCP/RPC; `daemon`, `web`, `studio`, and VS Code extension exist but were only lightly mapped here.

## 6. Scope Boundaries

- I did not build or run the gsd-2 source target.
- I did not inspect detailed workflow plugin internals beyond source paths that surfaced runtime topology.
- I did not perform file-by-file provenance mapping of `pi-coding-agent`.
- I did not audit every docs/source divergence, only obvious topology/runtime candidates.
- I did not adjudicate R-strategy or product-fit implications.
- I did not inspect external Pi or RTK repositories.
- I did not modify the source target.
- I did not write any file other than this assigned scout output.

## 7. Scout Caveat

This is a medium-reasoning source scout. It locates surfaces and nominates claims; it does not establish a complete replacement model of `gsd-2`.

## Source Freshness Addendum — 2026-04-28

Provisional delta note for `82bcf6b71..bf1d8aad0`: the broad topology/runtime map above remains usable, but two runtime details are fresher on `origin/main`.

- `gsd auto` is no longer accurately summarized as an unconditional shorthand for headless. In `bf1d8aad0`, `src/cli.ts:458-462` redirects through `shouldRedirectAutoToHeadless(...)`, and `src/cli-auto-routing.ts:1-8` makes that redirect conditional on subcommand `auto` plus non-TTY stdin or stdout.
- `AgentSession` session transition behavior changed inside the already-identified shared runtime abstraction. `bf1d8aad0:packages/pi-coding-agent/src/core/agent-session.ts:1608-1630` waits instead of aborting when a session transition starts during `agent_end`, while preserving abort-before-disconnect for normal transitions.

Delta judgment: addendum enough; no full Scout 01 rerun is recommended from this range alone unless downstream work depends specifically on auto-mode foreground ownership or `AgentSession.newSession()` handoff semantics.
