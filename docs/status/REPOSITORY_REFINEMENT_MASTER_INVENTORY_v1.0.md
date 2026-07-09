# REPOSITORY REFINEMENT MASTER INVENTORY

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Repository refinement must begin with a complete, accurate inventory of all existing assets. This establishes a baseline to ensure that no critical documentation, knowledge, or implementation logic is lost during the cleanup process. 

No files are deleted, renamed, or merged before being explicitly inventoried in this document. This master inventory will serve as the authoritative reference for all refinement decisions executed in Milestone GM-005.

---

## SECTION 3: Repository Inventory

The repository is structured into top-level directories and root-level files.

### 3.1 Root Directories
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `backend/` | Source Code | Contains the Python backend implementation, API, and engine logic. | Active |
| `frontend/` | Source Code | Contains the React/TypeScript frontend implementation. | Active |
| `docs/` | Documentation | Contains legacy project handover documentation. | Active |

### 3.2 Knowledge Packages
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `*_KNOWLEDGE_PACKAGE.md` | Knowledge Base | Defines the canonical rules, math, and architecture for domains (e.g., Planet, House, Dasha, Yoga, Mandali Generator). | Active |

### 3.3 Governance & Architecture
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | Governance | Defines strict ownership and data contracts for engines. | Active |
| `docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md` | Governance | Mandatory compliance checklist for future modifications. | Active |
| `docs/status/GM-004_COMPLETION_REPORT_v1.0.md` | Governance | Formal completion report for the GM-004 milestone. | Active |
| `docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` | Architecture | Overarching prediction rules. | Active |
| `GOLDEN_MASTER_MANIFEST.md` | Governance | Defines the core principles of the Golden Master repository. | Active |

### 3.4 Formula Documents
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `docs/status/FORMULA_CATEGORY_CATALOG_v1.md`, etc. | Catalog | Catalogs the astrological formulas and variants. | Active |
| `docs/status/FORMULA_LIBRARY_REVIEW_PACK.md`, etc. | Planning | Plans and reviews the formula index structures. | Active |
| `FORMULA_*_GOVERNANCE_v1.md` | Governance | Rules for managing and scaling formulas. | Active |

### 3.5 Phase Reports (Legacy/Reference)
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `PHASE8_*.md` to `PHASE16_*.md` | Audit/Report | Historical implementation reports, blueprints, and audits from prior phases. | Legacy / Reference |

### 3.6 Configuration & Tooling
| Name | Type | Purpose | Current Status |
| :--- | :--- | :--- | :--- |
| `docker-compose.yml` | Config | Docker orchestration file for local development. | Active |
| `pytest.ini` | Config | Configuration for pytest execution. | Active |

---

## SECTION 4: Classification

Major documents and components are classified as follows to guide future refinement:

* **Canonical**: 
  * `docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md`
  * `docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md`
  * `GOLDEN_MASTER_MANIFEST.md`
  * All active `KNOWLEDGE_PACKAGE` documents.
* **Supporting**: 
  * `docs/status/FORMULA_CATEGORY_CATALOG_v1.md`
  * `docs/status/QUESTION_COVERAGE_MATRIX_v1.md`
* **Reference**: 
  * `docs/status/PROGRAM_A_COMPLETION_REPORT.md`
  * Final state architecture reviews (e.g., `docs/architecture/PHASE14G_ARCHITECTURE_REVIEW.md`)
* **Legacy**: 
  * Older phase reports (`PHASE8`, `PHASE9`, `PHASE11` artifacts) that have been superseded by canonical Knowledge Packages.
* **Archive Candidate**: 
  * Highly granular implementation diffs (`PHASE14F_REGISTRY_DATA_DIFF.txt`)
  * Interim step reports and fixes (`docs/status/PHASE9_STEP1_REPORT_PROFILE_FIX.md`)
* **Future**: 
  * Planned GM-005 refinement documentation.

---

## SECTION 5: Duplicate Candidate Register

The following items are identified as potential duplication for later review. *(No deletion is recommended at this stage).*

* **Documents**: 
  * Multiple historical phase reports cover overlapping architecture (e.g., `docs/architecture/PHASE14A_ARCHITECTURE_REPORT.md` vs. Knowledge Packages).
  * `docs/status/DOCUMENTATION_INDEX_2026-06-19.md` vs. the new Master Inventory.
* **Rules & Architecture**: 
  * Formula governance rules are split across `FORMULA_GENERATION_GOVERNANCE_v1.md`, `FORMULA_REPOSITORY_GOVERNANCE_v1.md`, and `FORMULA_LIBRARY_SCALING_GOVERNANCE_v1.md`.
* **Definitions**: 
  * Question routing definitions exist in `docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` but are also scattered across various `PHASE11` and `PHASE14` implementation reports.

---

## SECTION 6: Repository Quality Assessment

* **Folder Consistency**: Moderate. A vast majority of markdown documents (over 100 files) are heavily clustered in the root directory rather than logically grouped under dedicated folders like `/docs/governance/` or `/docs/archive/`. 
* **Naming Consistency**: Moderate. Files use a mix of `_v1.md` suffixes, strict date stamps (`_2026-06-19.md`), phase prefixes, or generic naming conventions.
* **Documentation Consistency**: High for recent Golden Master governance documents; highly inconsistent for older iterative phase reports.
* **Knowledge Organization**: Strong, driven centrally by the canonical Knowledge Packages.
* **Governance Organization**: Strong, driven centrally by the GM-004 engine governance registries.
* **Implementation Organization**: Cleanly separated into `backend/` and `frontend/` source directories.

---

## SECTION 7: Refinement Readiness

The repository requires future refinement in the following areas:

1. **Root Directory Clutter**: Consolidating root-level markdown files into organized subdirectories.
2. **Naming Conventions**: Standardizing file naming conventions across all architectural, reference, and governance documents.
3. **Archival**: Safely moving historical, superseded phase reports into a dedicated `archive/` structure to reduce noise without destroying context.
4. **Consolidation**: Merging fragmented governance (e.g., formula scaling) into single, unified canonical sources.

*(Note: No refinement, renaming, merging, or deletion is performed in this document.)*

---

## SECTION 8: Out of Scope

This document explicitly does **NOT**:

* Delete files
* Rename files
* Merge documents
* Modify formulas
* Modify architecture
* Implement Version 2

---

## SECTION 9: Summary

The current repository state contains a robust, well-defined foundation of Canonical Knowledge Packages and strict Engine Governance constraints. However, the root directory suffers from significant clutter due to retained historical reporting artifacts (Phases 8-16). 

This Repository Refinement Master Inventory successfully maps the current state and classifies assets to ensure that nothing is lost during cleanup. It stands as the authoritative foundational reference for all future repository refinement work to be executed in Milestone GM-005.
