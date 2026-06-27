---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 08_FILES_MODIFIED_PHASE15

The following files were specifically modified during Phase 15 to enforce the Four Pillar Architecture and the No Double Penalty Rule:

## Core Engines
* `backend/app/config/astrology_constants.py`
  - Purpose: Removed legacy `AFFLICTION_PENALTIES` and `AFFLICTION_CAP`. Updated `PLANET_SCORING_MATRIX`, `HOUSE_SCORING_MATRIX`, and `DOMAIN_CONFIG` to 0-100 ranges.
* `backend/app/engines/planet_strength_engine.py`
  - Purpose: Restructured to calculate a deterministic 0-100 base score based on Dignity, House Placement, Aspects, Conjunctions, Combustion, Retrogression, Shadbala, and Varga.
* `backend/app/engines/house_strength_engine.py`
  - Purpose: Restructured to calculate a deterministic 0-100 base score based on SAV, Occupants, Benefic Aspects, Malefic Aspects, House Type, and House Yogas. Removed `lord_contribution`.
* `backend/app/engines/natal_promise_engine.py`
  - Purpose: Enforced the 35% / 30% / 20% / 15% outer aggregation weight. Completely removed post-hoc heuristic double penalties.

## Testing & Validation
* `backend/tests/test_weightage_calibration.py`
  - Purpose: Updated tests to verify inner and outer pillar weights align with the new percentage-based limits instead of additive matrices.
* `backend/tests/test_accuracy_validation.py`
  - Purpose: Rewrote regression logic to confirm the exact boundaries of classical astrological concepts (e.g. Venus combustion is handled locally, D9 fallback operates safely).
* `trace_marriage.py` (Temporary execution script)
  - Purpose: Extracted raw outputs directly from Raju's dataset to empirically prove engine execution flow.

## Documentation
* `docs/reference/PROMISE_ENGINE_FORMULA_v1.md`
  - Purpose: The architectural blueprint approved prior to code modifications.
* `docs/validation/PHASE_15_PROMISE_ENGINE_VALIDATION.md`
  - Purpose: The summary validation output proving phase success.
