---
archive_title: "PROJECT STATE SNAPSHOT"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\handovers"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PROJECT STATE SNAPSHOT

**SNAPSHOT DATE:** 2026-06-20
**SNAPSHOT TIME:** 22:30 IST

## Git Status
*   Branch: main
*   Working Tree: Clean
*   Latest Activity: Removed Transit Engine dependencies across test suite and evaluator.

## Completed Domains
1. Marriage
2. Career
3. Wealth
4. Health
5. Property
6. Education
7. Children
8. Litigation
9. Travel
10. Spirituality
11. Relationships

## Completed Formula Families
11 Base Families, 33 Variants. (44 Total).

## Current Coverage
~5% of targeted 500 Canonical Questions mapped to 44 Base/Variant schemas via `question_registry.json`.

## Architecture Freeze State
*   `NatalPromiseEngine`: FROZEN
*   `DashaEngine`: FROZEN
*   `FormulaEvaluator`: FROZEN
*   `QuestionRouter`: FROZEN
*   `FormulaRepositoryLoader`: FROZEN

## Governance Freeze State
*   `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1`
*   `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD`

## Known Open Questions
*   How should the LLM `AnswerComposer` reconcile a highly favorable Dasha with a highly negative Mandali transit overlay without hallucinating math?

## Next Recommended Phase
**Phase 15**: Implementation of the standalone `MandaliEngine` overlay.
