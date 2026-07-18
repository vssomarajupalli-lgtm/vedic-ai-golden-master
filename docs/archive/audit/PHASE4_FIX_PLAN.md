---
archive_title: "PHASE4_FIX_PLAN.md"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\audit"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE4_FIX_PLAN.md

## Phase 4 Fix Planning Summary

This document outlines the step-by-step implementation plan to resolve the three validated computational bugs in the Vedic-AI engines.

---

## 1. Dependency Analysis & Priority Order

### A. Which bug should be fixed first?
**Bug #3 (Varga Dignity Normalization)** and **Bug #1 (Varga Output Structure Mismatch)** should be resolved together first. 
* *Rationale*: Resolving these two issues unlocks correct divisional chart inputs and structures, which downstream engines immediately depend on. Bug #2 (YogaEngine Dignity Lookup) is independent of the Varga calculations and can be executed in parallel or immediately following.

---

## 2. Impact & Scope of Changes

### B. If Bug #1 (Varga Structure) is fixed, which downstream engines change?
Three downstream engines will change their runtime execution and output values:
1. **`RasiStrengthEngine`**: Will transition from using the flat `50.0` neutral baseline for all signs to using the actual D9/D10 dignity and vargottama modifiers.
2. **`NatalPromiseEngine`**: Will transition from using the flat `50.0` neutral baseline for all domains to using the specific Varga chart scores (e.g. D9 for Marriage, D10 for Career) based on the karaka's divisional dignity.
3. **`MasterProbabilityEngine`**: Will require modification inside its `_varga_validation` method to traverse the new chart-centric structure. Once adapted, the validation scores will change from static averages to real calculations.

### C. Which tests must be updated?
* **`backend/tests/test_varga_engine.py`**: Assertions must be updated from flat dictionary access (e.g. `results["sun"]`) to the new chart-centric nested dictionary path (e.g. `results["D9"]["planets"]["sun"]`).
* *Note*: `backend/tests/test_rasi_strength_engine.py` does **not** need mock changes because it already uses the correct chart-centric `RAJU_VARGA_OUTPUTS` format in its isolation tests.

### D. What files will be modified?
1. [varga_engine.py](file:///d:/vedic-ai-system/backend/app/engines/varga_engine.py) (Bug #1 and Bug #3)
2. [yoga_engine.py](file:///d:/vedic-ai-system/backend/app/engines/yoga_engine.py) (Bug #2)
3. [master_probability_engine.py](file:///d:/vedic-ai-system/backend/app/engines/master_probability_engine.py) (Restructure adaptation)
4. [test_varga_engine.py](file:///d:/vedic-ai-system/backend/tests/test_varga_engine.py) (Test alignment)

---

## 3. Risk Assessment

### E. Estimate Risk: **MEDIUM**
* *Justification*: While restructuring `VargaEngine` changes contract signatures between engines, these changes are confined to internal python classes. The system has a comprehensive suite of unit tests (`pytest`) that will immediately catch any contract drift or regression.

---

## 4. Detailed Implementation Plan

### Step 1: Varga Engine Fixes (Bug #1 & Bug #3)
* **File**: `backend/app/engines/varga_engine.py`
* **Changes**:
  * Normalize the dignity string lookup to lowercase and replace spaces with underscores:
    ```python
    d9_dignity = d9_data.get("dignity", "neutral").lower().replace(" ", "_")
    ```
    (Do the same for `d10_dignity`).
  * Restructure `VargaEngine.evaluate` to return a chart-centric nested dictionary grouped by `"D9"` and `"D10"` keys:
    ```json
    {
      "D9": {
        "planets": {
          "sun": {
            "metadata": {"entity_id": "sun", "entity_type": "planet"},
            "final_score": 70.0,
            "breakdown": {},
            "modifiers": {"D9_dignity_modifier": -5.0},
            "temporal_activation": {},
            "confidence_flags": ["D9_enemy"]
          },
          ...
        }
      },
      "D10": { ... }
    }
    ```

### Step 2: Adapt Master Probability Engine
* **File**: `backend/app/engines/master_probability_engine.py`
* **Changes**:
  * Update `_varga_validation` to aggregate planet modifiers across both charts:
    ```python
    def _varga_validation(self, varga_results: dict) -> float:
        if not varga_results:
            return self.stub
        per_planet = {}
        for varga_chart in varga_results.values():
            for planet, data in varga_chart.get("planets", {}).items():
                mods = data.get("modifiers", {})
                net = sum(mods.values())
                if planet not in per_planet:
                    per_planet[planet] = 0.0
                per_planet[planet] += net
        scores = [clamp_score(self.stub + net) for net in per_planet.values()]
        return round(sum(scores) / len(scores), 2) if scores else self.stub
    ```

### Step 3: Yoga Engine Fixes (Bug #2)
* **File**: `backend/app/engines/yoga_engine.py`
* **Changes**:
  * In `_eval_pancha_mahapurusha` (line 102), read planet dignity from `payload["planets"]` instead of `p_results`:
    ```python
    dignity = payload.get("planets", {}).get(p, {}).get("dignity", "neutral").lower().replace(" ", "_")
    ```
  * In `_eval_gaja_kesari` (lines 125-126), extract jupiter and moon dignity from `payload["planets"]`:
    ```python
    jup_d = payload.get("planets", {}).get("jupiter", {}).get("dignity", "neutral").lower()
    moon_d = payload.get("planets", {}).get("moon", {}).get("dignity", "neutral").lower()
    if jup_d != "debilitated" and moon_d != "debilitated":
    ```
  * In `_eval_neecha_bhanga` (line 256), extract dignity from `payload["planets"]`:
    ```python
    p_dignity = payload.get("planets", {}).get(p, {}).get("dignity", "neutral").lower()
    if p_dignity == "debilitated":
    ```

### Step 4: Align Varga Unit Tests
* **File**: `backend/tests/test_varga_engine.py`
* **Changes**:
  * Rewrite dictionary access assertions to match the new nested structure:
    ```python
    sun_mods = results["D9"]["planets"]["sun"]["modifiers"]
    self.assertEqual(sun_mods.get("D9_dignity_modifier"), 15.0)
    ```

### Step 5: Verification & Verification Checks
* Run `pytest` to verify that all Varga, Rasi, Yoga, and full-pipeline unit tests pass.
* Execute `python trace_chart.py` to confirm that the Raju canonical chart produces correct dynamic Varga and Yoga values.
