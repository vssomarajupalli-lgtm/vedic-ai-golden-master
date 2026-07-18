---
archive_title: "PHASE 16.0 – ASTROLOGY INTELLIGENCE CONSOLE MASTER BLUEPRINT"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE 16.0 – ASTROLOGY INTELLIGENCE CONSOLE MASTER BLUEPRINT

## PURPOSE
The Astrology Intelligence Console is the definitive, unified visibility interface of the Vedic-AI System. It acts as the primary validation, calibration, and diagnostic suite.

It provides complete transparency into the mathematical processing of the engine stack without requiring raw JSON inspection, log reading, or manual Python traces. It will serve End Users (for deep insights), Astrologers (for chart validation), QA (for correctness), and Architects (for future engine tuning).

---

## 1. PAGE HIERARCHY & NAVIGATION STRUCTURE

The Console will utilize a structured dashboard architecture with a persistent side-navigation or top-level tab structure, ensuring scalability.

* **Top Level Identity Bar:** Persistent display of Section A (Horoscope Identity Center) across all views.
* **Core Tabs / Navigation Sidebar:**
  * **Natal Foundations:** Rasi (B), Planets (C), Bhava (D)
  * **Advanced Synthesis:** Natal Promise (E), Varga (H), Yoga (G)
  * **Temporal Dynamics:** Dasha (F), Mandali (I), Gochara (J)
  * **Question & Evaluation:** Question Engine (K)
  * **System Operations:** Formula Verification (L), Calibration Center (M)

---

## 2. COMPONENT BLUEPRINTS & DATA SOURCE MAPPING

### SECTION A: HOROSCOPE IDENTITY CENTER
* **Display:** Name, DOB, TOB, POB, Lagna, Moon Sign, Nakshatra, Pada, Current Dasha, Current Mandali, Current Gochara Status.
* **Behavior:** Persistent header banner.
* **Data Source:** `metadata` object in the unified pipeline output + derived temporal states.
* **JSON Path:** `metadata.name`, `metadata.date_of_birth`, etc.

### SECTION B: RASI INTELLIGENCE CENTER
* **Display:** D1 planetary positions, Sign placements, House placements, Sign lords, Rasi strength summary.
* **Behavior:** Visual chart or summary grid. Expandable rows for deep planetary drill-down.
* **Data Source:** `Normalized Payload` + `PlanetEngine`.
* **JSON Path:** `normalized_payload.planets`, `engine_outputs.planets`.

### SECTION C: PLANET INTELLIGENCE MATRIX
* **Display:** Score, Grade, Sign, House, Dignity, Functional nature, Shadbala, BAV contribution.
* **Behavior:** Data grid/table with expandable rows revealing the exact `"breakdown"` dictionary (dignity, house_placement, aspects, conjunctions, combustion, retrogression, shadbala, varga_dignity).
* **Data Source:** `PlanetEngine`.
* **JSON Path:** `engine_outputs.planets.<planet_name>.breakdown`.

### SECTION D: BHAVA INTELLIGENCE MATRIX
* **Display:** House score, Grade, House lord, SAV contribution, Occupants, Benefic aspects, Malefic aspects, House yogas.
* **Behavior:** Data grid/table with 12 rows. Expandable to show `"breakdown"`.
* **Data Source:** `HouseEngine`.
* **JSON Path:** `engine_outputs.houses.<house_number>.breakdown`.

### SECTION E: NATAL PROMISE INTELLIGENCE
* **Display:** Marriage, Career, Wealth, Education, Property, Children, Health, Spirituality.
* **Behavior:** Accordion or grid. For each domain, show the calculation pillars: Bhava, Lord, Karaka, Varga, and Final Score.
* **Data Source:** `NatalPromiseEngine`.
* **JSON Path:** `engine_outputs.natal_promise.<domain_name>.breakdown`.

### SECTION F: DASHA INTELLIGENCE CENTER
* **Display:** Current MD, AD, PD. Include start/end dates, strength scores, and overall activation index.
* **Behavior:** Timeline visualization with a scrubber to view future states.
* **Data Source:** `DashaEngine`.
* **JSON Path:** `engine_outputs.dashas.synthesis`, `engine_outputs.dashas.timeline`.

### SECTION G: YOGA INTELLIGENCE CENTER
* **Display:** Active yogas, Failed yogas, Evaluation reasons.
* **Behavior:** Split view (Active vs. Failed). Expandable items showing the exact rule checks, trigger conditions, and pass/fail status per rule.
* **Data Source:** `YogaEngine`.
* **JSON Path:** `engine_outputs.yogas.active_yogas`, `engine_outputs.yogas.failed_yogas`.

