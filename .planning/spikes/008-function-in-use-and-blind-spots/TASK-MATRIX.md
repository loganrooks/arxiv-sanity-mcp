---
type: task-matrix
status: draft
date: 2026-04-16
author: codex
target: .planning/spikes/008-function-in-use-and-blind-spots
---

# Task Matrix

## Compared Configurations

### `control_minilm_tfidf_dual_view`

- incumbent `MiniLM centroid` view
- incumbent `TF-IDF` view
- purpose: current two-view arrangement control

### `candidate_minilm_specter2_dual_view`

- incumbent `MiniLM centroid` view
- challenger `SPECTER2 centroid` view
- purpose: test whether the specialized-domain challenger adds task value beyond the control

### `candidate_minilm_voyage_dual_view`

- incumbent `MiniLM centroid` view
- challenger `Voyage centroid` view
- purpose: test whether the broad-conceptual challenger adds task value beyond the control

### Packet Assembly Rule

- `[chosen for now]` The first pass should use the saved MiniLM profile family and centroid retrieval for the challenger view.
- `[derived]` `006` did not justify promoting `kNN-per-seed` to default status, and `007` narrowed at the family level rather than the method-specific level.
- `[chosen for now]` The evaluation packet for each run should therefore present the same `MiniLM` list plus one second-view list, not a reopened method matrix.

## Selected Profiles

### `P2` Language model reasoning

- role: broad conceptual profile
- why included:
  - strongest `Voyage` support case from `007`
  - best current site for testing whether frontier / failure-mode papers actually help outputs

### `P3` Quantum computing / quantum ML

- role: specialized technical profile
- why included:
  - strongest `SPECTER2` blind-review support case from prior spikes
  - cleanest site for testing whether specialized-domain divergence improves research outputs

### `P1` RL for robotics

- role: denser control profile
- why included:
  - strong incumbent coverage already exists
  - `Voyage` was close to redundant here, so this profile helps test whether challenger gains disappear on denser profiles

### Reserve Profile

- `[chosen for now]` `P8` is the reserve specialized profile if `P3` proves too narrow or too noisy during packet assembly.

## Task Instances

### `T1` `P2` exploratory

Goal: map the current frontier around reasoning failure modes, alternative reasoning mechanisms, and critiques of explicit chain-of-thought.

Deliverable: a 3-part landscape memo covering:
- frontier themes
- key tensions / disagreements
- a 6-paper reading path

Evaluation focus: whether challenger-only papers widen the landscape in a productive way rather than merely adding thematic variation.

### `T2` `P2` confirmatory

Goal: assess the claim that explicit chain-of-thought is not the only mechanism that supports useful reasoning behavior.

Deliverable: a short evidence memo with:
- claim status (`supported`, `mixed`, or `not supported`)
- 3 strongest supporting papers
- 2 strongest qualifications or counterpoints

Evaluation focus: whether challenger-only papers materially change the claim assessment.

### `T3` `P2` shortlist / triage

Goal: produce a shortlist of 5 papers for a researcher starting a project on reasoning failures and alternative reasoning mechanisms.

Deliverable:
- ranked 5-paper shortlist
- 1-sentence reason per paper
- 2 papers explicitly rejected from the packet and why

Evaluation focus: whether second-view papers survive triage and enter the final shortlist.

### `T4` `P3` exploratory

Goal: map the most relevant subareas adjacent to the seed set in quantum ML / quantum circuits.

Deliverable: a structured landscape memo covering:
- variational-model design
- optimization / compilation
- adjacent but still useful subareas

Evaluation focus: whether challenger-only papers reveal a more useful specialized landscape than the control.

### `T5` `P3` confirmatory

Goal: assess the claim that near-term quantum ML performance depends more on circuit design / optimization choices than on naive scaling.

Deliverable:
- claim status (`supported`, `mixed`, or `not supported`)
- evidence table with at least 4 cited papers
- one explicit limitation note

Evaluation focus: whether challenger-only papers materially improve the evidence base for the claim.

### `T6` `P3` shortlist / triage

Goal: produce a shortlist of 5 papers for a researcher who wants technically central follow-up reading on variational quantum model design and related optimization.

Deliverable:
- ranked 5-paper shortlist
- source-view note for each selected paper
- 2 near-miss papers and why they were excluded

Evaluation focus: whether specialized second-view papers displace incumbent choices.

### `T7` `P1` exploratory

Goal: map the practical landscape around RL for robotics, especially deployment, control, and embodiment-adjacent concerns.

Deliverable: a concise landscape memo with:
- core cluster
- practical-extension cluster
- out-of-scope adjacent work

Evaluation focus: whether challengers help on a denser profile or mostly reproduce the incumbent.

### `T8` `P1` confirmatory

Goal: assess the claim that practical / deployment-oriented papers materially widen the useful reading set for this profile.

Deliverable:
- claim status (`supported`, `mixed`, or `not supported`)
- 3 strongest positive examples
- 2 reasons the widening may not matter

Evaluation focus: whether challenger-only papers change the conclusion or merely add adjacent noise.

### `T9` `P1` shortlist / triage

Goal: produce a shortlist of 5 papers for a researcher who wants high-precision follow-up reading with minimal adjacency drift.

Deliverable:
- ranked 5-paper shortlist
- precision rationale for each selected paper
- 2 rejected challenger papers if any were considered

Evaluation focus: whether challengers help in a profile where the incumbent may already be sufficient.

## Prompt Frame

Use the same frame for every configuration run:

1. You are given:
   - one profile brief with seed papers
   - one task brief
   - one configuration packet containing the available recommendation views
2. You must work only from the provided packet.
   - no new retrieval
   - no web browsing
   - no external knowledge as evidence
3. Every substantive claim in the output must cite at least one paper from the packet.
4. Every cited paper must be tagged as:
   - `selected`
   - `contributed`
   - or `considered_but_not_used`
5. If a challenger-view paper changes the deliverable, say how it changed it.

## Tool / Turn / Context Budgets

### Tool budget

- allowed:
  - read the task brief
  - read the profile brief
  - read the configuration packet
  - write one local scratch note if needed
- disallowed:
  - web search
  - fresh retrieval
  - opening unrelated repo files during the run

### Turn budget

- `[chosen for now]` Maximum `10` reasoning / tool turns per run.

### Context budget

- one profile brief
- one task brief
- one configuration packet
- optional scratch note only

## Stopping Condition

Stop the run when one of these is true:

1. the requested deliverable is complete and internally cited
2. the run reaches the `10`-turn budget
3. the agent can no longer improve the output without violating the packet-only rule

## Output Schema

Each run should end with the same schema:

1. `task_id`
2. `configuration_id`
3. `selected_papers`
   - `arxiv_id`
   - `source_view`
   - `reason`
4. `contributed_papers`
   - `arxiv_id`
   - `source_view`
   - `contribution_type`
   - `effect_on_output`
5. `considered_but_not_used`
   - `arxiv_id`
   - `reason`
6. `final_output`
7. `self-reported limits`

### Closeout Rule

- `[chosen for now]` A paper counts as blind-spot evidence only if it appears in `contributed_papers`, not merely in `selected_papers`.
