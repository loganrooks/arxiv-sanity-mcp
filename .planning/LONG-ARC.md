---
document: LONG-ARC
status: canonical
type: planning-doctrine
scope: Durable doctrine that disciplines current planning to preserve VISION.md without overscoping into it.
last_updated: 2026-04-25
related_documents:
  - .planning/VISION.md
  - .planning/PROJECT.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
  - docs/adrs/ADR-0001-exploration-first.md
  - docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md
  - .planning/spikes/METHODOLOGY.md
  - .planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md
---

# Long-Arc Planning Doctrine

This file ratifies the durable doctrine that sits between `VISION.md` and the live operational canon (`ROADMAP.md`, `STATE.md`, phase plans). It is not a second roadmap, a deferred-features list, or a back door for importing later-phase delivery into the current phase. Its job is to keep current planning from foreclosing the long-arc vision while respecting the current milestone's scope.

## Current product and planning posture

- **v0.1** is complete and frozen (31/31 plans, 403 tests, MCP server with 10 tools + 4 resources + 3 prompts; validated with real data).
- **v0.2** has been architecturally committed via [ADR-0005](../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md): multi-lens MCP substrate, two lenses minimum (semantic + citation/community), bundle-of-signals profile primitive.
- **v0.2 detailed plan** is the next planning artifact; it does not yet exist.
- The 005-008 spike chain is **reshaped, not abandoned**: tournament narrowing is parked; semantic-lens spike work continues but as lens-design, not winner-pick.

## Protected seams

Architectural commitments that current and near-term planning must preserve:

- **Lens-extensibility.** A `Lens` interface that admits new lenses (semantic, citation/community, author, benchmark, methodological, temporal, behavior-derived) without consumer-side changes. Validated by shipping at least two lenses (ADR-0005).
- **Bundle-of-signals profile primitive.** `signal_type` open at the DB level (already true post-migration 005). New signal types added by registry, not by schema migration.
- **Per-lens provenance.** Every recommendation carries which lens surfaced it, what features matched, and what evidence the rank rests on. Per-lens explanations as first-class output.
- **MCP surface lens-awareness.** Tools accept `lens=` (or equivalent) parameter; resources expose per-lens views; prompts compose across lenses.
- **Citation/community as first-class data, not enrichment.** Citation graphs are retrieval-shaped (normalized edges, queryable), not write-once metadata.
- **Longitudinal state.** Workflow state, triage history, profile evolution, dismissed recommendations are durable across sessions. The profile is not a session-bound construct.
- **Inspectability of every signal.** ADR-0003 binds; no hidden ranker state.
- **MCP-native operations.** Per ADR-0004, MCP is the workflow substrate, not a thin search wrapper. Steering, intersection, lens-disagreement, and explanation are first-class operations exposed via MCP.
- **Explicit profile elicitation.** Any future profile-learning mechanism — behavior-derived (what was read, time-on-page, returned-to, dismissed), citation-anchor-derived, curated-prose, or otherwise — must require explicit researcher confirmation per signal addition. Implicit learning from behavior is foreclosed by VISION's anti-vision (`VISION.md:84`) and re-affirmed here as a v0.2-committed protected seam, even though no v0.2 phase implements it. This converts deferral-protection (the anti-vision is currently preserved by behavior-derived signals being out of scope per `MILESTONE.md` v0.2 deferrals) into mechanism-protection at the doctrine layer, so the seam survives the v0.2 → v0.3 transition where behavior-derived signals may enter scope.

## Anti-patterns to detect

Patterns we have already drifted into once. Current planning must watch for them and call them out when they appear.

