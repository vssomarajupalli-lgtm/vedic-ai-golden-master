# IMPLEMENTATION READINESS VERIFICATION

**Date:** 2026-06-19
**Context:** Phase 9 Step 4B

## 1. TransitEngine
*   **File Path:** `D:\vedic-ai-system\backend\app\engines\transit_engine.py`
*   **Class Name:** `TransitEngine`
*   **Output Schema:** Returns a dictionary containing:
    *   `activation_score` (float)
    *   `grade` (string)
    *   `activated_domains` (dict)
    *   `supporting_factors` (list)
    *   `obstructing_factors` (list)
    *   `breakdown` (dict mapping house_activation, bav_support, planet_activation, dasha_sync, vedha_layer)
    *   `confidence_flags` (list of strings)
    *   `stub_factors` (list)

## 2. NatalPromiseEngine
*   **File Path:** `D:\vedic-ai-system\backend\app\engines\natal_promise_engine.py`
*   **Class Name:** `NatalPromiseEngine`
*   **Output Schema:** Returns a dictionary mapped by domain (e.g., `{"marriage": {...}}`), where each domain contains:
    *   `score` (float)
    *   `raw_score` (float)
    *   `promise` (string)
    *   `breakdown` (dict with primary_house, support_houses, karaka_planet, house_lord, varga_support, sav_support, yoga_bonus, affliction_penalty)
    *   `primary_house` (string)
    *   `varga_chart` (string)
    *   `karaka` (string)
    *   `afflictions` (list of strings)

## 3. QuestionEngine
*   **File Path:** `D:\vedic-ai-system\backend\app\engines\question_engine.py`
*   **Methods:** 
    *   `__init__`
    *   `route_domain(self, question: str) -> str | None`
    *   `compose_response(self, question: str, domain: str | None, natal_promise: dict, dasha_activation: dict, transit_activation: dict, final_probability: dict, bav_timing_confidence: str = "UNKNOWN") -> dict`
    *   `_activation_label(multiplier: float) -> str`
    *   `_promise_grade(score: float) -> str`
*   **Current Capabilities:** Performs hardcoded keyword-prefix domain routing without semantic matching. Composes a flat dictionary synthesizing domain string, basic probability wrapper, dasha timing, transit scores, and generates a simple concatenated text string (`answer_text`).

## 4. Dosha Calculations
*   **Existing Modules:** The `NatalPromiseEngine` currently holds hardcoded logic in `_detect_affliction_flags` and `_compute_penalties`.
*   **Existing Outputs:** Applies raw point deductions (e.g., "saturn_in_7") and outputs them via `breakdown["affliction_penalty"]` and the `afflictions` list.
*   **Missing Outputs:** There is no standalone Dosha Evaluation Engine (`dosha_engine.py`). It lacks the explicit "Severity vs. Cancellation" computations mandated by the Formula Repository Governance for Kuja Dosha, Kalasarpa, Guru Chandal, Papakartari, and Pitru Dosha.

## 5. Formula Inputs Currently Available
As evidenced by `D:\vedic-ai-system\backend\app\pipeline_runner.py`:
*   `planet_results` (Planet strength, Shadbala)
*   `house_results` (Bhava strength, Bhava Bala)
*   `varga_results` (Divisional strength)
*   `dasha_results` (Active periods and strength)
*   `rasi_results` (Sign environment data)
*   `av_results` (Ashtakavarga BAV/SAV matrices)
*   `yoga_results` (Evaluated positive and negative combinations)
*   `functional_nature` (Ascendant based functional mappings)

## 6. Formula Inputs Missing
*   **Formula Loader / ID Router:** No modules currently exist to parse Question IDs (e.g., `MAR_001`) or map them to explicit formulas (e.g., `MAR_PROMISE_001`) defined in the governance layer.
*   **Weighted Prediction Synthesizer:** The specific math equation `(Promise*0.5 + Activation*0.2 + Yoga*0.15 - Dosha*0.15)` is not programmed into `QuestionEngine`. It currently passes through a legacy `final_probability` dict from `MasterProbabilityEngine`.
