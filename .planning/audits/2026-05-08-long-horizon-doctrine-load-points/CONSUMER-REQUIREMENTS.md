# GSD Long-Horizon Doctrine-Load-Point Hook — Consumer-Side Requirements

**Authored:** 2026-05-08
**Author:** Claude (in coordination with Logan), arxiv-sanity-mcp side
**Sibling artifact:** `~/workspace/projects/gsd-2-uplift/.planning/migration/2026-05-08-gsd-gsdr-consolidation-plan.md` (in-progress, authored by parallel migration agent)
**Status:** Draft for migration-agent consumption

---

## Purpose

This document specifies what a real consumer (arxiv-sanity-mcp, with a mature doctrine corpus) needs from a "doctrine-load-point" hook added to GSD's planning workflows (`discuss-phase`, `plan-phase`, `execute-phase`, `verify-work`). It is **input to the migration agent's GSD-side patch design** — concrete consumer requirements rather than abstract feature spec.

The motivating gap: GSD's planning skills currently load `PROJECT.md`, `REQUIREMENTS.md`, `STATE.md`, prior `CONTEXT.md` files. They do **not** explicitly load `LONG-ARC.md`-style architectural-doctrine documents. Long-horizon thinking — anti-pattern detection, protected-seam preservation, anti-vision warnings, ADR consultation at decision boundaries — happens (or doesn't) implicitly via CLAUDE.md routing. This is unreliable and project-specific. GSD should bake the discipline in.

---

## Doctrine corpus this project actually maintains

For grounding, here is what arxiv-sanity-mcp keeps. The patch should accommodate at least this shape; other projects may have less, but rarely more.

| Document | Path | Type | Function | Trigger surface |
|---|---|---|---|---|
| LONG-ARC.md | `.planning/LONG-ARC.md` | planning-doctrine | Durable doctrine between VISION and operational canon. Anti-patterns, protected seams, explicit non-decisions, what-current-planning-must-do, reopen conditions. | Phase-level work touching ranking/retrieval/abstractions/MCP/spike-process |
| VISION.md | `.planning/VISION.md` | product-vision | Product identity, multi-lens claim, lens trajectory, **anti-vision** (foreclosed paths), audience grounding, open vision questions. | Milestone-level decisions, abstraction-introducing work |
| ADRs | `docs/adrs/ADR-000{1..5}.md` | architecture-decision | Settled decisions with rationale. Each binds a class of decisions. | Plan-phase, when proposed work touches the ADR's domain |
| METHODOLOGY.md | `.planning/spikes/METHODOLOGY.md` | methodology-doctrine | Paired review for framing claims, model verification before delegation, single-reader factual claims need verification, calibrated language as default register. | Agent dispatch, audit-spec drafting, deliberation boundary |
| PROJECT.md, ROADMAP.md, STATE.md, REQUIREMENTS.md | `.planning/` | operational | Live operational canon. GSD already loads these. | Existing surface — not in scope for this patch. |

Each doctrine document has structured frontmatter:

```yaml
---
document: LONG-ARC                  # canonical name
status: canonical                   # canonical | hypothesis | superseded
type: planning-doctrine             # planning-doctrine | product-vision | architecture-decision | methodology-doctrine
scope: <one-line scope statement>
last_updated: 2026-04-25
related_documents:
  - .planning/VISION.md
  - docs/adrs/ADR-0001-exploration-first.md
  - .planning/spikes/METHODOLOGY.md
---
```

ADRs use a different but compatible frontmatter (`status: Accepted | Proposed | Superseded`, `decision-id`, `supersedes`, `superseded-by`).

---

## What the hook must do

### 1. Load doctrine into agent prompts at decision points

The hook must inject relevant doctrine into the agent's working context at specific phase points. Not the whole document — just the relevant sections, surfaced as structured prompt content.

**Concrete points where injection matters:**

