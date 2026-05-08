#!/usr/bin/env python3
"""
Spike 003 / W5: Voyage AI Embedding Screening

Phase 1: Screen voyage-4 and voyage-4-large on a 100-paper sample to determine
whether they capture a signal distinct from local models (MiniLM, SPECTER2).

Metric: Pairwise Jaccard overlap of top-20 neighbor lists across 10 seed papers.

Decision thresholds:
  - Jaccard > 0.8 with MiniLM => redundant, stop
  - Jaccard < 0.6 with BOTH local models => genuinely different signal, proceed to Phase 2
  - Heavy overlap with one but not other => better version of that model, not new signal

Rate limits (no payment method): 3 RPM, 10K TPM.
Strategy: batch 15 papers (~5K tokens) at a time, 65s pause between batches.
"""

import json
import os
import sys
import time
import sqlite3
import numpy as np
from pathlib import Path

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

# ---- Configuration ----
PROJECT_ROOT = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp")
SPIKE_DIR = PROJECT_ROOT / ".planning/spikes/003-strategy-profiling"
DATA_DIR = SPIKE_DIR / "experiments/data"
HARVEST_DB = PROJECT_ROOT / ".planning/spikes/001-volume-filtering-scoring-landscape/experiments/data/spike_001_harvest.db"
ARXIV_IDS_FILE = PROJECT_ROOT / ".planning/spikes/002-backend-comparison/experiments/data/arxiv_ids_19k.json"
MINIML_EMB_FILE = DATA_DIR / "miniLM_title_19k.npy"
SPECTER2_EMB_FILE = DATA_DIR / "specter2_adapter_19k.npy"
PROFILES_FILE = DATA_DIR / "interest_profiles.json"
OUTPUT_FILE = DATA_DIR / "w5_voyage_screening_results.json"

SAMPLE_SIZE = 100
TOP_K = 20
# Conservative rate-limited batch: 15 papers * ~350 tokens = ~5250 tokens (well under 10K TPM)
RATE_LIMITED_BATCH_SIZE = 15
BATCH_PAUSE_SECONDS = 65


def load_api_key():
    env_path = PROJECT_ROOT / ".env"
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                if key.strip() == 'VOYAGE_API_KEY':
                    return val.strip()
    raise RuntimeError("VOYAGE_API_KEY not found in .env")


def build_sample():
    """Select 100 papers: P1 seeds + held-out + P3 seeds + held-out + random fill."""
    print("\n=== STEP 1: Building 100-paper sample ===")

    with open(PROFILES_FILE) as f:
        profiles = json.load(f)
    with open(ARXIV_IDS_FILE) as f:
        all_ids = json.load(f)

    p1_seeds = [s["arxiv_id"] for s in profiles["profiles"]["P1"]["seed_papers"]]
    p3_seeds = [s["arxiv_id"] for s in profiles["profiles"]["P3"]["seed_papers"]]
    p1_heldout = [s["arxiv_id"] for s in profiles["profiles"]["P1"]["held_out_papers"]]
    p3_heldout = [s["arxiv_id"] for s in profiles["profiles"]["P3"]["held_out_papers"]]

    seed_ids = set(p1_seeds + p3_seeds + p1_heldout + p3_heldout)
    print(f"  Seed + held-out papers: {len(seed_ids)}")

    rng = np.random.RandomState(42)
    non_seed_ids = [aid for aid in all_ids if aid not in seed_ids]
    n_random = SAMPLE_SIZE - len(seed_ids)
    if n_random > 0:
        random_ids = list(rng.choice(non_seed_ids, size=n_random, replace=False))
    else:
        random_ids = []
        seed_ids = set(list(seed_ids)[:SAMPLE_SIZE])

    sample_ids = list(seed_ids) + random_ids
    print(f"  Total sample: {len(sample_ids)} ({len(seed_ids)} seed/heldout + {len(random_ids)} random)")

    query_seeds_p1 = profiles["profiles"]["P1"]["seed_subsets"]["subset_5"]
    query_seeds_p3 = profiles["profiles"]["P3"]["seed_subsets"]["subset_5"]

    return sample_ids, query_seeds_p1, query_seeds_p3


def get_paper_texts(sample_ids):
    """Fetch title + abstract for each paper from harvest DB."""
    print("\n=== STEP 2: Fetching paper texts ===")

    db = sqlite3.connect(str(HARVEST_DB))
    cursor = db.cursor()
    placeholders = ",".join("?" for _ in sample_ids)
    cursor.execute(
        f"SELECT arxiv_id, title, abstract FROM papers WHERE arxiv_id IN ({placeholders})",
        sample_ids
    )
    texts = {}
    for row in cursor.fetchall():
        arxiv_id, title, abstract = row
        text = f"{title}\n\n{abstract}" if abstract else title
        texts[arxiv_id] = text
    db.close()
    print(f"  Fetched texts for {len(texts)} papers")
    return texts


