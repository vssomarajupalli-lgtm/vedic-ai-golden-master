# Architecture Revision Report – Version 2
## Universal Gochara Mandali Model A
### Engineering Specification for GOCHARA_MANDALI_GOVERNANCE_v1.md Upgrade

---

## 1. Executive Summary

This report revises the previous architecture analysis to align with **Model A** finalized engineering decisions. The Universal Gochara Mandali Engine is redefined as a **deterministic spatial transformation engine** that consumes **Canonical JSON transit data** (Rasi + Nakshatra + Pada) and produces **Moon-centred Universal Mandali** outputs — **without any astronomical calculations, ephemeris, or longitude computations**.

---

## 2. Section Classification: Previous Response → Model A Alignment

| # | Previous Section | Classification | Rationale |
|---|------------------|----------------|-----------|
| 1 | Executive Summary | 🔄 **Revise** | Must reflect Model A: Canonical JSON only, no ephemeris |
| 2 | Data Flow: Canonical JSON → Mandali Engine | 🔄 **Revise** | Remove ephemeris/longitude layer; direct Canonical JSON → Mandali |
| 3 | Data Flow Table | 🔄 **Revise** | Update source columns: Canonical JSON provides Rasi/Nakshatra/Pada directly |
| 4 | Gochara Mandali Engine Responsibility | 🔄 **Revise** | Redefine: Reference frame transformation only; no spatial computation from longitude |
| 5 | Unnecessary Recalculation to Avoid | ✅ **Keep** | Valid; add Model A specific items (no longitude, no ephemeris) |
| 6 | Architecture Summary Diagram | 🔄 **Revise** | Remove Ephemeris Service; show Canonical JSON as sole source |
| 7 | Implementation Status Table | 🔄 **Revise** | Remove EphemerisService blocker; add UniversalMandaliEngine |
| 8 | Critical Conclusion | 🔄 **Revise** | Update to Model A terminology and data flow |
| — | **Model A vs Model B Distinction** | ➕ **Add** | New required section per decision #10 |
| — | **Lifetime Sade Sati / Bidirectional Projection** | ➕ **Add** | New required section per decisions #8, #9 |
| — | **Birth Position Detection** | ➕ **Add** | New required section per decision #9 |
| — | **Canonical JSON Transit Schema** | ➕ **Add** | Document exact input structure from Canonical JSON |
| — | **Universal Mandali Construction Algorithm** | ➕ **Add** | Deterministic rules from Rasi/Nakshatra/Pada only |
| — | **Consultation Object Output Contract** | ➕ **Add** | Structured output for AnswerComposer |
| — | **Engineering Diagrams** | ➕ **Add** | System Architecture, Responsibility, Data Flow, Lifetime Timeline, Birth Detection |

---

## 3. Model A vs Model B — Architectural Boundary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UNIVERSAL GOCHARA MANDALI                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────┐     ┌─────────────────────────────┐      │
│   │         MODEL A             │     │         MODEL B             │      │
│   │   (CURRENT — IMPLEMENT)     │     │   (FUTURE — DOCUMENT ONLY)  │      │
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

**Decision**: Model A is the **only** implementation target. Model B is documented as future compatibility in an appendix — **no code, no dependencies, no architecture for Model B**.

---

## 4. Revised System Architecture — Model A

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE — MODEL A                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────────────┐     ┌────────────────────────┐
│  CANONICAL   │     │  UNIVERSAL GOCHARA   │     │   CONSULTATION         │
│  JSON STORE  │────▶│  MANDALI ENGINE      │────▶│   OUTPUT OBJECTS       │
│              │     │  (Model A)           │     │                        │
│  • Natal     │     │                      │     │  • Mandali Numbers     │
│    - Moon    │     │  Input:              │     │  • Transit Status      │
│    - Rasi    │     │  • Natal Moon        │     │  • Sade Sati           │
│    - Nakshatra│    │    (Rasi, Nak, Pada) │     │  • Elinati Shani       │
│    - Pada    │     │  • Current Transit   │     │  • Ashtama Shani       │
│              │     │    (Planet, Rasi,    │     │  • Lifetime Timeline   │
│  • Transit   │     │    Nakshatra, Pada)  │     │  • Birth Position      │
│    - Planet  │     │                      │     │  • Consultation Objects│
│    - Rasi    │     │  Process:            │     │                        │
│    - Nakshatra│    │  1. Moon-centred     │     └───────────┬────────────┘
│    - Pada    │     │     Mandali Grid     │                 │
│              │     │  2. Map Transit      │                 ▼
│              │     │     → Mandali #      │     ┌────────────────────────┐
│              │     │  3. Detect Cycles    │     │   ANSWER COMPOSER      │
│              │     │  4. Project Lifetime │     │                        │
│              │     │  5. Birth Detection  │     │  • Mandali Advisory    │
│              │     │                      │     │  • Canonical Text      │
└──────────────┘     └──────────────────────┘     │  • Final Report        │
                                                   └────────────────────────┘

