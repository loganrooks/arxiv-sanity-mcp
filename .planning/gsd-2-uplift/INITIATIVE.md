---
type: initiative-staging
date: 2026-04-26
status: articulated; framing open; first-wave exploration not yet dispatched
articulation_age: one session old; not yet stress-tested or integrated with PROJECT.md / VISION.md
ground: .planning/gsd-2-uplift/DECISION-SPACE.md (load-bearing decision reference)
log: .planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md (dynamics)
parent_project: arxiv-sanity-mcp (staging here pending dedicated repo)
migration_trigger: when dedicated repo for the uplift project is created, this artifact and its siblings under .planning/gsd-2-uplift/ migrate there; STATE.md pending-todo updates accordingly
---

# gsd-2 Uplift Initiative — Staging Artifact

This document stages the gsd-2 uplift initiative forward. It is not the scoping document — scoping happens through first-wave exploration + second-wave design work. This document records the goal as articulated, the open framing questions, the inputs available, and the first-wave plan.

**For decisions and recommendation-space mapping**: see DECISION-SPACE.md.
**For session dynamics that produced these decisions**: see the deliberation log.

## §0. How to read this document

**Audience.** Future-Logan, future-Claude in fresh sessions, subagents dispatched for first-wave exploration, possibly external readers if the initiative gets sponsored or observed.

**What this document IS.** Forward-staging for the gsd-2 uplift initiative: records the goal as articulated, the open framing questions, the inputs available, and the first-wave plan. Useful as orientation when entering the initiative cold.

**What this document IS NOT.**
- Not a scoping document — scoping happens through first-wave + second-wave work.
- Not authoritative for design decisions — those flow from first-wave findings + second-wave scoping.
- Not authoritative for the goal articulation — one session old; provisional; see §1 caveat.
- Not an exhaustive enumeration of anything — per non-exhaustive-listings discipline; lists are starters.

