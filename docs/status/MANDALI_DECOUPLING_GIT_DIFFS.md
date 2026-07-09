# MANDALI DECOUPLING EXECUTION REVIEW

## A. Before/After Formula Arrays

**Before:**
```python
    FormulaSchema(
        formula_key="MAR_TIMING_BASE",
        formula_name="Marriage Timing Base",
        formula_category="Timing Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
        required_signals=["7th_house", "7th_lord", "venus", "lagna_lord"],
        required_dasha_layers=["mahadasha", "antardasha"],
        required_confidence_layers=["dasha_lord_aspect_7th", "dasha_lord_is_venus", "jupiter_transit_7th_lagna"],
        future_gochara_required=True,
        answer_template_key="timing_assessment_v1"
    )
```

**After:**
```python
    FormulaSchema(
        formula_key="MAR_TIMING_BASE",
        formula_name="Marriage Timing Base",
        formula_category="Timing Assessment",
        required_engines=["NatalPromiseEngine", "DashaEngine"],
        required_signals=["7th_house", "7th_lord", "venus", "lagna_lord"],
        required_dasha_layers=["mahadasha", "antardasha"],
        required_confidence_layers=["dasha_lord_aspect_7th", "dasha_lord_is_venus"],
        answer_template_key="timing_assessment_v1"
    )
```
*(This identical transformation was systematically applied to all 11 modified variants/bases)*

## B. Removed Transit Confidence Layers

The following exact strings were stripped from their respective `required_confidence_layers` arrays:
1. `"jupiter_transit_7th_lagna"` (from `MAR_TIMING_BASE`)
2. `"transit_saturn_jupiter_activate_10th"` (from `CAR_CHANGE_TIMING`)
3. `"transit_jupiter_aspect_lagna"` (from `HLT_RECOVERY_TIMING`)
4. `"transit_jupiter_saturn_activate_4th"` (from `AST_PROP_TIMING`)
5. `"transit_jupiter_aspect_5th_9th"` (from `FAM_CHILD_TIMING`)

## C. Removed TransitEngine References

1.  `"TransitEngine"` string deleted from `required_engines` array across 5 Base Families.
2.  `"transit"` object deleted from the `mock_chart_payload` fixture in the test suite.
3.  The following exact block was deleted from `backend/app/formulas/evaluator.py`:
    ```python
    if "transit" in layer.lower() and any("TransitEngine" in w for w in system_warnings):
        is_fulfilled = False
    ```

## D. Why 670 Tests Passed After Removing Dependencies

The 670 tests passed perfectly because the mathematical engines are modular and the `evaluator.py` logic is generic. 
1.  **Generic Evaluation:** The `evaluator.py` does not hardcode checks for specific Transit signals; it simply checks if the length of the fulfilled `required_confidence_layers` array matches the length of the required array. Because we deleted the `transit_...` strings from the requirement arrays in `registry_data.py`, the required length dropped from (e.g., 3 to 2). The Dasha mock payload fulfilled the remaining 2, resulting in a perfect 100% pass condition (`FAVORABLE`).
2.  **Mock Payload Update:** We updated `test_pipeline_end_to_end.py` to remove the `"transit"` JSON block from the `mock_chart_payload` and shifted the degradation test from `TransitEngine` to `DashaEngine`. This prevented the evaluator from throwing a "Missing Payload" error.
3.  **Legacy Assertions Fixed:** We updated `test_formula_inheritance.py` to assert that `future_gochara_required` is `False` instead of `True`, and to assert that `DashaEngine` is inherited instead of `TransitEngine`.

---

## E. Git Diff (Core Files)

