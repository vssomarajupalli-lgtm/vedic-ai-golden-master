# CURRENT_MANDALI_IMPLEMENTATION_BASELINE.md

## Investigation Report — Rāśi Mandali / Gochara / Transit System as-is

- **Mode**: READ-ONLY investigation. No source, test, configuration, formula, or architecture was modified.
- **Repository**: `D:\vedic-ai-golden-master`
- **Branch inspected**: `gm-017.6-print-export-unification`
- **Date of inspection**: 2026-08-12
- **Sole existing working-tree change (pre-existing, not introduced here)**: `M start.bat`

> This document describes exactly what the current code **does**. It does not compare, endorse, or judge against any newly proposed Mandali model. No implementation work is proposed here.

---

## 1. Executive Summary

The repository implements a **Moon-centered 12-Mandali Gochara system** governed by
`docs/GOCHARA_MANDALI_GOVERNANCE_v1.md` ("Model A"). The implementation is a
**pada-based** system:

- A **12-Mandali grid** is constructed by splitting the 108 Nakshatra Padas into 12
  consecutive 9-pada arcs, **centered on the natal Moon's absolute pada** (Mandali 1
  center = Moon's pada, subsequent centers at +9 padas modulo 108).
  Owner: `MandaliGridConstruction` / `Mandali` / `MandaliGrid`
  (`backend/app/engines/mandali_grid_construction.py`).
- Each **transit planet** is resolved to a Mandali number by looking up its
  **Nakshatra + Pada** (or, at runtime, its **longitude → absolute pada**) in that
  grid. Owner: `TransitMandaliResolver` (`transit_mandali_resolution.py`) with pure
  registry resolution via `NakshatraPadaResolver` (`nakshatra_pada_resolver.py`).
- **Saturn's special periods** (Sade Sati / Elinati Shani / Ashtama Shani) are
  projected as **Rasi-based windows** with **fixed 30-month (900-day) arithmetic**
  anchored on a Canonical Saturn `start_date` — *not* ephemeris, and *not* derived
  independently from the Mandali grid. Owner: `LifetimeCycleProjector`
  (`lifetime_cycle_projection.py`) + `BirthPositionDetector`
  (`birth_position_detection.py`).
- The **scoring TransitEngine** (`transit_engine.py`) consumes, in the live pipeline,
  the **Mandali numbers as "houses"** (`t_houses`), i.e. the Moon-relative Mandali
  house, and produces a single `activation_score` [0-100] feeding the
  MasterProbabilityEngine 5% weight.
- **Ephemeris** (Swiss Ephemeris, Lahiri sidereal) exists *outside* Model A and is
  used at runtime only to *build* the Canonical-format `current_transit` list
  (`EphemerisService` + `MandaliTransitAdapter`). The Universal Mandali Engine itself
  performs no astronomy.
- A **frozen golden-master test** (`test_transit_golden_master.py`) pins the entire
  longitude → pada → nakshatra → mandali → chart-box → stay-dates → transition chain
  to Swiss-Ephemeris-verified values.

Pre-existing test status: all Mandali/Gochara/Transit tests **pass** (143 + 217
subtests in the core capability suites; 44 collected across the transit suites with
1 explicit pre-existing skip). One unrelated pre-existing failure exists in
`test_report_builder.py::TestReportBuilder::test_extracts_correct_data` (a
`client_info` expectation, no Mandali/Gochara involvement).

---

## 2. Files Inspected

### Backend engines (`backend/app/engines/`)
| File | Role |
|------|------|
| `mandali_generator.py` | Compatibility facade (longitude methods) |
| `mandali_grid_construction.py` | Capability 7.3 — grid construction (canonical owner) |
| `transit_mandali_resolution.py` | Capability 7.4 — transit → Mandali |
| `nakshatra_pada_resolver.py` | Capability 7.2 — (Nakshatra, Pada) → absolute pada |
| `canonical_reference_data.py` | Capability 7.1 — registry loader/singleton |
| `universal_mandali_engine.py` | Capability 7.7 — composition engine |
| `lifetime_cycle_projection.py` | Capability 7.5 — Saturn cycle projection |
| `birth_position_detection.py` | Capability 7.6 — birth position classification |
| `transit_engine.py` | Deterministic Gochara scoring engine |
| `mandali_transit_adapter.py` | Ephemeris → Canonical `current_transit` adapter + date scanning |
| `master_probability_engine.py` | Consumes `transit.activation_score` (5%) |

### Pipeline / normalizer / builders / formatters / reports
- `backend/app/pipeline_runner.py` — wiring (Option A path)
- `backend/app/parsers/json_normalizer.py` — natal planet normalization incl. `longitude`
- `backend/app/builders/mandali_placement_factory.py`
- `backend/app/builders/mandali_chart_layout_builder.py`
- `backend/app/builders/transition_summary_builder.py`
- `backend/app/formatters/display_formatter.py` (`format_gochara_report`)
- `backend/app/reports/builder.py`, `backend/app/reports/schemas.py`
- `backend/app/utils/ephemeris_service.py`

### Schemas (`backend/app/schemas/`)
`mandali_response.py`, `natal_chart.py`, `current_chart.py`, `transition_summary.py`,
`mandali_chart_cell.py`

### Config registries (`backend/app/config/`)
`nakshatra_pada_registry.json` (108 entries), `nakshatra_rasi_registry.json` (108
mappings), `rasi_sequence_registry.json` (12), `astrology_constants.py` (transit
sub-system constants), `question_registry.json`

### Tests (`backend/tests/`)
`test_mandali_generator.py`, `test_mandali_grid_construction.py`,
`test_transit_mandali_resolution.py`, `test_nakshatra_pada_resolver.py`,
`test_canonical_reference_data.py`, `test_lifetime_cycle_projection.py`,
`test_birth_position_detection.py`, `test_gochara_integration.py`,
`test_transit_engine.py`, `test_transit_golden_master.py`,
`test_ephemeris_service.py`, `test_pipeline_runner.py`, `test_real_charts.py`,
`test_report_builder.py`

### Governance / docs / fixtures
- `docs/GOCHARA_MANDALI_GOVERNANCE_v1.md` (frozen normative spec)
- `extracted_json/raju_canonical_content.json` + `raju_machine_index.json` (fixtures)
- Frontend consumers: `frontend/src/components/{NatalMandaliChart,CurrentMandaliChart,PlanetTransitionTable,GocharaTab,PrintFramework}.tsx`, `frontend/src/components/consultation/*`, `frontend/src/types/mandali.ts`

---