NO EphemerisService  NO Swiss Ephemeris  NO Longitude Calculation  NO Orbital Math
```

---

## 5. Canonical JSON Transit Schema — Model A Input Contract

The Canonical JSON (pages 85–86, section "Transit / Gochara") provides **exactly** the data Model A requires:

```json
{
  "natal": {
    "moon": {
      "rasi": "Makara",
      "nakshatra": "Dhanishta",
      "pada": 2
    }
  },
  "current_transit": [
    {
      "planet": "Saturn",
      "rasi": "Meena",
      "nakshatra": "Uttara Bhadrapada",
      "pada": 3,
      "start_date": "30/03/2025",
      "end_date": "03/06/2027",
      "house_from_moon": 3,
      "interpretation": "3rd house Saturn (Upachaya)..."
    },
    {
      "planet": "Jupiter",
      "rasi": "Mithuna",
      "nakshatra": "Mrigashira",
      "pada": 2,
      "start_date": "05/12/2025",
      "end_date": "02/06/2026",
      "house_from_moon": 6,
      "interpretation": "6th house Jupiter (Shatru Jaya)..."
    },
    {
      "planet": "Rahu",
      "rasi": "Kumbha",
      "nakshatra": "Shatabhisha",
      "pada": 1,
      "start_date": "18/05/2025",
      "end_date": "05/12/2026",
      "house_from_moon": 2,
      "interpretation": "2nd house Rahu (Dhana Rahu)..."
    }
  ]
}
```

**Key Observations**:
- Canonical JSON provides **Rasi + Nakshatra + Pada** for each transit planet
- `house_from_moon` = classical Rasi-house from Moon (NOT Mandali)
- Start/end dates enable **lifetime cycle projection** via deterministic rules
- Interpretation text is **canonical reference** for AnswerComposer

---

## 6. Universal Mandali Construction Algorithm — Deterministic Rules

### 6.1 Nakshatra-Pada Reference Table (Static, Embedded)

```python
NAKSHATRA_PADA_SEQUENCE = [
    # (Nakshatra, Pada) for padas 1-108
    ("Ashwini", 1), ("Ashwini", 2), ("Ashwini", 3), ("Ashwini", 4),
    ("Bharani", 1), ("Bharani", 2), ("Bharani", 3), ("Bharani", 4),
    ("Krittika", 1), ("Krittika", 2), ("Krittika", 3), ("Krittika", 4),
    # ... all 27 nakshatras × 4 padas = 108 entries
    ("Revati", 1), ("Revati", 2), ("Revati", 3), ("Revati", 4)
]

RASI_OF_NAKSHATRA = {
    "Ashwini": "Mesha", "Bharani": "Mesha", "Krittika": "Mesha",
    "Rohini": "Vrishabha", "Mrigashira": "Vrishabha", "Ardra": "Mithuna",
    # ... complete mapping
}
```

### 6.2 Moon-Centred Mandali Grid Construction

```
ALGORITHM: build_mandali_grid(natal_moon_nakshatra, natal_moon_pada)
────────────────────────────────────────────────────────────────────
INPUT:  natal_moon_nakshatra (str), natal_moon_pada (1-4)
OUTPUT: mandali_grid[1..12] = { center_pada, padas[9], rasi_name }

1. moon_absolute_pada = nakshatra_pada_to_absolute(natal_moon_nakshatra, natal_moon_pada)
   # 1-108 index in NAKSHATRA_PADA_SEQUENCE

