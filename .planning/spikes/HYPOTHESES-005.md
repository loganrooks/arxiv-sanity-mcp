---
status: draft
date: 2026-03-30
scope: hypotheses for next spike round, with mechanism theories and falsification conditions
prior_work: Spikes 001-004, OPEN-QUESTIONS.md, SPIKE-DESIGN-PRINCIPLES.md
---

# Hypotheses for the Next Spike Round

## Theoretical orientation

The spike program so far has operated under an implicit philosophy: compare models by measuring their outputs (rankings, Jaccard, tau), then interpret the measurements through qualitative review. This is essentially a representational approach — we ask "what does this model's embedding space look like?" and try to read properties off the measurements.

The problem this produced (across all four spikes) is that representational evidence cannot answer functional questions. Knowing that SPECTER2 produces different rankings than MiniLM tells us nothing about whether those different rankings are useful to anyone. The "signal axis" characterizations (citation-community, deployment-realism) are representational claims about what the models encode, but the project needs functional knowledge: which configurations help researchers discover papers they would not otherwise find, and that they actually want?

This distinction — between what a model represents and what it does when someone uses it — is not a refinement of the existing approach. It requires a different kind of experiment. An experiment that tests function-in-use, not representation-in-isolation.

But there's a subtlety. We can't abandon representational evidence entirely. The mechanism theories below make representational claims (about embedding space geometry, about what information different training data encodes) that predict functional outcomes. The predictions are about function; the explanations invoke representation. This is the right relationship: representation serves as the theory that generates predictions about function, and function serves as the test that either supports or undermines the representational theory.

The hypotheses are structured as:
- **Mechanism**: Why we expect this outcome (the theory)
- **Prediction**: What we expect to observe (testable)
- **Sub-hypotheses**: More specific predictions that decompose the main claim
- **Falsification conditions**: What observations would undermine the mechanism, not just the prediction (a prediction can fail because the experiment was bad; a mechanism is challenged when the pattern of failure is inconsistent with the theory)
- **Scope**: Under what conditions the hypothesis is expected to hold

---

## H1: Evaluation method shapes which strategies appear best

### The vague version (from earlier)
"Agent-based evaluation will produce different quality rankings than list-review or metrics alone."

### What "different" means and why

**Mechanism**: Metrics and list-review both evaluate recommendations as static objects — lists to be scored or assessed. But recommendations function as interventions in a research process: they change what a researcher reads, which changes what connections they make, which changes what they produce. A recommendation's value is context-dependent — the same paper can be useless in one research context and transformative in another. Evaluation methods that ignore the research context will systematically misjudge context-dependent value.

Specifically: metrics like Jaccard and tau measure agreement between ranking systems. They cannot distinguish "different and better" from "different and worse" from "different and irrelevant." AI list-review adds a judgment of relevance, but the reviewer lacks the research context that determines whether relevance translates to utility. An agent doing a research task has a context: it needs papers to accomplish something, and the recommendations either help or don't.

**Prediction**: Strategy configurations that look equivalent under metrics and list-review will diverge under task-based evaluation. The divergence will be systematic, not random — it will correlate with properties of the task (exploratory vs confirmatory, narrow vs broad) and properties of the strategy (diversity-promoting vs precision-promoting).

### Sub-hypotheses

**H1a**: *Ordering within the top-K matters more for task-based evaluation than for list-review.* Two strategies with identical top-20 membership but different orderings will produce different task outcomes, because the agent processes papers sequentially and earlier papers shape the context for interpreting later ones. List-review, by contrast, evaluates each paper independently.

- Falsification: If agents produce identical research outputs regardless of recommendation ordering (for strategies with same top-20 membership), the ordering effect is negligible and list-review captures what matters.

**H1b**: *Exploratory tasks will value divergent papers more than confirmatory tasks.* An agent surveying a field ("map the landscape of X") benefits from recommendations that span the space, including papers that challenge assumptions. An agent seeking support for a specific claim benefits from precision. Strategies that produce "truly unique" papers (divergent from MiniLM + TF-IDF) will show higher value in exploratory tasks.

