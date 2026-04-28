---
type: wave-2-adjudication
date: 2026-04-28
adjudicator: topology-runtime
reasoning_effort: high
status: complete
---

# Wave 2 Adjudication 01 — Topology / Runtime

## 0. Adjudication Summary

Current Claude investigation remains usable for topology/runtime, with localized qualifications. The major source-backed claims survive: Pi packages are vendored and modified, ADR-010's clean seam is proposed-not-implemented, MCP/RPC/headless are distinct surfaces, and RTK/headless docs have real source tensions. The main correction is boundary discipline: "vendored modified Pi fork" is acceptable shorthand only if it does not erase the root GSD CLI/glue layer, bundled GSD extension layer, standalone MCP/RPC packages, web/VS Code/daemon surfaces, and partial informal seams.

Severity stratification: high for ADR-010 clean-seam status because it affects intervention strategy; medium for MCP/RPC/headless distinctions and omitted runtime surfaces; low-to-medium for RTK and headless exit-code mismatches unless downstream orchestration depends on them.

## 1. Claim Verdict Table

| Claim family | Verdict | Severity | Confidence | One-line reason |
|---|---|---|---|---|
| Vendored modified Pi fork: correct phrasing and boundaries | Survives with qualification | medium | high | Vendoring and modification are source/ADR-backed, but "fork" overcollapses GSD root, extension, and standalone integration layers if used as the whole topology. |
| ADR-010 clean seam: proposed-not-implemented, plus partial seams | Survives with qualification | high | high | The ADR-010 package seam is absent, while current source still has informal module, extension, loader, and runtime seams. |
| MCP/RPC/headless topology | Survives with qualification | medium | high | In-process MCP, standalone MCP, RPC mode/client, headless, and TTY-gated `auto` are distinct but connected. |
| RTK docs/source divergence | Survives with qualification | low | high | The exact allowed claim is provisioning-vs-activation ambiguity: README overreads as active by default, while source and preferences make runtime use opt-in. |
| Headless exit-code docs/source mismatch | Survives | low | high | Source uses `0/1/10/11`; README/user docs still say `0/1/2`. Material only for scripts/CI that branch on blocked/cancelled codes. |
| Peripheral vs relevant runtime surfaces | Survives with qualification | medium | medium-high | `web`, VS Code, and `daemon` are relevant runtime/integration surfaces; `studio` appears prototype-level from inspected evidence. Omission is acceptable only for narrow CLI/headless/MCP/RPC claims. |

## 2. Detailed Adjudication

### 2.1 Vendored modified Pi fork: correct phrasing and boundaries

