---
status: standing-reference
date: 2026-03-30
scope: critical lenses for spike research design and interpretation
related:
  - .planning/spikes/SPIKE-DESIGN-PRINCIPLES.md (practical rules — complements this document)
  - .planning/spikes/HYPOTHESES-005.md (hypotheses generated using these lenses)
  - .planning/deliberations/spike-epistemic-rigor-and-framework-reflexivity.md
  - .planning/deliberations/comparative-characterization-and-nonadditive-evaluation-praxis.md
provenance: >
  Produced through dialogue during Spike 004 post-execution critique (2026-03-28 to 2026-03-30).
  The conversation moved from self-critique of Spike 004's findings (seed sensitivity, MiniLM-centrism,
  Jaccard gatekeeping) to philosophical analysis of what went wrong methodologically, to identification
  of specific philosophies of science that could serve as critical lenses, to the question of how to
  preserve this thinking for future use.
---

# Spike Research Methodology

This document captures reusable critical lenses for spike design and interpretation. It complements SPIKE-DESIGN-PRINCIPLES.md (practical rules) with interpretive frameworks (analytical orientations that require judgment to apply).

**How to use this document**: Before designing a spike, an independent design critic should read each lens and ask whether the spike design is vulnerable to what the lens diagnoses. After execution, the findings critic should apply each lens to check whether the interpretation is warranted. The phase-mapping table at the end specifies which lenses apply when.

## The core distinction: representation vs function-in-use

Spikes 001-004 asked representational questions (what does the embedding space look like?) and tried to read functional conclusions off them (which model is better for researchers?). This doesn't work. Representational evidence constitutes one phenomenon (embedding space geometry); functional claims require evidence about a different phenomenon (what happens when someone uses the system).

Representation can serve as the *theory* that generates predictions about function. Function serves as the *test* that supports or undermines the representational theory. This is the right relationship: predict function from representation, then test function directly.

## Critical Lenses

### 1. Bayesian updating

**Diagnoses**: Binary verdicts (CONFIRMED/FALSIFIED) that throw away information about how much evidence shifted our confidence. Overclaiming followed by overqualifying ("SPECTER2 redundancy FALSIFIED!" → "well, actually, the seeds were different...").

**Recommends**: For each hypothesis, state a prior probability before execution and track how the evidence shifts it. Not formal Bayes factors — explicit statements of credence movement. "Before Spike 004, credence that SPECTER2 is redundant: ~0.7. After: ~0.3. Reasons for the shift: [tau evidence, seed sensitivity caveat, evaluation framework bias]."

**Concrete change**: Replace CONFIRMED/FALSIFIED with probability updates. Report the direction and magnitude of the shift, the evidence that produced it, and the conditions under which the shift would reverse.

**When it catches what others miss**: When a finding is partly confirmed and partly undermined. Binary verdicts force a choice; Bayesian updating represents the actual epistemic state.

### 2. Standpoint epistemology

**Diagnoses**: Evaluator monoculture. All quality judgments from one type of evaluator (AI list-review) with one implicit standpoint on what "relevant" means. The absent researcher is absent in a way that defaults to a specific standpoint without acknowledging it.

**Recommends**: Include structurally different evaluator types — not two instances of the same LLM, but genuinely different perspectives:
- An AI agent doing a research task (evaluator-as-user)
- A human researcher assessing recommendations (evaluator-as-expert)
- Category-metadata-based evaluation (evaluator-as-structure, no semantic model)

Where evaluators agree: high confidence regardless of which model is evaluated. Where they disagree: the disagreement reveals standpoint-dependent quality — the system should let users choose.

**Concrete change**: The convergence and divergence between evaluator types IS the finding, not noise to be averaged away.

**When it catches what others miss**: When AI reviewers and human researchers would disagree about what's valuable. This is likely for "productive provocations" — papers that challenge assumptions (valuable to an expert, hard for an AI to assess without research context).

### 3. Paradigm analysis

**Diagnoses**: Normal science within an unexamined paradigm. MiniLM-as-baseline defines what counts as evidence, what counts as a finding, what counts as an anomaly. Anomalies accumulate (seed sensitivity, Jaccard instability, evaluation-constitutes-findings) and get accommodated rather than prompting paradigm revision.

**Recommends**: Design at least one experiment that doesn't reference the incumbent model at all. Instead of "how does X compare to MiniLM?" ask "which configuration helps accomplish a research task?" The incumbent becomes one configuration among many, not the reference.

**Concrete change**: The experimental design itself should not privilege any model. Evaluation asks about task completion quality, not about agreement with a baseline.

