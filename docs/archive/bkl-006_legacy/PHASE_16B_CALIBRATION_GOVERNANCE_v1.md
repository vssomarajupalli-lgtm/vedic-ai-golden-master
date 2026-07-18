---
archive_title: "PHASE 16B.1 CALIBRATION GOVERNANCE CONSTITUTION"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# PHASE 16B.1 CALIBRATION GOVERNANCE CONSTITUTION

**Version:** 1.0
**Phase:** 16B.1
**Status:** FROZEN
**Architecture Baseline:** Phase 16A.3
**Calibration Baseline:** v1.0.0 (Base Legacy Parity)

---

## 1. Executive Summary

Phase 16B initiates the formal evidence-based tuning of the Vedic AI System. The objective of this phase is the **scientific calibration** of the system's accuracy. Phase 16A strictly locked and froze the core mathematical engine logic. Phase 16B does not redesign engines; rather, it exclusively manages the tuning of externalized constants housed in versioned calibration profiles. This document establishes the constitutional rules governing how and when calibration values may be adjusted to ensure all modifications are driven by verifiable statistical evidence.

---

## 2. Calibration Philosophy

The Calibration Governance operates under the following non-negotiable principles:

* **Deterministic engines are immutable.** No Python code governing mathematical logic may be altered.
* **Calibration profiles contain tunable values.** 100% of the mathematical adjustments must occur in external JSON profile files.
* **Calibration is evidence-driven.** Adjustments are based purely on statistically significant sample results.
* **No intuition-based tuning.** Ad-hoc weighting adjustments based on isolated "feelings" or astrological bias are banned.
* **No arbitrary weight changes.** A constant cannot be modified without accompanying statistical validation proving it produces superior historical accuracy.

---

## 3. Ground Truth Definition

All calibration requires a **Ground Truth**. A Ground Truth represents the absolute factual reality of a native's life against which the Vedic AI system's predictive accuracy is measured.

A valid Ground Truth entry must include:
* **Verified birth data:** Exact Date, Time, Location, Timezone, and DST status.
* **Verified life event:** The specific domain outcome (e.g., "Divorce", "Bankruptcy", "CEO Appointed").
* **Event date (when applicable):** The precise date or narrow timeframe the event occurred.
* **Supporting evidence:** Source of verification.
* **Confidence level:** High, Medium, Low.
* **Validation status:** Confirmed, Probable, Unverified.

**Important:** Only **Confirmed** cases may influence released calibration profiles.

---

## 4. Validation Dataset Requirements

To prevent overfitting to small samples, minimum dataset expectations are strictly enforced before any mathematical tuning is deemed statistically valid.

**Recommended Thresholds:**
* **Initial research dataset:** 50 verified charts.
* **Calibration dataset:** 100+ verified charts.
* **Mature release dataset:** 250+ verified charts.

**Domain Diversity:**
The dataset must require diversity across all core life domains. Validating success on a single domain does not justify a universal tuning change. Datasets should include cases related to:
* Marriage
* Career
* Children
* Health
* Finance
* Education
* Property
* Foreign Settlement
* Litigation
* Spirituality

---

## 5. Calibration Rules

The following strict boundaries govern calibration execution:

* **No calibration may be performed from a single horoscope.** Micro-optimizing for one native (e.g., the Raju Canonical Chart) breaks generalized accuracy.
* **No calibration may be justified using anecdotal evidence.** "Textbook" theories must be backed by real-world datasets.
* **Every calibration change must be supported by multiple validated cases.** 
* **Outliers must be documented separately.** Charts that drastically diverge from predictions must be categorized as outliers for specialized research, rather than forcing mathematical distortions across the baseline profile.

---

## 6. Statistical Methodology

All calibration must follow a rigorous, high-level scientific methodology:

**Prediction** 
↓ 
**Actual Outcome** (Compare Engine Output to Ground Truth)
↓ 
**Difference** (Calculate variance or error margin)
↓ 
**Error Analysis** (Identify the pattern causing the divergence)
↓ 
**Candidate Calibration** (Propose a profile adjustment)
↓ 
**Validation** (Run the entire dataset against the new profile)
↓ 
**Approval** (Verify that overall dataset accuracy improved)
↓ 
**New Calibration Profile** (Release the updated profile)

