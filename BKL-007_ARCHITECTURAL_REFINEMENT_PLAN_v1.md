# BKL-007 ARCHITECTURAL REFINEMENT PLAN v1

**Date:** 2026-07-09
**Phase:** GM-005 Repository Refinement
**Status:** Planning Complete

---

## 1. Refinement Planning Tables

### Refinement ID: ARP-001 (Consolidate Constitutional Truth)
*   **Repository Evidence:** `GOLDEN_MASTER_MANIFEST.md` exists simultaneously in `/` and `docs/governance/`.
*   **Objective:** Ensure a single authoritative source for constitutional rules to prevent automation/governance drift.
*   **Files/Folders involved:** `GOLDEN_MASTER_MANIFEST.md`, `docs/governance/GOLDEN_MASTER_MANIFEST.md`
*   **Current Owner:** Ambiguous (Split between Root and Governance)
*   **Proposed Authoritative Owner:** Chief Architect (`docs/governance/`)
*   **Constitutional Impact:** High
*   **Implementation Complexity:** Low
*   **Risk Assessment:** Deleting the active copy used by agents could break constitutional prompting. Requires verification of which file is injected.
*   **Dependencies:** Agent configuration paths.
*   **Expected Benefit:** Restores single source of truth.
*   **Recommendation:** Immediate

### Refinement ID: ARP-002 (Root Directory Clutter Relocation)
*   **Repository Evidence:** 135 files located directly in `/`.
*   **Objective:** Enforce strict modularity by moving loose documents to appropriate architectural or governance directories.
*   **Files/Folders involved:** All root directory files excluding repository management configuration (e.g., `.gitignore`, `README.md`).
*   **Current Owner:** Constitutional Scribe (Mechanically dumped over time).
*   **Proposed Authoritative Owner:** Designated modular owners (e.g., `docs/` for architecture/governance).
*   **Constitutional Impact:** Medium
*   **Implementation Complexity:** High (Requires 135 individual classifications).
*   **Risk Assessment:** Moving files breaks hardcoded references in historical/active documents.
*   **Dependencies:** ARP-001, CP-002 dependency verification.
*   **Expected Benefit:** Vastly improved repository maintainability and navigation.
*   **Recommendation:** GM-005

### Refinement ID: ARP-003 (Audit Legacy and Placeholder Debt)
*   **Repository Evidence:** 836 files contain keywords (TODO, FIXME, legacy, deprecated).
*   **Objective:** Classify legacy files as either active roadmap items or dead code requiring archiving.
*   **Files/Folders involved:** `backend/`, `frontend/`, `docs/`
*   **Current Owner:** Original Engine/Frontend Developers
*   **Proposed Authoritative Owner:** Respective Module Leads
*   **Constitutional Impact:** Low
*   **Implementation Complexity:** High (Deep codebase evaluation).
*   **Risk Assessment:** Premature deletion of placeholders may lose roadmap context.
*   **Dependencies:** None.
*   **Expected Benefit:** Reduces technical debt and clarifies active engine state.
*   **Recommendation:** Future GM

### Refinement ID: ARP-004 (Mechanical Artifact Purge)
*   **Repository Evidence:** Multiple temporary scratch files in `/`.
*   **Objective:** Remove temporary scripts generated during scribe/execution operations.
*   **Files/Folders involved:** `/scratch_*.py`
*   **Current Owner:** Repository Engineer
*   **Proposed Authoritative Owner:** None (Deletion)
*   **Constitutional Impact:** None
*   **Implementation Complexity:** Low
*   **Risk Assessment:** None (Scripts are entirely ephemeral).
*   **Dependencies:** None
*   **Expected Benefit:** Reduces root noise.
*   **Recommendation:** Immediate

---

## 2. Authoritative Document Ownership Matrix

| Document Category | Current Location | Proposed Authoritative Location | Authoritative Owner |
| :--- | :--- | :--- | :--- |
| Golden Master Constitution | `/` and `docs/governance/` | `docs/governance/` | Chief Architect |
| Architecture Decision Records | `docs/architecture/decisions/` | `docs/architecture/decisions/` | Architecture Advisor |
| BKL Decision Registers | `/` | `docs/governance/registers/` | Constitutional Scribe |
| Active Phase Readouts | `/` | `docs/status/` | Repository Engineer |
| Legacy/Archived Phases | `docs/archive/` | `docs/archive/` | Constitutional Scribe |
| System Orchestration | `/` (Dockerfiles) | `/` | Pipeline Engineer |

