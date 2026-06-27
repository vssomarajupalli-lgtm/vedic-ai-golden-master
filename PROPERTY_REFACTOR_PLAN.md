# PROPERTY REFACTOR PLAN

## 1. Current Model vs Identified Weakness
- **Current Model:** `AST_PROPERTY_BASE` evaluates the 4th House, 4th Lord, and Mars.
- **Weakness:** It identifies the physical asset (Mars/4th) but ignores the financial capacity required to execute a real estate transaction. Jupiter (Dhanakaraka), 2nd House (Savings), and 11th House (Gains) are entirely excluded. Furthermore, mapping Vehicle questions to Mars is incorrect.

## 2. Proposed Adjustments
- **Proposed Signals to Add:** `jupiter`, `2nd_house`, `11th_house`, `venus`.
- **Proposed Houses:** 2nd, 4th, 11th.
- **Proposed Karakas:** Mars (Land), Jupiter (Wealth), Venus (Vehicles/Luxury).

## 3. Structural Impact

### Formula Family Impact
1. **Modify Existing Base:** `AST_PROPERTY_BASE`
   - Add Signals: `jupiter`, `2nd_house`, `11th_house`.
2. **Future Base Placeholder:** `AST_VEHICLE_BASE` (to safely isolate Venus-based vehicle questions in the future).

### Variant Impact
1. **`AST_PROP_TIMING`:** Add `2nd_11th_lord_activation` to the required confidence layers. This enforces the rule that the 4th house activation must coincide with a period of financial capacity.

### Question Mapping Impact
- **No remapping required** for existing Property QIDs (4.1 through 4.6). They will inherently absorb the stronger financial logic.

### Backward Compatibility Impact
- Zero impact. The `FormulaEvaluator` safely expands array evaluation without breaking logic constraints.
