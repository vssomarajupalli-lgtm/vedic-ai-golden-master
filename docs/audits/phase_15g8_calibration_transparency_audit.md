# Phase 15G.8: Calibration & Constants Transparency Audit

## Executive Summary
This audit reviews the current deterministic calibration values within the Yoga Engine and the broader mathematical pipeline. The system was verified for "magic numbers", hidden modifiers, grade boundaries, and dead constants.

---

## PART A – CONSTANT INVENTORY

### 1. `backend/app/config/astrology_constants.py`
This is the primary repository for configuration objects.
- `PLANET_SCORING_MATRIX` (Dignity, House Placement, State, Aspects, Conjunctions)
- `HOUSE_SCORING_MATRIX` (House Type, Lord Dignity, Occupants, Aspects)
- `D9_SCORES`, `D10_SCORES`, `VARGOTTAMA_BONUS`
- `DASHA_SCORING_MATRIX` (Relationship Scalars)
- `SIGN_LORD_MAP`, `EXALTATION_MAP`, `DEBILITATION_MAP`, `OWN_SIGN_MAP`
- `SAV_BINDU_SCALE`, `RASI_SCORING_MATRIX`
- `PROBABILITY_GRADES`
- `BAV_GRADE_THRESHOLDS`, `BAV_PLANET_MODIFIER`, `SAV_FAVORABLE_THRESHOLD`
- `DASHA_BAV_CONFIDENCE`
- `NATAL_PROMISE_GRADES`, `DOMAIN_KARAKA`, `DOMAIN_CONFIG`

### 2. Engine-Local Constants
- `backend/app/engines/natal_promise_engine.py`: `_NEUTRAL = 50.0`
- `backend/app/engines/master_probability_engine.py`: `_STUB_SCORE = 50.0`
- `backend/app/engines/house_strength_engine.py`: `yogas_raw = 50.0` (Stub)
- `backend/app/engines/planet_strength_engine.py`: `shadbala_raw = 50.0` (Fallback)
- `backend/app/engines/rasi_strength_engine.py`: Default returns of `50.0` and safe scalar `1`.
- `backend/app/pipeline_runner.py`: Default lord missing fallback to `50.0`

---

## PART B – WEIGHT INVENTORY

### Planet Strength (`PLANET_SCORING_MATRIX`)
- Dignity (0-100)
- House Placement (10-100)
- Combust/Retrograde modifiers
- Benefic/Malefic aspects (±25)
- *Consumer:* `PlanetStrengthEngine` (`backend/app/engines/planet_strength_engine.py`)

### House Strength (`HOUSE_SCORING_MATRIX`)
- House Type (10-100)
- Lord Dignity (0-100)
- Occupants (±25)
- Aspects (±25)
- *Consumer:* `HouseStrengthEngine` (`backend/app/engines/house_strength_engine.py`)

### Rasi Strength (`RASI_SCORING_MATRIX`)
- Weights: `bhava` (0.35), `bhavadhipati` (0.30), `karaka` (0.20), `varga` (0.15)
- Occupant modifiers (±15)
- Dignity modifiers (-20 to +30)
- *Consumer:* `RasiStrengthEngine` (`backend/app/engines/rasi_strength_engine.py`)

### Natal Promise (`DOMAIN_CONFIG`)
- Weights: `primary_house` (0.25-0.30), `support_houses` (0.20), `karaka` (0.15-0.20), `lord` (0.15), `varga` (0.15), `sav` (0.05)
- *Consumer:* `NatalPromiseEngine` (`backend/app/engines/natal_promise_engine.py`)

### Master Probability (`MASTER_WEIGHTS`)
- Weights: `natal_promise` (0.40), `planet_strength` (0.15), `house_strength` (0.10), `rasi_strength` (0.10), `varga_validation` (0.10), `dasha_activation` (0.10), `transit_trigger` (0.05)
- *Consumer:* `MasterProbabilityEngine` (`backend/app/engines/master_probability_engine.py`)

---

## PART C – GRADE MAPPINGS

1. **Probability Grades** (`PROBABILITY_GRADES`):
   - Thresholds: 80 (EXCELLENT), 65 (VERY GOOD), 50 (GOOD), 35 (WEAK), 0 (TOO WEAK)
   - *Consumer:* Master Probability, Question Engine, Planet Engine, House Engine.

2. **Natal Promise Grades** (`NATAL_PROMISE_GRADES`):
   - Thresholds: 70 (STRONG), 50 (MODERATE), 30 (WEAK), 0 (PRESENT)
   - *Consumer:* `NatalPromiseEngine`

3. **BAV Grades** (`BAV_GRADE_THRESHOLDS`):
   - Thresholds: 7 (EXCELLENT), 6 (STRONG), 5 (GOOD), 4 (AVERAGE), 3 (BELOW_AVG), 2 (WEAK), 0 (CRITICAL)
   - *Consumer:* `AshtakavargaEngine`

---

## PART D – DEFAULT VALUES

- `50.0`: The universal Neutral/Stub/Fallback value across the entire backend.
- *Mathematical Impact*: Neutralizing a score to 50 prevents mathematical collapse in weighted averages for unimplemented stubs or missing data configurations.

---

## PART E – VERIFICATION CONSOLE READINESS

All of these constants are natively suitable for exposure in a frontend **"J. Calibration Console"**. 
Because they are static Python dictionaries in `astrology_constants.py`, the backend can simply expose an endpoint (e.g., `/api/v1/calibration`) that streams these JSON representations to the React client.

Layout mapping:
- **Weights:** `MASTER_WEIGHTS`, `DOMAIN_CONFIG`, `RASI_SCORING_MATRIX["weights"]`
- **Thresholds:** `SAV_FAVORABLE_THRESHOLD`
- **Grade Boundaries:** `PROBABILITY_GRADES`, `NATAL_PROMISE_GRADES`
- **Neutral Values:** Engine defaults (`50.0`)
- **Fallback Values:** Modifiers (e.g. `VARGOTTAMA_BONUS`)

---

## PART F – GOVERNANCE REVIEW

1. **Hidden Bonus Systems?** 
   - No "hidden" modifiers exist outside of central config. `VARGOTTAMA_BONUS` and `lord_own_bonus` are clearly articulated in `astrology_constants.py`.
2. **Hidden Penalty Systems?**
   - None. Negative values (like malefic aspects `-25`) are globally configured in `astrology_constants.py`.
3. **Dead Constants?**
   - None found.
4. **Constants Not Consumed?**
   - `NATURAL_BENEFICS` and `NATURAL_MALEFICS` are defined globally but also often manually array-checked in downstream components (opportunity to unify).
5. **Duplicate Constants?**
   - **YES.** `_NEUTRAL = 50.0` or `50` is declared locally in almost every engine file (`natal_promise_engine.py`, `master_probability_engine.py`, etc.). This should be centralized into `astrology_constants.py` as `NEUTRAL_BASE_SCORE = 50.0`.

---

## PART G – IMPLEMENTATION READINESS

**LOW RISK**
Exposing the constants as read-only via an API endpoint requires zero architectural adjustments and has no risk of breaking calculations. Re-mapping the duplicate `50.0` values to a global `NEUTRAL_BASE_SCORE` constant is extremely low risk.