---

## 3. Root Directory Classification Matrix

The 135 active root-level files have been mechanically categorized to accelerate ARP-002:

#### Governance
*   docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md
*   docs/governance/BKL-005_FINAL_CONSTITUTIONAL_AUDIT.md
*   docs/governance/FORMULA_GOVERNANCE_CONSOLIDATION_ANALYSIS_v1.0.md
*   docs/governance/FORMULA_GOVERNANCE_v1.0.md
*   GOLDEN_MASTER_MANIFEST.md
*   docs/governance/GOVERNANCE_COMPLIANCE_CHECKLIST_v1.0.md
*   docs/governance/GOVERNANCE_CONSISTENCY_REVIEW.md
*   docs/governance/GOVERNANCE_REFINEMENT_REVIEW.md
*   docs/governance/PHASE9_STEP3A_GOVERNANCE_PACKAGE_REPORT_2026-06-19_1130.md

#### Architecture
*   docs/architecture/ADR_INVENTORY_v1.0.md
*   docs/architecture/ANSWER_COMPOSER_ARCHITECTURE_v1.md
*   docs/architecture/ARCHITECTURE_DECISION_LOG_v1.0.md
*   docs/architecture/ASHTAKAVARGA_ARCHITECTURE_RECOMMENDATION_2026-06-19_1800.md
*   BKL-007_ARCHITECTURE_EVIDENCE_REPORT_v1.md
*   docs/architecture/FORMULA_EVALUATOR_ARCHITECTURE_v1.md
*   docs/architecture/FORMULA_LIBRARY_EXPANSION_ARCHITECTURE_v1.md
*   docs/architecture/FORMULA_REPOSITORY_ARCHITECTURE_v1.md
*   docs/architecture/PHASE10A_FORMULA_LOADER_BLUEPRINT_2026-06-19.md
*   docs/architecture/PHASE12A_FORMULA_ARCHITECTURE_REPORT.md
*   docs/architecture/PHASE13B_EVALUATOR_ARCHITECTURE_REPORT.md
*   docs/architecture/PHASE13D_COMPOSER_ARCHITECTURE_REPORT.md
*   docs/architecture/PHASE14A_ARCHITECTURE_REPORT.md
*   docs/architecture/PHASE14C_CATALOG_ARCHITECTURE_REPORT.md
*   docs/architecture/PHASE14G_ARCHITECTURE_REVIEW.md
*   docs/architecture/PHASE9_QUESTION_BLUEPRINT_UPDATE_REPORT.md
*   docs/architecture/QUESTION_BROWSER_UI_BLUEPRINT_v1.md
*   docs/architecture/QUESTION_REGISTRY_ARCHITECTURE_v1.md
*   docs/architecture/TIMING_ARCHITECTURE_ANALYSIS.md

