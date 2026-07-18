---
archive_title: "Phase 15F.11 – Signal Pipeline Architecture Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15F.11 – Signal Pipeline Architecture Audit

## 1. Complete Signal Lifecycle Trace
The lifecycle of signal data from raw pipeline generation to the frontend React component currently follows this fragile trajectory:

1. **PipelineRunner** ➔ Generates absolute truth matrices.
2. **Query Endpoint** (`queries.py`) ➔ Orchestrates formula execution.
3. **SignalTranslator** ➔ Attempts to adapt pipeline models to semantic formula requirements.
4. **FormulaEvaluator** ➔ Attempts to execute logical checks on the payload.
5. **extract_signals()** ➔ Performs blind recursive deep-search to isolate specific items.
6. **isolated_signals** ➔ The output payload dictionary used for response hydration.
7. **DisplayFormatter** ➔ Converts the JSON structures into textual arrays for the frontend.
8. **StructuredQuestionResponse** ➔ API response schema.
9. **QuestionResultCard** ➔ Frontend React component consuming the text arrays.

## 2. Layer Analysis

| Layer | Input Structure | Output Structure | Data State / Anomalies |
|-------|-----------------|------------------|------------------------|
| **PipelineRunner** | `RAJU_CANONICAL_RAW` | Full JSON (`internal_payload`) containing `engine_outputs`. | **Pristine.** True planetary states (`final_score`: 71) exist here. |
| **Query Endpoint** | `internal_payload` | `internal_payload` | **Erroneous Routing.** Passes `internal_payload` into `SignalTranslator` instead of extracting `engine_outputs` first. |
| **SignalTranslator** | `internal_payload`, `required_signals` | `final_payload` (Shallow copy of input) | **Data Missed.** Fails to locate `"planets"` at the top level. Outputs without appending required signals to the top level. |
| **extract_signals()** | `final_payload`, `required_signals` | `isolated_signals` | **Data Overwritten.** Recursively searches the tree. Finds `"moon"` in `planets` (good) but then finds `"moon"` in `ashtakavarga.planet_bav_support` and overwrites the rich dictionary. |
| **isolated_signals**| — | `{"moon": {"house": 2, "bindus": 4}}` | **Structurally Compromised.** The `final_score` and `breakdown` keys are completely lost. |
| **DisplayFormatter** | `isolated_signals` | Arrays of strings (`attention_factors`) | **Data Defaulted/Modified.** Looks for `final_score`, fails, defaults to `0`, and classifies it as `lacks strength (0/100)`. |
| **QuestionResultCard**| `StructuredQuestionResponse` | React DOM Elements | **Displays False Information.** |

## 3. Architecturally Correct Ownership Point
Currently, `FormulaEvaluator.extract_signals()` generates `isolated_signals`. This is an architectural violation; `FormulaEvaluator` should only care about mathematical logic, thresholds, and booleans.

**Recommendation: A. SignalTranslator (evolving into a Dedicated SignalEngine)**
`isolated_signals` should be built deterministically by `SignalTranslator`. The Translator inherently possesses the maps (`PLANET_MAP`, `HOUSE_MAP`) required to resolve semantic strings (e.g., `"7th_lord"`) to exact pipeline coordinates (e.g., `engine_outputs["planets"]["venus"]`).

## 4. Input Payload for SignalTranslator
**Answer: `engine_outputs`**
`SignalTranslator` operates exclusively on astrological data constructs. `internal_payload` encapsulates non-astrological wrapper metadata (e.g., `pipeline_metadata`, `processing_time_ms`, `status`). By passing `engine_outputs`, the Translator naturally interacts with top-level astrological domains (`planets`, `houses`, `ashtakavarga`), eliminating the current routing bug that breaks planetary hydration.

## 5. Recursive Deep-Search Extraction
**Should it remain? Absolutely Not.**
Blind recursive JSON extraction is an anti-pattern in deterministic astrology pipelines.
- **Ambiguity:** `moon` exists as a planet, a functional nature trait, a D9/D10 sub-planet, and an ashtakavarga BAV chart.
- **Collision:** Safe dictionary merging cannot handle intentional namespace overlaps (e.g., the BAV dictionary overwriting the `PlanetStrengthEngine` dictionary).
- **Performance:** Traversing a massive, heavily nested astrological dictionary repeatedly is highly inefficient.
Signals must be extracted via exact, absolute namespace paths (e.g., `payload["planets"]["moon"]`).

## 6. Recommended Final Stable Architecture
1. `SignalTranslator` is promoted. It takes `required_signals` and `engine_outputs`.
2. It uses exact path routing (e.g., `engine_outputs.get("planets", {}).get(sanskrit_name)`) to pluck exactly what is needed.
3. It directly outputs `isolated_signals` as a perfectly formed, flat dictionary.
4. `FormulaEvaluator` receives this clean `isolated_signals` dictionary and performs logic *without* executing any deep searches.
5. `DisplayFormatter` iterates over `isolated_signals` securely.

## 7. Migration Plan

### Step 1: Minimal Fix (Immediate Stabilization)
Modify `app/api/v1/endpoints/queries.py` to pass `engine_outputs` into `SignalTranslator` rather than the top-level `internal_payload`. This instantly allows `SignalTranslator` to append rich dictionaries to the payload root, preventing the `ashtakavarga` recursive overwrite.
```python
engine_outputs_dict = internal_payload.get("engine_outputs", internal_payload)
translated_payload = SignalTranslator.translate(f.required_signals, engine_outputs_dict)
```

### Step 2: Recommended Fix (Deprecation of Deep Search)
1. Refactor `SignalTranslator.translate` to return `isolated_signals` directly, mapping explicitly to exact paths.
2. Strip out `extract_signals()` entirely from `FormulaEvaluator`.
3. Pass `isolated_signals` directly into the evaluation and formatting layers.

### Step 3: Long-Term Architecture (Phase 16 Intelligence Console)
Extract `SignalTranslator` into a standalone `SignalExtractionService`. This allows the `Signal Trace Console`, the `Question Engine`, and future AI Prompt architectures to universally request semantic signals (e.g., `"10th_lord_in_d10"`) and receive standardized, deeply structured planetary/house dictionaries without any parsing overhead.
