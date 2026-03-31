---
question: "Does retrieval method change which models genuinely complement MiniLM and TF-IDF under a more robust evaluation frame?"
type: comparative + mechanistic
status: draft
depends_on:
  - ../005A-framework-robustness/DESIGN.md
  - ../PRE-SPIKE-ANALYSES.md
  - ../../HYPOTHESES-005.md
addresses:
  - H3: retrieval method interacts with embedding geometry
  - H2: training-data mechanism as interpretation layer
  - Codex Blocker 3: better second view than TF-IDF?
---

# Spike 005B: Retrieval Geometry and Complementarity

## Question

Once framework robustness is accounted for, does retrieval method change which models or model-pairs actually complement `MiniLM + TF-IDF`?

## Why this spike is second

The pre-spike analyses show that challenger complementarity is strongly profile-dependent. They also show that the aggregate incumbent remains `MiniLM + TF-IDF`. That makes retrieval interaction the next efficient uncertainty to test: it can strengthen or collapse challenger cases without requiring the cost of task-based evaluation.

## Commitment levels

### Settled

- This spike compares retrieval methods, not final user value.
- `MiniLM + TF-IDF` remains the incumbent baseline throughout.

### Chosen for now

- The core retrieval contrast is `centroid` vs `kNN-per-seed`.
- `P1`, `P3`, `P6`, and `P7` are discriminating profiles.
- `P2`, `P4`, and `P8` are control profiles where TF-IDF still has the strongest secondary-view claim.

### Hypothesis

- Some apparent model differences will collapse or invert once kNN is introduced.
- `SPECTER2` may gain more from kNN than centroid.
- `Qwen3` and `Stella` may separate more clearly under method variation than they do under centroid alone.

## What this spike is not

- It is not about human or agent task success.
- It is not a full fusion-landscape redo.

## Experimental design

### Phase 1: Retrieval implementation

Implement `kNN-per-seed` for the candidate models using the existing 2000-paper embeddings.

### Phase 2: Comparative run

For each candidate model, each robust profile family from 005A, and each checked-in seed variant:

- compute top-K sets under centroid and kNN
- compare pairwise tau and overlap changes
- compare `MiniLM + challenger` vs `MiniLM + TF-IDF` union coverage at `K=20/50/100`

### Phase 3: Mechanistic reading

Interpret results through `H2` without overstating it:

- if a model benefits under kNN, ask what that implies about local neighborhood structure
- if a model loses under kNN, ask whether centroid was washing out noise or preserving signal

### Phase 4: Qualitative checkpoint

Run qualitative review only on method-induced changes for:

- the discriminating profiles,
- the best challenger win cases,
- and the strongest TF-IDF control cases.

## Success criteria

- We can answer whether any challenger beats or ties TF-IDF as a second view under a robust frame.
- We can identify which retrieval method is load-bearing for each challenger claim.
- We can reduce the candidate set for 005C to 2-3 serious view configurations.

## Failure modes to watch

- kNN improves quantitative diversity but degrades qualitative value
- method effects are overwhelmed by framework effects that 005A did not resolve cleanly
- too many challenger configurations survive, leaving 005C unfocused

## Outputs

- retrieval comparison report
- robust complementarity table against `MiniLM + TF-IDF`
- shortlist of candidate view configurations for task-based evaluation
