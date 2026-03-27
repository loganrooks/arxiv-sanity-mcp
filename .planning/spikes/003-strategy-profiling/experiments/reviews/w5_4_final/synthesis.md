# W5.4 Synthesis: Parallel Views Architecture Validation

## Executive Summary

The parallel-views architecture -- presenting three labeled strategy outputs as "Similar Ideas," "Same Vocabulary," and "Adjacent Communities" -- is a defensible design concept with a serious execution problem. The concept of showing researchers multiple perspectives on relatedness is sound, but the current three-view configuration is not the right configuration. SPECTER2 ("Adjacent Communities") is redundant with MiniLM for all three tested profiles and its label is consistently inaccurate. The architecture should be simplified to two views, or SPECTER2 should be replaced with something that actually provides cross-community discovery.

---

## 1. Does the Parallel-Views Architecture Work as a Product?

**Partially.** The core insight is valid: different retrieval strategies capture different kinds of relatedness, and a researcher benefits from seeing multiple perspectives. But the current implementation fails to deliver on this promise because two of the three views (MiniLM and SPECTER2) produce substantially overlapping results.

### What works

- **MiniLM ("Similar Ideas")** is consistently the strongest view across all profiles. It surfaces papers that share the same research questions and methods. A researcher using only this view would get a good, focused reading list.

- **TF-IDF ("Same Vocabulary")** provides genuine complementary value when the profile's vocabulary is distinctive (P4: AI safety) but is actively harmful when the vocabulary is generic or dominated by a single broad term (P3: quantum ML). Its quality is profile-dependent.

- **The two-view combination of MiniLM + TF-IDF** reveals structural features of the research landscape that neither view reveals alone. For P4, this combination exposes two distinct sub-communities (jailbreak attack/defense vs safety-under-modification) that share vocabulary but ask different questions. This is genuinely useful.

### What does not work

- **SPECTER2 ("Adjacent Communities")** fails its label promise across all three profiles. It does not surface papers from adjacent communities. Instead, it surfaces papers from the same community with slightly different citation patterns. The MiniLM-SPECTER2 overlap is 12/20 for P1, 9/20 for P3, and 12/20 for P4. When two views share 45-60% of their papers, presenting them as separate perspectives is misleading.

- **SPECTER2 score compression** is a fundamental problem. Score ranges across all profiles:
  - P1: 0.9610-0.9682 (spread 0.0072, std 0.0022)
  - P3: 0.9475-0.9644 (spread 0.0170, std 0.0042)
  - P4: 0.9628-0.9775 (spread 0.0146, std 0.0042)

  These scores are compressed into such a narrow range that the ranking within the SPECTER2 view is essentially arbitrary. The model is saying "all of these papers are approximately equally related," which means the top-20 selection is not meaningful. Any 20 papers from the broader pool would produce a similar list.

- **60 papers is too many.** Even with three distinct views, 60 paper recommendations exceed what a researcher would triage in a single session. The tail quality drops in every view, especially past paper 15.

### Overlap pattern summary

| Profile | Total Unique (of 60) | All-3 Overlap | MiniLM-SPECTER2 Shared | TF-IDF Unique |
|---------|---------------------|---------------|----------------------|---------------|
| P1 (Medium) | 44 | 2 | 12 | 14 |
| P3 (Narrow) | 44 | 2 | 9 | 12 |
| P4 (Broad) | 42 | 3 | 12 | 12 |

The consistent finding: TF-IDF contributes the most unique papers, MiniLM and SPECTER2 converge.

---

## 2. Are Three Views the Right Number? Should SPECTER2 Be Dropped?

**Three views is one too many in the current configuration.** The evidence strongly supports dropping or replacing SPECTER2.

### The case against SPECTER2

1. **Redundancy with MiniLM.** Across all profiles, SPECTER2 and MiniLM share 45-60% of their top-20 papers. This level of overlap means a researcher switching from "Similar Ideas" to "Adjacent Communities" will see mostly the same papers with a few additions. This is not a meaningfully different perspective.

2. **Label inaccuracy.** "Adjacent Communities" implies cross-field discovery -- a systems biologist finding relevant work in epidemiology, or a quantum ML researcher finding connections to statistical learning theory. SPECTER2 does not deliver this. For P1, its unique papers are from the same RL-for-robotics community. For P4, its unique papers are from the same jailbreak/safety community. Only for P3 does SPECTER2 partially deliver on the label, surfacing some QML theory papers that are genuinely from an adjacent subfield.

3. **Score compression undermines ranking.** If the model cannot distinguish between its top and bottom picks, the view's ranking carries no information. A researcher has no basis for reading paper #1 before paper #20.