## 3. Current Architecture

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │ PIPELINE (PipelineRunner.process)                                       │
 │                                                                         │
 │ 1. JsonNormalizer.normalize()  → normalized natal payload               │
 │      (planets.moon.sign/nakshatra/pada/longitude, metadata)             │
 │ 2. Runtime Canonical JSON builder (pipeline_runner.py:118-183):         │
 │      EphemerisService.generate_transit_snapshot(target_date)  ─┐        │
 │      MandaliTransitAdapter.adapt(...) → current_transit[]      ┼─┐      │
 │      natal moon rasi/nakshatra/pada (from payload or longitude)│ │      │
 │      → canonical_json {natal:{moon, birth_date},               │ │      │
 │                        current_transit:[...]}                  │ │      │
 │ 3. UniversalMandaliEngine.generate_mandali_advisory(canonical_json)     │
 │      ├─ 7.2 NakshatraPadaResolver (registry, no longitude)              │
 │      ├─ 7.3 MandaliGridConstruction  → 12-Mandali grid on Moon pada     │
 │      ├─ 7.4 TransitMandaliResolver   → Mandali per transit planet       │
 │      ├─ 7.5 LifetimeCycleProjector   → Saturn cycles (Rasi windows)     │
 │      └─ 7.6 BirthPositionDetector    → birth position per window        │
 │      → mandali_advisory (dataclass → asdict)                            │
 │ 4. MandaliPlacementFactory.build_natal/build_current → placements       │
 │ 5. MandaliChartLayoutBuilder.build → 12-cell charts (natal + current)   │
 │ 6. TransitionSummaryBuilder.build → stay/transition dates               │
 │    → mandali_response_dto (MandaliResponseDTO → asdict)                 │
 │ 7. transit_payload: house = placement.mandali.number (content 359-366)  │
 │ 8. TransitEngine.evaluate(...) → activation_score + breakdown           │
 │ 9. MasterProbabilityEngine.reads activation_score (5% weight)           │
 └─────────────────────────────────────────────────────────────────────────┘
```

Two independent outputs carry Mandali/Gochara information to the frontend:
1. `engine_outputs["mandali_response_dto"]` — charts + transition summary (new DTO)
2. `engine_outputs["mandali_advisory"]` — advisory dataclass (backwards-compatible)

A third, **decoupled** path exists but is not fed by the pipeline:
`KnowledgeStore.get_gochara_report()` served at `/api/v1/knowledge/transit/report`
returns a static seeded knowledge-graph summary (`backend/app/core/knowledge_store.py:621`,
endpoint `backend/app/api/v1/endpoints/knowledge.py:229`). It has its own seed graph
("Gochara Mandali", "Mandali 1-12" nodes and "centered_on"/"resolves"/"activates"
edges). It is unrelated to the runtime transit calculations.

---

## 4. Current Data Flow

Step-by-step, with real code:

| # | Step | Actual source | Function / class | Input fields | Output fields |
|---|------|---------------|------------------|--------------|---------------|
| 1 | Natal Moon | `json_normalizer.py:111` | `JsonNormalizer._normalize_planets` | raw planet dict | `planets.moon.{name, sign, degree, longitude, nakshatra, house, ...}` |
| 2 | Moon Rāśi | normalizer sign map | `_clean_name(..., sign_map)` | raw `sign` | `planets.moon.sign` (e.g. `"Makara"`) |
| 3 | Moon Nakshatra | canonical PDF field | `_clean_string(p_data.get("nakshatra"))` | raw `nakshatra` | `planets.moon.nakshatra` — **can be `""` in the shipped fixture** |
| 4 | Moon Pada | canonical PDF | (passed through) | raw `pada` | normalized does not set `pada`; pipeline derives it |
| 5 | Runtime natal nakshatra/pada fallback | `pipeline_runner.py:138-143` | `MandaliGenerator.get_absolute_pada(longitude)` + `ref_data.get_nakshatra_pada()` | `planets.moon.longitude` | `(Dhanishta, 2)` for the fixture (abs pada 90) |
| 6 | Ephemeris snapshot | `ephemeris_service.py:72` | `EphemerisService.generate_transit_snapshot` | target UTC | `planets.{name, sign, degree, longitude, speed, is_retrograde}` |
| 7 | Canonical `current_transit` build | `mandali_transit_adapter.py:77-147` | `MandaliTransitAdapter.adapt` | snapshot + natal moon | per planet `{planet, rasi, nakshatra, pada, start_date, end_date, next_mandali, house_from_moon, interpretation}` |
| 8 | Mandali grid | `mandali_grid_construction.py:101` | `MandaliGridConstruction.build_grid(nakshatra, pada)` | natal nakshatra/pada | `MandaliGrid` (12×`Mandali`, each 9 padas) |
| 9 | Transit → Mandali | `transit_mandali_resolution.py:82` | `TransitMandaliResolver.resolve_transit_planet` | transit nakshatra/pada/rasi + grid | `TransitMandaliResolution` (planet, original, mandali, house_from_moon_classical, house_from_moon_mandali, interpretation_ref) |
| 10 | Advisory assembly | `universal_mandali_engine.py:400` | `_compose_advisory` | all capability outputs | `MandaliAdvisory` |
| 11 | Placements | `mandali_placement_factory.py:41,91` | `build_natal` / `build_current` | normalized natal planets / resolutions + grid | placement DTOs |
| 12 | Charts | `mandali_chart_layout_builder.py` | `MandaliChartLayoutBuilder.build` | placements + mandali_names | 12-cell grids |
| 13 | Transition summary | `transition_summary_builder.py:17` | `TransitionSummaryBuilder.build` | current_transit + grid + target | `TransitionSummaryDTO` |
| 14 | TransitEngine house feed | `pipeline_runner.py:360-366` | transit_payload assembly | current placements | `transit_payload.planets[].house = mandali number` |
| 15 | Transit scoring | `transit_engine.py:91` | `TransitEngine.evaluate` | transit_payload + natal + dasha + AV | `activation_score`, `breakdown`, `transit_houses`, `confidence_flags` |
| 16 | Pipeline output | `pipeline_runner.py:391-396` | — | — | `{metadata, master_probability, engine_outputs, target_date_utc}` |

---

## 5. MandaliGenerator — Actual Behavior

**Class**: `MandaliGenerator` — `backend/app/engines/mandali_generator.py:35` (a
"compatibility facade" per its own docstring, ADR-004 / GM-013A.1).

| Question | Answer (factual) |
|----------|------------------|
| What inputs does it receive? | A **Moon absolute pada (1-108)** for grid generation; a **transit longitude (deg)** + moon absolute pada for `resolve_transit_mandali`. Constructor optionally takes `CanonicalReferenceData` and `MandaliGridConstruction`. |
| Does it use Moon Rāśi? | Not as input. Moon Rāśi is *derived* via registry (`ref_data.get_rasi(nakshatra, pada)`) inside grid construction (MGC-06 / `mandali_grid_construction.py:132,152`). |
| Does it use Moon Nakshatra? | Yes — indirectly. `_grid_for_pada` converts absolute pada → `(nakshatra, pada)` via `ref_data.get_pada_entry()` and passes both to `build_grid`. |
| Does it use Moon Pada? | Yes (the absolute pada, or 1-4 pada via `get_pada_entry`). |
| How is the reference/center determined? | Mandali 1 center = Moon's absolute pada (MGC-02). |
| How are the 9 positions (of each Mandali) generated? | Fixed arithmetic: `center_pada = ((moon_abs + (N-1)*9 - 1) % 108) + 1`; `padas = center ± 4 mod 108` (`mandali_grid_construction.py:138-144`). |
| Are positions fixed or dynamic? | **Static per natal Moon** — deterministic; identical inputs → identical grid (MGC-07). They are not recomputed from transit. |
| How are Nakshatra/Padas assigned? | Registry lookup `get_pada_entry(absolute_pada)`. |
| Is the result person-specific? | **Yes** — changes with the natal Moon's nakshatra/pada (see `test_mgc01_various_moon_positions`). |
| Ordinary Rāśi boundaries? | **No.** Rāśi is used only as a *label* for the center pada (MGC-06) and for the Moon's own rāśi. Boundaries are pada-based. |
| Nakshatra/Pada boundaries? | **Yes** — the grid edges lie between consecutive absolute padas (quarter-nakshatras). |
| Planetary longitude? | The `get_absolute_pada(longitude)` static helper is pure math: `int(floor((lon % 360) / (10/3))) + 1` (`mandali_generator.py:59-66`). `resolve_transit_mandali(longitude, moon_pada)` uses it. These methods are NOT on the Model A advisory path (governance §9.1 marks them deprecated) **but they ARE used at runtime** in `pipeline_runner.py:140` (moon nakshatra derivation), `mandali_transit_adapter.py:158,220` (transit nakshatra/pada and Mandali-at-date lookups), and `mandali_placement_factory.py:68` (natal placements). |
| Ephemeris? | `MandaliGenerator` itself performs no ephemeris call. It consumes longitudes that the caller obtained from `EphemerisService`/`JsonNormalizer`. |
| What exactly does it return? | `generate_mandali_grid(moon_absolute_pada)` → `{1..12: {"center": int, "padas": [9 ints]}}`; `resolve_transit_mandali(longitude, moon_pada)` → int 1-12. |

---

## 6. TransitEngine — Actual Behavior

**Class**: `TransitEngine` — `backend/app/engines/transit_engine.py:45`

### A–F direct answers

- **A. Ordinary Rāśi resolution?** No. The engine never reads Rāśi; it receives house-like integers.
- **B. Nakshatra resolution?** No — nakshatra is not consumed by `evaluate()`.
- **C. Pada resolution?** No — pada is not consumed by `evaluate()`.
- **D. Resolution through MandaliGenerator?** Through the Mandali pipeline, yes — indirectly. In the live path the Mandali numbers are computed upstream by `TransitMandaliResolver` (pada-based) / `MandaliPlacementFactory.build_current`, then injected as `house` in `transit_payload`. If a caller passes `mandali_results` (a `MandaliResponseDTO` with `current_chart.placements`), `evaluate()` at `transit_engine.py:126-129` uses `placement.mandali["number"]` as the house. The `MandaliGenerator.resolve_transit_mandali` longitude-based helper is used by unit tests, not the pipeline.
- **E. Static-house fallback?** Yes. If no `mandali_results` placements exist, it falls back to `transit_payload[planet]["house"]` verbatim (`transit_engine.py:131-134`).
- **F. Competing transit-resolution paths?** Yes — two:
  1. **Mandali path**: house = `placement.mandali["number"]` (from `mandali_results` DTO),
  2. **Legacy path**: house = `transit_payload[planet]["house"]` (raw classical house from Canonical JSON, or any injected number).
- **G. Which is used in normal execution?** The **mandali path**, but implemented by pre-injecting the Mandali number into `transit_payload["planets"][planet]["house"]` in `pipeline_runner.py:360-366`, and *not* passing `mandali_results` (comment: "transit_payload already carries mandali-based house numbers ... legacy fallback path").

### Execution path during normal pipeline run

```
mandali_response_dto.current_chart.placements
   → placement.planet.lower() → placement.mandali["number"]      (pipeline_runner.py:360-366)
   → transit_payload["planets"][planet] = {"house": mandali_num, "sign": placement.rasi, "degree": 0}
   → TransitEngine.evaluate(transit_payload, normalized_payload, dasha_results, av_results, natal_promise_results)
   → t_houses = {planet: int(transit_payload[planet]["house"])}  (no mandali_results → legacy branch, transit_engine.py:131-134)
   → 5 sub-systems → weighted sum → clamp_score → activation_score
