---
id: sig-2026-03-20-spike-experimental-design-rigor
type: signal
project: arxiv-mcp
tags: [gsd-framework, spike-workflow, experimental-design, epistemic-rigor, process-gap]
created: 2026-03-20T15:30:00Z
updated: 2026-03-20T15:30:00Z
durability: convention
status: active
---

## Observation

Spike 003 (strategy profiling) revealed systematic gaps in the experimental design and execution process that produced findings with overstated confidence. Five specific failures:

### 1. Sample size / representativeness not validated
The Voyage embedding screening used a 100-paper pool with 20% selectivity (top-20 from 100). At this pool size, models are forced to agree — there aren't enough alternatives for meaningful divergence. The real-world selectivity would be 0.1% (top-20 from 19K). No pre-execution check caught this. The sample was also drawn from only 2 of 8 interest profiles.

### 2. Metric limitations not surfaced before use
Jaccard was used as the sole decision criterion for the Voyage screening. Its fundamental limitations (binary threshold artifact, nature-blind, treats all disagreements equally) were not documented before use or considered when designing the experiment. The DESIGN.md's own evaluation framework section provides sophisticated treatment of metric limitations for the core instruments — but the Voyage extension experiment was designed without this rigor.

### 3. Prescribed qualitative checkpoints skipped
The DESIGN.md specified four qualitative review checkpoints (W1, W3, W4.1, W5.4). Only W1 was executed in the initial session. The three skipped checkpoints, when later performed, contradicted quantitative conclusions in multiple cases (SPECTER2 redundancy, fusion profile-dependence, kNN niche utility). Skipping qualitative review is not just a process failure — it produces materially wrong conclusions.

### 4. Evaluation framework entanglement not treated as a limitation
The entire evaluation framework (BERTopic clusters, interest profile construction, LOO-MRR) is built on MiniLM's representation. This was noted in the DESIGN.md (Known evaluation biases) but the implications were underweighted: "relevant" in the evaluation means "relevant as MiniLM defines it." This entanglement inflates MiniLM's apparent advantage and penalizes strategies that find papers MiniLM doesn't cluster together. The qualitative reviews partially corrected this, but only after the initial DECISION.md was written with HIGH confidence levels.

### 5. Confidence levels did not distinguish measurement / interpretation / extrapolation
The initial DECISION.md used blanket HIGH/MEDIUM/LOW confidence levels. These collapsed three distinct epistemic questions:
- **Measurement**: Did we accurately measure what the instrument detects? (generally YES for 19K experiments)
- **Interpretation**: Does the measurement mean what we say it means? (DEPENDS on framework entanglement and qualitative correction)
- **Extrapolation**: Do findings hold beyond the testing conditions? (VARIES by finding and target domain)

Blanket confidence levels hide which dimension the confidence applies to and under what conditions it holds.

## Impact

- Voyage was prematurely rejected based on insufficient methodology
- SPECTER2 was initially included in the architecture based on quantitative metrics that qualitative review later contradicted
- The DECISION.md's confidence levels were misleading until revision
- Extension experiments (gap-fills) were designed ad-hoc without the rigor of the core DESIGN.md

## Pattern

This is the same pattern as `sig-2026-03-19-spike-framework-scope-gap`: the spike workflow framework assumes contained, simple experiments. When spikes grow into multi-wave investigations with extension experiments, the quality infrastructure (design review, checkpoint enforcement, metric validation) doesn't scale. The core DESIGN.md was excellent — the problem is that extension experiments and execution shortcuts bypassed it.

## Relationship to GSD Reflect framework

The GSD Reflect framework has rigorous quality infrastructure for development phases:
- **Plan checker agent**: Verifies plans will achieve phase goals before execution
- **Verifier agent**: Validates phase completion against goals after execution
- **Signal system**: Captures methodological concerns for reflection

No equivalent exists for spikes:
- No **spike design reviewer** that validates experimental methodology before execution
- No **checkpoint enforcer** that ensures prescribed review points are actually performed
- No **findings qualification template** that requires distinguishing measurement/interpretation/extrapolation confidence
- No **sample size / representativeness checklist** for empirical experiments
- No **metric limitation documentation requirement** before a metric is used as a decision criterion

## Recommendation

### For GSD Reflect framework

1. **Spike design review agent** (analogous to `gsdr-plan-checker`): Before spike execution begins, validate:
   - Sample size and representativeness relative to the question being asked
   - Metric selection with explicit limitation documentation
   - Decision thresholds with justification for why those thresholds are appropriate
   - Qualitative review checkpoints specified and marked as mandatory vs optional
   - Evaluation framework entanglement analysis (does the evaluation favor any particular approach?)

2. **Spike findings qualification template**: Require every spike DECISION.md to include:
   - Testing conditions (what the experiments actually tested)
   - Three-level confidence framework (measurement / interpretation / extrapolation)
   - Conditions under which findings hold vs conditions where extrapolation is uncertain
   - Known limitations and methodological failures

3. **Checkpoint enforcement**: When a DESIGN.md prescribes qualitative review checkpoints, the spike runner should verify they were performed before allowing synthesis (W5) to proceed.

4. **Extension experiment rigor**: When gap-fill or extension experiments are added during execution, they should go through the same design review as the core experiments, not be designed ad-hoc.

### For this project

- Spike 003 DECISION.md and FINDINGS.md updated with full epistemic qualifications
- Spike 004 designed with corrected methodology from the start
- The three-level confidence framework (measurement/interpretation/extrapolation) adopted as standard for future spike findings
