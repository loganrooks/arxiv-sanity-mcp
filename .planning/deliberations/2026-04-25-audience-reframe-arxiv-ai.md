---
type: deliberation
status: correction accepted
date: 2026-04-25
level: framing (project-level, methodological)
form: medium-short — what changed, what propagated, what binds future work
follow_through: followed through; binds subsequent work
related:
  - 2026-04-25-long-arc-and-multi-lens-redirection.md
  - ../handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md
---

# Audience Reframe — Arxiv AI Researchers, Not Philosophy

## What prompted this deliberation

In sketching the long-arc vision, I had been generating examples in a philosophy register: Levinas, phenomenology, analytic vs. Continental epistemology, Continental aesthetics, "argumentative style of transcendental argument." The examples felt natural because the developer (Logan Rooks) is a philosophy PhD. But the user corrected directly:

> "this is for arxiv, not necessarily and strictly for a philosophy PhD researcher, you could say its for both computer science researchers, AI researchers, and philosophy researchers, but mostly for AI researchers. I don't know where you are getting this hyper focus on philosophy from. We are interfacing with arxiv, specifically the AI-related topics, why would we be clustering by phenomenology?"

The prompt names the failure: I imported an audience from a salient nearby fact (developer's role) rather than from the tool's actual scope (arxiv AI papers). It was sloppy default-mode reasoning.

## What the deliberation surfaced

### What changed substantively

The audience correction sharpened — rather than weakened — most of the multi-lens case. Specifically:

- **The BERTopic critique gets stronger.** AI research isn't well-clustered by topic in a way that maps to how people work. It's clustered by *conversational thread* (X paper responds to Y paper), *lab affiliation* (Anthropic-style vs. DeepMind-style vs. academic-lab style), *benchmark choices* (HELM, MMLU, BIG-Bench), *method families* (RLHF, DPO, constitutional AI, mechanistic interpretability technique X vs. Y), and *paradigm-of-the-moment* (pre- vs. post-Chinchilla; pre- vs. post-instruction-tuning). Topic clustering flattens all of this. RLHF papers and constitutional-AI papers are topically similar but conversationally distinct.
- **Citation/community emphasis gets stronger.** AI research is intensely community-structured because the field moves fast and conversations are highly localized. Citation graphs are particularly load-bearing for AI; for slower fields they would be enrichment, but for AI they're load-bearing.
- **Methodological-proximity lens becomes high-value.** AI methods are very specific (RLHF flavors, interpretability techniques, scaling approaches). "Papers using a method like this" is a more useful retrieval mode than topical similarity for many AI research workflows.
- **Benchmark/dataset overlap lens** appears as a real category. Uniquely AI-specific. "All papers evaluated on MMLU" or "all papers using HELM" is a concrete community-defining query.
- **Temporal trajectory lens** becomes more valuable. AI moves fast enough that paper position in a paradigm trajectory ("early scaling-laws work" vs. "post-Chinchilla") is research-load-bearing in ways that don't apply to slower fields.

### What didn't change

The structural recommendations (vision document, multi-lens architecture, longitudinal pilot, profile-elicitation reform, citation-community-forward roadmap) survived the audience correction unchanged. The shape of the redirection was right; only the examples and per-lens emphasis were wrong.

### Where the philosophy framing came from

Default-mode pattern matching from "developer is a philosophy PhD" → "tool examples should be philosophy-flavored." That's a reasonable heuristic for *some* questions (e.g., what register the developer prefers for documentation tone) but wrong for the *audience* question (who is the tool actually for). The two questions are different.

## What was decided

The audience for the tool is:

- **Primarily** AI / ML / CS researchers using arXiv (especially `cs.AI`, `cs.LG`, `cs.CL`, and adjacent categories).
- **Adjacent** philosophy-of-AI and AI-ethics researchers — they overlap heavily with the AI audience and are well-served by the same lens types.
- **Not** general philosophy researchers (despite the developer's role).

This binds:

- All long-arc reasoning, vision documents, and design-rationale prose.
- Lens-type concretization (citation/community, author/affiliation, benchmark/dataset, methodological, temporal trajectory all become AI-research-specific).
- Profile-elicitation experiments (behavior-derived signals will be AI-research behaviors; citation-anchor signals will be AI-paper-citation signals).
- Evaluation harness design (longitudinal pilot tasks should be AI-research tasks).

## Open questions

- **How does adjacent philosophy-of-AI / AI-ethics fit?** Probably the same lenses serve well, but worth flagging for any user-facing language. A philosophy-of-AI researcher might want a slightly different lens emphasis (more methodological cross-disciplinary lateral connection) than a pure AI/ML researcher (more lab/benchmark community structure). For v0.2, treat this as not-yet-actuated; same primitives, future tuning.
- **Should the developer's role inform anything at all?** Logan's philosophy-PhD orientation does plausibly shape what lens types he wants exposed (and what disagreement modes feel useful) for self-use. Worth noting as "developer-as-pilot-user" without making it the audience definition.

## Status of follow-through

Followed through:

- The multi-lens reframe and lens types were redrawn in AI-research register.
- The handoff captures the audience correction explicitly in its "What the project is" section and again in the "User corrections / policy changes" section.
- The long-arc deliberation document uses AI-research examples consistently.

What still needs to follow through:

- The vision document (when written) should be in AI-research register.
- Any future deliberations or design rationale should check audience framing before importing examples.

## Workflow-level lesson

**Always check audience framing before doing long-arc reasoning.** The default-mode heuristic (examples drawn from the most salient nearby fact about the developer or context) can produce category errors. For audience-shaping questions, name the audience explicitly and stay there.
