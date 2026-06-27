# ENGINE_OUTPUT_AUDIT.md

## Phase 3 Engine Output Audit Summary

This document presents the detailed mathematical audit of the seven computational engines processing the **Raju Canonical Chart** (`canonical_content.json` + `machine_index.json`). 

---

## 1. Engine Statistics & Metrics

Below is the audited breakdown of inputs, outputs, and score statistics for each calculation engine in the pipeline.

### A. PlanetStrengthEngine
* **Input Counts**: 9 planets (standardized keys: `sun`, `moon`, `mars`, `mercury`, `jupiter`, `venus`, `saturn`, `rahu`, `ketu`).
* **Output Values**:
  * `sun`: **70**
  * `moon`: **30**
  * `mars`: **20**
  * `mercury`: **0** (clamped from -25)
  * `jupiter`: **90**
  * `venus`: **45**
  * `saturn`: **75**
  * `rahu`: **0** (clamped from -5)
  * `ketu`: **0** (clamped from -5)
* **Minimum Score**: 0
* **Maximum Score**: 90
* **Average Score**: 36.67

### B. HouseStrengthEngine
* **Input Counts**: 12 houses (keys: `"1"` through `"12"`).
* **Output Values**:
  * `House 1`: **15** (clamped via Lagna floor)
  * `House 2`: **41**
  * `House 3`: **11**
  * `House 4`: **32**
  * `House 5`: **40**
  * `House 6`: **0**
  * `House 7`: **14**
  * `House 8`: **0**
  * `House 9`: **58**
  * `House 10`: **40**
  * `House 11`: **42**
  * `House 12`: **8**
* **Minimum Score**: 0
* **Maximum Score**: 58
* **Average Score**: 25.08

### C. VargaEngine
* **Input Counts**: 2 varga charts (`D9` Navamsha and `D10` Dashamamsha).
* **Output Values** (synthesis scores: `50.0 + sum(modifiers)` clamped to `[0, 100]`):
  * `sun`: **55.0** (D9 enemy dignity -5.0, D10 exalted dignity +10.0)
  * `moon`: **80.0** (D9 exalted dignity +15.0, D9 vargottama bonus +15.0)
  * `mars`: **65.0** (D9 vargottama bonus +15.0)
  * `mercury`: **50.0** (no modifiers matched)
  * `jupiter`: **65.0** (D9 vargottama bonus +15.0)
  * `venus`: **80.0** (D9 exalted dignity +15.0, D9 vargottama bonus +15.0)
  * `saturn`: **90.0** (D9 exalted dignity +15.0, D9 vargottama bonus +15.0, D10 exalted dignity +10.0)
  * `rahu`: **65.0** (D9 vargottama bonus +15.0)
  * `ketu`: **65.0** (D9 vargottama bonus +15.0)
* **Minimum Score**: 50.0
* **Maximum Score**: 90.0
* **Average Score**: 68.33

### D. AshtakavargaEngine
* **Input Counts**: SAV chart (12 houses), BAV charts (7 classical planets).
* **Output Values (SAV score per house)**:
  * `House 1`: **54.0** (26 bindus)
  * `House 2`: **50.0** (25 bindus)
  * `House 3`: **54.0** (26 bindus)
  * `House 4`: **70.0** (30 bindus)
  * `House 5`: **38.0** (22 bindus)
  * `House 6`: **76.0** (32 bindus)
  * `House 7`: **62.0** (28 bindus)
  * `House 8`: **38.0** (22 bindus)
  * `House 9`: **50.0** (25 bindus)
  * `House 10`: **54.0** (26 bindus)
  * `House 11`: **100.0** (40 bindus)
  * `House 12`: **0.0** (0 bindus)
* **Output Values (Planet BAV support score)**:
  * `sun`: **62.5** (5 bindus, modifier +5)
  * `moon`: **62.5** (5 bindus, modifier +5)
  * `mars`: **37.5** (3 bindus, modifier -5)
  * `mercury`: **25.0** (2 bindus, modifier -5)
  * `jupiter`: **62.5** (5 bindus, modifier +5)
  * `venus`: **25.0** (2 bindus, modifier -5)
  * `saturn`: **50.0** (4 bindus, modifier 0)
