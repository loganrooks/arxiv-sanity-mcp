---
type: design-review
status: complete
date: 2026-03-21
reviewer: Codex (GPT-5.4)
target: .planning/spikes/004-embedding-model-evaluation/DESIGN.md
scope:
  - project-context
  - previous-spikes
  - immanent-critique
verdict: revise-before-execution
linked_artifacts:
  - .planning/spikes/004-embedding-model-evaluation/DESIGN.md
  - .planning/spikes/003-strategy-profiling/DECISION.md
  - .planning/spikes/003-strategy-profiling/FINDINGS.md
  - .planning/spikes/003-strategy-profiling/experiments/reviews/cross_spike_qualifications.md
  - .planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-jaccard-screening-methodology.md
  - .planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-spike-experimental-design-rigor.md
  - .planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-premature-spike-decisions.md
  - docs/01-project-vision.md
  - docs/02-product-principles.md
  - docs/05-architecture-hypotheses.md
  - docs/08-evaluation-and-experiments.md
  - docs/10-open-questions.md
  - /home/rookslog/workspace/projects/get-shit-done-reflect/.planning/deliberations/spike-epistemic-rigor-and-framework-reflexivity.md
---

# Spike 004 Design Review

## Executive Assessment

Spike 004 is a substantial improvement over Spikes 001-003 as a design artifact. It has traceability to prior failures, explicit epistemic limits, a healthier stance toward inconclusive outcomes, and a much better sense of the project's actual values than the earlier spikes.

That said, the design is **not yet execution-ready**. The most important problem is not that it repeats the exact first-order errors of Spike 003. It mostly does not. The deeper problem is that it still risks repeating the second-order error documented in the linked deliberation: the document is more rigorous in what it says about method than in the concrete protocol it actually commits execution to.

**Review verdict:** revise before execution.

## Materials Reviewed

### Primary target
- `.planning/spikes/004-embedding-model-evaluation/DESIGN.md`

### Immediate spike context
- `.planning/spikes/003-strategy-profiling/DECISION.md`
- `.planning/spikes/003-strategy-profiling/FINDINGS.md`
- `.planning/spikes/003-strategy-profiling/experiments/reviews/cross_spike_qualifications.md`
- `.planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-jaccard-screening-methodology.md`
- `.planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-spike-experimental-design-rigor.md`
- `.planning/knowledge/signals/arxiv-mcp/sig-2026-03-20-premature-spike-decisions.md`
- `.planning/spikes/003-strategy-profiling/experiments/data/sample_2000.json`

### Broader project context
- `docs/01-project-vision.md`
- `docs/02-product-principles.md`
- `docs/05-architecture-hypotheses.md`
- `docs/08-evaluation-and-experiments.md`
- `docs/10-open-questions.md`
- `docs/adrs/ADR-0001-exploration-first.md`
- `docs/adrs/ADR-0002-metadata-first-lazy-enrichment.md`
- `docs/adrs/ADR-0004-mcp-as-workflow-substrate.md`

### Cross-project methodological context
- `/home/rookslog/workspace/projects/get-shit-done-reflect/.planning/deliberations/spike-epistemic-rigor-and-framework-reflexivity.md`

## Standards Applied

This review evaluates Spike 004 against four standards:

1. **Project standards**
   - discovery over overload
   - explicit and steerable interest modeling
   - multiple kinds of relatedness
   - cost-aware and local-first defaults
   - open questions remain visible

2. **Experiment standards**
   - structured qualitative review first
   - compare alternatives without architectural foreclosure
   - evaluate not only quality, but also cost, latency, trust, and workflow usefulness

3. **Cross-spike lessons already learned**
   - Jaccard cannot serve as a sole decision criterion
   - evaluation frameworks can be entangled with the favored model
   - skipped qualitative checkpoints materially change conclusions
   - extension experiments designed outside the core design are dangerous
   - DECISION-shaped artifacts create closure pressure beyond the evidence

4. **Immanent standards from Spike 004 itself**
   - multiple metrics whose disagreements matter
   - qualitative review as first-class and blocking
   - negative and inconclusive outcomes are legitimate
   - MiniLM entanglement must be acknowledged, not forgotten
   - absent-researcher and user-situation considerations must remain visible