def get_local_embeddings(sample_ids):
    """Load MiniLM and SPECTER2 embeddings for the sample papers."""
    print("\n=== STEP 3: Loading local model embeddings ===")

    with open(ARXIV_IDS_FILE) as f:
        all_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(all_ids)}

    miniml_all = np.load(str(MINIML_EMB_FILE))
    specter_all = np.load(str(SPECTER2_EMB_FILE))
    print(f"  MiniLM full: {miniml_all.shape}, SPECTER2 full: {specter_all.shape}")

    sample_indices = []
    valid_ids = []
    for aid in sample_ids:
        if aid in id_to_idx:
            sample_indices.append(id_to_idx[aid])
            valid_ids.append(aid)

    sample_indices = np.array(sample_indices)
    miniml_sample = miniml_all[sample_indices]
    specter_sample = specter_all[sample_indices]

    # L2 normalize
    for arr in [miniml_sample, specter_sample]:
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1
        arr /= norms

    print(f"  MiniLM sample: {miniml_sample.shape}, SPECTER2 sample: {specter_sample.shape}")
    return valid_ids, miniml_sample, specter_sample


def embed_voyage_single_model(api_key, texts_list, model_name):
    """Embed texts with a single Voyage model, handling rate limits.

    Strategy: 15-paper batches, 65s pause. On rate limit error, wait longer and retry.
    """
    import voyageai

    vo = voyageai.Client(api_key=api_key)
    all_embeddings = []
    n_batches = (len(texts_list) + RATE_LIMITED_BATCH_SIZE - 1) // RATE_LIMITED_BATCH_SIZE

    for batch_idx in range(n_batches):
        start = batch_idx * RATE_LIMITED_BATCH_SIZE
        end = min(start + RATE_LIMITED_BATCH_SIZE, len(texts_list))
        batch = texts_list[start:end]
        est_tokens = sum(len(t) // 4 for t in batch)

        print(f"    Batch {batch_idx + 1}/{n_batches}: {len(batch)} texts (~{est_tokens} tok)")

        success = False
        for attempt in range(5):
            try:
                result = vo.embed(batch, model=model_name, input_type="document")
                all_embeddings.extend(result.embeddings)
                success = True
                break
            except Exception as e:
                err_str = str(e).lower()
                if "rate" in err_str or "429" in err_str or "limit" in err_str:
                    wait = BATCH_PAUSE_SECONDS * (attempt + 1)
                    print(f"    Rate limited (attempt {attempt + 1}/5), waiting {wait}s...")
                    sys.stdout.flush()
                    time.sleep(wait)
                else:
                    print(f"    ERROR: {e}")
                    raise

        if not success:
            raise RuntimeError(f"Failed to embed batch {batch_idx + 1} after 5 attempts")

        # Pause between batches
        if batch_idx < n_batches - 1:
            print(f"    Pausing {BATCH_PAUSE_SECONDS}s...")
            sys.stdout.flush()
            time.sleep(BATCH_PAUSE_SECONDS)

    embeddings = np.array(all_embeddings, dtype=np.float32)
    print(f"    Result: {embeddings.shape}")
    return embeddings


def embed_with_voyage_models(api_key, sample_ids, texts):
    """Embed sample with both voyage-4 and voyage-4-large."""
    print("\n=== STEP 4: Embedding with Voyage AI ===")
    ordered_texts = [texts[aid] for aid in sample_ids]
    n_batches = (len(ordered_texts) + RATE_LIMITED_BATCH_SIZE - 1) // RATE_LIMITED_BATCH_SIZE
    est_time_min = (n_batches * BATCH_PAUSE_SECONDS * 2 + BATCH_PAUSE_SECONDS) / 60
    print(f"  {len(ordered_texts)} papers, {n_batches} batches/model, ~{est_time_min:.1f} min total")

    results = {}
    for model_name in ["voyage-4", "voyage-4-large"]:
        print(f"\n  --- {model_name} ---")
        t0 = time.time()
        embeddings = embed_voyage_single_model(api_key, ordered_texts, model_name)
        elapsed = time.time() - t0

        # L2 normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1
        embeddings = embeddings / norms

        results[model_name] = {
            "embeddings": embeddings,
            "dim": embeddings.shape[1],
            "elapsed_s": round(elapsed, 2),
        }
        print(f"    Dim: {embeddings.shape[1]}, Time: {elapsed:.1f}s")

        # Pause between models
        if model_name == "voyage-4":
            print(f"\n  Pausing {BATCH_PAUSE_SECONDS}s before next model...")
            sys.stdout.flush()
            time.sleep(BATCH_PAUSE_SECONDS)

    return results


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def compute_overlap_analysis(sample_ids, query_seed_ids, embeddings_dict):
    """Compute top-K neighbor overlap across all models for each query seed."""
    print("\n=== STEP 5: Computing neighbor overlap ===")

    id_to_idx = {aid: i for i, aid in enumerate(sample_ids)}
    model_names = list(embeddings_dict.keys())

    # Build similarity matrices
    sim_matrices = {}
    for name, emb in embeddings_dict.items():
        sim_matrices[name] = emb @ emb.T
        print(f"  Sim matrix for {name}: {sim_matrices[name].shape}")

    all_results = []
    for seed_id in query_seed_ids:
        if seed_id not in id_to_idx:
            print(f"  WARNING: seed {seed_id} not in sample, skipping")
            continue

        seed_idx = id_to_idx[seed_id]
        neighbors = {}
        neighbor_ids = {}

        for name in model_names:
            scores = sim_matrices[name][seed_idx].copy()
            scores[seed_idx] = -np.inf
            top_k = set(np.argsort(scores)[::-1][:TOP_K].tolist())
            neighbors[name] = top_k
            neighbor_ids[name] = [sample_ids[i] for i in sorted(top_k)]

        pairwise = {}
        for i, m1 in enumerate(model_names):
            for m2 in model_names[i + 1:]:
                pair_name = f"{m1} vs {m2}"
                pairwise[pair_name] = round(jaccard(neighbors[m1], neighbors[m2]), 4)

        all_results.append({
            "seed_id": seed_id,
            "pairwise_jaccard": pairwise,
            "neighbor_ids": neighbor_ids,
        })
        j_str = " | ".join(f"{k}: {v:.3f}" for k, v in sorted(pairwise.items()))
        print(f"  {seed_id}: {j_str}")

    return all_results


def compute_summary(all_results):
    """Compute mean Jaccard for each model pair across all seeds."""
    print("\n=== Summary: Mean Jaccard overlap ===")

    pair_names = set()
    for r in all_results:
        pair_names.update(r["pairwise_jaccard"].keys())

    summary = {}
    for pair in sorted(pair_names):
        values = [r["pairwise_jaccard"][pair] for r in all_results if pair in r["pairwise_jaccard"]]
        mean_j = float(np.mean(values)) if values else 0
        std_j = float(np.std(values)) if values else 0
        min_j = float(np.min(values)) if values else 0
        max_j = float(np.max(values)) if values else 0
        summary[pair] = {
            "mean_jaccard": round(mean_j, 4),
            "std_jaccard": round(std_j, 4),
            "min_jaccard": round(min_j, 4),
            "max_jaccard": round(max_j, 4),
            "n_seeds": len(values),
            "all_values": [round(float(v), 4) for v in values],
        }
        print(f"  {pair}: {mean_j:.4f} +/- {std_j:.4f} (range: {min_j:.3f}-{max_j:.3f})")

    return summary


def make_decision(summary):
    """Apply decision thresholds."""
    print("\n=== DECISION ===")

    def get_j(pair):
        return summary.get(pair, {}).get("mean_jaccard", 0)

    miniml_v4 = get_j("miniLM vs voyage-4")
    miniml_v4l = get_j("miniLM vs voyage-4-large")
    specter_v4 = get_j("SPECTER2 vs voyage-4")
    specter_v4l = get_j("SPECTER2 vs voyage-4-large")
    v4_v4l = get_j("voyage-4 vs voyage-4-large")
    miniml_specter = get_j("miniLM vs SPECTER2")

    decisions = {}
    for model, miniml_j, specter_j in [
        ("voyage-4", miniml_v4, specter_v4),
        ("voyage-4-large", miniml_v4l, specter_v4l),
    ]:
        if miniml_j > 0.8:
            verdict = "REDUNDANT_WITH_MINIML"
            reason = f"Jaccard {miniml_j:.3f} > 0.8 with MiniLM"
        elif miniml_j < 0.6 and specter_j < 0.6:
            verdict = "GENUINELY_DIFFERENT"
            reason = f"Jaccard {miniml_j:.3f}/MiniLM and {specter_j:.3f}/SPECTER2, both < 0.6"
        elif specter_j > 0.8:
            verdict = "REDUNDANT_WITH_SPECTER2"
            reason = f"Jaccard {specter_j:.3f} > 0.8 with SPECTER2"
        elif miniml_j > 0.6 and specter_j < 0.6:
            verdict = "BETTER_MINIML"
            reason = f"Overlaps MiniLM ({miniml_j:.3f}) not SPECTER2 ({specter_j:.3f})"
        elif specter_j > 0.6 and miniml_j < 0.6:
            verdict = "BETTER_SPECTER2"
            reason = f"Overlaps SPECTER2 ({specter_j:.3f}) not MiniLM ({miniml_j:.3f})"
        else:
            verdict = "PARTIAL_OVERLAP"
            reason = f"Moderate overlap: MiniLM={miniml_j:.3f}, SPECTER2={specter_j:.3f}"

        decisions[model] = {
            "verdict": verdict,
            "reason": reason,
            "jaccard_vs_miniml": round(miniml_j, 4),
            "jaccard_vs_specter2": round(specter_j, 4),
        }
        print(f"  {model}: {verdict}")
        print(f"    {reason}")

    print(f"\n  voyage-4 vs voyage-4-large: {v4_v4l:.4f}")
    print(f"  MiniLM vs SPECTER2 (baseline): {miniml_specter:.4f}")

    proceed = any(d["verdict"] == "GENUINELY_DIFFERENT" for d in decisions.values())
    preferred = None
    if proceed:
        v4_sum = decisions["voyage-4"]["jaccard_vs_miniml"] + decisions["voyage-4"]["jaccard_vs_specter2"]
        v4l_sum = decisions["voyage-4-large"]["jaccard_vs_miniml"] + decisions["voyage-4-large"]["jaccard_vs_specter2"]
        preferred = "voyage-4" if v4_sum < v4l_sum else "voyage-4-large"
        print(f"\n  => PROCEED TO PHASE 2 with {preferred}")
    else:
        print(f"\n  => STOP. No sufficient new signal.")

    return {
        "decisions": decisions,
        "v4_vs_v4l_jaccard": round(v4_v4l, 4),
        "miniml_vs_specter2_jaccard": round(miniml_specter, 4),
        "proceed_to_phase2": proceed,
        "preferred_model": preferred,
    }


def main():
    print("=" * 60)
    print("SPIKE 003 / W5: Voyage AI Embedding Screening")
    print("=" * 60)
    sys.stdout.flush()

    api_key = load_api_key()
    print(f"API key loaded (length: {len(api_key)})")

    sample_ids, query_seeds_p1, query_seeds_p3 = build_sample()
    texts = get_paper_texts(sample_ids)
    sample_ids = [aid for aid in sample_ids if aid in texts]
    print(f"  Final sample size: {len(sample_ids)}")

    total_chars = sum(len(texts[aid]) for aid in sample_ids)
    print(f"  Estimated tokens: ~{total_chars // 4}")

    valid_ids, miniml_emb, specter_emb = get_local_embeddings(sample_ids)
    sample_ids = valid_ids

    voyage_results = embed_with_voyage_models(api_key, sample_ids, texts)

    embeddings_dict = {
        "miniLM": miniml_emb,
        "SPECTER2": specter_emb,
        "voyage-4": voyage_results["voyage-4"]["embeddings"],
        "voyage-4-large": voyage_results["voyage-4-large"]["embeddings"],
    }

    query_seed_ids = query_seeds_p1 + query_seeds_p3
    all_results = compute_overlap_analysis(sample_ids, query_seed_ids, embeddings_dict)
    summary = compute_summary(all_results)
    decision = make_decision(summary)

    output = {
        "experiment": "w5_voyage_screening",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "sample_size": len(sample_ids),
        "query_seeds": query_seed_ids,
        "query_seeds_found": [s for s in query_seed_ids if s in set(sample_ids)],
        "rate_limit_tier": "reduced (no payment method): 3 RPM, 10K TPM",
        "batch_size": RATE_LIMITED_BATCH_SIZE,
        "batch_pause_s": BATCH_PAUSE_SECONDS,
        "est_tokens_per_paper": total_chars // 4 // len(sample_ids),
        "models": {
            "miniLM": {"dim": int(miniml_emb.shape[1]), "source": "local"},
            "SPECTER2": {"dim": int(specter_emb.shape[1]), "source": "local"},
            "voyage-4": {
                "dim": int(voyage_results["voyage-4"]["dim"]),
                "embed_time_s": voyage_results["voyage-4"]["elapsed_s"],
                "source": "api",
            },
            "voyage-4-large": {
                "dim": int(voyage_results["voyage-4-large"]["dim"]),
                "embed_time_s": voyage_results["voyage-4-large"]["elapsed_s"],
                "source": "api",
            },
        },
        "per_seed_results": all_results,
        "summary": summary,
        "decision": decision,
        "top_k": TOP_K,
    }

    with open(str(OUTPUT_FILE), 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_FILE}")
    return decision


if __name__ == "__main__":
    decision = main()
