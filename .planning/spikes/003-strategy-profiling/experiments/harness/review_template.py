"""
Generate qualitative review markdown templates.

Takes a strategy's recommendations + seed papers and generates a
pre-filled review template ready for an AI agent reviewer.
"""

from __future__ import annotations

from datetime import datetime, timezone
from textwrap import dedent


def generate_review_template(
    strategy_name: str,
    strategy_id: str,
    profile_id: str,
    profile_name: str,
    seed_papers: list[dict],
    recommended_papers: list[dict],
    config: dict | None = None,
    variant: str = "characterization",
    blind_label: str | None = None,
) -> str:
    """Generate a pre-filled qualitative review markdown template.

    Args:
        strategy_name: Human-readable strategy name.
        strategy_id: Machine ID (e.g., "S1a").
        profile_id: Interest profile ID (e.g., "P1").
        profile_name: Interest profile name (e.g., "RL for robotics").
        seed_papers: List of dicts with "arxiv_id", "title", "abstract".
        recommended_papers: List of dicts with "arxiv_id", "title", "abstract".
        config: Optional config dict (top_k, etc.).
        variant: Review protocol variant:
            "characterization" - Single strategy, identity disclosed
            "blind_comparison" - Strategy identity withheld
            "cold_start" - Cold-start variant with bootstrap assessment
            "configuration" - Same strategy, different config
        blind_label: Label to use instead of strategy name for blind reviews.

    Returns:
        Markdown string ready for an AI reviewer.
    """
    display_name = blind_label if variant == "blind_comparison" else f"{strategy_name} ({strategy_id})"
    config_str = ", ".join(f"{k}={v}" for k, v in (config or {}).items()) or "default"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Build seed papers section
    seeds_section = []
    for i, sp in enumerate(seed_papers, 1):
        seeds_section.append(f"**Seed {i}**: {sp.get('title', 'Unknown')}")
        abstract = sp.get("abstract", "").strip()
        if abstract:
            # Truncate long abstracts for readability
            if len(abstract) > 500:
                abstract = abstract[:497] + "..."
            seeds_section.append(f"> {abstract}")
        seeds_section.append("")

    seeds_text = "\n".join(seeds_section)

    # Build recommended papers section
    recs_section = []
    for i, rp in enumerate(recommended_papers, 1):
        title = rp.get("title", "Unknown")
        abstract = rp.get("abstract", "").strip()
        arxiv_id = rp.get("arxiv_id", "?")

        recs_section.append(f"### Paper {i}: {title}")
        recs_section.append(f"*arXiv: {arxiv_id}*")
        recs_section.append("")
        if abstract:
            if len(abstract) > 600:
                abstract = abstract[:597] + "..."
            recs_section.append(f"> {abstract}")
            recs_section.append("")

        recs_section.append("**Connection to seeds**: [Describe the relationship. What connects this paper to the research interest?]")
        recs_section.append("")
        recs_section.append("**What a researcher would get from this**: [If a researcher read this paper, what would they gain?]")
        recs_section.append("")
        recs_section.append("**Discoverability**: [How likely is the researcher to find this paper without the recommendation?]")
        recs_section.append("")

        if variant == "cold_start":
            recs_section.append("**Bootstrap value**: [Would this recommendation help the user refine their interest profile?]")
            recs_section.append("")

        recs_section.append("**Tension or surprise**: [Optional. Flag anything interesting.]")
        recs_section.append("")
        recs_section.append("---")
        recs_section.append("")

    recs_text = "\n".join(recs_section)

    # Variant-specific sections
    if variant == "blind_comparison":
        comparative_section = dedent("""\
        ## Part 3: Comparative Assessment

        ### What each strategy found that the other missed
        [For each strategy, identify 1-3 unique papers and explain WHY this strategy
        found them and the other didn't.]

        ### Where they agree and what agreement means
        [Identify consensus papers. Are they "safe" central papers or genuinely
        the strongest by both logics?]

        ### The character of each strategy's errors
        [What do each strategy's false positives look like?]

        ### If a researcher could only use one
        [For this specific interest profile: which strategy would better serve
        the researcher, and why? Under what circumstances would you change your answer?]
        """)
    else:
        comparative_section = ""

    if variant == "configuration":
        config_section = dedent("""\
        ## Configuration-Specific Assessment

        ### What changed?
        [Is the difference visible in the papers, or only in the metrics?]

        ### Is the change an improvement?
        [For this interest profile, does the configuration change help or hurt?]
        """)
    else:
        config_section = ""

    template = dedent(f"""\
    # Qualitative Review: {display_name} for {profile_id} ({profile_name})

    ## Context
    - **Seeds**: {len(seed_papers)} papers (listed below)
    - **Strategy**: {display_name}
    - **Config**: {config_str}
    - **Top-K**: {len(recommended_papers)}
    - **Date**: {date_str}
    - **Variant**: {variant}

    ## Seed Papers

    {seeds_text}

    ## Part 1: Per-Paper Assessment

    For each recommended paper, assess three dimensions. Do NOT reduce these
    to numbers. The point is to articulate the nature of the connection
    (or lack thereof), not to rank papers on a scale.

    For clearly relevant or clearly irrelevant papers, a single sentence
    suffices. Reserve longer assessments for ambiguous cases -- the
    surprising connections, the subtle false positives. These are where
    strategy character is revealed.

    {recs_text}

    ## Part 2: Set-Level Assessment

    ### Overall character
    [In 2-3 sentences: what KIND of recommendations does this strategy produce?
    Is it a "more of the same" recommender or a "broaden your horizons" recommender?]

    ### Strengths
    [What does this recommendation set do well?]

    ### Gaps
    [What's missing? What papers should be here but aren't?]

    ### False positive pattern
    [What do the irrelevant recommendations have in common?]

    ### Failure modes
    [If this strategy fails, HOW does it fail? Obvious or subtle?]

    {comparative_section}
    {config_section}

    ## Part 4: Emergent Observations

    THIS SECTION IS THE MOST IMPORTANT.

    This is where findings that exceed the predefined categories go.
    The Spike 001 discovery that quality has three dimensions (topical
    precision, methodological kinship, discovery potential) came from
    open-ended observation, not from the rubric.

    Prompts (use any or none):
    - Did any recommended paper change how you understand the interest profile?
    - Did the recommendation set reveal a sub-community or approach you hadn't considered?
    - Is there a pattern that suggests the strategy "thinks" about relatedness in a specific way?
    - Did you notice something about the seeds themselves when reviewing the recommendations?
    - Does this strategy surface a type of paper that none of the metrics would capture?
    - Is there a quality dimension that the rubric above fails to measure?

    [Write observations here]

    ## Part 5: Metric Divergence

    Flag cases where your qualitative impression contradicts the quantitative
    metrics. These flags are crucial -- they indicate where our metrics are
    measuring the wrong thing.

    Examples:
    - "Metrics say coherence is high, but the set doesn't feel coherent"
    - "MRR is low but the recommendations are actually good"
    - "Diversity score is high but it feels like noise, not breadth"

    [Write divergences here]
    """)

    return template


