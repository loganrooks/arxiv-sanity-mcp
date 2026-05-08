---
question: "Do embedding models beyond MiniLM (Voyage-4, Stella v5, Qwen3-Embedding, GTE-large) capture signals that MiniLM misses, and if so, what kind?"
type: comparative
status: design-reviewed
round: 1
linked_deliberations:
  - spike-epistemic-rigor-and-framework-reflexivity.md (methodology — Codex-reviewed 2026-03-23)
  - responsibility-alterity-and-methodological-praxis.md (ethical orientation — Codex-reviewed 2026-03-23)
design_review:
  - date: 2026-03-23
    reviewer: codex-gpt-5.4
    scope: sibling deliberations reviewed; narrowed recommendations toward thinner first-pass hardening
    implication_for_this_spike: >
      The meta-methodology section is diagnostic, not additional protocol. Execute the
      experiment phases as designed. Use the meta-methodology as an interpretive lens
      for reading findings, not as extra steps to perform.
depends_on:
  - 003 (corpus, embeddings, interest profiles, evaluation framework, qualitative review protocol)
  - 003 epistemic qualifications (three-level confidence, methodology failures)
addresses:
  - "003 deferred: Do API embeddings add value? (Voyage screening inconclusive)"
  - "003 deferred: Would a different second view model be better than TF-IDF?"
  - "sig-2026-03-20-jaccard-screening-methodology (corrected methodology)"
methodological_improvements_over_003:
  - Representative sample (2000 papers, 1% selectivity vs 100 papers, 20%)
  - Multiple comparison metrics (not Jaccard alone)
  - Mandatory qualitative review before any verdict
  - Pre-registered predictions with falsification criteria
  - Three-level confidence framework for all findings
  - This DESIGN.md to be reviewed before execution
---

# Spike 004: Embedding Model Evaluation

## Question

Do embedding models beyond MiniLM — specifically Voyage-4 (API), Stella v5 400M, Qwen3-Embedding-0.6B, and GTE-large-en-v1.5 (local) — capture signals that MiniLM misses for academic paper recommendation? If so, what kind of signal, for which interest profiles, and at what cost?

This spike exists because Spike 003's Voyage screening was methodologically insufficient (sig-2026-03-20-jaccard-screening-methodology). The verdict was changed from STOP to INCONCLUSIVE. This spike re-evaluates with corrected methodology.

## What this spike is NOT

This spike does not re-evaluate the full strategy landscape. Spike 003's decided findings (strategy complementarity, fusion default-off, TF-IDF scale limits, eliminations) stand. This spike addresses only the deferred questions about embedding model selection.

## Why this matters

Spike 003's architecture decision — "MiniLM as primary, TF-IDF as second view" — is provisional. If Voyage or a local model captures a genuinely different signal, the architecture may need revision. The evaluation framework's entanglement with MiniLM (sig-2026-03-20-spike-experimental-design-rigor) means we cannot confidently claim MiniLM is optimal. A proper comparison requires:

1. Metrics that don't privilege MiniLM's representation
2. Qualitative assessment of what different models find differently
3. Testing across all 8 interest profiles, not a subset

## Epistemic position

This spike is designed in awareness of its own constitutive limitations:

- **The evaluation framework is still partially MiniLM-entangled.** Interest profiles were constructed from MiniLM-based BERTopic clusters. We can mitigate this (use category-based ground truth alongside cluster-based) but cannot fully eliminate it without rebuilding profiles from scratch.
- **Every metric constitutes what it measures.** Rank correlation, Jaccard, qualitative review — each makes different aspects visible and others invisible. We use multiple metrics not because their average is "more objective" but because their disagreements reveal the phenomenon's complexity.
- **Qualitative review is AI-generated.** It catches things metrics miss (Spike 003 demonstrated this repeatedly) but may have systematic biases we can't detect without human evaluation.
- **2000 papers is better than 100 but still a sample.** The full corpus is 19,252. Effects that emerge only at full scale won't be visible.

