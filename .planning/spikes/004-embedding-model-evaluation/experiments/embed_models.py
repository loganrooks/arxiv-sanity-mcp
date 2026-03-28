#!/usr/bin/env python3
"""
Spike 004 Phase 1: Embed 2000-paper sample with all 6 models.

Models:
  - MiniLM, SPECTER2: extract from existing 19K embeddings
  - Stella v5, Qwen3, GTE: download + embed locally on GPU
  - Voyage-4: API embedding (slow — runs last, can be backgrounded)

Output: per-model .npy files in experiments/data/ + checkpoint JSON.

Usage:
  conda activate ml-dev
  python embed_models.py [--skip-voyage] [--models MODEL1,MODEL2,...]

Protocol: See ../PROTOCOL.md Section 1 for embedding specifications.
"""

from __future__ import annotations

import argparse
import json
import os
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

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
SPIKE_003_DIR = SPIKE_004_DIR.parent / "003-strategy-profiling"
SPIKE_002_DIR = SPIKE_004_DIR.parent / "002-backend-comparison"
SPIKE_001_DIR = SPIKE_004_DIR.parent / "001-volume-filtering-scoring-landscape"

DATA_DIR = SPIKE_004_DIR / "experiments" / "data"
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"

# Source data
SAMPLE_PATH = SPIKE_003_DIR / "experiments" / "data" / "sample_2000.json"
HARVEST_DB = SPIKE_001_DIR / "experiments" / "data" / "spike_001_harvest.db"

# Existing 19K embeddings
MINILM_19K_PATH = SPIKE_002_DIR / "experiments" / "data" / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DIR / "experiments" / "data" / "arxiv_ids_19k.json"
SPECTER2_19K_PATH = SPIKE_003_DIR / "experiments" / "data" / "specter2_adapter_19k.npy"
SPECTER2_IDS_PATH = SPIKE_003_DIR / "experiments" / "data" / "specter2_adapter_ids.json"

# GPU batch sizes (conservative for 11GB VRAM)
BATCH_SIZES = {
    "stella": 32,    # 400M params, 1024-dim — conservative
    "qwen3": 16,     # 0.6B params — most conservative
    "gte": 48,       # 335M params, 1024-dim — moderate
}

# Voyage rate limiting
VOYAGE_BATCH_SIZE = 20  # papers per API call
VOYAGE_PAUSE_SECONDS = 22  # ~3 RPM = 20s between calls, plus margin


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_sample() -> tuple[list[str], list[dict]]:
    """Load 2000-paper sample IDs and metadata."""
    with open(SAMPLE_PATH) as f:
        sample = json.load(f)
    paper_ids = [p["arxiv_id"] for p in sample["papers"]]
    print(f"  Sample: {len(paper_ids)} papers")
    return paper_ids, sample["papers"]


def load_paper_texts(paper_ids: list[str]) -> dict[str, str]:
    """Fetch title + abstract for each paper from harvest DB."""
    conn = sqlite3.connect(str(HARVEST_DB))
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in paper_ids)
    rows = conn.execute(
        f"SELECT arxiv_id, title, abstract FROM papers "
        f"WHERE arxiv_id IN ({placeholders})",
        paper_ids,
    ).fetchall()
    conn.close()

    texts = {}
    for row in rows:
        title = row["title"] or ""
        abstract = row["abstract"] or ""
        texts[row["arxiv_id"]] = f"{title}\n\n{abstract}" if abstract else title
    print(f"  Loaded texts for {len(texts)} papers")
    return texts


def load_specter2_texts(paper_ids: list[str]) -> dict[str, str]:
    """SPECTER2 uses title [SEP] abstract format."""
    conn = sqlite3.connect(str(HARVEST_DB))
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in paper_ids)
    rows = conn.execute(
        f"SELECT arxiv_id, title, abstract FROM papers "
        f"WHERE arxiv_id IN ({placeholders})",
        paper_ids,
    ).fetchall()
    conn.close()

    texts = {}
    for row in rows:
        title = row["title"] or ""
        abstract = row["abstract"] or ""
        texts[row["arxiv_id"]] = f"{title} [SEP] {abstract}" if abstract else title
    return texts


