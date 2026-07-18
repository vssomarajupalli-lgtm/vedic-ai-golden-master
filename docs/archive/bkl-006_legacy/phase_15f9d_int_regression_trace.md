---
archive_title: "Phase 15F.9D – Int Object Regression Trace"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15F.9D – Int Object Regression Trace

## 1. Full Python Stack Trace
```python
Traceback (most recent call last):
  File "app/api/v1/endpoints/queries.py", line 133, in ask_structured_question
    formatted_result = DisplayFormatter.format_question_result(
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "app/formatters/display_formatter.py", line 121, in format_question_result
    score = signal_data.get("final_score", 0)
            ^^^^^^^^^^^^^^^
AttributeError: 'int' object has no attribute 'get'
```
*(Note: Because `ask_structured_question` catches exceptions internally and raises an HTTPException with stringified detail, the user sees `Question Engine failed: 'int' object has no attribute 'get'`)*

## 2. Exact File
`backend/app/formatters/display_formatter.py`

## 3. Exact Function
`format_question_result()`

## 4. Exact Line Number
Line 121: `score = signal_data.get("final_score", 0)`

## 5. Exact Variable Name
`signal_data`

## 6. Exact Runtime Value
`0` (or whatever integer value the Ashtakavarga engine calculated as the BAV score adjustment for that planet).

## 7. Why an integer is reaching a .get() call
The root cause lies in `FormulaEvaluator.extract_signals()` and its internal `find_keys()` recursive function. 

When searching the massive `engine_outputs` dictionary for `required_signals` (e.g., `"sun"`, `"mars"`), `find_keys()` traverses the tree in order.
1. It first enters `engine_outputs["planets"]` and correctly maps `found["sun"]` to the rich planet dictionary (`{"final_score": 50, ...}`).
2. Later, it recurses into `engine_outputs["ashtakavarga"]["engine_modifiers"]["planet_score_adjustments"]`.
3. In this sub-dictionary, the key `"sun"` exists again, but its value is an integer representing the BAV point modification (e.g., `0`).
4. Because the key matches `"sun"`, `find_keys()` executes `found.update({"sun": 0})`.
5. This **silently overwrites** the rich planet dictionary with the primitive integer `0`.

When this `isolated_signals` dictionary is passed into `DisplayFormatter.py` (which added a loop in Phase 15F.8 to extract `supporting_factors`), the formatter expects every `signal_data` to be a dictionary, resulting in `'int' object has no attribute 'get'`.

## 8. Which Phase 15F.9 changes introduced the failure
Phase 15F.9 did **not** introduce this logic flaw; the overwriting bug in `FormulaEvaluator` has existed since the method was written, and the loop triggering the crash was added in Phase 15F.8 (`supporting_factors` generation). 

However, Phase 15F.9 masked the error because its `timeline` list addition caused `PipelineRunner` to crash in `MasterProbabilityEngine` *before* the API could even reach the `ask_structured_question` endpoint. Once the Phase 15F.9B fix allowed the pipeline to succeed, the question endpoint was hit, instantly exposing this latent integer-overwrite bug.

## Recommended Minimal Fix
In `backend/app/formulas/evaluator.py`, modify the `find_keys` function to prevent primitive values from overwriting rich dictionary payloads:

```python
        def find_keys(d: Dict[str, Any], keys_to_find: set) -> Dict[str, Any]:
            found = {}
            for k, v in d.items():
                if k in keys_to_find:
                    # Prevent primitive overwrites of rich dictionaries
                    if k in found and isinstance(found[k], dict) and not isinstance(v, dict):
                        continue
                    found[k] = v
                elif isinstance(v, dict):
                    # ... recurse and safely merge ...
                    for sub_k, sub_v in find_keys(v, keys_to_find).items():
                        if sub_k in found and isinstance(found[sub_k], dict) and not isinstance(sub_v, dict):
                            continue
                        found[sub_k] = sub_v
```
