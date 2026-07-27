# GOCHARA_MANDALI_GOVERNANCE_v1.md
## Universal Gochara Mandali Engine — Model A
### Canonical Engineering Governance for Golden Master Version 1.0

---

## Document Control

| Attribute | Value |
|-----------|-------|
| Document ID | GOCHARA_MANDALI_GOVERNANCE_v1.md |
| Version | 1.0.0 |
| Status | FROZEN — Golden Master Canonical |
| Authority | Chief Architect |
| Classification | Normative Engineering Governance |
| Supersedes | All previous Gochara drafts, experimental transit models, legacy transit boundary definitions |
| Effective Date | Upon approval |

**Governance Freeze**: This document is the single authoritative Gochara specification for the Samartha Astro-AI system. All future Gochara implementations must follow this document. No modifications without governance approval.

---

## 1. Constitutional Governance Principles

The following principles are **permanent, non-negotiable, and version-locked**. They govern all Model A implementations and future Model B compatibility.

| ID | Principle | Normative Rule |
|----|-----------|----------------|
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

## 2. Model A Constitutional Rules

The following rules are **frozen constitutional requirements** for Model A.

### 2.1 Canonical JSON Only
Model A consumes only Canonical JSON. No Swiss Ephemeris. No longitude. No astronomy. No orbital mathematics.

### 2.2 Read Only
The engine only reads from Canonical JSON:
- Natal Moon (Rasi, Nakshatra, Pada)
- Transit Planets (Planet, Rasi, Nakshatra, Pada, start_date, end_date, house_from_moon)
- Birth Date

It never changes Canonical JSON.

### 2.3 Reference Frame Transformation Only
The engine performs only:
```
Moon Reference Frame → Universal Mandali
```
Nothing more.

### 2.4 Independent Advisory Engine
Universal Gochara Mandali is an **independent advisory engine**.
- It is NOT a scoring engine.
- It is NOT a strength engine.
- It is NOT a probability engine.
- It is NOT a calibration engine.
- Its responsibility ends with producing its own advisory output.

### 2.5 Independent Output Rule
Universal Gochara Mandali produces only `mandali_advisory` or equivalent standalone advisory objects.

It must **never modify**:
- Planet Strength
- Bhava Strength
- Rasi Strength
- Varga Strength
- Dasha Strength
- Ashtakavarga
- Functional Nature
- Yoga Scores
- Natal Promise
- Master Probability
- Existing report scores
- Existing percentages
- Existing weights
- Existing multipliers

### 2.6 Shared Canonical Transit
If Canonical JSON transit data is already used elsewhere, Universal Gochara Mandali may read exactly the same data.

It must **NOT**:
- Overwrite
- Reinterpret
- Replace
- Recalculate
- Influence

those engine outputs.

Multiple engines may consume the same Canonical JSON. Each engine owns only its own output.

### 2.7 No Hidden Integration
The following are **permanently prohibited**:
- PlanetStrength × Mandali
- BhavaStrength × Mandali
- Dasha × Mandali
- Probability × Mandali
- Yoga × Mandali
- Transit Score × Mandali
- Master Probability × Mandali
- Natal Promise × Mandali

No bonuses. No penalties. No modifiers. No multipliers. No hidden weighting.

### 2.8 Standalone Report Section
Universal Gochara Mandali shall appear as its own report section:

```
GOCHARA MANDALI ADVISORY
├── Current Mandali
├── Current Transit Positions
├── Mandali Activations
├── Sade Sati
├── Elinati Shani
├── Ashtama Shani
├── Important Advisory Statements
└── Upcoming Mandali Events
```

It shall **not** be merged into:
- Planet Strength
- Bhava Strength
- Any existing report

### 2.9 Future Integration
If someday Mandali must influence another engine, that requires:
- New governance
- New formulas
- Validation
- Calibration
- Version approval

Until then, Mandali remains **Advisory Only**.

---

## 3. Model A vs Model B — Architectural Boundary

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

## 4. System Architecture — Model A

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

## 5. Canonical JSON Transit Schema — Model A Input Contract

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

## 6. Canonical Reference Data Registry

