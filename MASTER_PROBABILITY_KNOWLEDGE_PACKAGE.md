# MASTER PROBABILITY ENGINE KNOWLEDGE PACKAGE

## 1. Executive Summary
The Master Probability Engine is the deterministic synthesis layer of the Vedic AI Golden Master platform. It sits at the top of the scoring stack and consumes all downstream engine outputs to produce a single, unified probability score. This engine encapsulates the core proprietary arithmetic formula that weighs the 7 foundational pillars of astrological logic into a single deterministic probability percentage.

## 2. Purpose
The purpose of the engine is to aggregate independent structural, environmental, and temporal assessments into a mathematically rigorous final conclusion. It guarantees that the identical input chart always yields the exact same percentage score, eliminating the variance common in LLM-driven astrological analysis.

## 3. Responsibilities
- Receives the fully computed `engine_outputs` dictionary from the `PipelineRunner`.
- Extracts the final computed scores from 7 distinct backend engines.
- Applies a static, hardcoded multiplier array (`MASTER_WEIGHTS`) to each layer.
- Computes the weighted average.
- Clamps the final score to a strictly bounded [0, 100] scale.
- Maps the numeric score to a qualitative Probability Grade (e.g., EXCELLENT, GOOD).
- Runs the `Lifetime Projection` analysis by iterating over the Dasha timeline and recalculating historical/future temporal activations.

## 4. Architecture
The architecture is a pure aggregation layer. 
**Crucial Architectural Rule:** The Master Probability Engine performs ZERO astrological recalculations. It does not check planetary dignities, houses, aspects, or transit positions. It strictly reads the `final_score` floats provided by the downstream engines.

## 5. Inputs
- `engine_outputs` (dict): A composite object containing the evaluated outputs from:
  - `natal_promise`
  - `planets`
  - `houses`
  - `rasis`
  - `vargas`
  - `dashas`
  - `transit`
  - `ashtakavarga`

## 6. Outputs
- `final_score` (int): Bounded [0, 100] integer.
- `raw_score` (float): Unclamped exact arithmetic score.
- `grade` (string): Qualitative label derived from `PROBABILITY_GRADES`.
- `breakdown` (dict): The exact contribution of each of the 7 pillars to the final score.
- `lifetime_projection` (list): An array of historically/future projected scores across all Vimshottari dasha periods.

## 7. Data Contracts
The engine guarantees that a missing dependency (a "stub") will return a neutral score of `50.0`. This ensures that partial data or incomplete feature pipelines do not artificially drag the overall probability score toward zero.

## 8. Engine Dependencies
The engine sits atop the entire pipeline and depends directly on:
1. `NatalPromiseEngine`
2. `PlanetStrengthEngine`
3. `HouseStrengthEngine`
4. `RasiStrengthEngine`
5. `VargaEngine`
6. `DashaEngine`
7. `TransitEngine`

## 9. Formula Dependencies
None directly. It executes the `CAL-001: Master Probability Synthesis` calculation internally.

## 10. Business Rules
- **No AI/ML:** The engine is purely deterministic arithmetic.
- **Stub Neutrality:** Any missing factor is assigned `50.0`.
- **Dasha Synthesis Override:** When calculating the lifetime projection, the engine iterates the `dashas.timeline` array and swaps the current `dasha_activation` score with the historical/future ones to generate a time-series graph of probability.

## 11. Deterministic Rules (The Master Weights)
The Master Probability Engine is the sole canonical owner of probability aggregation methodology and formula ownership.

### A. Core Engine Weights
The master aggregation formula is explicitly governed by the following ratio:
- `natal_promise`: 0.40 (40%)
- `planet_strength`: 0.15 (15%)
- `house_strength`: 0.10 (10%)
- `rasi_strength`: 0.10 (10%)
- `varga_validation`: 0.10 (10%)
- `dasha_activation`: 0.10 (10%)
- `transit_trigger`: 0.05 (5%)

### B. Probability Synthesis Formula
- **60/40 Synthesis Rule**: `(Natal Promise * 0.60) + (Dasha Activation * 0.40)`
- This exact mathematical synthesis rule is constitutionally owned by the Master Probability Engine and must never be redefined by any downstream orchestrator.

## 12. Execution Flow
1. Fetch all 7 factor sub-scores by inspecting the dictionaries emitted by downstream engines.
2. Calculate the weighted sum using `MASTER_WEIGHTS`.
3. Apply `clamp_score(raw)` to bound between 0-100.
4. Call `_grade(score)` to assign the qualitative label.
5. *(Lifetime Projection timeline orchestration looping moved to `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md`)*

## 13. Implementation Files
- `backend/app/engines/master_probability_engine.py`

## 14. Documentation Files
- `VEDIC_AI_MASTER_ARCHITECTURE.md` (Referenced in comments)
- `FORMULA_EVALUATOR_ARCHITECTURE_v1.md`

## 15. Governance References
- `FORMULA_MASTER_INDEX_PLAN.md` (Governs `CAL-001` extraction)

## 16. Technical Debt
- **Hardcoded Weighting:** `MASTER_WEIGHTS` is hardcoded in the Python file rather than being loaded from the central Formula Registry as `CAL-001`.
- **Dasha Calculation Duplication:** The Master Probability Engine duplicates the `0.60 * md_score + 0.40 * ad_score` calculation inside its `_dasha_activation()` method, which is also calculated inside the `AshtakavargaEngine` and `QuestionEngine`.
- **Lifetime Projection Complexity:** Generating the Lifetime Projection requires running a heavy `for` loop inside the master evaluator, which violates the strict single-evaluation responsibility of the engine.

## 17. Missing Documentation
- Documentation defining exactly how `varga_validation` modifiers are normalized to the [0, 100] scale is lacking.

## 18. Recommendations
- Extract `MASTER_WEIGHTS` into a JSON configuration (Formula Registry).
- Refactor the Lifetime Projection logic out of the `evaluate()` method and into a dedicated `ProjectionService` or `TimelineEngine` to maintain single-responsibility principles.
- Centralize the `0.60/0.40` Dasha weighting into an `astrology_math.py` utility to eliminate duplication across engines.
