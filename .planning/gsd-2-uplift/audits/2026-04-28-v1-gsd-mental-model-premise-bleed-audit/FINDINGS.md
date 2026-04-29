---
type: premise-bleed-audit-findings
date: 2026-04-29
auditor_step1: codex GPT-5.5 high
spec: ./AUDIT-SPEC.md
target:
  - .planning/gsd-2-uplift/INITIATIVE.md
  - .planning/gsd-2-uplift/DECISION-SPACE.md
  - .planning/gsd-2-uplift/exploration/SYNTHESIS.md
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md
  - .planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md
  - .planning/deliberations/2026-04-28-framing-widening.md
  - .planning/gsd-2-uplift/orchestration/preamble.md
  - .planning/gsd-2-uplift/orchestration/slice-01-mental-model.md
  - .planning/gsd-2-uplift/orchestration/slice-02-architecture.md
  - .planning/gsd-2-uplift/orchestration/slice-03-workflow-surface.md
  - .planning/gsd-2-uplift/orchestration/slice-04-artifact-lifecycle.md
  - .planning/gsd-2-uplift/orchestration/slice-05-release-cadence.md
  - .planning/gsd-2-uplift/orchestration/synthesis-spec.md
  - .planning/gsd-2-uplift/orchestration/audit-spec.md
status: step1-complete; no-step2-trigger
---

# §0. Step-1 summary

- Total premise-bleed instances surfaced: 6
- Classification breakdown:
  - Class A (cosmetic / wording-addendum): 1
  - Class B (substantive but non-disposition-changing): 5
  - Class C (load-bearing for §2.1 / §5 dispositions): 0
- Top-line read: Premise-bleed is real but front-loaded. It appears most clearly in the initial staging vocabulary ("patcher / skills / hybrid") and in early R1/R2/R3 question-shapes that made extension-style intervention easier to see than runtime-application orchestration surfaces. The downstream chain largely self-corrects: framing-widening, both syntheses, and the comparison explicitly elevate R4, decompose extension surfaces, and name headless/RPC/MCP/runtime surfaces.
- Step-2 escalation triggered: no (no Class C)

# §1. Per-instance findings

### Finding 1

