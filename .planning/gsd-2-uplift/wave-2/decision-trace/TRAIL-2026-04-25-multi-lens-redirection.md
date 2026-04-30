---
type: phase-D-test-artifact
date: 2026-04-30
production_method: Claude Code subagent (general-purpose subagent_type) invoked with decision-trace SKILL.md body as operating prompt; skill_path=~/.agents/skills/decision-trace/SKILL.md
test_task: .planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md (primary, low-D5a per F-PD-A5+B2)
phase: trajectory plan §1.4 Phase D — Option 5 subagent invocation (pure first-target evidence, channel (a))
disposition: subagent followed SKILL.md <process> + <output_format> faithfully; output preserved verbatim below for evidence-chain integrity
note: This trail is a Phase D test artifact. Authentic decision-trace skill output for the v0.2 multi-lens redirection decision; saved here (not at .planning/decision-traces/) to keep Phase D evidence corpus self-contained.
---

# Decision-trace: v0.2 multi-lens redirection (citation/community as load-bearing second lens; BERTopic generalized to bundle-of-signals)

## Decision under trace

On 2026-04-25, the project committed to redirect v0.2 from a tournament-style "pick the best embedding-model stack" frame to shipping a **multi-lens MCP substrate** with at least two lenses (the existing semantic lens plus a new citation/community lens), and to **generalize the BERTopic profile primitive into a bundle-of-signals** rather than replacing it. User-confirmed disposition is recorded at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:74-82`.

## Canonical record

No `.gsd/DECISIONS.md` and no `.planning/.gsd/DECISIONS.md` exist in this repository (verified by `find … -name DECISIONS.md` and `find … -type d -name .gsd`). The project has no `gsd_decision_save`-written canonical decision table.

The closest functional analogue to a canonical record is `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`, dated 2026-04-25, which captures the architectural shape post-hoc and explicitly cites the deliberation chain it rests on (`docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:1-9`, `:11-17`). ADR-0005's "Decision" block at `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:22-40` is the durable canon for the architectural commitment; the deliberation under trace is the rationale layer beneath it.

## Rationale chain

1. **Prompt: refuse small-fixes; demand foundations-questioning and long-arc orientation.** The user prompt rejected the small-fixes path (007 override annotation, 008 asymmetric-comparison fix, profile-family decision, then run 008) and asked for foundations-questioning + long-arc orientation — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:21-25`.

2. **Implicit-commitment audit surfaced six commitments the spike program had been operating under.** Profiles pre-built; retrieval as central operation; agent as evaluation unit; embedding-model choice as load-bearing decision; tournament narrowing as discovery mechanism; MiniLM as silent default — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:30-38`.

3. **Diagnosis: those six commitments collectively drifted away from ADR-0001's coexistence intent.** "The spike program had drifted toward winner-pick under tournament-narrowing despite ADR-0001's accepted commitment to exploration-first multi-lens architecture" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:40`. ADR-0001 itself states "multiple retrieval and ranking strategies can coexist" at `docs/adrs/ADR-0001-exploration-first.md:21-22`.

4. **The drift was invisible from inside the spike program because each step looked locally reasonable.** "Every step looked reasonable" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:40`. This claim is reinforced by the prior pressure-pass + paired-review chain that documented the local-reasonableness of each narrowing step, see `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md:258-285` (cross-artifact synthesis findings 1-7) and the "After the paired review" section at `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md:323-379`.

5. **Audience correction: the tool is for AI researchers primarily, not philosophy researchers.** The correction came as a separate user prompt and is recorded at `.planning/deliberations/2026-04-25-audience-reframe-arxiv-ai.md:17-22`. It bound the redirection's lens-type concretization to AI-research register at `.planning/deliberations/2026-04-25-audience-reframe-arxiv-ai.md:44-56`.

6. **Audience correction sharpens — does not weaken — the multi-lens case for AI research.** AI research is intensely community-structured (specific labs, conferences, paper threads); citation/community, benchmark/dataset, and methodological lenses become substantially more load-bearing than they would be for slower fields — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:44`. Same conclusion in audience-reframe document — `.planning/deliberations/2026-04-25-audience-reframe-arxiv-ai.md:29-33`.

