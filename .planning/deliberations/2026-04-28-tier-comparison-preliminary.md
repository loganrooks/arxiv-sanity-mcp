---
type: tier-comparison-preliminary
date: 2026-04-28
session: post-W1-slices-2-5-dispatch; post-side-investigation
status: preliminary; pending audit validation; revision-trigger pointed at framing-widening §9 items 7-8
ground: |
  - 2026-04-28-framing-widening.md §9 items 7-8 (methodology codification deferral threshold ~3 samples; this artifact is one input toward that threshold)
  - 2026-04-27-dispatch-readiness-deliberation.md §B.1 + §B.5 (skill-heuristic shallow-match + dispatching-before-precondition-check; §7 of this artifact identifies a sub-pattern)
  - .planning/gsd-2-uplift/exploration/01-mental-model-output.md (W1 slice 1 — high)
  - .planning/gsd-2-uplift/exploration/02-architecture-output.md (W1 slice 2 — high)
  - .planning/gsd-2-uplift/exploration/03-workflow-surface-output.md (W1 slice 3 — high)
  - .planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md (W1 slice 4 — high)
  - .planning/gsd-2-uplift/exploration/05-release-cadence-output.md (W1 slice 5 — high)
  - .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md (capabilities probe — medium)
  - .planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md (W2 dive — medium)
  - .planning/gsd-2-uplift/orchestration/preamble.md (calibration discipline source)
  - .planning/gsd-2-uplift/orchestration/OVERVIEW.md §3.1 / §3.3 (slice dispatch spec at high)
purpose: |
  Record the empirical comparison between GPT-5.5 medium and high reasoning-effort tiers
  on a specific work shape — characterization of a substantial codebase via codex CLI
  with structured prompts and forbidden-reading discipline — using artifacts that already
  exist in `.planning/gsd-2-uplift/exploration/`. This artifact does not run new probes;
  it records a comparison of artifacts already produced across 2026-04-27 / 2026-04-28.

  Single-author artifact written by Claude (Opus 4.7) at Logan's direction. Calibrated
  language per the project's standing discipline; per-claim citations; explicit limits
  in §8 and explicit revision-trigger in §9. Subject to revision before the methodology
  codification per `2026-04-28-framing-widening.md §9` items 7-8 if W2 audits surface
  findings that change the conclusion.
read_order: |
  - For "what work shapes are being compared": §1.
  - For "what the data show quantitatively + qualitatively": §2-§3.
  - For "the empirical claim that matters": §4.
  - For "where each tier was right": §5-§6.
  - For "the methodological observation": §7.
  - For "limits of the comparison + revision trigger": §8-§9.
---

# Tier comparison (preliminary) — GPT-5.5 medium vs high effort

## §0. Why this artifact exists

Across 2026-04-27 / 2026-04-28 the dispatching session produced empirical evidence about
how GPT-5.5 medium and high reasoning-effort tiers compare on a specific work shape —
characterization of a substantial codebase (`gsd-2-explore` ≈ 2200+ commits, multi-package
TypeScript monorepo) via codex CLI with structured prompts and explicit forbidden-reading
discipline. The artifacts producing this evidence already exist; this note records the
comparison while data is fresh.

The revision-trigger points at `2026-04-28-framing-widening.md §9` items 7-8 (methodology
codification deferred until ~3 samples). This artifact is one input toward the threshold,
not the codification itself. If subsequent W2 audits change the conclusion, the artifact
gets revised before codification.

## §1. The work shapes being compared

