---
archive_title: "Phase 15G.9: Remaining Transparency Gap Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.9: Remaining Transparency Gap Audit

## Executive Summary
This audit expands upon the findings of Phase 15G.8A to detail the exact subsystem footprints, required implementation effort, and prioritized ranking for the remaining transparency gaps inside the Vedic-AI Formula Verification Console.

All of the primary mathematical engines exist and compute properly in the backend. The primary bottleneck is Frontend Mapping.

---

## 1. Ranked Backlog

### HIGH PRIORITY

#### 1. Master Probability Synthesis Trace
- **Exact Subsystem Name:** Master Probability Engine
- **Engine Owner:** `MasterProbabilityEngine`
- **Exact JSON Path:** `master_probability`
- **Existing Backend Output:** Fully populated (`final_score`, `raw_score`, `breakdown`, `weights`, `live_factors`).
- **Why it is not visible today:** Skipped during Verification Console layout rendering.
- **Frontend Effort Required:** Medium (Requires a visual breakdown of the weighted percentages).
- **Backend Effort Required:** Zero.
- **Governance Risk:** Low.
- **Mathematical Importance:** **HIGH.** It is the final score aggregator deciding the output probability.
- **Status:** READY

#### 2. Ashtakavarga Trace
- **Exact Subsystem Name:** Ashtakavarga Engine
- **Engine Owner:** `AshtakavargaEngine`
- **Exact JSON Path:** `breakdown.engine_outputs.ashtakavarga`
- **Existing Backend Output:** Fully populated (`bav_charts`, `sav_chart`, `sav_analytics`, `engine_modifiers`).
- **Why it is not visible today:** Data structure is highly complex (2D matrices for 7 planets × 12 houses). Was deemed too complicated for initial transparency MVP.
- **Frontend Effort Required:** High (Requires complex CSS Grid matrix tables).
- **Backend Effort Required:** Zero.
- **Governance Risk:** Low.
- **Mathematical Importance:** **HIGH.** Directly manipulates Planet final_scores and House final_scores.
- **Status:** READY

#### 3. Rasi Strength Trace
- **Exact Subsystem Name:** Rasi Strength Engine
- **Engine Owner:** `RasiStrengthEngine`
- **Exact JSON Path:** `breakdown.engine_outputs.rasis`
- **Existing Backend Output:** Fully populated (12 objects containing `final_score`, `breakdown`, `modifiers`, `confidence_flags`).
- **Why it is not visible today:** UI skipped from Houses directly to Dashas.
- **Frontend Effort Required:** Medium (Can reuse House Trace component structure).
- **Backend Effort Required:** Zero.
- **Governance Risk:** Low.
- **Mathematical Importance:** **HIGH.** Contributes exactly 10% to the Master Probability.
- **Status:** READY

---

### MEDIUM PRIORITY

#### 4. Transit Trigger Trace
- **Exact Subsystem Name:** Transit Engine (Gochara)
- **Engine Owner:** `TransitEngine`
- **Exact JSON Path:** `breakdown.engine_outputs.transit`
- **Existing Backend Output:** Partial/Stub (`activation_score`, `activated_domains`, `breakdown`).
- **Why it is not visible today:** Heavily reliant on stub math; not yet a robust dynamic calculation.
- **Frontend Effort Required:** Medium.
- **Backend Effort Required:** Zero (Frontend can just display the stub output).
- **Governance Risk:** Low.
- **Mathematical Importance:** **MEDIUM.** Contributes 5% to Master Probability.
- **Status:** READY (as Stub)

---

### LOW PRIORITY

#### 5. Confidence Flag Trace
- **Exact Subsystem Name:** Global Confidence Flags
- **Engine Owner:** PipelineRunner / All Engines
- **Exact JSON Path:** Scattered (inside `planets`, `rasis`, `transit`, etc.)
- **Existing Backend Output:** Embedded as string arrays (e.g. `["D9_vargottama"]`).
- **Why it is not visible today:** They are currently visible inside individual nested drawers (e.g., inside Planet Venus drawer), but there is no global "Flags" summary.
- **Frontend Effort Required:** Low.
- **Backend Effort Required:** Medium (Requires `PipelineRunner` to aggregate all flags into a single master array).
- **Governance Risk:** Low.
- **Mathematical Importance:** **LOW.** Purely for explainability and human trust.
- **Status:** PARTIAL

#### 6. Probability Grade Trace
- **Exact Subsystem Name:** Calibration & Constants
- **Engine Owner:** Universal (`astrology_constants.py`)
- **Exact JSON Path:** None (Hardcoded in Python).
- **Existing Backend Output:** None (Strings like "EXCELLENT" are returned, but the boundary scale is hidden).
- **Why it is not visible today:** There is no backend REST endpoint to serve `astrology_constants.py` to the frontend.
- **Frontend Effort Required:** Medium (New Calibration Console UI).
- **Backend Effort Required:** Low (Create `/api/v1/calibration` FastAPI endpoint).
- **Governance Risk:** Low.
- **Mathematical Importance:** **LOW.** Visual labeling only.
- **Status:** MISSING

---

## 2. Recommended Implementation Order

To ensure rapid closure of transparency gaps with minimal architectural friction:

1. **Phase A: Master & Rasi Trace (Low Hanging Fruit)**
   - Expose `MasterProbabilityEngine` and `RasiStrengthEngine`. 
   - Both are 100% ready and only require frontend React components.
2. **Phase B: Ashtakavarga Matrix**
   - Implement the complex BAV/SAV tables.
3. **Phase C: Transit & Flags**
   - Expose the Transit stub. Implement a global flag aggregator in the backend pipeline.
4. **Phase D: Calibration API**
   - Create the `/api/v1/calibration` route and expose Probability Grade mapping and core weights.

---

## 3. Estimated Console Completeness After Each Phase

| Phase | Milestone | Estimated Completeness |
| :--- | :--- | :--- |
| **Current Baseline** | Phase 15G.8A | ~65% |
| **Phase A** | Master & Rasi Traces Added | ~80% |
| **Phase B** | Ashtakavarga Trace Added | ~90% |
| **Phase C** | Transit & Global Flags Added | ~95% |
| **Phase D** | Calibration Console Added | **100% Fully Transparent** |
