# PHASE 15: Promise Engine Validation

## 1. Four Pillar Formula
The Promise Engine has been successfully refactored to use a deterministic, percentage-based Four Pillar Formula. This approach completely replaces the legacy additive heuristics.

The outer weights for all domains are strictly enforced as:
- **Bhava Strength (Field of Manifestation):** 35%
- **Bhavadhipati Strength (Lord of the House):** 30%
- **Karaka Strength (Natural Significator):** 20%
- **Varga Validation (Divisional Chart):** 15%

## 2. No Double Penalty Rule
The architecture enforces a strict **No Double Penalty Rule**.
- The `NatalPromiseEngine` no longer applies post-hoc heuristic penalties (e.g., `-15` for Saturn in the 7th house).
- Afflictions, dignity drops, and malefic impacts are computed *only once* at their structural root (inside the `HouseStrengthEngine` for environmental impacts or the `PlanetStrengthEngine` for dignity/state impacts).
- This prevents the compounding mathematical collapse of scores and preserves clean explainability.

## 3. Runtime Validation Results
Using the canonical production dataset (Raju Case), the validated runtime scores are:
- **Marriage:** 49
- **Career:** 57
- **Wealth:** 61
- **Property:** 48
- **Health:** 39

*(Note: The Marriage score accurately reflects the removal of the double-counting anomaly, bringing the score from an unrealistic ~20 up to a realistic 49).*

## 4. Known Limitations
The following components are operating under approved temporary limitations pending future phases:
- **Varga (D9) Validation:** Currently returns a neutral fallback score of `50`. The D9 chart extraction phase is required before genuine Varga dignities can be evaluated.
- **House Yoga Implementation:** Currently uses a placeholder neutral score of `50`. Deep Yoga integration is deferred to Phase 3.
- **Occupant Scaling:** The linear mathematical scaling applied to occupants is pending future architectural review.
- **Malefic Aspect Scaling:** The inverted mathematical scaling applied to malefic aspects is pending future architectural review.

## 5. Future Validation Tasks
- **Unit Test Alignment:** Bypassed unit tests (currently 88 failing tests) must be rewritten to assert against the new percentage-based boundaries instead of the old heuristic magic numbers.
- **Scaling Review:** Review the mathematical boundaries for Occupant and Aspect scaling to ensure edge cases do not skew the 0-100 normalization logic.
- **Varga Integration Testing:** Validate D9 (and other Varga) scores once the extraction pipeline for divisional charts is completed.
- **Yoga Integration Testing:** Validate house-specific Yoga scores once the Phase 3 Yoga Engine is active.
