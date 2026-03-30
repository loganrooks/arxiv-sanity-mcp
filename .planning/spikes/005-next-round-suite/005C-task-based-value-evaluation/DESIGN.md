---
question: "Do the alternative views that survive 005A and 005B help complete research tasks or surface blind spots that matter in use?"
type: functional + comparative
status: draft
depends_on:
  - ../005A-framework-robustness/DESIGN.md
  - ../005B-retrieval-geometry-complementarity/DESIGN.md
  - ../../HYPOTHESES-005.md
addresses:
  - H1: evaluation method changes which strategies appear best
  - H5: the two-view arrangement may have valuable blind spots
---

# Spike 005C: Task-Based Value of Blind Spots

## Question

When an agent is doing actual research work rather than judging lists in isolation, do the surviving alternative views surface papers that change task outcomes in useful ways?

## Why this spike is last

This is the highest-value spike and the most expensive one. It should evaluate only the candidate views that survive the framework and retrieval gates. Otherwise it turns expensive task work into yet another representational sorting exercise.

## Commitment levels

### Settled

- This spike evaluates function-in-use, not representational difference.
- The findings remain limited by the absent-researcher problem unless a human checkpoint is added.

### Chosen for now

- The spike will compare 2-3 candidate view configurations selected by 005A and 005B.
- Tasks will include both exploratory and confirmatory modes.
- Profiles will be chosen from the discriminating set rather than the full 8-profile slate.

### Open

- Whether the user will be available for a small human-judgment checkpoint.
- Whether one agent protocol is sufficient or whether multiple evaluator types are required inside this spike.

## What this spike is not

- It is not a leaderboard for all models.
- It is not a replacement for human evaluation.

## Experimental design

### Phase 1: Candidate selection

Take only the candidate views that survive 005A and 005B. Example shapes:

- `MiniLM + TF-IDF` incumbent
- incumbent + `SPECTER2`-style view
- incumbent + `Qwen3/Stella`-style view

### Phase 2: Task definition

Define research tasks that differ in what "value" means:

- **Exploratory**: map a landscape, find adjacent mechanisms, locate blind spots
- **Confirmatory**: support or challenge a specific claim with relevant literature

### Phase 3: Agent runs

For each task:

- run the same agent protocol against each candidate view configuration
- track paper selection, use in output, and whether unique papers materially changed the result

### Phase 4: Evaluation

Compare strategy rankings under:

- list-based evaluation from prior spikes
- task-based evaluation here

The core output is whether the ranking of strategies changes by evaluation method.

## Success criteria

- We can say whether "truly unique" papers are actually used in task completion.
- We can say whether exploratory and confirmatory tasks prefer different view configurations.
- We can say whether prior list-review judgments understated or overstated challenger value.

## Failure modes to watch

- agents converge on the same papers regardless of view, making the protocol too insensitive
- task prompts accidentally encode one view's assumptions
- findings are overinterpreted as human preference

## Outputs

- task protocol
- task-based comparison report
- explicit update on whether blind spots are valuable in use or merely different on paper
