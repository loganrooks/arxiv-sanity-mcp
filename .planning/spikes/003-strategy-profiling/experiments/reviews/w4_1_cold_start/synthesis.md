# W4.1 Cold-Start Synthesis

## Central Question

**What is the minimum viable seed count for a useful recommendation experience? Does the answer depend on the profile type?**

## Summary Verdict

The answer depends heavily on profile type, seed selection quality, and what "useful" means. The quantitative claim that "MiniLM works from 1 seed" is an oversimplification that obscures critical failure modes.

---

## Findings by Profile

### P1: RL for Robotics (Medium Breadth)

| Condition | MiniLM | TF-IDF |
|-----------|--------|--------|
| 1 seed | 18/20 relevant | 17/20 relevant (1 clear miss: web agents) |
| 3 seeds | 20/20 relevant (but over-rotated to VLA theme) | 15/20 relevant (2 clear misses: DeepSeek-R1, UserLM) |

**Minimum viable seed count: 1 for MiniLM, 1 for TF-IDF.**

Both strategies produce usable sets from 1 seed. The single seed happened to have very distinctive vocabulary (offline MBRL, world models, uncertainty, real robots), which gave both strategies strong signal. At 3 seeds, MiniLM lost balance (over-indexed on VLA papers from the 2 newer seeds), while TF-IDF introduced spurious matches on the "R1" token in paper titles.

### P3: Quantum Computing / Quantum ML (Narrow)

| Condition | MiniLM | TF-IDF |
|-----------|--------|--------|
| 1 seed | 17/20 relevant (but only covers fault-tolerance, not QML) | 12/20 relevant (6 classical circuit misses) |
| 3 seeds | 17/20 relevant (now covers both fault-tolerance and QML) | 10/20 clearly relevant (noisy with quantum-adjacent fields) |

**Minimum viable seed count: 1 for MiniLM (with caveats), 3+ for TF-IDF.**

MiniLM produces coherent recommendations from 1 seed, but they cover only the seed's sub-area (fault tolerance), not the full profile (which includes QML). Three seeds -- one per sub-area -- bring the full profile into view. TF-IDF fails at 1 seed due to term ambiguity ("circuit" matching classical circuits) and remains noisy at 3 seeds.

### P4: AI Safety / Alignment (Broad)

| Condition | MiniLM | TF-IDF |
|-----------|--------|--------|
| 1 seed | 20/20 relevant (but echo chamber: all jailbreaks) | 18/20 relevant (slightly more diverse) |
| 3 seeds | 20/20 relevant (deeper echo chamber) | 20/20 relevant (similar echo chamber) |

**Minimum viable seed count: Depends on definition of "useful."**

Both strategies produce perfectly relevant papers at 1 seed. But the recommendations are near-identical jailbreak papers with almost no diversity. For profile refinement (helping the user discover what they care about within AI safety), neither strategy works well at any seed count tested, because the seeds are all from the same sub-area. The problem is not the strategy -- it is seed homogeneity interacting with a topically clustered field.

---

## Cross-Profile Patterns

### 1. Seed specificity determines 1-seed performance more than strategy choice