- Falsification: If agents doing exploratory tasks don't select truly unique papers at higher rates than agents doing confirmatory tasks, the task-type distinction doesn't predict strategy value.
- Partial falsification: If agents select truly unique papers but the resulting research output isn't better (the selected papers were interesting to encounter but didn't contribute to the output), then selection rate is not a good proxy for value.

**H1c**: *AI list-review systematically underestimates the value of productive provocations.* Papers that challenge a research direction's assumptions are hard to assess in isolation — their value depends on having a direction to be challenged. A reviewer looking at a list can judge topical relevance but not whether a paper would productively redirect someone's thinking. An agent mid-task can encounter redirection and either benefit or not.

- Falsification: If AI list-reviewers and task-based agents agree on which papers are valuable, including provocative papers, then list-review captures what matters and agent-based evaluation is unnecessary overhead.
- Scope: This hypothesis is most likely to hold for broad, interdisciplinary profiles and least likely for narrow, well-defined technical profiles.

**H1d**: *The evaluation method interacts with the strategy being evaluated.* Some strategies may look good under metrics (high MRR) but poor under task-based evaluation (the recommendations don't help accomplish the task), or vice versa. If so, the choice of evaluation method isn't just a matter of precision — it determines which strategies appear viable.

- Falsification: If the rank ordering of strategies is the same under metrics, list-review, and task-based evaluation (just with different absolute scores), then evaluation method is a precision issue, not a validity issue.
- This is the most consequential sub-hypothesis. If it holds, the findings from Spikes 003-004 are not just imprecise but potentially misleading about which strategies are best.

### What this means for experiment design

Testing H1 requires:
- Define 3+ research tasks per profile (mix of exploratory and confirmatory)
- Run agents with different strategy configurations on the same tasks
- Evaluate research output quality (not just which papers were selected)
- Compare strategy rankings under task-based evaluation vs metrics vs list-review

The agent doesn't need to be human-equivalent. It needs to be a consistent evaluator that processes recommendations in a research context rather than in isolation.

---

## H2: Training data determines what kind of relevance a model encodes

### The vague version
"SPECTER2's divergence from MiniLM reflects genuine research-community structure."

### What "reflects" means and why

**Mechanism**: Embedding models learn similarity from their training data. MiniLM was trained on general web text (paraphrase and NLI data) — it encodes vocabulary-level semantic similarity. SPECTER2 was trained on scientific document pairs linked by citation — it encodes citation-community co-membership. GTE was trained on diverse text pairs — it encodes broader semantic similarity that may include methodological or structural patterns MiniLM's training data doesn't cover.

These are different definitions of "similar." Two papers can be similar in vocabulary (MiniLM), similar in citation community (SPECTER2), similar in methodology (GTE, hypothetically), and these similarities can disagree. The disagreements are not noise — they reflect genuinely different aspects of paper relatedness. But whether any particular aspect matters depends on what the researcher is doing.

**Prediction**: The pattern of divergence between models will be predictable from their training data, not random. Specifically:

### Sub-hypotheses

**H2a**: *SPECTER2's divergence from MiniLM will be larger on profiles where citation-community structure diverges from vocabulary similarity.* Specialized domains (Quantum, Math foundations) have distinctive vocabulary that general-purpose models handle well, but they also have citation communities that cross vocabulary boundaries (a quantum computing paper might cite a condensed matter paper using very different language). SPECTER2 should capture these cross-vocabulary citation links.

- Testable on existing data: Compare SPECTER2 divergence across profiles. If divergence correlates with vocabulary specialization of the profile, this supports the mechanism. Spike 004 data shows SPECTER2's lowest tau on P3 (Quantum, tau=0.391 with one seed set) — consistent with prediction, but seed-sensitive.
- Stronger test: If we had citation data for the sample papers, we could directly test whether SPECTER2's divergent papers share more citation links with seeds than MiniLM's divergent papers do.
- Falsification: If SPECTER2's divergence is uniform across profiles (no correlation with domain specialization), the citation-community mechanism is not the explanation.

**H2b**: *Qwen3's vocabulary-match false positives will be predictable from vocabulary overlap.* Qwen3 scored an LLM-training RL paper comparably to robotics RL papers because both share RL vocabulary. This predicts that Qwen3 will produce false positives whenever the profile's core vocabulary appears in adjacent but distinct fields. Profiles with distinctive vocabulary (Quantum) will have fewer false positives than profiles with shared vocabulary (RL, which overlaps with LLM training).

- Testable on existing data: Compare Qwen3's noise rate across profiles. If it correlates with how much the profile's vocabulary overlaps with adjacent fields, this supports the mechanism.
- Falsification: If Qwen3's noise rate is uniform across profiles, vocabulary overlap is not the mechanism.

**H2c**: *Training data composition predicts which profiles each model diverges most on.* This is a generalization of H2a and H2b: not just SPECTER2 and Qwen3, but all models should show divergence patterns predictable from what their training data emphasizes.

- Difficulty: We don't have detailed training data composition for all models. For SPECTER2 (scientific documents + citations) and MiniLM (NLI + paraphrase) we know enough. For Stella, GTE, Qwen3, and Voyage, training data details are less available.
- Falsification: If model divergence patterns are not predictable from training data (they appear random or all models diverge on the same profiles), then training data is not the primary mechanism and embedding architecture or dimension may matter more.

### What this means for experiment design

H2 can be partially tested on existing data (comparing divergence patterns across profiles). The stronger test requires either citation data for the sample papers or constructing profiles from citation-community structure (which connects to H4).

---

## H3: Retrieval method interacts with embedding space geometry

### Mechanism

Centroid retrieval computes the average of seed embeddings and ranks papers by distance from the average. This works well when the "center" of a set of seeds is a meaningful location in embedding space — when the seeds define a convex region and papers near the center are indeed relevant.

kNN retrieval finds papers near each individual seed and aggregates. This works well when individual seed neighborhoods are tight and relevant — when a paper very similar to one seed is likely relevant even if dissimilar to other seeds.

These methods make different demands on embedding space geometry:
- Centroid rewards **smooth, well-separated topic regions** where the average of relevant papers lands in relevant territory
- kNN rewards **tight per-paper neighborhoods** where proximity to any one seed is a strong relevance signal

Models with different dimensionalities and training objectives produce different geometries. SPECTER2's score compression (all scores > 0.95 on some profiles) suggests its space is locally flat — everything near a seed looks equally similar. This is bad for centroid (can't discriminate near the center) but potentially fine for kNN (individual neighborhoods may still be informative). Qwen3's wider score spread suggests more rugged geometry — better for centroid-based discrimination, potentially noisier for kNN.

