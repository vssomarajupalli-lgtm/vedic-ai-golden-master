---
archive_title: "PHASE 9 STEP 2C: QUESTION ENGINE DASHA FIX"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE 9 STEP 2C: QUESTION ENGINE DASHA FIX

## Summary
The Question Engine API layer (`queries.py`) was unwrapping the HTTP request payload directly into the pipeline runner, causing a schema mismatch because the front-end sends the data wrapped in a `ChartProcessResponse` (which places raw outputs inside `.breakdown`). We added a safe unwrapping fallback directly before `pipeline_runner.answer_question()` is called.

## Files Changed
1. `backend/app/api/v1/endpoints/queries.py`
   - Added `internal_payload = request.engine_outputs.get("breakdown", request.engine_outputs)` to ensure the orchestrator gets the `engine_outputs` dictionary at the root level.

## Tests Executed
A manual test script validating the QuestionRequest schema unwrap was run successfully.

## Question Validation Result
`Active dasha: Venus Mahadasha / Jupiter Antardasha / Rahu Pratyantardasha.` successfully extracted instead of `Unknown Mahadasha / Unknown Antardasha / Unknown Pratyantardasha`.

## Governance Review
This fix modifies solely the API parsing boundary in `queries.py`.
- **DashaEngine**: Unchanged.
- **PipelineRunner**: Unchanged.
- **Astrology engines**: Unchanged.
- **Probability engines**: Unchanged.
- **Varga logic**: Unchanged.

The fix respects STRICT GOVERNANCE and allows correct temporal data to reach the LLM Response Builder logic without modifying mathematical core loops.
