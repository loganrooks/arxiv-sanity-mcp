---
audit_target: .planning/gsd-2-uplift/exploration/02-architecture-output.md
date: 2026-04-28
auditor: Claude Opus xhigh adversarial-auditor
status: complete
---

# Audit of slice 2 output — architecture

## §0. Audit summary

- **Critical findings:** none.
- **Material findings:** none. The slice's load-bearing claims (vendored Pi packages, ADR-010 status as proposed-not-implemented, in-process MCP mode plus standalone MCP package, RTK opt-in gating, two-file loader, pi-coding-agent as the entanglement nexus) all verify against source.
- **Minor findings:**
  - Several line-range citations are off by 1-2 lines (e.g., `package.json:14-19` for the workspaces block actually starts at line 15; `package-lock.json:1-80` is loose; `package.json:43-45` for engines is actually 43-45 — verified accurate; ranges on multi-section claims tend to be inclusive of nearby comment lines). None mislead a reader who follows the citation.
  - Finding 1.7 lists native modules (`grep/glob/ps/highlight/ast/diff/text/html/image/fd/clipboard/parser/truncation`) drawn from `packages/native/src/index.ts`'s docstring; the actual export surface in that file is broader (xxhash, ttsr, json-parse, stream-process, gsd-parser) and the `native/` Rust workspace has only three crates (ast/engine/grep). The slice's framing co-cites Cargo.toml without reconciling that the Rust workspace has only three crates while the TS wrapper exposes ~14 module groupings. Spirit-correct; not load-bearing.
  - Finding 5.7 cites `package-manager.ts:1635-1718` for skill discovery; the file is large and that range is plausible but I did not spot-check it. Lower-priority claim.
- **Clean:** Q2 (gsd-2 vs Pi SDK) — the load-bearing finding for downstream synthesis — is well-grounded. Findings 2.1, 2.5, 2.7 verify cleanly against `package.json`, ADR-010, and `loader.ts`. The README/source RTK divergence flagged in (v) is a real, concrete tension grounded in a verbatim README quote vs verbatim cli.ts behavior.

**Recommendation:** Clean → proceed (with optional addendum noting the minor citation/scope notes if the synthesis stage wants the higher-precision read).

## §1. Source verification

Five spot-checks against gsd-2 source.

### Spot-check 1: ADR-010 vendoring claim (Finding 2.5)

**Slice claim:** "a gsd-2 ADR says the project vendors Pi packages by copying source into `/packages/`, and that 'substantial original logic' has been written directly inside `pi-coding-agent`, with no reliable way to distinguish GSD files from Pi files without individual reading (`docs/dev/ADR-010-pi-clean-seam-architecture.md:10-30`)."

**Source:** `docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29` says verbatim "GSD vendors four packages from pi-mono ... by copying their source directly into `/packages/`" and "GSD has written substantial original logic directly inside `pi-coding-agent` — approximately 79 files" and "no reliable way to distinguish GSD files from pi files without reading them individually."

**Verdict:** verifiable. Citation accurate; quoted phrasing matches source.

### Spot-check 2: ADR-010 status / proposed seam (direction-shifting evidence)

**Slice claim:** "the proposed seam (`@gsd/agent-core`, `@gsd/agent-modes`) describes a future package structure rather than the current package tree" (paraphrasing direction-shifting bullet and Finding (iv) bullet 1).

**Source:** ADR-010 line 2 says "**Status:** Proposed". Line 47-57 specifies new packages `gsd-agent-core/` and `gsd-agent-modes/`. `ls /packages/` in source returns exactly: `daemon, mcp-server, native, pi-agent-core, pi-ai, pi-coding-agent, pi-tui, rpc-client` — no `gsd-agent-core` or `gsd-agent-modes`.

**Verdict:** verifiable. The "proposed but not implemented" claim is exactly correct and **load-bearing for synthesis**: any downstream plan that assumed the clean-seam refactor was already done would be wrong-shaped.

### Spot-check 3: RTK gating divergence (Finding 1.8 + (v))

**Slice claim:** README at line 22 says GSD provisions managed RTK to compress shell-command output and `GSD_RTK_DISABLED=1` disables it; source at `src/cli.ts:167-176` shows RTK is opt-in via `experimental.rtk` and disabled-by-default unless that preference is true.

