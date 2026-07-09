# PHASE9_STEP2B_QUESTION_ENGINE_DASHA_AUDIT

## Files involved:
- `frontend/src/api/backend.ts` (Frontend request constructor)
- `backend/app/schemas/question.py` (API Request Schema)
- `backend/app/api/v1/endpoints/queries.py` (Ask Question API)
- `backend/app/pipeline_runner.py` (Question Orchestrator)
- `backend/app/engines/question_engine.py` (Response Builder)

## Current code path:
1. **Question UI** generates request with `rawOutputs` (which is a `ChartProcessResponse` object).
2. **Ask Question API** (`queries.py`) receives this in `request.engine_outputs` and passes it directly to `pipeline_runner.answer_question(pipeline_output=request.engine_outputs)`.
3. **Pipeline Runner** (`pipeline_runner.py`) expects the `pipeline_output` argument to be the raw internal dictionary, so it attempts to extract `pipeline_output.get("engine_outputs", {})`.
4. Because the data is actually a `ChartProcessResponse`, the `engine_outputs` key does not exist at the root level. The lookup fails and returns an empty dictionary `{}`.
5. Empty dictionary is passed to `QuestionEngine.compose_response`.
6. **Response Builder** attempts `dasha_activation.get("synthesis", {})` on an empty dict, resulting in defaults ("unknown").
7. **Displayed Answer** renders "Unknown Mahadasha / Unknown Antardasha / Unknown Pratyantardasha".

## Expected schema:
Inside `pipeline_runner.answer_question`, `pipeline_output` is expected to have the root internal pipeline output shape:
```json
{
  "metadata": {},
  "master_probability": {},
  "engine_outputs": {
    "dashas": {
       "synthesis": { ... }
    }
  }
}
```

## Actual schema:
The API actually passes the serialized `ChartProcessResponse` shape:
```json
{
  "status": "COMPLETED",
  "final_score": 85.5,
  "probability_grade": "EXCELLENT",
  "breakdown": {
    "metadata": {},
    "master_probability": {},
    "engine_outputs": {
      "dashas": { ... }
    }
  },
  "yogas": []
}
```

## Root cause:
The frontend API call wraps the processed chart output inside `ChartProcessResponse`, placing the actual raw mathematical payload under the `breakdown` key. When `Ask Question API` passes this payload back to `pipeline_runner.py`, `pipeline_runner` tries to read `pipeline_output["engine_outputs"]` directly, but the data is buried one layer deeper inside `pipeline_output["breakdown"]["engine_outputs"]`. This schema mismatch causes the Dasha Engine outputs (and other timing layers) to be completely dropped during the question resolution phase.

## Minimal fix:
In `backend/app/api/v1/endpoints/queries.py`, when invoking `answer_question`, extract the `breakdown` layer so the pipeline runner receives the correct internal schema:
```python
        # Correctly unwrap the ChartProcessResponse schema
        internal_payload = request.engine_outputs.get("breakdown", request.engine_outputs)
        
        result = pipeline_runner.answer_question(
            question=request.question_text,
            pipeline_output=internal_payload
        )
```

## Files to modify:
- `backend/app/api/v1/endpoints/queries.py`

## Governance impact:
None. This is purely a serialization/data extraction schema bug between the API boundary and internal orchestrator. No astrological rules or prediction math need to be altered.

**PASS**
