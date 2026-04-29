---
type: premise-bleed-audit-findings-step2-independent
date: 2026-04-29
auditor_step2: Claude same-vendor adversarial-auditor-xhigh (independent mode per spec §3.4 manual-escalation)
mode: independent (no Step-1 priors; differential post-hoc in main thread)
spec: ./AUDIT-SPEC.md
status: step2-independent-complete; differential-pending-main-thread
target:
  - .planning/gsd-2-uplift/INITIATIVE.md (full)
  - .planning/gsd-2-uplift/DECISION-SPACE.md (§1.2, §1.7, §1.8, §1.17, §3 targeted)
  - .planning/gsd-2-uplift/exploration/SYNTHESIS.md (§0, §1, §2.1, §2.5, §6.4 targeted)
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md (full)
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md (full)
  - .planning/deliberations/2026-04-28-framing-widening.md (§1, §2, §3, §4 targeted)
  - .planning/gsd-2-uplift/orchestration/preamble.md + slice-01..05 + synthesis-spec + audit-spec (scan)
grounding:
  - .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md (primary)
  - .planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/GATE-2-DISPOSITION.md (primary)
slice_output_sampling_used: 0 of 3-5 cap
source_reading_used: 0 of 5 soft-cap (META-SYNTHESIS coverage was sufficient)
provenance_note: |
  This file was produced by an adversarial-auditor-xhigh subagent dispatched in independent mode
  per AUDIT-SPEC.md §3.4 manual-escalation. The subagent's runtime blocked its direct file write,
  so it returned the findings as text in its final result. The parent (main-thread Claude)
  transcribed the result verbatim into this file. The content (§0-§5 + executive summary) is the
  subagent's independent reading; main-thread Claude did not modify or summarize it.
---

# §0. Step-1 summary (this is a Step-1-shaped independent FINDINGS document per dispatch §"Operating mode")

- Total premise-bleed instances surfaced: **9**
- Classification breakdown: Class A: 4 (F1, F4, F5, F8); Class B: 3 (F2, F3, F7); Class C: 2 (F6, F9) — both narrowly-load-bearing.
- Top-line read: premise-bleed is **localized rather than pervasive**. The most concentrated v1-GSD framing sits in INITIATIVE.md §3.2 (literal "patcher / skills / hybrid" enumeration) and a paired propagation through DECISION-SPACE.md §1.8 + §3.6's "long-horizon framing" verbiage. The downstream SYNTHESIS.md, SYNTHESIS-CROSS.md, and SYNTHESIS-COMPARISON.md substantially correct via the framing-widening's R4 elevation, the four-extension-subsystems vocabulary (META-SYNTHESIS §2 item 3), and the comparison's §2.1 R4-disposition-timing surfacing. The two Class-C findings (F6, F9) are about residual under-weighting *after* that correction-work — not about uncorrected v1-GSD vocabulary.
- Step-2 escalation triggered: yes (Class C ≥ 1) — but I am operating under §3.4 manual-escalation discretion, so this is recorded for the main-thread differential, not as a conditional next step.

The synthesis layer's most striking property is *internal asymmetry*: SYNTHESIS-CROSS.md surfaces the framing-leakage caveat verbatim (`SYNTHESIS-CROSS.md:203`) while SYNTHESIS.md does not foreground it equivalently. SYNTHESIS-COMPARISON.md §3.3 *itself flags this asymmetry* as an asymmetric-coverage finding rather than a premise-bleed finding (`SYNTHESIS-COMPARISON.md:204-209`). The artifact-set already partly self-audits the property this audit is auditing; several findings sit adjacent to that self-audit and are calibrated to not duplicate it.

---

## §1. Per-instance findings