**Governance Rule CGP-09**: Shared reference data is externalized to a single canonical registry. Engines consume; they do not redefine.

### 6.1 Nakshatra-Pada Sequence Registry
**Registry ID**: `nakshatra_pada_registry`
**Version**: 1.0
**Location**: `backend/app/config/nakshatra_pada_registry.json`

| Absolute Pada (1-108) | Nakshatra | Pada | Rasi |
|----------------------|-----------|------|------|
| 1 | Ashwini | 1 | Mesha |
| 2 | Ashwini | 2 | Mesha |
| 3 | Ashwini | 3 | Mesha |
| 4 | Ashwini | 4 | Mesha |
| 5 | Bharani | 1 | Mesha |
| ... | ... | ... | ... |
| 108 | Revati | 4 | Meena |

**Completeness Requirement**: All 27 Nakshatras × 4 Padas = 108 entries. No gaps. No duplicates.

### 6.2 Nakshatra → Rasi Mapping Registry
**Registry ID**: `nakshatra_rasi_registry`
**Version**: 1.0
**Location**: `backend/app/config/nakshatra_rasi_registry.json`

| Nakshatra | Rasi |
|-----------|------|
| Ashwini, Bharani, Krittika (p1) | Mesha |
| Krittika (p2-4), Rohini, Mrigashira (p1-2) | Vrishabha |
| Mrigashira (p3-4), Ardra, Punarvasu (p1-3) | Mithuna |
| ... | ... |

**Completeness Requirement**: All 27 Nakshatras mapped. Pada-level granularity where Nakshatra spans Rasi boundary.

### 6.3 Rasi Sequence Registry
**Registry ID**: `rasi_sequence_registry`
**Version**: 1.0
**Location**: `backend/app/config/rasi_sequence_registry.json`

`["Mesha", "Vrishabha", "Mithuna", "Karkata", "Simha", "Kanya", "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"]`

**Completeness Requirement**: Exactly 12 Rasis in zodiacal order.

### 6.4 Registry Governance Rules
| Rule ID | Rule |
|---------|------|
| CRD-01 | Registries are loaded once at startup; never modified at runtime |
| CRD-02 | Registries are versioned; engine declares required registry version |
| CRD-03 | Missing or mismatched registry version → hard error (fail-fast) |
| CRD-04 | No engine embeds registry data; all access via CanonicalReferenceData capability |

---

## 7. Capability Specifications

The Universal Mandali Engine composes the following capabilities. Each capability has a single owner, defined inputs, deterministic rules, and defined outputs.

### 7.1 Capability: CanonicalReferenceDataAccess
**Purpose**: Provide read-only access to canonical registries.
**Owner**: Universal Mandali Engine

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| CRD-01 | Registries loaded once at startup; never modified at runtime |
| CRD-02 | Registries versioned; engine declares required registry version |
| CRD-03 | Missing or mismatched registry version → hard error (fail-fast) |
| CRD-04 | No engine embeds registry data; all access via this capability |

---

### 7.2 Capability: NakshatraPadaResolver
**Purpose**: Convert (Nakshatra, Pada) → Absolute Pada (1-108) using Canonical Registry.
**Owner**: Universal Mandali Engine

**Inputs**:
- `nakshatra` (string) — from Canonical JSON
- `pada` (integer 1-4) — from Canonical JSON
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| NPR-01 | Input: `nakshatra` (string), `pada` (1-4) from Canonical JSON |
| NPR-02 | Lookup in `nakshatra_pada_registry` — exact match required |
| NPR-03 | Output: absolute pada index (1-108) |
| NPR-04 | No longitude input; no trigonometric calculation |
| NPR-05 | Missing nakshatra/pada in registry → hard error |

**Output**: `absolute_pada` (integer 1-108)

---

### 7.3 Capability: MandaliGridConstruction
**Purpose**: Construct the 12-Mandali grid centered on the Natal Moon Pada.
**Owner**: Universal Mandali Engine

