# QUESTION ENGINE IMPLEMENTATION PLAN

**Date:** 2026-06-19
**Phase:** 10

## Executive Summary
This document outlines the strict build sequence for transitioning the Question Engine from its current MVP state to the Phase 9 Governance Blueprint standards. The implementation will be executed in five distinct, modular phases to minimize regression risks and guarantee architectural decoupling.

---

## Phase 10A: Formula Loader
**Objective:** Decouple the astrological conditions from the Python execution code.
*   **Action:** Build a parsing engine that reads external Formula Definitions (e.g., JSON or YAML blueprints mapping to `MAR_PROMISE_001`, `FIN_WEALTH_001`). 
*   **Dependencies:** None. Can be built in isolation.
*   **Estimated Files Affected:**
    *   `[NEW]` `backend/app/engines/formula_loader.py`
    *   `[NEW]` `backend/app/config/formulas/` (Directory for governance JSONs)
*   **Risk Assessment:** **Low.** Purely a structural ingestion layer. Does not interfere with current pipeline logic until integrated.

## Phase 10B: Question ID Router
**Objective:** Replace naive keyword domain routing with strict `[DOMAIN_PREFIX]_[XXX]` identifiers.
*   **Action:** Refactor the routing layer to map string inputs to explicitly governed Question IDs (e.g., mapping "Will I get married?" to `MAR_001`), which then query the Formula Loader for execution instructions.
*   **Dependencies:** Requires Phase 10A (Formula Loader).
*   **Estimated Files Affected:**
    *   `[MODIFY]` `backend/app/engines/question_engine.py`
*   **Risk Assessment:** **Medium.** Replaces the existing `DOMAIN_KEYWORDS` approach. Requires regression testing against existing question datasets to ensure mapping integrity.

## Phase 10C: Dosha Framework
**Objective:** Establish a dedicated mathematical framework for calculating Dosha penalties based on Severity and Cancellation inputs, capped at -15%.
*   **Action:** Extract the currently hardcoded `_detect_affliction_flags` logic from the `NatalPromiseEngine` and construct a standalone `DoshaEngine`. 
*   **Dependencies:** Requires existing base engines (Planet, House, Rasi).
*   **Estimated Files Affected:**
    *   `[NEW]` `backend/app/engines/dosha_engine.py`
    *   `[MODIFY]` `backend/app/engines/natal_promise_engine.py` (Remove hardcoded logic)
    *   `[MODIFY]` `backend/app/pipeline_runner.py` (Insert `DoshaEngine` into sequence)
*   **Risk Assessment:** **High.** Modifying `NatalPromiseEngine` and `pipeline_runner.py` risks breaking current downstream probability outputs. Strict unit testing is required before merging.

## Phase 10D: Answer Composer
**Objective:** Implement the governed 5-part response structure (Promise, Strength, Reason, Timing, Advice).
*   **Action:** Deprecate the simplistic text-concatenation approach in `QuestionEngine.compose_response` and implement a structured templating or JSON composer that strictly formats the 5-part qualitative output.
*   **Dependencies:** Requires Outputs from Phase 10A and 10C.
*   **Estimated Files Affected:**
    *   `[NEW]` `backend/app/engines/answer_composer.py` (or major update to `question_engine.py`)
*   **Risk Assessment:** **Low.** Primarily an output formatting layer.

## Phase 10E: Question Engine Refactor (The Synthesis)
**Objective:** Bring the final normalized mathematics online.
*   **Action:** Wire the `QuestionEngine` to orchestrate Phase 10A, 10B, 10C, and 10D. Implement the Master Prediction Formula: `(Promise*0.5 + Activation*0.2 + Yoga*0.15 - Dosha*0.15)`. Deprecate reliance on the legacy `MasterProbabilityEngine` for question-specific routing.
*   **Dependencies:** Must occur sequentially *after* Phase 10A, 10B, 10C, and 10D are verified.
*   **Estimated Files Affected:**
    *   `[MODIFY]` `backend/app/engines/question_engine.py`
    *   `[MODIFY]` `backend/app/pipeline_runner.py`
*   **Risk Assessment:** **Very High.** This effectively cuts over the application from the legacy engine to the new blueprint architecture.

---

## Build Execution Order
To maintain pipeline stability, execution MUST follow this sequence:
1. `Phase 10A` -> `Phase 10B`
2. `Phase 10C`
3. `Phase 10D` -> `Phase 10E`

*Status: Awaiting approval to begin Phase 10A.*