### Finding 1 — INITIATIVE.md §3.2 candidate-design-shapes uses literal v1-GSD vocabulary as the surfaced framing
- **Artifact / Location:** `INITIATIVE.md` §3.2 lines 81-88
- **Quote:** `"### §3.2 What design shape — patcher, skills, hybrid?"` followed by Patcher/Skills/Hybrid bullets (lines 84-86)
- **Lens-relevance:** §2.4 (a) primary; (c) skills as one of three intervention surfaces.
- **Type:** vocabulary-scan
- **Classification:** **Class A**
- **Justification:** This is the spec's own example of Class A. §3.2 explicitly says `Choice depends on what gsd-2 actually exposes (first-wave slice 4)` (`INITIATIVE.md:88`); §3 preamble names list non-exhaustive and informing-context-not-deliverables. Downstream artifacts do *not* inherit "patcher / skills / hybrid" — SYNTHESIS.md §2.5 maps to four-act plurality + R-strategy mix; SYNTHESIS-CROSS.md §2.5 uses "Modify / Configure / Orchestrate / Replace-informed-by"; SYNTHESIS-COMPARISON.md §5.2 does not re-import the original triad. Confidence: **medium-high**.
- **What dissolves:** if downstream syntheses inherited the triad, classification escalates; they don't.

### Finding 2 — INITIATIVE.md §1 "harness" terminology note absorbs gsd-2's standalone-runtime-application status into a thin-layer assembly definition
- **Artifact / Location:** `INITIATIVE.md` §1 line 44
- **Quote:** `"'harness' refers to the agent-development infrastructure assembly broadly: gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions that together support agential development. Not gsd-2 alone."`
- **Lens-relevance:** §2.4 (e) — "harness" framing places gsd-2 inside an assembly without naming gsd-2's own runtime-application surfaces (session control, headless, RPC, MCP, state machinery). Compresses to a register closer to v1-GSD's host-runtime-conventions vocabulary than to META-SYNTHESIS §1's plural-runtime-surface explicit naming (`META-SYNTHESIS.md:27, :37`).
- **Type:** vocabulary-scan + surface-weighting
- **Classification:** **Class B**
- **Justification:** The note explicitly says "Not gsd-2 alone" and primary-focus stays on gsd-2; SYNTHESIS.md F7 (`SYNTHESIS.md:47-48`) does the runtime-application-surface-naming work. Class-B-not-A: the note is in the staging artifact future readers entering cold will read first; framing matters. Class-B-not-C: synthesis-layer correction is sufficient for §2.1 / §5 dispositions.
- **What dissolves:** if a fresh reader enters via INITIATIVE.md only (e.g., dedicated-repo migration) without reading synthesis layer, escalates to C. Confidence: **medium**.

### Finding 3 — DECISION-SPACE.md §1.8 anchors R-mix on R2-base + R2+R3 hybrid without R4 in the original disposition framing
- **Artifact / Location:** `DECISION-SPACE.md` §1.8 lines 232-262 (heading + Operational implications 234-241)
- **Quote:** `"### §1.8 Upstream relationship: R2 base + primary; R2+R3 hybrid where workflow allows; R1 fallback"` ... `"Decision. The uplift project's relationship to gsd-2 upstream is R2 (extension) as base and primary"`
- **Lens-relevance:** §2.4 (b) and (g) — R-strategy disposition omits R4 (orchestrate-without-modifying) entirely. R4 is what targets headless / RPC / MCP / query / hook / workflow-template surfaces.
- **Type:** surface-weighting + negative-space (R4 absent despite headless/RPC/MCP being source-central per `META-SYNTHESIS.md:27, :37, :75`)
- **Classification:** **Class B**
- **Justification:** §1.8 was written 2026-04-26 before framing-widening (2026-04-28). Framing-widening §5 explicitly says: `"DECISION-SPACE.md §1.8 R1/R2/R3 hybrid → R1-R5 design space per §1 above. The R2-base recommendation persists as the working hypothesis within the R1-R5 space"` (`framing-widening.md:251`). §1.8 has been *operationally* widened but the artifact text wasn't revised. Why-Class-B: incubation reads synthesis + comparison primarily, both carry widened R-mix. Why-not-A: §1.8 framing is load-bearing for what evidence first-wave looks for (slice 4 became R2-viability-load-bearing; R4-relevant evidence was caught only via slice 3 + capabilities probe + W2 dive).
- **What dissolves:** if Logan disposes the §2.1 R4-disposition-timing question toward operate-under-shifted-frame, §1.8 needs explicit revision and finding becomes Class A artifact-side. Confidence: **medium-high**.
- **Grounding:** `META-SYNTHESIS.md:75`: *"R4 should remain explicit; headless/RPC/MCP and external orchestration surfaces are real and should not be forced into R2 vocabulary."*

