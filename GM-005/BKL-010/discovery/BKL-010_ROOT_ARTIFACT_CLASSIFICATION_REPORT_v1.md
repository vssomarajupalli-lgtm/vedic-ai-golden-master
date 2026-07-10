# BKL-010 Root Artifact Classification Report v1

**Date:** 2026-07-10
**Program:** GM-005 Repository Refinement
**Phase:** Discovery - Artifact Classification
**Location:** `GM-005/BKL-010/discovery/BKL-010_ROOT_ARTIFACT_CLASSIFICATION_REPORT_v1.md`

---

## 1. Classification Summary

The repository root currently contains 10 non-orchestration artifacts. These files are point-in-time reports, temporary diffs, or legacy governance logs that violate the Golden Master documentation architecture which mandates all documentation be housed within `docs/`.

*   **Total Files Evaluated:** 10
*   **Must Remain in Root:** 0
*   **Safe to Relocate:** 10
*   **Requiring Architecture Review:** 0

---

## 2. Artifact Classification Table

| File Name | Purpose | Origin | Usage Status | Recommended Location | Justification | Risk | Update Refs? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docs/governance/BKL-006_CHIEF_ARCHITECT_DECISION_REGISTER.md` | Record of architectural directives | BKL-006 | Active / Historical | `docs/governance` | Core governance file dictating rules, but belongs in the governance pillar, not root. | Low | Yes |
| `docs/status/BKL-007_ARCHITECTURAL_REFINEMENT_PLAN_v1.md` | Milestone execution plan | BKL-007 | Historical | `docs/status` | Point-in-time milestone plan. Belongs with milestone status files. | None | No |
| `docs/status/BKL-007_ARCHITECTURE_EVIDENCE_REPORT_v1.md` | Milestone discovery output | BKL-007 | Historical | `docs/status` | Milestone artifact detailing findings. | None | No |
| `docs/status/BKL-007_CONSTITUTIONAL_VALIDATION_REVIEW_v1.md` | Milestone validation output | BKL-007 | Historical | `docs/status` | Post-execution validation report for BKL-007. | None | No |
| `docs/status/BKL-007_REPOSITORY_DISCOVERY_REPORT_v1.md` | Milestone discovery output | BKL-007 | Historical | `docs/status` | Initial repository evaluation for BKL-007. | None | No |
| `docs/status/BKL-008_DISCOVERY_RECONCILIATION_REPORT_v1.md` | Milestone discovery output | BKL-008 | Historical | `docs/status` | Consolidation of BKL-008 findings. | None | No |
| `docs/status/BKL-008_REPOSITORY_DISCOVERY_REPORT_v1.md` | Milestone discovery output | BKL-008 | Historical | `docs/status` | Initial evaluation for BKL-008 legacy module cleanup. | None | No |
| `docs/status/LEGACY_MODULE_REMOVAL_EXECUTION_REPORT_v1.md` | Execution log for PDF module | BKL-008 | Historical | `docs/status` | Execution artifact documenting a codebase deletion. | None | No |
| `docs/archive/PHASE14F_QUESTION_REGISTRY_DIFF.txt` | Raw text diff dump | Phase 14 | Obsolete | `docs/archive` | Purely historical raw data dump from a past phase migration. | None | No |
| `docs/archive/PHASE14F_REGISTRY_DATA_DIFF.txt` | Raw text diff dump | Phase 14 | Obsolete | `docs/archive` | Purely historical raw data dump. | None | No |

---

## 3. Relocation Analysis

### Files That Must Remain in the Root
*   **None.** (All standard orchestration files such as `docker-compose.yml`, `pytest.ini`, `README.md`, and `.gitignore` were excluded from this classification as they are legitimate root residents).

### Files That Are Safe to Relocate
*   **All 10 files.** They have zero functional/runtime dependencies. Their presence in the root is purely the result of incomplete cleanup during past execution cycles. 

### Files Requiring Further Architectural Review
*   **None.** The documentation constitution (established in BKL-009) provides completely unambiguous target destinations for all of these artifacts.

---
**Status:** Classification Complete. Awaiting Architecture Advisor review before any file relocation implementation.
