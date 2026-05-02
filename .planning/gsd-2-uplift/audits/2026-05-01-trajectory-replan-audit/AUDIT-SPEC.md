---
type: trajectory-replan-audit-spec
date: 2026-05-01
status: draft-for-logan-disposition-before-audit-dispatch
target:
  artifact: .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md
  commit: ffc0fb0
  lines_at_commit: 842
scope: question-shape-fit + framing-inheritance-risk + recursive-failure-mode catch
spec_author: cross-vendor codex GPT-5.5 xhigh
spec_provenance:
  brief: .planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/SPEC-DRAFTING-BRIEF.md
  precedent: .planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md
disposition_owner: Logan
---

# (V'.a) Step 3 Trajectory-Replan Audit Spec

## §0. Read-guidance

This document specifies the audit to run on the (V'.a) Step 2 trajectory-plan
revision at commit `ffc0fb0`. It is an audit specification, not the audit
findings. Sections run: purpose (§1), scope (§2), execution (§3), lens questions
(§4), classification (§5), outputs (§6), disposition (§7), references (§8).

Treat this spec as execution authority. The Claude-authored
`SPEC-DRAFTING-BRIEF.md` is provenance, not a required audit input, unless Logan
explicitly asks an auditor to inspect spec-authoring provenance.

## §1. Purpose

### §1.1 Why this audit exists

The trajectory plan was revised after the 2026-04-30 methodology-question-shape
mismatch finding: Phase D changed from a single-target spike shape to a
mapping-shape substrate evidence phase; Phase E changed to a mapping-coherence
test; Phase F changed to a mapping-coherence plus intervention-feasibility gate.

The audit asks whether that revision actually solves the failure mode or merely
renames it.

The specific recursive risk is:

- Phase A audit checked the original trajectory plan under a plan-well-formedness
  scope.
- That audit did useful work, but it did not catch the Phase D
  methodology-question-shape mismatch.
- The miss matters because an audit scoped under the same misframe as the
  artifact can execute correctly and still fail to surface the misframe.
- Step 3 therefore audits not just plan quality but the shape of the question
  the plan thinks it is answering.

### §1.2 What this audit must be willing to conclude

The audit must be allowed to return any of these: mapping-shape is fit for
purpose; mapping-shape is broadly right but needs addenda; the revision remains
spike-shaped despite mapping vocabulary; mapping is incomplete or wrong; a
third or hybrid question-shape is needed; self-review is performative rather
than operational; or the spec-independence mitigation re-imported the same
frame.

Class C findings are allowed even if they restart the trajectory-replan cycle.
The audit's job is not to protect the revision from that outcome.

### §1.3 How this spec departs from the Claude drafting brief

This spec accepts the brief's required lens families but does not treat the
brief's frame as final. The following departures are intentional:

1. The audit treats "mapping" as a live candidate, not as the settled remedy.
   The plan's mapping vocabulary is itself under audit.
2. The 12 substrate-vision properties and the C1/C2/C3/C4 model are treated as
   imported scoping inputs, not as facts about gsd-2, arxiv-sanity-mcp, or the
   future substrate.
3. The Claude-authored drafting brief is not a default execution input for the
   auditors. The spec carries the lens questions directly so the audit does not
   need to reread a Claude scoping artifact to know what to check.
4. The audit includes evidence-type labels for findings. This is a
   cross-vendor-original addition: it prevents imported frames from becoming
   unmarked facts in the audit findings themselves.
5. The audit treats zero-C1 Phase F output as an unresolved gate-shape question,
   not merely as a plan edge case.
6. The audit explicitly checks whether "paired-default with Logan downgrade" is
   a real cost discipline or a disguised escape hatch from the very discipline
   the plan says is needed.

### §1.4 What this audit is not

This is not:

- A fresh codebase-understanding audit of gsd-2.
- A rewrite of the trajectory plan.
- An execution of Phase D mapping.
- A disposition of whether gsd-2-uplift should extract.
- A business, monetization, or harness-studio strategy review.

The audit can say the plan's shape is wrong. It should not draft the replacement
plan unless Logan later asks for that follow-up.

## §2. Scope And Inputs

### §2.1 Primary artifact under audit

Read the trajectory plan exactly as it existed at commit `ffc0fb0`:

```bash
git show ffc0fb0:.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md
```

The current working-tree copy may be identical, but the audit target is the
commit-pinned text. If the working tree differs, record the difference as a
scope note and audit `ffc0fb0`.

Special attention: header status; §0.5, §0.6, §0.8; Phase D/E/F/G (§1.4-§1.7);
paired audit and downgrade language (§2.3-§2.4); failure-mode matrix (§5.6);
verification checklists (§6); final caveat and self-review trace.

Also read the commit message body for `ffc0fb0`, because the self-review trace is
split between the final plan caveat and the commit body.

### §2.2 Required standing-context inputs

Read these before writing findings:

1. `.planning/deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md`
   - Full read. Ground for methodology mismatch, five frame revisions,
     Logan-disposition scope, audit-discipline limits, and closure pressure.
2. `.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md`
   - Full read. Treat as imported standing context, not observed fact. Focus:
     §0, §1, §3, §4, §5, §7.
3. `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md`
   - Full read. Ground for test-case-vs-substrate framing and
     stipulated-not-observed caveat.
4. `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md`
   and `DISPOSITION.md`
   - Full read. Use for output-shape precedent and what Phase A caught; do not
     treat Phase A scope as sufficient.
5. `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md`
   - Full read for spec and output-structure precedent.
6. `.planning/gsd-2-uplift/audits/2026-04-28-cross-vendor-codebase-understanding-audit/wave-3/META-SYNTHESIS.md`
   - Full read. Primary grounding for corrected gsd-2 vocabulary and surfaces.
7. `.planning/spikes/METHODOLOGY.md`
   - Full read, especially M1, calibrated register, pattern-watch, and
     model-verification.
8. `.planning/foundation-audit/METHODOLOGY.md`
   - Full read. Use evidence tracing, alternative evaluation, sensitivity
     analysis, and inference-chain integrity.

### §2.3 Optional targeted inputs

The auditor may use these if a finding requires them:

- `.planning/LONG-ARC.md` for anti-pattern source lines named in `AGENTS.md`.
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §7.1 if the
  auditor needs the original "useful inputs, not observed facts" discipline.
- `.planning/gsd-2-uplift/audits/2026-04-30-phase-d-entry-audit/` if the
  auditor needs to confirm the prior audit scope that failed to catch the
  mismatch.
- Narrow reads of `/home/rookslog/workspace/projects/gsd-2-explore/` only when
  META-SYNTHESIS is insufficient to ground a concrete surface/mechanic claim.

For optional source reads, record the file count and cite file:line in the
finding. Do not conduct a new gsd-2 codebase audit.

### §2.4 Forbidden-reading list

Auditors should not read:

- The current conversation transcript.
- `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/.logs/`.
- Runtime mirrors under `/home/rookslog/.claude/plans/` or similar.
- Runtime memory files.
- `SPEC-DRAFTING-BRIEF.md`, unless Logan explicitly asks for a
  spec-provenance check.

Rationale: the future audit should be scoped by this spec and the committed
artifacts, not by session-local Claude framing.

### §2.5 Evidence-type discipline

Every finding must label the strongest evidence supporting it:

- **Source-traceable:** user-authored doc, accepted ADR, or explicit user instruction.
- **Artifact-reported:** inspected plan, commit message, audit output, or artifact.
- **Derived:** traceable/artifact evidence plus a small stated bridge.
- **Interpretive:** framing judgment, analogy, or explanatory synthesis.
- **Stipulative/input-frame:** imported frame used as lens, not observed fact.

Do not use a derived or interpretive claim as if it were source-traceable.

## §3. Audit Execution Form

### §3.1 Default execution

The default audit is paired:

1. **Step 1 - cross-vendor audit**
   - Auditor: codex GPT-5.5 xhigh.
   - Output: `FINDINGS.md`.
   - Reads this spec and the scoped inputs in §2.
   - Does not read Step 2, because Step 2 does not yet exist.
2. **Step 2 - same-vendor independent audit**
   - Auditor: Claude same-vendor adversarial-auditor xhigh.
   - Output: `FINDINGS-STEP2.md`.
   - Reads this spec and the scoped inputs in §2.
   - Does not read Step 1 findings before finishing its own findings.
3. **Differential**
   - Author: main-thread Claude after both findings exist.
   - Output: `DIFFERENTIAL.md`.
   - Compares Step 1 and Step 2 without erasing either.
4. **Disposition**
   - Owner: Logan.
   - Output: `DISPOSITION.md`.

### §3.2 Downgrade path

Logan may downgrade to Step 1 only under explicit cost-bandwidth constraint.
If downgraded:

- `FINDINGS.md` must include a "single-vendor residual risk" section.
- The residual risk must specifically name what Step 2 would have checked:
  same-vendor register leakage, integration-grammar-as-fact, closure-pressure
  comfort language, and drift-back-to-spike-shape in Claude-shaped terms.
- `DISPOSITION.md` must record that the downgrade reintroduces the risk named in
  the 2026-04-30 calibration finding: effort-level alone did not break the
  closure-pressure pattern.

Downgrade is not a silent operational shortcut.

### §3.3 Step 1 method

The cross-vendor auditor performs:

1. Pre-read all required inputs in §2.2.
2. Read the trajectory plan at `ffc0fb0` and commit message body.
3. Build a claim inventory of the plan's revised commitments:
   - what changed from spike to mapping,
   - what is now treated as input,
   - what is now treated as gate criterion,
   - what is delegated to Logan,
   - what is delegated to later audits,
   - what remains under-specified.
4. Apply all §4 lens questions.
5. Produce findings classified under §5.
6. Include notable absences and inverse signals, not just defects.

### §3.4 Step 2 method

The same-vendor auditor performs the same method independently, with special
attention to:

- comfort-language and confident register,
- integration-grammar-as-fact,
- places where Claude phrasing makes an imported frame sound natural,
- self-review that appears open while operationally closing a risk,
- "Logan disposes" language that transfers audit load to Logan.

Step 2 must state that it did not read Step 1 before producing findings.

### §3.5 Differential method

`DIFFERENTIAL.md` must partition:

- **Joint findings:** both auditors identify the same or materially similar issue.
- **Cross-vendor-only findings:** likely substance, negative-space, or
  brief-inheritance catches; do not discount merely because same-vendor missed
  them.
- **Same-vendor-only findings:** likely register, comfort-language, or
  Claude-style integration catches; do not discount merely because codex missed
  them.
- **Classification disagreements:** same issue, different class.
- **Method disagreements:** auditors disagree about what question-shape the plan
  should use.

The differential should not force consensus. It should preserve the disagreement
and give Logan a clean disposition surface.

## §4. Lens Questions

### §4.1 Question-shape fit

Required-from-brief questions:

- **Q-SF-1:** Is the trajectory-plan revision still spike-shape masquerading as
  mapping? Check whether Phase D §1.4, despite mapping vocabulary, still
  converges toward a single-target-equivalent output or treats the map as
  resolvable by a one-time Logan disposition.
- **Q-SF-2:** Is mapping itself the right question-shape? Surface third shapes
  if present: broader-scoped spikes, cartography plus design-theory, capability
  taxonomy, intervention portfolio, staged option-generation, or another
  theory-construction form.
- **Q-SF-3:** Does §0.8's spike-vs-mapping dichotomy oversimplify the question
  space? Identify hybrid shapes the dichotomy excludes or misnames.
- **Q-SF-4:** Does the four-axis structure cover the evidence territory:
  gsd-2 surfaces, arxiv-sanity-mcp practice, intervention intents, and joint
  accommodation evidence? Should a fifth axis be present, or should two axes
  collapse?

Cross-vendor-original additions:

- **Q-SF-5:** Does the plan confuse "mapping the territory" with "ranking a
  portfolio of possible interventions"? If the real output is an intervention
  portfolio, the audit should say so.
- **Q-SF-6:** Does the four-axis map have a falsifiable adequacy condition, or
  can it always be declared "partially coherent" and moved forward?
- **Q-SF-7:** Are the 12-property overlay and C1/C2/C3/C4 model doing too much
  work before the mapping has earned them?
- **Q-SF-8:** Does the plan preserve spikes as nested tools inside mapping in an
  operational way, or only as a safety sentence in §0.8?

### §4.2 Framing-inheritance risk

Required-from-brief questions:

- **Q-FI-1:** Does the revision treat its framing vocabulary as observed fact
  rather than imported inputs? Examples: "12 substrate-vision properties",
  "C1/C2/C3/C4", "pressure-not-destination", "identity-preserving", and
  "mapping-shape" itself.
- **Q-FI-2:** Does EXTERNAL-VISION-CONTEXT.md import residual closure pressure
  that the revision inherits through §3, §4, and §5?
- **Q-FI-3:** Does the revision's self-review operate or perform? Did C2-C5
  actually address the risk, or did they add comfort language around it?
- **Q-FI-4:** Does closure-pressure-into-elaboration recur in the revised plan?
  Look for "resolved enough to commit" framings without evidence.
- **Q-FI-5:** Does in-session-collaboration risk compound across Step 1, Step 2,
  2026-05-01 vision articulation, and self-review without an independent break?

Cross-vendor-original additions:

- **Q-FI-6:** Does the plan convert "Logan corrected this" into evidence that
  the corrected frame is now safe? Logan correction is evidence of a break, not
  evidence of immunity.
- **Q-FI-7:** Does the plan add artifacts, audits, and gates in a way that feels
  rigorous but avoids a sharper decision about the question shape?
- **Q-FI-8:** Does the plan treat "burden of proof on exclusion" as a neutral
  scope discipline, or does it bias toward over-inclusion and scope expansion?
- **Q-FI-9:** Does "identity-distortion is narrow" become an unearned license to
  classify most interventions as safely in scope?

### §4.3 Methodology-question-shape mismatch

Required-from-brief questions:

- **Q-MM-1:** Is the methodology-question-shape mismatch correctly diagnosed?
  Test the 2026-04-30 counter-claim that broader-scoped spikes might have been
  enough.
- **Q-MM-2:** Does the revision adequately specify how mapping iterates? Decide
  whether under-specification is appropriate theory-construction discipline or
  performative openness.
- **Q-MM-3:** Does Phase E specify what coherence means at theory-construction
  stage? How do fresh-session re-read, cross-axis consistency, cross-vendor
  read, and theory-construction-quality lenses compose into a disposition?

Cross-vendor-original additions:

- **Q-MM-4:** Does the plan use spike methodology as a foil too strongly,
  flattening the actual spike methodology's interpretive lenses and paired-review
  practices?
- **Q-MM-5:** Does the plan confuse methodology fit with artifact shape? A map
  artifact can still be produced by a spike-like method.
- **Q-MM-6:** Does the plan say when a bounded nested spike should be required,
  optional, or forbidden inside Phase D mapping?
- **Q-MM-7:** Does the plan need a separate "theory of change" or "intervention
  portfolio" methodology rather than mapping or spike methodology?

### §4.4 Phase D mapping operationalization

Required-from-brief-adjacent questions:

- **Q-PD-1:** Are Phase D inputs too broad for a single map to remain coherent?
- **Q-PD-2:** Are S1-S8 intervention intents treated as revisable sketches, or
  do they function as hidden commitments?
- **Q-PD-3:** Does the 12-property overlay make every property appear
  candidate-in-scope by default, even where Phase D has not earned that breadth?
- **Q-PD-4:** Is the budget-deviation trigger useful, or does "feels meaningful"
  become an unverifiable executor judgment?

Cross-vendor-original additions:

- **Q-PD-5:** Does Phase D have enough stopping rules to prevent mapping from
  becoming open-ended design work?
- **Q-PD-6:** Does Phase D distinguish evidence about gsd-2's current capability
  from design desires for uplifted gsd-2?
- **Q-PD-7:** Does Phase D preserve arxiv-sanity-mcp's product authority, or can
  substrate-evidence needs start distorting project-side artifacts?

### §4.5 Phase E coherence test

Required-from-brief questions:

- **Q-PE-1:** Does Phase E define coherent / partially coherent / incoherent with
  enough precision for Logan disposition?
- **Q-PE-2:** Does partial coherence risk becoming the default path forward for
  any ambiguous map?
- **Q-PE-3:** Does the same evidence support an alternative map that would change
  Phase F gate conclusions?

Cross-vendor-original additions:

- **Q-PE-4:** Does Phase E test whether the map's categories were imported from
  EXTERNAL-VISION-CONTEXT.md rather than discovered during mapping?
- **Q-PE-5:** Does Phase E include a sensitivity check: which one category,
  property, or intent would change the readiness outcome if reclassified?

### §4.6 Phase F gate criteria and Phase G dispositions

Required-from-brief questions:

- **Q-PF-1:** Does Phase F criterion 2, at least one C1 path, operationalize
  correctly? If there are zero C1 paths, when is the answer Phase D re-execution
  versus (V'.b) trajectory reconsideration?
- **Q-PF-2:** Does criterion 5, methodology-mismatch finding integrated, risk
  being satisfied superficially by citation rather than operational integration?
- **Q-PG-1:** Are Phase G artifact dispositions right, especially
  METHODOLOGY-MISMATCH-FINDING.md as DUPLICATE and 2026-04-30 deliberation as
  per-deliberation Logan-disposed? Are other dispositions similarly
  under-considered?

Cross-vendor-original additions:

- **Q-PF-3:** Does the extraction gate assume that a coherent map implies a
  dedicated repo is the right next container?
- **Q-PF-4:** Does criterion 3, internal coherence plus diagnostic-loop
  preservation, specify how much arxiv-sanity-mcp dependency is acceptable?
- **Q-PG-2:** Does the MOVE/DUPLICATE/STAY table distinguish artifact custody from
  artifact authority? A duplicate can still have one authoritative side.
- **Q-PG-3:** Does extraction create a risk of splitting the evidence trail so
  future readers see conclusions without diagnostic context?

### §4.7 Paired-audit discipline and downgrade risk

Required-from-brief questions:

- **Q-AD-1:** Is paired-default-with-Logan-discretion-to-downgrade the right
  formulation, or does the downgrade escape hatch undermine the discipline's
  purpose?
- **Q-AD-2:** Is this Step 3 audit spec itself authored under conditions that
  re-import the failure mode? Identify constraints from this spec or its
  provenance that narrow the audit too much.

Cross-vendor-original additions:

- **Q-AD-3:** Does the plan distinguish downgrade-before-audit from
  downgrade-after-Step-1? These have different risk profiles.
- **Q-AD-4:** Does "same-vendor independent" have a concrete forbidden-reading
  boundary sufficient to prevent anchoring?
- **Q-AD-5:** Does the differential have authority to preserve disagreement, or
  is it likely to harmonize the two audits into a more comfortable synthesis?

### §4.8 Negative-space and meta-questions

Required-from-brief questions:

- **Q-NS-1:** What does the revision exclude from consideration? Is the exclusion
  principled or accidental?
- **Q-NS-2:** What does the revision not say but should say?
- **Q-META-1:** Is there an implicit frame the revision treats as natural rather
  than imported?

Cross-vendor-original additions:

- **Q-NS-3:** Which alternative phase shapes are not represented in the option
  space at all?
- **Q-NS-4:** Which risks are assigned to future audits instead of addressed in
  the plan text?
- **Q-NS-5:** Which parts of the plan become hard to question once the dedicated
  repo exists?
- **Q-META-2:** Does the plan confuse "more explicit" with "more resolved"?
- **Q-META-3:** Does the plan's own length and comprehensiveness make it harder
  to see the few live load-bearing uncertainties?

## §5. Classification Scheme

### §5.1 Classes

Use these classes for each finding:

- **Class A - ACCEPT-AS-STATED**
  - The plan's wording, scope, or mechanism is adequate.
  - The finding may record an inverse signal, small clarification, or residual
    risk that does not require plan change.

- **Class B - ADDENDUM-TRACTABLE**
  - The issue is real but can be handled by an addendum, dispatch instruction,
    local audit-output requirement, or explicit caveat.
  - The eight-phase trajectory and the mapping-shape revision can remain in
    place.

- **Class C - REVISE-BEFORE-COMMIT**
  - The issue affects the trajectory shape, question-shape, gate semantics,
    artifact authority, or audit discipline strongly enough that accepting the
    plan as revised would propagate a load-bearing error.
  - Class C includes any finding that mapping may be the wrong question-shape or
    that Phase D/E/F cannot be executed coherently under the current revision.

### §5.2 Classification calibration

Do not over-classify Class C just because the issue is intellectually
interesting. Class C requires downstream consequence.

Do not under-classify Class C because revision would be inconvenient. If the
plan's shape is wrong, it is Class C.

When uncertain between B and C, state:

- what downstream decision changes if the finding is true,
- what evidence would resolve the classification,
- whether Logan can safely proceed with an addendum,
- whether the issue needs plan-text revision before audit/commit.

### §5.3 Finding types

Use one or more:

- question-shape
- methodology-fit
- framing-inheritance
- integration-grammar-as-fact
- performative-openness
- closure-pressure
- negative-space
- phase-gate-semantics
- artifact-custody
- audit-discipline
- evidence-type-confusion
- scope-creep
- register/comfort-language
- inverse-signal

### §5.4 Confidence levels

Each finding records confidence:

- **High:** multiple independent evidence lines converge.
- **Medium-high:** strong artifact evidence plus plausible inference.
- **Medium:** plausible interpretation with alternatives.
- **Low:** weak signal worth surfacing, not disposition-driving alone.

Low-confidence findings can be Class B if useful as addenda. Low-confidence
findings should rarely be Class C unless the potential downside is large and the
uncertainty itself blocks safe commitment.

## §6. Output Structure

### §6.1 Step 1 output: `FINDINGS.md`

Frontmatter must record `type: trajectory-replan-audit-findings`, audit date,
auditor, `spec: ./AUDIT-SPEC.md`, `target_commit: ffc0fb0`, and
`status: step1-complete`.

Required sections:

1. **Summary.** Total findings, Class A/B/C breakdown, top-line read, strongest
   Class C candidate if any, and single-vendor residual risk if Step 2 is
   downgraded.
2. **Read boundary and method.** Required inputs read, optional inputs read and
   why, forbidden inputs not read, source-read count if any.
3. **Per-finding analysis.** For each finding: class, confidence, type, lens
   question IDs, artifact, location, short quote where relevant, evidence type,
   precise claim, justification, downstream consequence, what would dissolve or
   downgrade it, and disposition implication.
4. **Cross-artifact patterns.** Propagation patterns, repeated risk signatures,
   or contradictions across the plan and standing context.
5. **Notable absences and inverse signals.** Where the plan resists the failure
   mode and where mapping discipline appears operational.
6. **Alternative question-shapes surfaced.** Each alternative, whether it is
   live, and what would make it better than mapping.
7. **Confidence, limits, and non-binding disposition signal.** Include why
   Logan might accept-as-stated, accept with addendum, or require revision.

### §6.2 Step 2 output: `FINDINGS-STEP2.md`

If Step 2 fires, it writes a separate file, not an appendix to Step 1:

Frontmatter must record `type: trajectory-replan-audit-findings-step2`,
auditor, spec, target commit, `status: step2-complete-independent`, and
`step1_read_before_completion: false`.

Required sections mirror Step 1, with two additions: an independence statement
confirming Step 1 and forbidden inputs were not read, and a same-vendor register
/ comfort-language section focused on what same-vendor is structurally
positioned to catch.

### §6.3 Differential output: `DIFFERENTIAL.md`

If paired audit fires, `DIFFERENTIAL.md` must include: executive differential,
joint findings, cross-vendor-only findings, same-vendor-only findings,
classification disagreements, method disagreements, differential risks, and a
non-binding disposition signal. It must preserve real disagreement instead of
harmonizing it away.

### §6.4 Disposition output: `DISPOSITION.md`

After Logan disposes, `DISPOSITION.md` records: disposition summary,
per-finding disposition, required plan revisions or addenda, audit-discipline
disposition, residual risks accepted, and next action. Frontmatter must name
Logan as disposer and list the findings/differential inputs reviewed.

### §6.5 Output constraints

- Step 1 target length: 250-600 lines.
- Step 2 target length: 250-600 lines.
- Differential target length: 150-350 lines.
- Findings must cite short verbatim quotes where claims rest on text.
- Do not quote long passages.
- Do not rewrite the plan unless Logan asks after disposition.
- Do not collapse disagreement into a single harmonized "answer."

## §7. Disposition Pathway

### §7.1 Logan review order

Logan should review:

1. Summary and all Class C findings from Step 1.
2. Summary and all Class C findings from Step 2, if present.
3. `DIFFERENTIAL.md` executive differential, if present.
4. A sample of Class B findings for calibration.
5. The non-binding disposition signals.

### §7.2 Disposition options

Logan disposes one of:

- **Commit / accept-as-stated**
  - No Class C, or Logan rejects Class C findings as non-load-bearing.
  - Plan can proceed under the current revision.

- **Accept with addendum**
  - Class B items or bounded Class C risks can be handled by an addendum,
    audit-dispatch instruction, or local clarification before the next phase.
  - The plan body does not need structural revision.

- **Revise before commit / proceed**
  - One or more Class C findings change the plan's question-shape, phase
    mechanics, gate semantics, artifact custody, or audit discipline.
  - The trajectory plan must be revised and, if the revision is load-bearing,
    re-audited or at least rechecked under this spec's affected lenses.

### §7.3 Per-finding disposition record

For each finding, `DISPOSITION.md` records:

- accepted / rejected / modified,
- Logan reasoning,
- required write-set,
- whether revision is plan-body, addendum, or audit-instruction only,
- whether re-audit is required,
- residual risk accepted if no revision.

### §7.4 Re-audit triggers

Re-audit or targeted recheck is required if:

- mapping is replaced by another question-shape,
- Phase D/E/F gate semantics materially change,
- the paired-audit downgrade rule changes,
- the 12-property or C1/C2/C3/C4 model changes authority status,
- artifact custody or authority changes for Phase G,
- Step 3 audit finds the audit spec itself mis-scoped.

## §8. Cross-References

- Primary target: `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`
  at commit `ffc0fb0`, plus the `ffc0fb0` commit message body.
- Spec provenance, not default audit input:
  `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/SPEC-DRAFTING-BRIEF.md`.
- Standing context: 2026-04-30 methodology-mismatch deliberation,
  `EXTERNAL-VISION-CONTEXT.md`, and `RELATIONSHIP-TO-PARENT.md`.
- Audit precedents: Phase A trajectory `PLAN-AUDIT.md` + `DISPOSITION.md`;
  v1-GSD premise-bleed `AUDIT-SPEC.md`; cross-vendor codebase-understanding
  `wave-3/META-SYNTHESIS.md`.
- Methodology grounding: `.planning/spikes/METHODOLOGY.md`,
  `.planning/foundation-audit/METHODOLOGY.md`, `.planning/LONG-ARC.md`, and
  `AGENTS.md`.

---

*Spec drafted 2026-05-01 by cross-vendor codex GPT-5.5 xhigh for Logan
disposition before audit dispatch. This spec intentionally treats its own
provenance as a risk surface: it implements the Claude brief's required
coverage while preventing the brief from becoming the future audit's hidden
authority.*
