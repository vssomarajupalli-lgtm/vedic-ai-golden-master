# BUG_VALIDATION_AUDIT.md

## Bug Validation Audit Summary

This document presents reproducible evidence and technical validations for three major logic bugs discovered in the Vedic-AI computational engines.

---

## Finding 1: YogaEngine Dignity Lookup Bug

### A. Source Code Line Numbers
* **File**: [yoga_engine.py](file:///d:/vedic-ai-system/backend/app/engines/yoga_engine.py)
  * **Line 102** (inside `_eval_pancha_mahapurusha`): 
    ```python
    dignity = p_results.get(p, {}).get("dignity", "neutral")
    ```
  * **Lines 125-126** (inside `_eval_gaja_kesari`):
    ```python
    if p_results.get("jupiter", {}).get("dignity") != "debilitated" and \
       p_results.get("moon", {}).get("dignity") != "debilitated":
    ```
  * **Line 256** (inside `_eval_neecha_bhanga`):
    ```python
    if res.get("dignity") == "debilitated":
    ```

### B. Actual Runtime Values
* `p_results.get(p, {}).get("dignity")` evaluates to `None` for all planets, which triggers the fallback default of `"neutral"`.
* `res.get("dignity")` inside Neecha Bhanga Raja Yoga evaluates to `None`.
* `p_results.get("jupiter", {}).get("dignity")` and `p_results.get("moon", {}).get("dignity")` evaluate to `None`.

### C. Expected Values
* Planet dignity should be read from the raw normalized payload (`normalized_payload["planets"][p]["dignity"]`).
* For Saturn, dignity should resolve to `"exalted"`.
* For Jupiter and Mars, dignity should resolve to `"own_sign"`.
* For Mercury, dignity should resolve to `"debilitated"`.

### D. Proof that the Bug Changes Output
* In the Raju canonical chart, Saturn is **Exalted** in Kendra (**House 7**). This configuration meets all requirements for **Shasha Yoga** (one of the 5 classical Pancha Mahapurusha Yogas).
* In the actual runtime output, the `active_yogas` list contains only four yogas: `Harsha Yoga`, two `Raja Yoga` configurations, and `Kemadruma Yoga`. **Shasha Yoga is completely missing.**
* Because the lookup checks the output of `PlanetStrengthEngine` (which has no `"dignity"` field in its return dictionary) rather than the normalized input payload, Saturn's dignity is evaluated as `"neutral"`. Since `"neutral"` is not in `["exalted", "own_sign", "moolatrikona"]`, Shasha Yoga fails to activate.
* Similarly, `Neecha Bhanga Raja Yoga` (which cancels debilitation for planets like Mercury) can never evaluate as active because a planet's debilitated state is never detected.

### E. Estimated Impact
* **HIGH**: Misses major Raja Yogas and Mahapurusha Yogas, leading to incorrect calculations of planet/yoga potencies and domain promise adjustments.

---

## Finding 2: VargaEngine Dignity Normalization Bug

### A. Source Code Line Numbers
* **File**: [varga_engine.py](file:///d:/vedic-ai-system/backend/app/engines/varga_engine.py)
  * **Lines 52-53** (inside `_evaluate_planet` for D9):
    ```python
    d9_dignity = d9_data.get("dignity", "neutral").lower()
    d9_score = self.D9_SCORES.get(d9_dignity, 0.0)
    ```
  * **Lines 73-74** (inside `_evaluate_planet` for D10):
    ```python
    d10_dignity = d10_data.get("dignity", "neutral").lower()
    d10_score = self.D10_SCORES.get(d10_dignity, 0.0)
    ```

### B. Actual Runtime Values
* For Mars, Mercury, Jupiter, and Venus in `D9` or `D10`, the dignity string from `canonical_content.json` is `"Own House"`.
* This parses to `"own house"` (with a space character).
* `self.D9_SCORES.get("own house", 0.0)` resolves to `0.0`.
* `self.D10_SCORES.get("own house", 0.0)` resolves to `0.0`.

### C. Expected Values
* `"Own House"` should be normalized to `"own_house"` (replacing the space with an underscore).
* `self.D9_SCORES.get("own_house", 0.0)` should resolve to `10.0`.
* `self.D10_SCORES.get("own_house", 0.0)` should resolve to `5.0`.

### D. Proof that the Bug Changes Output
* For `mars`, the computed Varga modifiers returned by `VargaEngine` are only:
  ```json
  "modifiers": {"D9_vargottama_bonus": 15.0}
  ```
  with a computed validation score of `65.0`.
* If normalized correctly, Mars should also receive D9 own house (`+10.0`) and D10 own house (`+5.0`) dignity modifiers:
  ```json
  "modifiers": {"D9_vargottama_bonus": 15.0, "D9_dignity_modifier": 10.0, "D10_dignity_modifier": 5.0}
  ```
  resulting in a correct validation score of `50.0 + 30.0 = 80.0` (a depression of 15.0 points due to the bug).
* The same issue silences own-house dignity modifiers for Mercury, Jupiter, and Venus.

### E. Estimated Impact
* **MEDIUM**: Artificially depresses Varga-specific planet alignment scores, resulting in less accurate planetary activation modifiers.

---

## Finding 3: Varga Output Structure Mismatch

### A. Source Code Line Numbers
* **File**: [varga_engine.py](file:///d:/vedic-ai-system/backend/app/engines/varga_engine.py)
  * **Lines 34-41**: Returns a flat dictionary of planets:
    ```python
    results = {}
    for planet_name, planet_d1_data in planets.items():
        results[planet_name] = self._evaluate_planet(...)
    return results
    ```
* **File**: [rasi_strength_engine.py](file:///d:/vedic-ai-system/backend/app/engines/rasi_strength_engine.py)
  * **Line 316** (inside `_factor_varga`):
    ```python
    varga_planets = varga_outputs.get(varga_id, {}).get("planets", {})
    ```
* **File**: [natal_promise_engine.py](file:///d:/vedic-ai-system/backend/app/engines/natal_promise_engine.py)
  * **Line 295** (inside `_varga_score`):
    ```python
    varga = varga_results.get(varga_id, {})
    ```

### B. Actual Runtime Values
* `varga_results.get("D9", {})` resolves to `{}`.
* `varga_planets` inside `RasiStrengthEngine` evaluates to `{}`.
* `varga` inside `NatalPromiseEngine` evaluates to `{}`.
* `varga_score` for all signs defaults to `50.0`.
* `varga_support` for all 8 domains defaults to `50.0`.

### C. Expected Values
* `varga_results` should be structured grouped by Varga chart:
  ```json
  {
    "D9": {
      "planets": {
        "saturn": { "dignity": "exalted", "is_vargottama": true },
        ...
      }
    },
    "D10": { ... }
  }
  ```
* Downstream engines should receive active varga dignity modifiers rather than empty stubs.

### D. Proof that the Bug Changes Output
* For all 8 domains in `NatalPromiseEngine`, the `varga_support` is exactly `50.0` (the neutral fallback score).
* For example, the Career domain uses the `D10` chart and Saturn as its karaka. Since Saturn is exalted in D10 (`+10.0` modifier), the varga support score should have dynamically evaluated to `60.0`.
* Instead, the output is bypassed and returns exactly `50.0`. This occurs across all domains and signs, completely decoupling Navamsha (D9) and Dashamamsha (D10) results from the final outputs.

### E. Estimated Impact
* **CRITICAL**: Renders D9 and D10 calculations entirely useless in the final synthesis, silently disabling varga validation from affecting sign and domain promise outputs.
