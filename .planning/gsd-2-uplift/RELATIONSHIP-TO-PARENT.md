---
type: standing-context
date: 2026-04-29
status: standing — load-bearing for sessions touching gsd-2-uplift work or arxiv-sanity-mcp's diagnostic role
audience: future-Logan, future-Claude (in fresh sessions, including post-extraction sessions in the new repo), subagents dispatched on uplift work
parent_project: arxiv-sanity-mcp
relates_to: .planning/gsd-2-uplift/INITIATIVE.md, .planning/deliberations/2026-04-28-framing-widening.md, .planning/spikes/METHODOLOGY.md, .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md (§0.3)
post_extraction_disposition: DUPLICATE — this artifact lives on both sides of the extraction with bidirectional cross-references; both copies updated to point at the other (per trajectory plan §1.7 artifact-by-artifact disposition table)
---

# arxiv-sanity-mcp ↔ gsd-2-uplift: The Test-Case-vs-Substrate Relationship

This document carries a clarification that is load-bearing for any session working on gsd-2-uplift (here in arxiv-sanity-mcp's `.planning/`, or post-extraction in the dedicated repo) and for any session reasoning about arxiv-sanity-mcp's role in the broader long-horizon agential development arc. It articulates the **test-case-vs-substrate relationship** between the two projects so that future sessions do not collapse it.

The clarification originated in the trajectory plan at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §0.3, drafted 2026-04-29 in collaboration with Logan after the v1-GSD premise-bleed audit-arc surfaced the cost of letting framings inherit silently. This standing-context artifact lifts §0.3 out of the trajectory plan and into a place that auto-loads (via CLAUDE.md doctrine load-point) for the relevant session triggers.

## §1. What arxiv-sanity-mcp is in the bigger picture

**arxiv-sanity-mcp is NOT the long-horizon goal.** It is an MCP-native research discovery substrate (per CLAUDE.md "What This Project Is") with its own product trajectory, ADRs, and roadmap. That product trajectory is real and not subordinated to anything else. **At the same time**, arxiv-sanity-mcp is *a* **spike-intensive test case** for whether the agential-development substrate (currently scoped as: gsd-2 + Claude Code runtime + dev tooling + organizational conventions — substrate-shape itself part of what gsd-2-uplift investigates) can handle work where:

1. **Precedent is thin or absent.** No well-documented "right" stack/architecture to copy. The retrieval-and-ranking design space has multiple incompatible directions; no upstream gives the answer.
2. **Experimental design itself is load-bearing.** The wrong experiment forecloses optimal design routes; "fast enough" framings, premature comparative claims, and casual A/B reasoning silently destroy the design space. This is the kind of project where the spike methodology has to actually be applied, not perform-applied.
3. **The work necessarily produces new knowledge.** You cannot look up the answer; the answer comes out of the spike program, and the spike program's quality determines whether the answer is trustworthy.

The long-horizon goal is **a long-horizon agential development substrate** — Logan + Claude (or successor agents) being able to do deep, multi-month, intellectually-honest work together over years across many projects. gsd-2 is the current candidate substrate; whether and how to uplift it is the medium-horizon question (per trajectory plan §0.2).

arxiv-sanity-mcp's value to that long-horizon goal is **diagnostic, not consumptive.** The spike program at `.planning/spikes/`, the foundation-audit at `.planning/foundation-audit/`, the deliberation discipline at `.planning/deliberations/`, the paired-review M1 property in `.planning/spikes/METHODOLOGY.md`, the framing-widening discipline in `.planning/deliberations/2026-04-28-framing-widening.md`, the audit-of-audit discipline (premise-bleed audit-arc 2026-04-28), the §7 addendum point-of-use foregrounding pattern (SYNTHESIS-COMPARISON.md §7) — these are all instances of *the substrate working under conditions where the substrate is what's being tested*. When the substrate fails (closure-pressure recurrence, framing-leak, comfort-language), arxiv-sanity-mcp's working tree records the failure mode in a way that is hard to manufacture artificially.

**Both readings are simultaneously true.** arxiv-sanity-mcp is a real research discovery product *and* a diagnostic test case for the substrate. Neither reading subordinates the other. The product work is what creates the diagnostic conditions; the diagnostic loop is what makes the substrate-shape work credible.

### §1.1 Frame status — stipulated, not observed

The test-case-vs-substrate framing above is a frame Logan + Claude are choosing to apply on 2026-04-29, in response to the v1-GSD premise-bleed audit-arc surfacing the cost of letting framings inherit silently. It is **not an observed property** of the relationship between arxiv-sanity-mcp and gsd-2 — it is a stipulation about how to read evidence flowing from one into the other. Treat it as a useful input to deliberation, not as established fact. (This is the same "useful inputs, not observed facts" discipline `SYNTHESIS-COMPARISON.md §7.1` applies to its own §5 axes; this artifact applies it to itself recursively.)

What the stipulation rests on:

- **Single-case-anchoring caveat.** arxiv-sanity-mcp is *a* spike-intensive test case, not *the* test case. What its spike-intensive conditions surface about the substrate may not generalize to other-project-shapes the substrate eventually serves. Substrate-design decisions should triangulate against other diagnostic surfaces (paired-review M1 evidence, framing-widening §3.3 user-context plurality, foundation-audit findings, deliberation arcs — all currently arxiv-sanity-mcp-internal; cross-project triangulation depends on additional test-case anchors per framing-widening §3.3, which the substrate has not yet acquired) rather than treating arxiv-sanity-mcp's substrate-behavior signals as the substrate's behavior generally. Whether other test-case anchors should be added is open per framing-widening §3.3 user-context plurality.
- **"Long-horizon" admits a plurality.** Per framing-widening §2, "long-horizon development" itself has at least six operational meanings (solo-research over years, larger-team enterprise, OSS contribution, anticipatory-scaling, transition-as-event, transition-as-stance); the articulation in this §1 is *one* such reading. Which long-horizon shape is binding for the gsd-2-uplift initiative is open. Future evidence may shift the calibration.
- **When the readings tension.** "Diagnostic, not consumptive" specifies arxiv-sanity-mcp's value-relation to the long-horizon goal; it does not subordinate arxiv-sanity-mcp's own product trajectory. Operational hierarchy: arxiv-sanity-mcp's product trajectory is governed by its own ADRs/roadmap/CLAUDE.md (the product reading is operational authority for product decisions); the substrate-evidence channel is a parallel observational layer that does not override product-level authority. gsd-2-uplift work treats substrate-evidence as input but does not treat arxiv-sanity-mcp's product decisions as substrate-design decisions.
- **Loosening conditions.** If evidence accumulates that the framing overfits — e.g., gsd-2-uplift first-target outputs surface that arxiv-sanity-mcp's diagnostic signals are unrepresentative, or framing-widening's open questions resolve in directions that make the test-case framing redundant — loosen the framing per `framing-widening §9` deferred-items pattern. The frame's continued application is contingent on its remaining useful, not on its having been adopted.

## §2. Why this matters for execution

If a future session (or subagent) collapses the distinction — treating arxiv-sanity-mcp as "just the project" or treating gsd-2-uplift as "just a tool we're building for arxiv-sanity-mcp" — the diagnostic loop is lost. Two failure modes follow:

**Failure mode 1 — narrowing uplift to arxiv-sanity-mcp's specific needs.** If gsd-2-uplift work treats arxiv-sanity-mcp as the only user-context, the design narrows to what this one project happens to need. `INITIATIVE.md §3.3` and `DECISION-SPACE.md §3.8` already preserved a plurality of onboarding situations; framing-widening §3.3 ("Where this could be wrong") explicitly raised the possibility that arxiv-sanity-mcp is one user-context among many. **The test-case-vs-substrate frame is a different cut**: arxiv-sanity-mcp generates *evidence about substrate behavior under spike-intensive conditions*, which informs substrate design in ways that no specific user-context (including arxiv-sanity-mcp's own user-context) can substitute for.