**Disposition discipline.** Logan is the disposition step (per harvest §10.1 assumption #1). Recommendations or findings produced by subagents are subject to Logan's disposition, not auto-executed.

**Calibrated-language register.** This initiative inherits arxiv-sanity-mcp's calibrated-language discipline (per LONG-ARC.md anti-pattern "Closure pressure at every layer"). Subagents writing in this space should default to calibrated language: "appears to" rather than "is"; "first-wave findings suggest" rather than "first-wave proves"; "operating frame" rather than "decided" for provisional positions.

**For decisions + recommendation-space**: `.planning/gsd-2-uplift/DECISION-SPACE.md`.
**For session dynamics**: `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md`.

## §1. Goal as articulated

Per Logan 2026-04-26 (deliberation log §3, recorded in DECISION-SPACE.md §1.2):

> "how do we make the harness & thus agential development more robust and better over much longer horizons of development (across multiple milestones / releases, also thinking about how release workflows, prod, dev, integrate with the gsd-2 framework), as codebases become more complex, as the salient determining conditions of the design situation change (constraints, stakeholder desires, reframes, changing requirements etc.). that is the primary aim, not 'can we squeeze these long-term guardrails into existing artifacts / docs / workflows etc.', that might be the desireable approach but it must be evaluated against this ultimate goal, to uplift GSD-2 to be the best it possibly can be across longer and longer development horizons."

**Terminology note — "harness".** In Logan's articulation, "harness" refers to the agent-development infrastructure assembly broadly: gsd-2 + Claude Code (or successor runtime) + dev tooling + organizational conventions that together support agential development. Not gsd-2 alone. The initiative's primary focus is uplift of gsd-2 specifically, but "harness" framing keeps the surrounding infrastructure in scope where it bears on long-horizon development quality.

**Provisional caveat.** This articulation is one session old. It has not been stress-tested; not been integrated with PROJECT.md / VISION.md; not been validated through fresh-session re-articulation or external review. Treat as operating frame, not authoritative goal. Validation mechanism is itself an open question (DECISION-SPACE §3.1).

## §2. Operating frame (as of 2026-04-26)

**Direction**: uplift gsd-2 (and the surrounding agent-development infrastructure) toward the goal in §1.

**Upstream relationship**: R2 (extension) as base + primary, contingent on first-wave finding gsd-2 has adequate extension surfaces (slice 4); R2+R3 hybrid (extension + upstream PRs) where workflow allows, contingent on gsd-2 maintainers being receptive to PRs; design must work even if all upstream PRs rejected; R1 (fork) as fallback only if R2 proves infeasible. See DECISION-SPACE §1.8 for full reasoning + change-conditions.

**Distribution shape**: separate project, separate repo (independent, valuable, reusable). Supports multiple onboarding situations (§3 below).

**Sequencing**: first-wave exploration (5-slice parallel-Explore dispatch, see DECISION-SPACE §1.4) → incubation checkpoint → second-wave scoping → design → build → test → adoption.

**Operating-frame is provisional.** This is the working position as of 2026-04-26, not a foreclosing decision. First-wave evidence may shift any of the items above (per §3.1 metaquestion + R2/R3 contingencies). See DECISION-SPACE §1.6 (scope-now with incubation checkpoint) for the operational discipline that protects against trajectory-momentum carrying forward without re-evaluation.

## §3. Open framing questions

**These are framing questions to inform first-wave exploration, not first-wave deliverables.** First-wave agents executing slices should be sensitive to evidence relevant to these questions and flag findings, but answering them definitively is second-wave work informed by first-wave outputs. The questions stay open across first-wave; the incubation checkpoint (DECISION-SPACE §2.3) revisits them after synthesis.

The list below is not exhaustive. First-wave exploration may surface additional framing questions; the list expands as evidence accumulates.

### §3.1 Is uplift-of-gsd-2 the right intervention shape?

Operating frame as of 2026-04-26: yes — Logan's articulation.

Non-exhaustive starter examples of direction-shifting evidence first-wave might surface:
- gsd-2 architecturally hostile to long-horizon features (no native extension surface for what we'd add).
- gsd-2's substrate (Pi SDK) doesn't expose extension points needed.
- gsd-2's release cadence or breaking-change policy makes third-party uplift untenable.
- gsd-2's mission/scope so divergent that uplifting it would distort its identity.
- First-wave surfaces a fundamentally simpler shape (e.g., "vanilla gsd-2 + project-level discipline conventions") that meets the goal more directly.

**First-wave agents**: this list is a starter, not a checklist. In addition to executing your slice, flag any direction-shifting evidence you encounter even if it doesn't match these examples.

If first-wave shifts this answer, direction reframes accordingly. Until then, second-wave proceeds on uplift-of-gsd-2.

### §3.2 What design shape — patcher, skills, hybrid?

Three candidate shapes (non-exhaustive):
- **Patcher**: a tool that modifies an existing gsd-2 install to add uplift features.
- **Skills**: uplift as a set of new skills (Claude Code skills or equivalent) that work alongside gsd-2.
- **Hybrid**: combinations across patcher + skills + documentation + tooling.

Choice depends on what gsd-2 actually exposes (first-wave slice 4) and what shape best supports the migration paths in §3.3. Decision deferred to second-wave informed by first-wave findings.

### §3.3 What onboarding situations does the uplift package support?

Logan's three (in-scope candidates, not exhaustive):
- Init with uplifted-gsd-2 (fresh project starts using the uplifted package).
- Already on gsd-2, wants uplift (adds uplift to existing gsd-2 install).
- On other-gsd-version, needs migration to uplifted-gsd-2.

Additional candidates surfaced this session (deliberation log §6, DECISION-SPACE §3.8):
- Raw Claude Code project with history (already has work, code, history; can't just init).
- Downgrade from uplifted-gsd-2 → vanilla gsd-2.
- Within-uplifted version migration (vN → vN+1).
- Evaluation/preview mode (show what would change before committing).
- Mixed-conventions consolidation (partial gsd-2 + custom planning, wants to consolidate).
- Selective uplift (opt out of specific uplift features).
- Multi-project organizational adoption (org-level distribution / config / standardization).

First-wave informs which are technically feasible; second-wave decides v1 supported set.

### §3.4 Is "long-horizon" the right framing axis?

Other axes might matter as much: complexity-scale, team-scale, risk-management, value-coherence. Logan's articulation prioritizes time-extension; first-wave + second-wave evaluate whether that's the dominant axis or one of several. Tied to §3.1 (is uplift the right shape).

### §3.5 What's the validation mechanism for the goal articulation?

The goal as articulated is provisional. Stress-testing path is itself open: re-articulation in fresh session + comparison; first-wave findings testing it indirectly; external review; eventual codification in dedicated uplift repo's VISION.md.

## §4. Inputs available

| Input | Trust level | Use |
|---|---|---|
| gsd-2 README (`github.com/gsd-build/gsd-2`) | high (verifiable, public, provided by Logan) | First-wave slices 1-5; ground truth on artifact set + auto-load semantics + migration tooling |
| Pi SDK (`github.com/badlogic/pi-mono`) | high (verifiable; gsd-2's substrate) | First-wave slice 2 investigates relationship |
| RTK (`github.com/rtk-ai/rtk`) | high (verifiable; gsd-2's CLI tooling) | First-wave slice 2-3 references |
| arxiv-sanity-mcp project-internal experience | medium (codifies real observed lessons) | LONG-ARC.md anti-patterns; METHODOLOGY.md disciplines; 005-008 spike-program drift case; the audit-cycle deliberations |
| Wave 5 outputs (α/β/γ/δ shapes per harvest §5 / §10.6; harvest §11 soft note; archived dispatch package) | low to medium (current-runtime-shaped; uplift-relevance is open) | Reference for what shapes Claude constructed during current-runtime governance work; not authoritative for uplift design. α = doctrine load-points map; β = anti-pattern self-check; γ = deliberation-boundary protocol; δ-pointer-note = forward-looking protected-seams change-control |
| Gemini deep-research doc + reading-notes | mechanism-accurate; framing-misaligned | Reference for gsd-2 mechanism descriptions only; framing on uplift question is misaligned per reading-notes |

*Trust labels follow the harvest §10.11 hierarchy: high (verifiable + provided/public + observable); medium (project-internal; codifies real observed experience); low (real but limited or contextual). "Low" means treat with calibrated skepticism, not ignore.*

## §5. First-wave exploration plan

Per DECISION-SPACE §1.4. Five-slice parallel-Explore dispatch with refined slicing covering 8 question-areas:

1. Mental model + mission + target user.
2. Architecture + runtime + Pi SDK relationship.
3. Workflow surface + automation + testing.
4. Artifact lifecycle + extension surfaces + migration tooling + distribution/install.
5. Long-horizon-relevant features + gaps + meta-evolution (gsd-2's own release cadence + breaking-change policy).

Pilot dispatch slice 1 first; review output; calibrate; then parallel dispatch slices 2-5. Setup: shallow-clone gsd-2 to a sibling location (e.g., `~/workspace/projects/gsd-2-explore/`).

Explorer prompts have not been drafted yet; per option D they pair with first-wave-dispatch decision. When dispatch is committed, prompts go at `.planning/gsd-2-uplift/exploration/0X-<slice>.md`; outputs at `.planning/gsd-2-uplift/exploration/0X-<slice>-output.md`.

After first-wave outputs are synthesized, an **incubation checkpoint** runs (DECISION-SPACE §2.3): re-read goal articulation, check direction-shifting evidence per §3.1 starter list and beyond, check whether R1/R2/R3 hybrid has narrowed, decide whether second-wave proceeds on current direction or re-disposition needed.

### §5.1 Guidance for first-wave subagents

When dispatched on a slice prompt:

- **Execute your assigned slice's questions** as defined in the prompt at `.planning/gsd-2-uplift/exploration/0X-<slice>.md`. Your primary deliverable is the slice summary, not answers to §3 framing questions.
- **In addition, surface any direction-shifting evidence relevant to §3.1 metaquestion** (and any other §3 question). The starter list in §3.1 is non-exhaustive; flag any evidence-type encountered even if it doesn't match the examples.
- **Use calibrated language**: state findings with confidence labels; mark what you read vs deliberately did not read; flag where README claims diverge from source observations.
- **Treat §3 framing questions as informing-context, not deliverables.** Don't try to answer them definitively in your slice output; flag relevant evidence and let synthesis + incubation checkpoint integrate.
- **Do not edit INITIATIVE.md or DECISION-SPACE.md directly.** If you encounter material that suggests these documents need updating (new framing question; missed input; contested decision), flag it in your output's "open questions surfaced" section.
- **Disposition discipline**: your findings are subject to Logan's disposition. Surface what you found; recommend what shifts the analysis suggests; do not auto-execute reframes.
- **Output structure** (per slice prompt; reproduced here for orientation): (i) what you read; (ii) calibrated findings; (iii) what you deliberately did not read (scope boundaries); (iv) open questions surfaced; (v) flags where README claims diverge from source observations.

## §6. What's NOT in scope yet

These are explicitly deferred to second-wave or later, not because they're unimportant but because pre-deciding them would foreclose framings that should remain open:

- Concrete design shape (patcher / skills / hybrid; §3.2 above).
- Migration architecture for the onboarding situations (§3.3).
- Reusability scope (which projects the package targets; §3.3 multi-project org case).
- Specific intervention surfaces in gsd-2 (depends on first-wave slice 4).
- gsd-2 uplift roadmap / milestone structure.
- Success criterion for v1 (open question per DECISION-SPACE §3.2).
- Audience specifics (solo / team / OSS / multi-project org; §3.3).
- Licensing / IP model (deferred until dedicated repo exists).
- Convergence with broader landscape of harness work (deferred to second-wave landscape check).

## §7. Migration trigger

When a dedicated repo for the uplift project is created, this artifact and its siblings under `.planning/gsd-2-uplift/` migrate there. The decision-space and the deliberation log stay in arxiv-sanity-mcp's `.planning/` (they record arxiv-sanity-mcp's session that genesised the initiative); INITIATIVE.md and exploration outputs migrate to the new repo as initiative-scoping artifacts.

STATE.md pending-todo updates at migration time to reflect the new home.

## §8. Cross-references

**Ground.**
- `.planning/gsd-2-uplift/DECISION-SPACE.md` — load-bearing decision reference; cite for "what was decided + why + what would change it."
- `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md` — session dynamics; cite for "how was this arrived at."

**Predecessor records.**
- `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md` — predecessor handoff.
- `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` — Wave 5 dispositions including §10.6 LONG-ARC/VISION integration shapes (current-runtime-scoped; α/β/γ/δ defined here) and §11 uplift soft note. §10.14 forward-references this initiative.
- `.planning/research/gemini-deep-research/READING-NOTES.md` — Gemini doc reading-notes.
- `.planning/deliberations/2026-04-25-recording-deliberations-extensively.md` — meta-deliberation establishing the deliberation-log discipline that this initiative-staging artifact and its sibling log instantiate.

**Project-level reference (transitive via DECISION-SPACE.md).**
- `.planning/LONG-ARC.md` — anti-patterns and calibrated-language register source.
- `.planning/VISION.md` — arxiv-sanity-mcp's product vision; relevant if uplift becomes a roadmap dependency.
- `.planning/spikes/METHODOLOGY.md` — interpretive lenses and practice disciplines (M1 paired-review at line 112; methodology home for codification per DECISION-SPACE §3.9 if/when triggered).

**Forthcoming.**
- Deferral commit (harvest §10.9 + §11 + dispatch package archival).
- Wave 5 commits 1-3 (AGENTS.md, CLAUDE.md, STATE.md).
- Optional post-Wave-5-execution handoff.
- Explorer prompts (5 slices) when first-wave dispatch is committed.

---

*Single-author fallibility caveat per DECISION-SPACE §0. This document stages the initiative forward; it does not authorize specific design decisions or roadmap commitments. Those flow from first-wave findings + second-wave scoping.*