#### Documentation
*   docs/knowledge/API_LAYER_KNOWLEDGE_PACKAGE.md
*   docs/status/ASHTAKAVARGA_CLASSIFICATION_AUDIT_2026-06-19_1730.md
*   docs/status/BKL-001_EXECUTION_PACKAGE_v1.0.md
*   docs/status/BKL-002_EXECUTION_PACKAGE_v1.0.md
*   docs/status/BKL-005_COMPLETION_REPORT.md
*   BKL-006_CHIEF_ARCHITECT_DECISION_REGISTER.md
*   docs/status/BKL-006_CRL1_ARCHIVE_EXECUTION_PACKAGE.md
*   docs/status/BKL-006_REPOSITORY_DISCOVERY_REPORT.md
*   BKL-007_ARCHITECTURAL_REFINEMENT_PLAN_v1.md
*   BKL-007_REPOSITORY_DISCOVERY_REPORT_v1.md
*   docs/knowledge/CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md
*   docs/status/CURRENT_IMPLEMENTATION_AUDIT.md
*   docs/knowledge/DASHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   docs/status/DEPENDENCY_AUDIT_REPORT.md
*   docs/status/DEPLOYMENT_VALIDATION_REPORT.md
*   docs/status/DOCUMENTATION_INDEX_2026-06-19.md
*   docs/status/DOCUMENTATION_INDEX_PREPARATION_REPORT.md
*   docs/status/DOCUMENTATION_INDEX_REVIEW_AND_RECOMMENDATION.md
*   docs/knowledge/DOSHA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   docs/status/EDUCATION_FORMULA_ASTROLOGY_RATIONALE.md
*   docs/architecture/EDUCATION_REFACTOR_PLAN.md
*   docs/status/ENGINE_KNOWLEDGE_CONSOLIDATION_ANALYSIS_v1.0.md
*   docs/architecture/ENGINE_KNOWLEDGE_OWNERSHIP_MAPPING_v1.0.md
*   docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md
*   docs/status/FINAL_REPOSITORY_TREE_AUDIT.md
*   docs/status/FINAL_TREE_PLACEMENT_AUDIT.md
*   docs/status/FORMULA_CATEGORY_CATALOG_v1.md
*   docs/status/FORMULA_DOMAIN_MAP_v1.md
*   docs/status/FORMULA_FAMILY_CATALOG_v1.md
*   docs/status/FORMULA_IMPACT_MATRIX.md
*   docs/status/FORMULA_LIBRARY_GAP_ANALYSIS.md
*   docs/status/FORMULA_LIBRARY_REVIEW_PACK.md
*   docs/status/FORMULA_LIFECYCLE_MANAGEMENT_v1.md
*   docs/architecture/FORMULA_MASTER_INDEX_PLAN.md
*   docs/architecture/FORMULA_OWNERSHIP_MAPPING_v1.0.md
*   docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md
*   docs/governance/FORMULA_REPOSITORY_RISK_REGISTER_v1.md
*   docs/knowledge/FRONTEND_QUESTION_SYSTEM_KNOWLEDGE_PACKAGE.md
*   docs/knowledge/FUNCTIONAL_NATURE_ENGINE_KNOWLEDGE_PACKAGE.md
*   docs/status/GM-004_COMPLETION_REPORT_v1.0.md
*   docs/status/GOLDEN_MASTER_PROGRESS.md
*   docs/status/HEALTH_FORMULA_ASTROLOGY_RATIONALE.md
*   docs/architecture/HEALTH_REFACTOR_PLAN.md
*   docs/knowledge/HOUSE_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   docs/status/IMPLEMENTATION_READINESS_AUDIT_2026-06-19.md
*   docs/status/IMPLEMENTATION_READINESS_VERIFICATION_2026-06-19.md
*   docs/status/MANDALI_DECOUPLING_GIT_DIFFS.md
*   docs/status/MANDALI_DEPENDENCY_AUDIT.md
*   docs/knowledge/MANDALI_GENERATOR_KNOWLEDGE_PACKAGE.md
*   docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md
*   docs/status/PHASE11A_REGISTRY_IMPLEMENTATION_REPORT.md
*   docs/architecture/PHASE12B_DATA_MODEL_REPORT.md
*   docs/governance/PHASE14D_RISK_REGISTER.md
*   docs/status/PHASE14E_IMPLEMENTATION_REPORT.md
*   PHASE14F_QUESTION_REGISTRY_DIFF.txt
*   PHASE14F_REGISTRY_DATA_DIFF.txt
*   docs/status/PHASE14G_HARDENING_REVIEW.md
*   docs/status/PHASE15A_ENGINE_INTERFACE_AUDIT.md
*   docs/status/PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md
*   docs/status/PHASE15_PREPARATION_REPORT.md
*   docs/status/PHASE8_PDF_FIX_VALIDATION.md
*   docs/status/PHASE9_RECONCILIATION_AUDIT.md
*   docs/status/PHASE9_STEP1B_RESULTS_PROFILE_FIX.md
*   docs/status/PHASE9_STEP1_REPORT_PROFILE_FIX.md
*   docs/status/PHASE9_STEP2B_QUESTION_ENGINE_DASHA_AUDIT.md
*   docs/status/PHASE9_STEP2_DASHA_VISIBILITY_FIX.md
*   docs/architecture/PHASE9_STEP3B_REGISTRY_DATA_MODEL_REPORT.md
*   docs/knowledge/PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md
*   docs/knowledge/PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   docs/status/PROGRAM_A_COMPLETION_REPORT.md
*   docs/status/PROGRAM_A_FINAL_SUMMARY_REPORT.md
*   docs/status/PROGRAM_A_VERIFICATION_REPORT.md
*   docs/status/PROJECT_CONTINUITY.md
*   docs/status/PROPERTY_FORMULA_ASTROLOGY_RATIONALE.md
*   docs/architecture/PROPERTY_REFACTOR_PLAN.md
*   docs/knowledge/QUALITY_METRICS_ENGINE_KNOWLEDGE_PACKAGE.md
*   docs/status/QUESTION_BROWSER_USER_FLOW_v1.md
*   docs/status/QUESTION_COVERAGE_MATRIX_v1.md
*   docs/status/QUESTION_ENGINE_IMPACT_REPORT.md
*   docs/architecture/QUESTION_ENGINE_IMPLEMENTATION_PLAN_2026-06-19.md
*   docs/knowledge/QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md
*   docs/status/QUESTION_LIBRARY_REVIEW_2026-06-19_1230.md
*   docs/status/QUESTION_REGISTRY_BACKEND_CONTRACT_v1.md
*   docs/architecture/QUESTION_REGISTRY_MAPPING_v1.md
*   docs/status/QUESTION_REGISTRY_MASTER_v1.md
*   docs/status/QUESTION_ROUTER_CONTRACT_v1.md
*   docs/status/README_FIRST_PHASE9_UPDATE_REPORT.md
*   docs/status/RELEASE_CANDIDATE_AUDIT.md
*   docs/status/REPORT_SYSTEM_AUDIT.md
*   docs/knowledge/REPORT_SYSTEM_KNOWLEDGE_PACKAGE.md
*   docs/architecture/REPOSITORY_CANONICAL_SOURCE_MAPPING_v1.0.md
*   docs/status/REPOSITORY_CLASSIFICATION_AND_ARCHIVE_STRATEGY_v1.0.md
*   docs/architecture/REPOSITORY_CONFLICT_RESOLUTION_PLAN_v1.0.md
*   docs/status/REPOSITORY_DEPENDENCY_AND_IMPACT_ANALYSIS_v1.0.md
*   docs/status/REPOSITORY_DUPLICATION_AND_CONSOLIDATION_ANALYSIS_v1.0.md
*   docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md
*   docs/status/REPOSITORY_REFINEMENT_BACKLOG_v1.0.md
*   docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md
*   docs/status/REPOSITORY_REFINEMENT_EXECUTION_STRATEGY_v1.0.md
*   docs/status/REPOSITORY_REFINEMENT_MASTER_INVENTORY_v1.0.md
*   docs/knowledge/TRANSIT_ENGINE_KNOWLEDGE_PACKAGE.md
*   docs/status/UNMAPPED_QUESTION_REPORT_v1.md
*   docs/knowledge/VALIDATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md
*   docs/knowledge/VARGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   docs/status/VERSION_1_RELEASE.md
*   docs/knowledge/YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md
*   pytest.ini

#### Repository Management
*   docker-compose.yml

#### Temporary
*   scratch_discovery.py
*   scratch_generate_refinement_plan.py


---

## 4. Legacy Classification Matrix (836 Files)

Due to the volume (836 files), this matrix defines the classification structure required to resolve ARP-003. Individual file tagging is deferred to execution.

| Classification | Definition | Target Disposition | Owner Action Required |
| :--- | :--- | :--- | :--- |
| **Active** | Code contains TODOs for planned GM-006 roadmap features. | Keep | Prioritize in backlog. |
| **Deprecated** | Older phase engine logic that is superseded but structurally intact. | Archive | Move to `archive/engine_legacy/`. |
| **Placeholder** | Empty classes/functions built for future phases. | Review Further | Retain if scoped, delete if abandoned. |
| **Historical** | Notes, readouts, or test logs from legacy phases. | Archive | Move to `docs/archive/`. |
| **Unknown** | Unclear context; requires human/advisor review. | Review Further | Assign to Module Lead. |

---

**Rules Enforced in this Plan:**
* Planning only. Zero implementation executed.
* Zero file movement, deletion, or refactoring performed.
* Strictly derived from repository evidence.
* Ready to serve as the implementation blueprint for GM-005 BKL-007 execution.
