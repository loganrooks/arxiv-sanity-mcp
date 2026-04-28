---
type: gate-disposition
date: 2026-04-28
gate: 1
audit: 2026-04-28-cross-vendor-codebase-understanding-audit
decision: proceed-broad-sample
status: complete
---

# Gate 1 Disposition — Proceed Broad Sample

## 1. Decision

Proceed with **Wave 2 broad sample**: three high-reasoning adjudicators, aligned to the Wave 1 scout domains.

Wave 2 should use:

- `wave-2/wave-2-adjudication-01-topology-runtime.md`
- `wave-2/wave-2-adjudication-02-extension-workflow.md`
- `wave-2/wave-2-adjudication-03-release-practice.md`

This is not a constructive remap trigger. It is a bounded claim-adjudication pass.

## 2. Why Broad Sample, Not Narrow

Broad sample is warranted because each scout found claims that are mechanically source-supported at a surface level but still load-bearing and interpretive at the synthesis level.

### 2.1 Topology/runtime has several separate decision-bearing claims

Scout 01 confirms several simple topology/runtime claims, including plural runtime surfaces, the vendored Pi relationship, and missing ADR-010 clean-seam packages. It also explicitly says the architecture output and audit look mechanically accurate for checked simple claims, while intervention-strategy implications remain adjudication work (`wave-1/wave-1-scout-01-topology-runtime.md:13-21`).

The same scout nominates multiple high-adjudication claims: how to phrase "vendored modified Pi fork," whether there is a partial clean seam despite missing ADR-010 packages, which MCP surface matters, whether RPC/headless is a better orchestration seam than extensions for some uplift work, and whether docs/source divergence around RTK and headless exit codes is material (`wave-1/wave-1-scout-01-topology-runtime.md:117-133`).

This is too much for a single mixed-domain adjudicator without reintroducing broad plausible-summary risk.

### 2.2 Extension/workflow has the densest subsystem-boundary problem

Scout 02 confirms that extension/workflow surfaces are plural: Pi extensions, GSD ecosystem extensions, workflow plugins/templates, skills, shell hooks, and GSD post-unit/pre-dispatch hooks (`wave-1/wave-1-scout-02-extension-workflow.md:13-21`). It also maps at least eight mechanisms, including Pi extensions, GSD ecosystem extensions, workflow plugins, markdown-phase, yaml-step, skills, hooks, and the Claude Code CLI provider extension (`wave-1/wave-1-scout-02-extension-workflow.md:43-91`).

The scout explicitly marks semantic and strategic interpretation as high-adjudication work: whether all four surfaces should be called "extension surfaces," which subsystem is the right target for a given uplift act, whether markdown-phase limitations materially weaken R2 viability, whether yaml-step is mature enough for deterministic uplift workflows, and whether hook layers compose safely (`wave-1/wave-1-scout-02-extension-workflow.md:107-147`).

This domain should remain separate because it is the highest-risk place for conflating distinct mechanisms into one "extension" concept.

### 2.3 Release/practice remains materially bounded by history and practice interpretation

Scout 03 confirms that the local checkout is shallow and that cadence claims are visible-window observations, not complete-history claims (`wave-1/wave-1-scout-03-release-practice.md:13-20`, `wave-1/wave-1-scout-03-release-practice.md:48-55`). It also confirms formal machinery exists while observed practice still requires interpretation: release scripts, GitHub workflows, changelog scripts, templates, PR/contribution policy, breaking-change/deprecation machinery, and visible removals under `Fixed`/`Changed` sections (`wave-1/wave-1-scout-03-release-practice.md:57-90`).

The scout nominates high-adjudication claims around whether machinery-vs-practice is a stable pattern, whether recent removals lacked meaningful deprecation, whether absent `BREAKING CHANGE` markers indicate a convention-enforcement gap, whether cadence materially increases maintenance risk, and whether templates reflect actual project practice (`wave-1/wave-1-scout-03-release-practice.md:105-145`).

This requires its own adjudicator because the evidence mix is source, shallow local history, docs/templates, changelog practice, and potentially external GitHub release/PR evidence.

## 3. Why Not Pause, Re-Slice, Or Trigger Constructive Remap

### 3.1 No pause/re-slice trigger

The three scout domains still fit the material surfaced:

- topology/runtime: package boundaries, runtime entrypoints, Pi vendoring, MCP/RPC/headless.
- extension/workflow: extension APIs, workflow engines, skills, hooks, provider extension behavior.
- release/practice: changelog, tags/history, release scripts/workflows, breaking-change practice.

The freshness delta did not invalidate that partition. It found only a small topology/runtime freshness impact, a small release/practice freshness impact, and a concrete extension/workflow delta that was handled by running Scout 02 against fresh `origin/main` (`wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:56-62`, `wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:112-118`).

### 3.2 No constructive-remap trigger yet

The scouts found possible omissions and conflations, but not enough to conclude the Claude-led investigation is structurally unreliable before high adjudication.

Examples:

- Scout 01 says the checked architecture output and audit are mechanically accurate on simple claims, while strategic implications still need adjudication (`wave-1/wave-1-scout-01-topology-runtime.md:21`).
- Scout 02 confirms the source inventory basis for plural extension-adjacent subsystems, while reserving semantic/R-strategy mapping for high adjudication (`wave-1/wave-1-scout-02-extension-workflow.md:93-105`, `wave-1/wave-1-scout-02-extension-workflow.md:107-147`).
- Scout 03 confirms formal machinery and visible practice evidence, while explicitly limiting stable-pattern claims to high adjudication because of shallow history and interpretive practice questions (`wave-1/wave-1-scout-03-release-practice.md:96-103`, `wave-1/wave-1-scout-03-release-practice.md:105-145`).