- **Tournament narrowing.** Sequentially pruning the candidate set toward a winner under "disciplined" framing. Even when local steps look reasonable, narrow-by-default violates the coexistence posture ADR-0001 commits us to (capability claim about the architecture); LONG-ARC operationalizes it as a posture-to-honor at the implementation layer. **Counter-posture:** rank-and-deprioritize, not eliminate. Multi-lens framing replaces winner-pick.
- **Single-lens "interface" by accident.** Shipping a lens abstraction alongside only one lens — the abstraction ends up shaped exactly to that lens, and the second lens reveals the abstraction was wrong only after consumers depend on it. **Counter-posture:** validate abstractions by shipping a second implementation, not by design alone (ADR-0005).
- **Silent defaults.** A reference frame (MiniLM, TF-IDF, the incumbent profile family) becomes the implicit baseline that all alternatives are measured against, even when nothing argued for it being baseline. **Counter-posture:** name the reference frame explicitly; require challengers to be measured against multiple frames or against task outcomes, not against the frame itself.
- **ADR violation by gradual local-reasonable steps.** Each step locally defensible; cumulative drift away from an accepted ADR. The 005-008 spike chain did this to ADR-0001 over weeks. **Counter-posture:** periodic ADR-against-current-work audits at deliberation boundaries; ADRs are read at planning time, not just at writing time.
- **Closure pressure at every layer.** The pattern of confident remedies, prescriptive language, calibrated language reserved for closing footnotes rather than running through prose. Recurs at spike layer, audit layer, meta-audit layer. **Counter-posture:** calibrated language as default register, not exceptional. Pattern-watch at every level of work.
- **Embedding-model choice as load-bearing decision.** Treating "which model wins" as the architectural commitment when most actual tool-quality leverage lives upstream (query interpretation, profile elicitation, presentation, interaction-loop, trust calibration). **Counter-posture:** treat embedding-model selection as one lens-design decision among many, not as the v-anything architecture call.
- **Single-reader framing claims as authoritative.** Audit memos and framing critiques produced by one reader (or one model) propagated as ground truth. **Counter-posture:** paired review for framing claims (cross-vendor + same-vendor); see [METHODOLOGY.md](spikes/METHODOLOGY.md).

## Methodology doctrine (brief)

The full standing reference is [`spikes/METHODOLOGY.md`](spikes/METHODOLOGY.md). Doctrine-level summary, for current planning to cite:

- **Paired review for framing claims.** Single-reader output should not drive remedies on contestable framing. Cross-vendor + same-vendor pairing catches different categories of failure (substance vs register).
- **Model verification before delegation.** Audits, property checks, and gating evidence go to a known-quality model. Default Explore agent is for cheap surface searches, not for evidence that informs roadmap calls.
- **Single-reader factual claims need verification.** "X exists" or "Y is current state" claims about the codebase are checkable in seconds; verify before propagating.
- **Calibrated language as default register.** Confidence calibration that lives only in a closing footnote does not reach the prose it qualifies. Calibration must propagate to the framing language used throughout.
- **Pressure-test artifacts before adopting remedies.** When a deliberation proposes patches from a constructed option space, run diagnostic questions against the underlying evidence first. The constructed-option-space mistake recurs unless the next step is anchored in artifact reading rather than doctrine.

## Explicit non-decisions

These are deferred. Current planning should not silently decide them.

- **Third lens after citation/community.** Methodological vs benchmark/dataset vs author/affiliation. Each has different leverage and different data-integration cost. Open until v0.2 ships and post-v0.2 evidence informs the choice.
- **Fusion strategy.** RRF preferred *if fusion is used*. Fusion is one option among steering, intersection, lens-disagreement, and per-paper explanation; default is not fusion.
- **Methodological-lens taxonomy.** Curated method-tag taxonomy vs classifier vs hybrid. Open.
- **Profile-elicitation alternatives timing.** Behavior-derived, citation-anchor-derived, researcher-curated prose. Likely post-v0.2; possibly a small upfront spike if needed to de-risk the bundle-of-signals abstraction.
- **Semantic-lens embedding-model selection.** v0.1 baseline (TF-IDF + lexical) carries forward into v0.2; the "semantic" lens label is preserved for backward compatibility but does not yet imply dense embeddings. Revisit at v0.3 or earlier if pilot signals warrant. The rename-or-preserve question (whether to retire the `semantic` label in favor of `lexical`/`tfidf_lexical` when a real embedding lens ships) is part of that revisit, not a v0.2 decision. If a future v0.2 phase introduces dense embeddings (currently scoped out per `milestones/v0.2-MILESTONE.md` deferrals), the rename becomes coordinated with the substantive change rather than a standalone breaking change.
- **`008` fate.** Reshape as longitudinal pilot using multi-lens, shelve, or run for partial signal. Pending vision document interaction with v0.2 plan.
- **Phase ordering revision.** Whether Phase 6 (content normalization) and citation-graph data integration should be pulled forward into v0.2 to support citation/community lens. Likely yes; explicit decision deferred to v0.2 plan.
- **Eventual storage backend if multi-lens scales.** PostgreSQL with denormalized citations may suffice for years; pgvector or graph-DB introduction is not committed.
- **Multi-user or collaborative shape.** v-current is single-user MCP-native. Collaborative use is a future-shape note, not committed.

