# GM-013A.2 — PRE-IMPLEMENTATION BASELINE

**Date:** 2026-08-06
**Scope:** ADR-004 Canonical Representation Migration (English→Sanskrit rasi vocabulary)
**Fixture:** `extracted_json/raju_canonical_content.json` (Raju, DOB 14.05.1980, target 2026-01-15)
**Run mode:** synthetic ephemeris fallback (pyswisseph not installed)

## Observed pre-migration defects

| Area | Value | Defect |
|------|-------|--------|
| All planet dignities | `neutral` | EXALTATION/OWN/DEBILITATION maps are English; normalizer emits Sanskrit → never match |
| ascendant_sign | `aries` | normalizer `_normalize_metadata` fallback is English |
| `_calculate_longitude` | `27.7572` for moon | English `SIGNS_IN_ORDER.index("Makara")` ⇒ ValueError ⇒ returns degree only (WRONG longitude) |
| rasi_strength keys | English | dictionary keys are English in output |

## Baseline captured outputs

### Dignity values (all wrong)
```
sun: neutral, moon: neutral, mars: neutral, mercury: neutral, jupiter: neutral,
venus: neutral, saturn: neutral, rahu: neutral, ketu: neutral
```

### Planet strengths (final_score)
```
sun: 49, moon: 57, mars: 55, mercury: 58, jupiter: 60, venus: 61, saturn: 53,
rahu: 58, ketu: 58
```

### House strengths (final_score)
```
H2: 48, H3: 42, H4: 42, H6: 48, H8: 42, H9: 38, H10: 42, H11: 42, H12: 42
```

### Rasi strengths (final_score)
```
aries: 35, taurus: 34, gemini: 34, cancer: 34, leo: 34, virgo: 34,
libra: 34, scorpio: 35, sagittarius: 34, capricorn: 34, aquarius: 34, pisces: 34
```

### Master probability
```
score: null, grade: WEAK
```

### Question engine
```
null (no active question surfaced in this run)
```

### Transit
```
activation_score: 50, grade: GOOD
supporting_factors: dasha_transit_sync_md 16.8, sun_h10 12, moon_h7 12,
 mercury_h2 12, jupiter_h5 12, venus_h12 12, ketu_h11 12, dasha_transit_sync_ad 10.1
```

### Mandali
Center (Shravana) grid present; current_mandali name "Mandali 8".

## Full raw output
Stored at run time in `GM013A2_PRE_IMPLEMENTATION_BASELINE.md` capture directory (see comparator for score deltas).

**Note:** This baseline documents the wrong-matched dignities and broken longitude that ADR-004 migration is expected to correct. Intentional score changes after migration are the dignities + longitudes; the rest of the engine outputs are expected to remain stable.