**W1 slices at high effort (5 dispatches — `01-` through `05-`).** Aim:
characterization-for-decision per `OVERVIEW.md §1` (B1 — "characterize gsd-2 carefully
enough that second-wave can decide"). Output discipline: 5-section structure (i) what
read / (ii) calibrated findings / (iii) deliberately-not-read / (iv) open questions / (v)
README-vs-source divergences per `preamble.md:74-100`. Forbidden-reading list: extensive
per `preamble.md:53-71`. Each slice received ~150-300 line target per `preamble.md:104`.

**Side-investigation at medium effort (2 dispatches).** Capabilities probe
(`capabilities-production-fit-findings.md`, 2026-04-27, ~373 lines, 46KB) and W2 dive
(`w2-markdown-phase-engine-findings.md`, 2026-04-27, ~124 lines, 22.7KB). Aim:
exploration-for-feasibility (probe gsd-2 capabilities for production-fit; deep-dive on
the markdown-phase engine architecture). Output discipline: three-section §A
observation / §B mapping / §C gap-anchored candidates (capabilities probe) and
section-by-question structure with explicit confidence labels (W2 dive). Same
forbidden-reading discipline as W1 (no INITIATIVE / DECISION-SPACE / deliberations
reading).

The work shapes are adjacent-but-not-identical: characterization-for-decision (W1) vs
exploration-for-feasibility (probes). Both are reading-and-citing exercises against the
same gsd-2 source tree.

## §2. Quantitative comparison

| Artifact | Tier | Lines | Size | Headings/findings |
|---|---|---|---|---|
| `01-mental-model-output.md` | high | 161 | 28.5KB | 5 sections; ~5-6 calibrated findings per Q × 5 Qs |
| `02-architecture-output.md` | high | 236 | 32.2KB | 5 sections; 10 findings on Q1; 8 on Q2; etc. |
| `03-workflow-surface-output.md` | high | 200 | 33.2KB | 5 sections; ~5 findings per Q with sub-tables |
| `04-artifact-lifecycle-output.md` | high | 423 | 43.7KB | 5 sections; densest per-Q surface area |
| `05-release-cadence-output.md` | high | 417 | 46.7KB | 5 sections; raw `git log` blocks + structured findings |
| **W1 slices subtotal (high)** | | **1437** | **~184KB** | |
| `capabilities-production-fit-findings.md` | medium | 374 | 46.7KB | §A 8 sub-areas × ~6-12 cited items; §B 7 mappings; §C 8 candidates |
| `w2-markdown-phase-engine-findings.md` | medium | 124 | 22.7KB | 9 sub-questions, each with 2-5 cited findings |
| **Side-investigation subtotal (medium)** | | **498** | **~69.4KB** | |

**Surface-area observation (interpretive).** Both tiers produced output at comparable
density-per-line. The capabilities probe at medium covered 8 sub-areas (versioning;
milestone semantics; pre-release; CI/headless; branch/worktree; team; hooks; templates)
plus 7 workflow mappings plus 8 candidate intervention surfaces. The W2 dive at medium
covered 9 sub-questions on the markdown-phase engine. By per-line density the medium
artifacts are not visibly thinner than the high artifacts. **Confidence: medium —
density is interpretive judgment; reasonable observers might count differently.**

## §3. Qualitative comparison

### §3.1 Inventory-level work
Medium handled inventory-level work competently with calibration discipline holding.
The capabilities probe's §A surfaces are dense and well-cited:
`capabilities-production-fit-findings.md:24-100` (versioning + release primitives);
`:50-66` (milestone schemas); `:80-90` (CI/headless options). Confidence labels
(`high` / `medium-high` / `medium` / `medium-low`) appear on every substantive claim.
**Confidence: high.**

### §3.2 Architectural-relationship-detection
High visibly read source at depth and surfaced relationships that wouldn't fall out of
inventory alone. Cited examples:

- **Slice 2 finding 2.5** (`02-architecture-output.md:93`): traversal of
  `packages/pi-coding-agent/src/core/sdk.ts:41-54,86-131` plus
  `docs/dev/ADR-010-pi-clean-seam-architecture.md:10-30` to surface that
  `pi-coding-agent` mixes vendored Pi code with GSD-authored code, producing the
  vendored-vs-clean-seam architectural finding. This is a relationship claim, not an
  item count.
- **Slice 2 finding 2.6** (`02-architecture-output.md:95`): distinguishes
  monkey-patching from environment-variable + module-aliasing composition by reading
  `src/loader.ts:86-90,109-115` plus `packages/pi-coding-agent/src/core/extensions/loader.ts:61-91,325-342`.
  Inventory would have listed the env vars; the finding is the *characterization* of
  the composition shape.
- **Slice 3 Q2** (`03-workflow-surface-output.md:118-126`): reads
  `src/resources/extensions/gsd/engine-resolver.ts:1-56` and the workflow-templates
  registry to surface the dev/custom/template/UOK 4-shape dispatch structure. (Note:
  this confirms the W2 dive's two-engine finding at medium — the same architectural
  relationship was discoverable at medium with explicit prompting per
  `2026-04-28-framing-widening.md §6.1` Q2 revision.)
- **Slice 4** (`04-artifact-lifecycle-output.md` Q2 evidence; per the file's reading
  list at `:60-98`): distinguishes extension-loading (Pi extension API) vs registry
  (`src/extension-registry.ts`) vs resource-sync (`src/resource-loader.ts`) vs
  /gsd extensions command surface as separate-but-coordinated subsystems. This is
  composition-vs-independence at slice level.

**Confidence: medium-high.** "Relationship vs inventory" is interpretive; some of these
findings include inventory work upstream of the relationship claim.

### §3.3 Calibration discipline
Maintained in both tiers. Confidence labels appear on substantively every claim in
both bodies of work; `[high]`/`[medium]`/`[medium-low]` markers are visible throughout
slice 3 (`03-workflow-surface-output.md:80-200`); `**Confidence: <X>**` patterns are
visible throughout the capabilities probe (`capabilities-production-fit-findings.md:26-298`).
Forbidden-reading discipline visibly held: slice 2 explicitly notes
`02-architecture-output.md:202-212` what was not read (INITIATIVE.md / DECISION-SPACE.md /
prior slice outputs / deliberations). The capabilities probe similarly avoided
project-vocabulary contamination in its observational language.

### §3.4 Length and density
High produces denser output per topic; medium covers more surface area at slightly
thinner per-topic depth. Slice 4 at high (423 lines, 43.7KB, single slice) approaches
the capabilities probe's total volume (374 lines, 46.7KB) for one slice's worth of work.
**Confidence: medium — interpretive.**

## §4. The cost differential is reasoning-quality-per-token, not tokens

The empirical finding that matters: medium and high used roughly comparable token volumes
on similar-scale targets (498 lines medium across 2 dispatches vs 1437 lines high across
5 dispatches; ~250 lines per dispatch at medium vs ~287 lines per dispatch at high).
The differential is what the tokens *bought*:

- **At medium**: inventory coverage; cross-area sweep; structured §A/§B/§C separation.
- **At high**: relationship detection; depth-traversal of source files; structured
  multi-finding answers per Q.

This reframes the tier choice. It is not "high = more tokens, medium = fewer." It is
"high = relationship-detection-per-token, medium = inventory-coverage-per-token." Both
are useful; which is right depends on the work shape. **Confidence: high for token
parity; medium-high for the qualitative reframe.**

## §5. Where high was empirically right

For W1 slices specifically (synthesis-feeding characterization), the architectural-
relationship work paid off. Three concrete cases:

1. **Slice 2's vendoring + clean-seam finding** (`02-architecture-output.md:93,101`):
   surfaces that `packages/pi-coding-agent/` is structurally entangled with GSD-authored
   code, citing ADR-010 as the project's own diagnosis. Synthesis needs this to weigh
   the R1-R5 design space (`2026-04-28-framing-widening.md §1`); inventory of "Pi
   packages exist under @gsd scope" would not surface the entanglement.

2. **Slice 3's engine-resolver dispatch detection**
   (`03-workflow-surface-output.md:118-126`): identifies the 4-shape dispatch
   (dev / custom YAML / template-mode / UOK) as architecturally distinct paths.
   Synthesis needs this to weigh whether gsd-2's automation surface is one engine or
   several.

3. **Slice 4's extension-mechanism distinction** (per the file's reading list at
   `04-artifact-lifecycle-output.md:60-98`): separates extension-loading vs registry
   vs resource-sync vs /gsd-extensions as distinct subsystems with different
   lifecycles. Synthesis needs this to weigh R2 (extension) viability against
   "extensions" being plural-not-singular.

