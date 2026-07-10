# BKL-010 Repository Discovery Report v1

**Date:** 2026-07-10
**Program:** GM-005 Repository Refinement
**Phase:** Discovery (BKL-010)
**Location:** `GM-005/BKL-010/discovery/BKL-010_REPOSITORY_DISCOVERY_REPORT_v1.md`

---

## 1. Verified Repository Evidence

A fresh repository-wide inspection has been performed to evaluate the current state of the repository post BKL-009.

**A. Repository Structure (Root Level)**
*   The `docs/` hierarchy is now perfectly aligned with the 6-pillar Golden Master constitution.
*   However, the repository root (`/`) is currently cluttered with 10 legacy milestone reports and artifacts:
    *   `docs/governance/BKL-006_CHIEF_ARCHITECT_DECISION_REGISTER.md`
    *   `docs/status/BKL-007_ARCHITECTURAL_REFINEMENT_PLAN_v1.md`
    *   `docs/status/BKL-007_ARCHITECTURE_EVIDENCE_REPORT_v1.md`
    *   `docs/status/BKL-007_CONSTITUTIONAL_VALIDATION_REVIEW_v1.md`
    *   `docs/status/BKL-007_REPOSITORY_DISCOVERY_REPORT_v1.md`
    *   `docs/status/BKL-008_DISCOVERY_RECONCILIATION_REPORT_v1.md`
    *   `docs/status/BKL-008_REPOSITORY_DISCOVERY_REPORT_v1.md`
    *   `docs/status/LEGACY_MODULE_REMOVAL_EXECUTION_REPORT_v1.md`
    *   `docs/archive/PHASE14F_QUESTION_REGISTRY_DIFF.txt`
    *   `docs/archive/PHASE14F_REGISTRY_DATA_DIFF.txt`

**B. Source Tree Organization (Backend)**
*   The `backend/` root directory contains an accumulation of temporary scratch files, validation artifacts, and utility scripts mixed with core application files:
    *   **Scratch Data:** `av_tables.txt`, `av_tables2.txt`, `validation_check.txt`
    *   **Utility/Debug Scripts:** `inspect_av.py`, `run_validation.py`, `search_astakavarga.py`, `test_output_script.py`, `test_output_script2.py`, `trace_chart.py`
    *   **Core Execution:** `main.py`, `run.py` (ambiguous entry points).

**C. Source Tree Organization (Frontend)**
*   The `frontend/` directory is clean, structurally sound, and adheres to standard Vite/React project boundaries.

---

## 2. Architectural Observations

1.  **Golden Master Root Contamination:** The Golden Master constitution dictates a pristine repository root. Temporary execution reports and historical diffs should not reside alongside `docker-compose.yml`, `pytest.ini`, and core source directories. This violates repository navigation and maintainability principles.
2.  **Backend Boundary Blurring:** The presence of ad-hoc `.txt` dumps and `test_output_*.py` scripts in the `backend/` root degrades AI retrieval efficiency and creates architectural ambiguity. Utility scripts should be isolated from production application code.
3.  **Documentation Architecture Alignment:** Since BKL-009 successfully consolidated the documentation taxonomy, a clear constitutional path now exists for archiving the root-level BKL reports into `docs/status/` or `docs/archive/`.

---

## 3. Prioritized Backlog Proposal for BKL-010

Based on the evidence, the next highest-value refinement opportunity is **Root Level & Backend Structural Cleanup**. 

### BKL-010-1: Root Documentation & Artifact Archiving (Highest Priority)
*   **Objective:** Relocate all root-level BKL execution reports, plans, and legacy text diffs into the `docs/` architecture.
*   **Repository Evidence:** 10 orphaned reports/text files currently sit in the repository root.
*   **Expected Benefit:** Restores the repository root to a pristine state, improving navigation and strictly enforcing the rule that documentation belongs only in `docs/`.
*   **Estimated Complexity:** Low. (Strictly file migrations and reference updates).
*   **Risk:** Zero. (No code modifications).
*   **Why Prioritize:** The repository root is the first entry point for AI context parsing. Eliminating noise here provides the highest immediate ROI for repository health.

### BKL-010-2: Backend Scratch & Utility Isolation (Secondary Priority)
*   **Objective:** Isolate non-production scripts and text dumps in the `backend/` directory into dedicated `backend/scripts/` and `backend/scratch/` (or `backend/debug/`) directories.
*   **Repository Evidence:** 9 unmanaged scratch/debug files cluttering the `backend/` root.
*   **Expected Benefit:** Defines a strict boundary between production Python code and historical diagnostic utilities.
*   **Estimated Complexity:** Low to Medium. (May require updating internal paths within the debug scripts if they are still actively used).
*   **Risk:** Low. (These are utility scripts, not the main API).
*   **Why Prioritize:** Resolves architectural ambiguity in the backend root without requiring a full code refactor.

### Final Recommendation
I recommend **BKL-010-1: Root Documentation & Artifact Archiving** as the immediate focus for BKL-010, followed sequentially by **BKL-010-2**. This continues the trajectory of structural refinement established in BKL-008 and BKL-009.