2. FOR mandali_num IN 1..12:
     offset = (mandali_num - 1) * 9
     center_pada = ((moon_absolute_pada + offset - 1) % 108) + 1
     
     padas = []
     FOR i IN -4..+4:
         p = ((center_pada + i - 1) % 108) + 1
         padas.append(p)
     
     center_nakshatra, center_pada_num = NAKSHATRA_PADA_SEQUENCE[center_pada - 1]
     rasi_name = RASI_OF_NAKSHATRA[center_nakshatra]
     
     mandali_grid[mandali_num] = {
         "number": mandali_num,
         "center_pada": center_pada,
         "center_nakshatra": center_nakshatra,
         "center_pada_num": center_pada_num,
         "rasi_name": rasi_name,
         "padas": padas,
         "pada_details": [NAKSHATRA_PADA_SEQUENCE[p-1] for p in padas]
     }

3. RETURN mandali_grid
```

### 6.3 Transit Planet → Mandali Number Resolution

```
ALGORITHM: resolve_transit_mandali(transit_nakshatra, transit_pada, mandali_grid)
────────────────────────────────────────────────────────────────────────────
INPUT:  transit_nakshatra (str), transit_pada (1-4), mandali_grid[1..12]
OUTPUT: mandali_number (1-12)

1. transit_absolute_pada = nakshatra_pada_to_absolute(transit_nakshatra, transit_pada)

2. FOR mandali_num IN 1..12:
       IF transit_absolute_pada IN mandali_grid[mandali_num]["padas"]:
           RETURN mandali_num

3. RAISE Error("Transit pada not found in any mandali — grid corruption")
```

### 6.4 Preservation of Original Values (Governance Rule #7)

```
OUTPUT for each transit planet:
{
  "planet": "Saturn",
  "original": {
    "rasi": "Meena",
    "nakshatra": "Uttara Bhadrapada",
    "pada": 3
  },
  "mandali": {
    "number": 3,
    "name": "Mithuna Mandali",
    "center_nakshatra": "Mrigashira",
    "center_pada": 2
  },
  "house_from_moon_classical": 3,      # From Canonical JSON
  "house_from_moon_mandali": 3,        # Mandali number = Mandali-house
  "interpretation_ref": "canonical_page_85_saturn_3rd"
}
```

**Invariant**: `original.rasi`, `original.nakshatra`, `original.pada` are **never modified**.

---

## 7. Lifetime Sade Sati — Bidirectional Projection (Decisions #8, #9)

### 7.1 Saturn Cycle Deterministic Rules

```
SATURN_CYCLE_RULES:
- Saturn transits each Rasi for ~2.5 years (30 months)
- Full zodiac cycle = 12 × 2.5 = 30 years
- Sade Sati = Saturn in (Moon Rasi - 1, Moon Rasi, Moon Rasi + 1)
- In Mandali: Sade Sati = Saturn in Mandali {12, 1, 2}
- Elinati Shani = Saturn in Mandali 8 (8th from Moon Mandali)
- Ashtama Shani = Saturn in Mandali 8 (classical 8th house = Mandali 8)
```

### 7.2 Cycle Projection Algorithm

```
ALGORITHM: project_saturn_lifetime_cycles(natal_moon_rasi, current_date, canonical_transit)
────────────────────────────────────────────────────────────────────────────────────────
INPUT:  natal_moon_rasi (str), current_date (date), canonical_transit (Saturn entry)
OUTPUT: lifetime_cycles = { past: [], current: {}, future: [] }

1. PARSE canonical_transit for Saturn:
   - current_rasi = transit["rasi"]
   - current_start = parse_date(transit["start_date"])
   - current_end   = parse_date(transit["end_date"])

2. DETERMINE Saturn's position relative to Moon Rasi:
   moon_rasi_index = RASI_SEQUENCE.index(natal_moon_rasi)  # 0-11
   saturn_rasi_index = RASI_SEQUENCE.index(current_rasi)
   offset = (saturn_rasi_index - moon_rasi_index) % 12
   # offset 0=Moon Rasi, 1=2nd, 11=12th, etc.

3. BUILD complete 30-year cycle from current transit:
   cycle = []
   rasi = current_rasi
   date = current_start
   FOR i IN 0..11:
       cycle.append({ "rasi": rasi, "start": date, "end": add_months(date, 30) })
       rasi = next_rasi(rasi)
       date = add_months(date, 30)

4. EXTEND backward (past cycles) and forward (future cycles):
   - Each cycle = 30 years
   - Birth year determines which cycle native was born into

5. CLASSIFY each Sade Sati window (3 consecutive Rasis: offset 11, 0, 1):
   FOR each window in cycle:
       IF window overlaps birth_date:
           birth_position = "INSIDE"
       ELIF window.end < birth_date:
           birth_position = "BEFORE"
       ELSE:
           birth_position = "AFTER"

