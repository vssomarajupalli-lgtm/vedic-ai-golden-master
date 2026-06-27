# Phase 15F.8 + 15G.4 – Dasha Date & Yoga Trace Audit

## PART A – DASHA DATE HYDRATION AUDIT

### A1. Timeline Structure Audit
**Exact Timeline Object Structure:**
The raw data loader produces a `timeline` array of objects mapping chronological periods:
```json
[
  {
    "start_date": "2000-01-01",
    "mahadasha": "Shani",
    "antardasha": "Guru",
    "pratyantardasha": "Kuja"
  }
]
```

**Missing Date Fields:**
The `end_date` is structurally missing from the objects. The current engine logic infers the end date by looking at `timeline[i+1]['start_date']`. 

**Data Loss / Gap:**
The timeline array is **dropped** during the execution of `PipelineRunner`. The `ChartProcessResponse` wraps `engine_outputs`, but the `timeline` is never attached to `engine_outputs.dashas`. Therefore, the frontend has zero access to the timeline.

### A2. Active Period Audit (Raju Chart)
For the Raju Chart (`CASE_001_RAJU.json` canonical data):
* **Active MD:** Saturn
* **Active AD:** Jupiter
* **Active PD:** Venus
* **Start Date / End Date:** **LOST IN PIPELINE.** Cannot be retrieved from the API response payload.

### A3. Data Availability Matrix

| Field | Exists | JSON Path | Backend Change Needed |
|---------|---------|---------|---------|
| MD Lord | YES | `breakdown.engine_outputs.dashas.synthesis.active_md` | NO |
| MD Start Date | NO | N/A | YES |
| MD End Date | NO | N/A | YES |
| AD Lord | YES | `breakdown.engine_outputs.dashas.synthesis.active_ad` | NO |
| AD Start Date | NO | N/A | YES |
| AD End Date | NO | N/A | YES |
| PD Lord | YES | `breakdown.engine_outputs.dashas.synthesis.active_pd` | NO |
| PD Start Date | NO | N/A | YES |
| PD End Date | NO | N/A | YES |

### A4. Question Engine Impact
**Final Display Format Feasibility:**
To display the requested format (Lord + Start Date + End Date + Activation Index), significant **Backend Hydration and Schema Changes** are required. A frontend-only change is impossible because the dates are pruned by the `PipelineRunner` before the payload reaches the API response.

### A5. Timing Window Audit
* **What timeline data already exists?** The `normalized_payload` contains the `timeline` array during the pipeline run, but it doesn't survive to the API.
* **Can the future favorable period be calculated?** Not currently. `FormulaEvaluator` lacks an algorithm to scan future dashas.
* **What backend data is available today?** Only the currently active lords and their immediate synthesis strengths. 

---

## PART B – YOGA EVALUATION TRACE AUDIT

### B1. Yoga Inventory
The following yogas are currently implemented as hidden boolean stubs in `YogaEngine.py`:
* **Universal:** Gaja Kesari Yoga, Neecha Bhanga Raja Yoga, Adhi Yoga
* **Pancha Mahapurusha:** Ruchaka Yoga, Bhadra Yoga, Hamsa Yoga, Malavya Yoga, Sasa Yoga
* **Wealth:** Dhana Yoga, Lakshmi Yoga, Vasumathi Yoga
* **Career:** Raja Yoga, Dharma Karma Adhipati Yoga, Amala Yoga
* **Education:** Saraswati Yoga, Vidya Yoga
* **Marriage:** Kalatra Yoga, Saubhagya Yoga
* **Children:** Putra Yoga, Santana Yoga
* **Spiritual:** Moksha Yoga, Sanyasa Yoga, Parivraja Yoga

### B2. Current Output Structure
**Exact JSON Path:**
* `breakdown.engine_outputs.yogas.universal_yogas`
* `breakdown.engine_outputs.yogas.house_1_yogas` (up to `house_12_yogas`)

**Format:**
Arrays containing string literals of successfully passed yogas (e.g., `["Gaja Kesari Yoga"]`). There is no `failed_yogas` array.

### B3. Rule Visibility Audit

| Yoga | Rule Trace Exists | Failure Reason Exists | Ready for UI |
|--------|--------|--------|--------|
| All Yogas | NO | NO | NO |

* `YogaEngine` uses silent Python boolean checks (e.g., `_detect_hamsa_yoga`). It stores absolutely no intermediate calculations or failure reasons.

### B4. Verification Console Readiness
**Can the Formula Verification Console display rule breakdowns and failure reasons without backend changes?**
**EXACT ANSWER: NO.** The UI cannot display rules or pass/fail reasons because the backend mathematically deletes that context, returning only the names of successful yogas.

### B5. Future Target Layout
To support a trace layout (e.g., "Mercury in Kendra [✗] -> RESULT: FAILED"), the `YogaEngine` must be entirely refactored. It must shift from boolean returning methods to returning a dictionary for each yoga containing:
* `rules`: Array of rule evaluations with true/false states.
* `final_status`: "PASSED" or "FAILED".
* `failure_reason`: Human-readable text of the exact rule that caused the failure.

---

## PART C – REMAINING TRANSPARENCY GAPS

**1. Hidden Calculations still existing in the backend:**
* **Dasha Timelines:** Discarded by `PipelineRunner`.
* **Yoga Rules:** Swallowed by silent boolean returns in `YogaEngine`.
* **Varga Modifiers:** `VargaEngine` updates scores but leaves its `breakdown` tracking object empty `{}`.
* **Calibration Constants:** Weights are locked in Python files (`astrology_constants.py`) and never exposed to the API.

**2. Status Matrix:**

| Section | Status |
|----------|---------|
| Domain Formula Trace | COMPLETE |
| Planet Breakdown | COMPLETE |
| House Breakdown | COMPLETE |
| Dasha Breakdown (Lords/Strength) | COMPLETE |
| Engine Snapshot | COMPLETE |
| Signal Trace | PARTIAL (UI built; awaits backend schema update) |
| Dasha Dates | MISSING |
| Yoga Trace | MISSING |
| Varga Trace | MISSING |
| Calibration Console | MISSING |

### Recommended Implementation Order
1. **Schema Hydration:** Expose `isolated_signals` in `/ask-structured-question` to finish the Signal Trace UI.
2. **Dasha Timeline Rescue:** Modify `PipelineRunner` and `DashaEngine` to inject the active start/end dates into `engine_outputs.dashas.synthesis`.
3. **YogaEngine Refactor:** Rebuild Yoga detection to emit rule objects rather than strings.
4. **Varga Breakdown Tracking:** Populate the `{}` breakdown in `VargaEngine`.
5. **Calibration API:** Create an endpoint to serve `astrology_constants.py`.
