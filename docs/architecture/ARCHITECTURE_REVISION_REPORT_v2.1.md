# Architecture Revision Report – Version 2.1
## Universal Gochara Mandali Model A
### Engineering Governance Specification for GOCHARA_MANDALI_GOVERNANCE_v1.md Upgrade

---

## 1. Executive Summary

This report revises Architecture Revision Report v2 to strengthen **engineering governance** while preserving the Model A architecture unchanged. The Universal Gochara Mandali Engine remains a **deterministic spatial transformation engine** consuming **Canonical JSON transit data** (Rasi + Nakshatra + Pada) and producing **Moon-centred Universal Mandali** outputs — without astronomical calculations, ephemeris, or longitude computations.

**Governance Improvements in v2.1:**
- Pseudocode replaced with deterministic governance rules and invariants
- Embedded astronomical lookup logic removed; Canonical JSON established as authoritative source
- Fixed implementation classes replaced with capability-based responsibilities
- MandaliGenerator refactored (not deprecated) with clear capability boundaries
- Lifetime Projection expanded with governance rules, edge cases, and versioning
- Constitutional governance principles section added
- Normative governance separated from illustrative examples

---

## 2. Constitutional Governance Principles

The following principles are **permanent, non-negotiable, and version-locked**. They govern all Model A implementations and future Model B compatibility.

| # | Principle | Normative Rule |
|---|-----------|----------------|
| **CGP-01** | **Single Source of Truth** | Canonical JSON is the sole authoritative data source for Model A. No external ephemeris, no computed longitudes, no derived astronomical data. |
| **CGP-02** | **Immutability of Original Values** | Original Rasi, Nakshatra, Pada from Canonical JSON are never modified, transformed, or overwritten. Only reference frame changes. |
| **CGP-03** | **Determinism** | Given identical Canonical JSON input, the engine produces identical output. No randomness, no time-dependent variance, no hidden state. |
| **CGP-04** | **Explainability** | Every output value must be traceable to a specific Canonical JSON input field and a named governance rule. |
| **CGP-05** | **Engine Isolation** | Universal Mandali Engine performs only spatial reference frame transformation. It does not compute strengths, scores, probabilities, or interpretations. |
| **CGP-06** | **No Astronomical Computation in Model A** | Planetary longitude calculation, orbital mechanics, ephemeris interpolation, and high-precision astronomy are prohibited in Model A. |
| **CGP-07** | **Model B Compatibility** | Model A architecture must not preclude Model B. Model B is documented as appendix-only; no Model A code depends on Model B concepts. |
| **CGP-08** | **One Formula–One Owner** | Each deterministic rule (Mandali construction, cycle projection, birth detection) has exactly one owning capability. No duplicate calculations across engines. |
| **CGP-09** | **No Duplicate Calculations** | Shared reference data (Nakshatra-Pada sequence, Rasi mappings) is externalized to a single canonical registry. Engines consume; they do not redefine. |
| **CGP-10** | **Output Contract Stability** | The `mandali_advisory` output schema is versioned. Breaking changes require governance approval and migration path. |

---

## 3. Model A vs Model B — Architectural Boundary (Normative)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UNIVERSAL GOCHARA MANDALI                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────┐     ┌─────────────────────────────┐      │
│   │         MODEL A             │     │         MODEL B             │      │
│   │   (CURRENT — IMPLEMENT)     │     │   (FUTURE — APPENDIX ONLY)  │      │
│   ├─────────────────────────────┤     ├─────────────────────────────┤      │
│   │ Source: Canonical JSON      │     │ Source: Swiss Ephemeris     │      │
│   │ Input: Rasi + Nakshatra     │     │ Input: Longitude (deg)      │      │
│   │        + Pada               │     │ Compute: Longitude → Pada   │      │
│   │ No astronomical calculations│     │ Full orbital mathematics    │      │
│   │ Deterministic transformation│     │ Predictive future transits  │      │
│   │ Reference frame shift only  │     │ Continuous timeline         │      │
│   │ Lifetime projection via     │     │ High-precision astronomy    │      │
│   │   deterministic rules       │     │                             │      │
│   └─────────────────────────────┘     └─────────────────────────────┘      │
│                                                                             │
│   GOVERNANCE: Single document (GOCHARA_MANDALI_GOVERNANCE_v1.md)           │
│   Model B noted as future compatibility appendix only                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Normative Decision**: Model A is the **only** implementation target. Model B is documented as future compatibility in an appendix — **no code, no dependencies, no architecture for Model B**.

