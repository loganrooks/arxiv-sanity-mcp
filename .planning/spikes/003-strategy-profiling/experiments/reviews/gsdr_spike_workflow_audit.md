# GSD Reflect Spike Workflow Audit: Experimental Design Rigor

**Date:** 2026-03-20
**Auditor:** Claude (gsdr audit agent)
**Scope:** Whether GSD Reflect's spike workflow documentation provides adequate guidance for epistemically rigorous experimental design
**Trigger:** Methodological failures discovered during Spike 003 execution

---

## 1. What the Spike Workflow Docs Prescribe

The GSD Reflect spike workflow is defined across five files:

- **`gsdr-spike-runner.md`** (agent spec) — Defines the Build -> Run -> Document execution flow
- **`run-spike.md`** (workflow orchestrator) — Handles workspace creation, Design phase, agent spawning
- **`spike-execution.md`** (reference) — Spike types, phases, iteration rules, KB integration
- **`spike-integration.md`** (reference) — How spikes connect to plan-phase and new-project flows
- **`/gsdr:spike`** (command) — Entry point, routes to workflow

### What guidance exists for experimental rigor

**Spike types and success criteria patterns** (spike-execution.md Section 2): Defines four spike types (Binary, Comparative, Exploratory, Open Inquiry) with success criteria patterns per type. Comparative spikes require "winner criteria defined." Exploratory spikes allow "learning goals" that "can refine during spike as understanding grows."

**DESIGN.md as the contract** (spike-runner.md Step 1): The runner parses hypothesis, success criteria, and experiment plan from DESIGN.md. These are validated for completeness before execution proceeds.

**Checkpoint triggers** (spike-runner.md): Four categories — build failures, dramatically different results, Round 1 inconclusive, ambiguous success criteria. These are deviation-triggered, not design-review-triggered.

**Confidence levels** (spike-execution.md Section 6): Three levels defined — HIGH ("strong empirical evidence, clear winner, reproducible results"), MEDIUM ("some evidence with inference"), LOW ("limited data, educated guess").

**Anti-patterns** (spike-execution.md Section 10): Six anti-patterns including "Premature Spiking" (running spikes for questions research could answer), "Scope Creep," and "Missing Decision." None address experimental design quality.

**Research-first advisory** (run-spike.md Step 2): Before creating a workspace, the workflow assesses whether the question is better suited to research or experimentation. This is a triage gate, not a design quality gate.

### What guidance does NOT exist

The spike workflow documentation contains **zero guidance** on:

1. **Sample size requirements or representativeness** — No mention of how to determine appropriate sample sizes, what makes a sample representative, or when a sample is too small to support conclusions.

2. **Metric selection and limitation documentation** — No requirement to document what each metric measures, what it cannot measure, or its known failure modes. The DESIGN.md template fields (hypothesis, success criteria, experiment plan) do not include a "metric limitations" or "what this metric cannot tell us" field.

3. **Experimental design review before execution** — No review step between DESIGN.md creation and Build phase. The runner validates that DESIGN.md is "complete" (fields present), not that the experimental design is sound.

4. **Qualitative review requirements** — No mention of qualitative review anywhere in the spike workflow documentation. The entire framework assumes quantitative success criteria with measurable thresholds.

5. **Post-hoc epistemic qualification** — No requirement to distinguish measurement validity from interpretation validity from extrapolation validity when reporting confidence levels. The confidence level definitions (HIGH/MEDIUM/LOW) conflate "strong empirical evidence" with "clear winner" and "reproducible results" — three different epistemic claims.

6. **Evaluation framework bias assessment** — No requirement to identify or mitigate systematic biases in the evaluation methodology itself.

7. **Circular evaluation detection** — No guidance on recognizing when an evaluation framework is entangled with the thing being evaluated.

---

## 2. What's Missing: Specific Gaps That Enabled the Spike 003 Failures

### Gap 1: No Experimental Design Validation Gate

The workflow moves from DESIGN.md creation directly to execution. In interactive mode, the user can review DESIGN.md, but the review prompt asks for approval of the hypothesis, success criteria, and experiment plan — it does not prompt for critical assessment of the experimental design's validity. In YOLO mode, DESIGN.md is auto-approved and execution proceeds immediately.

**What this enabled:** Spike 003's DESIGN.md was extraordinarily well-designed — it included epistemic hazards, assumption tracking, bias mitigations, qualitative review protocol, and metric limitation documentation. But there was no mechanism to verify that this design was actually followed during execution. The DESIGN.md prescribed four qualitative review checkpoints (W1 screening, W3 combinations, W4.1 cold start, W5.4 final). Three of the four were skipped. The workflow has no checkpoint that asks "have you completed the qualitative reviews prescribed in DESIGN.md?"