```

### Sub-systems (weights from calibration / `astrology_constants.py:514`)
| Sub-system | Weight | Operates on |
|-----------|--------|-------------|
| `house_activation` | 0.30 | `t_houses` vs `TRANSIT_HOUSE_QUALITY` |
| `bav_support` | 0.20 | `t_houses` vs `bav_charts` bindus |
| `planet_activation` | 0.20 | transit-house conjunction/aspect vs natal houses |
| `dasha_sync` | 0.20 | active Dasha lords vs transit houses |
| `vedha_layer` | 0.10 | `VEDHA_PAIRS` obstruction |

Because `t_houses` are **Mandali numbers** in the live path, the classical Parashari
`TRANSIT_HOUSE_QUALITY` table (which is written for ordinary 12 house positions) is
applied **to Mandali house numbers**. Sade Sati flagging is likewise Mandali-based.

---

## 7. Planet Placement

### Per transit planet — fields actually stored today

| Planet | Source of longitude | Stored in ephemeris snapshot | In adapter `current_transit` | In `CurrentTransitPlanetPlacement` |
|--------|--------------------|------------------------------|------------------------------|-------------------------------------|
| Sun | `swe.SUN` (0) | sign, degree, longitude, speed, retro | planet, rasi, nakshatra, pada, dates, next_mandali, house_from_moon, interpretation | planet, rasi, nakshatra, pada, mandali{number,name}, status |
| Moon | `swe.MOON` (1) | same | same | same |
| Mars | `swe.MARS` (4) | same | same | same |
| Mercury | `swe.MERCURY` (2) | same | same | same |
| Jupiter | `swe.JUPITER` (5) | same | same | same |
| Venus | `swe.VENUS` (3) | same | same | same |
| Saturn | `swe.SATURN` (6) | same | same | same |
| Rahu | `swe.TRUE_NODE` (11) | same | same | same |
| Ketu | derived `Rahu + 180°` (`ephemeris_service.py:131-146`) | same | same | same |

- `longitude`: stored in the **ephemeris snapshot** (`EphemerisService` output) and in
  `End-to-end` natal transit payload. **Not stored** in the placement DTOs or in the
  `mandali_advisory` dataclasses.
- `rasi` / `nakshatra` / `pada`: stored in placement DTOs and resolutions.
- `Mandali`: stored as `mandali: {"number", "name"}` in placements; as `mandali: {"number","name","center_nakshatra","center_pada"}` in resolutions.
- `house`: stored in `CurrentTransitPlanetPlacement` **only implicitly as the Mandali number** inside `mandali.number`; and as `house_from_moon_classical` / `house_from_moon_mandali` in `TransitMandaliResolution`.
- `transit status`: stored as `status` in `CurrentTransitPlanetPlacement` and `TransitMandaliPosition` (`FAVORABLE | NEUTRAL | CHALLENGING`; rule `_determine_status`, `universal_mandali_engine.py:500-509`: 1-4 FAVORABLE, 5-8 NEUTRAL, 9-12 CHALLENGING).
- **Not present anywhere**: no planet-level "current Mandali residence days", no Mandali-level transit *timing* stored in the advisory (dates live only in `current_transit`/`TransitionSummaryDTO`).

---

## 8. Transit Period Calculation

Owner of period math: **`MandaliTransitAdapter._calculate_transit_dates`**
(`backend/app/engines/mandali_transit_adapter.py:184-215`), with internal helpers
`_mandali_at`, `_find_transition`, `_bisect_transition` (lines 217-280).

For each planet (per adapter `adapt()` at line 132):

1. `target_mandali = _mandali_at(planet, grid, target_date)` — live sidereal longitude
   via `EphemerisService.get_longitude`, mapped `→ get_absolute_pada → find_mandali_for_pada`.
2. **Entry** (`start_date`): most recent past crossing *into* `target_mandali`
   (backward daily scan, epoch step 1 day, max 1500 days, bisected ×45 iterations).
3. **Exit** (`end_date`): next future crossing *out of* `target_mandali`; the
   post-crossing Mandali is **`next_mandali`** (retrograde-aware: may be the previous Mandali).
4. If a crossing is not found in ±1500 days → `start_date = end_date = "—"`,
   `next_mandali = None` (no fabricated values).

| Question | Answer |
|----------|--------|
| Entry/exit condition | Planet's sidereal longitude crosses the boundary between two 9-pada Mandali arcs |
| Boundary used | **Mandali boundary** (pada-index based, every 9 absolute padas from the Moon pada; 9 × 3⅓° = 30°-wide arcs) |
| Date calculation | Ephemeris bisection over UTC datetime |
| Source of dates | Swiss Ephemeris planetary motion (`EphemerisService.get_longitude`) |
| Ephemeris used? | **Yes** (adapter only) |
| Interpolation? | 45-step bisection between 1-day samples (not polynomial interpolation) |
| Nakshatra/Pada boundary? | Implicit — Mandali edges sit on pada boundaries |
| Rāśi boundary? | No — grid edges are pada-based, not rāśi-based |
| Mandali boundary? | Yes — the arc edges of the Moon-centered grid |

`TransitionSummaryBuilder` (`transition_summary_builder.py:46-61`) then turns these
into `days_remaining` / `duration_days` using the adapter's `end_date`/`start_date`
and falls back to `(current_mandali % 12) + 1` for `next_mandali` **only** when the
adapter's `next_mandali` is missing.

**CURRENT CHECKPOINT = Mandali (pada-arc) boundary, resolved via ephemeris longitude
at runtime; Rāśi boundaries are not used for transit period timing.**

Saturn *lifetime* dates (separate system) use a different checkpoint — see §9.

---

## 9. Saturn Special Periods

Owners: `LifetimeCycleProjector` (`lifetime_cycle_projection.py`) and
`BirthPositionDetector` (`birth_position_detection.py`); composed in
`UniversalMandaliEngine._compose_sade_sati/_compose_elinati_shani/_compose_ashtama_shani`
(`universal_mandali_engine.py:538-681`).

| Aspect | Sade Sati | Elinati Shani | Ashtama Shani |
|--------|-----------|---------------|---------------|
| Rule | LCP-07: 3 consecutive Rāśis `(Moon-1, Moon, Moon+1)` | LCP-08: Rāśi at offset **+7** (8th) from Moon | LCP-09: same as Elinati (same Rāśi, different interpretation) |
| Reference point | Natal Moon Rāśi | Natal Moon Rāśi | Natal Moon Rāśi |
| Rāśi dependency | Yes | Yes | Yes |
| Moon dependency | Yes (Moon Rāśi only) | Yes (Moon Rāśi only) | Yes |
| Mandali dependency | Label only (`CycleWindow.mandali`) computed by a **heuristic** `(rasi_offset // 2) + 1` (`lifetime_cycle_projection.py:398-422`, self-described "simplified calculation") | same | same |
| Start/end dates | Fixed **30-month (900-day)** windows, iterated from the Canonical Saturn `start_date` (LCP-03/04/10) | same | same |
| Ephemeris? | **No** — fixed `30 days × 30 months = 900 days` increments (LCP-10) | No | No |
| Owning engine | `LifetimeCycleProjector` (+ `BirthPositionDetector` for birth classification) | same | same |

Additional essential facts:

- The **anchor** for all windows is the **Rasi-based Saturn transit from `current_transit`**
  (`planet == "Saturn"`), specifically its `start_date` + `rasi`. The `UniversalMandaliEngine`
  raises `InvalidInputError` if Saturn is absent from `current_transit`
  (`universal_mandali_engine.py:318-320`).
- Per-cycle phases: `Rising (Moon-1)`, `Peak (Moon)`, `Setting (Moon+1)`
  (`lifetime_cycle_projection.py:310-322`).
- Cycle numbering: 0 = anchor; negative past; positive future; 120-year horizon
  (≈4 cycles).
- **Separately**, `TransitEngine._generate_confidence_flags` flags `"saturn_sadesati"`
  when Saturn's `t_houses` value ∈ {12, 1, 2} (`transit_engine.py:680-684`). Because
  `t_houses` are **Mandali numbers** in the live path, this flag is **Mandali-based**
  (`Mandali 12/1/2`), i.e. it uses the Moon-centered grid — unlike the
  `LifetimeCycleProjection` Sade Sati which is Rāśi-based. **Both mechanisms coexist.**
- Tests covering these: `test_lifetime_cycle_projection.py` (LCP-01..10),
  `test_birth_position_detection.py` (BPD-01..06), and implicitly
  `test_gochara_integration.py::TestGocharaGovernanceCompliance::test_sade_sati_uses_three_mandalis`.

---

## 10. Ephemeris Integration

**Architecture component**: `EphemerisService`
(`backend/app/utils/ephemeris_service.py`).

- **Where planetary positions are obtained**: `pyswisseph` (`swisseph`) if installed;
  otherwise a **synthetic deterministic fallback** (`orbit_speeds * julian_day % 360`).
  The environment under test has SWE installed.
- **Owner of astronomical math**: `EphemerisService` (pipeline-scoped singleton). Model A
  engines (`MandaliGridConstruction`, `TransitMandaliResolver`, `NakshatraPadaResolver`,
  `UniversalMandaliEngine`, `LifetimeCycleProjector`, `BirthPositionDetector`) perform **zero**
  astronomical calculation — all registry/pada/date arithmetic only (governance CGP-06,
  VAL-01/02/03).
- **Precision**: raw double-precision sidereal longitude (`results[0][0]`), Lahiri ayanamsa
  (`swe.set_sid_mode(swe.SIDM_LAHIRI)`), re-asserted before every call
  (`ephemeris_service.py:99`). `FLG_SIDEREAL | FLG_SPEED`.
- **Return format**: `{name, sign, degree, longitude, speed, is_retrograde}` per planet.
- **Longitude available?** Yes — `longitude` (0-360 sidereal) is a first-class field.
- **Nakshatra/Pada from longitude?** Yes — at runtime, two places:
  `MandaliTransitAdapter._resolve_nakshatra_pada` (`mandali_transit_adapter.py:149-159`)
  uses `MandaliGenerator.get_absolute_pada(longitude)` → `ref_data.get_nakshatra_pada()`.
  The same chain derives the **natal Moon** nakshatra/pada when the PDF omits them
  (`pipeline_runner.py:138-143`).
- **Alternatively supplied by another layer?** Yes — when Canonical JSON is supplied
  with explicit transit `nakshatra`/`pada`, the Model A resolver consumes those directly
  and never touches longitude (TMR-01/NPR-02).
- **Does MandaliGenerator calculate anything astronomical?** No ephemeris; only pure
  longitude→pada arithmetic (`get_absolute_pada`).
- **Does TransitEngine calculate anything astronomical?** No — score arithmetic only.

> Note (fact): governance §2.5 / §9.1 declare Model A must not compute
> longitude/pada; the runtime adapter layer (`MandaliTransitAdapter` + `EphemerisService`)
> lives **outside** those capability classes and performs exactly that derivation to feed
> Model A. This boundary is the current factual state.

---

## 11. Current JSON / Data Structures

### 11.1 `mandali_response_dto` (`engine_outputs["mandali_response_dto"]`), schema_version "2.0"

```json
{
  "schema_version": "2.0",
  "natal_chart": {
    "chart_name": "Natal Moon-Centered Rasi Mandali",
    "placements": [
      {
        "planet": "Moon",
        "rasi": "Makara",
        "nakshatra": "Dhanishta",
        "pada": 2,
        "mandali": {"number": 1, "name": "Mandali 1 (Makara)"}
      }
    ],
    "grid": [
      {"mandali_number": 1, "mandali_name": "Mandali 1 (Makara)", "planets": ["MO"]}
    ]
  },
  "current_chart": {
    "chart_name": "Current Gochara Moon-Centered Rasi Mandali",
    "placements": [
      {
        "planet": "Saturn",
        "rasi": "Meena",
        "nakshatra": "Revati",
        "pada": 2,
        "mandali": {"number": 3, "name": "Mandali 3 (Meena)"},
        "status": "FAVORABLE"
      }
    ],
    "grid": [
      {"mandali_number": 3, "mandali_name": "Mandali 3 (Meena)", "planets": ["SA"]}
    ]
  },
  "transition_summary": {
    "summary_items": [
      {
        "planet": "Saturn",
        "current_rasi": "Meena",
        "current_nakshatra": "Revati",
        "current_pada": 2,
        "current_mandali": "Mandali 3 (Meena)",
        "next_mandali": "Mandali 4 (Mesha)",
        "start_date": "17.04.2026",
        "estimated_entry_date": "15.06.2028",
        "days_remaining": 677,
        "duration_days": 790
      }
    ]
  }
}
```
- Produced by: `PipelineRunner` (placements = `MandaliPlacementFactory`, grids =
  `MandaliChartLayoutBuilder`, summary = `TransitionSummaryBuilder`).
- Consumed by: frontend `ConsultationWorkspace`/`GocharaTab` via `report.mandali_analysis`.

### 11.2 `mandali_advisory` (`engine_outputs["mandali_advisory"]`), schema_version "1.0"

Key fields (dataclass `MandaliAdvisory`, `universal_mandali_engine.py:157-176`,
serialized via `asdict`):

```json
{
  "schema_version": "1.0",
  "reference_moon": {"rasi": "Makara", "nakshatra": "Dhanishta", "pada": 2, "mandali_1_center": "Dhanishta"},
  "current_mandali": {"number": 3, "name": "Mandali 3", "center_nakshatra": "Revati", "center_pada": 4},
  "current_transit_mandali": {
     "planet_name": {"mandali": {"number": N, "name": "...", "center_nakshatra": "...", "center_pada": N},
                     "house_from_moon_classical": N, "house_from_moon_mandali": N,
                     "status": "FAVORABLE|NEUTRAL|CHALLENGING", "interpretation_key": "..."}
  },
  "transit_resolutions": [
     {"planet": "...", "original": {"rasi": "...", "nakshatra": "...", "pada": N},
      "mandali": {"number": N, "name": "Mandali N", "center_nakshatra": "...", "center_pada": N},
      "house_from_moon_classical": N, "house_from_moon_mandali": N, "interpretation_ref": "..."}
  ],
  "mandali_activations": [{"mandali": N, "planets": ["..."], "activation_strength": "HIGH|MEDIUM|LOW"}],
  "sade_sati": {"cycles": [{"cycle_number": N, "period": "YYYY-YYYY",
                            "sade_sati_windows": [{"phase": "Rising|Peak|Setting", "rasi": "...",
                                                    "mandali": N, "start": "DD.MM.YYYY", "end": "DD.MM.YYYY",
                                                    "birth_position": "..."}]}],
                "birth_detection": {"position": "...", "cycle": N, "phase": "...", "description": "..."}},
  "elinati_shani": {"cycles": [...], "birth_detection": {...}},
  "ashtama_shani": {"cycles": [...], "birth_detection": {...}},
  "timeline": [{"period": "...", "cycle": N, "events": ["..."]}],
  "important_advisory_statements": ["..."],
  "upcoming_mandali_events": [{"event": "...", "date": "DD.MM.YYYY", "mandali": N}],
  "moon_absolute_pada": 90
}
```
- Produced by: `UniversalMandaliEngine.generate_mandali_advisory`.
- Consumed by: report builder (`important_advisory_statements`, `upcoming_mandali_events`,
  `current_mandali`) and `QuestionEngine.compose_response(..., mandali_activation=...)`.

### 11.3 `transit` (TransitEngine output) — `engine_outputs["transit"]`

```json
{
  "activation_score": 58,
  "grade": "GOOD",
  "activated_domains": {"marriage": N, "career": N, ...},
  "supporting_factors": [{"factor": "...", "score": N, "planet": "...", "house": N, "source": "..."}],
  "obstructing_factors": [...],
  "breakdown": {"house_activation": N, "bav_support": N, "planet_activation": N,
                "dasha_sync": N, "vedha_layer": N},
  "confidence_flags": ["jupiter_transit_positive", "dasha_lord_transiting"],
  "stub_factors": [],
  "transit_houses": {"sun": 7, "moon": 4, ...}
}
```
- Produced by: `TransitEngine.evaluate`; consumed by `MasterProbabilityEngine._transit_trigger`
  (reads `activation_score`) and `DisplayFormatter.format_gochara_report`.

### 11.4 `gochara_report` (report-level, `ReportBuilder` → `DisplayFormatter.format_gochara_report`)

`GocharaReport` (`reports/schemas.py:179`) with `transit_strength`, `transit_planets`,
`transit_houses`, plus an embedded `MandaliReport`.

**Factual gap in current output**: `format_gochara_report` reads
`pipeline_data["engine_outputs"]["mandali"]` (`display_formatter.py:633`) and
`transit_data["metadata"]` (`display_formatter.py:631`). The pipeline writes
**`mandali_advisory` and `mandali_response_dto`** — it never writes
`engine_outputs["mandali"]` — and `TransitEngine` output has **no `metadata`** key.
Consequently, in today's `gochara_report`: `MandaliReport` fields default empty,
`sade_sati_status = "Not Active"` (with `sat_house == 0`), and
`current_transit_date = ""`. The report-level **transit** portion
(`activation_score`, etc.) is populated.

---

## 12. Pipeline Integration

`PipelineRunner.process()` (`pipeline_runner.py:88`):

1. Normalizes input (`JsonNormalizer.normalize`).
2. Builds runtime `canonical_json` (lines 118-183): moon rasi/nakshatra/pada from the
   normalized payload (with longitude derivation fallback), birth date (D.D.MM.YYYY),
   `current_transit` from `EphemerisService` + `MandaliTransitAdapter` at the resolved
   `target_date_utc`. On any failure: `logging.warning` + empty `canonical_json`
   (Mandali block skipped).
3. Runs the strength/dasha/varga/rasi/BAV/natal engines (unchanged sibling pipeline).
4. If `canonical_json` has `natal` + `current_transit` (Option A path, lines 321-376):
   - `UniversalMandaliEngine.generate_mandali_advisory(canonical_json)`
   - `engine_outputs["mandali_advisory"] = asdict(...)`
   - factory placements, chart layout grids, transition summary
   - `engine_outputs["mandali_response_dto"] = asdict(MandaliResponseDTO(...))`
   - builds `transit_payload` with `house = mandali number`
   - `transit_results = self.transit_engine.evaluate(...)` — note `mandali_results`
     is intentionally **not** passed.
5. If no transit path ran → `transit_results = transit_engine._stub_result()`
   (`activation_score = 50`, `confidence_flags=["transit_stub_no_input"]`).
6. `engine_outputs["transit"]` → `MasterProbabilityEngine.evaluate(engine_outputs)`.

Failure mode on missing Saturn in `current_transit`: `UniversalMandaliEngine` raises
`InvalidInputError`; the `try/except` around the whole block (lines 121-183) catches
anything thrown during snapshot/adapter building and contextually skips Mandali —
but line 323 (the advisory call) is *outside* that `try`; an exception there
propagates up through `process()`.

---

## 13. Existing Tests

| Test file | What it proves | Passes |
|-----------|----------------|--------|
| `test_mandali_generator.py` | longitude→pada arithmetic; grid shape for Dhanishta p2 (lists), `resolve_transit_mandali` | ✅ |
| `test_mandali_grid_construction.py` | MGC-01..07; grid integrity; pada→mandali lookup; rasi names; determinism; person-varying grids | ✅ |
| `test_transit_mandali_resolution.py` | TMR-01..05; original values preserved; classical vs mandali house; errors; determinism | ✅ |
| `test_nakshatra_pada_resolver.py` | NPR registry resolution, round-trips | ✅ |
| `test_canonical_reference_data.py` | registry loading, versioning, integrity | ✅ |
| `test_lifetime_cycle_projection.py` | LCP-01..10 (30-month windows, anchor, phases, forward/backward, horizon, errors) | ✅ |
| `test_birth_position_detection.py` | BPD-01..06, inclusive boundaries, per-window-type independence | ✅ |
| `test_gochara_integration.py` | Grid generation, no-overlap, no-dynamic-radius, transit-engine mandali wiring; **pipeline test is explicitly `skip`ped** (pre-existing calibration mismatch note) | ✅ (1 skip) |
| `test_transit_engine.py` | TransitEngine breakdown keys, score ranges, domains, stub modes, `UniversalMandaliEngine` structure, Option-A pipeline reads activation_score | ✅ |
| `test_transit_golden_master.py` | **Frozen SWE baseline at 2026-08-07T12:23:01Z**: longitudes, current/natal chart DTOs, stay dates, transitions, SHA-256 signatures | ✅ |
| `test_ephemeris_service.py` | snapshot structure, Ketu = Rahu+180 | ✅ |
| `test_pipeline_runner.py` | pipeline orchestration incl. `_apply_bav_modifiers` | ✅ |
| `test_real_charts.py` | Raju end-to-end scores; `test_integration_...` uses `RAJU_CANONICAL_RAW` | ✅ |
| `test_report_builder.py` | report builder happy path — **one pre-existing, unrelated failure** (`client_info` dict mismatch) | ❌ (1) |

- Does any test verify **person-to-person** Moon-centered changes? Indirectly: grid tests
  vary the Moon nakshatra/pada (`test_mgc01_various_*`, `test_mgc02_various_*`,
  `test_mgc05_various_*`). No test explicitly compares two persons' transit results.
- Does any test verify **transit timing**? Yes — `test_transit_golden_master.py`
  (`test_planet_stay_frozen`, `test_transition_frozen`) pins entered/leaves/duration/days.

---

## 14. Current Limitations (as-implemented facts)

1. **Report-level Gochara Mandali block is effectively empty** — `format_gochara_report`
   reads a never-written `engine_outputs["mandali"]` key and a never-written
   `transit.metadata` key (`display_formatter.py:631,633,636`). See §11.4.
2. **Two Sade Sati notions coexist** — Mandali-based flag in `TransitEngine`
   ({12,1,2} on `t_houses`) vs Rāśi-based windows in `LifetimeCycleProjector`
   ((Moon-1, Moon, Moon+1) with fixed 900-day windows). They are not reconciled in code.
3. **Mandali number on Saturn-cycle windows is heuristic** — `_get_mandali_for_rasi_in_cycle`
   uses `(offset // 2) + 1`, not the actual `MandaliGrid`
   (`lifetime_cycle_projection.py:398-422`).
4. **Classical Parashari `TRANSIT_HOUSE_QUALITY` applied to Mandali house numbers**
   in the live path (`transit_engine.py`), because `t_houses` are Mandali numbers.
5. **Natal Moon nakshatra/pada may be derived from longitude** when the source PDF
   omits them (`pipeline_runner.py:138-143`); the shipped Raju fixture has
   `nakshatra: ""` for the Moon.
6. **Interpretation strings are placeholders** — `_get_interpretation` returns
   `"{Planet} transiting house {N} from Moon"` because no
   `transit_interpretations` registry exists on `CanonicalReferenceData`
   (`mandali_transit_adapter.py:177-182`).
7. **Ephemeris synthetic fallback** when `swisseph` is absent produces deterministic
   pseudo-orbits (not real astronomy).
8. **Not-implemented items**: no continuous future/retro transit timeline beyond the
   adapter's ≤1500-day scan endpoints; no Nakshatra-based (e.g., Nakshatra-tier
   transit) subsystem; no Vedha accounting *within* Mandali at degree level; no
   degree-level Mandali arc resolution within a pada.