---

## 4. System Architecture — Model A (Normative)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE — MODEL A                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────────────────────┐     ┌────────────────────────┐
│  CANONICAL   │     │  UNIVERSAL MANDALI ENGINE    │     │   CONSULTATION         │
│  JSON STORE  │────▶│  (Capability Composition)    │────▶│   OUTPUT OBJECTS       │
│              │     │                              │     │                        │
│  • Natal     │     │  Capabilities:               │     │  • Mandali Numbers     │
│    - Moon    │     │  • MandaliGridConstruction   │     │  • Transit Status      │
│    - Rasi    │     │  • TransitMandaliResolution  │     │  • Sade Sati           │
│    - Nakshatra│    │  • LifetimeCycleProjection   │     │  • Elinati Shani       │
│    - Pada    │     │  • BirthPositionDetection    │     │  • Ashtama Shani       │
│              │     │  • CanonicalReferenceData    │     │  • Lifetime Timeline   │
│  • Transit   │     │                              │     │  • Birth Position      │
│    - Planet  │     │  Inputs (Read-Only):         │     │  • Consultation Objects│
│    - Rasi    │     │  • Natal Moon (Rasi, Nak, Pada)│    │                        │
│    - Nakshatra│    │  • Current Transit Planets   │     └───────────┬────────────┘
│    - Pada    │     │    (Planet, Rasi, Nak, Pada, │                 │
│    - Dates   │     │     start_date, end_date)    │                 ▼
│    - House   │     │  • Birth Date                │     ┌────────────────────────┐
│              │     │  • Canonical Reference Data  │     │   ANSWER COMPOSER      │
│              │     │                              │     │                        │
└──────────────┘     └──────────────────────────────┘     │  • Mandali Advisory    │
                                                         │  • Canonical Text      │
