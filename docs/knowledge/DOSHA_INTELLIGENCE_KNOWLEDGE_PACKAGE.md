# DOSHA INTELLIGENCE KNOWLEDGE PACKAGE

## 1. Executive Summary
Dosha Intelligence represents the affliction and penalty framework within the Golden Master pipeline. Currently, it is a theoretical subsystem existing primarily as a technical debt placeholder. The overarching strategy (Phase 10C) dictates the creation of a standalone `DoshaEngine` to centralize all malefic penalties and astrological curses.

## 2. Purpose
The purpose of the Dosha framework is to detect classical afflictions (e.g., Kuja Dosha, Kemadruma Yoga, Chandal Dosha) and calculate a mathematical penalty that dynamically reduces the Master Probability Score (capped at a maximum -15% reduction).

## 3. Responsibilities (Planned)
- Detect structural afflictions based on planetary combinations.
- Evaluate cancellation criteria (Bhanga) which may nullify the penalty.
- Output a strict mathematical penalty scalar.

## 4. Architecture
Currently, there is **no dedicated architecture**. 
- Historically, afflictions were handled via hardcoded `_detect_affliction_flags` logic inside the `NatalPromiseEngine`.
- As of the latest refactoring, the `NatalPromiseEngine` explicitly states: `"afflictions": [], # Afflictions are now handled inside the respective planet/house engines`.
- However, the `PlanetStrengthEngine` and `HouseStrengthEngine` only handle *aspect* and *conjunction* malefic weighting; they do not possess discrete business logic for named Doshas (like Kuja Dosha).

## 5. Inputs (Planned)
- `normalized_payload`
- `planet_results` (to check for cancellation strength)

## 6. Outputs (Planned)
- `dosha_penalty_modifier` (float)
- `active_doshas` (list of strings)
- `cancellation_flags` (list of strings)

## 7. Data Contracts
- The Phase 10E Implementation Plan strictly limits the Dosha impact on the Master Prediction Formula to a maximum of **15% deduction** (`- Dosha*0.15`).

## 8. Engine Dependencies
- **Upstream:** None natively, though cancellation checks will require `PlanetStrengthEngine` scores.
- **Downstream:** Will be consumed by the `QuestionEngine` / `MasterProbabilityEngine`.

## 9. Formula Dependencies
- None currently registered. Future prefix `DOS_` will be added to the Formula Library.

## 10. Business Rules
- **No Double Penalty:** A planet heavily afflicted by Saturn is already penalized in the `PlanetStrengthEngine`. The `DoshaEngine` must not double-penalize the raw strength; it strictly applies the thematic penalty for the specific named Dosha.
- **Cancellation Priority:** If a cancellation condition (Bhanga) is met, the penalty multiplier drops to 0.

## 11. Deterministic Rules (Currently Unimplemented)
- **Kuja Dosha (Mars Affliction):** Mars in 1, 2, 4, 7, 8, 12 from Lagna.
- **Kemadruma Dosha:** Moon with no planets on either side.

## 12. Execution Flow
- Currently stubbed out and bypassed in `pipeline_runner.py` (Line 169: `"doshas": normalized_payload.get("doshas", {})`). The pipeline blindly extracts whatever string array the JSON parser emits, but performs zero mathematical calculations on it.

## 13. Implementation Files
- **Missing:** `backend/app/engines/dosha_engine.py` (Proposed in `docs/architecture/QUESTION_ENGINE_IMPLEMENTATION_PLAN_2026-06-19.md`)

## 14. Documentation Files
- `docs/architecture/QUESTION_ENGINE_IMPLEMENTATION_PLAN_2026-06-19.md` (Phase 10C)

## 15. Governance References
- Not yet mapped in the `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md`.

## 16. Technical Debt
- **Missing Framework:** The `DoshaEngine` does not exist. The application relies entirely on base structural weakness (Planet/House scores) to account for afflictions, which fails to capture the specific nuances of named astrological curses.

## 17. Missing Documentation
- Documentation defining exactly which Doshas will be supported, their specific penalty weights, and their cancellation rules.

## 18. Recommendations
- **Execute Phase 10C:** Build the `DoshaEngine` to decouple affliction logic completely from the parser and base engines.
- **Implement Cancellation Logic:** Ensure the engine evaluates Bhanga (cancellation) to prevent overly pessimistic probability scores.
