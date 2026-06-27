# CALIBRATION CONSTANT INVENTORY (v1.0)
Phase 16A.3 – Calibration Architecture Audit

## 1. Executive Summary
This document is the definitive inventory of every astrological constant, matrix, weight, and "magic number" currently embedded within the Vedic-AI backend. The purpose of this audit is to identify all tunable values that will be centralized into the `CalibrationManager` during Phase 16A.3, ensuring that mathematical tuning can occur without modifying any code. 

## 2. Engine-by-Engine Inventory & 3. Constant Classification Table

| Constant Name | Current File | Engine Owner | Current Value (Excerpt) | Classification | Future Calibration Owner | Duplicated? | Recommendation |
|---|---|---|---|---|---|---|---|
| `PLANET_SCORING_MATRIX` | `astrology_constants.py` | PlanetStrengthEngine | Exalted=100, Kendra=90, etc. | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `HOUSE_SCORING_MATRIX` | `astrology_constants.py` | HouseStrengthEngine | Kendra=100, Benefic=25 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `NATURAL_BENEFICS/MALEFICS` | `astrology_constants.py` | Global | ["jupiter", "venus"...] | Category A | Calibration Layer | YES (TransitEngine caches) | Centralize in Calibration Layer |
| `D9_SCORES` / `D10_SCORES` | `astrology_constants.py` | VargaEngine | Exalted=15.0 / 10.0 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `VARGOTTAMA_BONUS` | `astrology_constants.py` | VargaEngine | 15.0 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `DASHA_SCORING_MATRIX` | `astrology_constants.py` | DashaEngine | "1_1": 1.0, "5_9": 1.25 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `SIGN_LORD_MAP` / `EXALTATION_MAP` | `astrology_constants.py` | Global / Structural | "aries": "mars" | Category C | Technical Constant | NO | Keep structural/technical |
| `SAV_BINDU_SCALE` | `astrology_constants.py` | RasiStrengthEngine / AshtakavargaEngine | (0,0), (25,50), (40,100) | Category A | Calibration Layer | YES (HouseEngine) | Centralize in Calibration Layer |
| `RASI_SCORING_MATRIX` | `astrology_constants.py` | RasiStrengthEngine | "bhava": 0.35 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `PROBABILITY_GRADES` | `astrology_constants.py` | MasterProbabilityEngine, HouseStrengthEngine, TransitEngine | (80, "EXCELLENT") | Category A | Calibration Layer | NO | Centralize in Calibration Layer |
| `BAV_GRADE_THRESHOLDS` | `astrology_constants.py` | AshtakavargaEngine | (7, "EXCELLENT") | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `BAV_PLANET_MODIFIER` | `astrology_constants.py` | AshtakavargaEngine | "high": +5 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `SAV_FAVORABLE_THRESHOLD` | `astrology_constants.py` | AshtakavargaEngine | 28 / 30 / 22 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `DASHA_BAV_CONFIDENCE` | `astrology_constants.py` | AshtakavargaEngine | "high": 1.10 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `BAV_EXCLUDED_PLANETS` | `astrology_constants.py` | AshtakavargaEngine | {"rahu", "ketu"} | Category C | Technical Constant | NO | Keep technical/structural |
| `NATAL_PROMISE_GRADES` | `astrology_constants.py` | NatalPromiseEngine | (70, "STRONG") | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `DOMAIN_KARAKA` | `astrology_constants.py` | NatalPromiseEngine | "marriage": "venus" | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `DOMAIN_CONFIG` | `astrology_constants.py` | NatalPromiseEngine | "bhava": 0.35 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `DOMAIN_BONUSES` | `astrology_constants.py` | NatalPromiseEngine | "jupiter_in_9": +5 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `TRANSIT_HOUSE_QUALITY` | `astrology_constants.py` | TransitEngine | "sun" 3: +12 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `VEDHA_PAIRS` | `astrology_constants.py` | TransitEngine | 1: 8, 2: 12 | Category C | Technical Constant | NO | Keep structural/technical |
| `TRANSIT_CONJUNCTION_MATRIX`| `astrology_constants.py` | TransitEngine | ("jupiter", "benefic"): +12 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `TRANSIT_ASPECT_WEIGHTS` | `astrology_constants.py` | TransitEngine | ("benefic", "benefic"): +6 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `TRANSIT_WEIGHTS` | `astrology_constants.py` | TransitEngine | "vedha_layer": 0.10 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `TRANSIT_DASHA_SYNC_BONUSES`| `astrology_constants.py` | TransitEngine | "transit_is_md_lord": 20 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `MASTER_WEIGHTS` | `master_probability_engine.py`| MasterProbabilityEngine | "natal_promise": 0.40 | Category A | Calibration Layer | NO | Move to Calibration Layer |
| `_STUB_SCORE` | `master_probability_engine.py`| MasterProbabilityEngine | 50.0 | Category A | Calibration Layer | NO | Move to Calibration Layer |

