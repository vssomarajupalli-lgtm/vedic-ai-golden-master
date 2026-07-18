---
archive_title: "REPOSITORY REFINEMENT ACTION PLAN"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\roadmaps"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# REPOSITORY REFINEMENT ACTION PLAN

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Phase**: Evidence-Based Repository Refinement
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Refinement actions must follow rigorous evidence rather than assumptions. The Golden Master repository contains sensitive astrological logic and complex architectural dependencies; blindly deleting or merging files based on file names or perceived clutter guarantees knowledge loss.

This Action Plan converts the findings from the preceding GM-005 analysis documents into a structured, evidence-based refinement roadmap. Every proposed action documented here traces directly back to established proof.

---

## SECTION 3: Action Categories

All proposed refinements are classified into the following execution categories:

* **Document Consolidation**: Merging highly overlapping, non-governing documents (e.g., catalogs).
* **Knowledge Consolidation**: Extracting duplicated domain knowledge into a single Canonical source.
* **Governance Consolidation**: Merging competing rulesets into a single unified Constitution.
* **Reference Cleanup**: Updating internal Markdown links to point to Canonical sources instead of legacy documents.
* **Archive Preparation**: Relocating superseded, historical, or deprecated files to an `/archive` folder without deleting them.
* **Folder Standardization**: Reorganizing the directory tree to separate `/docs`, `/backend`, and `/frontend` cleanly.
* **Naming Standardization**: Renaming files to adhere strictly to the established `v1.0` or canonical naming conventions.
* **Historical Preservation**: Explicitly locking and tagging Legacy implementations (e.g., Transit Engine) so they are never accidentally refactored.
* **Cross-Reference Improvement**: Establishing formal Architectural Decision Records (ADRs) from buried historical context.

---

## SECTION 4: Refinement Candidate Register

| Candidate ID | Repository Asset | Category | Evidence Source | Reason | Expected Benefit | Risk | Decision Register Reference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ACT-001** | `FORMULA_CATEGORY_CATALOG_v1.md`, `FORMULA_FAMILY_CATALOG_v1.md` | Document Consolidation | Duplication Analysis | Overlapping formula indexing structures. | Single canonical formula catalog. | Broken markdown links in existing reports. | Pending | Proposed |
| **ACT-002** | `FORMULA_*_GOVERNANCE_v1.md` (3 files) | Governance Consolidation | Conflict Resolution Plan (CON-002) | Overlapping and competing formula lifecycle rules. | Unified, unambiguous governance rulebook. | Accidental omission of scaling rules during merge. | Pending | Proposed |
| **ACT-003** | `PHASE8` through `PHASE16` Implementation Readouts | Archive Preparation | Duplication Analysis | Superseded by Canonical Knowledge Packages; clutters root. | Clean repository root; clear canonical authority. | Loss of historical context if an ADR isn't created first. | Pending | Proposed |
| **ACT-004** | Pipeline Orchestration logic in Question & Probability Packages | Knowledge Consolidation | Conflict Resolution Plan (CON-001) | Both engines claim to dictate pipeline execution sequence. | Strict separation of architectural concerns. | High execution risk if boundaries are misunderstood. | Pending | Proposed |
| **ACT-005** | Legacy Phase Reports containing architectural decisions | Cross-Reference Improvement | Conflict Resolution Plan (CON-003) | Decisions are buried in implementation readouts. | Centralized, highly visible architectural constraints (ADRs). | Misinterpretation of legacy intent during extraction. | Pending | Proposed |

*(Note: Do not invent new candidates. Only act on evidence established during GM-005.)*

---

## SECTION 5: Refinement Priority

Every candidate action is classified by execution priority:

* **Critical**: Actions that resolve immediate mathematical or architectural ambiguity (e.g., **ACT-004** Pipeline Orchestration).
* **High**: Actions that resolve compliance or governance drift (e.g., **ACT-002** Formula Governance).
* **Medium**: Actions that drastically improve repository navigation but carry low architectural risk (e.g., **ACT-003** Archiving Phase Reports).
* **Low**: Cosmetic cleanup (e.g., **ACT-001** Catalog consolidation).
* **Future**: Identified cleanup that relies on unbuilt systems (e.g., Gochara engine documentation).

---

## SECTION 6: Execution Constraints

Implementation of any candidate in this action plan is strictly forbidden until the following constraints are met:

1. **Architecture Review**: Ensuring the action aligns with the Golden Master Manifest.
2. **Decision Register Entry**: The action must be logged and approved in `docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md`.
3. **Dependency Review**: Verification that downstream links or tests will not break.
4. **Knowledge Preservation Verification**: Ensuring no unique context is lost during a merge or archive.
5. **Git Checkpoint**: A secure state committed before execution.
6. **Validation**: Post-execution verification of repository integrity.

---

## SECTION 7: Success Criteria

The repository refinement will be considered successful if the following criteria are met post-execution:

* **Repository consistency**: File paths resolve correctly; tests pass.
* **No knowledge loss**: All astrological and domain context survives intact.
* **No architecture drift**: System boundaries remain identical to the pre-refinement state.
* **No broken references**: Internal Markdown and code imports are successfully updated.
* **No duplicated governance**: A single set of compliance rules exists.
* **No duplicate canonical ownership**: Every concept traces to exactly one authoritative source.

---

## SECTION 8: Out of Scope

This document explicitly prohibits:

* No implementation.
* No file deletion.
* No file movement.
* No file renaming.
* No document merging.
* No formula modification.

---

## SECTION 9: Summary

The Repository Refinement Action Plan establishes the evidence-based roadmap for physically cleaning the Golden Master repository. By categorizing proposed actions, assigning priorities, and enforcing strict execution constraints, the risk of catastrophic knowledge loss is mitigated.

Future repository refinement shall execute only approved actions sourced directly from this register.