- **Artifact:** `.planning/gsd-2-uplift/INITIATIVE.md`
- **Location:** §3.2, lines 81-88
- **Quote:** "What design shape -- patcher, skills, hybrid?" (`.planning/gsd-2-uplift/INITIATIVE.md:81`)
- **Lens-relevance:** §2.4(a), §2.4(c), §2.4(e)
- **Type:** vocabulary-scan
- **Classification:** Class B
- **Justification:** This is the cleanest v1-GSD vocabulary hit. The candidate set is framed around a modify-existing-installation pattern, skills, and a hybrid of those rather than typed runtime/application surfaces. The same section does constrain the vocabulary by saying "Choice depends on what gsd-2 actually exposes" (`.planning/gsd-2-uplift/INITIATIVE.md:88`), which keeps it below Class C. It is still more than cosmetic because the phrasing recurs later in the synthesis-spec and in SYNTHESIS §2.5 as the named origin of the design-shape question.
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Sampled later synthesis use. `SYNTHESIS.md` explicitly reopens the question as "Per `INITIATIVE.md §3.2` (patcher / skills / hybrid / something-else)" while mapping it into four-act plurality (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:318-321`). Sampling tally: 1/5.

### Finding 2

- **Artifact:** `.planning/gsd-2-uplift/INITIATIVE.md`
- **Location:** §2 and §5, lines 48-58 and 137-143
- **Quote:** "R2 (extension) as base + primary, contingent on first-wave finding gsd-2 has adequate extension surfaces" (`.planning/gsd-2-uplift/INITIATIVE.md:52`)
- **Lens-relevance:** §2.4(b), §2.4(f), §5.2.3(i)/(ii)
- **Type:** negative-space
- **Classification:** Class B
- **Justification:** Runtime-application surfaces are present in the slice partition through "Architecture + runtime + Pi SDK relationship" (`.planning/gsd-2-uplift/INITIATIVE.md:140`), but the operating-frame and load-bearing slice logic make "extension surfaces" the explicit hinge for whether R2 survives (`.planning/gsd-2-uplift/INITIATIVE.md:142`). Headless/RPC/MCP/session-control/state-control are not named as first-class candidate intervention surfaces in the initial operating-frame section. This omission matters because primary grounding treats plural runtime surfaces as central: "CLI/TUI, headless/RPC, in-process MCP, standalone MCP, RPC client, and adjacent integration surfaces are real" (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md:27`). It remains Class B because slice 2 and slice 3 prompts later ask runtime and workflow-surface questions, and the outputs surface headless/RPC/MCP clearly.
- **Grounding citation (if negative-space):** META-SYNTHESIS says the "plural runtime-surface claim survives" and names headless/RPC/MCP surfaces (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md:27`); it also says R4 should remain explicit because those surfaces are real (`.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md:73-75`).
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Sampled slice 3 output. It reports that the CLI exposes "headless" and "RPC/MCP/text execution" (`.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md:102`) and that `headless query` avoids LLM invocation (`.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md:104`). Sampling tally: 2/5.

### Finding 3

- **Artifact:** `.planning/gsd-2-uplift/DECISION-SPACE.md`
- **Location:** §1.8, lines 232-260
- **Quote:** "The uplift project's relationship to gsd-2 upstream is **R2 (extension) as base and primary**, with **R2+R3 hybrid (extension + upstream PRs) as preferred where workflow allows**." (`.planning/gsd-2-uplift/DECISION-SPACE.md:234`)
- **Lens-relevance:** §2.4(f), §2.4(g), §5.2.3(iii)
- **Type:** surface-weighting
- **Classification:** Class B
- **Justification:** The decision makes extension the base strategy and frames the load-bearing evidence around whether gsd-2 has "at least *some* extension surfaces" (`.planning/gsd-2-uplift/DECISION-SPACE.md:249`). Under the corrected frame, runtime/machine surfaces are not merely evidence for or against extension; they create R4-shaped intervention routes. The downstream comparison says the R-mix has "narrowed" and "widened" relative to this pre-W1 framing because R3 becomes conditional and R4 is elevated (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:306`). That means the original weighting was substantive. It is not Class C for this Step-1 audit because the final comparison explicitly surfaces the divergence and assigns Logan-adjudication rather than silently carrying the old R2 base frame into §5.
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Not sampled further; propagation is visible in the audited synthesis/comparison artifacts themselves.

### Finding 4

- **Artifact:** `.planning/gsd-2-uplift/orchestration/synthesis-spec.md`
- **Location:** §2.1-§2.5, lines 93-128
- **Quote:** "### §2.1 R2 (extension) viability per DECISION-SPACE §1.8" (`.planning/gsd-2-uplift/orchestration/synthesis-spec.md:95`)
- **Lens-relevance:** §2.4(a), §2.4(f), §2.4(g)
- **Type:** question-shape
- **Classification:** Class B
- **Justification:** The synthesis template asks directly for R2 and R3 viability, then asks design-shape candidates "Per §3.2 (patcher / skills / hybrid / something-else)" (`.planning/gsd-2-uplift/orchestration/synthesis-spec.md:125-127`). This prompt shape likely helped preserve the early vocabulary long enough that SYNTHESIS.md had to re-map it into R1-R5/four-act vocabulary. It is non-disposition-changing because the same synthesis-spec also includes framing-widening Part I §1 as an input, and the resulting SYNTHESIS.md did in fact evaluate R1-R5 including R4 and R5.
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Covered by Finding 1 propagation sample.

### Finding 5