6. RETURN structured lifetime_cycles with birth_position for each
```

### 7.3 Birth Position Detection (Decision #9)

```
BIRTH POSITION LOGIC:
────────────────────
Given: birth_date, sade_sati_windows[] (each with start, end, cycle_num)

FOR each window IN sade_sati_windows:
    IF birth_date >= window.start AND birth_date <= window.end:
        RETURN "BIRTH_INSIDE_SADE_SATI"
    ELIF birth_date < window.start:
        IF previous_window exists:
            RETURN "BIRTH_BEFORE_SADE_SATI"  # Next is first
        ELSE:
            RETURN "BIRTH_BEFORE_FIRST_SADE_SATI"
    # Continue loop

# If loop completes, birth is after last known window
RETURN "BIRTH_AFTER_SADE_SATI"
```

### 7.4 Lifetime Timeline Output Structure

```json
{
  "sade_sati": {
    "cycles": [
      {
        "cycle_number": 1,
        "period": "1965-1995",
        "sade_sati_windows": [
          { "phase": "Rising", "rasi": "Dhanus", "start": "1965-01", "end": "1967-07", "birth_position": "BEFORE" },
          { "phase": "Peak", "rasi": "Makara", "start": "1967-07", "end": "1970-01", "birth_position": "BEFORE" },
          { "phase": "Setting", "rasi": "Kumbha", "start": "1970-01", "end": "1972-07", "birth_position": "BEFORE" }
        ]
      },
      {
        "cycle_number": 2,
        "period": "1995-2025",
        "sade_sati_windows": [
          { "phase": "Rising", "rasi": "Dhanus", "start": "1995-01", "end": "1997-07", "birth_position": "BEFORE" },
          { "phase": "Peak", "rasi": "Makara", "start": "1997-07", "end": "2000-01", "birth_position": "INSIDE" },
          { "phase": "Setting", "rasi": "Kumbha", "start": "2000-01", "end": "2002-07", "birth_position": "AFTER" }
        ]
      },
      {
        "cycle_number": 3,
        "period": "2025-2055",
        "sade_sati_windows": [
          { "phase": "Rising", "rasi": "Dhanus", "start": "2025-03", "end": "2027-09", "birth_position": "AFTER" },
          { "phase": "Peak", "rasi": "Makara", "start": "2027-09", "end": "2030-03", "birth_position": "AFTER" },
          { "phase": "Setting", "rasi": "Kumbha", "start": "2030-03", "end": "2032-09", "birth_position": "AFTER" }
        ]
      }
    ],
    "birth_detection": {
      "position": "INSIDE",
      "cycle": 2,
      "phase": "Peak",
      "details": "Born during Saturn in Makara (Moon Rasi) — Peak Sade Sati"
    }
  },
  "elinati_shani": { ... similar structure for Mandali 8 ... },
  "ashtama_shani": { ... similar structure for Mandali 8 ... }
}
```

---

## 8. Universal Mandali Engine — Responsibility Contract

### 8.1 Inputs (Read-Only from Canonical JSON)

| Input | Source | Format |
|-------|--------|--------|
| Natal Moon Rasi | Canonical JSON natal section | String (e.g., "Makara") |
| Natal Moon Nakshatra | Canonical JSON natal section | String (e.g., "Dhanishta") |
| Natal Moon Pada | Canonical JSON natal section | Integer 1-4 |
| Current Transit Planets | Canonical JSON transit section | Array of {planet, rasi, nakshatra, pada, start_date, end_date, house_from_moon} |
| Birth Date | Canonical JSON natal section | DD.MM.YYYY |

### 8.2 Outputs (Produced by Engine)

| Output | Description | Consumer |
|--------|-------------|----------|
| `mandali_grid[1..12]` | Complete Moon-centred Mandali map | Internal / Debug |
| `transit_mandali[planet]` | Mandali number (1-12) for each transit planet | AnswerComposer |
| `sade_sati` | Lifetime cycles with birth detection | AnswerComposer |
| `elinati_shani` | Lifetime 8th Mandali cycles | AnswerComposer |
| `ashtama_shani` | Lifetime 8th Mandali cycles (classical) | AnswerComposer |
| `timeline` | Unified past/current/future consultation objects | AnswerComposer |
| `consultation_objects` | Structured objects for report rendering | AnswerComposer |

### 8.3 Engine Boundaries — What It Does NOT Do

| Prohibited | Reason |
|------------|--------|
| Compute planetary longitudes | Model A uses Canonical JSON Rasi/Nakshatra/Pada only |
| Call Swiss Ephemeris / pyswisseph | No astronomical dependency |
| Generate future transit predictions beyond Canonical JSON | Canonical JSON is the single source of truth |
| Modify original Rasi/Nakshatra/Pada | Preservation invariant (Governance #7) |
| Produce interpretation text | AnswerComposer consumes canonical text |
| Combine with Natal Promise / Dasha scores | Separate engines; AnswerComposer composes |

---

## 9. Data Flow — Model A Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW — MODEL A                                 │
└─────────────────────────────────────────────────────────────────────────────┘

CANONICAL JSON
     │
     │  Read: natal.moon.{rasi, nakshatra, pada}
     │       transit[].{planet, rasi, nakshatra, pada, start_date, end_date}
     │       natal.birth_date
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIVERSAL MANDALI ENGINE                                 │
│                                                                             │
│  1. BUILD MANDALI GRID                                                      │
│     natal_moon_pada → absolute_pada (1-108)                                │
│     FOR mandali 1..12: center = moon_pada + (n-1)*9 (mod 108)              │
│     Each mandali = 9 padas (center ±4)                                     │
│                                                                             │
│  2. RESOLVE TRANSIT MANDALI                                                 │
│     FOR each transit planet:                                               │
│       transit_pada → absolute_pada                                         │
│       FIND mandali containing transit_pada → mandali_number                │
│       PRESERVE original {rasi, nakshatra, pada}                            │
│                                                                             │
│  3. DETECT CYCLES                                                           │
│     Saturn: map mandali_number → Sade Sati (12,1,2), Elinati (8)           │
│     Other planets: map per governance rules                                │
│                                                                             │
│  4. PROJECT LIFETIME TIMELINE                                               │
│     FROM canonical Saturn start/end dates                                  │
│     Project 30-year cycles backward/forward                                │
│     Classify each window relative to birth_date                            │
│                                                                             │
│  5. BIRTH POSITION DETECTION                                                │
│     For each major cycle (Sade Sati, Elinati, Ashtama):                    │
│       Determine: BEFORE / INSIDE / AFTER                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
     │
     │ Output: Structured consultation objects
     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ANSWER COMPOSER                                     │
│                                                                             │
│  • Receives: Mandali advisory objects + Canonical interpretation text      │
│  • Composes: Final report with Mandali advisory block                      │
│  • Renders: PDF / PWA / Web                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Responsibility Diagram — Engine Isolation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENGINE RESPONSIBILITY MATRIX                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┬──────────────┬──────────────┬──────────────┬────────────────┐
│     CAPABILITY      │ PlanetStrength│ HouseStrength│   Dasha      │ Universal      │
│                     │   Engine      │   Engine     │   Engine     │ Gochara Mandali│
│                     │               │              │              │   Engine (A)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Planetary Longitude │   Computes   │   Consumes   │   Consumes   │  NEVER         │
│                     │   (Shadbala)  │              │              │                │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Rasi / Nakshatra /  │   Computes   │   Consumes   │   Consumes   │  CONSUMES      │
│ Pada (Natal)        │              │              │              │  (Canonical)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Transit Positions   │   N/A        │   N/A        │   N/A        │  CONSUMES      │
│ (Current)           │              │              │              │  (Canonical)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Mandali Grid        │   N/A        │   N/A        │   N/A        │  BUILDS        │
│ Construction        │              │              │              │  (Core Duty)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Transit → Mandali   │   N/A        │   N/A        │   N/A        │  RESOLVES      │
│ Mapping             │              │              │              │  (Core Duty)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Sade Sati / Elinati │   N/A        │   N/A        │   N/A        │  PROJECTS      │
│ Lifetime Cycles     │              │              │              │  (Core Duty)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Birth Position      │   N/A        │   N/A        │   N/A        │  DETECTS       │
│ Detection           │              │              │              │  (Core Duty)   │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Interpretation Text │   N/A        │   N/A        │   N/A        │  NEVER         │
│ Generation          │              │              │              │                │
├─────────────────────┼──────────────┼──────────────┼──────────────┼────────────────┤
│ Score/Probability   │   Produces   │   Produces   │   Produces   │  PRODUCES      │
│ Output              │   Strength   │   Strength   │   Timing     │  Mandali       │
│                     │   Scores     │   Scores     │   Multipliers│  Activation    │
└─────────────────────┴──────────────┴──────────────┴──────────────┴────────────────┘

ALL ENGINES: Stateless, Deterministic, Pure Functions
INTEGRATION: PipelineRunner → AnswerComposer (NO cross-engine math)
```

