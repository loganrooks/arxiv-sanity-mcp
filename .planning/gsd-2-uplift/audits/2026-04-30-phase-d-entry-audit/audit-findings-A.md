---
type: audit-findings
date: 2026-04-30
auditor: cross-vendor codex GPT-5.5
reasoning_level: high
mode: independent
artifact_under_audit: Phase D entry corpus
status: complete
---

# audit-findings-A.md — Phase D Entry Audit

## §0. Summary

Auditor: cross-vendor codex GPT-5.5 at high reasoning level, independent mode.

Class breakdown: 1 Class C, 4 Class B, 2 Class A.

Headline: the corpus is close, but not dispatch-ready as written. The main problem is not the E-primary/A-comparator strategy itself; it is that the mini-spec's parallel E/A comparator is structurally confounded by gsd-2's actual bundled-skill sync and first-wins skill collision behavior. The second-largest problem is that the existing gsd-2 decision primitive inventory is materially incomplete: gsd-2 already has a DB-backed decision-save path, canonical generated `DECISIONS.md` table, MCP decision tool, and memory dual-write path that the corpus under-counts.

Non-binding overall disposition signal: **Revise-before-dispatch, narrow**. I do not recommend re-architecting Steps 0-4. I recommend a short pre-dispatch revision/addendum that fixes the A/E comparator mechanics, re-bases decision-trace on gsd-2's existing decision substrate, and updates the activation/effective-state tests accordingly.

## §1. Methodology Applied

I read the required Phase D entry corpus listed in `AUDIT-SPEC.md`: `INCUBATION-CHECKPOINT.md` §7.10, `STEP1-design-space.md`, `STEP1-DISPOSITION.md`, `STEP2-practical-decisions.md`, `MINI-SPEC.md`, and `STEP4-gates-and-L-tier.md`. I read the upstream grounding required by the spec: `P5-effective-state-emission-findings.md`, `M2-codebase-snapshot-findings.md`, `INCUBATION-CHECKPOINT.md` §7/§7.9, `RELATIONSHIP-TO-PARENT.md`, trajectory-plan excerpts, `METHODOLOGY.md`, and `DECISION-SPACE.md` §1.17-§1.18.

I did not read `audit-findings-B.md` and did not read prior audit folders. I did inspect the gsd-2 source checkout at `/home/rookslog/workspace/projects/gsd-2-explore`, confirmed it was at commit `42ef05fbec6d581c12000efb2cd27e925294a1ea`, and used source checks to test claims about skills, resource sync, decision tools, preferences, and unit-context manifests.

Time allocation was evidence-heavy rather than stylistic: corpus read first, then source verification of the highest-risk claims called out by the prompt and `AUDIT-SPEC.md` §1/§3.

## §2. Findings

### F-PD-A1 — Parallel E/A comparator is structurally confounded by skill sync + same-name collision

**Class:** C  
**Confidence:** high  
**Lens:** design-framing-quality / substantive divergence / evidence-load  
**Where:** `MINI-SPEC.md` §1.E, §1.A, §2.1, §4; `STEP2-practical-decisions.md` §2.M4; gsd-2 `resource-loader.ts`, `skills.ts`

**What:** The mini-spec requires both Shape E and Shape A to exist simultaneously with `name=decision-trace`, and requires P1/P4 evidence that "both E and A appear" and that collision is diagnosed. Against gsd-2 source, that is not a clean parallel comparator. Bundled skills are synced into `~/.agents/skills` by `initResources`, and `syncResourceDir` removes matching destination subdirectories before copying bundled skills. The skill loader then deduplicates by skill name with first-wins collision behavior.

**Why:** The mini-spec says E lives at `src/resources/skills/decision-trace/SKILL.md` and A lives at `~/.agents/skills/decision-trace/SKILL.md`, both with `name=decision-trace` (`MINI-SPEC.md:66-80`, `MINI-SPEC.md:92-108`). It then defines P1 pass as "Both E and A appear" and P4 as simultaneous registration with first-wins collision diagnostic (`MINI-SPEC.md:116-120`), and makes P1-P4 part of success (`MINI-SPEC.md:164-166`).

