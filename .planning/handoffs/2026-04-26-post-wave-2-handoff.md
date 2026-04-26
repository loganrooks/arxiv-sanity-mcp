---
type: session-handoff
date: 2026-04-26 (revised, more thorough)
status: post-Wave-2-synthesis
predecessor: .planning/handoffs/2026-04-25-v0.2-plan-handoff.md
revision_note: |
  First version of this handoff (committed 48029c3) was deemed insufficiently
  thorough. This revision expands every section, captures rationale (not just
  decisions), surfaces tensions, corrects the mid-horizon framing per Logan's
  2026-04-26 clarification (gsd-2 uplift initiative is project-agnostic,
  not just migration), and is intended to fully restore context for any
  future session reading it cold.
---

# Handoff — Post Wave 2 Synthesis (Comprehensive)

This document is the durable record of: (a) what's been done in the v0.2 plan-revision and governance-audit cycles; (b) what's pending and why; (c) decisions made and the rationale behind each; (d) the corrected mid-horizon framing; (e) tensions and choice-points surfaced for Logan; (f) recommended sequencing; (g) what the next session should and should not do.

If you are reading this cold (fresh session), read it in order — sections build on each other.

## 1. Where we are right now

**Date:** 2026-04-26 evening (or any session after).

**Branch:** `spike/001-volume-filtering` (10+ commits ahead of origin; not pushed).

**Active work:** v0.2 multi-lens substrate planning. Two paired audit cycles complete:
- v0.2 plan paired audit cycle (2026-04-25): targets v0.2 plan documents.
- Governance-doc paired audit cycle (2026-04-26): targets ADRs 0001-0004, AGENTS.md, CLAUDE.md, REQUIREMENTS outside v0.2, ROADMAP outside Phases 12-17, STATE.md, foundation-audit notes, ECOSYSTEM-COMMENTARY.

Both cycles have produced: cross-vendor + same-vendor xhigh audits → comparison → synthesis. The v0.2 cycle's synthesis was revised (see §3); the governance cycle's synthesis is draft-pending-exemplar-review-and-Logan-decisions.

**Wave 1 commits landed** (v0.2 synthesis Adopt-now items: A1-A7 + M1 methodology amendment).

**Wave 2 is complete** (governance-doc paired audit cycle).

**Wave 3 has NOT started** (v0.2 synthesis B-tier + C-tier + D2 commits, post-governance-audit).

**Wave 4 has NOT started** (governance synthesis Adopt-now + with-shape commits).

**Phase 12 plan 1 authoring is BLOCKED** (decision: gsd-2 uplift initiative precedes Phase 12 to avoid wasted authoring work; see §6 for the corrected mid-horizon framing).

## 2. Artifact inventory

### v0.2 plan audit cycle artifacts (2026-04-25)

| Artifact | Path | Status |
|---|---|---|
| Cross-vendor audit | `.planning/audits/2026-04-25-v0.2-plan-audit-cross-vendor.md` | Complete |
| Same-vendor xhigh audit (original, contaminated) | `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial-xhigh-contaminated.md` | Complete; flagged contaminated; superseded |
| Same-vendor xhigh audit (independent rerun) | `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial-xhigh.md` | Complete; primary |
| Same-vendor high audit (original) | `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md` | Complete; secondary |
| Comparison | `.planning/audits/2026-04-25-v0.2-plan-audit-comparison.md` | Complete |
| Synthesis (revised with dispositions) | `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md` | Revised at commit 931bca1; operative dispositions document |
| Paired-audit prompt package | `.planning/audits/2026-04-25-v0.2-paired-audit-package/` | Reference |

### Wave 1 commits (executed v0.2 synthesis Adopt-now items)

| SHA | Description |
|---|---|
| `d0d860c` | A1+A2 — `lens=` default reconciled; multi-value semantics specified at ADR-0005 |
| `5a4adb0` | A3 — Phase 17 multi-attribution capture + change-control rule |
| `07415af` | A4 — Phase 14 spike pre-registered decision matrix + content-presence verification |
| `5501cc4` | A5+A6+A7 — critical-path correction; backward-compat ripple scope; anti-pattern phase-boundary checkpoints |
| `020b5d1` | M1 — METHODOLOGY discipline A independent-dispatch sub-discipline (Hypothesis status) |

### Wave 2 governance audit cycle artifacts (2026-04-26)

