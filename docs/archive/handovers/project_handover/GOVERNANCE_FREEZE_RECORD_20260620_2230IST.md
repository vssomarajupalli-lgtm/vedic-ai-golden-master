---
archive_title: "GOVERNANCE FREEZE RECORD"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# GOVERNANCE FREEZE RECORD

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## ASTROLOGICAL_PREDICTION_GOVERNANCE_v1

1.  **Core Principle:** An event can only occur if the natal chart contains the promise. Neither Dasha nor Transit can create an event that is absent from the natal promise.
2.  **Promise Engine Layer:** Must assess Bhava Strength, Lord Strength, Karakas, Yogas, Vargas, Functional Nature, and Afflictions.
3.  **Dasha Engine Layer:** Identifies activation periods. It does not guarantee manifestation.
4.  **Reporting Structure:** All predictions must strictly report A. Promise Assessment, B. Dasha Activation, C. Final Conclusion. D. Optional Mandali Commentary.

## PHASE15_MANDALI_DECOUPLING_DECISION_RECORD

1.  **Mandali Exclusion:** Mandali is strictly banned from `FormulaEvaluator` logic.
2.  **Probability Protection:** Mandali shall never override, modify, increase, decrease, or recalculate any Question Engine probability.
3.  **Future Timing Generation:** Future LLM modules may consume Mandali to narrate the nuances of an active Dasha window, but the mathematical gate remains purely Dasha-driven.

## Mandatory Rules
*   Formulas must always inherit from a recognized Base Family.
*   The `TransitEngine` is forever banned from `required_engines` in `registry_data.py`.
*   All tests must mock `DashaEngine`, never `TransitEngine`.

## Forbidden Actions
*   Future developers are **FORBIDDEN** from combining Promise Score, Dasha Score, and Mandali Score into a single weighted mathematical model. 
*   Future developers are **FORBIDDEN** from inserting `future_gochara_required` back into the `FormulaSchema`.