### Gap 2: No Sample Size or Representativeness Framework

The spike workflow treats "success criteria" as the only evaluation contract. If success criteria say "test on 100 papers," the runner measures against that threshold. But there is no guidance for evaluating whether 100 papers is a meaningful sample, whether the sample is representative, or what conclusions a given sample size can and cannot support.

**What this enabled:** The Voyage embedding screening used a 100-paper sample with 20% selectivity (top-20 from 100). At the full corpus scale of 19,000 papers, the equivalent selectivity would be ~0.1% (top-20 from 19,000). A 200x difference in selectivity fundamentally changes what the metric measures — high selectivity on a small sample tells you almost nothing about the model's behavior at realistic selectivity. This is a basic experimental design issue, but nothing in the workflow flags it.

### Gap 3: No Metric Limitation Requirements

The spike-runner.md Document phase template includes "Data: {measurements, observations}" but does not require documenting what each metric measures, what it cannot measure, or its known failure modes. The profile card schema has no field for metric limitations.

**What this enabled:** Jaccard similarity was used as the sole comparison metric for the Voyage screening, without noting that Jaccard measures set overlap, not ranking quality, and that two models producing different papers with different quality characteristics would show low Jaccard (suggesting non-redundancy) even if one is categorically worse. The metric was presented as sufficient evidence when it answered a different question than the one being asked.

### Gap 4: No Evaluation Framework Independence Requirement

Nothing in the spike workflow warns about evaluation frameworks that are entangled with the model being evaluated. There is no requirement to test whether the evaluation protocol itself is biased toward one approach.

**What this enabled:** The leave-one-out MRR evaluation used clusters defined by MiniLM embeddings to evaluate MiniLM embeddings. MiniLM's "dominance" on this metric was partially circular — it was being evaluated against its own representation of similarity. The qualitative review (which was done for W1, to its credit) caught this, but the quantitative metrics initially reported HIGH confidence without qualifying this entanglement.

### Gap 5: No Confidence Qualification Framework

The spike workflow's confidence levels (HIGH/MEDIUM/LOW) are defined as a single dimension. There is no requirement to distinguish:

- **Measurement confidence**: Are the numbers accurate? (Sample size, instrument precision, variance)
- **Interpretation confidence**: Does the metric measure what we think it measures? (Construct validity, metric limitations)
- **Extrapolation confidence**: Will these findings hold in other contexts? (Representativeness, sample bias)

A finding can have HIGH measurement confidence (the Jaccard number is accurate), LOW interpretation confidence (Jaccard doesn't answer the question we're asking), and UNKNOWN extrapolation confidence (100-paper sample may not predict 19K behavior).

**What this enabled:** Confidence levels were initially set at HIGH based on quantitative metrics alone. The qualitative review (when it was done) revealed that the metrics were measuring the wrong thing in several cases, but the confidence framework had no vocabulary for expressing "the numbers are right but the interpretation is questionable."

---

## 3. Adherence vs Documentation: Failure-by-Failure Analysis

| # | Failure | Guidance existed? | Followed? | Assessment |
|---|---------|------------------|-----------|------------|
| 1 | Voyage screening: 100-paper sample, 20% selectivity, should have been ~0.1% | **No** — No sample size or representativeness guidance anywhere in spike docs | N/A | **Documentation gap** |
| 2 | Jaccard as sole metric, no limitation documentation | **No** — No metric limitation requirements in spike docs | N/A | **Documentation gap** |
| 3 | Three of four qualitative review checkpoints skipped | **Partially** — DESIGN.md prescribed them, but nothing in the spike *runner* enforces DESIGN.md-prescribed checkpoints. The runner's checkpoint triggers are deviation-based (unexpected results), not protocol-adherence-based (did you do what DESIGN.md said to do?). | DESIGN.md guidance was not followed; runner docs don't enforce it | **Both** — DESIGN.md had good guidance but the runner has no enforcement mechanism |
| 4 | Evaluation framework entangled with MiniLM at every level | **No** — No circular evaluation detection guidance. DESIGN.md prescribed "model-independence requirement" but this was the spike author's addition, not a workflow-level concern. | DESIGN.md's own mitigation was partially implemented but the framework remained biased | **Documentation gap** at the workflow level; **adherence gap** for DESIGN.md's specific mitigations |
| 5 | Confidence set at HIGH without distinguishing measurement/interpretation/extrapolation validity | **No** — Confidence levels are defined as a single undifferentiated dimension. The definitions conflate "strong evidence" with "clear winner" with "reproducible." | The agent used the framework as documented — the framework itself is insufficient | **Documentation gap** |