---

## 11. Output Contract — Consultation Objects

### 11.1 Mandali Advisory Block (for AnswerComposer)

```json
{
  "mandali_advisory": {
    "reference_moon": {
      "rasi": "Makara",
      "nakshatra": "Dhanishta",
      "pada": 2,
      "mandali_1_center": "Dhanishta Pada 2"
    },
    "current_transit_mandali": {
      "Saturn": {
        "mandali_number": 3,
        "mandali_name": "Mithuna Mandali",
        "original_rasi": "Meena",
        "original_nakshatra": "Uttara Bhadrapada",
        "original_pada": 3,
        "classical_house_from_moon": 3,
        "mandali_house_from_moon": 3,
        "status": "FAVORABLE",
        "interpretation_key": "saturn_3rd_mandali_upachaya"
      },
      "Jupiter": { ... },
      "Rahu": { ... }
    },
    "sade_sati": {
      "current_cycle": 3,
      "current_phase": "Rising",
      "current_window": {
        "phase": "Rising",
        "rasi": "Dhanus",
        "mandali": 12,
        "start": "2025-03-30",
        "end": "2027-09-15",
        "months_remaining": 30
      },
      "birth_detection": {
        "position": "INSIDE",
        "cycle": 2,
        "phase_at_birth": "Peak",
        "description": "Born during Saturn in Makara (Moon Rasi) — Peak Sade Sati"
      },
      "lifetime_summary": {
        "total_cycles": 3,
        "completed": 2,
        "current": 3,
        "remaining_in_current": "Rising → Peak → Setting"
      }
    },
    "elinati_shani": { ... },
    "ashtama_shani": { ... },
    "timeline": [
      { "period": "1995-2025", "cycle": 2, "events": ["Sade Sati Peak (1997-2000)", "Elinati Shani (2005-2007)"] },
      { "period": "2025-2055", "cycle": 3, "events": ["Sade Sati Rising (2025-2027)", "Sade Sati Peak (2027-2030)"] }
    ]
  }
}
```

