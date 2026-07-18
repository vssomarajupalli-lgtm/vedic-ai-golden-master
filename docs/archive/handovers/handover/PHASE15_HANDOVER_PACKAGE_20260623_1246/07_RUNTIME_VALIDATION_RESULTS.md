---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable

# Archive Governance Metadata
archive_title: "07_RUNTIME_VALIDATION_RESULTS"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive/handovers/handover"
archive_reason: "Historical phase handover package; superseded by current project status"
original_version: "2026-06-23"
replacement_document: "Not specified (see docs/status/ for current project status)
---

# 07_RUNTIME_VALIDATION_RESULTS

## Latest Validated Runtime Outputs (CASE_001: Raju)

### Marriage
* **Score:** 49
* **Observation:** Removing the double penalty of Saturn in 7th accurately stabilized the score from an unrealistic ~20 to a realistic 49, reflecting the native's actual married status despite challenging combinations.

### Career
* **Score:** 57
* **Observation:** Correctly evaluates the 10th house environment, factoring the natural dignity of its lord.

### Wealth
* **Score:** 61
* **Observation:** Strong SAV points in the 11th house and supporting factors lead to a solid, above-average wealth promise.

### Property
* **Score:** 48
* **Observation:** Factors 4th house conditions, avoiding double penalties for afflicted lord placement.

### Health
* **Score:** 39
* **Observation:** Health naturally inverts support logic for dusthanas (6, 8, 12). The score accurately reflects known health struggles.

## Known Limitations
* **D9 Fallback Behavior:** Currently, because Varga (D9) data extraction is pending in the parsing layer, the `NatalPromiseEngine` assigns a neutral fallback score of `50`. This safely contributes 7.5 points `(50 * 0.15)` to every domain.
* **House Yoga Placeholder:** House-specific yogas currently default to a neutral `50`. Deep yoga identification is deferred to Phase 3.
* **Scaling Models:** Occupant and Malefic Aspect scaling currently utilize linear and inverted mathematical bounds which are functioning well but remain open for future edge-case review.