* **SAV Statistics**:
  * Minimum Score: 0.0 (House 12)
  * Maximum Score: 100.0 (House 11)
  * Average Score: 53.83
* **BAV Statistics**:
  * Minimum Score: 25.0 (Mercury, Venus)
  * Maximum Score: 62.5 (Sun, Moon, Jupiter)
  * Average Score: 46.43

### E. DashaEngine
* **Input Counts**: 3 active dasha levels in request payload, evaluates 2 (Mahadasha, Antardasha).
* **Output Values (Activation score)**:
  * `saturn` (Mahadasha lord): **90.56** (base_score 75.00 * multiplier 1.2075)
  * `jupiter` (Antardasha lord): **100.00** (base_score 90.00 * multiplier 1.2075 = 108.68, clamped to 100)
* **Minimum Score**: 90.56
* **Maximum Score**: 100.00
* **Average Score**: 95.28

### F. NatalPromiseEngine
* **Input Counts**: 8 domains (Marriage, Career, Wealth, Education, Children, Property, Health, Spirituality).
* **Output Values per Domain**:
  * **Marriage**: **19** (Grade: `PRESENT`)
    * *Breakdown*: `primary_house=14.00`, `support_houses=41.50`, `karaka_planet=40.00`, `house_lord=40.00`, `varga_support=50.00`, `sav_support=62.00`, `yoga_bonus=0.00`, `affliction_penalty=-15.00`
  * **Career**: **63** (Grade: `MODERATE`)
    * *Breakdown*: `primary_house=40.00`, `support_houses=21.00`, `karaka_planet=75.00`, `house_lord=75.00`, `varga_support=50.00`, `sav_support=54.00`, `yoga_bonus=11.25`, `affliction_penalty=0.00`
  * **Wealth**: **57** (Grade: `MODERATE`)
    * *Breakdown*: `primary_house=41.50`, `support_houses=49.00`, `karaka_planet=95.00`, `house_lord=40.00`, `varga_support=50.00`, `sav_support=50.00`, `yoga_bonus=0.00`, `affliction_penalty=0.00`
  * **Education**: **46** (Grade: `WEAK`)
    * *Breakdown*: `primary_house=40.00`, `support_houses=45.00`, `karaka_planet=38.00`, `house_lord=75.00`, `varga_support=50.00`, `sav_support=38.00`, `yoga_bonus=0.00`, `affliction_penalty=0.00`
  * **Children**: **57** (Grade: `MODERATE`)
    * *Breakdown*: `primary_house=40.00`, `support_houses=50.00`, `karaka_planet=77.00`, `house_lord=75.00`, `varga_support=50.00`, `sav_support=38.00`, `yoga_bonus=0.00`, `affliction_penalty=0.00`
  * **Property**: **35** (Grade: `WEAK`)
    * *Breakdown*: `primary_house=32.00`, `support_houses=41.50`, `karaka_planet=23.00`, `house_lord=35.00`, `varga_support=50.00`, `sav_support=70.00`, `yoga_bonus=0.00`, `affliction_penalty=0.00`
  * **Health**: **26** (Grade: `PRESENT`)
    * *Breakdown*: `primary_house=15.00`, `support_houses=97.33`, `karaka_planet=59.00`, `house_lord=15.00`, `varga_support=50.00`, `sav_support=54.00`, `yoga_bonus=-9.75`, `affliction_penalty=-10.00`
  * **Spirituality**: **61** (Grade: `MODERATE`)
    * *Breakdown*: `primary_house=33.00`, `support_houses=40.00`, `karaka_planet=95.00`, `house_lord=95.00`, `varga_support=50.00`, `sav_support=50.00`, `yoga_bonus=0.00`, `affliction_penalty=0.00`
* **Minimum Score**: 19 (Marriage)
* **Maximum Score**: 63 (Career)
* **Average Score**: 45.50

