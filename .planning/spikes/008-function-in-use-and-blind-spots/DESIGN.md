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

## Chosen For Now

1. Evaluate **task success, not list difference**.
   The unit of interest is whether a configuration helps an agent produce a better research output for a stated task.

2. Use a **mixed task set**:
   - exploratory tasks
   - confirmatory tasks

3. Use a **representative profile set**, not all 8 by default.
   Chosen for now, the likely anchor profiles are `P3`, `P5`, `P7`, `P8`, plus one control profile such as `P1` or `P4`.

4. If a small amount of human judgment is practically available, include it.
   If not, do not pretend AI-only task evaluation resolves the absent-researcher problem.

## Experimental Shape

### Phase 1: Task harness

- Define 3+ tasks per selected profile
- Separate exploratory and confirmatory task types
- Standardize agent context and stopping conditions

### Phase 2: Configuration runs

- Run the shortlisted configurations against the same tasks
- Capture which recommendations are selected, ignored, and used in the final outputs

### Phase 3: Blind-spot analysis

- Examine the papers surfaced by the candidate views but missed by the current two-view arrangement
- Check whether those papers contributed to the task outputs

### Phase 4: Evaluator plurality

- If available, add a small human check
- If unavailable, explicitly report the evaluation as still AI-only and bounded

## Success Criteria

1. The spike produces task-level comparisons, not only recommendation-list comparisons.
2. The output states whether blind-spot papers contributed to research outputs.
3. The output identifies where evaluator disagreement changes the conclusion.
4. Any architectural recommendation remains at most `[chosen for now]` unless human judgment materially supports it.

## Guardrails

- Do not let agent outputs stand in for human value without explicit qualification.
- Do not average exploratory and confirmatory tasks into one headline score.
- Do not reopen the full model set unless 005-007 fail to reduce uncertainty.
