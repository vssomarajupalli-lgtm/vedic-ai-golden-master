# FORMULA EVALUATOR ARCHITECTURE v1

## 1. Responsibilities
The `FormulaEvaluator` serves as the sole arbiter between the mathematical engines' raw output (`ChartProcessResponse`) and the generative Answer Composer.
- **Data Extractor:** Plucks only the specific variables defined in a formula's `required_signals`.
- **Condition Assessor:** Evaluates the `required_confidence_layers` purely as a series of boolean checks against the extracted data.
- **Degradation Manager:** Determines if a missing engine output degrades the final assessment from `FAVORABLE`/`UNFAVORABLE` to `MIXED`.

**Governance Limits:** The Evaluator performs **no mathematical calculations** (e.g., no degree measurements, no dasha boundary calculations) and utilizes **no hidden scoring systems**.

## 2. Formula Evaluation Flow
1. **Invocation:** The `PipelineRunner` successfully calculates the chart and passes `ChartProcessResponse` and `FormulaSchema` to `FormulaEvaluator.evaluate()`.
2. **Extraction:** The Evaluator iterates through `formula.required_signals` and isolates only those nodes from the massive JSON response.
3. **Engine Validation:** The Evaluator checks if all `formula.required_engines` actually populated data in the `ChartProcessResponse`.
4. **Condition Checking:** The Evaluator loops through `formula.required_confidence_layers` and marks each as `True` or `False`.
5. **Resolution:** The Evaluator resolves the final state (`FAVORABLE`, `MIXED`, or `UNFAVORABLE`) based on a strict matrix (no numeric weighting).
6. **Output:** Returns a `FormulaEvaluationResult` containing the final state, the isolated payload, and the appropriate `answer_template_key`.

## 3. Engine Output Consumption Model
The Evaluator acts as a "dumb consumer" of engine payloads.
- **Example:** If a formula requires `7th_lord_dignity`.
- **Action:** The Evaluator does not calculate dignity. It looks at the `NatalPromiseEngine` output block: `payload.natal_promise.houses[7].lord_dignity`.
- **Logic Rule:** If `payload.natal_promise.houses[7].lord_dignity` exists, it consumes the value ("Exalted", "Debilitated", etc.). If the string is in a hardcoded set of positive dignities, the layer passes.

## 4. Confidence Layer Evaluation Model
The Confidence Layer evaluation uses a strict boolean resolution matrix rather than a numeric score to prevent arbitrary weights.
- **Fatal Denials:** If the Natal Promise (D1) layer explicitly denies the event (e.g., severe affliction with no rescue yogas), the result is hardcoded to `UNFAVORABLE`, bypassing subsequent layers.
- **Positive Matrix:** If Natal Promise is supportive, and active Dasha aligns, and Transit aligns, the result is `FAVORABLE`.
- **Mixed Matrix:** If Natal Promise is supportive, but active Dasha does NOT align, the result is forced to `MIXED` (indicating delay or effort required).
- *Implementation detail:* The evaluator uses pure logical `AND`/`OR` gating mapped to the specific conditions in `required_confidence_layers`.

## 5. Graceful Degradation Strategy
To prevent systemic failure (Risk-FR-03), the Evaluator implements Graceful Degradation when an engine is offline or times out.
- **Trigger:** A required engine (e.g., `TransitEngine`) returns `None` or an empty object in the `ChartProcessResponse`.
- **Action:** The Evaluator aborts the specific confidence layers relying on that engine.
- **Consequence:** The final assessment state is instantly capped at `MIXED` (it cannot be definitively `FAVORABLE` or `UNFAVORABLE` without full data).
- **Injection:** A `system_warning` flag is appended to the final result, instructing the LLM to notify the user of the missing data scope.

## 6. Missing Payload Handling
(Mitigating Risk-FR-05)
- **Trigger:** An engine ran successfully, but the specific `required_signal` (e.g., `11th_house_bindus`) is missing or malformed inside the payload.
- **Action:** The Evaluator logs an error, treats that specific condition as `False` (unfulfilled), and continues evaluation. It does not invent or interpolate missing data. If critical, it triggers the Graceful Degradation to `MIXED`.

## 7. Future Gochara Hook Points
- **Trigger:** `formula.future_gochara_required == True`.
- **Phase 13 State:** The Evaluator simply notes the flag but consumes the standard, current-time TransitEngine output.
- **Future State:** This flag will eventually force the `PipelineRunner` to generate a 12-month future array. The Evaluator's architecture is already designed to consume arrays of signals (e.g., looping over 12 months of transits to find the `True` hit) rather than just a single static snapshot.

## 8. Answer Composer Integration Boundary
The `FormulaEvaluationResult` establishes a rigid firewall for the LLM.
The object passed to the Answer Composer contains **only**:
- `final_state` (FAVORABLE / MIXED / UNFAVORABLE)
- `answer_template_key`
- `isolated_signals` (A dictionary of ONLY the planets/houses requested by the formula).
- `system_warnings` (If degradation occurred).

The LLM is completely blind to the rest of the astrological chart, preventing hallucinated prose about unrequested planets.

## 9. Unit Test Strategy
The implementation phase (Phase 13C) will require exhaustive testing of the Evaluator.
- **Test 1:** Pass a mocked `ChartProcessResponse` with perfect alignments -> Assert `FAVORABLE`.
- **Test 2:** Pass a mocked `ChartProcessResponse` with an empty `TransitEngine` payload -> Assert `MIXED` and `system_warnings` generated.
- **Test 3:** Pass a mocked `ChartProcessResponse` missing a required signal -> Assert condition falls back to `False`.
- **Test 4:** Assert the `isolated_signals` dictionary completely strips out any planets/houses not defined in `formula.required_signals`.