The source does not support that evidence shape cleanly. `initResources` defaults `skillsDir` to `~/.agents/skills` and syncs bundled `resources/skills` there (`src/resource-loader.ts:559`, `src/resource-loader.ts:596-598`). `syncResourceDir` removes destination subdirectories that exist in source before copying (`src/resource-loader.ts:256-275`). Then skill loading records one winner per `skill.name` and reports the loser as collision (`packages/pi-coding-agent/src/core/skills.ts:401-417`), while the visible prompt block is generated from the resolved visible skills list (`packages/pi-coding-agent/src/core/skills.ts:311-338`). That means E may overwrite or occupy the same ecosystem path as A at runtime, and even if both physical files can be staged in separate paths, the observable prompt surface cannot satisfy "both appear" under the same name.

This is not just a test detail; it undermines the R2-vs-R4 comparator as specified. The corpus correctly wants the contrast to be R-strategy/integration surface, not semantic content (`MINI-SPEC.md:104-108`), but the current implementation plan tests install/sync/collision artifacts rather than a clean R2-vs-R4 decision-trace comparison.

**Suggested disposition:** Revise before dispatch. Keep E primary + A comparator if desired, but change the comparator mechanics before Phase D starts. Acceptable narrow fixes include: use distinct names such as `decision-trace` and `decision-trace-r4`; run sequential A-only/E-only observations rather than simultaneous same-name registration; or explicitly define the collision itself as the test and drop "both appear" as a pass condition. Do not dispatch with the current P1/P4/success wording.

### F-PD-A2 — Existing gsd-2 decision primitives are materially under-inventoried

**Class:** B  
**Confidence:** high  
**Lens:** substantive divergence / negative-space / design-framing-quality  
**Where:** `M2-codebase-snapshot-findings.md` §3/§7/§8; `STEP1-design-space.md` §1.3/§3.D/§3.E; gsd-2 MCP + DB writer + workflow docs

**What:** The corpus treats `.gsd/DECISIONS.md` primarily as a one-line convention appended by a few skills. Source shows a richer existing primitive family: MCP decision-save tools, structured decision fields, DB persistence, canonical generated `DECISIONS.md`, and memory dual-write with structured fields. That does not invalidate E primary, but it does mean Shape D was framed as more novel and heavier than gsd-2's actual surface warrants.

**Why:** M2 describes `.gsd/DECISIONS.md` as a "lightweight overlap" and "one-line decision log" (`M2-codebase-snapshot-findings.md:165-170`), while Step 1 says Shape D would enrich the file "from one-line append-only convention to structured" entries (`STEP1-design-space.md:157-164`). Step 1 then positions E as reading the one-line convention as-is and not testing `.gsd/DECISIONS.md` substrate evolution (`STEP1-design-space.md:197-206`).

But gsd-2 exposes `gsd_decision_save` / `gsd_save_decision` in the MCP workflow tool catalog (`packages/mcp-server/src/workflow-tools.ts:606-608`) with structured fields for scope, decision, choice, rationale, revisable, when-context, and made-by (`packages/mcp-server/src/workflow-tools.ts:1246-1255`). The tool description says it records a project decision to the GSD database and regenerates `DECISIONS.md` (`packages/mcp-server/src/workflow-tools.ts:1401-1415`). The workflow docs define a canonical table-shaped `DECISIONS.md` register (`src/resources/GSD-WORKFLOW.md:234-260`), and the writer generates a canonical table with a `Made By` column (`src/resources/extensions/gsd/db-writer.ts:76-112`). `saveDecisionToDb` persists structured decisions (`src/resources/extensions/gsd/db-writer.ts:455-489`) and dual-writes a structured memory record (`src/resources/extensions/gsd/db-writer.ts:572-604`).

So the closer existing analog is not only `forensics`; it is the existing decision-save/register/memory family. M2 itself flags MCP workflow tools and DECISIONS schema as not fully read (`M2-codebase-snapshot-findings.md:270-272`), but Step 4 still marks the existing-primitives inventory complete (`STEP4-gates-and-L-tier.md:131-135`). That completion claim is too strong.

**Suggested disposition:** Add a pre-dispatch revision/addendum to M2/Step 1/Mini-spec: decision-trace must be evaluated against the DB-backed decision substrate, not just hand-written `.gsd/DECISIONS.md` lines. Re-evaluate D-vs-E lightly: E can remain primary, but its B1/B4 tests should include the MCP/DB/table/memory path as source material, and Shape D should be described as extending an existing structured primitive rather than inventing structure from scratch.

