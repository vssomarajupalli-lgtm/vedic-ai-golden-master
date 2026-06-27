# MANDALI DEPENDENCY AUDIT

This map identifies exactly where Transit/Mandali dependencies are structurally embedded within the Question Engine architecture.

## 1. Engine Dependencies
The `TransitEngine` is explicitly listed in the `required_engines` array of the following Base Families:
*   **Marriage:** `MAR_TIMING_BASE`
*   **Career:** `CAR_CHANGE_TIMING` (Variant level)
*   **Health:** `HLT_LONGEVITY_BASE`, `HLT_VITALITY_BASE`
*   **Property:** `AST_PROPERTY_BASE`
*   **Progeny:** `FAM_PROGENY_BASE`

## 2. Signal Dependencies
The following `required_confidence_layers` evaluate specific Transit conditions:
*   **Marriage:** `jupiter_transit_7th_lagna` (in `MAR_TIMING_BASE`)
*   **Career:** `transit_saturn_jupiter_activate_10th` (in `CAR_CHANGE_TIMING`)
*   **Health:** `transit_jupiter_aspect_lagna` (in `HLT_RECOVERY_TIMING`)
*   **Property:** `transit_jupiter_saturn_activate_4th` (in `AST_PROP_TIMING`)
*   **Progeny:** `transit_jupiter_aspect_5th_9th` (in `FAM_CHILD_TIMING`)

## 3. Metadata Dependencies
The boolean flag `future_gochara_required = True` is declared on:
*   `MAR_TIMING_BASE`
*   `CAR_GROWTH_BASE`
*   `HLT_RECOVERY_TIMING`
*   `AST_PROP_TIMING`
*   `EDU_EXAM_SUCCESS_TIMING`
*   `FAM_CHILD_TIMING`

## 4. Evaluator Logic Dependencies
*   `backend/app/formulas/evaluator.py` (Line 77):
    *   `if "transit" in layer.lower() and any("TransitEngine" in w for w in system_warnings): is_fulfilled = False`
    *   The Evaluator is actively programmed to look for the word "transit" in confidence layers and bind it to the degradation state of the TransitEngine.

## 5. JSON Mapping Dependencies
*   `backend/app/config/question_registry.json` flags `future_gochara_required: true` on 10 explicit QIDs (Timing questions).

---
**Summary:** The Transit/Mandali engine is currently deeply coupled into the probability evaluation arrays of the Timing variants across 5 out of the 6 active domains.