4. **The partial exception proves the rule.** SPECTER2 performs best for P3 (narrow profile), where citation patterns in the quantum ML space do distinguish between practical QML and theoretical QML subcommunities. But this is exactly the case where the gap between SPECTER2 and MiniLM is also smallest in terms of useful contribution -- MiniLM already covers the practical QML papers well.

### The case for two views

MiniLM + TF-IDF provides:
- **Precision** (MiniLM): "What is most semantically similar to my research?"
- **Breadth** (TF-IDF): "What else in the broader literature uses the same terminology?"

These are genuinely different questions. A researcher can understand why these two views exist and when to use each one. The mental model is simple: "Do I want papers that think like me, or papers that talk like me?"

### If a third view were added

If a third view were to be added, it should actually deliver cross-community discovery. Options:
- **Category-bridging retrieval**: Explicitly find papers that bridge the profile's primary arXiv categories with related ones (e.g., for a cs.RO researcher, surface relevant papers from eess.SY or cs.CV that share methods but not community).
- **Citation-diversity-aware ranking**: Instead of SPECTER2's cosine similarity (which compresses), use a citation-graph walk that explicitly penalizes papers in the same dense citation cluster and rewards papers reachable only through bridge nodes.
- **Temporal novelty**: Surface papers from the last 30 days that are trending in the profile's neighborhood -- a "what's new" view rather than a "what's related" view.

---

## 3. Are the Labels Accurate and Helpful?

### "Similar Ideas" (MiniLM)
- **Accuracy**: High. The view consistently surfaces papers with similar ideas.
- **Helpfulness**: High. A researcher immediately understands what to expect.
- **Recommendation**: Keep label as-is.

### "Same Vocabulary" (TF-IDF)
- **Accuracy**: Technically accurate but potentially confusing.
- **Problem**: "Same Vocabulary" suggests precision ("these papers use my exact terms") but the reality is that vocabulary matching is a noisy signal. For narrow profiles (P3), it matches on overly broad terms ("quantum") and surfaces irrelevant papers. For broad profiles (P4), it works well because the vocabulary is distinctive.
- **Alternative labels considered**:
  - "Keyword Matches" -- more honest but sounds low-quality
  - "Wider Literature" -- captures the breadth intent but is vague
  - "Related Terminology" -- more accurate but still vague
- **Recommendation**: Consider "Wider Field" or "Broader Matches" -- something that sets the expectation of breadth over precision. Or keep "Same Vocabulary" but add a subtitle like "Papers sharing key terms (broader scope)."

### "Adjacent Communities" (SPECTER2)
- **Accuracy**: Low. The view does not surface papers from adjacent communities.
- **Problem**: The label creates an expectation of cross-field discovery that the view does not deliver. A researcher expecting to find relevant work from adjacent fields will instead find more papers from their own field.
- **Recommendation**: If SPECTER2 is retained, relabel to "Citation Network Neighbors" or "Related by Citations" -- something that honestly describes what the view produces. But the better recommendation is to drop this view entirely (see Section 2).

---

## 4. What Does Using Parallel Views Feel Like Compared to a Single Best Strategy?

### The single-strategy experience (MiniLM only)

A researcher using only MiniLM would get a focused, high-quality list of 20 papers that share their research questions and methods. For all three profiles, the top 12-15 papers from MiniLM are solidly relevant. The experience would feel like "the system understands my research." The limitation would be occasional tunnel vision -- missing papers that approach the same problem from a different angle or that use different vocabulary.

### The three-view experience (current architecture)

A researcher presented with three views would:
1. Start with "Similar Ideas" and find a good list.
2. Switch to "Adjacent Communities" and find... mostly the same papers. Confusion: "Why does this exist? It looks the same as the first view."
3. Switch to "Same Vocabulary" and find a mix of relevant papers and noise. For P3, they would encounter quantum networking and quantum communication papers and lose trust. For P4, they would discover the fine-tuning safety cluster and feel genuinely rewarded.

The dominant experience would be confusion about why "Adjacent Communities" exists, followed by either reward or frustration from "Same Vocabulary" depending on the profile.

### The two-view experience (proposed: MiniLM + TF-IDF)

A researcher presented with two views would:
1. Start with "Similar Ideas" for their core reading list.
2. Switch to "Same Vocabulary" / "Wider Field" when they want to explore what else is happening in the broader landscape.

This is a simpler, more honest mental model. The researcher understands the tradeoff: precision vs breadth. They switch views intentionally, not out of curiosity about what a third view might add.

### Critical assessment: Is MiniLM alone sufficient?

