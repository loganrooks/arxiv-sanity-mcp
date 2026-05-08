"""
W2.1: Feature input sensitivity -- title-only embeddings.

Tests whether title-only embeddings are a viable cheaper alternative to
abstract-based embeddings. Computes title-only MiniLM and SPECTER2 adapter
embeddings for all 19K papers, then profiles strategies S1g and S1h using
the same evaluation harness as W1A.

Comparison against W1A abstract-based profiles:
  S1g (title MiniLM) vs S1a (abstract MiniLM)
  S1h (title SPECTER2) vs S1c (abstract SPECTER2)

Branch point BP3: if quality drop is within 10%, title-only is viable.

Requires: conda activate ml-dev (torch 2.2.0+cu118 for GTX 1080 Ti)
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

EXPERIMENTS_DIR = Path(__file__).resolve().parent
SPIKE_003_DIR = EXPERIMENTS_DIR.parent
sys.path.insert(0, str(EXPERIMENTS_DIR))

SPIKE_001_DATA = (
    SPIKE_003_DIR.parent
    / "001-volume-filtering-scoring-landscape"
    / "experiments"
    / "data"
)
SPIKE_002_DATA = (
    SPIKE_003_DIR.parent / "002-backend-comparison" / "experiments" / "data"
)
SPIKE_003_DATA = SPIKE_003_DIR / "experiments" / "data"

SOURCE_DB = SPIKE_001_DATA / "spike_001_harvest.db"

# Existing abstract-based embeddings and IDs (for profiler loading)
MINILM_EMB_PATH = SPIKE_002_DATA / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DATA / "arxiv_ids_19k.json"
SPECTER2_EMB_PATH = SPIKE_003_DATA / "specter2_adapter_19k.npy"
SPECTER2_IDS_PATH = SPIKE_003_DATA / "specter2_adapter_ids.json"
PROFILES_PATH = SPIKE_003_DATA / "interest_profiles.json"
W1A_RESULTS_PATH = SPIKE_003_DATA / "w1a_content_profiles.json"

# Title-only embedding outputs
MINILM_TITLE_PATH = SPIKE_003_DATA / "miniLM_title_19k.npy"
SPECTER2_TITLE_PATH = SPIKE_003_DATA / "specter2_title_19k.npy"
OUTPUT_PATH = SPIKE_003_DATA / "w2_1_title_profiles.json"

EMBED_BATCH_SIZE = 64


class NumpyEncoder(json.JSONEncoder):
    """Handle numpy types in JSON serialization."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_papers():
    """Load all papers with titles from the corpus.

    Returns papers in the same order as the embedding ID files,
    verified against specter2_adapter_ids.json.
    """
    # Load canonical ID ordering
    with open(SPECTER2_IDS_PATH) as f:
        canonical_ids = json.load(f)
    canonical_set = set(canonical_ids)

    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract FROM papers "
        "WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()

    # Build lookup
    paper_map = {r["arxiv_id"]: dict(r) for r in rows}

    # Return in canonical order, filtering to papers with embeddings
    papers = []
    for aid in canonical_ids:
        if aid in paper_map:
            papers.append(paper_map[aid])
        else:
            # Should not happen -- but safety
            papers.append({"arxiv_id": aid, "title": "", "abstract": ""})

    assert len(papers) == len(canonical_ids), (
        f"Paper count {len(papers)} != canonical IDs {len(canonical_ids)}"
    )
    return papers, canonical_ids


# ---------------------------------------------------------------------------
# Embedding computation
# ---------------------------------------------------------------------------

def embed_batch(texts, tokenizer, model, max_length=512):
    """Embed a batch of texts, return CLS token embeddings."""
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    ).to("cuda")
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings.cpu().numpy()