### `registry_data.py`
```diff
@@ -11,11 +11,10 @@ SEED_FORMULAS = [
         formula_key="MAR_TIMING_BASE",
         formula_name="Marriage Timing Base",
         formula_category="Timing Assessment",
-        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
+        required_engines=["NatalPromiseEngine", "DashaEngine"],
         required_signals=["7th_house", "7th_lord", "venus", "lagna_lord"],
         required_dasha_layers=["mahadasha", "antardasha"],
-        required_confidence_layers=["dasha_lord_aspect_7th", "dasha_lord_is_venus", "jupiter_transit_7th_lagna"],
-        future_gochara_required=True,
+        required_confidence_layers=["dasha_lord_aspect_7th", "dasha_lord_is_venus"],
         answer_template_key="timing_assessment_v1"
     ),
@@ -43,11 +42,10 @@ SEED_FORMULAS = [
         formula_key="CAR_GROWTH_BASE",
         formula_name="Career Growth Base",
         formula_category="Timing Assessment",
         required_engines=["NatalPromiseEngine", "AshtakavargaEngine", "DashaEngine"],
         required_signals=["10th_house", "10th_lord", "11th_house"],
         required_vargas=["D1", "D10"],
         required_confidence_layers=["10th_lord_d10_strength", "positive_dasha"],
-        future_gochara_required=True,
         answer_template_key="timing_assessment_v1"
     ),
@@ -63,9 +61,8 @@ SEED_FORMULAS = [
         formula_name="Job Change Timing",
         formula_category="Timing Assessment",
         parent_formula_key="CAR_GROWTH_BASE",
-        required_engines=["TransitEngine"],
         required_signals=["5th_house", "9th_house"],
-        required_confidence_layers=["dasha_lords_connect_5th_9th", "transit_saturn_jupiter_activate_10th"],
+        required_confidence_layers=["dasha_lords_connect_5th_9th"],
         answer_template_key="timing_assessment_v1"
     ),
@@ -108,10 +105,9 @@ SEED_FORMULAS = [
         formula_key="HLT_LONGEVITY_BASE",
         formula_name="Longevity Assessment Base",
         formula_category="Multi-factor Assessment",
-        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
+        required_engines=["NatalPromiseEngine", "DashaEngine"],
         required_signals=["lagna", "8th_house", "8th_lord", "saturn"],
         required_confidence_layers=[],
-        future_gochara_required=False,
         answer_template_key="multifactor_assessment_v1"
     ),
@@ -126,10 +122,9 @@ SEED_FORMULAS = [
         formula_key="HLT_VITALITY_BASE",
         formula_name="Health and Vitality Base",
         formula_category="Strength Assessment",
-        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
+        required_engines=["NatalPromiseEngine", "DashaEngine"],
         required_signals=["lagna", "lagna_lord", "sun", "moon", "6th_house", "6th_lord", "8th_house", "12th_house"],
         required_confidence_layers=[],
-        future_gochara_required=False,
         answer_template_key="strength_assessment_v1"
     ),
@@ -153,9 +148,8 @@ SEED_FORMULAS = [
         formula_name="Recovery Timing",
         formula_category="Timing Assessment",
         parent_formula_key="HLT_VITALITY_BASE",
-        required_confidence_layers=["transit_jupiter_aspect_lagna", "positive_dasha"],
-        future_gochara_required=True,
+        required_confidence_layers=["positive_dasha"],
         answer_template_key="timing_assessment_v1"
     ),
@@ -175,10 +169,9 @@ SEED_FORMULAS = [
         formula_key="AST_PROPERTY_BASE",
         formula_name="Property Asset Base",
         formula_category="Multi-factor Assessment",
-        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
+        required_engines=["NatalPromiseEngine", "DashaEngine"],
         required_signals=["4th_house", "4th_lord", "mars", "jupiter", "2nd_house", "11th_house"],
         required_confidence_layers=[],
-        future_gochara_required=False,
         answer_template_key="multifactor_assessment_v1"
     ),
@@ -194,9 +187,8 @@ SEED_FORMULAS = [
         formula_name="Property Purchase Timing",
         formula_category="Timing Assessment",
         parent_formula_key="AST_PROPERTY_BASE",
-        required_confidence_layers=["dasha_activates_4th", "2nd_11th_lord_activation", "transit_jupiter_saturn_activate_4th"],
-        future_gochara_required=True,
+        required_confidence_layers=["dasha_activates_4th", "2nd_11th_lord_activation"],
         answer_template_key="timing_assessment_v1"
     ),
@@ -250,8 +242,7 @@ SEED_FORMULAS = [
         formula_category="Timing Assessment",
         parent_formula_key="EDU_ACADEMIC_BASE",
         required_signals=["6th_house"],
         required_confidence_layers=["dasha_activates_5th_6th"],
-        future_gochara_required=True,
         answer_template_key="timing_assessment_v1"
     ),
@@ -262,10 +253,9 @@ SEED_FORMULAS = [
         formula_key="FAM_PROGENY_BASE",
         formula_name="Progeny and Children Base",
         formula_category="Multi-factor Assessment",
-        required_engines=["NatalPromiseEngine", "DashaEngine", "TransitEngine"],
+        required_engines=["NatalPromiseEngine", "DashaEngine"],
         required_signals=["5th_house", "5th_lord", "9th_house", "jupiter"],
         required_confidence_layers=[],
-        future_gochara_required=False,
         answer_template_key="multifactor_assessment_v1"
     ),
@@ -281,9 +271,8 @@ SEED_FORMULAS = [
         formula_name="Childbirth Timing",
         formula_category="Timing Assessment",
         parent_formula_key="FAM_PROGENY_BASE",
-        required_confidence_layers=["dasha_activates_5th_9th", "transit_jupiter_aspect_5th_9th"],
-        future_gochara_required=True,
+        required_confidence_layers=["dasha_activates_5th_9th"],
         answer_template_key="timing_assessment_v1"
     ),
```

### `evaluator.py`
```diff
@@ -74,9 +74,6 @@ class FormulaEvaluator:
             
-            # Simulated boolean mapping: if degradation impacts the layer, mark False
-            if "transit" in layer.lower() and any("TransitEngine" in w for w in system_warnings):
-                is_fulfilled = False
             if "dasha" in layer.lower() and any("DashaEngine" in w for w in system_warnings):
                 is_fulfilled = False
```

### `question_registry.json`
*(Note: Excerpted. The script set `future_gochara_required` to `false` for every single entry in the file.)*
```diff
@@ -188,7 +188,7 @@
     "question_name": "Marriage Timing",
     "formula_key": "MAR_TIMING_BASE",
     "timing_required": true,
-    "future_gochara_required": true
+    "future_gochara_required": false
   },
   {
     "question_id": "10.1",
@@ -258,7 +258,7 @@
     "question_name": "Career Growth Timing",
     "formula_key": "CAR_GROWTH_BASE",
     "timing_required": true,
-    "future_gochara_required": true
+    "future_gochara_required": false
   },
```