These limitations don't invalidate the spike. They define the conditions under which its findings hold.

## Assumptions

| ID | Assumption | Confidence | Falsified if |
|----|-----------|------------|-------------|
| A1 | The 2000-paper representative sample preserves the corpus's distributional properties well enough for model comparison | High (stratified sampling, 130/130 categories, temporal coverage) | Strategy rankings on 2000-paper sample differ dramatically from rankings on full 19K corpus for MiniLM (our baseline) |
| A2 | Embedding models that capture genuinely different signals will produce substantially different top-20 neighbor lists (Jaccard < 0.6 AND qualitative difference) | Medium | Models with low Jaccard produce qualitatively similar papers (different papers, same kind of relevance) |
| A3 | All-MiniLM-L6-v2 as currently deployed is a reasonable baseline for comparison | High | MiniLM is misconfigured or there's a better version available |
| A4 | The Voyage free tier (3 RPM, 10K TPM) is sufficient for 2000-paper embedding | Low (estimated 2.2 hours) | Rate limiting makes it impractical; would need paid tier |
| A5 | Local models (Stella, Qwen3, GTE) will run on GTX 1080 Ti (11GB VRAM) | Medium | Model exceeds VRAM; would need CPU fallback or quantization |

## Models to evaluate

| Model | Dim | Source | Size | Status | Why include |
|-------|-----|--------|------|--------|-------------|
| all-MiniLM-L6-v2 | 384 | Local (downloaded) | 80MB | Baseline | Current primary model |
| SPECTER2 + adapter | 768 | Local (downloaded) | 440MB | Comparison | Spike 003 found redundant with MiniLM qualitatively — verify on broader profile set |
| voyage-4 | 1024 | API (Voyage) | — | **Primary target** | Spike 003 screening inconclusive; need proper evaluation |
| dunzhang/stella_en_400M_v5 | 1024 | Local (download needed, ~1.5GB) | 1.5GB | Screening | Best general-purpose model from 003 landscape research |
| Qwen/Qwen3-Embedding-0.6B | — | Local (download needed, ~2.4GB) | 2.4GB | Screening | Recent (2025), strong benchmarks, instruction-tunable |
| thenlper/gte-large-en-v1.5 | 1024 | Local (download needed, ~670MB) | 670MB | Screening | Solid performer, moderate size |

**Note on SPECTER2:** Spike 003 W5.4 found it redundant with MiniLM on P1, P3, P4. But this was 3/8 profiles with AI review. Including it here across all 8 profiles either confirms the redundancy finding or reveals it was profile-dependent.

## Methodology

### Why this methodology rather than another

This spike's experimental design embodies specific commitments about what counts as evidence and how evidence relates to conclusions. Making these explicit helps both execution (agents know what the methodology demands) and critique (reviewers can challenge the commitments, not just the execution).

**Commitment 1: Multiple metrics are not redundant — they're constitutive of different aspects of the phenomenon.** Jaccard, rank correlation, score distribution, category recall, and qualitative review don't measure the same thing with varying accuracy. Each constitutes a different aspect of "model difference" as an observable phenomenon. Jaccard constitutes it as a binary overlap question. Rank correlation constitutes it as an ordering question. Qualitative review constitutes it as a relevance-and-character question. When they disagree, the disagreement is the most informative data — it reveals that "model difference" is not one thing but several, and the choice of instrument determines which one you see.

This is why Spike 003's Voyage screening failed: it used one instrument (top-K Jaccard on a small pool) and treated its reading as the answer, when it was detecting one aspect of a multi-aspect phenomenon. The corrective is not "better metrics" but "multiple metrics whose disagreements are taken seriously."

**Commitment 2: Qualitative review is a first-class evaluation method, not validation of quantitative findings.** Quantitative instruments detect patterns; qualitative review interprets what those patterns mean. When they disagree (as they did repeatedly in Spike 003 — SPECTER2 redundancy, fusion profile-dependence, kNN niche utility, TF-IDF undervaluation), neither is wrong. They're producing different kinds of knowledge. The qualitative review is mandatory not because it's "more rigorous" but because it provides knowledge the instruments structurally cannot: what *kind* of papers a model finds, whether divergence is signal or noise, whether the researcher would actually value what the model surfaces.

