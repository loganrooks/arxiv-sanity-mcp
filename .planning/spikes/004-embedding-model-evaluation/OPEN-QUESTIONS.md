---
date: 2026-03-29
status: post-spike-004-assessment
scope: open research questions across the spike program (001-004)
---

# Open Research Questions

What remains unaddressed, untested, or insufficiently grounded after Spikes 001-004.

## A. Evaluation methodology — the deepest gap

These questions concern whether we can trust the evidence framework itself.

### A1. No human evaluation exists anywhere in the spike program

All 4 spikes use AI-generated qualitative review as the primary quality signal. The Spike 003 epistemic revision and the Spike 004 DESIGN.md both name the "absent researcher" as a constitutive limitation. But after 4 spikes, 21+ qualitative reviews (Spike 003) and 40 reviews (Spike 004), zero human judgments exist.

**What this threatens:** Every claim about which papers are "relevant," which divergent papers are "valuable," and which models capture "genuinely different signals" rests on an AI reviewer's notion of value. The narrative characterizations of models (citation-community, deployment-realism, etc.) may be plausible stories that don't match what an actual researcher would find useful.

**What would resolve it:** Even 5-10 human assessments per profile, comparing the models' top-20 lists, would either confirm or undermine the AI review findings. This is the single highest-value next step.

### A2. Interest profiles are MiniLM-entangled — never tested otherwise

All 8 profiles were constructed from MiniLM BERTopic clusters (Spike 001). Every evaluation since has used these profiles. Models that structure the similarity space differently from MiniLM are being evaluated against profiles that may not represent their strengths.

**What this threatens:** The tau and J@20 comparisons all measure "how much does Model X agree with MiniLM on what MiniLM thinks is relevant?" A model that finds genuinely better papers — ones a researcher would prefer — could score poorly if those papers don't match MiniLM's cluster structure.

**What would resolve it:** Construct alternative profiles from (a) category metadata alone, (b) a different model's clusters, or (c) researcher-provided seed sets not derived from any model. Compare model rankings under different profile constructions.

### A3. Seed sensitivity never formally characterized

Spike 004 post-execution analysis discovered that per-profile J@20 varies by up to 0.360 depending on which 5 seed papers are chosen. This was never anticipated in the DESIGN.md and was not part of the pre-registered predictions.

**What this threatens:** All per-profile findings from Spikes 003 and 004 may be seed-dependent. The "profile-dependence" findings (e.g., "SPECTER2 is strongest on Quantum") may be artifacts of particular seed selections.

**What would resolve it:** Systematic seed sensitivity analysis: for each profile × model, compute metrics across all seed subsets and report the distribution, not a point estimate. This turns scalar findings into confidence intervals.

### A4. What should the primary comparison metric be?

Spike 004 showed J@20 is too noisy, tau is stable but coarse (scalar over 2000 rankings), and qualitative review is non-reproducible. No single metric is satisfactory.

**What would resolve it:** This is partly a philosophical question about what aspect of "model difference" matters. But practically: rank-biased overlap (RBO), top-weighted rank correlation, or precision@K with confidence intervals might be more informative than raw Jaccard.

## B. Retrieval architecture — partially explored

### B1. Only centroid similarity tested for new models

All 5 challenger models in Spike 004 used centroid cosine similarity. Spike 003 tested kNN-per-seed and MMR but only for MiniLM/SPECTER2/TF-IDF. The "signal axes" identified in Spike 004 (citation-community, deployment-realism, etc.) may not persist under different retrieval methods.

**What this threatens:** A model that looks divergent under centroid scoring might converge with MiniLM under kNN. Or a model that looks noisy under centroid might excel under kNN-per-seed (if its per-seed neighborhoods are tighter).

### B2. Multi-model fusion never tested with new challengers

Spike 003 tested MiniLM+TF-IDF fusion and found it profile-dependent. But MiniLM+SPECTER2 fusion, MiniLM+GTE fusion, three-way fusion — none tested. The "parallel views" architecture recommendation is based on MiniLM+TF-IDF complementarity, not on whether the new challengers complement MiniLM differently.

### B3. Cross-encoder reranking dismissed due to domain mismatch

Spike 003 W3.4 found MS MARCO cross-encoder catastrophically bad (-71 to -85% MRR). But this was a specific model on a mismatched domain. Domain-adapted cross-encoders (e.g., fine-tuned on arXiv data, or using a more recent general model) were never tested.

### B4. Instruction-tuned embedding never tested

Stella v5 and Qwen3 both support instruction-tuned embedding (custom prompts for query vs document). The Spike 004 PROTOCOL.md noted document-only embedding. Query-time instruction tuning might change model behavior.

