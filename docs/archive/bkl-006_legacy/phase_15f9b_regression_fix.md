---
archive_title: "Phase 15F.9B - Dasha Timeline Regression Fix"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15F.9B - Dasha Timeline Regression Fix

## Objective
Fix the regression introduced during Phase 15F.9 (`AttributeError: 'list' object has no attribute 'get'`) while preserving the timeline rescue functionality in `dasha_results`.

## Files Changed
- `backend/app/engines/master_probability_engine.py`

## Exact Diff
```diff
diff --git a/backend/app/engines/master_probability_engine.py b/backend/app/engines/master_probability_engine.py
index d408d6d..a6c8c34 100644
--- a/backend/app/engines/master_probability_engine.py
+++ b/backend/app/engines/master_probability_engine.py
@@ -207,7 +207,8 @@ class MasterProbabilityEngine:
         if not dasha_results:
             return self.stub
 
-        entries = list(dasha_results.values())
+        # Filter out non-dictionary entries (like "timeline" list) to prevent attribute errors
+        entries = [e for e in dasha_results.values() if isinstance(e, dict)]
 
         # Identify MD and AD by confidence_flags
         md_data = next(
```

## Implementation Details
Replaced the blind list conversion of `dasha_results.values()` with a defensive list comprehension that explicitly filters for dictionary types `if isinstance(e, dict)`. This guarantees that the `next()` generators running `e.get("confidence_flags")` will strictly operate on planet dictionary payloads and inherently skip the `timeline` list (and any future primitive metadata added to the dasha payload) without stripping it from the larger `engine_outputs`.

## Test Results
1. **Question Engine Evaluation**: Successfully ran `ask_structured_question` over all `question_registry.json` elements against `RAJU_CANONICAL_RAW`. All questions generated valid `QuestionResultCard` structs safely without throwing exceptions.
2. **Backend Engine Tests**: Ran `pytest tests\test_real_charts.py`. The suite returned exactly 5 failures (which match the known classical calibration failures from prior phases) and 25 passes in 0.17s. The `TypeError` / `AttributeError` exception is resolved.

## Build Results
- Build successful. 
- Existing scores unchanged.
- Timeline remains preserved and passes smoothly to the frontend Question Result formatting layer.
- Question Engine operates seamlessly.
