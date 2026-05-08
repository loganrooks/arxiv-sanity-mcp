---
type: orchestrator-audit-map
date: 2026-05-01
audience: senior reviewer with zero context on the gsd-2-uplift initiative
purpose: faithful navigational map of `.planning/gsd-2-uplift/` for orchestrator-level disposition
author: mapping agent (Opus 4.7 1M-context)
not_recommendations: This document surfaces what the artifacts say. It does not recommend disposition.
---

# gsd-2-uplift initiative — orchestrator map

This document maps the `.planning/gsd-2-uplift/` initiative inside arxiv-sanity-mcp. It exists for an orchestrator who has zero prior context, must understand what is in flight, what has been produced, and where the work is stuck. Sections 1-10 follow the requested structure. Citations to file paths use absolute paths; line numbers are given where load-bearing.

---

## §1. Top-level shape

### §1.1 What this initiative is (per the artifacts)

**The initiative's stated goal** (per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/INITIATIVE.md:42`, Logan articulation 2026-04-26):

> "how do we make the harness & thus agential development more robust and better over much longer horizons of development (across multiple milestones / releases, also thinking about how release workflows, prod, dev, integrate with the gsd-2 framework), as codebases become more complex, as the salient determining conditions of the design situation change... to uplift GSD-2 to be the best it possibly can be across longer and longer development horizons."

The "harness" in this articulation refers to "gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions" jointly — not gsd-2 alone (per `INITIATIVE.md:44`).

**Project-shape definition (corrected 2026-05-01)** per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md:54`:

> gsd-2-uplift is an **identity-preserving, pressure-respecting** uplift of gsd-2 that **pushes its limits in reasonable ways** toward a set of **reasonable objectives — discovered and refined through exploration**, **anchored against concrete test cases**, producing an **uplifted-gsd-2 that is itself useful for current project work** without committing to convergence on harness-studio's full vision.

Five active properties (per `EXTERNAL-VISION-CONTEXT.md:56-67`):
1. Identity-preserving
2. Pressure-respecting (anti-foreclosure constraints from harness-studio's vision)
3. Pushing limits in reasonable ways (not minimalist)
4. Reasonable objectives discovered through exploration
5. Anchored against concrete test cases (currently arxiv-sanity-mcp; eventually prix-guesser and others)

**Test-case-vs-substrate framing** (per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md:19`):

> arxiv-sanity-mcp is NOT the long-horizon goal. It is an MCP-native research discovery substrate... At the same time, arxiv-sanity-mcp is *a* spike-intensive test case for whether the agential-development substrate... can handle work where: (1) Precedent is thin or absent; (2) Experimental design itself is load-bearing; (3) The work necessarily produces new knowledge.

This framing is **stipulated, not observed** (per `RELATIONSHIP-TO-PARENT.md:31-40` §1.1 added during Phase B audit).

### §1.2 Parent project relationship

The gsd-2-uplift work is staged inside arxiv-sanity-mcp's `.planning/` tree, with explicit migration trigger to a dedicated repo when one exists (per `INITIATIVE.md:181-185` §7). The dedicated repo does not yet exist. Custody rules (per INITIATIVE.md §7):
- DECISION-SPACE.md and the deliberation log STAY in arxiv-sanity-mcp (genesis trail)
- INITIATIVE.md and exploration outputs MIGRATE to the new repo

### §1.3 Current phase

**Active phase: Phase D under (V'.a) replan** — methodology has just shifted from spike-shape to mapping-shape (commit `ffc0fb0` 2026-05-01). Previous Phase D evidence is preserved as "interim work-product" (per commit `43e652b`); replanned mapping-shape Phase D has not yet executed. The trajectory plan revision (Step 2 of (V'.a)) is itself awaiting an audit (Step 3, currently being scoped).

**Predecessor phases A, B, C are complete** (Phase A trajectory-plan-self-audit; Phase B standing-context artifact; Phase C incubation-checkpoint adjudication).

### §1.4 Top-level directory layout

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/`:

| Path | Lines | Purpose |
|---|---|---|
| `INITIATIVE.md` | 224 | Forward-staging artifact; goal articulation; first-wave plan |
| `DECISION-SPACE.md` | 846 | Load-bearing decision reference (B1-B6 + §1.17 audit methodology + §1.18 Phase C dispositions) |
| `EXTERNAL-VISION-CONTEXT.md` | 351 | Standing-context: 12 substrate-vision properties + scope-discipline (2026-05-01) |
| `RELATIONSHIP-TO-PARENT.md` | 90 | Standing-context: test-case-vs-substrate (Phase B output 2026-04-29) |
| `trajectory/cheerful-forging-galaxy.md` | 842 | The trajectory plan (8 phases A-H) |
| `orchestration/` | 11 files | First-wave orchestration package + OVERVIEW.md (90KB log) |
| `audits/` | 7 audit folders | Audit infrastructure |
| `exploration/` | 14 files | First-wave outputs + syntheses + comparison |
| `wave-2/` | decision-trace + pre-D-probes | Phase D (interim) work |

### §1.5 How it is organized

The initiative uses three orthogonal organizational layers that any orchestrator must hold simultaneously:

1. **Initiative-scoping** (top-level: INITIATIVE / DECISION-SPACE / EXTERNAL-VISION-CONTEXT / RELATIONSHIP-TO-PARENT)
2. **Trajectory-execution** (`trajectory/cheerful-forging-galaxy.md` plan + `orchestration/OVERVIEW.md` execution log + per-phase audit folders)
3. **Substantive outputs** (`exploration/` for W1-W3 first-wave + `wave-2/` for Phase D interim)

The `exploration/` directory holds the first-wave (W1-W3) outputs which were the original entry into substrate work; `wave-2/` is a second wave (Phase D execution) that was renamed from a new naming-scheme attempt. The vocabulary is not consistent: "wave" sometimes refers to W1/W2/W3 (the cross-vendor orchestration package), sometimes to the audit's multi-wave structure (wave-1 scout / wave-2 adjudicator / wave-3 meta-synthesis), sometimes to wave-2/ as a phase-D-evidence directory. This is a navigational hazard for fresh readers.

---

## §2. Phase trajectory

### §2.1 The 8-phase plan (trajectory plan §1)

Per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md:174-462` (§1 Trajectory shape):

