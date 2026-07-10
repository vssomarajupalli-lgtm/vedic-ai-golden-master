# Phase 16 Architecture Revision Review

```text
Created : 2026-06-25
Time    : 10:25 AM IST
Phase   : Phase 16A
Type    : Architecture Review
Status  : PERMANENT RECORD
```

## Executive Summary

*Cross-References:*
- Preceded by: [Phase 16A.1 Mathematical Calibration Audit](file:///d:/vedic-ai-system/docs/governance/audits/phase_16a1_mathematical_calibration_audit.md)
- Followed by: [Phase 16A Architecture Freeze Audit](file:///d:/vedic-ai-system/docs/governance/audits/phase_16a_architecture_freeze_audit.md)

The proposed Phase 16 Architecture Revision provides an exceptionally strong foundation for the future of the Vedic-AI engine. By explicitly separating mathematical formulas (logic) from calibration values (weights/thresholds), the system will achieve true flexibility without sacrificing deterministic stability.

The roadmap and governance rules are structurally sound. However, this architectural review has identified a few critical risks—primarily regarding **Dependency Injection** for the Calibration Layer and a hidden **Double Counting** overlap between the House and Rasi engines.

---

## 1. Centralized Calibration Layer (Phase 16A.3)

**Feedback:** Fully aligned. Moving configurable values into a centralized `calibration/` structure is necessary.

**Architectural Improvement (Dependency Injection):**
Instead of having engines globally `import` calibration constants (e.g., `from app.calibration.weights import PLANET_MATRIX`), the architecture should define a `CalibrationProfile` object. 

*   **Why?** If values are hard-imported, A/B testing or switching calibration profiles requires code changes or server restarts.
*   **Solution:** The PipelineRunner or a `CalibrationManager` should load a `CalibrationProfile` (e.g., from a JSON/YAML file or DB) and inject it into the engines during `evaluate()`. This guarantees that "tuning" is truly decoupled from the codebase, allowing future reports to load the newest `calibration_v2.yaml` effortlessly.

## 2. Single Source of Mathematical Truth

**Feedback:** Fully aligned.

**Risk Identified (Stubs and Fallbacks):**
Currently, there are hardcoded "neutral" fallbacks scattered across engines (e.g., `50.0` for missing Varga data in Planet Engine, `_STUB_SCORE = 50.0` in Master Probability). These neutral anchors *must* also be migrated to the Calibration Layer. A neutral baseline is a mathematical decision and subject to future tuning.

## 3. No Backward Mathematical Compatibility Required

**Feedback:** Fully aligned. 

**Architectural Confirmation:** Since the engine relies on the Pipeline to generate the final JSON payload dynamically at runtime, as long as historical reports are stored statically (e.g., as saved PDFs or JSON snapshots in the database) and never re-evaluated by the backend, backward compatibility is naturally preserved.

## 4. Single Producer & No Double Counting Rule

**Feedback:** The definitions for Bhavadhipati and Karaka strength perfectly satisfy the Single Producer principle.

**Critical Risk Identified (House vs. Rasi Double Counting):**
Because Vedic astrology often uses Whole Sign Houses, a House (Bhava) and a Sign (Rasi) share the exact same physical space in the chart. 
*   **Current State:** The `HouseStrengthEngine` currently evaluates Occupants and Aspects. The `RasiStrengthEngine` *also* evaluates Occupants and Aspects. 
*   **The Conflict:** The `MasterProbabilityEngine` weights House (10%) and Rasi (10%). This means the presence of a malefic in Aries (if Aries is the 1st House) applies a penalty twice in the master pipeline.
*   **Architectural Improvement:** Before or during Phase 16B (Calibration), we must strictly separate their purviews.
    *   *Rasi Engine* should own environmental factors: Sign Lord strength, SAV Bindus, and inherent dignity of the sign.
    *   *House Engine* should own spatial factors: Aspects, directional strength (Dig Bala impacts), and House-specific Yogas.
    *   *Occupants* should belong exclusively to one of the two to prevent double penalization.

## 5. Permanent Immutable Governance

**Feedback:** Fully aligned. The reinforcement of the "Vargas refine but never overwrite D1" rule specifically addresses the primary violation caught in the Phase 15 Final Regression Audit.

## 6. Revised Roadmap Analysis

The roadmap flow is logical and reduces risk by isolating architecture updates (16A.3) from actual mathematical tuning (16B).

*   **Phase 16A.2 (Varga Architecture Review):** Essential, as currently only D9 and D10 are wired, but Natal Promise expects up to 13 different Vargas.
*   **Phase 16H (Moon-Centered Mandali Gochara):** This constraint is vital. Calculating transits from the Natal Moon Pada ensures we avoid heavy ephemeris calculations and strictly rely on the Canonical JSON, adhering to the Zero Astrological Recalculation rule.

---

## Conclusion

The architecture proposal is **APPROVED** with the following recommendations for Phase 16A.3:
1.  Implement a **Dependency Injected Calibration Profile** rather than static Python imports.
2.  Extract all hardcoded **fallback/stub values** (e.g., `50.0`) into the Calibration Layer.
3.  Prepare to resolve the **House vs. Rasi double-counting** overlap during calibration.