### F-PD-A3 — P5 layer-attribution success criterion is stricter than the available surface

**Class:** B  
**Confidence:** high  
**Lens:** evidence-load / effective-state-emission scope  
**Where:** `P5-effective-state-emission-findings.md` §2/§6/§7; `MINI-SPEC.md` §2.2/§4; gsd-2 preferences source

**What:** P5's sub-option (ii) recommendation is basically supported by source, but the mini-spec turns the caveat into a success criterion that may be unachievable without a helper/API tributary. It requires the skill to read preference files directly and preserve project/global/profile/mode layer attribution. Direct file reads do not recover all effective defaults or field-level provenance.

**Why:** P5 correctly finds no MCP or headless surface exposing effective preferences and recommends documenting the caveat (`P5-effective-state-emission-findings.md:22-37`, `P5-effective-state-emission-findings.md:241-286`, `P5-effective-state-emission-findings.md:358-380`). It also says the skill should capture layer attribution because the merge pipeline does not surface it (`P5-effective-state-emission-findings.md:384-392`). The mini-spec makes this B3 pass condition: read `~/.gsd/PREFERENCES.md` and `.gsd/PREFERENCES.md` directly and preserve project/global/profile/mode attribution (`MINI-SPEC.md:126-129`), then requires B1-B5 to pass for success (`MINI-SPEC.md:164-167`).

The source makes final layer attribution more complex. `loadEffectiveGSDPreferences` merges global and project preferences, then applies token-profile defaults and mode defaults as lower-priority layers (`src/resources/extensions/gsd/preferences.ts:149-201`). The returned `LoadedGSDPreferences` includes path, scope, preferences, and warnings, but no per-field provenance (`src/resources/extensions/gsd/preferences-types.ts:485-491`). Profile defaults derive concrete model/default values from available model IDs and routing config (`src/resources/extensions/gsd/preferences-models.ts:431-500`). Validation warns on unknown keys and says they are ignored (`src/resources/extensions/gsd/preferences-validation.ts:52-60`), confirming P5's silent-drop-adjacent open question as a real caveat rather than a Phase E-only curiosity.

**Suggested disposition:** Revise B3 before dispatch. Either downgrade it to "trace explicit file-origin and mark derived defaults as unresolved unless helper evidence is available," or add a tiny tributary that emits effective preferences with field provenance. Without that revision, Phase D can falsely fail a useful skill for not reconstructing provenance that gsd-2 itself does not expose.

### F-PD-A4 — Unit-context-manifest/composer status changes the activation and touchpoint story

**Class:** B  
**Confidence:** medium-high  
**Lens:** negative-space / substantive divergence / evidence-load  
**Where:** `M2-codebase-snapshot-findings.md` §8; `MINI-SPEC.md` §1.E/§2.1/§6; `STEP2-practical-decisions.md` §2.M4; gsd-2 `unit-context-*` and `auto-prompts.ts`

**What:** The mini-spec treats `skill-manifest.ts` allowlist updates as the likely conditional second touchpoint for lifecycle activation. Source shows the current unit-context composer/manifest surface is more advanced and more directly relevant than M2 sampled. For the specific lifecycle steps named by the mini-spec, `complete-milestone` and `reassess-roadmap` both have `skills: { mode: "all" }`, but different preferences policies; `reassess-roadmap` has `preferences: "none"`. That affects both activation testing and the P5 layer-attribution test.

**Why:** M2 explicitly flagged `unit-context-manifest.ts` Phase 2-4 status as uninvestigated (`M2-codebase-snapshot-findings.md:270`). The mini-spec nevertheless says that if lifecycle activation is excluded by per-unit-type allowlist, update `skill-manifest.ts`, likely for `complete-milestone` and `reassess-roadmap` (`MINI-SPEC.md:78-80`). It then tests P3 as per-unit-type allowlist behavior and makes possible allowlist cascades a falsifier (`MINI-SPEC.md:116-119`, `MINI-SPEC.md:233-235`). Step 2 similarly scopes the second touchpoint as `skill-manifest.ts` (`STEP2-practical-decisions.md:170-175`).

