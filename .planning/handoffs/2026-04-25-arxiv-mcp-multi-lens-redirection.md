---
type: context-handoff
status: active
date: 2026-04-25
purpose: |
  Self-contained handoff after a long methodology-audit conversation. Future Claude
  reading this should be able to resume work cold, with no conversation memory,
  knowing what is decided, what is open, what was learned, and what to do next.
  This handoff replaces the conversation history; do not assume anything in chat memory.
audience: Future Claude (or human reader) with no conversation context
read_first_after_this: see "Files to reopen first" section
---

# Arxiv-Sanity-MCP Multi-Lens Redirection — Context Handoff

## TL;DR

The arxiv-sanity-mcp project is at an inflection. v0.1 shipped (31/31 plans, MCP server with 10 tools, 403 tests passing). Post-v0.1, a four-spike research suite (005-008) was designed to inform v0.2's embedding-model architecture commitment. Through about two weeks of methodology-audit work — a deliberation, a review of the deliberation, an addendum reframing the response space dimensionally, a pressure pass on the suite handoffs, and a paired AI review (cross-vendor + Opus adversarial) of the pressure pass — we discovered that the spike program had quietly drifted away from ADR-0001's multi-lens commitment and into tournament-style narrowing. **Decision (user-confirmed 2026-04-25): redirect v0.2 from "pick the best embedding-model stack" to "ship a multi-lens MCP substrate with at least two lenses (existing semantic + new citation/community)."**

The immediate next concrete action is a **Property audit of the Phase 3 (interest modeling) implementation** to determine how lens-extensible the existing primitive is — that audit gates the roadmap commit between three options. After that: vision document, roadmap commit, v0.2 plan.

## Why this handoff exists

The conversation that produced this redirection accumulated significant context. Rather than carry that into the next session and risk losing it to compaction, this handoff captures:

1. The journey (twists and turns) so future-self knows how we got here.
2. What was decided, what is open, what is parked.
3. The lessons learned and mistakes not to repeat.
4. The immediate next action plus short / medium / long-term horizons.
5. Distinctions that must not flatten in summary (decided vs. open, active vs. parked, etc.).

After reading this handoff and the files in "Files to reopen first," future Claude should be able to continue without needing the prior conversation.

## What the project is

**Project:** `arxiv-sanity-mcp` — an MCP-native research discovery substrate inspired by arxiv-sanity. Goal: help researchers and agents discover, monitor, and triage arXiv papers through MCP tools, resources, and prompts. Not a "chat with papers" wrapper.

**Audience:** AI / CS / ML researchers primarily. Adjacent use by philosophy-of-AI and AI-ethics researchers. **Not** general philosophy researchers, despite the developer (Logan Rooks) being a philosophy PhD. The tool is for arXiv AI-related topics.

**Status:** v0.1 complete and frozen (2026-03-14). 11 phases, 31 plans, 403 tests. Currently in post-v0.1 inter-milestone exploration. v0.2 milestone definition is the active work.

**Working directory:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp/`

## Active control surface

- **Project root:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp/`
- **Branch:** `spike/001-volume-filtering` (the branch name is misleading — work has gone far beyond volume filtering; this is just the active branch)
- **Main branch:** `main`
- **Worktrees:** None in use.
- **Parallel workers:** None.
- **Latest committed checkpoint:** `8aafb4a docs(deliberation): record spike narrowing critique` (2026-04-25 morning, before paired-review work)
- **Significant uncommitted state:** Yes. See "Uncommitted files" section. The handoff and recent reviews are all uncommitted.

## Files to reopen first (in order)

After this handoff, future Claude should read in order:

1. `CLAUDE.md` — project rules and architectural constraints. Read first; it is binding.
2. `.planning/STATE.md` — project status (v0.1 frozen, in inter-milestone exploration).
3. `docs/adrs/0001-exploration-first-architecture.md` — the load-bearing ADR. Multi-lens coexistence is its core commitment. Recently re-prioritized as binding for v0.2 implementation, not just design.
4. **`.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md`** — the load-bearing design-direction deliberation from this session. Read this for the substantive redirection; the handoff sections are summaries of it.
5. `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` — the most recent methodology summary, including the layered "After the paired review" section appended 2026-04-25.
6. `.planning/deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md` — the deliberation with its addendum on the dimensional response space.
7. `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md` — paired-review evidence (same-vendor adversarial; caught register and rhetorical inflation).
8. `.planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md` — paired-review evidence (cross-vendor independent reading; caught substance and convergent fact about suite-contract tiebreaker).
9. `.planning/spikes/004-embedding-model-evaluation/OPEN-QUESTIONS.md` — surfaced the deeper substrate questions (MiniLM-entanglement, seed sensitivity, no human evaluation) that originally motivated 005-008.
10. `.planning/spikes/NEXT-ROUND-SUITE.md` — the current spike contract. Being effectively superseded by the multi-lens redirection.
11. `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md` — designed but not run. In flux per the redirection.
12. `.planning/deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md` — independent review of the deliberation, lodged before this round of work began.

