# PROJECT ENTRY POINT: VEDIC AI SYSTEM
**Status Date:** 2026-06-19
**Current Phase Status:** Phase 9 Completed / Phase 10 Preparation

## 1. Current Project Status
The Vedic AI System has advanced beyond the Phase 7 mathematical lock. The system now possesses a fully functional React/TypeScript frontend (Phase 8) and a rigidly defined Governance framework for the Question Engine (Phase 9). The current priority is transitioning from a free-text LLM Question Engine to a deterministic Question Registry system.

## 2. Completed Phase 8 and Phase 9 Work
* **Phase 8 (Frontend & Reporting):** React-based UI, complete PDF/HTML reporting suite, UI implementation of D1/Varga visuals, Dashboard data extraction.
* **Phase 9 (Question Engine Governance):** Addressed Dasha schema misalignment bugs spanning the UI API boundaries (`engine_outputs.dashas.synthesis`).
* **Phase 9 (Architecture):** Formulated the Question Registry Framework displacing the legacy free-text intent routing paradigm.

## 3. Active Development Priorities
The immediate focus is executing **Phase 10**:
1. **Phase 10A:** `FormulaLoader` Implementation (Mapping YAML configurations).
2. **Phase 10B:** Question ID Router deployment.
3. **Phase 10C:** UI Question Browser restructuring.

## 4. Question Registry Authority Documents
The following documents represent the undisputed ground-truth for Phase 10 development. Any Question Engine logic MUST map back to these architectural specs:
* `docs/architecture/QUESTION_REGISTRY_ARCHITECTURE_v1.md` (System Objective & UI Guidelines)
* `docs/status/QUESTION_REGISTRY_MASTER_v1.md` (24 Master Domains & 194+ Child Nodes)
* `docs/architecture/QUESTION_REGISTRY_MAPPING_v1.md` (Strict data schema requirements for nodes)
* `FORMULA_REPOSITORY_GOVERNANCE_2026-06-19_1600.md` (Mathematical rules)

## 5. Gochara Deferral Governance
While the mathematical foundations support Transit computations, Gochara (Transit) layers remain flagged as `future_gochara_required: true` in the Question Registry. Transits currently use snapshot mapping rather than timeline extrapolation. Modifying Mandali Transit boundaries or predicting future timeline epochs is formally deferred.

## 6. Documentation Naming Convention
All new governance, audit, and architecture documents MUST adhere to:
* Clear conceptual prefix (e.g., `IMPLEMENTATION_READINESS_AUDIT`).
* Appended timestamp if tracking a snapshot (e.g., `_2026-06-19`).
* Explicit version numbers for living schemas (e.g., `_v1`).

## 7. Protected Engine List
The following core mathematical engines are **MATHEMATICALLY LOCKED**. You are strictly forbidden from modifying their internal loop calculations, altering their mathematical return schemas, or duplicating their logic inside the Question Engine:
1. `DashaEngine`
2. `NatalPromiseEngine`
3. `YogaEngine`
4. `AshtakavargaEngine`
5. `TransitEngine`
6. `PipelineRunner` (The Master Orchestrator)

## 8. Next Implementation Roadmap (Phase 10)
1. **Formula Loader Blueprint:** Develop the YAML/JSON parsing mechanisms to extract formulas.
2. **Registry Mapping:** Bind frontend `question_id` requests directly to deterministic prediction logic.
3. **Frontend Modification:** Overhaul `QuestionEngine.tsx` to support the 24 Master Domain collapsible UI.
4. **Answer Composer Refactor:** Ensure LLM synthesis only receives mathematically filtered results.

---
**Legacy Phase 7 Handover Context:**
*If you need to recover the mathematical definitions of the core engines, refer to `SYSTEM_ARCHITECTURE.md` and `PROJECT_STATUS_MASTER.md` within the `HANDOVER_PACKAGE_2026-06-17_PHASE7_FINAL` directory.*
