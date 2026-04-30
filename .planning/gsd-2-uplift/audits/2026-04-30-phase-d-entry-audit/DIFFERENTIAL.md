---
type: audit-differential
date: 2026-04-30
status: complete
audit_folder: .planning/gsd-2-uplift/audits/2026-04-30-phase-d-entry-audit/
inputs:
  - audit-findings-A.md (cross-vendor codex GPT-5.5 high; 7 findings: 1C/4B/2A; disposition: Revise-before-dispatch, narrow)
  - audit-findings-B.md (same-vendor adversarial-auditor xhigh; 7 findings: 1C/3B/3A; disposition: Addendum-shape with one targeted revision)
authoring_discipline: |
  Differential analysis authored by main-thread Claude (Opus 4.7, /effort xhigh)
  2026-04-30 reading both audit findings together for the first time. Per
  premise-bleed audit precedent + Phase C precedent, differential is main-thread
  reconciliation, not auditor-produced; auditors remained in independent mode.
  This artifact synthesizes convergence + divergence into a combined disposition
  signal for Logan-disposition at DISPOSITION.md.
---

# DIFFERENTIAL.md — Phase D Entry Audit

## §0. Summary

Both auditors completed independently and produced complementary findings. The M1 paired-review property is strongly confirmed: cross-vendor (A) caught substantive/source divergence at the dispatch-mechanics layer; same-vendor (B) caught integration-grammar-as-fact + methodological-discipline-leak at the meta-layer. Two convergent findings (test-task D5a; checklist overclaim) provide calibration evidence that the corpus's transparency-coverage is partial — both auditors converged on risks the corpus itself surfaced but did not act on.

**Combined class breakdown across A + B:** 2 Class C (1 each, non-overlapping), 7 Class B (4 from A + 3 from B), 5 Class A (2 from A + 3 from B). After deduplicating the two convergent findings, **12 distinct concerns** carry into disposition.

**Combined disposition signal: Revise-before-dispatch (narrow), with B-derived addenda folded.**

A's "Revise-before-dispatch, narrow" is the stronger disposition; B's "Addendum-shape with one targeted revision" reads as appropriate within B's lens but understates the source-grounded mechanics issues A surfaced. Logan-disposition at DISPOSITION.md decides scope (revision items 1-5 below) + addenda (items 6-12).

## §1. Convergent findings (calibration evidence)

Both auditors independently surfaced these. Convergence does NOT diminish them — calibration evidence is still evidence. The corpus self-acknowledged each but did not act on the acknowledgment, which is the audit's value-add.

### Convergence-1 — Test-task D5a inheritance (A5 ↔ B2)

| | Audit A | Audit B |
|---|---|---|
| Class | A | B |
| Confidence | medium | high |
| Lens | D5a leak / negative-space | D5a leak / evidence-load |
| Where | STEP2 §2.M4; MINI-SPEC §2.3/§9 | MINI-SPEC §2.3, §9 #6 |
| Suggested fix | Add one low-inheritance comparator task | Amend §2.3 to add non-co-produced primary task |

**Differential:** B classes higher (B vs A) and higher confidence. B's argument is sharper: the mini-spec's "test surfaces whether decision-trace reconstruction can preserve the in-session-collaboration trail vs erasing it" inverts the failure mode. A converges on the same gap. Combined: **Class B, high confidence**; one non-co-produced primary task added before dispatch.

### Convergence-2 — STEP4 checklist artifact-existence vs discipline-completion (A6 ↔ B7)

| | Audit A | Audit B |
|---|---|---|
| Class | A | A |
| Confidence | high | medium |
| Lens | evidence-load / framing-leak | methodological-discipline-leak |
| Where | STEP4 §3, §4 | STEP4 §3, §4 #3 |
| Suggested fix | Rename row from "inventory complete" to "inventory pass performed; open primitives carried into audit" | Reframe "Checklist completion: 18/20" to "Checklist artifact-presence: 18/20" |

**Differential:** Both Class A. A specifically flags H3 row (existing-primitives inventory complete) as overclaiming; B flags the entire 18/20 framing. Combined: **Class A, high confidence**; one rephrasing absorbing both — STEP4 §3 reframes row labels + completion claim simultaneously.

## §2. A-only findings (cross-vendor strength: source-grounded substantive divergence)

### F-PD-A1 — E/A comparator mechanics confounded by gsd-2 skill sync + collision

**Class C, high confidence. Cross-vendor unique catch — the audit's most consequential finding.**