NO EphemerisService  NO Swiss Ephemeris  NO Longitude    │  • Final Report        │
NO Orbital Math      Calculation       NO Orbital Math   └────────────────────────┘
```

**Capability Composition**: The Universal Mandali Engine is not a monolithic class. It is a **composition of capabilities**, each independently testable and governed.

---

## 5. Canonical JSON Transit Schema — Model A Input Contract (Normative)

The Canonical JSON (pages 85–86, section "Transit / Gochara") provides exactly the data Model A requires. This schema is **normative** — implementations must accept this structure.

```json
{
  "natal": {
    "moon": {
      "rasi": "string",           // Required: Rasi name (e.g., "Makara")
      "nakshatra": "string",      // Required: Nakshatra name (e.g., "Dhanishta")
      "pada": "integer"           // Required: 1-4
    },
    "birth_date": "string"        // Required: DD.MM.YYYY
  },
  "current_transit": [
    {
      "planet": "string",         // Required: Planet name (Saturn, Jupiter, Rahu, etc.)
      "rasi": "string",           // Required: Transit Rasi
      "nakshatra": "string",      // Required: Transit Nakshatra
      "pada": "integer",          // Required: 1-4
      "start_date": "string",     // Required: DD.MM.YYYY
      "end_date": "string",       // Required: DD.MM.YYYY
      "house_from_moon": "integer", // Required: Classical Rasi-house from Moon (1-12)
      "interpretation": "string"  // Required: Canonical interpretation text
    }
  ]
}
```

**Normative Constraints:**
- All fields are required. Missing fields constitute invalid input.
- `pada` must be integer 1-4.
- `house_from_moon` must be integer 1-12 (classical Rasi-house, NOT Mandali).
- `start_date` ≤ `end_date` for each transit entry.
- Interpretation text is **canonical reference only** — engine does not parse or modify it.

---

## 6. Canonical Reference Data Registry (Normative)

**Governance Rule CGP-09**: Shared reference data is externalized to a single canonical registry. Engines consume; they do not redefine.

### 6.1 Nakshatra-Pada Sequence (Canonical Registry)

| Absolute Pada (1-108) | Nakshatra | Pada | Rasi |
|----------------------|-----------|------|------|
| 1 | Ashwini | 1 | Mesha |
| 2 | Ashwini | 2 | Mesha |
| 3 | Ashwini | 3 | Mesha |
| 4 | Ashwini | 4 | Mesha |
| 5 | Bharani | 1 | Mesha |
| ... | ... | ... | ... |
| 108 | Revati | 4 | Meena |

**Registry Location**: `backend/app/config/nakshatra_pada_registry.json` (single source of truth)

### 6.2 Nakshatra → Rasi Mapping (Canonical Registry)

| Nakshatra | Rasi |
|-----------|------|
| Ashwini, Bharani, Krittika (p1) | Mesha |
| Krittika (p2-4), Rohini, Mrigashira (p1-2) | Vrishabha |
| Mrigashira (p3-4), Ardra, Punarvasu (p1-3) | Mithuna |
| ... | ... |

**Registry Location**: `backend/app/config/nakshatra_rasi_registry.json`

### 6.3 Rasi Sequence (Canonical Registry)

`["Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"]`

**Registry Location**: `backend/app/config/rasi_sequence_registry.json`

---

## 7. Capability Specifications (Normative)

The Universal Mandali Engine composes the following capabilities. Each capability has a single owner, defined inputs, deterministic rules, and defined outputs.

### 7.1 Capability: MandaliGridConstruction

**Purpose**: Construct the 12-Mandali grid centered on the Natal Moon Pada.

**Inputs**:
- `natal_moon_nakshatra` (string) — from Canonical JSON
- `natal_moon_pada` (integer 1-4) — from Canonical JSON
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules (Invariants)**:
| Rule ID | Rule |
|---------|------|
| MGC-01 | Moon Absolute Pada = `nakshatra_pada_to_absolute(natal_moon_nakshatra, natal_moon_pada)` using Canonical Registry |
| MGC-02 | Mandali 1 center = Moon Absolute Pada |
| MGC-03 | Mandali N center = `((Moon_Absolute_Pada + (N-1)×9 - 1) mod 108) + 1` |
| MGC-04 | Each Mandali contains exactly 9 padas: center ±4 (modulo 108 wrap) |
| MGC-05 | All 108 padas covered exactly once across 12 Mandalis (no gaps, no overlaps) |
| MGC-06 | Mandali Rasi name = Rasi of center pada's Nakshatra (from Canonical Registry) |
| MGC-07 | Output is deterministic: identical inputs → identical grid |

**Outputs**:
- `mandali_grid[1..12]` where each entry contains:
  - `number` (1-12)
  - `center_pada` (1-108)
  - `center_nakshatra` (string)
  - `center_pada_num` (1-4)
  - `rasi_name` (string)
  - `padas` (array of 9 absolute pada indices)
  - `pada_details` (array of 9 {nakshatra, pada} from Registry)

---

### 7.2 Capability: TransitMandaliResolution

**Purpose**: Resolve each transit planet's Canonical JSON position to a Mandali number.

**Inputs**:
- `transit_planets[]` — from Canonical JSON (each: planet, rasi, nakshatra, pada)
- `mandali_grid[1..12]` — from MandaliGridConstruction
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules (Invariants)**:
| Rule ID | Rule |
|---------|------|
| TMR-01 | Transit Absolute Pada = `nakshatra_pada_to_absolute(transit_nakshatra, transit_pada)` using Canonical Registry |
| TMR-02 | Transit Mandali = unique Mandali N where Transit Absolute Pada ∈ `mandali_grid[N].padas` |
| TMR-03 | Exactly one Mandali contains the transit pada (guaranteed by MGC-05) |
| TMR-04 | Original Canonical JSON values (rasi, nakshatra, pada) are preserved in output — never modified |
| TMR-05 | Classical `house_from_moon` from Canonical JSON is preserved alongside Mandali number |

**Outputs** (per transit planet):
```json
{
  "planet": "string",
  "original": { "rasi": "string", "nakshatra": "string", "pada": "integer" },
  "mandali": { "number": "integer", "name": "string", "center_nakshatra": "string", "center_pada": "integer" },
  "house_from_moon_classical": "integer",
  "house_from_moon_mandali": "integer",
  "interpretation_ref": "string"
}
```

---

### 7.3 Capability: LifetimeCycleProjection

**Purpose**: Project Saturn's 30-year cycles bidirectionally from Canonical JSON transit dates.

**Inputs**:
- `natal_moon_rasi` — from Canonical JSON
- `birth_date` — from Canonical JSON (DD.MM.YYYY)
- `saturn_transit` — from Canonical JSON current_transit (planet="Saturn")
- `rasi_sequence_registry` — from Canonical Reference Data Registry

**Governance Rules (Invariants)**:
| Rule ID | Rule |
|---------|------|
| LCP-01 | Saturn transit duration per Rasi = 30 months (2.5 years) — fixed constant |
| LCP-02 | Full zodiac cycle = 12 × 30 months = 360 months = 30 years — fixed constant |
| LCP-03 | Current cycle anchor = Canonical JSON Saturn `start_date` and `rasi` |
| LCP-04 | Cycle construction: iterate 12 Rasis from anchor, each 30 months, forward and backward |
| LCP-05 | Past cycles: subtract 30 years per cycle from anchor until before birth_date |
| LCP-06 | Future cycles: add 30 years per cycle from anchor until governance-defined horizon |
| LCP-07 | Sade Sati window per cycle = 3 consecutive Rasis: (Moon_Rasi - 1), Moon_Rasi, (Moon_Rasi + 1) modulo 12 |
| LCP-08 | Elinati Shani window per cycle = Rasi at offset +7 from Moon_Rasi (8th house) |
| LCP-09 | Ashtama Shani window per cycle = Rasi at offset +7 from Moon_Rasi (classical 8th) |
| LCP-10 | All date arithmetic uses fixed 30-month increments — no astronomical precision |

**Outputs**:
- `cycles[]` where each cycle contains:
  - `cycle_number` (integer, ... -1, 0, 1, 2 ... where 0 = cycle containing Canonical JSON anchor)
  - `period` (string: "YYYY-YYYY")
  - `sade_sati_windows[]` (3 per cycle: Rising, Peak, Setting)
  - `elinati_shani_windows[]` (1 per cycle)
  - `ashtama_shani_windows[]` (1 per cycle)

---

### 7.4 Capability: BirthPositionDetection

**Purpose**: Classify native's birth position relative to each major cycle window.

**Inputs**:
- `birth_date` — from Canonical JSON
- `cycle_windows[]` — from LifetimeCycleProjection (each with start_date, end_date, cycle_number, phase)

**Governance Rules (Invariants)**:
| Rule ID | Rule |
|---------|------|
| BPD-01 | For each window: if `birth_date ∈ [start_date, end_date]` → `BIRTH_INSIDE` |
| BPD-02 | If `birth_date < start_date` of first window → `BIRTH_BEFORE_FIRST_CYCLE` |
| BPD-03 | If `birth_date < start_date` of window N and `birth_date > end_date` of window N-1 → `BIRTH_BEFORE_THIS_CYCLE` |
| BPD-04 | If `birth_date > end_date` of last window → `BIRTH_AFTER_LAST_CYCLE` |
| BPD-05 | Classification is per-window-type (Sade Sati, Elinati, Ashtama) — independent |
| BPD-06 | Output includes: position enum, cycle_number, phase, human-readable description |

**Outputs** (per cycle window type):
```json
{
  "position": "BIRTH_INSIDE | BIRTH_BEFORE_THIS_CYCLE | BIRTH_BEFORE_FIRST_CYCLE | BIRTH_AFTER_LAST_CYCLE",
  "cycle_number": "integer",
  "phase": "string",
  "description": "string"
}
```

---

### 7.5 Capability: CanonicalReferenceDataAccess

**Purpose**: Provide read-only access to canonical registries.

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| CRD-01 | Registries are loaded once at startup; never modified at runtime |
| CRD-02 | Registries are versioned; engine declares required registry version |
| CRD-03 | Missing or mismatched registry version → hard error (fail-fast) |
| CRD-04 | No engine embeds registry data; all access via this capability |

---

## 8. Lifetime Projection — Governance Rules, Edge Cases, Versioning (Normative)

### 8.1 Deterministic Governance Rules

| Rule ID | Rule |
|---------|------|
| LPG-01 | **Canonical JSON is the sole temporal anchor**. The Saturn `start_date`/`end_date` in Canonical JSON defines the current cycle anchor. No external date sources. |
| LPG-02 | **Fixed 30-month Rasi duration**. No variation for retrograde, variable speed, or astronomical precision. |
| LPG-03 | **30-year cycle periodicity**. Cycles extend infinitely in both directions mathematically; practically bounded by governance horizon. |
| LPG-04 | **Sade Sati = 3 consecutive Rasis**. Rising (12th), Peak (1st), Setting (2nd) from Moon Rasi. |
| LPG-05 | **Elinati/Ashtama = single Rasi at 8th offset**. Both map to Mandali 8; distinction is interpretive (AnswerComposer). |
| LPG-06 | **Birth detection is per-window-type**. A native can be INSIDE Sade Sati but BEFORE Elinati Shani. |
| LPG-07 | **Cycle numbering**: Cycle 0 = cycle containing Canonical JSON anchor. Negative = past. Positive = future. |

### 8.2 Edge Cases

| Edge Case | Governance Resolution |
|-----------|----------------------|
| Birth date exactly on window boundary (start or end) | **Inclusive**: `birth_date ∈ [start, end]` → `BIRTH_INSIDE` |
| Canonical JSON Saturn transit spans Rasi boundary | Canonical JSON provides single Rasi; 30-month rule applies from `start_date` |
| Birth date before first projected cycle | `BIRTH_BEFORE_FIRST_CYCLE` with `cycle_number` of earliest projected cycle |
| Birth date after governance horizon | `BIRTH_AFTER_LAST_CYCLE` with `cycle_number` of latest projected cycle |
| Canonical JSON missing Saturn transit | **Invalid input** — hard error (Saturn is mandatory for Sade Sati) |
| Registry version mismatch | **Hard error** — fail-fast (CRD-03) |
| Leap years / month-length variations | **Ignored** — 30 months = 30 × 30 days = 900 days fixed; date arithmetic uses fixed increments |

### 8.3 Versioning Guidance

| Version | Scope | Migration |
|---------|-------|-----------|
| **v1.0** | Initial Model A release | — |
| **v1.x** | Bug fixes in date arithmetic, registry updates | Backward compatible; same output for same input |
| **v2.0** | Schema changes to `mandali_advisory` output | Requires governance approval; AnswerComposer migration path documented |
| **Model B** | Appendix only; no Model A version dependency | Model B defines its own versioning |

**Registry Versioning**: Canonical Reference Data Registries carry independent version (e.g., `nakshatra_pada_registry.v1.json`). Engine declares `required_registry_version` in manifest.

---

## 9. MandaliGenerator — Refactored Capability (Normative)

**Governance Decision**: MandaliGenerator is **refactored**, not deprecated. Its longitude-based computation is replaced by Pada-based capabilities.

### 9.1 Legacy MandaliGenerator (Deprecated Interface)

| Legacy Method | Status | Replacement |
|---------------|--------|-------------|
| `get_absolute_pada(longitude_deg)` | **Deprecated** — Model A never calls | `NakshatraPadaResolver.resolve(nakshatra, pada)` |
| `generate_mandali_grid(moon_pada)` | **Refactored** → `MandaliGridConstruction` capability | Capability 7.1 |
| `resolve_transit_mandali(longitude, moon_pada)` | **Deprecated** — Model A never calls | `TransitMandaliResolution` capability |
| `evaluate(transit_payload, natal_payload)` | **Refactored** → Universal Mandali Engine composition | Engine composition |

### 9.2 New Capability: NakshatraPadaResolver

**Purpose**: Convert (Nakshatra, Pada) → Absolute Pada (1-108) using Canonical Registry.

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| NPR-01 | Input: `nakshatra` (string), `pada` (1-4) from Canonical JSON |
| NPR-02 | Lookup in `nakshatra_pada_registry` — exact match required |
| NPR-03 | Output: absolute pada index (1-108) |
| NPR-04 | No longitude input; no trigonometric calculation |
| NPR-05 | Missing nakshatra/pada in registry → hard error |

---

## 10. Engine Responsibility Matrix (Normative)

| Capability | Universal Mandali Engine | PlanetStrength Engine | HouseStrength Engine | Dasha Engine | Answer Composer |
|------------|-------------------------|----------------------|---------------------|--------------|-----------------|
| Planetary Longitude | **NEVER** | Computes (Shadbala) | Consumes | Consumes | NEVER |
| Rasi/Nakshatra/Pada (Natal) | Consumes (Canonical) | Computes | Consumes | Consumes | Consumes (text) |
| Transit Positions (Current) | Consumes (Canonical) | NEVER | NEVER | NEVER | NEVER |
| Mandali Grid Construction | **OWNS** (Cap 7.1) | NEVER | NEVER | NEVER | NEVER |
| Transit → Mandali Resolution | **OWNS** (Cap 7.2) | NEVER | NEVER | NEVER | NEVER |
| Sade Sati/Elinati/Ashtama Projection | **OWNS** (Cap 7.3) | NEVER | NEVER | NEVER | NEVER |
| Birth Position Detection | **OWNS** (Cap 7.4) | NEVER | NEVER | NEVER | NEVER |
| Canonical Reference Data | Consumes (Cap 7.5) | Consumes | Consumes | Consumes | Consumes |
| Strength Scores | NEVER | **OWNS** | **OWNS** | NEVER | Consumes |
| Dasha Timing Multipliers | NEVER | NEVER | NEVER | **OWNS** | Consumes |
| Interpretation Text | NEVER | NEVER | NEVER | NEVER | **OWNS** (canonical) |
| Mandali Advisory Output | **PRODUCES** | NEVER | NEVER | NEVER | Consumes |

**Invariant**: No engine computes what another engine owns (CGP-08, CGP-09).

---

## 11. Data Flow — Model A Pipeline (Normative)

```
CANONICAL JSON
     │
     │  Read (read-only):
     │  • natal.moon.{rasi, nakshatra, pada}
     │  • current_transit[].{planet, rasi, nakshatra, pada, start_date, end_date, house_from_moon}
     │  • natal.birth_date
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL MANDALI ENGINE                                 │
│  Capability Composition:                                                    │
│  1. CanonicalReferenceDataAccess → loads registries                         │
│  2. NakshatraPadaResolver → (nakshatra, pada) → absolute_pada              │
│  3. MandaliGridConstruction → natal_moon → mandali_grid[1..12]             │
│  4. TransitMandaliResolution → transit_planets + grid → mandali per planet │
│  5. LifetimeCycleProjection → saturn_transit + birth_date → cycles[]       │
│  6. BirthPositionDetection → birth_date + cycles → position per window     │
│                                                                             │
│  All steps: deterministic, stateless, traceable to Canonical JSON + Rules  │
└─────────────────────────────────────────────────────────────────────────────┘
     │
     │ Output: mandali_advisory (versioned schema)
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ANSWER COMPOSER                                     │
│  • Receives: mandali_advisory + canonical interpretation text              │
│  • Composes: Final report with Mandali advisory block                      │
│  • Renders: PDF / PWA / Web                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Output Contract — mandali_advisory Schema (Normative)