## What Spike 004 Gets Right

These are real strengths and should be preserved through revision.

1. **It is historically aware.**
   The design directly ties each methodological change to a documented failure in Spike 003 rather than presenting itself as abstract best practice.

2. **It correctly retracts the fantasy of metric sufficiency.**
   Unlike the Voyage screening in Spike 003, this design does not treat one quantitative instrument as equivalent to the answer.

3. **It improves the ethical and product framing.**
   The sections on user situations, local-first tradeoffs, and the absent researcher are aligned with the project's stated values, especially cost-awareness, explainability, and explicitness.

4. **It keeps inconclusive outcomes available.**
   This is a direct improvement over the premature closure pattern identified in Spike 003 and in the GSDR deliberation.

5. **It preserves optionality better than previous spikes.**
   It does not begin by assuming API embeddings are necessary or unnecessary, nor that semantic-only retrieval should dominate the architecture.

## Findings

Findings are ordered by severity. "Grounded" means directly supported by reviewed artifacts. "Inferred" means a judgment that follows from the artifacts but is not itself explicitly stated in them.

### 1. Blocker: The design's evidence contract does not match its execution protocol

**Grounded**

The design says:
- no model verdict may be issued without qualitative review
- "grounded" answers for the main questions require quantitative evidence plus qualitative review across all 8 profiles

But the actual qualitative review protocol does not do that. Phase 3 specifies:
- single-strategy characterization on `P1/P3/P4`
- blind pairwise review only on the 2 profiles showing most divergence

The branch logic also leaves the `0.8 <= Jaccard <= 0.9` regime under-specified. Models above `0.9` get a lightweight check. Models below `0.8` get a full review. The middle band is not clearly resolved.

**Why this matters**

This is the clearest way Spike 004 risks repeating Spike 003: the document states a more rigorous epistemic standard than the executable procedure actually enforces.

**Repeated pattern**

Yes. This is the same family of failure as Spike 003's DESIGN-level rigor not being matched by execution reality.

### 2. Blocker: Challenger-aware sample validation is acknowledged but not yet executable

**Grounded**

The design correctly recognizes that validating the sample only from MiniLM's perspective advantages the incumbent. It therefore proposes challenger validation and says the sample should expand toward challengers' high-scoring full-corpus regions if needed.

But the executable plan only specifies:
- embedding the 2000-paper sample with all models
- comparing MiniLM sample vs full corpus for `P1/P3/P4`

It does not specify how a challenger's "high-scoring regions of the full corpus" are to be computed if challenger full-corpus embeddings do not yet exist.

**Why this matters**

The design names the incumbent-bias problem but does not yet give itself the machinery to detect or repair it. That leaves the design dependent on a correction it has not operationalized.

**Repeated pattern**

Partially. This is not the same as the 100-paper mistake, but it is another case where a key methodological safeguard is stronger in prose than in procedure.

### 3. Blocker: The comparison set does not actually answer one of the questions Spike 004 says it addresses

**Grounded**

The frontmatter says this spike addresses:
- whether API embeddings add value
- whether a different second view model would be better than TF-IDF

But the experiment design compares each candidate model only against MiniLM.

That can tell us whether a model offers something over MiniLM. It cannot by itself tell us whether the model is a better **second view** than TF-IDF, because TF-IDF is not part of the direct comparison frame.

**Why this matters**

The project does not need to know merely whether another embedding differs from MiniLM. It needs to know whether changing the current `MiniLM + TF-IDF` provisional arrangement would improve discovery relative to the already-supported lexical complement.

This is especially important given:
- Spike 003's strong evidence that MiniLM and TF-IDF are complementary
- the project's commitment to multiple relatedness operators
- the architecture docs' bias toward lexical baseline plus selective semantic layering

**Repeated pattern**

Yes, in a softer form. Earlier spikes often asked one question and then smuggled in a larger architectural one. Spike 004 risks doing the same unless it separates:
- "different from MiniLM"
- "better second view than TF-IDF"
- "strong enough to revise architecture"

