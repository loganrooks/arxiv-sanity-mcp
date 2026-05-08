# Cross-Spike Qualification Report: Spikes 001 and 002 in Light of Spike 003

**Date:** 2026-03-20
**Author:** Retrospective analysis
**Purpose:** Identify claims in Spikes 001 and 002 that are directly contradicted, methodologically undermined, or qualified by Spike 003's findings. Ensure future readers of Spikes 001/002 encounter appropriate warnings.

---

## Spike 003 Methodological Findings Used as Criteria

This report applies six classes of Spike 003 findings as retrospective qualification criteria:

| ID | Criterion | Spike 003 Evidence |
|----|-----------|-------------------|
| M1 | Top-K Jaccard is insufficient as a sole comparison metric | `sig-2026-03-20-jaccard-screening-methodology`: pool size inflates agreement, collapses nature of divergence, sensitive to selectivity ratio |
| M2 | LOO-MRR evaluation is circularly biased toward MiniLM | FINDINGS.md Section 5, Section 8.1: clusters, profiles, held-out papers all derived from MiniLM embeddings |
| M3 | SPECTER2 was loaded without proper adapter in Spikes 001-002 | W0.1 fix documented; adapter changes ~35% of top-20 recommendations; Spearman 0.78 between base and adapter rankings |
| M4 | Qualitative review contradicted quantitative conclusions in multiple cases | W1 cross-strategy summary, W3 blind review, W5.4 synthesis: SPECTER2 redundancy, fusion profile-dependence, TF-IDF undervaluation by MRR |
| M5 | "Three quality dimensions" finding only emerged from qualitative review | W1 characterization: topical precision, methodological kinship, discovery potential -- invisible to all quantitative instruments |
| M6 | Small-sample enrichment data inflates effect sizes | Bibliographic coupling discrimination 0.467 on 95 papers; at full corpus scale, only 95/19,252 papers have reference data (0.5% coverage) |

---

## Part 1: Spike 001 — Volume, Filtering, and Scoring Landscape

### 1.1 Claims Directly Contradicted or Revised

#### CLAIM 001-A: "SPECTER2 captures discovery potential -- papers from adjacent research communities using different vocabulary"
- **Source:** FINDINGS.md Phase C1 Qualitative Review; DECISION.md "Embedding models are complementary, not competing"
- **What was claimed:** SPECTER2 uniquely provides cross-community discovery. MiniLM captures topical precision; SPECTER2 captures discovery potential. The system should use both models.
- **What Spike 003 found:** W5.4 qualitative review found SPECTER2 is redundant with MiniLM for CS/ML papers: 45-60% paper overlap in top-20, score compression (0.009 spread) making ranking noise. The "Adjacent Communities" label promise was not delivered for any of the three tested profiles. SPECTER2 was dropped from the default configuration.
- **Complication:** All Spike 001 SPECTER2 findings used the base model without the proximity adapter (M3). The W0.1 adapter fix changed ~35% of top-20 results. The Spike 001 qualitative review of SPECTER2 was evaluating a misconfigured model.
- **Status:** RETRACTED as stated. The complementarity claim was based on (a) a misconfigured model and (b) AI qualitative review that was not reproduced under corrected conditions. The "three quality dimensions" insight from the qualitative review (M5) remains valuable as a conceptual framework, but SPECTER2's role in delivering the "discovery potential" dimension is not supported by Spike 003 evidence. The SPECTER2-specific claims should be replaced with a domain-qualified statement: SPECTER2 may provide unique value in domains where citation communities diverge from vocabulary similarity (not CS/ML), but this is untested.

#### CLAIM 001-B: "Semantic search does NOT need pgvector at personal scale" / "Embedding search is faster than TF-IDF search"
- **Source:** FINDINGS.md A1c.3 Key Findings #1, #5; "Discoveries That Changed Our Thinking" #7, #8
- **What was claimed:** Brute-force dot product over 384-dim dense embeddings (16ms at 215K) is 30x faster than cosine similarity over 56K-dim sparse TF-IDF (516ms at 215K). pgvector is unnecessary at personal scale.
- **What Spike 002 found:** pgvector HNSW is 5-23x faster than numpy brute-force and scales near-constantly (~0.8ms regardless of corpus size). At 215K, the gap is 0.6ms vs 14ms. Spike 002 explicitly listed this as "FALSIFIED."
- **What Spike 003 contributes:** The pgvector finding is a Spike 002 result, not Spike 003. But Spike 003's evaluation framework reflection (M2) underscores that any cross-family search quality comparison between backends would need the same kind of entanglement audit applied to strategy comparisons.
- **Status:** Already FALSIFIED by Spike 002. Spike 001 FINDINGS.md and DECISION.md contain the correction in their "Revised Assessment" sections. No additional Spike 003 qualification needed beyond what Spike 002 already provided.