```json
{
  "schema_version": "1.0",
  "reference_moon": {
    "rasi": "string",
    "nakshatra": "string",
    "pada": "integer",
    "mandali_1_center": "string"
  },
  "current_transit_mandali": {
    "planet_name": {
      "mandali_number": "integer",
      "mandali_name": "string",
      "original_rasi": "string",
      "original_nakshatra": "string",
      "original_pada": "integer",
      "house_from_moon_classical": "integer",
      "house_from_moon_mandali": "integer",
      "status": "FAVORABLE | NEUTRAL | CHALLENGING",
      "interpretation_key": "string"
    }
  },
  "sade_sati": {
    "cycles": [
      {
        "cycle_number": "integer",
        "period": "string",
        "sade_sati_windows": [
          { "phase": "Rising|Peak|Setting", "rasi": "string", "mandali": "integer", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "birth_position": "enum" }
        ]
      }
    ],
    "birth_detection": {
      "position": "enum",
      "cycle": "integer",
      "phase": "string",
      "description": "string"
    }
  },
  "elinati_shani": { "same_structure_as_sade_sati" },
  "ashtama_shani": { "same_structure_as_sade_sati" },
  "timeline": [
    { "period": "string", "cycle": "integer", "events": ["string"] }
  ]
}
```

**Contract Stability**: `schema_version` increments only on governance-approved breaking changes. AnswerComposer must handle `schema_version` explicitly.

