#!/usr/bin/env python3
"""
Spike 005: Evaluation framework robustness.

This script performs the quantitative pass for Spike 005 by:
1. Constructing three profile-construction families on the existing 2000-paper sample:
   - the saved MiniLM-derived family from Spike 003
   - a metadata-plus-lexical category family
   - a SPECTER2-refined challenger family (with GTE fallback)
2. Re-running the Spike 004 comparison frame under each family
3. Emitting provisional quantitative classifications plus review targets for cases that
   change classification across profile families

The main operational compromise is explicit: outside MiniLM, the repository only has
checked-in challenger embeddings for the 2000-paper sample, not the full 19K corpus.
So alternative profile families are reconstructed inside the sample. This keeps the
comparison reproducible while leaving the family-construction scope clearly bounded.

Usage:
  python .planning/spikes/005-evaluation-framework-robustness/experiments/run_framework_robustness.py
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


SPIKE_005_DIR = Path(__file__).resolve().parent.parent
SPIKE_004_EXPERIMENTS = SPIKE_005_DIR.parent / "004-embedding-model-evaluation" / "experiments"
if str(SPIKE_004_EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(SPIKE_004_EXPERIMENTS))

import compare_models as base  # noqa: E402


EXPERIMENTS_DIR = SPIKE_005_DIR / "experiments"
CHECKPOINT_DIR = EXPERIMENTS_DIR / "checkpoints"
REVIEW_INPUT_DIR = EXPERIMENTS_DIR / "review_inputs"
SPIKE_003_DIR = SPIKE_005_DIR.parent / "003-strategy-profiling"
PROFILES_PATH = SPIKE_003_DIR / "experiments" / "data" / "interest_profiles.json"
SAMPLE_PATH = SPIKE_003_DIR / "experiments" / "data" / "sample_2000.json"

MODELS = ["specter2", "stella", "qwen3", "gte", "voyage"]
FAMILY_IDS = ["minilm_saved", "category_lexical", "specter2_refined"]
CLASSIFICATIONS = [
    "near-redundant",
    "distinct but not currently complementary",
    "candidate complementary second view",
    "blocked / unclear",
]

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]{1,}")
STOPWORDS = {
    "about", "above", "after", "again", "against", "along", "also", "among", "and",
    "another", "around", "based", "because", "been", "being", "between", "both",
    "build", "built", "can", "current", "data", "different", "does", "each", "for",
    "from", "into", "its", "more", "most", "must", "need", "not", "onto", "other",
    "over", "paper", "papers", "profile", "related", "same", "should", "show",
    "shown", "some", "such", "than", "that", "their", "them", "then", "these",
    "they", "this", "those", "through", "under", "using", "very", "what", "when",
    "where", "which", "with", "would", "your",
}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


@dataclass
class FamilyProfile:
    profile_id: str
    name: str
    description: str
    family_id: str
    family_label: str
    seed_papers: list[dict]
    held_out_papers: list[dict]
    category_cover: list[str]
    candidate_pool_size: int
    selection_details: dict


def load_sample_papers() -> tuple[list[dict], dict[str, dict]]:
    data = json.loads(SAMPLE_PATH.read_text())
    papers = data.get("papers", data)
    by_id = {paper["arxiv_id"]: paper for paper in papers}
    return papers, by_id


def load_saved_profiles() -> dict[str, dict]:
    return json.loads(PROFILES_PATH.read_text())["profiles"]


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) >= 3]


def paper_text(paper: dict) -> str:
    return f"{paper.get('title', '')} {paper.get('abstract', '')}"


def build_document_frequency(sample_papers: list[dict]) -> Counter:
    df = Counter()
    for paper in sample_papers:
        df.update(set(tokenize(paper_text(paper))))
    return df


def compute_category_cover(seed_papers: list[dict], target_mass: float = 0.80) -> list[str]:
    category_mass = Counter()
    total = 0
    for paper in seed_papers:
        cats = [c for c in (paper.get("categories") or "").split() if c]
        category_mass.update(cats)
        total += len(cats)

    if not total:
        return []

    chosen = []
    running = 0
    for cat, count in category_mass.most_common():
        chosen.append(cat)
        running += count
        if running / total >= target_mass:
            break
    return chosen


def build_profile_lexicon(profile: dict, document_frequency: Counter, corpus_size: int) -> dict[str, float]:
    seed_counter = Counter()

    def add_weighted_terms(text: str, weight: float) -> None:
        for token in tokenize(text):
            seed_counter[token] += weight

    add_weighted_terms(profile.get("name", ""), 4.0)
    add_weighted_terms(profile.get("description", ""), 3.0)
    for paper in profile["seed_papers"]:
        add_weighted_terms(paper.get("title", ""), 2.0)
        add_weighted_terms(paper.get("abstract", ""), 1.0)

    weighted = {}
    for token, tf in seed_counter.items():
        df = document_frequency.get(token, 0)
        idf = math.log((corpus_size + 1) / (df + 1)) + 1.0
        weighted[token] = round(tf * idf, 4)

    top_items = sorted(weighted.items(), key=lambda item: (-item[1], item[0]))
    return dict(top_items[:60])


def lexical_score(terms: dict[str, float], text: str) -> float:
    tokens = set(tokenize(text))
    return sum(weight for token, weight in terms.items() if token in tokens)


def candidate_pool(sample_papers: list[dict], category_cover: list[str]) -> list[dict]:
    if not category_cover:
        return list(sample_papers)
    selected = []
    cover = set(category_cover)
    for paper in sample_papers:
        cats = set((paper.get("categories") or "").split())
        if cats & cover:
            selected.append(paper)
    return selected


def rank_by_lexical_terms(candidates: list[dict], lexicon: dict[str, float]) -> list[dict]:
    ranked = []
    for paper in candidates:
        score = lexical_score(lexicon, paper_text(paper))
        if score <= 0:
            continue
        ranked.append(
            {
                "arxiv_id": paper["arxiv_id"],
                "title": paper.get("title", ""),
                "abstract": paper.get("abstract", ""),
                "categories": paper.get("categories", ""),
                "primary_category": paper.get("primary_category", ""),
                "year": paper.get("year"),
                "lexical_score": round(score, 4),
            }
        )
    return sorted(
        ranked,
        key=lambda paper: (-paper["lexical_score"], -(paper.get("year") or 0), paper["arxiv_id"]),
    )


def normalize_scores(raw: list[float]) -> list[float]:
    if not raw:
        return []
    arr = np.asarray(raw, dtype=float)
    lo = float(np.min(arr))
    hi = float(np.max(arr))
    if hi - lo < 1e-9:
        return [1.0 for _ in raw]
    return [float((value - lo) / (hi - lo)) for value in raw]


def top_k_ranked_list(scores: np.ndarray, ids: list[str], k: int) -> list[str]:
    top_idx = np.argsort(scores)[-k:][::-1]
    return [ids[i] for i in top_idx]


def challenger_refinement(
    candidates: list[dict],
    lex_ranked: list[dict],
    embeddings: np.ndarray,
    ids: list[str],
    challenger_key: str,
) -> tuple[list[dict], dict]:
    id_to_idx = {pid: i for i, pid in enumerate(ids)}
    anchors = [paper for paper in lex_ranked if paper["arxiv_id"] in id_to_idx][:15]
    if len(anchors) < 5:
        raise RuntimeError(f"Insufficient lexical anchors for {challenger_key}: {len(anchors)}")

    anchor_ids = [paper["arxiv_id"] for paper in anchors]
    challenger_scores = base.centroid_scores(embeddings, ids, anchor_ids)
    score_by_id = {pid: float(challenger_scores[idx]) for idx, pid in enumerate(ids)}

    refined = []
    raw_scores = []
    for paper in candidates:
        pid = paper["arxiv_id"]
        if pid not in score_by_id:
            continue
        raw_scores.append(score_by_id[pid])

    normalized = normalize_scores(raw_scores)
    norm_iter = iter(normalized)
    for paper in candidates:
        pid = paper["arxiv_id"]
        if pid not in score_by_id:
            continue
        score = next(norm_iter)
        refined.append(
            {
                "arxiv_id": pid,
                "title": paper.get("title", ""),
                "abstract": paper.get("abstract", ""),
                "categories": paper.get("categories", ""),
                "primary_category": paper.get("primary_category", ""),
                "year": paper.get("year"),
                "challenger_score": round(score_by_id[pid], 6),
                "challenger_score_normalized": round(score, 6),
            }
        )

    refined.sort(
        key=lambda paper: (
            -paper["challenger_score_normalized"],
            -paper["challenger_score"],
            -(paper.get("year") or 0),
            paper["arxiv_id"],
        )
    )

    details = {
        "challenger_model": challenger_key,
        "lexical_anchor_ids": anchor_ids,
        "n_lexical_anchors": len(anchor_ids),
        "construction_scope": "2000-paper sample only",
    }
    return refined, details


def make_family_profile(
    *,
    profile_id: str,
    family_id: str,
    family_label: str,
    source_profile: dict,
    selected_papers: list[dict],
    category_cover: list[str],
    candidate_pool_size: int,
    selection_details: dict,
) -> FamilyProfile:
    if len(selected_papers) < 20:
        raise RuntimeError(
            f"{profile_id}/{family_id} produced only {len(selected_papers)} papers; need at least 20"
        )
    seeds = selected_papers[:15]
    held_out = selected_papers[15:20]
    return FamilyProfile(
        profile_id=profile_id,
        name=source_profile["name"],
        description=source_profile["description"],
        family_id=family_id,
        family_label=family_label,
        seed_papers=seeds,
        held_out_papers=held_out,
        category_cover=category_cover,
        candidate_pool_size=candidate_pool_size,
        selection_details=selection_details,
    )


def build_profile_families(
    sample_papers: list[dict],
    saved_profiles: dict[str, dict],
    document_frequency: Counter,
    challenger_embeddings: np.ndarray,
    challenger_ids: list[str],
    challenger_key: str,
) -> tuple[dict[str, dict[str, FamilyProfile]], dict]:
    families = {family_id: {} for family_id in FAMILY_IDS}
    construction_notes = {
        "minilm_saved": {
            "status": "existing family reused",
            "source": str(PROFILES_PATH),
        },
        "category_lexical": {
            "construction": "category cover >=80% seed-category mass, then lexical ranking on sample candidate pool",
        },
        "specter2_refined": {
            "construction": "same category cover as category family, lexical anchors bootstrapped from seed texts, then challenger centroid ranking on sample candidate pool",
            "challenger_model": challenger_key,
        },
    }

    for profile_id, profile in saved_profiles.items():
        category_cover = compute_category_cover(profile["seed_papers"])
        lexicon = build_profile_lexicon(profile, document_frequency, len(sample_papers))
        candidates = candidate_pool(sample_papers, category_cover)
        lex_ranked = rank_by_lexical_terms(candidates, lexicon)

        minilm_selection = []
        for paper in profile["seed_papers"] + profile.get("held_out_papers", []):
            paper_copy = dict(paper)
            paper_copy["source"] = "saved_profile"
            minilm_selection.append(paper_copy)
        families["minilm_saved"][profile_id] = make_family_profile(
            profile_id=profile_id,
            family_id="minilm_saved",
            family_label="Saved MiniLM-derived family",
            source_profile=profile,
            selected_papers=minilm_selection,
            category_cover=category_cover,
            candidate_pool_size=len(candidates),
            selection_details={"construction_scope": "saved profile asset"},
        )

        category_selection = []
        for paper in lex_ranked[:20]:
            chosen = dict(paper)
            chosen["source"] = "category_lexical"
            category_selection.append(chosen)
        families["category_lexical"][profile_id] = make_family_profile(
            profile_id=profile_id,
            family_id="category_lexical",
            family_label="Category + lexical family",
            source_profile=profile,
            selected_papers=category_selection,
            category_cover=category_cover,
            candidate_pool_size=len(candidates),
            selection_details={
                "construction_scope": "2000-paper sample only",
                "n_lexicon_terms": len(lexicon),
                "top_lexicon_terms": list(lexicon.items())[:12],
            },
        )

        refined_ranked, refined_details = challenger_refinement(
            candidates,
            lex_ranked,
            challenger_embeddings,
            challenger_ids,
            challenger_key,
        )
        refined_selection = []
        for paper in refined_ranked[:20]:
            chosen = dict(paper)
            chosen["source"] = "specter2_refined"
            refined_selection.append(chosen)
        families["specter2_refined"][profile_id] = make_family_profile(
            profile_id=profile_id,
            family_id="specter2_refined",
            family_label=f"{challenger_key.upper()}-refined family",
            source_profile=profile,
            selected_papers=refined_selection,
            category_cover=category_cover,
            candidate_pool_size=len(candidates),
            selection_details=refined_details,
        )

    return families, construction_notes


def evaluate_model_on_family_profile(
    family_profile: FamilyProfile,
    model_key: str,
    model_emb: np.ndarray,
    model_ids: list[str],
    minilm_emb: np.ndarray,
    minilm_ids: list[str],
    tfidf_matrix,
    categories: dict[str, list[str]],
) -> dict:
    seed_ids = [paper["arxiv_id"] for paper in family_profile.seed_papers[:5]]
    model_scores = base.centroid_scores(model_emb, model_ids, seed_ids)
    minilm_scores = base.centroid_scores(minilm_emb, minilm_ids, seed_ids)
    tfidf_scores = base.tfidf_scores(tfidf_matrix, minilm_ids, seed_ids)

    jaccard_vs_minilm = base.compute_jaccard_at_k(
        model_scores, model_ids, minilm_scores, minilm_ids, base.K_VALUES,
    )
    jaccard_vs_tfidf = base.compute_jaccard_at_k(
        model_scores, model_ids, tfidf_scores, minilm_ids, base.K_VALUES,
    )
    rank_corr = base.compute_rank_correlation(model_scores, minilm_scores)
    model_cat_recall = base.compute_category_recall(
        model_scores, model_ids, seed_ids, categories,
    )
    minilm_cat_recall = base.compute_category_recall(
        minilm_scores, minilm_ids, seed_ids, categories,
    )
    divergent_vs_minilm = base.compute_divergent_paper_analysis(
        model_scores, model_ids, minilm_scores, minilm_ids, categories,
    )
    divergent_vs_tfidf = base.compute_divergent_paper_analysis(
        model_scores, model_ids, tfidf_scores, minilm_ids, categories,
    )

    model_top20_ranked = top_k_ranked_list(model_scores, model_ids, 20)
    minilm_top20_ranked = top_k_ranked_list(minilm_scores, minilm_ids, 20)
    tfidf_top20_ranked = top_k_ranked_list(tfidf_scores, minilm_ids, 20)
    model_top20 = set(model_top20_ranked)
    minilm_top20 = set(minilm_top20_ranked)
    tfidf_top20 = set(tfidf_top20_ranked)
    truly_unique = model_top20 - minilm_top20 - tfidf_top20

    return {
        "seed_ids": seed_ids,
        "rank_correlation_vs_minilm": rank_corr,
        "jaccard_vs_minilm": jaccard_vs_minilm,
        "jaccard_vs_tfidf": jaccard_vs_tfidf,
        "category_recall": model_cat_recall,
        "minilm_category_recall": minilm_cat_recall,
        "divergent_vs_minilm": divergent_vs_minilm,
        "divergent_vs_tfidf": divergent_vs_tfidf,
        "union_size_minilm_model_at_20": len(model_top20 | minilm_top20),
        "union_size_minilm_tfidf_at_20": len(minilm_top20 | tfidf_top20),
        "union_delta_vs_tfidf_at_20": len(model_top20 | minilm_top20) - len(minilm_top20 | tfidf_top20),
        "n_truly_unique": len(truly_unique),
        "truly_unique_ids": sorted(truly_unique),
        "top20_model_ranked_ids": model_top20_ranked,
        "top20_minilm_ranked_ids": minilm_top20_ranked,
        "top20_tfidf_ranked_ids": tfidf_top20_ranked,
    }


def provisional_quantitative_classification(summary: dict) -> tuple[str, list[str]]:
    reasons = []
    mean_j = summary["mean_jaccard_vs_minilm_at_20"]
    min_j = summary["min_jaccard_vs_minilm_at_20"]
    mean_union_delta = summary["mean_union_delta_vs_tfidf_at_20"]
    profiles_beating_tfidf = summary["profiles_beating_tfidf_on_union_at_20"]
    mean_cat_diff = summary["mean_category_recall_diff_vs_minilm"]

    if mean_j >= 0.75 and min_j >= 0.60:
        reasons.append("high_overlap_with_minilm_across_family")
        return "near-redundant", reasons

    if profiles_beating_tfidf >= 3 and mean_union_delta >= 0.0 and mean_cat_diff >= -0.05:
        reasons.extend(
            [
                "beats_or_matches_tfidf_union_on_multiple_profiles",
                "category_recall_not_materially_worse_than_minilm",
            ]
        )
        return "candidate complementary second view", reasons

    if profiles_beating_tfidf == 0 and mean_union_delta <= -1.0:
        reasons.extend(
            [
                "materially_distinct_from_minilm",
                "fails_union_coverage_against_tfidf_benchmark",
            ]
        )
        return "distinct but not currently complementary", reasons

    reasons.append("mixed_quantitative_signals_need_review")
    return "blocked / unclear", reasons


def summarize_model_family(per_profile_metrics: dict[str, dict]) -> dict:
    jaccard_20 = [metrics["jaccard_vs_minilm"]["jaccard_at_20"] for metrics in per_profile_metrics.values()]
    tau = [metrics["rank_correlation_vs_minilm"]["kendall_tau"] for metrics in per_profile_metrics.values()]
    union_delta = [metrics["union_delta_vs_tfidf_at_20"] for metrics in per_profile_metrics.values()]
    cat_diff = [
        metrics["category_recall"]["recall"] - metrics["minilm_category_recall"]["recall"]
        for metrics in per_profile_metrics.values()
    ]
    truly_unique = [metrics["n_truly_unique"] for metrics in per_profile_metrics.values()]

    summary = {
        "mean_jaccard_vs_minilm_at_20": round(float(np.mean(jaccard_20)), 4),
        "min_jaccard_vs_minilm_at_20": round(float(np.min(jaccard_20)), 4),
        "max_jaccard_vs_minilm_at_20": round(float(np.max(jaccard_20)), 4),
        "mean_tau_vs_minilm": round(float(np.mean(tau)), 4),
        "min_tau_vs_minilm": round(float(np.min(tau)), 4),
        "max_tau_vs_minilm": round(float(np.max(tau)), 4),
        "mean_union_delta_vs_tfidf_at_20": round(float(np.mean(union_delta)), 4),
        "profiles_beating_tfidf_on_union_at_20": int(sum(1 for delta in union_delta if delta > 0)),
        "profiles_matching_tfidf_on_union_at_20": int(sum(1 for delta in union_delta if delta == 0)),
        "mean_category_recall_diff_vs_minilm": round(float(np.mean(cat_diff)), 4),
        "mean_truly_unique_vs_both_at_20": round(float(np.mean(truly_unique)), 4),
    }
    classification, reasons = provisional_quantitative_classification(summary)
    summary["provisional_quantitative_classification"] = classification
    summary["provisional_quantitative_reasons"] = reasons
    return summary


def find_changed_cases(family_results: dict[str, dict]) -> list[dict]:
    changed = []
    baseline_classifications = {
        model_key: family_results["minilm_saved"]["classifications"][model_key]["provisional_quantitative_classification"]
        for model_key in MODELS
    }

    for family_id in FAMILY_IDS:
        if family_id == "minilm_saved":
            continue
        for model_key in MODELS:
            baseline_cls = baseline_classifications[model_key]
            current_cls = family_results[family_id]["classifications"][model_key]["provisional_quantitative_classification"]
            if current_cls == baseline_cls:
                continue

            baseline_profiles = family_results["minilm_saved"]["per_profile_metrics"][model_key]
            current_profiles = family_results[family_id]["per_profile_metrics"][model_key]
            profile_deltas = []
            for profile_id in sorted(current_profiles):
                base_metrics = baseline_profiles[profile_id]
                cur_metrics = current_profiles[profile_id]
                j_delta = (
                    cur_metrics["jaccard_vs_minilm"]["jaccard_at_20"]
                    - base_metrics["jaccard_vs_minilm"]["jaccard_at_20"]
                )
                union_delta = (
                    cur_metrics["union_delta_vs_tfidf_at_20"]
                    - base_metrics["union_delta_vs_tfidf_at_20"]
                )
                profile_deltas.append(
                    {
                        "profile_id": profile_id,
                        "jaccard_delta_vs_baseline_family": round(j_delta, 4),
                        "union_delta_shift_vs_baseline_family": int(union_delta),
                        "baseline_family_union_delta_vs_tfidf": base_metrics["union_delta_vs_tfidf_at_20"],
                        "current_family_union_delta_vs_tfidf": cur_metrics["union_delta_vs_tfidf_at_20"],
                        "baseline_family_top20_ranked_ids": base_metrics["top20_model_ranked_ids"],
                        "current_family_top20_ranked_ids": cur_metrics["top20_model_ranked_ids"],
                        "baseline_family_unique_vs_both": base_metrics["truly_unique_ids"],
                        "current_family_unique_vs_both": cur_metrics["truly_unique_ids"],
                    }
                )
            profile_deltas.sort(
                key=lambda item: (
                    -abs(item["jaccard_delta_vs_baseline_family"]),
                    -abs(item["union_delta_shift_vs_baseline_family"]),
                    item["profile_id"],
                )
            )
            changed.append(
                {
                    "family_id": family_id,
                    "model_key": model_key,
                    "baseline_classification": baseline_cls,
                    "current_classification": current_cls,
                    "review_profiles": profile_deltas[:3],
                }
            )

    return changed


def serialize_family_profiles(family_profiles: dict[str, FamilyProfile]) -> dict:
    result = {}
    for profile_id, family_profile in family_profiles.items():
        result[profile_id] = {
            "profile_id": family_profile.profile_id,
            "name": family_profile.name,
            "description": family_profile.description,
            "family_id": family_profile.family_id,
            "family_label": family_profile.family_label,
            "seed_papers": family_profile.seed_papers,
            "held_out_papers": family_profile.held_out_papers,
            "category_cover": family_profile.category_cover,
            "candidate_pool_size": family_profile.candidate_pool_size,
            "selection_details": family_profile.selection_details,
        }
    return result


def main() -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_INPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_papers, _ = load_sample_papers()
    saved_profiles = load_saved_profiles()
    document_frequency = build_document_frequency(sample_papers)
    categories = base.load_paper_categories()

    minilm_emb, minilm_ids = base.load_embeddings("minilm")
    if minilm_emb is None:
        raise RuntimeError("MiniLM sample embeddings are missing")

    challenger_choice = None
    challenger_data = None
    for challenger_key in ("specter2", "gte"):
        data = base.load_embeddings(challenger_key)
        if data is not None:
            challenger_choice = challenger_key
            challenger_data = data
            break
    if challenger_choice is None or challenger_data is None:
        raise RuntimeError("No challenger embeddings available for family construction")

    challenger_emb, challenger_ids = challenger_data
    _, tfidf_matrix = base.build_tfidf(minilm_ids)

    family_profiles, construction_notes = build_profile_families(
        sample_papers,
        saved_profiles,
        document_frequency,
        challenger_emb,
        challenger_ids,
        challenger_choice,
    )

    loaded_embeddings = {}
    for model_key in MODELS:
        data = base.load_embeddings(model_key)
        if data is None:
            raise RuntimeError(f"Embeddings missing for {model_key}")
        loaded_embeddings[model_key] = data

    family_results = {}
    for family_id in FAMILY_IDS:
        per_profile_metrics = {model_key: {} for model_key in MODELS}
        classifications = {}
        for model_key, (model_emb, model_ids) in loaded_embeddings.items():
            for profile_id, family_profile in family_profiles[family_id].items():
                per_profile_metrics[model_key][profile_id] = evaluate_model_on_family_profile(
                    family_profile,
                    model_key,
                    model_emb,
                    model_ids,
                    minilm_emb,
                    minilm_ids,
                    tfidf_matrix,
                    categories,
                )
            classifications[model_key] = summarize_model_family(per_profile_metrics[model_key])

        family_results[family_id] = {
            "profiles": serialize_family_profiles(family_profiles[family_id]),
            "per_profile_metrics": per_profile_metrics,
            "classifications": classifications,
        }

    changed_cases = find_changed_cases(family_results)

    checkpoint = {
        "phase": "phase1_quantitative_framework_robustness",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sample_scope": str(SAMPLE_PATH),
        "construction_notes": construction_notes,
        "family_ids": FAMILY_IDS,
        "challenger_family_model": challenger_choice,
        "models": MODELS,
        "classification_labels": CLASSIFICATIONS,
        "classification_note": "These are provisional quantitative classifications. Any family-induced classification change requires qualitative review before it can count as a spike conclusion.",
        "family_results": family_results,
        "changed_cases_for_review": changed_cases,
    }

    checkpoint_path = CHECKPOINT_DIR / "phase1_quantitative.json"
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2, cls=NumpyEncoder) + "\n")

    review_payload = {
        "generated_at": checkpoint["timestamp"],
        "source_checkpoint": str(checkpoint_path),
        "note": "Review these cases qualitatively before treating any family-induced classification change as real.",
        "cases": changed_cases,
    }
    review_input_path = REVIEW_INPUT_DIR / "phase1_changed_cases.json"
    review_input_path.write_text(json.dumps(review_payload, indent=2, cls=NumpyEncoder) + "\n")

    print("Spike 005 quantitative checkpoint written:")
    print(f"  {checkpoint_path}")
    print("Changed-case review input written:")
    print(f"  {review_input_path}")
    print()
    print("Per-family provisional classifications:")
    for family_id in FAMILY_IDS:
        print(f"  {family_id}:")
        for model_key in MODELS:
            classification = family_results[family_id]["classifications"][model_key]
            print(
                f"    {model_key}: {classification['provisional_quantitative_classification']} "
                f"(mean J@20={classification['mean_jaccard_vs_minilm_at_20']:.3f}, "
                f"mean union delta vs TF-IDF={classification['mean_union_delta_vs_tfidf_at_20']:.3f})"
            )
    print()
    print(f"Changed cases requiring qualitative review: {len(changed_cases)}")


if __name__ == "__main__":
    main()
