---
archive_title: "RUNTIME_TRACE_AUDIT.md"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\audit"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# RUNTIME_TRACE_AUDIT.md

## Runtime Trace Audit Summary
This audit traces the exact data structure and key counts at each step of the Vedic-AI stateless execution flow, highlighting where data becomes empty and how it causes the "fixed 48-score" issue.

---

## 1. Step-by-Step Data Trace (Raju Canonical Data)

### Step A: Frontend Upload
The user uploads `canonical_content.json` in the web interface.
- **Top-Level Keys**: `["_meta", "birth_data", "planets", "houses", "vargas", "dashas", "ashtakavarga"]`
- **Planets Count**: 9 (`Surya`, `Chandra`, `Kuja`, `Budha`, `Guru`, `Shukra`, `Shani`, `Rahu`, `Ketu`)
- **Houses Count**: 12 (`"1"` to `"12"`)
- **Vargas Count**: 2 (`"D9"`, `"D10"`)
- **Dashas Count**: 3 (`"mahadasha"`, `"antardasha"`, `"pratyantardasha"`)
- **Ashtakavarga Count**: 2 (`"sav_chart"`, `"bav_charts"`)

### Step B: FastAPI Post Request & Pydantic Validation
The client posts the payload to `POST /api/v1/process-chart` with body:
```json
{
  "canonical_content": { ... },
  "machine_index": { ... }
}
```
FastAPI validates this payload against `ChartProcessRequest`.

### Step C: `charts.py` Endpoint Execution
The endpoint `process_chart()` extracts and merges the data:
```python
raw_data = request.canonical_content
raw_data["_machine_index"] = request.machine_index
```
This payload is then passed directly into `pipeline.process(raw_data)`.
- **Top-Level Keys**: `["_meta", "birth_data", "planets", "houses", "vargas", "dashas", "ashtakavarga", "_machine_index"]`
- **Planets Count**: 9
- **Houses Count**: 12
- **Vargas Count**: 2
- **Dashas Count**: 3
- **Ashtakavarga Count**: 2

---

## 2. Key Counts at Processing Stages

Below are the exact counts of the structural data elements at each point in the backend execution pipeline:

### 1. Before `JsonNormalizer`
Inside `PipelineRunner.process()`, before passing the data to `self.normalizer.normalize()`:
- **Top-Level Keys**: `["_meta", "birth_data", "planets", "houses", "vargas", "dashas", "ashtakavarga", "_machine_index"]`
- **Planets Count**: 9
- **Houses Count**: 12
- **Vargas Count**: 2
- **Dashas Count**: 3
- **Ashtakavarga Count**: 2

### 2. After `JsonNormalizer`
The output of `self.normalizer.normalize()` (referred to as `normalized_payload`):
- **Top-Level Keys**: `["metadata", "planets", "houses", "vargas", "ashtakavarga", "dashas", "transits"]`
- **Planets Count**: 9 (standardized keys: `sun`, `moon`, `mars`, `mercury`, `jupiter`, `venus`, `saturn`, `rahu`, `ketu`)
- **Houses Count**: 12 (standardized keys: `"1"` to `"12"`)
- **Vargas Count**: 2 (standardized keys: `"D9"`, `"D10"`)
- **Dashas Count**: 3 (standardized keys: `"mahadasha"`, `"antardasha"`, `"pratyantardasha"`)
- **Ashtakavarga Count**: 2 (standardized keys: `"sav_chart"`, `"bav_charts"`)

### 3. Before PipelineRunner (Input to process)
This is identical to Stage 1 (**Before JsonNormalizer**), as the runner's first action is to invoke the normalizer.
- **Top-Level Keys**: `["_meta", "birth_data", "planets", "houses", "vargas", "dashas", "ashtakavarga", "_machine_index"]`
- **Planets Count**: 9
- **Houses Count**: 12
- **Vargas Count**: 2
- **Dashas Count**: 3
- **Ashtakavarga Count**: 2

### 4. After PipelineRunner (Final Output payload)
The final dictionary returned by `PipelineRunner.process()`:
- **Top-Level Keys**: `["metadata", "master_probability", "engine_outputs"]`
- **`engine_outputs` Sub-Keys**: `["planets", "houses", "vargas", "dashas", "ashtakavarga", "natal_promise", "transit", "yogas"]`
- **Planets Count**: 9 (sun, moon, mars, mercury, jupiter, venus, saturn, rahu, ketu)
- **Houses Count**: 12 ("1" to "12")
- **Vargas Count**: 2 (D9, D10)
- **Dashas Count**: 9 (The temporal engine projects dasha activation metrics for all 9 planets)
- **Ashtakavarga Count**: 4 (`sav_chart`, `bav_charts`, `planet_bav_support`, `dasha_bav_support`, `sav_analytics`, `engine_modifiers`)

---

## 3. Root Cause of the 48-Score Issue

The "fixed 48-score" issue is triggered when the `JsonNormalizer` receives a payload where all core data keys are either missing or nested incorrectly, causing the normalization filters to return empty structures.

### The Mechanism:
1. **Empty Input Resolution**:
   If the input payload does not match the normalizer's target dictionary structure (e.g., if keys are nested inside another key or are named differently), `JsonNormalizer` falls back to empty defaults:
   - `planets` = `{}`
   - `houses` = `{}`
   - `vargas` = `{}`
   - `dashas` = `{}`
   - `ashtakavarga` = `{"sav_chart": {}, "bav_charts": {}}`

2. **Neutral Baseline Fallback**:
   Because the normalizer output is empty, downstream calculation engines find no data for the native's chart. To prevent runtime crashes, the engines fall back to a **neutral baseline score of 50.0** for all structural factors:
   - Primary House score = `50.0`
   - Support Houses score = `50.0`
   - Karaka Planet score = `50.0`
   - House Lord score = `50.0`
   - Divisional Varga score = `50.0`

3. **SAV Zero Bias**:
   Unlike other factors, the Ashtakavarga SAV support has no default neutral baseline; it reads directly from the empty `sav_chart` and defaults to **`0.0`** bindu support.

4. **The Mathematical Proof**:
   In `NatalPromiseEngine`, the composite score is calculated using the weighted sum of these factors. For all domains, this weighted sum computes to:
   
   $$\text{Composite Score} = (w_1 \times 50.0) + (w_2 \times 50.0) + (w_3 \times 50.0) + (w_4 \times 50.0) + (w_5 \times 50.0) + (w_6 \times 0.0)$$
   
   Since the weights ($w_1 + w_2 + w_3 + w_4 + w_5 + w_6$) sum to $1.0$, and $w_6$ (SAV weight) is exactly $0.05$, the sum of the remaining weights is $0.95$.
   
   $$\text{Composite Score} = 0.95 \times 50.0 = 47.5$$
   
   Applying the rounding function `round(47.5)` yields exactly **`48`** with the grade **`WEAK`** across all 8 domains (Marriage, Career, Wealth, Education, Children, Property, Health, and Spirituality).
