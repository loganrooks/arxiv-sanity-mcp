---
question: "How much of the current model divergence survives alternative profile construction and checked-in seed variation?"
type: robustness + comparative
status: draft
depends_on:
  - ../PRE-SPIKE-ANALYSES.md
  - ../../HYPOTHESES-005.md
  - ../../SPIKE-DESIGN-PRINCIPLES.md
  - ../../METHODOLOGY.md
addresses:
  - H4: evaluation framework bias
  - Open question A2: MiniLM-entangled profiles
  - Open question A3: seed sensitivity
---

# Spike 005A: Framework Robustness and Seed Dependence

## Question

Do the model differences reported so far survive variation in profile construction and checked-in seed variants, or are they mainly artifacts of the current MiniLM-built evaluation frame?

## Why this spike comes first

The pre-spike analyses support three derived findings:

1. challengers do not form a single bloc,
2. seed sensitivity is profile-specific rather than uniform,
3. `MiniLM + TF-IDF` remains the strongest aggregate incumbent.

That combination makes framework robustness the highest-value next step. Without it, retrieval-method experiments and task-based evaluation risk interpreting artifacts as model properties.

## Commitment levels

### Settled

- This spike is about robustness, not utility.
- No architectural recommendation stronger than `Open` or `Chosen for now` may come out of this spike.

### Chosen for now

- The spike will compare at least three profile constructions:
  - current MiniLM-based profiles,
  - category-based profiles,
  - SPECTER2-based profiles.
- Checked-in seed variants will be carried through as an explicit dimension of the report.

### Open

- Whether a dedicated fixed-K seed generator needs to be built inside this spike or documented as an unresolved methodological limitation.

## What this spike is not

- It is not a retrieval-method spike.
- It is not a task-value spike.
- It is not the place to decide which views to ship.

## Design commitments from methodology

- **Paradigm lens**: one profile construction must not silently define the whole experiment.
- **Duhem-Quine lens**: profile construction and seed choice are auxiliary assumptions, not background noise.
- **Principle 7**: characterize seed sensitivity before reporting findings.
- **Principle 8**: compare all models to each other, not only to MiniLM.

## Experimental design

### Inputs

- Existing 2000-paper embeddings from Spike 004
- Existing `interest_profiles.json`
- New alternative profile sets:
  - category-based
  - SPECTER2-derived

### Phase 1: Alternative profile construction

Build two alternative profile families matching the current 8-profile coverage as closely as possible:

1. **Category-based profiles**
   - based on metadata rather than any embedding space
   - designed to reduce MiniLM entanglement

2. **SPECTER2-derived profiles**
   - make the prior incumbent a challenger
   - test whether framework favoritism is approximately symmetric

### Phase 2: Comparative rerun

For each profile family and checked-in seed variant:

- recompute pairwise tau matrices
- recompute MiniLM-vs-challenger and TF-IDF-vs-challenger overlaps
- recompute truly unique counts
- report which relations are stable vs framework-dependent

### Phase 3: Stability report

Classify findings into:

- **Stable across frameworks**
- **Profile-framework dependent**
- **Seed-sensitive**
- **Indeterminate**

## Success criteria

- We can say which model relations are framework-robust and which are not.
- We can say whether the current MiniLM-favoring frame materially changes rankings.
- We can produce a shortlist for 005B that is justified by robustness, not convenience.

## Failure modes to watch

- Category profiles too coarse to map onto the current research interests
- SPECTER2-derived profiles collapsing into a different but equally entangled frame
- Seed variation conclusions overstated from a still-incomplete variant family

## Outputs

- framework comparison report
- rerun metrics under each profile family
- candidate shortlist for 005B
- explicit list of claims that remain framework-dependent