### Finding 4 — DECISION-SPACE.md §1.4 slice-partition labels under-name runtime-application surfaces
- **Artifact / Location:** `DECISION-SPACE.md` §1.4 lines 113-119
- **Quote:** `"3. Workflow surface + automation + testing — user-invokable commands, automated workflows, hooks, testing primitives. 4. Artifact lifecycle + extension surfaces + migration tooling + distribution/install — .gsd/ artifacts, plugin/extension model..."`
- **Lens-relevance:** §2.4 (b), (d) — labels do not name session control, headless, RPC, MCP, state machinery, or extension *plurality* (the four-subsystem typing per META-SYNTHESIS §2 item 3).
- **Type:** question-shape + negative-space
- **Classification:** **Class A**
- **Justification:** Slice prompts (post-revision) substantially correct: slice 3 Q2 asks `"Specifically: are there multiple workflow engines or dispatch shapes within gsd-2's automation?"` (`slice-03-workflow-surface.md:27`); slice 4 Q2 asks about *multiple extension mechanisms... unified or distinct subsystems* (`slice-04-artifact-lifecycle.md:29`); slice 2 Q5 names the agent-runtime contract space (`slice-02-architecture.md:31`). Confidence: **high**.
- **What dissolves:** if a future re-slice treats §1.4 as the partition specification rather than reading the prompts, escalates to B.

### Finding 5 — INITIATIVE.md §3.5 validation-mechanism list never names validation-against-gsd-2-as-runtime-application
- **Artifact / Location:** `INITIATIVE.md` §3.5 lines 112-114
- **Quote:** `"Stress-testing path is itself open: re-articulation in fresh session + comparison; first-wave findings testing it indirectly; external review; eventual codification in dedicated uplift repo's VISION.md."`
- **Lens-relevance:** §2.4 (e) — treats goal as discursive object to be re-articulated and reviewed rather than as something to be validated against what gsd-2 actually exposes. Consistent with v1-GSD habit of treating harness as markdown/discursive surface.
- **Type:** negative-space + implication
- **Classification:** **Class A**
- **Justification:** This is a thin observation; flagged per spec §2.3 meta-discipline note about uncertain phrasings. The artifact correctly couples to first-wave findings as one mechanism. First-wave did test articulation against runtime surfaces (F7). §3.5 list is just under-explicit about that mechanism. Confidence: **medium**.

