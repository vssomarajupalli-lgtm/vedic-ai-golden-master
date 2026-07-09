# PLANET INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
Planet Intelligence forms the structural foundation of the Golden Master probability pipeline. It is composed of two primary deterministic engines: the **Planet Strength Engine** (calculating the inherent operational capability of the 9 celestial bodies) and the **Rasi Strength Engine** (evaluating the environmental quality of the 12 zodiac signs). These engines execute sequentially near the beginning of the pipeline and provide the baseline dependency scores consumed by all higher-order logic.

## 2. Purpose
- **Planet Strength Engine:** To derive a 0-100 score indicating a planet's raw capability to deliver results based on Dignity, House Placement, Aspects, Conjunctions, State (Combustion/Retrogression), Shadbala, and Varga support.
- **Rasi Strength Engine:** To derive a 0-100 score indicating the environmental support of a zodiac sign, which dictates how comfortable planets feel when occupying that space, calculated via SAV support, Lord Strength, Occupant Quality, and Balance.

## 3. Responsibilities
- Maps string-based dignities ("exalted", "own_sign") into rigid mathematical scalars.
- Calculates benefic/malefic impact from aspects and conjunctions.
- Evaluates Shadbala requirements and converts them into the standard probability scale.
- Evaluates Varga (D9/D10) dignity refinements.
- Groups occupants by sign to evaluate sign health.
- **Planet:** Outputs a base score that is later modified by Ashtakavarga BAV points.
- **Rasi:** Outputs a final environmental score consumed by the Master Probability Engine.

## 4. Architecture
Both engines strictly adhere to Phase 4/5 architectural rules:
- **Zero Astrological Recalculation:** The engines consume pre-extracted JSON data. They do not compute planetary degrees, house boundaries, or aspect geometry.
- **Stateless:** They retain no runtime memory between calculations.
- **Rule of Determinism:** Pure `stdlib` mathematical aggregation; no AI or fuzzy logic is permitted.

## 5. Inputs
- `planet_data` and `shadbala_data` (for Planet Strength).
- `normalized_payload` (houses, planets, metadata), `dependency_scores` (pre-computed Planet scores), and `varga_outputs` (for Rasi Strength).

## 6. Outputs
- **Planet Result:** 
  - `base_score` (Structural score)
  - `bav_modifier` (Environmental modifier injected later by Ashtakavarga Engine)
  - `final_score` (Clamped [0, 100] outcome)
- **Rasi Result:**
  - `final_score` (Clamped [0, 100] environmental outcome)
  - `grade` (Qualitative probability mapping)
  - `breakdown` (Contribution of SAV, Lord, Occupants, Dignity, and Vargas)

## 7. Data Contracts
- Outputs adhere to the standard payload contract: `metadata`, `final_score`, `raw_score`, `breakdown`, and `confidence_flags`.
- The Rasi Strength Engine requires the Planet Strength Engine to execute first, as Sign health is heavily dependent on Sign Lord health.

## 8. Engine Dependencies
- **PlanetStrengthEngine:** 
  - *Upstream:* `FunctionalNatureEngine` (for determining temporal benefics/malefics, though currently relies on static arrays).
  - *Downstream:* Consumed by almost every engine in the system (House, Rasi, Yoga, Dasha, Natal, Ashtakavarga).
- **RasiStrengthEngine:**
  - *Upstream:* `PlanetStrengthEngine`, `VargaEngine`.
  - *Downstream:* Consumed by `MasterProbabilityEngine` and `NatalPromiseEngine`.

## 9. Formula Dependencies
- Hardcoded constants loaded from `astrology_constants.py` via `CalibrationManager`.
  - `PLANET_SCORING_MATRIX`
  - `RASI_SCORING_MATRIX`
  - `SAV_BINDU_SCALE`

## 10. Business Rules
- **Shadbala Normalization:** Shadbala percentages are piece-wise interpolated where 160% = 100 score, 100% = 50 score, and <40% = 0 score.
- **Vargottama Bonus:** A planet occupying the same sign in D1 and D9/D10 receives a flat +15 bonus in the Rasi environmental calculation.
- **BAV Injection Rule:** Planet scores are mutated *after* execution by the `PipelineRunner`, which injects the Ashtakavarga BAV modifier into the `PlanetStrengthEngine` output dictionary.

## 11. Deterministic Rules
**Planet Strength Formula:**
- Dignity (25%) + House Placement (20%) + Aspects (15%) + Conjunctions (10%) + Combustion (10%) + Retrogression (5%) + Shadbala (10%) + Varga Dignity (5%).

**Rasi Strength Formula:**
- SAV Environment (35%) + Sign Lord Strength (25%) + Occupant Quality (20%) + Benefic/Malefic Balance (10%) + Dignity Impact (5%) + Varga Validation (5%).

## 12. Execution Flow
1. **Pipeline Runner** derives planet dignities (Exalted, Debilitated, etc.) by checking the `EXALTATION_MAP`.
2. **PlanetStrengthEngine** iterates over all 9 planets, calculating structural strength based on the 8-factor formula.
3. Pipeline executes Varga and Dasha engines.
4. **RasiStrengthEngine** executes. It groups planets into their respective signs, pulls the SAV points for that sign's house, pulls the Sign Lord's score from step 2, and evaluates the 6-factor environmental formula.
5. **AshtakavargaEngine** executes and the Pipeline Runner injects BAV modifiers into the Planet outputs.

## 13. Implementation Files
- `backend/app/engines/planet_strength_engine.py`
- `backend/app/engines/rasi_strength_engine.py`

## 14. Documentation Files
- `VEDIC_AI_MASTER_ARCHITECTURE.md` (Referenced for anchoring values)

## 15. Governance References
- `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` (`CAL-003: Planet Strength Aggregation`, `CAL-004: Rasi Strength Environmental Score`)

## 16. Technical Debt
- **Functional Nature Hardcoding:** `planet_strength_engine.py` relies on `NATAL_BENEFICS` and `NATAL_MALEFICS` (static natural benefics) rather than fully integrating the `FunctionalNatureEngine` map derived in the pipeline runner.
- **Varga Stubbing:** In `PlanetStrengthEngine`, `varga_raw` is stubbed to `50.0`, meaning Varga dignity (5%) is not currently impacting base planetary strength, though it *is* impacting Rasi strength.

## 17. Missing Documentation
- No documentation exists explaining why Varga dignity is calculated independently in the Rasi Engine but stubbed in the Planet Engine.

## 18. Recommendations
- Wire the `FunctionalNatureEngine` output into the `PlanetStrengthEngine` and `RasiStrengthEngine` so that aspects and conjunctions are evaluated based on temporal (functional) nature rather than purely natural nature.
- Complete the Varga integration stub in `PlanetStrengthEngine` by passing in `varga_outputs` and reading the D9 dignity modifiers, ensuring symmetry with how `RasiStrengthEngine` handles Vargas.
