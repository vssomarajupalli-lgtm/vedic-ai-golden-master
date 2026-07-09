# REPOSITORY CANONICAL SOURCE MAPPING

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Phase**: Canonical Knowledge Mapping
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Canonical Source Philosophy

To prevent conflicting rules and architectural drift, every concept must have exactly ONE canonical source. 

* **Canonical Source**: The absolute, unbreakable, single source of truth for a concept, rule, or architecture. It is the final authority.
* **Supporting Reference**: A document that utilizes or catalogs information from a canonical source (e.g., an index) but never redefines the rules.
* **Historical Reference**: A legacy document explaining past implementations (e.g., Phase readouts). They provide context but not active governance.
* **Cross Reference**: A document pointing to a canonical source for context (e.g., API docs pointing to data contracts).
* **Derived Documentation**: Documentation automatically generated from canonical code or schemas.
* **Temporary Documentation**: Working files that hold no governing authority.

---

## SECTION 3: Evidence Collection Method

Canonical ownership is determined through rigorous evidence collection, not filename assumptions. 

The contents of the repository's foundational assets have been analyzed, specifically focusing on:
* **Architecture documents** (`docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md`, `GOLDEN_MASTER_MANIFEST.md`)
* **Governance documents** (`docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md`, `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md`)
* **Knowledge Packages** (`*_KNOWLEDGE_PACKAGE.md`)
* **ADRs** (e.g., `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md`)
* **Formula Library & Master Index** (`FORMULA_CATEGORY_CATALOG_v1.md`, `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md`)
* **Validation & Calibration Frameworks**
* **Repository Analysis documents** (GM-005 outputs)

When a document explicitly declares ownership, provides the root mathematical rules, or establishes structural constraints, it is evaluated as the Canonical Source.

---

## SECTION 4: Canonical Source Registry

| Repository Concept | Canonical Source | Supporting References | Historical References | Primary Consumers | Evidence | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Architecture Rules** | `GOLDEN_MASTER_MANIFEST.md` | `docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` | Phase 14 Architecture Reports | Entire Repository | Explicitly defines overarching GM architecture. | |
| **Project Context** | `PROGRAM_A_COMPLETION_REPORT.md` | `VERSION_1_RELEASE.md` | Phase 8-16 Readouts | Developers | Establishes the exact completion state of Prog A. | |
| **ADR Collection** | *CONFLICT* (See Sec 6) | | Phase 8-16 Reports | Engineering | Decisions are scattered across phase reports. | |
| **Engine Governance** | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | `docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md` | `IMPLEMENTATION_READINESS_AUDIT_2026-06-19.md` | All Engines | Explicitly declares ownership and boundary rules. | |
| **Dependency Matrix** | `DEPENDENCY_AUDIT_REPORT.md` | `FORMULA_IMPACT_MATRIX.md` | Phase 13 Pipeline Reports | Pipeline Runner | Analyzes and defines the execution DAG. | |
| **Ownership Registry** | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | None | Phase 9 Reconciliation | Governance Audits | Explicit table of owners and must-never-owns. | |
| **Knowledge Packages** | `*_KNOWLEDGE_PACKAGE.md` | None | Older Phase 9 Step reports | Target Engines | Provide the mathematical and theoretical base. | |
| **Formula Library** | `FORMULA_CATEGORY_CATALOG_v1.md` | `FORMULA_FAMILY_CATALOG_v1.md` | Phase 12 Reports | Formula Evaluator | Catalogs all approved astrological formulas. | |
| **Formula Master Index** | `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | `QUESTION_COVERAGE_MATRIX_v1.md` | Phase 14 Reviews | Backend routing | Maps formulas to specific questions. | |
| **Calibration Framework** | `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | None | Phase 9 Profile Fixes | Master Probability | Sole authority on statistical tuning. | |
| **Validation Framework** | `VALIDATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | `DEPLOYMENT_VALIDATION_REPORT.md` | Phase 13 Validation Reports | QA Systems | Defines canonical test execution. | |
| **Question Engine** | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | `QUESTION_REGISTRY_MASTER_v1.md` | Phase 11 Reports | Frontend / Router | Defines the Orchestrator-Only intent. | |
| **Planet Engine** | `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | None | None | House, Yoga, Varga | Defines Ephemeris usage and planetary strength. | |
| **House Engine** | `HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | None | None | Yoga, Dosha | Defines Bhava Bala and cusp math. | |
| **Yoga Engine** | `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md` | None | Master Probability | Defines Yoga identification rules. | |
| **Dosha Engine** | `DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | None | None | Master Probability | Defines affliction severity capping. | |
| **Varga Engine** | `VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | `docs/architecture/ASHTAKAVARGA_ARCHITECTURE_RECOMMENDATION_2026-06-19_1800.md` | None | Dasha | Defines divisional chart arithmetic. | |
| **Dasha Engine** | `DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` | None | Phase 9 Dasha Fixes | Master Probability | Defines Vimshottari period activation. | |
| **Master Probability** | `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | None | Phase 9 Prediction Math | Question Engine | Synthesizes final probabilistic scores. | |
| **Mandali Generator** | `MANDALI_GENERATOR_KNOWLEDGE_PACKAGE.md` | `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` | Phase 15 Reports | Transit Engine | Canonical source for spatial Gochara grids. | |
| **Transit Engine** | `TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md` | None | Phase 7/8 Transit logic | None (Legacy) | Preserved legacy transit deterministic logic. | |
| **Pipeline** | `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md` | `DEPENDENCY_AUDIT_REPORT.md` | Phase 13 Pipeline Reports | Question Engine | REF-BKL-001 resolved conflict. | |
| **JSON Contracts** | `QUESTION_REGISTRY_BACKEND_CONTRACT_v1.md` | `QUESTION_ROUTER_CONTRACT_v1.md` | Phase 10B Contract Review | API, Frontend | Defines the I/O schemas for routing. | |
| **Repository Decision Register** | `docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md` | None | None | Architects | Logs all GM-005 structural changes. | |
| **Repository Inventory** | `REPOSITORY_REFINEMENT_MASTER_INVENTORY_v1.0.md` | None | `FINAL_REPOSITORY_TREE_AUDIT.md` | Architects | Central index of all repository assets. | |
| **Repository Classification**| `REPOSITORY_CLASSIFICATION_AND_ARCHIVE_STRATEGY_v1.0.md` | None | None | Architects | Defines Archive/Canonical/Legacy statuses. | |

