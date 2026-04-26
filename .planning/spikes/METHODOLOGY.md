---
status: standing-reference
date: 2026-03-30
scope: critical lenses for spike research design and interpretation
audit_synthesis: 2026-04-25-v0.2-plan-audit-synthesis.md
related:
  - .planning/spikes/SPIKE-DESIGN-PRINCIPLES.md (practical rules — complements this document)
  - .planning/spikes/HYPOTHESES-005.md (hypotheses generated using these lenses)
  - .planning/deliberations/spike-epistemic-rigor-and-framework-reflexivity.md
  - .planning/deliberations/comparative-characterization-and-nonadditive-evaluation-praxis.md
provenance: >
  Produced through dialogue during Spike 004 post-execution critique (2026-03-28 to 2026-03-30).
  The conversation moved from self-critique of Spike 004's findings (seed sensitivity, MiniLM-centrism,
  Jaccard gatekeeping) to philosophical analysis of what went wrong methodologically, to identification
  of specific philosophies of science that could serve as critical lenses, to the question of how to
  preserve this thinking for future use.
---

# Spike Research Methodology

This document captures reusable critical lenses for spike design and interpretation. It complements SPIKE-DESIGN-PRINCIPLES.md (practical rules) with interpretive frameworks (analytical orientations that require judgment to apply).

**How to use this document**: Before designing a spike, an independent design critic should read each lens and ask whether the spike design is vulnerable to what the lens diagnoses. After execution, the findings critic should apply each lens to check whether the interpretation is warranted. The phase-mapping table at the end specifies which lenses apply when.

## The core distinction: representation vs function-in-use

Spikes 001-004 asked representational questions (what does the embedding space look like?) and tried to read functional conclusions off them (which model is better for researchers?). This doesn't work. Representational evidence constitutes one phenomenon (embedding space geometry); functional claims require evidence about a different phenomenon (what happens when someone uses the system).

Representation can serve as the *theory* that generates predictions about function. Function serves as the *test* that supports or undermines the representational theory. This is the right relationship: predict function from representation, then test function directly.

## Critical Lenses

### 1. Bayesian updating

**Diagnoses**: Binary verdicts (CONFIRMED/FALSIFIED) that throw away information about how much evidence shifted our confidence. Overclaiming followed by overqualifying ("SPECTER2 redundancy FALSIFIED!" → "well, actually, the seeds were different...").

**Recommends**: For each hypothesis, state a prior probability before execution and track how the evidence shifts it. Not formal Bayes factors — explicit statements of credence movement. "Before Spike 004, credence that SPECTER2 is redundant: ~0.7. After: ~0.3. Reasons for the shift: [tau evidence, seed sensitivity caveat, evaluation framework bias]."

**Concrete change**: Replace CONFIRMED/FALSIFIED with probability updates. Report the direction and magnitude of the shift, the evidence that produced it, and the conditions under which the shift would reverse.

**When it catches what others miss**: When a finding is partly confirmed and partly undermined. Binary verdicts force a choice; Bayesian updating represents the actual epistemic state.

### 2. Standpoint epistemology

**Diagnoses**: Evaluator monoculture. All quality judgments from one type of evaluator (AI list-review) with one implicit standpoint on what "relevant" means. The absent researcher is absent in a way that defaults to a specific standpoint without acknowledging it.

**Recommends**: Include structurally different evaluator types — not two instances of the same LLM, but genuinely different perspectives:
- An AI agent doing a research task (evaluator-as-user)
- A human researcher assessing recommendations (evaluator-as-expert)
- Category-metadata-based evaluation (evaluator-as-structure, no semantic model)

Where evaluators agree: high confidence regardless of which model is evaluated. Where they disagree: the disagreement reveals standpoint-dependent quality — the system should let users choose.

**Concrete change**: The convergence and divergence between evaluator types IS the finding, not noise to be averaged away.

**When it catches what others miss**: When AI reviewers and human researchers would disagree about what's valuable. This is likely for "productive provocations" — papers that challenge assumptions (valuable to an expert, hard for an AI to assess without research context).

### 3. Paradigm analysis

