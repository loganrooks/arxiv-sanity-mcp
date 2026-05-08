# Foundation Audit — Justification Methodology

> **Relationship to `.planning/spikes/METHODOLOGY.md`:** This document covers *decision-review epistemic discipline* — how to evaluate whether project decisions rest on adequate epistemic grounds, trace evidence chains, and assess inference integrity. The spikes METHODOLOGY covers *spike research design and interpretation* — interpretive lenses, paired-review practice, and model-verification disciplines for audit and spike work. The two documents are complementary; consult this one for foundation-audit-style decision reviews and the spikes METHODOLOGY for spike design and paired-review dispatch. Cross-reference: `.planning/spikes/METHODOLOGY.md`.

## Purpose

Criteria and processes for evaluating whether project decisions rest on adequate epistemic grounds. Used during the Phase 5 foundation audit and available for future decision review.

## Core Principles

### 1. Evidence Tracing
Every claim must trace to identifiable evidence. Categories of evidence (strongest to weakest):
- **Empirical**: Measured behavior, test results, benchmarks, observed user behavior
- **Structural**: Follows necessarily from accepted constraints or architecture
- **Analogical**: Supported by well-documented precedent in similar systems
- **Inferential**: Reasonable conclusion from available information, but alternatives exist
- **Stipulative**: Declared without external support (acceptable for value judgments, problematic for factual claims)

### 2. Alternative Evaluation
A decision is better justified when plausible alternatives were identified and compared, not just when the chosen option has supporting arguments. Key question: *What was this decided against, and why did those alternatives lose?*

### 3. Sensitivity Analysis
How much would need to change for this decision to be wrong? Decisions robust to plausible perturbations need less justification than fragile ones. Categories:
- **Load-bearing**: If wrong, significant rework or architectural change required
- **Adjustable**: If wrong, can be corrected with bounded effort
- **Cosmetic**: If wrong, minimal downstream impact

### 4. Inference Chain Integrity
When a conclusion depends on a chain of reasoning (A → B → C → D), the weakest link determines the chain's strength. Identify:
- Where does the chain start? (axioms, user statements, design docs, AI inference?)
- Where are the transitions? (each → is a potential break point)
- What is the weakest link?

### 5. Category Discipline
Distinct epistemic categories must not be conflated:
- Exploration ≠ Specification (a "candidate approach" is not a requirement)
- Convention ≠ Constraint (a common practice is not a hard limit)
- Precedent ≠ Justification (Phase N did it this way ≠ Phase N+1 should)
- Author identity ≠ Project identity (who builds it ≠ what it's for)

## Evaluation Process

For each decision under review:

1. **State the claim precisely** — What exactly was decided?
2. **Trace the evidence** — What supports it? Classify the evidence type.
3. **Identify alternatives** — What else could have been decided? Why were they rejected (or were they)?
4. **Assess sensitivity** — Load-bearing, adjustable, or cosmetic? What breaks if this is wrong?
5. **Check the inference chain** — Is every link sound? Where is the weakest?
6. **Render a verdict**:
   - **Well-grounded**: Evidence is adequate, alternatives were considered, robust to perturbation
   - **Reasonable but under-justified**: Probably right, but the reasoning has gaps that should be documented
   - **Suspect**: Plausible alternatives were not adequately ruled out, or evidence is weak
   - **Unsound**: Relies on broken inference, category error, or missing evidence

## Confidence Notation

When recording findings, use explicit confidence markers:
- `[HIGH]` — Multiple independent lines of evidence converge
- `[MODERATE]` — Single line of evidence, but strong; or multiple weak lines
- `[LOW]` — Inferential, no direct evidence, reasonable but uncertain
- `[UNGROUNDED]` — No traceable evidence; stipulative or inherited from unexamined source

## What This Is Not

- Not a gatekeeping exercise — the goal is understanding, not blocking progress
- Not falsificationism specifically — we use inference to best explanation, coherence checking, and sensitivity analysis rather than trying to "disprove" each decision
- Not a demand for certainty — decisions under uncertainty are fine when the uncertainty is acknowledged and the decision is appropriately scoped