| Phase point | What to inject | Why |
|---|---|---|
| `discuss-phase:gray-area-surface` | `LONG-ARC.md § Explicit non-decisions` | When the discuss workflow is enumerating gray areas to discuss with the user, surface deferred-by-doctrine items so they don't get silently decided |
| `discuss-phase:option-presentation` | `LONG-ARC.md § Anti-patterns to detect` (relevant ones) | When presenting options to the user, flag if any matches a known anti-pattern (e.g., "Option B is tournament narrowing") |
| `plan-phase:before-research` | `LONG-ARC.md § Protected seams` + relevant ADRs | Before research dispatch, the planner needs to know what mustn't be broken |
| `plan-phase:after-draft` | All anti-patterns + protected seams + relevant ADRs (full content) | Run an explicit "ADR-against-current-work" audit on the draft plan |
| `execute-phase:task-boundary` | Anti-patterns relevant to the task type (e.g., "Closure pressure" for synthesis tasks) | Pattern-watch at every level of work |
| `verify-work:before-completion` | Protected seams + anti-vision items | Verification must check the work didn't drift |
| `new-milestone` | VISION.md (full) + LONG-ARC.md `§ Reopen conditions` | Milestone transitions are the natural reopen trigger |

### 2. Detect when triggers fire

Triggers map work-being-done to relevant doctrine. The arxiv-sanity-mcp project has a working trigger surface in `CLAUDE.md` — translate that pattern into structured config.

**Existing trigger pattern (from CLAUDE.md):**

```
Touching ranking, retrieval, or lens-architecture code → LONG-ARC.md (anti-patterns), ADR-0001, ADR-0005.
Adding a new abstraction or signal type → LONG-ARC.md (protected seams), VISION.md (anti-vision section).
Touching MCP tool, resource, or prompt surfaces → ADR-0004, LONG-ARC.md (MCP-native operations).
Proposing rights-affecting changes → ADR-0003.
Proposing changes to enrichment cost or scheduling → ADR-0002.
Proposing changes to spike program structure or methodology → METHODOLOGY.md, LONG-ARC.md (doctrine-interaction-with-spike-program).
```

**Trigger detection mechanisms — three levels of sophistication:**

- **Level 1 (cheap, sufficient):** explicit declaration in phase plan. `phase:requirements: [LENS-01, LENS-02]` triggers loading of all doctrine that mentions LENS-* requirements. Or `phase:touches: [ranking, retrieval]` triggers the relevant load-point.
- **Level 2 (medium):** keyword detection in phase goal/description. Surface candidate triggers; user confirms.
- **Level 3 (heavy):** semantic analysis of phase content vs doctrine corpus. Probably overkill for v1.

**Recommend: Level 1 with Level 2 fallback.** Phases declare what they touch; for unspecified phases, scan the goal text against trigger keywords.

### 3. Surface anti-patterns as named warnings, not generic risk

When an anti-pattern matches, the hook must surface it **by name with the project's counter-posture and a cite-back**. Generic "this might be a risk" is useless.

**Concrete shape:**

```
⚠️ Anti-pattern detected: "Tournament narrowing under disciplined framing"
   Source: LONG-ARC.md:47
   Pattern: Sequentially pruning candidates toward a winner.
   Counter-posture: rank-and-deprioritize, not eliminate; multi-lens framing replaces winner-pick.
   ADR binding: ADR-0001 (capability claim about coexistence architecture)
   What to do: re-frame the proposal as multi-lens; if winner-pick is genuinely intended, surface
   to deliberation rather than embedding it in a phase plan.
```

This format is non-negotiable; it's how anti-patterns become actionable rather than aspirational.

### 4. Run ADR-against-current-work audit at plan-phase boundary

LONG-ARC.md:50 explicitly calls out "ADR violation by gradual local-reasonable steps" as the canonical drift mode. The counter-posture LONG-ARC.md:103 specifies: "Run an ADR-against-current-work audit at each deliberation boundary. *Operational-hook status: pending.*"

**This patch is the operational-hook implementation.** Plan-phase, after draft, must:

1. Load all `accepted`-status ADRs (frontmatter filter)
2. For each ADR, run a check: does the draft plan contradict, weaken, or silently amend this ADR?
3. Surface findings as plan-level risk items
4. Require explicit acknowledgement (or doctrine update) for any non-trivial finding before plan finalizes

