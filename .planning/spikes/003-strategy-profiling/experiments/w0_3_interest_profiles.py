#!/usr/bin/env python3
"""
W0.3 — Define interest profiles and evaluation clusters for Spike 003.

Creates 8 interest profiles, each with:
  - 20 papers: 15 seed candidates + 5 held-out for leave-one-out eval
  - 3 random seed subsets (5, 10, 15 papers) for variance estimation
  - BERTopic cluster mapping
  - Category co-occurrence mapping
  - "Strongly related" papers (agreed by both criteria)

Data sources:
  - Spike 001 harvest DB (19,252 papers)
  - BERTopic results (48 topics)
  - MiniLM embeddings (384-dim, 19,252 papers)
  - arXiv ID ordering for embeddings
"""

import json
import sqlite3
import random
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

import numpy as np

# ---------- Reproducibility ----------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ---------- Paths ----------
BASE = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp")
SPIKE_001_DATA = BASE / ".planning/spikes/001-volume-filtering-scoring-landscape/experiments/data"
SPIKE_002_DATA = BASE / ".planning/spikes/002-backend-comparison/experiments/data"
SPIKE_003_DATA = BASE / ".planning/spikes/003-strategy-profiling/experiments/data"

DB_PATH = SPIKE_001_DATA / "spike_001_harvest.db"
BERTOPIC_PATH = SPIKE_001_DATA / "a2_corpus_visualization_results.json"
EMBEDDINGS_PATH = SPIKE_002_DATA / "embeddings_19k.npy"
IDS_PATH = SPIKE_002_DATA / "arxiv_ids_19k.json"

# ---------- Load data ----------

print("Loading data...")
conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row

with open(BERTOPIC_PATH) as f:
    bertopic_data = json.load(f)

with open(IDS_PATH) as f:
    arxiv_ids_ordered = json.load(f)

id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids_ordered)}

embeddings = np.load(str(EMBEDDINGS_PATH))
print(f"  Papers: {len(arxiv_ids_ordered)}, Embeddings: {embeddings.shape}")

# Pre-normalize embeddings once for cosine similarity
emb_norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
emb_norms = np.where(emb_norms == 0, 1, emb_norms)
normed_embeddings = embeddings / emb_norms

# ---------- Profile definitions ----------

