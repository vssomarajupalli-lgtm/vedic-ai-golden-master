---
archive_title: "ENGINE BOUNDARY VALIDATION"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "docs/engineering/validation/VEDIC_RULE_VALIDATION_REVIEW.md"
---

# ENGINE BOUNDARY VALIDATION

This document validates every calculation engine against **DR-007 (Engine Isolation Rule)**:
> *No Engine may directly call another Engine. All engines must consume data supplied by PipelineRunner, an Aggregated Payload, or a Prior Computed Results Dictionary.*

---

### 1. Data Layer (`json_normalizer.py`)
1. **Current Dependency Design**: Pure text parsing; no engine dependencies.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: `raw_pdf_data` -> `JsonNormalizer` -> `normalized_payload`.

### 2. Ascendant Layer
1. **Current Dependency Design**: Reads metadata parsed by JsonNormalizer. No engine calls.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: `normalized_payload["metadata"]` -> Ascendant logic.

### 3. Planet Strength Engine
1. **Current Dependency Design**: Consumes isolated `normalized_payload` subsets.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Reads parsed JSON; outputs `planet_results` dictionary.

### 4. House Strength Engine
1. **Current Dependency Design**: Requires Planet Strength (for house lord strength), which is safely injected by `PipelineRunner` as `lord_strength_score` into a copied payload.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Reads injected scores; outputs `house_results` dictionary.

### 5. Yoga Engine
1. **Current Dependency Design**: Receives `planet_results` and `house_results` dictionaries directly via its `evaluate()` arguments.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `yoga_results`.

### 6. Shodasavarga Engine
1. **Current Dependency Design**: Receives `planet_results` dictionary as read-only argument.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `varga_results`.

### 7. Dasha Engine
1. **Current Dependency Design**: Receives `planet_results` dictionary as read-only argument.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `dasha_results`.

### 8. Rasi Strength Engine
1. **Current Dependency Design**: Receives `planet_results` and `varga_results` dictionaries.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `rasi_results`.

### 9. Ashtakavarga Engine
1. **Current Dependency Design**: Receives `planet_results` dictionary.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `av_results`.

### 10. Natal Promise Engine
1. **Current Dependency Design**: Receives aggregated result dictionaries from Planet, House, Rasi, Varga, AV, and Yoga engines via `evaluate()` arguments.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `natal_promise_results`.

### 11. Transit Engine
1. **Current Dependency Design**: Receives result dictionaries from Dasha, AV, and Natal Promise via `evaluate()` arguments.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `transit_results`.

### 12. Question Engine
1. **Current Dependency Design**: The `QuestionEngine` directly imports and instantiates the `MasterProbabilityEngine` (`self.master_engine = MasterProbabilityEngine()`) to re-evaluate scoring dynamically based on isolated domain targets.
2. **DR-007 Compliance**: 🔴 **FAIL (DIRECT ENGINE CALL FLAGGED)**
3. **Required Corrections**: The `QuestionEngine` must remove all `import app.engines.master_probability_engine` references. It must strictly read the `pipeline_output` provided by the `PipelineRunner`. If dynamic re-scoring is required, the `PipelineRunner` must orchestrate the execution loop, not the `QuestionEngine`.
4. **Final Approved Boundary**: Must consume ONLY the final `pipeline_output` dictionary. Zero engine instantiations permitted.

### 13. Master Synthesis Engine (`MasterProbabilityEngine`)
1. **Current Dependency Design**: Receives the aggregated `engine_outputs` dictionary encompassing all calculated layers.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes prior dictionary payloads; outputs `master_probability` payload.

### 14. Quality Metrics Engine
1. **Current Dependency Design**: Analyzes the final `pipeline_output` dictionary statistically.
2. **DR-007 Compliance**: **PASS**
3. **Required Corrections**: None.
4. **Final Approved Boundary**: Consumes standard unified payload.

---

## Conclusion
The architecture demonstrates strict adherence to the Engine Isolation Rule (DR-007) across all core calculative layers, successfully passing data strictly via the `PipelineRunner`. 

There is **one strict violation** identified in the `QuestionEngine`, which currently acts as an orchestrator by directly calling the `MasterProbabilityEngine`. This boundary must be corrected before Phase 5 is considered structurally secure.