**Concrete output shape:**

```markdown
## ADR Audit (run 2026-05-08 at plan-phase:after-draft)

| ADR | Status | Audit finding |
|---|---|---|
| ADR-0001 (exploration-first) | Settled | ✓ Plan respects coexistence; no winner-pick |
| ADR-0002 (metadata-first lazy enrichment) | Settled | ⚠️ Plan task 12-02 may eager-enrich without justification |
| ADR-0003 (license/provenance) | Settled | ✓ |
| ADR-0004 (MCP as workflow substrate) | Settled | ✓ |
| ADR-0005 (multi-lens v0.2 substrate) | Settled | ✓ Plan implements ADR-0005's coexistence commitment in implementation |

**Action items:** acknowledge ADR-0002 finding before plan finalizes; either (a) revise task 12-02 to lazy-enrich or (b) record an explicit ADR-0002 amendment justifying the eager-enrich.
```

The audit's quality depends on agent capability. **Recommend: dispatch this audit to a known-quality model (Opus or equivalent).** Per project memory `feedback_no_explore_for_audits`: "Don't use default Explore agent for audits/gating evidence; use Opus directly or explicit `model: 'opus'` override."

### 5. Surface protected seams as gating warnings

Protected seams (LONG-ARC.md § "Protected seams") are architectural commitments that current planning must preserve. Touching them is not forbidden — but it requires explicit acknowledgement, not silent drift.

**Hook behavior:** if a phase plan touches a protected seam:
- Surface in plan as `[PROTECTED SEAM TOUCHED]: <seam>` with cite-back
- Require plan to record either (a) "preserves seam by <mechanism>" or (b) "amends seam — see deliberation `<path>`"
- Block plan-phase verification until acknowledgement is recorded

This is gating, not blocking. The user can always proceed; they just can't proceed silently.

### 6. Anti-vision check at milestone-audit boundary

Anti-vision items (VISION.md § "Anti-vision — what we are not") are *foreclosed* paths. Touching them is a stronger signal than touching protected seams — these are paths the project has explicitly rejected as part of product identity.

**Hook behavior at `new-milestone` and `milestone-audit`:**
- Load all anti-vision items
- For each, check whether the milestone (planned or shipped) drifts toward it
- If drift detected, surface as a milestone-level risk requiring explicit deliberation before commit

Example: VISION.md:80 "Not a ranked-list-but-fancier. Fusion-by-default would collapse multi-lens architecture back to single ranking." If a v0.2 phase silently defaults to fusion, the anti-vision check fires.

---

## Configuration shape (consumer-side proposal)

The patch needs a config knob in `.planning/config.json` so projects without a doctrine corpus aren't burdened. Proposed shape:

```json
{
  "doctrine": {
    "enabled": true,
    "documents": [
      {
        "path": ".planning/LONG-ARC.md",
        "type": "planning-doctrine",
        "frontmatter_status_required": "canonical",
        "load_at": ["discuss-phase", "plan-phase", "execute-phase", "verify-work"],
        "extract_sections": {
          "anti_patterns": "## Anti-patterns to detect",
          "protected_seams": "## Protected seams",
          "non_decisions": "## Explicit non-decisions",
          "reopen_conditions": "## Reopen conditions"
        }
      },
      {
        "path": ".planning/VISION.md",
        "type": "product-vision",
        "load_at": ["new-milestone", "milestone-audit", "plan-phase:before-draft"],
        "extract_sections": {
          "anti_vision": "## Anti-vision — what we are not"
        }
      },
      {
        "path": "docs/adrs/ADR-*.md",
        "type": "adr",
        "load_at": ["plan-phase:after-draft"],
        "frontmatter_status_filter": ["Accepted", "Settled"],
        "audit_command": "adr-against-current-work",
        "audit_model": "opus"
      },
      {
        "path": ".planning/spikes/METHODOLOGY.md",
        "type": "methodology-doctrine",
        "load_at": ["spike-design", "agent-dispatch", "deliberation-boundary"]
      }
    ],
    "trigger_routing": {
      "ranking|retrieval|lens-architecture": ["LONG-ARC.md§anti_patterns", "ADR-0001", "ADR-0005"],
      "abstraction|signal-type": ["LONG-ARC.md§protected_seams", "VISION.md§anti_vision"],
      "mcp-tool|mcp-resource|mcp-prompt": ["ADR-0004", "LONG-ARC.md§anti_patterns"],
      "rights|license|content-storage": ["ADR-0003"],
      "enrichment-cost|enrichment-scheduling": ["ADR-0002"],
      "spike-program|methodology": ["METHODOLOGY.md", "LONG-ARC.md§doctrine_interaction_with_spike_program"]
    },
    "behavior": {
      "anti_pattern_detection": "warn-by-name",
      "protected_seam_touch": "gate-with-acknowledgement",
      "anti_vision_drift": "surface-to-deliberation",
      "adr_audit_at_plan_phase": true,
      "fail_closed_on_malformed_doctrine": false
    }
  }
}
```

