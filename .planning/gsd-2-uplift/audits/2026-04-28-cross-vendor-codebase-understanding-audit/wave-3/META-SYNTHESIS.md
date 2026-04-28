---
type: wave-3-meta-synthesis
date: 2026-04-28
reasoning_effort: high
status: complete
source_commit: bf1d8aad0
---

# Wave 3 Meta-Synthesis — Cross-Vendor Codebase-Understanding Audit

## 0. Executive Conclusion

Conclusion label: **usable with addenda**.

The Claude-led investigation remains usable overall as an incubation input. Wave 2 did not find structural unreliability, a blocker, or multiple wrong load-bearing claims across domains; Gate 2 classified the result as localized qualifications and instructed this synthesis to preserve boundary corrections rather than discard the investigation (`GATE-2-DISPOSITION.md:14-19`, `GATE-2-DISPOSITION.md:78-89`).

The investigation is strongest as codebase understanding: it correctly located the vendored Pi substrate, ADR-010 clean-seam status, plural runtime surfaces, extension/workflow plurality, markdown-phase vs yaml-step split, and release/breaking-change machinery. Its weaker layer is strategic interpretation: R-strategy viability, extension-surface meaning, release-practice durability, and incubation posture require the addenda below.

Constructive remap decision: **conditionally deferred, not triggered now**. No constructive remap is needed before incubation can use this work, but a remap or narrower second-wave probe should be triggered if downstream scoping tries to rely on complete-history release culture, uniform extension-surface viability, or full source-surface stability without the follow-up evidence listed in §6.

## 1. What Survives

The core source-topology findings survive substantially.

- The specific ADR-010 clean-seam claim survives: ADR-010's proposed `gsd-agent-core` / `gsd-agent-modes` package seam is proposed-not-implemented, and the current package tree lacks those packages. The original synthesis put this at F1 and §1.1 (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:33-34`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:83-88`), Scout 01 mechanically confirmed it (`wave-1/wave-1-scout-01-topology-runtime.md:108-110`), and Wave 2 retained the claim at high confidence (`wave-2/wave-2-adjudication-01-topology-runtime.md:41-50`).
- The basic Pi-vendoring claim survives: gsd-2 is built around vendored Pi-derived packages with GSD modifications. Scout 01 confirmed package descriptions and ADR-010 evidence (`wave-1/wave-1-scout-01-topology-runtime.md:91-97`, `wave-1/wave-1-scout-01-topology-runtime.md:108-115`), and Wave 2 found the shorthand acceptable when bounded (`wave-2/wave-2-adjudication-01-topology-runtime.md:30-40`).
- The plural runtime-surface claim survives: CLI/TUI, headless/RPC, in-process MCP, standalone MCP, RPC client, and adjacent integration surfaces are real. The original synthesis stated a plural agent-runtime contract (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:47-48`), Scout 01 mapped the surfaces (`wave-1/wave-1-scout-01-topology-runtime.md:80-90`), and Wave 2 confirmed the topology with current `gsd auto` freshness preserved (`wave-2/wave-2-adjudication-01-topology-runtime.md:52-62`).
- The workflow-engine split survives: `markdown-phase` is prompt-dispatch with startup scaffolding, while `yaml-step` has deterministic graph/control/verification layers. The synthesis stated this as F4 and §1.2 (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:39-40`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:90-97`), Scout 02 confirmed the mechanical distinction (`wave-1/wave-1-scout-02-extension-workflow.md:63-73`, `wave-1/wave-1-scout-02-extension-workflow.md:101-103`), and Wave 2 retained it (`wave-2/wave-2-adjudication-02-extension-workflow.md:66-86`).
- The existence of substantial release and breaking-change machinery survives: package scripts, release workflows, changelog scripts, PR/contribution policy, templates, and experimental deprecation-waiver text are real. Scout 03 inventoried that machinery (`wave-1/wave-1-scout-03-release-practice.md:57-79`), and Wave 2 found the machinery strong even while qualifying practice conclusions (`wave-2/wave-2-adjudication-03-release-practice.md:31-40`).
- The incubation-level claim that additional first-wave exploration is not required before deliberation survives with discipline. The original synthesis said incubation can operate cleanly with explicit disposition discipline (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:566-576`), and Gate 2 independently reached "localized qualifications" rather than remap or blocker (`GATE-2-DISPOSITION.md:14-19`, `GATE-2-DISPOSITION.md:78-89`).