---

## SECTION 5: Knowledge Ownership Matrix

| Knowledge Domain | Authoritative Owning Document |
| :--- | :--- |
| **Architecture** | `GOLDEN_MASTER_MANIFEST.md` |
| **Governance** | `ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` |
| **Formula Definitions** | `FORMULA_CATEGORY_CATALOG_v1.md` |
| **Engine Definitions** | Respective `*_KNOWLEDGE_PACKAGE.md` |
| **Validation Rules** | `VALIDATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` |
| **Calibration Rules** | `CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` |
| **Pipeline Rules** | `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md` |
| **Repository Rules** | `docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md` |
| **Documentation Standards** | `REPOSITORY_CLASSIFICATION_AND_ARCHIVE_STRATEGY_v1.0.md` |
| **Decision Records** | `docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md` |

---

## SECTION 6: Conflict Register

The following domains have conflicting documents claiming ownership or containing overlapping definitive rules. These conflicts are recorded here and MUST be resolved through future refinement decisions.

* **Concept**: Pipeline Orchestration
  * **Status**: RESOLVED (REF-BKL-001)
  * **Resolution**: Created `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md` and extracted orchestration logic from Question Engine and Master Probability Engine.

* **Concept**: Probability Synthesis (CON-002)
  * **Status**: RESOLVED (REF-BKL-002)
  * **Resolution**: Removed hardcoded 60/40 math from Question Engine. Enforced Master Probability Engine as sole canonical owner.

* **Concept**: Formula Governance
  * **Status**: RESOLVED (REF-BKL-003)
  * **Resolution**: Consolidated `FORMULA_GENERATION_GOVERNANCE_v1.md`, `FORMULA_REPOSITORY_GOVERNANCE_v1.md`, and `FORMULA_LIBRARY_SCALING_GOVERNANCE_v1.md` into a single canonical source `docs/governance/FORMULA_GOVERNANCE_v1.0.md`.

* **Concept**: Architecture Decision Records (ADRs)
  * **Conflicting Documents**: `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` vs all other `PHASE*_REPORT.md` files.
  * **Evidence**: Only Phase 15 uses a formal ADR structure, while other phases embed major architectural decisions inside implementation readouts.
  * **Risk**: Lack of a centralized ADR collection makes architectural constraints difficult to discover and audit.

*(Note: Conflicts are progressively resolved through formal refinement decisions (e.g., REF-BKL-001).)*

---

## SECTION 7: Canonical Integrity Rules

To maintain the purity of the Golden Master, the following rules apply:

* **One Canonical Source Per Concept**: No architectural rule or mathematical logic may be defined in more than one place.
* **No Competing Definitions**: Conflicts identified in Section 6 must be resolved via the Decision Register.
* **No Competing Formula Definitions**: A formula may only be defined in the authorized catalog.
* **No Duplicate Governance**: Governance checklists and rules must be centralized.
* **Knowledge Preservation Before Consolidation**: When resolving a conflict, all underlying knowledge from the deprecated document must be preserved in the surviving Canonical source.

---

## SECTION 8: Out of Scope

This document explicitly does **NOT**:

* Rename files.
* Merge documents.
* Delete documents.
* Modify formulas.
* Modify architecture.
* Approve repository refinement.

---

## SECTION 9: Summary

The Repository Canonical Source Mapping successfully establishes the definitive source of truth for the core concepts governing the Golden Master repository. It elevates Canonical assets above supporting and reference materials and rigorously flags areas of architectural conflict.

Future repository refinement decisions logged in the Decision Register shall strictly preserve the canonical sources identified herein, ensuring that no foundational knowledge is lost during cleanup.