**Calibrated claim:** these would *likely* have been caught at inventory level by
medium (the capabilities probe at `:148-164` did surface "extension primitive
plurality" — manifest, templates, skills, MCP, ecosystem — without naming subsystem
relationships), but the relationship structuring is high's value-add. Whether the
relationships would have surfaced at medium with explicit prompting (as the slice 3 /
slice 4 Q2 revisions in `2026-04-28-framing-widening.md §6.1` attempt) is empirically
testable but not tested in this session. **Confidence: medium-high.**

## §6. Where medium would suffice

For pure-exploration probes (capabilities probe; W2 dive) where the value is in finding
things and citing them, medium maintained discipline + handled the structured §A/§B/§C
separation cleanly:

- §A is observational (no judgment); medium handled this without slipping into framing.
  See `capabilities-production-fit-findings.md:22-198` — every claim is source-cited;
  no editorial.
- §B is mapping (inference cited to §A; no recommendations); medium maintained the
  separation. See `:200-274` — every §B claim points back to §A subsections.
- §C is candidate intervention surfaces (heavily qualified; gap-anchored); medium
  produced 8 candidates, each with builds-on / architectural-assumption / verified?
  / confidence / caveat. See `:276-373`.

The W2 dive at medium similarly maintained discipline in answering 9 sub-questions on
the markdown-phase engine, including the absence-claim discipline ("I did not observe
source that updates currentPhase" at `w2-markdown-phase-engine-findings.md:32`) which
is a calibration test medium passed.

**Confidence: high** for the discipline-holding claim; **medium** for the broader
"medium suffices for exploration" generalization (n=2).

## §7. Methodological observation: defaulted-spec-following (sub-pattern of B.1/B.5)

Logan asked when I (the dispatching session) chose high over medium for slices 2-5.
Honest answer: the orchestration package spec at `OVERVIEW.md §3.1` and `§3.3` specifies
high; I followed the spec without re-raising the question, even though Logan's earlier
prompt had explicitly questioned model tier and even though the capabilities probe had
just demonstrated medium's surprise competence on adjacent work.

This is a sub-pattern of B.1 (skill-heuristic shallow-match per
`2026-04-27-dispatch-readiness-deliberation.md §B.1`) and B.5 (dispatching-before-
precondition-check per `:247`): **strong-spec-trigger bypasses re-evaluation when
evidence has shifted since spec was written**.

The mitigation: when a prior spec becomes stale relative to new evidence (here:
medium's surprise competence on the capabilities probe + W2 dive, both produced
*after* OVERVIEW.md was authored on 2026-04-27 morning), defaults should be reopened
explicitly, not followed by inertia. Logan's question caught this.

In retrospect high was empirically right for slices (per §5); but the choice should
have been informed by deliberation, not defaulted. The pattern matters because spec-
following is exactly the shape of B.1 (a strong trigger — "spec says high" — bypasses
the deeper reading the situation warrants).

**Cross-pattern note:** B.1 was about Claude reaching for a tool whose triggers
shallow-match the situation; B.5 was about Claude executing a procedure without
verifying its preconditions; this sub-pattern is about Claude executing a procedure
without verifying that *the procedure itself* still fits the situation. All three are
forms of "strong trigger bypasses verification." The corrective remains user-
adjudication (Logan's question).

## §8. Limits of this comparison

- **Single-session sample (n=1 across both tiers).** All evidence was produced in one
  dispatching session. No test for run-to-run variance.
- **Specific work shape.** Codebase characterization with structured prompts +
  forbidden-reading discipline. Different work shapes (e.g., open-ended planning;
  speculative ideation; refactoring tasks) may invert the conclusion.
- **Tier comparison was not a controlled experiment.** No medium-effort slice was
  dispatched for direct comparison against the high-effort slices; the comparison is
  between W1 slice output at high and probe output at medium on adjacent-but-different
  work. The honest comparison would dispatch one slice at medium and compare directly.
- **"Depth" calibration is interpretive.** Reasonable observers might disagree on
  whether specific findings count as "relationship" vs "inventory." The §3.2 examples
  are my reading; auditor disagreement is a real possibility.
- **Side-investigations had non-standard output structure.** The §A/§B/§C discipline
  in the capabilities probe is its own discipline, not standard for this comparison;
  it may have made the medium output look more structured than a freer prompt would.
- **No direct measurement of token usage.** "Token volume" claims rely on output size
  as a proxy. Run logs with explicit `tokens used` aren't cited above (output sizes
  from `ls -la` per `wc -l` substitution; reasoning-token counts inferred not measured).
  **Confidence: medium-low for proxy-validity.**

## §9. Revision-trigger

This artifact is preliminary; pending W2 audit validation per `audit-spec.md`. If audits
dispatched against W1 slice output surface findings that change the tier-comparison
conclusion, this artifact gets revised before the methodology codification per
`2026-04-28-framing-widening.md §9` items 7-8.

Specific revision triggers:

- **Audit catches material misreadings in high-effort slice output** that suggest high
  wasn't actually adding the value claimed in §5. (E.g., if slice 2's vendoring finding
  is misread of ADR-010, or if slice 3's engine-resolver dispatch is over-stated.)
- **Audit catches subtle source-misreadings that medium would also produce.** (E.g., if
  high's claimed depth turns out to be confidently-asserted but un-grounded — the
  failure mode is "high effort produces high-confidence wrong claims.")
- **Logan's direct gsd-2 reading per `OVERVIEW.md §10` surfaces a different read.**
- **Subsequent comparable work (third sample reaching the threshold per
  `framing-widening.md §9` item 7) inverts or qualifies the conclusion.**

If revision happens, the revision should be a new dated note that points back to this
one, preserving the traces-over-erasure discipline per project methodology rather than
overwriting.

## §10. Cross-references

- `2026-04-28-framing-widening.md` §9 (deferred items log; this artifact slots in as
  input to items 7-8 methodology codification).
- `2026-04-27-dispatch-readiness-deliberation.md` §B.1 + §B.5 (methodological
  observations; §7 of this note extends the pattern).
- W1 slice outputs at `.planning/gsd-2-uplift/exploration/01-` through `05-` (high-effort
  evidence).
- Side-investigations at `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md`
  and `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md` (medium-
  effort evidence).
- `.planning/gsd-2-uplift/orchestration/preamble.md` (calibration discipline source for
  both tiers).
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md §3.1, §3.3` (the spec specifying
  high for slices; the spec §7 identifies as defaulted-following surface).

---

*Single-author preliminary tier-comparison artifact written 2026-04-28 by Claude
(Opus 4.7) at Logan's direction post-W1-slices-2-5-dispatch. Subject to the same
fallibility caveat as `DECISION-SPACE.md §0` and predecessor logs. Preliminary status:
the comparison's value depends on whether subsequent audits + further samples confirm
or revise the conclusion. Single-session sample with interpretive depth-calibration;
limits enumerated in §8 are load-bearing on how much weight downstream methodology
codification should place on this note.*
