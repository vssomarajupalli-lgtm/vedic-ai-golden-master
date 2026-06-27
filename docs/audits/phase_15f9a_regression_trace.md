# Phase 15F.9A - Dasha Timeline Regression Trace

## 1. Stack Trace Profile
```python
Traceback (most recent call last):
  ...
  File "app/engines/master_probability_engine.py", line 211, in _dasha_activation
    md_data = next(
              ^^^^^
  File "app/engines/master_probability_engine.py", line 212, in <genexpr>
    (e for e in entries if "active_mahadasha" in e.get("confidence_flags", [])),
                                                 ^^^^^
AttributeError: 'list' object has no attribute 'get'
```
*(Note: A similar failure exists anywhere `dasha_results.items()` or `.values()` is iterated without fully protecting against non-dictionary top-level keys.)*

## 2. File Identification
- **File**: `backend/app/engines/master_probability_engine.py` (and potentially `pipeline_runner.py` / `transit_engine.py` / `quality_metrics_engine.py` if protection checks are bypassed).
- **Function**: `_dasha_activation(self, dasha_results: dict)`

## 3. Exact Line Number
- Line 212: `(e for e in entries if "active_mahadasha" in e.get("confidence_flags", []))`

## 4. Exact Variable Type Causing Failure
- The variable `e` is resolving to the newly injected `timeline` `list`. 
- Because `e` is a `list`, executing `e.get("confidence_flags", [])` immediately raises the `AttributeError`.

## 5. Failure Origination
- **Originates from**: `MasterProbabilityEngine` (and specifically, any synthesis layer that loops blindly over `engine_outputs.dashas.values()`).

## 6. Loop Audit: Iteration over `engine_outputs.dashas`
When the timeline was injected into the top level of `results` inside `DashaEngine`:
```python
results["timeline"] = timeline
```
It broke the previous structural contract where **every** value in `dasha_results` was guaranteed to be a planet dictionary (or the `synthesis` dictionary which safely fails `.get("confidence_flags")` by returning `[]`). 

Because `timeline` is a `list`, loops that use `.values()` will now attempt to call `.get()` on a list.

Loops audited:
1. `pipeline_runner.py` (_apply_bav_modifiers): **Safe** (Explicitly skips `"synthesis"` and `"timeline"` keys).
2. `transit_engine.py` (evaluate): **Safe** (Explicitly skips `"synthesis"` and `"timeline"` keys).
3. `quality_metrics_engine.py` (_dasha_activation_contribution): **Safe** (Explicitly skips `"synthesis"` and `"timeline"`).
4. `master_probability_engine.py` (_dasha_activation): **VULNERABLE** (Uses `list(dasha_results.values())` without filtering out the `timeline` list or `synthesis` struct).

## 7. Exact Root Cause
The `MasterProbabilityEngine` blindly converts `dasha_results.values()` into a list and creates a generator:
```python
entries = list(dasha_results.values())
md_data = next((e for e in entries if "active_mahadasha" in e.get("confidence_flags", [])))
```
Because Phase 15F.9 added `"timeline": [...]` directly to the `dasha_results` dictionary, `entries` now contains a `list` object. When the generator reaches the `timeline` element, it executes `[...].get("confidence_flags", [])`, raising the `AttributeError`. 

*(Note: Depending on the specific chart data, if the target Mahadasha lord is found early in the dictionary, the generator stops before hitting `timeline`—which is why it does not crash on every chart, but deterministically crashes when the generator is forced to evaluate the end of the list).*