---

## Document conventions the patch should accept

Don't impose a strict schema; doctrine documents grow organically. The patch should accept what arxiv-sanity-mcp already maintains:

1. **YAML frontmatter** with at least `type` and `status`. Other fields optional but useful (`last_updated`, `related_documents`, `scope`).
2. **Section headings** as the extraction unit. The config block names sections by heading text; the extractor reads from heading to next-equal-level heading.
3. **Cite-back convention.** When doctrine references itself or other doctrine, format is `path:line` (e.g., `LONG-ARC.md:47`). The patch should resolve these so cites stay live across edits.
4. **Status values are not standardized across project types.** LONG-ARC uses `canonical | hypothesis | superseded`. ADRs use `Accepted | Proposed | Superseded`. The config block declares which statuses count as load-eligible per document.

---

## What this patch should NOT do

- **Do not auto-update doctrine.** Doctrine is human-edited. The hook reads, surfaces, audits — never writes.
- **Do not enforce a canonical structure across projects.** Projects without LONG-ARC.md or VISION.md should still work; the hook degrades to "no doctrine configured."
- **Do not silently override.** Every gating decision requires explicit user acknowledgement; gates can be disabled per-config but not bypassed silently.
- **Do not duplicate existing GSD discipline.** GSD already has `gsd-list-phase-assumptions`, `gsdr-deliberate`, `gsdr-audit`. The hook complements these by giving them doctrine context, not by replacing them.

---

## Integration with existing GSDR meta-tools

The patch lives in GSD core but should provide hooks that GSDR's meta-tools can consume:

- **`gsdr:reflect`** — should be able to query "what doctrine was consulted in the last N phase boundaries; were any anti-patterns flagged but ignored?"
- **`gsdr:signal`** — anti-pattern flags should auto-emit signals (`signal_type=anti_pattern_detected`, `signal_value=<pattern_name>`, `provenance=<phase>:<task>:<file>:<line>`)
- **`gsdr:deliberate`** — when a deliberation references a protected seam, the hook surfaces the seam's text and binding ADR
- **`gsdr:audit`** — the 3-axis audit framework benefits from doctrine as a load-bearing reference

The patch should expose a clean API surface for these consumers, not just for the in-phase hooks.

---

## Open design questions for the migration agent

