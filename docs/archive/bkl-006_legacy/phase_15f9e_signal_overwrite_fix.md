---
archive_title: "Phase 15F.9E – Signal Extraction Overwrite Fix"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15F.9E – Signal Extraction Overwrite Fix

## 1. Objective
Implement the minimal fix to prevent `FormulaEvaluator.extract_signals()` from accidentally overwriting previously collected rich dictionary payloads (e.g., from `PlanetStrengthEngine`) with primitive integer values generated deep inside other engine payloads (like Ashtakavarga BAV modifiers). This definitively resolves the `AttributeError: 'int' object has no attribute 'get'` crash occurring in `DisplayFormatter`.

## 2. Files Changed
- `backend/app/formulas/evaluator.py`

## 3. Exact Diff
```diff
diff --git a/backend/app/formulas/evaluator.py b/backend/app/formulas/evaluator.py
index daed6ea..687420c 100644
--- a/backend/app/formulas/evaluator.py
+++ b/backend/app/formulas/evaluator.py
@@ -11,15 +11,24 @@ class FormulaEvaluator:
         
         def find_keys(d: Dict[str, Any], keys_to_find: set) -> Dict[str, Any]:
             found = {}
+            
+            def safe_set(k: str, v: Any):
+                # Prevent primitive values from overwriting existing rich dictionary payloads
+                if k in found and isinstance(found[k], dict) and not isinstance(v, dict):
+                    return
+                found[k] = v
+
             for k, v in d.items():
                 if k in keys_to_find:
-                    found[k] = v
+                    safe_set(k, v)
                 elif isinstance(v, dict):
-                    found.update(find_keys(v, keys_to_find))
+                    for sub_k, sub_v in find_keys(v, keys_to_find).items():
+                        safe_set(sub_k, sub_v)
                 elif isinstance(v, list):
                     for item in v:
                         if isinstance(item, dict):
-                            found.update(find_keys(item, keys_to_find))
+                            for sub_k, sub_v in find_keys(item, keys_to_find).items():
+                                safe_set(sub_k, sub_v)
             return found
 
         isolated = find_keys(payload, set(required_signals))
```

## 4. Implementation Details
The problematic `found.update(find_keys(...))` recursion blinded merged all overlapping keys found deeper in the output payload tree. The fix introduces an inline `safe_set(k, v)` merge helper. If `k` is already present inside `found` as a `dict`, and the incoming `v` is a primitive scalar (like `int` or `float`), it safely skips the overwrite assignment. This natively protects core `{"final_score": ...}` structural objects mapped early in the JSON extraction path while remaining non-destructive to regular `get` operations.

## 5. Regression Verification
- **Question Engine Execution**: A batch execution invoking `/ask-structured-question` across all registered questions was completed against `RAJU_CANONICAL_RAW`. All endpoints successfully passed and successfully extracted formatting payloads without the `AttributeError`.
- **Supporting Factors & Attention Factors**: Successfully regenerated using the protected isolated signal dictionaries. (e.g. `['Venus provides strong support (63/100).', '7th House provides strong support (54/100).', ...]`).
- **Engine Tests**: Back-end `pytest` suite tests continue to pass correctly, reflecting identical original scoring states (5 classical chart calibration expectations maintained as failures; zero system crashes).
- **Formula Verification Console**: Unaffected, backend breakdown outputs remain 100% structurally identical.

## 6. Git Status Summary
```text
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
        modified:   app/database/user_preferences.json
        modified:   app/formulas/evaluator.py

no changes added to commit
```
