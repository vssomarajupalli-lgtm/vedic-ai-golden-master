# FORMULA GOVERNANCE CONSOLIDATION ANALYSIS

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

The Golden Master repository relies on strict deterministic logic. Astrological formulas must be entirely predictable, auditable, and trace directly back to a single canonical mathematical source. 

This document performs a complete evidence-based analysis of all deterministic formula documentation in the repository. Its primary objective is to identify canonical formula sources, duplicate definitions, inconsistent ownership, and areas where calibration or probability math have bled out of their canonical boundaries. This document is strictly an analysis tool and performs **no repository modifications**.

---

## SECTION 3: Formula Analysis Methodology

Every formula category (Planet, House, Yoga, Dosha, Dasha, Varga, Master Probability, Calibration, Question) has been analyzed against the Master Inventory. The analysis determines:

* **Canonical Source**: The single authorized mathematical definition.
* **Supporting Documents**: Indexes or routing tables that reference the canonical source.
* **Duplicate References**: Legacy readouts or architectural documents that incorrectly redefine the formula.
* **Current Usage**: How the formula is actively processed.
* **Consumers**: The downstream engines reliant on the output.
* **Future GM-007 Ownership**: The designated owner for the upcoming Formula Consolidation milestone.
* **Repository Classification**: The current status of the asset (Canonical, Supporting, Archive Candidate, etc.).

---

## SECTION 4: Deterministic Formula Analysis Register

| Formula Category | Canonical Source | Supporting Documents | Duplicate References | Current Usage | Consumers | Future GM-007 Ownership | Repository Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Planet Formulas** | `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `FORMULA_CATEGORY_CATALOG_v1.md` | Legacy Phase 9 `PREDICTION_MATHEMATICS_REPORT` | Ephemeris resolution and planetary strength | House, Yoga, Varga | Planet Engine | Canonical |
| **House Formulas** | `HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `FORMULA_CATEGORY_CATALOG_v1.md` | Phase 8 implementation notes | Bhava Bala calculation | Yoga, Dosha | House Engine | Canonical |
| **Yoga Formulas** | `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `FORMULA_MASTER_INDEX_PLAN.md` | `FORMULA_REPOSITORY_DATA_MODEL_v1.md` (Conflict) | Yoga identification matrices | Master Probability | Yoga Engine | Canonical |
| **Dosha Formulas** | `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `FORMULA_CATEGORY_CATALOG_v1.md` | None | Affliction severity capping | Master Probability | Dosha Engine | Canonical |
| **Dasha Formulas** | `DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `FORMULA_CATEGORY_CATALOG_v1.md` | Phase 9 Dasha Fixes (`PHASE9_STEP2_DASHA_VISIBILITY_FIX.md`) | Vimshottari period activation | Master Probability | Dasha Engine | Canonical |
| **Varga Formulas** | `VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `ASHTAKAVARGA_ARCHITECTURE_RECOMMENDATION...` | None | Divisional chart arithmetic | Dasha Engine | Varga Engine | Canonical |
| **Master Probability** | `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | None | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` (Conflict) | Synthesizing final confidence scores | Question Engine | Master Probability Engine | Canonical |
| **Calibration Formulas** | `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | None | Phase 9 Profile Fixes (`PHASE9_STEP1_REPORT_PROFILE_FIX.md`) | Statistical tuning constants | Master Probability | Calibration Framework | Canonical |
| **Question Formulas** | `QUESTION_REGISTRY_MASTER_v1.md` | `QUESTION_COVERAGE_MATRIX_v1.md` | Dozens of `PHASE11` readouts | Routing API requests | Frontend, Pipeline | Question Engine | Canonical |

---

## SECTION 5: Findings & Duplication Identification

Based on the register in Section 4, the following conclusions are established:

### True Duplicates
* The `FORMULA_REPOSITORY_DATA_MODEL_v1.md` contains redundant mathematical structure for Yogas that overlaps with the `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`.
* Phase 9 step reports (e.g., Profile Fixes, Dasha Fixes) contain hardcoded math that duplicates the canonical Knowledge Packages.

### Shared References
* The `FORMULA_CATEGORY_CATALOG_v1.md` correctly references multiple engines. It serves properly as a *Supporting* document.

### Conflicting Definitions (Inconsistent Ownership)
* **Master Probability vs. Question Engine**: The Question Engine currently claims ownership over a 60/40 probability split, which inherently violates the `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` mandate. This is a severe architectural conflict.
* **Question Formulas**: Phase 11 documents redefine Question routing intent differently from the `QUESTION_REGISTRY_MASTER_v1.md`.

### Missing Ownership
* No missing ownership identified. Every formula maps strictly to a V2 Canonical Engine.

### Potential Consolidation Targets
* The redundant data models (e.g., `FORMULA_REPOSITORY_DATA_MODEL_v1.md`) should be archived or merged into the Yoga Intelligence package.
* Probability mathematics must be completely excised from the Question Engine documentation to restore its Orchestrator-Only status.

---

## SECTION 6: Out of Scope

This document is strictly an analytical instrument and explicitly does **NOT**:

* Modify formulas
* Rewrite formulas
* Merge documents
* Delete documents
* Change architecture
* Execute repository refinement

---

## SECTION 7: Summary

The deterministic formula architecture is fundamentally sound; the core Knowledge Packages hold absolute mathematical authority. However, significant documentation bloat exists in the form of legacy Phase reports and overlapping data models, creating a high risk of "Mathematical Drift" if developers consult the wrong document. 

The duplications and conflicts identified in this analysis validate the need for formal refinement execution, laying the groundwork for the upcoming GM-007 Formula Consolidation milestone.
