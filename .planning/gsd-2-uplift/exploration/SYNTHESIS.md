---
type: first-wave-synthesis
date: 2026-04-28
agent: Claude Opus xhigh synthesizer (general-purpose subagent; effort inherited from parent session)
inputs:
  - .planning/gsd-2-uplift/exploration/01-mental-model-output.md
  - .planning/gsd-2-uplift/exploration/02-architecture-output.md
  - .planning/gsd-2-uplift/exploration/03-workflow-surface-output.md
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md (with (vi) addendum)
  - .planning/gsd-2-uplift/exploration/05-release-cadence-output.md (with (vi) corrigenda)
  - .planning/gsd-2-uplift/exploration/02-architecture-audit.md
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md
  - .planning/gsd-2-uplift/exploration/05-release-cadence-audit.md
  - .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md
  - .planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md
  - .planning/deliberations/2026-04-28-framing-widening.md
  - .planning/gsd-2-uplift/INITIATIVE.md (§1, §3)
  - .planning/gsd-2-uplift/DECISION-SPACE.md (§1.7, §1.8, §1.11, §1.12, §3.4, §3.6)
status: complete
escalation_to_paired_synthesis: yes (Trigger 4 fires; Trigger 2 plausibly fires; rationale in §0)
---

# First-wave synthesis — gsd-2 characterization

## §0. Synthesis summary

This synthesis integrates five W1 slice outputs (codex GPT-5.5 high), three W2 audits (Claude Opus xhigh), two side-investigations at GPT-5.5 medium (capabilities probe + W2 markdown-phase dive), and the framing-widening artifact, to feed the incubation-checkpoint deliberation. The aim is integration, not advocacy — direction-shifting evidence is surfaced honestly even where it complicates the operating frame.

**Top-line findings, severity-stratified by bearing on operating-frame-update decisions:**

### Operating-frame-shift findings (would change a decision in DECISION-SPACE.md or the framing-widening if accepted)

- **F1. The Pi clean seam is proposed-not-implemented.** ADR-010 verified as `Status: Proposed`; the current package tree has no `gsd-agent-core` or `gsd-agent-modes`; ~79 GSD-authored files live inside vendored Pi packages with no reliable file-by-file provenance distinction (slice 2 Finding 2.5; audit §1 spot-check 2). **Confidence: high.** This shifts the R2-base operating frame by changing what "extension surface" means: extending gsd-2 today means extending an entangled vendored fork, not a clean library boundary. Bears on R1-R5 viability assessment in §2.1 below.

- **F2. The "extension surface" is plural, not singular — at least four parallel subsystems.** Slice 4's Finding 2.8 enumerated extension-adjacent mechanisms at one subsystem's layers; the slice 4 audit's CG-1 + (vi) addendum identified three additional distinct subsystems (ecosystem, workflow plugins, skills) with separate APIs, discovery, and dispatch (slice 4 audit §2; slice 4 (vi) addendum). Each subsystem solves different uplift problems. **Confidence: high (source-grounded enumeration).** This widens R2's surface and concretizes the framing-widening's plural-significations-of-uplift framework. Bears on §2.5 design-shape candidates.

- **F3. The breaking-change posture has elaborate machinery but the observed practice operates outside the formal channels.** Stated policy + tooling + workflow templates support staged deprecation; observed practice has zero `BREAKING CHANGE`-marked commits in visible 6-month window (~2200 commits, 34 tags); recent removals (Anthropic OAuth in v2.70.0/v2.74.0) have no visible pre-deprecation in the shallow window; experimental preferences explicitly waive the deprecation cycle (slice 5 findings 2.2, 2.6, 2.7, 4.5; slice 5 audit §5 cross-finding flag — directed to synthesis per D3). **Confidence: medium-high.** This is the load-bearing direction-shifter for any R2/R3 strategy that depends on stable extension surfaces. Bears on §2.1 R-strategy assessment + §3.1 contradiction.

- **F4. Two architecturally distinct workflow engines exist with very different determinism guarantees.** `markdown-phase` is prompt-dispatch with lightweight `STATE.json` and no observed phase-advance writes; `yaml-step` is graph-backed with deterministic `GRAPH.yaml` mutation, dependency tracking, structured `context_from`, and shell-command verification (slice 3 Finding Q2 case 1+2; W2 dive §1, §2, §4, §7). **Confidence: high.** Bears on §2.1 (R-viability where workflows are involved) and §2.5 (which intervention shapes are programmatically supported vs prompt-only).

- **F5. RTK gating divergence is real and concrete.** README at line 22 says GSD provisions managed RTK; source at `src/cli.ts:167-178` shows RTK opt-in via `experimental.rtk` (default disabled) (slice 1 (v); slice 2 Finding 1.8 + (v); slice 3 (v); slice 2 audit spot-check 3). **Confidence: high.** Less direction-shifting on its own, but a representative case for the broader docs-vs-source-drift pattern that bears on what kinds of evidence we can trust without source verification.

### Operating-frame-confirm findings (consistent with the operating frame; refinements rather than shifts)

- **F6. R2 is viable in some shape because gsd-2 has substantive extension primitives.** Even with F1's caveats (extending entangled fork, not clean library), the four parallel extension surfaces (F2) plus the `pi.extension: true` validator (`src/extension-validator.ts`) plus the gsd-2 contribution policy's "Extension-first. Can this be an extension instead of a core change?" principle (slice 4 audit §5 missed-but-noted) all support R2 viability per `DECISION-SPACE §1.8` assumption (1) (slice 4 Findings 2.1, 2.6, 2.7; slice 4 audit §5).

- **F7. gsd-2 is human-and-agent-facing-and-machine-facing.** The agent-runtime contract is plural (CLI/TUI; Pi extension API; `AGENTS.md`/`CLAUDE.md`; skills; in-process MCP via `--mode mcp`; standalone `@gsd-build/mcp-server`; RPC client; hooks). gsd-2 doesn't draw a single human-vs-agent line — it draws a transport-and-runtime line (UI-aware overlays vs headless/RPC/MCP) (slice 1 Finding 4.1-4.4; slice 2 Finding 5.1-5.9; slice 3 Q5; capabilities probe §A.4, §A.8). **Confidence: high.**

- **F8. Telemetry/observability/forensics is central, not peripheral.** Worktree telemetry, journal (daily-rotated JSONL, ~22 schema versions), forensics, doctor, debug sessions, metrics ledger, cost/budget controls, `/gsd export --html` reports — all flagged across slices as central enough for synthesis-stage integration (slices 1-5 cross-slice watchlists; capabilities probe §A.9; slice 5 audit §5 missed `SCHEMA_VERSION = 22`). **Confidence: high.** The reach matters for §2.5's design-shape candidates and for any R-strategy touching observability.

- **F9. Security/trust model is structurally present and central.** Hook trust marker (`.pi/hooks.trusted`); write-gate state-machine; tool-policy `UnitContextManifest`; exec-sandbox with timeout/byte caps; secret scanning; destructive-command classifier; project-trust gating for ecosystem extensions (slices 2, 3, 4 watchlists; capabilities probe §A.10). **Confidence: high.** Bears on what an extension can do at runtime + how R2 work has to negotiate trust boundaries.

### Open at synthesis stage (synthesis surfaced but couldn't resolve)

- **O1. Project-anchoring is interpretive.** Per framing-widening §3.3, Logan's read on whether arxiv-sanity-mcp sits "primarily Context A with strong Context F secondary" is binding. First-wave evidence doesn't ground-truth this; it characterizes gsd-2, not arxiv-sanity-mcp's actual context. Synthesis cannot dispose this — incubation-checkpoint work.

- **O2. R5 viability requires comparison frame first-wave didn't supply.** Whether replacement-informed-by is warranted depends on competitor-landscape evidence (framing-widening §9 item 3; deferred). First-wave reads gsd-2 only; "is gsd-2's design fit-for-our-purpose vs alternative tools?" requires evidence first-wave was scoped to exclude.

- **O3. Whether gsd-2's machinery-vs-practice gap (F3) is a stable feature or a transition state.** Visible window is shallow-clone-bounded (~6 months at high commit density). Whether the discrepancy reflects a pattern that will persist (the project's stated discipline doesn't hold operationally) or a transition state (project is moving toward stronger discipline; visible window catches mid-transition) requires deeper history sampling. Synthesis flags but cannot resolve.

- **O4. The four-act / four-surface plurality intersection.** F2 enumerates four extension subsystems; framing-widening §4 names four "uplift" acts. Whether each subsystem maps cleanly to one act (e.g., ecosystem-extensions = R2 modify-via-extension; skills/hooks-config = configure; orchestration scripts = R4; sibling-harness = R5) is an interpretive integration call. Synthesis surfaces the structure but defers the specific mapping to incubation/second-wave-scoping.

### Escalation to paired-synthesis: yes

Per `synthesis-spec.md §"Paired-synthesis escalation criterion"` (calibrated low — any one trigger fires escalation):