## 2. What Survives Only With Qualification

The following claims remain usable only with the Wave 2 qualifications carried forward.

1. **Topology/runtime boundary discipline.** "Vendored modified Pi fork" is usable only as shorthand for the Pi-derived substrate, not as the whole-system topology. Carry forward Wave 2's exact replacement: "gsd-2 is a GSD CLI/application layer built around vendored, modified Pi-derived packages; the Pi substrate is fork-like and entangled, but the whole repo is broader than that fork" (`wave-2/wave-2-adjudication-01-topology-runtime.md:30-40`). Also preserve: ADR-010's clean package seam is absent, while informal runtime and extension seams exist but do not solve ADR-010's provenance/entanglement problem (`wave-2/wave-2-adjudication-01-topology-runtime.md:41-50`).
2. **Runtime-surface distinctness.** Keep in-process MCP mode, standalone `@gsd-build/mcp-server`, RPC/headless orchestration, daemon/web/VS Code, and TTY-gated `gsd auto` separate. Wave 2's exact carry-forward labels are "in-process MCP mode (`gsd --mode mcp`)", "standalone `@gsd-build/mcp-server` orchestration server", and "RPC/headless orchestration (`--mode rpc`, `@gsd-build/rpc-client`, `gsd headless`)" (`wave-2/wave-2-adjudication-01-topology-runtime.md:52-62`). The source freshness delta specifically corrected `gsd auto` to a TTY-gated redirect, not unconditional headless shorthand (`wave-1/SOURCE-FRESHNESS-DELTA-2026-04-28.md:75-81`).
3. **Typed extension-surface vocabulary.** The synthesis's "four extension surfaces" claim survives only if "extension surface" is immediately typed. Wave 2 says to replace bare usage with "code extension API, GSD ecosystem extension, workflow plugin, skill/instruction resource, hook/rule interception layer, provider integration, and workflow MCP/machine surface where applicable" (`wave-2/wave-2-adjudication-02-extension-workflow.md:33-42`). Mechanism existence does not itself decide R2/R4/R5 meaning.
4. **Pi extensions vs GSD ecosystem extensions.** They are source-distinct, but the relationship is "parallel project-local loader plus GSD wrapper over Pi API," not fully independent subsystem and not simple alias (`wave-2/wave-2-adjudication-02-extension-workflow.md:44-53`).
5. **Markdown-phase vs yaml-step determinism limits.** `markdown-phase` is viable for agent-prompted procedural workflows, not executor-owned deterministic shell/action ownership (`wave-2/wave-2-adjudication-02-extension-workflow.md:66-75`). `yaml-step` determinism applies to graph mutation, dependency eligibility, context injection, and verification policy execution; prompt-authored step content remains agent-mediated (`wave-2/wave-2-adjudication-02-extension-workflow.md:77-86`).
6. **Trust/security is cross-cutting, not uniform.** Trust boundaries exist at extension, workflow, hook/rule, verification, and provider-permission layers; securing one layer does not secure the others (`wave-2/wave-2-adjudication-02-extension-workflow.md:88-108`).
7. **Shallow-history bounds on release/practice claims.** The machinery-vs-practice pattern is visible-window-bounded, not a complete-history or culture claim. Scout 03 established the shallow clone caveat (`wave-1/wave-1-scout-03-release-practice.md:48-55`), and Wave 2 says to state "visible-window machinery/practice divergence" rather than stable practice divergence or culture (`wave-2/wave-2-adjudication-03-release-practice.md:31-40`).
8. **Removal/deprecation and marker claims.** OAuth and `/gsd map-codebase` examples support "no visible local pre-deprecation found," not "no meaningful deprecation existed anywhere" (`wave-2/wave-2-adjudication-03-release-practice.md:42-51`). Absent `BREAKING CHANGE` markers support a marker-usage gap in inspected visible history, not a proven enforcement or culture gap (`wave-2/wave-2-adjudication-03-release-practice.md:53-62`).
9. **Release templates vs maintainer practice.** Bundled release/hotfix/API-breaking templates are capability and doctrine evidence, not proof that gsd-2 maintainers use those templates for gsd-2 releases (`wave-2/wave-2-adjudication-03-release-practice.md:75-84`).
10. **Mechanism existence vs R-strategy viability.** The original synthesis's R2 viability claim survives only as "viable in some shape," not as uniform extension viability. The original synthesis already contained both supporting and challenging evidence (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:173-186`); Wave 2 sharpens the rule that R-strategy meaning must be assigned after typed mechanism analysis, not inferred from extension/mechanism existence (`wave-2/wave-2-adjudication-02-extension-workflow.md:33-42`, `GATE-2-DISPOSITION.md:103-109`).

