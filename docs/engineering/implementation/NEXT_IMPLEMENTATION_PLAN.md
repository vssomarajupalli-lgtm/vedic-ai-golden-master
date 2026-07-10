# NEXT IMPLEMENTATION PLAN

This document organizes the remaining implementation work identified in the Gap Analysis and Boundary Validation reports into a structured execution order. 

**Smallest Safe Implementation**: Task 1 (Question Engine Boundary Fix) is the smallest safe implementation that can be completed immediately to secure the architecture before building new modules.

---

## 1. Quick Wins (Low Complexity, High Structural Value)

### Task 1: Fix `QuestionEngine` Boundary Violation (DR-007)
*   **File(s) Affected**: `backend/app/engines/question_engine.py`, `backend/app/pipeline_runner.py`
*   **Dependencies**: None.
*   **Estimated Complexity**: Low
*   **Risks**: Minor risk of breaking tests that assume `QuestionEngine` runs in isolation.
*   **Validation Requirements**: Ensure `QuestionEngine` no longer imports `MasterProbabilityEngine`. Verify that `PipelineRunner` successfully coordinates the question routing and probability re-evaluation without throwing dependency errors.

### Task 2: Implement Functional Nature (Ascendant Layer)
*   **File(s) Affected**: `backend/app/engines/planet_strength_engine.py` (or new `functional_nature_engine.py`), `backend/app/pipeline_runner.py`
*   **Dependencies**: Data Layer (`normalized_payload["metadata"]`).
*   **Estimated Complexity**: Low
*   **Risks**: Could alter downstream `final_score` distributions for planets.
*   **Validation Requirements**: Verify that planets acting as functional benefics/malefics based on Lagna (e.g., Mars for Cancer Lagna) receive correct modifiers.

---

## 2. Medium Complexity (Missing Logical Blocks)

### Task 3: Build & Integrate `DoshaEngine`
*   **File(s) Affected**: `backend/app/engines/dosha_engine.py` (NEW), `backend/app/pipeline_runner.py`
*   **Dependencies**: `PlanetStrengthEngine`, `HouseStrengthEngine`.
*   **Estimated Complexity**: Medium
*   **Risks**: Kuja Dosha extraction and validation requires careful handling of source data.
*   **Validation Requirements**: Must follow DR-009 (Kuja Dosha Extraction Authority) to extract, validate, and interpret doshas strictly from canonical source data before attempting fallback verification. Verify that detecting a dosha correctly penalizes the associated domain probability.

### Task 4: Refactor `DashaEngine` to Pure Extraction (DR-001)
*   **File(s) Affected**: `backend/app/engines/dasha_engine.py`
*   **Dependencies**: `canonical_content.json` schema updates.
*   **Estimated Complexity**: Medium
*   **Risks**: Modifying Dasha temporal multipliers could cause large shifts in final prediction probabilities.
*   **Validation Requirements**: Ensure engine performs zero mathematical prediction. Verify it strictly reads the active Mahadasha/Antardasha from canonical data and correctly outputs temporal confidence multipliers for downstream engines.

---

## 3. Major Modules (Heavy Data / Core Subsystems)

### Task 5: Implement Transit Engine (Samartha Gochara System)
*   **File(s) Affected**: `backend/app/engines/transit_engine.py`
*   **Dependencies**: `canonical_content.json` (for extracted Phalithalu), `ephemeris_service.py`, `AshtakavargaEngine`, `NatalPromiseEngine`.
*   **Estimated Complexity**: High
*   **Risks**: High risk of over-engineering. Must strictly adhere to the proprietary micro-gochara system design (not a standard transit engine).
*   **Validation Requirements**: Validate per DR-008 (Hybrid Probability Model). Transit activation must correctly separate Potential, Activation, and Timing Window without overriding the Natal Promise. Verify fallback mechanisms if `canonical_content.json` is missing transit data.

### Task 6: Implement Remedy Engine
*   **File(s) Affected**: `backend/app/engines/remedy_engine.py` (NEW), `backend/app/pipeline_runner.py`
*   **Dependencies**: `DoshaEngine`, `NatalPromiseEngine`, `MasterProbabilityEngine`.
*   **Estimated Complexity**: High
*   **Risks**: Mapping specific astrological afflictions to correct classical remedies requires high domain accuracy.
*   **Validation Requirements**: Verify that severe chart afflictions (e.g., low Health domain promise) successfully trigger the generation of appropriate remedy suggestions in the final output.
