---
spike: "004"
status: complete
date: 2026-03-28
voyage_status: complete (8% failure rate, API rate limiting)
confidence: interpretation-level (not extrapolation)
---

# Spike 004 Decision: Embedding Model Evaluation

## What this spike decided vs what it cannot decide

This spike can characterize how models differ from MiniLM. It cannot determine which differences are valuable to researchers. Every recommendation below is at most "Chosen for now" — provisional pending human evaluation.

## Decision-Readiness Classes

### Retain default (MiniLM + TF-IDF) — YES

The current arrangement should remain. This is the most defensible decision because:
- MiniLM + TF-IDF complementarity is the spike program's strongest finding (Spike 003, model-independent, confirmed qualitatively and quantitatively)
- No model demonstrated it was *better* — only that it was *different*
- Local-first, zero-dependency, fast
- Changing the default requires evidence this spike structurally cannot produce (human quality assessment)

### Candidates: further investigation (all)

The original synthesis promoted SPECTER2 and GTE to "optional experimental view" status. This was overclaimed. The evidence supports "further investigation" for all challengers, not operational recommendations for any.

**SPECTER2** — produces different rankings (tau=0.563). AI reviewers describe the divergent papers favorably, including in blind comparison on P2/P3. But: the AI reviewer's judgment is unvalidated, the characterization as "citation-community signal" is a narrative, and the blind comparisons had full written assessment only for SPECTER2 (potential selection bias in what we examined most carefully). Merits investigation with human evaluation.

**GTE** — most correlated with MiniLM (tau=0.637) while still finding some different papers. AI reviewers describe divergent papers as methodologically broader. Merits investigation but the case is thinner than SPECTER2's because the divergence is more modest.

**Voyage** — most different from MiniLM (tau=0.483). P2 blind comparison is the strongest single piece of qualitative evidence in the spike. But: API dependency, 8% failure rate, provider drift, local-first conflict. The signal may be real; the delivery is operationally problematic for this project.

**Stella** — moderate divergence (tau=0.640) with AI-described deployment-realism signal. xformers dependency is a practical constraint. Thinnest evidence case of the local models.

**Qwen3** — most divergent local model (tau=0.590) but with demonstrated noise (vocabulary-match false positive). Highest discovery potential if noise can be filtered. Merits investigation specifically on noise characteristics.

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

**Voyage-4** shows the most interesting divergence of any model on P2 (LM reasoning, J@20=0.333, 8 truly unique papers) with qualitative confirmation of value. But:
- API dependency conflicts with local-first project values
- 8% embedding failure rate from rate limiting
- Provider-side model drift makes findings non-reproducible
- Operationally impractical for local-first deployment (~117 min for 2000 papers at free tier)
- The signal is genuinely valuable — reasoning failure modes that no other model surfaces
- Best suited as an optional API-dependent view for users who accept the trade-off, not as a default

### Evidence insufficient

None — all 5 challengers received full evaluation (40 qualitative reviews total).

## Deferred Questions Updated

### From Spike 003

**"Do API embeddings add value?"**
→ **Yes, on some profiles.** Voyage-4 surfaces genuinely different papers on P2 (LM reasoning) that no local model finds. But the value is profile-dependent (P1 is nearly redundant with MiniLM), and the API dependency conflicts with local-first project values. The value exists but the delivery mechanism is problematic.

**"Would a different second view model be better than TF-IDF?"**
→ **Unanswered.** The Codex review (Blocker 3) explicitly noted this question requires TF-IDF in the comparison frame. PROTOCOL.md Section 4 added TF-IDF metrics, which were computed. But the synthesis never used them to answer this question. What the data shows: all embedding models have low overlap with TF-IDF (orthogonal signals, as expected). What it doesn't show: whether MiniLM + SPECTER2 covers more *relevant* papers than MiniLM + TF-IDF. "Relevant" requires human ground truth we don't have.

## Architecture Implications

**Constraint:** Per Codex review, any architectural claim remains at most "Chosen for now." This spike's evidence base cannot support "Settled" status.

### Current arrangement: MiniLM primary + TF-IDF secondary — Chosen for now (reaffirmed)

No change warranted. Both MiniLM and TF-IDF provide distinct, valuable signals. The low J@20 between challengers and TF-IDF (mean 0.29-0.54) confirms TF-IDF's signal is genuinely different from all embedding approaches.

### Additional views — Open (not "Chosen for now")

The original synthesis recommended SPECTER2 and GTE as optional views. This was premature. The evidence supports:
- Models produce different rankings (stable finding)
- Some models find papers neither MiniLM nor TF-IDF surface (measured)
- AI reviewers describe these papers favorably (unvalidated)

The evidence does not support:
- That the different papers are valuable to researchers (no human evaluation)
- That specific models should be offered as named views (the "signal axis" labels are AI narratives)
- That the architecture should change based on this spike alone

**The architecture should remain model-agnostic** (Spike 003 already recommended this). Whether and which additional views to offer is an open question that requires human evaluation to close.

### View architecture — Open

Remains fully open. This spike produced characterization data but not quality data, UX evidence, or architectural guidance.

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

1. **Voyage 8% failure rate.** 160/2000 papers failed to embed due to API rate limiting. Effective pool ~1840 papers.
2. **CS/ML domain only.** SPECTER2's advantage on specialized vocabulary may be larger in physics, biology, or humanities. Cannot extrapolate.
3. **AI-assessed quality.** No human researcher confirmed that the divergent papers are actually valuable. The "absent researcher" remains absent.
4. **2000-paper sample.** Effects at full corpus scale (19K+) may differ. The sample validation was strong (GO) but inherently limited.
5. **Blind review gap.** Only SPECTER2 had complete blind comparative assessments. Other models' qualitative evidence is from non-blind characterization reviews.
6. **MiniLM-entangled profiles.** Models that structure the similarity space differently from MiniLM are evaluated using profiles built from MiniLM's structure. This is a structural disadvantage for challengers that the methodology acknowledges but cannot eliminate.