---

## 13. Implementation Responsibilities (Normative)

| Component | Responsibility | Governance Status |
|-----------|----------------|-------------------|
| `CanonicalJSONLoader` | Load/validate Canonical JSON transit section | **New** — single parser |
| `NakshatraPadaRegistry` | Load/provide nakshatra-pada sequence & mappings | **New** — canonical registry |
| `RasiSequenceRegistry` | Load/provide rasi sequence | **New** — canonical registry |
| `NakshatraPadaResolver` | (Nakshatra, Pada) → Absolute Pada | **New** — replaces longitude-based pada calc |
| `MandaliGridConstruction` | Build 12-Mandali grid from Moon Pada | **Refactored** from MandaliGenerator |
| `TransitMandaliResolution` | Resolve transit planets to Mandali numbers | **Refactored** from MandaliGenerator |
| `LifetimeCycleProjection` | Project Saturn cycles bidirectionally | **New** |
| `BirthPositionDetection` | Classify birth position per window | **New** |
| `UniversalMandaliEngine` | Compose capabilities 1-7; produce mandali_advisory | **New** — capability orchestrator |
| `PipelineRunner` | Wire UniversalMandaliEngine into pipeline | **Revised** |
| `AnswerComposer` | Accept mandali_advisory; compose final report | **Revised** |
| `MandaliGenerator` (legacy) | **Refactored** — longitude methods deprecated; Pada methods retained for Model B appendix | **Refactored** |

