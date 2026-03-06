# Phase 1: Deep System Audit - Context

**Gathered:** 2026-03-05
**Status:** Ready for planning
**Source:** Formalized from orchestrator analysis and conversation deliberations

<domain>
## Phase Boundary

Comprehensive diagnostic audit of Dionysus system state across all domains: storage, processes/services, security posture, GPU/CUDA, project ecosystem, network/access, toolchain, and consolidated system map. This phase PRODUCES knowledge — it is the research. Read-only; no changes to the system.

Phase 3 (Critical Stabilization) will ACT on these findings. Phase 2 (Tool & Strategy Research) will use them as ground truth for tool evaluations.

</domain>

<decisions>
## Implementation Decisions

### Output Structure
- Separate per-domain audit files for parallel execution, PLUS a consolidated system map (AUD-08)
- Each domain file: structured markdown with tables for machine readability
- File naming: `{domain}-audit.md` in `.planning/research/` (e.g., `storage-audit.md`, `security-audit.md`)
- Consolidated system map at `.planning/research/system-audit.md` per requirements
- Include both human-readable prose AND structured tables/lists that downstream phases can grep/parse

### Audit Depth & Priority
- All 8 domains get covered, but weight heavier on known pain points:
  - **High priority:** Storage (~/.cache 67GB), Security (0.0.0.0 bindings, credentials), Process/service inventory
  - **Standard priority:** Project ecosystem, Network/access, Toolchain
  - **Lighter touch:** GPU/CUDA (document state, not deep analysis — becomes relevant in Phase 6)
- Existing audit scripts (`audit-workspace.sh`, `audit-home.sh`) should be leveraged, not duplicated

### Handling Actionable Findings
- Document only — do NOT fix anything during the audit
- Flag severity levels: CRITICAL (security risk), HIGH (blocking Phase 3), MEDIUM (should fix), LOW (nice to fix)
- Each finding gets a remediation note pointing to which phase addresses it
- "Fix it now" temptation must be resisted — the audit produces the map, Phase 3 follows the map

### Research Verification
- Cross-reference against synthesis.md and critical-audit.md where claims are testable from system state
- Don't exhaustively verify every claim — focus on claims that affect Phases 3-4 decisions
- Note discrepancies between theoretical research and actual system state
- Verification criteria from critical-audit.md should be checked where possible without external tool testing (that's Phase 2)

### Parallel Execution Strategy
- Independent audit domains run as parallel subagents (per roadmap)
- Domains with zero dependencies on each other: storage, processes, security, GPU, projects, network, toolchain
- Consolidated system map (AUD-08) runs AFTER all domain audits complete — it synthesizes findings

### Claude's Discretion
- Exact command sequences for gathering system information
- Level of detail in per-domain reports beyond the minimum specified in requirements
- How to handle edge cases (e.g., unreadable directories, permission-denied areas without sudo)
- Organization of the consolidated system map sections

</decisions>

<specifics>
## Specific Ideas

- The existing `audit-workspace.sh` and `audit-home.sh` scripts already run weekly via cron — their output should be incorporated or referenced, not re-implemented
- The `.planning/research/critical-audit.md` contains verification criteria organized by tool/claim — the audit should check system-state-verifiable criteria from this document
- The `.planning/research/synthesis.md` contains theoretical claims about the tool landscape — the audit grounds these in reality
- ~/scripts/ contains ~20 scripts from prior setup attempts — the audit should inventory these as part of the toolchain domain
- Known issues from PROJECT.md should each be verified: ~/.cache 67GB, broken HWE kernel, Docker data-root, VNC binding, Nginx default, VS Code servers, SyncThing peers

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `~/scripts/audit-workspace.sh`: Git status report for all projects — covers most of AUD-05
- `~/scripts/audit-home.sh`: Home directory conventions, disk usage, cache size, symlinks, .env permissions — covers parts of AUD-01, AUD-03
- `~/docs/workspace-audit.md` and `~/docs/home-audit.md`: Weekly auto-generated reports from above scripts

### Established Patterns
- Audit scripts output structured markdown tables — follow this pattern for consistency
- Cron-based weekly audits already exist — this phase does a deep one-time audit, not replacing the recurring ones

### Integration Points
- Audit findings feed directly into Phase 3 (Critical Stabilization) planning
- Audit findings validate/challenge `.planning/research/synthesis.md` and `critical-audit.md`
- Consolidated system map becomes the single source of truth referenced by all subsequent phases

</code_context>

<deferred>
## Deferred Ideas

- Automated monitoring/alerting based on audit findings — future capability
- Continuous audit pipeline (beyond weekly cron) — evaluate need after Phase 3
- Deep GPU benchmarking — Phase 6 scope

</deferred>

---

*Phase: 01-emergency-security-hardening*
*Context gathered: 2026-03-05*
