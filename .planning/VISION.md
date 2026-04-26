---
document: VISION
status: living — refine as the substrate matures
type: product-identity
audience: AI / CS / ML researchers (primary); AI-ethics, AI-philosophy researchers (adjacent)
last_updated: 2026-04-25
related_documents:
  - .planning/LONG-ARC.md
  - .planning/PROJECT.md
  - .planning/ROADMAP.md
  - docs/adrs/ADR-0001-exploration-first.md
  - docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md
  - .planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md
---

# arXiv Discovery MCP — Long-Term Vision

## Platform identity

A best-possible research-discovery substrate for AI / CS / ML researchers, MCP-native, that lives in the researcher's practice over years. Its center of gravity is not a single retrieval ranking; it is a **multi-lens substrate** that supports the operations practicing researchers actually perform: orienting attention in a fast-moving field, tracking intellectual lineages, locating dissent, recognizing paradigm shifts, sustaining longitudinal memory across reading sessions, calibrating trust through inspectable provenance, and steering between communities and methodological registers.

The platform is for someone whose research practice is shaped over months and years by what they read, who they read alongside, what arguments they find compelling, what methodologies they reach for, and what they have learned to ignore. The platform's job is to support that practice — not to replace judgment with ranked lists.

## What we inherit from arxiv-sanity, what we diverge from

**Inherit:** the product soul — discovery over overload, explicit taste modeling, fast browsing and triage, inspectable similarity, recent-paper monitoring.