9. **Knowledge-graph Gochara report is static/seeded** and disconnected from the
   runtime engines.

---

## 15. Unknowns / Evidence Required

| # | Question | Current evidence status |
|---|----------|--------------------------|
| 1 | Is the frozen golden-master SWE output externally re-verifiable? | Test asserts against `swisseph` directly at the frozen instant (`test_transit_golden_master.py:139`); no printed cross-check artifact in-repo. |
| 2 | Boundary consistency of `get_absolute_pada` (floor at 10/3°) vs registry pada numbering | Self-consistent with `nakshatra_pada_registry.json` (Ashwini p1..p4 = 1..4), but no dedicated boundary test at 3.333°×N edges. |
| 3 | Whether Mandali-arc entry/exit by *pada* was intended to be "exact" vs 30° arcs | `_TRANSIT_SCAN_MAX_DAYS = 1500` covers but cannot resolve Saturn outside ±1500 days; treated as "—" (adapter line 209). |
| 4 | `current_mandali` semantics (Mandali of Saturn transit) vs Moon's Mandali | Advisory defines it as Saturn's Mandali (`universal_mandali_engine.py:415-424`); governance §14 renders "Current Active Mandali" similarly — no evidence of a second interpretation. |
| 5 | Person-to-person comparison fidelity | No two-person test; extracted traces provided in §16 for one person only. |
| 6 | `format_gochara_report` empty-Mandali behavior: intentional or latent | Behavior is deterministic-empty; no test asserts non-empty `MandaliReport`. Needs a decision baseline, not asserted here. |