**Inputs**:
- `natal_moon_nakshatra` (string) — from Canonical JSON
- `natal_moon_pada` (integer 1-4) — from Canonical JSON
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| MGC-01 | Moon Absolute Pada = `NakshatraPadaResolver(natal_moon_nakshatra, natal_moon_pada)` |
| MGC-02 | Mandali 1 center = Moon Absolute Pada |
| MGC-03 | Mandali N center = `((Moon_Absolute_Pada + (N-1)×9 - 1) mod 108) + 1` |
| MGC-04 | Each Mandali contains exactly 9 padas: center ±4 (modulo 108 wrap) |
| MGC-05 | All 108 padas covered exactly once across 12 Mandalis (no gaps, no overlaps) |
| MGC-06 | Mandali Rasi name = Rasi of center pada's Nakshatra (from `nakshatra_rasi_registry`) |
| MGC-07 | Output is deterministic: identical inputs → identical grid |

**Output**: `mandali_grid[1..12]` where each entry contains:
- `number` (1-12)
- `center_pada` (1-108)
- `center_nakshatra` (string)
- `center_pada_num` (1-4)
- `rasi_name` (string)
- `padas` (array of 9 absolute pada indices)
- `pada_details` (array of 9 {nakshatra, pada} from Registry)

---

### 7.4 Capability: TransitMandaliResolution
**Purpose**: Resolve each transit planet's Canonical JSON position to a Mandali number.
**Owner**: Universal Mandali Engine

**Inputs**:
- `transit_planets[]` — from Canonical JSON (each: planet, rasi, nakshatra, pada)
- `mandali_grid[1..12]` — from MandaliGridConstruction
- `nakshatra_pada_registry` — from Canonical Reference Data Registry

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| TMR-01 | Transit Absolute Pada = `NakshatraPadaResolver(transit_nakshatra, transit_pada)` |
| TMR-02 | Transit Mandali = unique Mandali N where Transit Absolute Pada ∈ `mandali_grid[N].padas` |
| TMR-03 | Exactly one Mandali contains the transit pada (guaranteed by MGC-05) |
| TMR-04 | Original Canonical JSON values (rasi, nakshatra, pada) are preserved in output — never modified |
| TMR-05 | Classical `house_from_moon` from Canonical JSON is preserved alongside Mandali number |

**Output** (per transit planet):
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

### 7.5 Capability: LifetimeCycleProjection
**Purpose**: Project Saturn's 30-year cycles bidirectionally from Canonical JSON transit dates.
**Owner**: Universal Mandali Engine

**Inputs**:
- `natal_moon_rasi` — from Canonical JSON
- `birth_date` — from Canonical JSON (DD.MM.YYYY)
- `saturn_transit` — from Canonical JSON current_transit (planet="Saturn")
- `rasi_sequence_registry` — from Canonical Reference Data Registry

**Governance Rules**:
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

**Output**: `cycles[]` where each cycle contains:
- `cycle_number` (integer, ... -1, 0, 1, 2 ... where 0 = cycle containing Canonical JSON anchor)
- `period` (string: "YYYY-YYYY")
- `sade_sati_windows[]` (3 per cycle: Rising, Peak, Setting)
- `elinati_shani_windows[]` (1 per cycle)
- `ashtama_shani_windows[]` (1 per cycle)

---

### 7.6 Capability: BirthPositionDetection
**Purpose**: Classify native's birth position relative to each major cycle window.
**Owner**: Universal Mandali Engine

**Inputs**:
- `birth_date` — from Canonical JSON
- `cycle_windows[]` — from LifetimeCycleProjection (each with start_date, end_date, cycle_number, phase)

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| BPD-01 | For each window: if `birth_date ∈ [start_date, end_date]` → `BIRTH_INSIDE` |
| BPD-02 | If `birth_date < start_date` of first window → `BIRTH_BEFORE_FIRST_CYCLE` |
| BPD-03 | If `birth_date < start_date` of window N and `birth_date > end_date` of window N-1 → `BIRTH_BEFORE_THIS_CYCLE` |
| BPD-04 | If `birth_date > end_date` of last window → `BIRTH_AFTER_LAST_CYCLE` |
| BPD-05 | Classification is per-window-type (Sade Sati, Elinati, Ashtama) — independent |
| BPD-06 | Output includes: position enum, cycle_number, phase, human-readable description |

