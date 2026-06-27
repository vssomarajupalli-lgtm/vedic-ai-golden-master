# Phase 15 Final Regression Evidence

```text
Created : 2026-06-25
Time    : 10:25 AM IST
Phase   : Phase 15
Type    : Regression Evidence
Status  : PERMANENT RECORD
```

## Executive Summary

*Cross-References:*
- Followed by: [Phase 16A.1 Mathematical Calibration Audit](file:///d:/vedic-ai-system/docs/audits/phase_16a1_mathematical_calibration_audit.md)

This document provides objective, reproducible evidence from the **CURRENT** checked-out codebase demonstrating the critical regressions and architectural violations reported in the Final Release Readiness Validation.

---

## 1. D1 Immutability & Varga Refinement Violation

**Assertion:** The Varga Engine actively overwrites the D1 base score instead of applying a fractional modifier, violating both D1 Immutability and the Varga Refinement Principle.

**pytest command executed:**
`pytest backend/tests/test_varga_engine.py::TestVargaEngine::test_base_score_immutability -v`

**Actual pytest output (relevant section):**
```python
    def test_base_score_immutability(self):
        normalized_data = {"planets": {"saturn": {}}}
        dependency_scores = {"saturn": {"final_score": 75.0}}
    
        results = self.engine.evaluate(normalized_data, dependency_scores)
    
>       self.assertEqual(results["D9"]["planets"]["saturn"]["final_score"], 75.0)
E       AssertionError: 50.0 != 75.0

backend\tests\test_varga_engine.py:94: AssertionError
```

**Full failing test name:**
`backend/tests/test_varga_engine.py::TestVargaEngine::test_base_score_immutability`

**Details:**
*   **Assertion message:** `AssertionError: 50.0 != 75.0`
*   **Expected value:** `75.0` (The original D1 base score)
*   **Actual value:** `50.0` (The overwritten score)
*   **Source file and line number responsible:** `backend/app/engines/varga_engine.py:68` and `76`.

**Exact Code Path (Overwriting D1):**
In `backend/app/engines/varga_engine.py`:
```python
40: base_score = dependency_scores.get(planet_name, {}).get("final_score", 0.0)
# ... base_score is completely ignored ...
66: d9_strength_result = self.planet_engine.calculate_strength(d9_data, shadbala_data={})
68: d9_final_score = float(d9_strength_result.get("final_score", 50.0))
# ...
71: results["D9"]["planets"][planet_name] = {
# ...
76:     "final_score": d9_final_score, # OVERWRITES BASE SCORE
# ...
```

**Status:** The failure **EXISTS** in the current checked-out code.

---

## 2. Engine Isolation Rule (FormulaEvaluator Breakage)

**Assertion:** The `FormulaEvaluator` interface has been broken by adding `isolated_signals` as a required positional argument, breaking existing pipeline runners and violating Engine Isolation.

**pytest command executed:**
`pytest backend/tests/test_pipeline_end_to_end.py::test_negative_engine_degradation -v`

**Actual pytest output (relevant section):**
```python
    def run_pipeline(question_id: str, payload: Dict[str, Any]) -> ComposerPromptPackage:
        router = QuestionRouter()
        route_result = router.route_question(question_id)
        if route_result["status"] == "error":
            raise ValueError(route_result["message"])
    
        formula_key = route_result["formula_key"]
        formula = formula_repository_loader.get_formula(formula_key)
>       eval_result = FormulaEvaluator.evaluate(formula, payload)
E       TypeError: FormulaEvaluator.evaluate() missing 1 required positional argument: 'isolated_signals'

backend\tests\test_pipeline_end_to_end.py:50: TypeError
```

**Details:**
*   **Exact TypeError:** `TypeError: FormulaEvaluator.evaluate() missing 1 required positional argument: 'isolated_signals'`
*   **Exact Method Signature:** `def evaluate(formula: FormulaSchema, engine_outputs: Dict[str, Any], isolated_signals: Dict[str, Any]) -> FormulaEvaluationResult:` (from `backend/app/formulas/evaluator.py:29`)
*   **Caller:** `run_pipeline()` in `backend/tests/test_pipeline_end_to_end.py:50` (`eval_result = FormulaEvaluator.evaluate(formula, payload)`)
*   **Full failing test names:** All 4 tests in `test_pipeline_end_to_end.py` (e.g., `test_scenario_1_marriage_timing`, `test_negative_engine_degradation`).

**Status:** The failure **EXISTS** in the current checked-out code.

---

## 3. PlanetStrength Numerical Parity Breakage

**Assertion:** The transparency work significantly altered the numerical constants/weights in the `PlanetStrengthEngine`, completely breaking numerical parity without updating test expectations.

**pytest command executed:**
`pytest backend/tests/test_planet_strength_engine.py -v`

**Actual pytest output (failed assertions):**

**Failure 1 (Exalted planet):**
```python
>       self.assertEqual(result["raw_score"], 115.0)
E       AssertionError: 79.25 != 115.0
backend\tests\test_planet_strength_engine.py:27: AssertionError
```

**Failure 2 (Debilitated planet):**
```python
>       self.assertEqual(result["raw_score"], -20.0)
E       AssertionError: 20.75 != -20.0
backend\tests\test_planet_strength_engine.py:52: AssertionError
```

**Failure 3 (Dignity Modifier):**
```python
>       self.assertEqual(res1["breakdown"]["dignity"], 20)
E       AssertionError: 15.0 != 20
backend\tests\test_planet_strength_engine.py:78: AssertionError
```

**Failure 4 (Missing Data Default Fallback):**
```python
>       self.assertEqual(result["final_score"], 45)
E       AssertionError: 55 != 45
backend\tests\test_planet_strength_engine.py:72: AssertionError
```

**Status:** The 7 total test failures **EXIST** in the current checked-out code.

---

## Conclusion

The evidence extracted directly from the current active codebase (`pytest` executions) explicitly confirms that the previously reported architectural and mathematical violations are **NOT obsolete**, are currently active, and block the release.