# ---------------------------------------------------------------------------
# Model embedding functions
# ---------------------------------------------------------------------------

def extract_from_19k(
    paper_ids: list[str],
    emb_path: Path,
    ids_path: Path,
    model_name: str,
) -> tuple[np.ndarray, list[str], dict]:
    """Extract subset embeddings from existing 19K .npy file."""
    print(f"\n=== Extracting {model_name} from 19K embeddings ===")
    t0 = time.perf_counter()

    with open(ids_path) as f:
        all_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(all_ids)}

    all_emb = np.load(str(emb_path))
    print(f"  Full embeddings: {all_emb.shape}")

    indices = []
    valid_ids = []
    missing = []
    for pid in paper_ids:
        if pid in id_to_idx:
            indices.append(id_to_idx[pid])
            valid_ids.append(pid)
        else:
            missing.append(pid)

    if missing:
        print(f"  WARNING: {len(missing)} papers not found in 19K embeddings")

    sample_emb = all_emb[np.array(indices)]

    # L2 normalize
    norms = np.linalg.norm(sample_emb, axis=1, keepdims=True)
    norms[norms == 0] = 1
    sample_emb = sample_emb / norms

    elapsed = time.perf_counter() - t0
    print(f"  Extracted: {sample_emb.shape} in {elapsed:.1f}s")

    provenance = {
        "model": model_name,
        "source": str(emb_path),
        "method": "extracted from 19K",
        "n_papers": len(valid_ids),
        "n_missing": len(missing),
        "dimension": int(sample_emb.shape[1]),
        "duration_s": round(elapsed, 1),
    }
    return sample_emb, valid_ids, provenance


def embed_local_model(
    paper_ids: list[str],
    texts: dict[str, str],
    model_id: str,
    model_key: str,
    trust_remote_code: bool = False,
    prompt_name: str | None = None,
) -> tuple[np.ndarray, list[str], dict]:
    """Embed papers with a local sentence-transformers model."""
    from sentence_transformers import SentenceTransformer

    print(f"\n=== Embedding with {model_key} ({model_id}) ===")
    t0 = time.perf_counter()

    # Load model
    print(f"  Loading model...")
    model = SentenceTransformer(
        model_id,
        trust_remote_code=trust_remote_code,
        device="cuda",
    )
    t_load = time.perf_counter() - t0
    print(f"  Model loaded in {t_load:.1f}s")
    print(f"  Dimension: {model.get_sentence_embedding_dimension()}")
    print(f"  Max seq length: {model.max_seq_length}")

    # Prepare texts in sample order
    valid_ids = [pid for pid in paper_ids if pid in texts]
    text_list = [texts[pid] for pid in valid_ids]
    batch_size = BATCH_SIZES.get(model_key, 32)

    # Embed
    print(f"  Embedding {len(text_list)} papers (batch_size={batch_size})...")
    t_embed = time.perf_counter()

    encode_kwargs = {
        "batch_size": batch_size,
        "show_progress_bar": True,
        "normalize_embeddings": True,
    }
    if prompt_name:
        encode_kwargs["prompt_name"] = prompt_name

    embeddings = model.encode(text_list, **encode_kwargs)
    t_done = time.perf_counter()

    print(f"  Embedded: {embeddings.shape} in {t_done - t_embed:.1f}s")

    # Get model revision for provenance
    try:
        revision = model[0].auto_model.config._commit_hash or "unknown"
    except Exception:
        revision = "unknown"

    provenance = {
        "model": model_id,
        "model_key": model_key,
        "revision": revision,
        "method": "sentence-transformers encode",
        "device": "cuda",
        "batch_size": batch_size,
        "trust_remote_code": trust_remote_code,
        "prompt_name": prompt_name,
        "n_papers": len(valid_ids),
        "dimension": int(embeddings.shape[1]),
        "max_seq_length": model.max_seq_length,
        "normalization": "L2 (encode-time)",
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda or "N/A",
        "load_time_s": round(t_load, 1),
        "embed_time_s": round(t_done - t_embed, 1),
        "total_time_s": round(t_done - t0, 1),
    }

    # Free GPU memory
    del model
    torch.cuda.empty_cache()

    return embeddings, valid_ids, provenance