### 11.2 Integration Point

```
PipelineRunner.execute()
    │
    ├─▶ PlanetStrengthEngine.evaluate() → planet_strengths
    ├─▶ HouseStrengthEngine.evaluate() → house_strengths
    ├─▶ DashaEngine.evaluate() → dasha_results
    ├─▶ UniversalMandaliEngine.evaluate() → mandali_advisory  ◀ NEW
    │
    ▼
AnswerComposer.compose(
    planet_strengths,
    house_strengths, 
    dasha_results,
    mandali_advisory,           ◀ NEW PARAMETER
    canonical_text_refs
)
```

---

## 12. Implementation Responsibilities — Model A

| Component | File | Responsibility | Status |
|-----------|------|----------------|--------|
| `UniversalMandaliEngine` | `backend/app/engines/universal_mandali_engine.py` | Core Model A engine | 📋 **New** |
| `MandaliGridBuilder` | `backend/app/engines/mandali_grid_builder.py` | Static grid construction | 📋 **New** (extract from MandaliGenerator) |
| `TransitMandaliResolver` | `backend/app/engines/transit_mandali_resolver.py` | Transit → Mandali mapping | 📋 **New** |
| `LifetimeCycleProjector` | `backend/app/engines/lifetime_cycle_projector.py` | Sade Sati/Elinati/Ashtama projection | 📋 **New** |
| `BirthPositionDetector` | `backend/app/engines/birth_position_detector.py` | Birth cycle classification | 📋 **New** |
| `CanonicalJSONLoader` | `backend/app/core/canonical_json_loader.py` | Load/parse Canonical JSON transit section | 📋 **New** |
| `MandaliGenerator` | `backend/app/engines/mandali_generator.py` | **DEPRECATE** — longitude-based | ❌ **Remove** |
| `TransitEngine` | `backend/app/engines/transit_engine.py` | **REFACTOR** — consume MandaliEngine output | 🔄 **Revise** |
| `PipelineRunner` | `backend/app/pipeline_runner.py` | Wire UniversalMandaliEngine | 🔄 **Revise** |
| `AnswerComposer` | `backend/app/reports/consultation_summary_generator.py` | Accept mandali_advisory block | 🔄 **Revise** |