### Finding 6 — SYNTHESIS.md framing-leakage caveat present at §6.4 but structurally narrower than SYNTHESIS-CROSS.md §6's terminal caveat
- **Artifact / Location:** `SYNTHESIS.md` §6.4 lines 578-595 (the caveat is present, contrary to a quick read; but framed as *"Where in-house framing might be over-fitting cross-vendor observations"* — `SYNTHESIS.md:582`).
- **Comparison:** `SYNTHESIS-CROSS.md:203`: *"The R1-R5 and six-context frames are useful inputs, not observed facts in gsd-2. Where they overfit the evidence, incubation should loosen them rather than treat this synthesis as authority."* SYNTHESIS-COMPARISON.md §3.3 (`:204-209`) flags this asymmetry as asymmetric-coverage: *"Codex's caveat is substantively important and methodologically clean. Claude could-have-but-did-not surface this."*
- **Lens-relevance:** §2.4 (a) at the meta-level — same-vendor synthesis applies framing-widening's R1-R5 + six-context vocabulary throughout body, treating these as inputs-that-are-now-observations rather than as inputs-for-deliberation.
- **Type:** negative-space + implication
- **Classification:** **Class C** (narrowly load-bearing)
- **Justification:** Per SYNTHESIS-COMPARISON.md §2.1, the operating-frame-disposition-timing divergence between same-vendor and cross-vendor partly tracks how deeply each read framing-widening's §3.3 disposition-discipline. Same-vendor's deeper read may itself be a same-vendor-context-immersion artifact (per §4.1's "inverted asymmetry"); incubation reading SYNTHESIS.md may inherit framing as fact. Why-C-not-B: if incubation operates under R1-R5 / six-context as observed-facts-in-gsd-2 rather than as deliberation-frames, §5.3 context-anchoring + §5.2 R-mix dispositions inherit the over-fit silently. Why-narrowly-C: comparison-author already self-flags in §3.3 + §4.1; audit's marginal value is mainly pointing back at the comparison's own self-flagging. Confidence: **medium**.
- **What dissolves:** an addendum to SYNTHESIS.md or SYNTHESIS-COMPARISON.md §6 that lifts SYNTHESIS-CROSS.md §6's caveat into a cross-cited integration-frame reminder so incubation-reading carries it explicitly.
- **Grounding:** `META-SYNTHESIS.md:69-77` carries-forward — incubation can carry these as observations *qualified by* typed vocabulary requirements; treating R1-R5 as observed facts violates that typing discipline.
- **Disposition implication:** affects §5.1 (metaquestion under what context-anchoring) and §5.3 (context-anchoring disposition).

### Finding 7 — DECISION-SPACE.md §3.6 preserves the singular-axis question-shape
- **Artifact / Location:** `DECISION-SPACE.md` §3.6 lines 652-660
- **Quote:** `"Logan's articulation prioritizes time-extension as the key axis. ... Is 'long-horizon' the dominant framing or one of several?"`
- **Lens-relevance:** §2.4 (e) at second remove — question's framing presupposes a single axis to evaluate. Per `framing-widening.md:123`: the question presupposed a single axis; if the bundled-five-dimensions reading is correct, the question is mis-posed.
- **Type:** question-shape + implication
- **Classification:** **Class B**
- **Justification:** Framing-widening §2 corrects to six-context plurality. Both syntheses + comparison carry plurality. §3.6 artifact text remains. Why-B-not-C: incubation reads synthesis-and-comparison; §3.6 is in deferred-questions register where it's already framed as open. Why-not-A: question-shape presupposes singularity, exactly the implicit-narrowing the framing-widening corrected. Confidence: **medium**.
- **What dissolves:** if a fresh reader (or migration handoff) treats §3.6 as canonical question-shape rather than reading framing-widening, escalates to C.

### Finding 8 — Slice prompts (preamble + slice-01..05) scan-clean for v1-GSD vocabulary; slicing partition labels work against runtime-application-naming but prompts substantially correct
- **Artifact / Location:** `preamble.md` + `slice-01..05`
- **Quote (preamble.md:38-39):** `"Do not adopt the dispatching project's vocabulary if you encounter it leaking through gsd-2's documentation; report what you see using gsd-2's own terms or neutral terms."`
- **Lens-relevance:** §2.4 (a) negative; (b) +/- — slice 2 Q5 names plural agent-runtime contract; slice 3 Q2 (post-revision) asks about multiple workflow engines; slice 4 Q2 (post-revision) asks about multiple extension mechanisms; slice 5 Q5 stays observational.
- **Type:** vocabulary-scan + question-shape (negative finding)
- **Classification:** **Class A** (cosmetic-or-cleaner)
- **Justification:** Scanned each slice prompt + preamble for "patcher", "skills-bundle", "hybrid", "harness", "wrappers around gsd-2", "skills + hooks + markdown", "--mode headless". None present. Slice 1 Q4 names "agent-facing, human-facing, or both" (right openness shape). Slice 2 Q5 explicitly invites "no agent-runtime contract" as load-bearing-observation (`slice-02-architecture.md:49`). Confidence: **high**.
- **What dissolves:** if slice 1/3/4 *outputs* substantively used "patcher / skills-bundle" register (would only emerge from inspecting outputs — not in scope without propagation-sampling trigger), classification could shift; from prompts alone: clean.

### Finding 9 — SYNTHESIS-COMPARISON.md §4.4 framing-import drift observation does not extend to a same-vendor-framing-application-as-fact check at §5 axes
- **Artifact / Location:** `SYNTHESIS-COMPARISON.md` §4.4 lines 266-271 + §4.1 lines 242-250
- **Quote (§4.4):** *"The comparison author (Claude, in-session) initially reasoned about §0 anti-pattern self-checks by importing arxiv-sanity-mcp's project-specific anti-pattern checklist (from AGENTS.md) as if it were generic governance discipline applicable to gsd-2-uplift comparison reasoning. Logan corrected this..."*
- **Lens-relevance:** §2.4 (a) at meta — §4.4 catches one specific framing-import drift (host-project anti-pattern checklist). It does not do the broader symmetric check: did the comparison-author's *application* of framing-widening's R1-R5 / six-context as the integration grammar at §1, §2, §5 carry an analogous drift? Per `SYNTHESIS-CROSS.md:203` and `META-SYNTHESIS.md:38` (typed-extension-vocabulary), treating these as the integration grammar without explicit "these are inputs, not facts" framing in §1 is an analogous import.
- **Type:** negative-space + implication
- **Classification:** **Class C** (narrowly load-bearing)
- **Justification:** §4.4 is well-done and self-aware. The Class-C characterization is not "comparison author missed something obvious" — it's "comparison author surfaced a specific drift, but the symmetric integration-grammar-as-fact check is the deeper instance of the same pattern, and its absence affects §5 dispositions." §5.1 metaquestion + §5.2 R-mix + §5.3 context-anchoring all use R1-R5 / six-context as the deliberation grammar; if Logan reads them as observation-grammar instead of as inputs-Logan-brought-in, the deliberation surface shrinks. SYNTHESIS-COMPARISON.md §6.3 names the in-session-collaboration caveat and §6.5 names frame-revision discipline (`:399`), so structural correction is partially present at §6 — but downstream of where framing is applied at §5. Why-narrowly-C: §6 caveats partly mitigate. Confidence: **medium**.
- **What dissolves:** a §5 frontmatter note (or §5.1 opening note) carrying SYNTHESIS-CROSS.md §6's caveat verbatim, so integration grammar is foregrounded as inputs at point-of-use.
- **Grounding:** `META-SYNTHESIS.md:55` prohibition (*"Do not treat all extension-adjacent mechanisms as same-kind extension surfaces"*) — analogous: do not treat R1-R5 / six-context as same-kind observed-facts.
- **Disposition implication:** affects §5.1 (whether direction-holds-with-qualifications is within-frame or out-of-frame claim), §5.3 (whether six-context is the space within which Logan picks vs whether Logan can revise the space).

---

## §2. Cross-artifact propagation patterns

The audit's lens predicted v1-GSD vocabulary in INITIATIVE.md / DECISION-SPACE.md / framing-widening might propagate through slice prompts → SYNTHESIS → SYNTHESIS-CROSS → SYNTHESIS-COMPARISON. The pattern observed is **partial propagation followed by substantial correction**:

- **Pattern 1 — Original "patcher / skills / hybrid" framing localized to INITIATIVE.md §3.2.** Does not propagate into slice prompts (which forbid dispatching-project vocabulary; F8) or syntheses (which use four-act / four-extension-subsystem vocabulary instead). Framing-widening's §4 four-act + §1 R1-R5 widening lifted before W1 dispatch + post-W1 syntheses. Pattern 1: "introduced + caught + corrected."

- **Pattern 2 — "harness" framing as assembly-with-conventions.** INITIATIVE.md §1 terminology note (F2) sets gsd-2 inside an assembly. SYNTHESIS.md F7 corrects by naming plural agent-runtime contracts. SYNTHESIS-CROSS.md §1.1 (`SYNTHESIS-CROSS.md:41-46`) corrects more directly: *"gsd-2 is a product-scale agent host, not a thin planning layer... The target is a large runtime/product."* Pattern 2: "introduced + propagated lightly + corrected explicitly by cross-vendor synthesis."

- **Pattern 3 — R-mix narrowing to R1/R2/R3 in DECISION-SPACE §1.8.** F3. Framing-widening §1 widens to R1-R5 with R4 named. Both syntheses carry R1-R5. SYNTHESIS-COMPARISON.md §2.1 surfaces the residual: even with R4 widening accepted, *when* the operating frame shifts is the load-bearing divergence between same-vendor and cross-vendor reads. Pattern 3: "introduced + widened + residual disposition-timing surface for incubation."

- **Pattern 4 — Single-axis "long-horizon" framing in DECISION-SPACE §3.6.** F7. Framing-widening §2 corrects to six-context plurality. Stable through comparison. Pattern 4: "introduced + corrected upstream of synthesis dispatch + plurality stable."

- **Pattern 5 — Same-vendor framing-application-as-fact at the synthesis-comparison integration grammar level.** F6 + F9. Meta-pattern that emerges *because* framing-widening corrected upstream vocabulary: now R1-R5 / six-context / four-act is the integration grammar, which means same-vendor applies it without explicit "these are inputs not observed facts" framing at points of application. SYNTHESIS-CROSS.md §6 catches this; SYNTHESIS-COMPARISON.md §3.3 surfaces the catch as asymmetric-coverage; §4.4 names a sibling drift (host-project anti-pattern import); but symmetric framing-application-as-fact check is not extended to §5 axes.

Overall propagation trajectory: **introduce → propagate-lightly → correct-via-framing-widening → residual-at-synthesis-integration-grammar**. The residual (Pattern 5) is exactly where the audit lens predicted the failure mode would be most subtle — premise-bleed via integration-grammar inheritance rather than vocabulary-import.

---

## §3. Notable absences

Where the lens predicts premise-bleed should appear but doesn't:

- **Slice prompts.** Per F8: preamble explicitly forbids dispatching-project vocabulary import; slice 2 Q5 + slice 3 Q2 (post-revision) + slice 4 Q2 (post-revision) substantively name plural runtime / dispatch / extension subsystems. The slicing partition labels (DECISION-SPACE.md §1.4) under-name runtime-application surfaces, but the *prompts* substantially correct.
- **SYNTHESIS-CROSS.md.** Carries "thin planning layer" rejection (`:41-46`), names six R2-shaped surfaces (`:60-62, :178`), elevates R4 to first-class (`:85, :190`), carries framing-leakage caveat verbatim (`:203`). The cross-vendor read is the structural inverse-image of v1-GSD-bleed — exactly what audit-spec §3.2 predicted.
- **SYNTHESIS-COMPARISON.md §4.4.** The framing-import drift self-observation catches one specific instance and names it for traceability rather than burying it.
- **META-SYNTHESIS itself.** Coverage of runtime-application surfaces was sufficient grounding for every claim in this audit; no fallback to source reading needed (0 of 5).

The combined picture: the artifact set is *partly self-audited* on the property this audit audits, primarily because cross-vendor synthesis and the comparison's §3.3 + §4.1 + §4.4 + §6 do that work. The Class-C residual (F6, F9) is where the self-audit's reach stops short of §5 axes.

---

## §4. Confidence and limits

- **Confidence on classifications:** medium-high overall. Class A judgments (F1, F4, F5, F8) are high. Class B judgments (F2, F3, F7) are medium. Class C judgments (F6, F9) are medium — load-bearing-ness depends on whether §6 caveat-machinery is read together with §5 axes or only after them.
- **Self-flagged concerns:**
  - **Risk of under-classifying the framing-as-fact pattern.** Dispatch warns under-classification of register-shaped findings is the same-vendor risk to guard against. F6 and F9 are exactly register-shaped, and I have classified at the bottom of Class C ("narrowly load-bearing"). I considered escalating either to stronger Class C with disposition-changing implication and stepped back: SYNTHESIS-COMPARISON.md §6.5's `"If the comparison's framing of §2.1 is read by Logan as already-pre-disposing the operating-frame question, the comparison should be revised, not the framing forced to fit"` (`:400`) is the structural correction-mechanism, present. Narrow-Class-C is the right calibration — but I could be wrong about narrowness.
  - **Risk of confusing same-vendor-context-immersion-depth with premise-bleed.** Per SYNTHESIS-COMPARISON.md §4.1's "inverted asymmetry" observation, same-vendor reading framing-widening *deeper* may itself be context-immersion-depth rather than register-leak. F6 specifically might be appropriate context-immersion rather than premise-bleed; both readings have merit; classification is contestable.
  - **Same-vendor M1 caveat (per dispatch).** I am same-vendor with the comparison-author, who is same-vendor with the same-vendor synthesis. The shared Claude+Logan framing inheritance applies to me. Specifically I cannot self-detect: (i) whether the framing-widening's R1-R5 / six-context vocabulary that I treat as legitimately-applied-with-residual is in fact a deeper bleed; (ii) whether my Class C classifications of F6 and F9 are calibrated against §6 caveat-machinery rightly or whether I am undercounting because the caveat-machinery shares the inheritance. Differential analysis (post-hoc, in main thread) against the prior independent same-vendor read should test these.
  - **No sampling-trigger fired.** Slice-output propagation-sampling option (spec §5.2.5; cap 3-5) was not triggered because Class B/C findings were grounded in artifact-text-as-such, not in propagation that needed sampling. A more aggressive auditor might have sampled slice 4 + slice 5 outputs to test whether the four-extension-subsystems vocabulary actually appears in source-grounded form. I judged the slice 4 audit + (vi) addendum citations in SYNTHESIS.md F2 + SYNTHESIS-CROSS.md §1.3 + SYNTHESIS-COMPARISON.md §1.2 sufficient grounding without propagation-sampling. Conservatism may have under-tested this.
  - **No vetted-replacement-vocabulary lookup gap flagged.** Per spec §2.3 meta-discipline note. I noted F2's "harness as assembly-with-conventions" sits at the edge of the lookup's "harness as thin layer" row — recording here rather than inventing replacement language.
- **Out of scope (per §5.4 no-re-exploration):** I did not read gsd-2 source beyond META-SYNTHESIS coverage, did not re-execute slice questions, did not construct alternative synthesis or comparison readings, did not propose specific revision wordings.
- **Slice-output sampling tally:** 0 of 3-5 cap.
- **Source-reading tally:** 0 of 5 soft-cap.
- **Isolation incidents:** none. No Step-1 outputs were encountered. Forbidden-reading list respected (FINDINGS.md, .logs/, AUDIT-SPEC-REVIEW.md, comparison-drafting-decisions.md, post-W2-handoff, recent STATE.md/OVERVIEW.md updates referring to comparison-drafting status all not read).

---

## §5. Non-binding disposition signal

- **Why Logan might choose commit-as-is:** the only Class-C findings (F6, F9) are narrowly-load-bearing and already partly-self-audited by SYNTHESIS-COMPARISON.md §3.3 + §4.1 + §4.4 + §6. Class-B findings (F2, F3, F7) are operationally widened upstream (framing-widening) even where artifact text is unrevised. Class-A findings are correctly-bounded by the artifact set. Incubation reading SYNTHESIS-COMPARISON.md + both syntheses will encounter the integration-grammar caveat at §6, and §5 dispositions are explicitly Logan-disposed not pre-decided. If Logan reads §5 axes with §6 caveats actively-in-mind (not just at-end-of-read), the artifact-set works as-is.

- **Why Logan might choose commit-with-addendum:** F6 + F9 residuals point at a single corrigible thing — the integration grammar at SYNTHESIS-COMPARISON.md §5 is applied without the framing-leakage caveat foregrounded at the point-of-use. A small addendum (one paragraph) at SYNTHESIS-COMPARISON.md §5 frontmatter or §5.1 opening that lifts SYNTHESIS-CROSS.md §6's caveat (R1-R5 / six-context as inputs not observed facts; loosen-not-treat-as-authority) into the §5-axis-reading frame would dissolve both Class-C findings without revising the syntheses. The addendum could also note that F2's "harness" terminology and F3's R2-base disposition framing in INITIATIVE.md / DECISION-SPACE.md remain operationally widened by the framing-widening + synthesis layer, and that incubation should read them as such. This is the cheapest disposition that addresses the load-bearing residual.

- **Why Logan might choose revise-before-commit:** if Logan reads Pattern 5 (framing-application-as-fact at §5 axes; F6 + F9) as more than narrowly-load-bearing — i.e., if Logan reads the comparison's §5 as already-pre-disposing the deliberation-shape regardless of §6 caveat-machinery — revision rather than addendum is the right shape. Specifically: SYNTHESIS-COMPARISON.md §5.1's "what incubation should ask" sub-questions and §5.3 six-context anchoring's framing could be revised to make integration grammar foregrounded as inputs-Logan-can-revise rather than as the deliberation surface. Heavier than addendum; cost is real (revision touches §5's structural shape, not just frontmatter); value is preventing silent-narrowing at point-of-use. I don't think the evidence warrants this level — the §6 caveat machinery is present and the comparison itself surfaces the relevant typology — but Logan is the disposing reader.

