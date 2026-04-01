# Deliberation: Local Gap Propagation and Signal Interpretation

<!--
Deliberation template grounded in:
- Dewey's inquiry cycle (situation → problematization → hypothesis → test → warranted assertion)
- Toulmin's argument structure (claim, grounds, warrant, rebuttal)
- Lakatos's progressive vs degenerating programme shifts
- Peirce's fallibilism (no conclusion is permanently settled)

Additional orientation used here:
- Stiegler, interpretively: tooling and workflows are not neutral channels; they shape what becomes visible, memorable, and actionable
- Reflexive-hermeneutic caution: the "grounds" never gather themselves cleanly; apparent unity is partly an effect of our categories, nouns, and procedural forms
- Trace-attentive reading: what presents itself as one issue or one ground can still carry readable traces of plurality, other contexts, and pre-theoretical understandings that should inform praxis
-->

**Date:** 2026-03-31
**Status:** Open
**Trigger:** Conversation during spike-suite review and workflow adaptation raised a broader question: when a project detects a local workflow gap, how should that signal be interpreted and propagated upstream without mistaking a context-bound symptom for a universal defect?
**Affects:** Spike review workflow design, project-local GSDR overlays, future upstream contribution policy, signal interpretation discipline
**Related:**
- [2026-03-31-delegated-reviews-need-designated-artifacts.md](../knowledge/signals/arxiv-mcp/2026-03-31-delegated-reviews-need-designated-artifacts.md)
- [SPIKE-DESIGN-REVIEW-SPEC.md](../spikes/SPIKE-DESIGN-REVIEW-SPEC.md)
- [run-spike.md](/home/rookslog/.codex/get-shit-done-reflect/workflows/run-spike.md)
- [comparative-characterization-and-nonadditive-evaluation-praxis.md](./comparative-characterization-and-nonadditive-evaluation-praxis.md)

## Situation

The project has begun to use richer review and reflection practices than the current workflow system natively enforces. A concrete example just surfaced: an external review produced useful critique, but only as terminal output rather than as a designated artifact. That gap is locally salient, but it is not yet clear how it should be interpreted.

Several distinct possibilities are in play:

1. The issue may be mainly local to this repository's current way of using review prompts and external tools.
2. It may be a portable workflow gap that other projects would also hit once they adopt similar review rigor.
3. It may point to a deeper upstream design issue in how GSDR treats critique, persistence, and self-improvement.

The difficulty is not just classification. It is epistemic posture. If every local symptom is immediately framed as an upstream defect, the project overgeneralizes from situated friction. If every symptom is treated as merely local, the workflow cannot learn across deployments. The problem is how to mediate between symptom, interpretation, and propagation.

### Evidence Base

| Source | What it shows | Corroborated? | Signal ID |
|--------|--------------|---------------|-----------|
| [2026-03-31-delegated-reviews-need-designated-artifacts.md](../knowledge/signals/arxiv-mcp/2026-03-31-delegated-reviews-need-designated-artifacts.md) | A concrete workflow gap was observed: review output was useful but not artifactized by default | Yes (signal file read) | sig-2026-03-31-delegated-reviews-need-designated-artifacts |
| [SPIKE-DESIGN-REVIEW-SPEC.md](../spikes/SPIKE-DESIGN-REVIEW-SPEC.md) | A reusable review spec now exists locally, but artifact persistence is not yet part of the default contract | Yes (spec created in repo and inspected during session) | informal |
| [2026-03-21-codex-design-review.md](../spikes/004-embedding-model-evaluation/reviews/2026-03-21-codex-design-review.md) | The repo already has a precedent for durable spike review artifacts | Yes (file exists in repo) | informal |
| [run-spike.md](/home/rookslog/.codex/get-shit-done-reflect/workflows/run-spike.md) | The current Codex GSDR spike workflow handles design/build/run/document flow, but does not define an explicit upstream-propagation or review-artifact gate | Yes (workflow file read) | informal |
| `rg` scan over `~/.codex/get-shit-done-reflect` and `~/.codex/skills` for `upstream`, `review artifact`, `designated artifact`, and related terms | No existing first-class mechanism for review-artifact discipline or local-gap propagation was found in the current install | Yes (search returned no matches) | informal |
| Conversation on 2026-03-31 | The user explicitly raised the possibility that local workflow issues may reflect deeper upstream issues, but also challenged any framing that would prematurely close interpretive or design space | Yes (this conversation) | informal |

