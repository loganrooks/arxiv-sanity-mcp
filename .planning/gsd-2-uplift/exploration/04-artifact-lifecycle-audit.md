---
audit_target: .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md
date: 2026-04-28
auditor: Claude Opus xhigh adversarial-auditor
status: complete
---

# Audit of slice 4 output — artifact-lifecycle

## §0. Audit summary

- **Source verification:** All five spot-checked claims verified against gsd-2 source. Citations land within ±1-2 lines of the cited ranges; in one case the slice cites `paths.ts:1-9` and the file's header docblock is exactly lines 1-10 — clean. Minor citation drift on `commands-extensions.ts:798-841` (the actual handler runs roughly 796-844, but the citation is still useful and accurate to within reading tolerance). Verdict: clean on source-verification.
- **Completeness:** One material gap. The slice's Q2 asked "if multiple extension mechanisms appear ... what are the relationships between them?" The slice's Finding 2.8 acknowledges "several extension-adjacent mechanisms" but does not enumerate three concrete distinct subsystems that exist in source: (a) the **ecosystem layer** at `src/resources/extensions/gsd/ecosystem/loader.ts` which loads `.gsd/extensions/` extensions via a separate `GSDExtensionAPI`, (b) the **workflow plugins** subsystem at `src/resources/extensions/gsd/workflow-plugins.ts` with three-tier discovery (project / global / bundled) and four execution modes, (c) the **skills** subsystem with skill manifests (`src/resources/extensions/gsd/skill-manifest.ts`, `skill-discovery.ts`, etc.) and per-unit-type allowlists. The slice's open-question on `.pi/extensions` vs `.gsd/extensions` correctly flags the ecosystem layer's existence as an unknown, but Q2 itself wanted enumeration. **Severity: material** — Q2 is the slice's most load-bearing diagnostic per the slice spec, and the missing enumeration directly bears on "if I want to extend gsd-2 with feature X, where would the extension code go?"
- **Framing-leakage:** None observed. The output uses calibrated language consistently and uses gsd-2's own vocabulary (tier, manifest, registry, ecosystem, workflow plugins). No "α/β/γ", no "load-bearing", no "doctrine load-points", no "R2/R3" upstream-relationship vocabulary. Confidence labels are present per finding.
- **Calibration discipline:** Mostly appropriate. One minor over-confidence: Finding 4.1 marks "the public package appears to be the npm package `gsd-pi`, currently version `2.78.1`" as [high] which is fine, but uses "appears to be" hedge that the source pins definitively (`package.json:2-3` is unambiguous). Not a real problem; calibrated language is preferable to over-claiming. Finding 2.8 at [medium-high] is appropriately calibrated given the missed enumeration.
- **Direction-shifting evidence:** The slice surfaces the right load-bearing extension-surface architecture (manifest + entry module + ExtensionAPI + tier system + registry) and correctly flags that core gsd is itself an extension (Finding 2.7). The Q5 contribution-culture probe failed due to network/auth issues and the slice marks this incomplete with raw error output preserved — appropriate. The missed mechanisms (ecosystem, workflow plugins, skills) **strengthen rather than reverse** the slice's central direction-shifting claim that gsd-2 has a substantive extension system; their absence in the output is a completeness issue, not a directional misread.