## 3. What Fails Or Is Unsupported

No direct load-bearing original synthesis claim was found plainly wrong by this audit.

Several stronger readings are unsupported and should not be used:

- Do not use "gsd-2 is a Pi fork" as a whole-repo topology claim; it erases GSD root/application, bundled extension, standalone integration, and app surfaces (`wave-2/wave-2-adjudication-01-topology-runtime.md:30-40`, `wave-2/wave-2-adjudication-01-topology-runtime.md:85-94`).
- Do not claim there are no seams of any kind. The correct claim is that ADR-010's clean package seam is absent; informal seams exist (`wave-2/wave-2-adjudication-01-topology-runtime.md:41-50`).
- Do not treat all extension-adjacent mechanisms as same-kind extension surfaces or as one security/trust model (`wave-2/wave-2-adjudication-02-extension-workflow.md:33-42`, `wave-2/wave-2-adjudication-02-extension-workflow.md:88-97`).
- Do not claim `markdown-phase` owns deterministic shell execution or programmatic phase advancement from inspected evidence (`wave-2/wave-2-adjudication-02-extension-workflow.md:66-75`).
- Do not upgrade shallow local history into complete release-history, maintainer-culture, or all-user-facing deprecation conclusions (`wave-2/wave-2-adjudication-03-release-practice.md:31-40`, `wave-2/wave-2-adjudication-03-release-practice.md:42-62`).
- Do not treat rapid cadence alone as decisive fork/extension risk; it is a pressure requiring surface-churn and diff sampling (`wave-2/wave-2-adjudication-03-release-practice.md:64-73`).
- Do not treat bundled workflow templates as evidence of actual gsd-2 maintainer release practice without Actions logs, `.gsd/workflows/` artifacts, PRs, or maintainer docs (`wave-2/wave-2-adjudication-03-release-practice.md:75-84`).

## 4. Trust Impact

Trust in the original investigation's **codebase understanding** increases modestly. Cross-vendor scouts and high adjudicators mostly ratified the source map: the original synthesis's top-line technical claims were not refuted, and all three Wave 2 adjudicators recommended localized qualifications rather than structural unreliability (`GATE-2-DISPOSITION.md:22-29`).

Trust in the original investigation's **strategic interpretation** should remain bounded. The synthesis itself acknowledged high-uncertainty interpretive claims at load-bearing positions and called for paired/cross-vendor synthesis (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:63-75`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:578-595`). Wave 2 confirms that the risky layer is not source discovery but interpretation: R2/R3/R4/R5 viability, release-practice durability, and subsystem-to-uplift-act mapping.

Net trust change: use the Claude-led work as a strong map of candidate surfaces and tensions, but not as a final decision record. Incubation can rely on it to know what to discuss; it should not let any single shorthand become the decision.

## 5. Incubation Checkpoint Implications

Incubation can safely carry forward:

- gsd-2 is a substantive substrate, not architecturally hostile to uplift (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:566-576`).
- R2 remains viable in some shape, but only after typed surface selection and surface-specific stability checks (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:173-186`, `wave-2/wave-2-adjudication-02-extension-workflow.md:33-42`).
- R4 should remain explicit; headless/RPC/MCP and external orchestration surfaces are real and should not be forced into R2 vocabulary (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:202-213`, `wave-2/wave-2-adjudication-01-topology-runtime.md:52-62`).
- R5 remains named but not evaluated; competitor-landscape evidence is still needed before treating it as peer to R1-R4 (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:215-226`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:491-498`).
- The machinery-vs-practice gap is a real caution for long-horizon robustness, but incubation must decide whether the uplift goal addresses that gap or merely works within it (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:514-518`, `wave-2/wave-2-adjudication-03-release-practice.md:31-40`).