**When it catches what others miss**: When the evaluation framework systematically advantages the incumbent. H4 (framework bias) is the test: if model rankings change under different profile constructions, the findings were paradigm-dependent.

### 4. Mechanistic decomposition

**Diagnoses**: End-to-end testing that confirms something works without explaining why. When it breaks, you don't know what to fix. When it succeeds, you don't know what's load-bearing. "Signal axis" characterizations are mechanistic stories with untested mechanism steps.

**Recommends**: For hypotheses with proposed mechanisms (training data → embedding geometry → recommendation character → researcher value), design tests for individual steps, not just the endpoint.

**Concrete change**: Each mechanism step becomes an independently testable sub-hypothesis. "SPECTER2 captures citation-community structure" decomposes into: (a) SPECTER2 paper pairs with high cosine similarity have more citation links than MiniLM pairs, (b) SPECTER2's divergent papers share citation communities with seeds more than MiniLM's divergent papers do.

**When it catches what others miss**: When the end-to-end prediction holds but for the wrong reason. A model might produce "good" recommendations (per AI review) via a mechanism completely different from the one we hypothesize — and understanding the actual mechanism matters for when/where to deploy it.

### 5. Values-in-science analysis

**Diagnoses**: Non-epistemic values doing implicit work in evaluation. Local-first preference shapes which models get investigated seriously. Exploration-first architecture predisposes toward finding "models are different" rather than "one model is best." Cost-awareness biases toward cheap configurations.

**Recommends**: Explicitly separate epistemic findings from value-laden recommendations. Present findings as configurations ranked by different value profiles, not as a single recommendation.

**Concrete change**: "If you value local-first: MiniLM + TF-IDF. If you value discovery breadth with GPU: add SPECTER2. If you value maximum divergent discovery and accept API dependency: add Voyage." The epistemic finding (models produce different rankings) is the same; the recommendation depends on values.

**When it catches what others miss**: When a finding is nearly discarded because it conflicts with project values (Voyage's P2 discovery was almost missed because rate-limiting made it "operationally impractical" — a value judgment that almost blocked an epistemic finding).

### 6. Duhem-Quine analysis

**Diagnoses**: Hypotheses entangled with untested auxiliary assumptions. You never test a hypothesis in isolation — you test hypothesis + evaluation framework + profile construction + metric choice + seed selection + sample composition. When a prediction fails, the failure could be in the hypothesis or in any auxiliary.

**Recommends**: For each finding, identify which auxiliary assumptions are load-bearing. Design experiments that vary one auxiliary at a time to disentangle.

**Concrete change**: H4 (vary profile construction method) is a Duhem-Quine test. Add more: vary seed set (already shown to matter), vary retrieval method (H3), vary evaluation method (H1). Findings that survive all auxiliary variations are robust. Findings that change are auxiliary-dependent and must be reported as such.

**When it catches what others miss**: When a finding appears to be about the hypothesis but is actually about the evaluation framework. The MiniLM-entanglement discovery was exactly this — "SPECTER2 is divergent" was partly about SPECTER2 and partly about using MiniLM-derived profiles.

## Phase-Mapping: When to Apply Each Lens

| Phase | Lens | What to check |
|-------|------|---------------|
| **Hypothesis formulation** | Mechanistic | Are mechanism steps specified and independently testable? |
| **Hypothesis formulation** | Bayesian | Is a prior stated? Is the prediction specific enough to shift belief? |
| **Design critique** | Paradigm | Does this experiment test within a paradigm or question it? |
| **Design critique** | Duhem-Quine | Which auxiliary assumptions are load-bearing? Are they tested? |
| **Design critique** | Standpoint | Which evaluator types are included? What standpoints are missing? |
| **Execution** | Values | Are non-epistemic values shaping which configurations get tested? |
| **Interpretation** | Bayesian | How much did the evidence shift our credence? (Not: was it confirmed?) |
| **Interpretation** | Values | Are epistemic findings separated from value-laden recommendations? |
| **Post-execution critique** | All lenses | Independent critic applies each lens to the findings |

## What this document cannot do

This is a standing reference, not a protocol. It requires judgment to apply — knowing when a lens is illuminating vs when it's producing false positives. A critic who mechanically applies all lenses to every spike will generate noise. The lenses are tools for thinking, not checklists for compliance.

The document also cannot enforce its own consumption. It exists as available context. Making it operative requires a design review protocol that mandates reading it — which GSDR does not currently provide. See the filed gaps.