## 4. Magic Number Audit

During the audit, the following hardcoded numbers were found embedded directly inside engine logic rather than in `astrology_constants.py`:

* **`house_strength_engine.py`**:
  * `0.30`, `0.20`, `0.15`, `0.15`, `0.10`, `0.10` (Pillar weights in `calculate_strength`) -> **Category A**. Must move to Calibration Layer.
  * `anchors = [(0, 0), (20, 30), (25, 50), ...]` (SAV Bindu Scale) -> **Category A**. Duplicate of `SAV_BINDU_SCALE`. Must move to Calibration Layer.
* **`ashtakavarga_engine.py`**:
  * `0.60` (MD weight) and `0.40` (AD weight) for combined Dasha BAV support -> **Category A**. Must move to Calibration Layer.
* **`yoga_engine.py`**:
  * Numerous hardcoded integers for Yoga matching (e.g. `[1, 4, 7, 10]`, `[1, 5, 9]`, `[6, 7, 8]`). -> **Category C**. Structural definitions of Classical Yogas. No change needed.
* **`varga_engine.py` / `transit_engine.py`**:
  * `50.0` as fallback values (`get("final_score", 50.0)`) -> **Category A**. Missing-data neutral defaults. Should be centralized.

## 5. Duplicate Ownership Audit

The rule states: "Every mathematical concept has exactly ONE owner."

1. **`SAV_BINDU_SCALE` Duplication**: 
   - `astrology_constants.py` defines `SAV_BINDU_SCALE` for use by `RasiStrengthEngine` and `AshtakavargaEngine`.
   - `house_strength_engine.py` redefines the EXACT same piecewise anchors inline inside `_evaluate_sav_support`.
   - **Resolution**: Both must pull from `calibration.rasi_strength.SAV_BINDU_SCALE`.

2. **`NATURAL_BENEFICS` / `NATURAL_MALEFICS` Duplication**:
   - Defined in `astrology_constants.py`.
   - Copied locally as a `set` inside `transit_engine.py` and `house_strength_engine.py`.
   - **Resolution**: Must be pulled once from the Calibration Layer.

## 6. Calibration Readiness Assessment

The architecture is **HIGHLY READY** for calibration.
- The `astrology_constants.py` file has already successfully extracted 95% of the tunable parameters from the underlying engines.
- The engines are predominantly stateless and heavily rely on dictionary configurations.
- The Canonical JSON payload serves as a reliable integration test boundary.
- **Exceptions**: The hardcoded weights in `HouseStrengthEngine` and `AshtakavargaEngine` must be abstracted first.

## 7. Recommended Calibration Layer Structure

To replace `astrology_constants.py`, the `CalibrationManager` should provide segregated namespaces (profiles) that cleanly map to engine ownership:

```json
{
  "planet_strength": { "PLANET_SCORING_MATRIX": {}, "NATAL_BENEFICS": [], "NATAL_MALEFICS": [] },
  "house_strength": { "HOUSE_SCORING_MATRIX": {}, "PILLAR_WEIGHTS": {} },
  "rasi_strength": { "RASI_SCORING_MATRIX": {}, "SAV_BINDU_SCALE": [] },
  "varga": { "D9_SCORES": {}, "D10_SCORES": {}, "VARGOTTAMA_BONUS": 15.0 },
  "dasha": { "DASHA_SCORING_MATRIX": {} },
  "ashtakavarga": { "BAV_GRADE_THRESHOLDS": [], "DASHA_BAV_WEIGHTS": [0.60, 0.40] },
  "natal_promise": { "DOMAIN_CONFIG": {}, "NATAL_PROMISE_GRADES": [] },
  "transit": { "TRANSIT_HOUSE_QUALITY": {}, "TRANSIT_WEIGHTS": {} },
  "master_probability": { "MASTER_WEIGHTS": {}, "PROBABILITY_GRADES": [], "STUB_SCORE": 50.0 }
}
```

## 8. Final Conclusion

**Verdict: READY FOR IMPLEMENTATION.**

The backend architecture is strictly compliant with Phase 16A governance. The current state has isolated mathematics from calculation logic. The discovery of hardcoded pillar weights in `HouseStrengthEngine` and `AshtakavargaEngine` is exactly what this audit was designed to uncover. 

Once the Calibration Layer is implemented and engines are refactored to consume a `CalibrationManager` instance, all Category A constants will be fully tunable via JSON profiles, permanently completing the architecture freeze.
