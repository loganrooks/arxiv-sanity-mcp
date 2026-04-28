---
type: deliberation-log (comparison-drafting-decisions)
date: 2026-04-28
session: post-W3-paired-synthesis-landed; pre-incubation-checkpoint; SYNTHESIS-COMPARISON.md drafting in-session-collaborative
predecessor:
  - .planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md (D1-D5 disposition log; D5a recommended in-session-collaborative for comparison stage)
  - .planning/deliberations/2026-04-28-framing-widening.md (operating-frame ground; R1-R5 / six-context / four-act / four-surface pluralities)
ground:
  - .planning/gsd-2-uplift/exploration/SYNTHESIS.md (Claude Opus xhigh same-vendor synthesis; 609 lines)
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md (codex GPT-5.5 high cross-vendor synthesis; 207 lines)
  - .planning/gsd-2-uplift/orchestration/synthesis-spec.md (W3 synthesis spec; :172-189 paired-synthesis escalation criterion; :185-188 SYNTHESIS-COMPARISON.md path + incubation-feeding chain)
  - .planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md (predecessor handoff; §6 next-stage execution sequence; §3 comparison preview)
  - .planning/gsd-2-uplift/orchestration/OVERVIEW.md §11.5 (W3 synthesis disposition log; populated post-this-session)
status: complete (decisions DC0-DC4 disposed during in-session-collaborative comparison-drafting alignment-check)
purpose: |
  Capture the comparison-stage drafting decisions reached in the 2026-04-28
  post-paired-synthesis session, with qualified justifications preserving
  conditional structure ("what would change each recommendation").

  Five live decisions are recorded:
  - DC0: SYNTHESIS-COMPARISON.md structure (§0-§6 scaffold with three operational refinements)
  - DC1: §0 top-line takeaway differentiation across three divergence-types
  - DC2: §1 finding count and ordering (9 convergent; RTK collapsed in §1.5; §1.6 Claude-unique → §3 asymmetric coverage)
  - DC3: Per-finding "Bears on §5.X" pointer shape; integration load lives in §5
  - DC4: R4-weighting divergence characterized as substantive interpretive-disposition-timing (not register) — load-bearing for incubation starting position

  This log is dynamics-faithful. Headlines + reference flow into OVERVIEW.md §11.5.
  Comparison-stage decisions are smaller-scope than predecessor's W2 disposition
  log (D1-D5) but DC4 is genuinely load-bearing for incubation; recording venue
  warrants a sibling deliberation log rather than appending to the closed
  W2 log.

  Single-author artifact written by Claude (Opus 4.7, xhigh effort) at
  Logan's direction post-Logan-affirmation of the §0 + §1 first batch and the
  three checkpoint dispositions. Subject to the same fallibility caveat as
  DECISION-SPACE.md §0 and predecessor logs.
read_order: |
  - For "what was decided at comparison-drafting time + why + what would change it":
    this document.
  - For "the comparison artifact these decisions shape": SYNTHESIS-COMPARISON.md.
  - For "the syntheses being compared": SYNTHESIS.md (same-vendor) + SYNTHESIS-CROSS.md (cross-vendor).
  - For "the spec the comparison follows / departs from": synthesis-spec.md (esp. :172-189 + :185-188).
  - For "the predecessor disposition log that recommended in-session-collaborative
    drafting": 2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md (D5a).
  - For "the framing-widened operating frame this comparison inherits":
    2026-04-28-framing-widening.md.
---

# Comparison-drafting decisions — 2026-04-28

## §0. How to read this document

**Audience.** Future-Logan, future-Claude in fresh sessions, future-auditors of the SYNTHESIS-COMPARISON.md artifact or incubation-checkpoint deliberation, possibly external readers if the gsd-2 uplift initiative gets sponsored or observed.