---

## 14. Illustrative Examples (Non-Normative)

> **Note**: The following examples are **illustrative only**. They demonstrate the governance rules in action but are not part of the normative specification. Implementations must conform to the normative rules in Sections 5-13.

### 14.1 Worked Example — Raju Chart (Canonical JSON Pages 85-86)

**Input (from Canonical JSON):**
- Natal Moon: Makara Rasi, Dhanishta Nakshatra, Pada 2
- Birth Date: (from natal section)
- Current Transits:
  - Saturn: Meena Rasi, Uttara Bhadrapada Nakshatra, Pada 3 (30/03/2025 - 03/06/2027)
  - Jupiter: Mithuna Rasi, Mrigashira Nakshatra, Pada 2 (05/12/2025 - 02/06/2026)
  - Rahu: Kumbha Rasi, Shatabhisha Nakshatra, Pada 1 (18/05/2025 - 05/12/2026)

**Step 1 — NakshatraPadaResolver (NPR-01 to NPR-05):**
- Dhanishta Pada 2 → Absolute Pada 90 (via Registry)
- Uttara Bhadrapada Pada 3 → Absolute Pada 10 (via Registry)
- Mrigashira Pada 2 → Absolute Pada 64 (via Registry)
- Shatabhisha Pada 1 → Absolute Pada 95 (via Registry)

