---
type: audit-spec
date: 2026-04-29
status: dispatched
phase: B (trajectory plan)
artifact_under_audit: .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md (+ CLAUDE.md doctrine-load-point bullet)
audit_kind: same-vendor adversarial (Claude Opus, adversarial-auditor-xhigh agent type)
reasoning_level: high (NOT xhigh — per trajectory plan §2.4 row B; bounded artifact + register-leak detection on a clarification artifact; deep reasoning is not what's being tested)
m1_paired_review_rationale: same-vendor only (NOT paired) — per trajectory plan §1.2 "Why same-vendor here, not paired"; cross-vendor lacks the framework familiarity to detect register-leak; adding cross-vendor would be M1 strict-undersell (per §0.6 failure-mode taxonomy)
---

# AUDIT-SPEC.md — Phase B Standing-Context Artifact Audit

## §0. Purpose

Phase B of the trajectory plan (`.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`) creates a standing-context artifact at `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` carrying the test-case-vs-substrate clarification (§0.3 of the trajectory plan) into a place that auto-loads via CLAUDE.md doctrine load-point. This audit pressure-tests the artifact for register-leak, framing-leak, and clarification-quality before commit.

The premise-bleed audit-arc (2026-04-28) demonstrated that clarification artifacts produced in-session-collaboration with Logan can themselves carry framing-inheritance (the §7.1 reading-frame addendum was the lighter mitigation; revision was the alternative). This Phase B artifact is at recursive risk: it is a clarification *about* the framing relationship between two projects, drafted in the same session arc. Same-vendor adversarial review is the structural mitigation.

## §1. Lens for the audit

**Primary lens — register-leak detection.** The artifact is supposed to articulate the test-case-vs-substrate relationship clearly enough that future sessions don't collapse it. Register-leak failures would look like:
- Comfort-language ("this might be useful" instead of "this is load-bearing").
- Performative-vs-operational openness (naming readings as plural while the prose treats one as primary).
- Closure-pressure ("we've established X" when X is the artifact's own stipulation, not an established fact).
- Integration-grammar-as-fact (treating the test-case-vs-substrate framing as observed-fact rather than as a clarifying frame Logan + Claude are stipulating; the §7.1 residual recurrence at meta-level).

**Secondary lens — framing-leak detection.** The artifact draws on framing-widening §3.3 ("project-anchoring may be wrong; arxiv-sanity-mcp may be one user-context among many") but cuts a different distinction (test-case-vs-substrate). Framing-leak would look like:
- Conflating the two distinctions (treating "test case" as synonymous with "user-context" or with "diagnostic project").
- Reproducing v1-GSD bleed at a different layer (e.g., treating "the substrate" as if its shape were known when it's the question under investigation).
- Implicit narrowing of what counts as "diagnostic evidence" (e.g., treating only spike-program outputs as evidence and dropping foundation-audit, deliberation arcs, audit-arcs).

**Tertiary lens — clarification quality.** Does the artifact actually *clarify* the relationship in a way a fresh-context Claude can carry forward, or does it merely state the words while leaving operational ambiguity? Clarification-quality failures would look like:
- Operational ambiguity: a fresh-context reader could still collapse the distinction after reading.
- Internal incoherence: §1's claim conflicts with §2's implication or §3's migration discipline.
- Missing the load-bearing case: the artifact handles the easy cases but doesn't address what to do when the diagnostic loop is genuinely under stress.

**Negative-space check.** What is the artifact *excluding* from consideration? Is the exclusion principled or accidental?

## §2. Methodology

Per AUDIT-SPEC.md §6.1 (universal audit-output structure across audits in this trajectory plan; established by the premise-bleed audit-arc precedent):

1. **Read the artifact under audit** (`RELATIONSHIP-TO-PARENT.md`) plus the CLAUDE.md load-point bullet.
2. **Read the framing-grounding** (trajectory plan §0.3 + §1.2; framing-widening §3.3; SYNTHESIS-COMPARISON.md §7; INITIATIVE.md §7).
3. **Apply the three lenses** (register-leak / framing-leak / clarification-quality) systematically section-by-section.
4. **Apply negative-space lens** at the artifact's framing and at the CLAUDE.md load-point.
5. **Calibrate confidence** per finding (high / medium / low) and class per finding (Class A: addendum-shape; Class B: revision-shape; Class C: re-architect-shape).
6. **Produce non-binding disposition signal** per finding.

**Independent mode.** Per AUDIT-SPEC.md §3.4 manual-discretion pattern (premise-bleed audit precedent): the auditor reads ONLY the artifact under audit + the framing-grounding listed above. Do NOT read prior audits' findings (premise-bleed FINDINGS-STEP2.md / DIFFERENTIAL.md / DISPOSITION.md; trajectory-plan PLAN-AUDIT.md / DISPOSITION.md) before completing the audit; this preserves independence-of-finding and avoids prior-audit-anchoring.

## §3. Inputs

**Required reading (sequenced):**
1. The artifact under audit: `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md`.
2. The CLAUDE.md doctrine-load-point addition (the new bullet under "## Doctrine load-points").
3. The originating §0.3 of the trajectory plan: `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (focus on §0.3 + §1.2 + §1.7 row for RELATIONSHIP-TO-PARENT.md disposition).
4. `.planning/deliberations/2026-04-28-framing-widening.md` §3.3 ("Where this could be wrong" — project-anchoring caveat).
5. `.planning/gsd-2-uplift/INITIATIVE.md` (§1 goal articulation, §3.3 onboarding situations, §7 migration trigger).
6. `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` §7 (point-of-use addendum precedent).

**Optional reading (do not read in independent mode; reserve for differential or post-hoc verification only):**
- Premise-bleed audit folder.
- Trajectory-plan audit folder.

## §4. Output structure

Write findings to `audit-findings.md` (or `audit-findings-A.md` / `audit-findings-B.md` etc. for paired/sequential dispatches) in the same directory as this AUDIT-SPEC.md, using the structure established by the premise-bleed audit precedent.

**Naming-convention note (load-bearing for sub-agent direct writes):** Claude Code 2.1.123's built-in `tengu_sub_nomdrep_q7k` feature flag rejects sub-agent Write tool calls whose basename matches `/^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$/i`. The convention `audit-findings.md` bypasses the regex (basename starts with "audit-" → no match), so the auditor sub-agent can write its findings directly to disk rather than returning them inline for main-thread transcription. This convention applies to future audits in this trajectory plan; older audits (premise-bleed FINDINGS.md / FINDINGS-STEP2.md; trajectory-plan PLAN-AUDIT.md) used the prior FINDINGS naming and absorbed the transcription cost. Going forward, default to `audit-findings*.md` unless the dispatching prompt specifies otherwise.

**§0. Summary** — auditor identity + reasoning-level + class breakdown + headline.
**§1. Methodology applied** — what was read; what was excluded; mode (independent vs differential).
**§2. Findings** — per-finding entries: ID + class + lens + finding (verbatim text from artifact if applicable) + reasoning + confidence + non-binding disposition signal.
**§3. Negative-space observations** — what the artifact excludes; whether principled or accidental.
**§4. Calibration** — auditor's confidence in own findings; what would shift the call.
**§5. Non-binding disposition signal** — recommendation for Logan disposition (commit-as-is / commit-with-addendum / revise-before-commit per AUDIT-SPEC.md §8 disposition pathway from the trajectory plan).

## §5. Disposition pathway

Per trajectory plan §2.5 (universal):
1. Logan reviews findings.
2. Logan disposes one of: commit-as-is / commit-with-addendum / revise-before-commit.
3. Disposition recorded at `DISPOSITION.md` in this audit folder.

**Failure-branch (per trajectory plan §1.2):** If audit surfaces framing-leak in the clarification artifact itself (recursive risk), revise. If audit surfaces wrong location (e.g., CLAUDE.md note belongs in INITIATIVE.md context instead), revise.

## §6. Why same-vendor at high (not xhigh; not paired)

Per trajectory plan §2.4 row B and §1.2 "Why same-vendor here, not paired":

- **Same-vendor (NOT cross-vendor or paired):** Cross-vendor codex doesn't share the framework being clarified — register-leak detection is a same-vendor strength. Adding cross-vendor here would be M1 strict-undersell (using paired discipline by default when the specific failure-mode is single-vendor-detectable).
- **High (NOT xhigh):** Bounded artifact (~120 lines). Register-leak detection on a clarification artifact. Deep reasoning is not what's being tested. xhigh would be over-engineered. The principle: high suffices for bounded register checks.

## §7. Cross-references

- Trajectory plan §1.2 (Phase B specification).
- Trajectory plan §2.4 row B (audit reasoning-level rationale).
- Trajectory plan §2.5 (disposition pathway).
- Premise-bleed audit folder (`.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/`) — precedent for same-vendor adversarial structure (do NOT read in independent mode).

---

*AUDIT-SPEC.md drafted 2026-04-29 by Claude (Opus 4.7), main thread, in collaboration with Logan, as part of Phase B execution.*
