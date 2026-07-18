# Root Cause Analysis: Natal Promise Engine Returns Empty Result

**Date:** 2026-07-18  
**Classification:** Root Cause Analysis (Read-Only)  
**Repository:** D:\vedic-ai-golden-master

---

## Observed Behavior

- `NatalPromiseEngine.evaluate()` returns empty dict `{}` for all 8 domains
- Downstream: `MasterProbabilityEngine` returns 0 scores, `QuestionEngine` fails
- Test `test_all_8_domains_present` in `test_natal_promise_engine.py` would fail
- Real chart test `test_real_charts.py::TestRajuRealChart::test_all_8_natal_domains_scored` fails

---

## Expected Behavior

`NatalPromiseEngine.evaluate()` should return 8 domains with:
```python
{
    "marriage": {"score": int, "promise": str, "breakdown": {...}, "karaka": str, ...},
    "career": {...},
    "wealth": {...},
    "education": {...},
    "children": {...},
    "property": {...},
    "health": {...},
    "spirituality": {...}
}
```

---

## Execution Trace

### 1. PipelineRunner.process() → NatalPromiseEngine.evaluate()
**File:** `backend/app/pipeline_runner.py`, lines 177-186

```python
natal_results = self.natal_engine.evaluate(
    planet_results    = planet_results,
    house_results     = house_results,
    rasi_results      = rasi_results,
    varga_results     = varga_results,
    av_results        = av_results,
    yoga_results      = yoga_results,
    normalized_houses = normalized_payload.get("houses", {}),
    normalized_vargas = normalized_payload.get("vargas", {})
)
engine_outputs["natal_promise"] = natal_results
```

### 2. NatalPromiseEngine.evaluate() → _score_domain()
**File:** `backend/app/engines/natal_promise_engine.py`, lines 35-58

```python
def evaluate(self, ...) -> Dict[str, Any]:
    result = {}
    for domain in self.domains:
        result[domain] = self._score_domain(...)
    return result
```

**Key initialization (lines 24-33):**
```python
def __init__(self, calibration=None):
    if calibration is None:
        from app.calibration.calibration_manager import CalibrationManager
        calibration = CalibrationManager()
    self.config   = calibration.natal_promise.get("DOMAIN_CONFIG", {})   # ← EMPTY!
    self.domains  = list(self.config.keys())                            # ← EMPTY LIST!
    self.karaka   = calibration.natal_promise.get("DOMAIN_KARAKA", {})
    self.grades   = calibration.natal_promise.get("NATAL_PROMISE_GRADES", [])
    self.bonuses  = calibration.natal_promise.get("DOMAIN_BONUSES", {})
    self.sign_lord_map = calibration.rasi_strength.get("SIGN_LORD_MAP", {})
```

**Since `self.domains` is empty list, the for-loop never executes, returns `{}`**

---

## Root Cause: CalibrationManager.natal_promise Property Returns Incomplete Data

**File:** `backend/app/calibration/calibration_manager.py`, lines 434-449

```python
@property
def natal_promise(self) -> Dict[str, Any]:
    """Return natal promise calibration in engine-expected format."""
    try:
        from app.config.astrology_constants import NATAL_PROMISE_GRADES, DOMAIN_KARAKA
        return {
            "NATAL_PROMISE_GRADES": NATAL_PROMISE_GRADES,
            "DOMAIN_KARAKA": DOMAIN_KARAKA
        }
    except ImportError:
        pass

    # Fallback to legacy flat format
    legacy_data = self.active_profile.get("natal_promise", {})
    return legacy_data
```

### The Problem

| Engine Expects | CalibrationManager Returns | Source |
|----------------|---------------------------|--------|
| `DOMAIN_CONFIG` | ❌ **MISSING** | Constants has it, but not returned |
| `DOMAIN_KARAKA` | ✅ Present | Constants |
| `NATAL_PROMISE_GRADES` | ✅ Present | Constants |
| `DOMAIN_BONUSES` | ❌ **MISSING** | Constants has it, but not returned |
| `SIGN_LORD_MAP` | From `rasi_strength` property | Works |