### B5. Text format variations never tested

All models embedded `title \n\n abstract`. Never tested: title-only (Spike 003 eliminated this for MiniLM/SPECTER2, but not for the new models), abstract-only, title+abstract+categories, or title+abstract+author names.

## C. Scale and domain

### C1. New models tested only on 2000-paper sample

Spike 004's sample validation showed perfect MiniLM baseline (J=1.0) and no challenger degeneracy. But the structural comparison (J@100 = 0.50-0.56) means roughly half the top-100 papers differ between sample and full corpus neighborhoods. Effects visible only at 19K+ scale are not captured.

### C2. Non-CS/ML domains completely untested

The corpus is 77% CS. The project's design docs envision serving researchers across arXiv. SPECTER2's citation-community signal may be much stronger in physics, biology, or mathematics where community structure diverges more from vocabulary similarity. Conversely, general-purpose models might excel in interdisciplinary areas.

### C3. Temporal effects unknown

All testing on papers from 2023-2026 (the harvest window). Do model rankings change with paper age? Do older, more-cited papers get systematically different treatment across models?

### C4. No testing of enrichment-augmented retrieval

The project has OpenAlex enrichment (topics, citations, related works) but enrichment-augmented retrieval was never tested. Could enrichment features improve model complementarity?

## D. Practical deployment — never tested

### D1. How to present multiple views?

The architecture recommends "optional views" but no UX testing exists. Would a researcher actually switch views? Would they understand what "scientific-community view" vs "methodology-breadth view" means?

### D2. Interactive stability

When a researcher adds a seed paper, how much do recommendations change? Is MiniLM more stable than SPECTER2 under incremental seed addition? Spike 003 tested cold start (1 vs 5 seeds) but not incremental addition dynamics.

### D3. Cold start with new models

Spike 003 tested cold start for MiniLM and TF-IDF only. Do SPECTER2/GTE behave differently at 1-2 seeds?

### D4. Embedding maintenance

When new papers arrive (daily/weekly), what's the cost of maintaining embeddings for each model? MiniLM is ~80MB for 19K. SPECTER2/GTE would be ~150MB each. Is re-embedding incremental or full?

## E. Provider and model landscape — incomplete coverage

### E1. Only one API provider tested

Voyage-4 was the only API model. OpenAI embeddings (text-embedding-3-large), Cohere embed-v3, and Google's gecko were never evaluated. Voyage's P2 divergence might be Voyage-specific or might be a property of all large API models.

### E2. SPECTER2 adapter variants untested

SPECTER2 has multiple adapters (proximity, classification, etc.). Only the proximity adapter was tested. The classification adapter might behave differently for recommendation.

### E3. Embedding dimension reduction untested

Several models support Matryoshka (nested dimension) output. Reducing 1024-dim to 384-dim or 256-dim would save storage and potentially change model behavior.

### E4. Fine-tuning on domain data untested

All models used off-the-shelf. Fine-tuning MiniLM or GTE on arXiv paper pairs might dramatically change the comparison landscape.

## F. What would further challenge the Spike 004 findings

Ranked by expected impact:

1. **Human evaluation contradicting AI reviews** — the single most threatening possibility. If researchers say "the divergent papers SPECTER2 finds are not actually useful," the entire qualitative case collapses.

2. **Non-MiniLM profiles producing different model rankings** — if profiles constructed from GTE or SPECTER2 clusters show that MiniLM is the divergent model, the framing reverses.

3. **Different retrieval method changing the picture** — if kNN-per-seed makes SPECTER2 and MiniLM converge, the "different signal axis" claim weakens.

4. **Full corpus (19K) testing showing different results** — the sample validation was strong but 50% structural divergence at K=100 leaves room for scale effects.

5. **The "signal axes" being seed artifacts** — the characterizations (citation-community, deployment-realism) were from AI reviews on one seed set. Different seeds might produce different characterizations of the same model.

## Recommended next steps (ordered by value/cost ratio)

1. **Human evaluation** — 5-10 judgments per profile comparing model top-20 lists. Highest information value. Doesn't require new spikes.

2. **Seed sensitivity characterization** — compute all metrics across all seed subsets, report distributions. Can be done on existing data with a script.

3. **Full corpus embedding for SPECTER2 and GTE** — test whether sample findings hold at scale. ~10 min GPU time each.

4. **Non-MiniLM profile construction** — build profiles from GTE clusters or category metadata, re-run comparison. Tests the most threatening assumption.

5. **Multi-model fusion testing** — MiniLM+SPECTER2, MiniLM+GTE, three-way. Tests whether "parallel views" is actually better than fusion with the new models.