| Artifact | Path | Status |
|---|---|---|
| Paired-audit prompt package | `.planning/audits/2026-04-26-governance-paired-audit-package/` | Committed `36d70b0` |
| Cross-vendor audit | `.planning/audits/2026-04-26-governance-audit-cross-vendor.md` | Recovered from codex JSONL after `-o` flag overwrite (see §9 for the codex pitfall); committed `d30a974` |
| Same-vendor xhigh audit | `.planning/audits/2026-04-26-governance-audit-opus-adversarial-xhigh.md` | Complete; committed `d30a974` |
| Comparison | `.planning/audits/2026-04-26-governance-audit-comparison.md` | Committed `51abefc` |
| Synthesis (draft) | `.planning/audits/2026-04-26-governance-audit-synthesis.md` | Committed `51abefc`; status: draft-pending-exemplar-review-and-Logan-decisions |

### Other relevant artifacts

| Artifact | Path | Notes |
|---|---|---|
| First handoff (post-v0.2-audit) | `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md` | Predecessor; partly superseded by this revision |
| Custom subagent definition | `~/.claude/agents/adversarial-auditor-xhigh.md` | The grounded-critic subagent used for both same-vendor xhigh dispatches |
| METHODOLOGY (with M1) | `.planning/spikes/METHODOLOGY.md:112` | M1 codified at line 112; Hypothesis status; second test reinforced status (Wave 2 cycle) |
| Project root CLAUDE.md | `CLAUDE.md` (project root) | Auto-loaded as runtime instructions; identified by both governance audits as stale |
| Auto-memory | `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/memory/MEMORY.md` | Persists across sessions |

## 3. Decisions made (and why)

The two cycles produced significant decisions that should not be re-litigated absent new evidence.

### v0.2 cycle decisions

**Adopt now (Wave 1, executed):** A1-A7 + M1.
- A1 (reconcile `lens=` default across docs): convergent across all 4 audits; silent-defaults anti-pattern operationalized at document layer.
- A2 (multi-value `lens=` per-lens-dict default): silent-default-by-absence; first implementer's choice would become de facto API.
- A3 (Phase 17 multi-attribution capture + change-control rule): "lens-of-record" formulation pre-committed pilot's analysis to single-lens attribution; that's the tournament framing 008 was superseded for.
- A4 (Phase 14 pre-registered decision matrix): METHODOLOGY discipline B + Bayesian lens require pre-registered priors and decision rules; without matrix, post-hoc sunk-cost-bias toward "this is sufficient."
- A5 (critical-path correction): the previously-stated path was under-specification.
- A6 (backward-compat ripple scope): cross-vendor's coverage finding; same-vendor audits read at architectural layer and missed consumer-impact layer.
- A7 (anti-pattern phase-boundary checkpoints): vigilance is what failed in 005-008; mitigating recurrence with vigilance recapitulates the failure mode; structural counter-posture is phase-boundary checkpoints.
- M1 (independent-dispatch sub-discipline, Hypothesis status): the contaminated-vs-independent xhigh comparison documented finding-suppression and frame-inheritance effects of contaminated dispatch.

**Adopt with shape (Logan dispositioned 2026-04-26, in `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md`):**
- B1: shape (a) defer with explicit non-decision — cost asymmetry of breaking change vs hypothetical risk.
- B2: shape (a) inline "Considered and rejected" subsection in ADR-0005 — ADRs are canonical commit; deliberation docs harder to find.
- B3: **flipped to shape (b)** defer storage criteria to Phase 14 plan 2 PLAN.md — milestone-layer commits to "rationale recorded"; criterion-of-criterion is creep.
- B4: ROADMAP edit only, no LPILOT-04 — tripartite is implementation-of LPILOT-02/03, not its own commitment.

**Deliberate (Logan dispositioned 2026-04-26):**
- C1: **flipped to skip both** Provisional relabel AND lighter audit_synthesis frontmatter pointer — substantive remediation is the commit checklist itself; frontmatter-pointer is register-marker churn the team's own discipline D cautions against.
- C2: **narrowed** to 1 instance (VISION.md:34 header + :36 clause) — broader pass would itself recapitulate closure-pressure pattern at the meta-layer.
- C3: **narrowed** to architectural-commitments list (MILESTONE.md:14-20) only, NOT success-criteria list — different lists do different work; only commitment list benefits from status markers.

**Defer (Logan dispositioned 2026-04-26):**
- D1: METHODOLOGY scope-creep edits — opportunistic later edit when METHODOLOGY is next edited.
- D2: **promoted to adopt-now** LONG-ARC explicit profile elicitation seam — converts deferral-protection into mechanism-protection at doctrine layer; protects v0.3+ surface even though no v0.2 phase implements behavior-derived signals.

**Drop (uncontested):** N1 (B/C overlap finding), N2 (broader rhetorical-pass-everywhere ambition).

