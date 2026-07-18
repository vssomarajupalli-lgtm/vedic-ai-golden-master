---
archive_title: "CURRENT FORMULA LIBRARY STATUS"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# CURRENT FORMULA LIBRARY STATUS

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## Status Overview
*   **Base Families:** 11
*   **Variants:** 33
*   **Total Schemas:** 44
*   **Domains Covered:** 11
*   **Mapped Questions:** 20+ (Ongoing expansion)
*   **Registry Coverage:** ~5% of 500 canonical questions

## Expansion History
*   **Phase 14E:** Marriage (`MAR_`), Career (`CAR_`), Wealth (`WEA_`) implemented as proof of concept for the base/variant inheritance model.
*   **Phase 14F:** Health (`HLT_`), Property (`AST_`), Education (`EDU_`) implemented following Parashari strictness audits.
*   **Phase 14G:** Progeny (`FAM_`), Litigation (`LIT_`), Travel (`TRV_`), Spirituality (`SPR_`), Relationships (`REL_`) finalized and hardened.
*   **Phase 15 Prep:** Decoupled all transit parameters from the entire library.

## Future Expansion Strategy
The Formula Library is architecturally complete. No new python architectural models are required. 
Future expansion simply requires adding new mapping entries into `question_registry.json` and appending new `FormulaSchema` definitions into `registry_data.py` utilizing the exact same established pattern.