7. **Topic-cluster (BERTopic) representation flattens AI-research practice in particularly damaging ways.** "RLHF papers and constitutional-AI papers are topically similar but conversationally distinct; mechanistic-interpretability papers are topically similar but methodologically very diverse" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:44`.

8. **Foreclosures named: the current framing had foreclosed the multi-lens architecture itself, the longitudinal-practice evaluation surface, the deeper substrate (profile elicitation / taste capture / longitudinal memory) question, and the discursive-community register.** `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:50-56`.

9. **Long-arc vision (AI-research register) articulates what a best-possible tool would do across years.** Reading-history depth, argumentative-style recognition, lateral connections, intellectual-lineage tracking, discursive-community structure, legible operations, steerability, accountability-to-dissent, cross-session memory — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:58-71`.

10. **Citation/community lens chosen as the load-bearing v0.2 addition.** Reasons given: AI research is intensely community-structured; citation graphs are particularly load-bearing for AI; this is the highest-leverage AI-specific addition the spike program neglected — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:78`.

11. **BERTopic generalized to bundle-of-signals, not replaced.** Rationale: BERTopic stays as one signal among many; behavior-derived, citation-anchor-derived, and researcher-curated-prose signals can be added in parallel without breaking changes — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:79`. The deeper substrate motivation traces to `004/OPEN-QUESTIONS.md`'s A2 finding that "Interest profiles are MiniLM-entangled — never tested otherwise" at `.planning/spikes/004-embedding-model-evaluation/OPEN-QUESTIONS.md:23-29`.

12. **Cost of redirection accepted as methodological, not engineering: v0.1 stays.** "No code is being torn up; the redirection is methodological" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:81`.

13. **Two-lens validation reasoning: abstractions are most likely to be right when validated by a second implementation.** "Option B is preferred because abstractions are most likely to be right when validated by a second implementation. Option C risks the lens-extensibility abstraction being subtly wrong in ways that only become visible when adding the second lens — by which time consumers depend on it" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:93`. ADR-0005 reproduces this reasoning canonically at `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:19`, and rejects three alternatives in `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:42-52`.

## Alternatives considered

- **Option A — full multi-lens substrate in v0.2 (3-4 months engineering + spike work).** Disposed: rejected as too expensive for one milestone — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:88, 93`. ADR-0005 records it as overscoped given Property 1's verdict that the profile primitive does not need rewriting — `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:19`.

- **Option B — refactor primitives + ship two lenses (semantic + citation/community), ~2 months.** Disposed: chosen as the default-lean (still contingent on Property audit at the time of deliberation) — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:89, 93`. Confirmed in ADR-0005's decision block — `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:22-28`.

- **Option C — refactor for extensibility, ship one lens, multi-lens validated in v0.3 (~1 month).** Disposed: rejected because "Option C risks the lens-extensibility abstraction being subtly wrong in ways that only become visible when adding the second lens — by which time consumers depend on it" — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:93`. ADR-0005 sharpens the rejection: a single-lens "interface" risks shipping shaped exactly to the lens you happen to build, repeating the trap ADR-0001 names — `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:19`.

- **`008` as designed (tournament that picks a winner among carried challengers).** Disposed: spike `008` will not run as a tournament; reshape or replace as part of a longitudinal pilot, decision deferred pending vision document — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:80`. The handoff captures the same disposition with reasoning at `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md:298-306`.

- **Replace BERTopic with a successor cluster method.** Disposed: not the chosen direction; generalize-to-bundle-of-signals is the chosen pattern — `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:79`. Same disposition, fuller wording, in handoff lessons at `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md:123`.