### Governance cycle decisions (in `.planning/audits/2026-04-26-governance-audit-synthesis.md`)

**Adopt now (5 commits planned for Wave 4):**
- G-A1: STATE.md refresh (resolve 23-vs-31 plan count; remove "Pending Todos: None"; update session continuity; remove "Phase 6 next" framings) + bundled small fixes (ROADMAP Phase 2 success criteria; ROADMAP audit-citation reframe; REQUIREMENTS.md MCP-07 reframe).
- G-A2: CLAUDE.md (project root) minimal currency update — fix tool count (10→13), test count (~493), milestone (v0.2 active not Phase 6 next). Structural restructuring deferred to exemplar review.
- G-A3: ADR-doctrine pass — re-verify ADR citations against ADR text in LONG-ARC.md, MILESTONE.md, ADR-0005. Specific instances: MILESTONE.md:103 "binding"; ADR-0005:9 "as a binding posture" addition; LONG-ARC.md:46 "coexistence intent" paraphrase.
- G-A4: Foundation-audit closeout matrix in FINDINGS.md.
- G-A5: Pending-validation tracker (Q1, Q4, Q16) moved to STATE.md.

**Adopt with shape (Logan needs to disposition):**
- G-B1: ECOSYSTEM-COMMENTARY status annotations — shape (a) inline status table or (b) explicit deprecation pointer.
- G-B2: ADR-0005 reframe shape — shape (a) minimal one-sentence reframe (already in G-A3) or (b) explicit ~100-word subsection.
- G-B3: v2-deferred technology-name reframe — shape (a) capability-with-illustrative or (b) full removal of tech names.
- G-B4: Per-phase ADR-against-plan audit operational hook — shape (a) document the practice, (b) propose ADR-0006, or (c) defer to gsd-2 uplift. **Recommended (c)** to avoid arxiv-sanity-mcp-specific convention conflicting with project-agnostic uplift design.

**Structural (3 commits planned for Wave 4):**
- G-S1: Governance read-order map (added to CLAUDE.md as a small section; map can move to separate file later if CLAUDE.md restructured per exemplar review).
- G-S3: Deliberation directory index at `.planning/deliberations/INDEX.md`.
- G-S4: Methodology-document relationship note (cross-reference between foundation-audit/METHODOLOGY.md and spikes/METHODOLOGY.md).

**Deferred pending exemplar review (Wave 5):**
- G-D1: AGENTS.md "Known difficulty patterns" section.
- G-D2: AGENTS.md own ADR-citation example fix (misquotes ADR-0001 in the very example teaching the discipline).
- G-D3: CLAUDE.md restructuring (minimal pointer or full content?).
- G-D4: CLAUDE.md "Stack trajectory: Not Stack D" silent-default fix.

**Deferred to gsd-2 uplift initiative:**
- G-U1: Per-phase ADR-against-plan audit operational hook (recommended shape c above).
- G-U2: Post-audit follow-through convention as a workflow primitive.

**Drop:** G-N1 (ADR alternatives sections — taste, ADR genre appropriate as-is), G-N2 (ADR-0001 inheritance-rejection framing — preemptive), G-N3 (ADRs 0002-0004 common-misuses preemption — no observed misuse).

### Methodology decisions (M1 status)

M1 (independent-dispatch sub-discipline) was codified at `METHODOLOGY.md:112` in commit `020b5d1` with status `Hypothesis`. The Wave 2 governance audit cycle was M1's second test. The comparison documented:
- Structural divergence between paired audits (different dimension structures; CV produced 24 atomic findings, SV produced 17 multi-paragraph findings; different finding tiers).
- Substance convergence on the strongest doctrinal issues (12 of 25 issues strongly convergent).

This is the divergence-on-framing-with-convergence-on-substance pattern paired review is supposed to produce. **M1 status reinforced but not confirmed** (single comparison reinforces; multiple cycles required for confirmation). Status remains `Hypothesis`.

The synthesis recommends a one-line note added to METHODOLOGY.md at Wave 4 commit time documenting the second test result.

## 4. Pending Logan decisions