def embed_specter2(
    paper_ids: list[str],
    texts: dict[str, str],
) -> tuple[np.ndarray, list[str], dict]:
    """Embed with SPECTER2 + proximity adapter (CLS pooling)."""
    from adapters import AutoAdapterModel
    from transformers import AutoTokenizer

    print(f"\n=== Embedding with SPECTER2 + proximity adapter ===")
    t0 = time.perf_counter()

    print("  Loading model + adapter...")
    tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
    model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
    model.load_adapter(
        "allenai/specter2",
        source="hf",
        load_as="specter2_proximity",
        set_active=True,
    )
    model.eval()
    model.to("cuda")
    t_load = time.perf_counter() - t0
    print(f"  Loaded in {t_load:.1f}s")

    valid_ids = [pid for pid in paper_ids if pid in texts]
    text_list = [texts[pid] for pid in valid_ids]

    # Batch embed with CLS pooling
    batch_size = 64
    all_embeddings = []
    t_embed = time.perf_counter()

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        ).to("cuda")
        with torch.no_grad():
            outputs = model(**inputs)
            emb = outputs.last_hidden_state[:, 0, :]  # CLS token
        all_embeddings.append(emb.cpu().numpy())

        if (i // batch_size) % 10 == 0:
            print(f"  Batch {i // batch_size + 1}/{(len(text_list) + batch_size - 1) // batch_size}")

    embeddings = np.vstack(all_embeddings)

    # L2 normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    embeddings = embeddings / norms

    t_done = time.perf_counter()
    print(f"  Embedded: {embeddings.shape} in {t_done - t_embed:.1f}s")

    provenance = {
        "model": "allenai/specter2_base + proximity adapter",
        "model_key": "specter2",
        "method": "CLS token pooling via adapters library",
        "device": "cuda",
        "batch_size": batch_size,
        "max_length": 512,
        "text_format": "title [SEP] abstract",
        "n_papers": len(valid_ids),
        "dimension": int(embeddings.shape[1]),
        "normalization": "L2 (post-embed)",
        "torch_version": torch.__version__,
        "load_time_s": round(t_load, 1),
        "embed_time_s": round(t_done - t_embed, 1),
        "total_time_s": round(t_done - t0, 1),
    }

    del model
    torch.cuda.empty_cache()

    return embeddings, valid_ids, provenance


def embed_voyage(
    paper_ids: list[str],
    texts: dict[str, str],
    api_key: str,
) -> tuple[np.ndarray, list[str], dict]:
    """Embed with Voyage-4 API. Slow due to rate limiting (~2 hrs for 2000 papers)."""
    import voyageai

    print(f"\n=== Embedding with Voyage-4 API ===")
    print(f"  Rate limit: 3 RPM. Estimated time: ~{len(paper_ids) * VOYAGE_PAUSE_SECONDS / 60 / VOYAGE_BATCH_SIZE:.0f} min")
    t0 = time.perf_counter()

    vo = voyageai.Client(api_key=api_key)

    valid_ids = [pid for pid in paper_ids if pid in texts]
    text_list = [texts[pid] for pid in valid_ids]

    all_embeddings = []
    n_batches = (len(text_list) + VOYAGE_BATCH_SIZE - 1) // VOYAGE_BATCH_SIZE
    failures = []

    for i in range(0, len(text_list), VOYAGE_BATCH_SIZE):
        batch_num = i // VOYAGE_BATCH_SIZE + 1
        batch = text_list[i:i + VOYAGE_BATCH_SIZE]

        retries = 0
        while retries < 3:
            try:
                result = vo.embed(
                    batch,
                    model="voyage-4",
                    input_type="document",
                )
                all_embeddings.extend(result.embeddings)
                print(f"  Batch {batch_num}/{n_batches} OK ({len(all_embeddings)}/{len(text_list)} papers)")
                break
            except Exception as e:
                retries += 1
                wait = VOYAGE_PAUSE_SECONDS * (2 ** retries)
                print(f"  Batch {batch_num} error (attempt {retries}): {e}")
                print(f"  Waiting {wait}s before retry...")
                time.sleep(wait)
        else:
            print(f"  Batch {batch_num} FAILED after 3 retries")
            # Fill with zeros and record failure
            for j in range(len(batch)):
                all_embeddings.append([0.0] * 1024)
                failures.append(i + j)

        # Rate limit pause between batches
        if batch_num < n_batches:
            time.sleep(VOYAGE_PAUSE_SECONDS)

    embeddings = np.array(all_embeddings, dtype=np.float32)
    t_done = time.perf_counter()
    print(f"  Embedded: {embeddings.shape} in {t_done - t0:.1f}s")
    if failures:
        print(f"  WARNING: {len(failures)} papers failed to embed")

    provenance = {
        "model": "voyage-4",
        "model_key": "voyage",
        "method": "Voyage API",
        "input_type": "document",
        "api_model_string": "voyage-4",
        "provider_drift_possible": True,
        "n_papers": len(valid_ids),
        "n_failures": len(failures),
        "failed_indices": failures,
        "dimension": int(embeddings.shape[1]) if len(embeddings) > 0 else 0,
        "normalization": "L2 (API-side)",
        "batch_size": VOYAGE_BATCH_SIZE,
        "pause_seconds": VOYAGE_PAUSE_SECONDS,
        "total_time_s": round(t_done - t0, 1),
        "embed_date": datetime.now(timezone.utc).isoformat(),
    }

    return embeddings, valid_ids, provenance


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

MODEL_REGISTRY = {
    "minilm": {
        "method": "extract",
        "emb_path": MINILM_19K_PATH,
        "ids_path": MINILM_IDS_PATH,
        "display": "all-MiniLM-L6-v2",
    },
    "specter2": {
        "method": "specter2",
        "display": "SPECTER2 + proximity adapter",
    },
    "stella": {
        "method": "local",
        "model_id": "dunzhang/stella_en_400M_v5",
        "trust_remote_code": True,
        "display": "Stella v5 400M",
    },
    "qwen3": {
        "method": "local",
        "model_id": "Qwen/Qwen3-Embedding-0.6B",
        "trust_remote_code": True,
        "display": "Qwen3-Embedding-0.6B",
    },
    "gte": {
        "method": "local",
        "model_id": "Alibaba-NLP/gte-large-en-v1.5",
        "trust_remote_code": True,
        "display": "GTE-large-en-v1.5",
    },
    "voyage": {
        "method": "voyage",
        "display": "Voyage-4",
    },
}

DEFAULT_ORDER = ["minilm", "specter2", "stella", "gte", "qwen3", "voyage"]


def save_embeddings(model_key: str, embeddings: np.ndarray, paper_ids: list[str]):
    """Save embeddings and ID mapping."""
    emb_path = DATA_DIR / f"{model_key}_2000.npy"
    ids_path = DATA_DIR / f"{model_key}_2000_ids.json"

    np.save(str(emb_path), embeddings.astype(np.float32))
    with open(ids_path, "w") as f:
        json.dump(paper_ids, f)

    print(f"  Saved: {emb_path} ({embeddings.shape})")
    return str(emb_path), str(ids_path)


def load_voyage_api_key() -> str:
    """Load Voyage API key from project .env or ~/.env."""
    for env_path in [
        SPIKE_004_DIR.parents[2] / ".env",  # project root
        Path.home() / ".env",
    ]:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        if key.strip() == "VOYAGE_API_KEY":
                            return val.strip().strip("'\"")
    # Also check environment
    val = os.environ.get("VOYAGE_API_KEY", "")
    if val:
        return val
    raise RuntimeError("VOYAGE_API_KEY not found in .env or environment")


def main():
    parser = argparse.ArgumentParser(description="Spike 004 Phase 1: Embed models")
    parser.add_argument("--skip-voyage", action="store_true", help="Skip Voyage API (run locally only)")
    parser.add_argument("--models", type=str, help="Comma-separated model keys to run (default: all)")
    parser.add_argument("--extract-only", action="store_true", help="Only extract MiniLM/SPECTER2 from 19K")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which models to run
    if args.extract_only:
        models_to_run = ["minilm", "specter2"]
    elif args.models:
        models_to_run = [m.strip() for m in args.models.split(",")]
    else:
        models_to_run = DEFAULT_ORDER.copy()
        if args.skip_voyage:
            models_to_run.remove("voyage")

    print("=" * 60)
    print("SPIKE 004 PHASE 1: EMBEDDING")
    print(f"Models: {', '.join(models_to_run)}")
    print("=" * 60)

    # Load sample
    print("\n--- Loading sample ---")
    paper_ids, papers = load_sample()

    # Load texts (standard format for most models)
    texts = load_paper_texts(paper_ids)

    # Check for existing embeddings (resume support)
    existing = {}
    for key in models_to_run:
        emb_path = DATA_DIR / f"{key}_2000.npy"
        if emb_path.exists():
            existing[key] = True
            print(f"  {key}: already embedded (skip with --models to re-run)")

    # Run each model
    results = {}
    for model_key in models_to_run:
        if model_key in existing:
            print(f"\n--- Skipping {model_key} (already exists) ---")
            # Load existing provenance if available
            checkpoint_path = CHECKPOINT_DIR / "phase1_embeddings.json"
            if checkpoint_path.exists():
                with open(checkpoint_path) as f:
                    prev = json.load(f)
                if model_key in prev.get("models", {}):
                    results[model_key] = prev["models"][model_key]
            continue

        reg = MODEL_REGISTRY[model_key]
        try:
            if reg["method"] == "extract":
                emb, ids, prov = extract_from_19k(
                    paper_ids, reg["emb_path"], reg["ids_path"], reg["display"],
                )
            elif reg["method"] == "specter2":
                # SPECTER2 needs special text format and pooling
                spec_texts = load_specter2_texts(paper_ids)
                emb, ids, prov = embed_specter2(paper_ids, spec_texts)
            elif reg["method"] == "local":
                emb, ids, prov = embed_local_model(
                    paper_ids, texts, reg["model_id"], model_key,
                    trust_remote_code=reg.get("trust_remote_code", False),
                )
            elif reg["method"] == "voyage":
                api_key = load_voyage_api_key()
                emb, ids, prov = embed_voyage(paper_ids, texts, api_key)
            else:
                raise ValueError(f"Unknown method: {reg['method']}")

            # Save
            emb_path, ids_path = save_embeddings(model_key, emb, ids)
            prov["emb_path"] = emb_path
            prov["ids_path"] = ids_path
            prov["timestamp"] = datetime.now(timezone.utc).isoformat()
            results[model_key] = prov

        except Exception as e:
            print(f"\n  ERROR embedding {model_key}: {e}")
            results[model_key] = {
                "model_key": model_key,
                "status": "FAILED",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Write incremental checkpoint after each model
        checkpoint = {
            "phase": "phase1_embeddings",
            "sample_path": str(SAMPLE_PATH),
            "n_papers": len(paper_ids),
            "models": results,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
        with open(CHECKPOINT_DIR / "phase1_embeddings.json", "w") as f:
            json.dump(checkpoint, f, indent=2, cls=NumpyEncoder)

    # Final summary
    print("\n" + "=" * 60)
    print("PHASE 1 SUMMARY")
    print("=" * 60)
    for key, prov in results.items():
        status = prov.get("status", "OK")
        if status == "FAILED":
            print(f"  {key}: FAILED — {prov.get('error', 'unknown')}")
        else:
            dim = prov.get("dimension", "?")
            n = prov.get("n_papers", "?")
            t = prov.get("total_time_s", prov.get("duration_s", "?"))
            print(f"  {key}: {n} papers, {dim}-dim, {t}s")

    failed = [k for k, v in results.items() if v.get("status") == "FAILED"]
    if failed:
        print(f"\n  FAILURES: {', '.join(failed)}")
        print("  Re-run with --models={} to retry".format(",".join(failed)))


if __name__ == "__main__":
    main()