PROFILES = {
    "P1": {
        "name": "RL for robotics",
        "description": "Reinforcement learning applied to robotics and embodied agents",
        "breadth": "Medium",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                (lower(title) LIKE '%reinforcement learn%' OR lower(abstract) LIKE '%reinforcement learn%')
                AND (lower(title) LIKE '%robot%' OR lower(abstract) LIKE '%robot%' OR categories LIKE '%cs.RO%')
            )
            OR (
                categories LIKE '%cs.RO%'
                AND (lower(title) LIKE '%reinforcement%' OR lower(title) LIKE '%policy%gradient%'
                     OR lower(title) LIKE '%reward%' OR lower(title) LIKE '%sim%to%real%')
            )
        """,
        "relevance_keywords": [
            "reinforcement learning", "policy", "reward", "robot", "manipulation",
            "locomotion", "sim-to-real", "sim2real", "embodied", "control policy",
            "MDP", "actor-critic", "PPO", "SAC"
        ],
        "strong_title_keywords": ["reinforcement", "robot", "policy"],
        "relevant_categories": ["cs.RO", "cs.AI", "cs.LG"],
        "expected_bertopic_topics": [6],
    },
    "P2": {
        "name": "Language model reasoning",
        "description": "Reasoning capabilities of large language models",
        "breadth": "Medium",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                (lower(title) LIKE '%language model%' OR lower(title) LIKE '%llm%' OR lower(title) LIKE '%llms%')
                AND (lower(title) LIKE '%reason%' OR lower(abstract) LIKE '%reason%')
            )
            OR (
                lower(title) LIKE '%chain%of%thought%' OR lower(title) LIKE '%step%by%step%reason%'
            )
        """,
        "relevance_keywords": [
            "reasoning", "language model", "LLM", "chain-of-thought", "CoT",
            "logical reasoning", "mathematical reasoning", "step-by-step",
            "few-shot", "in-context learning", "prompt"
        ],
        "strong_title_keywords": ["reason", "language model", "LLM", "chain-of-thought"],
        "relevant_categories": ["cs.CL", "cs.AI", "cs.LG"],
        "expected_bertopic_topics": [0],
    },
    "P3": {
        "name": "Quantum computing / quantum ML",
        "description": "Quantum computing and quantum machine learning",
        "breadth": "Narrow",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                lower(title) LIKE '%quantum%'
                AND (lower(title) LIKE '%machine learn%' OR lower(title) LIKE '%neural%'
                     OR lower(title) LIKE '%comput%' OR lower(title) LIKE '%circuit%'
                     OR lower(title) LIKE '%algorithm%' OR lower(title) LIKE '%qubit%')
            )
            OR (
                categories LIKE '%quant-ph%'
                AND (lower(abstract) LIKE '%quantum machine learning%' OR lower(abstract) LIKE '%variational quantum%'
                     OR lower(abstract) LIKE '%quantum circuit%')
            )
        """,
        "relevance_keywords": [
            "quantum", "qubit", "quantum circuit", "quantum computing",
            "quantum machine learning", "variational", "quantum neural network",
            "quantum advantage", "quantum algorithm", "entanglement"
        ],
        "strong_title_keywords": ["quantum"],
        "relevant_categories": ["quant-ph", "cs.LG", "cs.AI"],
        "expected_bertopic_topics": [7],
    },
    "P4": {
        "name": "AI safety / alignment",
        "description": "AI safety, alignment, and responsible AI development",
        "breadth": "Broad",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                (lower(title) LIKE '%safety%' OR lower(title) LIKE '%alignment%' OR lower(title) LIKE '%align%')
                AND (lower(title) LIKE '%ai%' OR lower(title) LIKE '%model%' OR lower(title) LIKE '%llm%'
                     OR lower(abstract) LIKE '%artificial intelligence%' OR lower(abstract) LIKE '%language model%')
            )
            OR (
                lower(title) LIKE '%jailbreak%' OR lower(title) LIKE '%red team%'
                OR lower(title) LIKE '%rlhf%' OR lower(title) LIKE '%value alignment%'
            )
            OR (
                (lower(title) LIKE '%harm%' OR lower(title) LIKE '%toxic%' OR lower(title) LIKE '%guardrail%')
                AND (lower(abstract) LIKE '%language model%' OR lower(abstract) LIKE '%generative%')
            )
            OR (
                categories LIKE '%cs.CR%' AND lower(title) LIKE '%attack%'
                AND (lower(abstract) LIKE '%language model%' OR lower(abstract) LIKE '%llm%')
            )
        """,
        "relevance_keywords": [
            "safety", "alignment", "jailbreak", "red teaming", "RLHF",
            "guardrails", "harmful", "toxic", "responsible AI", "AI ethics",
            "robustness", "adversarial", "attack", "defense"
        ],
        "strong_title_keywords": ["safety", "alignment", "jailbreak", "attack"],
        "relevant_categories": ["cs.AI", "cs.CL", "cs.CR", "cs.CY"],
        "expected_bertopic_topics": [2, 8],
    },
    "P5": {
        "name": "Graph neural networks",
        "description": "Graph neural networks and geometric deep learning",
        "breadth": "Medium",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                lower(title) LIKE '%graph neural%' OR lower(title) LIKE '%graph network%'
                OR lower(title) LIKE '%gnn%' OR lower(title) LIKE '%gnns%'
                OR lower(title) LIKE '%message passing%neural%'
                OR lower(title) LIKE '%geometric deep learning%'
            )
            OR (
                lower(title) LIKE '%graph%' AND lower(title) LIKE '%convolution%'
                AND (lower(abstract) LIKE '%node%' OR lower(abstract) LIKE '%graph%')
            )
            OR (
                (lower(abstract) LIKE '%graph neural network%' OR lower(abstract) LIKE '%message passing neural%')
                AND lower(title) LIKE '%graph%'
            )
        """,
        "relevance_keywords": [
            "graph neural network", "GNN", "message passing", "node classification",
            "graph convolution", "link prediction", "geometric deep learning",
            "graph transformer", "spectral", "spatial graph"
        ],
        "strong_title_keywords": ["graph neural", "GNN", "graph network"],
        "relevant_categories": ["cs.LG", "cs.AI", "cs.SI"],
        "expected_bertopic_topics": [3],
    },
    "P6": {
        "name": "Diffusion models for generation",
        "description": "Diffusion models for image, video, and content generation",
        "breadth": "Medium",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                lower(title) LIKE '%diffusion model%' OR lower(title) LIKE '%diffusion%based%'
            )
            OR (
                lower(title) LIKE '%diffusion%'
                AND (lower(title) LIKE '%generat%' OR lower(title) LIKE '%image%'
                     OR lower(title) LIKE '%video%' OR lower(title) LIKE '%text%to%'
                     OR lower(title) LIKE '%denois%' OR lower(title) LIKE '%score%matching%')
            )
            OR (
                lower(title) LIKE '%stable diffusion%' OR lower(title) LIKE '%latent diffusion%'
                OR lower(title) LIKE '%ddpm%' OR lower(title) LIKE '%score%based generative%'
            )
        """,
        "relevance_keywords": [
            "diffusion model", "denoising", "score matching", "DDPM",
            "stable diffusion", "image generation", "text-to-image",
            "latent diffusion", "noise schedule", "sampling"
        ],
        "strong_title_keywords": ["diffusion", "denoising", "score"],
        "relevant_categories": ["cs.CV", "cs.LG", "cs.AI"],
        "expected_bertopic_topics": [0],
    },
    "P7": {
        "name": "Federated learning + privacy",
        "description": "Federated learning, differential privacy, and privacy-preserving ML",
        "breadth": "Medium",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE (
                lower(title) LIKE '%federated%'
            )
            OR (
                lower(title) LIKE '%differential privacy%' OR lower(title) LIKE '%differentially private%'
            )
            OR (
                lower(title) LIKE '%privacy%preserv%' AND lower(abstract) LIKE '%learn%'
            )
            OR (
                lower(title) LIKE '%privacy%' AND lower(title) LIKE '%machine learning%'
            )
            OR (
                lower(title) LIKE '%secure aggregat%' OR lower(title) LIKE '%private%learn%'
            )
        """,
        "relevance_keywords": [
            "federated learning", "differential privacy", "privacy-preserving",
            "secure aggregation", "local model", "communication efficiency",
            "data heterogeneity", "non-iid", "private"
        ],
        "strong_title_keywords": ["federated", "privacy", "private"],
        "relevant_categories": ["cs.LG", "cs.CR", "cs.DC"],
        "expected_bertopic_topics": [15],
    },
    "P8": {
        "name": "Mathematical foundations of neural networks",
        "description": "Theory of deep learning: approximation, generalization, optimization",
        "breadth": "Narrow",
        "search_sql": """
            SELECT arxiv_id, title, abstract, categories FROM papers
            WHERE
            -- Direct title matches: NN + theory keyword
            (
                (lower(title) LIKE '%neural network%' OR lower(title) LIKE '%deep learning%'
                 OR lower(title) LIKE '%deep neural%')
                AND (
                    lower(title) LIKE '%theory%' OR lower(title) LIKE '%convergence%'
                    OR lower(title) LIKE '%approximation%' OR lower(title) LIKE '%bound%'
                    OR lower(title) LIKE '%generalization%' OR lower(title) LIKE '%mathematical%'
                    OR lower(title) LIKE '%universal%' OR lower(title) LIKE '%optimization landscape%'
                    OR lower(title) LIKE '%express%'
                )
            )
            -- Specific theory topics
            OR lower(title) LIKE '%neural tangent kernel%'
            OR lower(title) LIKE '%universal approximation%'
            OR lower(title) LIKE '%deep learning theory%'
            OR lower(title) LIKE '%approximation rate%neural%'
            -- Overparameterization
            OR (
                (lower(title) LIKE '%overparamet%' OR lower(title) LIKE '%over-paramet%')
                AND (lower(abstract) LIKE '%neural%' OR lower(abstract) LIKE '%deep learn%')
            )
            -- Loss/optimization landscape
            OR (
                lower(title) LIKE '%loss landscape%'
                AND (lower(abstract) LIKE '%neural%' OR lower(abstract) LIKE '%deep%')
            )
            -- Generalization bounds for NNs
            OR (
                lower(title) LIKE '%generalization%bound%'
                AND (lower(abstract) LIKE '%neural%' OR lower(abstract) LIKE '%deep%')
            )
            OR (
                lower(title) LIKE '%generalization%deep%'
            )
            -- Convergence theory for NN training
            OR (
                lower(title) LIKE '%convergence%'
                AND (lower(title) LIKE '%gradient%' OR lower(title) LIKE '%sgd%')
                AND (lower(abstract) LIKE '%neural%' OR lower(abstract) LIKE '%deep%')
            )
            -- Expressiveness / depth separation
            OR (
                lower(title) LIKE '%express%' AND lower(title) LIKE '%neural%'
                AND (lower(title) LIKE '%depth%' OR lower(title) LIKE '%power%')
            )
            -- Abstract-level theory papers
            OR (
                lower(abstract) LIKE '%approximation theory%'
                AND lower(abstract) LIKE '%neural network%'
                AND lower(title) LIKE '%approximation%'
            )
            OR (
                lower(abstract) LIKE '%generalization theory%'
                AND lower(abstract) LIKE '%deep%'
                AND lower(title) NOT LIKE '%domain%'
            )
            -- stat.ML papers about NN convergence/optimization
            OR (
                categories LIKE '%stat.ML%'
                AND (lower(title) LIKE '%neural%' OR lower(title) LIKE '%deep%')
                AND (lower(title) LIKE '%convergence%' OR lower(title) LIKE '%optim%landscape%')
            )
            -- PAC-Bayesian / information-theoretic generalization
            OR (
                (lower(title) LIKE '%pac-bayes%' OR lower(title) LIKE '%pac bayes%')
                AND lower(abstract) LIKE '%neural%'
            )
        """,
        "relevance_keywords": [
            "approximation theory", "generalization bound", "convergence",
            "universal approximation", "neural tangent kernel", "overparameterized",
            "optimization landscape", "ReLU", "expressiveness", "depth separation",
            "PAC-Bayes", "loss landscape", "neural network theory"
        ],
        # For P8, we need looser strong-title check since theory papers have diverse titles
        "strong_title_keywords": [
            "neural network", "deep learning", "approximation", "generalization",
            "convergence", "universal", "overparamet", "expressiv", "bound",
            "PAC-Bayes", "loss landscape", "neural tangent"
        ],
        "relevant_categories": ["cs.LG", "stat.ML", "math.OC", "cs.NE"],
        "expected_bertopic_topics": [3, 17],
    },
}


# ---------- Helper functions ----------

def compute_relevance_score(title, abstract, keywords):
    """Score paper relevance based on keyword match density."""
    text = (title + " " + abstract).lower()
    score = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title.lower():
            score += 3
        if kw_lower in text:
            score += 1
    return score


def is_genuinely_on_topic(paper, profile):
    """Strict on-topic check: at least one strong keyword must appear in title."""
    title_lower = paper["title"].lower()
    abstract_lower = (paper.get("abstract", "") or "").lower()

    # Check strong title keywords (at least one must be in title)
    title_hit = any(kw.lower() in title_lower for kw in profile["strong_title_keywords"])
    if not title_hit:
        return False

    # Also need at least one relevance keyword in title+abstract
    text = title_lower + " " + abstract_lower
    relevance_hit = any(kw.lower() in text for kw in profile["relevance_keywords"])
    return relevance_hit


def select_papers(conn, profile, target_count=20):
    """Select papers using SQL search + relevance ranking."""
    cursor = conn.execute(profile["search_sql"])
    candidates = []
    seen = set()
    for row in cursor:
        aid = row["arxiv_id"]
        if aid in seen:
            continue
        seen.add(aid)
        title = row["title"]
        abstract = row["abstract"] or ""
        cats = row["categories"] or ""
        score = compute_relevance_score(title, abstract, profile["relevance_keywords"])
        candidates.append({
            "arxiv_id": aid,
            "title": title,
            "abstract": abstract[:300],
            "categories": cats,
            "relevance_score": score,
        })

    # Sort by relevance score descending, then by arxiv_id for determinism
    candidates.sort(key=lambda x: (-x["relevance_score"], x["arxiv_id"]))
    return candidates


def compute_centroid(paper_ids):
    """Compute normalized centroid embedding for a set of papers."""
    vecs = []
    for pid in paper_ids:
        idx = id_to_idx.get(pid)
        if idx is not None:
            vecs.append(normed_embeddings[idx])
    if not vecs:
        return None
    centroid = np.mean(vecs, axis=0)
    centroid = centroid / (np.linalg.norm(centroid) + 1e-10)
    return centroid


def find_cluster_papers(seed_ids, profile, top_k=200):
    """Find papers related to profile seeds using embedding similarity + categories."""
    centroid = compute_centroid(seed_ids)
    if centroid is None:
        return []

    sims = normed_embeddings @ centroid

    # Get top-K indices
    top_indices = np.argsort(sims)[::-1][:top_k]
    top_ids = [arxiv_ids_ordered[i] for i in top_indices]
    top_sims = [float(sims[i]) for i in top_indices]

    # Category matching
    cat_set = set(profile["relevant_categories"])
    cursor = conn.execute("SELECT arxiv_id, categories FROM papers")
    cat_matched = set()
    for row in cursor:
        paper_cats = set(row["categories"].split())
        if paper_cats & cat_set:
            cat_matched.add(row["arxiv_id"])

    results = []
    for aid, sim in zip(top_ids, top_sims):
        in_cats = aid in cat_matched
        results.append({
            "arxiv_id": aid,
            "embedding_similarity": round(sim, 4),
            "category_match": in_cats,
            "strongly_related": sim > 0.7 and in_cats,
        })

    return results


# ---------- Main execution ----------

print("\n=== Building Interest Profiles ===\n")

results = {}
profile_summary = []

for pid, profile in PROFILES.items():
    print(f"\n--- {pid}: {profile['name']} ({profile['breadth']}) ---")

    # Step 1: Find and rank candidate papers
    candidates = select_papers(conn, profile, target_count=20)
    print(f"  SQL candidates: {len(candidates)}")

    # Step 2: Strict quality filter
    verified = [c for c in candidates if is_genuinely_on_topic(c, profile)]
    print(f"  Verified on-topic: {len(verified)}")

    # Step 3: Select final papers from verified only (no padding with unverified)
    final_count = min(20, len(verified))
    selected = verified[:final_count]

    if final_count < 20:
        print(f"  NOTE: Only {final_count} verified papers available (target 20)")

    # Step 4: Split into seeds and held-out
    if final_count >= 20:
        seed_papers = selected[:15]
        held_out_papers = selected[15:20]
    elif final_count >= 15:
        # Keep 5 held out, rest as seeds
        held_out_papers = selected[final_count - 5:]
        seed_papers = selected[:final_count - 5]
    elif final_count >= 10:
        held_count = max(3, final_count // 4)
        seed_papers = selected[:final_count - held_count]
        held_out_papers = selected[final_count - held_count:]
    else:
        seed_papers = selected[:max(1, final_count - 2)]
        held_out_papers = selected[max(1, final_count - 2):]

    seed_ids = [p["arxiv_id"] for p in seed_papers]
    held_out_ids = [p["arxiv_id"] for p in held_out_papers]

    print(f"  Seeds: {len(seed_papers)}, Held-out: {len(held_out_papers)}")

    # Step 5: Create random seed subsets for variance estimation
    # Use deterministic shuffle based on profile ID
    rng = random.Random(SEED + hash(pid) % 10000)
    shuffled_seeds = list(seed_ids)
    rng.shuffle(shuffled_seeds)
    subset_5 = sorted(shuffled_seeds[:5])
    subset_10 = sorted(shuffled_seeds[:10])
    subset_15 = sorted(shuffled_seeds[:min(15, len(shuffled_seeds))])

    # Step 6: Find cluster papers
    cluster_info = find_cluster_papers(seed_ids, profile, top_k=200)

    embedding_related = [c for c in cluster_info if c["embedding_similarity"] > 0.5]
    category_related = [c for c in cluster_info if c["category_match"]]
    strongly_related = [c for c in cluster_info if c["strongly_related"]]

    # Step 7: BERTopic topic mapping
    topic_keyword_map = {}
    for topic in bertopic_data["bertopic"]["top_topics"]:
        topic_keyword_map[topic["topic_id"]] = [w.lower() for w in topic["top_words"]]

    topic_hits = Counter()
    for paper in selected:
        title_abstract = (paper["title"] + " " + paper.get("abstract", "")).lower()
        for tid, words in topic_keyword_map.items():
            word_matches = sum(1 for w in words if w in title_abstract)
            if word_matches >= 2:
                topic_hits[tid] += 1

    # Build output
    seed_details = [{
        "arxiv_id": p["arxiv_id"],
        "title": p["title"],
        "categories": p["categories"],
        "relevance_score": p["relevance_score"],
    } for p in seed_papers]

    held_out_details = [{
        "arxiv_id": p["arxiv_id"],
        "title": p["title"],
        "categories": p["categories"],
        "relevance_score": p["relevance_score"],
    } for p in held_out_papers]

    profile_result = {
        "profile_id": pid,
        "name": profile["name"],
        "description": profile["description"],
        "breadth": profile["breadth"],
        "total_candidates_found": len(candidates),
        "verified_on_topic": len(verified),
        "final_selected": final_count,
        "seed_papers": seed_details,
        "held_out_papers": held_out_details,
        "seed_subsets": {
            "subset_5": subset_5,
            "subset_10": subset_10,
            "subset_15": subset_15,
        },
        "cluster_mapping": {
            "embedding_related_count": len(embedding_related),
            "category_related_count": len(category_related),
            "strongly_related_count": len(strongly_related),
            "top_200_by_similarity": cluster_info[:20],
        },
        "bertopic_topic_hits": dict(topic_hits.most_common()),
        "relevant_categories": profile["relevant_categories"],
    }

    results[pid] = profile_result

    topics_str = ", ".join(f"T{t}({c})" for t, c in topic_hits.most_common(5))
    profile_summary.append({
        "id": pid,
        "name": profile["name"],
        "breadth": profile["breadth"],
        "found": len(candidates),
        "verified": len(verified),
        "seeds": len(seed_papers),
        "held_out": len(held_out_papers),
        "embedding_cluster": len(embedding_related),
        "category_cluster": len(category_related),
        "strongly_related": len(strongly_related),
        "topics": topics_str,
    })

    print(f"  BERTopic topics: {topics_str}")
    print(f"  Cluster: {len(embedding_related)} embed-related, "
          f"{len(category_related)} cat-related, "
          f"{len(strongly_related)} strongly-related")
    print(f"  Sample seed titles:")
    for p in seed_papers[:3]:
        print(f"    - {p['title'][:90]}")
    print(f"  Sample held-out titles:")
    for p in held_out_papers[:2]:
        print(f"    - {p['title'][:90]}")


# ---------- Save results ----------

output = {
    "metadata": {
        "created": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "corpus_size": len(arxiv_ids_ordered),
        "embedding_dim": int(embeddings.shape[1]),
        "n_profiles": len(results),
        "source_db": str(DB_PATH),
    },
    "profiles": results,
    "summary": profile_summary,
}

out_path = SPIKE_003_DATA / "interest_profiles.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n\n=== Results saved to {out_path} ===")

# ---------- Summary table ----------

print("\n=== Profile Summary ===\n")
hdr = f"{'ID':<4} {'Name':<45} {'Breadth':<8} {'Found':<6} {'Verif':<6} {'Seeds':<6} {'Held':<5} {'EmbClst':<8} {'CatClst':<8} {'Strong':<7}"
print(hdr)
print("-" * len(hdr))
for s in profile_summary:
    print(f"{s['id']:<4} {s['name']:<45} {s['breadth']:<8} {s['found']:<6} "
          f"{s['verified']:<6} {s['seeds']:<6} {s['held_out']:<5} "
          f"{s['embedding_cluster']:<8} {s['category_cluster']:<8} {s['strongly_related']:<7}")

# ---------- Validation ----------

print("\n=== Validation ===\n")

all_seeds = set()
all_held_out = set()
all_ok = True

for pid, prof in results.items():
    seeds = {p["arxiv_id"] for p in prof["seed_papers"]}
    held = {p["arxiv_id"] for p in prof["held_out_papers"]}

    overlap = seeds & held
    if overlap:
        print(f"  ERROR: {pid} has seed/held-out overlap: {overlap}")
        all_ok = False
    else:
        print(f"  {pid}: No seed/held-out overlap (OK)")

    cross_seed = seeds & all_seeds
    cross_held = held & all_held_out
    if cross_seed:
        print(f"    NOTE: {pid} shares {len(cross_seed)} seed papers with other profiles")
    if cross_held:
        print(f"    NOTE: {pid} shares {len(cross_held)} held-out papers with other profiles")

    all_seeds |= seeds
    all_held_out |= held

seed_held_cross = all_seeds & all_held_out
if seed_held_cross:
    print(f"\n  WARNING: {len(seed_held_cross)} papers are seeds in one profile and held-out in another")
    all_ok = False
else:
    print(f"\n  No cross-profile seed/held-out contamination (OK)")

print(f"\n  Total unique seed papers: {len(all_seeds)}")
print(f"  Total unique held-out papers: {len(all_held_out)}")
print(f"  Total unique papers used: {len(all_seeds | all_held_out)}")

# Check breadth consistency
print("\n=== Breadth Analysis ===\n")
for pid, prof in results.items():
    n_topics = len(prof["bertopic_topic_hits"])
    n_strongly = prof["cluster_mapping"]["strongly_related_count"]
    breadth = prof["breadth"]
    print(f"  {pid} ({breadth}): {n_topics} BERTopic topics, "
          f"{n_strongly} strongly-related papers in top-200")

conn.close()
print("\nDone.")