Before Wave 3 (v0.2 synthesis remaining commits) can proceed, Logan needs to confirm dispositions on B-tier and D2 (already dispositioned in the v0.2 synthesis revision; the revision itself records Logan's preferences). The Wave 3 commits are ready to execute on confirmation.

Before Wave 4 (governance synthesis Adopt-now + with-shape) can proceed, Logan needs to disposition:
- G-B1 shape (a) inline status table or (b) explicit deprecation pointer for ECOSYSTEM-COMMENTARY
- G-B2 shape (a) minimal one-sentence ADR-0005 reframe or (b) explicit ~100-word subsection
- G-B3 shape (a) capability-with-illustrative or (b) full removal for v2 technology naming
- G-B4 shape (a) lightweight document the practice, (b) propose ADR-0006, or (c) defer to gsd-2 uplift (recommended)

Before Wave 5 can proceed, Logan needs to provide exemplar AGENTS.md / CLAUDE.md files (and ideally a brief explanation of which principles he wants to harvest).

Before mid-horizon work can proceed, Logan needs to confirm the corrected mid-horizon framing (see §6) and decide on Phase 12 timing tension (see §7).

## 5. Tensions surfaced

These are choice-points the next session should preserve as choice-points, not flatten into decisions.

### Tension 1: Wave 3 vs Wave 4 ordering

Both waves touch overlapping documents (ADR-0005, MILESTONE.md, LONG-ARC.md). The synthesis recommended Wave 3 lands first. This is the lower-entropy choice; Wave 3 commits are scoped to v0.2 plan revisions (smaller blast radius), and Wave 4's governance edits don't conflict with Wave 3's because they touch different parts of the documents. But Logan could choose to bundle some Wave 3 + Wave 4 commits together (e.g., G-A3 ADR-doctrine pass and v0.2 B2 Considered-and-rejected subsection both touch ADR-0005). Bundling reduces commit count; not-bundling preserves atomic disposability.

### Tension 2: Phase 12 timing vs gsd-2 uplift duration

Phase 12 plan 1 authoring depends on gsd-2 evaluation per Logan's 2026-04-26 decision (gsd-2 changes how phases are authored). But the gsd-2 work is not "evaluate and migrate" — it's the substantial uplift initiative (see §6). If the uplift takes weeks/months, Phase 12 sits idle for that long.

Three resolution shapes:
- **(a)** Strict serial: gsd-2 uplift completes (or reaches a usable milestone) before Phase 12 plan 1 authoring begins. Cleanest substrate; longest delay.
- **(b)** Phase 12 in current GSD; migrate at natural breakpoint accepting some authoring rework. Faster delivery; some wasted work.
- **(c)** gsd-2 evaluation only (just enough to know the migration shape) before Phase 12; defer full uplift initiative to after v0.2 ships. Phase 12 authored against current GSD with foreknowledge of gsd-2 conventions; lower wasted work than (b), faster than (a).

Logan's 2026-04-26 statement suggests (a) ("gsd-2 changes how the phase might be authored... we would need to deliberate and think about that before moving on"). But the corrected mid-horizon framing makes the uplift initiative substantially larger than Logan's initial statement suggested. Worth re-confirming.

### Tension 3: Comparison §4 / §5 joint blind spots

Both governance audits acknowledged scope bounds. Joint blind spots include source-code-vs-doctrine alignment, `docs/templates/`, PROJECT.md as audit target, spike artifacts beyond METHODOLOGY.md, quick-task substrate, `docs/05-08`, and the user's `~/.claude/CLAUDE.md`. None of these were flagged as critical, but they remain open as candidates for a future audit cycle if any become load-bearing.

### Tension 4: Wave 4 commits before or after exemplar harvest?

Wave 4 (governance Adopt-now + with-shape, Structural) does not depend on exemplar review. Wave 5 (deferred-pending-exemplar AGENTS/CLAUDE substantive edits) does. The synthesis recommends Wave 4 lands before Wave 5; this is correct. But Logan could choose to do exemplar harvest first if it might affect the AGENTS/CLAUDE-touching decisions even at the Wave 4 layer (e.g., G-A2 CLAUDE.md minimal currency might land differently if exemplar review suggests a wholesale restructure). Recommended: keep G-A2 minimal-currency as-planned (Wave 4) and let exemplar review drive the structural restructuring (Wave 5 G-D3).

## 6. Mid-horizon framing (corrected per Logan 2026-04-26)

The first handoff (`48029c3`) framed mid-horizon as "gsd-2 evaluation → migration → long-term integration design." Logan corrected this on 2026-04-26: the mid-horizon is **substantially bigger and project-agnostic**.

### What the mid-horizon initiative is

A standalone initiative to **uplift gsd-2** with long-horizon planning capacity, integrating governance documents (LONG-ARC.md, VISION.md, and other long-arc artifacts) into gsd-2's workflow as a project-agnostic capability. The goal is not migration of arxiv-sanity-mcp's planning to gsd-2 — that's a downstream consequence. The goal is **a generally-useful enhanced gsd-2 that any project can use to plan within longer horizons**.

### Concrete deliverable shape

**An automated patcher repo.** A separate repo whose job is to take gsd-2 (vanilla) and apply the long-horizon-uplift patches. The patcher should handle multiple starting states:
- Project has gsd-2 already installed (just apply the patches)
- Project has no harness installed (install gsd-2 + apply patches)
- Project has existing governance docs (a vision doc, an architecture doc) that should seed the uplift's onboarding (Q&A-based document creation seeded from existing material)
- Project is greenfield (no existing docs; pure Q&A-based creation)

Once the patcher exists, any of Logan's projects (and other people's projects) can use the enhanced+uplifted gsd-2 to plan within long-arc horizons.

