---
type: trajectory-plan-audit-disposition
date: 2026-04-29
disposition: revise-before-execute (option (c) per AUDIT-SPEC.md §8.2)
disposed_by: Logan, post-PLAN-AUDIT.md review
applied_by: Claude (Opus 4.7), main thread
status: disposition-applied
spec: ./PLAN-AUDIT.md
plan_audited: /home/rookslog/.claude/plans/cheerful-forging-galaxy.md (runtime mirror at audit time)
plan_authoritative_post_revision: .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md (in-repo, version-controlled — established by F1 disposition)
---

# Disposition — Trajectory Plan Self-Audit (Phase A)

## §0. What was disposed

Logan disposed **revise-before-execute** (option (c) per AUDIT-SPEC.md §8.2) on the trajectory plan after reviewing the cross-vendor codex GPT-5.5 xhigh plan-self-audit findings. Disposition recorded in this DISPOSITION.md; revisions applied to the plan body; in-repo authoritative copy created at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`.

## §1. Audit arc summary

| Stage | Output | Headline |
|---|---|---|
| Plan draft | /home/rookslog/.claude/plans/cheerful-forging-galaxy.md (runtime location) | 8-phase trajectory + onboarding + audit cadence + per-audit reasoning-level table + commit map + failure-modes |
| Phase A audit | PLAN-AUDIT.md (codex GPT-5.5 xhigh cross-vendor) | 9 findings: 1A/6B/2C; medium-high confidence |
| Logan disposition | revise-before-execute (option (c)) | this file |
| Application | All 9 findings addressed via plan revisions; in-repo authoritative copy created | plan now revised at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` |

## §2. Why revise-before-execute (rather than commit-as-is or commit-with-addendum)

Per main-thread Claude recommendation (recorded against PLAN-AUDIT.md §5 non-binding disposition signal) and Logan's confirming disposition:

1. **F2 is genuinely trajectory-shaping.** The audit caught that Phase G's "What moves to new repo: `.planning/gsd-2-uplift/` (entire tree: INITIATIVE.md + DECISION-SPACE.md + audits/ + exploration/ + orchestration/)" directly contradicts INITIATIVE.md §7's authoritative custody rule that "DECISION-SPACE.md and the deliberation log stay in arxiv-sanity-mcp's `.planning/`." DECISION-SPACE.md custody is not a local wording choice — it determines which repo owns the genesis decision-trail and which repo's identity carries the genesis context. An addendum could correct this, but the plan body itself becoming the execution authority on this load-bearing point requires in-body revision.

2. **F1 (plan-file artifact-custody) requires changes the executor would otherwise make ad-hoc.** The plan file lived outside the arxiv-sanity-mcp git worktree (under `/home/rookslog/.claude/plans/`). Phase A's commit map said "plan file + audit folder" — but the runtime path can't be committed from this repo. Without in-body resolution, executor would need to invent the custody convention mid-execution. Better to resolve in the plan: in-repo authoritative location at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`; runtime mirror at `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` is a working-draft mirror only. Phase A commit places the in-repo copy under version control.

3. **F4 + F5 + F8 cluster as commit-protocol/control-matrix improvements** that benefit from being in the plan body, not appended.
   - F4: §0.6 lists 13 kinds of erring; §5.1-5.5 operationalizes 5. The remaining 8 rely on generic audit machinery + executor memory. Adding §5.6 control matrix mapping each kind → phases/check/recorded-at/owner converts the taxonomy from doctrine list to execution control surface.
   - F5: Phase G quality gate said xhigh in §1.7 but high in §2.4 reasoning-level table — the principle in §2.4 was correct (mechanical-coherence audit; high suffices), so the §1.7 line was the bug. Aligning resolves the audit-dispatch ambiguity.
   - F8: Cross-repo extraction creates two git histories; backward-traceability requires source-commit + target-commit + path-by-path map at every extraction commit. New §4.2.1 makes cross-repo commit-identity mandatory in EXTRACTION-LOG.md and both commits' bodies.

4. **F3 + F6 + F7 + F9 are surface fixes that the in-body revision absorbs cleanly** without requiring a separate addendum:
   - F3: `LONG-ARC.md` → `.planning/LONG-ARC.md` (path drift; the file is under `.planning/`, not at repo root).
   - F6: §0.5 cited memory files (`feedback_*`, `reference_*`) as if load-bearing; revised to add a self-containment note declaring the bullet text as execution authority and demoting memory-file citations to optional provenance.
   - F7: Phase H test "without reference to arxiv-sanity-mcp" overstated independence; revised to "from new-repo-local artifacts, while following explicit references back to arxiv-sanity-mcp for diagnostic evidence" — preserves the §0.3 diagnostic-loop relationship.
   - F9: Stale DRAFT status line + Phase B artifact-map TBD; updated to REVISED status + resolved Phase B location per §0.7 Q3 Option (a).

5. **Commit-as-is would leave executor inheriting two contradictions** (F1 plan-file custody; F2 DECISION-SPACE.md custody) that materially change what gets committed where. Commit-with-addendum is plausible but produces a plan-plus-addendum-as-execution-authority shape. Logan's stated requirement is "the plan file itself, not plan-plus-addendum, is the execution authority" — revise-before-execute matches this.

## §3. What was applied — per-finding revision trace

### §3.1 F1 (Class C — plan-file artifact-custody)

**Plan revisions applied:**
- Header status line + new "Authoritative location" line at top of plan: declares `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` as authoritative; runtime mirror at `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` is working-draft only.
- §1.1 Phase A: added "Plan-file authority resolution (per F1 disposition)" sub-section explicitly naming the in-repo path as authority.
- §1.1 Phase A commit body updated: "in-repo plan copy at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` + audit folder".
- §3.1 artifact map row A: dual location with **Authoritative** + **Mirror** labels.
- §3.2 naming conventions: added "Trajectory plan: `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`".
- §0.5 don't-modify-external bullet: rewritten to name in-repo as authority + runtime as `/loop` resume convenience only.
- §7 references: dual location stated.

