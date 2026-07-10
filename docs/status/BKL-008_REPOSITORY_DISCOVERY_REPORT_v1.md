# BKL-008 Repository Discovery Report v1

**Date:** 2026-07-09
**Program:** GM-005 Repository Refinement
**Phase:** Repository Discovery (BKL-008)

---

## 1. Executive Summary

This report presents a fresh, objective discovery of the Samartha Vedic AI Golden Master repository state following the completion of BKL-007. The repository demonstrates improved constitutional alignment through the successful consolidation of the `GOLDEN_MASTER_MANIFEST.md` and the mechanical purge of scratch artifacts. However, significant structural clutter and legacy technical debt remain. The primary objective of BKL-008 should be the disciplined execution of the previously validated Root Directory Relocation (ARP-002) and a targeted reduction of legacy artifacts, while establishing robust testing foundations for the frontend application.

## 2. Repository Health Since BKL-007

*   **Positive Indicators:**
    *   **Constitutional Truth Consolidated:** `GOLDEN_MASTER_MANIFEST.md` now exists exclusively in `docs/governance/`. The critical ambiguity identified in BKL-007 has been successfully resolved (ARP-001 Complete).
    *   **Artifact Purge Successful:** Zero `scratch_*.py` artifacts exist in the root directory (ARP-004 Complete).
    *   **Backend Structure:** The backend maintains a clean modular structure (`app`, `tests`, `main.py`, `run.py`) and is functionally executable via deterministically structured pipelines.
*   **Negative Indicators:**
    *   **Root Clutter Persists:** The root directory continues to house non-orchestration artifacts (e.g., `BKL-006`, `BKL-007` markdown files, and `PHASE14F` diff texts), violating the success criteria of ARP-002.
    *   **Legacy Volume High:** A substantial number of files (approx. 184) remain trapped in legacy, archive, phase, and handover directories.

## 3. Remaining Repository Refinement Opportunities

*   **Root Directory Standardization:** Relocating historical phase artifacts (`BKL-*`, `PHASE14F_*`) to a designated documentation or archive folder.
*   **Frontend Testing Infrastructure:** The `frontend` application completely lacks a testing framework (no Vitest, Jest, or associated test scripts in `package.json`), representing a significant gap in CI/CD readiness.
*   **Backend Legacy Pruning:** The `backend/archive_legacy_pdf_pipeline` directory remains present in the active codebase and should be formally archived or deleted.
*   **Documentation Consolidation:** Deeply nested `docs/` subdirectories (`handover`, `project_handover`, `phase9`, `archive`, `validation`, `status`, `knowledge`, `current_status`) create a fragmented knowledge graph.

## 4. Architecture Observations

*   **Backend Modularity:** The FastAPI implementation (`backend/main.py`) and the deterministic pipeline runner (`backend/run.py`) are cleanly separated. The pipeline architecture correctly utilizes `HoroscopeSourceLoader` and `PipelineRunner`.
*   **Frontend Stack:** The frontend utilizes Vite, React 19, Tailwind CSS v4, and Zustand. It is a modern stack but lacks testing architectural components.
*   **System Orchestration:** Dockerization exists for the backend (`backend/Dockerfile`) and frontend (`frontend/Dockerfile`), and a root `docker-compose.yml` ties them together.

## 5. Governance Observations

*   **Governance Hub:** `docs/governance/` serves as a robust repository for authoritative documentation (25 files), including the consolidated `GOLDEN_MASTER_MANIFEST.md` and explicit governance locks.
*   **ADR Integrity:** `docs/architecture/decisions/` maintains a clean registry of 16 Architecture Decision Records (ADR-001 through ADR-016).
*   **Phase Logs:** BKL-006 and BKL-007 decision registers and evidence reports are currently acting as root-level governance logs rather than being appropriately filed.

## 6. Documentation Observations

*   **File Extension Bloat:** The repository contains an overwhelming 369 Markdown files compared to 111 Python files, indicating a heavy documentation-to-code ratio.
*   **Fragmentation:** The `docs/` folder contains 17 subdirectories, many of which are semantically overlapping (e.g., `archive` vs `current_status` vs `status` vs `handover`).

## 7. Technical Debt Inventory

*   **Frontend Testing Deficit:** Absence of test scripts (`npm run test`) and testing dependencies in `frontend/package.json`.
*   **Dead Code Zones:** `backend/archive_legacy_pdf_pipeline` remains in the application backend tree.
*   **Dangling Roots:** 7+ non-orchestration files remain in the root directory.

## 8. Legacy Inventory

*   **Archival Clutter:** A programmatic scan reveals 184 files spanning across paths containing `archive`, `legacy`, `handover`, or `phase`. This represents significant indexing noise for AI agents.

## 9. Repository Consistency Review

*   **Alignment with ARP-002:** The repository fails the Root Directory Clutter Relocation rule. Execution of this relocation is incomplete.
*   **Alignment with ARP-003:** The legacy audit (deferred in BKL-007) has not been executed, leaving a large footprint of deprecated artifacts.

## 10. Risks

*   **Critical:** None identified in current discovery.
*   **High:** Broken markdown hyperlinks during the inevitable Root Directory Clutter Relocation (ARP-002) if not performed with an atomic search-and-replace strategy.
*   **Medium:** Missing frontend tests reduce the reliability of iterative UI modifications.
*   **Low:** Agent context window pollution due to the massive volume of deprecated markdown files (369 total `.md` files).

## 11. Recommendations

*   **Priority 1 (High Impact, Low Effort):** Execute the Root Directory Clutter Relocation (ARP-002) for `BKL-` and `PHASE14F-` files to an appropriate documentation subfolder (e.g., `docs/project_management/` or `docs/archive/`), updating all internal links atomically.
*   **Priority 2 (High Impact, Medium Effort):** Initialize a testing framework (e.g., Vitest) in the `frontend` directory to establish a baseline for UI reliability.
*   **Priority 3 (Medium Impact, Low Effort):** Delete or permanently archive `backend/archive_legacy_pdf_pipeline`.
*   **Priority 4 (Medium Impact, High Effort):** Consolidate the 17 `docs/` subdirectories into a streamlined taxonomy (e.g., `architecture/`, `governance/`, `engineering/`, `archive/`).

## 12. Proposed Backlog Items for BKL-008

*   **BKL-008-1:** Execute Root Directory Relocation (ARP-002 completion).
*   **BKL-008-2:** Initialize Frontend Testing Infrastructure.
*   **BKL-008-3:** Deprecate/Remove Backend Legacy PDF Pipeline.
*   **BKL-008-4:** Restructure and Consolidate Documentation Taxonomy.

## 13. Readiness Assessment

**Status: READY FOR ARCHITECTURE ADVISOR REVIEW**

The Repository Discovery phase (BKL-008) has been completed exclusively through non-destructive repository scanning. No files have been modified. The repository state is well-understood, and the proposed backlog items logically follow the uncompleted mandates of BKL-007 and newly discovered technical debt. Awaiting review and approval to transition to execution.