### SECTION H: VARGA INTELLIGENCE CENTER
* **Display:** D9 (Marriage, Dharma, Spiritual), D10 (Career, Authority, Growth). Future-ready slots for D20, D60.
* **Behavior:** Tabbed view by divisional chart.
* **Data Source:** `VargaEngine`.
* **JSON Path:** `engine_outputs.vargas.D9`, `engine_outputs.vargas.D10`.

### SECTION I: MANDALI INTELLIGENCE CENTER
* **Display:** Natal Moon Pada, Mandali center, Mandali sector activations, Benefic zones, Sensitive zones.
* **Behavior:** Visual concentric rendering (Moon-centered) and exact interpretation model logic trace.
* **Data Source:** `MandaliEngine` (Future Implementation).
* **JSON Path:** `engine_outputs.mandali`.

### SECTION J: GOCHARA INTELLIGENCE CENTER
* **Display:** Current transit positions, Mandali impact, Activation scores, Triggered houses, Triggered planets.
* **Behavior:** Dual-chart view (Natal vs Transit). Color-coded favorable/unfavorable impact grids.
* **Data Source:** `GocharaEngine` (Future Implementation).
* **JSON Path:** `engine_outputs.gochara`.

### SECTION K: QUESTION ENGINE INTELLIGENCE
* **Display:** Structured question result, Supporting factors, Attention factors, Dasha activation, Formula evaluation trace, Isolated signals.
* **Behavior:** Interactive formula tracing. Select a domain/question, view the signal evaluations dynamically.
* **Data Source:** `FormulaEvaluator`, `/ask-structured-question` endpoint.
* **JSON Path:** `StructuredQuestionResponse.results`, `isolated_signals`.

### SECTION L: FORMULA VERIFICATION CONSOLE
* **Display:** Complete calculation trace (Planet, House, Dasha, Yoga, Varga, Natal Promise, Question).
* **Behavior:** Deep diagnostic JSON tree viewer or step-by-step pipeline execution graph. Shows Inputs -> Intermediate Calculations -> Final Outputs.
* **Data Source:** `PipelineRunner`.
* **JSON Path:** Root `ChartProcessResponse.breakdown`.

### SECTION M: CALIBRATION CENTER
* **Display:** Configurable weights (Planet Engine: Dignity, House placement, Aspect, Shadbala, BAV; Natal Promise: Bhava, Lord, Karaka, Varga).
* **Behavior:** Form-based inputs. Allows QA to temporarily override backend constants and re-run the chart to validate the impact of weight tuning.
* **Data Source:** `app.core.constants` or future external DB configuration.

---

## 3. BACKEND DEPENDENCY MATRIX

| Console Section | Required Backend Engine | Current Status |
| :--- | :--- | :--- |
| Rasi Intelligence | `JsonNormalizer` / `PlanetEngine` | Ready |
| Planet Intelligence | `PlanetEngine` | Ready |
| Bhava Intelligence | `HouseEngine` | Ready |
| Natal Promise | `NatalPromiseEngine` | Ready |
| Dasha Intelligence | `DashaEngine` | Ready |
| Yoga Intelligence | `YogaEngine` | Ready |
| Varga Intelligence | `VargaEngine` | Ready |
| Mandali Intelligence | `MandaliEngine` | Pending Phase |
| Gochara Intelligence | `GocharaEngine` | Pending Phase |
| Question Engine | `FormulaEvaluator` | Ready |
| Verification Console | `PipelineRunner` | Ready |

---

## 4. FUTURE IMPLEMENTATION PHASES & RECOMMENDED ORDER

The Astrology Intelligence Console should be built modularly, parallel to backend readiness.

1. **Phase 16.1 - The Foundation:**
   * Build the master layout, routing, and persistent Identity Center (Section A).
   * Integrate Verification Console (Section L) to provide immediate JSON rendering, replacing terminal debugging.

2. **Phase 16.2 - Core Intelligence:**
   * Implement Planet (Section C), Bhava (Section D), and Rasi (Section B) matrices using existing stable endpoints.

3. **Phase 16.3 - Synthesis & Temporal:**
   * Implement Natal Promise (Section E), Varga (Section H), Yoga (Section G).
   * Implement Dasha (Section F) with timeline scrubber.

4. **Phase 16.4 - Question & Tuning:**
   * Implement Question Engine (Section K) providing the `isolated_signals` drill-down.
   * Implement Calibration Center (Section M) for live weight tuning.

5. **Phase 16.5 - Advanced Prediction Integration:**
   * Implement Mandali (Section I) and Gochara (Section J) **strictly AFTER** those respective backend engines are completed and merged into the PipelineRunner.