**In-repo copy created:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (committed via Phase A commit; 735 lines).

### §3.2 F2 (Class C — Phase G move/stay vs INITIATIVE.md §7 conflict)

**Plan revisions applied:**
- §1.7 Phase G: prose-block "What moves" / "What stays" / "What gets cited-by-reference" replaced with explicit **artifact-by-artifact disposition table** (~14 rows).
- §1.7 leading "Authoritative custody rule (per INITIATIVE.md §7 + Phase A audit F2 disposition)" paragraph: names INITIATIVE.md §7 as the authoritative custody rule and operationalizes it.
- DECISION-SPACE.md disposition explicitly **STAY** with reasoning ("Records arxiv-sanity-mcp's session that genesised the initiative; new repo gets its own decision-space starting from extraction-state if Logan disposes").
- INITIATIVE.md disposition **MOVE** + thin pointer/genesis-marker artifact replacement at original path.
- exploration/, audits/, orchestration/ → **MOVE** (initiative-scoping; substrate-shape work product).
- Genesis-recording deliberations → **STAY**; uplift-substantive deliberations → **per-deliberation Logan-disposed** with default heuristic.
- Per-handoff Logan-disposed treatment for `.planning/handoffs/`.
- RELATIONSHIP-TO-PARENT.md (Phase B output) → **DUPLICATE** (cite-by-reference); intrinsically about both sides.
- Plan file → **MOVE** (with arxiv-sanity-mcp citation kept).
- Spike program, foundation-audit, methodology files → **STAY** (and reapply, not migrate).
- §0.4 mandatory pre-reading item 4 explicitly flags INITIATIVE.md §7 as "load-bearing for Phase G move/stay table; the §7 text is the authoritative custody rule, not optional guidance."

### §3.3 F3 (Class B — LONG-ARC.md path drift)

**Plan revisions applied:**
- §0.4 item 3: `/home/rookslog/workspace/projects/arxiv-sanity-mcp/LONG-ARC.md` → `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/LONG-ARC.md` with explanatory note.
- §7 standing context list: `arxiv-sanity-mcp/LONG-ARC.md` → `arxiv-sanity-mcp/.planning/LONG-ARC.md`.
- §7 methodology grounding bullet: `LONG-ARC.md` → `.planning/LONG-ARC.md`.
- §7 spike-methodology reference: `METHODOLOGY.md` → `.planning/spikes/METHODOLOGY.md`.

### §3.4 F4 (Class B — failure-mode taxonomy lacks operationalization)

**Plan revisions applied:**
- New §5.6 "Failure-mode control matrix": 13-row table mapping each §0.6 failure-mode kind to **phase(s) where applies / concrete check / recorded-at artifact / owner**.
- §0.7 Q5 updated: references §5.6 mapping table for per-phase failure-mode subsetting.
- §0.6 leading paragraph: cross-references §5.6.
- §6.1 pre-execution verification: adds "§5.6 control matrix reviewed for the upcoming phase".
- §6.2 per-phase verification: adds "§5.6 failure-mode checks applicable to this phase have fired and been disposed".