**Commitment 3: The evaluation framework's entanglement with MiniLM is a condition to acknowledge, not a problem to solve.** The interest profiles were built from MiniLM BERTopic clusters. Rebuilding them from scratch would be expensive and would introduce different biases (whatever model or method we used instead). The honest approach is to use the profiles we have, supplement with model-independent ground truth (category-based recall), and be explicit about where MiniLM entanglement affects interpretations. Every finding carries this caveat; repeating it everywhere would be noise, but forgetting it anywhere would be dishonest.

**Commitment 4: Negative and inconclusive results are findings, not failures.** If Voyage adds nothing, that's informative. If no model beats MiniLM, that's informative. If the methodology itself proves inadequate mid-execution, that's the most informative finding of all. The spike doesn't need to "succeed" in the sense of finding a better model. It needs to produce honest, qualified answers to its questions.

### Where this methodology came from

This design is a direct response to five documented methodological failures in Spike 003:

| Spike 003 failure | Signal | How this spike addresses it |
|-------------------|--------|---------------------------|
| 100-paper pool with 20% selectivity | sig-2026-03-20-jaccard-screening-methodology | 2000-paper sample with 1% selectivity, plus sample validation gate |
| Jaccard as sole metric | sig-2026-03-20-jaccard-screening-methodology | 7 quantitative instruments + mandatory qualitative review |
| 3/4 qualitative checkpoints skipped | sig-2026-03-20-spike-experimental-design-rigor | Qualitative review is a blocking gate in the experiment design, not an optional step |
| Conclusions overstated relative to evidence | sig-2026-03-20-premature-spike-decisions | Three-level confidence framework; "decision deferred" as legitimate outcome; pre-registered predictions |
| Extension experiments designed ad-hoc | sig-2026-03-20-spike-experimental-design-rigor | Single design covering all models; no ad-hoc extensions without design review |

This traceability is itself a methodological commitment: the design doesn't just improve on Spike 003, it shows *how* and *why* each improvement addresses a specific documented failure. A future reviewer can assess whether the improvements actually resolve the failures they claim to address.

## Meta-methodology

The methodology section describes what this spike does and why. This section examines the commitments the methodology embodies and what they foreclose — not to relativize the methodology but to make its scope explicit so that findings can be held with appropriate force.

These commitments are stated as claims, with reasons, because they need to do work: make foreclosures visible, inform how findings are interpreted, enable critique during and after execution. They are also held as revisable — not because all readings are equally valid, but because any articulation of a methodology's commitments is an attempt to say something that exceeds the saying. The articulation is the best we can offer; it is not beyond interruption.

### The methodology's commitments

Each commitment below is stated with what it enables and what it forecloses, and an assessment of whether the foreclosure is an acceptable cost for this spike's question.

**1. Output-level comparison.** The methodology compares models by their top-K recommendation lists — what they surface for given seed papers. This is appropriate for the spike's question ("do models capture different signals for recommendation?") because recommendation IS an output-level phenomenon. A researcher experiences outputs, not embeddings.

But this framing makes representational differences invisible. A model that structures the full 2000-paper similarity landscape differently from MiniLM — creating neighborhoods that correspond to meaningful research communities, or capturing relationships MiniLM flattens — would not show this in the top-K unless the structural difference happens to manifest for our 8 profiles and seed sets. Whether this is an acceptable cost depends on whether we care about the embedding space as a research artifact or only about its recommendation outputs. For this spike: acceptable. For broader architectural decisions about the embedding layer: potentially not.

**2. Per-paper relevance assessment.** The qualitative review assesses each recommended paper: is this paper relevant to the seeds? This matches how researchers encounter recommendations (one paper at a time). But relevance might also be a set-level property — twenty papers that together map a research landscape might be more valuable than twenty individually relevant but redundant papers. The review template has a set-level section, but it's structured as summary rather than independent assessment.

