# REPOSITORY REFINEMENT BACKLOG

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

## SECTION 2: Backlog Philosophy

The Repository Refinement Backlog acts as the master execution queue for the GM-005 milestone. To safely untangle the repository's historical complexity, the backlog enforces the following constitutional principles:

* **Evidence First**: No item enters this backlog unless backed by an approved GM-005 analysis document.
* **One Refinement At A Time**: Backlog items are executed sequentially; batch modifications are forbidden to prevent cascading regressions.
* **Knowledge Preservation**: Context is ported to Canonical sources before any legacy document is moved.
* **Architecture Stability**: Execution must never sever an architectural dependency or drift away from the Golden Master Manifest.
* **Traceability**: Every execution maps back to a specific entry in the Decision Register.

---

## SECTION 3: Master Refinement Backlog

| Backlog ID | Knowledge Domain | Repository Asset | Evidence Source | Priority | Architectural Risk | Dependencies | Estimated Complexity | Decision Register Reference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BKL-001** | Engine Knowledge | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` vs `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | Conflict Resolution Plan | Critical | High | Pipeline Runner | High | Pending | Queued |
| **BKL-002** | Engine Knowledge | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | Formula Ownership Mapping | Critical | High | API Layer | Medium | Pending | Queued |
| **BKL-003** | Governance Knowledge | `FORMULA_*_GOVERNANCE_v1.md` | Canonical Source Mapping | High | High | Formula Catalogs | Medium | REF-BKL-003 | Complete |
| **BKL-004** | Formula Knowledge | `FORMULA_REPOSITORY_DATA_MODEL_v1.md` | Formula Ownership Mapping | High | Medium | Yoga Engine | Low | Pending | Queued |
| **BKL-005** | Documentation | Phase 8-16 Readouts (ADR Extraction) | Conflict Resolution Plan | Medium | Low | Historical Traceability | High | Pending | Queued |
| **BKL-006** | Legacy Archive | Phase 8-16 Readouts | Duplication Analysis | Medium | Low | BKL-005 | Low | Pending | Queued |
| **BKL-007** | Formula Knowledge | `FORMULA_CATEGORY_CATALOG_v1.md`, `FORMULA_FAMILY_CATALOG_v1.md` | Duplication Analysis | Low | Low | Engine references | Low | Pending | Queued |

---

## SECTION 4: Backlog Organization

To ensure safe refinement, the master backlog is grouped by architectural domain:

### 1. Engine Knowledge
* **BKL-001**: Extract Pipeline Orchestration logic from Question Engine and Master Probability Engine to establish a unified orchestration boundary.
* **BKL-002**: Remove hardcoded probability synthesis math (the 60/40 split) from Question Engine documentation to restore Orchestrator-Only purity.

### 2. Formula Knowledge
* **BKL-004**: Merge the duplicate Yoga Data Model into the Canonical Yoga Intelligence Package.
* **BKL-007**: Combine the redundant Formula Category and Family catalogs into a single canonical index.

### 3. Governance Knowledge
* **BKL-003**: Consolidate the three overlapping Formula Lifecycle/Repository Governance v1 documents into a single Constitutional rulebook.

### 4. Documentation & Legacy Archive
* **BKL-005**: Extract hidden architectural constraints and rules from legacy Phase 8-16 reports and convert them into formal ADRs.
* **BKL-006**: Move the now-superseded Phase 8-16 readouts into the `/archive` folder.

---

## SECTION 5: Execution Order

Refinement execution must follow a strict order to minimize repository shock. The recommended execution sequence is:

1. **BKL-001 & BKL-002 (Engine Knowledge)**: *Highest Architectural Risk*. Orchestration boundaries and calculation ownership must be fixed first to prevent active logic drift.
2. **BKL-003 (Governance Knowledge)**: *High Impact*. Formula governance must be unified before any physical formulas are moved or evaluated in upcoming milestones.
3. **BKL-004 & BKL-007 (Formula Knowledge)**: *Medium Risk*. Catalog cleanup ensures engines reference the correct data models.
4. **BKL-005 (Documentation)**: *Knowledge Preservation*. Ensure all historical context is secured into ADRs before archival.
5. **BKL-006 (Legacy Archive)**: *Lowest Risk*. Move the physical Phase readouts only after BKL-005 is complete.

---

## SECTION 6: Success Criteria

The GM-005 Repository Refinement Backlog is considered successfully completed when:

* **Single Source of Truth**: The repository reflects exactly one canonical source per concept.
* **No duplicate ownership**: Every engine and formula maps cleanly to a dedicated domain.
* **No conflicting governance**: Developers have exactly one compliance checklist to follow.
* **Knowledge preserved**: Archiving legacy documents resulted in zero loss of historical context.
* **Architecture preserved**: Deterministic calculations and output contracts remain completely untouched.

---

## SECTION 7: Out of Scope

This document explicitly prohibits:

* No implementation
* No repository changes
* No document merging
* No deletions
* No architecture modifications

---

## SECTION 8: Summary

The Repository Refinement Backlog synthesizes all evidence gathered during the GM-005 analysis phase into a single, prioritized execution queue. By strictly grouping refinements by domain and enforcing a rigid execution order based on architectural risk, this backlog provides a safe blueprint for untangling historical repository complexity.

Future refinement shall execute these backlog items only after formal approval through the Repository Refinement Decision Register.