**Diverge:**
- arxiv-sanity is a single-user web app oriented to one retrieval mode (TF-IDF + Karpathy's library). We are an MCP-native substrate exposing multiple retrieval / ranking / framing operations as first-class tools.
- arxiv-sanity treats taste as tags and library state. We treat taste as a **bundle of typed signals** (seed papers, followed authors, saved queries, behavior-derived signals, citation anchors, curated prose) that lenses interpret differently.
- arxiv-sanity's value lives in a session. Ours has to live across years — longitudinal memory of what was read, dismissed, returned to, cited, and disagreed-with is part of the platform, not a session log.
- arxiv-sanity is observational. Ours is **steerable** — the researcher selects between lenses, composes them, and inspects per-lens reasoning per recommendation.

## Load-bearing surface: the multi-lens substrate

The architecturally load-bearing claim of this platform is that *no single retrieval lens can serve practicing AI research*. AI research is intensely community-structured (specific labs, specific conferences, specific paper threads), methodologically diverse (RLHF vs DPO vs constitutional AI as distinct conversations, not a topic cluster), and rapidly paradigm-shifting (mechanistic interpretability papers are topically similar but methodologically diverse). Topic-cluster representation, semantic similarity, citation neighborhoods, author/affiliation signals, benchmark/dataset signals, and method-tag signals each surface different parts of the literature. The substrate exposes them as first-class lenses, not as fusion ingredients to be averaged.

Lens architecture must be validated by use, not by design — the abstraction is most likely to be right when *at least two* lenses are shipped against it. This is committed in ADR-0005.

## Research-practice operations served (beyond retrieval)

Retrieval is one operation among several. The platform aims to support:

- **Orientation** — give me the shape of a community I'm new to, the canonical works and the live debates.
- **Lineage tracking** — where did this idea come from; what cited what, what disagrees with what.
- **Dissent location** — papers that explicitly contest a position; alternative methodological camps.
- **Paradigm-shift detection** — what's recently broken from prior consensus; what's accumulated as anomaly.
- **Longitudinal memory** — what I cared about three weeks ago, three months ago, last year.
- **Steering** — pick a lens, narrow by another, intersect, surface disagreement-as-signal.
- **Per-recommendation explanation** — why this paper, by which lens, with what evidence, with what provenance.
- **Accountable-to-disagreement** — when I dismiss a recommendation, the disagreement enters the model.
- **Triage memory** — what I marked as cite-later vs read vs dismissed; what came back into relevance.

Some of these are v0.2 work (multi-lens, per-lens explanation, lens-disagreement). Some are post-v0.2 (longitudinal memory, accountable-to-disagreement, behavior-derived signals). The vision is what the long-arc tool serves; the roadmap stages it.

## Lens trajectory

| Lens | Status | Notes |
|---|---|---|
| Semantic (dense embedding) | committed (v0.1, refactored in v0.2) | Currently TF-IDF + lexical baseline; semantic-model selection is per-lens design, not winner-pick |
| Citation / community | committed (v0.2) | Highest-leverage AI-specific addition; OpenAlex-derived edges + co-citation neighborhoods |
| Author / affiliation | open — next candidate | Same data-integration shape as citation lens; lab-and-conference structure of AI research |
| Benchmark / dataset | open — next candidate | Uniquely AI-specific; Papers with Code as candidate source |
| Methodological | open — needs taxonomy work | Method-tag taxonomy: curated vs classifier; high leverage but harder |
| Temporal trajectory | speculative | Paradigm-shift detection; needs literature-grounded model of what counts as a trajectory |
| Behavior-derived | speculative | What I read, time-on-page, what I returned to; depends on longitudinal-memory infrastructure |

## Longitudinal-memory commitment

The platform's value compounds across sessions. State is durable, inspectable, and exportable. Reading history, triage decisions, profile evolution, dismissed recommendations, returned-to papers — all are part of the substrate, not session-bound. Longitudinal memory is what distinguishes a platform that serves a research practice from one that serves a session.

## Provenance and inspectability commitment

Every recommendation carries: which lens(es) surfaced it, what features matched, what evidence the rank rests on, where the underlying signals came from, and when they were captured. ADR-0003 commits this at the data-rights layer; the vision extends it to the recommendation layer. Inspectability is a precondition for trust calibration; trust calibration is a precondition for the platform mattering across years.

## Anti-vision — what we are not

- **Not a paper chatbot.** Conversation is not the product. Discovery and triage are.
- **Not a RAG wrapper.** RAG is one technique that may serve some operations; it is not the substrate's organizing principle.
- **Not a ranked-list-but-fancier.** Fusion-by-default would collapse multi-lens architecture back to single ranking. Fusion is one strategy among steering, intersection, lens-disagreement, and per-paper explanation — not the default.
- **Not arxiv-sanity-but-better.** The product overlap is real but the long-arc center of gravity is different (longitudinal memory, multi-lens steering, MCP-native operations).
- **Not a benchmark-leaderboard clone.** Not a winner-picker. ADR-0001 binds.
- **Not a generic discovery tool.** AI-research-specific signals (citation graph density, lab structure, benchmark-driven communities) are first-class. The tool is for arXiv AI-related topics; adjacent fields (AI-ethics, AI-philosophy) are served, but the vision is not field-general.
- **Not implicit-profile-learning without confirmation.** Behavior-derived signals enter the profile with explicit researcher acknowledgement, not silently.

## Audience grounding

**Primary:** AI / CS / ML researchers — graduate students, postdocs, industry researchers, professors. Practice characterized by daily-to-weekly arXiv engagement, citation-anchored writing, conference-cycle-bound reading, methodological-camp identification, and benchmark-structured discourse.

**Adjacent:** AI-ethics, AI-philosophy, philosophy-of-AI researchers — share AI's literature surface but with different selection criteria. Served by the AI-research lens trajectory; not the design center.

**Not the audience:** general humanities researchers, social-science researchers, biology/chemistry/physics researchers outside AI-adjacent subfields. Their practices are different enough (slower citation pace, different discursive structures, different community signals) that a tool optimized for AI research would serve them poorly. Future fork or sibling project, not v-anything of this one.

## Open vision questions

| Question | Why it matters |
|---|---|
| When does longitudinal memory become its own subsystem vs annotations on workflow state? | Determines whether v0.3+ adds memory-specific abstractions or extends the existing Phase 2 workflow primitives |
| What's the right MCP shape for lens-disagreement-as-signal? | Single tool with a `mode=disagreement` parameter, separate `lens_disagreement` tool, or composable filter operation — UX implication is significant |
| How should behavior-derived signals enter the profile without becoming silent defaults? | The MiniLM-as-silent-default lesson directly applies; capture mechanism must keep the researcher in the loop |
| What does multi-user / collaborative shape look like, if ever? | Currently single-user, MCP-native; collaborative use (shared profiles, lab-level lenses, citation-network-of-the-lab) is a future shape, not v-anything |
| Methodological lens taxonomy — curated vs classifier vs hybrid? | Affects whether a methodological lens is v0.3 or v0.4+ work |

## Reopen conditions

This document should be revised when:

1. **Audience identity changes** (e.g., the AI-research focus broadens or narrows materially).
2. **The multi-lens load-bearing claim is contradicted** — empirical evidence that one lens dominates research-practice value across users and operations.
3. **A research-practice operation we did not anticipate becomes load-bearing** — e.g., a lens type emerges that the current trajectory cannot accommodate.
4. **The longitudinal-memory commitment proves unviable** — operationally, ethically, or because it conflicts with how researchers actually use the tool.
5. **The "not arxiv-sanity-but-better" frame collapses** — i.e., we discover the long-arc tool *is* arxiv-sanity-but-better and the divergence claims were unwarranted.

Otherwise this document is canonical. It does not require rewriting on every roadmap revision.

---
*This vision is the post-2026-04-25 distillation of the multi-lens redirection deliberation. The deliberation captures the journey; this document captures the destination. Refer to LONG-ARC.md for the planning doctrine that disciplines current work to preserve this vision without overscoping into it.*
