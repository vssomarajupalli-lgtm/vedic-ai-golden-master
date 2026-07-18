---
archive_title: "Phase 15G.2 – Formula Verification Console Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.2 – Formula Verification Console Audit

## Objective
Design a completely transparent, internal-only diagnostics page to validate mathematical outputs from all astrology engines without needing server-side logging or terminal inspection.

---

## SECTION A: DOMAIN FORMULA TRACE
* **Audit Items:** Marriage, Career, Wealth, Education, Children, Property, Health, Spirituality.
* **Exact JSON Path:** `breakdown.engine_outputs.natal_promise.<domain>.breakdown`
* **Existing Backend Source:** `NatalPromiseEngine`
* **Available Immediately?:** Yes
* **Requires Hydration?:** No
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**
* **Notes:** The payload already contains exact integer scores for `bhava`, `bhavadhipati`, `karaka`, and `varga`, as well as `raw_score` and `score`.

---

## SECTION B: PLANET STRENGTH BREAKDOWN
* **Audit Items:** Final score, dignity, house placement, aspects, conjunctions, combustion, retrogression, shadbala, BAV.
* **Exact JSON Path:** `breakdown.engine_outputs.planets.<planet>.breakdown` (and `.bav_modifier`)
* **Existing Backend Source:** `PlanetStrengthEngine`
* **Available Immediately?:** Yes
* **Requires Hydration?:** No
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**
* **Notes:** The planet object correctly outputs the full component breakdown array.

---

## SECTION C: HOUSE STRENGTH BREAKDOWN
* **Audit Items:** Final score, SAV, occupants, benefic/malefic aspects, house type, yogas.
* **Exact JSON Path:** `breakdown.engine_outputs.houses.<house_number>.breakdown`
* **Existing Backend Source:** `HouseStrengthEngine`
* **Available Immediately?:** Yes
* **Requires Hydration?:** No
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**

---

## SECTION D: YOGA EVALUATION TRACE
* **Audit Items:** Evaluation rules, Pass/fail status, Failure reasons.
* **Exact JSON Path:** `breakdown.engine_outputs.yogas`
* **Existing Backend Source:** `YogaEngine`
* **Available Immediately?:** No (Only active yogas are passed back as an array of strings).
* **Requires Hydration?:** N/A
* **Requires Backend Modification?:** Yes
* **Requires Frontend-Only Implementation?:** No
* **Confidence Level:** 30%
* **Status:** **PARTIAL**
* **Notes:** The `YogaEngine` currently relies on hardcoded boolean stubs (e.g., `_detect_gaja_kesari_yoga`). It does not track rule-by-rule conditions, nor does it output why a specific yoga failed. The engine must be refactored to emit an evaluation dictionary rather than just an array of successful strings.

---

## SECTION E: DASHA FORMULA TRACE
* **Audit Items:** MD/AD/PD score source, Activation index.
* **Exact JSON Path:** `breakdown.engine_outputs.dashas.synthesis` and `breakdown.engine_outputs.dashas.<planet>.temporal_activation`
* **Existing Backend Source:** `DashaEngine`
* **Available Immediately?:** Yes
* **Requires Hydration?:** No
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**
* **Notes:** The synthesis block holds the aggregated scores. To explain the relationship multiplier (axis), the UI just needs to read the `temporal_activation` block of the respective active lord.

---

## SECTION F: VARGA VALIDATION TRACE
* **Audit Items:** D9, D10 scores and breakdown.
* **Exact JSON Path:** `breakdown.engine_outputs.vargas.D9.planets.<planet>`
* **Existing Backend Source:** `VargaEngine`
* **Available Immediately?:** Partial
* **Requires Hydration?:** No
* **Requires Backend Modification?:** Yes
* **Requires Frontend-Only Implementation?:** No
* **Confidence Level:** 50%
* **Status:** **PARTIAL**
* **Notes:** While `final_score` is outputted, the `breakdown` dictionary inside the Varga planetary objects is currently empty `{}`. The engine needs an upgrade to trace its internal calculations into the payload.

---

## SECTION G: SIGNAL TRACE CONSOLE
* **Audit Items:** Signal names, scores, metadata, breakdown.
* **Exact JSON Path:** `isolated_signals` (Returns full payload subset).
* **Existing Backend Source:** `FormulaEvaluator`
* **Available Immediately?:** Yes
* **Requires Hydration?:** Yes. It relies on `/ask-structured-question` returning the semantic translation.
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**

---

## SECTION H: WEIGHT CALIBRATION CONSOLE
* **Audit Items:** All scoring constants and weights.
* **Exact JSON Path:** N/A
* **Existing Backend Source:** `app.config.astrology_constants`
* **Available Immediately?:** No
* **Requires Hydration?:** N/A
* **Requires Backend Modification?:** Yes
* **Requires Frontend-Only Implementation?:** No
* **Confidence Level:** 10%
* **Status:** **MISSING**
* **Notes:** The weights (e.g., `PLANET_SCORING_MATRIX`, `HOUSE_SCORING_MATRIX`) are hardcoded in Python dictionaries. They are not exposed to the API. A new backend endpoint (`GET /calibration/weights`) is required to serve these to the frontend.

---

## SECTION I: ENGINE OUTPUT SNAPSHOT
* **Audit Items:** Collapsible JSON viewer for the entire pipeline.
* **Exact JSON Path:** `breakdown`
* **Existing Backend Source:** `PipelineRunner` (`ChartProcessResponse`)
* **Available Immediately?:** Yes
* **Requires Hydration?:** No
* **Requires Backend Modification?:** No
* **Requires Frontend-Only Implementation?:** Yes
* **Confidence Level:** 100%
* **Status:** **READY**

---

## DELIVERABLES SUMMARY

1. **Proposed UI Layout:** Multi-tabbed diagnostic interface mirroring the sections above.
2. **Data Availability Matrix:** 
   * Planets, Houses, Natal Promise, Dasha, Signals, JSON Viewer = **READY**
   * Yoga, Varga = **PARTIAL** (Require backend breakdowns)
   * Calibration = **MISSING** (Requires new endpoint)
3. **Hydration Requirements:** Only Section G requires secondary API polling (via QuestionEngine).
4. **Backend Gaps:** `YogaEngine` evaluation tracing, `VargaEngine` breakdowns, and a `Calibration` constants API.
5. **Frontend-Only Opportunities:** Sections A, B, C, E, and I can be built immediately as purely UI-driven features.
6. **Recommended Implementation Order:**
   * Step 1: Implement Section I (JSON Viewer) as a baseline.
   * Step 2: Implement Sections A, B, C (The core structural pillars).
   * Step 3: Implement Sections E, G (Dynamics and Evaluation).
   * Step 4: Refactor backend for Yoga/Varga (Sections D, F).
   * Step 5: Expose Python constants and build Calibration Console (Section H).