### Intervention surfaces (initial inventory; not exhaustive)

The uplift needs to intervene on multiple gsd-2 surfaces. Initial list (Logan's surfacing 2026-04-26):

1. **Workflows that create governance documents.** Currently gsd-2's workflows create ROADMAP, REQUIREMENTS, phase plans, etc. The uplift adds workflows that create LONG-ARC, VISION, and other long-arc-shaped documents. These workflows should be Q&A-based and capable of seeding from existing project material (if a project already has a vision doc, the workflow uses it as input rather than starting from scratch).

2. **Onboarding / initialization.** When uplifted gsd-2 is first installed in a project, what's the first-run experience? Likely a Q&A flow that produces the initial governance doc set. Should be smart about detecting existing material and offering to seed from it.

3. **Roadmapping-equivalent agent for LONG-ARC.md.** gsd-2 has roadmapping (creating ROADMAP from milestones). The uplift may need an agent that mirrors this for LONG-ARC.md — i.e., creating long-arc planning artifacts from project doctrine and product identity.

4. **Other intervention points TBD.** The full intervention surface needs design work. The audits (CR1-CR5) actually surface several mid-horizon-relevant patterns:
   - CR1 (calibration drift) suggests the uplift's plan-authoring workflows should verify ADR citations against ADR text at workflow time.
   - CR2 (post-audit follow-through) suggests the uplift should bake post-audit follow-through into a workflow primitive (G-U2 in the governance synthesis).
   - CR3 (governance read-order map) suggests the uplift should ship with a canonical document map and / or a workflow that generates one.
   - CR5 (ADR-doctrine drift) suggests the uplift should have an ADR-against-current-work review workflow as a phase boundary checkpoint (G-U1 in the governance synthesis; SV D2 surfaced this).

The arxiv-sanity-mcp audits are themselves a useful test case for what the uplift needs to handle — an existing project with mature governance docs that has nonetheless drifted in well-characterized ways.

### Why project-agnostic matters

If the uplift is arxiv-sanity-mcp-specific, it's just bespoke planning automation for one project. That's not what Logan wants. The uplift is meant to be useful across all of Logan's projects (and possibly others) — which means the design has to abstract over project shape, vision doc presence/absence, existing governance set state, etc. That abstraction is the hard part of the work.

### Inputs to the design work

- The Gemini 3.1 Pro Deep Research thread Logan ran on this: `https://gemini.google.com/share/326970d0fa1b`. Use as input to the **long-term integration design** session (not as pre-decided output).
- gsd-2 repo: `https://github.com/gsd-build/gsd-2`. Read first; understand the workflow surfaces and intervention points.
- gsd-to-gsd2 migration skill (Logan mentioned it exists). Use as reference for how migration mechanics work; the uplift might extend or replace this.
- The arxiv-sanity-mcp governance docs themselves (LONG-ARC.md, VISION.md, METHODOLOGY.md, etc.) as exemplars of long-arc-shaped documents the uplift should support.
- The audit synthesis dispositions (especially G-U1 and G-U2) as concrete features the uplift should provide.

### Mid-horizon sequencing (recommended)

1. **gsd-2 evaluation.** Read repo; understand workflow primitives, plan format, verification model, directory structure. Produce a deliberation document characterizing gsd-2 vs current GSD vs the uplift target. Likely outputs: deliberation doc; possibly an ADR-0006 if the v0.2 → v0.3 transition needs to commit to gsd-2.
2. **Long-term integration design.** Use Gemini Deep Research as input. Question: how do governance docs feed into uplifted gsd-2 workflows? What intervention surfaces exist? What should the patcher's API be? Likely outputs: design document; intervention-point inventory; abstract intervention strategy.
3. **Patcher repo bootstrapping.** Create the patcher repo. Implement initial intervention surfaces (probably starting with Q&A-based governance-doc creation since that's the most foundational). Test against arxiv-sanity-mcp as a real-world existing project case.
4. **arxiv-sanity-mcp uplift.** Apply the patcher to arxiv-sanity-mcp. Verify governance docs integrate with workflows. This is the first real-world test.
5. **Phase 12 plan 1 authoring** under uplifted gsd-2. The actual v0.2 implementation work resumes.

This sequencing puts arxiv-sanity-mcp Phase 12 substantially after the uplift work. Logan should re-confirm whether this delay is acceptable or whether tension 2's resolution should be (b) or (c) instead.

## 7. Recommended sequencing (consolidated)

### Wave 3 — v0.2 synthesis B-tier + C-tier + D2 (executable now if Logan confirms dispositions)

Per `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md` §9, Wave 3 is:

8. Plan-revision commit 5 (ADR-0005 + VISION + MILESTONE register): B2 + C2 + C3
9. Plan-revision commit 6 (LONG-ARC doctrine seams): B1 + D2
10. Plan-revision commit 7 (Phase 17 reporting): B4

### Wave 4 — governance synthesis Adopt-now + with-shape + Structural

Per `.planning/audits/2026-04-26-governance-audit-synthesis.md` §8, Wave 4 is 9 commits:

1. STATE.md refresh + bundled small fixes (G-A1 + row 19 + row 22 + row 10)
2. CLAUDE.md minimal currency (G-A2)
3. ADR-doctrine pass (G-A3)
4. Foundation-audit closeout (G-A4 + G-A5)
5. ECOSYSTEM-COMMENTARY status (G-B1, Logan's shape)
6. v2 tech-naming reframe (G-B3, Logan's shape)
7. Governance read-order map (G-S1)
8. Deliberation index (G-S3)
9. METHODOLOGY relationship note (G-S4) + M1 second-test annotation (synthesis §9)

Wave 4 lands after Wave 3 to avoid commit conflicts on shared documents.

### Wave 5 — exemplar harvest + AGENTS/CLAUDE deferred dispositions

10. Exemplar harvest session (Logan provides exemplar AGENTS.md / CLAUDE.md files; abstract principles; recommendations doc)
11. Wave 4 synthesis revision (incorporates exemplar findings; confirms G-D1 through G-D4)
12. Wave 5 commits (AGENTS.md / CLAUDE.md restructuring per revised dispositions)

### Wave 6+ — mid-horizon initiative (gsd-2 uplift)

Per §6 above. Substantial standalone initiative; multi-session scope.

### Phase 12 plan 1 authoring

Deferred until §7 mid-horizon resolution chosen (a/b/c per Tension 2). Default assumption: option (a) — Phase 12 waits for uplift to reach a usable milestone.

## 8. Recommended natural break points (handoff opportunities)

| Break point | Rationale |
|---|---|
| **Right now (after this commit)** | Cleanest break. Wave 2 fully closed; Wave 3 ready to execute on Logan's confirmation; Wave 4 ready on Logan's dispositions. A fresh session can pick up either wave's commits with this handoff alone. |
| After Wave 3 commits | If Logan wants to land Wave 3 in the current session before breaking. |
| After Wave 4 commits | Same. Wave 4 has 9 commits; substantial. |
| After exemplar harvest | Before Wave 5 commits. |
| After Wave 5 commits | Before mid-horizon initiative. Major breakpoint — mid-horizon is substantially different work. |
| Within mid-horizon: after gsd-2 evaluation | Before long-term integration design. |
| Within mid-horizon: after long-term integration design | Before patcher repo bootstrap. |
| Within mid-horizon: after patcher repo first version | Before arxiv-sanity-mcp uplift. |

Logan's preference recorded 2026-04-26: pause / compact at the **right-now** break point. This handoff is the durable record.

## 9. Methodology lessons learned (this audit cycle)

These are operational lessons from doing the two audit cycles. Worth preserving for the next paired-audit cycle.

### Codex CLI dispatch pitfall

`codex exec --output-last-message <file>` overwrites `<file>` with the agent's final chat message at process exit. If the agent uses `apply_patch` to write content to `<file>` during the run, that content is clobbered. **Don't co-locate the agent's write target with `-o` capture path.** Either:
- Have the agent write to one path and `-o` capture the agent message to a different path
- Skip `-o` entirely and recover audit content from the codex output stream / session JSONL

The Wave 2 cross-vendor audit hit this; recovery from `~/.codex/sessions/...rollout-*.jsonl` worked (the apply_patch input is preserved in the session JSONL even when the file on disk is clobbered). Use `jq -r '.payload | select(.type=="custom_tool_call" and .name=="apply_patch") | .input'` to extract.

### Subagent dispatch protocol that worked

The `adversarial-auditor-xhigh` custom subagent at `~/.claude/agents/adversarial-auditor-xhigh.md` works well for same-vendor xhigh dispatch. The subagent definition handles model+effort; the prompt handles task specifics. Both Wave 2 and the v0.2 cycle's independent xhigh used this pattern.

The write-first protocol (first tool call must be `Write`; last tool call must be `Bash ls -la`) prevents the agent from confabulating "system reminder said don't write" — which happened in the v0.2 cycle's first xhigh dispatch. Both Wave 2 and the independent xhigh dispatch honored the protocol; both files appeared on disk.

### Forbidden-reading list discipline (M1)

Both Wave 2 dispatches honored the forbidden-reading list. Compliance is verifiable in tool-use traces (the agents' Read calls don't reference forbidden paths). This is the second test of M1; it reinforces the discipline's Hypothesis status.

The cost of the forbidden-reading discipline is trivial (~10-20 lines added to each prompt). The benefit is measurable in the comparison's structural divergence (different dimension structures, different finding granularities) — which is what paired review is supposed to produce.

### Comparison vs synthesis as separate artifacts

Both v0.2 and Wave 2 cycles produced comparison and synthesis as separate artifacts. The comparison is mechanical (map findings to each other; identify convergent risks; surface divergences). The synthesis is decision-focused (tier dispositions; propose edits; sequence commits). Splitting them keeps each artifact focused.

The comparison is much shorter than the synthesis (~150-300 lines vs ~400-500 lines).

### Synthesis is single-author and fallible

Both synthesis documents are single-author. The v0.2 synthesis was revised after Logan's dispositions, and the revision flipped multiple dispositions (B3, C1) and narrowed others (C2, C3) and promoted one (D2 from defer to adopt-now). This is evidence that single-author synthesis is fallible at the disposition layer.

Recommended posture: synthesis dispositions should be treated as recommendations, not commitments. Logan's review and disposition is the actual decision step.

### Auto-summary leakage from background subagents

When a subagent is dispatched in background and completes, the dispatching session receives an auto-summary of the agent's findings. This leaks the agent's findings into the dispatching session's context, which can bias subsequent work in the dispatching session.

Mitigation: do comparison and synthesis in a fresh session (not the dispatching session). The Wave 2 case partially violated this (comparison and synthesis happened in the dispatching session); the comparison's §4 documents this self-aware-of-bias and the synthesis writes from a clean reading of both audits. But cleaner sessions for synthesis are still preferred.

## 10. What the next session should NOT do

- **Do not skip the comparison and go straight from audits to synthesis.** Comparison is a separate analytical step; bundling it loses the convergence-matrix artifact.
- **Do not bolt exemplar AGENTS/CLAUDE harvest onto the Wave 2 audit as an addendum.** Treat as separate deliverable. Paired audits are paired by structure (cross-vendor + same-vendor independent); single-author addendum would muddy the audit's epistemic provenance.
- **Do not start Phase 12 plan 1 authoring before mid-horizon resolution.** Logan decided 2026-04-26 that gsd-2 changes how phases are authored; authoring against current GSD then redoing post-uplift is wasted work. The mid-horizon initiative may take time; Phase 12 waits.
- **Do not begin the gsd-2 uplift initiative as part of this audit cycle.** It's a substantial standalone initiative; should land after Wave 5 (exemplar harvest + AGENTS/CLAUDE deferred dispositions) to avoid substrate-changing while dispositions are being executed.
- **Do not let the Gemini Deep Research thread anchor the gsd-2 evaluation.** It's input to the **long-term integration design** (mid-horizon item 2), not the gsd-2 evaluation itself. The evaluation should read gsd-2 directly first.
- **Do not re-litigate Wave 1 commits.** A1-A7 + M1 are settled. New evidence could prompt revision; absent new evidence, they stand.
- **Do not re-litigate Logan's dispositioned items.** B-tier + C-tier + D2 in v0.2 synthesis are dispositioned. The Wave 3 commits execute them on Logan's confirmation. If new evidence emerges (e.g., from Wave 2 governance audit findings affecting v0.2 doctrine claims), the v0.2 synthesis can be re-revised, but absent that, dispositions stand.
- **Do not commit the governance synthesis's deferred-pending-exemplar items in Wave 4.** Those wait for Wave 5. Doing them in Wave 4 forecloses the exemplar harvest's recommendations.
- **Do not skip the "pre-flight check" for the Wave 4 commits.** Several Wave 4 edits depend on facts that should be verified at edit time (current tool count via tests; current test count via pytest; correct STATE.md velocity numbers). Don't propagate stale numbers.
- **Do not assume the AGENTS.md own example misquote (G-D2) is small.** It's the document teaching the discipline of accurate ADR-citation, and its example misquotes ADR-0001. The fix is small but the symbolic significance is large; treat it as worth doing carefully when Wave 5 lands.
- **Do not co-locate codex agent's write target with `-o` capture path** (see §9 Methodology lessons).

## 11. Cross-references

- v0.2 synthesis (operative dispositions): `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md`
- v0.2 comparison: `.planning/audits/2026-04-25-v0.2-plan-audit-comparison.md`
- Wave 2 governance synthesis: `.planning/audits/2026-04-26-governance-audit-synthesis.md`
- Wave 2 governance comparison: `.planning/audits/2026-04-26-governance-audit-comparison.md`
- Original handoff (this document supersedes): `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md`
- M1 discipline: `.planning/spikes/METHODOLOGY.md:112` (Hypothesis status; reinforced by Wave 2 cycle)
- METHODOLOGY full doc: `.planning/spikes/METHODOLOGY.md`
- LONG-ARC: `.planning/LONG-ARC.md`
- VISION: `.planning/VISION.md`
- ADR-0005 (multi-lens substrate, the v0.2 architectural commit): `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
- v0.2 milestone: `.planning/milestones/v0.2-MILESTONE.md`
- ROADMAP (post-Wave 1 edits): `.planning/ROADMAP.md`
- REQUIREMENTS (post-Wave 1 edits): `.planning/REQUIREMENTS.md`
- STATE.md (current, but stale per governance audit; refresh in Wave 4): `.planning/STATE.md`
- CLAUDE.md (project root, stale per governance audit; minimal-currency fix in Wave 4): `CLAUDE.md`
- AGENTS.md (project root; substantive edits deferred to Wave 5): `AGENTS.md`
- Foundation-audit findings: `.planning/foundation-audit/FINDINGS.md`
- Foundation-audit methodology: `.planning/foundation-audit/METHODOLOGY.md`
- ECOSYSTEM-COMMENTARY: `.planning/ECOSYSTEM-COMMENTARY.md`
- Auto-memory: `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/memory/MEMORY.md`
- gsd-2 repo (mid-horizon target): `https://github.com/gsd-build/gsd-2`
- Gemini Deep Research thread (mid-horizon design input): `https://gemini.google.com/share/326970d0fa1b`
- Custom subagent definition (used in both same-vendor xhigh dispatches): `~/.claude/agents/adversarial-auditor-xhigh.md`

## 12. Quick-reference: commit SHAs

In chronological order on `spike/001-volume-filtering`:

| SHA | Description |
|---|---|
| ca7e568 | docs(audits): synthesize v0.2 plan audit findings into tiered plan revisions (original) |
| 931bca1 | docs(audits): revise v0.2 plan synthesis with dispositions and 3-wave sequencing |
| d0d860c | docs(v0.2): reconcile lens= default and specify multi-value semantics (A1+A2) |
| 5a4adb0 | docs(v0.2): Phase 17 multi-attribution capture and change-control rule (A3) |
| 07415af | docs(v0.2): pre-registered decision matrix for OpenAlex coverage spike (A4) |
| 5501cc4 | docs(v0.2): milestone-level corrections (A5+A6+A7) |
| 020b5d1 | docs(methodology): independent-dispatch sub-discipline (M1, Hypothesis) |
| 36d70b0 | docs(audits): governance-doc paired audit package (Wave 2) |
| d30a974 | docs(audits): record Wave 2 governance-doc paired audit outputs |
| 51abefc | docs(audits): governance audit comparison + synthesis (Wave 2 closure) |
| 48029c3 | docs(handoff): post-Wave-2 audit handoff with locked-in plan (this revision supersedes) |

(Plus this commit, which will revise the handoff above.)

## 13. The single highest-priority action for the next session

**Confirm the handoff captures everything correctly with Logan, then either:**
- (a) execute Wave 3 commits (v0.2 B-tier + C-tier + D2) in the current session if context allows, or
- (b) handoff to a fresh session that starts with this document, then executes Wave 3.

Wave 3 is the lowest-friction next step: dispositions are recorded; commits are scoped to specific document edits; no exemplar dependency; no gsd-2 dependency. Wave 4 follows once Logan dispositions G-B1 through G-B4 in the governance synthesis. Wave 5 follows once Logan provides exemplar AGENTS/CLAUDE files. Mid-horizon (gsd-2 uplift) follows Wave 5.

Phase 12 is at the end of the queue. That's intentional — getting the substrate right matters more than getting Phase 12 started fast.