A1 grounds in source: `resource-loader.ts:559, 596-598` (initResources defaults skillsDir to `~/.agents/skills` and syncs bundled `resources/skills` there); `resource-loader.ts:256-275` (syncResourceDir removes destination subdirectories before copying); `skills.ts:401-417` (skill loader dedupes by name with first-wins collision). MINI-SPEC §1.E + §1.A both define `name=decision-trace`, then §2.1 P1 says "Both E and A appear" + P4 says "first-wins resolution + collision diagnostic emitted in logs."

**The contradiction is mechanical:** the bundled-skill sync overwrites the user-side location at `initResources` time; even if both files can be staged, the observable prompt block cannot satisfy "both appear" under the same name. The current P1/P4/success wording would test install/sync/collision artifacts, NOT R2-vs-R4 decision-trace mechanics.

**B did not catch this** — B's lens emphasis was meta-level (integration-grammar-as-fact); B accepted the comparator setup as drafted and probed its inherited framings, not its source-mechanics.

**Why this is hard-blocker for dispatch:** Phase D evidence under the current P1/P4/success criteria would be ambiguous-by-construction. Phase E reading "decision-trace works as in-tree skill" against ambiguous evidence would re-disposition the wrong axis.

**Suggested fixes (per A's recommendation):** EITHER (i) use distinct names (`decision-trace` for E; `decision-trace-r4` for A) preserving R-strategy contrast at name level; OR (ii) sequential A-only / E-only observations rather than simultaneous same-name registration; OR (iii) explicitly define the collision itself as the test and drop "both appear" as pass condition. Logan-discretion to pick; (i) preserves the cleanest semantic contrast; (ii) preserves cleanest install-side independence; (iii) accepts the collision as data.

### F-PD-A2 — Existing gsd-2 decision primitives materially under-inventoried

**Class B, high confidence. Cross-vendor unique — source-grounded.**

A2 grounds in source: `packages/mcp-server/src/workflow-tools.ts:606-608, 1246-1255, 1401-1415` (gsd_decision_save / gsd_save_decision MCP tools with structured fields: scope, decision, choice, rationale, revisable, when-context, made-by; tool description "records project decision to GSD database and regenerates DECISIONS.md"); `src/resources/GSD-WORKFLOW.md:234-260` (canonical table-shaped DECISIONS.md register definition); `src/resources/extensions/gsd/db-writer.ts:76-112, 455-489, 572-604` (canonical table generation, structured saveDecisionToDb, dual-write structured memory record).

**The corpus's gap-mapping treats `.gsd/DECISIONS.md` as one-line append-only convention** (M2 §3.B + STEP1-design-space §1.3 + Shape D framing); source shows a richer existing primitive family — DB-backed, MCP-exposed, canonical-table-generated. Shape D was framed as more novel/heavier than gsd-2's actual surface warrants.

**Relationship to B1:** A2 (existing decision-DB substrate) and B1 (`/gsdr:deliberate` prior-art) are complementary, not redundant. A2 catches the gsd-2-INTERNAL substrate under-inventory; B1 catches the gsd-2-ADJACENT-RUNTIME (gsdr/Claude Code) prior-art exclusion. Combined: H3 "existing-primitives inventory complete" claim collapses on two fronts.

**Suggested fix:** decision-trace must be evaluated against the DB-backed decision substrate, not just hand-written `.gsd/DECISIONS.md` lines. E remains primary; B1/B4 tests should include MCP/DB/table/memory path as source material. Shape D-style framing should describe extending an existing structured primitive rather than inventing structure.

### F-PD-A3 — P5 layer-attribution success criterion stricter than available surface

**Class B, high confidence. Cross-vendor unique — source-grounded.**

A3 grounds in source: `src/resources/extensions/gsd/preferences.ts:149-201` (loadEffectiveGSDPreferences merges global + project, then applies token-profile defaults and mode defaults as lower-priority); `preferences-types.ts:485-491` (LoadedGSDPreferences has path, scope, preferences, warnings — no per-field provenance); `preferences-models.ts:431-500` (profile defaults derive concrete model values from registry state); `preferences-validation.ts:52-60` (validation warns on unknown keys + says they are ignored — confirms P5 silent-drop adjacent open question).

**MINI-SPEC §2.2 B3 requires "preserve project/global/profile/mode layer attribution"** as success criterion (read directly from PREFERENCES.md). Direct file reads CAN'T recover all effective defaults or field-level provenance — gsd-2 itself does not expose per-field provenance via its data structures. The mini-spec asks the skill to reconstruct provenance gsd-2 doesn't surface.

**Suggested fix:** EITHER (i) downgrade B3 to "trace explicit file-origin and mark derived defaults as unresolved unless helper evidence is available"; OR (ii) add a tiny tributary that emits effective preferences with field provenance (likely a small change to `preferences.ts` LoadedGSDPreferences shape). (i) preserves Phase D scope; (ii) is Phase E-shaped per axis 1 disposition.

### F-PD-A4 — Unit-context-manifest/composer activation surface broader than skill-manifest.ts

**Class B, medium-high confidence. Cross-vendor unique — source-grounded.**

A4 grounds in source: `src/resources/extensions/gsd/unit-context-composer.ts:1-21, 149-187` (composeUnitContext was added as phase 3.5 v2 surface — NOT future-looking; it's current); `unit-context-manifest.ts:402-421` (complete-milestone has skills:{mode:"all"}, preferences:"active-only", inlines decisions); `unit-context-manifest.ts:508-523` (reassess-roadmap has skills:{mode:"all"}, preferences:"none", inlines decisions); `auto-prompts.ts:827-840, 869-890` (explicit skill activation should not be dropped by unit-type manifest; manifest's "real home" is skill catalog rendering; auto-match gated only under skill_discovery:"auto").

**MINI-SPEC §1.E + STEP2 §2.M4 + MINI-SPEC §6 falsifiers all route activation concern through `skill-manifest.ts`** as the sole/primary second touchpoint. Source shows the activation surface is a 5-dimensional matrix: skill catalog visibility / explicit skill activation / auto-discovery / unit-context manifest skill mode / preference-inlining policy.

**Critical concrete implication:** if `reassess-roadmap` is a test step (it is — per MINI-SPEC §2.2 P3), `preferences: "none"` may make P5 caveat behavior non-observable in that unit context. The skill cannot test layer-attribution under reassess-roadmap because preferences aren't inlined.

**Suggested fix:** Add an activation matrix before dispatch covering all 5 dimensions. Don't assume `skill-manifest.ts` is the only/primary second touchpoint. Update P3 + B3 success criteria conditional on unit-type's preferences policy.

### F-PD-A7 — Heal-skill exclusion acceptable but should become Phase D observation hook

**Class A, medium confidence. Cross-vendor unique.**

Acceptable under STEP2 ≤2 touchpoint envelope, but Phase D can log non-implementation observation: "Did this run reveal anything skill-health should capture?" without implementing skill-health integration.

**Suggested fix:** add observation line to EXECUTION-LOG.md / FINDINGS.md. Don't integrate the subsystem unless another falsifier fires.

## §3. B-only findings (same-vendor strength: meta-level + framing-leak)

### F-PD-B1 — gsdr-drop operationalization removes strongest prior-art comparator

**Class C, high confidence. Same-vendor unique — meta-level catch.**

The corpus drops gsdr-side shapes (B/C from initial proposal) on R-strategy grounds correctly, but operationalizes the drop by silently removing M2's identified decisive prior-art overlap (`/gsdr:deliberate`) from the gap-mapping. STEP1-DISPOSITION §3.A challenge 7 explicitly checks for in-tree `deliberate` and answers "no" — but M2 found `/gsdr:deliberate` in `~/.claude/commands/gsdr/`, not as gsd-2 candidate-shape, but as **prior-art comparator** in adjacent runtime.

**Relationship to A2:** A2 catches gsd-2-INTERNAL decision-DB substrate gap; B1 catches gsd-2-ADJACENT-RUNTIME prior-art gap. Both flag H3 "inventory complete" claim from different angles.

**A did not catch this specific framing** — A noted "existing primitives under-inventoried" but at substrate level (decision-DB family), not at prior-art-as-comparator level for the specific decision-trace semantics overlap.

**Suggested fix:** targeted revision — paragraph in STEP1-design-space §1.3 explicitly preserving `/gsdr:deliberate` as prior-art-not-candidate-shape (with acausal-runtime grounds), + row in MINI-SPEC §2.2 differentiation tests adding "B5b: differentiation from `/gsdr:deliberate`'s deliberation-shape" alongside B5's forensics differentiation.

### F-PD-B3 — H5 channel-separation as declared rule, not built-in mechanism

**Class B, medium-high confidence. Same-vendor unique — methodological-discipline-leak.**

MINI-SPEC §7 specifies per-claim audit at FINDINGS.md drafting time: each load-bearing claim labeled `(a)` / `(b)` / `(a→b)`. The discipline is enforced by the auditor reading FINDINGS.md, not by anything FINDINGS.md itself does. The cycle: Claude writes evidence → Claude labels evidence → audit reads labels-plus-evidence; if Claude unconsciously bridges (a)→(b) at FINDINGS.md drafting, the labels themselves are co-produced.

**Suggested fix:** §8.4-style operational addition to §7.3 — EXECUTION-LOG.md inline-tags channel-(a)/(b)/(a→b) at observation-time using same inline-discipline as §8.4 M5 categorization. FINDINGS.md inherits inline tags; relabeling requires explicit reasoning.

### F-PD-B4 — Stack D foreclosure pattern as shallow-match

**Class A, medium confidence. Same-vendor unique — skill-heuristic shallow-match recurrence at design level.**

STEP1-DISPOSITION §2.A reasoning chain item 5 reaches for the CLAUDE.md "Stack D foreclosed" pattern as license to choose Shape E over Shape D. The structural similarity is real, but the dispositional weight is shallow: the ground for E over D should be Phase-D-internal, not pattern-match from the codebase product trajectory.

**Suggested fix:** single-sentence amendment in STEP1-DISPOSITION.md §2.A item 5: "Item 5 is rhetorical reinforcement; the disposition rests on items 1-4. Phase D entry audit can disregard item 5 if it does not add ground beyond items 1-4."

### F-PD-B5 — /effort max → /effort xhigh sequence as recorded does not constitute independent-disposition-evidence

**Class A, medium confidence. Same-vendor unique — co-production-laundering.**

The framing "Claude surfaced at max + Logan accepted at xhigh" can read as quasi-procedural authentication of the disposition. The disclaimer in §5 #6 mitigates substantially; the recurrence across STEP1-DISPOSITION + STEP2 + STEP4 + MINI-SPEC frontmatters is the risk surface.

**Suggested fix:** standing-clarification at top of STEP1-DISPOSITION.md §0: "References to /effort max → /effort xhigh sequence in this corpus's provenance blocks are procedural-traceability records, not disposition-authority claims."

### F-PD-B6 — H/M/L tier framing recurs as if-observed at §7.10 → corpus boundary

**Class A, medium confidence. Same-vendor unique — integration-grammar-as-fact at meta-level.**

§7.10.0 + §7.10.6 disclaim H/M/L as observed taxonomy. STEP4 §2 then uses L1-L8 enumeration as a checklist with status-per-L-item. L4 + L6 are arguably the same observation under different framings.

**Suggested fix:** single sentence in STEP4 §2 preamble — L-items not assumed orthogonal; convergence noted rather than registered separately.

## §4. M1 paired-review property — confirmation

**Cross-vendor strength (codex GPT-5.5 high) confirmed:**
- Source-grounded substantive divergence: A1 (skill-sync mechanics), A2 (decision-DB substrate), A3 (preferences source structure), A4 (unit-context-composer surface). Each cites specific file:line references in gsd-2 source verifying the claim.
- B did not surface any of these — B's reading was at corpus-internal-coherence layer, not at corpus-vs-source layer.

**Same-vendor strength (Claude Opus 4.7 adversarial-auditor xhigh) confirmed:**
- Meta-level + framing-leak: B1 (substrate-confusion drop operationalization), B3 (declared-rule-vs-built-in-mechanism), B4 (shallow-pattern-match), B5 (co-production-laundering), B6 (integration-grammar-as-fact at tier framing). Each catches a meta-level pattern in the corpus's own reasoning structure.
- A did not surface any of these — A's reading was at source-vs-claim layer, not at corpus-reasoning-structure layer.

**Convergence at low-confidence-but-corroborated boundary:**
- A5 ↔ B2 (test-task D5a) — A medium / B high; B's framing dominates.
- A6 ↔ B7 (checklist overclaim) — A high / B medium; A's specificity (H3 row) dominates.

**Conclusion:** M1 paired-review property holds. Cross-vendor + same-vendor at xhigh-or-equivalent produces complementary findings, not redundancy. The 8 divergent findings (A1-A4 + B1, B3-B6) are genuine value-add from the pairing structure; either alone would have missed half the audit's catch.

## §5. Combined disposition signal

**Combined: Revise-before-dispatch (narrow), with B-derived addenda folded.**

A's "Revise-before-dispatch, narrow" dominates over B's "Addendum-shape with one targeted revision" because:
1. A1 is a hard-blocker (Class C, source-grounded) — dispatching with current P1/P4/success wording produces structurally-confounded evidence.
2. A2 + A3 + A4 jointly require source-grounded mini-spec revisions before dispatch — these aren't addendum-deferrable without losing dispatch-readiness.
3. B's disposition was generated without seeing A's source-mechanics evidence (independent mode); had B seen A1, B's disposition signal likely shifts toward Revise-before-dispatch.

**Required revisions before dispatch (5 items):**

1. **F-PD-A1:** E/A comparator mechanics + P1/P4/success criteria. Pick fix-shape (i)/(ii)/(iii) per A's options.
2. **F-PD-A2 + F-PD-B1:** Existing-primitives inventory completion claim — both gsd-2-internal decision-DB substrate (A2) AND gsd-2-adjacent-runtime gsdr prior-art (B1). Revise STEP1-design-space §1.3 inventory + STEP4 §3 row 4 status + MINI-SPEC §2.2 differentiation tests.
3. **F-PD-A3:** P5 layer-attribution success criterion (B3) — downgrade or add tributary.
4. **F-PD-A4:** Unit-context-manifest activation matrix — Phase D scope add.
5. **F-PD-A5 + F-PD-B2:** Test-task D5a — add non-co-produced primary task to MINI-SPEC §2.3.

**Addenda (can fold into revision commit OR separate addendum):**

6. **F-PD-A6 + F-PD-B7:** STEP4 §3 checklist row labels + completion claim rephrase (convergent — single edit absorbing both).
7. **F-PD-A7:** Heal-skill observation hook — EXECUTION-LOG/FINDINGS observation line.
8. **F-PD-B3:** H5 channel-separation §8.4-style inline-tagging extension.
9. **F-PD-B4:** Stack D foreclosure pattern disclaimer in STEP1-DISPOSITION §2.A item 5.
10. **F-PD-B5:** /effort sequence procedural-clarification at STEP1-DISPOSITION §0.
11. **F-PD-B6:** H/M/L tier convergence-check sentence in STEP4 §2 preamble.
12. **A's "would benefit from xhigh re-dispatch":** A4 only as candidate; A's call is "high was enough for dispatch decision; xhigh would only help for full source-level activation architecture audit before coding." Defer to Logan-discretion at DISPOSITION.md.

**Estimated revision cost:** 6-8 hours for items 1-5 (the 4 source-grounded fixes + the test-task amendment). Items 6-11 are 30-90 min batch-able as an addendum commit alongside or following.

## §6. Calibration evidence about transparency-coverage

The corpus has rendered transparency at every artifact's "audit-priority risks" section. Convergence analysis:

- **Convergent + corpus-acknowledged:** test-task D5a (B2 acknowledges; A5 + B2 catch). Acknowledgment didn't lead to action.
- **Convergent + corpus-acknowledged:** checklist overclaim (STEP4 §4 #3 acknowledges; A6 + B7 catch). Acknowledgment didn't lead to action.
- **A-only + corpus-NOT-acknowledged:** A1, A2, A3, A4 — none of these were in any audit-priority-risks section. **Source-grounded findings live entirely in the audit's value-add space.**
- **B-only + corpus-NOT-acknowledged:** B1 — explicitly checked-but-not-found in audit-priority-risks sections. **Cross-substrate prior-art exclusion lives entirely in the audit's value-add space.**
- **B-only + corpus-acknowledged:** B3 (MINI-SPEC §9 #4); B6 (§7.10.0 + §7.10.6); B7 (STEP4 §4 #3) — acknowledgments present but unacted.

**Pattern:** Transparency-coverage is high (corpus surfaces many of its own risks). Acknowledgment-conversion-to-action is low — most acknowledged risks are not operationalized into mini-spec amendments. The audits' value-add is partly novel-finding (A1-A4, B1) and partly acknowledgment-to-action conversion (B2, B3, B6, B7, A5, A6).

**Implication for Logan-disposition:** the corpus's transparency discipline is genuine but has a delivery gap. Disposition can either (i) convert acknowledged risks to action item-by-item (B's preferred shape: addendum) OR (ii) batch-revise alongside source-grounded fixes (A's preferred shape: revise-before-dispatch). The combined signal recommends (ii) for items 1-5, (i) for items 6-11.

## §7. Cross-references

- `audit-findings-A.md` — cross-vendor codex GPT-5.5 high (this folder)
- `audit-findings-B.md` — same-vendor adversarial-auditor xhigh (this folder)
- `AUDIT-SPEC.md` — paired-audit contract (this folder)
- `POST-MORTEM.md` — codex attempt-1 hung-stdin investigation (this folder)
- Phase D entry corpus (under audit; 6 artifacts):
  - `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.10
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md`
  - `.planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP4-gates-and-L-tier.md`
- DISPOSITION.md — Logan-disposition pending (this folder)

---

*DIFFERENTIAL.md authored by main-thread Claude (Opus 4.7, /effort xhigh) 2026-04-30 reading both audit-findings-A.md + audit-findings-B.md together for the first time. Per premise-bleed audit precedent + Phase C precedent, differential is main-thread reconciliation; auditors remained in independent mode. Combined disposition signal awaits Logan-disposition at DISPOSITION.md.*