Source shows the composer is not merely future-looking: `composeUnitContext` was added as the phase 3.5 v2 surface (`src/resources/extensions/gsd/unit-context-composer.ts:1-21`, `src/resources/extensions/gsd/unit-context-composer.ts:149-187`). The `complete-milestone` manifest has `skills: { mode: "all" }`, `preferences: "active-only"`, and inlines `decisions` (`src/resources/extensions/gsd/unit-context-manifest.ts:402-421`). `reassess-roadmap` also has `skills: { mode: "all" }`, but `preferences: "none"` and inlines `decisions` (`src/resources/extensions/gsd/unit-context-manifest.ts:508-523`). `auto-prompts.ts` says explicit skill activation should not be dropped by the unit-type manifest and describes the manifest's "real home" as skill catalog rendering, with auto-match gated only under `skill_discovery: "auto"` (`src/resources/extensions/gsd/auto-prompts.ts:827-840`, `src/resources/extensions/gsd/auto-prompts.ts:869-890`).

**Suggested disposition:** Add an activation matrix before dispatch: distinguish skill catalog visibility, explicit skill activation, auto-discovery, unit-context manifest skill mode, and preference-inlining policy. Do not assume `skill-manifest.ts` is the only or primary second touchpoint. In particular, if `reassess-roadmap` is a test step, record that `preferences: "none"` may make P5 caveat behavior non-observable in that unit context.

### F-PD-A5 — Real test-task selection is D5a-heavy with no low-inheritance comparator

**Class:** A  
**Confidence:** medium  
**Lens:** D5a leak / negative-space  
**Where:** `STEP2-practical-decisions.md` §2.M4; `MINI-SPEC.md` §2.3/§9; `RELATIONSHIP-TO-PARENT.md` §1

**What:** The corpus acknowledges that framing-widening and backup test tasks carry D5a inheritance, but it does not add a lower-inheritance comparator task. This is acceptable as an addendum-level issue, not a blocker, because the risk is acknowledged. Still, the current test set may over-reward a skill that mirrors the co-produced vocabulary rather than independently reconstructing a decision.

**Why:** Step 2 defends real tasks over synthetic tasks and names framing-widening / premise-bleed / incubation-checkpoint as candidates, while acknowledging all are Claude+Logan co-produced (`STEP2-practical-decisions.md:173-196`, `STEP2-practical-decisions.md:204-206`). The mini-spec names framing-widening and incubation-checkpoint as test/backup surfaces and flags D5a inheritance (`MINI-SPEC.md:306-320`). `RELATIONSHIP-TO-PARENT.md` also says the test-case-vs-substrate frame is stipulated, not observed (`RELATIONSHIP-TO-PARENT.md:31-40`).

**Suggested disposition:** Add one low-inheritance comparator task if cheap: for example, reconstruct a gsd-2 decision from source/DB/workflow docs alone, or use a small synthetic counter-task only to test whether the skill overfits the R1-R5/six-context/four-act vocabulary. Keep the real arxiv-sanity-mcp task as primary, but add the comparator to detect vocabulary mirroring.

### F-PD-A6 — Checklist completion overstates inventory quality

**Class:** A  
**Confidence:** high  
**Lens:** evidence-load / framing-leak  
**Where:** `STEP4-gates-and-L-tier.md` §3/§4; `M2-codebase-snapshot-findings.md` §8

**What:** Step 4 appropriately acknowledges that checklist completion is artifact-existence rather than artifact-quality, but it still marks "H3 existing-primitives inventory complete" as complete. The source checks above show the inventory was not complete in the substantive sense: decision-save/DB/memory and unit-context surfaces were known open questions and turned out to be relevant.

**Why:** M2 listed `unit-context-manifest`, MCP workflow tools, DECISIONS schema, and skill-health as uninvestigated (`M2-codebase-snapshot-findings.md:262-275`). Step 4 marks H3 inventory complete using M2 + Step 1 as evidence (`STEP4-gates-and-L-tier.md:131-135`) while also saying the checklist is artifact-existence, not artifact-quality (`STEP4-gates-and-L-tier.md:154-160`). The second statement is the right discipline; the row label should follow it.

**Suggested disposition:** Addendum only: rename the row/status from "inventory complete" to "inventory pass performed; open primitives carried into audit." This avoids turning a sampled probe into closure evidence.

### F-PD-A7 — Heal-skill / skill-health exclusion is acceptable, but should become a Phase D observation hook

**Class:** A  
**Confidence:** medium  
**Lens:** negative-space  
**Where:** `M2-codebase-snapshot-findings.md` §8; `STEP2-practical-decisions.md` §2.M4