def generate_comparison_template(
    profile_id: str,
    profile_name: str,
    seed_papers: list[dict],
    strategy_a_name: str,
    strategy_a_recs: list[dict],
    strategy_b_name: str,
    strategy_b_recs: list[dict],
) -> str:
    """Generate a blind pairwise comparison template.

    Strategy identities are withheld; they appear as "Strategy A" and "Strategy B".

    Args:
        profile_id: Interest profile ID.
        profile_name: Interest profile name.
        seed_papers: Seed papers (shared context).
        strategy_a_name: Real name of strategy A (recorded for later, not shown to reviewer).
        strategy_a_recs: Strategy A's recommendations.
        strategy_b_name: Real name of strategy B.
        strategy_b_recs: Strategy B's recommendations.

    Returns:
        Markdown template with strategy identities withheld.
    """
    # Generate individual reviews for each strategy (blind)
    review_a = generate_review_template(
        strategy_name=strategy_a_name,
        strategy_id="?",
        profile_id=profile_id,
        profile_name=profile_name,
        seed_papers=seed_papers,
        recommended_papers=strategy_a_recs,
        variant="blind_comparison",
        blind_label="Strategy A",
    )

    review_b = generate_review_template(
        strategy_name=strategy_b_name,
        strategy_id="?",
        profile_id=profile_id,
        profile_name=profile_name,
        seed_papers=seed_papers,
        recommended_papers=strategy_b_recs,
        variant="blind_comparison",
        blind_label="Strategy B",
    )

    # Combine with a mapping footer (for post-review unblinding)
    combined = dedent(f"""\
    # Blind Pairwise Comparison: {profile_id} ({profile_name})

    **Important**: Review both strategy outputs independently before reading
    the comparative sections. Strategy identities are withheld.

    ---

    {review_a}

    ---

    {review_b}

    ---

    ## Unblinding (do NOT read until review is complete)

    <!-- UNBLINDING KEY (for post-review analysis only):
    Strategy A = {strategy_a_name}
    Strategy B = {strategy_b_name}
    -->
    """)

    return combined