---

## 16. Exact End-to-End Execution Trace (real repository values)

Fixture: `extracted_json/raju_canonical_content.json` (Raju chart), frozen target
`2026-08-07T12:23:01.407563Z` — identical values the golden-master test freezes.
(Pipeline executed read-only to produce this trace.)

```
INPUT horoscope (canonical_content) 
  ↓ JsonNormalizer._normalize_planets
NATAL MOON payload:
  { name: "moon", sign: "Makara", degree: 27.7572, longitude: 297.7572,
    nakshatra: "", pada: (absent), house: 6, ... }
  ↓ pipeline_runner.py:138-143  (nakshatra blank → derive from longitude)
Moon RASI  = Makara
Moon NAKSHATRA = Dhanishta   (via abs pada 90 → ref_data.get_nakshatra_pada)
Moon PADA  = 2
Moon absolute pada (registry) = 90        (Mandali1 center)
  ↓ EphemerisService.generate_transit_snapshot(target)  [SWE, Lahiri]
Transit snapshot (longitude, sign, deg, retro):
  sun 110.7956 Karkata  | moon 39.4970 Vrishabha | mars 63.2145 Mithuna
  mercury 92.5334 Karkata | jupiter 104.1710 Karkata | venus 156.4898 Kanya
  saturn 350.4025 Meena (R) | rahu 305.6601 Kumbha (R) | ketu 125.6601 Simha (R)
  ↓ MandaliTransitAdapter.adapt  (longitude → abs pada → nakshatra/pada ; arc-crossing scan)
current_transit[] (one row per planet), e.g.:
  {"planet": "Saturn", "rasi": "Meena", "nakshatra": "Revati", "pada": 2,
   "start_date": "17.04.2026", "end_date": "15.06.2028", "next_mandali": 4,
   "house_from_moon": 3, "interpretation": "Saturn transiting house 3 from Moon"}
  ↓ MandaliGridConstruction.build_grid("Dhanishta", 2)   → MandaliGrid (moon_abs_pada=90)
Grid (centers): M1=90, M2=99, M3=108, M4=9, M5=18, M6=27, M7=36, M8=45,
                M9=54, M10=63, M11=72, M12=81
  ↓ TransitMandaliResolver.resolve_all_transit_planets(..., grid)
Mandali per transit planet (M = mandali number, status per 1-4/5-8/9-12 rule):
  Sun→7(Ashlesha p2, NEUTRAL)   Moon→4(Krittika p4, FAVORABLE)
  Mars→5(Mrigashira p3, NEUTRAL) Mercury→6(Punarvasu p4, NEUTRAL)
  Jupiter→7(Pushya p4, NEUTRAL)  Venus→8(U.Phalguni p3, NEUTRAL)
  Saturn→3(Revati p2, FAVORABLE) Rahu→1(Dhanishta p4, FAVORABLE)
  Ketu→7(Magha p2, NEUTRAL)
  ↓ UniversalMandaliEngine._compose_advisory
mandali_advisory:
  reference_moon: {"rasi": "Makara", "nakshatra": "Dhanishta", "pada": 2, "mandali_1_center": "Dhanishta"}
  current_mandali: {"number": 3, "name": "Mandali 3", "center_nakshatra": "Revati", "center_pada": 4}
  sade_sati.birth_detection: {"position": "BIRTH_BEFORE_FIRST_CYCLE", "cycle": -1,
                              "phase": "Rising", "description": "Born before the first Sade Sati period."}
  ↓ PipelineRunner transit-payload feed (house = mandali number)
TransitEngine.evaluate(transit_payload = {sun:{house:7}, moon:{house:4}, mars:{house:5},
  mercury:{house:6}, jupiter:{house:7}, venus:{house:8}, saturn:{house:3},
  rahu:{house:1}, ketu:{house:7}})
  ↓ 5 sub-systems weighted sum + clamp
transit result: activation_score = 58, transit_houses = {sun:7, moon:4, mars:5, mercury:6,
  jupiter:7, venus:8, saturn:3, rahu:1, ketu:7},
  confidence_flags = ["jupiter_transit_positive", "dasha_lord_transiting"]
  ↓ TransitionSummaryBuilder
transition_summary items (real):
  Sun     M7(Karkata)->M8(Simha)   entered 30.07.2026 leaves 30.08.2026  days 22
  Moon    M4(Mesha)->M5(Vrishabha) entered 05.08.2026 leaves 07.08.2026   days 0
  Mars    M5(Vrishabha)->M6(Mithuna) entered 09.07.2026 leaves 22.08.2026  days 14
  Mercury M6(Mithuna)->M7(Karkata)  entered 06.06.2026 leaves 14.08.2026   days 6
  Jupiter M7(Karkata)->M8(Simha)    entered 03.08.2026 leaves 30.08.2027   days 387
  Venus   M8(Simha)->M9(Kanya)      entered 16.07.2026 leaves 14.08.2026   days 6
  Saturn  M3(Meena)->M4(Mesha)      entered 17.04.2026 leaves 15.06.2028   days 677
  Rahu    M1(Makara)->M12(Dhanus)   entered 20.04.2026 leaves 26.10.2027   days 444
  Ketu    M7(Karkata)->M6(Mithuna)  entered 20.04.2026 leaves 26.10.2027   days 444
  ↓ engine_outputs
PIPELINE OUTPUT: engine_outputs["mandali_advisory"], engine_outputs["mandali_response_dto"],
  engine_outputs["transit"], master_probability.final_score (transit 5% weight)
```

