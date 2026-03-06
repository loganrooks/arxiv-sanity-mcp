---
phase: 1
slug: emergency-security-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-05
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Shell commands (file existence + content checks) |
| **Config file** | none — no test framework needed for audit/documentation phase |
| **Quick run command** | `ls .planning/research/*-audit.md 2>/dev/null \| wc -l` |
| **Full suite command** | `for f in storage process security gpu project network toolchain system; do test -f ".planning/research/${f}-audit.md" && echo "OK: ${f}-audit.md" \|\| echo "MISSING: ${f}-audit.md"; done` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Verify output file exists and contains expected sections
- **After every plan wave:** All domain files for that wave exist with non-zero findings
- **Before `/gsd:verify-work`:** Full suite — all 8 files exist, system-audit.md references all 7 domain files, severity-tagged findings present
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | AUD-01 | file+content | `test -f .planning/research/storage-audit.md && grep -c '\|' .planning/research/storage-audit.md` | W0 | pending |
| 01-02-01 | 02 | 1 | AUD-02 | file+content | `test -f .planning/research/process-audit.md && grep -c 'Severity' .planning/research/process-audit.md` | W0 | pending |
| 01-03-01 | 03 | 1 | AUD-03 | file+content | `test -f .planning/research/security-audit.md && grep -c 'CRITICAL' .planning/research/security-audit.md` | W0 | pending |
| 01-04-01 | 04 | 1 | AUD-04 | file+content | `test -f .planning/research/gpu-audit.md` | W0 | pending |
| 01-05-01 | 05 | 1 | AUD-05 | file+content | `test -f .planning/research/project-audit.md && grep -c 'workspace/projects' .planning/research/project-audit.md` | W0 | pending |
| 01-06-01 | 06 | 1 | AUD-06 | file+content | `test -f .planning/research/network-audit.md` | W0 | pending |
| 01-07-01 | 07 | 1 | AUD-07 | file+content | `test -f .planning/research/toolchain-audit.md` | W0 | pending |
| 01-08-01 | 08 | 2 | AUD-08 | file+crossref | `test -f .planning/research/system-audit.md && grep -c 'Critical Findings' .planning/research/system-audit.md` | W0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [x] `.planning/research/` directory exists — confirmed
- No test framework needed — this is a documentation/audit phase, not code
- Validation is file existence + content structure checks via shell commands

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| System map completeness | AUD-08 | Cross-domain synthesis quality is subjective | Review system-audit.md — does it reference all 7 domain audits? Are findings prioritized? |
| Verification against prior research | All | Checking claim accuracy requires judgment | Spot-check 3-5 claims from synthesis.md against audit findings |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [x] Feedback latency < 1s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