Logan disposes per §8.

---

## Executive summary (per dispatch brief, 2-4 paragraphs)

**Headline + classification breakdown.** Nine premise-bleed instances surfaced: 4 Class A (cosmetic/wording-addendum), 3 Class B (substantive but non-disposition-changing), 2 Class C (load-bearing for §2.1/§5 dispositions, both narrowly so). The independent read is that premise-bleed is **localized rather than pervasive**. The literal v1-GSD vocabulary ("patcher / skills / hybrid"; R1/R2/R3-without-R4; "long-horizon" as singular axis) sits in INITIATIVE.md §3.2 + DECISION-SPACE.md §1.8 + §3.6 as artifact-traces of the original framing, and was substantially corrected upstream of the syntheses by the framing-widening artifact. The residual (Findings 6 + 9) is at the meta-level: the framing-widening's R1-R5 / six-context / four-act vocabulary is *now the integration grammar* of SYNTHESIS.md and SYNTHESIS-COMPARISON.md §5, applied without explicit "these are inputs not observed facts in gsd-2" framing at the points-of-application. SYNTHESIS-CROSS.md §6 carries this caveat; SYNTHESIS-COMPARISON.md §3.3 + §4.1 + §4.4 self-audit the asymmetry, and §6.5 carries frame-revision discipline — but these caveats are downstream of where the framing is applied at §5 axes.