### G. MasterProbabilityEngine
* **Input Counts**: 7 synthesis factors (Natal Promise 40%, Planet Strength 15%, House Strength 10%, Rasi Strength 10%, Varga Validation 10%, Dasha Activation 10%, Transit Trigger 5%).
* **Output Breakdown**:
  * `natal_promise`: **45.50** (Weight: 40%)
  * `planet_strength`: **37.22** (Weight: 15%)
  * `house_strength`: **25.08** (Weight: 10%)
  * `rasi_strength`: **51.92** (Weight: 10%)
  * `varga_validation`: **68.33** (Weight: 10%)
  * `dasha_activation`: **95.00** (Weight: 10%)
  * `transit_trigger`: **50.00** (Weight: 5% — neutral stub fallback)
* **Final Synthetic Score**: **50** (Grade: `GOOD`)
* **Minimum Factor Score**: 25.08 (House Strength)
* **Maximum Factor Score**: 95.00 (Dasha Activation)
* **Average Factor Score**: 53.29

---

## 2. Which Engine First Produces Incorrect Values?

### **YogaEngine** (Calculated at Step 3.5 in PipelineRunner)

The **YogaEngine** is the first calculation module in the pipeline execution flow that produces incorrect values.

#### **Evidence 1: Missing Exaltation Shasha Yoga**
* Saturn is **Exalted** in **Kendra** (House 7) in the Raju chart. This represents a classic **Shasha Yoga** (one of the Pancha Mahapurusha Yogas).
* However, `YogaEngine` does not list `"Shasha Yoga"` in `active_yogas`.
* **Root Cause**: In `app/engines/yoga_engine.py` (lines 102-104), the engine attempts to read the planet dignity from `planet_results` (the output of `PlanetStrengthEngine`):
  ```python
  dignity = p_results.get(p, {}).get("dignity", "neutral")
  ```
  However, the `PlanetStrengthEngine` output structure does **NOT** contain a top-level `"dignity"` field. Consequently, the dignity defaults to `"neutral"` for all planets, failing the requirement `dignity in ["exalted", "own_sign", "moolatrikona"]`.

#### **Evidence 2: Broken Neecha Bhanga Raja Yoga Detection**
* Mercury (`Budha`) is **Debilitated** in D1, representing a candidate for Neecha Bhanga Raja Yoga.
* `YogaEngine` does not identify Neecha Bhanga Raja Yoga because it checks:
  ```python
  if res.get("dignity") == "debilitated":
  ```
  Since `res` (the planet strength result) does not contain a `"dignity"` key, this condition evaluates to `False` for all debilitated planets.

---

### **VargaEngine** (Calculated at Step 4 in PipelineRunner)

 the **VargaEngine** is the second calculation module that produces incorrect values.

#### **Evidence 1: Mismatched Dignity lookup due to space characters**
* In `canonical_content.json`, the dignity for Mars, Mercury, Jupiter, and Venus in `D9` and `D10` is specified as `"Own House"`.
* When parsed, this is converted to lowercase as `"own house"`.
* In `app/engines/varga_engine.py`, the lookup fails to match `"own_house"` (with underscore) inside the constants `D9_SCORES` and `D10_SCORES`:
  ```python
  d9_score = self.D9_SCORES.get(d9_dignity, 0.0)
  ```
  As a result, Mars, Mercury, Jupiter, and Venus are assigned a dignity modifier of `0.0` instead of their proper values (+10.0 and +5.0).
* Under Mars, `varga_results` only shows `{'D9_vargottama_bonus': 15.0}` instead of its proper modifiers.

#### **Evidence 2: Incompatible Output Structure for Downstream Engines**
* `VargaEngine.evaluate` returns a flat dictionary keyed by **planet name** (e.g. `{"sun": {...}}`).
* However, downstream consumers `RasiStrengthEngine` and `NatalPromiseEngine` expect a varga-chart-centric dictionary structure:
  * In `RasiStrengthEngine._factor_varga`:
    ```python
    varga_planets = varga_outputs.get(varga_id, {}).get("planets", {})
    ```
    where `varga_id` is `"D9"` or `"D10"`.
  * In `NatalPromiseEngine._varga_score`:
    ```python
    varga = varga_results.get(varga_id, {})
    ```
* Because `varga_results` is not keyed by varga ID, these downstream engines receive empty dictionaries `{}` and default to the neutral fallback score of **`50.0`** for all varga calculations (as seen in `varga_support=50.0` for all 8 domains).
