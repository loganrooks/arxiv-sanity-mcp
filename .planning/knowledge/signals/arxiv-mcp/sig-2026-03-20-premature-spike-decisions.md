---
id: sig-2026-03-20-premature-spike-decisions
type: signal
project: arxiv-mcp
tags: [gsd-framework, spike-workflow, epistemic-rigor, premature-closure, experimental-design]
created: 2026-03-20T16:00:00Z
updated: 2026-03-20T16:00:00Z
durability: principle
status: active
severity: notable
signal_type: capability-gap
phase: spike-003
plan: n/a
polarity: negative
source: manual
occurrence_count: 2
related_signals: [sig-2026-03-19-spike-framework-scope-gap, sig-2026-03-20-spike-experimental-design-rigor]
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## What Happened

Spike 003's DECISION.md made concrete architecture decisions — drop SPECTER2, two views not three, MiniLM as primary, parallel views as THE architecture, no API embeddings needed — while the same document's epistemic qualifications section (Section 8) systematically undermines the evidence base for those decisions. The qualification section documents:

- Evaluation framework entangled with MiniLM at every level (clusters, profiles, LOO-MRR)
- SPECTER2 redundancy finding based on 3-profile AI qualitative review in one domain (CS/ML)
- Voyage verdict based on methodologically insufficient screening (100-paper pool, Jaccard only)
- Cross-family MRR comparisons inflated by circular evaluation bias
- All quality assessments are proxy-based or AI-generated with no human validation

Despite these qualifications, the document still makes definitive architecture decisions. The honest position for several of these is "decision deferred pending further experimentation" — but the DECISION.md template has a "Decision" section that structurally pressures closure. There is no concept of a partially-decided spike or a spike that concludes with "we learned X but cannot yet decide Y."

Additionally, experiments conducted in a confirmatory or profiling mode may uncover results that challenge prior assumptions. The workflow should accommodate pivoting to further exploratory work when this happens, rather than pushing toward conclusions based on the evidence originally expected.

## Context

The pattern: write a Decision section (because the template requires it), then qualify it so heavily that the qualifications effectively retract the decision. This produces a document that a naive reader takes as "decided" but a careful reader recognizes as "provisional at best." The naive reading is dangerous because downstream implementation work may proceed on the authority of a "decision" that the evidence doesn't support.

Specific decisions that should be deferrals:

| Currently stated as | Should be | Why |
|--------------------|-----------| ----|
| "Drop SPECTER2" | Deferred — may not be redundant outside CS/ML | Based on 3 AI-reviewed profiles in one domain |
| "MiniLM as primary" | Provisional v1 default — advantage may be circular | Evaluation framework inflates MiniLM |
| "Two views not three" | Deferred — optimal view count unknown | Depends on SPECTER2 decision |
| "No API embeddings needed" | Deferred — screening was insufficient | Already revised to LOW confidence |
| "Parallel views as architecture" | Provisional default — fusion has profile-dependent value | W3 qualitative found fusion helps narrow topics |

Decisions that ARE justified:
- float16 storage (direct paired measurement)
- Strategy eliminations: SVM, title-only, cross-encoder (clear measured cause)
- Strategies are complementary (both quant + qual support)
- TF-IDF has scale and cold-start limitations (measured)

## Potential Cause

Three interacting causes:

1. **Template pressure.** The DECISION.md template expects a "Decision" section with a "Chosen approach." This creates psychological and structural pressure to decide something, even when the evidence warrants deferral. The format doesn't accommodate "we learned a lot but the decision isn't ready."

2. **Sunk cost of experimentation.** After running 5 waves, 21 qualitative reviews, and multiple extensions across 3 sessions, there is pressure to "have something to show for it" — a concrete decision feels more valuable than a well-qualified "not yet." But premature closure destroys the value of the qualification work by encouraging readers to skip to the Decision section.

3. **Missing workflow concept.** GSD Reflect's spike workflow has no concept of:
   - A spike that defers its decision to a follow-up spike
   - Partial decisions (some findings are decisive, others need more work)
   - Decision readiness criteria (what evidence would be sufficient to decide?)
   - Experiments that start confirmatory but discover they need to become exploratory

   The plan-checker agent verifies plans before execution. No equivalent exists to verify that a spike's evidence actually supports its stated decisions before the DECISION.md is finalized.

The deeper issue: the spike workflow assumes experiments produce answers. Sometimes experiments produce better questions. The framework should treat "decision deferred with clearer question" as a legitimate, valuable spike outcome — not a failure to conclude.
