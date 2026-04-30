---
type: audit-findings
date: 2026-04-30
auditor: same-vendor adversarial-auditor-xhigh
reasoning_level: xhigh
mode: independent
artifact_under_audit: Phase D entry corpus (INCUBATION-CHECKPOINT §7.10 + STEP1-design-space + STEP1-DISPOSITION + STEP2-practical-decisions + MINI-SPEC + STEP4-gates-and-L-tier)
status: complete
---

# audit-findings-B.md — Phase D Entry Audit (Same-Vendor)

## §0. Summary

**Auditor.** Same-vendor adversarial-auditor (Claude Opus 4.7), xhigh reasoning, independent mode, fresh session.

**Class breakdown.** 3 Class A (addendum-shape) / 3 Class B (revision-shape) / 1 Class C (re-architect-shape). Plus 4 negative-space items.

**Headline.** The corpus is largely well-disciplined: rendered transparency at every artifact's "audit-priority risks" section is genuine, the gate/checklist completion is verifiable not performative, and channel-separation (H5) + categorization (M5) + falsifier (H4) amendments materially improve the dispatch contract beyond what §7.9.3 required. Two real problems land:

1. **An apparent substrate-confusion drop.** STEP1-design-space.md drops "gsdr-side shapes" (B/C from initial proposal) on the grounds that "gsdr lives on Claude Code; gsd-2 has its own runtime." But the M2 probe explicitly identifies `/gsdr:deliberate` as the **decisive structural overlap** with decision-trace semantics — "arguably IS a decision-trace skill, just not labeled that way" (M2 §3 / §0). Excluding the gsdr-side shapes is *defensible* (R-strategy + repo-of-residence are different from *prior-art comparison*), but the corpus operationalizes the exclusion in a way that quietly drops the strongest existing-primitive overlap from the gap-mapping work. This is the largest design-framing-quality risk in the corpus and the only Class C finding.