**Output** (per cycle window type):
```json
{
  "position": "BIRTH_INSIDE | BIRTH_BEFORE_THIS_CYCLE | BIRTH_BEFORE_FIRST_CYCLE | BIRTH_AFTER_LAST_CYCLE",
  "cycle_number": "integer",
  "phase": "string",
  "description": "string"
}
```

---

### 7.7 Capability: UniversalMandaliEngine (Orchestrator)
**Purpose**: Compose capabilities 7.1–7.6; produce `mandali_advisory` output.
**Owner**: Universal Mandali Engine

**Governance Rules**:
| Rule ID | Rule |
|---------|------|
| UME-01 | Executes capabilities in sequence: 7.1 → 7.2 → 7.3 → 7.4 → 7.5 → 7.6 |
| UME-02 | All steps deterministic, stateless, traceable to Canonical JSON + Rules |
| UME-03 | Produces only `mandali_advisory` — no scores, no strengths, no probabilities |
| UME-04 | Never modifies other engine outputs (CGP-05, CGP-07) |
| UME-05 | Output schema versioned per CGP-10 |

---

## 8. Lifetime Projection — Governance Rules, Edge Cases, Versioning

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

## 9. MandaliGenerator — Refactored Capability

**Governance Decision**: MandaliGenerator is **refactored**, not deprecated. Its longitude-based computation is replaced by Pada-based capabilities.

### 9.1 Legacy MandaliGenerator Interface Mapping
| Legacy Method | Status | Replacement |
|---------------|--------|-------------|
| `get_absolute_pada(longitude_deg)` | **Deprecated** — Model A never calls | `NakshatraPadaResolver.resolve(nakshatra, pada)` |
| `generate_mandali_grid(moon_pada)` | **Refactored** → `MandaliGridConstruction` capability | Capability 7.3 |
| `resolve_transit_mandali(longitude, moon_pada)` | **Deprecated** — Model A never calls | `TransitMandaliResolution` capability |
| `evaluate(transit_payload, natal_payload)` | **Refactored** → Universal Mandali Engine composition | Capability 7.7 |

### 9.2 Retained for Model B Appendix
Pada-based methods of MandaliGenerator are retained solely for Model B appendix compatibility. They are not used in Model A execution path.

---

## 10. Engine Responsibility Matrix

| Capability | Universal Mandali Engine | PlanetStrength Engine | HouseStrength Engine | Dasha Engine | Answer Composer |
|------------|-------------------------|----------------------|---------------------|--------------|-----------------|
| Planetary Longitude | **NEVER** | Computes (Shadbala) | Consumes | Consumes | NEVER |
| Rasi/Nakshatra/Pada (Natal) | Consumes (Canonical) | Computes | Consumes | Consumes | Consumes (text) |
| Transit Positions (Current) | Consumes (Canonical) | NEVER | NEVER | NEVER | NEVER |
| Mandali Grid Construction | **OWNS** (Cap 7.3) | NEVER | NEVER | NEVER | NEVER |
| Transit → Mandali Resolution | **OWNS** (Cap 7.4) | NEVER | NEVER | NEVER | NEVER |
| Sade Sati/Elinati/Ashtama Projection | **OWNS** (Cap 7.5) | NEVER | NEVER | NEVER | NEVER |
| Birth Position Detection | **OWNS** (Cap 7.6) | NEVER | NEVER | NEVER | NEVER |
| Canonical Reference Data | Consumes (Cap 7.1) | Consumes | Consumes | Consumes | Consumes |
| Strength Scores | NEVER | **OWNS** | **OWNS** | NEVER | Consumes |
| Dasha Timing Multipliers | NEVER | NEVER | NEVER | **OWNS** | Consumes |
| Interpretation Text | NEVER | NEVER | NEVER | NEVER | **OWNS** (canonical) |
| Mandali Advisory Output | **PRODUCES** | NEVER | NEVER | NEVER | Consumes |

**Invariant**: No engine computes what another engine owns (CGP-08, CGP-09).

---

## 11. Data Flow — Model A Pipeline

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

## 12. Output Contract — mandali_advisory Schema

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