#### CLAIM 001-C: "Bibliographic coupling — works for new papers with zero citations. Connected Papers' approach. Computable from existing data."
- **Source:** DECISION.md Success Criteria Answer #3 (top 5 signals); FINDINGS.md Phase B2
- **What was claimed:** Bibliographic coupling is listed as signal #4 of the top 5 worth computing. It "works for new papers" and is "computable from existing data."
- **What Spike 003 found:** Bibliographic coupling (S3a) has zero MRR on the full corpus because only 1/120 seed papers has reference data. The focused evaluation on the 95 papers with references shows discrimination 0.467, but this is 95 out of 19,252 papers (0.5% coverage). The signal is algorithmically valid but operationally non-functional at current enrichment levels.
- **Small-sample concern (M6):** The 0.467 discrimination was measured on 95 papers. Spike 001's B2 phase enriched only 460 papers via OpenAlex. Claims about bibliographic coupling's value as a signal were based on literature review (B1), not on demonstrated performance at operational scale. The literature review evidence is valid (Connected Papers uses it successfully), but the implication that it is "computable from existing data" was misleading -- existing data has 0.5% reference coverage.
- **Status:** QUALIFIED. The algorithm is valid (Spike 003 confirmed). The ranking as signal #4 should carry a caveat that it requires substantial enrichment expansion (from 0.5% to a meaningful fraction of the corpus) before it becomes operational. The phrase "computable from existing data" should be corrected to "computable once reference data is enriched."

### 1.2 Claims That Depend on Methodology Spike 003 Found Insufficient

#### CLAIM 001-D: "MiniLM captures topical precision; SPECTER2 captures discovery potential; Consensus papers have higher category overlap (0.40 vs 0.32)"
- **Source:** FINDINGS.md Phase C1 Qualitative Review; DECISION.md "Embedding models are complementary, not competing"
- **Methodological issues:**
  - Uses SPECTER2 without adapter (M3) -- all SPECTER2 comparisons are against a misconfigured model
  - The 12-strategy comparison on "model-independent ground truth" used category co-membership, which Spike 001 itself notes "favors metadata-based strategies by construction"
  - The R@100 metric (MiniLM 17%, SPECTER2 16%) shows near-identical performance, which the qualitative review then interpreted as "different dimensions" -- but the qualitative review was of the misconfigured model
  - No Spike 003-style evaluation framework entanglement analysis was performed
- **What survives:** The conceptual finding that multiple strategies capture different aspects of relatedness is confirmed by Spike 003 (W1 cross-strategy summary, W3 consensus analysis). The specific claim about MiniLM vs SPECTER2 complementarity is undermined by M3. The three quality dimensions framework (M5) remains valuable but its attribution to specific models needs revision.
- **Status:** QUALIFIED. The three-quality-dimensions framework is the durable finding; the model-specific attributions (MiniLM=precision, SPECTER2=discovery) need re-evaluation with the corrected adapter. After Spike 003's W5.4 review with the corrected adapter, SPECTER2's "discovery potential" role was not confirmed for CS/ML papers.

#### CLAIM 001-E: "Each embedding model wins on its own clusters, loses on the other's. Neither is 'better'"
- **Source:** FINDINGS.md Phase C1 Round 3, "Fair cross-model evaluation"
- **Methodological issues:**
  - Evaluation framework entanglement (M2): "each model wins on its own clusters" is a tautological finding when the clusters are defined by the model's own embeddings. This is exactly the kind of circular evaluation Spike 003 documented in Section 8.1. The "fair" evaluation reproduced the circularity rather than eliminating it.
  - SPECTER2 without adapter (M3)
