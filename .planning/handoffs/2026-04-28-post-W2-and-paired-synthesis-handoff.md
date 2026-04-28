---
type: session-handoff
date: 2026-04-28
status: post-W2-audits-disposed; both W3 syntheses (same-vendor + cross-vendor) landed; SYNTHESIS-COMPARISON.md pending; incubation-checkpoint downstream
predecessor: .planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md
purpose: |
  Hand off the 2026-04-28 W2-audits-disposed → W3-paired-synthesis-landed
  session arc to fresh sessions. The arc covered: W2 audit dispatch + disposition
  + recording (D1-D4); W3 same-vendor synthesis dispatch + landing (D5);
  paired-synthesis escalation triggered + dispatched + landed; SYNTHESIS-COMPARISON.md
  pending in-session-collaborative draft.

  Fresh session's primary work is producing SYNTHESIS-COMPARISON.md per the
  proposed structure in §6 below (or revising the structure if Logan disposes
  differently). The comparison artifact feeds incubation-checkpoint per
  `DECISION-SPACE §2.3`. Incubation itself is Logan-led + out of orchestration
  scope.

  This handoff is written for fresh sessions to execute cold. Predecessor context
  restoration is helpful but not strictly required.
onboarding_read_order: |
  Read in this order if starting fresh:
  1. CLAUDE.md (project root) — auto-loaded; establishes project identity.
  2. AGENTS.md — agent behavior rules + project-specific anti-patterns.
  3. This handoff — full state of play and next-stage execution sequence.
  4. .planning/gsd-2-uplift/exploration/SYNTHESIS.md — Claude Opus xhigh
     same-vendor synthesis (609 lines); load-bearing input #1 for comparison.
  5. .planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md — codex GPT-5.5 high
     cross-vendor synthesis (207 lines); load-bearing input #2 for comparison.
  6. .planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md
     — D1-D5 disposition log with conditional structure ("what would change each
     recommendation"); auditable record of why each disposition was chosen.
  7. .planning/deliberations/2026-04-28-framing-widening.md — operating-frame
     ground (R1-R5 design space; six-context plurality; four-act plurality;
     project-anchoring framework). Load-bearing for synthesis interpretation.
  8. .planning/gsd-2-uplift/INITIATIVE.md — initiative-staging artifact; goal
     as articulated; open framing questions.
  9. .planning/gsd-2-uplift/DECISION-SPACE.md — load-bearing decision reference;
     B1-B6 in §1.11-§1.16; §2.3 incubation-checkpoint.
  10. .planning/gsd-2-uplift/orchestration/OVERVIEW.md — wave structure + §11
     dispositions log (especially §11.4 W2 audit dispositions just batch-updated).
  11. .planning/gsd-2-uplift/orchestration/synthesis-spec.md — W3 synthesis spec;
     §"Paired-synthesis escalation criterion" at :172-189 (escalation triggered);
     §"Synthesis output" structure for SYNTHESIS-COMPARISON.md guidance.
  12. .planning/gsd-2-uplift/exploration/0[2,4,5]-*-audit.md — three audits
     (referenced by both syntheses).
  13. .planning/gsd-2-uplift/exploration/0[1-5]-*-output.md — five slice outputs
     (slice 4 has (vi) addendum; slice 5 has (vi) corrigenda + 6 strikethrough
     corrections).

  Optional (selectively when relevant):
  - .planning/STATE.md — project state (updated this session).
  - .planning/deliberations/2026-04-28-tier-comparison-preliminary.md — tier
    comparison + B.6 sub-pattern naming.
  - .planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md —
    predecessor; W1-and-framing-widening-arc context.
  - .planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md
    + .planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md —
    side-investigation evidence at GPT-5.5 medium.
agents_running: |
  No agents running when this handoff was written. The cross-vendor codex
  paired-synthesis (background ID `b8ikf3e4m`) completed successfully and
  produced SYNTHESIS-CROSS.md before handoff drafting.
---

# Handoff — Post-W2 audits + paired-synthesis landed

This document is the durable record of the 2026-04-28 session arc that began post-W1-parallel-dispatch + framing-widening (per predecessor handoff) and extended through W2 audit dispatch + disposition + recording, W3 same-vendor synthesis, and paired-synthesis escalation + dispatch + landing. It captures: (a) what landed; (b) what's pending; (c) the trajectory ahead; (d) lessons learned worth carrying forward; (e) what NOT to do; (f) cross-references.

If reading cold, follow the onboarding read-order in the frontmatter. Sections build on each other.

## §1. Where we are right now

**Date:** 2026-04-28 (session began with handoff onboarding; ended at SYNTHESIS-COMPARISON.md drafting threshold; handoff written before context-clear).

**Branch:** `spike/001-volume-filtering` (substantial commits ahead of origin; not pushed).

**Active work:** gsd-2 uplift initiative — first-wave synthesis stage. **Both W3 syntheses landed; SYNTHESIS-COMPARISON.md is the pending in-session-collaborative artifact** before incubation-checkpoint.

**Recent commits this session:** none yet — this session's work has not been committed. The session arc produced substantial new artifacts and edits; commit-readiness is a fresh-session decision.

**Pending:**
- **SYNTHESIS-COMPARISON.md.** Per `synthesis-spec.md:188`. In-session-collaborative draft (Logan + fresh-session-Claude at xhigh) per D5a recommendation that comparison stage benefits from Logan adjudication. Proposed structure in §6 below.
- **Commit the session's work.** Five new/modified files at minimum: SYNTHESIS.md (new); SYNTHESIS-CROSS.md (new); deliberation log (new); slice 4 + slice 5 outputs (in-place addenda); OVERVIEW.md §11.4 (batch update); INDEX.md + STATE.md (updated). Logan disposes commit timing.
- **Incubation-checkpoint per `DECISION-SPACE §2.3`.** Logan-led; out of orchestration scope. Inputs include both syntheses + comparison artifact + framing-widening + DECISION-SPACE.md + INITIATIVE.md.

## §2. The session's work (chronological)

### §2.1 Onboarding (predecessor handoff read)

Session began by reading `.planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md` per `/clear` invocation. Onboarding read-order followed: CLAUDE.md, AGENTS.md, predecessor handoff, framing-widening, INITIATIVE.md, DECISION-SPACE.md, OVERVIEW.md, audit-spec.md, tier-comparison-preliminary.md, synthesis-spec.md, predecessor §B methodological observations, cross-vendor (re)audit history, slice outputs.

### §2.2 W2 audit dispatch (D1-D5 prep)

Logan asked "do you have specs written for them?" — caught a posture-level B.6 surface where Claude was about to default-follow audit-spec.md template substitution. Logan then asked "do you think the template is sufficient yourself?" — explicit invitation to substantive evaluation.

Three small clarifications were inlined at substitution time:
1. Forbidden reading scope extended to all of `.planning/deliberations/` (covers framing-widening which is typed differently from "deliberation log").
2. Side-investigation outputs (`capabilities-production-fit-findings.md`, `w2-markdown-phase-engine-findings.md`, `2026-04-28-tier-comparison-preliminary.md`) explicitly forbidden — they're dispatching-project evidence; reading them risks pattern-matching to findings auditor "should" find.
3. Parallel-dispatch caveat on cross-audit pattern recognition (parallel audits may not see each other's outputs).

Three audits dispatched in parallel via `adversarial-auditor-xhigh`: slices 2, 4, 5.

### §2.3 W2 audit landings

All three audits landed within ~5-6 min wall-clock:

- **Slice 2 audit** (`02-architecture-audit.md`) — verdict **clean → proceed**. 5/5 source spot-checks verified. ADR-010 `Status: Proposed` verified verbatim at `gsd-2 docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`. RTK gating divergence verified verbatim. No critical or material findings; no framing-leakage.
- **Slice 4 audit** (`04-artifact-lifecycle-audit.md`) — verdict **minor → addendum** with one severity-tagged "material" CG-1 disposed via substantive-trigger reading. CG-1: Q2 missed enumeration of three additional extension subsystems (ecosystem at `ecosystem/loader.ts:1-110`; workflow plugins at `workflow-plugins.ts:1-60`; skills at `skill-manifest.ts:1-60`). Auditor disposed material→addendum because findings *add* to slice's central claim rather than reverse it. No framing-leakage.
- **Slice 5 audit** (`05-release-cadence-audit.md`) — verdict **minor → addendum**. Math reproduces exactly across 8 spot-checks. Three citation line-number errors (file lengths overshot; content verified correct). Cross-finding integration flag at audit §5: machinery-vs-practice on breaking-change communication (auditor flagged as synthesis-stage; D3 directed to synthesis). No framing-leakage.

### §2.4 Recommendation map exchange + D1-D5 disposition

Logan asked for "recommended response to each [open question / decision point]... why or why not... make explicit any assumptions or salient factors... possible pushback points... what would change your recommendation" — explicit B.4 conditional-structure invitation.

Recommendation map produced for D1-D5 with conditional flips. Logan affirmed all five recommendations.

D1-D5 with their dispositions:
- **D1 — Slice 4 CG-1.** In-place addendum at end of slice 4 file using auditor's suggested paragraph from audit `:144-146`.
- **D2 — Slice 5 citation errors.** In-place strikethrough-and-correct at six citation occurrences + corrigenda section (vi) at end. Auditor's corrected line numbers used.
- **D3 — Slice 5 cross-finding integration flag.** Left for synthesis (auditor's call); flag captured in audit §5 → synthesis-input chain per `synthesis-spec.md:35`.
- **D4 — OVERVIEW.md §11.4 update timing.** Batch-update post-disposition (one inflection point with all three slice dispositions).
- **D5 — W3 synthesis dispatch shape.** Single same-vendor synthesizer (Claude Opus xhigh dispatched-subagent; effort inherited from parent xhigh session); spec-following on escalation eval with pre-flagged expectation that Trigger 4 likely fires.

Full reasoning + conditional structure recorded in `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` (D1-D5 sections; ~470 lines).

### §2.5 Recording stage

Per Logan's "record these decisions and these qualified justifications somewhere appropriate for auditing reasons":

- **Deliberation log:** `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` written. ~470 lines; D1-D5 with substantive justification + assumptions + conditional flips; §4 records B.6 surface caught and addressed across the session arc.
- **OVERVIEW.md §11.4:** batch-updated with all five slice dispositions (slice 1 not triggered; slice 2 clean; slice 3 skipped; slice 4 minor → addendum; slice 5 minor → addendum). References deliberation log for full reasoning.
- **Slice 4 (vi) addendum:** auditor's suggested paragraph applied in-place (extension-mechanism enumeration completion). Original (v) section preserved verbatim.
- **Slice 5 (vi) corrigenda + 6 inline strikethrough corrections:** trace-preserving citation fixes at lines 244, 245, 304 (×2), 318, 332 (×2), 378 (×2). Corrected line numbers per auditor's spot-check 5.
- **INDEX.md + STATE.md:** updated with deliberation log entry; STATE.md `stopped_at` + `last_activity` + Status + Active work updated.

### §2.6 W3 same-vendor synthesis dispatch + landing

Substrate gap surfaced at dispatch time: no purpose-built synthesis-xhigh subagent type exists. Three options weighed (general-purpose at opus; in-session at xhigh; adversarial-auditor-xhigh repurposed). Logan corrected the substrate-gap analysis: dispatched subagents inherit parent reasoning level. With effort inherited, general-purpose at opus model meets both opus + xhigh requirements with cleaner attribution.

Dispatched: general-purpose subagent at opus model with rich synthesis-spec-derived prompt. Inputs: 5 slice outputs (with addenda) + 3 audit outputs + framing-widening + DECISION-SPACE.md + INITIATIVE.md + side-investigation evidence + tier-comparison + W2 disposition log. Forbidden: SYNTHESIS-CROSS.md (which doesn't yet exist; still listed for completeness).

**Landed:** `SYNTHESIS.md` at 609 lines. Frontmatter sets `escalation_to_paired_synthesis: yes` (Trigger 4 fires; Trigger 2 plausibly fires; Trigger 3 plausibly fires). Eight sections (§0-§7) all populated. Substantive findings F1-F8 in §0 stratification.

### §2.7 Citation verification (Logan's "are we certain... grounded in citations" pass)

Logan asked "Are we certain about these findings? are they grounded in citations to the workspace?" — explicit verification request rather than spec-trust.

Five spot-checks executed directly against gsd-2 source:
- **F1 ADR-010 status:** ✓ Verified verbatim at `docs/dev/ADR-010-pi-clean-seam-architecture.md:3` (`Status: Proposed`). Pi packages tree confirms no `gsd-agent-core` / `gsd-agent-modes` (only `daemon, mcp-server, native, pi-agent-core, pi-ai, pi-coding-agent, pi-tui, rpc-client`).
- **F2 four extension subsystems:** ✓ All four exist as named (`ecosystem/loader.ts` 201 lines; `workflow-plugins.ts` 403 lines; `skill-manifest.ts` 175 lines; pi-coding-agent extensions via `extension-validator.ts` + `extension-discovery.ts` + `extension-registry.ts`). Bonus: `ecosystem/gsd-extension-api.ts` exists (10KB) corroborating ecosystem-has-separate-API claim.
- **F3 zero BREAKING-marked commits:** ✓ Independently re-verified — 2217 visible 6-month commits; grep returns 0 matches.
- **F4 two-engine architecture:** ✓ All named files exist (`engine-resolver.ts`, `workflow-engine.ts`, `custom-workflow-engine.ts`, `dev-workflow-engine.ts`, `engine-types.ts`, `workflow-plugins.ts`).
- **F5 RTK gating divergence:** ✓ Verified verbatim. README.md:22 says "GSD now provisions a managed RTK binary..."; src/cli.ts:170-172 says "RTK is opt-in via experimental.rtk preference. Default: disabled."
- **F8 SCHEMA_VERSION = 22:** ✓ Verified at `gsd-db.ts:183`.

Result: F1-F5 factual content is source-grounded; the *interpretive layering* (e.g., "shifts what extension surface means", "machinery-vs-practice as cross-finding pattern", "plural significations of uplift") is synthesis-stage and is exactly what paired-synthesis escalation tests.

### §2.8 Paired-synthesis dispatch + landing

Per `synthesis-spec.md:185-188` escalation directive (any one of four triggers fires escalation).

Dispatched: codex GPT-5.5 high cross-vendor synthesizer via background `codex exec` (bg ID `b8ikf3e4m`). Prompt at `/tmp/codex-synthesis-cross-prompt.md`; 268,544 tokens used; ~10 min wall-clock.

**Forbidden reading enforced:** Claude's SYNTHESIS.md, Gemini deep-research doc, predecessor handoff. Codex confirmed independence in §0 frontmatter note.

**Landed:** `SYNTHESIS-CROSS.md` at 207 lines. Eight sections (§0-§7). Independent integration of audited W1 evidence + framing-widening operating frame.

**Trailing codex log error** ("thread 019dd313-6fff-7303-9a16-7fda2a2e5cc0 not found") is benign post-completion noise; apply_patch succeeded (file is on disk).

## §3. Both syntheses — substantive comparison preview

A draft comparison preview was produced in-session before context-clear. Captured here so fresh-session can use it as scaffolding (or revise if comparison work surfaces different patterns).

### §3.1 Convergent findings (high robustness for incubation)

Both vendors reach these independently from the audited evidence base:

- **Pi vendoring + clean-seam tension; ADR-010 proposed-not-implemented.** Claude F1 + §1.1; codex §0 OFS-2 + §1.x patterns + §2.1 R1 caveat.
- **Extension-surface plurality (4 parallel subsystems).** Claude F2 + §1.3; codex §1.3 + §3.3.
- **Two-engine architecture (markdown-phase prompt-dispatch vs yaml-step deterministic).** Claude F4 + §1.2; codex §1.2 with independent source spot-checks at `commands-workflow-templates.ts:424-508` and `custom-workflow-engine.ts:90-226`.
- **Release/breaking-change machinery-vs-practice gap.** Claude F3 + §1.7; codex §3.4.
- **Docs-vs-source drift as recurring class.** Claude F5 + §1.5; codex §1.5.
- **RTK gating divergence.** Claude F5 instance; codex §3.2.
- **R2 viable but with substantial caveats.** Both at medium-high confidence.
- **Telemetry/observability/security central.** Claude F8/F9 + §1.4; codex §1.4.
- **B4 split held; abstract long-horizon-relevance interpretation belongs at synthesis.** Both §2.6.

### §3.2 Divergent findings (different reads — incubation deliberation)

- **R4 weighting in operating-frame-update.** Codex §0 explicitly elevates R4 to operating-frame-shift status ("R2+R4 mix unless ... core/Pi entanglement"); explicit recommendation §5: "Treat R4 as first-class in the checkpoint." Claude treats R4 as warranted naming addition in §2.1 R4 sub-section (medium-high) but doesn't elevate it as decisively in §0 stratification. **Codex more directive; Claude more deliberative.** Real interpretive divergence on synthesis-level emphasis.
- **Synthesis register/length.** Claude: 609 lines, F1-F8 numbered findings, dense interpretive structure with framing-widening vocabulary applied throughout. Codex: 207 lines, more compact, more directive in §5 recommendations ("Pick a first second-wave target that tests the frame cheaply"; "Avoid starting with Pi seam refactoring or deterministic release engines"). Compression difference is substantive — codex makes operationally crisper recommendations; Claude makes more comprehensive pattern integrations.
- **R5 framing.** Codex §0 OS-2: "R5 is not demanded by first-wave evidence, but it is no longer merely a cancellation bucket." Claude §2.1 R5: "not first-wave-decidable; requires comparison frame." Codex more open to R5-as-real-option; Claude more "pending-evidence-suspended."

### §3.3 Unique findings (one surfaces; other missed — completeness signal)

- **Codex unique:** Specific source spot-checks codex independently verified beyond the audit's spot-checks (`commands-workflow-templates.ts:424-508`; `custom-workflow-engine.ts:90-226`; `workflow-plugins.ts:120-221`). M1-cross-vendor strength.
- **Codex unique:** §4 enumerates 7 specific "what resolves" probe questions with operational specificity (e.g., "temporal-stability probe over Pi extension API, ecosystem extension API, workflow plugins, and skills"; "live GitHub PR/issue analysis when network/auth allows"). More concrete than Claude's parallel §4.
- **Claude unique:** F1-F8 numbered-findings stratification (codex covers similar ground via §0 + §1 patterns but no parallel labeled-findings structure for downstream citation).
- **Claude unique:** §1.8 "Substrate richness vs depth-of-attention as the limiting factor" — methodological observation about how-to-characterize-gsd-2 (wave-structure discipline), not just what-gsd-2-is. Codex has no parallel section.
- **Claude unique:** §2.5 design-shape candidates table (8 candidates × four-act mapping × R-strategy mapping × W2-dive verification status). Codex §2.5 covers similar ground via prose but doesn't tabulate.

## §4. Direction-shifting evidence accumulated through W2 + W3

Synthesis output naturally integrates this; flagging here for fresh-session orientation:

- **Pi vendoring entanglement is more substantial than operating-frame-`§1.8` likely assumed.** ADR-010 proposed-not-implemented; ~79 GSD-authored files inside vendored Pi packages. Bears on R1 vs R2 viability: extension-against-vendored-Pi is fragile.
- **Extension surface is at least four parallel subsystems** (pi-coding-agent extensions; GSD ecosystem; workflow plugins; skills) — not one. Strengthens R2 surface but also fragments it; R2 should be decomposed by target subsystem.
- **markdown-phase workflow plugins are prompt-dispatch, not deterministic.** Limits the kind of R2 work that can land via this mechanism. Either reroute to yaml-step (which has determinism but fewer exemplars) or accept agent-prompted indirection or build wrapper code around markdown-phase or use R4 (orchestrate-from-outside).
- **Breaking-change machinery vs practice gap.** Elaborate machinery (PR template; `api-breaking-change` workflow; `BREAKING CHANGE:` detection in changelog generator); zero observed BREAKING-marked commits in 6mo visible window. Stability claims based on machinery alone are weaker than they appear.
- **Release/workflow tightly interleaved.** Release templates live in same workflow-plugins subsystem as project-internal templates; release artifacts under `.gsd/workflows/`; gsd-2's *own* release uses CI scripts running outside the workflow plugin system. Any uplift work treating release cadence as separate from artifact/workflow mechanics misses that they share infrastructure.
- **R4 (orchestrate-without-modifying) deserves explicit operating-frame status.** Codex synthesis explicitly elevates R4; Claude synthesis names it as warranted addition. Headless mode + JSON output + RPC + MCP make R4 substantively viable.
- **R5 is not first-wave-decidable** — requires deferred competitor-landscape probe (framing-widening §9 item 3). Both syntheses agree.

## §5. Lessons learned worth carrying forward

### §5.1 B.6 surface caught and addressed across the session arc

Three Logan-adjudication catches forced substantive re-evaluation rather than spec-deference:

1. **"Do you have specs written for them?"** caught Claude about to default-follow audit-spec.md template substitution. Resolution: three small clarifications inlined at substitution time.
2. **"Do you think the template is sufficient yourself?"** explicit invitation to substantive evaluation rather than spec-deference. Resolution: substantive re-evaluation produced the three additions; Logan affirmed.
3. **"What might be your recommended response to each... why or why not... make explicit any assumptions or salient factors"** forced full conditional structure on the recommendation map. Resolution: D1-D5 with conditional flips; Logan affirmed all five.

The pattern matters for the broader B.6 codification deferred per `framing-widening §9` items 7-8. This session is one sample (third-sample threshold reached for the defaulted-spec-following sub-pattern after this session + tier-comparison §7 + 2026-04-27 §B.5).

**Mitigation observable in this session:** each spec-aligned recommendation carried explicit "why this is right" justification anchored to *current evidence* (audit findings; framing-widening; tier-comparison) rather than spec-text quotation. The fingerprint of substantive re-evaluation is *current-evidence anchoring*, not spec-rephrasing.

The discipline this codifies: when following any prior spec, briefly note "spec says X; evidence since spec was written includes Y; I'm proceeding with X because [reason] / proposing departure to Z because [reason]." Verbal-discipline-at-recommendation-stage, not artifact-level.

### §5.2 Substrate-gap discovery: dispatched subagents inherit reasoning level

Initial assumption: synthesis-spec.md specifies xhigh; available subagent types don't include synthesis-shaped-xhigh; substrate gap. Surfaced to Logan as three options (A general-purpose at opus default-effort; B in-session at xhigh; C adversarial-auditor-xhigh repurposed).

Logan corrected: dispatched subagents inherit parent reasoning level. With effort inherited from parent xhigh session, general-purpose at opus model meets both opus + xhigh requirements with cleaner attribution.

**Codified for future:** when dispatching a subagent and effort matters, parent's effort is inherited unless overridden. The Agent tool's `model` parameter only controls model; effort inherits. Verifiable: this session's audits (adversarial-auditor-xhigh) and synthesis (general-purpose at opus, parent xhigh) both produced xhigh-quality outputs.

### §5.3 Citation-verification chain: synthesis → audit → workspace held end-to-end

Logan's "are we certain... grounded in citations to the workspace?" verification pass spot-checked F1-F5 directly against gsd-2 source. All five spot-checks verified.

**Pattern:** the audit-stage source verification (synthesis-spec inputs include audited slices) means the synthesis can confidently cite slice/audit; spot-verifying synthesis citations against workspace re-confirms the chain holds. The chain has now been verified at three levels: cross-vendor reads cite source; same-vendor audit verifies source; synthesis cites audit; this session's spot-checks verify synthesis. All four levels converge.

**Implication:** synthesis confidence labels on factual content are well-grounded. Synthesis confidence labels on interpretive content (operating-frame implications; six-context anchoring; R-strategy weighting) are appropriately calibrated — interpretive layering is what paired-synthesis catches.

### §5.4 Trace-preserving in-place edits work

D2's strikethrough-and-correct approach preserved auditing while making citations work. Future readers chasing slice 5 citations get corrected line numbers; the original error is visible via strikethrough; the corrigenda section explains the convention. This is the right shape for content-correct-but-citation-wrong findings.

For future similar work: trace-preserving in-place edits are project-aligned (per `feedback_methodology_and_philosophy.md` traces-over-erasure discipline); attribution annotation at section-start (e.g., "Added by Claude (Opus 4.7) post-W2-audit per disposition recorded in...") preserves the agent-vs-Claude distinction.

### §5.5 In-session-collaboration shape for comparison-stage work

Per D5a recommendation, synthesizer dispatch is appropriate for first-synthesis-stage (cleaner attribution; fresh context; M1 paired-review). Comparison-stage is the right inflection point for in-session work because:
- Logan adjudication on divergent findings is load-bearing (synthesis interpretive divergences are exactly the question for incubation).
- Both syntheses already exist; comparison is *integration of existing artifacts*, not new synthesis.
- Comparison artifact is the bridge between synthesis-stage and incubation-stage; in-session lets Logan + Claude jointly draft the bridge.

This generalizes: synthesis-and-paired-synthesis stages benefit from dispatched subagents (independence); comparison/integration/disposition stages benefit from in-session collaboration (Logan adjudication mid-flight).

## §6. Next-stage execution sequence — SYNTHESIS-COMPARISON.md

Fresh session should:

### §6.1 Read both syntheses thoroughly

Don't read on first onboard pass; come back to them after primary onboarding. Read SYNTHESIS.md (609 lines) and SYNTHESIS-CROSS.md (207 lines) in full. Both are dense; budget 30-60 min.

### §6.2 Validate the §3 comparison preview

Section §3 above is a draft preview produced in-session before context-clear. Fresh session should either:
- Affirm the convergent / divergent / unique categorization (treat as scaffolding for SYNTHESIS-COMPARISON.md).
- Revise where the categorization missed nuances or mis-classified findings.

### §6.3 Propose comparison artifact structure to Logan

Proposed structure (drafted in-session pre-handoff; subject to Logan disposition):

```markdown
---
type: paired-synthesis-comparison
date: <date>
synthesizers: [Claude Opus xhigh (SYNTHESIS.md); codex GPT-5.5 high (SYNTHESIS-CROSS.md)]
status: complete
---

# Paired-synthesis comparison — gsd-2 first-wave

## §0. Comparison summary
What this comparison does for incubation; M1 paired-review framing; scope.

## §1. Convergent findings (both vendors reach independently — robustness signal)
For incubation: highest-confidence inputs. List + per-finding citation chain (which sections of each synthesis converge).

## §2. Divergent findings (different reads on same evidence — incubation deliberation)
Per divergence: where each synthesis lands; what evidence supports each read; what the divergence implies for incubation. Logan disposes the divergent reads.

## §3. Unique findings (one synthesizer surfaced; other missed — completeness signal)
Per unique finding: which synthesis carries it; whether the other would likely converge on a fresh read or genuinely missed it. Useful for incubation as completeness-of-coverage check.

## §4. Methodological observations (M1 in action)
What same-vendor caught vs cross-vendor caught; whether tier-comparison preliminary's expectations held; framing-leak observations.

## §5. Integrated read for incubation-checkpoint
NOT a third synthesis — a convergence-aware integration that makes both syntheses navigable for Logan + Claude reading at incubation. Operating-frame implications across R1-R5; six-context plurality concretization; metaquestion read.

## §6. Confidence and limits
What the comparison can and can't establish; in-session-collaboration caveat (this comparison is Claude-in-session-with-Logan, not a third independent synthesizer).
```

### §6.4 Draft SYNTHESIS-COMPARISON.md in-session at xhigh

Per D5a recommendation, comparison stage is in-session. Fresh-session-Claude drafts; Logan adjudicates §2 divergent findings + §5 integrated read. Estimated draft time: 45-90 min depending on Logan adjudication frequency.

### §6.5 After comparison lands

Both syntheses + comparison feed incubation-checkpoint per `DECISION-SPACE §2.3`. Incubation is **Logan-led + out of orchestration scope.** Fresh-session-Claude does NOT auto-execute incubation-checkpoint; Logan disposes the operating-frame-update questions.

If incubation re-disposes the operating frame (e.g., R-strategy mix shifts; context-anchoring narrows; metaquestion answer changes), update DECISION-SPACE.md + INITIATIVE.md per the re-disposition outcome.

### §6.6 Commit cadence

This session's work has not been committed. Logan disposes commit timing. Files needing commit (at minimum):
- `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` (new)
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` (new)
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` (new)
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md` (new)
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md` (new)
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md` (new)
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md` (modified — (vi) addendum)
- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md` (modified — (vi) corrigenda + 6 strikethroughs)
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` (modified — §11.4 batch update)
- `.planning/deliberations/INDEX.md` (modified — new entry)
- `.planning/STATE.md` (modified — last_activity + stopped_at)

After SYNTHESIS-COMPARISON.md lands:
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` (new)
- Possibly STATE.md update.

## §7. Medium and long horizons (perspective for orientation)

§6 frames the near-horizon work (SYNTHESIS-COMPARISON.md → incubation-checkpoint). This section keeps the medium and long horizons in view so fresh-session reasoning stays anchored to the broader trajectory, not just the immediate-next-step.

Per `.planning/deliberations/2026-04-28-framing-widening.md` Part II §7 (medium) + §8 (long); read those sections directly if depth is needed.

### §7.1 Medium horizon (next 1-3 months)

The path after SYNTHESIS-COMPARISON.md lands:

- **Incubation-checkpoint per `DECISION-SPACE §2.3`.** Logan-led; out of orchestration scope. Re-reads goal articulation; checks direction-shifting evidence per `INITIATIVE.md §3.1`; checks whether R-strategy hybrid (now R1-R5) has narrowed; decides whether second-wave-scoping proceeds, re-disposes, or cancels.
- **Conditional second-wave-scoping per `DECISION-SPACE §1.6`.** If incubation says proceed: second-wave scopes the design phase. The framing-widening's four-act plurality + R1-R5 + six-context plurality give second-wave a structured space to reason within. Per both syntheses' §5 recommendations, second-wave should pick a first concrete target that tests the frame cheaply (good candidates: effective-state visibility; release-metadata artifact linked to milestones; long-arc decision-trace skill/workflow; headless orchestration recipe).
- **Conditional cancellation per `DECISION-SPACE §1.11` (B1).** If first-wave evidence + incubation surface that the operating frame is wrong-shaped, cancellation is a substantive output. Both syntheses agree direction-holds at this stage but qualify the operating-frame shape; cancellation is not currently licensed by evidence but remains a substantive option per B1.
- **R5 disposition.** If first-wave evidence + incubation lean toward R5 (replacement-informed-by) being the right composition, second-wave-scoping has a different shape: design a sibling harness rather than design uplift extensions. Both syntheses agree R5 is not first-wave-decidable; requires the deferred competitor-landscape probe (per framing-widening §9 item 3). Whether this probe runs *before* incubation (if R5 looks live to Logan) or *after* (if R5 stays parked) is a Logan-disposed pre-incubation decision.
- **Context-plurality disposition.** Logan's read on arxiv-sanity-mcp's anchoring (per framing-widening §3.3) shapes which contexts second-wave-scoping prioritizes. Primarily-A-with-strong-F: emphasize comprehension-across-time + progressive-activation work; Context-F-primary-with-explicit-B-aspiration: re-elevate release-coordination work; multi-context-pluralized: design uplift to span multiple representative onboarding situations per `INITIATIVE.md §3.3`. **This is a load-bearing Logan disposition** for second-wave shape.
- **Side-probe trigger evaluation.** Per framing-widening §9 deferred items log: 17 items across probes / methodology / audits / synthesis-stage / roadmap. Incubation evaluates whether any side-probe is on the critical path for second-wave-scoping; if yes, dispatch before second-wave; if no, defer further or drop.
- **arxiv-sanity-mcp v0.2 implementation status.** Per `STATE.md` and `CLAUDE.md`: phases 12-17 are authored but on hold pending gsd-2 uplift evaluation. If incubation greenlight uplift work, v0.2 implementation may resume in parallel (depending on Logan's resource allocation between uplift and v0.2). If incubation re-disposes (e.g., narrows uplift scope or cancels), v0.2 implementation is unblocked.

### §7.2 Long horizon (1+ year considerations)

These are mostly tracked elsewhere; named here for completeness.

- **Migration of `.planning/gsd-2-uplift/` to dedicated repo.** Per `INITIATIVE.md` frontmatter `migration_trigger`. Conditional on (a) initiative graduating from staging via incubation greenlight, and (b) dedicated repo being created. Not yet active; should not block any near-horizon work.
- **Stage 1 audit deferred quality findings.** Per `framing-widening §9` item 10 + `STATE.md` pending-todos. Quality work that doesn't block first-wave dispatch or comparison artifact. Address opportunistically; non-blocking. Items: §A decision-table compression of §1.2 bifurcation; "Logan's framing" parenthetical in §4.5; §3 prefix vs §5.1 deliverables-vs-informing tension; R2-base contingency phrasing; "load-bearing" overuse.
- **Methodology codification of session-disciplines.** Per `framing-widening §9` items 7-9. Threshold-based codification (~3 samples). **Threshold reached** for the defaulted-spec-following sub-pattern (B.6) after this session: tier-comparison §7 + 2026-04-27 §B.5 + this session's three Logan-adjudication catches = 3 samples. Codification venue: `METHODOLOGY.md` or `AGENTS.md`; Logan-disposed methodology decision; not blocking near-horizon work but worth scheduling for post-incubation.
- **Production-fitness synthesis as durable artifact.** Per `framing-widening §8`. The capabilities probe + W2 dive + slice-output material answers Logan's substantive production-fitness questions but isn't yet in a citable synthesis form. SYNTHESIS.md and SYNTHESIS-CROSS.md partially serve this role now; whether to consolidate into a separate production-fitness artifact is post-incubation work.
- **arxiv-sanity-mcp's own v0.2+ implementation roadmap.** Phases 12-17 (multi-lens substrate work) per the project's roadmap. Whether to resume in parallel with uplift or wait until uplift produces a stable harness target is post-incubation Logan disposition. If uplift produces a primarily-R4-shape (orchestrate-from-outside) outcome, v0.2 implementation can proceed independently with later integration; if uplift produces a primarily-R2-shape (extension) outcome, v0.2 implementation may benefit from waiting for the extension to stabilize.
- **gsd-2 uplift R-strategy mix actual implementation.** If second-wave proceeds, the second-wave-scoping → design → build → test → adopt cycle. Likely 6-18 months depending on R-strategy mix complexity.
- **LONG-ARC.md anti-patterns + multi-lens substrate work.** The arxiv-sanity-mcp project's long-arc commitments per `LONG-ARC.md` and ADR-0005. Multi-lens substrate is a long-arc commitment that survives any uplift outcome; uplift work should be evaluated for compatibility with multi-lens substrate (e.g., does uplift's plural extension surfaces compose with multi-lens lens type plurality? Per AGENTS.md "validate abstractions by shipping a second implementation" discipline.)

### §7.3 What this perspective does for current work

Three orientations the medium + long horizon awareness provides:

1. **Comparison artifact shape.** SYNTHESIS-COMPARISON.md is *for* incubation-checkpoint — its purpose is to make both syntheses navigable for incubation deliberation. Not for future-readers-in-general. Optimize for incubation-stage utility; surface convergent findings as robustness, divergent findings as deliberation-input, unique findings as completeness-signal. Don't pad with synthesis content the syntheses already carry.
2. **Incubation-checkpoint proximity.** Comparison work is near-horizon (~hours); incubation is medium-horizon (~days-to-weeks); second-wave is medium-to-long-horizon (~months). Don't conflate these. Comparison should not pre-decide incubation's questions; incubation should not pre-decide second-wave-scoping's design choices.
3. **Long-arc anti-pattern resistance.** Per LONG-ARC.md + AGENTS.md, the project has drifted toward tournament-narrowing under "disciplined" framing before. Both syntheses + comparison should preserve R1-R5 plurality + six-context plurality + four-act plurality across reasoning stages. The framing-widening's argument that "decision spaces should not narrow without evidence" applies through incubation. Closure-pressure at every layer is the named anti-pattern; resist it.

## §8. What NOT to do

### §8.1 Do NOT auto-execute incubation-checkpoint

Per `DECISION-SPACE §2.3` + harvest §10.1 assumption #1 + this handoff's §6.5: incubation is Logan-led. Fresh-session-Claude does NOT dispose the operating-frame-update questions; Claude proposes options + recommendations; Logan picks.

### §8.2 Do NOT skip comparison artifact and jump directly to incubation

The comparison artifact is the bridge. Without it, incubation operates on two parallel syntheses without integration; convergence/divergence/unique-findings are not surfaced; M1 paired-review's downstream-utility collapses to "Logan reads both 800 lines and integrates mentally."

Per `synthesis-spec.md:188`: "Both syntheses + comparison feed incubation-checkpoint." The "+ comparison" is load-bearing; don't skip it.

### §8.3 Do NOT modify SYNTHESIS.md or SYNTHESIS-CROSS.md

Both are landed artifacts. If errors are noticed during comparison drafting, surface as comparison-§6 finding (not as synthesis edit). Synthesis artifacts are immutable post-landing per audit-spec.md/synthesis-spec.md disposition discipline.

### §8.4 Do NOT collapse R1-R5 back to R1/R2/R3 in the comparison or downstream

The framing-widening explicitly preserves R4/R5 as named options. Both syntheses worked within R1-R5. Comparison should evaluate convergence/divergence within R1-R5 vocabulary, not collapse back to R1/R2/R3. (This was a flagged risk in the predecessor handoff §7.3; still applies.)

### §8.5 Do NOT pre-decide design shape in the comparison

Comparison is *integration of synthesis findings for incubation*, not design proposal. Second-wave-scoping and design happen post-incubation if incubation disposes proceed-to-design. The four-act plurality + R1-R5 framework give a structured space within which incubation reasons; the comparison surfaces the reasoning inputs, not the design conclusion.

### §8.6 Do NOT modify gsd-2 source

`~/workspace/projects/gsd-2-explore/` is read-only target throughout this initiative. Per predecessor handoff §7.6 + B.5 procedural discipline.

### §8.7 Do NOT bypass disposition-discipline

Logan disposes substantive choices. Closure-pressure (rushing) and opening-pressure (always finding more to deliberate) are both Logan-disposed. When in doubt, surface as recommendation with conditional structure; Logan picks.

### §8.8 Do NOT default-follow synthesis-spec without re-evaluation

B.6 discipline: synthesis-spec was authored 2026-04-27; framing-widening landed 2026-04-28; both syntheses now landed. The escalation triggers fired; the spec's "compare and integrate" directive holds. But if comparison-stage work surfaces substrate gaps or methodology questions, re-evaluate explicitly rather than defaulting.

## §9. Open questions / pending dispositions

### §9.1 Comparison-shape disposition (whose call when comparison drafts)

Logan-led. Proposed structure in §6.3 above. Alternative shapes Logan may prefer:
- More compact comparison (skip §3 unique findings if completeness-signal is low-value for incubation).
- Different §5 integrated-read framing (e.g., per-R-strategy comparison instead of per-finding).
- Synthesizer-attribution per finding (each convergent finding cites both synthesis section refs; each divergent finding cites both reads side-by-side).

### §9.2 Whether incubation pre-reads SYNTHESIS-COMPARISON.md or both syntheses directly

Logan-led. The comparison is the bridge; incubation can read it as primary input + dive into synthesis sections as needed. Or incubation can read both syntheses fully + use comparison as navigator. Logan disposes.

### §9.3 Whether the deferred competitor-landscape probe should fire before incubation

Per framing-widening §9 item 3 + both syntheses §0/§4. R5 viability cannot be evaluated without it. **What might warrant pre-incubation dispatch:** if Logan's read of arxiv-sanity-mcp's anchoring (per framing-widening §3.3) leans Context-F-primary-with-explicit-B-aspiration, R5 evaluation matters more, and the probe should run before incubation. **What might warrant incubation-then-probe:** if Logan's read leans Context-A-primary-with-aspiration-F, R5 is less load-bearing for first-wave dispositions; defer the probe.

### §9.4 Stage 1 audit deferred quality findings

Still pending per framing-widening §9 item 10 + STATE.md pending-todos. Address opportunistically post-incubation; non-blocking.

### §9.5 B.6 codification trigger

Three samples now (this session + tier-comparison §7 + 2026-04-27 §B.5). Per framing-widening §9 item 7-8 the codification threshold is ~3 samples. Whether to codify now in METHODOLOGY.md or AGENTS.md is a Logan-disposed methodology decision; not blocking.

## §10. Cross-references

**Decision and operating-frame inputs.**
- `.planning/gsd-2-uplift/INITIATIVE.md` — initiative-staging.
- `.planning/gsd-2-uplift/DECISION-SPACE.md` — load-bearing decision reference; B1-B6 in §1.11-§1.16; §2.3 incubation-checkpoint.
- `.planning/deliberations/2026-04-28-framing-widening.md` — operating-frame ground.
- `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` — D1-D5 disposition log with conditional structure.

**Orchestration package.**
- `.planning/gsd-2-uplift/orchestration/OVERVIEW.md` — wave structure + §11 dispositions log (especially §11.4 W2 audit dispositions).
- `.planning/gsd-2-uplift/orchestration/synthesis-spec.md` — W3 synthesis spec; `:172-189` paired-synthesis escalation criterion; `:188` comparison artifact path.
- `.planning/gsd-2-uplift/orchestration/audit-spec.md` — W2 audit template + dispatch criteria.
- `.planning/gsd-2-uplift/orchestration/preamble.md` — common preamble for slice dispatch.
- `.planning/gsd-2-uplift/orchestration/slice-01-mental-model.md` through `slice-05-release-cadence.md`.
- `.planning/gsd-2-uplift/orchestration/cross-vendor-audit.md` + `cross-vendor-reaudit.md` — orchestration audit history.

**W3 synthesis evidence.**
- `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` — Claude Opus xhigh same-vendor synthesis (609 lines).
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` — codex GPT-5.5 high cross-vendor synthesis (207 lines).
- (Pending: `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md`.)

**W2 audit evidence.**
- `.planning/gsd-2-uplift/exploration/02-architecture-audit.md` — clean → proceed.
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md` — minor → addendum.
- `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md` — minor → addendum.

**W1 evidence.**
- `.planning/gsd-2-uplift/exploration/01-mental-model-output.md` (slice 1; high).
- `.planning/gsd-2-uplift/exploration/02-architecture-output.md` (slice 2; high).
- `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md` (slice 3; high).
- `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md` (slice 4; high; with (vi) addendum).
- `.planning/gsd-2-uplift/exploration/05-release-cadence-output.md` (slice 5; high; with (vi) corrigenda + 6 strikethrough corrections).
- `.planning/gsd-2-uplift/exploration/capabilities-production-fit-findings.md` (capabilities probe; medium).
- `.planning/gsd-2-uplift/exploration/w2-markdown-phase-engine-findings.md` (W2 dive; medium).

**Deliberation logs.**
- `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` — genesis-arc.
- `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md` — orchestration package + B1-B6 + §B.1-§B.5 methodological observations.
- `.planning/deliberations/2026-04-28-framing-widening.md` — current operating frame.
- `.planning/deliberations/2026-04-28-tier-comparison-preliminary.md` — tier comparison + §7 B.6 sub-pattern.
- `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` — D1-D5.
- `.planning/deliberations/INDEX.md` — index for all dated deliberations.

**Predecessor handoffs.**
- `.planning/handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md` — predecessor; W1-and-framing-widening-arc.
- `.planning/handoffs/2026-04-27-post-stage-1-uplift-genesis-handoff.md` — Stage 1 → Stage 2 transition.
- `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md` — further-predecessor.
- `.planning/handoffs/2026-04-26-post-wave-4-handoff.md` — codex-CLI pitfall reminders.

**Project doctrine referenced.**
- `CLAUDE.md` — project identity + accepted ADRs + doctrine load-points.
- `AGENTS.md` — project-specific anti-patterns to detect.
- `LONG-ARC.md` — anti-patterns at lines 42-54.
- `.planning/spikes/METHODOLOGY.md` — M1 paired-review at line 112; forbidden-reading extension at line 117.
- `.planning/foundation-audit/METHODOLOGY.md` — epistemic discipline.

**Source citations** (selective; full per-finding citations in each synthesis).
- gsd-2 source at `~/workspace/projects/gsd-2-explore/`.
- Pi-vendored packages at `~/workspace/projects/gsd-2-explore/packages/`.
- Workflow engines at `src/resources/extensions/gsd/{workflow-engine,engine-resolver,dev-workflow-engine,custom-workflow-engine}.ts`.
- Extension subsystems at `src/{extension-registry,extension-discovery,extension-validator}.ts` + `src/resources/extensions/gsd/{ecosystem/loader,workflow-plugins,skill-manifest}.ts` + `packages/pi-coding-agent/src/core/extensions/`.
- ADR-010 at `docs/dev/ADR-010-pi-clean-seam-architecture.md`.
- Release tooling at `scripts/{generate-changelog,bump-version,update-changelog}.mjs` + `.github/workflows/{prod-release,dev-publish,next-publish}.yml`.

---

*Single-author session handoff written 2026-04-28 by Claude (Opus 4.7, xhigh effort) at Logan's direction post-W2-audits-disposed + post-paired-synthesis-landed pre-context-clear. Subject to the same fallibility caveat as DECISION-SPACE.md §0 and predecessor handoffs. Stress-testing happens when fresh session reads + executes; if any direction reads mis-recorded, re-deliberation supersedes. The fresh session's primary work is producing SYNTHESIS-COMPARISON.md per §6 above.*