## 13. Implementation Responsibilities

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

## 14. Standalone Report Section — GOCHARA MANDALI ADVISORY

The Universal Gochara Mandali Engine output shall render as a standalone report section:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GOCHARA MANDALI ADVISORY                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CURRENT MANDALI                                                            │
│  ─────────────────                                                          │
│  Reference Moon: [Rasi] [Nakshatra] Pada [N]                               │
│  Mandali 1 Center: [Nakshatra] Pada [N]                                    │
│  Current Active Mandali: [Mandali Number] — [Mandali Name]                 │
│                                                                             │
│  CURRENT TRANSIT POSITIONS                                                  │
│  ──────────────────────────                                                 │
│  ┌─────────┬──────────┬────────────┬────────┬────────────┬──────────────┐ │
│  │ Planet  │ Original │ Mandali    │ Class. │ Mandali    │ Status       │ │
│  │         │ Rasi     │ Number     │ House  │ House      │              │ │
│  ├─────────┼──────────┼────────────┼────────┼────────────┼──────────────┤ │
│  │ Saturn  │ Meena    │ 4          │ 3      │ 4          │ FAVORABLE    │ │
│  │ Jupiter │ Mithuna  │ 10         │ 6      │ 10         │ NEUTRAL      │ │
│  │ Rahu    │ Kumbha   │ 2          │ 2      │ 2          │ CHALLENGING  │ │
│  └─────────┴──────────┴────────────┴────────┴────────────┴──────────────┘ │
│                                                                             │
│  MANDALI ACTIVATIONS                                                        │
│  ──────────────────                                                         │
│  Active Mandalis: [4, 10, 2]                                               │
│  Activated Planets: Saturn, Jupiter, Rahu                                  │
│                                                                             │
│  SADE SATI                                                                  │
│  ─────────                                                                  │
│  Current Cycle: 3                                                           │
│  Current Phase: Rising                                                      │
│  Current Window: Dhanus (Mandali 12) — 30/03/2025 to 03/06/2027           │
│  Birth Detection: INSIDE (Cycle 2, Peak Phase)                             │
│  Lifetime Summary: 3 cycles projected (1965-2055)                          │
│                                                                             │
│  ELINATI SHANI                                                              │
│  ─────────────                                                              │
│  Current Cycle: 3                                                           │
│  Current Window: [Rasi] (Mandali 8) — [dates]                              │
│  Birth Detection: [position]                                                │
│                                                                             │
│  ASHTAMA SHANI                                                              │
│  ──────────────                                                             │
│  Current Cycle: 3                                                           │
│  Current Window: [Rasi] (Mandali 8) — [dates]                              │
│  Birth Detection: [position]                                                │
│                                                                             │
│  IMPORTANT ADVISORY STATEMENTS                                              │
│  ──────────────────────────────                                             │
│  • [Canonical interpretation text for current transits]                    │
│  • [Sade Sati phase guidance]                                              │
│  • [Elinati/Ashtama guidance]                                              │
│                                                                             │
│  UPCOMING MANDALI EVENTS                                                    │
│  ─────────────────────────                                                  │
│  • [Date] — Saturn enters [Rasi] (Mandali [N]) — [Phase]                  │
│  • [Date] — Jupiter enters [Rasi] (Mandali [N]) — [Phase]                 │
│  • [Date] — Sade Sati Peak begins (Mandali 1)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Rendering Rules**:
- This section appears **after** all existing report sections
- This section is **independent** — no cross-references to Planet Strength, Bhava Strength, etc.
- Canonical interpretation text is used verbatim from Canonical JSON
- Status (FAVORABLE/NEUTRAL/CHALLENGING) derived from Mandali position per governance rules

---

## 15. Pipeline Integration

### 15.1 PipelineRunner Integration
```python
# PipelineRunner.execute() — normative integration point
def execute(self, canonical_json, ...):
    # Existing engines (unchanged)
    planet_strengths = PlanetStrengthEngine.evaluate(...)
    house_strengths = HouseStrengthEngine.evaluate(...)
    dasha_results = DashaEngine.evaluate(...)
    
    # NEW: Universal Mandali Engine (Advisory Only)
    mandali_advisory = UniversalMandaliEngine.evaluate(canonical_json)
    
    # AnswerComposer receives all independently
    return AnswerComposer.compose(
        planet_strengths=planet_strengths,
        house_strengths=house_strengths,
        dasha_results=dasha_results,
        mandali_advisory=mandali_advisory,  # NEW PARAMETER
        canonical_text_refs=canonical_json
    )
```