- **Artifact:** `.planning/gsd-2-uplift/exploration/SYNTHESIS.md`
- **Location:** §1.1, lines 83-88
- **Quote:** "gsd-2 is a vendored modified Pi fork with substantial GSD-authored code embedded inside `pi-coding-agent`" (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:86`)
- **Lens-relevance:** §2.3 replacement-vocabulary lookup; META-SYNTHESIS §3 prohibited articulations
- **Type:** vocabulary-scan
- **Classification:** Class A
- **Justification:** This is a vocabulary-precision concern rather than a live premise-bleed driver. The corrected lookup says to avoid the over-compressed whole-repo shorthand and instead describe a GSD CLI/application layer built around vendored, modified Pi-derived packages. The surrounding SYNTHESIS section is trying to explain entanglement and ADR-010, not reduce the whole repo to Pi. Later artifacts preserve the boundary correction, and the comparison names the broader "GSD glue plus bundled extensions" framing. A wording addendum would be enough; downstream conclusions do not change.
- **Grounding citation (if negative-space):** n/a
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Not sampled; this is a local wording/classification issue.

### Finding 6

- **Artifact:** `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md`
- **Location:** §5.2, lines 298-312
- **Quote:** "R2 (extension). Viable but surface-specific (per §1.6 + §1.2). Decomposes across Pi extensions / GSD ecosystem extensions / workflow plugins / skills / hooks / MCP tools -- six R2-shaped surfaces, not one." (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:302`)
- **Lens-relevance:** §2.4(c), §2.4(f), §2.4(g)
- **Type:** surface-weighting
- **Classification:** Class B
- **Justification:** The comparison's local phrasing risks re-importing an R2 umbrella over surfaces that the corrected lookup says should be typed before R-strategy assignment. Hooks and MCP tools can be R2-shaped in some contexts, but the same artifact also treats R4 as "strongly viable" with "headless, query, RPC, MCP, hooks, workflow templates" (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:304`). This is therefore not an under-weighting failure in the conclusion; it is a local vocabulary-precision issue in the R2 decomposition sentence. The corrected frame would keep the type vocabulary stable before assigning R2 vs R4 meaning.
- **Disposition implication (Class C only):** n/a
- **Propagation sample (if applicable):** Not sampled; this is in the final comparison artifact itself.

# §2. Cross-artifact propagation patterns

- Pattern 1: Initial design-shape vocabulary propagated, then got corrected. INITIATIVE.md starts with "patcher / skills / hybrid" (`.planning/gsd-2-uplift/INITIATIVE.md:81-86`); synthesis-spec repeats that frame as a required design-shape prompt (`.planning/gsd-2-uplift/orchestration/synthesis-spec.md:125-127`); SYNTHESIS.md then explicitly re-maps it through four-act plurality (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:318-321`). The propagation exists, but the later artifacts correct rather than preserve the v1-GSD candidate set.
- Pattern 2: R2-base framing propagated into the original operating frame, then became the central divergence instead of a hidden premise. DECISION-SPACE.md says R2 is base/primary (`.planning/gsd-2-uplift/DECISION-SPACE.md:234`); framing-widening adds R4 and R5, including external orchestration over `gsd headless` and MCP surfaces (`.planning/deliberations/2026-04-28-framing-widening.md:77-85`); SYNTHESIS-COMPARISON.md then marks R4 weighting as a Logan-adjudication divergence (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:150-163`). This is the main reason I do not classify any item as Class C: the potentially load-bearing issue is surfaced for disposition rather than silently embedded.
- Pattern 3: Runtime-application surfaces were under-named in early staging but overrepresented in evidence outputs and final synthesis. Slice outputs name standalone CLI/application status, headless/MCP/RPC, state, session control, workflow engines, and extension plurality (`.planning/gsd-2-uplift/exploration/01-mental-model-output.md:64-86`, `.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md:102-130`, `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md:296-330`). The omission did not survive as absence in SYNTHESIS-CROSS or SYNTHESIS-COMPARISON.
- Pattern 4: The strongest remaining bleed is vocabulary precision, not substance. Terms like "extension surface," "vendored modified Pi fork," and "R2-shaped surfaces" recur, but the audited artifacts usually surround them with qualifications, confidence limits, and explicit deferral. The risk is future reader compression, not current §2.1/§5 conclusion failure.

# §3. Notable absences