**Diagnoses**: Normal science within an unexamined paradigm. MiniLM-as-baseline defines what counts as evidence, what counts as a finding, what counts as an anomaly. Anomalies accumulate (seed sensitivity, Jaccard instability, evaluation-constitutes-findings) and get accommodated rather than prompting paradigm revision.

**Recommends**: Design at least one experiment that doesn't reference the incumbent model at all. Instead of "how does X compare to MiniLM?" ask "which configuration helps accomplish a research task?" The incumbent becomes one configuration among many, not the reference.

**Concrete change**: The experimental design itself should not privilege any model. Evaluation asks about task completion quality, not about agreement with a baseline.

**When it catches what others miss**: When the evaluation framework systematically advantages the incumbent. H4 (framework bias) is the test: if model rankings change under different profile constructions, the findings were paradigm-dependent.

### 4. Mechanistic decomposition

**Diagnoses**: End-to-end testing that confirms something works without explaining why. When it breaks, you don't know what to fix. When it succeeds, you don't know what's load-bearing. "Signal axis" characterizations are mechanistic stories with untested mechanism steps.

**Recommends**: For hypotheses with proposed mechanisms (training data → embedding geometry → recommendation character → researcher value), design tests for individual steps, not just the endpoint.

**Concrete change**: Each mechanism step becomes an independently testable sub-hypothesis. "SPECTER2 captures citation-community structure" decomposes into: (a) SPECTER2 paper pairs with high cosine similarity have more citation links than MiniLM pairs, (b) SPECTER2's divergent papers share citation communities with seeds more than MiniLM's divergent papers do.

**When it catches what others miss**: When the end-to-end prediction holds but for the wrong reason. A model might produce "good" recommendations (per AI review) via a mechanism completely different from the one we hypothesize — and understanding the actual mechanism matters for when/where to deploy it.

### 5. Values-in-science analysis

**Diagnoses**: Non-epistemic values doing implicit work in evaluation. Local-first preference shapes which models get investigated seriously. Exploration-first architecture predisposes toward finding "models are different" rather than "one model is best." Cost-awareness biases toward cheap configurations.

**Recommends**: Explicitly separate epistemic findings from value-laden recommendations. Present findings as configurations ranked by different value profiles, not as a single recommendation.

**Concrete change**: "If you value local-first: MiniLM + TF-IDF. If you value discovery breadth with GPU: add SPECTER2. If you value maximum divergent discovery and accept API dependency: add Voyage." The epistemic finding (models produce different rankings) is the same; the recommendation depends on values.

