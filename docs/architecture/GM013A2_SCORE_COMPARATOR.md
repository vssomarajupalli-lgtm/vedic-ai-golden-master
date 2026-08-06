# GM-013A.2 — SCORE COMPARATOR (PRE → POST ADR-004)

**Horoscope:** Raju (14.05.1980), target 2026-01-15, canonical data `extracted_json/raju_canonical_content.json`.

## Intentional changes (all from canonical vocabulary migration)

Per ADR-004, dignity maps previously compared **English** keys against **Sanskrit** `planet.sign`,
so *every* dignity resolved to `neutral` and `_calculate_longitude` returned degree-only (English
`SIGNS_IN_ORDER.index("Makara")` → ValueError). Post-fix these are mathematically correct.

### Dignity (pre: ALL neutral → post: correctly derived)
| Planet | Sign | PRE | POST |
|--------|------|-----|------|
| sun | Kanya | neutral | neutral |
| moon | Makara | neutral | neutral |
| mars | Dhanus | neutral | neutral |
| mercury | Kanya | neutral | **exalted** |
| jupiter | Dhanus(9) | neutral | neutral |
| venus | Simha | neutral | neutral |
| saturn | Mesha | neutral | **debilitated** |
| rahu | Kumbha | neutral | neutral |
| ketu | Simha | neutral | neutral |

### Planet strengths (final_score)

| Planet | PRE | POST | Note |
|--------|-----|------|------|
| sun | 49 | 49 | unchanged |
| moon | 57 | 57 | unchanged |
| mars | 55 | 55 | unchanged |
| mercury | 58 | **71** | now exalted (Kanya) |
| jupiter | 60 | 60 | unchanged |
| venus | 61 | 61 | unchanged |
| saturn | 53 | **40** | now debilitated (Mesha) |
| rahu | 58 | 58 | unchanged |
| ketu | 58 | 58 | unchanged |

### House strengths
Unchanged (48/42/... same as pre).

### Rasi strengths (pre English keys → post Sanskrit keys)
```
PRE:  aries 34, taurus 34, ..., scorpio 35 ...
POST: Mesha 34, Vrishabha 34, Mithuna 38, Karkata 34, Simha 33, Kanya 42,
      Tula 34, Vrishchika 35, Dhanus 30, Makara 34, Kumbha 28, Meena 34
```
Keys migrated to canonical; small score deltas follow from correct dignity/lord resolution.

### Master probability
```
PRE:  score null, grade WEAK
POST: score null, grade WEAK   (master score aggregation unchanged)
```

### Question engine / Mandali
Unchanged from pre-baseline for this fixture (question_engine not surfaced; Mandali grid structurally identical, canonical rasi names only).

### Transit
```
PRE:  activation_score 50
POST: activation_score 58   (upstream planet strength feeds transit house; dignity change drives delta)
```

## Differences explanation

Every delta is attributable to one ADR-004 behavior: **dignity is no longer always neutral**.
Mercury (Kanya = exaltation) rose, Saturn (Mesha = debilitation) dropped. All downstream
aggregations ("", houses, transit/master) reflect only this correction. No engine weights,
formulas, or responsibilities were changed.

## Regression status (full backend suite)

- **Resolved by ADR-004:** the English/Sanskrit vocabulary test group (json_normalizer,
  rasi_strength, ashtakavarga, ephemeris, functional_nature) is now fully green.
- **Still failing (pre-existing, verified via `git stash` — the identical 20 failures occur with
  and without ADR-004 applied):** Mandali default-nakshatra `RegistryAccessError` (appears in
  pipeline/Mandali integration), ReportBuilder `questions` signature, FastAPI `target_date_utc`
  contract, birth-position boundary math, formula-pipeline nakshatra/pada gap. These are out of
  ADR-004 scope (tracked in GM-013A.3 planning).
- **New failures caused by ADR-004:** 0.
- Final: **719 passed, 20 failed, 1 skipped.**