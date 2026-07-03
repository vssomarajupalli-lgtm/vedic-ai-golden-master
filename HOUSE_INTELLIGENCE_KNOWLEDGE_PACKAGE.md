# HOUSE INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
House Intelligence governs the evaluation of the 12 Bhavas (houses) in the native's chart. It is comprised of two core deterministic calculation engines: the **House Strength Engine** (calculating the structural strength of a house using the Bhava Pillar formula) and the **Ashtakavarga Engine** (calculating the mathematical bindu support points for houses and transit transits). Together, these engines quantify the structural capacity of a life domain (e.g., Marriage, Career) to deliver its results.

## 2. Purpose
- **House Strength Engine:** Determines a 0-100 probability score for how strong and protected a specific house is, based on occupants, aspects, and lord strength.
- **Ashtakavarga Engine:** Translates extracted SAV (Sarvashtakavarga) and BAV (Bhinnashtakavarga) bindus into a 0-100 scoring scale, providing crucial environmental modifiers that adjust planet strength, dasha timing, and house strength.

## 3. Responsibilities
- Computes the aggregate impact of benefic vs malefic occupants inside a house.
- Computes the aggregate impact of benefic vs malefic aspects directed at a house.
- Interpolates raw Ashtakavarga bindu counts (e.g., 28 SAV points, 5 BAV points) into standard 0-100 probability scores via piecewise linear functions.
- Resolves zodiac signs to relative house numbers based on the Lagna (Ascendant).
- Generates BAV timing multipliers for Dasha lords.
- Runs consistency checks ensuring the sum of the 7 planet BAVs equals the house SAV.

## 4. Architecture
Both engines strictly comply with Phase 4 structural decoupling:
- **No Coordinate Math:** The Ashtakavarga Engine reads *extracted* SAV/BAV data from the `canonical_content.json`. It does not recalculate bindus from planetary longitude coordinates.
- **Modifier Injection:** The Ashtakavarga Engine does not alter planet scores directly. It generates a dictionary of `engine_modifiers` (e.g., `planet_score_adjustments: {"jupiter": 5}`). The `PipelineRunner` acts as the orchestrator to physically mutate the downstream objects.
- **Separation of Aspects:** Benefic and Malefic aspects are evaluated in isolated mathematical buckets to ensure clarity in the strength `breakdown`.

## 5. Inputs
- `house_data`: Extracted JSON for occupants, aspects, and house type.
- `bhava_bala_data`: Quantitative house strength metrics (stubbed).
- `normalized_payload`: Access to `ashtakavarga`, `planets`, and `dashas`.
- `dependency_scores`: Requires `PlanetStrengthEngine` output.

## 6. Outputs
- **House Strength Result:** 
  - `final_score` (Clamped [0, 100])
  - `breakdown` (Contribution of SAV, Occupants, Aspects, Type, Yogas)
- **Ashtakavarga Result:**
  - `bav_charts` (Planet-by-planet BAV breakdown)
  - `sav_chart` (House-by-house SAV breakdown)
  - `planet_bav_support` (Base modifiers per planet)
  - `dasha_bav_support` (Timing confidence multiplier)
  - `sav_analytics` (Peaks, weak points, consistency audit)
  - `engine_modifiers` (The payload injected by the Pipeline Runner)

## 7. Data Contracts
- The House Strength Engine treats the SAV score as 30% of its total calculation, creating a tight contract with the Ashtakavarga extraction layer.
- Ashtakavarga guarantees all outputs are keyed by relative house numbers (1-12) rather than Zodiac Signs to ensure compatibility with domain routing logic.

