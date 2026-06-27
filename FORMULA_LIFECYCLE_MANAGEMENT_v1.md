# FORMULA LIFECYCLE MANAGEMENT v1

## 1. Overview
This document outlines the strict administrative workflow for proposing, reviewing, approving, and modifying formulas within the Vedic AI System. The lifecycle ensures that mathematical consistency is preserved across updates and that deprecated logic does not break existing application behavior.

## 2. Formula Review Process
All new Formula Families and Variants must proceed through a strict 4-step lifecycle:

1. **Proposal:** An engineer or astrologer submits a JSON schema draft for a new formula. The proposal must include a written justification detailing why existing variants cannot satisfy the requirement (enforcing the strict reuse mandate).
2. **Review:** The Governance Team audits the formula against the Rule of Dumb Evaluation: verifying that the formula introduces no hidden scoring, no custom math, and requests only valid, deterministic signals.
3. **Approval:** Once mathematically verified, the formula is approved and merged into the Formula Repository schema.
4. **Registry Assignment:** The `QuestionRegistry` is updated to map the appropriate natural language `question_id` inputs to the newly approved `formula_key`.

## 3. Formula Change Control

### 3.1 Versioning
When a formula requires a modification (e.g., adding a new confidence layer to increase accuracy), it MUST be versioned forward if the change fundamentally alters past behavior.
- **Example:** `MAR_TIMING_001` becomes `MAR_TIMING_002`.
- The `QuestionRegistry` is updated so that all incoming queries map to the new `002` version.

### 3.2 Deprecation & Backward Compatibility
To protect historical evaluation records, generated PDFs, and saved user dashboard states, formulas are **never deleted**.
- **Deprecation Workflow:** Old formulas (e.g., `MAR_TIMING_001`) remain in the codebase indefinitely. They are simply unmapped from active `QuestionID` routes.
- **Backward Compatibility:** If a user re-loads a historically saved reading that explicitly references `MAR_TIMING_001`, the system can still process the exact same payload through the exact same logic, ensuring absolute backward compatibility and data integrity.

## 4. Maintenance Audits
To prevent registry decay, automated tests will periodically scan the Formula Repository:
- Identifying orphaned formulas (formulas with zero active `QuestionID` mappings).
- Flagging duplicate configurations (variants whose `required_confidence_layers` perfectly match another variant).
