# BKL-007 REPOSITORY DISCOVERY REPORT v1

**Date:** 2026-07-09
**Phase:** GM-005 Repository Refinement
**Status:** Discovery Complete

---

## 1. Executive Summary

*   **Overall repository health:** Structurally fragmented but consolidating. The repository shows distinct isolation between legacy documentation (`docs/archive/`), active documentation (`docs/`), backend engine (`backend/`), and frontend application (`frontend/`).
*   **Readiness for refinement:** The repository is primed for structural refinement. The successful completion of BKL-006 cleared 60 zero-dependency artifacts, reducing immediate noise.
*   **High-level observations:** 
    * Significant duplication exists (e.g., `GOLDEN_MASTER_MANIFEST.md` exists in root and `docs/governance/`).
    * Large volume of documentation (366 markdown files).
    * High ratio of files containing legacy/placeholder markers (107 files identified with TODO/FIXME/Legacy keywords).

## 2. Repository Inventory

*   **Complete folder structure (Top-level distribution):**
    *   `root`: 136 files
    *   `backend`: 128 files
    *   `frontend`: 45 files
    *   `docs`: 238 files
*   **Major modules:** Backend (Python FastAPI), Frontend (React/Vite).
*   **Documentation inventory:** 366 markdown documents globally.
*   **Configuration files:** 18 configuration files (YAML, JSON, TOML, Dockerfiles).
*   **Test suites:** 44 test/spec files identified.
*   **Scripts and utilities:** 4 executable scripts identified.

## 3. Legacy Inventory

*   **Legacy files & Deprecated components:** 60 legacy execution reports successfully archived under `docs/archive/bkl-006_legacy/`. 36 constitutional artifacts deferred under CP-002.
*   **Placeholder implementations:** 107 files contain legacy, deprecated, TODO, FIXME, or placeholder terminology in source code.
*   **Duplicate files:** 20 duplicate filenames detected across distinct paths (e.g., `GOLDEN_MASTER_MANIFEST.md` in root and docs).
*   **Archived content:** Centralized under `docs/archive/`.
*   **Dead or unused code:** Discovery phase identifies potential dead code based on legacy text markers. Explicit structural dependency mapping required for active engines.

## 4. Architecture Inventory

*   **Module ownership:** Strict separation between engine (`backend/`) and presentation (`frontend/`).
*   **Dependency flow:** Frontend acts as consumer of Backend APIs. Docs govern architecture via ADRs.
*   **Pipeline integrity:** Orchestration configurations (e.g., Dockerfiles) exist independently in both backend and frontend.
*   **Engine boundaries:** Backend encapsulates astrological formulas and calculation logic. 
*   **Configuration ownership:** Duplicated across boundaries.
*   **Cross-module relationships:** Tightly coupled via explicit API contracts (implied, structurally separate).

## 5. Governance Inventory

*   **Documentation consistency:** Structurally fragmented. Root contains numerous loose governance files alongside `docs/` hierarchy.
*   **Naming conventions:** Mixed. Some documents use `ALL_CAPS_SNAKE_CASE` (e.g., `docs/architecture/ADR_INVENTORY_v1.0.md`), others use standard capitalization (e.g., `README.md`).
*   **Decision Register references:** The BKL-006 Chief Architect Decision Register is correctly established as the canonical source for archive decisions.
*   **Architecture document alignment:** ADRs are localized in `docs/architecture/decisions/`.
*   **Constitutional compliance observations:** The presence of `GOLDEN_MASTER_MANIFEST.md` in both root and `docs/governance/` represents a severe constitutional ambiguity.

## 6. Risk Inventory

*   **Critical:** 
    *   *Ambiguous Source of Truth:* `GOLDEN_MASTER_MANIFEST.md` duplication between root and governance directory. (Evidence: File duplication scan).
*   **High:** 
    *   *Root Clutter:* Substantial number of active documents (136 files) reside in the repository root, risking accidental modification or architectural confusion.
*   **Medium:** 
    *   *Placeholder Accumulation:* 107 files contain TODO/FIXME markers indicating unresolved technical debt.
*   **Low:** 
    *   *Redundant Scripts:* Presence of `scratch_*.py` files in root from mechanical Scribe operations.

## 7. Refinement Opportunities

*   Consolidate root-level governance documents into the `docs/governance/` hierarchy.
*   Resolve `GOLDEN_MASTER_MANIFEST.md` duplication.
*   Establish a centralized configuration registry.
*   Clean up temporary `scratch_*.py` files generated during execution.
*   Standardize documentation naming conventions across the `docs/` tree.

## 8. Overall Assessment

**Ready for BKL-007 Architecture Review:** YES. 

The repository evidence clearly establishes the structural baseline. The existence of fragmented governance files and explicit duplication issues provides immediate actionable intelligence for the upcoming refinement phases. No assumptions were made; all observations are backed by programmatic repository scans.