The most important variable at 1 seed is the seed paper itself:
- A seed with distinctive technical vocabulary (P1's offline MBRL paper) gives both strategies enough signal to work.
- A seed in a narrow domain with ambiguous vocabulary (P3's quantum circuit paper) exposes TF-IDF's weaknesses while MiniLM handles it.
- A seed from a topically clustered field (P4's jailbreak paper) produces high precision but low diversity from both strategies.

At 1 seed, the question "does this seed have distinctive, unambiguous vocabulary?" predicts performance better than "which strategy are we using?"

### 2. MiniLM consistently outperforms TF-IDF on relevance precision

Across all conditions:

| Condition | MiniLM avg relevant/20 | TF-IDF avg relevant/20 |
|-----------|----------------------|----------------------|
| 1 seed | 18.3 | 15.7 |
| 3 seeds | 19.0 | 15.0 |

MiniLM never produces clearly irrelevant papers. TF-IDF produces 0-6 irrelevant papers depending on profile and seed count. The gap is largest for P3 (narrow domain with ambiguous terms) and smallest for P4 (topically clustered field with unambiguous terms).

### 3. Precision is necessary but not sufficient at cold start

P4 reveals that perfect relevance (20/20) can coexist with poor cold-start utility. If every recommendation is a minor variation on the seed, the user cannot use the recommendations to refine their profile. Cold start needs a different optimization target than steady-state recommendations:

- **Steady state:** maximize relevance to the user's known interests.
- **Cold start:** maximize information gain about the user's interests.

These are different objectives. A recommendation set that includes some "adjacent but not exactly matching" papers is more useful at cold start because it gives the user meaningful choices to react to.

### 4. Diversity matters more at cold start than at steady state

MiniLM's tight semantic matching produces highly relevant but homogeneous sets. TF-IDF's noisier matching produces less relevant but more diverse sets. At cold start, the diversity is more valuable:

- **P4 at 1 seed:** TF-IDF arguably outperforms MiniLM because its slightly noisier matches include T2I safety, healthcare safety, and multimodal defense -- giving the user more dimensions to react to.
- **P1 at 1 seed:** MiniLM's broader coverage of RL sub-topics (offline, online, sim-to-real, locomotion, manipulation) provides both precision and diversity. This is the ideal case.
- **P3 at 1 seed:** MiniLM's precision wins because TF-IDF's "diversity" is actually contamination (classical circuits).

The lesson: diversity is valuable when it comes from related sub-areas, not from irrelevant fields. MiniLM provides relevant diversity; TF-IDF provides a mix of relevant diversity and noise.

### 5. The 1-to-3 transition can help or hurt depending on seed heterogeneity

| Profile | Seed heterogeneity | MiniLM 1-to-3 effect | TF-IDF 1-to-3 effect |
|---------|-------------------|---------------------|---------------------|
| P1 | High (MBRL, VLA, multi-agent) | Over-rotated to VLA (+precision, -balance) | Added noise (R1 token matches) |
| P3 | High (complexity, applied QML, VDD) | Gained QML coverage (+balance, +coverage) | Reduced classical circuit noise (+precision) |
| P4 | Low (jailbreak, jailbreak, jailbreak) | Deepened echo chamber (=precision, -diversity) | Similar echo chamber (=precision) |

When seeds are heterogeneous, adding seeds helps (P3) or at least maintains quality (P1). When seeds are homogeneous, adding seeds can make the echo chamber worse (P4).

---

## Minimum Viable Seed Count: Recommendations

### For the system's cold-start UX

**1 seed is viable for MiniLM but not for TF-IDF in narrow domains.**

MiniLM produces usable (if incomplete) recommendations from 1 seed across all three profile types tested. TF-IDF fails for narrow domains with ambiguous vocabulary (P3) and should not be offered as the sole strategy at 1 seed.

**3 seeds is the practical minimum for good coverage** when the profile spans multiple sub-areas (which most real profiles do). However, the seeds must be heterogeneous -- 3 seeds from the same sub-area (P4) are no better than 1.

### Concrete UX guidance

1. **At 0-1 seeds:** Offer recommendations only with MiniLM. Display a prominent caveat: "Based on limited data -- these recommendations may not cover all your interests." Do not offer TF-IDF as the primary strategy.

2. **At 2-3 seeds:** Check seed heterogeneity. If seeds are from the same narrow sub-area, prompt the user to add a seed from a different angle. "You've added 3 papers about jailbreak attacks. Would you also be interested in alignment theory, interpretability, or AI governance?"

3. **At 5+ seeds:** Both strategies should perform adequately. The cold-start period is over.

4. **Never offer TF-IDF alone for narrow domains.** TF-IDF's term-ambiguity problem (quantum "circuit" vs. analog "circuit") is not a cold-start issue that goes away with more seeds -- it is a fundamental limitation of lexical matching in specialized domains.

---

## Does "MiniLM works from 1 seed" hold up qualitatively?

**Partially.**

- For P1 (medium breadth, distinctive seed): Yes. The 1-seed set is genuinely useful and a researcher could start working with it.
- For P3 (narrow domain, specific seed): Yes for relevance, no for coverage. The set covers the seed's sub-area but misses the other half of the profile.
- For P4 (broad profile, clustered seed): Yes for relevance, no for utility. The set is relevant but provides no information gain because it is an echo chamber.

The metric captures relevance but misses two critical cold-start dimensions:
1. **Coverage:** Does the set represent the full breadth of the user's interests? (Fails for P3 at 1 seed.)
2. **Diversity / information gain:** Does the set help the user refine their profile by offering meaningful choices? (Fails for P4 at any seed count tested.)

A more honest summary: **MiniLM produces relevant papers from 1 seed. Whether those papers constitute a useful cold-start experience depends on how distinctive the seed is and whether the user's interests extend beyond the seed's specific topic.**

---

## Open Questions for System Design

1. **Should cold-start recommendations optimize for diversity rather than precision?** The P4 finding strongly suggests yes. A cold-start recommendation algorithm should explicitly maximize topical spread within the relevant field, not just semantic similarity to seeds.

2. **Should the system detect seed homogeneity and prompt for diversification?** Yes. If all seeds cluster in one sub-area of a field, the system should tell the user. This is a UX problem, not a retrieval problem.

3. **Should TF-IDF be offered at cold start at all?** Only as a complement to MiniLM, never alone. TF-IDF's term-ambiguity failures in narrow domains (P3) are severe enough to undermine user trust. TF-IDF adds value when its broader matching picks up adjacent sub-topics (P4), but this value does not justify the contamination risk.

4. **Is "minimum viable seed count" the right question?** The data suggests that seed quality (distinctiveness, heterogeneity, coverage of profile sub-areas) matters more than seed quantity. Three homogeneous seeds (P4) are less useful than one distinctive seed (P1). The real question is: **what makes a good seed set for cold start?**