**Prediction**: There will be significant model × retrieval method interactions. Some models will rank better under kNN than centroid, and this will be predictable from their score distribution properties.

### Sub-hypotheses

**H3a**: *SPECTER2 will benefit more from kNN than centroid, relative to its centroid performance.* The score compression observed in Spike 004 predicts that centroid retrieval underutilizes SPECTER2's information — the centroid can't discriminate when everything scores > 0.95. Per-seed neighborhoods may be more informative.

- Falsification: If SPECTER2 performs equally or worse under kNN vs centroid, the score compression is not masking useful per-seed information — it's genuine lack of discrimination.

**H3b**: *Qwen3 will benefit more from centroid than kNN, relative to its kNN performance.* Qwen3's wider score spread and vocabulary sensitivity predict that individual seed neighborhoods will be noisy (vocabulary-match false positives contaminate per-seed results). Centroid averaging should wash out some noise.

- Falsification: If Qwen3's kNN results are cleaner than its centroid results, the noise is not seed-local but systematic, and averaging doesn't help.

**H3c**: *The optimal retrieval method will be profile-dependent within the same model.* Dense, well-defined profiles (P4 AI safety, P5 Graph NNs) may favor centroid (clear center). Broad, heterogeneous profiles (P2 LM reasoning, P8 Math foundations) may favor kNN (no single center, but individual seeds land in relevant neighborhoods).

- This connects to Spike 003's finding that kNN works for P4 (dense) but not aggregate — extending it to new models.

### What this means for experiment design