**Source:**
- `README.md:22` verbatim: "GSD now provisions a managed [RTK](https://github.com/rtk-ai/rtk) binary on supported macOS, Linux, and Windows installs to compress shell-command output ... GSD forces `RTK_TELEMETRY_DISABLED=1` for all managed invocations. Set `GSD_RTK_DISABLED=1` to disable the integration."
- `src/cli.ts:167-178` verbatim: "RTK is opt-in via experimental.rtk preference. Default: disabled ... if (!rtkEnabled) { process.env[GSD_RTK_DISABLED_ENV] = '1'; rtkDisabled = true }".

**Verdict:** verifiable. README implies on-by-default-except-when-disabled; source implements off-by-default-unless-preference-set. The slice flags this correctly. One nuance the slice surfaces honestly: the README may be describing provisioning, not activation — i.e., the install script does provision the binary (`scripts/install.js:153-164` confirmed: `RTK_VERSION = '0.33.1'`, `RTK_REPO = 'rtk-ai/rtk'`), but the runtime flag does not flip on without `experimental.rtk`. That gap is real.

### Spot-check 4: in-process MCP server (Finding 5.8)

**Slice claim:** "`gsd --mode mcp` starts an in-process MCP server exposing the active session's registered tools over stdin/stdout (`src/cli.ts:693-712`; `src/mcp-server.ts:57-78`, `src/mcp-server.ts:96-178`)."

**Source:** `src/cli.ts:693-713` verbatim contains `if (mode === 'mcp')` branch that calls `startMcpServer({ tools: session.agent.state.tools ?? [], version: ... })`. `src/mcp-server.ts:71-79` defines `startMcpServer` exported function. The in-process MCP path "Activate every registered tool before starting the MCP transport" is verified.

**Verdict:** verifiable. The slice's distinction between in-process MCP mode (in `src/`) and the standalone `@gsd-build/mcp-server` package is accurate and important for synthesis.

### Spot-check 5: vendoring of pi-coding-agent (Finding 2.1)

**Slice claim:** "`@gsd/pi-coding-agent` ... 'vendored from pi-mono' for the Pi packages (`packages/pi-coding-agent/package.json:1-50`)".

**Source:** `packages/pi-coding-agent/package.json:4` verbatim: `"description": "Coding agent CLI (vendored from pi-mono)"`. Same pattern in `packages/pi-agent-core/package.json:4`: `"General-purpose agent core (vendored from pi-mono)"`.

**Verdict:** verifiable. The vendoring claim is concrete (description string, not just inferred), which strengthens its load-bearing-ness.

## §2. Completeness

In-scope diagnostic-question coverage was thorough. A few in-scope items I noticed the slice did not surface that synthesis might want:

- **`piConfig` field at the root (minor).** The root `package.json:39-42` declares `"piConfig": { "name": "gsd", "configDir": ".gsd" }`. The slice does not directly cite this even though it is a load-bearing piece of how GSD rebrands Pi at runtime — the loader's `pkg/` shim is *also* used to set this, and the dual-path (root piConfig + shim) is part of what the cli.ts rebrand mechanism reads. Q1/Q2 slightly under-covers this.
- **`gsd.linkable` workspace convention (minor).** `loader.ts:185-203` reads `gsd.linkable === true` from each workspace package's package.json to decide which packages to symlink-or-copy into `node_modules/@gsd/`. This is the actual mechanism that resolves "vendored package becomes addressable as `@gsd/pi-*` at runtime" — central to Q2 but the slice does not cite this convention by name. The slice does cite `loader.ts:174-199` which covers the surrounding logic.
- **Optional `koffi` and `@anthropic-ai/claude-agent-sdk` (minor).** The slice's runtime-dependency-graph claim (Finding 1.5) does not surface that `@anthropic-ai/claude-agent-sdk` and `koffi` are optional dependencies at root (`package.json:146-153`). Not load-bearing for the architectural picture; relevant if synthesis cares about provider-coupling depth.
- **No mention of `studio/` (a workspace member).** The slice's tree includes `studio/` with one-line description but does not connect it to the workspace declaration. Minor.

**Verdict:** completeness adequate. The slice could be more precise about the *mechanism* of vendoring (the `gsd.linkable` + symlink dance in loader.ts) but the *fact* of vendoring is well-covered.

## §3. Framing-leakage

I scanned the slice output for the dispatching project's in-house vocabulary patterns flagged in the audit prompt:

- **"α / β / γ / δ" shapes:** absent.
- **"doctrine load-points" / "anti-pattern self-check":** absent.
- **"artifact-mapping" framing:** absent.
- **"long-horizon agential development" / "harness-uplift":** absent.
- **"R2 / R1" or "R2/R3 hybrid" upstream-relationship vocabulary:** absent.
- **"Calibrated language" register matching project's in-house patterns:** the slice uses "high confidence / medium confidence / medium-low confidence" tags consistently, and "appears to" rather than "is" in many places. This is exactly the calibration discipline the preamble asked for, so its presence is *prompted-for*, not leakage. The register does not slip into the more elaborate moves I would flag (e.g., "load-bearing", "structural smuggle", "reverse-engineered necessity" — none of those appear).
- **"Direction-shifting evidence" phrase appears in the slice (line 101).** This phrase is *also* in the preamble's standard output structure section (preamble.md:96), so the slice is responding to a prompted prompt, not adopting unprompted in-house vocabulary. Not leakage.

**Note on terminology that *is* gsd-2's own:** "vendored from pi-mono" — this is gsd-2's own description string in its own package.jsons. The slice using it is faithful to source, not leakage.

**One minor stylistic register note:** Finding 5.10 uses "central enough to flag for cross-slice synthesis because hooks are both an agent contract and a security/trust surface" — the "central enough to flag" phrasing is mildly evaluative and matches the cross-slice watchlist in the preamble (preamble.md:44-51), again responding to prompted-for behavior. Not leakage.

**Verdict:** no framing-leakage observed. The slice respected forbidden-reading and used neutral or gsd-2-own vocabulary throughout.

## §4. Calibration discipline

Calibration is generally well-applied per claim. Spot-checks:

- **Finding 1.1 (high):** "appears to be a Node/TypeScript CLI package named `gsd-pi`". The "appears to" is over-cautious given `package.json:2` says verbatim `"name": "gsd-pi"`. Could be "is" without overreach. *Minor: slightly over-hedged.* Not consequential.
- **Finding 1.8 (medium):** "RTK is a managed external binary, not a TypeScript library dependency." Source-evidence is concrete (install.js, package.json deps, cli.ts gating). Could be high confidence. *Minor: slightly over-hedged.*
- **Finding 1.10 (medium):** "the ordinary CLI is not itself sandboxed by default in the code I read" — appropriately calibrated; the negative claim depends on completeness of reading, and medium reflects that.
- **Finding 2.6 (medium):** "not monkey-patching in the narrow sense, but not clean library use either" — appropriately calibrated. The negative ("did not observe monkey-patching") is bounded to what was read, and the positive characterization (vendoring + env vars + extension registration + module aliasing) is concrete.
- **Finding 5.10 (medium):** "hooks/security/trust contract" — appropriately calibrated; trust model claims rest mostly on docs (`docs/user-docs/hooks.md`) which the slice acknowledges.
- **(v) RTK divergence flag (medium):** appropriately calibrated. The "may be a README register issue, a release transition artifact, or a distinction between provisioning and activation" closing is honest about residual uncertainty.

**Pattern observation:** the slice tends to slightly *over-hedge* on concrete, source-verified facts (Findings 1.1, 1.8) and is *appropriately calibrated* on inferred or absence-claim findings (1.10, 2.6, 5.10). The over-hedge is mild and consistent — no calibration inversions where thinly-evidenced claims get high confidence.

**Verdict:** calibration discipline is sound. Mild over-hedge tendency does not affect synthesis-relevant claims.

## §5. Direction-shifting evidence

### What was surfaced

The slice surfaces three pieces of direction-shifting evidence, all of which I verified independently:

1. **ADR-010 is *Proposed*, not implemented.** The current source tree has no `packages/gsd-agent-core` or `packages/gsd-agent-modes`. Any downstream plan assuming a clean Pi-vs-GSD seam would be wrong-shaped. (Verified directly via `ls /packages/`.) **Highest direction-shifting potential of any claim in the slice.**
2. **gsd-2 vs Pi SDK is not a clean library boundary.** `pi-coding-agent` contains GSD-authored code intermixed with vendored Pi code; the ADR estimates ~79 GSD-authored files inside that package. Treating "GSD as an app on top of Pi SDK" would mischaracterize what GSD currently is. (Verified via package descriptions, ADR-010, and the `@gsd/pi-coding-agent` import surface in cli.ts.)
3. **README/source RTK activation divergence.** Concrete tension between stated and implemented behavior. (Verified verbatim.)

### What was flagged but I do not think shifts direction

- (iv) bullet "Multi-user/collaboration is present but not scoped here (medium-low confidence)" — this is appropriately scoped as out-of-slice and does not need to shift direction. Honest acknowledgment, not a false positive.

### What was missed (I did not find missed direction-shifters)

I scanned for:

- **Hidden coupling beyond what ADR-010 admits.** The extension loader's alias map (`packages/pi-coding-agent/src/core/extensions/loader.ts:325-342`) explicitly aliases both `@gsd/pi-*` *and* `@mariozechner/pi-*` to the same vendored modules, supporting external Pi-ecosystem extensions importing from the original scope while still resolving to gsd-2's vendored copies. This is in the slice (Finding 2.7) and is potentially direction-shifting in a synthesis-stage way: **gsd-2's vendoring posture is bidirectionally compatible with upstream Pi extensions but routes them to gsd-2's modified copies**. Synthesis should note this: "downstream consumer can write a Pi extension that runs in either upstream Pi or in gsd-2 without code change, but the runtime behavior in gsd-2 will reflect gsd-2's modifications, not upstream Pi." The slice surfaces the fact; it does not draw out this implication, but that's synthesis-stage work.
- **Pi rebranding mechanism subtlety.** `loader.ts:88-90` sets `PI_PACKAGE_DIR = pkgDir` (the `pkg/` shim directory), and `pkg/` contains a separate `package.json` with `piConfig.name = "gsd"` and `configDir = ".gsd"`. The dispatching project, if it were considering wrapping or extending gsd-2, would need to know that the rebrand is implemented via env-var-pointed-at-shim-package — i.e., gsd-2 does not modify Pi internals to rebrand; it relies on Pi's own config-from-env hook. This is mildly direction-shifting because it suggests Pi was designed to be wrappable. The slice surfaces "PI_PACKAGE_DIR" as one of the env vars (Findings 1.4, 2.6) but does not name the rebranding mechanism cleanly. Marginal miss; synthesis can recover this from cited source.

### Convergent direction-shifters across the slice

Reading findings 2.1, 2.5, 2.6, 2.7, and (iv) bullet 1 together, the picture is:

> The "clean seam" between gsd-2 and Pi SDK is *aspirational* (ADR-010 Proposed), not *implemented*. Today, gsd-2 is a vendored fork of four Pi packages with substantial GSD-authored code embedded in `pi-coding-agent`, plus a GSD glue layer in `src/`, plus bundled extensions. Any proposed intervention shape that depends on Pi-vs-gsd-2 separability needs to plan for the seam refactor first, or accept that interventions land inside the entanglement.

The slice does not state this synthesis-explicit conclusion (correctly — that's synthesis-stage work) but the constituent findings converge on it cleanly.

## §6. Recommendation

**Clean → proceed.**

The slice's load-bearing claims for synthesis (vendoring shape, ADR-010 proposed-not-implemented, in-process MCP mode plus standalone MCP package, RTK opt-in gating, the agent-runtime contract being plural rather than singular) all verify against source. Citations are accurate within minor line-range tolerance. Calibration is sound, with a mild over-hedge tendency that does not invert any claim. No framing-leakage observed; the slice respected forbidden-reading.

Optional addendum the synthesis stage may want to incorporate without re-dispatching the slice:

- Note that the `gsd.linkable` convention in workspace `package.json` files is the runtime mechanism that ties vendoring to module resolution (Q2 implementation detail).
- Note that the rebrand mechanism is shim-directory + `PI_PACKAGE_DIR` env var — i.e., Pi appears to have been designed to be wrappable, which constrains how downstream synthesis frames "Pi knows about gsd-2 vs gsd-2 imports Pi."
- Note that the convergent reading of Findings 2.x produces a synthesis-ready statement: "gsd-2 is a vendored modified Pi fork plus GSD glue layer; the clean seam is proposed, not implemented."

If synthesis chooses not to write an addendum and instead carries those notes inline, that is also fine — the slice's own findings already point at all three.

## §7. Same-vendor framing-leakage caveat

I am same-vendor relative to the cross-vendor reader I am auditing. My critique here grounds in within-artifact verifiable contradictions where possible — five spot-checks against gsd-2 source, all of which the slice's claims survived. Where my findings are interpretive (especially §3 framing-leakage scan and §5's "convergent direction-shifters" reading), I have flagged them at lower severity and written them as observations rather than conclusions. Cross-vendor audit of my audit would catch different things (e.g., whether my own register is inflating the audit's apparent rigor); this audit does not substitute for that.

One specific same-vendor risk: I might be reading the slice *sympathetically* because its calibration register (high/medium/medium-low confidence labels, "appears to" hedging) matches the register I produce by default. I tried to compensate by spot-checking five concrete claims against source rather than evaluating the slice on its rhetorical surface. The spot-checks all verified, which is an empirical rather than register-based ground for the clean verdict. But I cannot fully compensate for sympathetic reading; the cross-vendor synthesis stage should treat my "clean → proceed" verdict as one input, not a final pass.