- **Status:** RETRACTED as evidence. The finding is methodologically circular. The conclusion "neither is better" may be correct, but the evidence cited does not support it. Spike 003 provides better evidence: qualitative review across 3 profiles found all strategies produce ~80% on-topic results, but with different character.

#### CLAIM 001-F: "Co-author network R@100 = 82% on category co-membership ground truth"
- **Source:** FINDINGS.md Phase C1, 12-strategy comparison table
- **Methodological issues:**
  - Category co-membership as ground truth favors metadata-based strategies by construction (acknowledged in Spike 001's own caveat)
  - The 82% number cannot be compared to embedding R@100 (17%, 16%) because the ground truth is biased toward metadata strategies
  - Spike 003's Jaccard screening critique (M1) applies here: comparing strategies across fundamentally different signal types using a single metric that favors one type
- **Status:** QUALIFIED. The relative ranking within metadata strategies (co-author 82% > rare category 50% > BERTopic 47%) is internally valid. The cross-family comparison (co-author 82% vs MiniLM 17%) is invalid because the ground truth systematically favors metadata-based strategies.

#### CLAIM 001-G: "B2 correlations: FWCI r=0.75, citation percentile r=0.39, etc."
- **Source:** FINDINGS.md Phase B2
- **Methodological issues:**
  - Based on 460 enriched papers (small sample, M6)
  - Near-zero citations for January 2026 papers -- the importance proxy (citations) is unreliable
  - Spike 001 itself notes this limitation but still lists the correlations as findings
  - Spike 003 found FWCI and citation signals (S2d/S2e) "non-functional at 2.6% enrichment coverage"
- **Status:** QUALIFIED. The correlation structure (FWCI strongest, content signals near-zero) is informative about signal relationships but cannot be treated as predictive power estimates. The claim that FWCI is signal #1 to compute (DECISION.md) depends on enrichment coverage that does not exist.

### 1.3 Claims That Still Hold Despite Spike 003 Methodological Critiques

These claims are based on direct measurements unaffected by evaluation framework entanglement, SPECTER2 adapter issues, or small-sample enrichment problems.

| Claim | Evidence Type | Why It Survives |
|-------|-------------|-----------------|
| Big4 captures 81% of configured categories' papers | Direct count from OAI-PMH harvest | No proxy or evaluation framework involved |
| SQLite FTS5 search is fast at scale (30ms p50 at 215K) | Latency measurement | Direct hardware measurement |
| TF-IDF matrix fits in RAM (157 MB at 215K) | Memory measurement | Direct measurement |
| Brute-force embedding search is fast (16ms p50 at 215K) | Latency measurement | Direct measurement |
| WAL mode eliminates concurrent access degradation | Latency measurement under load | Direct measurement |
| GPU provides ~20x speedup for embedding computation | Computation time measurement | Direct measurement, model-independent |
| All strategies are resource-feasible at 19K/month (C2) | Resource computation | Cost calculations, not quality claims |
| Daily volume ~550-600 for big4 categories | Direct count | No proxy involved |
| Category purity 0.40 across 48 BERTopic topics (A2) | Direct measurement | Uses MiniLM embeddings for BERTopic, but the purity measurement itself is against arXiv categories (metadata), not quality |
| Vocabulary: 4% of terms cover 80% of content (A3) | Direct count | Corpus statistics, no evaluation framework |

### 1.4 Recommended Qualification Notes for Spike 001 Documents

#### For FINDINGS.md, after Phase C1 Qualitative Review heading:

```
> **NOTE (Spike 003, 2026-03-20):** All SPECTER2 findings in this section
> used the base model without the proximity adapter. Spike 003 W0.1 fixed
> the adapter loading; the corrected model changes ~35% of top-20 results.
> The W5.4 qualitative review with the corrected adapter found SPECTER2
> qualitatively redundant with MiniLM for CS/ML papers (45-60% overlap,
> score compression making ranking noise). The "discovery potential"
> attribution to SPECTER2 is not confirmed under corrected loading.
> The three quality dimensions framework (topical precision, methodological
> kinship, discovery potential) remains valuable but is not attributable
> to specific models as stated here.
```

#### For FINDINGS.md, after Phase C1 "12-strategy comparison" table:

```
> **NOTE (Spike 003, 2026-03-20):** Cross-family R@100 comparisons in
> this table (e.g., co-author 82% vs MiniLM 17%) use category
> co-membership as ground truth, which systematically favors metadata-based
> strategies. Spike 003 documented this class of evaluation framework
> entanglement in Section 8.1. Within-family comparisons (e.g., among
> metadata strategies) remain valid. Cross-family comparisons should not
> be interpreted as quality rankings.
```

#### For FINDINGS.md, after "Embedding models are complementary, not competing" in DECISION.md:

```
> **NOTE (Spike 003, 2026-03-20):** This complementarity claim was based
> on SPECTER2 without the proximity adapter (fixed in Spike 003 W0.1)
> and on a qualitative review methodology later found insufficient by
> Spike 003's own standards. The W5.4 qualitative review with the corrected
> adapter found SPECTER2 redundant with MiniLM for CS/ML papers.
> The complementarity between MiniLM and TF-IDF IS confirmed by Spike 003
> (Jaccard 0.179, different held-out recoveries 2/15 vs 5/15).
> Reframe: the confirmed complementarity is semantic embedding vs lexical
> matching, not MiniLM vs SPECTER2.
```

#### For FINDINGS.md, after Phase B2 correlations:

```
> **NOTE (Spike 003, 2026-03-20):** These correlations are based on
> 460 enriched papers with near-zero citation maturity. Spike 003 found
> FWCI and citation signals non-functional at 2.6% enrichment coverage
> (S2d/S2e). The correlation structure is informative about signal
> relationships but does not demonstrate operational utility. Bibliographic
> coupling (listed as signal #4 in DECISION.md) requires enrichment
> expansion from 0.5% to meaningful coverage before it becomes operational.
```

#### For DECISION.md, after "Each embedding model wins on its own clusters":

```
> **NOTE (Spike 003, 2026-03-20):** This "fair cross-model evaluation"
> reproduces the circular evaluation bias documented in Spike 003
> Section 8.1. Each model winning on its own clusters is tautological
> when clusters are defined by the model's own embeddings. The conclusion
> "neither is better" may be correct but this evidence does not support it.
```

---

## Part 2: Spike 002 — SQLite vs PostgreSQL Backend Comparison

### 2.1 Claims Directly Contradicted or Revised

#### CLAIM 002-A: "H1 FALSIFIED: FTS5 and tsvector return substantially similar results" (Average Jaccard 0.39)
- **Source:** FINDINGS.md Dimension 1, Hypothesis Results table
- **What was claimed:** Average Jaccard 0.39 (below 0.5 threshold) means FTS5 and tsvector return substantially different results. This was labeled as the "most important finding."
- **What Spike 003 found about Jaccard (M1):** Top-K Jaccard collapses the nature of divergence into a single number. A Jaccard of 0.39 does not tell you whether the divergence is (a) boundary noise from rank #19 vs #21 disagreements, (b) different papers of similar quality, or (c) one backend returning genuinely better papers. Spike 003's Voyage screening found Jaccard 0.717-0.772 and originally interpreted this as "no new signal" -- then retracted that interpretation because Jaccard was insufficient as a sole decision criterion.
- **Spike 002's own caveat:** The FINDINGS.md methodological caveats (added 2026-03-19) already flag that "Jaccard measures disagreement, not which backend returns better papers" and that "H1 falsified should read 'backends disagree' -- not 'one is better.'" The DECISION.md further qualifies that divergence is "ranking-function-driven (BM25 vs cover density), not quality-driven."
- **Status:** QUALIFIED (partly self-corrected). The Jaccard measurement itself is accurate. The original "falsified" framing was too strong, and Spike 002 partially corrected this in its own caveats. Spike 003's Jaccard critique (M1) reinforces this correction: Jaccard 0.39 means "the backends disagree" but says nothing about which is better, whether the disagreement is at rank boundaries or throughout the list, or whether human relevance judgments would favor one set. The "most important finding" framing should be downgraded -- the disagreement is real but its significance is unknown without qualitative review of the divergent results.

#### CLAIM 002-B: "Search quality is relative to the user. We measured Jaccard overlap between backends, not relevance to user intent."
- **Source:** FINDINGS.md "What These Numbers Don't Tell You" #1; DECISION.md "What we cannot state" #1
- **Status:** This is not a claim to contradict -- it is Spike 002's own honest caveat. Spike 003's M1 criterion validates this self-qualification. Spike 002 correctly identified the limitation but still structured its findings around Jaccard as the primary evidence, creating a tension between the caveat and the presentation. A future reader might see "FALSIFIED" in the hypothesis table and skip the caveats.

### 2.2 Claims That Depend on Methodology Spike 003 Found Insufficient

#### CLAIM 002-C: "Choosing between FTS5 and tsvector is not just a performance decision -- it is a retrieval quality decision"
- **Source:** FINDINGS.md Dimension 1, bottom paragraph
- **Methodological issues:**
  - Based entirely on Jaccard overlap (M1)
  - No qualitative review of divergent results (Spike 002 acknowledges this in its "Open for Spike 003" section)
  - No human relevance judgments
  - The divergence could be entirely at rank boundaries with no user-perceptible quality difference
  - Spike 003 demonstrated (W1 cross-strategy summary) that strategies with very different Jaccard overlap can all produce ~80% on-topic results -- divergence in top-K does not necessarily mean quality divergence
- **Status:** QUALIFIED. The backends do return different papers (measured). Whether this constitutes a "retrieval quality decision" cannot be determined without qualitative review or human evaluation. Spike 002's DECISION.md softened this to "Both sets of results are plausible upon inspection" -- this softer claim is appropriate, but the FINDINGS.md headline framing remains too strong.

#### CLAIM 002-D: "FTS5 failures: Two queries fail entirely" (hyphenated terms)
- **Source:** FINDINGS.md Dimension 1, root causes
- **Status:** HOLDS. This is a direct observation about parser behavior (FTS5 parses hyphens as syntax), not a quality comparison that depends on Jaccard or evaluation framework. This is a genuine functional limitation of FTS5.

#### CLAIM 002-E: Tradeoff Map — "Search quality" listed as PostgreSQL Major advantage (Jaccard 0.39)
- **Source:** FINDINGS.md Tradeoff Map, first row
- **Methodological issues:**
  - "Major" magnitude is assigned based on Jaccard 0.39 alone
  - Spike 003 M1: Jaccard as sole metric is insufficient for quality claims
  - The Tradeoff Map equates "different results" with "PostgreSQL has better search quality," which is not supported
  - The DECISION.md Tradeoff Map corrected this to "Keyword search results: Divergence is ranking-function-driven, not quality-driven" -- but FINDINGS.md retains the "Major" designation
- **Status:** QUALIFIED. The FINDINGS.md Tradeoff Map should not list "Search quality" as a PostgreSQL advantage of "Major" magnitude based solely on Jaccard divergence. The corrected framing from DECISION.md ("both return plausible papers") is more appropriate.

### 2.3 Claims That Still Hold Despite Spike 003 Methodological Critiques

| Claim | Evidence Type | Why It Survives |
|-------|-------------|-----------------|
| FTS5 is 3.5-4.8x faster than tsvector for keyword search | Direct latency measurement | Hardware benchmark, no quality proxy |
| pgvector HNSW is 5-23x faster than numpy, near-constant ~0.8ms | Direct latency measurement | Hardware benchmark |
| HNSW recall >= 0.91 at all scale points | Exact vs approximate comparison | Direct measurement against known ground truth |
| PostgreSQL is 3-5x slower for bulk import | Direct timing measurement | No quality proxy |
| Both backends handle concurrent R+W without degradation | Direct measurement under load | No quality proxy |
| PostgreSQL connection setup is ~87x slower | Direct measurement | No quality proxy |
| PostgreSQL uses 2x disk space | Direct measurement | No quality proxy |
| Workflow-level difference is 1.4x (6ms absolute) | Direct timing measurement | No quality proxy |
| FTS5 cannot parse hyphenated terms (functional limitation) | Observed behavior | Parser behavior, not quality judgment |

### 2.4 Recommended Qualification Notes for Spike 002 Documents

#### For FINDINGS.md, after Hypothesis Results table:

```
> **NOTE (Spike 003, 2026-03-20):** The H1 result ("FALSIFIED") uses
> Top-K Jaccard as its sole criterion. Spike 003's Voyage screening
> experience (sig-2026-03-20-jaccard-screening-methodology) documented
> five specific limitations of Jaccard as a decision metric: it collapses
> the nature of divergence, is sensitive to pool size, cannot distinguish
> boundary noise from meaningful divergence, and should not be used as
> a sole decision criterion. "Backends disagree" is supported; "one
> backend has better search quality" is not. No qualitative review of
> the divergent results was performed. Spike 003's W1 cross-strategy
> summary found that strategies with Jaccard 0.179 all produced ~80%
> on-topic results -- divergence in overlap does not necessarily imply
> quality divergence.
```

#### For FINDINGS.md Dimension 1, after "Implication: Choosing between FTS5 and tsvector is a retrieval quality decision":

```
> **NOTE (Spike 003, 2026-03-20):** This conclusion is stronger than
> the evidence supports. The divergence is measured (Jaccard 0.39) but
> its quality implications are not. The DECISION.md correctly softened
> this to "Both sets of results are plausible upon inspection." The
> difference is driven by ranking functions (BM25 vs cover density) and
> query parsing, not by one backend finding objectively better papers.
> This remains an open question pending qualitative review.
```

#### For FINDINGS.md Tradeoff Map, as a footnote to "Search quality — Major":

```
> **NOTE (Spike 003, 2026-03-20):** "Major" magnitude is based on
> Jaccard divergence, not on demonstrated quality difference. The
> DECISION.md Tradeoff Map corrected this assessment. Backends return
> different papers; neither has been shown to return better papers.
```

#### For FINDINGS.md "Revised Assessment of Spike 001 Claims" table:

```
> **NOTE (Spike 003, 2026-03-20):** The "pgvector unnecessary" claim
> was correctly identified as falsified by Spike 002's latency data.
> The "search quality" assessment (FTS5 returns different papers than
> tsvector) remains methodologically incomplete per Spike 003's Jaccard
> critique -- "different" is measured, "worse" is not.
```

---

## Part 3: Cross-Spike Patterns

### 3.1 The Jaccard Problem Spans Both Spikes

Jaccard overlap appears as evidence in three contexts across Spikes 001-002:

| Context | Jaccard Value | Used To Conclude | M1 Status |
|---------|--------------|------------------|-----------|
| Spike 002 D1: FTS5 vs tsvector | 0.39 | Backends return different papers ("FALSIFIED") | Conclusion too strong; divergence is real but quality implication is unknown |
| Spike 001 C1: Consensus papers category overlap | 0.40 vs 0.32 | Consensus papers more relevant | Reasonable within-study use, but the 0.08 difference is small and unvalidated |
| Spike 003 W5a: Voyage vs local models | 0.717-0.772 | Originally STOP, revised INCONCLUSIVE | Demonstrated insufficiency of Jaccard as sole criterion |

The pattern: Jaccard was used across all three spikes as if it provided quality information, but it only provides overlap information. Spike 003's self-correction (changing the Voyage verdict from STOP to INCONCLUSIVE) is the clearest evidence that this metric class is insufficient for quality decisions.

### 3.2 The SPECTER2 Adapter Problem Propagates

All Spike 001 SPECTER2 findings and any Spike 002 findings that reference SPECTER2 comparisons are compromised by the improper loading. The chain of impact:

1. Spike 001 C1: SPECTER2 qualitative review assessed a misconfigured model
2. Spike 001 DECISION: "Embedding models are complementary" cites SPECTER2's discovery potential
3. Spike 001 recommended architecture includes SPECTER2 as a third view
4. Spike 003 W0.1 fixed the adapter; W5.4 found SPECTER2 redundant with MiniLM under correction
5. Spike 003 DECISION dropped SPECTER2 from default configuration

The Spike 001 recommendation for a three-strategy architecture (MiniLM + SPECTER2 + TF-IDF) is replaced by Spike 003's two-strategy architecture (MiniLM + TF-IDF). Any downstream implementation that followed Spike 001's recommendation should be updated.

### 3.3 The Quantitative-Qualitative Gap Is Systemic

Spike 001 conducted one AI qualitative review (C1, 3 seeds x 3 recommendation sets). Spike 003 conducted 21 qualitative reviews across 4 checkpoints. The pattern across both:

| Finding | Quantitative Verdict | Qualitative Verdict | Resolution |
|---------|---------------------|--------------------|----|
| SPECTER2 value (Spike 001) | R@100 = 16%, near MiniLM | "Discovery potential" -- complementary | Spike 003 qualitative overturned: redundant |
| TF-IDF value (Spike 003) | MRR 0.104 (4x below MiniLM) | 5/15 held-out recovery (2.5x above MiniLM) | Complementary signal, not inferior |
| Fusion (Spike 003) | All fusions degrade MiniLM by 22-30% | Helps narrow topics (P8), neutral for broad (P4) | Profile-dependent, not universally bad |
| kNN (Spike 003) | Aggregate -58% MRR | Works for dense topics (P4/AI safety) | Profile-dependent niche |
| Cold start (Spike 003) | Coverage 0.366 at 1 seed | Echo chambers for broad topics | "Produces results" is not "works" |

The lesson: Spike 001 had too little qualitative review to catch the quantitative-qualitative divergence. Its conclusions about strategy quality were based primarily on quantitative metrics (R@100, Jaccard, category overlap), which Spike 003 showed are insufficient for cross-family strategy comparison.

### 3.4 Small-Sample Enrichment Claims

Both Spike 001 and Spike 003 share this problem:

| Spike | Claim | Sample | Issue |
|-------|-------|--------|-------|
| 001 B2 | FWCI r=0.75 with citations | 460 papers | Near-zero citation maturity makes proxy unreliable |
| 001 DECISION | Bibliographic coupling is signal #4 | Literature review, not measured | No operational data |
| 003 W1C | Bibliographic coupling discrimination 0.467 | 95 papers | 0.5% of corpus; effect size likely inflated by selection |
| 003 DECISION | "Bibliographic coupling algorithm is valid" | 95 papers | Tagged MEDIUM confidence with "tiny sample" caveat |

Spike 003 handled this better than Spike 001 by explicitly tagging the confidence level and noting the sample limitation. Spike 001 listed bibliographic coupling as a top-5 signal without indicating the evidence was entirely from literature review, not from operational measurement.

---

## Part 4: Summary of Actions

### Claims to Retract
1. **Spike 001:** SPECTER2 as a complementary embedding model delivering "discovery potential" (based on misconfigured model + insufficient qualitative review)
2. **Spike 001:** "Each embedding model wins on its own clusters" as evidence for complementarity (tautological evaluation)

### Claims to Qualify
1. **Spike 001:** Three quality dimensions framework -- keep the framework, remove model-specific attributions
2. **Spike 001:** Bibliographic coupling as top-5 signal -- add enrichment coverage requirement
3. **Spike 001:** B2 correlation structure -- add citation maturity and sample size caveats
4. **Spike 001:** 12-strategy R@100 comparison -- add cross-family comparison invalidity note
5. **Spike 002:** "H1 FALSIFIED" -- soften to "backends disagree" per Spike 002's own caveat
6. **Spike 002:** "Retrieval quality decision" -- qualify as "retrieval difference, quality implications unknown"
7. **Spike 002:** Tradeoff Map "Search quality -- Major" -- downgrade per DECISION.md's own correction

### Claims That Stand
1. **Spike 001:** All FTS5, TF-IDF, and embedding latency/memory measurements
2. **Spike 001:** Volume mapping, category distribution, vocabulary statistics
3. **Spike 001:** WAL mode concurrent access findings
4. **Spike 001:** GPU speedup measurements
5. **Spike 001:** Resource feasibility calculations (C2)
6. **Spike 002:** All latency comparisons (FTS5 vs tsvector, numpy vs HNSW)
7. **Spike 002:** Write performance, backup, disk footprint measurements
8. **Spike 002:** FTS5 hyphen parsing limitation (functional observation)

### Documents Requiring Qualification Notes
1. `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/001-volume-filtering-scoring-landscape/FINDINGS.md` -- 4 notes (see Section 1.4)
2. `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/001-volume-filtering-scoring-landscape/DECISION.md` -- 1 note (see Section 1.4)
3. `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/002-backend-comparison/FINDINGS.md` -- 4 notes (see Section 2.4)

Note: Spike 001 FINDINGS.md already contains a "Critical Limitations" section (added 2026-03-19) that flags the SPECTER2 adapter issue and evaluation biases. The recommended notes above are more specific and reference Spike 003 evidence directly, so they complement rather than duplicate the existing limitations section.