**Step 2 — MandaliGridConstruction (MGC-01 to MGC-07):**
- Moon Absolute Pada = 90 → Mandali 1 center
- Mandali 1: center=90 (Dhanishta P2, Makara), padas=86-94
- Mandali 2: center=99 (Shatabhisha P3, Kumbha), padas=95-103
- Mandali 3: center=1 (Purva Bhadrapada P1, Meena), padas=104-108,1-4
- Mandali 4: center=10 (Uttara Bhadrapada P2, Meena), padas=5-13
- ... (all 12 Mandalis constructed per MGC-03, MGC-04)

**Step 3 — TransitMandaliResolution (TMR-01 to TMR-05):**
- Saturn Absolute Pada 10 ∈ Mandali 4 padas → Mandali 4
- Jupiter Absolute Pada 64 ∈ Mandali 10 padas → Mandali 10
- Rahu Absolute Pada 95 ∈ Mandali 2 padas → Mandali 2

**Step 4 — LifetimeCycleProjection (LCP-01 to LCP-10):**
- Saturn anchor: Meena Rasi, start 30/03/2025
- Moon Rasi: Makara (index 9 in Rasi Sequence)
- Saturn Rasi: Meena (index 11) → offset = (11-9) mod 12 = 2
- Cycle 0 (2025-2055): Meena→Mesha→Vrishabha→Mithuna→Karkata→Simha→Kanya→Tula→Vrishchika→Dhanus→Makara→Kumbha
- Sade Sati windows Cycle 0: Dhanus (12), Makara (1), Kumbha (2) → 2025-2032
- Cycle -1 (1995-2025): ... Sade Sati 1995-2002
- Cycle -2 (1965-1995): ... Sade Sati 1965-1972

