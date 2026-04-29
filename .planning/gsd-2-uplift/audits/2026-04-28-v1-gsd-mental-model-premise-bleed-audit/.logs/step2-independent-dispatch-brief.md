# Step-2 Independent Same-Vendor Premise-Bleed Audit — Dispatch Brief

You are the **Step-2 independent same-vendor adversarial auditor** for the v1-GSD mental-model premise-bleed audit on the gsd-2-uplift initiative.

## Operating mode (load-bearing — read first)

The spec at `AUDIT-SPEC.md` defines two steps: §3.3 Step-1 cross-vendor baseline (codex GPT-5.5 high) and §3.4 Step-2 same-vendor stress (default-fires-on-Class-C-with-differential). **You are operating under §3.4's manual-escalation discretion** — specifically, the "independent same-vendor read for cross-checking" example. This overrides §3.4's default-firing-condition + differential-analysis structure in the following ways:

- You operate **independently** of any Step-1 read. You do **not** read Step-1 findings, Step-1 dispatch brief, Step-1 logs, or any Step-1-derived material. The forbidden-reading list below makes this concrete.
- You produce a **self-contained independent FINDINGS document** following spec §6.1's Step-1 structure (not §6.2's differential structure). The differential analysis between your independent read and the prior independent read happens later in a separate step that you are not responsible for.
- Your role is **adversarial register-focused critique of plan-level framing**, grounded in stated goals + accepted ADRs + methodology disciplines (per your same-vendor adversarial-auditor doctrine). The audit lens is at spec §2; method is at spec §5.

This dispatch is methodologically deliberate: Logan invoked the spec §3.4 manual-escalation discretion to obtain an independent same-vendor read free of Step-1 priors, so that any later differential between the two independent reads carries no anchoring contamination.

## What to do

**Read the spec first**, in full:

```
/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md
```

Then execute the audit per the spec, with the §3.4-manual-discretion overrides above:

- §2 lens definition (corrected-frame vocabulary + §2.3 replacement-vocabulary lookup + META-SYNTHESIS §3 prohibited articulations).
- §4 artifacts under audit + §4.2 grounding inputs (prior-audit primary; narrow source-reading fallback at soft default ~5 file reads with explicit overflow protocol).
- §5 method — per-artifact pass with required §5.2.3 negative-space check; §5.3 cross-artifact propagation pass; §5.4 no-re-exploration discipline. (Use §5.2 sub-steps 1-4 + 6 + conditional 5; ignore §5.5 which presupposes Step-1 visibility.)
- §6.1 output shape — produce a self-contained Step-1-shaped FINDINGS document (you are *not* writing the differential §6.2 structure).

Apply the same classification rubric (§7) and disposition pathway (§8 non-binding signal per §6.1 §5).

## Forbidden reading (composed: spec §3.5 + Step-1-isolation additions)

You must **not** read any of:

**Per spec §3.5:**
- This conversation's transcript or any session-context.
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/handoffs/2026-04-28-post-W2-and-paired-synthesis-handoff.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/2026-04-28-comparison-drafting-decisions.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC-REVIEW.md`
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/STATE.md` and recent OVERVIEW.md updates referring to comparison-drafting status.

**Step-1 isolation (additional forbidden items for independence):**
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/FINDINGS.md` — Step-1 output. Do not read.
- `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/.logs/` — Step-1 dispatch logs/lastmsg. Do not read.
- Any other path containing "step1", "FINDINGS", "Step-1" outputs from the prior dispatch.

If you discover a file in your reading that appears to be Step-1 output or refers to Step-1 findings, **stop reading it immediately** and note the encounter in your FINDINGS-STEP2.md §4 self-flagged-concerns section as an isolation-incident. Do not let Step-1 content shape your independent read.

## Output target

Write your findings to:

```
/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/FINDINGS-STEP2.md
```

(Note: **NOT** `FINDINGS.md` — that's already taken by the prior independent read. Write to the `-STEP2` filename.)

Use the file structure per spec §6.1. Frontmatter:
- `type: premise-bleed-audit-findings-step2-independent`
- `auditor_step2: Claude same-vendor adversarial-auditor-xhigh (independent mode per spec §3.4 manual-escalation)`
- `mode: independent (no Step-1 priors; differential post-hoc in main thread)`
- `status: step2-independent-complete; differential-pending-main-thread`
- `target: <list of artifacts read>`

The file should be self-contained.

## Discipline reminders

- **Cite verbatim** for every quoted artifact passage; pair quotes with file:line citations.
- **Negative-space findings** (§5.2.3) must cite both the absent surface AND the grounding citation that establishes its source-centrality. Use prior-audit primary grounding first (§4.2 primary list); fallback to source-reading only when primary doesn't ground a specific claim, with explicit per-read justification under the soft-cap-with-overflow protocol.
- **Vetted-replacement vocabulary lookup** (§2.3) is a *reference, not a substitute* for vocabulary-precision judgment. If a v1-GSD-shaped phrasing in the audited artifacts plausibly belongs on the lookup but isn't there, flag it in FINDINGS §4 self-flagged-concerns rather than inventing replacement language.
- **Classification calibration** (§7): when uncertain between classes, name the uncertainty + list what would resolve it. Do not over-classify Class C; do not under-classify.
- **Non-binding disposition signal** (§6.1 §5): give per-option reasoning for commit-as-is / commit-with-addendum / revise-before-commit. Do not pick one — Logan disposes per §8.
- **No drafting suggestions** (§6.3): no revised wording proposals; no reframe proposals; no scope expansion to substance audit.
- **Length target** (§6.3): 200-500 lines for a single-step independent FINDINGS file.
- **Adversarial discipline**: as same-vendor reader, you are most likely to catch register-shaped framing-leak that cross-vendor would miss. Under-classification of register-shaped findings is the failure mode to guard against here. Over-classification is also a failure mode but the typical same-vendor risk is the opposite.
- **Same-vendor framing-leak caveat (M1)**: you and the dispatching project share Claude+Logan framing inheritance; flag in §4 self-flagged-concerns where you suspect you cannot self-detect a shared frame.

When complete, your final message should be a 2–4 paragraph executive summary covering: (1) headline independent findings + classification breakdown counts; (2) any isolation incidents encountered (per the forbidden-reading section); (3) confidence + key self-flagged concerns including same-vendor M1 caveat; (4) anything surprising relative to the spec's framing prediction.