Testing H3 requires implementing kNN retrieval for all models (not just MiniLM as in Spike 003). The experiment is: for each model × profile × retrieval method, compute top-20 and evaluate quality. This is a 5 model × 8 profile × 2 method = 80 configuration experiment, computationally cheap on existing embeddings.

---

## H4: Evaluation framework bias determines how much findings are trustworthy

### Mechanism

The interest profiles were constructed from MiniLM BERTopic clusters. What a profile "means" — which papers count as relevant — is determined by where MiniLM draws boundaries in embedding space. A model that draws boundaries differently will disagree with MiniLM not because it's wrong but because it has a different definition of "the same topic."

This is not a measurement error — it's a constitutive feature of the evaluation. The profiles don't represent researcher interests directly; they represent MiniLM's interpretation of researcher interests. Changing the profile construction method changes what "relevant" means.

**Prediction**: Model rankings will change under different profile construction methods, and the magnitude of change will indicate how much the current findings are framework-dependent.

### Sub-hypotheses

**H4a**: *Category-based profiles will produce more uniform model rankings.* Category metadata (e.g., "cs.LG papers about reinforcement learning") is a coarser signal that all models handle similarly. If model rankings converge under category-based profiles, the divergence we observed is partly an artifact of MiniLM-specific profile boundaries.

- Falsification: If category-based profiles produce equally divergent model rankings, the divergence is robust to profile construction method and the MiniLM-entanglement concern is overstated.

**H4b**: *SPECTER2-constructed profiles will make SPECTER2 look better and MiniLM worse.* If we build profiles from SPECTER2's BERTopic clusters instead of MiniLM's, SPECTER2 becomes the incumbent and MiniLM the challenger. If MiniLM's tau vs SPECTER2-as-baseline drops below 0.6 (similar to SPECTER2's current tau vs MiniLM-as-baseline), the framework bias is approximately symmetric — each model looks good when it defines the evaluation.

- Falsification: If MiniLM still dominates even under SPECTER2-constructed profiles, MiniLM is genuinely better for this domain, not just the evaluation framework's favorite.
- This is the most direct test of whether MiniLM's apparent advantage is real or artifactual.

**H4c**: *The framework bias will be larger for some models than others.* Models that structure similarity very differently from MiniLM (Voyage, tau=0.483) should show larger ranking changes under framework switching than models that structure it similarly (GTE, tau=0.637).

- Falsification: If all models show equal ranking changes regardless of their tau distance from MiniLM, the framework bias is not proportional to model difference and the mechanism is wrong.

**H4d**: *If rankings are stable across 3+ profile construction methods, the findings are robust.* This is the convergence criterion: findings that survive evaluation under MiniLM profiles, SPECTER2 profiles, and category profiles can be treated as framework-independent. Findings that change are framework-dependent and must be reported as such.

### What this means for experiment design

Testing H4 requires constructing alternative profiles (a one-time computation per method) and re-running the comparison. It's computationally cheap and addresses the single most threatening assumption in the spike program.

---

## H5: The two-view arrangement has blind spots that matter

### Mechanism

