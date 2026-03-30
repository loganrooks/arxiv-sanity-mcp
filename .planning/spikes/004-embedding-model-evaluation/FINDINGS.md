---
spike: "004"
status: complete
date: 2026-03-28
voyage_status: complete (8% embedding failure rate — 160/2000 papers, rate limit)
---

# Spike 004 Findings: Embedding Model Evaluation

## Scope and Conditions

These findings hold for:
- **Corpus**: 2000-paper sample from 19,252 arXiv papers (1% selectivity)
- **Domain**: CS/ML (77% of corpus), 130 categories represented
- **Profiles**: 8 interest profiles constructed from MiniLM BERTopic clusters
- **Assessment**: AI qualitative review (no human judges)
- **Sample validation**: GO (perfect MiniLM baseline, no challenger degeneracy)
- **Voyage-4**: Complete with 8% embedding failure rate (160/2000 papers failed due to API rate limiting). Effective pool ~1840 papers. Findings cover all 5 challengers.

### Standing caveats
- Interest profiles are MiniLM-entangled (constructed from MiniLM BERTopic clusters)
- Sample validated primarily from MiniLM's perspective
- All qualitative judgments are AI-generated substitutes for researcher judgment
- Blind comparison reviews were fully completed for SPECTER2 only; other models' blind reviews contain paper data but limited written assessment. This is a methodology gap — most qualitative depth comes from characterization reviews.

## Methodological Correction

