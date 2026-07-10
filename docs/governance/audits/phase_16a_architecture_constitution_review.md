# Phase 16A – Architecture Constitution Review

```text
Created : 2026-06-25
Time    : 10:25 AM IST
Phase   : Phase 16A
Type    : Constitution Review
Status  : PERMANENT RECORD
```

## Executive Summary

*Cross-References:*
- Preceded by: [Phase 16A Architecture Freeze Audit](file:///d:/vedic-ai-system/docs/governance/audits/phase_16a_architecture_freeze_audit.md)
- Followed by: [Phase 16A Final Constitution Review](file:///d:/vedic-ai-system/docs/governance/audits/phase_16a_final_constitution_review.md)

This document serves as the formal architectural confirmation of the **Phase 16A Architecture Constitution (Final Revision)**. The proposed constitution establishes an ironclad framework that permanently isolates mathematical logic from configurable values, guaranteeing that future calibrations will be deterministic, safe, and free from cross-engine contamination. 

The architecture is **APPROVED** and is ready to govern all subsequent Phase 16 development.

---

## Deliverable Confirmations

### 1. Ownership Matrix
**Confirmed.** The assignment of every astrological concept to exactly one permanent owner is logically sound. By isolating concepts like Bhavadhipati Strength and Karaka Strength purely to the `PlanetStrengthEngine`, we eliminate the risk of shadow calculations creeping into the pipeline.

### 2. Formula Ownership Register
**Confirmed.** Enforcing a 1-to-1 relationship between mathematical formulas and specific engines strictly adheres to the Single Producer Principle. `MasterProbabilityEngine` owns the aggregation; it must never own the core formula of its dependencies.

### 3. Calibration Architecture
**Confirmed.** A single `CalibrationManager` loading one active profile is the optimal solution. It satisfies the requirement that future reports use the newest mathematics seamlessly while preventing the massive technical debt associated with managing multiple parallel runtime profiles. All configurable arrays, dictionaries, thresholds, and percentage weights natively belong here.

### 4. House vs Rasi Separation
**Confirmed.** The absolute boundary established—House owns spatial/ray factors (Occupants, Aspects, Activation, Classification) while Rasi owns environmental/zodiacal factors (Sign Environment, Lord Quality, SAV)—is the definitive cure for the Double Counting violation identified in the previous audit. This rule mathematically guarantees that a malefic in Aries will only be penalized once.

### 5. Varga Governance
**Confirmed.** The rule that Varga NEVER overwrites D1 is critical. Treating Varga strictly as a refinement layer that outputs modifiers (or independent refinement scores) preserves D1 Immutability. The `NatalPromiseEngine` consuming (Planet Strength + Varga Refinement) is the correct architectural pattern.

### 6. Dasha Ownership
**Audit Finding:** Currently, the `DashaEngine` computes timeline aggregations (using a 50/30/20 ratio for MD/AD/PD), but the `MasterProbabilityEngine` actively recalculates the MD/AD ratio using a 60/40 split. 
**Resolution:** Per the Constitution, `DashaEngine` must be the sole owner of the Dasha aggregation formula. During Phase 16B calibration, the `MasterProbabilityEngine` must be stripped of its 60/40 calculation and simply consume the final output produced by `DashaEngine`.

### 7. Hidden Risks
While the Constitution is rock-solid, the following risks must be carefully managed during Phase 16A.3 and 16B execution:
*   **Missing Hardcoded Stubs:** Neutral fallbacks (e.g., `50.0` or `4` bindus) are heavily embedded in the engines. Failing to migrate even one to the Calibration Layer will break the single-source-of-truth rule.
*   **Varga Overwrite Refactoring:** The `VargaEngine` currently overwrites the D1 score in code. Re-engineering this to output modifiers without breaking downstream consumers requires careful surgical precision in Phase 16B.
*   **Dasha Aggregation Leakage:** As noted in Deliverable 6, `MasterProbabilityEngine` must have its duplicate dasha calculation logic removed.

### 8. Final Recommendation
The Phase 16A Architecture Constitution is the definitive blueprint for the Vedic-AI engine. It resolves all architectural ambiguities and establishes a permanent foundation for continuous mathematical improvement.

**Recommendation:** Proceed immediately to **Phase 16A.3: Calibration Architecture**. Build the `CalibrationManager` and successfully migrate all values out of the engine files, strictly adhering to the "No mathematical changes" rule for this step.
