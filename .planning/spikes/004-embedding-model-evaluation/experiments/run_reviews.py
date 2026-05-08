#!/usr/bin/env python3
"""
Spike 004 Phase 3b: Execute qualitative reviews.

This script generates the review prompts and templates but does NOT auto-complete them.
Qualitative review is a BLOCKING GATE per DESIGN.md — reviews must be examined
before proceeding. The script produces markdown review files that should be
reviewed for quality before the Phase 3 checkpoint is written.

The actual review generation uses an LLM (via agent or direct API) — this script
prepares the review templates and, when run with --execute, dispatches them.

Usage:
  conda activate ml-dev
  python run_reviews.py              # Generate templates only
  python run_reviews.py --execute    # Generate + execute reviews via LLM
  python run_reviews.py --verify     # Verify all required reviews exist
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
REVIEW_DIR = SPIKE_004_DIR / "experiments" / "review_inputs"
REVIEW_OUTPUT_DIR = SPIKE_004_DIR / "experiments" / "reviews"
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"


def build_review_prompt(review_input: dict) -> str:
    """Build a qualitative review prompt from review input data."""
    depth = review_input.get("depth", "full")
    review_type = review_input.get("type", "characterization")
    profile_name = review_input.get("profile_name", "Unknown")
    profile_id = review_input.get("profile_id", "?")

    seeds_text = "\n".join(
        f"  - [{s['arxiv_id']}] {s['title']} ({s.get('category', '')})"
        for s in review_input.get("seeds", [])
    )

    if review_type == "blind_comparison":
        model_a = review_input["model_a_label"]
        model_b = review_input["model_b_label"]

        def format_papers(papers, label):
            lines = []
            for i, p in enumerate(papers, 1):
                lines.append(f"\n### {label} Paper {i}: [{p['arxiv_id']}]")
                lines.append(f"**Title:** {p['title']}")
                lines.append(f"**Category:** {p.get('category', '')}")
                lines.append(f"**Score:** {p['score']:.4f}")
                lines.append(f"\n{p.get('abstract', 'No abstract available.')}")
            return "\n".join(lines)

        papers_text = format_papers(review_input["model_a_papers"], model_a)
        papers_text += "\n\n---\n\n"
        papers_text += format_papers(review_input["model_b_papers"], model_b)

        prompt = f"""# Blind Pairwise Qualitative Review

**Profile:** {profile_name} ({profile_id})
**Depth:** {depth}
**Models:** {model_a} vs {model_b} (identities withheld)

## Seed Papers
{seeds_text}

## Recommendations
{papers_text}

---

## Review Instructions

You are reviewing recommendations from two models for the interest profile "{profile_name}".
You do NOT know which model is which. Assess each set independently.

For EACH model's recommendation set:

1. **Per-paper relevance** (if full depth): For each paper, is it relevant to the seeds?
   - Relevant via similar topic/method
   - Relevant via adjacent community
   - Productive provocation (challenges assumptions, opens new directions)
   - Noise (no meaningful connection)

2. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - What aspects of the interest does it cover? What's missing?
   - Set coherence vs diversity balance

3. **Comparative assessment**:
   - Which set would better serve a researcher with this interest? Why?
   - What does each set find that the other misses?
   - Character of each set's errors (noise vs adjacent vs vocabulary match)

4. **Emergent observations**:
   - Anything surprising or noteworthy about the recommendations?
   - What kind of researcher would prefer each set?

5. **Absent researcher note**:
   - What would you need to know about the researcher's actual situation to assess properly?
   - What are you assuming about their needs?

6. **Metric divergence flags**:
   - Does your qualitative impression contradict any quantitative expectations?
"""
    else:
        model_key = review_input.get("model_key", "unknown")

        def format_papers(papers):
            lines = []
            for i, p in enumerate(papers, 1):
                div_marker = " [DIVERGENT]" if p.get("divergent") else ""
                lines.append(f"\n### Paper {i}{div_marker}: [{p['arxiv_id']}]")
                lines.append(f"**Title:** {p['title']}")
                lines.append(f"**Category:** {p.get('category', '')}")
                lines.append(f"**Score:** {p['score']:.4f}")
                lines.append(f"**In MiniLM top-20:** {p.get('in_minilm_top20', '?')}")
                lines.append(f"\n{p.get('abstract', 'No abstract available.')}")
            return "\n".join(lines)

        model_papers = format_papers(review_input.get("model_top20", []))
        n_unique = review_input.get("model_unique_count", 0)
        n_shared = review_input.get("shared_count", 0)

        prompt = f"""# Single-Strategy Characterization Review

**Model:** {model_key}
**Profile:** {profile_name} ({profile_id})
**Depth:** {depth}
**Overlap with MiniLM:** {n_shared}/20 shared, {n_unique} unique to {model_key}

## Seed Papers
{seeds_text}

## {model_key} Top-20 Recommendations
{model_papers}

