# Evaluation and Experiments

**Status:** Draft  
**Date:** 2026-03-08

If we want to keep the design space open, we need a clear way to compare alternatives.

## 1. What we are evaluating

We are not only evaluating search relevance.

We are evaluating:

- discovery usefulness,
- recommendation quality,
- workflow friction,
- explanation quality,
- cost,
- latency,
- and rights / provenance robustness.

## 2. Core experiment tracks

## Track A — Retrieval
Compare:
- fielded lexical,
- lexical full text / abstract,
- semantic retrieval,
- graph expansion,
- hybrid candidate generation.

Questions:
- Which is best for exact terminology?
- Which is best for concept drift / vocabulary mismatch?
- Which is most trustworthy?
- Which is cheapest?

## Track B — Related-paper discovery
Compare:
- paper-to-paper lexical similarity,
- embedding similarity,
- OpenAlex `related_works`,
- citation-neighborhood expansion,
- hybrid relatedness.

Questions:
- Which notion of “related” helps users most in practice?
- Do different workflows want different relatedness operators?

## Track C — Interest modeling
Compare:
- tags only,
- seed sets,
- collections/workspaces,
- saved queries,
- mixed profiles,
- negative examples.

Questions:
- Which is easiest to steer?
- Which yields the best recommendations?
- Which is best for agents?

## Track D — Workflow support
Compare:
- stateless search-only interaction,
- collections + triage,
- saved queries + watches,
- checkpoints + deltas.

Questions:
- Which objects remove the most agent friction?
- What is actually needed in v1?

## Track E — Content normalization
Compare:
- HTML extraction,
- source-derived extraction,
- GROBID XML,
- Marker markdown,
- Docling,
- PDF-only fallback.

Questions:
- Which produces the best markdown for research-agent use?
- Which is most robust?
- Which is cheapest?

## 3. Evaluation assets we should build early

### A. Golden query set
A curated set of real discovery queries, covering:
- exact term queries,
- acronym-heavy queries,
- broad exploratory questions,
- author/entity lookups,
- recent-paper monitoring tasks.

### B. Golden seed set
A set of representative seed papers for:
- finding neighbors,
- backward/forward citation expansion,
- and project bootstrapping.

### C. Golden workflow scripts
Representative agent workflows, such as:
- “find this week’s new papers in a topic”
- “expand from these 3 seeds”
- “build a shortlist for project X”
- “what changed since last Monday?”

### D. Content benchmark set
A small but diverse collection of papers for evaluating content extraction:
- clean TeX papers
- image-heavy PDFs
- equation-heavy papers
- tables
- code blocks
- multi-column layouts

## 4. Metrics

### Retrieval metrics
- judged relevance@k
- coverage / recall on known important papers
- diversity
- novelty
- redundancy

### Recommendation metrics
- profile fit
- user / evaluator preference
- controllability
- explanation usefulness

### Workflow metrics
- number of tool calls required
- state-management friction
- ability to resume
- ability to compute deltas correctly

### Content metrics
- heading fidelity
- reference fidelity
- table fidelity
- equation fidelity
- markdown cleanliness
- section chunk quality

### Operational metrics
- latency
- storage cost
- API cost
- local compute cost
- failure rate
- cache hit rate

### Trust metrics
- explanation usefulness
- provenance completeness
- rights / license correctness

## 5. Evaluation style

The first evaluation style should be **structured qualitative review**, not just offline leaderboard metrics.

Why:
- many of the core questions are product questions,
- agent workflows are hard to reduce to a single scalar metric,
- and explanation / trust matter.

## 6. Decision gates

Before freezing any major choice, ask:

### Gate 1 — Search
Is the new approach clearly better than the strongest lexical baseline on representative queries?

### Gate 2 — Relatedness
Does the new method surface neighbors that are more useful than the baseline for real tasks?

### Gate 3 — Interest model
Does the richer model improve steerability rather than merely adding complexity?

### Gate 4 — Workflow object
Does this state object remove genuine friction in agent workflows?

### Gate 5 — Content backend
Is the quality gain worth the cost and operational burden?

### Gate 6 — Rights handling
Can we implement it safely and clearly enough to ship?

## 7. Default experiment process

1. write down the hypothesis,
2. define the comparison baseline,
3. define the dataset / workflow,
4. define success / failure criteria,
5. run the experiment,
6. record results and cost,
7. either:
   - keep it open,
   - choose for now,
   - or write an ADR.

## 8. Required experiment metadata

Every experiment record should capture:

- date,
- author / agent,
- hypothesis,
- alternatives tested,
- datasets or workflows used,
- implementation notes,
- metrics,
- qualitative observations,
- cost / latency notes,
- decision outcome.

Use `docs/templates/experiment-template.md`.

## 9. Strong early experiments to run

### Experiment 1
Metadata + lexical baseline vs lexical + OpenAlex graph filters

### Experiment 2
Seed expansion:
- local lexical baseline
- OpenAlex `related_works`
- Semantic Scholar recommendations
- hybrid merge

### Experiment 3
Interest profile representations:
- tags
- seed sets
- collections + seeds

### Experiment 4
Content pipeline:
- arXiv HTML
- source-derived
- Marker
- Docling
- GROBID intermediate

### Experiment 5
Processing promotion strategies:
- demand-driven (touch-to-promote)
- cohort-based (recent window auto-promotes)
- budget-constrained exploration (bandit-like allocation)
- two-phase (collect triage data, then train classifier)

Measure: compute cost per useful discovery, recall of eventually-important papers, user satisfaction with surfaced results.

### Experiment 6
Undervalued paper discovery:
- low-citation high-similarity surfacing
- cross-category serendipity (exploration budget fraction)
- author-emergence signals
- baseline: popularity-only ranking

Measure: fraction of surfaced papers that users later save/cite, novelty of discoveries vs baseline, serendipity dial calibration.

## Working conclusion

The system should be built so that strong comparisons are easy to run and easy to document.
