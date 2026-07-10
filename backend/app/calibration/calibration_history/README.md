# Calibration History

This directory contains sequential calibration snapshots taken during the 20-horoscope validation process for Golden Master v1.0.

## Snapshot Naming Convention

- `calibration_001.json` through `calibration_020.json` — Sequential validation snapshots
- `v1.0_frozen.json` — Final promoted calibration (immutable)

## Snapshot Format

Each snapshot contains:
- `snapshot_id` — Sequential identifier (e.g., `calibration_007`)
- `timestamp` — ISO 8601 timestamp
- `horoscope_id` — Identifier of the validation horoscope
- `reason` — Human-readable reason for the calibration change
- `changes_made` — List of parameter changes with old/new values
- `validation_score` — Overall validation score (0-100)
- `engineer` — Name of the calibrating engineer

## Usage

1. After each horoscope validation, call `CalibrationManager.save_snapshot()`
2. After all 20 validations, call `CalibrationManager.promote_to_frozen()` to create `v1.0_frozen.json`
3. The frozen profile becomes the production calibration for Golden Master v1.0

## Protection

- This directory is created automatically by the Calibration Manager
- Do not manually edit snapshots — they are audit records
- `v1.0_frozen.json` is promoted atomically from `v1.0_current.json`