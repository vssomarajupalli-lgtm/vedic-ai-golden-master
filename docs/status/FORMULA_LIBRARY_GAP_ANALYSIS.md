# FORMULA LIBRARY GAP ANALYSIS

## 1. Missing Formulas (Implemented but NOT Registered)
The current `registry_data.py` contains 33 canonical formulas. However, an analysis of the engine layer reveals significant business logic implemented outside the Formula Repository.

- **Yoga Detection Formulas**: `yoga_engine.py` implements 23 discrete astrological formulas (e.g., *Gaja Kesari Yoga, Neecha Bhanga Raja Yoga, Dhana Yoga, Saraswati Yoga*) using hardcoded python methods (`_detect_*_yoga()`). These are fully qualified astrological business rules that are completely absent from the central Formula Library.
- **Master Synthesis Formula**: The core algorithm for combining the 7 distinct astrological pillars (40% Natal, 15% Planet Strength, 10% House Strength, etc.) is hardcoded inside `master_probability_engine.py` (`MASTER_WEIGHTS` and `_weighted_sum`). 
- **Bhava (House) Strength Formula**: `house_strength_engine.py` embeds a rigid formula (30% SAV, 20% Occupants, 15% Benefic Aspect, 15% Malefic Aspect, 10% Type, 10% Yoga) rather than registering this calculation.

## 2. Unregistered Formulas
- **NLP Domain Routing**: `question_engine.py` contains a hardcoded `DOMAIN_KEYWORDS` mapping. While not strictly an astrological formula, it acts as the master classification rule governing which formula gets triggered.
- **Ashtakavarga Scoring**: `ashtakavarga_engine.py` contains a piecewise linear interpolation formula for SAV points that is embedded directly in `_sav_score()`.

## 3. Duplicate Formula Logic
- **Dasha Weighting Duplication**: Both `master_probability_engine.py` and `ashtakavarga_engine.py` duplicate the exact same mathematical logic for combining Mahadasha and Antardasha timing multipliers: `0.60 * md_score + 0.40 * ad_score`. 
- **Grade Thresholding**: The logic to convert a numeric score to a qualitative label (e.g., "EXCELLENT", "GOOD") is duplicated across multiple engines (`house_strength_engine.py`, `master_probability_engine.py`, `ashtakavarga_engine.py`) using identical or slightly varying iteration loops over constants.

## 4. Hidden Calculations
- **Lifetime Projection Engine Overload**: `master_probability_engine.py` hides a complex business rule within `evaluate()` where it iterates over the entire lifetime dasha timeline, swapping out the active dasha score and recalculating the total probability to generate a `lifetime_projection`.
- **BAV Consistency Engine**: `ashtakavarga_engine.py` embeds a hidden validation rule (`bav_consistency_check`) that validates if the sum of all 7 planet BAVs equals the total SAV for a given house.

## 5. Candidate Formula Library Additions
Based on the gap analysis, the following families should be added to the Formula Repository:

1. **`YOG_` (Yoga Family)**: E.g., `YOG_GAJA_KESARI`, `YOG_DHANA`. The schema must be extended to support structural boolean condition checks (e.g., Planet A in Kendra to Planet B).
2. **`CAL_` (Calculation Family)**: E.g., `CAL_HOUSE_STRENGTH`, `CAL_PLANET_STRENGTH`, `CAL_MASTER_PROBABILITY`. Extracting these mathematical weights out of the python engines and into the registry.
3. **`RUT_` (Routing Family)**: E.g., `RUT_MARRIAGE_KEYWORDS`.

## 6. Recommendations
1. **Deprecate Engine-Level Logic**: The `yoga_engine.py` must be refactored to remove the 23 `_detect_*_yoga` methods. It should act solely as an evaluator that reads `YOG_` formulas from the central registry.
2. **Centralize Mathematics**: Extract the 60/40 MD/AD multiplier and the piece-wise scoring interpolations into a centralized `astrology_math.py` utility, or better, register them in the Formula Library.
3. **Schema Expansion**: The `FormulaSchema` in `schema.py` currently only supports extracting variables (`required_signals`, `required_confidence_layers`). It must be expanded to support relational logic (e.g., "Lord of X is conjunct Lord of Y") to fully support the ingestion of the Yoga formulas.