---

## 17. Final Current-State Diagram

```
 PDF/Horoscope
     │ raw
     ▼
 JsonNormalizer ──► planets.moon (sign, degree, longitude, nakshatra[may be ""])
     │
     ├─(longitude fallback)→ get_absolute_pada → (Dhanishta,2)  [pipeline:140]
     │
     ▼
 EphemerisService (SWE, Lahiri) ──► transit snapshot (9 planets, sidereal longitude)
     │
     ▼
 MandaliTransitAdapter ──► current_transit[{planet,rasi,nakshatra,pada,
     │                        start_date,end_date,next_mandali,house_from_moon,interpretation}]
     │      (longitude→pada→nak; ≤1500-day arc crossing scan + bisection)
     ▼
 canonical_json { natal:{moon{rasi,nakshatra,pada}, birth_date}, current_transit[] }
     │
     ▼
 UniversalMandaliEngine (Cap 7.1–7.7, NO astronomy)
     ├── NakshatraPadaResolver   (nak,pada)→abs_pada            [registry]
     ├── MandaliGridConstruction (12×9 pada arcs on Moon abs pada) [registry]
     ├── TransitMandaliResolver  (transit nak/pada → Mandali #)  [registry]
     ├── LifetimeCycleProjector  (Saturn 30-month Rasi windows)  [fixed 900-day]
     └── BirthPositionDetector   (birth vs windows)              [date compare]
     │
     ├──► engine_outputs.mandali_advisory
     │
     └──► MandaliPlacementFactory + ChartLayoutBuilder + TransitionSummaryBuilder
              └──► engine_outputs.mandali_response_dto
                    └── transit_payload.house = mandali.number
                          └──► TransitEngine.evaluate ──► engine_outputs.transit
                                └─► activation_score ──► MasterProbabilityEngine (5%)
ReportBuilder ──► report.mandali_analysis / report.gochara_report
```

