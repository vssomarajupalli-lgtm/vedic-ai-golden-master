# QUESTION ENGINE IMPACT REPORT

If the rule `Question Engine = Natal Promise + Dasha Activation` is permanently frozen, the following cascading failures will occur unless modified:

## 1. Engine Degradation Failures
If `TransitEngine` is removed from the payload generation step (to honor the isolation rule), but remains in the `required_engines` array of the Formulas (e.g. `FAM_PROGENY_BASE`), the `FormulaEvaluator` will detect the missing payload and throw an "Engine Degradation: TransitEngine output is missing" warning. This automatically triggers the formula to downgrade to "MIXED" state.

## 2. Invalid Confidence Layers
Variants like `AST_PROP_TIMING` rely on layers such as `transit_jupiter_saturn_activate_4th` to reach 100% layer fulfillment. If Mandali is disconnected from the evaluator, this boolean layer will forever evaluate as `False`. Therefore, the Variant will fail to ever return a "FAVORABLE" state, breaking the timing probability for all Property timing questions.

## 3. Answer Composer Misalignment
The Answer Composer uses `future_gochara_required = True` to determine if it should inject a "deferment" text (e.g., "The exact timing requires future transit calculations"). If Mandali is moved to an independent advisory layer in the final JSON payload (Reporting Structure Layer 3), the Question Engine schemas no longer need this deferment flag at all, because the Question Engine isn't supposed to know or care about Gochara anymore.

## 4. Required Modifications List
To comply with the new Governance, we must:
1.  **Refactor `registry_data.py`**:
    *   Strip `TransitEngine` from all `required_engines`.
    *   Strip all `transit_...` flags from `required_confidence_layers`.
    *   Remove `future_gochara_required` entirely.
2.  **Refactor `evaluator.py`**:
    *   Remove the hardcoded check for the string `"transit"` in the layer evaluator.
3.  **Refactor `question_registry.json`**:
    *   Remove or false out all `future_gochara_required` flags.
4.  **Refactor Answer Composer (LLM Prompt Layer)**:
    *   Update the Answer Composer to accept a new `mandali_commentary` string alongside the Question Engine result, combining them at the NLP stage rather than the mathematical stage.
