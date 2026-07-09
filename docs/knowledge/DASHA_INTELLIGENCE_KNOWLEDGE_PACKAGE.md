# DASHA INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
The Dasha Engine evaluates the temporal activation of planetary energy in a native's life based on the Vimshottari Dasha system. Unlike traditional astrological calculators, the Dasha Engine in the Golden Master architecture *does not calculate the timeline itself*. It expects the timeline to be pre-extracted (e.g., from a parsed PDF) and focuses strictly on analyzing the astrological relationship between the Mahadasha (MD) and Antardasha (AD) lords to compute a temporal activation multiplier.

## 2. Purpose
The purpose of the Dasha Engine is to determine how efficiently the active period lords can deliver their natal promise. It accomplishes this by assessing the axis relationship (e.g., 1/7, 6/8) between the Mahadasha and Antardasha lords.

## 3. Responsibilities
- Receives the normalized timeline and a target evaluation date.
- Identifies the currently active Mahadasha (MD), Antardasha (AD), and Pratyantardasha (PD) lords.
- Computes the geometric relationship (axis) between the MD and AD lords based on their house placements.
- Applies a `relationship_multiplier` based on the computed axis.
- Computes the aggregate dasha strength using the formula: `(MD_Score * 0.50) + (AD_Score * 0.30) + (PD_Score * 0.20)`.
- Reconstructs the Dasha timeline array with activation percentages for the UI transparency layer.

## 4. Architecture
The Dasha Engine is a stateless evaluation node (Phase 6). It is dependent on the `PlanetStrengthEngine` for base structural scores. It sits before the `MasterProbabilityEngine`, injecting temporal multipliers into the stream so that downstream engines can calculate probability based on *when* the user is asking the question.

## 5. Inputs
- `normalized_data`: Must contain the `dashas.timeline` object, specifying historical and future Dasha start/end dates.
- `dependency_scores`: Output from the `PlanetStrengthEngine` containing the base `final_score` for all planets.
- `target_date`: Defaults to today's date if not provided.

## 6. Outputs
- `[planet_id]` (dict): Individual payload for the MD, AD, and PD lords containing `temporal_activation` data and `confidence_flags`.
- `synthesis` (dict): Summary object containing the active lords, dates, individual strengths, and combined `dasha_strength`.
- `timeline` (list): The original timeline array appended with `dasha_activation` percentages and `end_date` bounds for every historical and future period.

## 7. Data Contracts
- The engine guarantees it will never calculate astrological positions natively. It only evaluates relationships based on provided inputs.
- The output structure for individual lords conforms strictly to the standard JSON contract (Metadata, Final Score, Breakdown, Temporal Activation, Confidence Flags).

## 8. Engine Dependencies
- **Upstream:** `PlanetStrengthEngine` (Requires the D1 planetary strengths).
- **Downstream:** `MasterProbabilityEngine` and `TransitEngine` consume its synthesis output.

## 9. Formula Dependencies
- `calculate_planetary_axis(house_1, house_2)`: A utility formula located in `astrology_math.py`.

## 10. Business Rules
- **No Timeline Calculation:** The engine assumes the parser has perfectly extracted the Vimshottari timeline.
- **Relationship Application:** The relationship multiplier (derived from the axis) is applied to both the MD and AD lords. The PD lord currently receives a default multiplier of 1.0 (legacy behavior).

## 11. Deterministic Rules
- **Dasha Aggregation Weighting:** `dasha_strength` = `(MD * 0.50) + (AD * 0.30) + (PD * 0.20)`.
- **Relationship Matrix:** Uses `DASHA_SCORING_MATRIX.relationship_scalars` to determine the multiplier (e.g., a 6/8 axis yields a penalty multiplier, whereas a 1/7 axis yields a bonus or neutral multiplier).

## 12. Execution Flow
1. Accept timeline and target date. Sort timeline chronologically.
2. Locate the active record based on the target date.
3. Extract MD, AD, and PD lords.
4. Call `calculate_planetary_axis()` for the MD and AD lords based on their D1 house placements.
5. Fetch the `relationship_multiplier` from the calibration matrix.
6. Generate standard result payloads for the MD, AD, and PD lords.
7. Calculate the aggregate `dasha_strength`.
8. Iterate over the entire timeline and inject `dasha_activation` percentages for UI rendering.

## 13. Implementation Files
- `backend/app/engines/dasha_engine.py`
- `backend/app/utils/astrology_math.py` (Axis calculations)

## 14. Documentation Files
- Currently undocumented outside of inline code comments.

## 15. Governance References
- Not directly governed by a specific document, but relies on `astrology_constants.py` for its scoring matrix.

## 16. Technical Debt
- **Duplicated Aggregation Weights:** The `(MD * 0.60) + (AD * 0.40)` weighting exists in `master_probability_engine.py` and `ashtakavarga_engine.py`, but `dasha_engine.py` itself aggregates strength as `(MD * 0.50) + (AD * 0.30) + (PD * 0.20)`. This mathematical inconsistency across the codebase needs resolution.
- **Missing PD Logic:** The Pratyantardasha (PD) lord axis is intentionally skipped and hardcoded to a 1.0 multiplier due to legacy constraints.

## 17. Missing Documentation
- Documentation on how `DASHA_SCORING_MATRIX` scalars are calibrated.
- Documentation addressing the discrepancy between the 50/30/20 rule inside the engine vs the 60/40 rule used by downstream consumers.

## 18. Recommendations
- **Standardize Dasha Weighting:** Resolve the conflict between the 50/30/20 formula and the 60/40 formula used elsewhere in the codebase. Extract the chosen mathematical rule into a centralized utility.
- **Expand Axis Calculation:** Upgrade the engine to calculate the AD/PD axis relationship rather than hardcoding the PD multiplier to 1.0.
