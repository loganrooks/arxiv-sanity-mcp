---
type: phase-D-step-3-mini-spec
date: 2026-04-30
gsd_2_commit: 42ef05fbe (Phase D dispatch baseline; verified main@42ef05fbe, clean tree)
phase: trajectory plan §1.4 Phase D — first-second-wave-target dispatch + execution
sub-step: §7.10.4 Step 3 — mini-spec drafting (gate 3 amended per §7.9.3 (c) + §7.10 H4/H5/M5)
status: |
  Drafted by Claude (Opus 4.7, /effort xhigh, in-session-collaboration with Logan)
  per trajectory plan §7.10.4 Step 3 + §0.7 hybrid autonomy. Logan green-lit
  autonomous Step-2-and-onward at /effort xhigh turn 2026-04-30 with explicit
  correction "you didn't really proceed autonomously because you are checking in
  with me" — Step 3 proceeds without check-in. Mini-spec is the Phase D dispatch
  contract: it specifies what gets built (E + A), what evidence counts (success +
  falsification), what channel separation discipline applies (H5), and what
  per-decision categorization rule fires (M5).

authoring_discipline: |
  Mini-spec is operational-not-philosophical: each section produces a concrete
  artifact / behavior / decision-rule the executor (or reader) can apply
  unambiguously at Phase D execution. Where Step 1/2 reasoned about WHY, Step 3
  specifies WHAT + HOW. Per §7.9.3 (c) addendum: contract requirements include
  artifact produced + skill behavior tested + workflow-template composition scope
  + decision-trace evidence definition + F-discipline observability. Per §7.10
  amendments: gate 3 mini-spec also carries falsification criteria (H4) +
  substrate-vs-first-target channel separation (H5) + per-decision
  test-case-vs-substrate rule (M5).

  D5a in-session-collaboration risk applies recursively at Step 3 layer; mini-spec
  is co-produced under shared framing. Phase D entry audit per plan §2.4 row D
  paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor
  xhigh audit of evidence-load) is the structural correction. The audit reads
  §7.10 + STEP1-design-space + STEP1-DISPOSITION + STEP2-practical-decisions +
  this mini-spec together as one corpus.

ground:
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md (H6/H7/M1/M3/M4 dispositions; load-bearing for build location + abort triggers + scope)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md (axis 1-4 dispositions; E primary + A comparator)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md §3.A + §3.E (E + A candidate specifications)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md (sub-option (ii) caveat; layer-attribution requirement)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md (skill subsystem mechanics; primitives inventory)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7.9.3 (gate 3 contract requirements) + §7.10.1 (H4/H5) + §7.10.2 (M5)
  - .planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md §1 + §2 (test-case-vs-substrate; H5 anchor; M5 categorization)
  - ~/workspace/projects/gsd-2-explore at commit 42ef05fbe (build target)

read_order: |
  - For "what gets built": §1 (artifacts produced — E + A specifications).
  - For "what behavior is tested": §2 (skill behavior + activation patterns + queries).
  - For "what's in/out of scope": §3 (workflow-template composition scope; OOS per axis 1+4).
  - For "what counts as success": §4 (successful decision-trace evidence definition).
  - For "F-discipline observability": §5 (progressive-activation as observed-not-assumed).
  - For "what counts as failure of the chosen first-target": §6 (H4 falsification criteria).
  - For "channel separation between first-target evidence and substrate-shape evidence": §7 (H5).
  - For "per-decision test-case-vs-substrate categorization": §8 (M5 rule).
  - For "audit-priority risks at Step 3 layer": §9.
  - For "cross-references": §10.
---

# Phase D Step 3 — Mini-spec (gate 3 amended)

This mini-spec is the Phase D dispatch contract: it specifies what gets built (Shape E in-tree gsd-2 skill + Shape A user-side gsd-2 skill), what behavior is tested, what evidence counts as success, what evidence counts as falsification, and the channel-separation + categorization rules that govern Phase D's evidence-claims.

## §1. Artifacts produced

### §1.E Shape E — In-tree gsd-2 skill

**Location:** `src/resources/skills/decision-trace/SKILL.md` on branch `phase-d-decision-trace-spike` of `~/workspace/projects/gsd-2-explore/` (off `main` at commit 42ef05fbe per §2.H6 disposition).

**Artifact specification:**