- The orchestration preamble directly resists pre-pitched intervention framing: "Do not anchor your reading to any specific intervention shape (patcher / extension / fork / etc.)" (`.planning/gsd-2-uplift/orchestration/preamble.md:15-17`). This is an inverse signal: the slice agents were not simply handed the v1-GSD premise.
- Slice 3 explicitly asked for multiple workflow engines or dispatch shapes and told the reader to "Resist assuming a single engine" (`.planning/gsd-2-uplift/orchestration/slice-03-workflow-surface.md:27`). That negative-space concern is therefore already handled at question-shape level for workflow surfaces.
- Slice 4 explicitly asked whether multiple extension mechanisms are unified or distinct and listed workflow templates, skills, MCP tools, hooks, and ecosystem plug-ins as examples (`.planning/gsd-2-uplift/orchestration/slice-04-artifact-lifecycle.md:29`). This strongly reduced the chance that "skills" would remain the primary extension surface.
- SYNTHESIS-CROSS begins by saying gsd-2 is a "product-scale agent host, not a thin planning layer" (`.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md:41-46`). That directly falsifies the predicted thin-layer bleed at the cross-vendor synthesis layer.
- SYNTHESIS-COMPARISON names the in-session/framing caveat and says convergent findings within R1-R5/six-context framing do not validate the framing itself (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:373-377`). That is a strong self-correction against treating the imported vocabulary as settled ontology.

## §3.1 Per-artifact calibration notes

These notes are not additional findings. They record why the per-artifact pass did not produce more Class B/C candidates.

- **INITIATIVE.md:** The opening "harness" definition is broad enough to avoid the thin-layer sense as its main meaning. It says "harness" refers to "gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions" and explicitly says "Not gsd-2 alone" (`.planning/gsd-2-uplift/INITIATIVE.md:44`). The word is therefore not itself a premise-bleed finding; the issue is the later design-shape vocabulary and R2 emphasis.

- **INITIATIVE.md:** The document also marks itself provisional. It says the articulation "has not been stress-tested" and should be treated as "operating frame, not authoritative goal" (`.planning/gsd-2-uplift/INITIATIVE.md:46`). This lowers confidence that the early v1-GSD vocabulary was intended as a settled decision rather than a starter frame.

- **DECISION-SPACE.md:** §1.8 is the strongest early surface-weighting issue, but the same file's incubation checkpoint asks to check whether "R1/R2/R3 hybrid has narrowed" and whether "direction-shifting evidence surfaced beyond the starter list" (`.planning/gsd-2-uplift/DECISION-SPACE.md:576-579`). That means the file has an update mechanism for precisely the kind of premise correction found later.

- **framing-widening.md:** This artifact is mostly a correction rather than a bleed site. It explicitly defines R4 as work that can "invoke `gsd headless`" and compose with MCP surfaces while leaving gsd-2 unchanged (`.planning/deliberations/2026-04-28-framing-widening.md:77-83`). It also states that R4 is named to "avoid implicit narrowing" (`.planning/deliberations/2026-04-28-framing-widening.md:85`).

- **framing-widening.md:** The artifact does still list custom skills and hooks inside R4 configuration examples (`.planning/deliberations/2026-04-28-framing-widening.md:79`), but it immediately distinguishes artifacts gsd-2 integrates from artifacts that invoke gsd-2 from external orchestrators (`.planning/deliberations/2026-04-28-framing-widening.md:81-85`). I therefore did not count this as skills-primary bleed.

- **SYNTHESIS.md:** The artifact contains early shorthand like "vendored modified Pi fork," but its substantive sections strongly correct the v1-GSD frame: it names "two architecturally distinct workflow engines" (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:39`), "at least four parallel extension surfaces" (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:99-108`), and R4 as "viable" with headless/RPC/MCP evidence (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:202-213`).

- **SYNTHESIS.md:** I considered whether §2.5's table over-weights workflow-plugin R2 candidates, but the table includes R4 entries for "generic release-pipeline headless recipe" and "preference-effective-state check" (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:334-337`). That prevents a Class C reading.

