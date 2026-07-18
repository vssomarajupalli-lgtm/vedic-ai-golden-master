---
archive_title: "Phase 15F.12 – Signal Pipeline Refactor Implementation"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15F.12 – Signal Pipeline Refactor Implementation

## 1. Overview
The signal extraction pipeline for the Question Engine has been successfully refactored based on the Phase 15F.11 Architecture Audit. Recursive deep-search logic has been permanently eliminated, and signal generation has been centralized into `SignalTranslator` utilizing explicit, deterministic namespace routing.

## 2. Files Modified

### A. `app/api/v1/endpoints/queries.py`
- Corrected the routing payload passed to `SignalTranslator.translate`.
- `SignalTranslator` now securely receives `engine_outputs_dict` instead of the top-level `internal_payload`.
- `FormulaEvaluator.evaluate` now explicitly receives both `engine_outputs_dict` and `isolated_signals`.

### B. `app/formulas/signal_translator.py`
- Completely refactored `translate()`.
- It now returns a deterministic `isolated_signals` dictionary directly, abandoning the unstable behavior of modifying a deep copy of the massive pipeline payload.
- All planetary, house, and lord extractions occur strictly via `engine_outputs.get("planets")` and `engine_outputs.get("houses")`.

### C. `app/formulas/evaluator.py`
- **DELETED** `extract_signals()` and its dangerous `find_keys()` recursive search.
- Updated the signature of `evaluate()` to enforce the architectural boundary: it now receives `isolated_signals` passively and focuses purely on logical formulas.

## 3. Signal Trace Comparison

**Before Refactor (Phase 15F.10):**
```python
isolated_signals["moon"] = {
  "house": 2, 
  "bindus": 4, 
  "modifier": 0
} # Overwritten by Ashtakavarga Engine
```
Frontend Render: `Moon lacks strength (0/100).`

**After Refactor (Phase 15F.12):**
```python
isolated_signals["moon"] = {
  "final_score": 71,
  "breakdown": {
    "dignity": 25.0,
    "house_placement": 10.0,
    ...
  }
} # Precisely extracted from PlanetStrengthEngine
```
Frontend Render: `Moon provides strong support (71/100).`

## 4. Regression Risk Assessment
- **Zero impact** on `PipelineRunner` math or logic, as `engine_outputs` is evaluated completely undisturbed.
- **Zero API impact**, as the exact same `StructuredQuestionResponse` structure is returned from `DisplayFormatter`.
- **High Stability**: The removal of recursive scraping mathematically guarantees zero cross-engine JSON collisions (e.g., Ashtakavarga `moon` vs Planet `moon`), satisfying all architectural requirements for the future Phase 16 Intelligence Console expansions.

The Question Engine has been secured.