Incubation should avoid assuming:

- that a clean Pi/GSD library seam exists now;
- that "extension" names a single intervention surface;
- that `markdown-phase` can deliver deterministic execution guarantees;
- that release machinery equals stable release discipline;
- that shallow-history observations prove maintainer culture;
- that project anchoring is settled by first-wave gsd-2 evidence rather than user disposition (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:482-489`).

## 6. Follow-Up Evidence Needs

Must-have before incubation: **none**. The audit supports proceeding to incubation with the addenda above. This matches the original synthesis's "no additional first-wave exploration is necessary before incubation can operate" claim (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:566-576`) and Gate 2's localized-qualification disposition (`GATE-2-DISPOSITION.md:14-19`).

Must-have before committing second-wave scope, depending on chosen path:

- For R3-dependent design: contribution-culture evidence from PR bodies/reviews/release discussions, because the first-wave contribution-culture probe failed and R3 viability remains not first-wave-decidable (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:188-200`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:500-506`).
- For R5 as a real peer option: competitor-landscape or sibling-harness comparison evidence (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:215-226`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:491-498`).
- For R2 work touching `pi-coding-agent` internals: provenance or stable-surface mapping, because ADR-010's entanglement diagnosis remains operative (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:430-433`, `wave-2/wave-2-adjudication-01-topology-runtime.md:41-50`).
- For Context F/progressive activation commitments: a scenario probe across markdown-phase/yaml-step and external orchestration surfaces (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:435-440`, `.planning/gsd-2-uplift/exploration/SYNTHESIS.md:508-512`).
- For release-stability claims: deeper history, GitHub Releases/PR bodies, Actions logs, and representative tag-to-tag diff sampling on the exact uplift-dependent surfaces (`wave-2/wave-2-adjudication-03-release-practice.md:108-115`).
- For any experimental-gated dependency such as RTK: classify whether the chosen surface is experimental and whether the deprecation waiver applies (`wave-2/wave-2-adjudication-03-release-practice.md:97-106`).

Can defer to second-wave scoping:

- user-side adoption-pattern probe for reusability breadth (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:463-468`);
- schema-migration drift characterization (`.planning/gsd-2-uplift/exploration/SYNTHESIS.md:442-447`);
- full daemon/web/studio/VS Code topology unless chosen uplift surfaces depend on those integrations (`wave-2/wave-2-adjudication-01-topology-runtime.md:85-94`).

## 7. Constructive Remap Decision

Decision: **conditionally deferred; not triggered by this audit**.

The audit plan says constructive remap should trigger if multiple load-bearing synthesis claims are wrong or unsupported across more than one domain, if major source surfaces are absent from the original stack, if artifact vocabulary conflates distinct subsystems, if release/practice or workflow/execution evidence materially changes R-strategy viability, or if meta-synthesis concludes structural unreliability (`AUDIT-PLAN.md:313-325`).

Those conditions are not met strongly enough now. The only vocabulary-conflation risk, "extension surface," is corrected by typed vocabulary; it does not require a replacement codebase map (`wave-2/wave-2-adjudication-02-extension-workflow.md:33-42`). Release/practice and workflow evidence qualify R-strategy viability but do not reverse the incubation posture (`wave-2/wave-2-adjudication-03-release-practice.md:31-40`, `wave-2/wave-2-adjudication-02-extension-workflow.md:66-86`). Gate 2 explicitly says no adjudicator reported structural unreliability or immediate remap trigger (`GATE-2-DISPOSITION.md:22-29`).

Remap should be reconsidered only if second-wave scoping needs a complete replacement architecture model rather than the bounded surface map produced here, or if follow-up probes find the qualified claims fail in practice for chosen uplift surfaces.

## 8. Limits

This meta-synthesis is an integration artifact, not fresh codebase exploration. It did not perform broad new source reads; it relies on the required Wave 1 scout reports, source freshness delta, Wave 2 adjudications, gate dispositions, and the original Claude synthesis.

The source target was treated as read-only. `origin/main` was checked only for commit identity and matched `bf1d8aad0473809a58be4e7d7fd386ffa1581d8a`.

This synthesis does not decide the actual uplift strategy. It adjudicates whether the Claude-led investigation is safe to use for incubation, and it specifies the addenda incubation must carry forward.
