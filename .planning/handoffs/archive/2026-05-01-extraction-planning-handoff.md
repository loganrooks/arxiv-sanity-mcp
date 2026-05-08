---
type: extraction-planning-handoff
date: 2026-05-01
status: small + temp; written for the planning-stage session that produces the extraction plan
purpose: |
  Onboard a fresh-context Claude (at /effort max) into the task of PLANNING
  the extraction of gsd-2-uplift work into its own repo + the cleanup of
  arxiv-sanity-mcp. This handoff is not the plan; it enables the plan.
  Subject to deletion or archival after the extraction plan is committed and
  executed.
audience: fresh-context Claude in next session, /effort max, planning-not-executing
not_a_plan: |
  This is a HANDOFF for the planning stage. The PLAN is what the next session
  produces. The plan should be detailed + thorough; this handoff is small +
  scoped to onboarding.
---

# Extraction-planning handoff

## §0. What just happened (one paragraph)

The gsd-2-uplift work has accumulated significant weight in arxiv-sanity-mcp's planning tree (~25 deliberations, ~15 audit folders, ~5 governance/standing-context artifacts, an 842-line trajectory plan, an 683-line audit-spec for that plan, a 329-line differential of that audit-spec). The closure-pressure-into-elaboration pattern from 2026-04-30 §5.1 recurred at meta-level during this session: 6 commits + ~250K codex tokens producing audit-of-audit infrastructure to verify a plan revision to do mapping work that hasn't started. Logan signaled "this is ridiculous" then "this is messing everything up here." The signal is the frame-revision-check trigger that the (V′.a) Step 4 mechanism failed to fire on its own. The disposition: extract gsd-2-uplift to its own repo + clean arxiv-sanity-mcp's planning tree of all uplift artifacts.

## §1. The corrected relationship (load-bearing for planning)

gsd-2-uplift and arxiv-sanity-mcp are connected by a **question**, not by ownership:

> **gsd-2-uplift exists to ask whether gsd-2 (the standalone agent runtime at `~/workspace/projects/gsd-2-explore/`) can be uplifted to handle the complex research and frontier design work that arxiv-sanity-mcp does — work involving complex experimental AI systems and configurations.**

arxiv-sanity-mcp is a **test case** for that question. The substrate-evidence-channel role (per `RELATIONSHIP-TO-PARENT.md`) is preserved post-extraction. **But arxiv-sanity-mcp's planning tree should not have gsd-2-uplift artifacts leaking in.** The test-case-vs-substrate relationship is referenceable from both sides; the artifacts live in the new repo.

This is the corrected framing: connection-by-question, not connection-by-co-location. Phase G's "trail-of-references" + "diagnostic-loop preserved" disciplines apply, but they are achieved through cross-repo references, NOT through retaining gsd-2-uplift artifacts inside arxiv-sanity-mcp.

## §2. What the planning session must produce

A **detailed + thorough extraction plan** covering three coordinated parts. Each part has its own internal mechanics; together they form one coherent migration.

### §2.1 Part A — Extraction migration plan (gsd-2-uplift → new repo)

