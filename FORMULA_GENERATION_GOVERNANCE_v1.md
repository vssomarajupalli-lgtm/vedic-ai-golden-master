# FORMULA GENERATION GOVERNANCE v1

## 1. Overview
This document establishes the strict governance rules controlling the creation and expansion of the Formula Library. Its primary objective is to prevent formula explosion, ensure absolute mathematical determinism, and maintain alignment with the Phase 14A Architecture (Formula Family + Inheritance Model).

## 2. Formula Family Governance
A **Formula Family** acts as the foundational baseline for a specific domain inquiry (e.g., `MAR_TIMING_BASE`).

- **Creation Rule:** A new Formula Family may ONLY be created when the root astrological target (the core primary houses and karakas) changes. For example, moving from "Marriage Timing" (7th house) to "Career Timing" (10th house) justifies a new Family.
- **Reuse Mandate:** If a new Question ID targets the exact same domain and astrological parameters as an existing Family, a new Family MUST NOT be created. 
- **Inheritance Mandate:** All subsequent variations of a Family must inherit from the Base to ensure global fixes cascade successfully.

## 3. Formula Variant Governance
A **Formula Variant** is a child formula that inherits from a Family Base but adds or overrides specific layers (e.g., `MAR_TIMING_DELAY`).

- **Creation Rule:** A Variant may ONLY be created if the *mathematical evaluation logic* (the `required_confidence_layers` or `required_signals`) fundamentally differs from the Base. 
- **Justifiable Differences:** Adding a rule to check for Saturn's aspect on the 7th house (delay) justifies a Variant.
- **Unjustifiable Differences:** A change in linguistic tone (e.g., "Will I marry late?" vs "At what age will I tie the knot?") DOES NOT justify a new Variant. Both must map to the same Variant. Semantic variations are strictly the domain of the Answer Composer templates.

## 4. Question Mapping Governance
The `QuestionRegistry` connects natural language queries to Formula Variants.

- **Many-to-One Mapping:** Multiple `question_id` inputs must aggressively map to the same Formula Variant whenever the astrological math is identical.
- **Duplicate Prevention:** The `QuestionRegistryLoader` enforces uniqueness on `question_id` and actively tracks formula reuse to prevent duplicate mappings.

## 5. Template Governance
Templates govern the linguistic boundaries applied by the Answer Composer.

- **Creation Rule:** A new template (`.txt` file) is justified ONLY when the fundamental structure of the narrative must change (e.g., shifting from a `timing_assessment` format to a `strength_assessment` format).
- **Reuse Mandate:** Templates must remain generic (e.g., `favorable`, `mixed`, `unfavorable`) and be reused across hundreds of formulas. 
- **Proliferation Control:** Creating specific templates for individual formulas (e.g., `marriage_delay_favorable.txt`) is strictly forbidden.

## 6. Canonical Evidence Governance
All generated Formulas must comply with the **"Evaluate Once, Consume Many"** principle.
- Formulas must output standard `FormulaEvaluationResult` payloads.
- Formulas must never embed logic meant exclusively for the LLM. The extracted evidence must be perfectly compatible with the Canonical JSON Export, Future Astrologer PDFs, and UI Strength Dashboards. No downstream system is permitted to recalculate astrology.

## 7. Future Mandali Compatibility
All new Formulas must be evaluated for compatibility with future Moon-centered Mandali overlays.
- A formula must not contain logic that hard-blocks dynamic Gochara.
- Timeline-based formulas must support the `future_gochara_required` flag, ensuring that when the Mandali engine is activated, transit data can seamlessly integrate as additional boolean confidence layers without requiring an architectural rewrite.
