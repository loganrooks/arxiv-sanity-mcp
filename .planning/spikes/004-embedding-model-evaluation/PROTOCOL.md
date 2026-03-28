---
status: execution-ready
addresses:
  - "Codex review blocker 1: protocol/claims mismatch on qualitative review coverage"
  - "Codex review blocker 2: challenger sample validation not executable"
  - "Codex review blocker 3: TF-IDF missing from comparison frame"
  - "Codex review blocker 4: embedding protocol under-specified"
  - "Codex major 5: Jaccard gatekeeping authority"
  - "Codex major 6: blocking gate enforcement"
  - "Codex moderate 9: decision-readiness criteria"
date: 2026-03-27
---

# Spike 004 Execution Protocol

This document resolves the blockers identified in the Codex design review (2026-03-21)
before execution. It supplements DESIGN.md — the design's epistemic commitments,
methodology rationale, and meta-methodology remain authoritative. This document
locks down the executable procedure.

## 1. Embedding Protocol (Blocker 4)

All models embed the same text: `title + "\n\n" + abstract`. Exceptions noted below.

| Model | Repo / API | Dim | Text format | Max tokens | Pooling | Normalization | Instructions |
|-------|-----------|-----|-------------|-----------|---------|---------------|-------------|
| all-MiniLM-L6-v2 | sentence-transformers | 384 | `title \n\n abstract` | 256 | Mean | L2 (post-embed) | None |
| SPECTER2 + proximity | allenai/specter2_base + adapter | 768 | `title [SEP] abstract` | 512 | CLS token | L2 (post-embed) | None |
| voyage-4 | Voyage API | 1024 | `title \n\n abstract` | API default | API-side | L2 (API returns normalized) | input_type="document" |
| Stella v5 400M | dunzhang/stella_en_400M_v5 | 1024 | `title \n\n abstract` | 512 | Mean (via encode) | L2 (post-embed) | `Instruct: Retrieve semantically similar research papers\nQuery: ` prefix for queries only; documents embedded without prefix |
| Qwen3-Embedding-0.6B | Qwen/Qwen3-Embedding-0.6B | — | `title \n\n abstract` | 512 | Mean (via encode) | L2 (post-embed) | Uses default task instruction from model config |
| GTE-large-en-v1.5 | Alibaba-NLP/gte-large-en-v1.5 | 1024 | `title \n\n abstract` | 512 | Mean (via encode) | L2 (post-embed) | None |

**Note on SPECTER2 format exception:** SPECTER2 uses `title [SEP] abstract` because that is its training convention. All other models use `title \n\n abstract` for consistency.

### Provenance recording

Each embedding run records in its checkpoint file:
- Model name, exact HuggingFace revision hash or API model string
- Embedding date/time
- torch version, CUDA version, sentence-transformers version
- For Voyage: API model name (cannot pin version — provider-side drift possible; interpretation confidence adjusted accordingly per Codex recommendation)
- Text format used, truncation applied, normalization method
- Number of papers embedded, any failures

### Scoring protocol

All models use the same scoring: **centroid cosine similarity**.
1. Compute centroid of seed paper embeddings (mean of L2-normalized vectors)
2. L2-normalize the centroid
3. Score = dot product of centroid with each paper's embedding
4. Rank by descending score

This matches the existing Spike 003 protocol exactly.

### TF-IDF protocol (for comparison frame — Blocker 3)

TF-IDF is included as a comparison target, not as an embedding model.
- Reuse existing infrastructure: `TfidfVectorizer(max_features=50000, stop_words="english")` on abstracts
- Same centroid scoring protocol
- Computed on the 2000-paper sample (not extracted from 19K — TF-IDF must be fit on the evaluation corpus)

## 2. Qualitative Review Coverage (Blocker 1)

The design claims "no verdict without qualitative review across all 8 profiles." The protocol now matches this claim with tiered coverage:

| Model classification | Profiles reviewed | Review depth | Blind comparison |
|---------------------|------------------|-------------|-----------------|
| **Divergent**: any profile Jaccard@20 < 0.8 with MiniLM | All 8 | Full W1 template | 2 most divergent profiles |
| **Mid-overlap**: all profiles 0.8-0.9 | 5 profiles (3 most divergent + 1 median + 1 highest overlap for contrast) | Full W1 template | 1 most divergent profile |
| **High-overlap**: all profiles > 0.9 | 3 profiles (2 most divergent + 1 random) | Abbreviated (set-level + emergent observations, skip per-paper) | None |
| **Near-identical**: all profiles > 0.95 | 2 profiles (most divergent + 1 random) | Abbreviated | None |

**Middle-band (0.8-0.9) is now explicitly specified** (Codex blocker 1 sub-issue).

**Classification uses multiple signals, not Jaccard alone** (Codex major 5):
A model is classified by its *most divergent* profile's Jaccard, but the classification can be **upgraded** (toward more review) if:
- Kendall's tau disagrees with Jaccard classification by 1+ tier
- Score distribution shows notably different separation characteristics
- Category recall diverges by >10pp on any profile

Classification can never be downgraded by non-Jaccard metrics. This addresses Jaccard's gatekeeping authority: it sets the floor, other metrics can only raise it.

## 3. Challenger Sample Validation (Blocker 2)

### Executable procedure

After embedding all models on the 2000-paper sample:

**Step 1 — MiniLM baseline validation:**
Compare MiniLM top-20 on 2000-paper sample vs full 19K corpus for P1, P3, P4.
- Pass: Jaccard > 0.8 for all 3 profiles
- This validates the sample preserves MiniLM's neighborhoods

**Step 2 — Challenger degeneracy check (per model, all 8 profiles):**
For each challenger model, compute top-20 scores per profile:
- **Score spread**: std(top-20 scores). Flag if < 0.005 (scores essentially identical)
- **Score gap**: mean(top-20) - mean(bottom-1980). Flag if < 0.01 (no discrimination)
- **Ceiling check**: max(score). Flag if < 0.15 (model finds nothing relevant in sample)

If any model is flagged on 3+ profiles: the sample may not contain that model's relevant papers. Record the flag and downgrade that model's extrapolation confidence.

**Step 3 — Structural comparison:**
For each challenger, compute Jaccard of its top-100 vs MiniLM's top-100 per profile.
If Jaccard@100 > 0.9 across all profiles, the models are drawing from the same pool — the sample works for both. If Jaccard@100 < 0.5 on any profile, the models disagree about which papers matter — investigate whether the sample is biased or the models genuinely differ.

### What this cannot do

This procedure detects degenerate challenger behavior on the sample but **cannot prove** the sample is representative from the challenger's perspective. Full validation would require full-corpus challenger embeddings, which is impractical for all models.

**Impact on findings**: All findings carry the caveat that the sample was validated primarily from MiniLM's perspective. Challenger-specific conclusions carry lower extrapolation confidence. This is stated once here and in the synthesis, not repeated per-finding.

## 4. TF-IDF in Comparison Frame (Blocker 3)

TF-IDF enters the comparison at Phase 2:

For each candidate model, compute:
1. **Model vs MiniLM** (existing design): all 7 quantitative metrics
2. **Model vs TF-IDF** (new): Jaccard@20/50/100, Kendall's tau, per-profile Jaccard

This enables answering: "Does Model X find papers that **both** MiniLM and TF-IDF miss?"

For any model showing promise in Phase 3 qualitative review, the synthesis addresses:
- Is it a better *complement* to MiniLM than TF-IDF? (finds different things)
- Is it a better *replacement* for MiniLM? (finds similar things, better)
- Does it add a genuinely *third* signal axis?

The decision frame for architecture implications is: `MiniLM + TF-IDF` is the current baseline. Any recommended change must justify itself against this pair, not just against MiniLM alone.

## 5. Pre-Synthesis Checklist (Codex Major 6)

Before any synthesis or verdict, this checklist must be satisfied. The automation enforces this via checkpoint files — Phase 4 scripts refuse to run unless all checkpoints exist.

```
[ ] Phase 1 checkpoint: all models embedded, provenance recorded
[ ] Phase 1 checkpoint: sample validation complete (go/no-go recorded)
[ ] Phase 2 checkpoint: all quantitative metrics computed for all models
[ ] Phase 2 checkpoint: branch classification recorded with justification
[ ] Phase 3 checkpoint: qualitative reviews complete per coverage table
[ ] Phase 3 checkpoint: pre-synthesis review — any anomalies flagged?
[ ] Limitations updated with any execution-time discoveries
```

## 6. Decision-Readiness Classes (Codex Moderate 9)

Synthesis outputs use exactly these classes:

| Class | Meaning | Evidence required |
|-------|---------|------------------|
| **Retain default** | MiniLM + TF-IDF remains the best provisional arrangement | No model shows qualitatively valuable divergence across profiles |
| **Candidate: optional experimental view** | Model X merits being offered as an additional view | Quantitative divergence + qualitative value on 2+ profiles |
| **Candidate: further investigation** | Model X shows promise under conditions our methodology can't fully assess | Suggestive but not conclusive evidence; specific conditions named |
| **Evidence insufficient** | The spike's methodology cannot answer the question for this model | Degenerate sample, rate limit failures, anomalous results |

Architecture revision (changing the default second view, replacing MiniLM) requires evidence this spike **cannot plausibly supply**. Per the Codex review: any architectural claim remains at most "Chosen for now" unless the evidence base becomes stronger than this design can deliver.

## 7. Automation and Gate Enforcement

### Checkpoint files

Each phase writes a JSON checkpoint to `experiments/checkpoints/`:
- `phase1_embeddings.json` — provenance, timing, any failures
- `phase1_validation.json` — sample validation results, go/no-go
- `phase2_metrics.json` — all quantitative results
- `phase2_classification.json` — branch classification per model with justification
- `phase3_reviews.json` — review completion status, coverage verification
- `phase4_synthesis.json` — final synthesis metadata

Each phase script checks for required predecessor checkpoints before running.

### Git workflow

- Design revision (this PROTOCOL.md + scripts): 1 commit
- Phase 1 (embed + validate): 1 commit with results
- Phase 2 (metrics): 1 commit with results
- Phase 3 (reviews): 1 commit per review batch
- Phase 4 (synthesis): 1 commit with FINDINGS.md and DECISION.md

### Responsiveness clause

Per DESIGN.md principle 16: if execution reveals that this protocol needs revision (a metric is measuring the wrong thing, a gate is too strict/lenient, an anomaly suggests the assumptions are off), the protocol is revised and the revision is documented in the commit message. The protocol is a plan, not a contract.