## Framing

The immediate question is not merely whether to save review output to files. The deeper question is how a project should interpret and route its own workflow frictions.

**Core question:** What gate or workflow should govern when a project-local gap is treated as a local adaptation issue, a portable workflow gap, or an upstream concern, and how much deliberation should mediate that movement?

**Adjacent questions:**
- What makes a signal a symptom of a deeper design issue rather than a context-bound workaround request?
- How much interpretation should happen before a local observation becomes an upstream recommendation?
- How do we preserve openness in the response space without falling into indefinite meta-deliberation?
- What kinds of artifacts should link project-local experimentation to upstream learning?
- How should research, philosophical lenses, and reference designs inform workflow redesign without being used as false authority?
- How do we attend responsibly to traces of plurality, background horizons, and other ways of signifying that remain partially present within what is disclosed?

## Analysis

### Option A: Direct Escalation

- **Claim:** Treat each locally important workflow gap as presumptively upstream-relevant and move quickly to patch or report it upstream.
- **Grounds:** Local friction is often the first visible form of a more general defect. Fast propagation increases learning speed.
- **Warrant:** If the workflow is intended to travel across projects, early local symptoms are useful probes of systemic weakness.
- **Rebuttal:** This risks overgeneralizing from one deployment context and mistaking local orchestration choices for upstream design failures.
- **Qualifier:** Useful for obvious omissions, but too aggressive as a default.

### Option B: Strict Localism

- **Claim:** Treat workflow gaps as local until proven otherwise; patch them in the project and avoid upstream framing unless recurrence appears elsewhere.
- **Grounds:** Tooling behavior is always mediated by project goals, habits, and local constraints.
- **Warrant:** Local adaptation is cheaper and avoids burdening upstream with context-specific noise.
- **Rebuttal:** This blocks learning across deployments and lets the same issue reappear under different names in other projects.
- **Qualifier:** Good as an anti-overreach discipline, but too inert as a learning strategy.

### Option C: Layered Propagation Gate

- **Claim:** Introduce a gate that classifies each issue at three levels: local symptom, portable workflow gap, and upstream architectural concern, with explicit tests before escalation.
- **Grounds:** The current conversation already distinguishes between immediate manifestation and underlying issue. The repo now has signals, review specs, and deliberation artifacts that can support this layered interpretation.
- **Warrant:** A layered gate preserves reversibility and contextual sensitivity while still allowing robust upstream learning. It treats signals as traces that require interpretation, not as self-interpreting facts.
- **Rebuttal:** This can become bureaucratic if every minor issue triggers a full deliberation cycle.
- **Qualifier:** Probably the right default, provided the gate is lightweight and only escalates to deeper deliberation when the issue appears structurally important.

### Option D: Plural Praxis Translation Layer

- **Claim:** Treat deliberation as one node inside a broader procedural praxis that translates multiple input types into concrete workflow proposals: local signals, project artifacts, research traces, philosophical lenses, and reference designs.
- **Grounds:** The current issue cannot be fully understood by signal classification alone. It involves memory and retention practices, workflow contracts, the interpretation of recurrence, and the problem of how local experience should inform upstream change. Different intellectual sources illuminate different parts of that problem.
- **Warrant:** A workflow learns better when it does not force every issue into a single form of reasoning. Signals are good at detection, deliberations at interpretation, research at situating prior art, philosophical lenses at exposing hidden assumptions, and reference designs at showing concrete alternative arrangements. A translation layer can hold these together without letting any single source dominate.
- **Rebuttal:** This risks becoming rhetorically rich but procedurally vague unless the translation into design proposals is explicit and bounded.
- **Qualifier:** Strong candidate if made concrete through a small set of required artifact fields and response categories.

### Option E: Reflexive Trace-Attunement