| Phase | Goal | Status | Output location |
|---|---|---|---|
| **A** | Plan-self-audit (cross-vendor xhigh) | COMPLETE | `audits/2026-04-29-trajectory-plan-audit/` |
| **B** | Standing-context artifact (RELATIONSHIP-TO-PARENT.md + CLAUDE.md load-point) | COMPLETE | `RELATIONSHIP-TO-PARENT.md` + `audits/2026-04-29-relationship-to-parent-audit/` |
| **C** | Incubation-checkpoint adjudication on SYNTHESIS-COMPARISON.md | COMPLETE | `exploration/INCUBATION-CHECKPOINT.md` + DECISION-SPACE.md §1.18 + `audits/2026-04-29-incubation-checkpoint-audit/` |
| **D** | Substrate-shape mapping (REVISED 2026-04-30 from spike-shape to mapping-shape per (V'.a)) | UNDER REPLAN — interim corpus only | `wave-2/decision-trace/` (interim) + `audits/2026-04-30-phase-d-entry-audit/` |
| **E** | Mapping-coherence + theory-construction quality test (REVISED) | NOT STARTED | `MAPPING-COHERENCE-CHECK.md` (planned) |
| **F** | Extraction-readiness gate (REVISED) | NOT STARTED | `EXTRACTION-READINESS.md` (planned) |
| **G** | Extraction execution (move artifacts to dedicated repo) | NOT STARTED | New repo + `EXTRACTION-LOG.md` |
| **H** | Post-extraction integration (verify both repos coherent) | NOT STARTED | EXTRACTION-LOG.md updates |

### §2.2 What "(V'.a)" is and what step is current

**(V'.a)** is the trajectory-replan disposition that fired 2026-04-30 when Phase D mid-arc surfaced a methodology-question-shape-mismatch finding (per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md:191-203`). The "V'" naming derives from the recommendation chain in that deliberation; (V'.a) is the specific replan path Logan accepted.

**(V'.a) has 5 concrete steps** (per the deliberation log §4 + trajectory plan §0.7 Q6):

| Step | Description | Status |
|---|---|---|
| 1 | Mark current Phase D evidence as interim work-product | DONE (commit `43e652b`) |
| 2 | Author trajectory-plan revision (mapping-shape Phase D) | DONE (commit `ffc0fb0`) |
| 3 | Plan-self-audit cycle scoped to question-shape-fit | IN PROGRESS — audit-spec drafting underway |
| 4 | Build frame-revision-check into trajectory mechanics | Mechanism embedded in plan revision; standalone codification disposition pending |
| 5 | Author METHODOLOGY-MISMATCH-FINDING.md as standalone substrate-shape evidence artifact | NOT STARTED |

Latest commit on the branch (`spike/001-volume-filtering`) is **`da64b2c` 2026-05-01** — Step 3 Claude-parallel-skeleton authored. So the active state is: **mid Step 3, with cross-vendor codex audit-spec draft also recently landed (commit `f6af0f1`)**.

### §2.3 The progression as it actually happened

Reading commit history (`git log --oneline --since='2026-04-26'`):

1. **2026-04-26 to 2026-04-27** — Initiative genesis (commits `41cf12b` `5c513fc` `d627a02` audit waves; `b229940` `4c7ad01` AUDIT-SPEC).
2. **2026-04-28** — W3 syntheses + comparison (commits `5313e6c` `73e5615` `ac609c9`); v1-GSD premise-bleed audit-arc (commits `b8db2a0` `fae9650` `a79e761`).
3. **2026-04-29** — Trajectory plan + Phase A + Phase B (commits `f1e0a68` `092da0b` `ee1716d` `24aad62` `767ad6f` `004a1a7`).
4. **2026-04-29** — Phase C steps 2/3-5/6 (commits `4422bab` `e1da6ae` `98505f1` `50f7261`).
5. **2026-04-30** — Phase D entry (commit `5a377fb`); Phase D dispatch mid-arc (commit `c0465a4`); methodology-mismatch finding + (V'.a) disposition (commit `43e652b`).
6. **2026-05-01** — EXTERNAL-VISION-CONTEXT.md + 12-property articulation (commit `c1b098c`); trajectory plan (V'.a) Step 2 revision (commit `ffc0fb0`); Step 3 spec-drafting brief (commit `f6af0f1`); Step 3 Claude parallel skeleton (commit `da64b2c`).

The arc covers ~5 days of intensive work producing ~30 commits on the gsd-2-uplift branch, with the methodology-mismatch finding mid-Phase-D forcing a complete trajectory replan.

### §2.4 OVERVIEW.md as the running execution log

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/OVERVIEW.md` (90KB; 750+ lines) is the procedural shell + dispositions log. §11 (per-wave dispositions log) has accumulated 14 sub-sections (§11.1 through §11.6.14) recording each phase/step disposition with audit results, lessons, and Logan adjudications. This is the canonical execution-state log; STATE.md `stopped_at:` field is a tightly-condensed pointer to its latest sub-section.

---

## §3. Audit infrastructure

### §3.1 Audit folders inventory

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/`:

| Folder | Date | What it audited | Outcome |
|---|---|---|---|
| `2026-04-28-cross-vendor-codebase-understanding-audit/` | 2026-04-28 | Whether the Claude-led W1-W3 investigation understood gsd-2 source well enough | 4-wave audit (scout / adjudicator / meta-synthesis / wave-4 empty); produced META-SYNTHESIS.md as primary grounding for "what gsd-2 actually is"; Gate 2 disposition: localized qualifications needed |
| `2026-04-28-v1-gsd-mental-model-premise-bleed-audit/` | 2026-04-28 | SYNTHESIS-COMPARISON.md for v1-GSD premise-bleed (mental model contamination from old gsd) | 6 artifacts (AUDIT-SPEC + SPEC-REVIEW + FINDINGS Step-1 + FINDINGS-STEP2 + DIFFERENTIAL + DISPOSITION); Logan disposed commit-with-addendum; landed §7 audit addendum |
| `2026-04-29-trajectory-plan-audit/` | 2026-04-29 | The trajectory plan itself (Phase A) | Cross-vendor codex GPT-5.5 xhigh; 9 findings (1A/6B/2C); revise-before-execute; all 9 addressed via in-body revisions |
| `2026-04-29-relationship-to-parent-audit/` | 2026-04-29 | RELATIONSHIP-TO-PARENT.md (Phase B) | Same-vendor adversarial-auditor xhigh paired (audit-findings-A + audit-findings-B); convergent disposition commit-with-addendum; landed §1.1 frame-status-stipulated subsection |
| `2026-04-29-incubation-checkpoint-audit/` | 2026-04-29 | INCUBATION-CHECKPOINT.md (Phase C) | Paired (cross-vendor codex GPT-5.5 xhigh + same-vendor adversarial-auditor xhigh independent) + DIFFERENTIAL.md; Logan disposed Option 4 hybrid (commit-with-revision-and-addendum) |
| `2026-04-30-phase-d-entry-audit/` | 2026-04-30 | Phase D entry MINI-SPEC + STEP1-4 outputs | Paired (cross-vendor codex GPT-5.5 high after attempt-1 hung — see POST-MORTEM.md + same-vendor adversarial-auditor xhigh); 11 findings; Logan disposed Revise-before-dispatch full-width |
| `2026-05-01-trajectory-replan-audit/` | 2026-05-01 | (V'.a) Step 2 trajectory-plan revision (Phase A audit redo, scoped to question-shape-fit) | IN PROGRESS — audit-spec landed (cross-vendor codex draft); SPEC-DRAFTING-BRIEF and CLAUDE-PARALLEL-SKELETON committed; audit dispatch pending Logan disposition |

### §3.2 Audit pattern conventions

Each audit folder typically contains:
- `AUDIT-SPEC.md` — what to audit, with what lenses, against what classification
- `audit-findings-A.md` and/or `audit-findings-B.md` — paired-audit outputs (per `audit-findings*.md` naming convention bypassing `tengu_sub_nomdrep_q7k` regex per `audits/2026-04-29-relationship-to-parent-audit/AUDIT-SPEC.md:4`)
- `FINDINGS.md` and `FINDINGS-STEP2.md` — alternate naming used in pre-2026-04-29 audits (premise-bleed)
- `DIFFERENTIAL.md` — main-thread Claude differential analysis when paired
- `DISPOSITION.md` — Logan's disposition + reasoning trail
- `POST-MORTEM.md` — when something operational went wrong (only in phase-d-entry-audit)
- `.logs/` directory in some folders — codex execution traces

### §3.3 What the audits found (load-bearing summaries)

**Cross-vendor codebase-understanding audit** (`audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md`): produced the canonical "what gsd-2 actually is" frame. Key findings: (1) standalone agent application/runtime (NOT v1-GSD pattern of workflow-markdown + skills + hooks); (2) vendored modified Pi fork plus GSD glue plus bundled extensions; (3) at least 4 parallel extension subsystems; (4) two-engine workflow architecture (markdown-phase + yaml-step); (5) ADR-010 clean-seam refactor proposed-not-implemented. This artifact remains load-bearing context for Phase D mapping work (per trajectory plan §0.4 mandatory pre-reading item 10).

**Premise-bleed audit** (`audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/`): Step-1 cross-vendor codex 6 instances 1A/5B/0C; Step-2 same-vendor independent 9 instances 4A/3B/2C; differential found vendor-position-symmetric. F6+F9 surfaced "integration-grammar-as-fact" (treating SYNTHESIS-COMPARISON.md §5 framing-vocabulary as observed-fact rather than as inputs). Disposition: §7 audit addendum landed with point-of-use foregrounding pattern.

**Trajectory-plan-audit (Phase A)** (`audits/2026-04-29-trajectory-plan-audit/`): Cross-vendor codex GPT-5.5 xhigh; 9 findings (1A/6B/2C). Class C: F1 plan-file artifact-custody (plan was outside arxiv-sanity-mcp); F2 Phase G move/stay map conflicted with INITIATIVE.md §7 custody rule. All 9 addressed in-body. Notable lesson: this audit fired correctly under its scope but did NOT catch the methodology-question-shape-mismatch — because the spec itself was scoped under the misframe (per 2026-04-30 §5.3 audit-discipline-limits finding).

**Phase B audit** (`audits/2026-04-29-relationship-to-parent-audit/`): Same-vendor only (cross-vendor would be M1 strict-undersell); two paired dispatches (audit-findings-A + audit-findings-B) returned commit-with-addendum convergence on F-RTP-1 (artifact treated test-case-vs-substrate as observed-fact rather than stipulated frame); landed §1.1 frame-status-stipulated subsection modeled on SYNTHESIS-COMPARISON.md §7.1 pattern.

**Phase C audit** (`audits/2026-04-29-incubation-checkpoint-audit/`): Paired discipline; convergent C1 finding (§7.4 substrate-shape-anchoring projection) + divergent C2's; Logan disposed Option 4 hybrid (commit-with-revision-and-addendum); landed surgical revisions + §7.9 audit addendum + §7.10 negative-space survey amendment.

**Phase D entry audit** (`audits/2026-04-30-phase-d-entry-audit/`): Paired; first cross-vendor codex dispatch hung (POST-MORTEM.md documents stdin-inheritance bug; 37 min idle; recalibrated codex xhigh→high); 11 findings disposed Revise-before-dispatch; M1 paired-review property described as "strong confirmation" (per OVERVIEW §11.6.11). NOTABLY: this audit did not catch the methodology-question-shape-mismatch that surfaced 24 hours later — per 2026-04-30 §5.3, "audit-spec didn't include 'challenge the intervention-surface choice' or 'challenge the methodology fit'."

**Trajectory-replan audit (V'.a Step 3)** (`audits/2026-05-01-trajectory-replan-audit/`): IN PROGRESS. Three artifacts have landed: AUDIT-SPEC.md (drafted by cross-vendor codex per B-strong protocol), SPEC-DRAFTING-BRIEF.md (Claude's brief to codex), CLAUDE-PARALLEL-SKELETON.md (Claude's blind parallel draft for differential calibration). The audit itself has not yet dispatched.

### §3.4 Audit dispositions pattern

The dispositions follow a 3-option pathway from AUDIT-SPEC.md v2 §8 (and a hybrid Option 4 surfaced 2026-04-29):

- **Commit-as-is**: Class A only or Logan reads B/C as not load-bearing
- **Commit-with-addendum**: Class B/C tractable as addendum
- **Revise-before-commit**: Class C affects load-bearing-claim shape
- **Option 4 hybrid (Logan-disposed 2026-04-29)**: surgical revision at highest-leverage leak surfaces + targeted audit addendum + Phase D dispatch-readiness additions (extension of standard option set)

Audit reasoning-level (xhigh vs high) is per-audit per §2.4 of trajectory plan; codex `high` ≈ Opus `xhigh` per Logan calibration in POST-MORTEM.md §4.

---

## §4. Deliberation infrastructure

### §4.1 Project-level deliberations directory

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/` contains 18 deliberation files + INDEX.md + reviews/ subdirectory. The INDEX.md (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/INDEX.md`) is the navigation entry-point.

**Deliberations directly producing the gsd-2-uplift initiative:**

| File | Date | Status | Role |
|---|---|---|---|
| `2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` | 2026-04-26 | active | Genesis arc; produced INITIATIVE.md + DECISION-SPACE.md + Wave-5 commits; cross-vendor dispatch deferral reasoning |
| `2026-04-27-dispatch-readiness-deliberation.md` | 2026-04-27 | active | First-wave dispatch readiness; produced decisions B1-B6 in DECISION-SPACE.md §1.11-§1.16; orchestration package |
| `2026-04-28-framing-widening.md` | 2026-04-28 | active | **Two-part framing-widening**: extends R1/R2/R3 → R1-R5 design space; six-context plurality of "long-horizon"; four-act plurality of "uplift"; 17-item deferred items log §9 |
| `2026-04-28-tier-comparison-preliminary.md` | 2026-04-28 | preliminary | GPT-5.5 medium vs high reasoning-effort tier comparison for codebase work |
| `2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` | 2026-04-28 | active | D1-D5 dispositions for W2 audits + W3 synthesis dispatch shape |
| `2026-04-28-comparison-drafting-decisions.md` | 2026-04-28 | active | DC0-DC4 dispositions for SYNTHESIS-COMPARISON.md drafting |
| `2026-04-28-audit-spec-review-deliberation.md` | 2026-04-28 | adjudication-complete | Audit-spec review-and-response for v1-GSD premise-bleed audit; F1-F7 adjudications |
| `2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` | 2026-04-30 | deliberation-complete; (V'.a) disposed | **The methodology-mismatch finding + (V'.a) disposition canonical record** |

### §4.2 Pre-uplift deliberations referenced as standing context

| File | Date | Status | Why it matters |
|---|---|---|---|
| `2026-04-25-long-arc-and-multi-lens-redirection.md` | 2026-04-25 | produced-ADR | Used as test-task in Phase D first-target spike (per `wave-2/decision-trace/EXECUTION-LOG.md`) |
| `2026-04-25-pressure-artifacts-before-remedy.md` | 2026-04-25 | policy-adopted | Reusable workflow discipline; feeds METHODOLOGY.md |
| `2026-04-25-recording-deliberations-extensively.md` | 2026-04-25 | policy-adopted | Meta-deliberation establishing the deliberation-log discipline that this initiative instantiates |

### §4.3 No deliberations directory inside gsd-2-uplift/

The gsd-2-uplift initiative does not have its own deliberations/ subdirectory. All deliberation logs live at the project level (`.planning/deliberations/`). This is intentional per INITIATIVE.md §7 custody rule (deliberation log STAYS in arxiv-sanity-mcp at extraction time).

### §4.4 Named methodological deliberations

Three deliberations have produced named methodological patterns invoked elsewhere:

- **framing-widening** (`2026-04-28-framing-widening.md`): defines R1-R5 design space + six-context plurality (A solo-research / B small-team / C enterprise / D platform-team / E transition-as-event / F transition-as-stance) + four-act plurality of uplift (modify / configure / orchestrate-around / replace-informed-by) + §9 17-item deferred items log. Cited throughout subsequent work.
- **premise-bleed audit-arc** (`audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/`): paired-vendor audit pattern (Step-1 cross-vendor + Step-2 same-vendor independent + DIFFERENTIAL + Logan disposition). Has become the standard audit-arc shape; §1.17 in DECISION-SPACE codifies as "7-rule audit methodology."
- **methodology-mismatch finding** (`2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md`): names the spike-vs-mapping question-shape distinction that triggered (V'.a) replan.

---

## §5. Wave/exploration outputs

### §5.1 exploration/ directory contents

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/`:

**Per-slice W1 outputs (cross-vendor codex GPT-5.5 high):**
- `01-mental-model-output.md` (28KB)
- `02-architecture-output.md` (32KB) + `02-architecture-audit.md`
- `03-workflow-surface-output.md` (33KB)
- `04-artifact-lifecycle-output.md` (45KB) + `04-artifact-lifecycle-audit.md`
- `05-release-cadence-output.md` (49KB) + `05-release-cadence-audit.md`

Plus side-investigation outputs:
- `capabilities-production-fit-findings.md` (46KB)
- `w2-markdown-phase-engine-findings.md` (22KB)

**W3 syntheses + comparison:**
- `SYNTHESIS.md` (79KB; same-vendor Claude Opus xhigh; 609 lines; F1-F8 numbered findings stratification)
- `SYNTHESIS-CROSS.md` (32KB; cross-vendor codex GPT-5.5 high; 207 lines)
- `SYNTHESIS-COMPARISON.md` (86KB; in-session-collaborative comparison; 9 convergent + 3 divergent + 6 asymmetric findings; 4-axis incubation-checkpoint integration §5)
- `INCUBATION-CHECKPOINT.md` (89KB; Phase C surfacing artifact + §7 disposition record + §7.9 audit addendum + §7.10 Phase D entry pre-mini-spec amendment)

### §5.2 SYNTHESIS-COMPARISON.md role (referenced repeatedly)

`exploration/SYNTHESIS-COMPARISON.md` is the load-bearing input that fed the entire trajectory plan. It integrates the two paired W3 syntheses:

- **§1 Convergent findings** (9): Pi vendoring; extension plurality; two-engine architecture; release machinery-vs-practice gap; docs-vs-source drift; R2 viable; telemetry/observability/security centrality; B4 split holding; R3 under-evidenced.
- **§2 Divergent findings** (3): R4 weighting (substantive interpretive-disposition-timing); R5 framing (register at common operational endpoint); synthesis register/length (artifact-shape).
- **§3 Asymmetric coverage** (6 items).
- **§4 Five methodological observations**: M1 paired-review observed-as-claimed-in-some-instances-and-inverted-in-others; convergence-as-robustness-within-framing; tier-comparison preliminary; framing-import drift surfaced (initiative-maturity signal); stratification methodology converged.
- **§5 Four-axis incubation-checkpoint integration**: §5.1 metaquestion / §5.2 R-mix / §5.3 six-context anchoring / §5.4 side-probe triggers / §5.5 cross-axis composition.
- **§6 Confidence + limits + D5a in-session-collaboration caveat.**
- **§7 Premise-bleed audit addendum** (landed 2026-04-29 post-audit): §7.1 reading-frame for §5 axes (the "point-of-use foregrounding" pattern); §7.2 artifact-side carry-forward; §7.3 what-the-audit-did-not-surface; §7.4 cross-references.

The §7.1 reading-frame (treating R1-R5 / six-context / four-act vocabulary as inputs Logan brought in via framing-widening, NOT as observed facts in gsd-2) is invoked at point-of-use by every downstream artifact.

### §5.3 wave-2/ directory

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/wave-2/`:

- `pre-D-probes/` — Phase D entry pre-flight probes:
  - `M2-codebase-snapshot-findings.md` (35KB; gsd-2 skill subsystem snapshot + primitives inventory)
  - `P5-effective-state-emission-findings.md` (24KB; effective-state emission probe)
  - `STEP1-design-space.md` + `STEP1-DISPOSITION.md` (5 candidate shapes A/D/E/F/G; Logan disposed §6.E primary + §6.E.(i) parallel R4 comparator)
  - `STEP2-practical-decisions.md` (existing-clone branch + `~/workspace/projects/gsd-2-explore/` + 8-day budget + 5 abort triggers)
  - `STEP4-gates-and-L-tier.md` (gates + L-tier sweep)

- `decision-trace/` — Phase D execution work-product (NOW MARKED INTERIM per (V'.a) Step 1):
  - `MINI-SPEC.md` (49KB; Phase D dispatch contract under spike framing; superseded by replan)
  - `EXECUTION-LOG.md` (52KB; Phase D execution log §0-§4; §4 INTERIM-OUTPUT marker)
  - `TRAIL-2026-04-25-multi-lens-redirection.md` (21KB; subagent invocation evidence — channel-(a) clean pass on B1/B2/B4/B5/B5b/B5c)

The interim Phase D evidence corpus surfaced two substantive findings:

1. **Skill-shape gsd-2-native-placement misfit** (per 2026-04-30 §3.1): Decision-trace's gsd-2-native placement is companion-tool to `gsd_decision_save` MCP tool (analogous to `gsd graph query`) OR extension structurally analogous to forensics. Skill-shape was R4 (orchestrate-without-modifying) disguised as R2 (extension).
2. **Substrate-mismatch IS substrate-shape evidence** (per 2026-04-30 §3.2): arxiv-sanity-mcp does NOT use `gsd_decision_save`; arxiv-sanity-mcp's actual decision-trail lives in `.planning/deliberations/` + ADRs + handoffs + git + audits + STATE.md. The misfit between gsd-2's decision-DB substrate and arxiv-sanity-mcp's actual conventions is itself substrate-shape evidence channel-(b).

These two findings are now carried forward into the replanned mapping-shape Phase D as inputs (not as final findings).

---

## §6. Methodology artifacts

### §6.1 Disciplines that have crystallized

Multiple methodological patterns have emerged from the gsd-2-uplift work. Most are NOT yet codified in reusable form (per pending-todo in STATE.md re: codification of session-disciplines).

| Discipline | First named at | Codified in | Status |
|---|---|---|---|
| **M1 paired-review property** | `.planning/spikes/METHODOLOGY.md:104-115` (pre-uplift) | `METHODOLOGY.md:104-115` | Refined: SYNTHESIS-COMPARISON.md §4.1 notes asymmetry empirically more complex (cross-vendor catches substance/vocabulary; same-vendor catches register/integration-grammar — but observed-as-inverted in some instances) |
| **Framing-widening** | `2026-04-28-framing-widening.md` | The deliberation log itself (acts as canonical reference); not yet abstracted to METHODOLOGY.md | Active (Part I framing widened; Part II roadmap derived; deferred-items log §9 with 17 items) |
| **Premise-bleed audit-arc** | `2026-04-28-v1-gsd-mental-model-premise-bleed-audit/` | DECISION-SPACE.md §1.17 (7-rule audit methodology) + AUDIT-SPEC.md v2 | Codified — used as template for Phase A/B/C/D audits |
| **Audit-of-audit** | Implicit in (V'.a) Step 3 | Trajectory plan §2.4 paired-default for Step 3 audit-spec drafting itself; SPEC-DRAFTING-BRIEF.md + CLAUDE-PARALLEL-SKELETON.md (B-strong) | In-flight — first instance is the active 2026-05-01 trajectory-replan audit |
| **Closure-pressure-into-elaboration pattern** | `LONG-ARC.md:51` (pre-uplift) + recurring observations | Named in many deliberations; codification pending | RECURRING — observed at every layer, including 2026-05-01 turn-cluster (per EXTERNAL-VISION-CONTEXT.md §7.1) |
| **Comfort-language detection** | AGENTS.md (pre-uplift) | AGENTS.md anti-patterns | Active discipline |
| **Performative-vs-operational openness** | Pre-uplift | AGENTS.md | Active discipline; explicitly called out in §0.6 failure-mode taxonomy |
| **Point-of-use foregrounding** | Premise-bleed audit § 7.1 reading-frame; carried forward | SYNTHESIS-COMPARISON.md §7.1 + replicated in RELATIONSHIP-TO-PARENT.md §1.1 + INCUBATION-CHECKPOINT.md §0.2 | Pattern transferable; "applied recursively to itself" pattern noted |
| **Frame-revision-check ((V'.a) Step 4)** | `2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` §4 step 4 | Trajectory plan §0.5 + §6.1 + §6.2 + §1.4 process steps 2/5/9 | Embedded in trajectory mechanics; codification disposition pending |
| **Methodology-question-shape-mismatch** | `2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` §3.5 | Trajectory plan §0.6 + §5.6 row | Added as 14th failure-mode kind; row added 2026-04-30 |
| **METHODOLOGY-MISMATCH-FINDING.md as artifact** | (V'.a) Step 5 | Trajectory plan §3.1 D-aux row | NOT YET AUTHORED — Step 5 pending |
| **Logan-disposition discipline scope clarification** | `2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` §2.7 | Codification candidate for `.planning/spikes/METHODOLOGY.md` or `AGENTS.md` | Pending threshold-judgment per DECISION-SPACE §3.9 |
| **Offshoot pattern** | EXTERNAL-VISION-CONTEXT.md §7.5 (per Property 8) | Demonstrated 2x (gsd-modifier→harness-studio 2026-04-24; prix-guesser→paddock 2026-04-25); needs 3rd instance per existing pattern | Threshold-pending |
| **B-strong protocol** (audit-spec independence at scope-level) | Self-review of (V'.a) Step 2 Concern 1 | SPEC-DRAFTING-BRIEF.md + CLAUDE-PARALLEL-SKELETON.md (first instance) | First instance executing now |
| **Burden-of-proof on exclusion** | EXTERNAL-VISION-CONTEXT.md §4.1 (Logan-corrected) | EXTERNAL-VISION-CONTEXT.md §4.1 + §7.2 | Codified as scope-discipline |
| **Four-category C1/C2/C3/C4 scope-confidence model** | EXTERNAL-VISION-CONTEXT.md §4.2 | EXTERNAL-VISION-CONTEXT.md §4.2 | Codified for mapping-shape Phase D scope-control |
| **Identity-distortion narrowness** | EXTERNAL-VISION-CONTEXT.md §4.3 + §7.3 | EXTERNAL-VISION-CONTEXT.md §4.3 | Codified |

### §6.2 The 14-row failure-mode taxonomy

Per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md:122-139` §0.6 + §5.6 control matrix at lines 727-746:

1. Framing error
2. Premise-bleed
3. Closure-pressure
4. Scope creep
5. Comparative-claims-without-comparative-data
6. False-confidence calibration
7. Comfort-language
8. Performative-vs-operational openness
9. Integration-grammar-as-fact
10. Skill-heuristic shallow-match
11. Strict-M1 undersell at recommendation stage
12. Execution error
13. In-session-collaboration risk
14. **Methodology-question-shape mismatch (added 2026-04-30 per (V'.a))**

Each row maps in §5.6 to: phase(s) where it applies, concrete check, recorded-at artifact, and owner (Logan / auditor / executor).

### §6.3 Where methodology gets codified vs. left at deliberation-level

Pattern observed: methodology codification in `.planning/spikes/METHODOLOGY.md` requires a 2-3 deliberation-log threshold per DECISION-SPACE §3.9. As of STATE.md's pending-todos: the threshold has been reached on closure-pressure recurrence + comfort-language + performative-vs-operational openness + non-exhaustive-listings + push-for-assumptions + skill-heuristic shallow-match + strict-M1 undersell — codification candidate ready but not executed. METHODOLOGY-MISMATCH-FINDING.md ((V'.a) Step 5) is the only one explicitly committed to standalone-artifact form.

---

## §7. Migration plan

### §7.1 Phase G artifact-by-artifact disposition table

Per `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md:387-407` §1.7:

| Artifact | Disposition | Reasoning |
|---|---|---|
| `INITIATIVE.md` | **MOVE** | Initiative-scoping artifact; replace in arxiv-sanity-mcp with thin pointer |
| `DECISION-SPACE.md` | **STAY** (per INITIATIVE.md §7) | Records arxiv-sanity-mcp's session genesis |
| `exploration/` | **MOVE** | Initiative-scoping exploration outputs |
| `audits/` | **MOVE** | Audits about uplift artifacts |
| `orchestration/OVERVIEW.md` | **MOVE** | Initiative coordination record |
| `wave-2/` | **MOVE** | Substrate-shape mapping work (interim + final) |
| `RELATIONSHIP-TO-PARENT.md` | **DUPLICATE** (cite-by-reference) | Intrinsically about both sides; bidirectional reference |
| `EXTERNAL-VISION-CONTEXT.md` | **DUPLICATE** (cite-by-reference) | Per its frontmatter `post_extraction_disposition: DUPLICATE`; vision-context cross-project |
| `METHODOLOGY-MISMATCH-FINDING.md` | **DUPLICATE** (cite-by-reference) | Self-correction from initial MOVE on Step 2 self-review; substrate-shape evidence + diagnostic-loop record |
| `2026-04-30-phase-d-methodology-mismatch...` deliberation | **Per-deliberation Logan-disposed** | Both readings (STAY for session-dynamic; MOVE for substrate-shape content) defensible |
| `trajectory/cheerful-forging-galaxy.md` | **MOVE** (with arxiv-sanity-mcp citation kept) | Plan governs the extraction it just executed |
| Genesis-recording deliberations (`2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md`) | **STAY** (per INITIATIVE.md §7) | Session-genesis records |
| Uplift-substantive deliberations (`2026-04-28-framing-widening`, comparison-drafting, audit-spec-review) | **Per-deliberation Logan-disposed** | Default heuristic: STAY if session-dynamic; MOVE if substrate-shape-substantive |
| Uplift handoffs (`.planning/handoffs/`) | **Per-handoff Logan-disposed** | Default heuristic: STAY if bridges arxiv-sanity-mcp stewardship; MOVE if bridges new-repo work |
| `.planning/spikes/` | **STAY** | Diagnostic about substrate-shape but the spike work is arxiv-sanity-mcp-shaped |
| `.planning/foundation-audit/` | **STAY** | Project-side; about arxiv-sanity-mcp |
| Methodology files (METHODOLOGY.md, LONG-ARC.md, AGENTS.md, CLAUDE.md) | **STAY (and reapply, not migrate)** | Current-runtime-shaped; new repo authors its own |

### §7.2 What gets cited-by-reference

**From new repo to arxiv-sanity-mcp** (per trajectory plan §1.7):
- Spike-program outputs (substrate behavior under arxiv-sanity-mcp-spike conditions)
- Foundation-audit findings (project-side substrate-handling evidence)
- DECISION-SPACE.md (genesis decision-trail)
- Genesis-recording deliberations + handoffs

**From arxiv-sanity-mcp to new repo**:
- INITIATIVE.md (replaced with ~10 line thin pointer)
- exploration/, audits/ (replaced with similar pointers)
- This trajectory plan
- RELATIONSHIP-TO-PARENT.md (kept locally + cites new-repo copy)

### §7.3 Phase H verification

Per trajectory plan §1.8: fresh-context Claude tests on each side that load-bearing reconstruction works. "Yes" means coherence-with-intact-references-back, NOT independence. The diagnostic-loop relationship (arxiv-sanity-mcp practice as substrate-evidence-channel) must remain readable post-extraction.

### §7.4 Migration trigger has not yet fired

The migration is gated on Phase F passing (extraction-readiness). Phase F is gated on Phase E passing (mapping-coherence). Phase E is gated on Phase D producing a substrate-shape map. **Phase D has not yet executed under the replanned mapping-shape**. The interim Phase D corpus + the (V'.a) Step 3 audit are between current state and Phase D mapping-shape execution.

The dedicated repo does not exist yet (per INITIATIVE.md §7 + STATE.md pending-todos).

---

## §8. What's stuck or in flight

### §8.1 Active right now (latest commit `da64b2c` 2026-05-01)

**(V'.a) Step 3 audit-spec drafting** — three artifacts in `audits/2026-05-01-trajectory-replan-audit/`:

1. `SPEC-DRAFTING-BRIEF.md` (commit `f6af0f1`): Claude's brief to cross-vendor codex GPT-5.5 xhigh; explains why codex (not Claude) is drafting the spec ("recursive failure-mode" — if Claude scopes the spec, Step 3 reproduces Phase A's failure mode of scoping under the same misframe as the artifact).
2. `AUDIT-SPEC.md` (committed; codex-authored): the actual audit-spec; 29KB; says "this spec accepts the brief's required lens families but does not treat the brief's frame as final"; explicit departures from brief listed in §1.3.
3. `CLAUDE-PARALLEL-SKELETON.md` (commit `da64b2c`): Claude's blind parallel skeleton for differential calibration; documents what Claude WOULD have drafted; "the divergence itself is signal about (V'.a) Step 2's framing-inheritance residuals."

**Logan-side action remaining for Step 3 dispatch** (per STATE.md):
- Dispose audit-spec drafting form (B-strong/medium/weak)
- Optional fresh-session re-read before Step 3 audit dispatch (Logan-side intuitions feed audit-spec lens-questions)

**Working tree state at this entry** (per STATE.md `stopped_at:`):
- arxiv-sanity-mcp dirty (cheerful-forging-galaxy.md + OVERVIEW.md + STATE.md uncommitted) — note this is from Step 2 commit; check git status for current
- harness-studio clean
- gsd-2-explore phase-d-decision-trace-spike branch unchanged from `23b1ddc89`

### §8.2 Pending (V'.a) execution steps

Per STATE.md and trajectory plan §0.7 Q6:
- **Step 3** (in progress): plan-self-audit cycle scoped to question-shape-fit
- **Step 4** (mechanism in plan; standalone codification disposition pending): frame-revision-check codification
- **Step 5** (NOT STARTED): METHODOLOGY-MISMATCH-FINDING.md standalone artifact

### §8.3 Pending phases (E, F, G, H)

Phase E (mapping-coherence test) requires Phase D mapping-shape outputs which require (V'.a) Step 3 to dispose. Phases F/G/H all downstream.

### §8.4 Pending standing-action items (per STATE.md pending-todos)

- Draft `.planning/gsd-2-uplift/ORCHESTRATION.md` per decision B6 — superseded in practice by `orchestration/OVERVIEW.md`; pending-todo entry stale
- Light orchestration-plan audit before pilot dispatch — done as cross-vendor + reaudit
- Pilot dispatch through W3 synthesis — done
- Selective W2 audits — done
- Incubation checkpoint — done (Phase C)
- Stage 1 audit findings (deferred quality + minor) — opportunistic
- Phase 12 plan 1 authoring (on hold pending uplift findings + incubation checkpoint)
- Codification of session-disciplines threshold reached — pending evaluation
- Migration of `.planning/gsd-2-uplift/` artifacts to dedicated repo — pending Phase F

### §8.5 Active blockers

Three structural blockers:

1. **Methodology-question-shape-mismatch** (resolved disposition; execution not yet finalized): (V'.a) Step 3 audit must dispatch and dispose before Phase D mapping-shape can begin.
2. **Closure-pressure-into-elaboration pattern recurrence** (per EXTERNAL-VISION-CONTEXT.md §7.1 + 2026-04-30 §5.4 calibration findings): this pattern is documented as surviving /effort max + pattern-recognition-active + paired audit-discipline + premise-bleed audit precedent. It broke only on Logan-correction-with-defense-against-critics-framing. The pattern is a "live risk under (V'.a), not resolved one" per STATE.md `stopped_at:` field.
3. **In-session-collaboration risk compounding** (D5a per Step 3 brief §4.2 Q-FI-5): "Each artifact in the chain inherits Logan-co-framing from prior artifacts. The chain compounds without independent breaks (Phase A audit was the prior independent break; nothing since 2026-04-29)."

### §8.6 What's not yet done that the plan says is required

- METHODOLOGY-MISMATCH-FINDING.md ((V'.a) Step 5) — referenced in §0.4 mandatory pre-reading item 17 of trajectory plan as "forthcoming"
- Phase D mapping-shape execution (substrate-shape map) — the load-bearing artifact for Phases E/F
- Phase E/F/G/H — all not started

---

## §9. Tone observations

The following observations are descriptive, not evaluative.

### §9.1 Register

The register is **methodology-heavy, recursive, and self-instrumenting**. Examples:

- The trajectory plan (`cheerful-forging-galaxy.md`) is 842 lines with 8 phases; each phase carries goal/inputs/outputs/quality-gate/failure-branch/commit; the plan has its own phase A "plan-self-audit" + (V'.a) re-audit underway.
- The Step 3 audit infrastructure includes: SPEC-DRAFTING-BRIEF (Claude → codex), AUDIT-SPEC (codex draft), CLAUDE-PARALLEL-SKELETON (Claude blind parallel for differential), each with its own framing-inheritance-risk acknowledgment.
- RELATIONSHIP-TO-PARENT.md applies its own §7.1 reading-frame discipline to itself recursively (per RELATIONSHIP-TO-PARENT.md §1.1).
- EXTERNAL-VISION-CONTEXT.md §7 records meta-disciplines surfaced through the conversation that produced EXTERNAL-VISION-CONTEXT.md.
- The §0.6 failure-mode taxonomy added a 14th row ("methodology-question-shape mismatch") on 2026-04-30 in response to the failure mode that produced (V'.a). That row is then mapped in §5.6 control matrix.

### §9.2 Bias toward elaboration vs. closure

The artifacts repeatedly name closure-pressure as a recurring pattern requiring active resistance:

- LONG-ARC.md anti-patterns include "Closure pressure at every layer."
- Multiple deliberations record closure-pressure-into-elaboration recurrence (2026-04-25 multi-lens redirection; 2026-04-26 dispatch-deferral; 2026-04-30 §5.1 + §5.4 finding the pattern survives /effort max + pattern-recognition-active; 2026-05-01 EXTERNAL-VISION-CONTEXT.md §7.1 records recurrence in the very turn-cluster that produced the corrective artifact).
- The trajectory plan §0.5 explicit discipline: "Closure-pressure recurrence: 'resolved enough to commit' framings... resist."
- Multiple artifacts mark their own status with caveats: "single-author + in-session-collaboration fallibility caveat"; "frame status — stipulated, not observed"; "self-review process operates-or-performs."

The pattern observed in artifacts: ELABORATION is the default; CLOSURE requires pause + Logan-correction. (V'.a) is itself an instance of replanning rather than closing — the closure happens only at Logan-disposition moments, and even then is qualified ("I accept (V'.a) but lets perhaps record these decisions and this deliberation so I can compact").

### §9.3 Meta-work vs. product work

The orchestration package (`orchestration/`) plus audits (`audits/`) plus trajectory plan + standing-context artifacts together total roughly 100KB+ of meta-work artifacts; the substantive substrate-shape evidence (interim Phase D corpus in `wave-2/decision-trace/`) is ~52KB of EXECUTION-LOG.md + ~21KB of TRAIL + the MINI-SPEC. The proportion of meta-work to product work is high.

The arxiv-sanity-mcp product work (v0.2 multi-lens substrate; Phases 12-17) is **explicitly on hold** per STATE.md "Phase 12 plan 1 authoring (on hold pending gsd-2 uplift first-wave findings + incubation checkpoint)."

### §9.4 Vocabulary density

The vocabulary is dense and self-referential. A partial list of named patterns/disciplines an outside reader must hold:

- M1 paired-review property (with empirical-complexity refinement)
- D5a in-session-collaboration caveat
- §7.1 reading-frame (point-of-use foregrounding)
- Closure-pressure-into-elaboration pattern
- Framing-widening (R1-R5; six-context; four-act)
- Premise-bleed audit-arc
- Audit-discipline limits (per 2026-04-30 §5.3)
- Frame-revision-check ((V'.a) Step 4 mechanism)
- Methodology-question-shape mismatch
- Identity-distortion narrowness
- Burden-of-proof on exclusion
- Four-category C1/C2/C3/C4 scope-confidence model
- 12 substrate-vision properties (per EXTERNAL-VISION-CONTEXT.md §3)
- 5 active properties (per EXTERNAL-VISION-CONTEXT.md §1)
- B-strong protocol
- Test-case-vs-substrate framing
- Pressure-not-destination
- Offshoot pattern
- Logan-disposition discipline scope clarification
- Heal-skill observation hook
- Spikes-nest-inside-mapping discipline
- "horizon stack" (long / medium / short / immediate)

### §9.5 Naming conventions

The `(V'.a)` notation, `M1`/`M2`/`M3`/`M4`/`M5`, `P1`/`P2`/`P3`/`P4`/`P5`, `B1`/`B2`/`B3`/`B4`/`B5`, `R1`/`R2`/`R3`/`R4`/`R5`, `S1`-`S8`, `C1`/`C2`/`C3`/`C4`, `F-RTP-1`/`F-IC-A1`/`F-PD-A1`, `H1`-`H7` + `M1`-`M5` + `L1`-`L8`, etc. are all distinct schemes used in different contexts. Without prior context, vocabulary lookup is required.

### §9.6 Single-author fallibility caveats

Many artifacts begin or end with "single-author + in-session-collaboration fallibility caveat" referring to the same Claude+Logan in-session collaboration that produced them. The caveat acknowledges Claude inheritance from Logan's framing. The caveat is genuine; the practice of carrying it forward into every artifact has produced a thicket of "this artifact may be wrong because the same author wrote the previous artifact" notes.

---

## §10. Quick assessment

What the artifacts evidence (no recommendation):

### §10.1 Evidence visible from the artifacts

**Pace observation**: The initiative produced ~30 commits in ~5 days (2026-04-26 to 2026-05-01). Each commit includes substantial documentation work (audits, dispositions, deliberations). The Phase D execution alone produced multi-thousand-line work products (EXECUTION-LOG.md + TRAIL + MINI-SPEC + interim corpus). Then the methodology-mismatch finding mid-Phase-D forced a complete trajectory-replan, marking that work as interim.

**Closure observation**: Per the calibration findings explicitly recorded:
- Five frame-revisions during Phase D mid-arc on Logan's direct prompting (2026-04-30 §1.1-§1.6)
- The closure-pressure-into-elaboration pattern survives /effort max + pattern-recognition-active + paired audit-discipline (2026-04-30 §5.4)
- The pattern recurred again during the 2026-05-01 turn-cluster that produced EXTERNAL-VISION-CONTEXT.md (§7.1)
- The pattern recurred during the self-review process for (V'.a) Step 2 (per plan final caveat note)
- The Phase D entry paired audit fired but did NOT catch the methodology-question-shape-mismatch (2026-04-30 §5.3)

**Trajectory observation**: Phase A complete; Phase B complete; Phase C complete; Phase D under (V'.a) replan with current evidence corpus marked interim per 2026-04-30 §2.8 + commit `43e652b`. Phases E-H reshaped under (V'.a) but not yet executed. (V'.a) itself has 5 steps; Steps 1+2 done; Step 3 in progress; Steps 4+5 pending.

**Goal observation**: Per `EXTERNAL-VISION-CONTEXT.md:54` (project-shape definition corrected 2026-05-01): the project is "an identity-preserving, pressure-respecting uplift of gsd-2... pushes its limits in reasonable ways toward a set of reasonable objectives — discovered and refined through exploration." The 12 substrate-vision properties (§3) describe what the eventual substrate would do; the C1/C2/C3/C4 scope-confidence model (§4.2) describes how to gate them; mapping-shape Phase D (per trajectory plan §1.4) is the work that would produce the evidence those decisions need.

**Foreclosure observation**: The dedicated repo for the uplift project does not yet exist (INITIATIVE.md §7 migration trigger has not fired). The trajectory plan Phase G is the planned extraction step; it is gated on Phases D/E/F all passing. The cited migration triggers in trajectory plan §1.6 criterion 4 (a/b/c/d) include: (a) disposition explicitly commits to dedicated-uplift-repo; (b) substrate-shape mapping work has internal gravitational center independent of arxiv-sanity-mcp; (c) materially-competing-for-shared-resources signal; (d) cross-project portfolio-shape work.

**Product impact observation**: Per STATE.md, "Phase 12 plan 1 authoring [is] on hold pending gsd-2 uplift first-wave findings + incubation checkpoint." The arxiv-sanity-mcp v0.2 product work (multi-lens substrate; Phases 12-17) is sequenced behind the gsd-2-uplift evaluation. The current branch is `spike/001-volume-filtering` but no spike-001 work has been done on this branch since 2026-04-26; all commits on this branch since then are gsd-2-uplift documentation.

**Pattern-recursion observation**: The (V'.a) Step 3 audit infrastructure (SPEC-DRAFTING-BRIEF + AUDIT-SPEC + CLAUDE-PARALLEL-SKELETON) is explicitly designed to break the framing-inheritance recursion that the previous Phase A audit failed to break. The audit-of-audit pattern is itself an artifact of recognizing that audits scoped under the same misframe don't catch the misframe. Whether this iteration breaks the recursion is open.

### §10.2 What an orchestrator would need to dispose

To answer "should this work be folded into an existing milestone, extracted to its own project, or paused":

**Evidence pertinent to "fold into existing milestone"**:
- The methodology-mismatch finding is substantive substrate-shape evidence (per 2026-04-30 §3.1-§3.2): two distinct findings about gsd-2 surface-mechanics vs. arxiv-sanity-mcp practice that the spike methodology produced as side-effects.
- The 12 substrate-vision properties + scope-discipline (per EXTERNAL-VISION-CONTEXT.md §3-§4) are now articulated and committed.
- arxiv-sanity-mcp's v0.2 milestone (Phases 12-17) is explicitly on hold pending uplift findings.

**Evidence pertinent to "extract to its own project"**:
- The artifacts are ~50% generic substrate-design content (EXTERNAL-VISION-CONTEXT.md, methodology disciplines, audit infrastructure) that would belong in a dedicated repo.
- The artifacts repeatedly cite the migration trigger (INITIATIVE.md §7) and have explicit DUPLICATE/MOVE/STAY dispositions per artifact.
- harness-studio (the larger vision repo) already exists at `~/workspace/projects/harness-studio/`; the offshoot pattern (Property 8) is demonstrated 2x.
- Phase G extraction is the planned endpoint of the trajectory plan; it is gated on Phases D/E/F passing.

**Evidence pertinent to "pause"**:
- The closure-pressure-into-elaboration pattern is documented as surviving /effort max + pattern-recognition-active + paired audit-discipline (per 2026-04-30 §5.4 + 2026-05-01 §7.1).
- The recursion of audit-on-audit (Step 3 includes brief + spec + parallel-skeleton + paired audit + Logan disposition) means each iteration costs ~1-2 days of intensive context.
- The interim Phase D corpus (now marked superseded) represents ~1 day of work that did not produce final findings.
- The trajectory plan replan history: Phase D under spike-shape produced the corpus; the corpus surfaced the methodology-mismatch; (V'.a) replan was Step 2 of redoing Phase D; Step 3 is auditing the replan; Step 4 is codifying the mechanism; Step 5 is documenting the finding. 5 sub-steps to redo Phase D.

**The artifacts do not themselves recommend any of these three.** Disposition is Logan's per INITIATIVE.md §0 disposition discipline.

---

## §11. Reading paths for the orchestrator

For navigating in 30 minutes:
1. `INITIATIVE.md` (~30 min read; the goal articulation + first-wave plan)
2. `RELATIONSHIP-TO-PARENT.md` (~10 min; test-case-vs-substrate framing — load-bearing for any session)
3. `STATE.md` lines 1-35 (~5 min; current state)
4. `trajectory/cheerful-forging-galaxy.md` §0.1-§0.8 + §1.1-§1.8 phase summaries (~30 min)
5. Skim `orchestration/OVERVIEW.md` §11 for execution-state log

For navigating in 2 hours (full context):
6. `EXTERNAL-VISION-CONTEXT.md` (351 lines; 12 substrate-vision properties + scope-discipline)
7. `DECISION-SPACE.md` §1.7 metaquestion + §1.8 R-mix + §1.18 Phase C dispositions
8. `2026-04-28-framing-widening.md` §1-§5 (R1-R5 + six-context + four-act)
9. `2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md` (the methodology-mismatch finding + (V'.a))
10. `exploration/SYNTHESIS-COMPARISON.md` §0-§7 (incubation-feeding integration)
11. `audits/2026-05-01-trajectory-replan-audit/SPEC-DRAFTING-BRIEF.md` + `AUDIT-SPEC.md` + `CLAUDE-PARALLEL-SKELETON.md` (current active state)

---

*Map authored 2026-05-01 by orchestrator audit agent (Opus 4.7 1M-context). The map describes what is in the artifacts; it does not recommend what to do with the work. Single-author + in-session-collaboration caveat applies recursively (this map is a single-author artifact reading single-and-collaborative-author artifacts; readings may differ; if any item feels mis-articulated, re-read the cited artifact).*