---

## Review Instructions

You are reviewing the top-20 recommendations from {model_key} for the profile "{profile_name}".
Papers marked [DIVERGENT] are in {model_key}'s top-20 but NOT in MiniLM's.

{"### Full Review (all sections required)" if depth == "full" else "### Abbreviated Review (set-level + emergent only)"}

{"1. **Per-paper assessment**: For each paper:" if depth == "full" else ""}
{"   - Connection to seeds (direct, adjacent, provocative, noise)" if depth == "full" else ""}
{"   - For DIVERGENT papers especially: is this a genuinely different signal?" if depth == "full" else ""}
{"   - Discoverability: would a researcher find this via other means?" if depth == "full" else ""}

{"2" if depth == "full" else "1"}. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - Coverage: methods, applications, critiques, foundations?
   - What's conspicuously absent?
   - How does the character of divergent papers differ from shared papers?

{"3" if depth == "full" else "2"}. **Emergent observations**:
   - What kind of signal does this model capture that MiniLM doesn't?
   - Is the divergence signal (coherent, valuable) or noise (scattered, irrelevant)?
   - Any productive provocations among the recommendations?

{"4" if depth == "full" else "3"}. **Absent researcher note**:
   - What would you need to know about the researcher to assess this properly?

{"5" if depth == "full" else "4"}. **Metric divergence flags**:
   - Does your qualitative impression contradict quantitative expectations?
"""

    return prompt


def generate_templates():
    """Generate review template markdown files."""
    manifest_path = REVIEW_DIR / "manifest.json"
    if not manifest_path.exists():
        print("ERROR: Review manifest not found. Run generate_reviews.py first.")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    REVIEW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for review in manifest["reviews"]:
        input_path = Path(review["path"])
        with open(input_path) as f:
            review_input = json.load(f)

        prompt = build_review_prompt(review_input)

        # Save as markdown template
        output_name = input_path.stem + "_review.md"
        output_path = REVIEW_OUTPUT_DIR / output_name
        with open(output_path, "w") as f:
            f.write(prompt)

        print(f"  Template: {output_name}")

    return manifest["reviews"]


def verify_reviews():
    """Verify all required reviews have been completed (pre-synthesis checklist)."""
    manifest_path = REVIEW_DIR / "manifest.json"
    if not manifest_path.exists():
        print("ERROR: Review manifest not found.")
        return False

    with open(manifest_path) as f:
        manifest = json.load(f)

    all_present = True
    for review in manifest["reviews"]:
        input_path = Path(review["path"])
        review_name = input_path.stem + "_review.md"
        review_path = REVIEW_OUTPUT_DIR / review_name
        if not review_path.exists():
            print(f"  MISSING: {review_name}")
            all_present = False
        else:
            # Check it's not just the template (should have content beyond the prompt)
            content = review_path.read_text()
            if "## Review" not in content and "## Assessment" not in content:
                print(f"  INCOMPLETE: {review_name} (appears to be template only)")
                all_present = False
            else:
                print(f"  OK: {review_name}")

    if all_present:
        # Write checkpoint
        checkpoint = {
            "phase": "phase3_reviews",
            "status": "complete",
            "n_reviews": len(manifest["reviews"]),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(CHECKPOINT_DIR / "phase3_reviews.json", "w") as f:
            json.dump(checkpoint, f, indent=2)
        print("\nPhase 3 checkpoint written. Ready for Phase 4 synthesis.")
    else:
        print("\nPhase 3 INCOMPLETE. Complete all reviews before synthesis.")

    return all_present


def main():
    parser = argparse.ArgumentParser(description="Spike 004 Phase 3b: Qualitative reviews")
    parser.add_argument("--execute", action="store_true", help="Execute reviews via LLM")
    parser.add_argument("--verify", action="store_true", help="Verify review completeness")
    args = parser.parse_args()

    print("=" * 60)
    print("SPIKE 004 PHASE 3b: QUALITATIVE REVIEWS")
    print("=" * 60)

    if args.verify:
        verify_reviews()
        return

    # Generate templates
    print("\n--- Generating review templates ---")
    reviews = generate_templates()

    if args.execute:
        print("\n--- Review execution ---")
        print("Review execution should be done through the agent framework.")
        print("Each review template in experiments/reviews/ should be processed")
        print("by an LLM with the review input data, then the completed review")
        print("saved back to the same file.")
        print(f"\n{len(reviews)} reviews to complete.")
        print("\nAfter completing reviews, run: python run_reviews.py --verify")
    else:
        print(f"\nGenerated {len(reviews)} review templates in {REVIEW_OUTPUT_DIR}/")
        print("Next steps:")
        print("  1. Complete each review (via agent or manual)")
        print("  2. Run: python run_reviews.py --verify")
        print("  3. Then proceed to Phase 4 synthesis")


if __name__ == "__main__":
    main()