### 4. Blocker: The embedding-generation protocol is under-specified at exactly the point where prior spikes already failed

**Grounded**

The design names models, rough sizes, and runtime assumptions. It does not specify:
- exact text fields embedded
- concatenation format
- whether titles and abstracts are both used for every model
- model-specific instructions or prefixes
- tokenizer truncation rules
- pooling or normalization policy
- seed aggregation method for recommendation scoring
- whether existing 19K embeddings are strictly comparable to new sample embeddings

**Why this matters**

Spike 001 and 003 already demonstrated that model-loading/configuration details can invalidate conclusions. After that lesson, protocol-level ambiguity here is not a minor omission. It is a core methodological hole.

**Repeated pattern**

Yes. Different content, same structural class: a comparison spike that risks invalid comparison because protocol details are not locked down enough.

### 5. Major: The design still gives Jaccard too much gatekeeping authority relative to its own methodological claims

**Grounded**

The design argues, correctly, that:
- different metrics constitute different aspects of the phenomenon
- disagreement among metrics is itself informative
- high-overlap models may still differ meaningfully in ordering

But the branch logic and the "genuinely different signal" criteria still rely heavily on Jaccard thresholds to decide which models deserve which kind of interpretive attention.

**Why this matters**

This is not the same mistake as using Jaccard alone. But it is adjacent to it. The design has philosophically decentered Jaccard while procedurally leaving it near the center.

**Repeated pattern**

Yes, but at a higher level of sophistication. The error is no longer "Jaccard is the answer." It is "Jaccard still does too much of the traffic control."

### 6. Major: "Blocking gate" remains a document property, not a workflow property

**Grounded**

The design says qualitative review is a blocking gate. The linked signals and deliberation both show that the actual workflow lacks enforcement mechanisms for this kind of thing. Spike 003 skipped its prescribed checkpoints even though the DESIGN.md was already sophisticated.

**Why this matters**

Without an enforcement or explicit pre-synthesis checklist, this is still vulnerable to the exact policy-without-adherence failure Spike 003 exposed.

**Repeated pattern**

Directly yes. This is the 003 adherence gap in near-identical structural form.

### 7. Major: The design risks outrunning the project's architectural posture

**Grounded + inferred**

Grounded:
- Project docs favor metadata-first, lexical baseline, and local-first defaults.
- Spike 003 explicitly deferred architecture-level decisions around embedding primacy and view count.
- Spike 004 includes architecture implications as a success criterion and synthesis output.

Inferred:
- As written, Spike 004 could still be read downstream as authority for revising architecture on the basis of AI qualitative review over one sampled, CS/ML-dominant corpus slice.

**Why this matters**

Project context matters here. The architecture hypotheses and ADRs do not forbid revising the semantic layer, but they do require reversibility, cost-awareness, and visible open questions. Any architectural claim coming out of 004 should therefore remain at most:
- **Chosen for now**
or
- **Open**

unless the evidence base becomes stronger than the current design can plausibly supply.

**Repeated pattern**

Yes. This is the premature-closure danger identified in Spike 003, now relocated into the phrase "architecture implications."

### 8. Major: Reproducibility and provenance are under-considered for model evaluation

**Inferred**

The project's product principles say provenance and inspectability are core. The design discusses cost and local/API tradeoffs, but it does not explicitly require recording:
- exact model revision or checkpoint hash
- tokenizer version
- instruction/prompt text for embedding APIs
- API model version/date
- whether provider-side model drift is possible

**Why this matters**

For API embeddings especially, "quality" that cannot be reproduced or precisely attributed is weaker evidence than the same quality from a pinned local checkpoint. This should affect interpretation and extrapolation confidence, not just implementation notes.

**Repeated pattern**

Not clearly a repeated spike mistake, but a missing consideration relative to project standards.

### 9. Moderate: The design still lacks explicit decision-readiness criteria

**Grounded**

Spike 003's lessons emphasize that some spikes should end with "decision deferred with clearer question." Spike 004 says that outcome is legitimate, which is good. But it does not clearly define what evidence would be sufficient to produce each class of outcome:
- retain current default
- offer candidate as optional experimental view
- revise provisional default
- defer decision