**Isolation incidents encountered.** None. No Step-1 outputs were inadvertently read. The forbidden-reading list (FINDINGS.md, .logs/, AUDIT-SPEC-REVIEW.md, comparison-drafting-decisions.md, post-W2-handoff, recent STATE.md/OVERVIEW.md updates) was respected fully. Slice-output sampling cap 0/3-5 used; source-reading cap 0/5 used (META-SYNTHESIS coverage was sufficient for all grounding claims, including the M1 paired-review caveat ground for Findings 6 and 9).

**Confidence + key self-flagged concerns including same-vendor M1 caveat.** Confidence on classifications is medium-high overall (Class A high, Class B medium, Class C medium). The principal self-flagged concerns: (i) under-classifying register-shaped findings is the same-vendor failure mode the dispatch brief warns against, and Findings 6 + 9 are register-shaped at the bottom of Class C — I have considered escalating and stepped back because the comparison's §6 caveat-machinery is the structural correction, but the calibration is contestable; (ii) the same-vendor M1 inheritance applies to me — I cannot self-detect whether my treatment of the framing-widening's R1-R5 / six-context as legitimately-applied-with-residual is itself a deeper bleed, nor whether my reliance on SYNTHESIS-COMPARISON.md's caveat-machinery as sufficient correction is calibrated rightly given that the caveat-machinery shares the same Claude+Logan inheritance; (iii) I did not trigger slice-output propagation-sampling because Class B/C findings were grounded in artifact-text directly, but a more aggressive auditor might have sampled slice 4 + slice 5 outputs to test whether the four-extension-subsystems vocabulary appears in source-grounded form rather than as synthesis-construct.