**Failure mode 2 — collapsing arxiv-sanity-mcp's spike-program outputs into "project-specific decisions."** The spike program's findings, the foundation-audit's findings, the deliberation arcs, and the audit-arcs are *both* project-specific (they shape arxiv-sanity-mcp's roadmap) *and* substrate-evidential (they are observations of how the substrate behaves under spike-intensive conditions, with all the failure modes and recoveries those conditions surface). Future sessions that read these artifacts only as project-specific lose the substrate-evidence channel.

**Implication.** When deliberating about substrate-shape (gsd-2-uplift work), preserve the test-case framing. When deliberating about arxiv-sanity-mcp's own work, recognize that the spike-program's quality also serves the substrate-evidence channel. The two readings are simultaneously active; neither subordinates the other.

## §3. What this implies for migration

When the gsd-2-uplift initiative extracts to its own dedicated repo (per trajectory plan Phase G; per `INITIATIVE.md §7` migration trigger; the §7 custody rule "DECISION-SPACE.md and the deliberation log stay in arxiv-sanity-mcp's `.planning/`" is authoritative), the test-case-vs-substrate trail-of-references must be preserved on both sides:

- **In arxiv-sanity-mcp** post-extraction: pointer artifacts at moved-from paths plus this RELATIONSHIP-TO-PARENT.md retained locally (with cross-reference updated to point at the new repo's copy). The spike program, the foundation-audit, the genesis-recording deliberations, and DECISION-SPACE.md stay here. The "diagnostic loop" continues on this side: this is where substrate-evidential conditions occur.
- **In the new gsd-2-uplift repo** post-extraction: this RELATIONSHIP-TO-PARENT.md duplicated (with cross-reference pointing back at arxiv-sanity-mcp's copy). The new-repo work cites back to arxiv-sanity-mcp's spike-program outputs, foundation-audit, and decision-space genesis as substrate-behavior evidence. The "diagnostic dependency" is explicit and traceable, not hidden.

The bidirectional reference is intentional. Trajectory plan §1.7 specifies this artifact's disposition as **DUPLICATE (cite-by-reference)** rather than MOVE or STAY because the artifact is intrinsically about both sides of the relationship; it has to live on both sides to remain meaningful in either context.

**Phase H verification (per trajectory plan §1.8) explicitly tests** that fresh-context Claude on the new-repo side can reconstruct the medium-horizon work *from new-repo-local artifacts while following explicit references back to arxiv-sanity-mcp for diagnostic evidence*. "Yes" means coherence-with-intact-references-back; it does NOT mean independence. The diagnostic loop is preserved by reference, not by duplication of all evidence.

## §4. Cross-references

**Originating artifact:** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §0.3 (this artifact lifts §0.3 into a standing location).

**Initiative-scoping:**
- `.planning/gsd-2-uplift/INITIATIVE.md` (§7 migration trigger; §1 goal articulation; §3.3 onboarding situations).
- `.planning/gsd-2-uplift/DECISION-SPACE.md` (§1.6 incubation discipline; §3.8 onboarding plurality; §1.2 goal as articulated).

**Framing context:**
- `.planning/deliberations/2026-04-28-framing-widening.md` §2 (six-context plurality of "long-horizon development" — the artifact's §1.1 single-case-anchoring caveat draws on this) and §3.3 ("Where this could be wrong" — flags that arxiv-sanity-mcp may be one user-context among many; this artifact extends with a different cut: arxiv-sanity-mcp is *also* a substrate-shape test case, not just a user-context).
- `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §7 (the addendum that surfaced the integration-grammar-as-fact residual; precedent for point-of-use clarification artifacts; §1.1 above applies §7's "useful inputs, not observed facts" discipline to this artifact recursively).

**Substrate-evidential channels:**
- `.planning/spikes/METHODOLOGY.md` (six interpretive lenses + paired-review practice disciplines A-F + M1 paired-review property — the spike program's methodology is itself an instance of substrate-evidence about how rigorous spike work is conducted under the substrate).
- `.planning/foundation-audit/METHODOLOGY.md` (decision-review epistemic discipline — the foundation-audit is substrate-evidence about decision-review under the substrate).
- `.planning/spikes/` (spike outputs as substrate-behavior evidence under spike-intensive conditions).
- `.planning/foundation-audit/` (foundation-audit findings as substrate-behavior evidence under decision-review conditions).

**Trajectory plan integration:**
- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §0.3 (the §0.3 articulation that this artifact carries forward into standing-context).
- §1.2 (Phase B; this artifact's authoring phase).
- §1.7 (Phase G artifact-by-artifact disposition table; this artifact's DUPLICATE disposition).
- §1.8 (Phase H integration verification; tests references-back coherence on both sides).
- §2.1-§2.3 (audit cadence — the operational mechanism for catching framing-collapse failures across phases; this artifact articulates the framing, audit cadence enforces it).

---

*Drafted 2026-04-29 by Claude (Opus 4.7) in collaboration with Logan, as Phase B of the trajectory plan. Subject to the same in-session-collaboration fallibility caveat as DECISION-SPACE.md §0; the same-vendor adversarial-auditor at high reasoning level (per trajectory plan §2.4 row B) is the structural mitigation for register-leak in this clarification artifact.*
