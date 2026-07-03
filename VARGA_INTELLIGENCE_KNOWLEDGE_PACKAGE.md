# VARGA INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
The Varga Engine (Phase 5) is a structural refinement layer that evaluates the divisional charts (primarily D9 Navamsha and D10 Dashamamsha). Its function is to validate and refine the base strength of planets derived from the D1 (Natal) chart by assessing their dignity in higher harmonic environments. 

## 2. Purpose
The engine provides a secondary validation check on planetary strength. A planet that is strong in D1 but debilitated in D9 indicates a surface-level promise that fails to manifest, whereas a debilitated D1 planet exalted in D9 signals hidden strength (Neecha Bhanga). The engine computes these additive modifiers.

## 3. Responsibilities
- Maps string-based Varga dignities (e.g., "friendly", "enemy") to strict numeric modifiers.
- Detects contradictions between D1 and D9 dignities.
- Applies the Vargottama bonus (+15) when a planet occupies the same sign in D1 and the divisional chart.
- Recalculates base strength using the `PlanetStrengthEngine` directly on the Varga data to provide an isolated divisional score.

## 4. Architecture
The architecture strictly enforces the "Immutable D1 Rule".
- **Additive Modifiers Only:** The Varga Engine does not alter the D1 `final_score` of a planet. It outputs a dictionary of `modifiers` (e.g., `D9_dignity_modifier`) that can be applied externally by the `RasiStrengthEngine` or `NatalPromiseEngine`.

## 5. Inputs
- `normalized_data`: Must contain the `vargas` object with parsed D9 and D10 sub-charts, including dignity and Vargottama flags.
- `dependency_scores`: Output from the `PlanetStrengthEngine` (D1 scores).

## 6. Outputs
- Returns a dictionary keyed by Varga ID (`D9`, `D10`).
- Inside each Varga ID is a `planets` dictionary containing:
  - `final_score` (The structural score of the planet calculated *within* that specific varga).
  - `modifiers` (The +/- impact derived from the dignity).
  - `confidence_flags` (e.g., `varga_contradicted`, `neecha_bhanga_varga`, `D9_vargottama`).

## 7. Data Contracts
- The `vargas` object in the JSON payload must pre-calculate the Vargottama boolean flag; the engine does not perform sign-matching logic itself, it strictly reads the extracted flag.

## 8. Engine Dependencies
- **Upstream:** `PlanetStrengthEngine` (for the D1 dependency scores).
- **Downstream:** Consumed heavily by `RasiStrengthEngine` (which applies the modifiers to sign health), `NatalPromiseEngine` (which weighs Varga data as 15% of the domain score), and `MasterProbabilityEngine`.

## 9. Formula Dependencies
- `D9_SCORES`, `D10_SCORES`, and `VARGOTTAMA_BONUS` matrices loaded from `astrology_constants.py`.

## 10. Business Rules
- **Contradiction Detection:** If a planet is D1 Exalted but D9 Debilitated, it flags as `varga_contradicted`. If it is D1 Debilitated but D9 Exalted, it flags as `neecha_bhanga_varga`.
- **Recursive Strength Calculation:** The Varga Engine instantiates a fresh copy of the `PlanetStrengthEngine` and passes the D9/D10 data through it, returning an isolated 0-100 score for that specific chart.

## 11. Deterministic Rules
- **Vargottama:** +15 bonus.
- **D9/D10 Dignity:** (Placeholder values, derived from config) Exalted (+), Own/Moola (+), Friendly (+), Enemy (-), Debilitated (-).

## 12. Execution Flow
1. Load D1 dependency scores.
2. Iterate through all 9 planets.
3. Fetch D9 data for the planet. 
4. Check D9 dignity against the `D9_SCORES` matrix and append the modifier.
5. Check for Vargottama flag and append the `VARGOTTAMA_BONUS`.
6. Compare D1 dignity against D9 dignity to detect contradictions.
7. Pass the D9 data into `planet_engine.calculate_strength()` to get the Varga-specific final score.
8. Repeat steps 3-7 for D10 data.
9. Return the composite results object.

## 13. Implementation Files
- `backend/app/engines/varga_engine.py`

## 14. Documentation Files
- Currently undocumented outside of inline code comments.

## 15. Governance References
- Not yet mapped as a standalone calculation in the Formula Master Index.

## 16. Technical Debt
- **Missing Data Fallback:** If Varga data is missing from the JSON, it fails over to a string `"Data Unavailable"` rather than a numeric stub (`50.0`), which could cause downstream type-errors if parsed blindly.
- **Incomplete Integration:** As noted in the `PLANET_INTELLIGENCE_KNOWLEDGE_PACKAGE`, the base `PlanetStrengthEngine` stubs out its own internal Varga evaluation, relying entirely on downstream consumers (like Rasi/Natal) to apply the Varga modifiers.

## 17. Missing Documentation
- Documentation on how `D10_SCORES` differentiate from `D9_SCORES` in the calibration matrix.

## 18. Recommendations
- Fix the `"Data Unavailable"` type inconsistency by ensuring `final_score` always returns a `float` (e.g., `50.0`).
- Resolve the architectural split regarding where Varga validation truly lives: whether it should mutate the D1 Planet Score directly, or remain as a separate 10% pillar in the Master Probability formula.