---

## A | B | C | D Classification

**A. CURRENTLY IMPLEMENTED**
- 12-Mandali grid construction on the natal Moon pada (Cap 7.3).
- (Nakshatra, Pada) → absolute pada registry resolution (Cap 7.2).
- Transit planet → Mandali resolution (Cap 7.4).
- Runtime transit generation via Swiss Ephemeris (Lahiri) and adapter to Canonical format.
- Mandali-arc entry/exit/next-Mandali timing via ephemeris crossing bisection.
- Transit scoring engine (5 subsystems) consuming Mandali house numbers.
- Rāśi-based Saturn Sade Sati / Elinati / Ashtama windows with fixed 30-month arithmetic
  and birth-position detection.
- Frozen golden-master regression for the whole transit chain.
- Frontend Mandali charts + transition table rendering.

**B. CURRENTLY PARTIAL**
- Report-level `gochara_report` Mandali/Sade-Sati block is wired to fields that are never
  populated (`engine_outputs.mandali`, `transit.metadata`) → empty in today's output.
- Mandali number associated with Saturn-cycle windows is a heuristic, not the real grid.
- Birth/per-window relationship computed, but per-planet lifetime Mandali residency
  timeline within arcs is limited to the adapter's ≤1500-day scan.
- Natal Moon nakshatra/pada: relies on PDF extraction, with longitude derivation fallback
  (the shipped fixture uses the fallback).

