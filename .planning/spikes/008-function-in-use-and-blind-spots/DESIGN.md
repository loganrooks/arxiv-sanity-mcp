---
question: "For the shortlisted configurations, which ones help actual research tasks, and do their so-called blind-spot papers contribute to outputs rather than merely increasing difference metrics?"
type: comparative + task-evaluation
status: drafted
round: 1
depends_on:
  - 005 (evaluation framework robustness)
  - 006 (model-retrieval interactions)
  - 007 (training-data mechanism probes)
  - H1 and H5 from HYPOTHESES-005.md
linked_references:
  - ../HYPOTHESES-005.md
  - ../SPIKE-DESIGN-PRINCIPLES.md
  - ../METHODOLOGY.md
  - ../004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md
---

# Spike 008: Function-In-Use And Blind-Spot Value

## Question

For the configurations that remain live after Spikes 005-007, which ones actually help research tasks, and do the papers outside the current two-view arrangement contribute to task outputs or merely to measured difference?

## Why This Spike Last

This is the most expensive spike in the sequence because it requires task infrastructure, evaluator design, and potentially some human judgment. It should therefore operate only on a narrowed candidate set and after the strongest framework and retrieval confounds have already been reduced.

## Hypotheses Addressed

- **Primary:** `H1`
- **Primary:** `H5`

## Prior Credence And Update Target

- `[chosen for now]` Prior `P(H1) = 0.70`
- `[chosen for now]` Prior `P(H5) = 0.45`

This spike should shift `H1` upward only if task-based evaluation materially changes the comparative picture produced by list-based metrics and reviews. It should shift `H5` upward only if blind-spot papers do more than get noticed: they must change the final task outputs in a traceable way.

## Chosen For Now

1. Evaluate **task success, not list difference**.
   The unit of interest is whether a configuration helps an agent produce a better research output for a stated task.

2. Always include the current `MiniLM + TF-IDF` arrangement as the control configuration.

3. Run at most **three configurations** in one pass:
   - the incumbent control,
   - plus up to two shortlisted challengers or ambiguous candidates from 006/007.

4. Use a **mixed task set**:
   - exploratory tasks
   - confirmatory tasks

5. Use a **representative profile set**, not all 8 by default.
   Chosen for now, the likely anchor profiles are `P3`, `P5`, `P7`, `P8`, plus one control profile such as `P1` or `P4`.

6. Human adjudication is a required closeout gate.
   If a human check cannot be run, 008 may produce an AI-only pilot artifact, but it may not close `H1` or `H5` and may not support an architectural recommendation.

## Experimental Shape

### Phase 1: Task harness

- Define exactly **three task templates per selected profile**:
  - one exploratory landscape-mapping task,
  - one confirmatory evidence-checking task,
  - one shortlist-building / triage task.
- Standardize the prompt frame, tool budget, turn budget, context budget, and stopping condition across configurations.
- Write the task matrix before execution; task design is not allowed to drift configuration by configuration.

### Phase 2: Configuration runs

- Run the shortlisted configurations against the same tasks
- Capture which recommendations are selected, ignored, and used in the final outputs

### Phase 3: Contribution tagging and blind-spot analysis

- Define `selected` as: a paper opened, inspected, or explicitly chosen by the agent during the run.
- Define `contributed` as: a paper that materially changes the final output by adding evidence, changing a claim, entering the final shortlist, or displacing a prior choice.
- Blind-spot papers count as valuable only through `contributed`, not merely through `selected`.

### Phase 4: Mandatory qualitative review

- Review the final task outputs and the contribution traces for each configuration.
- Examine whether blind-spot papers were substantive contributors, decorative citations, or dead-end detours.
- Review exploratory and confirmatory tasks separately rather than averaging them into one narrative.

### Phase 5: Evaluator plurality and human adjudication

- Run at least one human review pass over a sampled set of task outputs and claimed blind-spot contributions.
- If human review is unavailable, stop at `pilot only / incomplete` rather than treating AI-only evaluation as a completed functional verdict.

## Success Criteria

1. The spike produces task-level comparisons, not only recommendation-list comparisons.
2. The task matrix is pre-registered and reused across all compared configurations.
3. The output states whether blind-spot papers were merely selected or actually contributed to research outputs.
4. The spike includes a mandatory qualitative review over outputs and contribution traces.
5. The output identifies where evaluator disagreement changes the conclusion.
6. Human adjudication is present or the spike is explicitly marked `pilot only / incomplete`.
7. Any architectural recommendation remains at most `[chosen for now]` unless human judgment materially supports it.

## Guardrails

- Do not let agent outputs stand in for human value without explicit qualification.
- Do not average exploratory and confirmatory tasks into one headline score.
- Do not reopen the full model set unless 005-007 fail to reduce uncertainty.
- Do not count a blind-spot paper as valuable merely because it appeared in the run transcript; it must change the resulting work product.
