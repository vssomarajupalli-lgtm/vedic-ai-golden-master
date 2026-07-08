# PHASE 12D: FORMULA REPOSITORY IMPLEMENTATION BLUEPRINT

## 1. Formula Repository File Layout

The implementation will introduce a specialized module within the `core` directory, isolating it from the `engines` and the `api`.

*   `backend/app/core/formula_repository/`
    *   `__init__.py`
    *   `loader.py` (Contains `FormulaRepositoryLoader`)
    *   `validator.py` (Contains `FormulaValidator` for boot-time checks)
    *   `evaluator.py` (Contains `FormulaEvaluator` to process confidence layers)
    *   `registry/`
        *   `marriage_formulas.json` (or `.py` dictionaries since JSON is banned in this doc's generation constraint)
        *   `career_formulas.json`
        *   `wealth_formulas.json`

## 2. Formula Loader Flow

1.  **Request Initiation:** The `QuestionRouter` receives a `question_id` and resolves it to a `formula_key`.
2.  **Loader Invocation:** The Router calls `FormulaRepositoryLoader.get_formula(formula_key)`.
3.  **Cache Check:** The Loader checks its internal memory dictionary for the parsed formula.
4.  **Retrieval:** If cached, it returns the formula schema object. If not, it loads it from the specific category file within the `registry` folder.
5.  **Not Found Handling:** If the key is missing, it raises a `FormulaNotFoundError`.

## 3. Formula Validation Flow (Boot-Time)

1.  **System Boot:** Upon FastAPI startup, `FormulaValidator.validate_all()` executes.
2.  **Key Uniqueness:** Scans all files in the `registry` folder. If a duplicate `formula_key` is found, the server crashes with a `DuplicateFormulaError`.
3.  **Engine Verification:** Reads `required_engines` for each formula and verifies those engines exist in the system registry.
4.  **Signal Verification:** Ensures `required_signals` conform to known astrological entities (e.g., rejecting typos like "7th Hus").
5.  **Threshold Validation:** Mitigating Risk-FR-01, it ensures `required_confidence_layers` has explicit, unambiguous mathematical thresholds for evaluation.

## 4. Formula Evaluation Flow

1.  **Data Plucking:** The `FormulaEvaluator` receives the `ChartProcessResponse` (the massive JSON payload from the Mathematical Engines) and the `FormulaSchema`.
2.  **Null Payload Check:** (Mitigating Risk-FR-05) The Evaluator attempts to extract exactly what is specified in `required_signals`. If an array is completely empty or missing, it aborts the layer.
3.  **Isolation:** The Evaluator creates a specialized, minimized payload containing ONLY the requested signals, blinding the rest of the chart.

## 5. Confidence Layer Evaluation Flow

1.  **Sequential Checking:** The `FormulaEvaluator` processes the `required_confidence_layers`.
2.  **Natal Base:** It checks the Natal Promise layer first. If this evaluates to a definitive 'Denied' state, the evaluation halts, overriding all subsequent positive layers.
3.  **Dasha/Transit Overlays:** It checks the active Dasha and Transits against the `required_signals`.
4.  **Strict Matrix Resolution:** (Mitigating Risk-FR-01) The Evaluator runs the results through a hardcoded matrix to output a definitive string: `FAVORABLE`, `MIXED`, or `UNFAVORABLE`. No subjective "majority" counting.

## 6. Answer Template Resolution Flow

1.  **Template Binding:** Based on the `FAVORABLE` / `MIXED` / `UNFAVORABLE` output from the Evaluator, the system selects the `positive_template`, `neutral_template`, or `challenging_template`.
2.  **Context Injection:** The selected template, along with the minimized signal payload and the evaluation result string, is passed to the Answer Composer.
3.  **Strict Boundary:** The LLM receives instructions to format the result using the selected template. It is explicitly forbidden from overriding the evaluation result string.

## 7. Failure Handling

1.  **Formula Not Found:** Returns HTTP 500 (Configuration Error) to prevent the user from experiencing silent failures.
2.  **Validation Failure at Boot:** Prevents server deployment.
3.  **Payload Extraction Failure:** If a requested signal cannot be plucked due to a malformed `ChartProcessResponse`, the Evaluator triggers the Engine Degradation protocol.

## 8. Engine Degradation Handling

(Mitigating Risk-FR-03)
1.  **Detection:** The `FormulaEvaluator` realizes a `required_engine` (e.g., `TransitEngine`) failed to populate the `ChartProcessResponse`.
2.  **Fallback Evaluation:** The Evaluator skips the confidence layers associated with that engine.
3.  **Forced Neutrality:** The final result is capped at `MIXED`. It cannot be `FAVORABLE` or `UNFAVORABLE` if critical timing data is missing.
4.  **Template Injection:** A system warning string is appended to the payload for the Answer Composer: *"Note: Transit data is currently unavailable. This assessment relies purely on static Natal and Dasha indicators."*

## 9. Future Gochara Hook Points

1.  **Flag Detection:** If `future_gochara_required == true`, the Evaluator flags the `PipelineRunner`.
2.  **Reference Shift:** A placeholder function `evaluate_moon_centered_transits()` is called.
3.  **Current State:** In Phase 12, this function simply returns the standard Lagna-based transit array.
4.  **Future State:** In the Gochara Phase, this function will inject the Moon's longitude into the `TransitEngine` and calculate a 12-month future array before returning the payload to the Evaluator.
5.  **State Wiping:** (Mitigating HAZ-GO-01) The reference shift flag is strictly scoped to the specific evaluation thread and destroyed immediately after resolution.

## 10. Unit Test Strategy

1.  **Validation Tests:** `test_formula_validator.py` - Intentionally feed duplicate keys and invalid signals to ensure it crashes.
2.  **Loader Tests:** `test_formula_loader.py` - Ensure successful caching and retrieval.
3.  **Evaluator Matrix Tests:** `test_formula_evaluator.py` - Provide mocked `ChartProcessResponse` payloads and assert that the `FAVORABLE`/`MIXED`/`UNFAVORABLE` matrix resolves with 100% mathematical accuracy.
4.  **Degradation Tests:** Pass a payload missing the `TransitEngine` outputs and verify it degrades to `MIXED` with the correct warning string.