### §3.5 F5 (Class B — Phase G xhigh/high inconsistency)

**Plan revisions applied:**
- §1.7 Phase G quality gate: "Cross-vendor xhigh audit" → "Cross-vendor **high** audit" with explicit alignment-with-§2.4 sentence: "Aligned with §2.4: mechanical-coherence (orphan-reference + missed-migration + cross-reference integrity) is bounded; xhigh would be over-engineered for this audit shape."
- §2.4 row G unchanged (was already correct: cross-vendor high).

### §3.6 F6 (Class B — §0.5 memory-file provenance gap)

**Plan revisions applied:**
- §0.5 leading paragraph: new "Note on self-containment (per Phase A audit F6 disposition)" declares bullet summaries as **execution authority**; memory-file citations are optional provenance pointers; execution does NOT depend on reading memory files.
- §0.5 individual bullets: changed `(per feedback_X)` → `(provenance: feedback_X)` for clarity.
- §0.5 "Don't-modify-external" bullet: rewritten with in-repo plan authority resolution (also addresses F1).
- §7 memory-references section: relabeled as "Memory references (optional provenance pointers, NOT load-bearing for execution per §0.5 self-containment note)" with explicit explanation that they may not be available in a fresh session and execution does not depend on them.

### §3.7 F7 (Class B/C-boundary — Phase H "without reference" overstates independence)

**Plan revisions applied:**
- §1.8 Phase H process step 1: "without reference to arxiv-sanity-mcp" → "**from new-repo-local artifacts, while following explicit references back to arxiv-sanity-mcp for diagnostic evidence** (spike-program outputs, foundation-audit findings, plan-audit trail, DECISION-SPACE.md genesis record)" + clarification that "yes" means coherence-with-references-back, not independence.
- §1.8 Phase H process step 2: extended to also confirm "which artifacts stayed (DECISION-SPACE.md, deliberations, spike program) and why".
- §1.8 Phase H quality gate: "Both fresh-context tests pass (yes-and-yes, where 'yes' means coherence-with-intact-references-back, NOT independence)".
- §1.6 Phase F criterion-3 internal-coherence: clarification added that "internal coherence here means the new-repo-content stands on its own internal logic, NOT that it has zero references back to arxiv-sanity-mcp; explicit references back for diagnostic evidence are expected and preserved."
- §6.3 final-state verification: rewritten to "New repo internal coherence holds with intact references-back to arxiv-sanity-mcp" + "explicit references-back are traceable and resolve correctly".

### §3.8 F8 (Class B — cross-repo commit-identity gap)

**Plan revisions applied:**
- New §4.2.1 "Cross-repo commit-identity rules (Phase G + Phase H)": explicit rules requiring (1) EXTRACTION-LOG.md to include source repo commit hash, target repo initial commit hash, path-by-path disposition table, final post-Phase-H commit hashes on both sides; (2) both commit bodies to reference paired commit hash, with follow-up commit pattern when paired hash not yet known at primary commit time; (3) EXTRACTION-LOG.md as cross-repo integrity ledger.
- §1.7 Phase G commit pattern: arxiv-sanity-mcp side body MUST include new-repo initial commit hash; new-repo side body MUST include arxiv-sanity-mcp source commit hash.
- §1.7 Phase G outputs: EXTRACTION-LOG.md target line-count revised upward (150-300) reflecting the cross-repo identity ledger expansion.
- §1.8 Phase H outputs: EXTRACTION-LOG.md updated with "final cross-repo commit identities (both sides' final commit hashes after Phase H corrections)".
- §4.1 Phase G commit groups: adds "(3) Cross-repo commit-identity follow-up commits per §4.2.1".
- §6.3 final-state verification: cross-repo commit identities recorded per §4.2.1 explicitly listed.

### §3.9 F9 (Class A — stale DRAFT status + Phase B TBD)

**Plan revisions applied:**
- Header status: "DRAFT — awaiting Logan-disposition on §0.7 open-questions before finalization" → "REVISED 2026-04-29 (post-Phase-A-audit; revise-before-execute disposition applied per audit findings F1-F9). Ready for Phase B execution."
- New "Plan-self-audit status" header line: complete; cross-references PLAN-AUDIT.md.
- §3.1 artifact map row B: "TBD per Logan §0.7 Q3 disposition" → "`.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` (per §0.7 Q3 Option (a)) + CLAUDE.md doctrine-load-point addition".
- Plan footer: rewritten to record the revise-before-execute disposition + per-finding revision trace pointer.

