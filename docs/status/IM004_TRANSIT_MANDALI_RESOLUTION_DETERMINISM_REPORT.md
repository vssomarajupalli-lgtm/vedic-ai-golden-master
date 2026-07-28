# IM-004 TransitMandaliResolution Determinism Report

## Executive Summary

**Status: PASSED** ✅

The TransitMandaliResolution capability (Capability 7.4) has been verified to produce deterministic output. Identical inputs consistently produce identical outputs across multiple executions.

---

## Test Methodology

### Determinism Test Protocol
- **Test Function**: `test_deterministic_output` in `test_transit_mandali_resolution.py`
- **Iterations**: 10 consecutive executions with identical inputs
- **Input Data**: Fixed transit planet data (Saturn in Shatabhisha Pada 3)
- **Mandali Grid**: Fixed grid centered on Dhanishta Pada 2 (Moon = Absolute Pada 90)
- **Verification**: Deep equality comparison of all output fields

### Test Input
```json
{
  "planet": "Saturn",
  "rasi": "Kumbha",
  "nakshatra": "Shatabhisha",
  "pada": 3,
  "house_from_moon": 2,
  "interpretation": "Saturn in Shatabhisha"
}
```

### Mandali Grid Configuration
- **Moon Nakshatra**: Dhanishta
- **Moon Pada**: 2
- **Moon Absolute Pada**: 90
- **Grid Centers**: 90, 99, 108, 9, 18, 27, 36, 45, 54, 63, 72, 81

---

## Results

### Execution Consistency
| Iteration | Mandali Number | Center Pada | Center Nakshatra | Classical House | Mandali House | Status |
|-----------|----------------|-------------|------------------|-----------------|---------------|--------|
| 1 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 2 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 3 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 4 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 5 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 6 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 7 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 8 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 9 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |
| 10 | 2 | 99 | Purva Bhadrapada | 2 | 2 | ✅ Match |

### Field-by-Field Verification
All output fields verified identical across 10 iterations:

| Field | Type | Consistent |
|-------|------|------------|
| `planet` | string | ✅ |
| `original.rasi` | string | ✅ |
| `original.nakshatra` | string | ✅ |
| `original.pada` | integer | ✅ |
| `mandali.number` | integer | ✅ |
| `mandali.name` | string | ✅ |
| `mandali.center_nakshatra` | string | ✅ |
| `mandali.center_pada` | integer | ✅ |
| `house_from_moon_classical` | integer | ✅ |
| `house_from_moon_mandali` | integer | ✅ |
| `interpretation_ref` | string | ✅ |

---

## Determinism Guarantees

### Source of Determinism
1. **CanonicalReferenceData** - Singleton registry loaded once at startup (CRD-01)
2. **NakshatraPadaResolver** - Pure function: (nakshatra, pada) → absolute_pada (NPR-01 to NPR-05)
3. **MandaliGridConstruction** - Pure arithmetic: moon_pada + (N-1)×9 mod 108 (MGC-01 to MGC-07)
4. **TransitMandaliResolution** - Pure lookup: absolute_pada → mandali via grid (TMR-01 to TMR-05)

### No Sources of Non-Determinism
- ❌ No random number generation
- ❌ No time-dependent operations
- ❌ No external API calls
- ❌ No file I/O during resolution
- ❌ No global mutable state
- ❌ No thread-local storage
- ❌ No hash randomization dependencies

### Mathematical Determinism
The core resolution is a pure mathematical function:
```
transit_absolute_pada = registry_lookup(transit_nakshatra, transit_pada)
mandali_number = find_mandali_containing(transit_absolute_pada, mandali_grid)
```
Both operations are deterministic lookups with no branching on external state.

---

## Regression Test Results

### Full Test Suite
```
============================= test session starts =============================
collected 20 items

backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_convenience_function PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_custom_dependency_injection PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_deterministic_output PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_invalid_nakshatra_raises_error PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_invalid_pada_raises_error PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_invalid_pada_zero_raises_error PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_mandali_name_format PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_output_structure_complete PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr01_transit_absolute_pada_resolution PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr01_various_transit_positions PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr02_no_overlaps PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr02_unique_mandali_assignment PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr03_exactly_one_mandali_per_pada PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr04_multiple_planets_preserved PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr04_original_values_preserved PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr05_classical_house_preserved PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolution::test_tmr05_various_classical_houses PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolutionIntegration::test_uses_canonical_reference_data PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolutionIntegration::test_uses_mandali_grid_construction PASSED
backend/tests/test_transit_mandali_resolution.py::TestTransitMandaliResolutionIntegration::test_uses_nakshatra_pada_resolver PASSED

=================== 20 passed, 132 subtests passed in 0.17s ===================
```

---

## Conclusion

**TransitMandaliResolution is fully deterministic.**

- All 20 unit tests pass
- 132 subtests pass
- 10/10 determinism iterations produce identical output
- No sources of non-determinism in the code path
- Complies with governance rule CGP-03 (Determinism) and TMR-01 through TMR-05

**Recommendation**: Approved for production use. No further determinism testing required.

---

*Report Generated: 2026-07-26*
*Capability: 7.4 TransitMandaliResolution*
*Governance: GOCHARA_MANDALI_GOVERNANCE_v1.md Section 7.4*