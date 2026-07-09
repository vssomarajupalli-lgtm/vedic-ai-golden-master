# HEALTH REFACTOR PLAN

## 1. Current Model vs Identified Weakness
- **Current Model:** `HLT_VITALITY_BASE` evaluates Lagna, Lagna Lord, Sun, 6th House, 6th Lord.
- **Weakness:** The Moon (mental health/fluids) is missing. The 8th House (chronic illness) and 12th House (hospitalization) are missing. Most critically, Longevity (8th house/Saturn) is mathematically merged with General Vitality (Lagna/Sun), which violates classical Ayurdaya calculations.

## 2. Proposed Adjustments
- **Proposed Signals to Add:** `moon`, `saturn`, `8th_house`, `8th_lord`, `12th_house`, `12th_lord`.
- **Proposed Houses:** 1st, 6th, 8th, 12th.
- **Proposed Karakas:** Sun (Vitality), Moon (Mind/Fluids), Saturn (Longevity).

## 3. Structural Impact

### Formula Family Impact
1. **Create New Base:** `HLT_LONGEVITY_BASE` 
   - Signals: `lagna`, `8th_house`, `8th_lord`, `saturn`.
2. **Modify Existing Base:** `HLT_VITALITY_BASE`
   - Add Signals: `moon`, `8th_house`, `12th_house`.

### Variant Impact
1. **`HLT_ILLNESS_RISK`:** Add `8th_lord_activation` and `12th_house_activation` to distinguish between acute disease, chronic disease, and hospitalization.
2. **`HLT_LONGEVITY_ASSESSMENT` (New Variant):** Inherits from `HLT_LONGEVITY_BASE`. Evaluates `8th_house_strength` and `saturn_dignity`.

### Question Mapping Impact
- **QID 6.2** ("Will I have a long life?") must be remapped from `HLT_GENERAL_VITALITY` to the new `HLT_LONGEVITY_ASSESSMENT` variant.

### Backward Compatibility Impact
- Zero impact. No user queries have been processed in production, and no pipelines break from schema expansion.