**Surprise relative to the spec's framing prediction.** The spec predicted that v1-GSD vocabulary (patcher/skills/hybrid; harness-as-thin-layer; under-weighted runtime-application surfaces) might propagate through slice prompts → syntheses → comparison. What I observed instead is a different shape: the vocabulary-level bleed is largely localized to INITIATIVE.md + DECISION-SPACE.md and substantially corrected at framing-widening + slice-prompt-revision time. The residual is one register-step subtler — the *integration grammar* at the synthesis-comparison level (R1-R5 / six-context / four-act applied throughout §1, §2, §5 of SYNTHESIS-COMPARISON.md) inherits the framing-as-fact pattern that was the deeper failure mode the spec lens anticipated. The artifact-set has substantial self-audit machinery for this (SYNTHESIS-CROSS.md §6 caveat; SYNTHESIS-COMPARISON.md §3.3, §4.1, §4.4, §6.5), and the audit's marginal value is mostly: pointing back at where the artifact-set's own self-audits don't quite reach (the §5-axis-reading frame). The cheapest disposition that addresses the load-bearing residual is a one-paragraph addendum at SYNTHESIS-COMPARISON.md §5 lifting SYNTHESIS-CROSS.md §6's caveat into the point-of-use; revision is heavier than the evidence warrants but not unreasonable if Logan reads Pattern 5 as more-than-narrowly load-bearing.
