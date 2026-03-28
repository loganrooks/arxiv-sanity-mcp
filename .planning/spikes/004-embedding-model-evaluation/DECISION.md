---
spike: "004"
status: complete
date: 2026-03-28
voyage_status: pending
confidence: interpretation-level (not extrapolation)
---

# Spike 004 Decision: Embedding Model Evaluation

## Decision-Readiness Classes

### Retain default (MiniLM + TF-IDF) — YES, with qualification

The current provisional arrangement of MiniLM primary + TF-IDF secondary should remain the default. No model demonstrated sufficient advantage to warrant replacement, and the local-first, zero-dependency nature of MiniLM + TF-IDF aligns with project values.

**However**, the finding that all models are substantially divergent from MiniLM — and that each captures a genuinely different signal axis — means the two-view architecture is leaving discoverable papers on the table. The question is not whether to replace MiniLM but whether to add optional third views.

### Candidates: optional experimental view

**SPECTER2** merits being offered as an optional third view for users working in specialized scientific domains (quantum, mathematical foundations, any field with distinctive scientific vocabulary). Evidence:
- Dramatically different signal on P3 (J@20=0.379) with qualitative confirmation of value
- Strongly preferred over MiniLM in blind comparison on P3
- Coherent divergent papers across all profiles — no noise
- Already local, already fast (49s for 2000 papers), no new dependencies
- Score compression is a known limitation for within-topic ranking

**GTE** merits being offered as an optional third view for users who want broader methodological coverage. Evidence:
- Consistently finds foundational methodology papers MiniLM misses
- Highest tau correlation with MiniLM (least disruptive to add)
- No noise observed in any review
- Local-first, moderate resource requirements (117s, 1024-dim)
- But: modest divergence — the value-add over MiniLM is real but not dramatic

### Candidates: further investigation

**Stella v5** shows a potentially valuable deployment-realism signal but requires further investigation under different conditions:
- Strongest divergence on P6 (Diffusion, J@20=0.379) and P7 (Federated learning, J@20=0.481)
- Deployment-realism signal is interesting but only emerged clearly on 2 profiles
- Requires xformers, which constrains the torch/CUDA version — operational burden for uncertain gain
- Worth re-evaluating when the corpus includes more interdisciplinary or systems-oriented papers

**Qwen3** shows the most divergent signal but with reliability concerns:
- Most truly unique papers (up to 7 per profile) — highest discovery potential
- Vocabulary-match false positives are a structural problem (RL-for-LLMs scored comparably to RL-for-robotics)
- Best suited as a diversity signal in fusion, not as a standalone view
- Worth investigating with a post-filter to remove vocabulary-match noise

**Voyage-4**: pending. Cannot assess until API embedding completes.

### Evidence insufficient

None for the 4 local models — each received full evaluation. Voyage is pending.

## Deferred Questions Updated

### From Spike 003

**"Do API embeddings add value?"**
→ **Still deferred.** Voyage embedding in progress. Will be updated as an addendum.

**"Would a different second view model be better than TF-IDF?"**
→ **Answer: No, but the question is wrong.** No embedding model is a better *second view* than TF-IDF because embedding models and TF-IDF capture genuinely orthogonal signals. The real question is: should there be a *third* view? The evidence supports offering optional third views (SPECTER2 and GTE) but not replacing TF-IDF.

## Architecture Implications

**Constraint:** Per Codex review, any architectural claim remains at most "Chosen for now." This spike's evidence base cannot support "Settled" status.

### Current arrangement: MiniLM primary + TF-IDF secondary — Chosen for now (reaffirmed)

No change warranted. Both MiniLM and TF-IDF provide distinct, valuable signals. The low J@20 between challengers and TF-IDF (mean 0.29-0.54) confirms TF-IDF's signal is genuinely different from all embedding approaches.

### Optional third views — Chosen for now (new)

The architecture should support optional additional views without requiring them. Concrete recommendation:
1. SPECTER2 as "scientific-community" view — available when user works in specialized domains
2. GTE as "methodology-breadth" view — available when user wants wider methodological coverage
3. Both are local-first and require no API dependencies

This is "Chosen for now" because:
- Only tested on CS/ML profiles
- AI qualitative review, no human confirmation
- MiniLM-entangled profiles may understate the value of views that structure the space differently

### View architecture — Open

The question of how many views to offer, how to name them, and whether to fuse them automatically vs presenting them as alternatives remains open. This spike provides characterization data but not UX evidence.

## User Situation Considerations (Success Criterion 6)

| Model | API dependency | GPU required | Disk | Embed time (2K papers) | Local-first compatible |
|-------|---------------|-------------|------|----------------------|----------------------|
| MiniLM | None | Optional (CPU OK) | 80MB | <1s (extract) | Yes |
| SPECTER2 | None | Yes (CLS pooling) | 440MB | 49s | Yes |
| TF-IDF | None | No | ~2MB (sparse) | <1s | Yes |
| GTE | None | Yes (encode) | 670MB | 117s | Yes |
| Stella | None (but xformers required) | Yes | 1.5GB | 81s | Yes, with constraint |
| Qwen3 | None | Yes | 2.4GB | 98s | Yes |
| Voyage-4 | **Yes (API)** | No | 0 | ~37 min (rate-limited) | **No** |

SPECTER2 and GTE are both local-first compatible with modest resource requirements. Stella's xformers dependency is a practical constraint. Qwen3 is the largest model. Voyage's API dependency conflicts with local-first project values — even if it adds value, the dependency may not be worth the trade-off for this project.

## Limitations of This Decision

1. **Only 4 of 5 challengers evaluated.** Voyage results pending.
2. **CS/ML domain only.** SPECTER2's advantage on specialized vocabulary may be larger in physics, biology, or humanities. Cannot extrapolate.
3. **AI-assessed quality.** No human researcher confirmed that the divergent papers are actually valuable. The "absent researcher" remains absent.
4. **2000-paper sample.** Effects at full corpus scale (19K+) may differ. The sample validation was strong (GO) but inherently limited.
5. **Blind review gap.** Only SPECTER2 had complete blind comparative assessments. Other models' qualitative evidence is from non-blind characterization reviews.
6. **MiniLM-entangled profiles.** Models that structure the similarity space differently from MiniLM are evaluated using profiles built from MiniLM's structure. This is a structural disadvantage for challengers that the methodology acknowledges but cannot eliminate.