**Metrics:**
* **Error measurement:** The delta between the calculated probability score and the confirmed Ground Truth outcome.
* **Confidence:** The aggregate certainty of the dataset.
* **Repeatability:** Ensuring the model holds firm when subjected to holdout (untrained) data.
* **Acceptance thresholds:** A calibration is only accepted if the Net Accuracy of the entire dataset strictly improves without causing catastrophic regressions in previously solved charts.

---

## 7. Calibration Profile Versioning

All calibration values exist solely inside centralized JSON profiles, which undergo semantic versioning.

**Example Sequence:**
```
v1.0.0 (Base legacy parity)
↓
v1.1.0 (Minor tuning adjustment)
↓
v1.2.0 (Further refinement)
↓
v2.0.0 (Major dataset validation milestone)
```

**Versioning Rules:**
* **Existing profiles become immutable after release.**
* **Never edit historical profiles.** If an error is found in `v1.1.0`, it must be corrected in `v1.1.1` or `v1.2.0`.
* **New calibration creates a new version.**
* **Exactly one approved profile is active** at any given runtime.
* **Historical reports remain reproducible.** Any previous analysis can be perfectly regenerated by injecting the specific historical JSON profile version used at the time.

---

## 8. Calibration Approval Workflow

Before a new calibration profile version is released, the proposal must document:

* **Reason:** Why the change is needed.
* **Evidence:** The specific dataset/Ground Truth proving the error.
* **Affected constants:** Which exact values in the JSON are mutating.
* **Expected impact:** The anticipated shift in calculation behavior.
* **Validation cases:** The charts that will confirm the fix.
* **Statistical justification:** Proof that overall accuracy improved.
* **Rollback plan:** The version to fallback to in case of undetected regression.

**Approval Sequence:**
Research → Review → Validation → Approval → Release

---

## 9. Rollback Policy

In the event that a newly deployed calibration profile introduces unforeseen regressions or performs worse in broader production:

* **Deactivate the new profile** immediately.
* **Reactivate the previous approved profile** as the primary active runtime state.
* **Preserve both versions.** Do not delete the failed profile from the registry; mark it as deprecated for autopsy.
* **Never overwrite history.** The failed deployment remains a historical record.

---

## 10. Architecture Compliance

The Calibration Governance inherently reaffirms and protects the Phase 16A Architecture Constitution:

* ✓ **Canonical JSON unchanged:** Input payload schema is locked.
* ✓ **D1 Immutability:** No mutation of fundamental birth chart mathematics.
* ✓ **Four Pillar Promise Architecture:** Structure remains identical.
* ✓ **No Double Penalty Rule:** Enforced at the engine level.
* ✓ **Engine Isolation:** Kept intact; engines do not cross-talk.
* ✓ **Read-only CalibrationManager:** The JSON config is injected statelessly.
* ✓ **One Active Calibration Profile:** Guaranteed reproducibility.
* ✓ **Versioned Calibration Profiles:** Strict immutability for past versions.
* ✓ **Frozen Engine Contracts:** JSON payload shapes outputted by engines never change.
* ✓ **No runtime tuning:** Values are locked for the duration of the pipeline execution.

---

## 11. Success Criteria

Phase 16B.1 is officially complete when:
* Governance is permanently documented.
* Calibration workflow is frozen.
* Statistical methodology is defined.
* Profile versioning is frozen.
* Approval process is frozen.
* Rollback process is frozen.

Only once this constitution is fully acknowledged may the project advance to **Phase 16B.2 – Ground Truth Framework**.

---

## 12. Calibration Scope Governance

Calibration is strictly limited to **Category A Calibration Constants** identified during Phase 16A.3 (`CALIBRATION_CONSTANT_INVENTORY_v1.md`). Calibration may adjust only approved numerical values contained within versioned calibration profiles.

Calibration shall **never** modify or override any of the constitutional components listed in **Section 10 (Architecture Compliance)**.

Calibration proposals are explicitly prohibited from:
* inventing new astrological principles
* introducing hidden scoring modifiers
* bypassing deterministic calculations
* creating undocumented mathematical behaviour
* embedding calibration logic inside engine code
* modifying historical calibration profiles

If a proposed improvement cannot be achieved through approved Category A Calibration Constants, the proposal must be rejected or escalated as a separate architectural review rather than a calibration change.

**The Phase 16A.3 Calibration Constant Inventory (CALIBRATION_CONSTANT_INVENTORY_v1.md) remains the authoritative source defining which constants are eligible for calibration. Any proposal to introduce new calibration constants requires a separate architectural review and constitutional approval before implementation.**