- **SYNTHESIS-CROSS.md:** This is the strongest inverse signal. It opens with "R2 remains viable, but not as a single clean 'extension' path" and says first-wave evidence supports "a plural extension/configuration/orchestration picture" including "headless/RPC/MCP" (`.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md:31`). That is the corrected frame, not premise-bleed.

- **SYNTHESIS-CROSS.md:** It explicitly says the target is "a large runtime/product" and warns that any intervention assuming a small surface will miss coupling and maintenance cost (`.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md:41-46`). I found no Class B/C premise-bleed in this artifact.

- **SYNTHESIS-COMPARISON.md:** The comparison is where a Class C candidate would most matter, because it feeds §5 incubation. It does contain the local "six R2-shaped surfaces" concern recorded in Finding 6. But the same section says R4 is "strongly viable" with "headless, query, RPC, MCP, hooks, workflow templates" (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:304`), and then asks Logan whether incubation operates under shifted R2+R4 or evaluates whether to shift (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:307-312`).

- **preamble.md:** The common preamble is anti-premise-bleed by design. It forbids anchoring to prior thinking and tells slice readers to use gsd-2's own terms or neutral terms rather than adopting dispatching-project vocabulary (`.planning/gsd-2-uplift/orchestration/preamble.md:37-40`).

- **slice prompts:** Slice 1 asks for source-grounded self-presentation; slice 2 asks runtime architecture and agent-runtime contract; slice 3 asks workflow engines, hooks, and testing; slice 4 asks extension surfaces and multiple mechanisms; slice 5 asks concrete release/drift inventory. The prompt set is imperfect because synthesis-spec retained old design-shape wording, but the slice prompts themselves do not force a v1-GSD frame.

- **audit-spec.md:** The W2 audit template explicitly includes "Framing-leakage detection" and asks whether cross-vendor output adopted dispatching-project vocabulary (`.planning/gsd-2-uplift/orchestration/audit-spec.md:72-82`). This is an inverse signal: the workflow expected premise bleed and installed an audit check before synthesis.

- **slice outputs sampled:** Slice 3 and slice 4 outputs did not show the early premise surviving. Slice 3 surfaces headless/RPC/MCP/runtime distinctions (`.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md:102-130`), while slice 4 surfaces a substantive extension system and then qualifies that mechanisms are "distinct subsystems with different artifacts and lifecycles" (`.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md:326-328`).

# §4. Step-1 confidence and limits

- Confidence on classification: medium-high.
- Self-flagged concerns:
  - The boundary between Class B and Class C is closest on Findings 2-3. If a reader treats the final comparison's §5.2 as already disposing R4 rather than surfacing it for Logan, Finding 3 could be argued upward. I did not classify it as Class C because §2.1 and §5.2 of the comparison explicitly preserve Logan-adjudication and name both operating-under-shifted-frame and evaluate-whether-to-shift paths (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:158-163`, `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:307-312`).
  - "R2-shaped surfaces" in SYNTHESIS-COMPARISON §5.2 may deserve a future lookup-table entry, because it can blur typed mechanism vocabulary with strategy assignment. I flag it as a concern rather than invent replacement language.
  - The audit spec's own prediction highlights over-weighting skills/workflow-markdown and under-weighting runtime/application surfaces. I found that prediction accurate for INITIATIVE.md and synthesis-spec, but less accurate for the later syntheses and comparison.