## 8. Engine Dependencies
- **HouseStrengthEngine:**
  - *Upstream:* `PlanetStrengthEngine` (Extracts lord's final score for interpolation).
  - *Downstream:* Consumed by `MasterProbabilityEngine`, `NatalPromiseEngine`.
- **AshtakavargaEngine:**
  - *Upstream:* `PlanetStrengthEngine`.
  - *Downstream:* Mutates `PlanetStrengthEngine` and `DashaEngine` outputs via the `PipelineRunner` injection. Consumed directly by `HouseStrengthEngine` and `TransitEngine`.

## 9. Formula Dependencies
- `HOUSE_SCORING_MATRIX`: Matrix defining point values for benefic/malefic occupants and aspects.
- `BAV_GRADE_THRESHOLDS`, `SAV_BINDU_SCALE`: Piecewise arrays mapping raw bindus to score percentages.

## 10. Business Rules
- **No Rahu/Ketu in BAV:** Adhering to the classical Parashari standard, Rahu and Ketu are excluded from Bhinnashtakavarga (BAV) bindu extraction and analysis.
- **BAV Consistency Override:** The `bav_consistency_check` flags a failure if `Sum(BAV) != SAV`, but it intentionally *does not override* the values, preserving the exact data extracted from the canonical source text.

## 11. Deterministic Rules
**House Pillar Formula (CAL-002):**
- SAV Points (30%) + Occupants (20%) + Benefic Aspects (15%) + Malefic Aspects (15%) + House Type (10%) + Yogas (10%).

**Ashtakavarga Modifiers (CAL-005/006):**
- **Planet BAV Modifier:** bindus >= 5 yields High (+); bindus == 4 yields Neutral (0); bindus < 4 yields Low (-).
- **Dasha BAV Timing:** `0.60 * MD_score + 0.40 * AD_score`. Maps to a confidence scalar multiplied against the Dasha Engine activation score.

## 12. Execution Flow
1. **Pipeline Runner** normalizes raw JSON.
2. `PlanetStrengthEngine` generates lord scores.
3. **HouseStrengthEngine** loops through houses 1-12. Fetches lord score, calculates occupant/aspect balances, and piece-wise converts SAV bindus to a percentage. Output is saved to `house_results`.
4. (Later in Pipeline) **AshtakavargaEngine** executes, evaluating BAV tables.
5. It computes `planet_bav_support` and `dasha_bav_support`.
6. **Pipeline Runner** calls `_apply_bav_modifiers()`, injecting the Ashtakavarga results into the already computed `planet_results` and `dasha_results`.

## 13. Implementation Files
- `backend/app/engines/house_strength_engine.py`
- `backend/app/engines/ashtakavarga_engine.py`

## 14. Documentation Files
- `VEDIC_AI_MASTER_ARCHITECTURE.md` (Governs BAV modifier logic)

## 15. Governance References
- `FORMULA_MASTER_INDEX_PLAN.md` (`CAL-002: Bhava Pillar`, `CAL-006: SAV Interpolation`)

## 16. Technical Debt
- **House Yogas Stubbed:** In `house_strength_engine.py`, `yogas_raw` is hardcoded to `50.0`. It does not yet consume the output of the `YogaEngine` to detect house-specific yogas.
- **Benefic/Malefic Hardcoding:** Like the Planet engine, `house_strength_engine.py` uses static natural benefics/malefics rather than functional nature.
- **Mathematical Duplication:** The `0.60 * md_score + 0.40 * ad_score` formula in `ashtakavarga_engine.py` is duplicated from the Master Probability engine.

## 17. Missing Documentation
- Documentation on how the `HOUSE_SCORING_MATRIX` scalar weights (25 for benefic, -25 for malefic) were calibrated.

## 18. Recommendations
- Implement Phase 3 integration for `house_yogas` by passing the `YogaEngine` results into the `HouseStrengthEngine`.
- Move the `_evaluate_sav_support()` interpolation logic entirely into the `AshtakavargaEngine` and have `HouseStrengthEngine` simply read the finalized SAV percentage, removing redundant mathematical logic.
- Switch to using `functional_nature` mapping for aspect and occupant evaluation.