**When it catches what others miss**: When a finding is nearly discarded because it conflicts with project values (Voyage's P2 discovery was almost missed because rate-limiting made it "operationally impractical" — a value judgment that almost blocked an epistemic finding).

### 6. Duhem-Quine analysis

**Diagnoses**: Hypotheses entangled with untested auxiliary assumptions. You never test a hypothesis in isolation — you test hypothesis + evaluation framework + profile construction + metric choice + seed selection + sample composition. When a prediction fails, the failure could be in the hypothesis or in any auxiliary.

**Recommends**: For each finding, identify which auxiliary assumptions are load-bearing. Design experiments that vary one auxiliary at a time to disentangle.

**Concrete change**: H4 (vary profile construction method) is a Duhem-Quine test. Add more: vary seed set (already shown to matter), vary retrieval method (H3), vary evaluation method (H1). Findings that survive all auxiliary variations are robust. Findings that change are auxiliary-dependent and must be reported as such.

**When it catches what others miss**: When a finding appears to be about the hypothesis but is actually about the evaluation framework. The MiniLM-entanglement discovery was exactly this — "SPECTER2 is divergent" was partly about SPECTER2 and partly about using MiniLM-derived profiles.

## Practice disciplines

Added 2026-04-25 after the methodology-audit cycle (pressure pass + paired AI review + operationalization audit + property audit). The six lenses above are interpretive — they govern how a finding should be read. The disciplines below are operational — they govern how reviews, audits, and remedies should be produced. Both layers matter; the audit cycle showed that lens-rigor without practice-rigor produces high-confidence-but-wrong artifacts.

### A. Paired review for framing claims

**Diagnoses:** Single-reader audit memos and framing critiques propagated as ground truth. The 2026-04-25 pressure pass on the 005-008 handoffs claimed the suite contract did not pre-register a tiebreaker (it did, at `NEXT-ROUND-SUITE.md:65-69`), and ranked findings "highest impact" by fiat. Both errors caught only by paired review (cross-vendor + same-vendor).

**Recommends:** For audits or critiques whose framing claims are load-bearing on remedies, dispatch a paired review before adopting remedies. Pair structurally:

- **Cross-vendor reader** (e.g., GPT via codex CLI, xhigh effort) — catches substance more readily; reads carefully against the artifacts; less attuned to in-house rhetorical patterns.
- **Same-vendor adversarial reader** (fresh Claude session, xhigh effort) — catches register more readily; better at spotting Anthropic-internal rhetorical inflation, all-caps emphasis labels, prescriptive consequences ("Forces:") that overrun their diagnostic grounds.

The pair caught more together than either alone in the 2026-04-25 cycle. Cross-vendor saw substance; same-vendor saw register; both converged on a single textual fact that anchored the most reliable signal.

**Concrete change:** Audit-level remedies do not get adopted from single-reader output if the framing is contestable. Schedule a paired review before composition.

**Concrete change (extension, status: Hypothesis pending second methodology-audit cycle):** Same-vendor adversarial dispatches must not include other audits of the same artifact set as references, even at lower effort levels or earlier dates. Anchoring on prior findings produces delta-on-prior reasoning, which suppresses net-new finding discovery and inherits prior framings even where independent reading would re-evaluate them. The dispatching prompt must include an explicit forbidden-reading list naming all prior audits of the same artifact set; the agent's compliance is verifiable in its tool-use trace. The contaminated 2026-04-25 xhigh dispatch (preserved at `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial-xhigh-contaminated.md`) is the documented evidence base; the comparison at `.planning/audits/2026-04-25-v0.2-plan-audit-comparison.md` characterizes the observed effects (net-new finding suppression in two categories; one finding flipped from problem to strength under independent reading; prior framings inherited where independent reading would re-evaluate). Status remains `Hypothesis` until a second methodology-audit cycle either confirms or weakens the pattern.

**When it catches what others miss:** Single readers tend to overreach on framing claims they cannot fully cross-check; pairs surface the overreach. Self-review does not work for contestable framings — the same author cannot independently audit their own register.

### B. Model verification before delegating gating audits

**Diagnoses:** Audits dispatched to default sub-agents whose model is unverified, with verdicts then propagated as if they were known-quality. The 2026-04-25 Property audit was first dispatched to a default Explore agent (likely Haiku/Sonnet), reached "Property 1 = coupled" by reading an early alembic migration as current state, and missed that a later migration superseded it. Re-running with `model: "opus"` flipped the verdict; one direct read of the later migration confirmed the rerun.

**Recommends:** For audits that gate roadmap or architectural decisions:

- Do them directly, or dispatch with explicit `model: "opus"` (or known-quality equivalent).
- Default sub-agents (Explore in particular) are for cheap surface searches: file location, symbol presence, pattern matching. They are not for evidence claims that supersede each other across migrations or require independent reasoning about coupling.

**Cost test:** if a wrong verdict would cost more than half a day of rework or would propagate into a roadmap commit, the model must be known.

**Concrete change:** Audit dispatches must record the reviewer's model as part of the artifact's frontmatter. Audits with unverified model are marked `provisional` and do not gate decisions.

### C. Single-reader factual claims about the codebase need verification

**Diagnoses:** Claims of the form "X is current state" or "Y exists in the code" propagated without checking. The 2026-04-25 first audit cited a CHECK constraint from migration 003 as binding; verification (`ls alembic/versions/` + reading migration 005) took 30 seconds and reversed the verdict.

**Recommends:** Before propagating a load-bearing claim about the codebase, verify it. The cost is seconds; the cost of acting on a wrong claim is whatever the downstream commitment is worth.

**Concrete change:** For audits, every load-bearing factual claim cites a file:line. Verifications run as a cheap pass before remedies are written.

**When it catches what others miss:** Memory-of-pattern claims ("this is how this codebase usually works") are uniquely vulnerable. The verification step is non-negotiable when a claim is doing remedy-shaping work.

### D. Calibrated language as default register, not closing-section exception

**Diagnoses:** Confidence calibration confined to a closing footnote ("findings 1 and 2 are framing claims and may be wrong") while the prose above used unhedged rhetorical inflation ("load-bearing," "highest-impact," all-caps "CRITICAL," "Forces:"). The closing calibration does not reach the prose it qualifies. The 2026-04-25 pressure pass exhibited this pattern at the audit layer, replicating exactly what it diagnosed in the spike layer.

**Recommends:** Hedged, calibrated language runs through the prose. Confidence levels are stated where claims are made, not in a closing section. Rhetorical labels ("load-bearing," "critical," all-caps emphasis) require argument under them, not in lieu of argument.

**Concrete change:** Reviewers reading audit drafts flag rhetorical-inflation tokens ("Forces:", all-caps emphasis, "load-bearing," "highest-impact") and require either supporting argument or tonal de-escalation.

**When it catches what others miss:** Closure-pressure recurs at every layer of work. Calibration that does not propagate to register is not calibration.

### E. Pressure-test artifacts before adopting remedies

**Diagnoses:** Deliberations propose remedies from a constructed option space (Options A/B/C/D) without anchoring in concrete failure modes present in the artifacts the remedies would patch. The 2026-04-16 deliberation on sequential narrowing initially landed at Option C (challenge surface) drawn from a four-option space the deliberation itself constructed; the independent review identified that the option space was constructed to make C the only sensible answer.

**Recommends:** When a deliberation proposes patches, run diagnostic questions against the underlying evidence (handoffs, artifacts, source) *before* composing remedies. The pressure pass produces a separate artifact that does not overwrite the source evidence.

**Concrete change:** Multi-stage deliberation: situation → analysis → pressure pass on the underlying evidence → composition of remedy from the surfaced findings, not from the originally-constructed option space.

### F. Pattern-watch at every layer of work

**Diagnoses:** The closure-pressure pattern (premature commitment, rhetorical inflation, prescriptive remedies overrunning diagnostic grounds) recurred at the spike layer (005-008 narrowing toward a winner), at the audit layer (pressure pass overreach), and at the meta-audit layer (six confident reorientation components walked back to a smaller set under assumption audit). Each layer's discipline did not transfer to the next.

**Recommends:** When auditing a layer below, audit also the audit's own susceptibility to the pattern. Self-application is part of the discipline, not optional polish.

**Concrete change:** Methodology-audit artifacts include a self-application section explicitly addressing whether the audit itself exhibits what it diagnoses.

## Phase-Mapping: When to Apply Each Lens

| Phase | Lens | What to check |
|-------|------|---------------|
| **Hypothesis formulation** | Mechanistic | Are mechanism steps specified and independently testable? |
| **Hypothesis formulation** | Bayesian | Is a prior stated? Is the prediction specific enough to shift belief? |
| **Design critique** | Paradigm | Does this experiment test within a paradigm or question it? |
| **Design critique** | Duhem-Quine | Which auxiliary assumptions are load-bearing? Are they tested? |
| **Design critique** | Standpoint | Which evaluator types are included? What standpoints are missing? |
| **Execution** | Values | Are non-epistemic values shaping which configurations get tested? |
| **Interpretation** | Bayesian | How much did the evidence shift our credence? (Not: was it confirmed?) |
| **Interpretation** | Values | Are epistemic findings separated from value-laden recommendations? |
| **Post-execution critique** | All lenses | Independent critic applies each lens to the findings |

## What this document cannot do

This is a standing reference, not a protocol. It requires judgment to apply — knowing when a lens is illuminating vs when it's producing false positives. A critic who mechanically applies all lenses to every spike will generate noise. The lenses are tools for thinking, not checklists for compliance.

The document also cannot enforce its own consumption. It exists as available context. Making it operative requires a design review protocol that mandates reading it — which GSDR does not currently provide. See the filed gaps.