**What:** Deferring heal-skill / skill-health integration is acceptable for the skill-only Phase D envelope, but the exclusion leaves a useful observation surface unused. Phase D is partly about whether a new skill activates and produces useful or bad outcomes; skill-health is explicitly adjacent to "skill X was used and should be reviewed."

**Why:** M2 flagged heal-skill / skill-health as not read and potentially relevant (`M2-codebase-snapshot-findings.md:268`, `M2-codebase-snapshot-findings.md:275`). Step 2 excludes it and flags it for Phase E (`STEP2-practical-decisions.md:181-190`). That is reasonable under the ≤2 touchpoint envelope, but Phase D can still log whether decision-trace would have generated a skill-health review queue item if the subsystem were in scope.

**Suggested disposition:** Add a non-implementation observation line to EXECUTION-LOG/FINDINGS: "Did this run reveal anything skill-health should capture?" Do not integrate the subsystem in Phase D unless another falsifier fires.

## §3. Negative-Space Catalogue

Load-bearing exclusions:

1. **Bundled-skill sync semantics.** The corpus treats in-tree E and user-side A as separable locations; gsd-2 syncs bundled skills into the same ecosystem skill directory and dedupes by name. This is load-bearing for dispatch.

2. **DB-backed decision substrate.** The corpus under-counts `gsd_decision_save`, `DECISIONS.md` generation, and memory dual-write as existing primitives. This is load-bearing for deciding what decision-trace should read and what Shape D means.

3. **Field-level preference provenance.** The corpus asks for layer attribution but does not account for the fact that gsd-2's effective preference object lacks per-field provenance and derives defaults from profile/mode/model registry state. This is load-bearing for B3 success/failure interpretation.

4. **Unit-context-manifest/composer activation surface.** The corpus routes activation concern through `skill-manifest.ts`; source indicates unit-context and auto-prompt behavior need to be part of the activation evidence matrix.

Principally excluded with acceptable justification:

1. **Workflow template / router skill.** Excluding it is principled for a first skill-only spike, provided falsifier #4 is honored if the single skill exceeds 500 lines or becomes workflow-shaped.

2. **Hook primitive and YAML deterministic workflow.** Excluding these is acceptable under reversibility and spike-size constraints. I found no source evidence that they must be in Phase D.

3. **Full skill-health integration.** Excluding implementation is acceptable, but observation should be logged because skill-health is relevant to "new skill produced bad outcome."

4. **Cross-project decision-trace.** Excluding cross-project scope is acceptable; `RELATIONSHIP-TO-PARENT.md` explicitly treats arxiv-sanity-mcp as a diagnostic test case, not the whole substrate universe.

## §4. Synthesis

Is the corpus dispatch-ready? **Not as written.** The problem is narrow but real: the A/E comparator success criteria conflict with gsd-2's actual skill sync and collision behavior. Dispatching without revising this will produce ambiguous evidence even if the implementation work is competent.

Biggest risk: Phase D returns "A vs E evidence" that is actually "same-name collision / managed-resource overwrite / prompt catalog visibility evidence." That would contaminate Phase E's re-read of substrate shape.

Strongest landed discipline: the corpus repeatedly names its own audit-priority risks instead of burying them. The H5 channel separation rule and M5 test-case-vs-substrate labeling are the right kind of discipline, even though they need source-grounded refinement before dispatch.

Would benefit from xhigh re-dispatch: none of my findings require xhigh to make the disposition call. The only candidate is F-PD-A4 if Phase D wants a full source-level activation architecture audit before coding; for the dispatch decision, high-effort source checks were enough to show the mini-spec needs an activation matrix.

## §5. Non-binding Overall Disposition Signal

**Revise-before-dispatch, narrow.**

Required before Phase D first-target dispatch:

1. Fix the E/A comparator mechanics and P1/P4/success criteria.
2. Add the existing decision-save/DB/generated-DECISIONS/memory primitive family to the source-grounding.
3. Revise B3 layer-attribution so it is achievable and falsifiable against gsd-2's actual preference surfaces.
4. Add a source-grounded activation matrix covering skill catalog, explicit activation, auto-discovery, unit-context manifest, and preferences policy.

No re-architecture of the six-step Phase D entry workflow is warranted by this audit.