| Attribute | Value |
|---|---|
| File | Single `SKILL.md` (no router subdirectories at Phase D scope; router only if §6 falsifier #4 fires and licenses Phase E follow-up) |
| Frontmatter validation | Per `packages/pi-coding-agent/src/core/skills.ts:81-95, 112-151`: `name=decision-trace`, `description` ≤1024 chars + keyword-rich + states activation conditions, no `disable-model-invocation` (model can invoke), parent-directory match enforced |
| Body length | ≤500 lines per `src/resources/skills/create-skill/SKILL.md:42-54` doctrine |
| Body structure | Pure XML structure per `create-skill` doctrine (no markdown headings in body); progressive disclosure (split to references/ if >500 lines, but Phase D scope is single-file) |
| Description draft target | Surface decision-trace activation conditions: reconstructing past decisions over multi-year project lifetimes; reading `.gsd/DECISIONS.md` + activity + journal for evidence; producing decision-trail reconstruction artifact; layer-attribution-aware (per P5 caveat) |

**Conditional second touchpoint (≤2 total per §2.M4 envelope):**

If §2 skill-behavior testing surfaces "decision-trace must activate at specific lifecycle steps but per-unit-type allowlist excludes it from those steps," update `src/resources/extensions/gsd/skill-manifest.ts:33-123` `UNIT_TYPE_SKILL_MANIFEST` to add `decision-trace` to the relevant allowlist entries. Likely candidates per M2 + STEP1-design-space §3.E + activation matrix below: `complete-milestone` (trace-back-on-completion; `preferences:"active-only"` per `unit-context-manifest.ts:402-421` — P5 caveat observable). If allowlist update is not sufficient and a different unit-type's preferences-policy / unit-context-composer surface forces another touchpoint, M1 abort trigger #3 (coordination cascade) fires.

**Activation surface — 5-dimensional matrix (added per Phase D entry audit F-PD-A4 disposition):**

The activation surface for a gsd-2 skill is NOT routed solely through `skill-manifest.ts`. Per audit-grounded source review (`unit-context-composer.ts:1-21, 149-187`; `unit-context-manifest.ts:402-421` complete-milestone, `:508-523` reassess-roadmap; `auto-prompts.ts:827-840`), activation depends on 5 dimensions:

| Dimension | Source | Per-test-step observability |
|---|---|---|
| **D1 — Catalog visibility** | `auto-prompts.ts:707-797` description-keyword similarity matching; `<available_skills>` block | P1 in §2.1 tests this directly; observable across all unit-types |
| **D2 — Explicit activation** | User/agent explicitly invokes skill via Skill tool | P2 in §2.1 tests this; observable across all unit-types |
| **D3 — Auto-discovery** | Gated under `skill_discovery:"auto"` preference; `auto-prompts.ts:869-890` auto-match logic | Observable only under matching preference setting |
| **D4 — Unit-context-manifest skill mode** | `unit-context-manifest.ts:402-421` per-unit-type `skills:{mode:"all"}` or `{mode:"allowlist", ...}` | P3 in §2.1 tests this; observable per unit-type |
| **D5 — Preference-inlining policy** | `unit-context-manifest.ts` per-unit-type `preferences:"active-only"` / `"all"` / `"none"` | **Critical for B3 P5-caveat observability:** P5 layer-attribution caveat is observable ONLY in unit-types where preferences are inlined into context (`"active-only"` or `"all"`). Unit-types with `preferences:"none"` (e.g., `reassess-roadmap` per `:508-523`) make B3 non-observable — preferences are not in the context the skill reads. |

**P3 + B3 test-step routing per matrix:** P3 activation test routes to `complete-milestone` (D5=`"active-only"`; B3-observable) NOT `reassess-roadmap` (D5=`"none"`; B3-non-observable). Without this routing per matrix, P3 + B3 jointly produce false-negative evidence about layer-attribution behavior. This routing replaces the original P3 wording that named reassess-roadmap as activation-test surface.

**What this artifact does NOT include:**

- No router-pattern subdirectories (`workflows/`, `references/`, `templates/`, `scripts/`) — single SKILL.md only.
- No workflow template at `src/resources/extensions/gsd/workflow-templates/decision-trace.md` (deferred to Phase E if E's evidence licenses; per axis 1 disposition).
- No modifications to `auto-prompts.ts` (the description-keyword similarity matching at lines 707-797 already handles activation; no new mechanism needed).
- No modifications to `.gsd/DECISIONS.md` schema (Shape D — out-of-scope-this-arc per axis 1).
- No new MCP tool registration (per P5 §4: no `gsd_prefs`/`gsd_skills` tool exists; Shape E is skill-shape, not MCP-shape).

### §1.A Shape A — User-side gsd-2 skill (parallel R4 comparator)

**Location:** `~/.agents/skills/decision-trace-r4/SKILL.md` (skills.sh ecosystem standard per `skills.ts:15-26, 421-433`; gsd-2 discovers at runtime).

**Name choice rationale (per Phase D entry audit F-PD-A1 disposition):** Shape A registers under distinct name `decision-trace-r4` (NOT `decision-trace`). Reason: gsd-2's `resource-loader.ts:559, 596-598` syncs bundled `resources/skills` to `~/.agents/skills` at `initResources` time, and `syncResourceDir 256-275` removes destination subdirectories before copying. With identical names, the in-tree bundled skill (E) overwrites the user-side primitive (A) at init — no parallel observability. Distinct names preserve R-strategy contrast at the layer that matters (residence-path: in-tree-via-bundle vs user-side-via-installation), not name-identity. R4 in real deployment ships user-side primitives that need not match in-tree analog names.

**Artifact specification:**

| Attribute | Value |
|---|---|
| File | Single `SKILL.md` (same single-file constraint as E) |
| Frontmatter `name` | `decision-trace-r4` (distinct from E's `decision-trace` per A1 disposition) |
| Frontmatter validation | Same shape as E (Anthropic Agent Skills standard) |
| Body length | ≤500 lines (same constraint) |
| Body structure | Same XML structure constraint |
| Description draft target | Same activation conditions as E; description-keyword space SHOULD be substantively similar to E's. Workload-uniformity (same input deliberation produces decision-trace output regardless of which is invoked) is preserved by content equivalence; the distinct names allow side-by-side discovery without first-wins overwrite. |

**Critical constraint for parallel R4 contrast (per axis 2 disposition):**

A's body content SHOULD be substantively equivalent to E's at semantic level (same decision-trace behavior; same P5 caveat handling; same layer-attribution preservation). The contrast under test is **R-strategy + residence-path + integration surface**, NOT skill-design content. If A and E diverge in semantic content, Phase D evidence becomes confounded — we'd be testing two different skills, not two R-strategies for the same skill.

**Recommended approach:** Author E first (in-tree); copy to A's location with name swap (`decision-trace` → `decision-trace-r4` in frontmatter) + minimal user-side path adaptations.

## §2. Skill behavior tested

### §2.1 Activation patterns under test

| Pattern | Test description | Pass condition |
|---|---|---|
| **P1 — Description-keyword discovery** | Run gsd-2 against a project (arxiv-sanity-mcp itself per §2.M4); inspect `<available_skills>` system-prompt block | Both `decision-trace` (E) and `decision-trace-r4` (A) appear under their distinct names per §1.A name disposition; descriptions are keyword-rich + discriminate from `forensics`/`handoff` |
| **P2 — Activation-context match** | In a context with tokens like "what was the rationale for X?" / "trace decision Y" / "why did we choose Z over W?" — observe whether Skill tool fires for decision-trace | Skill tool invokes one of `decision-trace` / `decision-trace-r4` at least once across ≥3 such contexts; activation gates on description-keyword similarity per `auto-prompts.ts:707-797`, not name-identity |
| **P3 — Per-unit-type allowlist behavior** | Test activation at activation-matrix-compatible unit-type per §1.E activation matrix (NOT reassess-roadmap; see §6 + activation-matrix table). Default candidate: `complete-milestone` (per M2 §2.B; `preferences:"active-only"`). Compare to `execute-task` (wildcard fallback per skill-manifest.ts:119-122) | Allowlist behavior is observable and predictable in `preferences:"active-only"` unit-context; allowlist update is conditionally needed (see §1.E conditional second touchpoint) |
| **P4 — Distinct-name parallel observability** | Both `decision-trace` (E, in-tree-bundled) and `decision-trace-r4` (A, user-side) registered under distinct names; observe whether both appear, which fires preferentially under different contexts, and whether description-keyword overlap shifts activation | Both names appear in `<available_skills>` simultaneously (no first-wins overwrite under distinct names); per-context activation distribution observable; description-keyword overlap behavior measurable |
| **P5 — Description rewrite cycle** | Iterate description until P1 + P2 fire reliably across ≥3 test contexts | ≤3 rewrites per `create-skill/SKILL.md:58` (>3 = §6 falsification flag) |

### §2.2 Query / reconstruction behavior tested

| Behavior | Test description | Pass condition |
|---|---|---|
| **B1 — Read existing DECISIONS.md** | Skill reads arxiv-sanity-mcp's `.planning/deliberations/` directory (or `.gsd/DECISIONS.md` analog if present) and produces decision-trail | Output cites file:line refs to source artifacts; no fabrication |
| **B2 — Cross-reference activity/journal** | Skill cross-references decision-time evidence (timestamps; commit-history; deliberation status transitions) | Output includes timestamp-anchored evidence chain, not just summary |
| **B3 — Layer attribution (P5 caveat handling)** | Skill reads `~/.gsd/PREFERENCES.md` + `.gsd/PREFERENCES.md` directly per §1.4 standing constraint. Per Phase D entry audit F-PD-A3 disposition: trace explicit file-origin (PREFERENCES.md / project.md scope per `preferences-types.ts:485-491` `LoadedGSDPreferences.path` + `.scope` fields); mark derived defaults (token-profile / mode per `preferences-models.ts:431-500`) as 'unresolved without inspection of preferences.ts merge logic' | Trace artifact has explicit layer-attribution annotations for explicit file-origin layers (project / global); derived defaults (token-profile / mode) explicitly marked 'unresolved' rather than fabricated. **Honest scoping per source surface:** gsd-2's `LoadedGSDPreferences` (preferences-types.ts:485-491) does not expose per-field provenance for derived defaults — the skill cannot reconstruct what gsd-2 itself does not surface. Phase E may license tributary work emitting per-field provenance (option ii from F-PD-A3 disposition; Phase D scope holds option i). |
| **B4 — Falsifiable predictions surfacing** | Skill identifies past predictions made (e.g., from `/gsdr:deliberate` workflow per M2 §3.A — if any deliberation has predictions in `evaluation_trigger`-shape) and reports their evaluation status | Output includes "predictions made + outcome status" subsection where applicable |
| **B5 — Forensics-vs-decision-trace differentiation** | Skill is invoked in a context where `forensics` would also plausibly fire (e.g., a failed auto-mode run that was a decision); decision-trace produces reconstruction-shaped output (rationale chain), NOT forensics-shaped output (symptom→root-cause) | Outputs are differentiable; skill activation discrimination works at semantic level |
| **B5b — Decision-DB-substrate differentiation** (added per Phase D entry audit F-PD-A2 disposition) | Skill is invoked against a project where `gsd_decision_save` MCP tool / `db-writer` canonical-table generator have written structured DECISIONS.md entries; decision-trace's reconstruction OUTPUT is read against the existing WRITE-side substrate per `workflow-tools.ts:606-608, 1246-1255` + `db-writer.ts:455-489` | Decision-trace extends `gsd_decision_save`'s WRITE-side structured records at the READ/RECONSTRUCT side (rationale chain across entries; cross-reference to activity/journal); the new skill does NOT duplicate the existing WRITE-side; differentiation is observable in skill output (cites canonical-table entries by ID; reconstructs across multiple entries; surfaces gaps where decisions were not captured by existing primitives) |
| **B5c — `/gsdr:deliberate` prior-art differentiation** (added per Phase D entry audit F-PD-B1 disposition) | Skill is invoked on a deliberation in `.planning/deliberations/` that has prediction-shape + evaluation-status (the artifact class `/gsdr:deliberate` operates on per M2 §0/§3); decision-trace's reconstruction OUTPUT is read against `/gsdr:deliberate`'s deliberation-shape | Decision-trace differs from `/gsdr:deliberate` in **runtime + integration** (gsd-2 in-tree skill vs Claude Code slash-command), not in core artifact-class coverage. Phase D evidence on "did decision-trace produce something `/gsdr:deliberate` does not, on the same artifact?" surfaces whether the work is genuinely novel-by-content or only novel-by-runtime. **This is a coverage-question test, not a replacement-question test** — `/gsdr:deliberate` cannot be invoked from gsd-2 runtime (acausal-runtime grounds; per STEP1-design-space §1.3 prior-art-not-candidate-shape note). |
| **B5d — Distinct-name parallel observability sub-test** (added per Phase D entry audit F-PD-A1 disposition) | Both `decision-trace` (E, in-tree-bundled at `src/resources/skills/decision-trace/SKILL.md`) and `decision-trace-r4` (A, user-side at `~/.agents/skills/decision-trace-r4/SKILL.md`) are registered simultaneously per §1.A name disposition. Observe (i) whether both appear in `<available_skills>` block; (ii) whether per-context activation distribution shows discoverable preference patterns; (iii) whether description-keyword overlap shifts the activation distribution under controlled prompt variations | Both names appear; per-context distribution observable; description-keyword overlap behavior measurable. **Sub-test for collision-policy data:** if same-name registration were attempted (NOT this primary test), `resource-loader.ts` syncResourceDir + first-wins collision per `skills.ts:401-417` would block A; observation here is what happens UNDER distinct-name preservation (clean parallel observability, the design intent). |

### §2.3 Test task selection (per §2.M4 envelope)

> **Test-task revision note (per Phase D entry audit F-PD-A5 + F-PD-B2 disposition, applied 2026-04-30):** Original primary test-task (2026-04-28 framing-widening deliberation) is co-produced by current-arc Claude+Logan in-session-collaboration. Phase D evidence on "skill reconstructed decision-trace from a co-produced deliberation" is circular by D5a leak (the framing the skill reconstructs is the framing Claude already wrote). Revised: primary task is now a pre-current-arc deliberation (lower D5a inheritance — different session-context, different framing trajectory). Framing-widening retained as **backup with explicit D5a-caveat**, NOT primary.

**Primary test task (low-D5a):** Reconstruct rationale chain for the **2026-04-25 long-arc-and-multi-lens-redirection deliberation** at `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md`.

**Rationale for this task selection:**

- **Pre-current-arc:** This deliberation pre-dates the gsd-2-uplift initiative genesis (2026-04-26) and the current Phase D dispatch arc; D5a inheritance is materially weaker (different session-context, different framing trajectory, different reasoning patterns) than co-produced framing-widening.
- **Multi-lens-shape:** the deliberation surfaces multi-lens redirection — substantive content with rationale chain across multiple decision points; full enough to exercise B1+B2+B3.
- **Cross-references exist** to long-arc / multi-lens patterns visible in subsequent project artifacts; B2 testable across artifact boundaries.
- **Phase D entry audit can read trace artifact against the actual deliberation source** — verifiable; reading the trace artifact does not require Logan or current-arc Claude to participate in evaluation (lower-D5a evaluation surface).

**Backup test task (with explicit D5a-caveat):** **2026-04-28 framing-widening deliberation** at `.planning/deliberations/2026-04-28-framing-widening.md`. Acknowledged co-produced (current-arc Claude+Logan in-session-collaboration); use ONLY if primary task proves too thin to exercise B1-B5; carry explicit D5a-caveat in FINDINGS.md when reading evidence ("this evidence inherits Logan-framing inheritance from current-arc; reading is procedural-not-evidentiary at substrate-shape claim layer").

**Secondary backup (further-from-D5a if needed):** **2026-04-25 load-bearing-assumptions-audit deliberation** at `.planning/deliberations/2026-04-25-load-bearing-assumptions-audit.md`. Also pre-current-arc; substantive audit-shape content; B4 testable if predictions surface.

**Counter-task** (for B5 differentiation): a synthetic auto-mode-failure scenario (described in skill-prompt-test-context, not requiring real failure) — tests B5 without producing a real failure log.

## §3. Workflow-template composition scope

**Scope: OUT.**

Per axis 1 disposition: skill-only at Phase D; workflow template (markdown-phase or YAML) deferred to Phase E if E's evidence licenses. This mini-spec does NOT specify a `decision-trace.md` workflow template at `src/resources/extensions/gsd/workflow-templates/`. Phase E may license it based on E's evidence on:

- Whether decision-trace work is multi-phase enough to benefit from workflow-template structure
- Whether skill-only feels under-structured at multi-year reconstruction scale
- Whether `spike.md` workflow Phase 3's offer-pattern (offers `spike-wrap-up`) would compose cleanly with a `decision-trace` workflow template

**Falsifier for OOS scope** (per §6.H4 #5 below): if Phase D execution surfaces "skill-only is structurally under-scoped for the work" — e.g., skill body would exceed 500 lines because reconstruction needs explicit phase structure — surface as Phase D evidence + Phase E re-disposition trigger; do NOT silently extend scope.

## §4. Successful decision-trace evidence definition

**Phase D produces successful decision-trace evidence if and only if ALL of the following hold:**

1. **§1.E + §1.A artifacts shipped** — both SKILL.md files exist, validate per `skills.ts:81-95, 112-151`, and are ≤500 lines each.
2. **§2.1 activation patterns P1-P4 pass** — keyword-discovery + context-match + allowlist-behavior + collision-diagnostic all observable and predictable across ≥3 test contexts each.
3. **§2.2 query behaviors B1-B5 pass** — DECISIONS.md/deliberations read + cross-reference + layer-attribution + predictions surfacing + forensics-differentiation all demonstrated on the §2.3 test task.
4. **§2.1 P5 description-rewrite cycle stays within ≤3 rewrites** — descriptions converged on discrimination from `forensics`/`handoff` without overrun.
5. **EXECUTION-LOG.md captures observation honestly** — what worked, what didn't, what surprised; no comfort-language; per §0.5 disposition-discipline traces-over-erasure.
6. **FINDINGS.md reads against the dispositions** — per-axis evidence ("did the E-primary disposition hold?"; "did the A-comparator surface useful divergence?"; "did the OOS confirmations for F + G remain warranted by Phase D evidence?").

**Definition explicitly excludes:**

- "The skill feels useful" — subjective; not falsifiable at Phase D scale.
- "Logan + Claude found the trace artifacts helpful" — D5a in-session-collaboration risk; cannot serve as Phase D evidence (it's exactly the inherited-framing surface).
- "Phase D shipped on time" — schedule discipline is M1 abort triggers, NOT success criterion.
- "Workflow template would also work" — counterfactual outside Phase D evidence-load.

**The successful-evidence definition is also the ceiling for claims:** if all 6 hold, Phase D's claim is "decision-trace skill-shape + parallel R4-vs-R2 contrast is workable on gsd-2's skill subsystem under the described conditions" — NOT "decision-trace is the right shape for substrate" (that's Phase E's question, gated by H5 channel separation §7).

## §5. F-discipline observability

**F-discipline = transition-as-stance optionality** (per §7.4 A+F-primary anchoring; framing-widening §2 six-context).

**The §7.9.3 (c) requirement: F-discipline observability must be progressive-activation as observed property, not assumed by design choice.**

### §5.1 What "progressive activation" means for decision-trace at Phase D

Decision-trace is F-discipline-observable if the skill's activation + behavior **progressively reveals additional capability under load**, NOT all-at-once. Concretely:

| Layer | Observable progression |
|---|---|
| L1 — Discovery | Skill is in `<available_skills>` block but not yet contextually-active |
| L2 — Activation | Description-keyword match fires for decision-trace-shaped contexts |
| L3 — Light-touch invocation | Skill invocation produces 1-paragraph reconstructions for simple decisions (single artifact, recent timeframe) |
| L4 — Heavy invocation | Skill invocation produces full rationale chains with cross-references for complex decisions (multi-artifact, multi-month timeframe) |
| L5 — Substrate-aware invocation | Skill invocation reflects on its own activation conditions (meta-level: "I'm activating because the context has decision-trace tokens"); the skill is observable-as-skill, not just operationally-effective |

**F-discipline observability test:** can the executor (or a reader of EXECUTION-LOG.md) observe the skill traversing L1 → L2 → L3 → L4 progressively across the test task? Or does it skip layers (e.g., always heavy invocation; no light-touch case)?

### §5.2 What F-discipline observability is NOT

**Not assumed by design choice:** the skill body should NOT be authored with explicit "L1 mode / L2 mode / L3 mode" branching. The progression should be observable from outside (in EXECUTION-LOG.md) without being prescribed inside (in SKILL.md). If the skill needs explicit mode-branching to demonstrate progression, that's evidence F-discipline is NOT observed-but-assumed (and the skill design should be re-considered).

**Not "the skill works for many contexts":** F-discipline is about **stance optionality** — the user can adopt different stances toward the same decision over time (recall vs reconstruct vs critique vs plan-from). If the skill only supports one stance (e.g., always reconstruction), F-discipline is NOT observed.

**Not "the skill is configurable":** configurability is a substrate property; F-discipline is about how the skill USES the substrate's configurability under varying operating contexts.

### §5.3 Falsifier for F-discipline observability

If the skill always produces the same shape of output regardless of context (no L1-L4 progression observable), or if the skill cannot support stance-shifting (recall→reconstruct→critique→plan-from on the same decision), surface as Phase D evidence: F-discipline is NOT observable in this design; Phase E re-read interrogates whether F-anchoring should be deprioritized OR whether the skill design needs re-shaping.

## §6. H4 — Falsification criteria

**Inverse of §4 success criteria.** What evidence would tell us decision-trace is the WRONG first-target for Phase D?

### §6.1 First-target falsifiers (per H5 channel: scoped to decision-trace skill specifically)

| # | Falsifier | What it surfaces |
|---|---|---|
| 1 | **Activation pattern P1-P4 fails to converge across ≥3 rewrites** (description-keyword discrimination from `forensics`/`handoff` not achievable at ≤3 rewrites) | gsd-2's keyword-driven activation is structurally brittle for reconstruction-shaped semantics; OR decision-trace is the wrong primitive name (collision is too tight) |
| 2 | **Query behaviors B1-B3 require >2 coordination touchpoints** (skill-only insufficient; needs auto-prompts integration + extension-validator update + manifest test update + ...) | Shape E was wrong-shape; the work is actually Shape D-shape (schema enrichment) or Shape F-shape (hooks); §2.M1 abort trigger #3 fires |
| 3 | **B4 falsifiable predictions surfacing fails** (no decision artifacts in arxiv-sanity-mcp's deliberations have prediction structure the skill can reliably extract) | gsd-2's existing decision-capture primitives (`design-an-interface`, `write-milestone-brief`, `spike-wrap-up`) don't write prediction-shaped outputs; decision-trace's evaluation-loop dimension is unsupported by substrate; design needs re-shape OR substrate needs separate work |
| 4 | **Skill body exceeds 500 lines** without router-pattern split | The work is multi-phase enough to need workflow-template structure; Phase E re-disposition fires for workflow-template addition (which was OOS at Phase D per axis 1) |
| 5 | **B5 forensics-differentiation fails** (decision-trace and forensics produce indistinguishable output in differentiating contexts) | Description-keyword space + activation-pattern is too coarse-grained; decision-trace overlaps too much with forensics to be a separate skill; consolidate into forensics-extension OR rename to differentiate semantically |
| 6 | **R4 (A) and R2 (E) outputs diverge in unexpected ways** beyond R-strategy + integration surface | The user-side discovery + activation pattern is materially different from in-tree, in ways that confound the parallel-R4 contrast; axis 2 (i) parallel R4 disposition was wrong choice |

### §6.2 Substrate-shape falsifiers (per H5 channel: scoped to gsd-2 substrate; surfaced through but not reduced to decision-trace evidence)

These fire only with H5-explicit substrate-anchoring claims (per §7 below):

| # | Falsifier | What it surfaces |
|---|---|---|
| 7 | **The 8-day budget overruns due to substrate-side friction** (build cycle / test loop / discovery cache / validation flow forces re-runs that aren't decision-trace-specific) | gsd-2's substrate development friction is higher than Phase D entry assumed; spike-program METHODOLOGY's "earliest possible test" is harder to achieve in this substrate; trajectory plan §1.4 implicit "1-2 weeks" budget is mis-calibrated for gsd-2 work |
| 8 | **P5 caveat handling forces substrate-modification beyond skill body** (reading PREFERENCES.md directly cannot reconstruct layer-attribution; in-process API is the only path) | P5 sub-option (ii) "documented caveat, do not re-scope" is wrong call retroactively; P5 sub-option (i) re-scope should fire at Phase E |
| 9 | **The per-unit-type allowlist update is needed for Phase D but its addition cascades through manifest-strict-mode + test-failures + downstream skill resolution** | gsd-2's per-unit-type allowlist couples skill design to lifecycle-step model more tightly than M2 surfaced; substrate-shape evidence: the manifest is harder to extend than the skill subsystem suggests at first read |
| 10 | **Activation matrix dimensions D1-D5 (per §1.E activation matrix) cannot be jointly satisfied at any unit-type for the P3 + B3 test-step pair** (added per Phase D entry audit F-PD-A4 disposition) | gsd-2's per-unit-type preference-inlining policy + skill-mode + auto-discovery dimensions interact such that no unit-type makes both activation AND P5-caveat-attribution observable simultaneously; substrate-shape evidence: the unit-context-composer surface needs extension before reconstruction-shaped skills can fully exercise layer-attribution at activation surfaces |

### §6.3 What falsifier-firing means operationally

Per §2.M1 abort triggers + §5.4 productive-curiosity pattern:

- **Falsifiers 1, 2, 5 firing → §2.M1 abort trigger fires (re-design-space at Step 1).**
- **Falsifiers 3, 4 firing → Phase D evidence flagged for Phase E re-disposition (no abort; surface and proceed).**
- **Falsifiers 6 firing → axis 2 comparator re-disposition at Phase E (i ↔ ii ↔ iii).**
- **Falsifiers 7-9 firing → substrate-shape evidence; H5 channel-separation discipline preserves; Phase E re-reads as cross-cutting evidence.**

## §7. H5 — Substrate-vs-first-target channel separation

### §7.1 The two channels (definitions)

**Channel (a) — First-target evidence:** claims about whether the decision-trace skill (E or A) works/doesn't work in the conditions we're testing. Scoped to: skill discoverability, activation patterns, query behaviors, output quality on the test task.

**Channel (b) — Substrate-shape evidence:** claims about whether gsd-2 substrate handles "long-arc decision-trace work" well/poorly. Scoped to: how gsd-2's skill subsystem handles this kind of work generally (not just our specific skill); whether the substrate's decision-capture primitives support the reconstruction-shape semantics; whether the per-unit-type allowlist + skill manifest design accommodates new primitives like decision-trace cleanly.

### §7.2 The discipline rule

**No claim crosses channels without explicit anchoring.**

A Phase D claim of the shape "decision-trace skill works at L4 invocation depth" is channel-(a) — and it stays in channel (a) unless the FINDINGS.md explicitly anchors a substrate-shape extension claim with separate evidence. The substrate-shape extension would look like: "decision-trace skill's L4 behavior demonstrates that gsd-2's skill subsystem supports reconstruction-shaped semantics at long-arc scale, BECAUSE [explicit cross-skill comparison + explicit primitive-coverage argument]." Without that anchoring, the substrate-shape claim is unsupported.

### §7.3 Operational test for channel separation

**Per-claim audit at FINDINGS.md drafting time:** for each load-bearing claim, label it `(a)` or `(b)` or `(a→b)` (anchored extension):

- `(a)` claims need only first-target evidence.
- `(b)` claims need explicit substrate-shape anchoring (cross-skill comparison + primitive-coverage argument).
- `(a→b)` claims must show the bridge — what makes this first-target evidence licensable as substrate-shape evidence?

**Phase D entry audit (Step 5) reads FINDINGS.md against this discipline:** any unlabeled claim or any `(a→b)` without explicit bridge fails the audit.

### §7.3.1 EXECUTION-LOG.md inline-tagging discipline (added per Phase D entry audit F-PD-B3 disposition)

The §7.3 per-claim audit applies at FINDINGS.md drafting time, but FINDINGS.md is itself a co-produced reflective artifact — labels assigned at drafting can unconsciously bridge `(a)→(b)` if Claude integrates evidence into a finding-narrative before applying labels. **Mitigation: extend §8.4-style inline-tagging discipline to channel-separation at observation-time.**

**Discipline rule:** EXECUTION-LOG.md inline-tags channel-`(a)` / `(b)` / `(a→b)` at *observation-time* (when the evidence is first written), using the same inline-discipline as §8.4 M5 categorization. FINDINGS.md inherits the inline tags; relabeling at drafting time requires explicit reasoning + rationale recorded in the same line.

**Pattern (combines §8.4 M5 + §7.3 channel inline-tagging):**

```
[2026-MM-DD HH:MM] Skill activated for `decision-trace-r4` (A) at description-keyword match — ✅ activated. M5: substrate-anchored (gsd-2 manifest convention). Channel: (a) first-target evidence.

[2026-MM-DD HH:MM] Both `decision-trace` (E) and `decision-trace-r4` (A) appeared in `<available_skills>` block under distinct names per §1.A name disposition; per-context activation distribution shows E preferred 4/5 contexts. M5: substrate-leaning. Channel: (a→b); bridge: this is evidence about gsd-2's distinct-name parallel observability surface, not just specific skill behavior. Logan-discretion to read as (b) if Phase E re-analyses cross-skill.
```

**Why observation-time vs post-hoc:** observation-time labeling is contemporaneous with the observation event; post-hoc labeling at FINDINGS.md drafting is reflective-after-integration. Contemporaneous labeling is harder to bridge unconsciously because the observation hasn't yet been integrated into a finding-narrative. **Acknowledged partial mitigation:** observation-time labels are still Claude-authored under in-session-collaboration; same vendor catches the recursion at Phase E re-read or paired audit. The discipline is lower-D5a than post-hoc but not zero-D5a; Phase E re-read provides the structural correction.

**Operational form for FINDINGS.md drafting:** read EXECUTION-LOG.md inline tags as the source of truth; if a FINDINGS.md claim re-labels, add inline rationale ("re-labeled (a→b) at FINDINGS.md drafting because <explicit reasoning>"). Auditor at Step 5 audit OR Phase E re-read catches re-labels-without-rationale as discipline-leak.

### §7.4 Why this discipline matters (per RELATIONSHIP-TO-PARENT.md §2 failure-mode 1)

The convergent C1 finding from the premise-bleed audit-arc was: projection from test-case-anchored evidence to substrate-shape-anchoring is weakly licensed. Phase D operating without explicit channel separation re-fires C1 at Phase E re-read time. The discipline prevents that.

## §8. M5 — Per-decision test-case-vs-substrate categorization

### §8.1 The rule

**Each implementation choice within Phase D execution lands on one side or the other:**

- **Test-case-anchored:** specific to arxiv-sanity-mcp (or to the chosen test task). Decisions made because of arxiv-sanity-mcp's planning structure, deliberation conventions, or specific existing artifacts.
- **Substrate-anchored:** specific to gsd-2 (or to the substrate-class). Decisions made because of gsd-2's skill subsystem mechanics, manifest conventions, or substrate primitives.

### §8.2 Examples of the categorization

| Implementation choice | Side | Reasoning |
|---|---|---|
| Skill reads `.planning/deliberations/` | **Test-case-anchored** | arxiv-sanity-mcp's deliberation directory structure; not a gsd-2 substrate convention |
| Skill reads `~/.gsd/PREFERENCES.md` + `.gsd/PREFERENCES.md` | **Substrate-anchored** | gsd-2's preference-file convention per `preferences.ts:178-198` |
| Skill description includes "long-arc" + "multi-year" keywords | **Either, depending on intent** | If because arxiv-sanity-mcp is a multi-year project (test-case); if because gsd-2's typical user runs multi-year projects (substrate) |
| Skill activates at unit-type=`complete-milestone` | **Substrate-anchored** | gsd-2's per-unit-type allowlist convention |
| Skill output format includes "Decision rationale chain with file:line refs" | **Test-case-leaning, substrate-extensible** | The format is shaped by arxiv-sanity-mcp's artifact conventions; substrate-extension claim requires explicit cross-project anchoring |

### §8.3 Why this discipline matters (per RELATIONSHIP-TO-PARENT.md §2)

If implementation choices silently mix test-case-anchored decisions with substrate-anchored decisions, Phase E + extraction inherit a code base whose substrate-claims cannot be cleanly migrated to a different test case. M5 forces the categorization at decision-time; FINDINGS.md inherits + audits.

### §8.4 Operationalization at execution time

EXECUTION-LOG.md captures each non-trivial implementation choice with its M5 categorization in-line. Per Phase D entry audit F-PD-B3 disposition, channel-`(a)`/`(b)`/`(a→b)` tag is inline alongside M5 (per §7.3.1 above):

```
[2026-MM-DD HH:MM] Skill description revised to include "multi-year project lifetimes" — M5: test-case-leaning (arxiv-sanity-mcp is multi-year; not asserted as substrate property). Channel: (a) first-target.
[2026-MM-DD HH:MM] Activation tested at unit-type=complete-milestone — M5: substrate-anchored (per gsd-2 manifest convention; D5=`"active-only"` per activation matrix). Channel: (a→b); bridge: per-unit-type allowlist behavior is substrate-shape evidence, not just decision-trace behavior.
```

### §8.5 Heal-skill observation hook (added per Phase D entry audit F-PD-A7 disposition)

**Acknowledged exclusion + observation-only hook:** Heal-skill / skill-health subsystem integration is OOS per STEP2 §2.M4 (≤2 coordination touchpoints envelope; M2 §8 #3 flagged for Phase E). Phase D execution does NOT implement skill-health integration. **However**, Phase D execution observes the question without implementing — at end of execution OR when notable observation surfaces, EXECUTION-LOG.md captures one inline observation:

```
[2026-MM-DD HH:MM] Heal-skill observation: <did this Phase D run reveal anything skill-health should capture? Free-text observation; no implementation>
```

**Default observation slot:** end of Phase D execution (post-FINDINGS.md drafting) gets an explicit "heal-skill observation" line, even if observation is "nothing surfaced." This defers the skill-health question to Phase E (or later) with a low-cost hook into observation channel.

**Why this is observation-only, not implementation:** implementing skill-health integration would expand the M4 ≤2 coordination touchpoints envelope + force scoping Phase E-shaped work into Phase D. Observation slot lets the executor flag if Phase D evidence implies skill-health is load-bearing for substrate without expanding scope mid-Phase.

## §9. Audit-priority risks at Step 3 layer

1. **§5 F-discipline observability is theory-loaded.** L1-L5 progression layers are Claude-imported organizing structure; gsd-2 doesn't impose a layer model on skill activation. If F-discipline isn't observable as L1→L5 progression but IS observable some other way, this mini-spec under-specifies the actual observable. Phase D entry audit catches.

2. **§4 success criteria items 1-6 may be jointly too strict.** All 6 must hold for "successful evidence." If 5/6 hold, is that partial-success or failure? Mini-spec doesn't specify. Audit-priority: should partial-pass have its own disposition pathway?

3. **§6 falsifiers 1-6 (first-target) and 7-9 (substrate-shape) overlap-able.** Falsifier 7 (8-day budget overrun) could be substrate-shape OR could be Shape E being wrong-shape. The triage rules at §6.3 are heuristic; cleaner separation would name observable conditions that distinguish channel-(a) from channel-(b) cleanly. Audit-priority: are the triage rules well-specified or wishful?

4. **§7 channel-separation discipline is a declared rule, not a built-in mechanism.** If the executor (or Claude during execution) accidentally violates the rule at FINDINGS.md drafting, only the audit catches. Substrate-shape claims with weak anchoring would survive into Phase E if audit is also captured. Audit-priority: does paired-audit M3 selection actually catch this, or is it a discipline-shape that's only as good as the readers?

5. **§8 M5 categorization at execution-log time may interrupt flow.** Capturing M5 inline at every implementation choice is additional discipline overhead; risk is the executor (or Claude) defers / batches and the categorization rots. Audit-priority: is M5 inline-discipline practically sustainable, or does it need a sweep-pass at end-of-Phase-D?

6. **Test task selection (framing-widening) carries D5a inheritance.** Picking that deliberation as the reconstruction target means decision-trace is being tested on a deliberation Claude+Logan co-produced. The skill's reconstruction will read framings that Claude already-wrote. Risk: skill validates the existing framing rather than independently reconstructing it. Audit-priority: backup-task (incubation-checkpoint) might suffer same issue; would a synthetic task (no Logan-framing) be cleaner?

7. **D5a recursion at Step 3 layer.** Mini-spec is co-produced; Phase D entry audit per plan §2.4 row D paired is the structural correction. Audit reads §7.10 + STEP1-design-space + STEP1-DISPOSITION + STEP2-practical-decisions + this mini-spec together.

## §10. Cross-references

### Step 0/1/2 outputs (load-bearing for Step 3)

- `.planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md` — sub-option (ii) caveat; B3 layer-attribution requirement.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md` — skill subsystem mechanics; per-unit-type allowlist; description-keyword similarity matching.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md` §3.A + §3.E — A + E candidate specifications.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md` — axis 1-4 dispositions (E primary + A comparator).
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP2-practical-decisions.md` — H6 work-location + H7 staging + M1 budget+abort + M3 auditor + M4 envelope.

### Standing context

- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.9.3 (c) Phase D dispatch contract requirements + §7.10.1 H4 + H5 + §7.10.2 M5.
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` §1 + §2 — H5 channel separation + M5 categorization rule grounding.

### Trajectory plan governance

- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §1.4 + §2.4 row D (paired audit) + §0.6 failure-mode taxonomy (channel-separation maps to integration-grammar-as-fact + comparative-claims-without-comparative-data).

### Methodology grounding

- `.planning/spikes/METHODOLOGY.md` — six interpretive lenses (Bayesian, Standpoint, Paradigm, Mechanistic, Values, Duhem-Quine); applied at FINDINGS.md drafting time per §7.3.
- `reference_spike_design.md` provenance pointer — falsifiable predictions + abort triggers + scope boundaries.

### What Phase D entry audit (Step 5) reads from Step 3

Per plan §2.4 row D paired:

- This MINI-SPEC.md (gate-3 contract; H4/H5/M5 amendments operationalized)
- Forward-reference to FINDINGS.md (not yet written; drafted post-execution)
- §4 success criteria + §6 falsifiers + §7 channel rule + §8 categorization rule

The audit reads MINI-SPEC alongside §7.10 + STEP1-design-space + STEP1-DISPOSITION + STEP2-practical-decisions — structural correction for Step 3 D5a inheritance + mini-spec evidence-load calibration + falsifier completeness + channel-separation discipline robustness.

### Logan-disposition turn

- 2026-04-30 /effort xhigh "green light" + "you didn't really proceed autonomously because you are checking in with me" — autonomous-within-phase Step 2 → Step 3 → Step 4 dispatch authorized; pause-point is Step 5 (Phase D entry audit) + Step 6 (Logan green-light at Phase D dispatch entry).

---

*Step 3 mini-spec authored by Claude (Opus 4.7, /effort xhigh) 2026-04-30 in-session-collaboration with Logan per trajectory plan §7.10.4 Step 3 + §0.7 hybrid autonomy. Mini-spec is the Phase D dispatch contract: gate-3 amended per §7.9.3 (c) + §7.10 H4/H5/M5. The in-session-collaboration risk applies recursively; Phase D entry audit per plan §2.4 row D paired is the structural correction. Subject to same fallibility caveat as STEP2-practical-decisions and DECISION-SPACE.md §0.*
