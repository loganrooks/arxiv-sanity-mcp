---
type: audit-disposition-surface
audit: 2026-04-30-phase-d-entry-audit
date: 2026-04-30
authoring_discipline: |
  Per STEP1-DISPOSITION.md precedent (Phase D entry Step 1) + Phase C DISPOSITION.md
  precedent (audit-arc disposition with reasoning trail). Claude (Opus 4.7, /effort
  max) surfaces per-finding disposition + reasoning + adversarial defense + sensitivity
  map + acknowledged audit-priority risks. Logan disposes verbatim after reading.
  D5a recursion acknowledged: this DISPOSITION.md inherits Logan-framing inheritance
  (Logan asked the question that shaped the structure: "How would you dispose each
  axis and why?"); §4 acknowledged-audit-priority-risks records the recursion.
disposed_by: Logan Rooks
disposition: option 3 — Revise-before-dispatch (combined signal, full-width with B1 absorbed)
authority: AUDIT-SPEC.md §7 (Phase D entry) + AUDIT-SPEC.md §8 universal disposition pathway
status: applied (revisions per §2 sequence; Phase D dispatch follows Step 6 green-light)
---

# Phase D Entry Audit — Disposition Surface

## §0. Disposition

**Logan-disposed 2026-04-30 (/effort xhigh): "lets go with your recommendation"** — i.e., Claude's recommendation surfaced at §5 of this DISPOSITION.md (option 3 — Revise-before-dispatch combined-signal-shape, with B1 absorbed per §1.2 defense; not the §3.3 narrower variant).

**Disposition triggering exchange:**
- Logan (2026-04-30 /effort max): "How would you dispose each axis and why? Be transparent in your reasoning, render it auditable, be ready to be challenged on all fronts, if your position is defensible then defend it, but do so honestly... Map out the disposition space, how recommendations might change if certain other salient factors of the design situation changed."
- Claude surfaced this DISPOSITION.md with §1 per-finding reasoning + §2 revision plan + §3 sensitivity map (8 scenarios) + §4 acknowledged audit-priority risks (6 items) + §5 disposition options + §6 application plan; recommended option 3 OR option 4 conditional on B1 disposition.
- Logan (2026-04-30 /effort xhigh): "lets go with your recommendation". Disposition is option 3 — combined signal full-width including B1 absorption per §1.2 defense (audit's coverage-vs-replacement counter is decisive over acausal-runtime push-back).

**Disposition shape:** All 11 findings disposed accept-and-revise per §1; revisions applied per §2 sequence (items 1-11) in single revision commit; STEP1-DISPOSITION.md + STEP1-design-space.md + STEP2-practical-decisions.md + MINI-SPEC.md + STEP4-gates-and-L-tier.md edited; EXECUTION-LOG.md template extended with H5 inline-tagging discipline + heal-skill observation hook; DISPOSITION.md §0 + frontmatter updated to applied state; STATE.md + OVERVIEW.md coordination updated; Phase D dispatch follows Step 6 green-light per AUDIT-SPEC.md §7 pathway.

**§4 acknowledged audit-priority risks carried forward.** Logan-disposition does not bypass them; Phase E reads against them. Specifically risk #1 (D5a recursion at this DISPOSITION.md) + risk #6 (cost-estimate may be optimistic; ~50% buffer recommended) remain operative.

## §0.1 Summary (pre-disposition signal — preserved for trail)

Combined audit signal from DIFFERENTIAL.md §5: **Revise-before-dispatch (narrow), with B-derived addenda folded.** Twelve distinct concerns after deduplicating two convergent findings. Driver: A1 hard-blocker (Class C, source-grounded; the E/A comparator collision mechanics confound P1/P4/success criteria).

Claude-surfaced per-finding disposition: **Accept-and-revise on 11 of 12 findings**, with one cluster (A2 + B1) treated as a single combined inventory revision. One Class C item (A1) is hard-blocker requiring resolution before dispatch. Five Class B items (A2+B1, A3, A4, A5+B2, B3) are source-grounded or methodology-grounded revisions. Five Class A items (A6+B7, A7, B4, B5, B6) are light revisions or addenda batch-able with the larger revision commit.

Estimated cost: ~6-8 hours for items 1-6 (revisions); ~30-90 minutes for items 7-11 (light revisions / addenda batch). Single revision commit feasible in autonomous mode after Logan-disposition.

Logan disposed option 3 per AUDIT-SPEC.md §7 pathway at the §0 turn above.

## §1. Per-finding disposition

### §1.1 F-PD-A1 — E/A comparator mechanics (Class C, hard-blocker)

**Disposition:** Accept; revise. Apply option (i) — distinct names: `decision-trace` for E (in-tree); `decision-trace-r4` for A (user-side R4 comparator).

**Reasoning:**
- Source-grounded per A: `resource-loader.ts:559, 596-598` syncs bundled `resources/skills` to `~/.agents/skills` at init; `syncResourceDir 256-275` removes destination subdirectories before copy; `skills.ts:401-417` first-wins collision. With same name, Shape A user-side primitive cannot persist alongside Shape E in-tree primitive — the bundled-skill sync overwrites at init time. Current MINI-SPEC §2.1 P1 ("Both E and A appear") and §2.1 P4 ("first-wins resolution + collision diagnostic") would test gsd-2's install/sync/collision behavior, NOT R2-vs-R4 decision-trace contrast.
- Option (i) preserves R-strategy contrast at the layer that matters: residence-path (in-tree-via-bundle vs user-side-via-installation), not name-identity.
- Cost: ~10-15 min. Rename in MINI-SPEC §1.A; update §2.1 P1 + P4; add B5c sub-test row in §2.2 ("if same-name registration were attempted under collision policy, what would happen?") to preserve the collision-policy data as a sub-observation without contaminating R-strategy contrast.

**Adversarial challenge:** "Distinct names mean Shape A isn't being compared against the SAME skill Shape E would install — you're not really testing R4 if the user-side primitive has a different name from the in-tree analog."

**Defense:** R-strategy is about residence-path, not name-identity. R4 (orchestrate-without-modifying) ships as a user-side primitive; in real R4 deployment, names diverge whenever the in-tree analog ships under a different name. The test-task should produce identical input/output workload regardless of name. Defense holds.

**Counter-defense (preempted):** Adversarial position (iii) (collision-as-test) is a coherent alternative — Phase D evidence becomes "gsd-2 first-wins is the collision policy; this means user-side R4 primitives are blocked when bundled-skill ships same name; therefore R4 strategy needs distinct naming convention." This produces real R4-design data BUT conflates with R-strategy contrast. Option (i) + B5c sub-test row gives both data-streams cleanly.

### §1.2 F-PD-A2 + F-PD-B1 — Existing-primitives inventory (Class B + C, combined)

**Disposition:** Accept; revise as combined inventory pass.

**Reasoning:**
- A2 source-grounded: `workflow-tools.ts:606-608, 1246-1255, 1401-1415` (gsd_decision_save MCP tool); `GSD-WORKFLOW.md:234-260` (canonical DECISIONS.md table); `db-writer.ts:76-112, 455-489, 572-604` (canonical-table-generator + saveDecisionToDb + dual-write structured memory). gsd-2 has a richer existing decision-record substrate than corpus inventoried.
- B1 structural argument: M2 §0/§3 identifies `/gsdr:deliberate` as **decisive** structural overlap with decision-trace semantics — implementing trigger taxonomy + severe-testing + falsifiable predictions + evaluation-status lifecycle on `.planning/deliberations/` (the same artifact class). When STEP1-design-space §1.3 dropped gsdr-side candidate-shapes on R-strategy grounds, it operationalized the drop by also dropping `/gsdr:deliberate` from the prior-art comparator inventory — a different question.
- Two distinct gaps: gsd-2-INTERNAL substrate (A2) + gsd-2-ADJACENT-RUNTIME prior-art (B1). Combined inventory revision touches both.
- Cost: ~30-60 min. STEP1-design-space §1.3 inventory adds (a) row for `gsd_decision_save` + DECISIONS.md + db-writer pipeline; (b) row preserving `/gsdr:deliberate` as prior-art-not-candidate-shape with acausal-runtime grounds spelled out. STEP4 §3 row 4 status reframed from "complete" to "pass performed; open primitives carried into audit." MINI-SPEC §2.2 adds B5b row (differentiation from `gsd_decision_save` / DECISIONS.md / db-writer) + B5c row (differentiation from `/gsdr:deliberate`'s deliberation-shape).

**Adversarial challenge to B1 acceptance:** "gsd-2 cannot consume `/gsdr:deliberate` from gsd-2 runtime; the comparison is acausal; adjacency-runtime is OOS for Phase D scope."

**Defense:** Acausality dissolves the *replacement* question (correct: can't use it instead), not the *coverage* question (does the work already get done in adjacent runtime). RELATIONSHIP-TO-PARENT.md §1 frames substrate as "gsd-2 + Claude Code runtime + dev tooling + organizational conventions jointly" — adjacency-runtime IS in-scope for substrate-shape evaluation, even if not in-scope for R-strategy candidate-shape selection. Phase E will ask "did decision-trace's evidence justify building in-tree alongside an existing slash-command-shape primitive?" — Phase D evidence cannot answer that without naming the comparator.

**Narrower-rejection alternative path:** Accept A2; reject B1 on narrow OOS grounds. This is defensible if the stated scope of Phase D is "gsd-2 internal substrate-shape evidence only" — record explicitly in DISPOSITION.md. Cost reduction: ~30 min. Risk: Phase E may resurface the question, requiring loop-back. My recommendation is to absorb B1 now (cost asymmetry favors absorption), but Logan-discretion holds.

### §1.3 F-PD-A3 — P5 layer-attribution success criterion (Class B)

**Disposition:** Accept; revise (option i — downgrade success criterion).

**Reasoning:**
- Source-grounded: `preferences.ts:149-201` merges global+project then applies token-profile defaults + mode defaults as lower-priority; `LoadedGSDPreferences` (preferences-types.ts:485-491) exposes `path`, `scope`, `preferences`, `warnings` — no per-field provenance. `preferences-validation.ts:52-60` warns on unknown keys + says they are ignored (confirms P5 silent-drop adjacent open question).
- MINI-SPEC §2.2 B3 currently requires "preserve project/global/profile/mode layer attribution" as success criterion. Direct file reads CAN'T recover all field-level provenance because gsd-2 itself does not surface it.
- Option (i) downgrades B3: "trace explicit file-origin (PREFERENCES.md / project.md scope) and mark derived defaults (token-profile / mode) as 'unresolved without inspection of preferences.ts merge logic.'"
- Option (ii) (add tributary emitting per-field provenance) is Phase E-scoped per axis 1 disposition (Phase D is in-tree skill, not gsd-2 source amendment). Within Phase D's 8-day budget, downgrading is cheaper.
- Cost: ~15 min. Single MINI-SPEC §2.2 B3 wording change.

**Adversarial challenge:** "If the skill marks fields as 'unresolved,' it loses its core value — the user wanted decision-trace to BE the layer-attribution explainer."

**Defense:** Decision-trace's primary value is recovering decision-trace from `.planning/deliberations/` outputs, not from preferences-system internals. Preference-attribution is one input the skill might cite, not the skill's primary work. Marking limitations is honest scoping; Phase E or future phase can decide whether tributary is justified. Defense holds.

### §1.4 F-PD-A4 — Unit-context-manifest activation matrix (Class B)

**Disposition:** Accept; revise.

**Reasoning:**
- Source-grounded: `unit-context-composer.ts:1-21, 149-187` (composeUnitContext is current Phase 3.5 surface); `unit-context-manifest.ts:402-421` (complete-milestone has `preferences:"active-only"`); `unit-context-manifest.ts:508-523` (reassess-roadmap has `preferences:"none"`); `auto-prompts.ts:827-840`. Activation surface is 5-dimensional: catalog visibility / explicit activation / auto-discovery / unit-context-manifest skill mode / preference-inlining policy.
- Concrete contradiction in test design: MINI-SPEC §2.2 P3 specifies reassess-roadmap as activation-test surface AND B3 specifies preferences-attribution as success criterion. But reassess-roadmap has `preferences:"none"` — preferences are not inlined into that unit-context. P5 caveat behavior is non-observable in that unit context.
- Cost: ~1-2h. STEP2 §2.M4 + MINI-SPEC §1.E + §6 add 5-dim activation matrix table. Per-test-step matrix says which dimension is observable. Replace reassess-roadmap with a `preferences:"active-only"` unit-type for P5-attribution test surface (e.g., complete-milestone).

**Adversarial challenge:** "Adding 5-dim matrix bloats the mini-spec; you should just say 'observed in compatible unit-types.'"

**Defense:** The matrix makes test-design legible to Phase D executor. Without it, the executor has to derive the activation surface from source at execution time, increasing failure modes (per §0.6 execution-error). Spike-program discipline (METHODOLOGY.md) wants test-design legibility. Defense holds.

### §1.5 F-PD-A5 + F-PD-B2 — Test-task D5a inheritance (Class B, convergent)

**Disposition:** Accept; revise. Add non-co-produced primary task to MINI-SPEC §2.3.

**Reasoning:**
- Convergent across both auditors. Current test-task = 2026-04-28 framing-widening deliberation. That artifact is co-produced by current-session Claude+Logan. Phase D evidence reads: "skill reconstructed decision-trace from a deliberation it was framed alongside" — circular by D5a leak.
- Suggested fix: pick existing pre-current-arc deliberation from `.planning/deliberations/` (e.g., 2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md or earlier). Different session-context, different framing trajectory, different reasoning patterns — D5a-low (not zero, but materially reduced).
- Cost: ~30 min. Pick artifact + amend MINI-SPEC §2.3 + adjust B4 falsifier wording to reflect lower-D5a anchor.

**Adversarial challenge:** "Even pre-arc deliberations were authored by Logan+Claude — D5a-zero is impossible."

**Defense:** D5a is a gradient, not binary. "Low D5a" means framing inheritance is materially weaker. Phase D evidence on a low-D5a test-task is more diagnostic than evidence on a high-D5a test-task. The test isn't "produce zero-inheritance test-task" — it's "produce evidence that the skill works on something OTHER than its co-produced framing-source." Defense holds.

### §1.6 F-PD-A6 + F-PD-B7 — STEP4 18/20 checklist overclaim (Class A, convergent)

**Disposition:** Accept; revise (single edit absorbing both).

**Reasoning:**
- Convergent. Both auditors flag: row labels conflate "artifact exists" with "discipline performed." H3 row "existing-primitives inventory complete" overclaims (per A2 + B1 — inventory had two systematic gaps).
- Cost: ~15-30 min. STEP4 §3 reframes row labels from "X complete" to "X pass performed: yes/no" or "X artifact-presence: yes/no" depending on what the row tracks. H3 row reframes to "existing-primitives inventory pass performed; open primitives carried into audit (A2 + B1 found further gaps; addressed in revision)."

**No serious adversarial challenge.** Accept.

### §1.7 F-PD-A7 — Heal-skill observation hook (Class A)

**Disposition:** Accept; addendum (FINDINGS.md / EXECUTION-LOG.md template).

**Reasoning:**
- Heal-skill exclusion from STEP2 ≤2 touchpoint envelope is acceptable. Phase D execution can log non-implementation observation without integrating heal-skill subsystem.
- Cost: ~5 min. Add observation-line to EXECUTION-LOG.md / FINDINGS.md template: "Did this run reveal anything skill-health should capture?"
- Doesn't require corpus revision; lives in the execution-template that Phase D writes to.

**No adversarial challenge.** Accept as addendum.

### §1.8 F-PD-B3 — H5 channel-separation declared rule vs built-in mechanism (Class B)

**Disposition:** Accept; revise (extend §8.4 inline-tagging pattern to §7.3 H5).

**Reasoning:**
- MINI-SPEC §7 specifies per-claim audit at FINDINGS.md drafting time (each load-bearing claim labeled `(a)` / `(b)` / `(a→b)`). The discipline is enforced by auditor reading FINDINGS.md, not by anything FINDINGS.md itself does. Cycle: Claude writes evidence → Claude labels evidence → audit reads labels-plus-evidence; if Claude unconsciously bridges (a)→(b) at FINDINGS.md drafting, the labels themselves are co-produced.
- §8.4-style operational extension to §7.3: EXECUTION-LOG.md inline-tags channel-(a)/(b)/(a→b) at observation-time using same inline-discipline as §8.4 M5 categorization. FINDINGS.md inherits inline tags; relabeling at drafting time requires explicit reasoning.
- Consistent with corpus's own mitigation pattern (§8.4 M5 already uses inline-tagging for per-decision categorization). Extension is precedent-grounded.
- Cost: ~30 min. Add inline-tagging discipline to MINI-SPEC §7.3 + EXECUTION-LOG.md template.

**Adversarial challenge:** "Inline-tagging at observation-time is also Claude-authored — same risk recurs."

**Defense:** Yes, but with different timing-shape. Observation-time labeling is contemporaneous with the observation event; post-hoc labeling at FINDINGS.md drafting is reflective. Contemporaneous labeling is harder to bridge unconsciously because the observation hasn't yet been integrated into a finding-narrative. Not zero-D5a but lower-D5a than post-hoc. Defense holds.

### §1.9 F-PD-B4 — Stack D foreclosure shallow-match (Class A)

**Disposition:** Accept; surgical revision.

**Reasoning:**
- STEP1-DISPOSITION §2.A reasoning chain item 5 reaches for "Stack D foreclosed" pattern as license for Shape E over Shape D. The structural similarity is real; the dispositional weight is shallow — the ground for E over D should be Phase-D-internal, not pattern-match from product trajectory.
- Single-sentence amendment: "Item 5 is rhetorical reinforcement; the disposition rests on items 1-4. Phase D entry audit can disregard item 5 if it does not add ground beyond items 1-4."
- Cost: ~5 min.

**No adversarial challenge.** Accept.

### §1.10 F-PD-B5 — /effort sequence procedural-clarification (Class A)

**Disposition:** Accept; surgical revision (standing clarification at §0).

**Reasoning:**
- STEP1-DISPOSITION §5 #6 already disclaims this; B5's point is the disclaimer is mid-document while recurrence across multiple frontmatters elevates the framing risk.
- Standing-clarification at top of STEP1-DISPOSITION.md §0: "References to /effort max → /effort xhigh sequence in this corpus's provenance blocks are procedural-traceability records, not disposition-authority claims."
- Cost: ~5 min.

**No adversarial challenge.** Accept.

### §1.11 F-PD-B6 — H/M/L tier convergence-check (Class A)

**Disposition:** Accept; surgical revision.

**Reasoning:**
- §7.10.0 + §7.10.6 disclaim H/M/L as observed taxonomy. STEP4 §2 then uses L1-L8 enumeration as a checklist with status-per-L-item. L4 + L6 are arguably the same observation under different framings.
- Single sentence in STEP4 §2 preamble: "L-items are organizing tier per §7.10.0; not assumed orthogonal. Convergence noted in §3 rather than registered as separate items."
- Cost: ~5 min.

**No adversarial challenge.** Accept.

## §2. Combined revision plan (if Logan accepts §1 wholesale)

**Sequence:**

1. F-PD-A1 — MINI-SPEC §1.A rename + §2.1 P1/P4 + §2.2 add B5c sub-test (~15 min).
2. F-PD-A2 + F-PD-B1 — STEP1-design-space §1.3 inventory + STEP4 §3 row 4 status + MINI-SPEC §2.2 B5b + B5c (~45 min).
3. F-PD-A3 — MINI-SPEC §2.2 B3 wording (~15 min).
4. F-PD-A4 — STEP2 §2.M4 + MINI-SPEC §1.E + §6 activation matrix (~90 min).
5. F-PD-A5 + F-PD-B2 — MINI-SPEC §2.3 test-task swap (~30 min).
6. F-PD-B3 — MINI-SPEC §7.3 + EXECUTION-LOG.md template (~30 min).
7. F-PD-A6 + F-PD-B7 — STEP4 §3 + §4 rephrase (~20 min).
8. F-PD-A7 — EXECUTION-LOG.md template observation hook (~5 min).
9. F-PD-B4 — STEP1-DISPOSITION §2.A item 5 (~5 min).
10. F-PD-B5 — STEP1-DISPOSITION §0 standing-clarification (~5 min).
11. F-PD-B6 — STEP4 §2 preamble (~5 min).

**Total estimated cost:** ~4-5 hours focused work. Lower than DIFFERENTIAL.md §5 estimate (6-8h) because items 7-11 are tighter than estimated; items 1-6 substantive at the source-grounded core.

**Commit shape:** single revision commit covering items 1-11 + DISPOSITION.md + this file's frontmatter status update. Coordination updates (STATE.md + OVERVIEW.md §11.6.11 or §11.7) batch into Phase D atomic.

## §3. Sensitivity map — how disposition shifts under different design factors

### §3.1 Phase D budget reduced (8 → 4 days)
- A1 still hard-blocker; same disposition (option i).
- A2+B1 may compress to A2-only (drop gsdr prior-art row); narrower-rejection of B1 becomes more defensible under tighter scope.
- A3 already cheap; same.
- A4 matrix compresses to "drop reassess-roadmap as P5-test-surface; defer matrix to Phase E."
- A5+B2 same.
- B3 may demote to "noted in §9 deferred items."
- Items 7-11 all cheap; same.

### §3.2 Cross-vendor audit had not fired (only B audit available)
- Disposition would have been Addendum-shape per B's signal.
- A1/A2/A3/A4 source-grounded findings would be entirely missing.
- Phase D would dispatch with confounded comparator (A1) and discover mechanics issue at execution time, requiring loop-back to Phase C/D entry.
- This is the M1 paired-review property's value-add demonstrated: cross-vendor catches what same-vendor's lens-position can't reach.

### §3.3 Logan accepts B1 narrower-rejection (acausal-runtime grounds)
- Combined disposition shifts to Revise-before-dispatch (narrow), 5 substantive revisions instead of 6.
- A2 alone covers gsd-2-internal inventory gap.
- B1 explicitly recorded as deferred-with-acausal-runtime-grounds in DISPOSITION.md §6 cross-reference.
- Phase E reads stability against bounded-scope corpus; may resurface B1 if substrate-shape evidence warrants.
- Cost reduction: ~30 min. Risk: future loop-back if Phase E catches what Phase D scoped out.

### §3.4 Logan accepts A1 option (iii) collision-as-test
- Phase D evidence becomes "gsd-2's collision policy when same-name skills collide; first-wins resolution."
- R-strategy contrast must come from differentiated outputs (e.g., decision-trace produces different content from /gsdr:deliberate even with same name in different runtimes).
- Higher risk for Phase E re-disposition; lower scientific-confidence on R-strategy evidence.
- Likely cost: same as option (i) but evidence-quality lower.

### §3.5 First-target shape changed from in-tree skill (E) to user-side workflow (A)
- Axis 1 disposition reverses (settled per STEP1-DISPOSITION); A1 mechanics flips direction.
- Out-of-scope for Phase D entry audit; would re-disposition Step 1 and require new Phase D entry audit.

### §3.6 `/gsdr:deliberate` were in gsd-2-internal (not gsdr-adjacent)
- B1 dissolves entirely (no acausal-runtime question; comparison is internal-vs-internal).
- A2 substrate-DB inventory gap remains.
- Decision-trace re-frames as clearer R2 extension/refactor of an existing internal primitive.
- Would re-disposition axis 1 (E vs B-extension-of-deliberate would become live).

### §3.7 Phase D budget extended (8 → 12 days)
- A4 matrix could expand to include tributary work (option ii for A3 — tributary emitting per-field preferences provenance).
- A5+B2 could accommodate multiple non-co-produced test-tasks.
- B3 inline-tagging could be paired with auditor verification step.
- Items 1-11 same; additional items become live.

### §3.8 Re-architect (4th option) becomes warranted
- Would happen if A1 + B1 jointly suggested entire Phase D entry corpus is structurally compromised.
- I do not read evidence as supporting this. 10 of 12 findings are local revisions. A1's mechanics issue is significant but solvable with renaming; the dispositions at axis level (E primary; A R4-comparator) remain defensible after audit.
- Re-architect would require Logan-discretion override of the audit's narrower disposition signal; defensible only if Logan reads the cumulative pattern as deeper substrate-confusion the audit lenses didn't reach.

## §4. Acknowledged audit-priority risks for Logan-disposition

Per §0.5 D5a recursion + traces-over-erasure discipline. Logan disposes; these are flagged for adversarial pressure-test.

1. **D5a recursion at this DISPOSITION.md.** Logan asked the question that shaped the structure ("How would you dispose each axis and why?"). This DISPOSITION.md inherits Logan-framing inheritance. If the framing of "dispose-each-axis-with-reasoning" itself biased toward accept-all-and-revise (rather than reject-some-and-narrow), this surface participates in the bias. Mitigation: §1.2 narrower-rejection alternative path explicitly surfaced; §3.3 sensitivity scenario explicitly surfaced. Logan can disposition narrower than my recommendation if the bias-check fires.

2. **A1 option-(i) preference may underweight option-(iii)'s design-data value.** Option (iii) (collision-as-test) is dismissed at §1.1 as conflating R-strategy contrast. But it produces real R4-design data (collision-policy-implies-naming-convention) that option (i) doesn't. My disposition treats this as B5c sub-test absorption, but Logan might prefer option (iii) primary if collision-policy data is more decision-relevant than R-strategy contrast at this Phase D.

3. **A2+B1 absorption framing assumes inventory-completeness is the goal.** Alternative framing: Phase D scope = "decision-trace skill at first-target," not "comprehensive inventory of decision-record primitives." If the latter is OOS for this Phase D, both A2 (gsd-2-internal substrate gap) and B1 (gsdr prior-art gap) become OOS; the corpus's narrower scoping was correct and the audit overreached. I find the audit's argument decisive (per §1.2 defense), but Logan-discretion holds.

4. **A4 5-dim matrix may be over-engineered.** B's lens didn't catch this (only A); A's recommendation is to add full matrix. Alternative: minimal matrix (drop reassess-roadmap, replace with compatible unit-type; defer full matrix to Phase E if needed). Logan-discretion to pick scope.

5. **B3 inline-tagging extension may face the same recursion B3 itself catches.** I argue at §1.8 defense that observation-time labeling is lower-D5a than post-hoc. But "lower" is not "zero" — the recursion is genuinely partial mitigation. Logan might prefer to demote B3 to deferred-items per §9 if "partial mitigation" reads as "performative-vs-operational openness."

6. **Estimated revision cost (4-5h vs DIFFERENTIAL.md's 6-8h) may be optimistic.** Source-grounded revisions (items 2-4) often take longer than estimated because each touches multiple surfaces and triggers re-checks of downstream coherence. Logan should buffer the estimate by ~50% if planning around it. If actual cost exceeds 6h, possible signal that scope of revision is broader than dispositioned — pause + reassess.

## §5. Disposition options (Logan picks)

Per AUDIT-SPEC.md §7 universal:

1. **Accept-as-is.** Class A only readable; B1 + A1 + A2/A3/A4 dismissed. (Not recommended; A1 hard-blocker per source-grounded mechanics.)
2. **Addendum-shape** (B's signal). Items folded as §10 addendum at INCUBATION-CHECKPOINT.md §7.10 or new MINI-SPEC §10. Phase D dispatch proceeds with caveats. (Defensible if A1 read as not-blocker.)
3. **Revise-before-dispatch** (combined signal — Claude-recommended). Apply §1 dispositions per §2 revision plan. Phase D dispatch follows revision commit + Step 6 Logan green-light.
4. **Revise-before-dispatch (narrower variant).** Same as 3 but with §3.3 narrower-rejection of B1; A2 alone covers inventory gap. Cost: ~30 min less.
5. **Re-architect.** Step 1-4 work re-disposed. (Not recommended; §3.8 sensitivity argues against.)

**Claude-surfaced recommendation:** option 3 OR option 4 depending on §3.3 disposition of B1.

## §6. Application plan (post-disposition)

If Logan disposes option 3 (or 4):
1. Apply revisions per §2 sequence. Single revision commit.
2. Update this DISPOSITION.md frontmatter status from "surfaced" to "applied."
3. Update DISPOSITION.md §0 with verbatim Logan-disposition language.
4. Update STATE.md (Phase D entry → Step 6 awaiting green-light).
5. Update OVERVIEW.md (§11.6.11 or §11.7 Phase D entry audit-arc + disposition).
6. Verify clean tree.
7. Surface to Logan for Step 6 green-light.

If Logan disposes option 1 (Accept-as-is):
1. Update §0 with verbatim Logan-disposition.
2. STATE.md + OVERVIEW.md updates.
3. Surface to Logan for Step 6 green-light + Phase D atomic commit.

If Logan disposes option 2 (Addendum-shape):
1. Draft addendum at INCUBATION-CHECKPOINT.md §7.10 or MINI-SPEC §10 covering all 12 findings.
2. Update §0 + STATE.md + OVERVIEW.md.
3. Surface to Logan for Step 6 green-light.

## §7. Cross-references

- `audit-findings-A.md` (cross-vendor codex GPT-5.5 high; 7 findings: 1C/4B/2A; non-binding signal: Revise-before-dispatch narrow)
- `audit-findings-B.md` (same-vendor adversarial-auditor xhigh; 7 findings: 1C/3B/3A; non-binding signal: Addendum-shape with one targeted revision)
- `DIFFERENTIAL.md` (main-thread reconciliation; combined signal: Revise-before-dispatch narrow with B-derived addenda folded)
- `POST-MORTEM.md` (codex attempt-1 hung-stdin investigation)
- `AUDIT-SPEC.md` §7 (disposition pathway; this DISPOSITION.md follows)
- Phase D entry corpus under audit:
  - `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.10
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md`
  - `.planning/gsd-2-uplift/wave-2/decision-trace/MINI-SPEC.md`
  - `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP4-gates-and-L-tier.md`
- Phase C precedent (audit-arc disposition with reasoning trail + Option 4 hybrid):
  - `.planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/DISPOSITION.md`

---

*DISPOSITION.md surfaced by main-thread Claude (Opus 4.7, /effort max) 2026-04-30 per Logan-prompted disposition-surfacing-with-adversarial-defense pattern (parallel to STEP1-DISPOSITION.md). Logan-disposition pending. The §1 per-finding reasoning + §2 revision plan + §3 sensitivity map + §4 acknowledged-audit-priority-risks + §5 disposition options are surfaced for Logan-disposition; verbatim Logan-disposition language replaces "pending" frontmatter status + §0 summary on disposition. The in-session-collaboration risk applies recursively to this DISPOSITION.md itself per §4 risk #1; Logan-disposition is the structural correction.*
