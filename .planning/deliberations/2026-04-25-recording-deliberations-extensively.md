---
type: deliberation
status: policy articulated; being acted on
date: 2026-04-25
level: workflow / process / documentation policy
form: short meta-deliberation; self-referential
follow_through: being acted on now (this and sibling docs)
related:
  - 2026-04-25-long-arc-and-multi-lens-redirection.md
  - 2026-04-25-audience-reframe-arxiv-ai.md
  - 2026-04-25-pass-fail-vs-nuance-of-differences.md
  - 2026-04-25-mediation-vs-position-taking.md
  - 2026-04-25-load-bearing-assumptions-audit.md
  - 2026-04-25-pressure-artifacts-before-remedy.md
---

# Recording Deliberations Extensively

## What prompted this deliberation

After writing the multi-lens redirection handoff at `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md`, I had captured many of this session's methodological turns as compressed sections (e.g., a "Lessons learned" list with 9 items). The user pushed:

> "can we actually also record some of these deliberations extensively? and not just as small sections on a handout? including what prompted the deliberation, any open or next questions, whether this leads to some kind of concrete decision, whether it is something more at the workflow level, or at the design problem level (like X needs to be reopened), or whether we are now presented with an array of potential options etc. etc. etc., let the form of the deliberation doc fit the context of the deliberation and where it might lead to or did (many deliberations in this session I don't think were entirely followed through)"

The prompt names the failure of compressed-into-handoff capture: deliberations carry information in their *form* and their *follow-through history*, not just in their conclusion. A "Lessons learned" bullet point loses the prompt that triggered it, the alternatives that were surfaced, the partial follow-through, and the workflow-vs-design-level distinction.

## What the deliberation surfaced

### What a deliberation document needs to capture

For each substantive deliberation in a session:

- **What prompted it** — the specific intervention or observation that triggered the deliberation, ideally quoted.
- **What the deliberation surfaced** — the substantive content; alternatives considered; what was reframed or learned.
- **What was decided** — the concrete outcome, if any. Possibly:
  - A concrete decision (with named cells in a response space, named direction, etc.).
  - A workflow-level pattern or discipline.
  - A design-problem reopening (X needs to be reopened, Y needs to be redesigned).
  - An array of options without commitment yet.
  - A principle articulation that binds future work.
  - An open question that needs more work.
- **Open or next questions** — what remains undone, contestable, or pending.
- **Status of follow-through** — honest. *Many deliberations in this session were only partially followed through.* The honesty is more valuable than the optimistic version.
- **Workflow-level vs design-problem-level** — different deliberation types need different reader treatment. A workflow pattern can be referenced from any future work; a design-problem reopening only applies to its specific subject.

### Why form should fit context

A workflow-pattern articulation (e.g., "pressure the artifacts before adopting a remedy") can be a 400-word recipe. A design-direction redirection (e.g., the multi-lens redirection) needs narrative form, an explicit decision, options, open questions, and follow-through honesty — 1500+ words. A correction-to-framing (e.g., the audience reframe) sits in between. Forcing all deliberations into a single template loses information.

### What "fit-to-context" looks like in practice

Deliberation documents from this session:

| Doc | Form | Length | Why this form |
|---|---|---|---|
| Long-arc and multi-lens redirection | Long-form narrative | ~1500w | Most consequential; needs the journey, decision, options, open questions |
| Audience reframe | Medium-short | ~700w | Correction with substantive propagation; needs the prompt and the resulting reframe |
| Pass/fail vs nuance | Short principle | ~600w | Workflow pattern; reusable; partial follow-through worth flagging |
| Mediation vs position | Short principle | ~600w | Workflow pattern; sibling to the verdict-shaping pattern |
| Load-bearing assumptions audit | Short discipline | ~600w | Recipe-shaped; reusable |
| Pressure artifacts before remedy | Short workflow | ~600w | Workflow pattern; produced a substantive artifact this session |
| Recording deliberations extensively (this) | Short meta | ~500w | Self-referential; documents the policy itself |

### What this policy precludes

- **Storing deliberations only in conversation memory.** Conversation memory is lost at compaction. Deliberation documents are not.
- **Compressing deliberations into handoff sections.** The handoff is for orientation; deliberations are for trace integrity.
- **Forcing all deliberations into a single template.** Form follows substance; the substance varies.
- **Optimistic follow-through reporting.** If a deliberation was only partially followed through, the document says so. The pattern of partial follow-through is itself a finding worth recording.

## What was decided

**Policy (binds subsequent work):**

1. Substantive deliberations get their own documents in `.planning/deliberations/` with date-prefixed naming.
2. Each document captures: prompt, substance, outcome, open questions, follow-through honesty, and form notes.
3. Form fits context — workflow patterns are short and recipe-shaped; design redirections are long and narrative.
4. Compressed handoff sections are *secondary* documentation — they point to the deliberation documents, not replace them.
5. Partial follow-through is named explicitly; the pattern of partial follow-through is itself worth recording.

**Discoverability convention:** date-prefixed names for session-clustered deliberations. Existing deliberation files use descriptive slugs without date prefixes. Both conventions coexist; the date prefix helps when many deliberations cluster on one date (as this session did).

## Open questions

- **When does a methodological turn become a "deliberation worth its own document" vs. a passing observation?** Probably any time the turn produces: a workflow pattern, a principle articulation, a design redirection, an array-of-options, or a partial-follow-through worth flagging. Passing observations that don't bind future work don't need their own documents.
- **How to handle deliberations that span multiple sessions?** The current convention treats each document as standalone. A deliberation that continues in a future session could either get a new document (with reference to the prior) or update the existing one (with explicit dated additions, like the addendum pattern in `sequential-narrowing-anti-regret-and-spike-inference-limits.md`). Both are fine; the choice depends on whether the new work is continuation or revision.
- **Should there be an index?** Currently the deliberations folder has no index file. As the count grows, an index would help. For now, six new documents from this session is small enough that the directory listing serves.

## Status of follow-through

Being acted on now. This document and its six siblings are the act. Pattern-watch needed: the policy can drift back to compressed-handoff capture if not maintained. Future Claude reading the handoff should see references to the deliberation documents and use them as primary sources, not the handoff's compressed summaries.

## Workflow-level lesson

**Trace integrity is its own deliverable.** The compressed-handoff-section approach optimized for orientation at the cost of journey-preservation. Deliberation documents preserve the journey: the prompt, the alternatives, the resulting commitment (if any), and the honest follow-through. That information has value beyond the deliberation's specific conclusion.

## Form notes

This document is self-referential: it both states the policy and is produced by the policy. The brevity matches the policy's claim that workflow articulations should be short. Deliberation documents that follow this policy in subsequent sessions should pattern-match this form, but should not be constrained by it where the substance demands a different form.