1. **Where does the doctrine-loader live?** Options: (a) inline in each phase command's SKILL.md (copy-paste, simple but DRY-violating); (b) separate `gsd-doctrine-load` agent invoked from each phase; (c) a runtime hook injected by GSD's session-start. Trade-off is between simplicity and reusability. **Lean: (b)** — clean separation, agent-callable from any phase, testable.
2. **Section extraction: regex-based or markdown-AST?** Regex is fragile but cheap. Markdown-AST is robust but requires a parser dependency. Trade-off varies by GSD's existing dependency posture. **Lean: regex with explicit heading-text matching** for v1; AST upgrade if heading-name drift causes pain.
3. **Trigger keyword detection: hand-curated or learned?** v1 should be hand-curated (the trigger map is part of project config). Future: GSDR's signal-collector could learn trigger correlations from past phase outcomes.
4. **ADR audit: synchronous in plan-phase or async via `gsdr:audit`?** Synchronous gates plan finalization; async surfaces findings post-draft. **Lean: synchronous with `audit_model: "opus"` config**, dispatchable via `gsdr:audit` for re-runs.
5. **Multi-project doctrine sharing.** Logan has multiple projects (scholardoc, philograph-mcp, audiobookify, etc.). Should doctrine be sharable across projects via symlink, or always project-local? **Lean: project-local for v1**, with `related_documents` frontmatter pointing to cross-project references as advisory.
6. **What happens when doctrine is missing or malformed?** `fail_closed_on_malformed_doctrine: false` (default warn-and-continue). Strict projects can flip the flag.

---

## Acceptance criteria for the patch (consumer-side)

The patch is acceptable to arxiv-sanity-mcp when:

1. ✅ Running `/gsd-discuss-phase 12` loads `LONG-ARC.md § Explicit non-decisions` and surfaces deferred items as "do-not-decide-silently" gray areas.
2. ✅ Running `/gsd-plan-phase 12` runs an ADR-against-current-work audit on the draft plan and surfaces findings before finalization.
3. ✅ Running `/gsd-execute-phase 12` includes anti-pattern context in the executor's prompt at task boundaries (specifically: "Closure pressure at every layer" and "Single-lens interface by accident" for Phase 12).
4. ✅ When a phase plan touches a protected seam (e.g., "Lens-extensibility"), the plan output explicitly records `[PROTECTED SEAM TOUCHED]: <seam> — preserved by <mechanism>` before plan-phase verification can pass.
5. ✅ When a milestone audit runs, anti-vision drift is surfaced as a milestone-level risk if any v0.2 phase silently defaults to fusion (per VISION.md:80).
6. ✅ The patch degrades gracefully on projects without `.planning/LONG-ARC.md` (no doctrine configured → no hook activity).
7. ✅ The patch composes with GSDR's meta-tools (signals auto-emitted, deliberations can reference seams, audits can re-run on demand).
8. ✅ Performance: doctrine-loading adds ≤2s to phase-command startup (rough budget; calibrate against real arxiv-sanity-mcp doctrine corpus size).

---

## Cross-references

- **Migration plan (in-progress):** `~/workspace/projects/gsd-2-uplift/.planning/migration/2026-05-08-gsd-gsdr-consolidation-plan.md`
- **arxiv-sanity-mcp LONG-ARC.md:** `.planning/LONG-ARC.md` (118 lines, canonical)
- **arxiv-sanity-mcp VISION.md:** `.planning/VISION.md` (117 lines)
- **CLAUDE.md doctrine load-points:** project-root, lines ~30-43 (current routing-by-trigger surface, durable across runtimes per its own self-description)
- **Methodology doctrine:** `.planning/spikes/METHODOLOGY.md` (interpretive lenses + practice disciplines per project memory `reference_spike_design`)
- **gsd-2-uplift INITIATIVE.md:** `~/workspace/projects/gsd-2-uplift/.planning/INITIATIVE.md` — this consumer requirements doc partially answers what that initiative was scoping, by giving the migration agent concrete shape from a real consumer

---

## Note on scope

This document is **consumer requirements**, not implementation. It says what the hook must do from arxiv-sanity-mcp's perspective; it does not say how GSD should implement it. The migration agent has authority on implementation shape (level of indirection, code structure, testing approach). Conflicts between this consumer-requirements document and the migration agent's implementation plan should be resolved through discussion before patches are applied.

If a requirement here proves expensive or impossible, the migration agent should surface it as an open question in their plan rather than silently dropping it. The corollary: requirements here are not all equally load-bearing. The ADR audit (§4) and anti-pattern surfacing (§3) are non-negotiable; configuration shape (§Configuration shape) is illustrative; cross-project sharing (§Open design questions Q5) is genuinely open.

---

*Draft 2026-05-08. Will be revised once the migration agent's plan lands and design conflicts surface.*