- **Artifact-by-artifact disposition** for every file under `.planning/gsd-2-uplift/` + relevant deliberations + handoffs. The trajectory plan's §1.7 artifact-by-artifact table is the **starting point**, not the final answer. Re-evaluate each row under the corrected framing (connection-by-question, not co-location). Specifically: METHODOLOGY-MISMATCH-FINDING.md was self-corrected to DUPLICATE in commit `ffc0fb0`; under the corrected framing, DUPLICATE may no longer be right.
- **Git history strategy.** Do we use `git subtree split` to preserve commit history? Do we cherry-pick? Do we `cp -r` and re-author commit history? Each has tradeoffs; choose one and justify.
- **Cross-reference rewriting strategy.** Many artifacts cite paths within `.planning/gsd-2-uplift/`. After move, those paths are wrong on both sides. Specify rewrite rules: which paths get rewritten where; who owns rewrites; how to verify completeness.
- **Pointer-stub design** at moved-from paths in arxiv-sanity-mcp. Minimum content per stub. Disposition: do they exist or not? (Stubs preserve trail-of-references but also leave a residue of gsd-2-uplift in arxiv-sanity-mcp planning tree. Tradeoff: trail-readability vs. clean-tree.)
- **Commit cadence on both sides** during migration. Atomic per logical unit. Cross-repo commit-identity (the `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §4.2.1 rules apply but may need adaptation).
- **Special-case handling:** EXTERNAL-VISION-CONTEXT.md (currently DUPLICATE per its own frontmatter; harness-studio side already has its sibling at `~/workspace/projects/harness-studio/docs/deliberations/2026-05-01-gsd-2-substrate-transfer-and-pressure-clarification.md`); Step 3 audit-of-audit infrastructure at `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/` (codex AUDIT-SPEC.md + DIFFERENTIAL-SPEC.md + CLAUDE-PARALLEL-SKELETON.md + SPEC-DRAFTING-BRIEF.md — historical record per §3 below).

### §2.2 Part B — New-repo bootstrap (gsd-2-uplift's own home)

- **Repo location + name.** Suggested `~/workspace/projects/gsd-2-uplift/`; Logan-disposable.
- **Governance docs adapted for gsd-2-uplift's own identity** (NOT just cribbed from arxiv-sanity-mcp). Each one needs deliberate authorship:
  - **CLAUDE.md** — what is gsd-2-uplift; what are its accepted decisions; what are its key constraints; what are its doctrine load-points. arxiv-sanity-mcp's CLAUDE.md is pattern-precedent; content is bespoke.
  - **AGENTS.md** — agent behavior + working posture for gsd-2-uplift work. Notably: the closure-pressure-into-elaboration pattern + audit-discipline-limits findings + Logan-disposition-discipline scope (per 2026-04-30 §2.7) need to be load-bearing here from day one. The new repo inherits the lessons; lessons need to be present in governance.
  - **LONG-ARC.md** — anti-patterns + protected seams specific to substrate-design-work. Different content from arxiv-sanity-mcp's LONG-ARC.md (which is research-discovery-substrate-specific).
- **Identity artifacts:**
  - **PROJECT.md** — what is gsd-2-uplift specifically (per EXTERNAL-VISION-CONTEXT.md §1 5-property project-shape: identity-preserving / pressure-respecting / pushes-limits-in-reasonable-ways / reasonable-objectives-discovered-through-exploration / anchored-against-concrete-test-cases). The "preliminary final answer" Claude produced at end of 2026-05-01 vision-articulation turn-cluster is candidate content.
  - **VISION.md** — substrate-vision properties (the 12) + pressure-not-destination relationship to harness-studio. EXTERNAL-VISION-CONTEXT.md is candidate content (with adaptation).
  - **ROADMAP.md or equivalent** — if applicable. The trajectory plan was Phase D-shaped; post-extraction, the actual question is "do mapping-shape Phase D work" — need an articulation of how that's structured in new repo. Or: skip ROADMAP entirely until mapping evidence accumulates.
  - **STATE.md or equivalent** — current state at extraction time.
- **Inherited artifacts** (from extraction): trajectory plan, audit folders, deliberations (uplift-substantive), handoffs (uplift-related), exploration outputs, INITIATIVE.md, DECISION-SPACE.md, EXTERNAL-VISION-CONTEXT.md (DUPLICATE side), RELATIONSHIP-TO-PARENT.md (DUPLICATE side), Phase D interim corpus.
- **What gets dropped vs. kept** from inherited artifacts. Specifically:
  - **(V′.a) Step 3 audit-of-audit infrastructure** (codex AUDIT-SPEC.md, DIFFERENTIAL-SPEC.md, CLAUDE-PARALLEL-SKELETON.md, SPEC-DRAFTING-BRIEF.md): the audit was disposed-as-not-dispatched per Logan's "ridiculous"/"messing everything up" signal. The artifacts move with the rest as historical record (the closure-pressure-recurrence-at-meta-level evidence is itself substrate-shape evidence) but the audit doesn't dispatch. Move them to a `historical/` or `archive/` subfolder; preserve the trace; do not run the audit.
  - **The trajectory plan itself.** Post-extraction, the plan governs the extraction it just executed; it lives in new repo as historical record. The plan's Phase D + E + F gates may or may not apply post-extraction; the new repo's roadmap (if any) is its own decision.
- **Cross-references back to arxiv-sanity-mcp**: spike program, foundation-audit, ADRs, deliberations that stayed, DECISION-SPACE.md (genesis trail), STATE.md.

### §2.3 Part C — arxiv-sanity-mcp cleanup

- **Purge points:** every file/path under `.planning/gsd-2-uplift/` (delete or pointer-stub per Part A disposition); uplift-substantive deliberations under `.planning/deliberations/` (move to new repo per heuristic; check for residual references-back from arxiv-sanity-mcp); uplift-related handoffs under `.planning/handoffs/` (per same heuristic); cross-references in CLAUDE.md, AGENTS.md, STATE.md, ROADMAP.md, REQUIREMENTS.md, LONG-ARC.md, ECOSYSTEM-COMMENTARY.md, ADRs (any of them) that mention gsd-2-uplift or treat it as load-bearing for arxiv-sanity-mcp work.
- **CLAUDE.md cleanup:** remove the doctrine load-point for `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (or rewrite to point at new-repo's copy). Remove governance read-order entries for gsd-2-uplift artifacts. Remove any references to "gsd-2-uplift" in the project-identity sections.
- **STATE.md restoration:** strip the trailing gsd-2-uplift narrative from `stopped_at` + `last_activity`; restore frontmatter to v0.2 multi-lens substrate state; resume-readiness for v0.2 implementation work (Phases 12-17 per LONG-ARC.md sequencing).
- **LONG-ARC.md cleanup:** any anti-pattern entries derived from gsd-2-uplift work that are not arxiv-sanity-mcp-specific should be moved to new-repo's LONG-ARC.md. Anti-patterns that are arxiv-sanity-mcp-specific or test-case-as-substrate-evidence-shaped stay.
- **AGENTS.md:** check for any agent-conduct rules introduced for gsd-2-uplift work (closure-pressure recurrence; comfort-language; M1 paired-review; framing-widening) — these are general-purpose disciplines applicable to arxiv-sanity-mcp work too. Decision: keep general disciplines; move uplift-specific applications to new repo.
- **ECOSYSTEM-COMMENTARY.md:** if it references uplift work, prune or pointer-rewrite.
- **Spike program (`/.planning/spikes/`)** STAYS. Foundation-audit (`/.planning/foundation-audit/`) STAYS. These are arxiv-sanity-mcp-side; new repo cites by reference.
- **Verification of cleanup completeness:** define a method. (E.g., grep for "gsd-2-uplift" recursively; list all hits; confirm each is intentional.)
- **v0.2 resumption-readiness check:** can a fresh Claude session in arxiv-sanity-mcp pick up v0.2 work without confusion? Specifically: STATE.md says where v0.2 is; Phase 12 plan (per Phase 12 plan 1 authoring task) can begin without gsd-2 uplift first-wave evidence (per LONG-ARC.md sequencing — was that on hold pending uplift, or is it now unblocked?).

### §2.4 Sequencing + safety

- **Order of operations.** The three parts interlock. Suggested sequence: (1) commit current state on both sides (arxiv-sanity-mcp clean tree); (2) bootstrap new repo (Part B governance docs authored before any artifact moves); (3) execute migration (Part A artifact-by-artifact moves, atomic commits, cross-reference rewrites); (4) execute cleanup (Part C purge + STATE.md restoration); (5) verification on both sides; (6) final commits + cross-repo identity recording.
- **Safety constraints.** Both repos must be in coherent state at every commit boundary. No half-migrated artifact configurations. If migration is interrupted, both sides should be in resumable state.
- **Verification protocol.** Define explicit checks: arxiv-sanity-mcp grep-for-uplift-residue; new-repo internal-coherence + reference-resolution; bidirectional cross-reference resolution; fresh-context test on both sides.

## §3. What's already disposed (planning session does NOT re-litigate)

- **Audit-of-audit dropped.** The (V′.a) Step 3 paired audit at `.planning/gsd-2-uplift/audits/2026-05-01-trajectory-replan-audit/` does not dispatch. Codex AUDIT-SPEC.md + DIFFERENTIAL-SPEC.md + CLAUDE-PARALLEL-SKELETON.md + SPEC-DRAFTING-BRIEF.md exist as historical record (closure-pressure-recurrence-at-meta-level evidence). They move with the rest. **Do not propose dispatching them.** Their substantive critiques (Q-FI-6 Logan-correction-doesn't-immunize; Q-FI-7 artifact-rigor-as-substitute; Q-MM-4 spike-as-straw-man; Q-Meta-3 length-obscures-load-bearing-uncertainties; etc.) are recorded; they apply to the plan that's now historical post-extraction.
- **Phase D mapping work happens in new repo,** not in arxiv-sanity-mcp. This is the test-case-vs-substrate relationship preserved through cross-repo references rather than through co-location.
- **Trajectory plan applies to extraction it just executed.** Post-extraction, new repo's planning shape is new-repo's decision. The trajectory plan does not need re-revising before extraction; it served its purpose.
- **(V′.a) Step 4 + Step 5 are subsumed into extraction.** Frame-revision-check mechanism (Step 4) is in the trajectory plan + can be ported to new repo's AGENTS.md. METHODOLOGY-MISMATCH-FINDING.md (Step 5) was deferred per (V′.a); the methodology-mismatch finding lives in 2026-04-30 deliberation log + EXTERNAL-VISION-CONTEXT.md §7; no need to author a separate artifact in arxiv-sanity-mcp before extraction.

## §4. Mandatory inputs for planning session (small set)

Read these in order before drafting the extraction plan:

1. **This handoff** — full read.
2. **`.planning/STATE.md`** — current state-of-play; specifically the (V′.a) Step 2 + Step 3 mid-arc entries.
3. **`.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md`** — test-case-vs-substrate framing standing context.
4. **`.planning/gsd-2-uplift/EXTERNAL-VISION-CONTEXT.md`** §1 (project-shape) + §2 (pressure-not-destination) — corrected understanding of what gsd-2-uplift is.
5. **`.planning/gsd-2-uplift/INITIATIVE.md`** §7 — original migration trigger + custody rules; the §7 text is precedent but the corrected framing per §1 of this handoff supersedes co-location-based custody.
6. **`.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`** §1.7 (Phase G artifact-by-artifact table) — extraction-disposition starting point. **Re-evaluate each row under the corrected framing.**
7. **Last 4-5 messages of conversation log** at `/home/rookslog/.claude/projects/-home-rookslog-workspace-projects-arxiv-sanity-mcp/c42b9b37-07cd-4b19-be7b-c65f0cadf895.jsonl` (or whatever the current session log path is) — Logan's "ridiculous" + "messing everything up" + "no lets create a small temp handoff" + Claude's response. The frustration signal + extraction disposition + the planning-stage instruction.
8. **`.planning/CLAUDE.md`** + **`.planning/AGENTS.md`** + **`.planning/LONG-ARC.md`** — for understanding what arxiv-sanity-mcp's governance structure looks like (precedent for new-repo governance bootstrap; identifies cleanup points).

Targeted re-reads as needed during planning. Do NOT do exhaustive re-read of every audit folder + deliberation; the trajectory plan §1.7 table + DIFFERENTIAL-SPEC.md §1 (convergent decisions) summarize what's load-bearing. Targeted re-read where a specific disposition needs justification.

## §5. Stance discipline (avoid recursion)

Logan's signal was clear: the meta-rigor recursion has been the failure mode. The planning session must:

1. **Produce a plan, not an audit-of-the-plan.** No paired-discipline default-fires on this plan unless Logan disposes them. The planning session is at /effort max specifically because the depth of reasoning at ONE level (the plan) is what Logan wants — not the depth of audit-of-audit-of-audit cycles.
2. **Honor Logan's "ridiculous" disposition.** The 2026-04-30 §5.1-§5.4 calibration findings about closure-pressure-pattern recurrence apply to the planning session itself. Watch for: "we should also audit the plan" framings (per the differential's Q-FI-7); "comprehensive coverage" framings (per Q-Meta-3); "more rigorous artifacts" substituting for clearer decisions.
3. **The plan should be detailed and thorough on operational mechanics**, not on meta-deliberation about whether the plan is well-formed. Detailed = artifact-by-artifact dispositions; specific cross-reference rewrite rules; explicit verification steps; concrete commit cadence; named git operations. Not = re-articulating the framing-inheritance-risk per phase or producing audit-spec lens-questions.
4. **Use existing analysis where it's already done.** The trajectory plan's §1.7 table has artifact-by-artifact dispositions. The DIFFERENTIAL-SPEC.md has substantive critiques. EXTERNAL-VISION-CONTEXT.md has the corrected framing. Don't re-derive these; reference them and adjust where the corrected framing changes the answer.
5. **Resist ad-hoc artifact generation.** Authoring a planning-stage handoff (this artifact) is the appropriate scope-of-meta. Authoring a planning-stage handoff-handoff is the failure-mode signature. The plan should be one document (or a small set), not a constellation.
6. **Trust that the new repo will iterate on its own governance.** The new-repo bootstrap doesn't need to be perfect on day one. It needs to be coherent enough that fresh-context Claude can pick up from STATE.md + CLAUDE.md and continue working. Subsequent sessions in the new repo refine governance through use.

The success criterion for the planning session: **a plan Logan can read once and execute (or have Claude execute) without further meta-deliberation cycles.**

## §6. Cross-references / current state pointers

**Current state at handoff:**

- Working tree clean.
- Last 6 commits this session: `ffc0fb0` (Step 2 + self-review) → `f6af0f1` (SPEC-DRAFTING-BRIEF) → `da64b2c` (CLAUDE-PARALLEL-SKELETON) → `f15dc5d` (codex AUDIT-SPEC + DIFFERENTIAL-SPEC). All on branch `spike/001-volume-filtering`.
- Predecessors: `c1b098c` (EXTERNAL-VISION-CONTEXT.md + 12-property substrate-vision); `43e652b` (Phase D mid-arc methodology-mismatch + (V′.a) recording); `c0465a4` (Phase D dispatch mid-arc).
- harness-studio commit `7a11d89` (sibling 2026-05-01-gsd-2-substrate-transfer-and-pressure-clarification.md).
- gsd-2-explore branch `phase-d-decision-trace-spike` unchanged from `23b1ddc89` (Shape E SKILL.md interim work).

**Artifact location map (for migration planning):**

```
arxiv-sanity-mcp/
├── .planning/
│   ├── gsd-2-uplift/                                    (whole subtree → migrates)
│   │   ├── INITIATIVE.md
│   │   ├── DECISION-SPACE.md
│   │   ├── RELATIONSHIP-TO-PARENT.md                     (DUPLICATE; both sides)
│   │   ├── EXTERNAL-VISION-CONTEXT.md                    (DUPLICATE; both sides)
│   │   ├── trajectory/cheerful-forging-galaxy.md
│   │   ├── exploration/SYNTHESIS*.md
│   │   ├── orchestration/OVERVIEW.md + slice-*.md
│   │   ├── audits/2026-04-28-* (premise-bleed + cross-vendor codebase)
│   │   ├── audits/2026-04-29-trajectory-plan-audit
│   │   ├── audits/2026-04-30-phase-d-entry-audit
│   │   ├── audits/2026-05-01-trajectory-replan-audit (audit-of-audit; historical)
│   │   └── wave-2/decision-trace                        (Phase D interim corpus)
│   ├── deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md  (per-deliberation Logan-disposed)
│   ├── deliberations/2026-04-27-dispatch-readiness-deliberation.md  (uplift-substantive → migrate)
│   ├── deliberations/2026-04-28-framing-widening.md  (uplift-substantive → migrate)
│   ├── deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md
│   ├── deliberations/2026-04-28-comparison-drafting-decisions.md
│   ├── deliberations/2026-04-28-audit-spec-review-deliberation.md
│   ├── deliberations/2026-04-30-phase-d-methodology-mismatch-and-trajectory-replan.md  (uplift-substantive → migrate)
│   ├── handoffs/2026-04-26-post-wave-4-handoff.md (uplift-related → migrate)
│   ├── handoffs/2026-04-28-post-W1-and-framing-widening-handoff.md (uplift-related → migrate)
│   ├── handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md (uplift-related → migrate)
│   ├── handoffs/2026-05-01-extraction-planning-handoff.md  (this file; STAYS for execution; archive after)
│   ├── spikes/                                          (STAYS; arxiv-sanity-mcp-side)
│   ├── foundation-audit/                                (STAYS; arxiv-sanity-mcp-side)
│   ├── STATE.md                                         (cleanup-stripped)
│   ├── ROADMAP.md, REQUIREMENTS.md, LONG-ARC.md         (check for uplift refs)
│   ├── ECOSYSTEM-COMMENTARY.md                          (check for uplift refs)
│   └── PROJECT.md                                       (check for uplift refs)
├── CLAUDE.md                                             (cleanup; doctrine-load-point removal)
├── AGENTS.md                                             (cleanup; uplift-specific applications)
└── docs/adrs/                                            (check for uplift-derived ADRs)

External cross-references:
- ~/workspace/projects/harness-studio/                   (NOT migrated; pressure-relationship preserved via cross-references)
- ~/workspace/projects/paddock/                          (NOT migrated; offshoot-pattern reference)
- ~/workspace/projects/gsd-2-explore/                    (NOT migrated; the substrate being uplifted; new-repo cites by reference)
```

**Suggested new-repo location:** `~/workspace/projects/gsd-2-uplift/` (Logan-disposable in plan).

## §7. Closing notes for the planning session

- **/effort max applied at planning time.** The plan benefits from depth-of-reasoning at the planning level. The extraction itself is mechanical-coherence-bounded once the plan is detailed enough.
- **The extraction is a real operation.** Two repos must work post-extraction. A botched extraction that breaks either repo's coherence is the failure mode worse than over-elaboration. The plan must specify enough mechanical detail that execution is unambiguous; safety constraints are not optional.
- **The handoff is small + temp.** This artifact does its job by enabling the planning session. It doesn't need to be polished. Archive or delete after extraction is complete and verified.
- **The next session is at fresh context.** All context not in this handoff or in §4 mandatory inputs is unavailable. Plan accordingly.

---

*Handoff authored 2026-05-01 by Claude (Opus 4.7) at /effort xhigh in-session-collaboration with Logan. Subject to in-session-collaboration framing-inheritance from this conversation; the next session's fresh-context read at /effort max is the structural break. Logan-disposed: small + temp + scope-to-planning-onboarding.*
