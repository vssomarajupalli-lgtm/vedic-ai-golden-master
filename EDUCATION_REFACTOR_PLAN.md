# EDUCATION REFACTOR PLAN

## 1. Current Model vs Identified Weakness
- **Current Model:** `EDU_ACADEMIC_BASE` evaluates 4th, 5th, 9th Houses, Mercury, and Jupiter.
- **Weakness:** The Moon (mental focus) is absent, ignoring the psychological capacity to study. Rahu (technical/foreign studies) is absent, ignoring modern educational paradigms. Foreign Education (12th/Rahu) and Higher Education (9th/Jupiter) are converged into a single variant, which conflates two entirely different astrological mechanisms.

## 2. Proposed Adjustments
- **Proposed Signals to Add:** `moon`, `rahu`, `12th_house`.
- **Proposed Houses:** 4th, 5th, 9th, 12th.
- **Proposed Karakas:** Mercury (Logic), Jupiter (Wisdom), Moon (Focus), Rahu (Foreign/Tech).

## 3. Structural Impact

### Formula Family Impact
1. **Modify Existing Base:** `EDU_ACADEMIC_BASE`
   - Add Signals: `moon`, `rahu`, `12th_house`.

### Variant Impact
1. **Split Variant:** `EDU_HIGHER_EDUCATION`
   - **`EDU_HIGHER_ACADEMICS`:** Focuses on `9th_house_strength` and `jupiter_dignity`.
   - **`EDU_FOREIGN_STUDY`:** Focuses on `12th_house_activation`, `9th_house_activation`, and `rahu_dignity`.

### Question Mapping Impact
- **QID 5.3** ("Will I pursue higher education?") stays on `EDU_HIGHER_ACADEMICS`.
- **QID 5.4** ("Will I go abroad for studies?") must be remapped to the new `EDU_FOREIGN_STUDY` variant.

### Backward Compatibility Impact
- Zero impact. Data-layer remapping is fully supported by the Question Router.