- **Claim:** Add an explicit step in which the project attends to the traces of plurality, other contexts, and pre-theoretical understandings carried within what appears as a single issue, rather than relying only on a declaration of "our horizon."
- **Grounds:** The conversation has sharpened that the issue is not merely that multiple lenses exist, nor merely that we should confess our own framing. It is that what is disclosed as one thing can still signify otherwise, and can carry traces of multiplicity within its apparent sameness. If these traces are ignored, the translation layer may still consolidate too quickly around one reading while calling itself plural.
- **Warrant:** Responsible praxis requires more than self-positioning. It requires disciplined attention to the traces of what the current framing leaves partially unsaid but not wholly absent: missing standpoints, alternative uses, neighboring contexts, sedimented assumptions, and different practical inheritances. This does not dissolve disclosure into pure multiplicity; it resists mistaking the gathered presentation for exhaustive presence.
- **Rebuttal:** This can become vague or ornamental unless tied to specific prompts and concrete design consequences.
- **Qualifier:** Necessary as a discipline, but only if operationalized lightly and linked to actual response options.

## Tensions

1. **Speed vs interpretation**
   Fast escalation improves responsiveness but increases the risk of misclassifying a local symptom as a systemic flaw.

2. **Local context vs upstream generality**
   The same workflow may fail for different reasons in different projects. Abstraction is necessary, but premature abstraction distorts.

3. **Signal discipline vs signal inflation**
   Formal signals help traceability, but not every friction deserves the same interpretive weight.

4. **Pragmatic patching vs deeper critique**
   A local fix may resolve the immediate issue while leaving untouched the underlying workflow logic that produced it.

5. **Memory vs foreclosure**
   Stiegler's relevance here is practical: artifact systems shape what is retained and therefore what becomes actionable. Better retention can either deepen learning or prematurely harden one interpretation into workflow doctrine.

6. **Plural sources vs false authority**
   Research, philosophy, and reference designs can deepen design judgment, but they can also be misused as prestige cover for decisions that still require local testing and qualification.

7. **Reflexive responsibility vs regress**
   The project should attend to the traces of other possible readings and background commitments, but complete explicitness is impossible. The praxis must therefore acknowledge both the necessity and the limit of reflexive work.

## Recommendation

**Current leaning:** Option C implemented inside Option D, with Option E as a standing discipline on how translation and response are conducted.

The project likely needs a lightweight propagation gate with explicit layers, but that gate should sit inside a broader praxis rather than functioning as the whole response mechanism.

### Proposed procedural praxis

1. **Capture**
   Record the local symptom as a signal, review artifact, or execution note.

2. **Interpret**
   Use a short deliberation only when the issue touches contracts, abstractions, or recurring orchestration patterns.

3. **Attend to traces**
   Add a short trace-attunement note before translation:
   - what terms are doing the conceptual gathering here?
   - what multiplicities or other contexts are still traceable within this gathered presentation?
   - what pre-theoretical understandings, practical inheritances, or absent standpoints may be shaping the issue as currently named?
   - what alternative significations remain plausible even if they are not the primary operational framing?
   - what cannot be made fully explicit but still should be acknowledged?

4. **Translate**
   For issues that survive interpretation, produce a small translation artifact or section with:
   - source traces: local artifacts, research inputs, philosophical lenses, reference designs
   - what each source affords
   - what each source does not license
   - candidate response types

5. **Respond**
   Choose among response types rather than assuming every issue wants the same kind of fix.

6. **Propagate**
   Escalate upstream only when the issue has been stated at the level of missing contract, missing gate, or faulty abstraction.

### Response repertoire

The response space should remain explicitly plural. A project-level deliberation should help open and compare these options, not determine them exhaustively.

Possible response types:

1. **Interpretive change**
   Reclassify the issue without changing tooling. Example: tighten how signals are read before escalation.

2. **Artifact change**
   Add or reorganize durable artifacts. Example: require designated review outputs under `.planning/.../reviews/`.

3. **Procedural change**
   Change the required sequence or checkpoints. Example: require `artifact_path` in review requests.

4. **Sensor or signal change**
   Add detection, recurrence tracking, or better clustering for workflow issues.