def compute_embeddings(texts, tokenizer, model, label=""):
    """Compute L2-normalized embeddings for all texts in batches."""
    n = len(texts)
    all_embeddings = []
    t0 = time.perf_counter()

    for i in range(0, n, EMBED_BATCH_SIZE):
        batch = texts[i : i + EMBED_BATCH_SIZE]
        emb = embed_batch(batch, tokenizer, model)
        all_embeddings.append(emb)

        if (i // EMBED_BATCH_SIZE) % 50 == 0:
            elapsed = time.perf_counter() - t0
            done = i + len(batch)
            rate = done / elapsed if elapsed > 0 else 0
            eta = (n - done) / rate if rate > 0 else 0
            print(
                f"  [{label}] {done:6d}/{n} ({100*done/n:.1f}%) "
                f"| {elapsed:.0f}s elapsed | ~{eta:.0f}s remaining"
            )

    total_time = time.perf_counter() - t0
    embeddings = np.concatenate(all_embeddings, axis=0).astype(np.float32)

    # L2 normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-10)
    embeddings = embeddings / norms

    print(f"  [{label}] Total: {n} texts in {total_time:.1f}s "
          f"({total_time/n*1000:.2f}ms/text)")
    print(f"  [{label}] Shape: {embeddings.shape}, dtype: {embeddings.dtype}")

    # Verify normalization
    check_norms = np.linalg.norm(embeddings[:10], axis=1)
    assert np.allclose(check_norms, 1.0, atol=1e-5), (
        f"Normalization failed: {check_norms}"
    )

    return embeddings, total_time


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_minilm():
    """Load MiniLM model for title embedding."""
    from sentence_transformers import SentenceTransformer

    print("Loading MiniLM (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
    return model


def load_specter2_adapter():
    """Load SPECTER2 base + proximity adapter."""
    from adapters import AutoAdapterModel
    from transformers import AutoTokenizer

    print("Loading SPECTER2 base model...")
    tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
    model = AutoAdapterModel.from_pretrained("allenai/specter2_base")

    print("Loading proximity adapter...")
    model.load_adapter(
        "allenai/specter2",
        source="hf",
        load_as="specter2_proximity",
        set_active=True,
    )
    print("Adapter loaded and set active")
    model.eval()
    model.to("cuda")
    return tokenizer, model


# ---------------------------------------------------------------------------
# Phase 1: Compute title-only embeddings
# ---------------------------------------------------------------------------

def phase1_compute_title_embeddings(papers, canonical_ids):
    """Compute title-only embeddings for both models."""
    print("\n" + "=" * 70)
    print("PHASE 1: Compute title-only embeddings")
    print("=" * 70)

    titles = [p["title"] for p in papers]
    title_lengths = [len(t.split()) for t in titles]
    print(f"  Title stats: n={len(titles)}, "
          f"mean_words={np.mean(title_lengths):.1f}, "
          f"median_words={np.median(title_lengths):.0f}, "
          f"max_words={max(title_lengths)}")

    results = {}

    # --- MiniLM title embeddings ---
    print("\n--- MiniLM title-only embeddings ---")
    minilm = load_minilm()

    # SentenceTransformer uses its own encode method
    t0 = time.perf_counter()
    minilm_title_emb = minilm.encode(
        titles,
        batch_size=EMBED_BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        device="cuda",
    )
    minilm_time = time.perf_counter() - t0
    minilm_title_emb = minilm_title_emb.astype(np.float32)

    # Verify normalization
    check = np.linalg.norm(minilm_title_emb[:10], axis=1)
    assert np.allclose(check, 1.0, atol=1e-5), f"MiniLM norm check failed: {check}"
    print(f"  MiniLM title: {minilm_title_emb.shape}, {minilm_time:.1f}s "
          f"({minilm_time/len(titles)*1000:.2f}ms/title)")

    # Save
    np.save(MINILM_TITLE_PATH, minilm_title_emb)
    print(f"  Saved: {MINILM_TITLE_PATH} ({minilm_title_emb.nbytes / 1024 / 1024:.1f} MB)")

    results["minilm"] = {
        "model": "all-MiniLM-L6-v2",
        "input": "title only",
        "dim": int(minilm_title_emb.shape[1]),
        "n_papers": int(minilm_title_emb.shape[0]),
        "compute_time_s": round(minilm_time, 2),
        "per_paper_ms": round(minilm_time / len(titles) * 1000, 3),
        "memory_mb": round(minilm_title_emb.nbytes / 1024 / 1024, 1),
    }

    del minilm
    torch.cuda.empty_cache()

    # --- SPECTER2 adapter title embeddings ---
    print("\n--- SPECTER2 adapter title-only embeddings ---")
    tokenizer, specter2_model = load_specter2_adapter()

    # SPECTER2 title-only: just the title, no [SEP] abstract
    specter2_title_emb, specter2_time = compute_embeddings(
        titles, tokenizer, specter2_model, label="SPECTER2-title"
    )

    # Save
    np.save(SPECTER2_TITLE_PATH, specter2_title_emb)
    print(f"  Saved: {SPECTER2_TITLE_PATH} ({specter2_title_emb.nbytes / 1024 / 1024:.1f} MB)")

    results["specter2"] = {
        "model": "allenai/specter2_base + proximity adapter",
        "input": "title only",
        "dim": int(specter2_title_emb.shape[1]),
        "n_papers": int(specter2_title_emb.shape[0]),
        "compute_time_s": round(specter2_time, 2),
        "per_paper_ms": round(specter2_time / len(titles) * 1000, 3),
        "memory_mb": round(specter2_title_emb.nbytes / 1024 / 1024, 1),
    }

    del specter2_model
    torch.cuda.empty_cache()

    # --- Similarity between title-only and abstract embeddings ---
    print("\n--- Title vs Abstract embedding similarity ---")

    # MiniLM: compare title-only vs abstract embeddings
    minilm_abstract_emb = np.load(MINILM_EMB_PATH)
    cos_sims = np.sum(minilm_title_emb * minilm_abstract_emb, axis=1)
    results["minilm_title_vs_abstract"] = {
        "cosine_mean": round(float(np.mean(cos_sims)), 4),
        "cosine_std": round(float(np.std(cos_sims)), 4),
        "cosine_median": round(float(np.median(cos_sims)), 4),
        "cosine_min": round(float(np.min(cos_sims)), 4),
        "cosine_max": round(float(np.max(cos_sims)), 4),
    }
    print(f"  MiniLM title-vs-abstract cosine: "
          f"mean={np.mean(cos_sims):.4f}, std={np.std(cos_sims):.4f}, "
          f"median={np.median(cos_sims):.4f}")

    # SPECTER2: compare title-only vs abstract embeddings
    specter2_abstract_emb = np.load(SPECTER2_EMB_PATH)
    cos_sims2 = np.sum(specter2_title_emb * specter2_abstract_emb, axis=1)
    results["specter2_title_vs_abstract"] = {
        "cosine_mean": round(float(np.mean(cos_sims2)), 4),
        "cosine_std": round(float(np.std(cos_sims2)), 4),
        "cosine_median": round(float(np.median(cos_sims2)), 4),
        "cosine_min": round(float(np.min(cos_sims2)), 4),
        "cosine_max": round(float(np.max(cos_sims2)), 4),
    }
    print(f"  SPECTER2 title-vs-abstract cosine: "
          f"mean={np.mean(cos_sims2):.4f}, std={np.std(cos_sims2):.4f}, "
          f"median={np.median(cos_sims2):.4f}")

    return minilm_title_emb, specter2_title_emb, results


# ---------------------------------------------------------------------------
# Phase 2: Profile title-only strategies using harness
# ---------------------------------------------------------------------------

def phase2_profile_strategies(minilm_title_emb, specter2_title_emb, canonical_ids):
    """Profile S1g (MiniLM title) and S1h (SPECTER2 title)."""
    print("\n" + "=" * 70)
    print("PHASE 2: Profile title-only strategies")
    print("=" * 70)

    from harness import StrategyProfiler
    from harness.strategy_protocol import SimpleStrategy
    from harness.resource_meter import measure_storage

    # Load profiler with ABSTRACT embeddings (for clustering, instruments, etc.)
    # The profiler's clustering and instruments use the standard MiniLM abstract
    # embeddings. We only swap in title embeddings for the strategies themselves.
    profiler = StrategyProfiler.from_spike_data(
        db_path=str(SOURCE_DB),
        minilm_emb_path=str(MINILM_EMB_PATH),
        minilm_ids_path=str(MINILM_IDS_PATH),
        profiles_path=str(PROFILES_PATH),
        specter2_emb_path=str(SPECTER2_EMB_PATH),
        specter2_ids_path=str(SPECTER2_IDS_PATH),
    )

    paper_ids = profiler.paper_ids
    id_to_idx = profiler.id_to_idx

    # Build title embedding id_to_idx (same ordering as canonical)
    title_id_to_idx = {aid: i for i, aid in enumerate(canonical_ids)}

    # --- S1g: MiniLM title-only centroid similarity ---
    print("\n[S1g] MiniLM title-only centroid similarity")

    def s1g_score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [title_id_to_idx[sid] for sid in seed_ids
                        if sid in title_id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = minilm_title_emb[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        scores = minilm_title_emb @ centroid
        return scores

    s1g = SimpleStrategy(
        name="MiniLM title-only centroid",
        strategy_id="S1g",
        score_fn=s1g_score_fn,
        paper_ids=paper_ids,
    )

    # --- S1h: SPECTER2 adapter title-only centroid similarity ---
    print("\n[S1h] SPECTER2 adapter title-only centroid similarity")

    def s1h_score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [title_id_to_idx[sid] for sid in seed_ids
                        if sid in title_id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = specter2_title_emb[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        scores = specter2_title_emb @ centroid
        return scores

    s1h = SimpleStrategy(
        name="SPECTER2 adapter title-only centroid",
        strategy_id="S1h",
        score_fn=s1h_score_fn,
        paper_ids=paper_ids,
    )

    # --- Profile both ---
    all_cards = []
    strategy_timings = {}

    for strategy, config in [
        (s1g, {"embedding": "MiniLM", "dim": 384, "input": "title_only",
                "centroid": "normalized"}),
        (s1h, {"embedding": "SPECTER2_adapter", "dim": 768, "input": "title_only",
                "centroid": "normalized"}),
    ]:
        print(f"\n{'='*60}")
        print(f"PROFILING: {strategy.name} ({strategy.strategy_id})")
        print(f"{'='*60}")
        t0 = time.perf_counter()

        card = profiler.profile(
            strategy,
            config=config,
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=100,
        )
        t1 = time.perf_counter()
        strategy_timings[strategy.strategy_id] = t1 - t0

        # Print summary
        print(f"\n  --- Summary for {strategy.strategy_id} ---")
        instruments = card.get("instruments", {})
        for inst_name in [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]:
            inst = instruments.get(inst_name, {})
            mean = inst.get("mean")
            std = inst.get("std")
            if mean is not None:
                print(f"    {inst_name:<25s} {mean:.4f} (+/- {std:.4f})")

        res = card.get("resources", {})
        lat = res.get("query_latency_ms", {})
        if lat:
            print(f"    latency p50={lat.get('p50', 0):.2f}ms  "
                  f"p95={lat.get('p95', 0):.2f}ms")
        print(f"    profiling time: {strategy_timings[strategy.strategy_id]:.1f}s")

        all_cards.append(card)

    # Storage footprint
    storage_info = {}
    storage_info["S1g"] = measure_storage(
        [str(MINILM_TITLE_PATH)]
    )
    storage_info["S1h"] = measure_storage(
        [str(SPECTER2_TITLE_PATH)]
    )

    return all_cards, strategy_timings, storage_info, profiler


# ---------------------------------------------------------------------------
# Phase 3: Compare against W1A abstract-based profiles
# ---------------------------------------------------------------------------

def phase3_compare_with_w1a(title_cards):
    """Load W1A results and compare title-only vs abstract metrics."""
    print("\n" + "=" * 70)
    print("PHASE 3: Title-only vs Abstract comparison (BP3 evaluation)")
    print("=" * 70)

    with open(W1A_RESULTS_PATH) as f:
        w1a_data = json.load(f)

    # Extract abstract-based cards for S1a and S1c
    abstract_cards = {}
    for card in w1a_data["profile_cards"]:
        if card["strategy_id"] in ("S1a", "S1c"):
            abstract_cards[card["strategy_id"]] = card

    # Build title card lookup
    title_card_map = {c["strategy_id"]: c for c in title_cards}

    instrument_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]

    comparisons = {}
    print(f"\n{'Metric':<28s} {'Abstract':>10s} {'Title':>10s} {'Delta':>10s} {'Pct':>8s} {'Within10%':>10s}")
    print("-" * 80)

    for pair_label, abstract_sid, title_sid in [
        ("MiniLM", "S1a", "S1g"),
        ("SPECTER2", "S1c", "S1h"),
    ]:
        print(f"\n--- {pair_label} ---")
        abstract_card = abstract_cards[abstract_sid]
        title_card = title_card_map[title_sid]

        pair_comparison = {}
        for inst_name in instrument_names:
            abstract_val = abstract_card["instruments"].get(inst_name, {}).get("mean")
            title_val = title_card["instruments"].get(inst_name, {}).get("mean")

            if abstract_val is not None and title_val is not None:
                delta = title_val - abstract_val
                # Percentage change (relative to abstract baseline)
                if abs(abstract_val) > 1e-10:
                    pct_change = (delta / abs(abstract_val)) * 100
                else:
                    pct_change = 0.0 if abs(delta) < 1e-10 else float("inf")

                # For most instruments, higher is better (MRR, proximity,
                # coherence, coverage). For diversity/novelty/surprise,
                # the direction depends on interpretation.
                # BP3 criterion: quality drop within 10% of abstract baseline
                # We check the absolute percentage change for key quality metrics.
                within_10 = abs(pct_change) <= 10.0

                entry = {
                    "abstract_mean": round(float(abstract_val), 4),
                    "title_mean": round(float(title_val), 4),
                    "delta": round(float(delta), 4),
                    "pct_change": round(float(pct_change), 2),
                    "within_10_pct": within_10,
                }
                pair_comparison[inst_name] = entry

                print(f"  {inst_name:<26s} {abstract_val:10.4f} {title_val:10.4f} "
                      f"{delta:+10.4f} {pct_change:+7.1f}% "
                      f"{'YES' if within_10 else 'NO':>10s}")
            else:
                pair_comparison[inst_name] = {
                    "abstract_mean": abstract_val,
                    "title_mean": title_val,
                    "delta": None,
                    "pct_change": None,
                    "within_10_pct": None,
                }

        # Also compare latency
        abstract_lat = abstract_card.get("resources", {}).get("query_latency_ms", {})
        title_lat = title_card.get("resources", {}).get("query_latency_ms", {})
        pair_comparison["latency_p50_ms"] = {
            "abstract": abstract_lat.get("p50"),
            "title": title_lat.get("p50"),
        }
        pair_comparison["latency_p95_ms"] = {
            "abstract": abstract_lat.get("p95"),
            "title": title_lat.get("p95"),
        }

        comparisons[pair_label] = {
            "abstract_strategy": abstract_sid,
            "title_strategy": title_sid,
            "instruments": pair_comparison,
        }

    # --- BP3 verdict ---
    # Key quality metrics for the decision: LOO-MRR and coverage
    print(f"\n{'='*60}")
    print("BP3 VERDICT: Is title-only within 10% of abstract?")
    print(f"{'='*60}")

    key_metrics = ["leave_one_out_mrr", "coverage", "seed_proximity", "topical_coherence"]
    for pair_label in ["MiniLM", "SPECTER2"]:
        comp = comparisons[pair_label]["instruments"]
        verdicts = []
        for m in key_metrics:
            entry = comp.get(m, {})
            pct = entry.get("pct_change")
            within = entry.get("within_10_pct")
            verdicts.append(within)
            status = "PASS" if within else "FAIL" if within is not None else "N/A"
            print(f"  {pair_label} {m}: {status} ({pct:+.1f}%)" if pct is not None else
                  f"  {pair_label} {m}: N/A")

        all_pass = all(v for v in verdicts if v is not None)
        comparisons[pair_label]["bp3_all_key_metrics_within_10_pct"] = all_pass
        print(f"  => {pair_label} BP3 overall: {'VIABLE' if all_pass else 'NOT VIABLE'}")

    return comparisons


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("W2.1: Feature Input Sensitivity -- Title-Only Embeddings")
    print("=" * 70)
    t_start = time.perf_counter()

    # Load papers
    papers, canonical_ids = load_papers()
    print(f"Loaded {len(papers)} papers")

    # Phase 1: Compute title-only embeddings
    minilm_title_emb, specter2_title_emb, embedding_results = (
        phase1_compute_title_embeddings(papers, canonical_ids)
    )

    # Phase 2: Profile title-only strategies
    title_cards, strategy_timings, storage_info, profiler = (
        phase2_profile_strategies(minilm_title_emb, specter2_title_emb, canonical_ids)
    )

    # Phase 3: Compare against W1A
    comparisons = phase3_compare_with_w1a(title_cards)

    # ----- Comparison table -----
    print(f"\n{'='*60}")
    print("CROSS-STRATEGY COMPARISON (title-only)")
    print(f"{'='*60}")
    comparison_data = profiler.compare(title_cards)

    print(f"\n{'Strategy':<40s} {'MRR':>7s} {'Prox':>7s} {'Coher':>7s} {'Div':>7s} "
          f"{'Novel':>7s} {'Surpr':>7s} {'Cover':>7s} {'p50ms':>7s}")
    print("-" * 110)
    for card in title_cards:
        inst = card.get("instruments", {})
        lat = card.get("resources", {}).get("query_latency_ms", {})

        def fmt(v, width=7):
            return f"{v:{width}.4f}" if v is not None else f"{'N/A':>{width}s}"

        mrr = inst.get("leave_one_out_mrr", {}).get("mean")
        prox = inst.get("seed_proximity", {}).get("mean")
        coher = inst.get("topical_coherence", {}).get("mean")
        div_ = inst.get("cluster_diversity", {}).get("mean")
        nov = inst.get("novelty", {}).get("mean")
        surp = inst.get("category_surprise", {}).get("mean")
        cov = inst.get("coverage", {}).get("mean")
        p50 = lat.get("p50")

        name = f"{card['strategy_name']} ({card['strategy_id']})"[:38]
        print(f"{name:<40s} {fmt(mrr)} {fmt(prox)} {fmt(coher)} {fmt(div_)} "
              f"{fmt(nov)} {fmt(surp)} {fmt(cov)} {fmt(p50)}")

    # ----- Save results -----
    total_time = time.perf_counter() - t_start

    output = {
        "experiment": "W2.1: Feature input sensitivity -- title-only embeddings",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_time_s": round(total_time, 1),
        "corpus_size": len(papers),
        "embedding_computation": embedding_results,
        "profile_cards": [c for c in title_cards],
        "comparison_vs_abstract": comparisons,
        "cross_strategy_comparison": comparison_data,
        "storage": storage_info,
        "strategy_profiling_times_s": {
            k: round(v, 1) for k, v in strategy_timings.items()
        },
        "environment": {
            "conda_env": "ml-dev",
            "torch": torch.__version__,
            "cuda": str(torch.cuda.is_available()),
            "gpu": (torch.cuda.get_device_name(0)
                    if torch.cuda.is_available() else "N/A"),
        },
        "notes": {
            "bp3_criterion": "Title-only viable if quality drop within 10% of abstract "
                             "on key metrics (LOO-MRR, coverage, seed_proximity, "
                             "topical_coherence).",
            "clustering_note": "Clustering for instruments uses MiniLM abstract embeddings "
                               "(same as W1A) to ensure fair comparison. Only the scoring "
                               "strategy uses title-only embeddings.",
            "specter2_input_format": "Title only (no [SEP] abstract). SPECTER2 was trained "
                                     "on 'title [SEP] abstract' format, so title-only may "
                                     "produce suboptimal embeddings.",
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\n{'='*70}")
    print("W2.1 COMPLETE")
    print(f"{'='*70}")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")
    print(f"MiniLM title embeddings: {MINILM_TITLE_PATH}")
    print(f"SPECTER2 title embeddings: {SPECTER2_TITLE_PATH}")

    return output


if __name__ == "__main__":
    main()
