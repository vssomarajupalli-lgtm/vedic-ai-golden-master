# CALIBRATION FRAMEWORK KNOWLEDGE PACKAGE

## 1. Executive Summary
The Calibration Framework is the mathematical heart of the Golden Master. It abstracts all hardcoded scoring matrices, point values, and weights away from the calculation engines and centralizes them into manageable, versioned "Profiles".

## 2. Purpose
To ensure that astrological constants (like the +15 bonus for Vargottama or the 0.40 weight for Natal Promise) are not buried inside Python logic. By extracting them into a Calibration Registry, developers can easily tweak the mathematical tuning of the platform without altering the execution code.

## 3. Responsibilities
- Store all configuration matrices (e.g., `D9_SCORES`, `HOUSE_SCORING_MATRIX`).
- Allow hot-swapping of mathematical profiles (e.g., loading a `v1.0.0_base` profile vs a `v1.1.0_strict` profile).
- Provide a typed, dot-notation interface (via `CalibrationManager`) for engines to safely access these constants.

## 4. Architecture
- `calibration_registry.py`: Handles the loading and storage of different profiles.
- `calibration_manager.py`: Acts as the orchestrator. When an engine boots up, it asks the manager for its specific configuration slice (e.g., `calibration.varga` or `calibration.natal_promise`).
- `calibration_types.py`: Defines the Data Classes ensuring the matrices adhere to the correct shapes.

## 5. Inputs
- Static JSON or Python dataclass configurations located in the `profiles/` directory.

## 6. Outputs
- Strongly-typed Python objects injected directly into the `__init__` methods of the various Strength Engines.

## 7. Data Contracts
- The `CalibrationManager` performs data restoration (e.g., `_restore_int_keys`) to ensure that integer keys in dictionaries (which JSON enforces as strings) are converted back into Python `int` objects before the engines use them.

## 8. Implementation Files
- `backend/app/calibration/calibration_manager.py`
- `backend/app/calibration/calibration_registry.py`
- `backend/app/calibration/calibration_types.py`
- `backend/app/calibration/profiles/`

## 9. Technical Debt & Recommendations
- Currently, many constants are still imported directly from `app.config.astrology_constants`. The Calibration Framework needs to fully absorb these legacy constants to realize its potential as the single source of mathematical truth.