This is partially addressable within the current design: the set-level assessment could be given more weight in the review protocol, and "landscape-mapping" could be named as an explicit quality dimension. Whether to do this depends on whether the added complexity is warranted by the spike's question. For model comparison specifically, per-paper assessment plus diversity metrics may be sufficient. Flag for the qualitative reviewers to attend to set-level properties even if the template emphasizes per-paper.

**3. Divergence as the interesting thing.** The three criteria for "genuinely different signal" all reference what one model finds that another doesn't. This foregrounds difference and backgrounds agreement. A model that recommends the same papers as MiniLM but ranks them better (better score calibration, better ordering for browsing) would be dismissed as redundant. Kendall's tau captures rank correlation quantitatively, but the qualitative review doesn't systematically examine whether rank order affects the recommendation experience.

Partially addressable: for models with high Jaccard (>0.9), compare rank ordering qualitatively rather than dismissing them as redundant. A model that agrees on *what* to recommend but disagrees on *priority* might be meaningfully different in practice.

**4. Disciplinary scope.** All 8 profiles are CS/ML topics. The corpus is 77% CS. For this project — an arXiv CS/ML discovery tool — this is appropriate scoping, not a hidden assumption. The evaluation tests within the deployment domain.

The foreclosure is real but deliberate: a model that excels at interdisciplinary connection won't show its value here. This is the right tradeoff for this spike. If all models look similar on CS/ML profiles, the question "do they differ on interdisciplinary profiles?" becomes a potential follow-up, not a current gap.

**5. Relevance as the quality criterion.** The methodology asks "is this paper relevant to the research interest?" But researchers also want to be surprised, challenged, or shown perspectives they wouldn't seek. The qualitative review can detect "productive provocation" in its emergent observations section, but the template frames relevance as primary. This is appropriate for comparing recommendation models (relevance is the minimum viable property) while acknowledging that the most interesting differences between models might show up in what kind of *irrelevant* papers they surface — noise vs productive tangent.

### What this analysis means for execution

The methodology is well-scoped for its question. Most foreclosures are acceptable costs. Two are partially addressable without overhaul:

1. **Set-level assessment**: Instruct qualitative reviewers to attend to whether a recommendation set maps a landscape, not just whether individual papers are relevant. Add as a named dimension, not just a summary section.
2. **Rank-order for high-Jaccard models**: If a model produces Jaccard > 0.9 with MiniLM, compare rank ordering qualitatively before dismissing as redundant. A model that agrees on *what* but disagrees on *priority* may be meaningful.

Findings from this spike should carry scope markers: they hold for output-level comparison of recommendation quality within CS/ML interest profiles, assessed by AI qualitative review. Extrapolation beyond this scope (to other domains, to representational claims about embedding spaces, to claims about what human researchers would prefer) requires different evidence.

This analysis of commitments is itself revisable. If execution surfaces a commitment not identified here, or reveals that a foreclosure identified as acceptable is actually distorting findings, the analysis should be updated — and the fact that it was updated should be recorded, not erased.

### Practical failure modes

Distinct from the interpretive reading above, the methodology has practical vulnerabilities that are more straightforwardly checkable:

1. **Shared metric blind spot.** All quantitative metrics operate over the same top-K lists. Full-space structural differences between models are invisible. (This overlaps with observation #1 above but is also a practical point — adding a full-space metric like embedding-space clustering would partially address it.)
2. **AI reviewer bias.** If the reviewer's implicit notion of "relevant" aligns with MiniLM's, it will systematically favor MiniLM-like models. Blind comparison partially mitigates but doesn't eliminate.
3. **Sample effects.** The 2000-paper sample is 10% of the corpus. Effects dependent on candidate pool density may be understated. Mitigated by sample validation gate.
4. **Profile coverage.** 8 CS/ML profiles may not span the space where model differences matter. Acknowledged as deliberate scoping, not oversight.

### Responsiveness during execution

This spike's methodology emerged from a situated critique of Spike 003, driven by specific philosophical commitments developed through dialogue. A different conversation would have produced a different methodology. This doesn't make the methodology arbitrary — the critique identified real failures with documented evidence — but it means the methodology is one response to those failures, not the only possible one.

If during execution something doesn't fit — a metric seems to be measuring the wrong thing, the qualitative review feels perfunctory, the sample validation gate produces an ambiguous result, or an anomaly suggests the commitments identified above are actively misleading — the appropriate response is not to proceed mechanically but to pause and ask whether the methodology needs revision. The DESIGN.md is a plan, not a contract. Deviations should be documented, not hidden, but they should be possible.

The protocol makes responsiveness possible (by providing structure against which anomalies become visible) and makes responsiveness difficult (by creating inertia toward "following the plan"). Holding both — structure and openness to what exceeds it — is the condition of doing this kind of work.

## Sample

Using the representative 2000-paper sample built during Spike 003 review session:
- `experiments/data/sample_2000.json` (in Spike 003 directory)
- 2000 papers: 160 profile papers (guaranteed) + 1400 category-stratified + 440 random
- 130/130 categories represented
- Temporal: 2023-2026 stratified
- Selectivity: top-20 from 2000 = 1% (vs 0.1% full corpus, vs 20% in Spike 003 Voyage screening)

### Sample validation (pre-execution check)

Before running experiments, verify representativeness — but not only from MiniLM's perspective:

1. **MiniLM validation**: MiniLM top-20 on sample vs full 19K for 3 profiles (P1, P3, P4). If Jaccard > 0.8, the sample preserves MiniLM's neighborhoods.
2. **Challenger validation**: After embedding the sample with all models (Phase 1), verify that each model's top-20 on the 2000-paper sample isn't degenerate — i.e., that the sample contains enough papers in each model's neighborhoods to produce meaningful recommendations. A model whose top-20 scores are all near-zero or near-identical suggests the sample doesn't contain the papers that model would find relevant.
3. **This is a go/no-go gate.** If the sample works for MiniLM but not for a challenger model, the sample is biased toward MiniLM. In that case: expand the sample with additional papers from the challenger's high-scoring regions of the full corpus.

The concern: validating the sample using only the baseline model guarantees the playing field works for the incumbent but not for the challengers. A sample that preserves MiniLM's similarity structure might not preserve Voyage's. This is a structural advantage for MiniLM that should be checked, not assumed away.

## Metrics

### Why multiple metrics

Spike 003 demonstrated that single metrics mislead: Jaccard said Voyage was redundant; but Jaccard at 20% selectivity on 100 papers collapses model differences. MRR said MiniLM was 4x better than TF-IDF; qualitative review showed they're complementary with similar on-topic rates. No single metric tells the full story. Multiple metrics, including their disagreements, are the data.

### Quantitative instruments

| Metric | What it detects | What it cannot detect | MiniLM bias? |
|--------|----------------|----------------------|-------------|
| **Rank correlation (Kendall's tau)** | How correlated are the full rankings of two models, not just top-K | Whether correlated rankings are both good or both bad | Low — compares rankings, not cluster membership |
| **Top-K Jaccard (K=20, 50, 100)** | Binary overlap at multiple thresholds | Nature of divergence; boundary effects reduced at higher K | Low — symmetric comparison |
| **Score distribution analysis** | Score spread, separation between relevant/irrelevant, ranking informativeness | Whether well-separated scores correspond to actual quality | None — model-internal property |
| **Semantic clustering of divergent papers** | Whether model-unique papers form a coherent pattern (signal) or are scattered (noise) | Whether the coherent pattern is actually useful | Medium — clustering itself uses embeddings |
| **Per-profile Jaccard** | Whether model agreement varies by interest profile | Why it varies | Low |
| **LOO-MRR** | How well the model recovers held-out papers from known-coherent clusters | Circular for MiniLM; useful only as within-model check | **HIGH** — clusters defined by MiniLM. Use as reference, not decision criterion. |
| **Category-based recall** | How many papers from seed-matching categories appear in top-K | Whether category matching equals relevance | None — metadata-based, model-independent |

### Qualitative review

**Mandatory checkpoint.** No model verdict may be issued without qualitative review. This is a blocking gate, not an optional validation step.

For each model that shows quantitative divergence from MiniLM (Jaccard < 0.8 at K=20 on any profile):

1. **Review the divergent papers.** For each profile, examine the papers Model X finds that MiniLM doesn't. Are they:
   - Relevant but using different vocabulary? (Genuinely different signal — valuable)
   - From adjacent communities with shared methodology? (Cross-community — potentially valuable)
   - Productive provocations — not "relevant" in the standard sense but would genuinely serve a researcher by challenging assumptions, opening new directions, or connecting to adjacent fields? (Potentially the most valuable kind of difference)
   - Random noise? (Model instability — not valuable)
   - Vocabulary matches without conceptual relevance? (False positives — not valuable)

2. **Review using the W1 template** from Spike 003 (per-paper narrative assessment, set-level assessment, emergent observations, metric divergence flags). **Addition to template for this spike:** the set-level assessment should explicitly address whether the recommendation set *as a whole* maps a research landscape — not just whether individual papers are relevant. Does the set tell a story? Does it cover different aspects of the interest (methods, applications, critiques, foundations)?

3. **Blind comparison** where feasible: reviewer sees "Model A" and "Model B" without knowing which is MiniLM. This prevents confirmation bias toward the familiar model.

4. **Attend to what the review can't capture.** The reviewer is an AI model, not the researcher who would actually use these recommendations. The reviewer's notion of "relevant" or "valuable" is itself situated. The review should include a section noting: "What would I need to know about the researcher's actual situation to assess this recommendation set properly? What am I assuming about their needs?" This doesn't fix the absent-researcher problem — it preserves the trace of the absence so that findings carry the awareness of whose judgment is missing.

### What counts as "a genuinely different signal"

A model adds value if:
1. It finds papers MiniLM misses (Jaccard < 0.8) **AND**
2. The different papers are qualitatively valuable (not noise) **AND**
3. The value is of a *different kind* than MiniLM provides (not just a slightly different ranking of the same kind of paper)

**OR** if it meets criteria 1+2 without criterion 3 but provides meaningfully higher recall (finds more relevant papers of the same kind). A model that's not a new signal axis but is simply better at what MiniLM does is still a finding worth reporting.

**OR** if it meets none of the above on the 8 CS/ML profiles but the qualitative reviewer flags papers that suggest the model might perform differently in a context our profiles don't cover (interdisciplinary, non-CS, different research mode). This is not a positive verdict — it's a flag for further investigation under different conditions.

Note on "valuable" vs "relevant": the qualitative reviewer should be explicitly invited to notice value beyond standard relevance — papers that would challenge the researcher's assumptions, open unexpected directions, or connect to adjacent fields in productive ways. A model that produces more "productive provocations" alongside its relevant papers may be more valuable than one that produces only safe, obviously-relevant recommendations. Whether this constitutes "value" is itself a judgment the reviewer should make and justify, not assume.

## Pre-registered predictions

These are recorded before any experiments run so they cannot be retrofitted.

| ID | Prediction | Falsified if |
|----|-----------|-------------|
| P1 | Voyage-4 will show higher Jaccard with MiniLM on the 2000-paper sample (>0.8) than on the 100-paper sample (0.717), because the larger pool enables more selective top-K | Voyage Jaccard on 2000-paper sample is LOWER than on 100-paper sample |
| P2 | At least one local model (Stella, Qwen3, or GTE) will have Jaccard < 0.7 with MiniLM on at least 2 profiles, indicating a potentially different signal | All local models show Jaccard > 0.8 with MiniLM across all profiles |
| P3 | SPECTER2 redundancy with MiniLM (found in 003 W5.4) will hold across all 8 profiles | SPECTER2 shows Jaccard < 0.6 with MiniLM on 2+ profiles not tested in 003 |
| P4 | Models that show quantitative divergence from MiniLM will show qualitatively different paper types (not just different papers of the same type) | Qualitative review finds divergent papers are the same kind as MiniLM's, just ranked differently |
| P5 | Score distribution analysis will reveal at least one model with better score separation than MiniLM (which has spread ~0.053) | All models have equal or worse score separation |
| P6 | No single model will dominate across all 8 profiles — profile-dependence will persist | One model is strictly better than MiniLM on all profiles by qualitative assessment |

## Experiment design

### Phase 1: Embed and compute (parallelizable)

1. **Embed 2000-paper sample with all 6 models.**
   - MiniLM and SPECTER2: extract from existing 19K embeddings (no new computation)
   - Voyage-4: API call. ~2.2 hours at free tier. Run as background task.
   - Stella v5, Qwen3, GTE: download models, embed on GPU. Estimate ~5-15 min each.

2. **Sample validation gate.** Before proceeding: compare MiniLM top-20 on sample vs full corpus for P1, P3, P4. If Jaccard > 0.8, sample is representative. If not, stop and redesign.

### Phase 2: Quantitative comparison (parallelizable per model)

For each model vs MiniLM:
1. Compute Kendall's tau (full ranking correlation) across all 8 profiles
2. Compute Jaccard at K=20, 50, 100 per profile
3. Compute score distribution (spread, separation, informativeness)
4. Compute LOO-MRR (as reference, not decision criterion — document entanglement caveat)
5. Compute category-based recall (model-independent ground truth)
6. Cluster the divergent papers (papers in Model X top-20 but not MiniLM top-20) — do they form coherent groups?

**Branch point:** Models with Jaccard > 0.9 with MiniLM across all 8 profiles proceed to a lightweight qualitative check (3 profiles, abbreviated review — are the few divergent papers interesting or noise?) before being classified as redundant. A model that's quantitatively redundant on 7/8 profiles but diverges meaningfully on 1 may still be worth offering for that profile's domain. Models with Jaccard < 0.8 on any profile proceed to full Phase 3 qualitative review.

### Phase 3: Qualitative review (mandatory — blocking gate)

For each model that passed the Phase 2 branch point:
1. Single-strategy characterization review across P1, P3, P4 (medium, narrow, broad) — same protocol as Spike 003 W1
2. Blind pairwise comparison with MiniLM across the 2 profiles showing most divergence
3. Emergent observation section: what kind of papers does this model find that MiniLM misses? Is it a genuinely different signal or just noise?

**This is the decision point.** The qualitative review determines whether quantitative divergence translates to qualitative value.

### Phase 4: Synthesis

1. For each model: measurement confidence, interpretation, extrapolation conditions
2. Architecture implications: does the two-view architecture need revision?
3. If a model adds genuine value: what should the view be called? What does it find?
4. Update Spike 003 deferred decisions with evidence
5. Honest limitations section: what this spike can and cannot tell us

## Practical constraints

| Constraint | Limit | Mitigation |
|-----------|-------|-----------|
| GTX 1080 Ti (11GB VRAM) | Stella v5 400M and Qwen3 0.6B may be tight | Batch embedding, quantized loading if needed |
| Voyage free tier (3 RPM) | ~2.2 hours for 2000 papers | Run as background task; or add payment method for 300 RPM |
| Disk space (~80GB free on /home) | Model downloads ~5GB total | Acceptable |
| No human judges | All quality assessment is AI-generated | Acknowledge in confidence framework |

## Success criteria

This spike succeeds if it provides grounded answers to:

| # | Question | What "grounded" means |
|---|----------|----------------------|
| 1 | Does Voyage-4 capture a different signal than MiniLM? | Quantitative (multiple metrics) + qualitative review, on representative sample, across all 8 profiles |
| 2 | Do any local models add value over MiniLM? | Same evidence standard as #1 |
| 3 | Is the SPECTER2 redundancy finding from 003 robust? | Tested on 8 profiles (was 3), with qualitative review |
| 4 | Should the two-view architecture be revised? | Evidence-based recommendation with three-level confidence, considering user context (API dependency, hardware requirements, local-first values) |
| 5 | What kind of signal does each valuable model capture? | Qualitative characterization with narrative evidence |
| 6 | What user situations does each model serve? | Access requirements (API key, GPU, disk), cost implications, operational dependency, alignment with local-first architecture values |

Success criterion 6 is important because a model that's marginally better but requires API dependency might be the wrong recommendation for users who value local-first operation — or the right recommendation for users who prioritize quality over independence. The spike should provide the information for users to make this judgment, not make it for them.

## Where this spike cannot see

This section records the known limits of this spike's methodology so they don't need to be discovered later.

1. **The 2000-paper sample is still a sample.** Effects visible only at full corpus scale (19K+) will be missed. The sample validation gate mitigates this partially.
2. **Interest profiles are MiniLM-entangled.** The profiles were built from MiniLM BERTopic clusters. Category-based recall partially addresses this, but a model that finds papers MiniLM wouldn't cluster together is still penalized by profile-based metrics.
3. **AI qualitative review has unknown biases.** The reviewer may systematically prefer certain kinds of recommendations. We can't detect this without human comparison.
4. **One month of data.** Temporal effects, seasonal variation, conference deadlines may affect which models work best.
5. **CS/ML domain.** Findings may not generalize to physics, math, biology, or non-arXiv literature.
6. **The question "what kind of signal?" is interpretive.** Two reviewers might characterize the same set of papers differently. The characterization is an interpretation, not a measurement.
7. **The absent researcher.** No actual researcher participates in the evaluation. The AI reviewer substitutes for the researcher's judgment about what is valuable. This substitution is not just a practical limitation — it is a structural absence that affects what "valuable" means in the findings. The researchers who will use this system, whose needs the findings will shape, are present only as traces in the interest profiles (which are themselves AI-constructed from MiniLM clusters). The qualitative review protocol asks the reviewer to note what it would need to know about the researcher's actual situation to assess recommendations properly — this preserves the trace of the absence without pretending to fill it.

## On the design of this spike

This design was revised through a dialogue about responsibility — not as an add-on but as a re-examination of whether the spike attends adequately to what and who it affects. Six specific revisions resulted:

1. **Sample validation expanded** to check representativeness for challenger models, not just MiniLM. A sample validated only from the incumbent's perspective structurally advantages the incumbent.
2. **Verdict criteria broadened** to recognize value beyond standard relevance (productive provocations, landscape-mapping), higher recall without new signal type, and flags for contexts our profiles don't cover.
3. **Phase 2 branch point softened** — Jaccard > 0.9 no longer means automatic stop. Even quantitatively redundant models get a lightweight qualitative check, because a model redundant on 7/8 profiles but divergent on 1 may still serve that profile's users.
4. **Qualitative review template expanded** to invite the reviewer to notice value beyond relevance, assess set-level landscape properties, and note what it would need to know about the researcher's actual situation to judge properly.
5. **Success criterion 6 added** — user situation (API dependency, hardware, cost, local-first values). The spike should inform users' choices, not make choices for them.
6. **Absent researcher named** as a constitutive limit, not just a practical one. The trace of the absence is preserved in the review protocol rather than erased by acting as though AI assessment is equivalent to researcher judgment.

These revisions were motivated by the recognition that methodological rigor is not just instrumentally valuable (produces better findings) but is a form of responsibility to those the methodology touches — the future users, the researchers whose needs the profiles don't represent, the models being evaluated under conditions that may not give them a fair hearing. The concrete changes above are how that recognition shows up in the experimental design. They do not resolve the responsibility — no design can — but they attend to it more carefully than the previous version.

See: `deliberations/responsibility-alterity-and-methodological-praxis.md` (GSD Reflect project) for the philosophical context of these revisions.