**Summary:** Four of five failures stem from documentation gaps (the spike workflow simply doesn't address these concerns). One failure (qualitative review skipping) is a combination: the DESIGN.md had good guidance but the runner has no mechanism to enforce protocol adherence during execution.

---

## 4. Comparison with Plan-Checker and Verifier

### What the plan-checker provides that spikes lack

The `gsdr-plan-checker` is a dedicated verification agent with:

- **11 verification dimensions** covering requirement coverage, task completeness, dependency correctness, key links, scope sanity, verification derivation, context compliance, and 4 semantic validation dimensions
- **Severity-classified findings** (blocker, warning, info, advisory)
- **Structured issue output** with fix hints
- **Goal-backward analysis** — starts from what the phase should deliver, works backward to verify the plan addresses it
- **An explicit adversarial posture** ("A plan can have all tasks filled in but still miss the goal")

The plan-checker operates as a gate: plans do not proceed to execution until the checker passes them (or the user overrides findings). This is fundamentally different from the spike workflow, which has no equivalent gate between DESIGN.md and execution.

### What the verifier provides that spikes lack

The `gsdr-verifier` operates after execution with:

- **Three-level artifact verification** (exists, substantive, wired)
- **Anti-pattern scanning** (TODOs, placeholders, empty implementations)
- **Goal-backward verification** against must-haves
- **Gap structuring** for remediation

The verifier embodies the principle that "task completion does not equal goal achievement." Nothing analogous exists for spikes — the spike runner does not verify that experimental execution actually tested the hypothesis, that the evaluation methodology was sound, or that the conclusions follow from the evidence.

### The asymmetry

GSD Reflect has a rigorous gate-keeping architecture for implementation work:

```
PLAN.md --> [plan-checker: 11 dimensions] --> EXECUTION --> [verifier: 3-level check]
```

But for experimental work (spikes), the architecture is:

```
DESIGN.md --> [user review in interactive / auto-approve in YOLO] --> EXECUTION --> [nothing]
```

The plan-checker and verifier were designed because the system recognized that plans can look complete but miss the goal, and that execution can produce files but not achieve the outcome. The same insight applies to experimental design and execution: a DESIGN.md can look thorough but have flawed methodology, and experiment execution can produce numbers but not answer the question.

The spike workflow lacks both a pre-execution design review agent and a post-execution findings review agent. This is the structural gap.

---

## 5. Recommendations

### 5.1 Create a Spike Design Reviewer Agent (`gsdr-spike-design-reviewer`)

Analogous to `gsdr-plan-checker`, this agent would review DESIGN.md before execution proceeds. It would check:

**Experimental Design Dimensions:**

| Dimension | What it checks |
|-----------|---------------|
| Sample representativeness | Is the sample size justified? Does selectivity at sample scale match selectivity at deployment scale? Are representativeness assumptions stated? |
| Metric coverage | Are multiple complementary metrics used? Is each metric's limitation documented? Is there a metric for each aspect of the hypothesis? |
| Evaluation independence | Is the evaluation framework independent of the thing being evaluated? Are there circular evaluation risks? |
| Qualitative review planning | Are qualitative review checkpoints defined? Are they integrated into the experiment waves, not just appended at the end? |
| Epistemic hazard inventory | Are known ways the experiment could mislead explicitly listed with mitigations? |
| Assumption tracking | Are assumptions stated with confidence levels and falsification criteria? |
| Bias mitigation | Are known evaluation biases listed with mitigations? |
| Baseline calibration | Are appropriate baselines defined that bound the measurement scale? |
| Confidence decomposition | Do success criteria distinguish measurement confidence from interpretation confidence from extrapolation confidence? |

This agent would produce findings with severity levels, just like the plan-checker. Blocker-level findings would prevent execution in interactive mode and trigger a checkpoint in YOLO mode.

### 5.2 Add Protocol Adherence Checkpoints to the Spike Runner

The spike runner's checkpoint triggers are currently deviation-based (unexpected results, build failures). Add protocol-adherence triggers:

- **After each wave completes:** "DESIGN.md prescribes the following checkpoints for this wave: [list]. Have all been completed?" If not, checkpoint with explanation of what was skipped and why.
- **Before Document phase:** "DESIGN.md prescribes the following qualitative reviews: [list]. Which have been completed?" If any are missing, require explicit justification.

This addresses the specific failure where DESIGN.md prescribed good methodology but execution skipped critical steps.

### 5.3 Extend the Confidence Framework

Replace the single-dimension confidence level with a structured confidence assessment:

```yaml
confidence:
  measurement: HIGH    # Are the numbers accurate?
  interpretation: MEDIUM  # Does the metric measure what we claim?
  extrapolation: LOW   # Will this hold in other contexts?
  overall: MEDIUM      # Minimum of the three
  basis: |
    Measurement: 3 seed selections, variance < 10%.
    Interpretation: LOO-MRR uses MiniLM clusters to evaluate MiniLM. Circular.
    Extrapolation: January 2026 only; one month may not represent typical distribution.
```

This forces the agent to articulate what kind of confidence it has, not just how much. The overall confidence is the minimum of the three dimensions — you cannot claim HIGH confidence if interpretation validity is questionable.

### 5.4 Add Sample Size and Representativeness Checklist to DESIGN.md Template

For any experiment that involves sampling:

```markdown
## Sample Design

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Population size | {N} | {what is the full dataset?} |
| Sample size | {n} | {why this number?} |
| Selectivity at sample scale | {top-K / n} | {e.g., 20/100 = 20%} |
| Selectivity at deployment scale | {top-K / N} | {e.g., 20/19000 = 0.1%} |
| Selectivity ratio | {sample / deployment} | {e.g., 200x — is this acceptable?} |
| Representativeness argument | {how do we know the sample represents the population?} |
```

This would have caught the Voyage screening issue immediately: a 200x selectivity mismatch would be visible at design time.

### 5.5 Add Metric Limitation Requirements to the Evaluation Protocol

For each metric used in a spike, require:

```markdown
| Metric | What it measures | What it cannot measure | Known failure modes | When it misleads |
|--------|-----------------|----------------------|--------------------|--------------------|
| Jaccard | Set overlap between two result sets | Ranking quality, relevance quality, whether different results are better or worse | High Jaccard can mean redundancy; low Jaccard can mean either complementarity or one model being bad | When comparing models at different selectivity levels; when one model returns different but worse results |
```

### 5.6 Create a Spike Findings Reviewer Agent (`gsdr-spike-findings-reviewer`)

Analogous to `gsdr-verifier`, this agent would review DECISION.md before KB persistence. It would check:

- Do conclusions follow from the evidence presented?
- Are confidence levels justified by the data?
- Are metric limitations acknowledged in the interpretation?
- Were prescribed qualitative reviews completed and integrated?
- Are extrapolation claims bounded appropriately?
- Is the decision qualified by the epistemic limitations of the evaluation?

### 5.7 Add Circular Evaluation Detection to Spike Anti-Patterns

Add to spike-execution.md Section 10:

```markdown
### Circular Evaluation
**Symptom:** Evaluation framework uses the same model/method/representation as the strategy being evaluated. Example: using MiniLM-defined clusters to evaluate MiniLM embedding quality.
**Fix:** Require evaluation on at least one framework independent of the strategy being tested. If the evaluation framework was designed using one model's representations, test whether the same conclusions hold on an independent representation.
```

---

## 6. Overall Assessment

The Spike 003 failures are **primarily documentation gaps, not adherence failures.** The spike workflow documentation provides procedural guidance (how to run a spike) but not methodological guidance (how to design a rigorous experiment). The one area where adherence was also a factor (qualitative review skipping) is itself a documentation gap — the runner has no mechanism to enforce protocol adherence, even when DESIGN.md prescribes it.

The contrast with the plan-checker is instructive. GSD Reflect recognized that implementation plans need adversarial review before execution and created a dedicated agent with 11 verification dimensions. The same recognition has not been applied to experimental design. The plan-checker's motto — "plan completeness does not equal goal achievement" — has a direct experimental analog: **experimental design completeness does not equal methodological soundness.** A DESIGN.md can have all the right sections filled in while containing flawed sample designs, biased evaluation frameworks, and single-metric evaluations.

The recommendation is to create a spike-design-reviewer agent with experimental design dimensions, a spike-findings-reviewer agent for post-hoc verification, and to extend the runner with protocol-adherence checkpoints. Together, these would give spikes the same gate-keeping rigor that plans already have.

Spike 003's DESIGN.md was, ironically, the best evidence that the spike workflow needs this infrastructure. The DESIGN.md itself was a model of epistemic rigor — it prescribed epistemic hazards, bias mitigations, qualitative review integration, and metric limitation documentation. But all of that rigor lived in the DESIGN.md document, not in the workflow infrastructure. When execution pressure (YOLO mode, long session, many parallel experiments) pushed the agent to cut corners, nothing stopped it. The DESIGN.md was a policy document without enforcement. GSD Reflect's plan-checker exists precisely because policy documents without enforcement don't work — and that lesson applies equally to experimental design.
