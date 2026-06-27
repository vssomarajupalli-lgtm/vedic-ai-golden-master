# ASHTAKAVARGA CLASSIFICATION AUDIT

**Date:** 2026-06-19_1730
**Context:** Phase 9 Step 3G Addendum

## 1. Objective
Review existing Phase 9 Step 3 governance references to Ashtakavarga and determine its correct structural classification within the Question Engine architecture.

## 2. Review of Existing Governance References
Based on an audit of the approved Phase 9 Step 3 documents, Ashtakavarga is currently referenced across multiple architectural layers:

*   **Timing Engine Design & Prediction Mathematics:** References Kakshya transits to fine-tune PD (Pratyantardasha) activation and determine the exact month/week a transit yields results.
*   **Question Router Blueprint:** Defines SAV/BAV as a "gating mechanism" for Formula Group execution.
*   **Varga Mapping Governance:** Defines SAV/BAV points in transiting signs as necessary transit validation.
*   **Formula Repository Governance:** Maps Ashtakavarga thresholds to both `PROMISE_001` (Base Natal Promise) and `TIMING_001` (Activation) formulas.
*   **Formula Weighting Governance:** Mentions Ashtakavarga operating as an activation capper (acting as a gate for score manifestation).

## 3. Classification Determination
Based on the systemic footprint across the blueprints, Ashtakavarga cannot be isolated to a single mathematical pillar. It must be classified as a **Combination Modifier** that intersects with three distinct layers:

### A. Bhava Strength Modifier (Natal Promise Layer)
*   **Role:** Validates the static, baseline strength of a Bhava. SAV/BAV profiles structurally modify the raw Bhava Bala, elevating or suppressing the fundamental `PROMISE_001` before any time periods are evaluated.

### B. Timing Modifier (Activation Layer)
*   **Role:** Operates dynamically when analyzing transits (Gochara). Kakshya analysis acts as a microscopic timing filter, restricting the broad Dasha (PD) manifestation windows into specific weeks or months.

### C. Confidence Modifier (Gating Mechanism)
*   **Role:** Operates as a structural gatekeeper for the overall Prediction Score. A fundamentally weak SAV acts as an invisible ceiling, capping the maximum allowable Activation score and thereby reducing the engine's overall confidence in a positive manifestation.

## 4. Audit Governance Constraints
*   **Zero File Modifications:** Existing governance files (`FORMULA_WEIGHTING_GOVERNANCE`, `PREDICTION_MATHEMATICS`, etc.) remain locked and unmodified.
*   **Zero Hardcoding:** This audit firmly establishes the theoretical classification of Ashtakavarga. It intentionally avoids introducing or enforcing any hardcoded numerical SAV/BAV thresholds, Kakshya point rules, or rigid activation caps, ensuring those variables remain dynamic and safely abstracted.
*   **Documentation Only:** No engine code was created or modified.