**C. CURRENTLY NOT IMPLEMENTED**
- No Nakshatra-based (quarter-nakshatra tier / Nakshatra lord) transit subsystem.
- No degree-level Mandali arc boundary precision inside a pada.
- No continuous future transit timeline beyond scan endpoints / fixed 30-month cycles.
- No ephemeris-based Saturn cycle projection (Model B; governance says appendix only).
- No `transit_interpretations` registry (interpretation strings are default placeholders).
- No Vedha/Mandali interaction beyond `t_houses` scoring.
- No person-to-person comparison test.

**D. CURRENTLY UNCLEAR / NEEDS EVIDENCE**
- Whether applying Parashari `TRANSIT_HOUSE_QUALITY` to Mandali numbers is intended
  (factual behavior, no governance text describing it).
- Boundary exactness of `get_absolute_pada` floor arithmetic at pada edges (no test).
- Whether the empty report-level Mandali block is a known acceptance baseline or a latent gap.
- `start.bat` working-tree modification predates this inspection; unrelated to Mandali.

---

## Governance Verification (read-only checklist)

- [x] No source file modified
- [x] No test modified
- [x] No configuration modified
- [x] No formula modified
- [x] No architecture modified
- [x] No new implementation added
- [x] No existing behavior changed
- [x] No backlog created
- [x] No guessed rules presented as facts (all claims cite file/line or executed trace)

**FINAL STATUS: INSPECTION ONLY — NO CODE CHANGES.**