---

## 13. Lifetime Timeline — Visual Specification

```
LIFETIME SADE SATI TIMELINE (Example: Moon in Makara)
════════════════════════════════════════════════════════════════════════════════

CYCLE 1 (1965-1995)          CYCLE 2 (1995-2025)          CYCLE 3 (2025-2055)
─────────────────────        ─────────────────────        ─────────────────────
                             ┌─────────────────────┐
                             │      BIRTH          │◀── Native born 1998
                             │  (Inside Peak)      │
        ┌─────────────┐      │  ┌─────────────┐    │      ┌─────────────┐
        │  Rising     │      │  │   PEAK      │    │      │  Rising     │
        │  Dhanus     │      │  │  Makara     │    │      │  Dhanus     │
        │  1965-1967  │      │  │  1997-2000  │    │      │  2025-2027  │
        └─────────────┘      │  └─────────────┘    │      └─────────────┘
        ┌─────────────┐      │  ┌─────────────┐    │      ┌─────────────┐
        │   PEAK      │      │  │  Setting    │    │      │   PEAK      │
        │  Makara     │      │  │  Kumbha     │    │      │  Makara     │
        │  1967-1970  │      │  │  2000-2002  │    │      │  2027-2030  │
        └─────────────┘      │  └─────────────┘    │      └─────────────┘
        ┌─────────────┐      │                     │      ┌─────────────┐
        │  Setting    │      │                     │      │  Setting    │
        │  Kumbha     │      │                     │      │  Kumbha     │
        │  1970-1972  │      │                     │      │  2030-2032  │
        └─────────────┘      │                     │      └─────────────┘
                             │                     │
                             ▼                     ▼
                        BIRTH POSITION:         FUTURE PROJECTION:
                        INSIDE (Peak)           Cycle 3 — All AFTER birth

ELINATI SHANI (Mandali 8) — Same 30-year cycle, offset by 7 Mandalis
ASHTAMA SHANI (Mandali 8) — Classical 8th house = Mandali 8
```

---

## 14. Birth Detection — Decision Tree

```
                    ┌─────────────────────┐
                    │  For Each Major     │
                    │  Cycle Window       │
                    │  (Sade Sati,        │
                    │   Elinati, Ashtama) │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ birth_date >=       │
                    │ window.start AND    │
                    │ birth_date <=       │
                    │ window.end          │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
         ┌─────────┐    ┌─────────────┐  ┌─────────────┐
         │  YES    │    │    NO       │  │    NO       │
         │         │    │ birth_date  │  │ birth_date  │
         │         │    │ < window.   │  │ > window.   │
         │         │    │ start       │  │ end         │
         └────┬────┘    └──────┬──────┘  └──────┬──────┘
              │                │                │
              ▼                ▼                ▼
      ┌───────────────┐ ┌─────────────┐ ┌─────────────────┐
      │ BIRTH_INSIDE  │ │ Check prev  │ │ Continue to     │
      │ _CYCLE        │ │ window:     │ │ next window     │
      │               │ │ if exists → │ │                 │
      │ Record:       │ │ BIRTH_BEFORE│ │ If last window  │
      │ - cycle_num   │ │ _THIS_CYCLE │ │ → BIRTH_AFTER   │
      │ - phase       │ │ else →      │ │ _ALL_CYCLES     │
      │ - description │ │ BIRTH_BEFORE│ │                 │
      └───────────────┘ │ _FIRST_CYCLE│ └─────────────────┘
                        └─────────────┘
```

---

## 15. Worked Example — Raju Chart (Canonical JSON Pages 85-86)

### Input (from Canonical JSON)
```
Natal Moon: Makara Rasi, Dhanishta Nakshatra, Pada 2
Birth Date: (from natal section)

Current Transits:
- Saturn: Meena Rasi, Uttara Bhadrapada Nakshatra, Pada 3 (30/03/2025 - 03/06/2027)
- Jupiter: Mithuna Rasi, Mrigashira Nakshatra, Pada 2 (05/12/2025 - 02/06/2026)
- Rahu: Kumbha Rasi, Shatabhisha Nakshatra, Pada 1 (18/05/2025 - 05/12/2026)
```