**Why this matters**

Without explicit output classes, the synthesis phase remains vulnerable to interpretive drift and sunk-cost closure pressure.

### 10. Moderate: The design's independent ground truth remains weak

**Grounded**

The design relies on category-based recall as the most model-independent quantitative instrument. But prior spikes already showed that category-based ground truth can favor some kinds of strategies by construction, or at least fail to capture the phenomenon of interest well.

**Why this matters**

This does not invalidate the metric. It means it should be explicitly treated as a narrow instrument, not as the independent quantitative arbiter that solves the entanglement problem.

## Repeated Patterns Across Spikes

### Pattern A: Methodological self-awareness outruns executable protocol

| Spike | Form of the problem |
|------|----------------------|
| 001 | strong conceptual claims built on misconfigured SPECTER2 and entangled evaluation |
| 002 | caveats existed, but Jaccard still dominated the presentation logic |
| 003 | DESIGN.md was strong; execution bypassed its own safeguards |
| 004 | methodological philosophy is strong; executable protocol still has unresolved gaps |

### Pattern B: Architecture questions expand faster than the experiment's actual evidence base

| Spike | Form of the problem |
|------|----------------------|
| 001 | multiple relatedness claims pushed toward architecture recommendations |
| 002 | backend divergence risked being treated as quality judgment |
| 003 | model and view-count conclusions outran the qualified evidence |
| 004 | candidate-model comparison risks being read as architecture-settling evidence |

### Pattern C: A metric is demoted in theory but remains powerful in practice

| Spike | Metric issue |
|------|---------------|
| 002 | Jaccard described as disagreement, still framed as key differentiator |
| 003 | MRR and Jaccard explicitly criticized, but still shaped conclusions |
| 004 | Jaccard is no longer sovereign, but still controls too much branching logic |

### Pattern D: Known limitations are named but not always converted into procedure

This is the deepest continuity from 003 to 004.

## Immanent Critique

This section evaluates Spike 004 by its own standards, not by an external methodology.

### Standard 1: "Multiple metrics whose disagreements are taken seriously"

**Assessment:** Partial pass.

The document genuinely pluralizes the instruments and explicitly says disagreements are informative. That is a major improvement.

It falls short because the procedural architecture still routes too much attention through Jaccard thresholds. The design says disagreements matter, but the branch logic still gives one metric disproportionate power over which disagreements become visible.

### Standard 2: "Qualitative review is first-class, not validation"

**Assessment:** Partial pass.

The design clearly treats qualitative review as constitutive rather than decorative. This is one of its strongest sections.

It falls short because:
- the actual coverage does not match the stronger rhetoric of "across all 8 profiles"
- the workflow still lacks enforcement
- the design does not yet specify what happens in the middle-overlap cases clearly enough

### Standard 3: "Entanglement is a condition to acknowledge, not a problem to solve"

**Assessment:** Honest but incomplete.

The design is much more honest than 003 about MiniLM entanglement. That honesty is real.

But it risks becoming a stable caveat rather than a live design constraint. The challenger-validation section tries to keep the issue active, but because that section is not yet executable, the entanglement may remain acknowledged without being materially constrained.

### Standard 4: "Negative and inconclusive results are findings, not failures"

**Assessment:** Strong pass at the level of framing; partial pass at the level of downstream risk.

The document has the right verbal posture toward inconclusiveness. This is good and should stay.

The residual risk is that the synthesis section still asks for architecture implications, which invites the same downstream appetite for conclusion that the document is trying to resist.

### Standard 5: "Responsibility to absent users and researcher situations"

**Assessment:** Strong pass.

This is probably the strongest qualitative improvement over previous spikes. The user-situation criterion and absent-researcher section are aligned with the project's product principles and with the linked deliberation's concerns.

### Standard 6: "Responsiveness during execution"

**Assessment:** Partial pass.

The design explicitly says methodology can be revised if anomalies surface. That is good.