## §4. Methodological notes

### §4.1 Plan-self-audit dispatch deviation

The Phase A audit dispatched cross-vendor codex GPT-5.5 xhigh single-vendor (no paired Step-2). Per §2.3, paired discipline is conditional-fire at Logan-discretion at Phase A. Logan did not invoke paired here; the cross-vendor audit alone was sufficient to surface 9 findings including 2 Class C, and the differential analysis was performed in main thread (this DISPOSITION.md serves as the analysis record).

**Tradeoff acknowledged.** Single-vendor cross-vendor audit may have under-detected same-vendor register-leak / integration-grammar-as-fact at the meta-level (per premise-bleed audit precedent where Step-2 same-vendor caught what Step-1 cross-vendor missed). If Logan reads in-session-collaboration risk on this DISPOSITION.md or on the revised plan as load-bearing, a Phase A paired Step-2 (same-vendor adversarial-auditor xhigh independent) can be invoked retrospectively. The trajectory has been designed to absorb this: §1.4 first-target findings, §1.5 stability test, and §1.8 Phase H integration audit each provide downstream re-examination opportunities.

### §4.2 In-session-collaboration caveat applies recursively

This DISPOSITION.md is itself drafted in-session by Claude with Logan-framing inheritance. The §0.5 D5a caveat applies: a fully-independent third reader might read the per-finding revision trace and surface points where the revisions over-extend or under-extend the audit's findings. The mitigation is: (a) revisions are traceable and reversible (the in-repo plan file is version-controlled); (b) future audits at Phase E + Phase H will re-examine the trajectory state; (c) Logan's disposition recorded the revise-before-execute call, with the per-finding revisions delegated to Claude execution within scope.

### §4.3 Confidence on revisions

- **High** that F1 + F2 (Class C) are correctly disposed: explicit artifact-custody rules in INITIATIVE.md §7 grounded F2; F1 was a category-recognized authority resolution.
- **High** that F3 + F5 + F9 (path/level/status surface fixes) are correctly applied.
- **Medium-high** that F4 (failure-mode control matrix) makes the right granularity calls — possible residual: some matrix rows may need refinement at execution time when a phase actually invokes a specific check.
- **Medium-high** that F6 (self-containment note) sufficiently dissolves the provenance gap — possible residual: a fresh-context Claude in a stricter dispatch boundary might still read the bullets as authoritative-but-incomplete without the memory files; the explicit "execution does NOT depend on reading memory files" sentence is the principal mitigation.
- **Medium-high** that F7 (Phase H test phrasing) preserves the diagnostic-loop relationship correctly.
- **Medium** that F8 (cross-repo commit-identity rules) catch all the cases — extraction is novel work; rules may need refinement at Phase G execution time. The §4.2.1 framework is sufficient as a starting-point.

## §5. What this disposition does NOT decide

- **Phase B–H specifics.** Each subsequent phase's actual outputs and dispositions remain Logan-disposed at execution time. This disposition only governs the plan-revision shape.
- **Whether to dispatch a paired Step-2 same-vendor adversarial-auditor on Phase A.** Logan can invoke this retrospectively if the in-session-collaboration risk on the revised plan or on this DISPOSITION.md is read as load-bearing for execution; this disposition does not foreclose that option.
- **The dedicated-uplift-repo's location, name, or internal structure.** Forms in Phase G per Logan-disposition.
- **The pointer-artifact text at moved-from paths in arxiv-sanity-mcp post-Phase-G.** Phase G drafts these; this disposition only specifies that they exist (~10 lines each).

## §6. Cross-references

- `./PLAN-AUDIT.md` (Phase A audit findings; cross-vendor codex GPT-5.5 xhigh).
- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (revised plan; in-repo authoritative location established by F1 disposition).
- `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` (runtime mirror; not the execution authority post-revision).
- `.planning/gsd-2-uplift/INITIATIVE.md` §7 (authoritative custody rule grounding F2 disposition).
- `.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/DISPOSITION.md` (precedent for premise-bleed audit-arc + addendum-foregrounding pattern).
- `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.17 (audit methodology applied to this Phase A audit).

---

*Disposition recorded 2026-04-29 by Claude (Opus 4.7), main thread, in-session-collaboration with Logan. Subject to same fallibility caveat as DECISION-SPACE.md §0. Future Phase E + Phase H audits provide re-examination of the trajectory state established by this revision.*