- **Three additional alternatives recorded in ADR-0005 (post-hoc, not in the deliberation itself):** (i) refactor + 0 lenses with paired internal review — rejected because design-only review cannot detect single-lens-interface trap; (ii) lens abstraction + thin stub second lens — rejected because storage-shape problems only surface against retrieval-shaped data; (iii) defer abstraction; run two parallel pipelines first — rejected because parallel pipelines do not exercise the consumer-side coexistence problem — `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:42-52`.

## Predictions and evaluation status

The deliberation does not contain a `falsifiable_predictions` block, an `evaluation_trigger` block, or pre-registered probability priors of the kind seen in `008/DESIGN.md`. The closest things to predictions are:

- **Prediction: "Option C risks the lens-extensibility abstraction being subtly wrong in ways that only become visible when adding the second lens."** Source: `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:93`. **Status: not-tracked as a falsifiable prediction.** Option C was rejected, so the prediction is unevaluable by the chosen path; it cannot be confirmed or contradicted because the alternative was not run.

- **Prediction: "abstractions are most likely to be right when validated by a second implementation."** Source: `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:93`. **Status: pending** — would be evaluated against v0.2 shipping evidence (whether the lens abstraction holds up under the second-lens implementation). No explicit evaluation trigger or threshold is named in the deliberation.

- **Implicit prediction: "Citation/community is the highest-leverage AI-specific addition the spike program neglected."** Source: `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:78`. **Status: not-tracked** — no metric, threshold, or evaluation trigger pre-registered in the deliberation.

The absence of explicit `falsifiable_predictions` / `evaluation_status` blocks is itself trail evidence: this deliberation operated in design-direction mode, not in pre-registered-spike mode. The handoff at `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md:310-320` flags the Property audit as the immediate next concrete action that would gate Option A/B/C; that audit ran the same day and is now recorded at `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` (cited in ADR-0005 at `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:11-17`), which converts what was a "pending audit" into a now-evaluated property check.

## Layer attribution

OMITTED with note: this deliberation does not turn on preference-attribution. No `~/.gsd/PREFERENCES.md` or `.gsd/PREFERENCES.md` field is in scope. The decision rests on architectural deliberation and ADR-rooted commitments, not on token-profile / mode / preference-merge layers. Skill's `<process>` Step 6 is therefore not actuated.

## Gaps in record

- **No canonical `.gsd/DECISIONS.md` row.** No `.gsd/` directory exists in the project; the project's decision capture is via ADRs (`docs/adrs/`) and deliberation artifacts under `.planning/deliberations/`, not via the `gsd_decision_save` substrate. Would need: a project-side adoption of gsd-2 native `.gsd/DECISIONS.md`, or an explicit decision to treat ADRs + deliberations as the canonical layer (the de-facto current state, but not formally declared).

- **No falsifiable predictions block.** The deliberation does not pre-register predictions, evaluation triggers, or thresholds in the form `008/DESIGN.md` uses (P(H1)=0.70 etc.). Would need: an addendum or follow-up artifact specifying what evidence at v0.2 close would confirm or contradict the "two-lens validation" reasoning, with concrete metrics and thresholds.

- **No explicit disposition of "Option B chosen" inside the deliberation.** The deliberation at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:84-93` calls Option B the "default lean" with the choice "contingent on a Property audit of Phase 3 (interest modeling) implementation." The actual Option B commit happened later the same day in ADR-0005 at `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:22-28`, after the Property audit ran. The bridge between "default lean, audit-pending" (this deliberation) and "Option B committed" (ADR-0005) is the audit at `.planning/audits/2026-04-25-phase-3-property-audit-opus.md`, not a separate deliberation step. The audit's contribution to the chain is reasoned about in ADR-0005 but is not a deliberation artifact in `.planning/deliberations/`.

- **No explicit user-confirmation timestamp inside the deliberation.** The deliberation's frontmatter says "decided — implementation open" and the body says "user-confirmed 2026-04-25" at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:75`, but there is no transcript or activity-log citation tying that confirmation to a specific session event. Would need: `.gsd/activity/*.jsonl` or `.gsd/journal/2026-04-25.jsonl` cross-references — neither exists in this project.