But the same section also acknowledges that the design creates inertia toward plan-following. Since no process mechanism is added here beyond the statement itself, the responsiveness claim remains fragile.

## Missing Considerations

These are not all blockers, but they are missing from the current consideration set.

1. **Direct comparison to the current lexical second view**
   - If the question includes "better second view than TF-IDF," then TF-IDF should appear in the decision frame, not only as background context.

2. **Model protocol provenance**
   - Exact embedding recipe, checkpoint, tokenizer, instructions, normalization, and truncation should be captured up front.

3. **Decision classes**
   - The synthesis needs explicit output categories so it does not collapse into a yes/no architecture recommendation.

4. **Repeatability under provider drift**
   - Especially for Voyage, interpretation confidence should depend partly on reproducibility and version pinning.

5. **Minimal human anchoring**
   - Even a very small human sanity-check layer would better align the spike with its own user-situation criterion. [inferred]

## Recommendations Before Execution

These are recommendations for the spike design, not settled project decisions.

### Settled

1. **Revise the qualitative-review contract so the protocol matches the claims.**
   Either:
   - weaken the success-criteria language from "across all 8 profiles"
   or
   - strengthen the protocol so every verdict has clearly defined all-profile qualitative coverage rules.

2. **Specify the embedding protocol in full.**
   Lock down:
   - fields embedded
   - text formatting
   - truncation
   - normalization
   - model-specific instructions
   - aggregation and ranking logic
   - provenance fields to record

3. **Add an explicit middle-band branch for `0.8 <= Jaccard <= 0.9`.**
   Right now the branch logic is incomplete.

4. **Add a pre-synthesis checklist.**
   Before any synthesis or verdict:
   - required quantitative outputs present
   - required qualitative reviews present
   - sample validation outcome recorded
   - limitations updated

### Chosen For Now

1. **Bring TF-IDF into the decision frame for architecture-facing conclusions.**
   Not because Spike 004 needs to re-run Spike 003, but because "better second view than TF-IDF" cannot otherwise be answered.

2. **Constrain 004 outputs to a limited result vocabulary.**
   Suggested classes:
   - retain current provisional default
   - candidate merits optional experimental view
   - candidate merits further investigation under different conditions
   - evidence insufficient

3. **Treat API-dependency and reproducibility as interpretation/extrapolation criteria, not just operational notes.**
   This better fits the project's local-first and provenance-first values.

### Hypothesis

1. **A small human review layer may produce more value than adding more quantitative instrumentation.**
   This follows from both the project docs and the spike's own "absent researcher" section, but remains untested. [inferred]

### Open

1. **Whether architecture revision should be in scope at all for Spike 004**
   A narrower and safer scope would be:
   - characterize candidate embedding differences
   - update deferred questions
   - leave architecture as provisional unless evidence is overwhelming

2. **Whether challenger-aware sample repair is practical without much heavier full-corpus work**
   If not, the design should say so explicitly and downgrade the strength of conclusions accordingly.

## Decision Readiness Assessment

### Safe outputs for Spike 004

These are plausibly supportable after revision:
- whether tested models differ from MiniLM on this sampled CS/ML corpus
- what kinds of papers the divergent sets contain
- what operational burdens each model introduces
- whether SPECTER2 redundancy appears robust within the tested domain

### Outputs that should remain provisional even after a successful run

- changing the architecture's default second view
- preferring API embeddings over local-first defaults
- any claim that a model is "best" in a general sense
- any claim that findings generalize beyond recent CS/ML arXiv without new evidence

## Final Assessment

Spike 004 is the first spike in this sequence that seriously internalizes the critique produced by the earlier ones. It has genuine epistemic memory. It is better aligned with the project's actual soul than Spikes 001-003 were at corresponding moments.

But the comprehensive judgment is:

- **Improved:** yes
- **Methodologically self-aware:** yes
- **Faithful to project values:** mostly yes
- **Free of repeated mistakes:** no
- **Execution-ready as written:** no

The main repetition is not the old naive error of trusting one metric. The main repetition is subtler: a document whose methodological intelligence still exceeds the specificity and enforceability of the procedure that would implement it.

That is the central issue to fix before execution.