**Step 5 — BirthPositionDetection (BPD-01 to BPD-06):**
- Compare birth_date to each window → classify INSIDE/BEFORE/AFTER per cycle

**Output**: `mandali_advisory` per Section 12 schema.

---

## 15. Summary of Changes from Version 2

| Aspect | Version 2 | Version 2.1 (This Report) |
|--------|-----------|---------------------------|
| **Pseudocode** | Implementation-oriented algorithms | **Deterministic governance rules & invariants** |
| **Astronomical Lookup** | Embedded in algorithms | **Removed**; Canonical Reference Data Registry |
| **Class Definitions** | Fixed implementation classes | **Capability-based responsibilities** |
| **MandaliGenerator** | Deprecated | **Refactored** into Pada-based capabilities |
| **Lifetime Projection** | Algorithm description | **Governance rules, edge cases, versioning** |
| **Constitutional Principles** | Implicit | **Explicit CGP-01 to CGP-10** |
| **Normative vs Illustrative** | Mixed | **Clearly separated** (Sections 5-13 normative; Section 14 illustrative) |
| **Output Contract** | Example structure | **Versioned schema with stability rules** |
| **Registry Management** | Not specified | **Canonical Reference Data Registry with versioning** |

---

## 16. Approval Request

This **Architecture Revision Report v2.1** defines the final engineering governance for **Model A** Universal Gochara Mandali Engine.

**Please review and approve** before expanding into the complete `GOCHARA_MANDALI_GOVERNANCE_v1.md` governance document.

### Checklist for Approval
- [ ] Constitutional Governance Principles (CGP-01 to CGP-10) accepted
- [ ] Model A vs Model B boundary confirmed
- [ ] Canonical JSON Input Contract (Section 5) accepted
- [ ] Canonical Reference Data Registry (Section 6) accepted
- [ ] Capability Specifications (Section 7) accepted
- [ ] Lifetime Projection Governance (Section 8) accepted
- [ ] MandaliGenerator Refactoring (Section 9) accepted
- [ ] Engine Responsibility Matrix (Section 10) accepted
- [ ] Output Contract Schema (Section 12) accepted
- [ ] Implementation Responsibilities (Section 13) accepted
- [ ] Normative/Illustrative separation confirmed

---

*End of Architecture Revision Report v2.1*