**What this document IS.** Auditable record of the five live decisions reached during in-session-collaborative drafting of `SYNTHESIS-COMPARISON.md`. Each decision section names: (i) the decision; (ii) the disposition chosen; (iii) substantive justification (anchored to current evidence — both syntheses' verbatim content + framing-widening + handoff); (iv) explicit assumptions; (v) conditional flips ("what would change the recommendation under what conditions").

**What this document IS NOT.** Not the disposition log itself (OVERVIEW.md §11.5 is the canonical home per audit-spec.md / synthesis-spec.md disposition pattern). Not a substitute for reading SYNTHESIS-COMPARISON.md. Not a re-synthesis (synthesis-stage work is upstream and complete).

**Disposition discipline.** Logan disposed all five decisions after the §0+§1 first-batch landed and three checkpoint questions were surfaced. This log captures the recommendations + Logan's affirmation + the conditional flips. Per harvest §10.1 assumption #1 + DECISION-SPACE.md §0, Logan disposes substantive choices.

**B.6 surface caught and addressed.** The synthesis-spec.md (2026-04-27) does not dictate comparison structure beyond the file path at `:185`. The handoff §6.3 scaffold is the predecessor session's draft; this session re-evaluated the scaffold against current evidence (both syntheses landed; framing-widening operating-frame ground) before disposing. DC0 affirms the scaffold; DC1-DC4 refine within it. Each decision's "Substantive justification" anchors to *current evidence* — both syntheses' verbatim content + handoff §3 preview + framing-widening §0 plurality-preservation discipline — rather than spec-rephrasing.

**Calibration register.** Calibrated language per LONG-ARC.md anti-pattern "Closure pressure at every layer": "interpretive divergence" over "disagreement"; "operating-frame disposition timing" over "fundamental disagreement"; "Logan-disposed at incubation" over "decided" for surfacing-not-deciding work.

**Methodological observation surfaced this session.** During DC1 reasoning, I default-cited arxiv-sanity-mcp's `AGENTS.md` anti-pattern checklist (tournament-narrowing; single-lens-by-accident; etc.) as if it were generic governance discipline applicable to gsd-2-uplift comparison reasoning. Logan corrected: AGENTS.md is codex's memory file (Claude's is CLAUDE.md), and both arxiv-sanity-mcp memory files are project-specific to arxiv-sanity-mcp's own implementation work — not shaped for staged-initiative work like gsd-2 uplift. The drift signals migration trigger (per `INITIATIVE.md §7`) is approaching readiness — as initiative content matures, arxiv-sanity-mcp-framing-import is a recurring failure mode. Recorded in §4 below; not blocking DC0-DC4 dispositions.

## §1. Premise — what's in scope here, and what's not

Five comparison-drafting decisions sit between W3 paired-synthesis landed (per OVERVIEW §11.4 + handoff §2.6-§2.8) and SYNTHESIS-COMPARISON.md complete. **The decisions don't pre-decide R-strategy, project-anchoring, or any operating-frame question** — those flow from incubation-checkpoint per `DECISION-SPACE §2.3`, which is Logan-led + out of orchestration scope (handoff §6.5 + §8.1). What's in scope: comparison-artifact structure + per-section disposition mechanics. Deferred to incubation: substantive disposition of R-mix; project-anchoring; whether to dispatch deferred competitor-landscape probe (`framing-widening §9` item 3) before second-wave-scoping.

**Largest single load-bearing call: DC4 (R4-divergence-characterization).** This characterization shapes what incubation operates under at starting position — codex's read declares operating-frame shift at synthesis stage; Claude's read defers shift to incubation evaluation. Different starting positions yield different incubation disposition shapes. DC0-DC3 are operational-structure decisions; DC4 is a substantive reading that propagates into §2.1 of SYNTHESIS-COMPARISON.md and from there into incubation reading. This shapes the careful-justification weighting below: DC4 gets the most depth.

## §2. What's being disposed — preview

For audit-trail completeness, the dispositions disposed by this log:

- **DC0**: Affirm the §0-§6 scaffold per handoff §6.3 with three operational refinements (DC1-DC3).
- **DC1**: §0 top-line takeaway differentiates three divergence-types: substantive R4-disposition-timing; register R5; artifact-shape register/length.
- **DC2**: §1 carries 9 convergent findings. RTK gating divergence stays collapsed within §1.5 (docs-vs-source class) as the canonical example. §1.6 (release/workflow-interleaving) re-categorized as Claude-unique → moves to §3 asymmetric coverage when §3 is drafted.
- **DC3**: Per-finding "Implication for incubation" multi-clause lines refactored to tight "Bears on §5.X" pointers; integration load lives in §5 multi-axis structure.
- **DC4**: R4-weighting divergence characterized as substantive interpretive-disposition-timing divergence (not register) — codex declares synthesis-stage shift from "R2 base unless infeasible" toward "R2+R4 mix unless core/Pi entanglement"; Claude preserves R2 base + names R4-inclusion as "net widening the operating frame should absorb" with explicit deferral to incubation. Load-bearing for incubation starting position.

## §3. Decisions

### §3.1 DC0 — Comparison structure: §0-§6 scaffold per handoff §6.3 with three operational refinements

**Decision.** Affirm the handoff §6.3 scaffold (`§0` summary; `§1` convergent findings; `§2` divergent findings; `§3` asymmetric coverage; `§4` methodological observations; `§5` integration for incubation; `§6` confidence and limits) with three operational refinements (DC1-DC3 below). No re-design from first principles; the scaffold is sound for incubation-feeding utility.

**Substantive justification.**

The handoff §6.3 scaffold is anchored to (a) the canonical M1 paired-review shape (METHODOLOGY.md:104-115; DECISION-SPACE §1.13), (b) what `synthesis-spec.md:185-188` implies incubation reads, and (c) `DECISION-SPACE §2.3` incubation-checkpoint disposition list (metaquestion + R-mix + direction-shifting evidence + side-probe triggers + scoping decision). Each scaffold section maps to a substantive purpose: §1 surfaces robustness inputs; §2 surfaces deliberation inputs (Logan-adjudication); §3 surfaces completeness inputs; §4 surfaces M1-process observations; §5 integrates across incubation's actual disposition axes; §6 carries calibration.

The B.6 self-check (per `2026-04-28-tier-comparison-preliminary.md §7` defaulted-spec-following sub-pattern + `framing-widening §9` items 7-8): synthesis-spec.md was authored 2026-04-27 + framing-widening landed 2026-04-28; both syntheses now landed 2026-04-28. The escalation triggers fired (Trigger 4 per `SYNTHESIS.md §0`); the spec's "compare and integrate" directive holds. Re-evaluating against current evidence: the scaffold accommodates the framing-widening's R1-R5 / six-context / four-act / four-surface pluralities (DC2's §3 + DC3's §5 multi-axis) without structural revision. Re-design would burn cycles on a sound shape.

The fresh-from-first-principles alternative (re-design rather than refine) was offered at the prior message ("if you want a fresh-from-first-principles structure proposal rather than refinements-on-the-handoff-draft, I can do that instead"). Logan affirmed refinements over re-design. The scaffold's integrity holds.

**Assumptions.**

- **A1.** The handoff §6.3 scaffold matches what incubation actually disposes. Grounded in `DECISION-SPACE §2.3` operational-incubation list + `synthesis-spec.md:185-188`; high confidence.
- **A2.** Incubation reads syntheses + comparison together (not comparison alone). Per `synthesis-spec.md:188`: "Both syntheses + comparison feed incubation-checkpoint." Comparison's job is integration, not standalone-decisive.
- **A3.** Three operational refinements within the scaffold are sufficient to address current-evidence gaps; structural re-design is not warranted. Grounded in DC1-DC3 reasoning below.

**Conditional flips.**

- **If incubation's read pattern is "scan comparison; rarely dive into syntheses,"** the scaffold's §3 (asymmetric coverage) and §4 (methodological observations) read as overhead. **What would flip:** Logan's read pattern explicitly favoring comparison-as-primary-input. Counter-condition: per `handoff §9.2`, this is Logan-disposed; default to scaffold serving both use cases.
- **If the syntheses' divergences are sharper than I credit (e.g., conflicting findings, not just interpretive emphasis),** §2 needs structural restructure (per-divergence side-by-side with explicit reconciliation framing). **What would flip:** my read of divergences as "interpretive register / disposition-timing" rather than "factual conflict." Counter-condition: both syntheses converge on substantive findings (DC2 §1's 9 convergent items); divergences are interpretive at incubation-relevant points.
- **If incubation runs cold (Logan reads cold without prior session memory),** §0 summary needs to carry more orientation work. **What would flip:** explicit Logan disposition that comparison serves cold-read. Counter-condition: handoff §6.3 already implies cold-read serviceability; §0 carries top-line + scope + caveat.

**Confidence.** High. Scaffold validated against incubation-disposition list + paired-review shape; refinements operationalize within sound shape.

### §3.2 DC1 — §0 top-line takeaway: three-divergence-type differentiation

**Decision.** §0 top-line takeaway differentiates three divergence-types rather than collapsing them under "register/emphasis":

1. **R4 weighting — substantive interpretive-disposition-timing divergence** (codex declares operating-frame shift at synthesis stage; Claude preserves R2 base + defers shift-disposition to incubation).
2. **R5 framing — register divergence at common operational endpoint** (codex "no longer merely a cancellation bucket"; Claude "not first-wave-decidable; requires comparison frame"; both converge operationally on deferring R5 evaluation pending the deferred competitor-landscape probe per `framing-widening §9` item 3).
3. **Synthesis register/length — artifact-shape divergence** (Claude 609-line dense-deliberative with framing-widening vocabulary applied throughout + F1-F8 numbered findings stratification; codex 207-line compact-directive with operationally crisp §5 recommendations).

**Substantive justification.**

My initial framing characterized all three as "register/emphasis." Re-reading both syntheses verbatim during the alignment-check exposed that this collapsed a substantive divergence:

- Codex `SYNTHESIS-CROSS.md §0` OFS-1 verbatim: *"shifts the operating frame from 'R2 base unless infeasible' toward 'R2+R4 mix unless the needed surface requires core/Pi entanglement.'"* — synthesis declares the shift.
- Claude `SYNTHESIS.md §2.1` net read verbatim: *"Pre-decided in the operating frame: R2 base + primary; R1 as fallback. Both persist as working hypotheses within the widened R1-R5 space... Direction-shifting: the inclusion of R4 explicitly + the deferred-pending-probe disposition for R5 are net widenings the operating frame should absorb. Whether this changes second-wave-scoping shape is incubation-checkpoint work."* — synthesis defers the shift to incubation.

The divergence is **when** the operating-frame shift happens (synthesis-stage in codex; incubation-stage in Claude), not just rhetorical emphasis. Test of substantive-vs-register: does it change incubation's starting position? Yes — codex's read has incubation operate under "R2+R4-mix-as-already-shifted-frame"; Claude's read has incubation evaluate whether-to-shift. Different disposition shapes. **Substantive.** This becomes DC4's load-bearing characterization.

R5 framing genuinely is register-shaped: both come to the same operational conclusion (defer R5 evaluation; dispatch competitor-landscape probe before commitment per `framing-widening §9` item 3). Codex more open-framed; Claude more pending-evidence-suspended. They agree on what to do.

Synthesis register/length is artifact-shape divergence — affects how incubation reads each but isn't a divergence on findings.

The three-way differentiation is more honest than "register/emphasis" and surfaces the load-bearing R4 disposition-timing question explicitly for incubation. Per `LONG-ARC.md` "Closure pressure at every layer" anti-pattern: collapsing substantive divergence into register would be tidy-summary-misrepresenting-unsettled-situation.

**Assumptions.**

- **A1.** "Operating-frame disposition timing" is substantive because it changes incubation's starting position. Test passes: codex-read and Claude-read yield different incubation disposition shapes.
- **A2.** Both authors would recognize their reads under this characterization. Verbatim quotes above sourced directly from synthesis files; characterization derives from the wording, not interpretive overlay.
- **A3.** R5 register-divergence is genuine (both converge operationally). Verified: both cite `framing-widening §9` item 3 as the gating evidence-need.

**Conditional flips.**

- **If R4 divergence reads as register-only to your eye** ("both name R4 explicitly; the wording is a stylistic difference; both syntheses leave R4 disposition open"). **What would flip:** the simpler "register only" framing collapses all three divergences into rhetorical-emphasis. Counter: codex's "shifts the operating frame from X toward Y" is declarative-not-conditional; Claude's "Whether this changes second-wave-scoping shape is incubation-checkpoint work" is explicitly-deferred. The wordings carry different commitments.
- **If R5 framing reads as substantively divergent** (codex actually opens R5 as live-now while Claude refuses). **What would flip:** R5 needs the substantive treatment too; §0 differentiates four divergence-types not three. Counter: both end at same operational conclusion (deferred-pending-probe); the divergence is at the read-not-disposition level.
- **If artifact-shape divergence reads as not-load-bearing for incubation** (just stylistic). **What would flip:** drop from §0 takeaway; surface only in §4 methodological observations. Counter: artifact-shape affects how incubation reads each synthesis (Claude's 609-line denseness vs codex's 207-line compactness shapes incubation reading-pattern); load-bearing enough for §0 mention.

**What this decision does not decide.**

- The substantive R4 disposition itself (DC4 names the divergence; §5.2 of SYNTHESIS-COMPARISON.md surfaces both reads + evidence; incubation disposes which read it operates under).
- Project-anchoring (six-context plurality) — Logan-disposed at incubation per `framing-widening §3.3`.

**Confidence.** Medium-high on the three-way differentiation; medium-high on R4 as substantive (not register); high on R5 as register-with-converged-operational-endpoint; medium on artifact-shape's §0-load-bearing-ness.

### §3.3 DC2 — §1 finding count and ordering: 9 convergent findings; RTK collapsed in §1.5; §1.6 re-categorized to §3

**Decision.** §1 carries 9 convergent findings (vs handoff §3.1's 9; vs initial draft's 10). Specific shape:

- §1.1 Pi vendoring + clean-seam tension; ADR-010 proposed-not-implemented.
- §1.2 Extension-surface plurality (4 parallel subsystems).
- §1.3 Two-engine workflow architecture (markdown-phase prompt-dispatch vs yaml-step deterministic).
- §1.4 Release/breaking-change machinery-vs-practice gap (load-bearing direction-shifter).
- §1.5 Docs-vs-source divergence as recurring class (RTK gating divergence as canonical instance).
- §1.6 R2 viable but with substantial caveats (was §1.7).
- §1.7 Telemetry/observability/security/trust as central design surface (was §1.8).
- §1.8 B4 split held (was §1.9).
- §1.9 R3 (upstream-PR-pipeline) under-evidenced (was §1.10).

Initial draft's §1.6 (Tightly-interleaved release/workflow/artifact infrastructure) re-categorized as Claude-unique surfacing → moves to §3 asymmetric coverage when §3 is drafted.

**Substantive justification.**

**RTK collapse.** §1.5 carries docs-vs-source divergence as a class; RTK is the most-cited individual instance (slice 1 (v); slice 2 Finding 1.8 + (v); slice 3 (v); slice 2 audit verbatim spot-check 3 verifying README:22 vs cli.ts:167-178). §1.5 lists RTK as the first cited instance with explicit verbatim audit verification flag. Surfacing RTK as standalone §1.X (per handoff §3.1's listing) double-counts the same observation — once in §1.5 as instance, once standalone. Cleaner to keep §1.5 as the class with RTK as canonical example. Per `framing-widening §10.3` plurality-vs-fragmentation discipline: don't fragment a coherent pattern (docs-vs-source class) into instances unless instances carry distinct downstream implications. RTK's implications fold into the class.

**§1.6 re-categorization.** Re-reading codex `SYNTHESIS-CROSS.md` carefully: §3.4 carries machinery-vs-practice (subsumed in `SYNTHESIS-COMPARISON.md §1.4`), and §1.1 lists slice 5's release artifacts inventory. **Codex does not directly state the "tightly-interleaved release/workflow/artifact infrastructure" observation.** Claude carries this in `SYNTHESIS.md §1.4` as a dedicated cross-slice pattern integration sourced to slice 5 (iv) item 8's explicit synthesis-stage flag. So this is **Claude-unique surfacing**, not convergent. Mis-categorization in initial draft; corrected to §3 asymmetric coverage.

**§1.10 (R3 under-evidenced) addition vs handoff.** Handoff §3.1 didn't list R3 under-evidenced as standalone convergent finding. Re-checking both syntheses: Claude `SYNTHESIS.md §2.1` R3 medium-low; codex `SYNTHESIS-CROSS.md §0` OS-1 R3 medium-low. Both at identical confidence labels with identical underlying evidence (CONTRIBUTING.md + visible PR throughput + failed live probe + deferred deeper-probe). Genuinely convergent. Keep — bears on §5.4 side-probe triggers.

Net: 9 findings vs handoff's 9. Specifically: handoff's standalone RTK item folds into §1.5; handoff's `release/breaking-change machinery-vs-practice` (kept), `R2 viable` (kept), `telemetry/observability/security` (kept), and `B4 split held` (kept) all map 1:1; handoff's `Pi vendoring` (kept), `Extension-surface plurality` (kept), `Two-engine` (kept), `Docs-vs-source class` (kept) map 1:1; new §1.9 R3 under-evidenced replaces handoff's standalone-RTK as the 9th item.

**Assumptions.**

- **B1.** Handoff §3.1's count is informed but not authoritative. Predecessor's draft preview, refined by current evidence reading. Holds.
- **B2.** §3 asymmetric coverage is the right home for Claude-unique observations. Per recommended structure (DC0); per the §3 purpose ("what each surfaced uniquely — completeness signal"). Holds.
- **B3.** Both syntheses' verbatim content is the ground for convergence-vs-asymmetry classification. Verified against both files during alignment-check.

**Conditional flips.**

- **If you read codex `§1.1 + §3.4` as substantively carrying the release/workflow-interleaving observation,** §1.6 stays in §1 with asymmetric-structure-but-convergent-substance note. **What would flip:** my close-read of codex finding the interleaving claim absent. Counter-condition: re-checked codex §1.1 inventories release artifacts but doesn't make the interleaving-claim; §3.4 carries machinery-vs-practice not interleaving. Different observation.
- **If finding count itself is not load-bearing for incubation** (any structurally-sound integration works), this is mostly cosmetic. **What would flip:** Logan preference for tighter §1 (e.g., 7 findings collapsing R3 + B4-split into other items). Counter: each finding has distinct downstream implications; further collapse loses signal.
- **If you want §1 to track handoff §3.1 more closely** (explicit traceability to predecessor's preview), surface RTK as standalone §1.X again. Counter: tracks-handoff-by-default is B.6-anti-pattern (defaulted-spec-following); current-evidence read warrants the collapse.

**What this decision does not decide.**

- Whether other Claude-unique observations exist in §1 that also belong in §3 (full §3 drafting will surface).
- Whether codex-unique observations exist beyond the handoff §3.3 enumeration (covered in §3 drafting).

**Confidence.** Medium-high. Verified against both syntheses' verbatim content; the collapse + recategorization choices are evidence-grounded.

### §3.4 DC3 — Per-finding "Bears on §5.X" pointer shape; integration load lives in §5

**Decision.** Each §1.X carries a tight one-line "Bears on §5.X axis" pointer rather than a multi-clause "Implication for incubation" line. Multi-axis integration content lives in §5 (§5.1 metaquestion / §5.2 R1-R5 mix / §5.3 six-context anchoring / §5.4 side-probe triggers).

Concrete refactoring shape — current §1.1 implication: *"R1 maintenance cost is structurally heavier than DECISION-SPACE §1.8's 'R1 fallback only' framing assumed; R2 work targeting pi-coding-agent internals is functionally R1-shaped because the clean seam doesn't exist; load-bearing for R-strategy disposition."* (Three claims; first two are immediate consequences; third is integration-flavored pre-empting §5.2.)

Refactored §1.1 pointer: *"Bears on §5.1 metaquestion integration (does direction hold given entanglement?) + §5.2 R1-R5 mix integration (R1 cost-model + whether R2 work targeting Pi-vendored counts as R2 or R1-shaped)."* (Tight pointer; integration deferred to §5 axis; no pre-emption.)

**Substantive justification.**

Per-finding multi-clause "Implication for incubation" was doing too much — gloss + integration-gesture mixed. Per the recommended structure, §5 carries multi-axis integration (§5.1-§5.4); per-finding implications either (a) duplicate §5's integration claims at finer granularity, or (b) gesture at integration without doing it, distorting §1 toward partial-integration.

The split — tight pointers in §1; integration in §5 — yields:
- Sharper §1 (more claim-density per line; less interpretive overlay).
- §5 carries integration load substantively (matches its multi-axis purpose).
- Incubation's read pattern (per `handoff §9.2` Logan-disposed) is supported either way: scan §1 → dive into §2-§4 → integrate via §5; or scan §1 + §5 directly.

Per `LONG-ARC.md` "Closure pressure at every layer": multi-clause implications in §1 risk pretending settlement (per-finding integration is interpretive at incubation-relevant points; surfacing as fait-accompli pre-empts incubation). Tight pointers preserve the open-to-integration shape.

**Assumptions.**

- **C1.** §5 will be substantial enough to carry integration load. Per recommended multi-axis structure (§5.1-§5.4 sub-sections), yes.
- **C2.** Incubation's read pattern is some mix of "scan inputs + dive into integration" rather than "read per-finding implications standalone." Not verified — Logan-disposed per `handoff §9.2`. Hybrid pointer-shape supports both.
- **C3.** Multi-axis integration in §5 doesn't fragment what should be unified observations. Test: each §1.X bears on at least one §5 axis cleanly; some bear on multiple (§1.1 → §5.1 + §5.2; §1.4 → §5.1 + §5.2 + §5.4). Multi-axis structure handles this naturally.

**Conditional flips.**

- **If you want §1 maximally self-contained** (incubation can read §1 + §5 without §2-§4 coverage), keep multi-clause implications; §1 carries duplication-with-§5 cost. **What would flip:** Logan preference for §1-as-standalone-input. Counter-condition: per `synthesis-spec.md:188`, comparison feeds incubation as part of full chain; §1 standalone is not the canonical use case.
- **If §5 is going to be lighter than the multi-axis structure suggests** (e.g., one combined integration paragraph rather than four sub-sections), per-finding implications in §1 become more important. **What would flip:** §5 collapses to single integration view. Counter-condition: multi-axis structure was affirmed (DC0); §5 will carry the load.
- **If incubation read pattern is unknown and we want §1 to serve both "primary input" and "navigator" use cases,** hybrid: keep one-line "immediate consequence" + leave a pointer to §5 axis. This is what the refactored shape does — pointer + minimal disambiguation, not pure pointer.

**What this decision does not decide.**

- The specific §5.X content (drafted in §5 batch).
- Whether some §1.X items genuinely need fuller per-finding context (the refactor is uniform; if specific findings need exception, drafting will surface).

**Confidence.** High. Refactor preserves §1 information while sharpening claim-density; integration load lives where the multi-axis structure can carry it.

### §3.5 DC4 — R4 divergence characterized as substantive interpretive-disposition-timing (load-bearing for incubation)

**Decision.** §2.1 of SYNTHESIS-COMPARISON.md characterizes the R4 divergence as **substantive interpretive-disposition-timing divergence** — codex's read declares operating-frame shift at synthesis stage; Claude's read preserves R2 base and defers shift-disposition to incubation. The characterization includes:

- **What codex's read does to incubation:** incubation operates under "R2+R4-mix-as-already-shifted-frame" at starting position; R-mix evaluation begins from "which subsystem(s) carries first second-wave target" rather than "should we add R4 explicitly."
- **What Claude's read does to incubation:** incubation evaluates whether-to-shift R2-base-frame to absorb R4 at starting position; R-mix evaluation includes the disposition step itself.
- **What both reads agree on:** R4 has standing in the widened R1-R5 design space; some uplift work is naturally R4-shaped (R4-elevation is convergent at the inclusion level; the divergence is at the operating-frame disposition level).

This is **load-bearing for incubation starting position.**

**Substantive justification.**

This is the most load-bearing decision in this session because it changes incubation's starting position. The characterization is anchored to verbatim synthesis content:

- Codex `SYNTHESIS-CROSS.md §0` OFS-1: *"shifts the operating frame from 'R2 base unless infeasible' toward 'R2+R4 mix unless the needed surface requires core/Pi entanglement.'"* (Declarative; synthesis-stage shift; recommendation §5: *"Treat R4 as first-class in the checkpoint."*)
- Claude `SYNTHESIS.md §2.1` net read: *"Pre-decided in the operating frame: R2 base + primary; R1 as fallback. Both persist as working hypotheses within the widened R1-R5 space; first-wave evidence narrows R1's case but doesn't flip its disposition; first-wave evidence widens R2's substantive surface but qualifies R2's depth (entanglement; engine-mode constraints). Direction-shifting: the inclusion of R4 explicitly + the deferred-pending-probe disposition for R5 are net widenings the operating frame should absorb. Whether this changes second-wave-scoping shape is incubation-checkpoint work."* (Conditional; R2-base persists; explicit incubation-deferral.)

Test of substantive-vs-register: does the divergence change what incubation does? Yes — different starting positions yield different disposition shapes:
- Codex-starting-position: incubation reasons within R2+R4-mix as the operating frame; the question is *what specific subsystems × acts × R-strategies* the first second-wave target uses.
- Claude-starting-position: incubation reasons within R2-base + widening-recognition; the question includes *whether to absorb R4 into operating frame as peer-strategy or as case-specific-strategy*.

Both starting positions are defensible — codex's read is licensed by first-wave evidence (R4's substantive infrastructure: headless mode + JSON output + RPC + MCP + hooks; per `SYNTHESIS-CROSS.md §2.1` R4 sub-section); Claude's read is licensed by `DECISION-SPACE §0` disposition discipline (Logan disposes operating-frame changes, not synthesis). The reads diverge on **whether synthesis has standing to declare operating-frame shifts vs whether shifts must come from incubation/Logan-disposition.**

The implication for SYNTHESIS-COMPARISON.md §2.1: surface both reads + the evidence behind each + the disposition-shape-delta + Logan-adjudication that incubation will need to make. Do not pre-decide which read incubation operates under.

**Assumptions.**

- **D1.** Synthesis-stage operating-frame-shift declarations are interpretively-licensed-but-Logan-disposable. Per `DECISION-SPACE §0` + `INITIATIVE.md §0` disposition discipline: Logan disposes substantive operating-frame changes; synthesis surfaces but does not dispose. Both reads honor this differently — codex's "shifts" reads as recommendation-to-incubation; Claude's "operating frame should absorb" reads as recommendation-to-incubation-with-explicit-disposition-deferral. Same underlying discipline, different surfacing.
- **D2.** The framing-widening §1.3 ("R1-R5 as a composable space, not a tournament") is the operating frame both syntheses inherit. Both honor R4 as composable-with-R2; the divergence is at the disposition-timing level not the inclusion level.
- **D3.** Incubation has standing to dispose operating-frame shifts. Per `DECISION-SPACE §2.3` + `framing-widening §7` medium-horizon disposition list: yes; incubation re-disposes operating frame on first-wave evidence.

**Conditional flips.**

- **If you read codex's "shifts the operating frame from X toward Y" as recommendation-to-incubation rather than synthesis-stage declaration,** the divergence collapses to register (both syntheses recommend R4 elevation; codex more directively-worded; Claude more deliberatively-worded). **What would flip:** my read of codex's wording as declarative. Counter-condition: codex `§5` recommendation: *"Treat R4 as first-class in the checkpoint"* — the imperative reads as operationally-load-bearing-recommendation more than register.
- **If you read Claude's "Whether this changes second-wave-scoping shape is incubation-checkpoint work" as register-equivalent to codex's "Treat R4 as first-class,"** the divergence again collapses to register. Counter-condition: Claude's wording explicitly defers to incubation; codex's wording explicitly directs at incubation. The directive vs deferential register is part of the substance — what the syntheses claim authority to do shapes what incubation operates under.
- **If you read both reads as substantively saying the same thing** ("synthesis recommends R4 elevation; incubation disposes; same starting-position"), the divergence is rhetorical-only. Counter-condition: the test of starting-position-equivalence — does incubation begin from "R2+R4-mix" or from "R2-base + decision-about-whether-to-shift-to-R2+R4"? — yields different disposition shapes per the verbatim content.
- **If incubation's starting-position is not actually shaped by synthesis register,** DC4's load-bearing-ness is over-credited. Counter-condition: per `DECISION-SPACE §1.7` + `framing-widening §10.4` interpretive-claims-as-Logan-disposed discipline, synthesis register at load-bearing positions is exactly what incubation reads from + decides under.

**What this decision does not decide.**

- Which read incubation operates under (Logan-disposed at incubation; SYNTHESIS-COMPARISON.md §2.1 surfaces both).
- The substantive R-mix that emerges from incubation (downstream from this disposition; second-wave-scoping work).
- Whether codex's read is "more correct" than Claude's or vice versa (the divergence is the data; surfacing without endorsing is the appropriate comparison-stage action).

**Confidence.** Medium-high on the substantive-disposition-timing characterization; medium-high on it being load-bearing for incubation starting-position; medium on whether the divergence-shape is fully captured by "disposition-timing" framing or whether finer-grained framing surfaces additional sub-divergences (incubation may surface).

## §4. Methodological note — arxiv-sanity-mcp framing-import drift surfaced

During DC1 reasoning, my prior recommendation message cited `AGENTS.md` anti-pattern checklist (tournament-narrowing under "disciplined" framing; single-lens-by-accident; single-reader framing claims as authoritative; closure pressure at every layer) as if it were generic governance discipline applicable to gsd-2-uplift comparison reasoning. Logan corrected on two grounds:

1. **AGENTS.md is codex's memory file** (loaded by Codex CLI dispatched on cross-vendor work — slices 1-5 + cross-vendor synthesis). My auto-loaded project file is `CLAUDE.md` (per arxiv-sanity-mcp's setup; also auto-loaded into this session's context per VSCode extension wrapping). I cited the wrong file for my own behavioral grounding.
2. **The specific anti-patterns are arxiv-sanity-mcp-project-specific** — about the 005-008 spike chain drift modes (tournament narrowing of retrieval candidates; single-lens-by-accident under ADR-0005's multi-lens substrate; embedding-model-as-load-bearing decision; etc.). Both `AGENTS.md` and `CLAUDE.md` in arxiv-sanity-mcp are shaped for arxiv-sanity-mcp's own implementation work; neither is shaped for staged-initiative work like gsd-2 uplift, which lives at `.planning/gsd-2-uplift/` per `INITIATIVE.md §7` migration_trigger.

I imported arxiv-sanity-mcp's specific drift-mode checklist as if it were generic governance discipline. Category error.

**Right grounds for gsd-2-uplift-specific anti-pattern self-checks:**

- `framing-widening §0 + §10` — "decision spaces should not narrow without evidence"; "non-exhaustive listings should stay non-exhaustive in practice." Generalizable; gsd-2-uplift-anchored.
- `DECISION-SPACE §4` — closure-pressure-recurrence at meta-layer; comfort-language detection; performative-vs-operational openness; non-exhaustive-listings; push-for-assumptions; self-diagnosis-from-inside-pattern. Session-discipline observations the initiative produced.
- `LONG-ARC.md` generic anti-patterns — closure-pressure-at-every-layer is generic; specific instances (lines 47-53) are arxiv-sanity-mcp-specific. Generic shape transfers; specific items don't.
- `handoff §8` — explicit gsd-2-uplift anti-patterns (don't collapse R1-R5; don't pre-decide design shape; don't auto-execute incubation; etc.).
- `METHODOLOGY.md` M1 paired-review discipline.
- B.6 deferred-codification (`framing-widening §9` items 7-9) — defaulted-spec-following sub-pattern.

**Migration-trigger signal.** This drift event is a small data point that the migration trigger (per `INITIATIVE.md §7`: *"when a dedicated repo for the uplift project is created, this artifact and its siblings under .planning/gsd-2-uplift/ migrate there"*) is approaching readiness. As initiative content matures (now landed: framing-widening, both syntheses, multi-deliberation-log arc, comparison artifact in-progress, forthcoming incubation), the cost of arxiv-sanity-mcp-framing-import grows. Future sessions on this work will keep importing arxiv-sanity-mcp's framings unless either (a) the initiative migrates to its own repo with its own behavioral grounding (CLAUDE.md / AGENTS.md shaped for the uplift work), or (b) some interim mechanism (e.g., a `.planning/gsd-2-uplift/CLAUDE.md` that auto-loads when working in that directory; or explicit handoff-level reframing of which files to prioritize) addresses the framing-import drift.

**Not blocking DC0-DC4 dispositions.** DC1's substantive content (the three-divergence-type differentiation) was not load-bearing on AGENTS.md citation; only the anti-pattern self-check sub-section was mis-grounded. Substantive structure unchanged; replace that sub-section's grounds with the correct list above. **Recorded here for future-session pattern-recognition + as a methodological signal that the migration trigger is becoming actionable.**

This is the third sample for the defaulted-spec-following / framing-import-drift sub-pattern (per the B.6 codification threshold of ~3 samples per `framing-widening §9` items 7-8). Prior samples: tier-comparison §7 + 2026-04-27 §B.5 + 2026-04-28 W2 audit dispositions session §4. The current session's framing-import-drift adds a fourth sample. Codification venue: `METHODOLOGY.md` or `AGENTS.md` per `framing-widening §9` items 7-8; or a new gsd-2-uplift-specific `CLAUDE.md` if migration triggers; Logan-disposed methodology decision; not blocking near-horizon work.

## §5. What's next

Per the cross-decision dependency map:

1. **DC0-DC4 disposed → SYNTHESIS-COMPARISON.md revision.** §0 + §1 revised in-place per DC1-DC3; §1.6 removed (re-categorized to §3 when drafted); per-finding implications refactored to "Bears on §5.X" pointers; §2.1 R4 divergence framed per DC4 in §2 batch.
2. **§2 batch → §3 batch → §4 batch → §5 batch → §6 batch.** Each Logan-adjudication checkpoint: §2 (divergent findings; R4 + R5 + register/length), §5 (multi-axis integration; especially §5.3 six-context anchoring as Logan-disposed surfacing of project-anchoring).
3. **Comparison complete → OVERVIEW.md §11.5 update + INDEX.md update + STATE.md update.** Per handoff §6.6 commit cadence (Logan disposes commit timing).
4. **Comparison feeds incubation-checkpoint per `DECISION-SPACE §2.3`.** Logan-led; out of scope for this session.

Concrete next actions:

- Apply DC1-DC3 revisions to SYNTHESIS-COMPARISON.md §0 + §1 (this batch).
- Update OVERVIEW.md §11.5 with W3 paired-synthesis disposition + comparison-drafting in-session-collaborative + reference to this deliberation log.
- Update INDEX.md with new deliberation log entry.
- Continue to §2 batch with DC4 R4-divergence-characterization in §2.1.

## §6. Cross-references

**Sibling artifacts (decisions / dynamics).**
- `.planning/gsd-2-uplift/DECISION-SPACE.md` — load-bearing decision reference; B1-B6 in §1.11-§1.16; §2.3 incubation-checkpoint; §4 methodology observations.
- `.planning/deliberations/2026-04-28-framing-widening.md` — operating-frame ground (R1-R5 design space; six-context plurality; four-act plurality; project-anchoring framework); §9 deferred items log.
- `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` — D1-D5 disposition log; D5a recommended in-session-collaborative for comparison stage.
- `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` — tier-comparison input; §7 names B.6 sub-pattern.
- `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md` — orchestration package + B1-B6 + §B.1-§B.5 methodological observations.

**Comparison artifact this log shapes.**
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` — in-progress comparison artifact.

**Synthesis inputs being compared.**
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` — Claude Opus xhigh same-vendor synthesis (609 lines).
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` — codex GPT-5.5 high cross-vendor synthesis (207 lines).

**Spec inputs.**
- `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` — W3 synthesis spec; `:172-189` paired-synthesis escalation criterion; `:185-188` SYNTHESIS-COMPARISON.md path + incubation-feeding chain.
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` — §11.5 W3 synthesis disposition log (populated post-this-session).
- `.planning/gsd-2-uplift/orchestration/audit-spec.md` — W2 audit template (referenced for disposition pattern).

**Predecessor handoff.**
- `.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md` — predecessor; this session's onboarding artifact + §6 next-stage execution sequence + §3 comparison preview validated against current-evidence reading.

**Project doctrine referenced.**
- `LONG-ARC.md` — anti-patterns including closure-pressure-at-every-layer; this log resists that pressure by preserving conditional structure across DC0-DC4.
- `CLAUDE.md` — project identity (arxiv-sanity-mcp; not gsd-2-uplift); §4 surfaces the framing-import drift this session caught.
- `AGENTS.md` — codex's memory file (not Claude's); §4 surfaces the file-citation error.
- `.planning/spikes/METHODOLOGY.md` — M1 paired-review at line 112; B3 vendor split derives from it.
- `INITIATIVE.md §7` — migration trigger; §4 surfaces approaching-readiness signal.

---

*Single-author deliberation log written 2026-04-28 by Claude (Opus 4.7, xhigh effort) at Logan's direction post-Logan-affirmation of the §0 + §1 first batch and three checkpoint dispositions. Subject to the same fallibility caveat as DECISION-SPACE.md §0 and predecessor logs. The log captures the recommendations + Logan's affirmation + the conditional flips. If any decision feels mis-recorded in Logan's read, re-deliberation supersedes this log.*