**The constants file (`astrology_constants.py`) HAS all required data:**
- `DOMAIN_CONFIG` (lines 299-389) ✅
- `DOMAIN_KARAKA` (lines 286-295) ✅
- `NATAL_PROMISE_GRADES` (lines 278-283) ✅
- `DOMAIN_BONUSES` (lines 395-407) ✅

**But `CalibrationManager.natal_promise` property only returns 2 of 4 required keys!**

---

## Dependency Analysis

### Upstream (Data Sources)
| Component | Status | Notes |
|-----------|--------|-------|
| `astrology_constants.py` | ✅ Complete | All 4 required dicts present |
| `v1.0_current.json` profile | ✅ Complete | Has "domains", "grades", "bonuses" |
| `CalibrationManager` | ❌ Broken | `natal_promise` property incomplete |

### Downstream (Affected Systems)
| System | Impact | Severity |
|--------|--------|----------|
| `NatalPromiseEngine` | Returns `{}` — no domains | 🔴 Critical |
| `MasterProbabilityEngine` | `natal_promise` factor = 0 | 🔴 Critical |
| `QuestionEngine` | No domain scores for routing | 🔴 Critical |
| `PipelineRunner` | `engine_outputs["natal_promise"] = {}` | 🔴 Critical |
| Real chart tests | All 8 domain assertions fail | 🔴 Critical |
| Formula Evaluator | Missing natal_promise inputs | 🟠 High |

---

## Root Cause Statement

**The `CalibrationManager.natal_promise` property returns only 2 of 4 required configuration keys from constants (`NATAL_PROMISE_GRADES`, `DOMAIN_KARAKA`), omitting `DOMAIN_CONFIG` and `DOMAIN_BONUSES` which are also defined in `astrology_constants.py`. This causes `NatalPromiseEngine.__init__` to initialize `self.config = {}` and `self.domains = []`, making `evaluate()` return an empty dict.**

---

## Affected Code Locations

| File | Line | Issue |
|------|------|-------|
| `backend/app/calibration/calibration_manager.py` | 434-449 | `natal_promise` property incomplete |
| `backend/app/engines/natal_promise_engine.py` | 28-29 | `self.config` and `self.domains` become empty |

---

## Recommended Fix Approach (High-Level)

**Option A: Fix CalibrationManager (Recommended)**
Update `CalibrationManager.natal_promise` property to return all 4 required keys from constants:
```python
from app.config.astrology_constants import (
    NATAL_PROMISE_GRADES, DOMAIN_KARAKA, 
    DOMAIN_CONFIG, DOMAIN_BONUSES
)
return {
    "NATAL_PROMISE_GRADES": NATAL_PROMISE_GRADES,
    "DOMAIN_KARAKA": DOMAIN_KARAKA,
    "DOMAIN_CONFIG": DOMAIN_CONFIG,
    "DOMAIN_BONUSES": DOMAIN_BONUSES
}
```

**Option B: Fix NatalPromiseEngine**
Change engine to use keys that CalibrationManager actually returns (but this breaks the expected interface).

**Option C: Merge profile + constants**
Have CalibrationManager merge profile data with constants for all keys.

---

## Severity Assessment

| Dimension | Rating |
|-----------|--------|
| **Release Blocking** | 🔴 YES — V1.0 cannot release |
| **Downstream Impact** | 🔴 5+ systems affected |
| **Fix Complexity** | 🟢 Low — single property fix |
| **Risk of Regression** | 🟢 Low — constants already correct |

---

## Next Steps

1. **Immediate:** Fix `CalibrationManager.natal_promise` property to return all 4 keys
2. **Verify:** Run `test_natal_promise_engine.py` — should pass all 17 tests
3. **Verify:** Run `test_real_charts.py::TestRajuRealChart` — should pass domain assertions
4. **Regression:** Run full test suite — should reduce 102 failures significantly

---

**Ready for Chief Architect Review:** ✅ YES  
**Classification:** ROOT CAUSE ANALYSIS — READ ONLY  
**No code modified during this investigation.**