**Tier summary:** 1 material finding (completeness gap in Q2 mechanism enumeration), 2 minor findings (calibration nuance on Finding 4.1; the slice's open-questions list is doing some of the work that Q2 should have done in-line), no critical findings, no framing-leakage.

## §1. Source verification

Five spot-checks targeting the highest-stakes claims (extension surfaces, migration tooling, package metadata).

**SC-1: `extension-registry.ts:15-48` (manifest and registry-entry interfaces).** [verifiable]

Slice claim: "Registry entries include extension ID, enabled flag, source, disable metadata, version, installed origin, and install type" cited at `src/extension-registry.ts:34-48`.
Source verification: lines 34-43 show `ExtensionRegistryEntry` with `id`, `enabled`, `source: "bundled" | "user" | "project"`, `disabledAt`, `disabledReason`, `version`, `installedFrom`, `installType`. The `ExtensionManifest` interface at lines 15-32 matches the slice's field list. Verdict: **verifiable, accurate**. Confidence: high.

**SC-2: `extension-discovery.ts:9-17` (entry resolution from `pi.extensions` or fallback) and `:61-119` (directory scanning + shadowing).** [verifiable]

Slice claim: "Source discovery resolves entry paths from package `pi.extensions`, falls back to `index.ts`/`index.js`, scans extension directories, and lets installed extensions with the same manifest ID shadow bundled extensions" at `src/extension-discovery.ts:9-17`, `61-119`.
Source verification: lines 18-52 implement `resolveExtensionEntries()` which checks `pkg.pi.extensions` then falls back to `index.ts`/`index.js`. Lines 61-119 implement `discoverExtensionEntryPaths()` and `mergeExtensionEntryPaths()` which explicitly note "Installed extensions with the same manifest ID as a bundled extension take precedence (D-14)" at line 86. Verdict: **verifiable, accurate**. Confidence: high. Minor note: slice cites "9-17" but the relevant docblock plus `resolveExtensionEntries` signature spans roughly lines 9-17 + the implementation runs through line 52; the citation as written points to the docblock, which is fine.

**SC-3: `migrate/writer.ts:140` (boundary map skip per D004).** [verifiable]

Slice claim: "the migration writer formats roadmap title, vision, success criteria, and slice checklist, but explicitly skips writing the boundary map 'per D004'" at `src/resources/extensions/gsd/migrate/writer.ts:112-143`.
Source verification: line 140 contains exactly the comment `// Skip Boundary Map section entirely per D004`. The `formatRoadmap` function at lines 112-143 emits title, vision, success criteria, and slices but does not emit any boundary-map section. Verdict: **verifiable, accurate**. Confidence: high. The slice's quote of "per D004" is verbatim from source.

**SC-4: `migrate/transformer.ts:241-254` (requirement mapping with hardcoded fields).** [verifiable]

Slice claim: "Requirement records are assigned class `core-capability`, source `inferred`, and `primarySlice` `'none yet'`."
Source verification: lines 241-254 implement `mapRequirements` with exactly `class: 'core-capability'`, `source: 'inferred'`, `primarySlice: 'none yet'`. Verdict: **verifiable, accurate**. Confidence: high.

**SC-5: `package.json:2-13` and `update-check.ts:8-12` (package identity and update-check cache).** [verifiable]

Slice claim: "package `gsd-pi`, version `2.78.1`" and "update checker caches state at `~/.gsd/.update-check`, queries `https://registry.npmjs.org/gsd-pi/latest`".
Source verification: `package.json:2-3` shows `"name": "gsd-pi"`, `"version": "2.78.1"`. `update-check.ts:8-12` shows `CACHE_FILE = join(appRoot, '.update-check')` where `appRoot = ~/.gsd` per `app-paths.ts:4`, and `DEFAULT_REGISTRY_URL = https://registry.npmjs.org/${NPM_PACKAGE_NAME}/latest`. Verdict: **verifiable, accurate**. Confidence: high.

**Summary of source verification:** All five high-priority spot-checks are accurate at the cited ranges. No fabricated claims; no wrong citations. The slice's source-citation discipline is good.

## §2. Completeness

**CG-1: Q2 mechanism enumeration is incomplete.** [material]

Q2 explicitly asks: "**If multiple extension mechanisms appear** (e.g., a top-level extension manifest, workflow templates, skills, MCP tools, hooks, ecosystem plug-ins, or others), what are the relationships between them? Are they unified ... or distinct subsystems with different lifecycles? For each mechanism: cite the registration entry-point, the discovery mechanism, and the invocation/dispatch pipeline."

The slice's Finding 2.8 says "There are several extension-adjacent mechanisms, but they are not a single declarative plugin manifest" and gestures at "extension entry loading + ExtensionAPI ... registry/manifest controls discovery ... resource sync ... `/gsd extensions` manages user-installed packages." This is the same-system enumeration but at different layers, not separate-system enumeration. Three concrete additional subsystems exist in source and were not enumerated:

- **Ecosystem layer** at `src/resources/extensions/gsd/ecosystem/loader.ts:1-110`. Loads `.gsd/extensions/` (project-local) extensions via a separate `GSDExtensionAPI` (`src/resources/extensions/gsd/ecosystem/gsd-extension-api.ts:1-10` notes the wrapper "intercepts only" — distinct from the standard pi `ExtensionAPI`). Has its own trust gate (`isProjectTrusted` inlined; `loader.ts:25-38`). Has its own ready-promise singleton and logging path. The slice's open-question on the `.pi/extensions` vs `.gsd/extensions` discrepancy detected the symptom; the cause is that there are *two parallel project-local extension subsystems*, not one with a path discrepancy.
- **Workflow plugins** at `src/resources/extensions/gsd/workflow-plugins.ts:1-60`. Three-tier discovery (project > global > bundled), four execution modes (`oneshot`, `yaml-step`, `markdown-phase`, `auto-milestone`), separate registry at `workflow-templates/registry.json` with 25 bundled templates including `bugfix`, `refactor`, `spike`, `release`, `pr-review`, etc. This is a genuinely separate extension surface with its own dispatch pipeline (`/gsd workflow <name>`) and its own artifact-dir conventions per template.
- **Skills** subsystem at `src/resources/extensions/gsd/skill-manifest.ts:1-60`, `skill-discovery.ts`, `skill-catalog.ts`, `skill-health.ts`, `skill-telemetry.ts`, plus `~/.agents/skills` and `src/resources/skills/`. Per-unit-type skill allowlist resolver (RFC #4779) with an inclusion-list semantic. The slice's Finding 2 reading mentions "managed-resource sync" copies bundled resources but does not surface skills as a distinct extension surface in their own right.

**Why this matters:** the slice's framing prompt names this slice "load-bearing for the dispatching project's downstream decisions about how (or whether) to relate to gsd-2 as an extension target." A reader asking "if I want to extend gsd-2 with feature X, where would the extension code go?" would want to know that there are at least four distinct surfaces (pi-coding-agent extensions / GSD ecosystem extensions / workflow templates / skills), not one extension subsystem with a path discrepancy. The slice's open-questions section partially compensates by flagging the path-discrepancy and the broader telemetry/security watchlists, but the synthesis stage will still need to enumerate these surfaces — that work belongs at slice level.

**Confidence on this finding: high** (source-verifiable; the missing surfaces exist in source as separately-architected subsystems with their own loaders, discovery, and dispatch).

**CG-2: Q3 migration-tooling preservation gap is appropriately flagged.** [clean]

The slice's Finding 3.3 correctly identifies that the parser reads more than the writer emits (verification files, extra files, quick tasks, top-level config, old STATE.md content). This is well-grounded and properly hedged ("appears either dropped, transformed indirectly, or not written by this path"). No completeness gap here.

**CG-3: Q5 contribution probe is appropriately bounded.** [clean]

Q5 is marked incomplete with raw error output preserved. The slice's local-fallback observations (CONTRIBUTING.md sections; PR numbers from git log) are stated as raw observation, not interpretation. The slice spec required no qualitative characterization, and the slice respected that. Clean.

## §3. Framing-leakage

**No framing-leakage observed.**

I scanned for the specific patterns flagged by the audit prompt:

- "α / β / γ / δ" shapes: not present.
- "doctrine load-points": not present.
- "anti-pattern self-check": not present.
- "Artifact-mapping": not present (despite the slice's title containing "artifact lifecycle", the framing is direct and uses gsd-2's own vocabulary).
- "Long-horizon agential development" / "harness-uplift": not present.
- "R2 / R1" / "R2/R3 hybrid" upstream-relationship vocabulary: not present (the prompt was revised to remove this and the output is clean).
- "Calibrated language" register matching project's in-house patterns: the output does use calibrated language (per the preamble's instruction), but uses it cleanly and at the level of individual findings rather than as a closing-footnote scope-disclaimer. This is the right register for the artifact and not a leakage signal. Confidence labels are inline with claims.

**Confidence on no-leakage: medium-high** (interpretive claim; same-vendor reading risk noted in §7).

## §4. Calibration discipline

**Strengths:**

- Confidence labels appear inline per finding ([high], [medium-high], [medium]) — appropriate.
- Hedging language ("appears to", "this slice did not trace ... end-to-end", "I did not see") is used where source-evidence is partial.
- Finding 1.5 correctly downgrades to [medium] given the schema-vs-tooling tension (boundary maps documented but not emitted).
- Finding 2.8 at [medium-high] is appropriately calibrated for an interpretive claim about subsystem decomposition.

**Minor observations:**

- **Finding 4.1 ([high])** uses "the public package appears to be the npm package `gsd-pi`, currently version `2.78.1`". The "appears to be" hedge is slightly looser than warranted — `package.json:2-3` is unambiguous on both name and version. This is a register choice (favoring the calibrated-language default) rather than miscalibration; flag as minor only.
- **Finding 5 (Q5) status: incomplete [high]** — the [high] confidence applies to the *fact that the probe was incomplete*, not to claims about contribution culture. Reader could parse this either way; making the scope of the confidence label explicit (e.g., "the probe failed; this is the raw evidence") would help, but is not blocking.
- **Open-questions section** is doing some legitimate work that Q2 should have done in-line. The path-discrepancy open-question, in particular, is more substantive than an open question — it's a finding (there are two parallel project-local extension subsystems). Moving it into Q2 with appropriate confidence labeling would strengthen the output. This bridges into §2's CG-1.

**Pattern check:** no inconsistent calibration where Q1 over-claims and Q5 over-hedges, or vice versa. Calibration is internally consistent.

## §5. Direction-shifting evidence

**Surfaced (correctly):**

- Finding 2.7 — "Core GSD itself is implemented as an extension" — this is genuinely direction-shifting for any consumer evaluating gsd-2 as an extension target. It tells the reader the extension API is product-load-bearing, not a third-party afterthought. The slice flags this concretely.
- Finding 1.2 + 1.3 — `.gsd` may be project-local OR a symlink to external state; STATE.md is derived cache, not source-of-truth. These shape any "where do we put our artifacts?" question.
- Finding 3.6 — separate migration tooling for in-project `.gsd/` to external state, distinct from v1 `.planning` migration. Direction-shifting because it tells the reader that artifact-location migration has been thought about as a separate concern.
- Watchlist flags in (iv) — telemetry/observability as central; security/trust boundary central for extensions. These respect the slice scope and surface them as integration questions for synthesis. Appropriate.

**Missed (or partially missed):**

- The plurality of extension surfaces (CG-1) is direction-shifting evidence that was *partially* surfaced via the open-questions section but not fully integrated into Q2's main answer. A reader of just (ii) Q2 + (v) would conclude "one extension system with some adjacent metadata layers"; a reader who reads source would conclude "four parallel extension surfaces with different APIs, lifecycles, and dispatch pipelines." Synthesis would need to resolve this; the slice's job was to surface it.
- The CONTRIBUTING.md observation that "Extension-first" is an explicit architecture principle (`CONTRIBUTING.md:127` "Extension-first. Can this be an extension instead of a core change?") was read but not surfaced as direction-shifting evidence. This is a significant signal for any consumer evaluating "is gsd-2 receptive to extensions vs forks?" — the project's own contribution policy answers that affirmatively. The slice's Q5 fallback observation lists this as a section header but does not characterize it. Given the slice spec's instruction to *not* characterize qualitatively in Q5, this restraint is defensible — but it could have been surfaced in §(iv) open-questions as "explicit architecture principle relevant to extension-target evaluation." Severity: minor.

**False positives (in slice, on independent reading):**

None identified. Each substantive finding I traced back to source held up.

**Integration flag for synthesis:**

The combination of (a) core gsd is an extension, (b) extension-first contribution policy, (c) plurality of extension surfaces (ecosystem, workflow plugins, skills, pi-coding-agent extensions), (d) tiered manifest system with explicit community tier — these together point at gsd-2 having a more substantive extension story than the slice's main answer (Q2) communicates. The synthesis stage should treat the slice's open-questions and CONTRIBUTING.md observations as load-bearing alongside Q2's findings, not as marginalia.

## §6. Recommendation

**Minor findings → addendum.**

Rationale:

- Source verification is clean (5/5 spot-checks accurate at cited ranges).
- No framing-leakage observed.
- Calibration is appropriate with minor register-only notes.
- The one material finding (CG-1: Q2 mechanism enumeration is incomplete) is *partially* compensated by the open-questions section flagging the `.pi/extensions` vs `.gsd/extensions` discrepancy. Synthesis can resolve the gap by reading source directly for the named subsystems (ecosystem, workflow plugins, skills) — the citations in this audit (`ecosystem/loader.ts:1-110`, `workflow-plugins.ts:1-60`, `skill-manifest.ts:1-60`) are sufficient pointers.
- The Q5 incomplete-probe is genuinely incomplete due to network/auth failures, not slice-author negligence. Local-fallback observations are appropriate.

A re-dispatch is not warranted because (a) the missing enumeration is recoverable at synthesis stage from the citations this audit provides, (b) the rest of the slice's analysis is sound, and (c) re-dispatching would burn budget on a slice that is mostly correct. An addendum noting the three additional extension subsystems (ecosystem / workflow plugins / skills) with the citations from §2 of this audit would be sufficient.

**Suggested addendum content (one paragraph):**

> Addendum (post-audit, 2026-04-28): the slice's Finding 2.8 enumerates extension-adjacent mechanisms at the level of "entry loading / registry / resource sync / `/gsd extensions` install flow" — i.e., layers of one subsystem. Audit identified three additional distinct subsystems with separate APIs, discovery, and dispatch: (1) **ecosystem extensions** (`src/resources/extensions/gsd/ecosystem/loader.ts`, `gsd-extension-api.ts`) which load `.gsd/extensions/` via a `GSDExtensionAPI` wrapper distinct from pi's `ExtensionAPI`, trust-gated and isolated from pi's loader chain — this is the actual cause of the `.pi/extensions` vs `.gsd/extensions` apparent discrepancy flagged in (iv); (2) **workflow plugins** (`workflow-plugins.ts`, `workflow-templates/registry.json`) with three-tier discovery (project > global > bundled) and four execution modes; (3) **skills** (`skill-manifest.ts`, `skill-discovery.ts`, `~/.agents/skills`) with per-unit-type allowlists. Q2's relationship-mapping should treat gsd-2 as having at least four parallel extension surfaces, not one.

## §7. Same-vendor framing-leakage caveat

I am same-vendor relative to the cross-vendor reader I'm auditing. My critique is grounded in within-artifact verifiable contradictions where possible:

- Source-verification findings (§1) are fully verifiable from the gsd-2 source tree; high confidence.
- The completeness gap (§2 CG-1) is grounded in named source files I read directly (`ecosystem/loader.ts`, `workflow-plugins.ts`, `skill-manifest.ts`); high confidence on existence, medium-high confidence on the framing that "Q2 wanted enumeration" — that reading is mine, but it is grounded in the slice spec's explicit Q2 prompt language ("If multiple extension mechanisms appear ... what are the relationships between them?"). A different reader could argue Finding 2.8's gesture-level treatment is sufficient; I think the slice spec's "cite the registration entry-point, the discovery mechanism, and the invocation/dispatch pipeline" requirement makes enumeration the right read.
- Framing-leakage detection (§3) is interpretive; I labeled it medium-high confidence and found nothing concrete.
- Direction-shifting-evidence assessment (§5) is interpretive; the false-positives subsection is empty because I tried hard to find them and could not, but I want to flag that as a same-vendor sympathy risk: I may be reading the slice's open-questions section as doing more work than it does, because I read the *source* and could plausibly construct what the slice should have surfaced. A cross-vendor reader of this audit would catch where my finding-construction outran the slice's actual claim.

Cross-vendor audit of my audit would catch different things; this audit does not substitute. Specifically: a cross-vendor reader might disagree with whether the ecosystem/workflow-plugins/skills subsystems count as "extension surfaces" in the slice spec's Q2 sense — they are not all manifest+entry-module shapes, and a stricter reading of "extension" would exclude workflow-plugins (which are markdown/YAML templates, not code) and skills (which are markdown/SKILL.md format with a manifest layer). I think the slice spec's example list ("workflow templates, skills, MCP tools, hooks, ecosystem plug-ins") explicitly invites all four into scope, but a stricter reader might disagree.