For a product that prioritizes simplicity, MiniLM alone is nearly sufficient for all three profiles. The added value of TF-IDF is:
- **P1**: Marginal. TF-IDF adds some VLA/foundation model papers that are interesting but not essential.
- **P3**: Negative. TF-IDF adds mostly noise.
- **P4**: Significant. TF-IDF surfaces a genuinely distinct research cluster (safety under modification).

The case for two views rests primarily on P4-like profiles where the field has distinct sub-communities with overlapping vocabulary. For profiles like P1 and P3, a single view with a diversity flag or a "you might also like" section would be equally effective.

---

## Cross-Profile Findings

### Profile breadth affects view utility differently than expected

| Profile | Breadth | Best View | TF-IDF Quality | SPECTER2 Value |
|---------|---------|-----------|----------------|----------------|
| P1 (RL for robotics) | Medium | MiniLM | Mixed | Negligible |
| P3 (Quantum ML) | Narrow | MiniLM | Poor | Partial |
| P4 (AI Safety) | Broad | MiniLM | Good | Negligible |

The expected pattern might be: narrow profiles need fewer views, broad profiles need more. The actual finding is: TF-IDF quality depends on vocabulary distinctiveness (not breadth), and SPECTER2 is redundant regardless of breadth.

### SPECTER2 score compression is a systemic problem

SPECTER2 cosine similarity scores are compressed into the 0.94-0.97 range for all profiles. This is not a profile-specific issue -- it is a property of the embedding space. SPECTER2 embeddings are trained for citation prediction, which optimizes for distinguishing cited-from-uncited papers. Within the top-100 most-cited-like papers, the model has no gradation. This makes SPECTER2 fundamentally unsuitable for ranking within a shortlist.

### The "all-three-views" overlap is not a quality signal

Papers appearing in all three views (2 per profile for P1 and P3, 3 for P4) are not consistently the best papers. They are papers that happen to match all three retrieval strategies, which in practice means they are generic enough to be centrally located in all three spaces. For P4, the all-three overlap papers are genuinely excellent (Jailbreak-Zero, RL-based attacks, Safety Arms Race survey). For P1, they are average. Overlap count is not a reliable quality proxy.

---

## Recommendations

### Architecture decision

1. **Drop SPECTER2 as a default view.** It is redundant with MiniLM and its label is misleading. The score compression makes its ranking uninformative.

2. **Ship two views: MiniLM ("Similar Ideas") and TF-IDF ("Wider Field").** These provide genuinely different perspectives with a clear mental model for the researcher.

3. **Consider TF-IDF quality gating.** For narrow profiles where TF-IDF quality is poor (like P3), detect this condition (e.g., when the dominant vocabulary term accounts for >30% of TF-IDF weight) and either warn the researcher or hide the TF-IDF view.

4. **Reduce the default list size.** 10-15 papers per view instead of 20. The tail quality drops significantly past paper 12-15 in every view.

5. **If cross-community discovery is a product goal**, build it explicitly. SPECTER2 is not the tool for this job. Consider citation-graph walks that penalize within-cluster papers, or explicit category-bridging retrieval.

### Label recommendations

| Current Label | Proposed Label | Rationale |
|--------------|---------------|-----------|
| Similar Ideas (MiniLM) | Similar Ideas | Keep. Accurate and intuitive. |
| Same Vocabulary (TF-IDF) | Wider Field | Sets expectation of breadth over precision. |
| Adjacent Communities (SPECTER2) | (Drop) | View is redundant. |

### Metric recommendations for future evaluation

- **Qualitative distinctiveness** matters more than paper count. Two views with 8 unique papers each can have very different value if one's unique papers are thematically coherent and the other's are random.
- **Score range/compression** should be a view health metric. A view whose top-20 scores span less than 0.02 is not meaningfully ranking its papers.
- **Label-match rate** should be tracked: what fraction of a view's unique papers actually match the researcher's expectation from the label?
- **Profile-conditional quality** should be measured. TF-IDF quality varies dramatically across profile types, and the system should either adapt or warn.

---

## Final Verdict

The parallel-views concept is sound but the current three-view implementation is not the right product. The honest assessment is:

- **MiniLM alone** gets you 80% of the way for all profiles.
- **MiniLM + TF-IDF** gets you to 90% for profiles with distinctive vocabulary (P1, P4) and 80% for narrow profiles with generic vocabulary (P3).
- **Adding SPECTER2** does not improve the researcher experience for any tested profile. It adds confusion (why does this look the same?) and erodes trust (the "Adjacent Communities" label promises something it does not deliver).

The decision should be: two views by default, with the option to enable a third if and when a genuinely cross-community retrieval strategy is developed. Do not ship three views where two are redundant just because three sounds more comprehensive.