### 15.2 AnswerComposer Integration
- Receives `mandali_advisory` as independent parameter
- Renders `GOCHARA MANDALI ADVISORY` section per Section 14
- Does **not** combine Mandali output with any other engine output
- Does **not** modify any other engine output based on Mandali

---

## 16. Validation Checklist — Golden Master Version 1.0

Before any Model A implementation is accepted, it must pass all checks:

| Check ID | Validation | Pass/Fail |
|----------|------------|-----------|
| **VAL-01** | No Swiss Ephemeris import or dependency | ☐ |
| **VAL-02** | No planetary longitude computation | ☐ |
| **VAL-03** | No astronomical/orbital mathematics | ☐ |
| **VAL-04** | Canonical JSON is sole data source | ☐ |
| **VAL-05** | Original Rasi/Nakshatra/Pada never modified | ☐ |
| **VAL-06** | Only reference frame transformation performed | ☐ |
| **VAL-07** | Output is only `mandali_advisory` | ☐ |
| **VAL-08** | No modification of Planet/Bhava/Rasi/Varga/Dasha/Ashtakavarga/Functional Nature/Yoga/Natal Promise/Master Probability | ☐ |
| **VAL-09** | No hidden integration (bonuses, penalties, multipliers, weights) | ☐ |
| **VAL-10** | Standalone GOCHARA MANDALI ADVISORY report section | ☐ |
| **VAL-11** | Mandali section not merged into any existing report | ☐ |
| **VAL-12** | Deterministic: identical input → identical output | ☐ |
| **VAL-13** | All capabilities traceable to Canonical JSON + named rules | ☐ |
| **VAL-14** | Registry versioning enforced (fail-fast on mismatch) | ☐ |
| **VAL-15** | Engine isolation: no cross-engine computation | ☐ |
| **VAL-16** | Output schema versioned; AnswerComposer handles version | ☐ |
| **VAL-17** | Lifetime projection uses fixed 30-month increments only | ☐ |
| **VAL-18** | Birth detection per-window-type (independent) | ☐ |
| **VAL-19** | MandaliGenerator longitude methods not called in Model A path | ☐ |
| **VAL-20** | Model B appendix only — no Model A dependency | ☐ |

---

## 17. Appendix — Model B Compatibility (Informative Only)

Model B is documented here for future compatibility. **No Model A code depends on this appendix.**

### 17.1 Model B Scope
- Source: Swiss Ephemeris (pyswisseph or equivalent)
- Input: Planetary longitudes (degrees)
- Compute: Longitude → Pada → Mandali
- Continuous timeline with high-precision astronomy
- Predictive future transits beyond Canonical JSON

### 17.2 Model B Integration Point (Future)
If Model B is implemented, it would:
- Replace `NakshatraPadaResolver` with `LongitudeToPadaResolver`
- Replace `LifetimeCycleProjection` with `EphemerisBasedProjection`
- Require new governance, formulas, validation, calibration, version approval
- **Until then**: Model A remains Advisory Only per Constitutional Rule 2.9

### 17.3 Shared Capabilities (Model A → Model B)
The following Model A capabilities are designed for Model B reuse:
- `MandaliGridConstruction` (Pada-based, no longitude dependency)
- `TransitMandaliResolution` (Pada-based)
- `BirthPositionDetection` (date-based, no astronomy)
- `CanonicalReferenceDataAccess` (registry access)

---

## 18. Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-26 | Chief Architect | Initial Golden Master Canonical release |

---

## 19. Approval Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Chief Architect | | | |
| Lead Engineer | | | |
| Governance Officer | | | |

---

**END OF GOCHARA_MANDALI_GOVERNANCE_v1.md**

*This document is FROZEN. No modifications without governance approval.*