"Truly unique" papers (in a challenger's top-20 but not in MiniLM's or TF-IDF's) exist in a region of the paper space that the current two-view arrangement doesn't cover. The existence of this region is measured (Spike 004). The value of this region is not.

The region could contain:
(a) Relevant papers that MiniLM and TF-IDF miss due to vocabulary differences, different community structure, or different notions of similarity — genuine blind spots
(b) Irrelevant papers that the challenger finds due to noise, false positives, or inappropriate generalization — false discoveries
(c) Papers that are relevant in some research contexts but not others — context-dependent value

If (a) dominates, adding challengers improves the system. If (b) dominates, challengers add noise. If (c) dominates, the question is whether the system can match challengers to contexts.

**Prediction**: The distribution of (a), (b), (c) will vary by model and by profile, predictable from the model's noise characteristics and the profile's specificity.

### Sub-hypotheses

**H5a**: *Truly unique papers will be selected by research agents at higher rates than random papers from outside the top-20.* This is the baseline test: do challengers' unique finds have any value at all?

- Falsification: If selection rates for truly unique papers equal random baseline, the challengers are finding papers that are different but not useful.

**H5b**: *Models with lower noise rates will have higher selection rates for their truly unique papers.* SPECTER2 and GTE (no noise observed in AI reviews) should have higher selection rates than Qwen3 (demonstrated vocabulary-match false positives).

- Falsification: If Qwen3's truly unique papers are selected at equal or higher rates than SPECTER2's, the "noise" we observed isn't noise from the perspective of task completion — what looked like false positives in list-review may be useful in context.

**H5c**: *Papers that are truly unique to multiple challengers will be selected at higher rates than papers unique to a single challenger.* Convergent divergence — multiple independent models finding the same paper that MiniLM misses — is a stronger signal of a genuine blind spot than a single model finding it.

- Falsification: If convergent-divergence papers aren't selected at higher rates, multiple models agreeing doesn't indicate value — it indicates shared failure modes.

**H5d**: *The proportion of (a) vs (b) vs (c) will correlate with profile specificity.* Narrow profiles (P4 AI safety) leave less room for genuine blind spots — the MiniLM + TF-IDF combination covers the well-defined space adequately. Broad profiles (P2 LM reasoning) have more room for valuable papers that the two-view arrangement misses.

### What this means for experiment design

Testing H5 requires the agent-based evaluation from H1 — the agent must be completing research tasks, and we measure which recommendations contribute to the output. The truly unique papers are already identified in the Spike 004 data; the test is whether they prove useful in context.

---

## What should come before these hypotheses are tested

### Pre-spike analyses (existing data, no new experiments)

1. **Model-to-model comparison matrix** — compute tau between all pairs, not just vs MiniLM. Tests whether models cluster into distinct "signal axes" or all just differ from MiniLM similarly.

2. **Seed sensitivity formal characterization** — compute all metrics across all seed subsets, report distributions with confidence intervals. Establishes the noise floor against which findings should be read.

3. **Answer Codex Blocker 3 with existing data** — use the TF-IDF comparison data to assess: does MiniLM + SPECTER2 cover more papers than MiniLM + TF-IDF? (Coverage, not quality — quality requires H5.)

### Infrastructure prerequisites

4. **Profile construction from alternative sources** — build category-based and SPECTER2-based profiles. Required for H4 but also sharpens all other hypotheses by establishing framework robustness before testing.

5. **kNN implementation for all models** — required for H3. Computationally simple on existing embeddings.

6. **Agent research task definitions** — required for H1 and H5. Define specific research tasks per profile (3+ each, mix of exploratory and confirmatory). This is design work, not computation.

### Process prerequisites (GSDR gaps)

7. **Independent design critique** — before executing, dispatch a separate agent to review the experimental design. The Codex review model worked for Spike 004 design but was external to GSDR.

8. **Findings critique protocol** — after execution, before committing findings, dispatch a separate agent to challenge the interpretations.

---

## On the relationship between these hypotheses and research design iteration

These hypotheses are themselves products of the spike program's failures. H1 exists because Spikes 003-004 evaluated with the wrong method. H4 exists because we identified MiniLM-entanglement in the design but didn't address it in execution. H3 exists because we tested models on only one retrieval method.

A better initial design might have prevented some of these — H4 could have been tested from the start if the first spike had built multiple profile sets. But H1 (the evaluation method matters) and H3 (the interaction effect is significant) could only emerge from running Spikes 003-004 and discovering their limitations. You don't know that your evaluation method is insufficient until you've used it enough to see what it misses.

This suggests the iterative structure is not merely a consequence of imperfect design — it's constitutive of experimental work in uncertain domains. Each round produces findings AND reveals the conditions under which those findings hold (or fail to hold). The conditions become the hypotheses for the next round. The research design improves not because we get better at avoiding mistakes but because each round makes a different set of assumptions explicit and testable.

What CAN be improved through process design: catching failures where the execution didn't follow the design's own commitments (MiniLM-centrism identified but not addressed, Jaccard demoted but still sovereign). An independent critic catches these in real-time. What CANNOT be prevented through process design: discovering that the evaluation framework itself constitutes the findings. That's the kind of thing you learn by doing.