- Classification calibration notes:
  - I treated "Class C" as requiring a live downstream conclusion that would likely change if corrected-frame vocabulary were applied.
  - I did not treat "old framing appears in an older staging artifact" as Class C when the later incubation-facing artifact surfaces the correction.
  - I treated negative-space findings as Class B when the absent surface is later recovered by slice outputs or synthesis.
  - I treated vocabulary shorthand as Class A when the surrounding paragraph preserves the corrected substantive claim.
  - I treated vocabulary shorthand as Class B when the shorthand could affect how a future reader identifies the R-strategy or intervention target.
  - The strongest possible Class C argument would be: early R2-base framing still anchors the comparison's §5.2 deliberation order.
  - My reason for rejecting that argument is that the comparison explicitly distinguishes "operate-under-shifted-frame" from "evaluate-whether-to-shift" (`.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:158-163`).
  - A second auditor might still decide that the comparison's framing of the two options is too R2-base-shaped. That would be a fair stress question, but Step-2 is not auto-triggered under this Step-1 classification.
  - I did not count "harness" as a standalone finding because INITIATIVE.md defines it broadly and explicitly distinguishes it from gsd-2 alone (`.planning/gsd-2-uplift/INITIATIVE.md:44`).
  - I did not count "skills" mentions inside typed surface lists when skills appeared alongside workflow plugins, hooks, MCP, headless, or RPC.
  - I did count "skills" as bleed when it was one of three named candidate design shapes before typed surface discovery.
  - I did not count "workflow templates" as bleed where the artifact distinguishes markdown-phase prompt dispatch from yaml-step graph execution.
  - I did count prompt-level R2/R3-only shapes as bleed when they made R4 absent or later than extension viability.
  - I did not treat source-output absences as source defects; this audit is about framing register, not codebase-understanding.
  - I relied on prior-audit primary grounding for corrected-frame authority rather than opening gsd-2 source.
- Cross-vendor framing-leakage caveat: As codex, I may be less sensitive to in-house register cues in the same-vendor artifacts. The clearest residual candidates I can see are explicit vocabulary items rather than subtle stylistic bleed.
- Slice-output sampling tally: 2 slice-output sections sampled, capped at 3-5 per §5.2.5. Sampled `03-workflow-surface-output.md:102-130` and `04-artifact-lifecycle-output.md:296-330`.
- Source-reading tally: 0 gsd-2 source files read. All corrected-frame grounding came from prior-audit primary inputs and sampled checked-in outputs.
- Out-of-scope:
  - I did not re-audit gsd-2 source claims.
  - I did not evaluate whether R4 should win at incubation.
  - I did not propose revised wording.
  - I did not read the forbidden handoff, comparison-drafting deliberation, audit-spec-review deliberation, AUDIT-SPEC-REVIEW.md, STATE.md, or recent OVERVIEW.md status material.

# §5. Non-binding disposition signal

- **Why Logan might choose commit-as-is:** No Class C items surfaced. The potentially load-bearing R4/runtime-application issue is already visible in SYNTHESIS-COMPARISON as a Logan-adjudication divergence, with both start-position options preserved. The final comparison does not silently keep "patcher / skills / hybrid" as the operative frame.
- **Why Logan might choose commit-with-addendum:** The early-artifact premise-bleed is real enough that a short audit addendum could prevent future readers from treating INITIATIVE.md §3.2 or DECISION-SPACE.md §1.8 as current vocabulary. The addendum could also record that "R2-shaped surfaces" should be read as typed-surface shorthand, not as strategy assignment.
- **Why Logan might choose revise-before-commit:** If Logan reads the comparison's R4 disposition-timing section as too dependent on the original R2-base frame, or reads §5.2's "six R2-shaped surfaces" sentence as materially re-collapsing runtime/machine surfaces into R2, then revision before commit would reduce risk. My Step-1 read does not require that path, but it is the plausible route if Logan wants the final comparison to carry less residual v1-GSD vocabulary.

Additional disposition calibration:

- Commit-as-is is most defensible if Logan reads SYNTHESIS-COMPARISON §2.1 and §5.2 as already making the R4 correction auditable enough.
- Commit-with-addendum is most defensible if Logan wants the premise-bleed concern recorded without reopening the comparison draft.
- Revise-before-commit is most defensible only if Logan reads the residual vocabulary as likely to mislead incubation itself, not merely future readers.
- Step-2 is not automatically recommended by this Step-1 file because the Class C count is zero.
- Logan can still manually escalate under AUDIT-SPEC §3.4 if the cluster of Class B findings warrants same-vendor stress.
- The surprising result is not that premise bleed appeared; it did.
- The surprising result is that the later audit/synthesis chain already names most of the correction the spec predicted this audit might need to surface.