## Future shape notes

These are directions current planning must preserve. They are not immediate scope imports.

- **Additional lenses** (author/affiliation, benchmark/dataset, methodological, temporal trajectory, behavior-derived) — preserved future shape; substrate must accommodate without rewriting consumers.
- **Longitudinal pilot** as v0.2 evaluation surface (replacing tournament `008`).
- **Behavior-derived profile signals** — what was read, time-on-page, returned-to, cited approvingly, dismissed.
- **Lens-disagreement as MCP operation** — first-class output, not just an analysis affordance.
- **Per-paper explanation as first-class** — every recommendation inspectable.
- **Multi-corpus expansion** — beyond arXiv to OpenReview, conference proceedings, preprint servers in adjacent fields. Not committed; not foreclosed.
- **Calibration against real reading practice** — pilot with one researcher (Logan), then beyond.

## Doctrine interaction with the spike program

- The spike program serves lens design, not winner-pick. Spikes that test which configuration helps a research task are valid; spikes that "narrow toward `008`" under tournament framing are not.
- Spike-level pressure-passes precede remedy adoption (the 2026-04-25 cycle established this pattern).
- Spike methodology is governed by [`spikes/METHODOLOGY.md`](spikes/METHODOLOGY.md). Cross-reference, do not duplicate.
- Spike-program structural changes (e.g., reshaping `008`) are part of the v0.2 plan, not free-floating spike redesign.

## What current planning must do

- **Cite this file** when phase sequencing, architectural seams, or rewrite-trigger decisions materially interact with long-arc posture.
- **Preserve future seams** without padding the current phase into a later one. Lens-extensibility, bundle-of-signals primitive, longitudinal state — these stay open even when not active.
- **Record explicit non-actions** when the correct move is to defer rather than silently decide. Add to "Explicit non-decisions" above.
- **Run an ADR-against-current-work audit at each deliberation boundary.** The 005-008 drift was invisible from inside the spike program; periodic explicit audit is the counter-posture. *Operational-hook status: pending. The audit cadence, ownership, and artifact format are tracked for the gsd-2 long-horizon-planning uplift to integrate as a project-agnostic workflow primitive. Until then, the discipline is self-imposed at deliberation boundaries; no specific cadence is committed.*
- **Watch for anti-patterns.** Name them when they appear; do not let them ride.
- **Escalate to VISION.md** only when the question is product identity or eventual platform shape, not planning doctrine.

## Reopen conditions

Reopen this file only when one of these changes materially:

1. **Product identity** (escalate to VISION.md first).
2. **The multi-lens substrate commitment** is reversed or amended.
3. **The longitudinal-memory commitment** proves unviable.
4. **A new anti-pattern** is identified through a methodology audit cycle and warrants doctrinal placement.
5. **The boundary between doctrine and live operational canon** shifts (e.g., new artifact types are introduced).
6. **Audience identity changes** (e.g., the AI-research focus broadens or narrows).

Otherwise this document is canonical. It does not require rewriting on every roadmap revision.
