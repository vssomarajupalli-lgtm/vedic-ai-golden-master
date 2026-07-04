# REPOSITORY DUPLICATION AND CONSOLIDATION ANALYSIS

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

Duplication analysis must strictly precede repository refinement. Before any file is modified, merged, or archived, the exact nature of its duplication must be mathematically and architecturally analyzed. 

Apparent duplication does not automatically justify removal. In the Golden Master repository, **knowledge preservation has a higher priority than repository simplification**. This document identifies duplication candidates and serves as the evidence base for future entries in the Repository Refinement Decision Register.

---

## SECTION 3: Duplication Classification Model

To ensure safe refinement, every instance of suspected duplication is classified into one of the following categories:

* **True Duplicate**: Exact 1:1 mathematical or textual replication. Warrants removal of the duplicate.
* **Complementary Documents**: Documents that appear similar but serve distinct architectural audiences (e.g., frontend vs backend contracts). 
* **Intentional Redundancy**: Logic duplicated by design to preserve strict domain boundaries (e.g., decoupling engines).
* **Historical Reference**: Older implementations containing superseded logic that must be retained for regression testing.
* **Merge Candidate**: Highly overlapping documents that can be safely combined without knowledge loss.
* **Archive Candidate**: Historical or interim documents whose knowledge is now fully encapsulated in a Canonical source.
* **Preserve Separately**: Documents with slight overlaps that must not be merged due to architectural separation of concerns.

---

## SECTION 4: Repository Duplication Analysis

Based on the Repository Refinement Master Inventory, the following areas have been analyzed for duplication:

* **Architecture documents**: 
  * Overlap observed between `PHASE14G_ARCHITECTURE_REVIEW.md` and current `KNOWLEDGE_PACKAGE` documents. 
  * *Classification*: Archive Candidate for Phase 14 reports.
* **Governance documents**: 
  * Formula governance is split across `FORMULA_GENERATION_GOVERNANCE_v1.md`, `FORMULA_REPOSITORY_GOVERNANCE_v1.md`, and `FORMULA_LIBRARY_SCALING_GOVERNANCE_v1.md`.
  * *Classification*: Merge Candidate into a single Canonical Formula Governance document.
* **Knowledge Packages**: 
  * Highly distinct. Minor overlap in definitions across `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` and `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`.
  * *Classification*: Preserve Separately (maintains strict domain boundaries).
* **Formula documents**: 
  * `FORMULA_CATEGORY_CATALOG_v1.md` and `FORMULA_FAMILY_CATALOG_v1.md` contain overlapping indexing.
  * *Classification*: Merge Candidate.
* **ADR references**: No significant duplication found.
* **Validation documentation**: Multiple `PHASE*` validation reports exist. *Classification*: Archive Candidate.
* **Calibration documentation**: Isolated to `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md`. Unique.
* **Engine documentation**: Redundancy exists between `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` and `DEPENDENCY_AUDIT_REPORT.md`. *Classification*: Merge Candidate (consolidate dependency matrices).
* **API documentation**: Unique.
* **Frontend documentation**: Unique.
* **Reports**: Dozens of `PHASE8` through `PHASE16` reports. *Classification*: Historical Reference / Archive Candidates.
* **Examples**: None identified.

---

## SECTION 5: Formula Duplication Analysis

Astrological formulas must be analyzed strictly to prevent mathematical drift:

* **Planet formulas**: Contained in `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.
* **House formulas**: Contained in `HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.
* **Yoga formulas**: Spread across `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` and `FORMULA_REPOSITORY_DATA_MODEL_v1.md`. *Status*: Shared (Requires future review to consolidate mathematical source of truth).
* **Dosha formulas**: Contained in `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.
* **Varga formulas**: Contained in `VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.
* **Dasha formulas**: Contained in `DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.
* **Probability formulas**: Overlap between `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` and `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md`. *Status*: Duplicated (Question Engine currently hardcodes a 60/40 split). Requires future review for consolidation.
* **Question formulas**: Definitions scattered across `PHASE11` reports and `QUESTION_REGISTRY_MASTER_v1.md`. *Status*: Duplicated. Requires future review.
* **Calibration constants**: Unique to `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md`. *Status*: Unique.

*(Note: No formulas are modified by this document. This is analysis only.)*

---

## SECTION 6: Knowledge Consolidation Candidates

Specific domain knowledge appears in multiple places and should eventually be consolidated:

* **Architecture principles**: Found in `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` and `GOLDEN_MASTER_MANIFEST.md`. 
  * *Target State*: Single Canonical Source.
* **Governance rules**: Found in `GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md` and multiple `PHASE` reports.
  * *Target State*: Single Canonical Source (the GM-004 checklist).
* **JSON contracts**: Contract schemas are defined in both API documentation and Engine Data Contracts.
  * *Target State*: Cross Reference (API docs should reference Engine contracts, not duplicate them).
* **Pipeline descriptions**: `PipelineRunner` logic is described in both the `QUESTION_ENGINE` and `MASTER_PROBABILITY` packages.
  * *Target State*: Separate Knowledge (Pipeline orchestration should have its own canonical package).
* **Engine descriptions**: Duplicated across Phase reports and Knowledge Packages.
  * *Target State*: Historical Reference (Phase reports to be archived).
* **Glossary / Definitions**: Astrological terminology is redefined in almost every Knowledge Package.
  * *Target State*: Single Canonical Source (e.g., a Global Astrological Glossary).

---

## SECTION 7: Repository Risk Assessment

Refinement and consolidation carry inherent risks that must be mitigated through the Decision Register:

* **Knowledge loss**: Overzealous merging of phase reports could destroy the context of *why* an architectural decision was made.
* **Incorrect consolidation**: Merging complementary documents (e.g., Frontend UI state vs Backend API response) could blur architectural boundaries.
* **Hidden dependencies**: Deleting a seemingly duplicate definition might break downstream validation scripts.
* **Broken references**: Consolidating formula files will break Markdown links in historical ADRs.
* **Historical information loss**: Moving legacy code (Transit Engine) without documenting its lineage severs the audit trail.
* **Governance inconsistency**: Consolidating governance documents must not accidentally omit a constitutional rule.

---

## SECTION 8: Refinement Recommendations

Based on this analysis, the following high-level recommendations are submitted for future entries in the Decision Register:

* **Requires detailed review**: Question formula duplication across Phase 11 reports and the Question Registry.
* **Requires evidence**: Any proposed deletion of Phase 8-16 implementation reports to prove no unique knowledge exists.
* **Requires Decision Register entry**: Consolidation of the three Formula Governance documents.
* **Preserve separately**: Yoga and Dosha Intelligence packages; do not merge despite structural similarities.
* **Merge candidate**: `FORMULA_CATEGORY_CATALOG_v1.md` and `FORMULA_FAMILY_CATALOG_v1.md`.
* **Archive candidate**: All `PHASE8_*.md` through `PHASE16_*.md` interim implementation readouts.

*(Note: No implementation recommendations are authorized. All execution requires a separate, approved Decision Register entry.)*

---

## SECTION 9: Out of Scope

This document is strictly an analysis tool and explicitly does **NOT**:

* Delete files
* Rename files
* Merge documents
* Move files
* Modify formulas
* Modify architecture
* Approve repository changes

---

## SECTION 10: Summary

The repository contains significant documentation duplication stemming from the iterative, phase-based development of Program A (Phases 8-16). While the core astrological mathematical engines (Planet, House, Dasha, etc.) are highly cohesive and unique, the governance, formula catalogs, and historical reporting architectures are highly fragmented.

This analysis identifies clear consolidation targets. However, future repository refinement must be performed only after formal approval through the **Repository Refinement Decision Register**, ensuring that knowledge preservation remains the highest priority.
