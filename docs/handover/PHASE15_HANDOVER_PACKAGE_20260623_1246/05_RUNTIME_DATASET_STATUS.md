---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 05_RUNTIME_DATASET_STATUS

## Active Production Files
- `extracted_json/raju_canonical_content.json`
- `extracted_json/raju_machine_index.json`

## Why these are the current production files
These files represent "CASE_001 Reality Validation". Raju is a known, verified natal chart with established life facts (e.g., is married, has specific career markers). Testing against a known reality prevents the AI from passing tests that produce mathematically functional but astrologically inaccurate conclusions.

## Why legacy files still exist
Legacy files (e.g., `canonical_content.json`) remain in the directory to serve as regression stubs and alternative data configurations from earlier testing phases. They should not be used for current validation.

## Exact backend/run.py runtime configuration
In `backend/run.py`, the file loads have been hardcoded for validation testing:
```python
# Force usage of verified Raju dataset
canonical_path = "extracted_json/raju_canonical_content.json"
machine_index_path = "extracted_json/raju_machine_index.json"
```

## Dasha Timeline Availability
The Dasha Timeline issue is closed. The canonical dataset contains rigid timeline continuity blocks, preventing the 'Unknown MD / Unknown AD' synthesis error from appearing.

## Known Dataset Lessons Learned
- Ensure the extraction parser explicitly tags and normalizes fields so engines don't receive `None` values (e.g., dict conversions vs list conversions).
- Legacy test JSONs can pollute validation if not actively isolated during system runs.