Post-execution analysis revealed that per-profile J@20 is highly seed-sensitive (range up to 0.360 on a single profile depending on which 5 seed papers are used). The classification of all models as "divergent" was based on per-profile J@20 thresholds — the metric the Codex review explicitly warned against giving gatekeeping authority (finding #5), and that PROTOCOL.md Section 2 was designed to de-emphasize.

**Stable metrics tell a clearer story.** Kendall's tau (full ranking correlation) varies by only 0.006-0.013 across seed choices. Mean J@20 varies by 0.033-0.087. The per-profile J@20 headlines in the original synthesis were the noisiest signal; the aggregate picture and tau are robust.

The findings below are corrected to lead with seed-stable metrics. Per-profile J@20 is retained as supplementary detail, not as primary evidence.

## Model Overview

| Model | Dim | Mean tau vs MiniLM | Mean J@100 | Mean J@20 | Embed Time |
|-------|-----|--------------------|-----------|-----------|------------|
| SPECTER2 + adapter | 768 | 0.563 | 0.507 | 0.610 | 49s |
| Stella v5 400M | 1024 | 0.640 | 0.561 | 0.574 | 81s |
| Qwen3-Embedding-0.6B | 1024 | 0.590 | 0.529 | 0.550 | 98s |
| GTE-large-en-v1.5 | 1024 | 0.637 | 0.526 | 0.639 | 117s |
| Voyage-4 | 1024 | 0.483 | 0.499 | 0.575 | ~117 min (API) |

All models show moderate rank correlation with MiniLM (tau 0.48-0.64) — genuinely different rankings, not redundant, not random. Voyage is the most different (tau 0.483); Stella and GTE are the most similar (tau ~0.64). These findings are stable across seed choices (tau range < 0.014 across all seed variants tested).

**Tau stability across seed choices (range across 5 seed variants):**
SPECTER2: 0.006 | Stella: 0.008 | Qwen3: 0.013 | GTE: 0.013 | Voyage: 0.010

## Pre-registered Predictions

| ID | Prediction | Result | Notes |
|----|-----------|--------|-------|
| P1 | Voyage J@20 > 0.717 (Spike 003) on larger sample | **MIXED** | P1: J@20=0.818 (confirmed — higher on larger sample). But P2: J@20=0.333 (dramatically divergent on LM reasoning). Mean 0.575 — Voyage is not redundant, it's profile-dependent. |
| P2 | At least one local model J@20 < 0.7 on 2+ profiles | **CONFIRMED** | All 4 models show J@20 < 0.7 on 3+ profiles. Qwen3 shows < 0.6 on 4/8. |
| P3 | SPECTER2 redundancy holds across all 8 profiles | **FALSIFIED** | SPECTER2 J@20 = 0.379 on P3 (Quantum), 0.538 on P2/P8. Redundancy finding from Spike 003 does not generalize. |
| P4 | Divergent models show qualitatively different paper types | **CONFIRMED** | Each model captures a distinct signal character (see per-model findings) |
| P5 | At least one model has better score separation than MiniLM | **CONFIRMED** | SPECTER2 shows extreme score compression (all >0.95 on P1); Qwen3 shows wider score spread. Both are "different" rather than "better" — score distribution character varies by model. |
| P6 | No single model dominates all 8 profiles | **CONFIRMED** | Model rankings vary substantially by profile. P3 and P6 are the most discriminating profiles. |

### Prediction P3: falsified, but with caveats

Spike 003 found SPECTER2 redundant with MiniLM on P1, P3, P4 (3 profiles, 100-paper pool, 20% selectivity). On the 2000-paper sample, SPECTER2 shows tau=0.563 with MiniLM (moderate correlation, not redundant) and mean J@100=0.507 (roughly half of the top-100 papers differ). This is robust across seed choices.

**Caveat:** The specific per-profile J@20 values (e.g., P3=0.379 with first_5 seeds) are seed-sensitive — the same profile gives J@20=0.739 with different seeds. The falsification rests on the stable aggregate picture (tau, J@100), not on any single per-profile J@20 value.

## Per-Model Findings

### SPECTER2 + proximity adapter

**Classification:** divergent
**Signal character:** Methodological/citation-community similarity. Trained on scientific documents, captures within-community relatedness that general-purpose models miss.

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
| P1 | 0.739 | 0.608 | 0.80 | 0.667 | 3 |
| P2 | 0.538 | 0.658 | 0.70 | 0.481 | 4 |
| P3 | 0.379 | 0.391 | 0.90 | 0.290 | 8 |
| P4 | 0.818 | 0.644 | 0.85 | 0.379 | 2 |
| P5 | 0.667 | 0.505 | 0.85 | 0.538 | 4 |
| P6 | 0.600 | 0.596 | 0.80 | 0.379 | 4 |
| P7 | 0.600 | 0.535 | 0.95 | 0.538 | 3 |
| P8 | 0.538 | 0.547 | 0.85 | 0.290 | 6 |

#### Measurement confidence
High. Jaccard and rank correlation computed correctly on well-validated sample. SPECTER2 re-embedded fresh (not extracted) using correct adapter configuration. Score distributions show consistent behavior across profiles.

#### Interpretation
SPECTER2 captures a genuinely different signal from MiniLM, concentrated in domains with specialized scientific vocabulary (Quantum: J@20=0.379, Math foundations: J@20=0.538). The extremely low J@20 vs TF-IDF (0.290 on P3, P8) confirms SPECTER2 finds papers neither MiniLM nor TF-IDF surface — this is not a redundant signal axis.

Qualitative reviews confirm: on P3 (Quantum), SPECTER2 strongly outperformed MiniLM in blind comparison, with higher-fidelity capture of the variational quantum ML space. On P8, 6 divergent papers formed a coherent extension into KAN theory, implicit bias, mechanistic interpretability. On P1, divergent papers shared RL methodology even when application domains differed.

Score compression is notable: all scores above 0.95 on P1. This may indicate SPECTER2 struggles to differentiate within a coherent topic — everything looks equally relevant. This is a weakness for ranking but potentially a strength for recall.

#### Extrapolation conditions
The SPECTER2 advantage appears strongest on domains with specialized scientific vocabulary (quantum, mathematical foundations) where citation-community structure diverges from general semantic similarity. It is likely less advantageous on mainstream CS/ML topics where vocabulary overlap between MiniLM and SPECTER2 is high (P4 J@20=0.818, P5 J@20=0.818 on Spike 003 data). This finding should hold for other specialized scientific domains but cannot be extrapolated to non-scientific text.

#### Qualitative review summary
SPECTER2 finds papers that share methodology and citation-community membership. Its divergent papers are consistently on-topic but spread along a relevance gradient from directly relevant to methodology-adjacent. Strongest value on specialized scientific domains. Weakness: score compression limits ranking quality within a topic, and no productive provocations observed — SPECTER2 stays within the research community rather than connecting to adjacent ones.

### Stella v5 400M

**Classification:** divergent
**Signal character:** Deployment-realism and practical engineering concerns. Surfaces papers about hardware constraints, real-world deployment, and operational considerations.

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
| P1 | 0.739 | 0.648 | 0.80 | 0.600 | 3 |
| P2 | 0.538 | 0.716 | 0.60 | 0.481 | 3 |
| P3 | 0.429 | 0.545 | 0.85 | 0.429 | 6 |
| P4 | 0.667 | 0.703 | 0.80 | 0.538 | 2 |
| P5 | 0.818 | 0.597 | 0.95 | 0.600 | 2 |
| P6 | 0.379 | 0.658 | 0.75 | 0.333 | 7 |
| P7 | 0.481 | 0.603 | 0.90 | 0.379 | 6 |
| P8 | 0.538 | 0.613 | 0.90 | 0.429 | 4 |

#### Measurement confidence
High. Model loaded correctly with xformers attention. Embeddings are 1024-dim, L2-normalized. Scores and rankings computed consistently.

#### Interpretation
Stella diverges most on P6 (Diffusion, J@20=0.379, 7 truly unique papers) and P7 (Federated learning, J@20=0.481, 6 unique). Its highest tau values (0.716 on P2, 0.703 on P4) suggest it preserves MiniLM's ordering better than other challengers even where overlap is moderate — it finds different papers but ranks the shared ones similarly.

Qualitative review on P1: Stella's 3 divergent papers form a coherent "deployment realism" thread — offline RL augmentation, neural MPC tuning, microrobot control. The microrobot paper (sub-centimeter quadrupedal robot on ARM Cortex-M0) was flagged as the closest thing to a productive provocation across all reviews.

On P7: divergent papers scatter across FL subfields rather than forming a coherent thread. Mixed quality — some genuinely interesting (nonparametric point processes, ECA attack) alongside routine application papers.

#### Extrapolation conditions
Stella's deployment-realism signal is probably a general property of its training data and embedding space, not specific to these profiles. Whether this translates to useful recommendations depends on whether the researcher values practical engineering extensions or prefers staying within the theoretical core. This is a user-situation question, not a model quality question.

#### Qualitative review summary
Stella favors the algorithmic substrate and deployment layer, where MiniLM favors the perception/imitation layer. Divergent papers are consistently on-topic with no noise. On specialized topics (P6, P7), divergence is highest and most interesting. Set-level quality is good — maps research landscapes rather than listing similar papers. Less score compression than SPECTER2.

### Qwen3-Embedding-0.6B

**Classification:** divergent
**Signal character:** Widest divergence of all models but with vocabulary-match noise. Captures both genuine cross-domain connections and false positives from shared terminology.

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
| P1 | 0.538 | 0.599 | 0.75 | 0.538 | 6 |
| P2 | 0.538 | 0.662 | 0.70 | 0.429 | 4 |
| P3 | 0.538 | 0.459 | 0.80 | 0.538 | 4 |
| P4 | 0.667 | 0.680 | 0.85 | 0.481 | 3 |
| P5 | 0.818 | 0.567 | 0.95 | 0.667 | 1 |
| P6 | 0.333 | 0.553 | 0.65 | 0.481 | 6 |
| P7 | 0.538 | 0.599 | 0.90 | 0.379 | 5 |
| P8 | 0.429 | 0.534 | 0.85 | 0.290 | 7 |

#### Measurement confidence
High for the measurements themselves. Qwen3 produced well-formed 1024-dim embeddings. Category recall at 0.65 on P6 is the lowest of any model on any profile — not degenerate but noticeably weaker.

#### Interpretation
Qwen3 is the most divergent model overall (mean J@20 = 0.550, 7 truly unique papers on P8). But the qualitative review revealed a critical distinction: Qwen3's embedding space does not cleanly separate topical relevance from vocabulary overlap. On P1, one clear false positive (DCPO for LLM training) scored comparably to genuinely relevant papers (0.686 vs 0.686), demonstrating that similarity scores in the tail do not reliably distinguish signal from noise.

The genuine finds are real though. The hydraulic quadruped paper (>300 kg robot, first successful RL sim-to-real on heavy hydraulic hardware) was a legitimate discovery that MiniLM missed, possibly because the hydraulic/actuator-modeling framing differs from typical RL robotics vocabulary.

#### Extrapolation conditions
Qwen3's noise problem is likely structural — as a general-purpose embedding model trained on diverse text, shared vocabulary patterns (RL terminology appears in both robotics and LLM alignment) create false associations. This should be expected on any profile where the core vocabulary overlaps with adjacent but distinct fields. Caution warranted when using Qwen3 as a standalone retrieval model; its value may be higher as a diversity signal in multi-view fusion.

#### Qualitative review summary
Most divergent but least reliable. Genuine finds include papers MiniLM misses due to framing differences (hydraulic robotics, microrobot control). But vocabulary-match false positives are a real problem — tail-end scores cannot distinguish relevance from vocabulary overlap. Noise rate estimated at ~1/6 on P1. Best suited as a supplementary signal rather than primary retrieval model.

### GTE-large-en-v1.5

**Classification:** divergent
**Signal character:** Wider methodological envelope. Captures foundational methodology papers that aren't explicitly labeled for the target domain.

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
| P1 | 0.667 | 0.639 | 0.75 | 0.538 | 4 |
| P2 | 0.667 | 0.690 | 0.55 | 0.481 | 2 |
| P3 | 0.600 | 0.506 | 0.75 | 0.667 | 2 |
| P4 | 0.739 | 0.720 | 0.85 | 0.481 | 2 |
| P5 | 0.818 | 0.625 | 0.95 | 0.667 | 1 |
| P6 | 0.538 | 0.623 | 0.70 | 0.481 | 4 |
| P7 | 0.600 | 0.577 | 0.80 | 0.481 | 4 |
| P8 | 0.481 | 0.640 | 0.90 | 0.333 | 6 |

#### Measurement confidence
High. GTE loaded cleanly, produced consistent 1024-dim embeddings. Highest mean tau of all challengers (0.627), indicating GTE preserves MiniLM's ranking structure better while still finding different papers at the top.

#### Interpretation
GTE is the least divergent challenger (mean J@20 = 0.639) and the most correlated with MiniLM (mean tau = 0.627). It finds 1-6 truly unique papers per profile. Its divergent papers on P1 split into two categories: foundational RL methodology (PPO stability, offline RL augmentation, unsupervised meta-learning) and VLM-to-robotics pipelines.

The highest tau values (0.720 on P4, 0.690 on P2) combined with moderate Jaccard suggest GTE and MiniLM agree on paper ordering but disagree at the margin — they have similar "taste" but different edge definitions. Category recall at 0.55 on P2 is notably low, suggesting GTE pulls in cross-category papers on some profiles.

#### Extrapolation conditions
GTE's wider methodological envelope is a modest but real signal. It is the safest challenger to introduce because it causes the least disruption to existing rankings while still surfacing additional papers. Whether the methodological-envelope signal is useful depends on researcher preference for foundational vs applied papers.

#### Qualitative review summary
GTE captures a broader methodological envelope than MiniLM — pulling in foundational work not explicitly labeled for the target domain. Divergent papers are coherent and mildly valuable, extending profiles into methodology substrate without losing topical coherence. No noise observed. No strong productive provocations. The most conservative challenger — least divergent, most correlated, lowest risk.

### Voyage-4

**Classification:** divergent
**Signal character:** Broad semantic similarity with strong profile-dependence. Most MiniLM-like on narrow profiles (P1 RL: J@20=0.818), most divergent on broad conceptual profiles (P2 LM reasoning: J@20=0.333). Lowest mean tau (0.500) of all challengers.
**Limitation:** 8% embedding failure rate (160/2000 papers). Effective pool ~1840 papers.

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
| P1 | 0.818 | 0.525 | 0.80 | 0.538 | 2 |
| P2 | 0.333 | 0.524 | 0.60 | 0.481 | 8 |
| P3 | 0.538 | 0.386 | 0.70 | 0.538 | 3 |
| P4 | 0.667 | 0.582 | 0.85 | 0.481 | 3 |
| P5 | 0.739 | 0.476 | 0.90 | 0.667 | 2 |
| P6 | 0.481 | 0.536 | 0.80 | 0.481 | 6 |
| P7 | 0.481 | 0.468 | 0.95 | 0.481 | 6 |
| P8 | 0.538 | 0.498 | 0.90 | 0.333 | 5 |

#### Measurement confidence
Medium. Voyage embeddings are API-generated with provider-side model that cannot be version-pinned. 8% failure rate means 160 papers are missing from comparisons. These papers never appear in top-K (they score 0), so top-K rankings are valid but computed over a smaller effective pool. Findings are not reproducible at checkpoint level due to potential API model drift.

#### Interpretation
Voyage shows the most extreme profile-dependence of any model: J@20 ranges from 0.818 (P1) to 0.333 (P2). On P1 (narrow, well-defined RL for robotics), Voyage agrees with MiniLM almost completely — 18/20 shared papers. On P2 (broader LM reasoning), it diverges dramatically with 8 truly unique papers.

The blind comparison on P2 was the most consequential Voyage review. The reviewer found the divergent papers are *not noise* — they surface reasoning failure modes and alternative mechanisms that are genuinely valuable and complementary to MiniLM's CoT methodology focus. A model with the lowest quantitative agreement is producing qualitatively excellent recommendations.

The lowest mean tau of all challengers (0.500) suggests Voyage structures the similarity space quite differently from MiniLM at a global level, even where top-K overlap is high.

#### Extrapolation conditions
Voyage's profile-dependence pattern — high agreement on narrow profiles, high divergence on broad conceptual profiles — may be a general property of larger embedding models (1024-dim) vs MiniLM (384-dim). But this cannot be confirmed without testing on additional profiles and domains. The API dependency and 8% failure rate are practical constraints that limit Voyage's utility for this project's local-first architecture.

#### Qualitative review summary
Voyage captures broader conceptual similarity on open-ended profiles. Its P2 divergence was qualitatively validated as the most interesting finding of the entire spike — reasoning failure modes and alternative reasoning mechanisms that none of the other models or TF-IDF surface. But: API dependency, provider drift risk, rate limiting, and 8% failure rate make it operationally problematic. The signal is real; the delivery mechanism is unreliable for local-first deployment.

## Cross-Model Analysis

### Signal axes identified

The four challengers cluster into distinct signal types:

1. **Citation-community (SPECTER2)**: Trained on scientific documents, captures within-community relatedness. Strongest on specialized scientific vocabulary domains.
2. **Deployment-realism (Stella)**: Surfaces practical engineering and deployment considerations. Favors algorithmic substrate over perception layer.
3. **Vocabulary-sensitive general (Qwen3)**: Widest aperture, captures cross-domain vocabulary matches. Includes both genuine finds and noise.
4. **Methodological-envelope (GTE)**: Widens the methodological scope of recommendations. Most conservative, highest correlation with MiniLM.

These are genuinely different signal axes, not different rankings of the same papers. The "truly unique" counts (papers in Model X's top-20 but in neither MiniLM's nor TF-IDF's) range from 1-8 per profile, confirming each model accesses a region of the paper space that the current MiniLM + TF-IDF arrangement misses.

### MoReBRAC observation

The offline RL data augmentation paper "MoReBRAC" appeared as a divergent pick for SPECTER2, Stella, and GTE — three of four challengers found it, but MiniLM did not. This suggests a potential systematic MiniLM blind spot for papers framed as general-purpose methodology rather than domain-specific application.

### TF-IDF comparison frame

All challengers show very low J@20 vs TF-IDF (mean 0.29-0.54 across profiles). This means the embedding models and TF-IDF find substantially different papers, as expected. More importantly, all challengers find papers that **both** MiniLM and TF-IDF miss (the "truly unique" column). This is evidence for a third signal axis beyond the current two-view architecture.

No challenger is a better *replacement* for MiniLM — they diverge too much to serve as drop-in substitutes. The question is whether any is a valuable *third view*.

### Profile dependence

Model rankings vary substantially by profile:

| Profile | Most unique model | Least unique model | Most discriminating |
|---------|------------------|-------------------|-------------------|
| P1 (RL robotics) | Qwen3 (6) | — | Moderate |
| P2 (LM reasoning) | Qwen3/SPECTER2 (4) | GTE (2) | Moderate |
| P3 (Quantum) | SPECTER2 (8) | GTE (2) | **High** — SPECTER2 excels |
| P4 (AI safety) | Qwen3 (3) | SPECTER2/Stella/GTE (2) | Low — models converge |
| P5 (Graph NNs) | SPECTER2 (4) | GTE/Qwen3 (1) | Low — all converge |
| P6 (Diffusion) | Stella (7) | — | **High** — Stella/Qwen3 diverge most |
| P7 (Fed learning) | Stella (6) | SPECTER2 (3) | Moderate |
| P8 (Math foundations) | Qwen3 (7) | — | **High** — all models diverge |

P3, P6, and P8 are the most discriminating profiles — they show the largest model differences and are the profiles where a third view would add the most value.

## Methodology Notes

### Anomalies encountered during execution
1. **Environment dependency chain breakage.** Installing xformers (required by Stella v5) pulled torch 2.11/CUDA 13.0, incompatible with the GTX 1080 Ti's CUDA 12.4 driver. Required downgrading to torch 2.7.0+cu126. This is a practical constraint: Stella requires xformers, which constrains the torch/CUDA version range.

2. **Universal divergence.** All models classified "divergent" — the protocol's mid-overlap, high-overlap, and near-identical tiers were unused. The branch logic designed in PROTOCOL.md Section 2 was unnecessary because no model fell into those bands. This means all models received full 8-profile review (32 total reviews), which was more work than anticipated but provided comprehensive coverage.

3. **Blind review completeness gap.** Only SPECTER2's blind comparison reviews received full written assessments from the review agents. Other models' blind reviews contain paper data but limited interpretive text. This weakens the blind comparison evidence for Stella, Qwen3, and GTE. The characterization reviews (non-blind) are thorough for all models.

4. **GTE repo ID correction.** The DESIGN.md listed `thenlper/gte-large-en-v1.5` but the correct repo for v1.5 is `Alibaba-NLP/gte-large-en-v1.5`. The `thenlper` org hosts the older non-v1.5 model. Caught during model gating check before execution.

### Where this spike could not see

From DESIGN.md, updated with execution-time discoveries:
1. **The 2000-paper sample** — effects visible only at full corpus scale will be missed
2. **MiniLM-entangled profiles** — category-based recall partially addresses but doesn't eliminate
3. **AI qualitative review biases** — unknown and undetectable without human comparison
4. **CS/ML domain** — cannot generalize beyond this domain
5. **The absent researcher** — AI reviewer substitutes for researcher judgment about value
6. **Score distribution as quality proxy** — we noted score compression (SPECTER2) and wide spread (Qwen3) but cannot determine which is better without knowing the researcher's browsing behavior
7. **NEW: Blind review coverage gap** — only SPECTER2 had complete blind assessments. The comparative evidence for other models relies on non-blind characterization reviews, which may be biased by knowing the model identity.

### What exceeded the design

Per principle 20: what happened that DESIGN.md couldn't hold.

1. **The degree of universal divergence was not anticipated.** The design's branch logic assumed a spectrum from redundant to divergent. Instead, every model is substantially divergent from MiniLM on the 2000-paper sample. This changes the framing from "does anything beat MiniLM?" to "which of several genuinely different signals are most valuable?"

2. **The MoReBRAC convergence.** Three challengers independently surfacing the same paper that MiniLM missed was not anticipated by any metric in the design. It suggests systematic MiniLM blind spots that the methodology can detect only as individual divergent papers — the design didn't include a "convergent divergence" instrument.

3. **Score compression as a signal.** SPECTER2's extreme score compression (all >0.95 on P1) is not noise — it reflects how SPECTER2 structures the similarity space. The design treated score distribution as a diagnostic metric but it may be a more fundamental model property than anticipated.
