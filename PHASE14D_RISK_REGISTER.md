# PHASE 14D: RISK REGISTER

## 1. Formula Explosion Risk
**Description:** Engineers or Astrologers bypass the Many-to-One convergence rule, creating a unique Formula Variant for every new Question ID introduced.
**Severity:** HIGH
**Mitigation:** The Formula Lifecycle Governance mandates a formal proposal process. Any new Variant proposal must explicitly prove that existing variants cannot handle the mathematical logic before it is approved.

## 2. Governance Drift Risk
**Description:** As new domains are added (e.g., Spirituality, Travel), developers attempt to introduce dynamic scoring or weighted variables inside the JSON formulas to capture nuance.
**Severity:** CRITICAL
**Mitigation:** The Phase 13C Boolean Gate remains completely locked. The Evaluator schema natively rejects any weighted values, ensuring formulas remain deterministic.

## 3. Maintenance Risk
**Description:** An astrological correction is needed (e.g., modifying how Ashtakavarga bindus are thresholded), requiring developers to hunt down and update 60 different Formula Variants.
**Severity:** MEDIUM
**Mitigation:** The Base/Inheritance model ensures that the Ashtakavarga threshold is defined exactly once in the Base Family. Child variants automatically inherit the fix, drastically reducing maintenance overhead.

## 4. Inheritance Conflict Risk
**Description:** A Child Variant accidentally overrides a critical safety check established by the Base Family (e.g., stripping out the TransitEngine requirement for a timing question).
**Severity:** MEDIUM
**Mitigation:** The Answer Composer architecture explicitly prevents LLM hallucination in the event of missing data. If an engine is accidentally stripped, the pipeline naturally degrades to a `MIXED` final state with system warnings, preventing catastrophic false predictions.

## 5. Variant Ambiguity Risk
**Description:** The difference between `CAR_GROWTH_VARIANT` and `CAR_PROMOTION_VARIANT` becomes ambiguous, leading Question Routers to map Question IDs inconsistently.
**Severity:** LOW
**Mitigation:** The Formula Repository must maintain exhaustive documentation within the JSON `description` fields for every variant, explicitly defining the mathematical boundary between similar variants.
