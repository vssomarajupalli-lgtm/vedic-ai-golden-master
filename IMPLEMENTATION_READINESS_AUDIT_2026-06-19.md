# QUESTION ENGINE IMPLEMENTATION READINESS AUDIT

**Date:** 2026-06-19
**Context:** Phase 9 Step 4

## Objective
Review the existing codebase to determine implementation readiness for the Question Engine based on the newly locked Phase 9 Step 3 Governance Blueprints.

---

## 1. Which Formula Inputs Already Exist?
The `pipeline_runner.py` successfully normalizes the JSON payload and provides the following critical base inputs required by the new Formula Repository:
*   **Bhava Bala:** Natively extracted and available.
*   **Shadbala:** Natively extracted and available.
*   **Lagna (Ascendant):** Passed via metadata.
*   **Dasha Timeline:** Available via the Dasha Engine.

## 2. Which Engine Outputs Already Exist?
The existing pipeline sequentially fires and holds the outputs of:
*   `PlanetStrengthEngine`: Lord and Karaka scores.
*   `HouseStrengthEngine`: Primary Bhava scores.
*   `VargaEngine`: Divisional chart scores.
*   `DashaEngine`: Active MD/AD/PD and timeline strength.
*   `TransitEngine`: Gochara transit activation scores.
*   `YogaEngine`: Evaluated planetary combinations.
*   `NatalPromiseEngine`: Baseline domain potential.

## 3. Which Question Engine Requirements Are Already Satisfied?
*   **Architectural Decoupling:** `QuestionEngine` currently receives separated components (promise, dasha, transit) from `pipeline_runner.py` without attempting to recalculate them internally (DR-008 constraint satisfied).
*   **Keyword Routing:** A basic MVP version of the Domain Router exists, matching user strings to domains (e.g., "marriage", "career").
*   **Response Construction:** The `compose_response` function already structures an output dictionary containing probabilities, dasha info, and basic answer text.

## 4. Which Requirements Are Missing?
*   **Formula Repository Abstraction:** The current `QuestionEngine` lacks the mechanism to load and parse external formula definitions (`MAR_PROMISE_001`).
*   **Dosha Evaluation Engine:** A dedicated module computing "Severity vs. Cancellation" (as mandated by Step 3D/3F) does not exist in the pipeline.
*   **Weighted Prediction Mathematics:** The `QuestionEngine` currently leans on a legacy probability synthesizer. It needs to be refactored to implement the strict `(Promise*0.5 + Activation*0.2 + Yoga*0.15 - Dosha*0.15)` normalization defined in Step 3E.
*   **5-Part Answer Composer:** The `compose_response` method returns basic text but does not fulfill the strict 5-part qualitative contract (Promise, Strength, Reason, Timing, Advice) required by Step 3C.
*   **Question ID System:** The system routes straight to domains rather than generating the required `[DOMAIN_PREFIX]_[XXX]` standard IDs.

## 5. Can Implementation Begin Immediately?
**No. Structural refactoring is required first.**
Before the Question Engine can dynamically synthesize predictions, the following prerequisites must be resolved:
1.  A Formula Loader must be implemented to read the new governance formulas into the engine runtime.
2.  A Dosha Evaluation framework must be added to the `pipeline_runner.py` to calculate net impact penalties.
3.  The `QuestionEngine` must be refactored to replace its current probability logic with the new Phase 9 normalized mathematical blueprint. 

Implementation should proceed by building the missing Dosha layer and Formula Loader before modifying the `QuestionEngine` itself.
