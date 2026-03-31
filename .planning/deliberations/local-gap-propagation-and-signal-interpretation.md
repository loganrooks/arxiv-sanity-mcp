# Deliberation: Local Gap Propagation and Signal Interpretation

<!--
Deliberation template grounded in:
- Dewey's inquiry cycle (situation → problematization → hypothesis → test → warranted assertion)
- Toulmin's argument structure (claim, grounds, warrant, rebuttal)
- Lakatos's progressive vs degenerating programme shifts
- Peirce's fallibilism (no conclusion is permanently settled)

Additional orientation used here:
- Stiegler, interpretively: tooling and workflows are not neutral channels; they shape what becomes visible, memorable, and actionable
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

## Recommendation

**Current leaning:** Option C.

The project likely needs a lightweight propagation gate with explicit layers:

1. **Local issue**
   A concrete symptom in this repo. Capture it as a signal or artifact.

2. **Portable gap candidate**
   Ask: would another project using the same workflow likely hit this? What is the minimal abstraction of the issue?

3. **Upstream concern**
   Ask: does the issue expose a missing contract, missing gate, or faulty abstraction in GSDR itself?

Only the third layer should drive upstream patch proposals. The second layer is where short project-level deliberation belongs. Not every signal needs full deliberation, but signals that concern workflow contracts, interpretation discipline, or recurring orchestration patterns probably do.

**Open questions blocking conclusion:**
1. What are the minimum tests for moving from local issue to portable gap candidate?
2. Should project-local overlays be preferred over upstream patches until recurrence is shown?
3. What artifact should aggregate local divergences into a usable upstream feedback queue?

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