- Claim under audit: `gsd-2` is a "vendored modified Pi fork."
- Current artifact evidence: Slice 2 says `gsd-2` vendors four Pi-derived packages under `@gsd` and is not a clean external Pi dependency (`.planning/gsd-2-uplift/exploration/02-architecture-output.md:83-101`). The audit verifies ADR-010 vendoring and `pi-coding-agent` package descriptions (`.planning/gsd-2-uplift/exploration/02-architecture-audit.md:26-40`, `.planning/gsd-2-uplift/exploration/02-architecture-audit.md:60-66`). Synthesis turns this into a "vendored modified Pi fork" pattern (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:83-88`).
- Source evidence inspected: Root package is `gsd-pi`, with workspace members `packages/*`, `studio`, and `extensions/*`, plus `gsd`/`gsd-cli` bins (`/home/rookslog/workspace/projects/gsd-2-explore/package.json:1-24`). Four Pi packages explicitly say "vendored from pi-mono" (`/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-agent-core/package.json:1-10`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-ai/package.json:1-10`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-tui/package.json:1-10`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/package.json:1-14`). ADR-010 says GSD copied four Pi packages into `/packages/`, chose vendoring to modify upstream packages freely, and has substantial GSD-authored logic inside `pi-coding-agent` (`/home/rookslog/workspace/projects/gsd-2-explore/docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`).
- Reasoning: The phrase is accurate as a compressed description of the Pi-derived package substrate. "Modified" is source-backed mainly by ADR-010's diagnosis and current package structure, not by a file-by-file provenance map. "Fork" is a useful maintenance/topology term, but it is not precise enough for the whole system because root `src/cli.ts`, loader/env setup, bundled GSD resources, standalone MCP/RPC packages, web mode, and other apps are not simply "the Pi fork."
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: high.
- Downstream correction or qualification: Use: "gsd-2 is a GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled, but the whole repo is broader than that fork."

### 2.2 ADR-010 clean seam: proposed-not-implemented, plus partial seams

- Claim under audit: ADR-010's clean seam is proposed-not-implemented; `gsd-agent-core` and `gsd-agent-modes` are absent; check whether partial seams qualify "no clean seam."
- Current artifact evidence: Scout 01 confirms ADR-010 status and package absence while nominating partial seam adjudication (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:108-122`). Gate 1 identifies this as a Wave 2 claim family (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-1-DISPOSITION.md:115-120`). Synthesis treats clean seam as proposed-not-implemented (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:33-34`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:127-128`).
- Source evidence inspected: ADR-010 status is `Proposed` (`/home/rookslog/workspace/projects/gsd-2-explore/docs/dev/ADR-010-pi-clean-seam-architecture.md:1-4`), and it proposes new `gsd-agent-core/` and `gsd-agent-modes/` packages (`/home/rookslog/workspace/projects/gsd-2-explore/docs/dev/ADR-010-pi-clean-seam-architecture.md:43-57`). Current `packages/` contains `daemon`, `mcp-server`, `native`, `pi-agent-core`, `pi-ai`, `pi-coding-agent`, `pi-tui`, and `rpc-client`, with no `gsd-agent-core` or `gsd-agent-modes` directories. The loader sets `PI_PACKAGE_DIR`, GSD paths, bundled extension paths, and links packages via `gsd.linkable` (`/home/rookslog/workspace/projects/gsd-2-explore/src/loader.ts:79-90`, `/home/rookslog/workspace/projects/gsd-2-explore/src/loader.ts:109-119`, `/home/rookslog/workspace/projects/gsd-2-explore/src/loader.ts:174-220`). `@gsd/pi-coding-agent` exports public session, extension, resource loader, and SDK surfaces (`/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/index.ts:1-15`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/index.ts:50-169`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/pi-coding-agent/src/index.ts:190-212`).
- Reasoning: "No clean seam" is true for the specific ADR-010 package seam. It is false if read as "no seams of any kind." Current source has partial/informal seams: loader/CLI split, environment-based Pi rebranding, linkable package convention, the Pi extension API, exported SDK/session APIs, standalone MCP/RPC packages, and bundled GSD extension boundaries. These seams are real but do not deliver ADR-010's promised dependency inversion and provenance separation.
- Verdict: Survives with qualification.
- Severity: high.
- Confidence: high.
- Downstream correction or qualification: Downstream synthesis should say "ADR-010's clean GSD-vs-Pi package seam is not implemented; existing informal runtime and extension seams exist but do not solve the provenance/entanglement problem ADR-010 names."

### 2.3 MCP/RPC/headless topology

- Claim under audit: In-process MCP, standalone MCP package, RPC mode/client, headless, daemon, and `auto` routing must be distinguished; check current synthesis for conflation and preserve the `gsd auto` freshness addendum.
- Current artifact evidence: Scout 01 distinguishes runtime surfaces and warns about MCP/RPC conflation (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:80-90`, `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:135-144`). The freshness delta corrects `gsd auto` to TTY-gated redirect only (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:75-81`). Synthesis says the agent-runtime contract is plural and names CLI/TUI, in-process MCP, standalone MCP, RPC client, and hooks (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:47-48`).
- Source evidence inspected: `src/cli.ts` routes `headless` as its own subcommand (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts:425-435`), routes `auto` to headless only through `shouldRedirectAutoToHeadless(...)` (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts:458-463`), and that function returns true only for subcommand `auto` with non-TTY stdin or stdout (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli-auto-routing.ts:1-8`). Print mode routes `--mode rpc` to `runRpcMode` and `--mode mcp` to `startMcpServer` (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts:619-721`). `src/mcp-server.ts` exposes active session tools over stdio (`/home/rookslog/workspace/projects/gsd-2-explore/src/mcp-server.ts:57-78`, `/home/rookslog/workspace/projects/gsd-2-explore/src/mcp-server.ts:96-178`). The standalone MCP package exposes `gsd-mcp-server` and a broader orchestration/workflow/read tool surface (`/home/rookslog/workspace/projects/gsd-2-explore/packages/mcp-server/package.json:1-30`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/mcp-server/README.md:1-12`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/mcp-server/README.md:76-127`). The RPC client package is a standalone SDK for spawning an agent process and consuming typed events (`/home/rookslog/workspace/projects/gsd-2-explore/packages/rpc-client/README.md:1-29`, `/home/rookslog/workspace/projects/gsd-2-explore/packages/rpc-client/README.md:48-103`).
- Reasoning: Current source strongly supports the scout's distinction. Headless is an orchestrator that uses RPC, not the same thing as RPC mode or the RPC client package (`/home/rookslog/workspace/projects/gsd-2-explore/src/headless.ts:1-13`, `/home/rookslog/workspace/projects/gsd-2-explore/src/headless.ts:147-231`). In-process MCP and standalone MCP both use stdio MCP but expose different populations and startup/session models. `auto` is not unconditional headless shorthand on current `origin/main`; it stays interactive when stdin/stdout are TTYs.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: high.
- Downstream correction or qualification: Keep three separate labels: "in-process MCP mode (`gsd --mode mcp`)", "standalone `@gsd-build/mcp-server` orchestration server", and "RPC/headless orchestration (`--mode rpc`, `@gsd-build/rpc-client`, `gsd headless`)"; add that `gsd auto` is TTY-gated.

### 2.4 RTK docs/source divergence

- Claim under audit: RTK docs/source divergence: true divergence or provisioning-vs-activation distinction; decide exact downstream claim.
- Current artifact evidence: Slice 2 flags RTK as a managed external binary whose runtime use is gated by `experimental.rtk` (`.planning/gsd-2-uplift/exploration/02-architecture-output.md:77-78`, `.planning/gsd-2-uplift/exploration/02-architecture-output.md:232-235`). The slice audit verifies a README/source tension and explicitly notes the provisioning-vs-activation nuance (`.planning/gsd-2-uplift/exploration/02-architecture-audit.md:42-51`). Synthesis treats RTK as a concrete docs-vs-source divergence and representative of docs/source drift (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:41-42`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:388-396`).
- Source evidence inspected: README says GSD provisions managed RTK to compress shell-command output and `GSD_RTK_DISABLED=1` disables the integration (`/home/rookslog/workspace/projects/gsd-2-explore/README.md:20-24`). The install script provisions/skips RTK via install-time flags/env and declares RTK version/repo (`/home/rookslog/workspace/projects/gsd-2-explore/scripts/install.js:153-164`, `/home/rookslog/workspace/projects/gsd-2-explore/scripts/install.js:268-403`). Loader broadly applies RTK path/telemetry env (`/home/rookslog/workspace/projects/gsd-2-explore/src/loader.ts:117-119`). Runtime bootstrap says RTK is opt-in via `experimental.rtk` and sets `GSD_RTK_DISABLED=1` when not enabled (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts:161-199`). Preferences docs say experimental features are off by default and `rtk` default is false/opt-in (`/home/rookslog/workspace/projects/gsd-2-explore/src/resources/extensions/gsd/docs/preferences-reference.md:279-280`, `/home/rookslog/workspace/projects/gsd-2-explore/src/resources/extensions/gsd/docs/preferences-reference.md:696-704`).
- Reasoning: The strongest exact claim is not "all docs contradict source." It is: the README can be read as activation-by-default, while current source and preferences docs distinguish provisioning/path setup from runtime activation. That is a real docs/source tension at the README level and a provisioning-vs-activation distinction at the system level.
- Verdict: Survives with qualification.
- Severity: low.
- Confidence: high.
- Downstream correction or qualification: Downstream synthesis may say "RTK is provisioned/available broadly, but runtime compression is opt-in via `experimental.rtk`; README language overstates or compresses that distinction."

### 2.5 Headless exit-code docs/source mismatch

- Claim under audit: Candidate mismatch between headless source exit codes and docs; decide whether real and material.
- Current artifact evidence: Scout 01 identifies source `0/1/10/11` versus README `0/1/2` as a candidate mismatch needing precise check (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:99-103`, `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:127-130`). Synthesis references headless exit codes as `0/1/10/11` for R4 orchestration evidence (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:206-208`).
- Source evidence inspected: `src/headless.ts` documents exit codes `0`, `1`, `10`, and `11` (`/home/rookslog/workspace/projects/gsd-2-explore/src/headless.ts:1-13`). `src/headless-events.ts` defines `EXIT_SUCCESS = 0`, `EXIT_ERROR = 1`, `EXIT_BLOCKED = 10`, `EXIT_CANCELLED = 11`, and maps statuses accordingly (`/home/rookslog/workspace/projects/gsd-2-explore/src/headless-events.ts:10-48`). README still says `0` complete, `1` error/timeout, `2` blocked (`/home/rookslog/workspace/projects/gsd-2-explore/README.md:425-438`). User commands docs also say `2` blocked (`/home/rookslog/workspace/projects/gsd-2-explore/docs/user-docs/commands.md:279-321`), and GitBook headless docs repeat `2` blocked (`/home/rookslog/workspace/projects/gsd-2-explore/gitbook/features/headless.md:49-56`).
- Reasoning: The mismatch is real in current source/docs. It is not material to broad package topology, but it is material to machine-facing orchestration claims because scripts and CI may branch on blocked/cancelled status. It also reinforces the docs/source verification discipline from the synthesis.
- Verdict: Survives.
- Severity: low.
- Confidence: high.
- Downstream correction or qualification: Use source codes `0/1/10/11` for orchestration claims. Treat README/user docs `2` blocked as stale until proven otherwise.

### 2.6 Peripheral vs relevant runtime surfaces

- Claim under audit: Are `daemon`, `web`, `studio`, and VS Code extension merely peripheral, or should current synthesis/topology claims qualify their omission?
- Current artifact evidence: Scout 01 lists `daemon`, `web`, `studio`, and VS Code as under-covered runtime surfaces (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:40-70`, `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-1/wave-1-scout-01-topology-runtime.md:131-144`). Gate 1 makes this an adjudication claim family (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-1-DISPOSITION.md:115-120`). Synthesis F7 names plural agent-runtime contracts but omits web, studio, daemon, and VS Code in the top-line list (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:47-48`).
- Source evidence inspected: `daemon` is a package with `gsd-daemon` bin, Discord/project-monitoring description, and dependency on `@gsd-build/rpc-client` (`/home/rookslog/workspace/projects/gsd-2-explore/packages/daemon/package.json:1-35`); its CLI supports launchd install/status and normal daemon start (`/home/rookslog/workspace/projects/gsd-2-explore/packages/daemon/src/cli.ts:1-95`). Web mode is routed directly by root CLI (`/home/rookslog/workspace/projects/gsd-2-explore/src/cli.ts:332-356`), has a local server launcher (`/home/rookslog/workspace/projects/gsd-2-explore/src/web-mode.ts:60-88`, `/home/rookslog/workspace/projects/gsd-2-explore/src/web-mode.ts:524-560`), and docs describe project management, real-time progress, and per-project bridge services (`/home/rookslog/workspace/projects/gsd-2-explore/docs/user-docs/web-interface.md:1-44`). VS Code extension package contributes a chat participant, views, many commands, and workspace activation (`/home/rookslog/workspace/projects/gsd-2-explore/vscode-extension/package.json:1-44`, `/home/rookslog/workspace/projects/gsd-2-explore/vscode-extension/package.json:45-233`, `/home/rookslog/workspace/projects/gsd-2-explore/vscode-extension/package.json:334-400`), and its client spawns `gsd --mode rpc` (`/home/rookslog/workspace/projects/gsd-2-explore/vscode-extension/src/gsd-client.ts:79-131`). Studio is an Electron/Vite app with a stubbed preload bridge from inspected source (`/home/rookslog/workspace/projects/gsd-2-explore/studio/package.json:1-31`, `/home/rookslog/workspace/projects/gsd-2-explore/studio/src/main/index.ts:1-39`, `/home/rookslog/workspace/projects/gsd-2-explore/studio/src/preload/index.ts:1-21`).
- Reasoning: `web`, VS Code, and `daemon` are not merely peripheral to runtime topology; they are integration/runtime surfaces layered over CLI/RPC/state. They may be peripheral to a narrow uplift question focused on CLI/headless/MCP/RPC, but a topology claim that says "plural runtime contracts" should at least name them or state the omission. Studio appears less mature from inspected evidence, so it should be flagged as present but not treated as load-bearing without deeper proof.
- Verdict: Survives with qualification.
- Severity: medium.
- Confidence: medium-high.
- Downstream correction or qualification: Add a bounded note: "The primary adjudicated integration seams are CLI/headless/RPC/MCP. Web, VS Code, and daemon are additional runtime/integration surfaces, mostly built on those seams; studio exists but appears prototype-level from inspected source."

## 3. Cross-Domain Flags

- Extension/workflow adjudicator: partial seams matter. The Pi extension API and GSD bundled extension boundaries are real, but they do not equal ADR-010's clean package seam.
- Extension/workflow adjudicator: VS Code and daemon are runtime consumers of RPC-shaped contracts, not separate replacement agent kernels from the evidence inspected here.
- Release/practice adjudicator: RTK and headless exit-code mismatches are concrete docs/source drift examples. They support a source-verification discipline, but this adjudication does not decide whether docs/source drift is a stable release-practice pattern.
- All adjudicators: preserve source freshness. `gsd auto` is TTY-gated in current `bf1d8aad0`; do not carry forward the older unconditional-headless shorthand.

## 4. Limits

- I did not build or run `gsd-2`.
- I did not inspect external Pi or RTK repositories.
- I did not perform file-by-file provenance mapping inside `pi-coding-agent`.
- I did not fully map `daemon`, `web`, `studio`, or VS Code internals; I inspected only enough to judge whether their omission should qualify topology/runtime claims.
- I did not adjudicate release-practice or extension/workflow strategy except where it directly touched topology/runtime boundaries.
- I treated `/home/rookslog/workspace/projects/gsd-2-explore/` as read-only and made no source edits.

## 5. Recommendation For Gate 2

localized qualifications needed