- **Trigger 4 fires (high-uncertainty interpretive claims at load-bearing positions).** This synthesis carries multiple interpretive claims at load-bearing positions for incubation-checkpoint:
  - §2.1 R-strategy viability mapping across R1-R5 (interpretive integration of slice + audit + framing-widening evidence).
  - §2.3 long-horizon framing axis read against six-context plurality (where evidence concretizes which contexts).
  - §2.4 project-anchoring (per framing-widening §3.3, this is interpretive — Logan's read is binding).
  - §3.1 contradiction resolution (machinery-vs-practice on breaking-change posture is synthesis-level integration of slice 5's findings).
- **Trigger 2 plausibly fires (load-bearing no-change claims).** §2.2 surfaces evidence both *for* and *against* the metaquestion's "uplift-of-gsd-2 is the right shape" position; the integrated read holds the operating frame intact but the rationale rests substantially on this synthesis's reading. If incubation reads §2.2 as the primary basis for not-pivoting, paired-synthesis adds robustness.
- **Trigger 3 plausibly fires (major contradiction resolution).** §3.1 on machinery-vs-practice is a cross-slice contradiction synthesis resolves in a way that materially shapes downstream interpretation.

The dispatching session pre-flagged Trigger 4 as structurally likely; that prediction holds. Paired-synthesis with cross-vendor (codex GPT-5.5 high or xhigh per B3 escalation-stage decision) is warranted.

---

## §1. Cross-slice pattern integration

Patterns that emerge across multiple slices. Cross-references the framing-widening's vocabulary (R1-R5; six contexts; four-act plurality) where applicable.

### §1.1 The Pi-vendoring + clean-seam tension

- **Contributing slices/inputs:** slice 1 (Finding 1.2 entry-point mediation through `loader.ts` + `cli.ts` two-file pattern); slice 2 (Findings 2.1-2.7; audit-verified spot-check 1, 2, 5); slice 4 (Finding 2.7 — core gsd is itself an extension); ADR-010 verbatim; slice 2 audit §5 convergent direction-shifter.
- **Pattern:** gsd-2 is a vendored modified Pi fork with substantial GSD-authored code embedded inside `pi-coding-agent` (~79 files per ADR-010), wired together by environment variables (`PI_PACKAGE_DIR`, `GSD_CODING_AGENT_DIR`) and a `gsd.linkable` workspace convention that symlinks vendored packages into `node_modules/@gsd/*`. The extension loader explicitly aliases both `@gsd/pi-*` and `@mariozechner/pi-*` to the same vendored modules, supporting upstream-Pi-ecosystem extensions while routing them to gsd-2's modifications. ADR-010 proposes a clean seam (`@gsd/agent-core`, `@gsd/agent-modes`) but is `Status: Proposed`; the seam doesn't exist yet.
- **What it implies for uplift:** any R2 work (extension) lives inside the vendored fork's runtime surface, not on top of a clean Pi library; any R3 work (upstream PR) targets gsd-2's repo (which gsd-2 maintainers control), not pi-mono (which Pi maintainers control); R2 work that touches pi-coding-agent internals is functionally R1-shaped (modifying the vendored fork directly) per ADR-010's own diagnosis ("no reliable way to distinguish GSD files from pi files without reading them individually").
- **Confidence:** high (source-verified at audit; ADR-010 verbatim; package descriptions explicit).

### §1.2 The two-engine architecture (markdown-phase vs yaml-step)

- **Contributing slices/inputs:** slice 3 Finding Q2 case 1 (DevWorkflowEngine vs CustomWorkflowEngine vs workflow-templates vs UOK kernel — 4-shape dispatch); W2 dive §1, §2, §4, §7; capabilities probe §A.8 (workflow templates registry; modes `oneshot`/`yaml-step`/`markdown-phase`/`auto-milestone`).
- **Pattern:** gsd-2's automation layer is not one workflow engine but at least two with very different determinism guarantees:
  - **markdown-phase** (e.g., release, hotfix, observability-setup): prompt-dispatch; lightweight `STATE.json`; no observed phase-advance writes by the executor; commands in markdown body are *instructions to the agent*, not executor-owned shell steps; deterministic shell execution unobserved/refuted at executor level for this mode.
  - **yaml-step** (e.g., test-backfill, docs-sync): graph-backed; deterministic `GRAPH.yaml` mutation; dependency-aware step dispatch; structured `context_from` for prior-step artifacts; `shell-command` verification via `spawnSync("sh", ["-c", ...])`.
- **What it implies for uplift:** §2.5's intervention candidates that depend on deterministic execution (e.g., `§C.2` semver-aware release plugin; `§C.3` programmatic hotfix backport invocation) hit a determinism boundary when targeting markdown-phase mode. Reframing as yaml-step (which has the determinism but fewer existing exemplars) is one path; building wrapper code around markdown-phase is another; accepting agent-prompted indirection is a third. This is a real R-strategy fork — different acts (per framing-widening §4 plurality) target different engine modes.
- **Confidence:** high (W2 dive at medium with explicit absence-claim discipline + slice 3 at high cross-confirms the architectural distinction).

### §1.3 Plural extension surfaces (at least four parallel subsystems)

- **Contributing slices/inputs:** slice 4 Finding 2.8 (extension-adjacent layers within one subsystem); slice 4 audit §2 CG-1 + (vi) addendum (three additional distinct subsystems); capabilities probe §A.8.
- **Pattern:** gsd-2 has at least four parallel extension surfaces, each with separate APIs, discovery, and dispatch:
  1. **pi-coding-agent extensions** — manifest + entry module exporting activation function receiving `ExtensionAPI`; multi-root discovery (global `~/.gsd/agent/extensions/`, project `.pi/extensions/` trust-gated, bundled `src/resources/extensions/`); registry at `~/.gsd/extensions/registry.json`; dependency-aware topological sort.
  2. **GSD ecosystem extensions** — separate `GSDExtensionAPI` wrapper (`gsd-extension-api.ts`) loading `.gsd/extensions/` (project-local) with own trust gate + own ready-promise singleton + own logging path. Resolves the apparent `.pi/extensions` vs `.gsd/extensions` discrepancy: there are two parallel project-local extension subsystems.
  3. **Workflow plugins** — `workflow-plugins.ts` + `workflow-templates/registry.json` with three-tier discovery (project > global > bundled), four execution modes (`oneshot` / `yaml-step` / `markdown-phase` / `auto-milestone`), 25 bundled templates including release, hotfix, refactor, spike, pr-review, ci-bootstrap, observability-setup.
  4. **Skills** — `skill-manifest.ts` / `skill-discovery.ts` / `skill-catalog.ts` with discovery from `~/.agents/skills/`, project `.agents/skills/`, bundled `src/resources/skills/`; per-unit-type allowlists (RFC #4779).
- **What it implies for uplift:** "is gsd-2 receptive to extensions" is the wrong question shape. The right question is "which subsystem(s) does the work-shape we're considering target, and how does each subsystem differ in lifecycle/trust/registration/dispatch?" Different uplift acts (per framing-widening §4) naturally target different subsystems. The plurality strengthens R2 viability *if* the uplift work decomposes onto these surfaces; it weakens R2 viability *if* the uplift work needs cross-subsystem coordination that the parallel architecture doesn't natively support.
- **Confidence:** high (source-grounded enumeration via slice 4 audit; corroborated by capabilities probe §A.8).

### §1.4 The release/workflow tight interleaving

- **Contributing slices/inputs:** slice 5 (iv) item 8 explicitly flagged for synthesis ("release mechanics and product workflow are tightly interleaved"); slice 4 Findings 4.1-4.7 (npm + GitHub Releases + GHCR + workflow templates + version bump scripts); capabilities probe §A.1, §A.3, §A.8.
- **Pattern:** release mechanics and product workflow are tightly interleaved — release templates (markdown-phase) live in the same workflow-plugins subsystem as project-internal templates (refactor, spike); the bundled `release` and `api-breaking-change` workflows write artifacts under `.gsd/workflows/releases/` and `.gsd/workflows/api-breaks/`; the `release` workflow's prepare/bump/publish/announce phases are agent-prompted, not executor-deterministic per F4/§1.2; gsd-2's *own* release uses CI scripts (`generate-changelog.mjs`, `bump-version.mjs`) that run *outside* the workflow plugin system.
- **What it implies for uplift:** any uplift work treating "release cadence" as separate from "artifact/workflow mechanics" misses that they share infrastructure. This is one of the framing-widening's six contexts (Context B/C/E/F all stress release-coordination differently); how gsd-2's tightly-interleaved approach maps onto each context is a synthesis-stage observation, not a slice-stage one.
- **Confidence:** medium-high (cross-slice integration; pattern flagged but not fully traced).

### §1.5 Docs-vs-source divergences as a recurring class

- **Contributing slices/inputs:** slice 1 (v) (RTK default; reassess-after-slice default); slice 2 (v) (RTK activation/register); slice 3 (v) (RTK; verification-after-execute scope; reassessment); slice 4 (iv) (`.pi/extensions` vs `.gsd/extensions`; extension-command-completion narrower than implementation; boundary-map docs/migrator skip); slice 5 (iv) item 4 (CI/CD pipeline doc states automatic Dev→Test→Prod; workflow source is `workflow_dispatch`); capabilities probe §A.6 docs/source divergence note (team `git.isolation`).
- **Pattern:** README/docs frequently overstate or simplify behavior that source actually gates by preference, mode, or environment. This is a class of finding (not single instances): RTK; reassess-after-slice; verification scope; team mode defaults; CI/CD automation language; `.gsd/extensions` vs `.pi/extensions`. The audit verified each instance is concrete and load-bearing for downstream work.
- **What it implies for uplift:** any uplift design that depends on README claims being precisely-correct will likely encounter drift. Source verification before extension is necessary; relying on README descriptions of stable behavior is risky. This is a generalizable observation about gsd-2's documentation-discipline state.
- **Confidence:** high (multiple instances; audit-verified; clearly a class).

### §1.6 ADR-010 as a worked example of an internal seam-tension

- **Contributing slices/inputs:** slice 2 Finding 2.5; slice 2 audit spot-check 2 (verified `Status: Proposed`).
- **Pattern:** ADR-010 names the vendoring + clean-seam tension as gsd-2's *own* diagnosed problem ("no reliable way to distinguish GSD files from Pi files without reading them individually"). The ADR proposes a refactor (`@gsd/agent-core`, `@gsd/agent-modes`) but is `Status: Proposed`. The current state is the diagnosed-problem state; the proposed solution doesn't exist in the package tree.
- **What it implies for uplift:** uplift work that aligns with ADR-010's proposed seam (e.g., uplift extensions targeting a clean `@gsd/agent-core` boundary) would be planning against an architectural future the project itself acknowledges but hasn't reached. Two readings: (i) align with the proposed seam, accept that uplift work has scaffolding that depends on the seam landing — adds coupling to gsd-2's roadmap; (ii) align with the current entangled state, accept that uplift work will need refactor-along-with-gsd-2 if the seam lands. Neither is wrong; the choice is operational.
- **Confidence:** high (ADR-010 verbatim; current state observable).

### §1.7 Machinery-vs-practice on breaking-change communication

- **Contributing slices/inputs:** slice 5 (Findings 2.1-2.7, 4.5, 4.6); slice 5 audit §5 cross-finding integration flag (D3 directed to synthesis); capabilities probe §A.1, §A.3.
- **Pattern (per slice 5 audit §5):** gsd-2 has elaborate breaking-change *machinery*:
  - CONTRIBUTING.md asks for explicit signposting (`CONTRIBUTING.md:120-122`).
  - PR template has explicit "Breaking changes" checkbox (`.github/PULL_REQUEST_TEMPLATE.md:51-54`).
  - Bundled `api-breaking-change` workflow template has staged deprecate-then-remove process with phases survey/migrate/deprecate/release.
  - Release workflow template + `generate-changelog.mjs` recognize `BREAKING CHANGE:` footer / `!:` syntax and propose major bumps.
  - `CHANGELOG.md` follows Keep-a-Changelog format with Added/Fixed/Changed/Deprecated/Removed sections.

  But the *observed practice* in the visible (shallow-clone-bounded) 6-month window:
  - Zero `BREAKING CHANGE`-marked commits or `### Breaking Changes` section headings.
  - Recent removals (Anthropic OAuth in v2.70.0/v2.74.0) appear in `Fixed` sections without visible pre-deprecation in the changelog before the removal.
  - Rapid release cadence (~6.2 tags/visible-week; average tag-gap 0.160 weeks).
  - Communication mode is changelog narrative (Keep-a-Changelog Added/Fixed/Changed entries) with descriptive commit messages, rather than convention-enforcement (`!:` markers; `### Breaking Changes` sections).
  - Experimental preferences explicitly waive the deprecation cycle (`preferences-types.ts:277-287`).
- **What it implies for uplift:** machinery + practice = effective discipline only when both align; here they diverge. For R2 strategy depending on stable extension surfaces, this matters: stability claims based on machinery alone are weaker than they appear. For R3 strategy contributing upstream, the convention-enforcement gap suggests upstream PRs adding `BREAKING CHANGE:` discipline to commits would face an uphill cultural fit. (See O3 — whether this is feature or transition is unresolved.)
- **Confidence:** medium-high (cross-finding integration verified by slice 5 audit; bounded by shallow-clone visible window).

### §1.8 Substrate richness vs depth-of-attention as the limiting factor

- **Contributing slices/inputs:** slice 4 audit CG-1 (Q2 enumeration miss at high-tier despite slice spec's explicit prompt); tier-comparison preliminary §3.2, §5; framing-widening §6.1 honest 50% catch estimate on Q2 revisions.
- **Pattern:** gsd-2's substrate (multi-package monorepo; ~2200 commits 6-month visible; multi-language including Rust native; extensive bundled extensions; multiple workflow engines; plural extension subsystems) outpaces any single slice agent's depth-of-attention even at high effort. Slice 4's Q2 missed three subsystems despite the slice spec's explicit "if multiple extension mechanisms appear" question; the audit caught the miss because audit was xhigh + targeted re-read of named source files; the framing-widening prompt-revision (`§6.1`) added Q2 subsidiaries acknowledging this was likely. Slice 2 Finding 1.7 listed native modules from a docstring but the actual TS export surface is broader (the audit noted this without flagging as material).
- **What it implies for uplift:** for any uplift work that depends on full-surface enumeration (e.g., "enumerate all interaction points before deciding R-strategy"), single-pass slice work is insufficient. The orchestration-level wave-structure-on-large-targets discipline (per framing-widening §9 item 7) — W1 survey + W2 deep-dives + W3 synthesis — is the substantive correction. This itself is a methodological direction-shifting observation about how *to* characterize gsd-2, not just about what gsd-2 is.
- **Confidence:** medium-high (sample size limited; tier-comparison preliminary with n=1 across both tiers per its §8 limits).

---

## §2. Operating-frame test results

### §2.1 R-strategy viability across the widened R1-R5 space (per framing-widening §1)

Each R evaluated against first-wave + audit evidence. Citations point to which slice/audit/probe contributes which evidence.

#### R1 fork (modify gsd-2 source by maintaining a fork)

- **Viability: viable but high-cost; pre-decided as fallback only.**
- **Evidence supporting:** gsd-2's vendored Pi packages already demonstrate that fork-shape works structurally — gsd-2 *itself* is a vendored fork of pi-mono (slice 2 Findings 2.1, 2.5; audit spot-check 5). The technical machinery for forking exists and is in active use within gsd-2's own composition.
- **Evidence challenging:** rapid release cadence (slice 5 Finding 1.1: ~84-401 commits/week visible) means fork maintenance burden compounds quickly; existing `DECISION-SPACE §1.8` change-condition #4 ("if gsd-2's release cadence is too slow for our needs") is the inverse of what's observed — cadence is fast, not slow, which makes R1's "independent release control" attractive but its "track upstream + resolve conflicts" expensive.
- **Implications:** R1's pre-disposition as fallback (per §1.8) is consistent with first-wave evidence; nothing here flips R1 from fallback to primary.
- **Confidence:** medium-high.

#### R2 extension (build via gsd-2's extension primitives)

- **Viability: viable but with substantial caveats; the primitive landscape is richer than expected and the entanglement is also more substantial than expected.**
- **Evidence supporting (R2 stronger than original `§1.8` framing assumed):**
  - Slice 4 + audit + (vi) addendum: gsd-2 has at least four parallel extension subsystems (F2; §1.3 above) — pi-coding-agent extensions, GSD ecosystem extensions, workflow plugins, skills. This is more surface than the original §1.8 assumption (1) ("at least *some* extension surfaces accommodating uplift content") gave it credit for.
  - Slice 4 Finding 2.7: core GSD itself is an extension. The extension API is product-load-bearing, not third-party afterthought.
  - Slice 4 audit §5 (missed but noted): gsd-2's CONTRIBUTING.md has "Extension-first. Can this be an extension instead of a core change?" as an explicit architecture principle.
  - Capabilities probe §A.8: 25+ bundled workflow templates; tier system with explicit community tier; extension validator (`src/extension-validator.ts`) requires `gsd.extension: true` and forbids bundling `@gsd/*` host packages.
- **Evidence challenging (R2 weaker than original §1.8 framing assumed):**
  - F1: vendored fork + clean-seam-proposed-not-implemented means R2 work targeting `pi-coding-agent` internals is functionally R1-shaped. ADR-010's diagnosis applies to extension authors too: distinguishing what's stable Pi surface vs gsd-2-owned-modification requires file-by-file source reading.
  - W2 dive: markdown-phase workflow plugins are prompt-dispatch, not deterministic — limits the kind of R2 work that can land via this mechanism (any work needing executor-controlled determinism reroutes to yaml-step or out of workflow plugins entirely).
  - F3: machinery-vs-practice on breaking changes means stability claims for any extension surface require source verification, not docs-trust.
- **Implications:** R2 base + primary persists as a working hypothesis but with the mix narrower than assumed. Not all extension surfaces are equally fit for uplift work; the choice between subsystems matters; some uplift work is not naturally R2-shaped at all (see R4).
- **Confidence:** medium-high (substantive evidence both supporting and qualifying).

#### R3 upstream-PR-pipeline (contribute features upstream)

- **Viability: questionable; first-wave evidence is mixed and the contribution-culture probe was incomplete.**
- **Evidence supporting:**
  - CONTRIBUTING.md is structurally rich (slice 4 Q5 fallback): structural requirements include issue-first for new features, ADRs for significant decisions, explicit-disclosure for breaking public API/CLI/config/file-structure changes, conventional commits, single-concern PRs, CI + `npm run verify:pr`, extension-PR specifics.
  - Recent merge commits visible (PR numbers #5080, #5062, #5060, #5055, #5058, #5053 in the last day of visible history per slice 5 (i)) — indicating active PR throughput.
  - Bundled api-breaking-change workflow template + slice 5 Finding 2.3 (staged deprecate-then-remove); the *machinery* is contribution-friendly.
- **Evidence challenging:**
  - F3 / §1.7: machinery-vs-practice gap. CONTRIBUTING asks for `BREAKING CHANGE:` discipline; visible practice has zero such commits. R3 PRs introducing this discipline upstream would be culturally novel.
  - Slice 4 Q5 contribution-culture probe failed (`gh` API errors); deep contribution-culture characterization deferred per `DECISION-SPACE §1.15` B5.
  - `DECISION-SPACE §1.8` assumption (2) ("gsd-2 maintainers are at least open to PRs") is unverified at first-wave depth.
- **Implications:** R3 viability is not first-wave-decidable. Per `DECISION-SPACE §1.8` change-condition #2, if R3 collapses (maintainers non-receptive; unmaintained), R2-only design works as fallback. Whether to launch R3 work requires the deferred contribution-culture probe (per `DECISION-SPACE §1.15` B5 deep probe trigger) before second-wave commits to R3-dependent design.
- **Confidence:** medium-low (probe was light by design; deeper investigation deferred).

#### R4 orchestrate-without-modifying (per framing-widening §1.1)

- **Viability: viable; first-wave evidence supports R4 as a real distinct strategy with strong infrastructure underneath.**
- **Evidence supporting:**
  - Slice 1 Finding 4.4 + slice 3 Q1 + capabilities probe §A.4: `gsd headless` is well-developed — JSON/JSONL/stream-JSON output, exit codes (0/1/10/11), `headless query` for deterministic LLM-free state queries, supervised mode, `--answers`, `--events` filters, max-restarts, resume.
  - Slice 2 Finding 5.8 + capabilities probe §A.8: standalone `@gsd-build/mcp-server` package + `@gsd-build/rpc-client` package — gsd-2 explicitly publishes RPC + MCP integration surfaces. RPC client docs (`packages/rpc-client/README.md`) describe spawning, handshake, prompts, steering, follow-ups, typed events.
  - W2 dive §5: even gsd-2's own workflow templates can only invoke other GSD operations through agent-prompt mediation, which means a substantial range of "uplift" work that *might* be R4-shaped (orchestrate gsd-2 from outside via headless mode + JSON parsing) wouldn't naturally fit R2.
- **Evidence challenging:**
  - The framing-widening's §1.1 own caveat: the line between R2 (configure-with-extensions) and R4 (orchestrate-from-outside) is fuzzy; some specific work could go either way. First-wave doesn't reduce that fuzziness.
  - R4 work doesn't compose with the four parallel extension subsystems' lifecycle — it sits adjacent to them, which means coordination with R2 work needs explicit design.
- **Implications:** R4 deserves explicit naming in the operating frame, not subsumption under R2. Some uplift work is naturally R4 (release-pipeline gating; multi-team release-train coordination; CI integration that calls `gsd headless next` and parses output). Treating these as R2 forces them into a misfitting shape.
- **Confidence:** medium-high.

#### R5 replacement-informed-by (per framing-widening §1.2)

- **Viability: not first-wave-decidable; requires comparison frame first-wave was scoped to exclude.**
- **Evidence supporting (potential):**
  - F1 + §1.1: Pi vendoring entanglement is substantial; ADR-010 describes the diagnosed seam problem as not-yet-solved. If our context's needs require a clean library-style harness, R5 (sibling harness) avoids the entanglement.
  - Capabilities probe §B.7 mismatches: several gaps (RC primitives; release-coordination metadata; structured milestone-release mapping) where gsd-2's approach is composable-from-primitives rather than supported-directly. If our context heavily needs supported-directly primitives in these areas, R5 might be cleaner than R1-R4 work to bend gsd-2.
- **Evidence challenging:**
  - F6: gsd-2 has substantive extension primitives + four parallel surfaces. Sibling-harness approach forfeits this infrastructure.
  - F7: gsd-2's plural agent-runtime contracts (CLI/extension API/skills/MCP/RPC) are well-developed. Building these from scratch is a substantial cost.
  - Framing-widening §10.2 honest test: "does §6.2 dispatch + §7 incubation actually use R5 distinct from R1/R2/R3?" — first-wave evidence by itself doesn't license R5 as primary.
- **Implications:** R5 viability assessment requires the deferred competitor-landscape probe (framing-widening §9 item 3). Without it, R5 is on the table per the widening but cannot be evaluated as peer to R1-R4. The framing-widening's argument for explicit naming holds: a deliberation under R1-R4 will find R1-R4-shaped evidence; R5 needs explicit consideration even when not yet decidable.
- **Confidence:** medium-low (insufficient first-wave evidence to assess; deferred probe needed).

#### Net read on R-strategy mix

- **Compositions that look viable:** R2+R3+R4 mix (the framing-widening's §1.3 "all three" composition); R2+R4 (extension where surfaces fit + orchestration where they don't); R1 narrow-patches + R2 extension (per `DECISION-SPACE §1.8`).
- **Compositions that look unviable:** R3 alone (no evidence yet that maintainers will accept the kind of changes uplift would propose, absent deeper probe); pure-R2 with the assumption that all uplift work fits the extension framework (W2 dive shows markdown-phase prompt-dispatch limits this).
- **Pre-decided in the operating frame:** R2 base + primary; R1 as fallback. Both persist as working hypotheses within the widened R1-R5 space; first-wave evidence narrows R1's case but doesn't flip its disposition; first-wave evidence widens R2's substantive surface but qualifies R2's depth (entanglement; engine-mode constraints).
- **Direction-shifting:** the inclusion of R4 explicitly + the deferred-pending-probe disposition for R5 are net widenings the operating frame should absorb. Whether this changes second-wave-scoping shape is incubation-checkpoint work.

### §2.2 §1.7 metaquestion — direction-shifting evidence summary

Per `INITIATIVE.md §3.1` starter list and beyond:

**Evidence supporting "uplift-of-gsd-2 is the right shape":**

- gsd-2 is a substantive coding-agent application with substantive extension primitives (F6; slice 4 Findings 2.1-2.7; capabilities probe §A.7-§A.8). The "architecturally hostile to long-horizon features" check from `INITIATIVE.md §3.1` starter list does not surface — the architecture is broadly accommodating.
- Pi SDK exposes the extension points uplift would likely need (slice 2 Finding 5.6: extension API supports tools, commands, shortcuts, providers, event handlers, UI primitives). The "Pi SDK doesn't expose extension points" check does not surface as fatal.
- gsd-2's mission ("orchestration layer between you and AI coding agents for planning, execution, verification, shipping" per slice 1 Finding 2.2) has substantive overlap with the uplift goal (long-horizon agential development support). The "mission/scope so divergent that uplift would distort identity" check does not surface as fatal.
- gsd-2 has structural primitives gesturing at long-horizon work: milestone/slice/task hierarchy (slice 1 Finding 1.6); requirement contract artifacts with traceability (slice 5 Finding 3.3; slice 4 Finding 1.5); journal + telemetry + forensics surfaces (F8); team mode with shared/local artifact boundaries (slice 1 Finding 3.4; slice 5 Finding 4.4; capabilities probe §A.6); 22 schema migrations indicating ongoing schema evolution (slice 5 audit §2 — missed `SCHEMA_VERSION = 22`).

**Evidence challenging "uplift-of-gsd-2 is the right shape":**

- F1 + §1.1: Pi vendoring entanglement is more substantial than the operating frame likely assumed. ADR-010's clean-seam refactor is `Status: Proposed`; uplift work lands in the entanglement, not the proposed clean architecture.
- F3 + §1.7 (machinery-vs-practice): release cadence is rapid; breaking-change communication operates outside the formal channels the project has set up. R2 stability claims for any specific extension surface need source verification, not docs-trust. The starter-list check "release cadence makes third-party uplift untenable" partially surfaces (cadence isn't untenable but is fast enough that fork-tracking is real cost).
- F4 + §1.2: markdown-phase workflow plugins are prompt-dispatch only; uplift work needing deterministic execution at this layer hits a real boundary.
- The framing-widening §3.3 "Logan's read of arxiv-sanity-mcp's context might differ" issue: project-anchoring is interpretive (O1); first-wave evidence cannot ground-truth whether arxiv-sanity-mcp's actual harness need is well-served by uplift-of-gsd-2 vs alternative shapes.
- The framing-widening's R5 widening (deferred): "fundamentally simpler shape that meets the goal more directly" check from `INITIATIVE.md §3.1` starter list partially surfaces but cannot be assessed without comparison-frame evidence (O2).

**Evidence orthogonal to the metaquestion:**

- F2 / §1.3: extension-surface plurality. Doesn't directly bear on whether uplift is right shape; it bears on what shape uplift takes if pursued.
- F5 / §1.5: docs-vs-source drift class. Methodological observation about gsd-2's documentation discipline; bears on synthesis confidence calibration but not metaquestion.
- F7-F9: human/agent/machine plurality; observability centrality; security/trust centrality. Each enriches the picture without flipping the metaquestion.

**Synthesis read on the metaquestion:** **direction holds, but the operating-frame shape narrows in important ways.** First-wave evidence does not surface a fatal direction-shifter. It does surface (i) the entanglement is more substantial than assumed, (ii) the engine-determinism boundary partitions the workflow-plugin surface, (iii) the breaking-change machinery-vs-practice gap weakens R2 stability claims for specific surfaces, (iv) R4 deserves explicit operating-frame status, (v) R5 cannot be evaluated without deferred comparison-frame probe.

The metaquestion answer "uplift-of-gsd-2 is the right shape" persists as the operating-frame hypothesis. The qualifier the synthesis adds: which act of uplift (per framing-widening §4 four-act plurality) and which R-strategy mix is right is *not* settled by first-wave evidence — it depends on context-anchoring (O1) and act-selection that maps to subsystem-selection. **Confidence: medium-high on the direction-holds reading; medium on the qualifier-substance.**

### §2.3 Long-horizon framing — six-context plurality (per framing-widening §2)

The question: did first-wave evidence concretize the six contexts (A solo-research / B small-team-product / C larger-team-enterprise / D platform-team / E transition-as-event / F transition-as-stance)?

#### Where gsd-2 currently load-bears on this spectrum (empirical question)

- **Context A (solo-research-tool over years).** Strongly served. Slice 1 Finding 3.3: solo-mode is first-class with sensible defaults (auto-push, worktree isolation). The artifact discipline (milestone/slice/task summaries with provides/requires/affects/key_files/key_decisions/patterns_established/observability_surfaces fields per capabilities probe §A.2) directly addresses Context A's binding constraint of "comprehension-across-time" per framing-widening §3.2.
- **Context B (small-team consumer-facing product).** Partially served. Slice 1 Finding 3.4: team mode exists with explicit setup (unique milestone IDs; push branches; pre-merge checks). Slice 5 Finding 4.4 + capabilities probe §A.6: team-mode primitives are visible. But framing-widening §2.2 + capabilities probe §B.5 mismatches: release-coordination, freeze windows, approver rosters, launch comms, rollout ownership — these are external to GSD artifacts. Team primitives are present but the release-engineering side is composable-from-primitives, not supported-directly.
- **Context C (larger-team enterprise).** Weakly served. Capabilities probe §A.10: write-gate, journal, forensics, secret-scan, destructive-command classifier are present and substantive. But coordination-at-scale tooling (multi-tenant deployment, multiple parallel release branches, regulatory compliance, structured RCAs at scale) wasn't visible in the first-wave reads.
- **Context D (platform-team across organization).** Not visibly served. gsd-2 is itself a tool; it doesn't visibly support the meta-level governance question (cross-team consistency for adopters; version-pinning; org-wide governance).
- **Context E (transition-as-event).** Unprobed. Solo-mode → team-mode transition exists as a configuration toggle but the *transition behavior* — what survives when team-size changes; whether artifact discipline holds across the discontinuity — wasn't probed by first-wave.
- **Context F (transition-as-stance / anticipatory-scaling).** Mixed. gsd-2 has primitives that *could* support anticipatory-scaling (team mode toggle; workflow plugins activatable on demand; modular extensions). Whether the activation transitions are smooth (the binding F demand) wasn't directly tested. Capabilities probe §A.6 docs/source divergence on team `git.isolation` is a small empirical signal that progressive activation is partially documented and partially source-defined; the kind of evidence Context F needs.

#### Where gsd-2 could be made load-bearing through R1-R5 work (counterfactual)

- For Context B: capabilities probe §C.1-C.6 candidates address several gaps (release metadata linked to milestones; semver-aware release plugin; hotfix backport workflow; RC/staging template; release-pipeline headless recipe; release coordination checklist).
- For Context C: substantial expansion needed; no first-wave-evidence-supported low-cost path observed.
- For Context F: progressive-activation work could be substantive — capabilities probe §C.8 (preference-effective-state check in release workflows) addresses the activation-discoverability problem; the framing-widening §9 item 15 ("two-engine progressive activation") flags the markdown-phase/yaml-step distinction as bearing on Context F's progressive-activation demand.

#### Slice 5 + slice 4 + capabilities probe contributions

- Slice 5 (concrete patterns): release cadence + breaking-change posture + 17-feature inventory directly bear on Contexts B/C/E/F (release-coordination demand).
- Slice 4 (extension surfaces): the four-parallel-surface architecture + tier system + community-tier promotion path are Context F primitives — they *could* support progressive activation.
- Capabilities probe §A + §B: the §B.1-§B.7 mappings explicitly assess "supported / composable-from-primitives / not-supported" for release work shapes that span Contexts B/C/E.

#### Synthesis read on the long-horizon axis

**Six-context plurality is concretized partially by first-wave evidence; the framing-widening's argument that the axis is plural-not-singular is supported.** The evidence concretizes:

- Context A is gsd-2's strongest fit (Logan's articulation note about milestone/slice/task discipline explicitly aimed here; per slice 1 Finding 1.6 + framing-widening §2.1).
- Context B is partial — primitives present, release-coordination external.
- Contexts C/D are weakly-or-not served.
- Contexts E/F are interesting cases where primitives exist but transition/activation behavior wasn't directly tested.

The single-axis "long-horizon" framing per `DECISION-SPACE §3.6` collapses these distinctions — Logan's articulation referenced multi-year horizons, multiple milestones, release workflows, complexity scaling, and changing requirements *together*, but they impose different harness demands that the six-context plurality preserves. **Confidence: medium-high on plurality being supported; medium on specific context-concretization (interpretive).**

### §2.4 Project-anchoring (per framing-widening §3)

The framing-widening's §3.1 reading is "arxiv-sanity-mcp primarily Context A with strong Context F secondary." Per framing-widening §3.3 + §10.4, **this is interpretive and Logan's read is binding**. Synthesis can offer evidence-based observations but cannot dispose this question.

#### Does first-wave evidence bear on whether gsd-2 fits primarily-A-with-strong-F well?

Directly: gsd-2's strongest fit appears to be Context A (per §2.3 above). gsd-2 has Context F primitives (modular extensions; activatable workflows; team mode toggle) but the activation-behavior testing wasn't done.

If arxiv-sanity-mcp's anchoring is primarily-A-with-strong-F (the framing-widening's §3.1 read), gsd-2's fit is mostly-good with caveats around progressive-activation (Context F demand). The capabilities probe §C candidates targeting RC/staging/release-coordination would be over-investment for primarily-A-with-strong-F context.

If arxiv-sanity-mcp's anchoring is *not* primarily-A-with-strong-F (e.g., Logan reads it differently per framing-widening §3.3 alternative readings — primary Context F with explicit B aspiration; or Context A with no F aspiration; or Context B-aimed-for-community-adoption), the conclusion differs: Context F-primary anchoring would emphasize gsd-2's modular-surface primitives + progressive-activation testing; Context B-aimed anchoring would re-elevate the §C candidates.

#### Or does evidence point toward a different anchoring?

The framing-widening §3.3 explicitly raises a third reading: "the gsd-2 uplift initiative is for the gsd-2 community more broadly, not specifically for arxiv-sanity-mcp" — under which project-anchoring should be plural across multiple representative user-contexts (per `INITIATIVE.md §3.3` onboarding situations + `DECISION-SPACE §3.8` additional candidates). First-wave evidence does not adjudicate this reading vs the arxiv-sanity-mcp-anchored reading. Both fit the evidence.

**Synthesis read:** **interpretive at appropriate confidence; explicit deferral to incubation-checkpoint.** The framing-widening's §3.1 reading is internally consistent and grounded in observation of arxiv-sanity-mcp's posture (CLAUDE.md, project structure). It is not licensed by first-wave evidence to be authoritative; Logan's disposition at incubation determines anchoring. **Confidence: medium-low (interpretive at load-bearing position — this is Trigger 4 territory).**

### §2.5 §3.2 design-shape candidates (concrete intervention surfaces)

Per `INITIATIVE.md §3.2` (patcher / skills / hybrid / something-else) and the framing-widening's four-act plurality of uplift (modify / configure / orchestrate-around / replace-informed-by): what concrete intervention shapes does first-wave evidence surface as candidates?

This is **surfacing**, not pre-deciding. Second-wave-scoping makes the call.

#### Candidates from capabilities probe §C (gap-anchored)

The capabilities probe surfaced 8 gap-anchored candidates (§C.1-§C.8). Mapped to the four-act plurality:

| Candidate | Targets gap | Four-act mapping | R-strategy mapping | Verified by W2 dive? |
|---|---|---|---|---|
| §C.1 release metadata linked to milestones | B.1, B.6 mismatches | Modify (extension) or Configure (custom workflow) | R2 (workflow plugin) | Partially verified — viable as prose/markdown; refuted as structured linkage without schema (W2 dive §6, §8) |
| §C.2 semver-aware release workflow plugin | B.1 mismatch | Modify (workflow plugin enhancement) | R2 (workflow plugin) | Partially verified — agent-prompted yes; deterministic-executor-owned refuted for markdown-phase (W2 dive §2, §8) |
| §C.3 hotfix branch/backport workflow plugin | B.2 mismatch | Modify (workflow plugin) or Orchestrate (external script) | R2 (workflow plugin) or R4 (external script) | Partially verified — branch creation + agent-prompted procedure yes; programmatic backport invocation refuted (W2 dive §5, §8) |
| §C.4 RC/staging workflow template | B.3 mismatch | Modify (workflow plugin) | R2 (workflow plugin) | Partially verified — viable as prompt/artifact workflow; durable structured RC/soak state needs additional design (W2 dive §1, §4, §8) |
| §C.5 generic release-pipeline headless recipe | B.4 mismatch | Orchestrate (external) or document | R4 | Not directly verified by W2 dive but supported by capabilities probe §A.4 + §C.5 own analysis |
| §C.6 release coordination checklist artifact | B.5 mismatch | Modify (workflow plugin) or Configure (custom artifact) | R2 (template addition) | Not verified |
| §C.7 explicit milestone-release mapping note | B.6 mismatch | Configure (doc convention) or Modify (schema extension) | R2 minor or R3 PR | Not verified |
| §C.8 preference-effective-state check | cross-cutting docs/source drift | Orchestrate (preflight check) or Modify (workflow preflight) | R4 (headless query) or R2 (workflow plugin) | Not verified |

#### Cross-act observations

- Several candidates have natural bifurcation between R2 (modify-via-extension) and R4 (orchestrate-via-headless). E.g., §C.5 release-pipeline recipe is naturally R4; §C.8 preference-effective-state check could be either. The framing-widening's four-act plurality + R1-R5 widening makes this bifurcation visible; the original R1/R2/R3 framing without R4 would have forced these into R2 misfit.
- W2 dive substantially refines what's possible at R2: candidates depending on deterministic execution at markdown-phase mode hit a determinism boundary; candidates that recast as yaml-step have determinism but fewer existing exemplars; candidates that work via prompt-mediation-only retain markdown-phase patterns at the cost of execution non-determinism.
- The four parallel extension subsystems (§1.3) mean different candidates target different subsystems. §C.4 (RC/staging) is naturally a workflow plugin; an uplift skill (per framing-widening §4 act 2 "configure") might address the gap differently; an ecosystem extension might add still different surfaces. Same gap, multiple subsystem-and-act paths.

#### Other candidate shapes evidence supports

- **Long-arc decision-trace artifacts** (per framing-widening §3.2): compose with milestone summaries to support Context A's comprehension-across-time. Evidence: gsd-2's summary fields (capabilities probe §A.2: provides/requires/affects/key_files/key_decisions/patterns_established) suggest the artifact-extension shape is viable.
- **Progressive-activation primitives for Context F**: per framing-widening §9 item 15, the markdown-phase/yaml-step distinction may bear on this. Whether to extend gsd-2 in this direction is Context-anchoring-dependent.
- **Workflow-plugin ecosystem contributions** (per framing-widening §4 act 1 + R3): if R3 collapses on contribution-culture grounds, this redirects to R2 only.

**This is surfacing, not pre-deciding.** Second-wave scoping makes the call about which candidates to pursue, in what mix, and against which context-anchoring. The four-act / R1-R5 / six-context framework gives second-wave a structured space to reason within. **Confidence: medium-high on candidate surfacing; medium on candidate-vs-context fit (depends on §2.4 disposition).**

### §2.6 B4 resolution — slice 5 split

Per `DECISION-SPACE §1.14` (B4): slice 5 was provisionally split — concrete observable patterns in slice 5; abstract long-horizon-relevance interpretation moved to W3 synthesis. **Pilot disposition needed to dispose whether the split holds.**

#### Did the split hold?

Reading slice 5 output: yes. Slice 5 (i)-(v) is purely observational — release cadence math, breaking-change machinery enumeration, multi-milestone artifact concrete-feature inventory, prod/dev distinction observation, 17-feature catalog. Slice 5 (iv) item 2 explicitly defers: "Open question — interpretive; defer to synthesis. Release cadence numbers by themselves require a comparison frame to be meaningful."

Slice 5 audit §3 confirms: "the slice prompt at lines 64-69 specifically directs the agent away from time-horizon characterization ... The slice complies — Finding 5 inventory is purely observational, and the open-questions section explicitly defers interpretation."

The split is intact. Slice 5 produced concrete-observable; abstract long-horizon interpretation is for synthesis to integrate.

#### Does abstract long-horizon-relevance interpretation belong here at synthesis?

Yes (per pilot disposition holding). §2.3 above (six-context plurality) carries the abstract long-horizon interpretation, grounded in slice 5's concrete observations + cross-slice features, applying the framing-widening's six-context plurality.

The integration shape: slice 5's release-cadence + breaking-change + 17-feature inventory feeds into §2.3's mapping of where gsd-2 currently load-bears on the A-F spectrum. Slice 5 (iv) item 8 ("release mechanics and product workflow are tightly interleaved") + slice 5 audit §5 cross-finding flag (machinery-vs-practice) feed §1.4 + §1.7 cross-slice patterns, which in turn ground §2.3's Context B/C/E/F discussions about release-coordination.

**Synthesis read:** the split held; the abstract interpretation lives here at synthesis (per §2.3 and §1.4 + §1.7 cross-slice patterns) where it can be integrated with cross-slice context. The framing-widening's six-context plurality is the structured space within which the abstract interpretation is articulated. **Confidence: high.**

---

## §3. Slice contradictions

Where slice X says something slice Y says differently. Flagged concretely; not papered over.

### §3.1 Machinery-vs-practice on breaking-change communication (cross-finding pattern within slice 5)

This is technically *cross-finding within slice 5* rather than *cross-slice*, but the slice 5 audit §5 explicitly directed integration to synthesis (D3) and the pattern bears on cross-slice readings of stability/durability for any R2 work.

- **Slice 5 says (machinery side):** Findings 2.1 (CONTRIBUTING contributor policy requires explicit signposting), 2.2 (release-note format includes Deprecated/Removed categories), 2.3 (api-breaking-change workflow template with staged deprecate-then-remove process), 2.4 (release tooling recognizes semver-major triggers via `BREAKING CHANGE` / `!:`), 2.5 (in-code deprecation markers exist).
- **Slice 5 says (practice side):** Findings 2.6 (observed practice includes both staged deprecation and removal-style changes without visible pre-deprecation in shallow history), 2.7 (visible commit/release messages do not consistently use explicit "breaking" wording for removals — zero `BREAKING CHANGE` commits in 6-month visible window per slice 5 audit spot-check 7), 4.5 (experimental preferences explicitly waive deprecation cycle).
- **Audit findings:** slice 5 audit §5 explicitly named this pattern + flagged for synthesis (D3 directed to synthesis).
- **Resolution at synthesis:** The pattern integrates as direction-shifting evidence (F3) per §1.7 — gsd-2 has elaborate breaking-change machinery but operates via narrative-changelog discipline rather than convention-enforcement. Whether this is feature (intentional informality) or transition state (project moving toward convention enforcement; visible window catches mid-transition) is unresolved at synthesis (O3) and would need deeper history sampling. **Bears on §2.1 R2/R3 viability + §2.5 design-shape candidates depending on stable extension surfaces.**

### §3.2 Docs-vs-source RTK gating divergence (consistent across slices)

- **Slice 1 (v) says:** README claims RTK is provisioned for shell-output compression with `GSD_RTK_DISABLED=1` to disable; source shows RTK opt-in via `experimental.rtk` (default disabled).
- **Slice 2 (v) + Finding 1.8 says:** same finding; verbatim README quote vs verbatim cli.ts behavior.
- **Slice 3 (v) says:** same finding (RTK default posture appears overstated in README).
- **Slice 4 doesn't address:** out of slice scope.
- **Slice 5 doesn't address:** out of slice scope.
- **Audit findings:** slice 2 audit spot-check 3 verified the divergence verbatim; flagged as concrete README/source tension.
- **Resolution at synthesis:** **convergent across three slices**, no contradiction. This is a real concrete divergence, audited. The reading slice 2 surfaces — "the README may be describing provisioning, not activation — i.e., the install script does provision the binary, but the runtime flag does not flip on without `experimental.rtk`" — is the most charitable read. Even under this reading, it's a concrete divergence between README and source, and a representative case for the broader docs-vs-source-drift pattern (§1.5).

### §3.3 The boundary-map docs/migrator skip (within slice 4)

- **Slice 4 Finding 1.5 says:** GSD-WORKFLOW.md schemas show milestone roadmaps include a `Boundary Map` section; migration writer at `migrate/writer.ts:140` explicitly skips boundary map "per D004" with no migrator emission.
- **Audit findings:** slice 4 audit spot-check 3 verified verbatim; flagged as documented-but-not-emitted.
- **Resolution at synthesis:** **internal docs/source tension within gsd-2.** Same class as the RTK divergence — the documented format includes a section the migration tooling skips. Bears on uplift work that depends on standard artifact emission (any uplift artifact-shape that requires Boundary Map presence has to verify at runtime, not from docs).

### §3.4 Reassess-after-slice default (slice 1 + slice 3)

- **Slice 1 (v) says:** README's main loop includes `Reassess Roadmap` and describes adaptive replanning after each slice; source `auto-dispatch.ts` defaults dedicated reassessment to off unless `prefs.phases.reassess_after_slice` is true.
- **Slice 3 (v) says:** "Roadmap reassessment docs appear potentially tensioned" — README presents reassessment as automatic; configuration docs say slice-level reassessment requires `reassess_after_slice: true`.
- **Audit findings:** not specifically spot-checked but consistent with the docs-vs-source pattern slice 2 audit verified.
- **Resolution at synthesis:** **convergent across two slices** as a docs-vs-source divergence; another instance of §1.5 pattern.

### §3.5 Verification scope (slice 3 vs README)

- **Slice 3 (v) + Q2 finding says:** README presents "automated verification commands with retry/fix loops"; source post-unit verification is explicitly scoped to `execute-task` units with separate behavior for validation milestones.
- **Resolution at synthesis:** scope-narrowing rather than hard contradiction; the slice itself frames it that way. Another instance of the docs-vs-source-simplification pattern.

### Pattern across §3.1-§3.5: the docs-vs-source-drift class

Five distinct cases (machinery-vs-practice; RTK; boundary-map; reassess-default; verification scope) all exhibit the same shape: docs/README make a more-general claim than source-observable behavior supports, with source gating the behavior on preferences/modes/scope conditions. This is §1.5 — a class of finding, not single instances.

**Implication for synthesis confidence calibration:** any synthesis claim resting on README/docs alone (without source verification) inherits this drift risk. The first-wave slices were designed with source-as-ground-truth discipline; this synthesis inherits source-grounded claims at high confidence and docs-anchored claims at calibrated lower confidence.

---

## §4. Open questions surfaced

Beyond the existing §3 framing questions in INITIATIVE.md and the framing-widening §9 deferred items log. Each: question; why open at synthesis stage; what would resolve.

### §4.1 The provenance-mapping question (within pi-coding-agent)

- **Question:** how much of `pi-coding-agent` is original Pi vs GSD-authored, and how does this change which extension API surfaces are stable to build R2 on?
- **Why open:** ADR-010 reports ~79 GSD-authored files inside `pi-coding-agent` per slice 2 Finding 2.1 + audit spot-check 1. First-wave didn't perform file-by-file provenance classification (slice 2 Finding 2.6 explicitly defers).
- **What would resolve:** file-by-file provenance map; or alignment with ADR-010's proposed clean seam if the seam refactor lands; or a "this is the stable surface" doc commitment from gsd-2 maintainers (R3-adjacent).
- **Why this matters for incubation:** R2 work targeting pi-coding-agent internals has different stability properties than R2 work targeting bundled GSD extensions. Without provenance map, R2 work is uniformly cautious; with map, some surfaces could be classified safe-to-extend and others risky.

### §4.2 The two-engine fitness for progressive activation

- **Question:** do markdown-phase and yaml-step compose into a smooth Context F progressive-activation story, or do they bifurcate the workflow surface in a way that complicates progressive uplift adoption?
- **Why open:** framing-widening §9 item 15 flagged this as synthesis-stage; W2 dive established the architectural distinction but didn't probe progressive-activation behavior.
- **What would resolve:** scenario probe — design a progressive-activation flow (e.g., team starts Context A with markdown-phase release; transitions to Context B needing yaml-step deterministic verification) and trace whether the transition is smooth.
- **Why this matters for incubation:** if progressive activation is a binding Context F demand and the two-engine architecture complicates it, R2 work touching workflow plugins faces a structural choice (commit to one engine; design across both).

### §4.3 The 22-schema-migration history as drift signal

- **Question:** does gsd-2's `SCHEMA_VERSION = 22` history signal stable evolution, instability, or something else relevant to durability of any uplift schema additions?
- **Why open:** slice 5 audit §2 noted the missed citation; first-wave didn't explicitly characterize migration history. 22 migrations could mean (a) careful evolution with backward-compat through migrations, or (b) churn. Different implications for any R2 work that adds schema fields.
- **What would resolve:** sampling specific migrations + characterizing change types (additions, renames, removals, restructures) over recent versions.
- **Why this matters for incubation:** uplift work that adds artifact schema fields lands in a 22-migration history; whether the historical pattern is additive-stable or restructuring-frequent shapes design.

### §4.4 Whether the "core gsd is itself an extension" reading is fully load-bearing

- **Question:** is the bundled-GSD-as-extension architecture a strong signal for R2 viability, or a developer-convenience-pattern that doesn't extend cleanly to third-party extension authors?
- **Why open:** slice 4 Finding 2.7 + slice 4 audit §5 flagged this strongly. But "core gsd extension is bundled and registered first; non-critical registrations wrapped to fail-gracefully" (slice 4 Finding 2.7) reads as having privileged access to internals (registers worktree commands, exit handling, hook emission, ecosystem loaders). Whether third-party extensions have equivalent access or whether some surfaces are core-only-effective wasn't probed.
- **What would resolve:** trace specific registration paths in core-vs-third-party comparison; check for `internal` markers or core-only extension capabilities.
- **Why this matters for incubation:** R2 viability assessment depends on whether the third-party extension surface is comparable to the bundled one. If yes, R2 is strong; if no, R2 has a privileged-tier-only ceiling.

### §4.5 What the "shallow-clone visible window" hides

- **Question:** does the 6-month visible window represent the project's stable cadence/practice, or is it a transition state we're catching mid-evolution?
- **Why open:** slice 5 throughout — preflight notes shallow-clone; cadence/breaking-change practice claims are explicitly window-bounded.
- **What would resolve:** deepening the clone (per slice 5 (iv) item 1); historical stability comparison.
- **Why this matters for incubation:** if the machinery-vs-practice gap (F3) is a transition state, R3 strategy may align with project trajectory; if it's a stable feature, R3 may be culturally novel.

### §4.6 Whether reusability scope breadth is decidable from current evidence

- **Question:** per `DECISION-SPACE §1.8` assumption (3) — "reusability across projects is a load-bearing goal" — does first-wave evidence support how broadly the uplift package needs to be reusable?
- **Why open:** capabilities probe §A.6 + slice 5 Finding 4.4 (mode defaults divergence; team mode primitives) shows team-mode is partially documented and partially source-defined. This bears on adopter experience and reusability fit.
- **What would resolve:** the deferred user-side adoption-pattern probe (framing-widening §9 item 6).
- **Why this matters for incubation:** §3.3 onboarding situations + §3.8 additional candidates list spans a broad reusability scope; whether all are in v1 scope or only some bears on second-wave-scoping shape.

---

## §5. Recommendations for incubation-checkpoint

Per `DECISION-SPACE §2.3`, the checkpoint:
- Re-reads goal articulation.
- Checks direction-shifting evidence per `INITIATIVE.md §3.1` starter list and beyond.
- Checks whether R-strategy hybrid (now R1-R5) has narrowed.
- Decides whether second-wave proceeds or re-disposition needed.

Synthesis-level recommendations for what to look at and why:

### §5.1 Explicit disposition on project-anchoring (O1)

The framing-widening §3.3 raises three readings of arxiv-sanity-mcp's anchoring:
- Primary Context A with strong Context F secondary (the framing-widening's §3.1 read).
- The uplift initiative serves the gsd-2 community more broadly; project-anchoring should be plural across multiple representative user-contexts.
- A different anchoring entirely (e.g., primary F with explicit B aspiration).

First-wave evidence cannot dispose this. Logan's read is binding. **Recommendation:** explicit disposition at incubation-checkpoint before second-wave-scoping commits to a context-mix. The synthesis carries the framing-widening's §3.1 reading as one option but does not endorse it as authoritative.

### §5.2 Decide on R5 viability assessment path

R5 cannot be evaluated from first-wave evidence (O2). Three paths at incubation:
- Defer R5 evaluation to second-wave, accepting the deliberation proceeds under R1-R4 with R5 explicitly named-but-unassessed.
- Dispatch the deferred competitor-landscape probe (framing-widening §9 item 3) before second-wave-scoping commits.
- Accept R5 as not-decidable and proceed under R1-R4-only operating frame.

**Recommendation:** the framing-widening's argument for explicit naming of R5 is structural — without explicit consideration, R1-R4 work finds R1-R4 evidence. If the competitor-landscape probe is cheap relative to second-wave-scoping commitment, dispatch before scoping. If expensive, name R5 as a parking-lot consideration to revisit if second-wave evidence accumulates pointing toward sibling-harness shape.

### §5.3 Decide on the deferred contribution-culture deep probe (R3 viability)

Slice 4 Q5 contribution-culture probe failed (`gh` API errors). Per `DECISION-SPACE §1.15` B5, deep probe is conditional on R2 viability per slice 4. R2 looks viable per F6 + §2.1; this triggers the deep probe trigger.

R3 viability is the gating question for whether design proceeds on R2-only or R2+R3 mix. F3's machinery-vs-practice gap suggests R3 may be culturally novel.

**Recommendation:** deep contribution-culture probe is the highest-priority deferred item from `framing-widening §9` for second-wave-scoping shape. Dispatch before scoping if scoping commits to R3 work; defer if scoping operates as if R3 is bonus.

### §5.4 Decide whether two-engine-progressive-activation matters for second-wave scope

Per §4.2 + framing-widening §9 item 15. If Context F is a binding constraint for the chosen anchoring, this matters; if not, it doesn't.

**Recommendation:** condition this on §5.1 disposition. If anchoring is Context A primary with no F, deprioritize. If Context F is load-bearing, this question is on critical path.

### §5.5 Re-read goal articulation against the §1.7 machinery-vs-practice finding

`INITIATIVE.md §1` framing emphasizes "harness & thus agential development more robust and better over much longer horizons of development." gsd-2's machinery-vs-practice gap on breaking-change communication (F3 / §1.7) is itself a long-horizon-development issue — discipline that exists on paper but doesn't operate is a specific failure mode that long-horizon work should address.

**Recommendation:** explicit incubation-stage consideration of whether the uplift goal includes addressing machinery-vs-practice gaps in the harness itself, or whether it operates within whatever practice the harness exhibits.

### §5.6 Apply the dispatching-project's anti-pattern self-check to operating-frame disposition

Per `AGENTS.md` "Project-specific anti-patterns to detect":

- **Tournament narrowing:** the original R1/R2/R3 framing implicitly narrowed away R4 + R5; the framing-widening corrected this. Incubation should check whether the synthesis's R-strategy mix recommendations themselves are tournament-narrowing in some other way (e.g., did synthesis exclude any composition that has standing?).
- **Closure pressure at every layer:** synthesis is structurally susceptible to producing tidy framings under load-bearing pressure. The §0 escalation flag + paired-synthesis trigger acknowledge this; cross-vendor synthesis comparison would test whether this synthesis carries closure-pressure smoothing.
- **Single-reader framing claims as authoritative:** the framing-widening's §3.1 project-anchoring is single-reader interpretive — synthesis carries this without endorsing as authoritative (per §2.4); incubation should explicitly verify this is held interpretive.
- **Single-lens "interface" by accident:** the four-act / R1-R5 / six-context / four-surface plurality framework should not collapse during incubation into a single dimension; that would re-narrow what the framing-widening worked to widen.

**Recommendation:** these are checklist items for incubation deliberation, not synthesis commitments. The synthesis flags them; incubation applies them.

### §5.7 Specific deferred-items-log items synthesis surfaced as load-bearing for incubation

Per framing-widening §9, the following deferred items are flagged as load-bearing for incubation-checkpoint:

- **§9 item 3 (competitor-landscape probe):** load-bearing for §5.2 (R5 viability).
- **§9 item 6 (user-side adoption-pattern probe):** load-bearing for §4.6 (reusability scope).
- **§9 item 5 (temporal-stability probe):** load-bearing for §4.1 + §2.1 R2 viability — whether specific extension surfaces are stable enough to build on. F3 + §1.7 (machinery-vs-practice) sharpens this.
- **§9 items 7-8 (methodology codification):** the dispatching-session pattern of wave-structure-on-large-targets has reached the ~3-sample threshold per tier-comparison preliminary §7. Codification is timely.
- **§9 item 12 (telemetry/observability as design-surface):** confirmed central by F8 + cross-slice watchlists. Synthesis-stage; incubation should consider whether design-shape candidates that touch observability are part of v1 or deferred.
- **§9 item 14 (solo-to-team transition coherence):** O1 + §2.3 + §4.2 surface this; load-bearing for Context F-anchored uplift.
- **§9 item 15 (two-engine progressive activation):** §4.2 + §5.4.

**Recommendation:** incubation-checkpoint reviews these explicitly rather than treating them as background.

---

## §6. Confidence and limits

### §6.1 What synthesis couldn't resolve

- O1 (project-anchoring) — interpretive; Logan's read is binding.
- O2 (R5 viability) — requires comparison-frame evidence first-wave excluded.
- O3 (machinery-vs-practice as feature or transition) — requires deeper historical sampling.
- O4 (four-act / four-surface mapping) — interpretive integration call.
- §4.1-§4.6 open questions surfaced but not addressed (provenance mapping; two-engine progressive activation; schema-migration drift signal; bundled-GSD-as-extension load-bearing-ness; shallow-clone window; reusability scope decidability).

### §6.2 What would need a second wave or different exploration shape

- Deep contribution-culture probe before R3-dependent design (§5.3).
- Competitor-landscape probe before R5 evaluation as peer to R1-R4 (§5.2).
- Provenance-mapping probe before R2 work targets pi-coding-agent internals (§4.1).
- Progressive-activation scenario probe before Context F-anchored design commits (§4.2).
- Deeper history sampling before durability claims about machinery-vs-practice gap (§4.5).
- Light user-adoption-pattern probe before reusability-scope commitments (§4.6).

### §6.3 Is first-wave evidence sufficient for incubation-checkpoint to operate cleanly?

**Yes, with explicit disposition discipline.** First-wave evidence:
- Confirms gsd-2 is a substantive characterizable substrate (not architecturally hostile to uplift).
- Does not surface fatal direction-shifters for the metaquestion's "uplift-of-gsd-2" answer.
- Concretizes the framing-widening's R1-R5 + six-context + four-act pluralities.
- Surfaces real qualifications to the operating frame (entanglement; engine-determinism boundary; machinery-vs-practice gap; R4 explicit; R5 deferred) that incubation can dispose.

What incubation needs that synthesis can't supply: project-anchoring disposition (O1); the deferred probes (§5.2, §5.3, §4.6) if their gating questions are on second-wave-scoping critical path; Logan's read on whether the machinery-vs-practice gap (§5.5) bears on uplift goal articulation.

**Synthesis read on whether additional first-wave exploration is warranted:** **no, additional first-wave exploration is not necessary before incubation can operate.** The deferred probes are load-bearing for *second-wave-scoping*, not for incubation-checkpoint deliberation; incubation can dispose them as "dispatch-before-scoping" or "defer-as-parking-lot." **Confidence: medium-high.**

### §6.4 Same-vendor framing-leakage caveat

This synthesis is single-author Claude Opus xhigh, same-vendor relative to the W2 audits and the framing-widening's authorship. Audit verified slice register at audit stage; this synthesis applies in-house framing (R1-R5; six contexts; four-act plurality) from the framing-widening to slice and audit content.

**Where in-house framing might be over-fitting cross-vendor observations:**

- The R1-R5 + four-act + six-context + four-surface pluralities are dispatching-project framings (framing-widening). Slice content (codex GPT-5.5 high) doesn't carry these vocabularies; this synthesis applies them. If the framing-widening's pluralities themselves over-fragment what's in evidence, this synthesis inherits that over-fragmentation.
- The "machinery-vs-practice" framing for §1.7 is the slice 5 audit's framing (Claude Opus xhigh same-vendor). Synthesis carries it forward. A cross-vendor synthesis might frame the gap differently (e.g., "narrative-changelog-discipline as alternative to convention-enforcement" — same observation, different normative frame).
- §2.4's project-anchoring deference to Logan is appropriate but inherits the framing-widening's framing of which contexts to consider. A cross-vendor synthesis might surface different contexts.
- §2.5's design-shape candidates inherit the four-act plurality. A cross-vendor synthesis might reframe candidates differently (e.g., as workflow-vs-skill-vs-extension distinctions per gsd-2's own subsystem vocabulary, rather than per the four-act framework).

**Where this synthesis is grounded against in-house framing leak:**

- Source-grounded findings (F1, F2, F4, F5; §1.1, §1.2, §1.3, §1.5) are concrete and would survive cross-vendor synthesis.
- Audit-verified spot-checks (vendoring; ADR-010 status; RTK divergence; in-process MCP; pi-coding-agent description; boundary-map skip; alias telemetry; MCP alias deprecation; cadence math; tag math) are concrete.
- The four-extension-subsystem enumeration is source-grounded via the slice 4 audit's named files.

**Net read:** cross-vendor synthesis would likely converge on the source-grounded findings; the interpretive integration applying R1-R5 / four-act / six-context / four-surface frameworks is where divergence is most likely. This is exactly Trigger 4 territory and motivates the escalation flag in §0. **Confidence: medium-high on caveat-shape; medium on caveat-magnitude.**

---

## §7. Single-author + same-vendor caveat

This synthesis is a same-vendor (Claude Opus xhigh) reading of the slices and audits. Same-vendor framing-leakage caveat applies per §6.4. Per the dispatching session's pre-flag, Trigger 4 was structurally likely; per this synthesis's §0 escalation evaluation, Trigger 4 fires (confirmed) and Triggers 2 + 3 plausibly fire.

The escalation_to_paired_synthesis flag in frontmatter is `yes`. A cross-vendor synthesis (codex GPT-5.5 at appropriate tier per `DECISION-SPACE §1.13` B3 escalation-stage decision) is warranted before incubation-checkpoint reads from synthesis. The comparison artifact (paired-synthesis comparison) is the substantive output; this single-author synthesis is one input to that comparison.

If paired-synthesis is dispatched and the comparison surfaces material divergences, those divergences should be incorporated into incubation-checkpoint inputs alongside this synthesis. If the comparison shows convergence on substantive findings with divergence only on interpretive-framing, the framing-divergence itself is incubation-relevant evidence (per the framing-widening's argument that decision-spaces should not narrow without evidence).

---

*Single-author first-wave synthesis written 2026-04-28 by Claude Opus xhigh general-purpose subagent at the dispatching session's direction. Subject to the same fallibility caveat as `DECISION-SPACE.md §0` and predecessor logs. Per `synthesis-spec.md §"Paired-synthesis escalation criterion"`, escalation flag is `yes`. Synthesis is the load-bearing input for incubation-checkpoint per `DECISION-SPACE §2.3`; paired-synthesis comparison (if dispatched) is the material that incubation reads alongside this artifact.*