- **Spike `008`'s fate remains undecided.** `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:80, 105` records "Decision deferred pending vision document." ADR-0005 confirms the same at `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md:77`. Would need: a follow-up disposition once the vision document is drafted; that artifact does not yet exist (status flag at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:112`).

- **Vision document referenced but not written.** `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:102, 112` flags it as the artifact that should set the criterion the spike program is judged against; status: ✗ not yet drafted at time of deliberation. Trail cannot recover what the vision document would say; would need the document itself.

## Cross-references to existing primitives

- **`gsd_decision_save` MCP tool / `.gsd/DECISIONS.md` substrate.** Not used in this project; no canonical row exists for this decision (see `Gaps in record` first item). The trail therefore extends beyond rather than complements existing canonical-table primitives.

- **ADR-0005 (`docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`).** Functions as the durable architectural canon for the decision the deliberation under trace produced. The trail does not subsume ADR-0005; it cites the deliberation as the rationale layer beneath ADR-0005's Decision block.

- **Adjacent-runtime `/gsdr:deliberate` slash command.** Available in this runtime per the system reminder ("gsdr:deliberate: Start or continue a structured deliberation about a design question, grounded in signals and philosophical principles"). The deliberation under trace was not produced by `/gsdr:deliberate` invocation per se — it is a long-form narrative deliberation written in this project's `.planning/deliberations/` convention rather than a structured prediction-shape output. The trail surfaces `/gsdr:deliberate`'s existence as adjacent prior art without claiming to subsume what it would produce against this decision.

- **Pressure-pass + paired-review chain at `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md`** (with cross-vendor at `.planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md` and Opus adversarial at `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md`). These artifacts produced the methodological pressure that exposed the closure-pressure pattern in the spike program; the deliberation under trace cites them in its frontmatter at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:9-13` as part of the journey that produced the redirection. They are evidence-chain antecedents, not subsumed by the trail.

- **Handoff at `.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md`** is forward-looking (continuation framing for future Claude). The trail discriminates from handoff shape: the trail is backward-looking reconstruction of how the decision was made, not a continue.md for next session. The handoff is a peer artifact in the record, cited where its content provides additional anchoring (`.planning/handoffs/2026-04-25-arxiv-mcp-multi-lens-redirection.md:97-113` for the journey timeline; `:115-126` for the lessons).

## Confidence

**High** for the rationale chain steps 1-13 and for the alternatives section: each claim cites the deliberation directly, often with corroborating citations in ADR-0005, the audience-reframe deliberation, and the handoff. The deliberation under trace is unusually well-narrativized (`.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:121-133` explicitly explains the form), which makes reconstruction unusually low-fabrication-risk.

**Medium** for the Predictions section: the deliberation lacks pre-registered falsifiable predictions, so the trail's "implicit prediction" framings are interpretive labels applied to claims-with-prediction-shape, not direct citations to a `falsifiable_predictions` block. A reader who insists on strict pre-registration would prefer the gap to be marked simpler ("no predictions in record") and the implicit-prediction labels removed.

**Low** for any timeline-anchoring claim that would require activity-log or journal evidence: this project does not run gsd-2 native runtime, so `.gsd/activity/*.jsonl` and `.gsd/journal/YYYY-MM-DD.jsonl` are not available. The "user-confirmed 2026-04-25" claim at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:75` cannot be tied to a specific transcript event from the trail's evidence base.

What would shift confidence: (a) a follow-up artifact pre-registering falsifiable predictions for the two-lens-validation hypothesis would lift Predictions confidence to high; (b) project-side adoption of `.gsd/DECISIONS.md` and back-fill of this decision as a canonical row would close the canonical-record gap; (c) the vision document, when written, would resolve the load-bearing open dependency the deliberation itself flags at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md:102, 112`.