That means the right next move is claim adjudication, not replacement mapping.

## 4. Modifications, Reframes, And Additions Before Wave 2

### 4.1 No major reframing of the audit plan

The original audit posture should stand: this remains a challenge audit before a constructive remap. The scouts did not show that a full replacement model is already required.

### 4.2 Keep the three-domain split

The three-domain split should be retained for Wave 2. Collapsing to one high adjudicator would undercut the reason for Wave 1: source surfaces are broad enough that a single agent would likely compress topology, extension/workflow, and release/practice into a plausible but under-grounded synthesis.

### 4.3 Add explicit Wave 2 qualification: use freshness addenda

Adjudicator A and Adjudicator C must treat the Scout 01 and Scout 03 source freshness addenda as part of the reports. The delta scout found that the original reports were not materially invalidated, but some details changed:

- `gsd auto` is no longer accurately summarized as unconditional headless shorthand; it is TTY-gated in the fresh source (`wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:75-81`; `wave-1/wave-1-scout-01-topology-runtime.md:161-168`).
- Scout 03's latest-commit observation is stale after fetch, but the delta did not touch release machinery, changelog, PR templates, version metadata, or tags (`wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:83-94`; `wave-1/wave-1-scout-03-release-practice.md:160-169`).

### 4.4 Add explicit Wave 2 qualification: release/practice claims remain shallow-history-bounded

Adjudicator C must not turn the shallow local history into a complete-history claim. Scout 03 reports the clone is shallow and says cadence/absence findings are lower-bound or visible-window observations (`wave-1/wave-1-scout-03-release-practice.md:48-55`).

If Adjudicator C needs complete release history, GitHub release bodies, PR discussions, or Actions evidence, it should request a scoped escalation or mark the claim as not decidable from inspected evidence. It should not silently infer full practice from the shallow clone.

### 4.5 Add explicit Wave 2 qualification: separate mechanism inventory from R-strategy meaning

Adjudicator B should distinguish:

- existence of mechanisms, which Scout 02 often mechanically confirms;
- semantic grouping, such as whether workflows/skills/hooks are "extension surfaces";
- downstream strategy meaning, such as whether a mechanism supports R2, R4, or a hybrid.

Scout 02 explicitly says mapping the four surfaces to R-strategy viability is non-mechanical (`wave-1/wave-1-scout-02-extension-workflow.md:21`).

## 5. Wave 2 Claim Families

### 5.1 Adjudicator A — Topology / Runtime

Minimum claim families:

1. Vendored modified Pi fork: correct phrasing and boundaries.
2. ADR-010 clean seam: proposed-not-implemented, plus whether partial seams exist elsewhere.
3. MCP/RPC/headless topology: in-process MCP vs standalone MCP vs RPC/headless/daemon surfaces.
4. RTK docs/source divergence: provisioning vs activation.
5. Headless exit-code docs/source mismatch.
6. Whether `daemon`, `web`, `studio`, and VS Code extension are peripheral or relevant runtime surfaces.

### 5.2 Adjudicator B — Extension / Workflow

Minimum claim families:

1. Whether all identified mechanisms should be called extension surfaces.
2. Pi coding-agent extensions vs GSD ecosystem extensions.
3. Workflow plugins vs skills vs hooks as distinct surfaces.
4. `markdown-phase` prompt-dispatch limitations.
5. `yaml-step` deterministic claims, including which layers are deterministic.
6. Hook/trust/security composition.
7. Claude Code CLI provider/permission behavior as workflow automation surface.

### 5.3 Adjudicator C — Release / Practice

Minimum claim families:

1. Machinery-vs-practice: stable pattern vs transition state.
2. Whether visible removals lacked meaningful deprecation.
3. Whether absent `BREAKING CHANGE` markers imply convention-enforcement gap.
4. Whether rapid cadence materially increases fork/extension maintenance risk.
5. Whether bundled release/hotfix/API-breaking templates reflect actual project practice.
6. Whether release mechanics and product workflow are tightly interleaved enough to shape uplift design.
7. Experimental deprecation waiver and relevance to uplift-dependent surfaces.

## 6. Conditions For Wave 2

Wave 2 should proceed under these conditions:

1. **Use high reasoning, not xhigh.** The adjudication tasks are bounded but interpretive.
2. **Do not ask adjudicators to construct a full replacement model.** They adjudicate selected claims.
3. **Each adjudicator should cite source lines and current audit artifacts.**
4. **Each adjudicator should classify verdicts as survives / survives with qualification / unsupported / wrong / not decidable from inspected evidence.**
5. **Adjudicator C must preserve shallow-history caveats unless additional history is explicitly gathered.**
6. **Any network-dependent or history-deepening work should be explicit, scoped, and justified.**
7. **If two or more domains find materially wrong load-bearing synthesis claims, Gate 2 should consider constructive-remap trigger.**

## 7. Next Step

Write Wave 2 adjudicator specs in `wave-2/`, using this disposition's claim families and conditions. After the specs are written, dispatch the three high-reasoning adjudicators.
