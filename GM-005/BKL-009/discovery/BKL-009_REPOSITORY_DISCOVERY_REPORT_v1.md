# BKL-009 Repository Discovery Report v1

**Date:** 2026-07-10
**Program:** GM-005 Repository Refinement
**Phase:** Repository Discovery (BKL-009)

---

## 1. Executive Summary

This report outlines the structural state of the Samartha Vedic AI Golden Master repository following the completion of BKL-008. While previous milestones successfully eradicated isolated dead code (Legacy PDF Pipeline) and consolidated foundational governance (`GOLDEN_MASTER_MANIFEST.md`), the current discovery reveals severe fragmentation within the repository's documentation taxonomy. The documentation-to-code ratio is highly unbalanced (369 Markdown files vs. 111 Python files), and overlapping domains drastically impair AI retrieval efficiency. The highest-value opportunity for BKL-009 is a comprehensive documentation taxonomy consolidation.

## 2. Verified Repository Facts

*   **Documentation Volume:** The repository contains 369 Markdown (`.md`) files. In contrast, the operational backend contains 111 Python (`.py`) files.
*   **Documentation Sprawl:** The `docs/` root contains 17 top-level subdirectories, many of which are semantically identical or deeply fragmented:
    *   **Status Domain:** Spread across `docs/status` (66 files), `docs/current_status` (13 files), and `docs/current` (4 files).
    *   **Archive Domain:** Spread across `docs/archive` (13 files, plus 60 in `docs/archive/bkl-006_legacy`), `docs/handover` (13 files), and `docs/project_handover` (11 files).
    *   **Knowledge Domain:** Spread across `docs/knowledge` (18 files) and `docs/reference` (9 files).
*   **Timestamped Nomenclature:** Directories like `docs/engineering/question_engine` contain 14 files heavily utilizing timestamped snapshot naming conventions (e.g., `ANSWER_COMPOSER_DESIGN_2026-06-19_1130.md`), rather than living canonical names.
*   **Redundant Pathing:** An extraneous nested directory exists at `docs/docs/samartha_v2`, compounding traversal depth.

## 3. Architectural Observations

*   **AI Retrieval Efficiency (Critical Impact):** The current taxonomy is hostile to Retrieval-Augmented Generation (RAG) and Agentic context gathering. An AI agent attempting to retrieve the "current project status" or "system architecture" will ingest massive amounts of duplicate, deprecated, or superseded context due to the overlapping folder domains (`status` vs `current_status`, or snapshot timestamped files).
*   **Governance Structure:** The `docs/governance/` folder is well-utilized (25 files) but lacks strict boundaries separating structural rules from phase-specific transition logs.
*   **Architecture Consistency:** `docs/architecture` is robust (32 files) and appropriately isolates its `decisions/` (ADR) registry (16 files). However, overlapping folders like `docs/engineering/implementation` and `docs/engineering/validation` dilute the centralized architectural truth.
*   **Repository Navigation:** The flat proliferation of 17 top-level `docs/` folders creates high cognitive load for human engineers and automated agents alike.
*   **Technical Debt (Documentation):** Snapshotting (saving daily state as uniquely named files instead of relying on Git history) has created an unsustainable maintenance burden.

## 4. Recommendations

### Priority 1: Execute Documentation Taxonomy Consolidation
Consolidate the fragmented domains into a strict, unified hierarchy.
*   **Merge Status:** Consolidate `docs/current_status` and `docs/current` strictly into `docs/status`. Purge or archive historical status snapshots.
*   **Merge Archives:** Relocate `docs/handover` and `docs/project_handover` entirely into `docs/archive/`.
*   **Merge Knowledge:** Consolidate `docs/reference` into `docs/knowledge/`.
*   **Flatten Redundancy:** Eliminate the nested `docs/docs/samartha_v2` path.

### Priority 2: Eradicate Snapshot Nomenclature
Enforce a "Living Document" architecture. Rename timestamped files (e.g., `*_2026-06-19_1130.md`) to canonical, timeless names (e.g., `QUESTION_ENGINE_ARCHITECTURE.md`). Historical states are the responsibility of the Git commit tree, not the filesystem taxonomy.

### Priority 3: Establish Strict Folder Boundaries
Define exactly 4-5 canonical documentation folders (e.g., `architecture`, `governance`, `engineering`, `status`, `archive`) and forbid the creation of ad-hoc root-level `docs/` subdirectories during future phases.

## 5. Readiness Assessment

**Status: READY FOR ARCHITECTURE ADVISOR REVIEW**

This discovery phase (BKL-009) was completed using exclusively non-destructive repository scanning. No files were modified. The findings unequivocally point to documentation taxonomy consolidation as the most critical structural refinement remaining. Awaiting review and approval to proceed with the BKL-009 structural reconciliation.