5. **Governance change**
   Introduce criteria for when local issues become portable-gap candidates or upstream concerns.

6. **Local overlay**
   Patch project-local workflow behavior without changing upstream immediately.

7. **Upstream design proposal**
   When justified, propose a reusable change to GSDR itself.

8. **Lexical or conceptual revision**
   Change the vocabulary or categories through which the issue is being understood when the current gathering terms suppress relevant traces of plurality or background commitments.

### Intellectual inputs and what they afford

This praxis should not treat philosophy or research as ornamental. It should use them as different kinds of disciplined constraint.

- **Dewey**
  Treat workflow friction as an indeterminate situation that requires inquiry, not instant classification.

- **Stiegler**
  Ask what the artifact and retention system makes visible, forgettable, or actionable.

- **Mayo**
  Require severe enough checks before claiming an issue is portable or upstream-worthy.

- **Lakatos**
  Ask whether workflow modifications are progressive or merely protective patches around anomalies.

- **Cartwright / patchy-capacity thinking**
  Expect many workflow interventions to be locally valid before they are general.

- **Reference designs**
  Use them through critical inheritance: extract patterns, preconditions, and trade-offs rather than copying surface forms.

- **Reflexive-hermeneutic discipline**
  Treat key terms as provisional gathering points rather than self-identical essences; ask what traces of multiplicity, background horizons, and alternative significations remain readable within them, and what practical consequences follow from ignoring those traces.

### Concrete design direction for GSDR

If this line of thought is adopted, the likely concrete proposals are not just "more deliberation." They are things like:

1. A required `artifact_path` field in reusable review specs and review-oriented skills.
2. A project-local `UPSTREAM-GAPS.md` or equivalent queue that aggregates portable-gap candidates without forcing immediate upstream action.
3. A lightweight translation template for turning signals plus lenses plus reference designs into concrete workflow proposals.
4. A propagation gate that asks the same questions every time:
   - what is local here?
   - what appears portable?
   - what abstraction or contract failure is being alleged?
   - what evidence would falsify that allegation?
5. A short `trace-attunement note` field in deliberation or review artifacts, capturing the operative framing, missing standpoints, background commitments, and traces of plausible alternative readings.
6. A `counter-reading` field for major workflow proposals: what materially different interpretation of the same issue remains plausible?

Only the third layer should drive upstream patch proposals. The second layer is where short project-level deliberation belongs. Not every signal needs full deliberation, but signals that concern workflow contracts, interpretation discipline, or recurring orchestration patterns probably do.

**Open questions blocking conclusion:**
1. What are the minimum tests for moving from local issue to portable gap candidate?
2. Should project-local overlays be preferred over upstream patches until recurrence is shown?
3. What artifact should aggregate local divergences into a usable upstream feedback queue?
4. What is the smallest useful "translation artifact" between signal and concrete GSDR design proposal?
5. Which philosophical lenses are actually useful often enough to operationalize, and how do we keep them from becoming decorative vocabulary?
6. How much trace-attentive reflexive work is enough to improve judgment without paralyzing action?

## Predictions

**If adopted, we predict:**

| ID | Prediction | Observable by | Falsified if |
|----|-----------|---------------|-------------|
| P1 | Fewer workflow complaints will be discussed only in terminal chat; more will land in durable review, signal, or deliberation artifacts | Next 3 workflow adjustments in this repo | New workflow gaps continue to be handled ad hoc without artifactization |
| P2 | Upstream-facing concerns will become narrower and better-justified because they will pass through a local/portable/upstream distinction first | Next time a GSDR workflow patch is proposed | Proposed upstream changes still collapse local symptoms directly into universal fixes |
| P3 | The project will identify a small number of recurring workflow-contract issues rather than a growing pile of disconnected complaints | After several more spike/review cycles | Signals accumulate without any discernible clustering or propagation logic |

## Decision Record

**Decision:** Not yet concluded
**Decided:** N/A
**Implemented via:** Not yet implemented
**Signals addressed:** sig-2026-03-31-delegated-reviews-need-designated-artifacts

## Evaluation

Pending.

## Supersession

Not superseded.