The other six session deliberation documents (workflow patterns and principles) are listed below in "Session deliberation documents" — read those when the workflow patterns are relevant to subsequent work.

## Session deliberation documents (2026-04-25)

These were written after this handoff to record this session's deliberations extensively, with form fitting context. They are primary sources; the handoff's "Lessons learned" and journey sections are summaries of them.

| Document | Type | Form | Status |
|---|---|---|---|
| [`2026-04-25-long-arc-and-multi-lens-redirection.md`](../deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md) | design-direction | long-form narrative | decided — implementation open |
| [`2026-04-25-audience-reframe-arxiv-ai.md`](../deliberations/2026-04-25-audience-reframe-arxiv-ai.md) | framing correction | medium-short | followed through |
| [`2026-04-25-pass-fail-vs-nuance-of-differences.md`](../deliberations/2026-04-25-pass-fail-vs-nuance-of-differences.md) | workflow / writing posture | short principle | PARTIAL — pattern recurring |
| [`2026-04-25-mediation-vs-position-taking.md`](../deliberations/2026-04-25-mediation-vs-position-taking.md) | workflow / writing posture | short principle | PARTIAL — required re-prompting |
| [`2026-04-25-load-bearing-assumptions-audit.md`](../deliberations/2026-04-25-load-bearing-assumptions-audit.md) | workflow / discipline | short reusable recipe | followed through |
| [`2026-04-25-pressure-artifacts-before-remedy.md`](../deliberations/2026-04-25-pressure-artifacts-before-remedy.md) | workflow / methodology | short workflow | followed through |
| [`2026-04-25-recording-deliberations-extensively.md`](../deliberations/2026-04-25-recording-deliberations-extensively.md) | meta / process policy | short meta | being acted on |

Three of the seven (pass/fail vs nuance, mediation vs position-taking, recording-deliberations-extensively) name patterns where follow-through was partial or where the pattern recurs. Future Claude should pattern-watch for these across subsequent work — the closure-pressure family of failures is the underlying concern, and it recurs at every layer.

Optionally, also useful:

- `.planning/foundation-audit/FINDINGS.md` — earlier project-level audit work; methodology context.
- `.planning/spikes/METHODOLOGY.md` — spike-program methodology principles.
- `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md` — explicit norms (no winner-crowning, no binary verdicts).

## Recent journey — the twists and turns

Approximately:

1. **v0.1 shipped (2026-03-14).** 11 phases, 31 plans. Working tool with one retrieval lens (`MiniLM + TF-IDF`-style) over BERTopic-derived interest profiles.
2. **Spikes 001-004 (early-to-mid 2026).** Evaluated stack candidates. Spike 004 specifically evaluated embedding models against MiniLM + 5 challengers (`SPECTER2`, `Voyage`, `GTE`, `Qwen3`, `Stella`), producing a "signal axes" story.
3. **`004/OPEN-QUESTIONS.md` (2026-03-29)** surfaced deep gaps in the evaluation framework: A1 no human evaluation; A2 profiles MiniLM-entangled (built from MiniLM BERTopic clusters in Spike 001); A3 seed sensitivity discovered post-hoc; B1 only centroid retrieval tested; etc. These were named as the highest-priority gaps before any v0.2 architecture choice.
4. **`NEXT-ROUND-SUITE.md` (2026-03-30)** designed Spikes 005-008 to address those gaps in sequence: 005 → A2 (profile-construction family robustness); 006 → B1 (retrieval geometry); 007 → mechanism probes; 008 → A1 (function-in-use with human adjudication).
5. **005-007 ran (Apr 2026).** Each produced narrowing decisions. 005 carried `MiniLM-saved` as incumbent + `category + lexical` as alternative; 006 narrowed to four families; 007 narrowed to `SPECTER2` + `Voyage`, deferring `Stella`.
6. **Deliberation `sequential-narrowing-anti-regret-and-spike-inference-limits.md` (2026-04-16).** Logan raised the question of whether the narrowing chain was over-closing. Original recommendation: Option C — keep narrowing, add a "challenge surface" section to handoffs.
7. **Independent review of the deliberation (2026-04-25 morning).** Critiqued the deliberation: option space was constructed; "challenge surface" is documentation not mechanism; philosophy mobilised as atmospherics; deliberation didn't apply its own discipline to itself; "anti-regret" did unexamined work; no concrete failure mode anchored the analysis. Proposed a richer remedy set.
8. **Addendum to the deliberation (2026-04-25 mid-day).** Reframed the post-pressure-pass response space as a 4-dimensional matrix: Subject × Nature × Trigger × Scope. Decided to pressure-test the artifacts before adopting any remedy.
9. **Pressure pass on handoff artifacts (2026-04-25 afternoon).** Read-and-annotate audit of `005`/`006`/`007` `HANDOFF.md` + `NEXT-ROUND-SUITE.md` + `008/DESIGN.md`. Produced 7 findings; flagged Findings 1 and 2 as the most contestable (framing claims).
10. **Paired AI review (2026-04-25 evening).** Cross-vendor (GPT-5.5 via codex CLI, xhigh reasoning effort) + Opus adversarial (fresh Claude session, xhigh effort). Two independent readings. Both converged on a key factual error in the pressure pass (the suite contract `NEXT-ROUND-SUITE.md:65-69` *does* pre-register a `007 → 008` ranking putting complementarity #1, mechanism #2; the pressure pass claimed it was "not pre-registered"). Both pushed back on rhetorical inflation, prescriptive consequences, "single decision excluding Stella" framing. Cross-vendor: Findings 1-2 survive with qualifications. Opus adversarial: Finding 1 doesn't survive as written, sharper finding survives inside; Finding 2 partially retracts (chain-wide claim self-contradicted by pressure pass's own treatment of 006 as honest deferral).
11. **"After the paired review" section appended to the pressure pass (2026-04-25).** Captured the convergent fact, the multiple defensible readings, the divergent diagnostic styles, and self-application of the closure-pressure pattern at the audit layer.
12. **Operationalization audit and walkback (2026-04-25 late evening).** Walked back six recommendations to three concrete actions (007 override annotation; 008 asymmetric-comparison-surface fix; MiniLM-profile-family decision). Surfaced load-bearing assumptions per recommendation; honestly flagged where confidence was lower than the prescriptive language implied.
13. **Audience correction (2026-04-25, late).** Logan corrected: the tool is for AI researchers primarily, not philosophy researchers. The long-arc vision examples I'd been generating (Levinas, phenomenology, Continental aesthetics) were misframed.
14. **Multi-lens reframe (2026-04-25, latest).** With the audience corrected, the BERTopic critique gets stronger (AI research isn't well-clustered by topic — it's clustered by lab, benchmark, paradigm-of-the-moment). Citation/community emphasis gets stronger. Concrete lens types nameable. ADR-0001's "multiple retrieval/ranking strategies must coexist" was being violated by the spike program's tournament framing. Logan confirmed: redirect to multi-lens. Don't worry about cost of redirection — we haven't built much (the redirection is methodological, not engineering — v0.1 stays).

## Lessons learned (mistakes not to repeat)

- **Closure-pressure recurs at every layer.** The methodology-audit work itself exhibited the same closure pressure it diagnosed in the spike program. The pattern: persuasive framing in lieu of argument; prescriptive remedies overrunning their diagnostic grounds; calibrated language reserved for closing footnotes rather than running through prose. Watch for this; flag it explicitly when it appears.
- **Single-author framing claims are unreliable.** The pressure pass had a factual error (claimed the tiebreaker was "not pre-registered" when it was) and rhetorical inflation. Both were caught only by paired AI review. For framing claims about codebase or methodology, single-reader output should not drive remedies without independent challenge.
- **Cross-vendor catches substance; same-vendor catches register.** Different review pairs catch different failures. For methodology audits, both are useful. Cross-vendor (GPT-class) is more accommodating and reads carefully against the artifacts; same-vendor (Opus) is more critical of internal rhetorical patterns.
- **"I cannot run /gsd-review" is not the same as "I cannot dispatch cross-vendor reviews."** Slash commands are user-only; tooling (codex CLI, Agent tool with model override) is dispatchable by Claude via Bash and Agent. Don't conflate them.
- **`/gsd-review` is GSD-phase-shaped, not spike-shaped.** For spike-methodology audits, dispatch directly via Bash + codex (cross-vendor) and Agent + Opus (same-vendor adversarial). Reasoning effort `xhigh` justified for framing-claim audits.
- **Audience matters in vision-articulation work.** Importing default-mode philosophy examples was a sloppy mistake driven by Logan's role rather than the tool's audience. Always check audience framing before doing long-arc reasoning. The tool is for AI researchers; reason in that register.
- **Tournament narrowing violates ADR-0001.** Even when narrowing looks "disciplined," it's not the same as multi-lens architecture. ADR-0001's "multiple retrieval/ranking strategies must coexist" is binding. Spike programs that narrow toward a winner — however carefully — are quietly violating the ADR.
- **The BERTopic profile primitive is lossy for AI research.** Topic clusters don't capture lab affiliations, conversational threads, benchmark choices, method families, or paradigm trajectories. Generalize the primitive to a "bundle of signals" rather than picking a successor cluster method. Don't tear up; augment.
- **MiniLM as silent default is the deeper issue beneath 005's findings.** Spike 005 partially de-MiniLM-ified by carrying `category + lexical` profiles, but `MiniLM-saved` remained the incumbent reference. The MiniLM-entanglement was attenuated, not removed. This concern, identified in `004/OPEN-QUESTIONS.md` A2, has been carried forward by inertia rather than questioned at the root.
- **Stop framing things as pass/fail verdicts.** The two reviewers did not produce verdicts on the pressure pass. They produced two readings whose differences carry information. Mediating-and-synthesizing for its own sake is its own form of unhelpful. Take a position with reasoning; preserve plurality where it's load-bearing; don't false-balance.

## Current state distinctions

### Decided (canon — pre-existing ADRs)

- **ADR-0001:** exploration-first multi-lens architecture. Multiple retrieval/ranking strategies must coexist. Interest state is not reduced to tags. Unresolved questions stay documented. **Now binding for v0.2 implementation, not just design.**
- **ADR-0002:** metadata-first, lazy enrichment.
- **ADR-0003:** license and provenance first. Track provenance for all content and ranking signals.
- **ADR-0004:** MCP as workflow substrate. Design for agent workflows (collections, saved queries, triage state).

### Decided (this redirection — user-confirmed 2026-04-25)

- **v0.2 will be multi-lens.** ADR-0001 honored in implementation, not just design.
- **Citation/community lens is the load-bearing v0.2 addition** (the second lens beyond existing semantic). Reasons: AI research is intensely community-structured; citation graphs are particularly load-bearing for AI; this is the highest-leverage AI-specific addition the spike program neglected.
- **BERTopic profile primitive will be generalized to bundle-of-signals**, not replaced. BERTopic stays as one signal among many; behavior-derived, citation-anchor-derived, and researcher-curated-prose signals can be added in parallel without breaking changes.
- **Spike 008 will not run as a tournament.** It will be reshaped (or replaced) as part of a longitudinal pilot using multi-lens MCP. Decision deferred pending vision document.
- **Cost of redirection is acceptable.** No code is being torn up; the redirection is methodological. Plan to do it properly.

### Active (currently being worked on)

- **The multi-lens redirection** (this conversation's outcome). Pending Property audit + vision document.
- **This handoff document** (just written; uncommitted).

### Open (not decided, awaiting work)

- **Property audit of Phase 3 implementation.** Highest-leverage open item. Three properties:
  1. Is the existing interest-profile primitive lens-extensible (bundle-of-signals shape) or BERTopic-coupled?
  2. Are MCP tool signatures lens-aware (accept a `strategy=` parameter or equivalent), or do they assume single-lens?
  3. Is storage committed to one similarity type, or already abstracted per-lens?
- **Vision document.** ≤2-page constraint-articulation of what the tool should be in 5 years for an AI researcher. Iteratable; rewrite every 6 months.
- **Roadmap commit (Option A vs B vs C).** Depends on Property audit results.
  - Option A — full multi-lens substrate in v0.2 (3-4 months engineering + spike work).
  - Option B — refactor + ship two lenses (semantic + citation/community) (~2 months).
  - Option C — refactor for extensibility, ship one lens, multi-lens validated in v0.3 (~1 month).
  - Default lean: **B**, contingent on audit.
- **Per-lens design decisions.** See "Multi-lens design" section below for which lenses need spikes vs not.
- **Combination strategy.** Steering, fusion, intersection, disagreement, per-paper explanation. Multiple modes. To be designed.
- **`008` fate.** Reshape as longitudinal pilot, shelve, or run for partial signal. Pending vision document outcome.
- **Profile-elicitation alternatives.** Behavior-derived, citation-anchor-derived, researcher-curated prose. Spike value high, not yet planned.
- **Phase ordering.** Should Phase 6 (content normalization) and citation-graph data integration be pulled forward to v0.2? Likely yes given multi-lens commit; needs explicit decision.
- **Which lens after citation/community?** Methodological lens has high AI-research leverage; benchmark/dataset lens is uniquely AI-specific. Either could be next. Open.

### Parked (not active, not killed)

- **Tournament-style narrowing of embedding models.** Not abandoned (still useful for *one* lens — the semantic one), but no longer load-bearing for v0.2 architecture commitment.
- **005's `SPECTER2`-refined profile-construction family.** Was cost-deferred at 005; remains an open question for whether to revive in profile-elicitation spike.
- **MMR alternative retrieval geometry.** Cost-deferred at 006; remains open.
- **`Qwen3` challenger.** Dropped at 006; remains dropped unless multi-lens framing changes the case for it.
- **The original pressure pass's larger remedies** (split `008`, widen `008`, retroactively patch `005`/`006`/`007` more broadly). Don't actuate; they were overreach per the paired review.
- **Findings 5 and 7 from the original pressure pass** (Qwen3 chain dependency; "narrow-at-each-step" pathologization). Touched by the adversarial overstep audit; should be re-examined when revisiting that pass, but not via self-review (which doesn't work for contestable framings).

### Repo-local evidence

- All artifacts under `.planning/` and `docs/`.
- The two AI-generated reviews (cross-vendor + Opus adversarial) — written 2026-04-25, uncommitted. They contain specific textual citations to the spike artifacts; reading them is faster than re-reading all the spike artifacts to reach the same conclusions.

### Upstream / external evidence (not yet integrated)

- Logan's behavioral history in the tool. Not currently captured. Would feed a behavior-derived profile signal.
- Citation graphs (Semantic Scholar API, OpenAlex). Not yet integrated. Required for citation/community lens.
- Benchmark metadata (Papers with Code). Not yet integrated. Required for benchmark/dataset lens.
- Author/affiliation metadata. Partially in arxiv metadata; richer in Semantic Scholar / OpenAlex.

### Current task vs deferred follow-up

- **Current task:** Property audit of Phase 3 implementation.
- **Deferred (after Property audit):** Vision document.
- **Deferred (after vision):** Roadmap commit + v0.2 plan + `008` fate decision + 007 override annotation.

### Committed vs uncommitted

**Committed up to:** `8aafb4a docs(deliberation): record spike narrowing critique` (the last commit before this round of audit work).

**Uncommitted (session of 2026-04-25):**

Modified:

- `.planning/config.json` — pre-existing modification, not from this session, scope unknown.
- `.planning/deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md` — addendum and review-status section appended.
- `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` — layered "After the paired review" section appended.

New:

- `.planning/deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md` — independent review of the deliberation.
- `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` — the pressure pass itself (initial creation in this session).
- `.planning/spikes/reviews/2026-04-25-paired-review-package/README.md` — paired-review package readme.
- `.planning/spikes/reviews/2026-04-25-paired-review-package/cross-vendor-prompt.md` — cross-vendor reviewer prompt.
- `.planning/spikes/reviews/2026-04-25-paired-review-package/opus-adversarial-prompt.md` — Opus adversarial reviewer prompt.
- `.planning/spikes/reviews/2026-04-25-paired-review-package/artifacts-index.md` — paths index for paired-review.
- `.planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md` — AI-generated, two-phase cross-vendor review output.
- `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md` — AI-generated, Opus adversarial review output.
- `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md` — this file.
- `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md` — design-direction deliberation (the load-bearing one).
- `.planning/deliberations/2026-04-25-audience-reframe-arxiv-ai.md` — framing-correction deliberation.
- `.planning/deliberations/2026-04-25-pass-fail-vs-nuance-of-differences.md` — workflow-pattern deliberation (partial follow-through).
- `.planning/deliberations/2026-04-25-mediation-vs-position-taking.md` — workflow-pattern deliberation (partial follow-through).
- `.planning/deliberations/2026-04-25-load-bearing-assumptions-audit.md` — discipline deliberation (reusable).
- `.planning/deliberations/2026-04-25-pressure-artifacts-before-remedy.md` — workflow-pattern deliberation.
- `.planning/deliberations/2026-04-25-recording-deliberations-extensively.md` — meta-deliberation (this policy).

Pre-existing untracked, scope unknown:

- `.planning/measurement/` — untracked, not from this session.

**Recommended commit grouping (when ready):**

1. The deliberation review + addendum (the methodology-meta work pre-paired-review).
2. The paired review package + the two AI-generated reviews + the layered post-review section (the paired-review work).
3. The seven session deliberation documents (the extensive-recording policy applied to this session's deliberations).
4. This handoff (separately, marking the redirection inflection).

But the user has not asked for a commit; do not commit without explicit instruction.

### This worktree's scope vs parallel workers

- **This worktree:** the only active worktree. Branch `spike/001-volume-filtering`.
- **No parallel workers.**
- **No worktrees in use.**
- **No GitHub PRs in flight** for the redirection work.

## Multi-lens design — extensibility, combination, lens-specific decisions

### Extensibility pattern

- A `Lens` interface: `query(seed_or_profile, options) → ranked_results_with_provenance`.
- Each lens is a registered implementation (plugin pattern or module-level registry).
- Storage abstracted per-lens. Some need vector index (semantic), some need graph (citation), some need relational queries (benchmark, author).
- Common result schema: paper IDs + per-lens scores + per-lens explanations + provenance fields.
- MCP surface exposes lens choice as a parameter (`strategy=` or equivalent); default to "all available" or a configurable preferred set.

Adding a new lens later becomes: implement the interface, register the lens, optionally add backing storage. No changes to consumers if the abstraction is right. The abstraction is most likely to be right if it is **validated by shipping at least two lenses** — which is why Option B (ship two lenses in v0.2) is preferred over Option C (design only, ship one lens).

### Combination strategies (fusion and otherwise)

Listed in order of likely usefulness for a research tool, not order of complexity:

1. **Steering (no fusion).** User picks a lens; gets that lens's results. Most direct honoring of ADR-0001. Different MCP tools per lens, or one tool with a `lens=` parameter.
2. **Lens disagreement as signal.** "Papers in lens A but NOT in lens B." Surfaces lens-specific findings. Particularly valuable for AI research — surfaces what one community knows that another doesn't.
3. **Set intersection / union.** "Papers in lens A AND lens B" (narrows) or OR (widens). User-driven AND/OR composition.
4. **Per-paper explanation.** Show *why* this paper appears: which lens(es), what scores, what features matched. Inspectable by design (matches ADR-0003).
5. **Reciprocal rank fusion (RRF).** Simple, parameter-free fusion when fusion is needed. First choice for fusion experiments.
6. **Borda count / weighted sum.** Risky across lens types (score scales aren't comparable). Not first-choice.
7. **Learning-to-rank fusion.** Heavyweight; needs labeled data. Defer.

The **non-fusion alternatives** (steering, disagreement, intersection, explanation) are arguably more interesting than fusion for a research tool. Fusion is a UI shortcut; the others are research-practice operations. Treating fusion as one option among several rather than the default avoids collapsing multi-lens architecture back into "ranked-list-but-fancier."

### Per-lens decision-making — do we need spikes?

Differentiated by whether the lens depends on a **modeling** choice or a **data integration** problem.

| Lens | Spike needed? | Reason |
|---|---|---|
| Topical (TF-IDF/BM25) | No | Well-understood; implement and check |
| Semantic (dense embedding) | Yes (already happening) | Modeling choice; this is what 005-008 has been doing; reframe from tournament to lens-design |
| Citation/community | Light | Data-integration choice (Semantic Scholar vs OpenAlex; freshness; coverage). Retrieval logic is graph traversal — well-known |
| Author/affiliation | Light | Same shape as citation |
| Benchmark/dataset | Light | Source choice (Papers with Code as default), coverage, freshness |
| Methodological | Yes | Needs a method-tag taxonomy; classifier vs curated taxonomy is genuinely contested |
| Temporal trajectory | Yes | Needs a model of what counts as a paradigm trajectory; non-trivial; recent literature on paradigm-detection in ML may apply |

**Spikes are warranted where the lens depends on a modeling choice. Unnecessary where the lens is a data-integration problem with well-understood retrieval logic.**

For v0.2: citation/community needs only a light data-integration spike (or none, if existing AI engineers can pick a source confidently). The semantic lens spike work (005-008) continues but reframes from tournament to lens-design. Methodological and temporal lenses are v0.3+ work.

## What `008` once run would tell us — given the redirection

`008` was designed for a tournament that picks a winner among the carried challengers. With the multi-lens reframe, the tournament question is dissolved.

**Still useful from `008`:**

- Whether function-in-use evaluation can be done at all with the current task harness (yes/no on the methodology).
- Whether the human adjudication apparatus produces stable judgments.
- Whether `SPECTER2` and `Voyage` produce noticeable function-in-use differences from the incumbent semantic lens — even with no winner picked.

**No longer load-bearing:**

- The "winner" verdict.
- The "two challengers + incumbent" structure as evidence for v0.2 architecture commitment.
- The narrowing decisions inherited from `007`.

**Honest verdict:** `008` as designed is not the right experiment for the multi-lens direction. It would tell us something about the methodology and the existing semantic lens, but not what we need for v0.2 architecture. Either reshape (a longitudinal pilot using 2-4 lenses) or shelve. The 007 override annotation and 008 spec asymmetry fixes still apply *if* `008` runs in any form, but `008` itself is not the load-bearing v0.2 input anymore.

## Horizons

### Immediate next action

**Property audit of Phase 3 (interest modeling) implementation.** Read the existing code; answer the three properties:

1. Is the profile primitive lens-extensible (bundle-of-signals shape) or BERTopic-coupled?
2. Are MCP tool signatures lens-aware (accept a `strategy=` parameter), or do they assume single-lens?
3. Is storage committed to one similarity type, or already abstracted per-lens?

Cost: ~half a day. Outcome: gates the Option A/B/C roadmap decision.

**How to do it:** read the source for the interest-modeling primitive (probably `arxiv_sanity_mcp/interest/` or similar); read the MCP tool signatures (probably `arxiv_sanity_mcp/mcp/` or `arxiv_sanity_mcp/server/`); read the storage layer for retrieval. Produce a short audit memo with the three property answers and a recommendation for Option A/B/C.

### Short-term (next 1-2 weeks)

1. Property audit completed.
2. Vision document drafted (≤2-page constraint-articulation; AI-research register; iteratable). Logan probably best to draft first cut.
3. Roadmap commit (Option B preferred; A or C contingent on audit).
4. v0.2 plan: refactor primitives to bundle-of-signals + `RetrievalStrategy` abstraction + ship existing semantic lens + add citation/community lens + longitudinal-pilot harness.
5. `008` fate decided: reshape as longitudinal pilot, or shelve.
6. `007` override annotation appended (small upstream housekeeping).

### Medium-term (v0.2 milestone)

- Multi-lens MCP substrate shipped with semantic + citation/community lenses.
- Profile primitive generalized to bundle-of-signals.
- Longitudinal pilot running with one user (Logan).
- Lens-disagreement and intersection MCP tools exposed.
- Per-paper provenance inspectable.
- ADR-0001 honored in implementation.

### Long-term (v0.3+)

- Additional lenses: author/affiliation, benchmark/dataset, methodological, temporal trajectory.
- Profile-elicitation alternatives spike (behavior-derived, citation-anchor-derived, researcher-curated prose).
- Fusion experiments where fusion is warranted.
- Real-user pilot beyond Logan.
- Phase ordering possibly revised: Phase 6 content normalization may have moved forward into v0.2 to support citation/community data integration.

## Open questions and unresolved blockers

- **Phase 3 lens-coupling.** Property audit answers this. Until then the roadmap commit is hand-waving.
- **Which lens is second in v0.2** if Option B is taken — citation/community (current default) or methodological (also high-leverage)? Default citation/community because the data integration is well-defined; methodological needs taxonomy work first.
- **Phase ordering.** Whether Phase 6 (content normalization) and citation-graph integration should be pulled into v0.2, or whether the citation lens can be added with minimal Phase 6 work.
- **Vision document scope.** Constraint-articulation vs blueprint. Constraint preferred. ≤2 pages. Iteratable.
- **`008` reshape vs shelve.** Depends on vision document and pilot harness design.
- **Profile-elicitation alternatives spike timing.** Before or after v0.2 ships? Likely after, because v0.2's bundle-of-signals primitive will be informed by what other signals look like — but a small upfront spike could de-risk the abstraction.
- **MiniLM-entanglement remediation.** 005 partially addressed this; it has been carried forward by inertia. The bundle-of-signals primitive lets us add non-MiniLM-derived signals without breaking; the question is which to add first and when.

## User corrections / policy changes (this session)

These should bind subsequent work:

1. **Stop framing things as pass/fail verdicts.** Think about what nuances of differences demand. Two reviews that disagree carry information; don't reduce to a verdict.
2. **Reviews wrote their own outputs.** Don't re-record their content; record dispatch and reflect on differences.
3. **Don't mediate-and-synthesize for its own sake.** Take a position with reasoning. Synthesizing is sometimes a way to avoid commitment; the user wants commitment.
4. **The audience is AI researchers**, not philosophy researchers — despite the developer's role. Stop importing philosophy examples into long-arc reasoning.
5. **Cost of redirection is acceptable.** "We haven't built much" — meaning the redirection is methodological, not engineering. Don't pull punches because of cost concerns.
6. **Want the best possible research tool.** Willing to question framing at the foundations. Don't retreat to safe-refinement answers when foundations-questioning is warranted.
7. **`gsd-review` is GSD-phase-shaped.** For spike-methodology audits, dispatch directly via Bash + codex (cross-vendor) and Agent + Opus (same-vendor adversarial). The user explicitly redirected away from `gsd-review`.
8. **The pressure-pass closure-pressure pattern is real.** Future Claude should watch for it in their own writing, especially when audits propose lots of remedies. Calibrated language as default register, not closing-section exception.

## Appendix — concrete artifact references

| Artifact | Path |
|---|---|
| Project entrypoint | `CLAUDE.md` |
| Project state | `.planning/STATE.md` |
| Pressure pass (with paired-review section) | `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` |
| Cross-vendor review | `.planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md` |
| Opus adversarial review | `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md` |
| Paired-review package | `.planning/spikes/reviews/2026-04-25-paired-review-package/` |
| Deliberation (with addendum + post-review status) | `.planning/deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md` |
| Deliberation review | `.planning/deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md` |
| **Long-arc + multi-lens redirection deliberation (load-bearing)** | `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md` |
| Audience reframe deliberation | `.planning/deliberations/2026-04-25-audience-reframe-arxiv-ai.md` |
| Pass/fail vs nuance deliberation | `.planning/deliberations/2026-04-25-pass-fail-vs-nuance-of-differences.md` |
| Mediation vs position-taking deliberation | `.planning/deliberations/2026-04-25-mediation-vs-position-taking.md` |
| Load-bearing assumptions audit (discipline) | `.planning/deliberations/2026-04-25-load-bearing-assumptions-audit.md` |
| Pressure-artifacts-before-remedy (workflow) | `.planning/deliberations/2026-04-25-pressure-artifacts-before-remedy.md` |
| Recording deliberations extensively (meta) | `.planning/deliberations/2026-04-25-recording-deliberations-extensively.md` |
| Suite contract | `.planning/spikes/NEXT-ROUND-SUITE.md` |
| `008` design | `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md` |
| `004` open questions | `.planning/spikes/004-embedding-model-evaluation/OPEN-QUESTIONS.md` |
| ADR-0001 (load-bearing) | `docs/adrs/0001-exploration-first-architecture.md` |
| This handoff | `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md` |

## Sign-off

This handoff is the canonical context-restoration document for the multi-lens redirection. Future Claude reading this fresh should:

1. Read this handoff in full.
2. Read the files in "Files to reopen first" in order.
3. Begin with the immediate next action: the Property audit of Phase 3.
4. Treat the user corrections in the corresponding section as binding.

The redirection is decided. The implementation depends on the Property audit. Everything else is downstream.
