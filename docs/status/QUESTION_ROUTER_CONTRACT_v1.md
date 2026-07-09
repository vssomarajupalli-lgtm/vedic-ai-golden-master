# QUESTION ROUTER CONTRACT v1

## 1. ROUTER CONTRACT
The Question Router is the orchestrator module bridging the API Request with the Formula Repository. It determines exactly what mathematical rules govern the incoming `question_id`.

### Input
- `question_id` (string)
- `pipeline_output` (The un-nested `engine_outputs` dictionary)

### Output
- `evaluated_formula` (A consolidated JSON object containing strictly the required mathematical booleans/scores mapped from the `engine_outputs`).

### Validation Rules
1. **Sanity Check:** Ensure the `question_id` exists in the local registry.
2. **Data Availability Check:** Validate that `pipeline_output` contains all layers mandated by the `docs/architecture/QUESTION_REGISTRY_MAPPING_v1.md` schema (e.g., if `timing_required` is true, the `dashas.synthesis` object MUST be present).
3. **Strict Rejection:** If required engine outputs are missing, the Router aborts and throws an internal schema validation error.

## 2. ANSWER CONTRACT
The Answer Composer (LLM) receives the final filtered output from the Router and formats it into natural language.

### What Answer Composer Receives
The Answer Composer receives the `evaluated_formula` and a system prompt dictating the answer structure.
**Example Payload Sent to LLM:**
```json
{
  "system_instruction": "Format the following astrological data into a 2-sentence response regarding Marriage Timing.",
  "data_context": {
    "natal_promise_score": 75,
    "active_mahadasha": "Venus",
    "active_antardasha": "Jupiter",
    "transit_activation_score": 60.0
  }
}
```

### Forbidden Actions
- **No Mathematics:** The LLM is strictly forbidden from inferring astrological rules, predicting dates, or analyzing houses directly.
- **No Hallucinations:** The LLM must not invent `active_mahadasha` lords if they are not explicitly present in the `data_context`.

### Engine Isolation Preservation
The Answer Composer operates in a complete sandbox. It has zero visibility into the `DashaEngine`, `TransitEngine`, or `NatalPromiseEngine`. It only receives the final strings and integers output by the Router's mapping formula.

## 3. GOVERNANCE
The implementation of the Question Router and Answer Composer MUST explicitly uphold the Phase 7 Architectural Locks:
- `DashaEngine` **UNCHANGED**
- `NatalPromiseEngine` **UNCHANGED**
- `YogaEngine` **UNCHANGED**
- `AshtakavargaEngine` **UNCHANGED**
- `TransitEngine` **UNCHANGED**

**No Math Duplication:** The Router will solely *read* from `pipeline_output`. It will NEVER recalculate base strength, calculate a Dasha timeline, or assess planetary dignities itself.