2. **Test-task selection compounds D5a inheritance rather than discharging it.** The mini-spec selects the 2026-04-28 framing-widening deliberation as primary test task, with the 2026-04-29 incubation-checkpoint as backup, and a synthetic counter-task only for B5 differentiation. Both candidate primaries are deeply Logan+Claude co-produced *with the very framing the skill will read back*. The mini-spec acknowledges this (§9 #6) but does not act on it: there is no mechanism that prevents Phase D evidence on B1-B4 from being a measurement of "skill agrees with its drafters' framings." Class B.

**Non-binding overall disposition signal.** **Addendum-shape with one targeted revision.** F-PD-B1 (substrate-confusion drop) wants targeted revision (a paragraph in STEP1-design-space §1.3 + a row in MINI-SPEC §2.2 B5 acknowledging the gsdr prior-art comparison without restoring the dropped shapes). F-PD-B2 (test-task D5a) wants a small mini-spec amendment (a non-co-produced control task added to the §2.3 task set). The remaining findings are addendum-shape. **Phase D dispatch is not blocked**, but the two B-class items want resolution before EXECUTION-LOG.md begins recording evidence, because the framing they fix is what FINDINGS.md will be read against.

The corpus's strongest landed discipline is the M5 categorization rule with inline EXECUTION-LOG examples (MINI-SPEC §8.4) — a discipline-shape that approaches a built-in mechanism through its operationalization at decision-time, not just at FINDINGS.md drafting time.

## §1. Methodology applied

**Read in full:**
- AUDIT-SPEC.md (audit's own contract).
- The 6-artifact corpus: INCUBATION-CHECKPOINT §7.10, STEP1-design-space, STEP1-DISPOSITION, STEP2-practical-decisions, MINI-SPEC, STEP4-gates-and-L-tier.
- Upstream grounding: P5 findings (full §0-§7), M2 findings (full §0-§8), RELATIONSHIP-TO-PARENT (full).
- Trajectory plan §1.4 (Phase D goal) and §2.4 row D (audit shape) verbatim.
- Spot-checks: framing-widening structure outline; INITIATIVE.md substrate framing.

**Not read (independent-mode discipline):** premise-bleed audit folder; trajectory-plan audit folder; incubation-checkpoint audit folder; relationship-to-parent audit folder; cross-vendor audit-findings-A.md (does not exist yet from my position; reserved for differential).

**Time budget.** ~2.5h wall-clock. Most time on STEP1-design-space (R-strategy claims + composition table + the gsdr-drop reasoning) and MINI-SPEC §1-§8 (the dispatch contract is where evidence-load lives or fails). STEP4 read quickly because gates 1+2+4 reaffirmed Step 1+2 dispositions; the L-tier sweep took focused reading because L4/L6 are precisely the kind of recursive material a same-vendor audit should pressure-test.

**Lens emphasis.** Per dispatch instructions: integration-grammar-as-fact at meta-level; methodological-discipline-leak (declared rule vs built-in mechanism); co-production-laundering at /effort max → /effort xhigh sequence; skill-heuristic shallow-match recurrence (Stack D foreclosure pattern at design level). Negative-space lens applied across the whole corpus.

## §2. Findings

### F-PD-B1 — gsdr-drop operationalization removes the corpus's strongest prior-art comparator

- **Class.** C (re-architect-shape, narrow).
- **Confidence.** High.
- **Lens.** Design-framing-quality + framing-leak.
- **Where.** STEP1-design-space.md frontmatter `authoring_discipline` (lines 19-25), §1.2 `What this Step 1 artifact does NOT do` bullet 4-5 (lines 79-80), §1.3 inventory table row "`~/.gsd/knowledge/signals/*` ... EXCLUDED from gap-mapping — gsdr substrate, not gsd-2" (line 100), §7 Logan-correction reference (lines 406-408). Read against M2-codebase-snapshot-findings.md §0 (lines 13-15) + §3.A (lines 138-146) + §3 closing block (lines 161-169).

- **What.** STEP1-design-space drops the gsdr-side shapes (the "B/C from initial proposal" — slash-command at `~/.claude/commands/gsdr/decision-trace.md`; extension of `/gsdr:deliberate`) on the grounds that gsdr is "a separate project from gsd-2 uplift." That R-strategy framing is correct: a slash-command in `get-shit-done-reflect` is R-strategy-orthogonal to gsd-2 work. But M2 §0 + §3 establishes a *separate* claim that the corpus does not surface: **`/gsdr:deliberate` is the decisive structural overlap with decision-trace semantics** — "arguably IS a decision-trace skill, just not labeled that way" (M2 §0 closing sentences) — implementing exactly the trigger taxonomy + severe-testing + falsifiable predictions + evaluation-status lifecycle the proposed decision-trace skill is supposed to handle (M2 §3 first overlap entry).

  STEP1-design-space §1.3 inventory acknowledges `forensics` as "the closest existing structural analog to 'decision-trace'" within gsd-2-internal — but `forensics` is M2's *2nd-tier* overlap candidate, behind `/gsdr:deliberate` in §3 ("In rough order of overlap depth, by binding evidence: 1. `/gsdr:deliberate` (decisive overlap)"). The reframe from "1st-tier overlap is `/gsdr:deliberate` per M2" to "1st-tier overlap is `forensics` per Step 1" happens silently when gsdr-side shapes are dropped on R-strategy grounds.

- **Why.** Three grounds:

  1. **Stated end-goal.** The Phase D dispatch contract requires "B5 forensics-vs-decision-trace differentiation" (MINI-SPEC §2.2 + §6.1 #5 falsifier). But `/gsdr:deliberate` is the *more dangerous* overlap by M2's evidence: it does what decision-trace claims to do, on the same artifact-class (`.planning/deliberations/`), with predictions + evaluation lifecycle that decision-trace's B4 test depends on the existence of (MINI-SPEC §2.2 B4: "if any deliberation has predictions in `evaluation_trigger`-shape"). The mini-spec tests differentiation against the wrong analog. (Note: an unverified-but-named **internal `gsd:audit-milestone`** is also flagged as adjacent; M2 §8 #2 "Relationship between the gsd-2 internal `/gsd:*` commands and `get-shit-done-reflect`'s `/gsdr:*` commands... was not investigated" — a separate small gap.)

  2. **Methodology discipline.** Per §0.6 failure-mode taxonomy + the corpus's own §7.10 H3 ("existing-primitives unmapped"), gap-mapping discipline requires comparison against the strongest analog, not the strongest *available-shape-eligible* analog. Restricting analog comparison to "primitives we'd consider building" silently shifts gap-mapping from "what already exists doing this work?" to "what already exists doing this work *that I might re-implement*?" The latter is reverse-engineered to license the chosen path.

  3. **Long-term vision (RELATIONSHIP-TO-PARENT.md §1).** "Whether and how to uplift [gsd-2]" — the substrate is "gsd-2 + Claude Code runtime + dev tooling + organizational conventions" *jointly*, not gsd-2 source code in isolation. Excluding gsdr-shaped artifacts from gap-mapping cuts against this scoping. Phase E reads "did decision-trace's substrate-shape evidence justify building in-tree alongside an existing slash-command-shape primitive?" — and Phase D evidence cannot answer that if the comparator was excluded at Step 1.

- **What would dissolve this.** A counter-argument that the gsdr-drop happened at *substrate-of-residence* level (correct R-strategy framing) AND that prior-art comparison happens *separately* in the gap-mapping — and the corpus already does that comparison. I checked: it doesn't. STEP1-design-space §3.A through §3.G compares each candidate against `forensics`/`spike-wrap-up`/`design-an-interface`/`write-milestone-brief`/`handoff`/`review`/`.gsd/DECISIONS.md`/workflow templates — never against `/gsdr:deliberate`. STEP1-design-space §1.3 inventory ends with a row explicitly **excluding** `~/.gsd/knowledge/signals/*` from gap-mapping as "gsdr substrate, not gsd-2." STEP1-DISPOSITION §3.A challenges/defenses table line 4 ("M2's primitive sampling may have missed an in-tree `deliberate` analog") explicitly checks for in-tree `deliberate` and answers "no" — but that's not what M2 found; M2 found a `/gsdr:deliberate` *in `~/.claude/commands/gsdr/`*, which the corpus has chosen not to read as analog. The defense is structurally aware of the question and structurally answers a different question.

  Alternatively: an argument that prior-art comparison against gsdr is non-load-bearing because gsd-2 cannot consume gsdr's slash-commands at runtime, so the comparison would be acausal. This is partly true (gsd-2 has its own runtime) but doesn't dissolve the finding: it dissolves the *replacement* question, not the *coverage* question. Phase D evidence on "does decision-trace work as in-tree skill?" should be read against the prior "what shape does the work already have, in what runtime?" — and `/gsdr:deliberate` in Claude Code runtime is the answer that the corpus systematically excludes.

- **Suggested improvement direction.** Targeted revision (not re-architect of dispositions): one paragraph in STEP1-design-space §1.3 explicitly preserving `/gsdr:deliberate` as **prior-art-not-candidate-shape**, with the acausal-runtime grounds spelled out — and one row in MINI-SPEC §2.2 differentiation tests adding "B5b: differentiation from `/gsdr:deliberate`'s deliberation-shape" alongside B5's forensics differentiation. This preserves the Phase D dispatch decisions (E primary + A comparator) while restoring the gap-mapping discipline. Logan + Claude's choice; my role is to surface that the gap exists.

### F-PD-B2 — Test-task selection inherits the framings the skill is meant to reconstruct

- **Class.** B (revision-shape).
- **Confidence.** High.
- **Lens.** D5a leak + evidence-load.
- **Where.** MINI-SPEC.md §2.3 (lines 132-146) — "Test task: Reconstruct rationale chain for the **2026-04-28 framing-widening deliberation**"; backup is "2026-04-29 incubation-checkpoint disposition"; counter-task only fires for B5 (synthetic auto-mode-failure). MINI-SPEC §9 #6 acknowledges the risk; STEP2-practical-decisions §3 #4 acknowledges. The acknowledgments are not operationalized.

- **What.** Both candidate primary test tasks are Claude+Logan co-produced under the same in-session-collaboration that produced the Phase D entry corpus itself. Decision-trace tested on framing-widening reads R1-R5 design-space + six-context plurality + four-act plurality + project-anchoring — *the exact integration grammar* INCUBATION-CHECKPOINT §0.2 + §7.1 reading-frame flagged as "Logan-imported inputs, loose-able if overfit, NOT observed facts in gsd-2." The same Claude that wrote the deliberation will be authoring the skill; the same Logan will be reading the trace artifacts. The test cannot distinguish:

  - "Skill correctly reconstructed the rationale chain" (the success claim) from
  - "Skill agrees with the rationale chain its authors wrote" (the D5a-confounded outcome).

  The mini-spec's §2.3 rationale defense ("test surfaces whether decision-trace reconstruction can preserve the in-session-collaboration trail vs erasing it") inverts the failure mode: preserving the trail is the easy property; the hard property is whether the reconstruction would land *the same way* on a deliberation the reconstructor didn't write.

- **Why.** Three grounds:

  1. **Stated end-goal (MINI-SPEC §4 success criteria).** "B1-B5 pass" is the success condition for B-behaviors. B1 ("read existing DECISIONS.md") + B2 ("cross-reference activity/journal") + B3 ("layer attribution") are testable on co-produced artifacts. B4 ("falsifiable predictions surfacing") is the contested one — and the mini-spec hedges B4 as "where applicable," conditional on whether deliberations have prediction structure. On framing-widening: §9 deferred items act as predictions per the mini-spec's reading. But Claude wrote those deferred items knowing the §9 structure; the skill (also Claude-authored) reading them back is reading author-intent, not extracting predictions from artifact-evidence. The B4 evidence is corrupted by co-authorship.

  2. **Methodology discipline (foundation-audit METHODOLOGY + §0.5 disposition-discipline).** The discipline is "calibrated language; pre-registered thresholds; model verification." Pre-registered thresholds are absent here: the mini-spec specifies pass conditions at behavior level (file:line refs cited; no fabrication; layer attribution annotations present) but not at *content* level (what would a wrong reconstruction look like?). On a co-produced deliberation, "agreement" is the easy outcome; on a non-co-produced deliberation, "agreement" requires the skill to reach the actual structure. The test-task selection eliminates the harder check.

  3. **Risk to delivery.** Phase E reads Phase D evidence under H5 channel separation (MINI-SPEC §7). Channel-(b) substrate-shape claims of the form "gsd-2's skill subsystem supports reconstruction-shaped semantics" require the channel-(a) evidence to actually be evidence — not author-agreement. If Phase D produces "decision-trace successfully reconstructed framing-widening" and Phase E asks "is this substrate-shape-licensable?", Phase E auditor (per plan §1.5 step 2) reads the evidence chain and finds the test target was Claude-authored. The H5 discipline catches it at Phase E rather than Phase D, but the cost is a Phase E re-disposition cycle.

- **What would dissolve this.** A demonstration that the test-task includes *content checks* that adversarially probe the reconstruction (e.g., "skill must surface alternatives the deliberation considered but rejected; reconstruction reads as adequate iff a third-party reading of the artifact agrees on which alternative was chosen and why"). The mini-spec's §4 success criteria item 6 ("FINDINGS.md reads against the dispositions") gestures toward this but doesn't operationalize: "did the E-primary disposition hold?" is FINDINGS-level evidence, not test-task content evidence.

  Alternatively: a demonstration that the framing-widening deliberation has enough internal-self-correction structure that Claude reading-back is meaningfully different from Claude writing-forward (e.g., the §9 deferred items contain predictions that Claude-the-author *did not have access to verify at write time*; a successful reconstruction would surface which predictions resolved and which haven't). The §9 deferred items are mostly forward-looking (Phase D, Phase E triggers), so resolution-status-now is mostly "deferred" or "active" — which doesn't exercise B4 falsifiability.

- **Suggested improvement direction.** A small mini-spec amendment to §2.3: keep framing-widening as the *capacity* test (does the skill even handle a deliberation of this shape?), but add a non-co-produced primary task — either a non-Claude-authored deliberation in the project (DECISION-SPACE.md §1.x dispositions might qualify if any are genuinely Logan-only-authored), a deliberation from another project (philograph-mcp / scholardoc / philo-rag-simple if any have decision logs in a similar shape), or a synthetic deliberation Logan or a third agent constructs *for adversarial purposes*. The synthetic counter-task already exists for B5; extend the same construction discipline to B1-B4. The "test on a real task" defense in STEP2-practical-decisions §2.M4 ("real tasks test whether the skill's shape fits work shapes the skill didn't anticipate") only holds if the real task has shape the skill author didn't anticipate — which co-produced deliberations don't.

### F-PD-B3 — H5 channel-separation discipline is declared rule, not built-in mechanism — and the discipline is co-production-corrected

- **Class.** B (revision-shape).
- **Confidence.** Medium-high.
- **Lens.** Methodological-discipline-leak.
- **Where.** MINI-SPEC.md §7 (lines 246-272) channel-separation discipline; §9 #4 acknowledges "channel-separation discipline is a declared rule, not a built-in mechanism. If the executor (or Claude during execution) accidentally violates the rule at FINDINGS.md drafting, only the audit catches." The acknowledgment is honest but does not act on itself.

- **What.** §7 specifies a per-claim audit at FINDINGS.md drafting time: each load-bearing claim labeled `(a)` / `(b)` / `(a→b)`. The discipline is *enforced by the auditor reading FINDINGS.md*, not by anything FINDINGS.md itself does. This means: (i) the EXECUTION-LOG.md draft does not yet need labels (§7.3 specifies "Per-claim audit at FINDINGS.md drafting time"); (ii) the FINDINGS.md author (Claude in-session-collaboration with Logan; same authors as the rest of the corpus) labels the claims; (iii) the Phase D entry stability audit per plan §1.5 reads the labels.

  The cycle: Claude writes evidence → Claude labels evidence → audit reads labels-plus-evidence. If Claude during FINDINGS.md drafting unconsciously bridges (a)→(b) by labeling a substrate-shape claim as `(a→b)` with weakly anchored bridge-prose, the labels themselves are co-produced under the same D5a inheritance the rest of the corpus is. The mini-spec's mitigation ("any unlabeled claim or any `(a→b)` without explicit bridge fails the audit") is a discipline at the auditor's reading, not a mechanism at FINDINGS.md's structure.

- **Why.**

  1. **Stated end-goal (RELATIONSHIP-TO-PARENT.md §2 failure-mode 1).** The exact failure being prevented is "projection from test-case-anchored evidence to substrate-shape-anchoring is weakly licensed." The convergent C1 finding from premise-bleed audit was this exact pattern materializing in disposition reasoning-trace. The mini-spec §7.4 cites this — and its mitigation is "Per-claim audit at FINDINGS.md drafting time." But the audit reads the same FINDINGS.md draft co-produced under the same in-session-collaboration that produced disposition reasoning-trace. The mitigation is one rotation of the same wheel, not a different mechanism.

  2. **Methodology discipline.** A "built-in mechanism" alternative would look like: EXECUTION-LOG.md captures evidence with provisional channel-tag at observation-time (per §8.4 inline-discipline pattern, which already exists for M5 categorization), and FINDINGS.md *inherits the provisional tags* rather than re-labeling. The labels then live closer to the evidence-source, harder to drift in synthesis. This is a small operational shift, not a re-architect — but the mini-spec doesn't make it.

  3. **Risk to delivery.** If Phase D produces 9 falsifier-discriminating, well-tagged-on-paper evidence claims and Phase E auditor reads the labels and accepts them, but a fresh-session Phase F re-read finds that a (b) claim was actually a (a) with a confident-sounding bridge — the failure is structurally identical to the premise-bleed audit-arc's convergent C1, surfacing two phases later than at Phase D dispatch. The cost compounds.

- **What would dissolve this.** A demonstration that channel labels are anchored to *something the FINDINGS.md author cannot un-make*. If Phase D's evidence base is canonical (e.g., EXECUTION-LOG entries with timestamp + observation; tagged at observation; the FINDINGS.md author can summarize but not relabel), the mechanism approaches built-in. The mini-spec is one §8.4-style amendment away from this; it just doesn't have it.

  Alternatively: an argument that the same-vendor independent paired audit at this Phase D entry IS the structural correction *for* §7's discipline — and the same paired audit fires again at Phase E re-read time. This is true but circular: the audit catches at Phase D entry (now) and then can be expected to catch again at Phase E. It does not catch at FINDINGS.md authoring time, which is the load-bearing surface for the substrate-shape claims being made. Two audits before Phase E is not the same as a built-in mechanism between observation and synthesis.

- **Suggested improvement direction.** One §8.4-style operational addition to §7.3: "EXECUTION-LOG.md inline-tags channel-(a)/(b)/(a→b) at observation-time using the same inline-discipline pattern as §8.4 M5 categorization. FINDINGS.md inherits inline tags; relabeling requires explicit reasoning at FINDINGS.md draft." This is a small revision; it would dissolve much of the finding's force.

### F-PD-B4 — Stack D foreclosure pattern applied at design level reads as principled but is shallow-pattern-match-shaped

- **Class.** A (addendum-shape).
- **Confidence.** Medium.
- **Lens.** Skill-heuristic shallow-match recurrence at design level.
- **Where.** STEP1-DISPOSITION.md §2.A reasoning chain item 5 (lines 78-79): "CLAUDE.md 'Stack D foreclosed' pattern applies recursively at Phase D scoping. 'The maximalist Stack D... is foreclosed because it commits compute and complexity that v0.x has no evidence to justify; the trajectory remains open if v0.3+ evidence warrants reopening' — the project-level discipline applies to D's bundling: schema-versioning + new skill + 4-5 skill modifications. Trajectory remains open to D at Phase E if E's evidence licenses it." Reaffirmed at §3.A challenges-table line 1 defense.

- **What.** The CLAUDE.md "Stack D foreclosed" line refers to a specific architectural decision in arxiv-sanity-mcp's product trajectory — a maximalist stack that "commits compute and complexity that v0.x has no evidence to justify." The disposition reaches for that pattern as license to choose Shape E over Shape D in Phase D scoping. The structural similarity is real (both are "this is more than the current evidence justifies"), but the dispositional weight the disposition puts on the analogy is shallow: the ground for choosing E over D in Phase D should be Phase-D-internal (E's coordination cost; D's schema-versioning bundling), not "this looks like the Stack D pattern from the codebase."

  The challenge-table at §3.A line 1 ("Why not D? Tests more surfaces.") defense reads: "D bundles schema-versioning convention claim with decision-trace skill claim — Phase E can't separate them cleanly. Foreclosure pattern from CLAUDE.md applies recursively." Item 1 of the defense (bundling argument) is the actual ground; item 2 (foreclosure pattern) is rhetorical reinforcement. The disposition structure does the load-bearing work in item 1; item 2 is legitimating-by-analogy, which is the shallow-match pattern the §0.6 failure-mode taxonomy specifically flags.

- **Why.**

  1. **Stated end-goal.** STEP1-DISPOSITION's role is to record "auditable reasoning trail" so that Phase D entry audit can pressure-test the disposition. Reasoning-by-analogy is harder to pressure-test than reasoning-from-evidence: the analog can always be denied or re-analogized. The disposition's actual ground (D's schema-versioning bundling raises Phase E disentanglement cost) is fine; the "foreclosure pattern applies" sentence weakens auditability rather than strengthening it.

  2. **Methodology discipline.** Per spike-program METHODOLOGY's six lenses (Bayesian / Standpoint / Paradigm / Mechanistic / Values / Duhem-Quine) + foundation-audit's calibrated-language discipline: pattern-match across artifact-classes is Paradigm-lens move; load-bearing dispositions should be Mechanistic-lens (what specifically does D do that E doesn't?) backed by Bayesian (what evidence-yield differs?). The disposition reasoning is mostly Mechanistic + Bayesian; item 5 leaks Paradigm-lens analogizing where it isn't needed.

- **What would dissolve this.** A reading of item 5 as "rhetorical compression of items 1-4" rather than independent-load-bearing reasoning. Plausible: the items are numbered in a list, and item 5 starts "applies recursively" which signals analogy not new ground. Under that reading the finding is taste, not substance. I'm leaving it as Class A rather than dropping for two reasons: (i) §3.A defense table also leans on the analogy as "foreclosure pattern from CLAUDE.md applies recursively" without restating items 1-4 — the analogy travels separately; (ii) STEP1-DISPOSITION §5 #2 ("E-vs-D weighing may under-weight schema-versioning evidence yield. D's substrate-shape coverage is broader. The 'Stack D foreclosed pattern applies recursively' argument is a real principle but applying it at Phase D scoping is itself Claude-imported reading; defensible counter exists.") explicitly flags this risk. The acknowledgment is genuine; my finding extends it from acknowledgment to "this shows up as a load-bearing argument fragment, not just a residual risk."

- **Suggested improvement direction.** Single-sentence amendment in STEP1-DISPOSITION.md §2.A item 5 reframing: "Item 5 is rhetorical reinforcement; the disposition rests on items 1-4. Phase D entry audit can disregard item 5 if it does not add ground beyond items 1-4." This kind of footnote is what the corpus already does well at audit-priority risk sections; extending it to load-bearing reasoning items would tighten auditability. Class A because the disposition is defensible without item 5.

### F-PD-B5 — /effort max → /effort xhigh sequence as recorded does not constitute independent-disposition-evidence

- **Class.** A (addendum-shape).
- **Confidence.** Medium.
- **Lens.** Co-production-laundering.
- **Where.** STEP1-DISPOSITION.md `authoring_discipline` (lines 13-22), §1 disposition table footer (line 61), §5 #6 (lines 182-183): "/effort max → /effort xhigh sequence is part of the auditable trail. Claude's surfacing was performed at maximum reasoning effort; Logan's accept-as-stated was given at xhigh after surfacing. The accept happened under conditions where Logan had access to Claude's full reasoning surface; it was not a rubber-stamp under bounded reasoning. Auditor reads this as evidence-of-deliberate-acceptance, not evidence-of-cleared-quality (Logan's accept does not substitute for Phase D entry audit)."

- **What.** §5 #6 is honest about what the sequence is and isn't: it records that Logan accepted under conditions of access to Claude's full reasoning, and explicitly disclaims that the accept is a quality-clearance. Good. The risk that remains: the framing "Claude surfaced at max + Logan accepted at xhigh" can read, in Phase E re-reads, as a *quasi-procedural authentication* of the disposition — "we did the high-effort surfacing-then-acceptance ritual, therefore the disposition is well-grounded." The disclaimer in §5 #6 is one paragraph among 5 acknowledged risks; the framing of "auditable trail" recurs across the disposition + STEP2 + STEP4 frontmatters as if the sequence itself does evidentiary work.

  The specific recurrence: STEP2-practical-decisions.md `authoring_discipline` (lines 16-22) cites "Logan green-lit Step 2 dispatch at /effort xhigh turn 2026-04-30 immediately following STEP1-DISPOSITION.md accept-as-stated" — and STEP4 `status` block similarly cites green-light. The sequence becomes part of the artifacts' provenance-of-authority, which is exactly the laundering shape: not "Logan accepted Step 1, therefore Step 2 dispatch is licensed" (procedural license, fine) but "Logan accepted Step 1 at xhigh after Claude surfaced at max, therefore the *content* of Step 2 inherits authoritative grounding."

- **Why.**

  1. **Stated end-goal.** §5 #6's own framing is correct: the sequence is evidence-of-deliberate-acceptance, not evidence-of-cleared-quality. The audit-trail discipline is for procedural traceability; not for disposition authority.

  2. **Methodology discipline.** Per §0.5 disposition-discipline + traces-over-erasure (feedback_methodology_and_philosophy): preservation of the trail is correct; promotion of the trail to authority-substitute is the failure mode. The line is fine — recording "Logan accepted at /effort xhigh after Claude surfaced at /effort max" is traces-over-erasure. The risk is a downstream-reader interpretation, not a current-corpus claim.

- **What would dissolve this.** A reading of the corpus's many citations of the /effort max → /effort xhigh sequence as procedural-traceability, not authority-claim. Plausible: every citation is in a frontmatter `authoring_discipline` or `status` block, not in a substantive reasoning bullet. Under that reading the finding is taste — the sequence-citation is procedural, not substantive.

  I am leaving as Class A because: (i) the corpus is read by future-Claude in fresh sessions, and frontmatter `status` blocks are exactly what fresh-session readers consult for provenance; (ii) the same sequence is cited in MINI-SPEC.md `status` (lines 7-14) which describes itself as "the Phase D dispatch contract," and Phase D dispatch is exactly the surface where authority-claims have downstream effect. The risk is mild; the disclaimer in §5 #6 already mitigates substantially. Addendum-shape, not revision-shape.

- **Suggested improvement direction.** A standing-clarification at the top of STEP1-DISPOSITION.md §0 (or at MINI-SPEC.md §0): "References to /effort max → /effort xhigh sequence in this corpus's provenance blocks are procedural-traceability records, not disposition-authority claims. Phase D entry audit + Phase E stability test are the substantive quality gates; Logan's /effort xhigh acceptance authorizes proceeding with the work-flow, it does not certify the disposition's correctness." One sentence in one place, cross-referenced where the sequence recurs. The corpus already does similar standing-clarifications (the D5a recursion acknowledgments at every artifact's frontmatter); adding this one is consistent with that discipline.

### F-PD-B6 — H/M/L tier framing recurs as if-observed at the §7.10 → corpus boundary

- **Class.** A (addendum-shape).
- **Confidence.** Medium.
- **Lens.** Integration-grammar-as-fact at meta-level.
- **Where.** INCUBATION-CHECKPOINT.md §7.10.0 acknowledges "tiers are non-binding signal; Logan's calibration governs" (line 592). §7.10.6 acknowledges "Integration-grammar-as-fact recurrence risk at §7.10 layer" (line 710). STEP4-gates-and-L-tier.md §2 sweep (lines 73-125) — each L-item is treated as a distinct concern with its own status assignment.

- **What.** §7.10.0 + §7.10.6 disclaim H/M/L as observed taxonomy. STEP4 §2 then uses the L1-L8 enumeration as a checklist with status-per-L-item. The L1-L8 organizing structure is treated *as if* it carved the negative-space at meaningful joints — each L gets its own status, its own "addressed/recorded/operationalized" designation. The §7.10.6 acknowledgment was that the tier-claims could function as fact; the STEP4 sweep operationalizes them as fact in checklist-form, sweeping each Li in turn.

  Specifically: L4 ("this-planning-session-as-substrate-evidence") and L6 ("substrate primitives during Phase D design — recursivity") are arguably the same observation under different framings: substrate-evidence inheres in this session because this session is using substrate primitives. Treating them as separate L-items in the sweep produces "L4 addressed; L6 acknowledged" status — two boxes ticked for one underlying observation. L1 ("skill-heuristic shallow-match risk") and L8 ("dispatch-readiness-resolution audit shape") are similarly framing-orthogonal — could equally well have been combined or split differently. The sweep doesn't surface this; it processes the enumeration as given.

- **Why.**

  1. **Methodology discipline (§0.6 failure-mode taxonomy + the corpus's own §7.10.6 acknowledgment).** The risk is named correctly: tier-claims functioning as fact rather than as Claude's organizing-frame. STEP4 §2 sweep is the surface where the risk would materialize; the sweep does not check whether the L-items still carve the space at meaningful joints once they're being checklisted.

  2. **Risk to delivery.** Phase E reads STEP4 §2 sweep as "Phase D entry handled L1-L8." If L4 and L6 are the same observation, the sweep over-claims coverage; if L1 absorbs into L8, the sweep over-counts checklist items. Phase F readiness gate reads checklist completion; over-counting compounds.

- **What would dissolve this.** Either (i) demonstrating that L1-L8 carve at distinct joints (e.g., L4 is about *this* session's planning-quality-as-evidence; L6 is about *Phase D execution* using substrate-primitives) — plausibly so for that specific pair, but the pattern of "treat enumeration as the unit of analysis" applies across the sweep regardless. Or (ii) reframing STEP4 §2 not as "sweep through L1-L8" but as "address the underlying concerns L1-L8 surface" — the difference is whether the sweep is enumeration-bound or concern-bound. The current §2 prose is closer to the former.

- **Suggested improvement direction.** A single sentence in STEP4 §2's preamble: "L1-L8 are the §7.10 enumeration; the sweep addresses the concerns each L surfaces, but L-items are not assumed orthogonal. Where two L-items converge on one concern, the sweep notes the convergence rather than registering both as 'addressed.'" This preserves the sweep's traceability to §7.10 while loosening the integration-grammar-as-fact recurrence. Addendum-shape, low-cost.

### F-PD-B7 — STEP4 checklist 18/20 completion claim conflates artifact-existence with discipline-completion

- **Class.** A (addendum-shape).
- **Confidence.** Medium.
- **Lens.** Methodological-discipline-leak.
- **Where.** STEP4-gates-and-L-tier.md §3 (lines 127-152): the 20-item completion checklist; §4 #3 acknowledges: "Checklist completion claim (18/20) is artifact-existence, not artifact-quality. All 20 items have artifacts pointing to them; whether the artifacts adequately address the items is what Step 5 audit decides."

- **What.** §4 #3 is honest. The risk that remains: checklists travel forward into Phase E + Phase F readiness gates as evidence-of-completion. A future-session reader (per CLAUDE.md governance read-order map: "Agent starting a session" → STATE.md → relevant phase plan) sees "18/20 complete" and reads it as "Phase D entry passed 18 of 20 disciplines." But the discipline is "executor confirms" per the checklist's own language (§7.10.5); the §3 table flips "executor confirms" to "checklist item has an artifact." Subtly different.

  The shape of the conflation: §7.10.5 said "[ ] Pre-D parallel probes fired (P5 + codebase-snapshot); outputs read." STEP4 §3 row 1 says "✅ | `pre-D-probes/P5-effective-state-emission-findings.md` + `pre-D-probes/M2-codebase-snapshot-findings.md`." The check went from "outputs read" (a discipline) to "outputs exist" (an artifact-listing). For most rows this is fine — the executor implicitly read the outputs to draft the next artifact — but row 11 ("H4 falsification criteria drafted") and row 13 ("M5 per-decision rule drafted") are exactly the rows where draft-quality is the audit-priority concern, and the checklist treats them as artifact-existence too.

- **Why.**

  1. **Stated end-goal.** Phase D entry audit (this audit) IS what closes the artifact-existence vs discipline-completion gap. §4 #3's acknowledgment recognizes this. The risk is downstream: Phase E reads "18/20 complete" plus this audit's findings; Phase F readiness gate reads similarly. Each phase's reader has progressively less context for the conflation.

  2. **Risk to delivery.** Mild — the audit catches now. The finding is Class A because the corpus already has the right disclaimer; my role is to surface that the disclaimer travels less far than the checklist does.

- **What would dissolve this.** A reading of §3 as "completion = artifact-exists + frontmatter-cites-it" (which is what it actually says) and trust that downstream readers consult §4 #3's caveat. Plausible if §3 + §4 always travel together; less plausible if checklist-snippets get extracted into STATE.md or summary readouts.

- **Suggested improvement direction.** Reframe §3's "Checklist completion: 18/20 items complete" to "Checklist artifact-presence: 18/20 items have artifacts (Step 5 audit reads artifact-quality)." Single-line change. Addendum-shape.

## §3. Negative-space catalogue

The corpus's §7.10.6 + §4.5 + §5 risk-acknowledgments are genuine and substantial. The audit reads them as prioritized challenge surfaces, not as completed self-audit. Items below are exclusions the corpus does not surface OR principal-exclusions whose justification I want to test.

**N1 — `gsd:audit-milestone` and the gsd-2 internal `/gsd:*` command surface (vs gsdr's `/gsdr:*`).** M2 §8 #2 explicitly flags: "Relationship between the gsd-2 internal `/gsd:*` commands and `get-shit-done-reflect`'s `/gsdr:*` commands... was not investigated. The gsd-2 codebase contains `commands/` (e.g., `commands-bootstrap.ts`, `commands-handlers.ts`) referencing GSD-WORKFLOW.md." The corpus reads "in-tree" and "user-side" as the binary; the M2 finding suggests there's an in-tree command surface (`/gsd:*`) that the gap-mapping does not engage. If `/gsd:audit-milestone` exists in gsd-2-explore and is structurally relevant to decision-trace, Shape E is comparing "new in-tree skill" against an inventory missing one in-tree analog category. STEP1-design-space §1.3 inventory does not include any `/gsd:*` row. Bounded-coverage gap that the corpus does not surface (M2 §8 #2 surfaces it; corpus does not import).

**N2 — Heal-skill / skill-health subsystem implications.** STEP2 §2.M4 puts heal-skill out-of-scope ("M2 §8 open question 3; flagged for Phase E"). M2 §8 #3 + §8 #10 surface that heal-skill writes to `.gsd/skill-review-queue.md` and is part of the per-unit post-analysis cycle. For a skill *whose entire purpose is reading past records* (decision-trace), the staleness and review-queue surfaces could be load-bearing for Phase D evidence: does the new decision-trace skill itself become subject to staleness deprioritization? Does the skill-review-queue produce decision-relevant outputs that decision-trace should read? The OOS scoping is defensible (Phase D shouldn't grow), but the OOS justification ("M2 §8 open question 3") is *under-developed* for Phase D evidence purposes — it's deferred without specifying what evidence at Phase E would warrant un-deferring.

**N3 — Cross-project decision-trace as principal exclusion.** STEP2 §2.M4 OOS "Cross-project decision-trace": "Per-project scope only at Phase D; cross-project surface is a different question." This is the right scoping decision — but it forecloses one of the cleaner test-task options (decision-trace from another project's deliberation, which would address F-PD-B2 D5a). The exclusion is principal, not negative-space-leak; flagging because it's load-bearing for the F-PD-B2 finding's improvement-direction.

**N4 — Validation-layer silent-drop hypothesis (P5 §7 #1).** P5 explicitly flags this as severity-amplifier — "If `validatePreferences()` silently drops unknown keys, that's a fourth drift vector below the merge pipeline. Worth a 15-min spot check at Phase D entry audit." STEP4 §1.2 pre-disposes P5 sub-option (ii) without addressing the spot-check P5 itself recommended. The spot-check is the smallest-possible Phase-D-entry-audit-time-defrag — a 15-minute extension to the M2 + P5 scope that would convert P5's "moderate" to either "moderate confirmed" or "severe." Doing it at Step 0 would have informed the disposition; not doing it at Step 5 leaves the severity-amplifier as a Phase-D-execution-time risk only catchable through MINI-SPEC §6.1 falsifier #8. Defensible deferral; flagging because the P5 author specifically requested it at Phase D entry audit time and the audit-time is now.

## §4. Synthesis

**Is the Phase D entry corpus dispatch-ready?** Yes, with two actionable revisions before EXECUTION-LOG.md begins:
1. F-PD-B1 (gsdr-drop) wants the prior-art comparison restored without restoring the dropped shape candidates. ~30-60 minutes of writing in two locations.
2. F-PD-B2 (test-task D5a) wants a non-co-produced primary task added to MINI-SPEC §2.3. ~30-60 minutes including selecting the alternative.

The remaining findings (B3 channel-discipline mechanism; B4 Stack D analogy; B5 /effort sequence; B6 H/M/L recurrence; B7 checklist conflation) are addendum-shape — quality improvements that don't block dispatch. F-PD-B3 (channel-discipline as declared rule) is the closest of the remaining to wanting attention; if Logan reads it as Class B I would not fight that disposition.

**Single biggest risk.** F-PD-B1: the corpus's strongest existing-primitive overlap (`/gsdr:deliberate`) is structurally excluded from gap-mapping. This is the kind of finding that compounds: Phase D evidence on "decision-trace skill works" cannot disentangle from "decision-trace as separate primitive was justified given an existing slash-command-shape primitive does almost the same work in adjacent runtime." Phase E re-read will catch this if Phase D doesn't address it; the cost of catching at Phase E is a re-disposition cycle.

**Single strongest discipline-move.** MINI-SPEC §8.4 M5 inline-discipline pattern. The pattern of capturing categorization at observation-time inside EXECUTION-LOG.md, with concrete example syntax, approaches a built-in mechanism. It's the model F-PD-B3 wants extended to channel-tags. The M5 operationalization is what the rest of the corpus's discipline-shapes should aspire to.

**Calibration check on this audit.** I converged with the corpus's transparency on B6 (H/M/L tier recurrence — flagged at §7.10.6) and B7 (checklist conflation — flagged at STEP4 §4 #3); diverged on B1 (gsdr-drop is not in the corpus's risk acknowledgments at all — checked STEP1-design-space §4.5, STEP1-DISPOSITION §5, MINI-SPEC §9, STEP4 §4) and B2 (mini-spec acknowledges the risk at §9 #6 but does not act on it). Convergent findings provide calibration evidence that the corpus's transparency-coverage is high; B1 in particular suggests the dropped substrate-class isn't visible from inside the dispositional reasoning, which is exactly the kind of meta-level integration-grammar-as-fact same-vendor audit is positioned to catch.

## §5. Non-binding overall disposition signal

**Addendum-shape with one targeted revision.**

- **Targeted revision (before Phase D dispatch):** F-PD-B1 + F-PD-B2 (the two B-class items). Revisions are local — STEP1-design-space §1.3 paragraph + MINI-SPEC §2.2 row + MINI-SPEC §2.3 task amendment. Both operationalize risks the corpus acknowledges (B2) or implicates without acknowledging (B1); neither requires re-disposing axes 1-4.

- **Addendum (can be a single AUDIT-DISPOSITION.md addendum at the corpus's audit folder, or in-frontmatter standing-clarifications):** F-PD-B3 (channel inline-tagging extension) + F-PD-B4 (Stack D analogy disclaimer) + F-PD-B5 (/effort sequence procedural-clarification) + F-PD-B6 (H/M/L sweep convergence-check) + F-PD-B7 (checklist artifact-presence reframe). All are small; total estimated cost ~30-60 minutes if batched.

- **Re-architect-shape findings:** none. F-PD-B1 was Class C in label but the suggested improvement direction is local revision, not re-architect. Logan can read F-PD-B1 as Class B with the local revision and I would not contest.

- **Phase D dispatch readiness conditional on:** the two targeted revisions landing as commits before EXECUTION-LOG.md begins, OR Logan-disposed acceptance of the findings as-known-risk with explicit decision recorded at AUDIT-DISPOSITION.md. Either pathway is procedurally clean; the corpus's discipline already includes "traces-over-erasure" so a "we read the audit, decided not to revise B1/B2 because [reason]" disposition is well-formed.

The corpus is closer to dispatch-ready than the AUDIT-SPEC.md's disposition options suggest is the typical paired-audit outcome at Phase D entry. The transparency-coverage at audit-priority-risk sections + the M5 operationalization + the gate/checklist verifiability are doing real work. The two B-class findings are the audit's value-add beyond the corpus's self-acknowledgment; addendum-shape findings tighten quality without blocking.