### Step 1: Moon Absolute Pada
- Dhanishta = Nakshatra #23 (0-indexed: 22)
- Pada 2 → Absolute = 22×4 + 2 = **90**

### Step 2: Mandali Grid (Mandali 1 centered on Pada 90)
| Mandali | Center Pada | Center Nakshatra | Center Pada# | Rasi Name | 9 Padas |
|---------|-------------|------------------|--------------|-----------|---------|
| 1 | 90 | Dhanishta | 2 | Makara | 86-94 |
| 2 | 99 | Shatabhisha | 3 | Kumbha | 95-103 |
| 3 | 108→1 | Purva Bhadrapada | 1 | Meena | 104-108,1-4 |
| 4 | 10 | Uttara Bhadrapada | 2 | Meena | 5-13 |
| 5 | 19 | Revati | 3 | Meena | 14-22 |
| 6 | 28 | Ashwini | 4 | Mesha | 23-31 |
| 7 | 37 | Bharani | 1 | Mesha | 32-40 |
| 8 | 46 | Krittika | 2 | Vrishabha | 41-49 |
| 9 | 55 | Rohini | 3 | Vrishabha | 50-58 |
| 10 | 64 | Mrigashira | 4 | Mithuna | 59-67 |
| 11 | 73 | Ardra | 1 | Mithuna | 68-76 |
| 12 | 82 | Punarvasu | 2 | Karkata | 77-85 |

### Step 3: Transit Resolution
- **Saturn**: Uttara Bhadrapada Pada 2 → Absolute Pada 10 → **Mandali 4**
- **Jupiter**: Mrigashira Pada 4 → Absolute Pada 64 → **Mandali 10**
- **Rahu**: Shatabhisha Pada 1 → Absolute Pada 95 → **Mandali 2**

### Step 4: Sade Sati Detection
- Sade Sati = Mandali {12, 1, 2}
- Saturn in Mandali 4 → **NOT in Sade Sati**
- Rahu in Mandali 2 → **Rahu in Sade Sati zone** (but Rahu not Saturn)

### Step 5: Lifetime Projection (Saturn)
- Current: Saturn in Meena (Mandali 4) 2025-2027
- Cycle 3 (2025-2055): Rising=Dhanus(12) 2025-27, Peak=Makara(1) 2027-30, Setting=Kumbha(2) 2030-32
- Birth detection: Compare birth_date to Cycle 2 windows (1995-2025)

---

## 16. Summary of Changes from Version 1

| Aspect | Version 1 (Previous) | Version 2 (This Report) |
|--------|---------------------|------------------------|
| **Data Source** | Ephemeris → Longitude → Mandali | Canonical JSON (Rasi/Nakshatra/Pada) → Mandali |
| **Engine Type** | Astronomical + Spatial | Pure Spatial Transformation |
| **Longitude** | Required | **Never used** |
| **Swiss Ephemeris** | Required dependency | **Prohibited** |
| **Future Transits** | Computed from ephemeris | Projected from Canonical JSON dates via deterministic rules |
| **Sade Sati** | Current snapshot only | **Lifetime bidirectional projection** |
| **Birth Detection** | Not specified | **Explicit algorithm for BEFORE/INSIDE/AFTER** |
| **MandaliGenerator** | Longitude-based (deprecated) | **Replaced by MandaliGridBuilder (Pada-based)** |
| **TransitEngine** | Computes activation scores | **Consumes UniversalMandaliEngine output** |
| **Governance** | Single document | **Single document upgraded (Option A)** |
| **Model B** | Implicit future | **Explicit appendix only — no implementation** |

---

## 17. Approval Request

This **Architecture Revision Report v2** defines the final approved architecture for **Model A** Universal Gochara Mandali Engine.

**Please review and approve** before expanding into the complete `GOCHARA_MANDALI_GOVERNANCE_v1.md` governance document.

### Checklist for Approval
- [ ] Model A data flow (Canonical JSON only) confirmed
- [ ] No ephemeris/longitude dependencies in Model A
- [ ] Lifetime Sade Sati projection algorithm accepted
- [ ] Birth position detection logic accepted
- [ ] Engine responsibility isolation matrix accepted
- [ ] Output contract (mandali_advisory) accepted
- [ ] Implementation responsibility assignments accepted
- [ ] Model B documented as appendix-only confirmed

---

*End of Architecture Revision Report v2*