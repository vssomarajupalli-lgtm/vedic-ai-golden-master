---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 09_PENDING_WORK

Priority ordered roadmap for upcoming development cycles.

## P1 Formula Validation Audit
* **Objective:** Fix the 88 failing unit tests across the broader suite.
* **Files Impacted:** `backend/tests/*`
* **Dependencies:** None.
* **Risks:** Test logic might accidentally test against deprecated concepts rather than the new Four Pillar matrix.
* **Expected Outcome:** 100% test pass rate ensuring pipeline stability.

## P2 D9 Extraction Integration
* **Objective:** Extract Navamsha (D9) chart data from PDFs and map it into the canonical JSON structure.
* **Files Impacted:** `backend/app/parsers/*`, `backend/app/normalizers/*`
* **Dependencies:** Understanding of PDF structure for D9 tables.
* **Risks:** PDF format variations could lead to extraction misses.
* **Expected Outcome:** `NatalPromiseEngine` automatically substitutes the `50` fallback with authentic D9 Varga dignity scores.

## P3 D10 Extraction Integration
* **Objective:** Extract Dashamsha (D10) chart data for career validation.
* **Files Impacted:** Same as P2.
* **Dependencies:** P2
* **Risks:** Same as P2.
* **Expected Outcome:** Accurate Varga scoring for the Career domain.

## P4 House Yoga Implementation
* **Objective:** Implement the Phase 3 Yoga Engine to replace the `50` fallback in the House Strength calculation.
* **Files Impacted:** `backend/app/engines/house_strength_engine.py`, `backend/app/engines/yoga_engine.py` (future)
* **Dependencies:** Yoga engine mapping definitions.
* **Risks:** Double counting yoga strength if not carefully bound.
* **Expected Outcome:** House scores accurately reflect special yogas (e.g. Mahapurusha).

## P5 Occupant Scaling Review
* **Objective:** Review edge cases where extreme numbers of occupants (e.g. 4+ malefics) skew the `[0, 100]` bound.
* **Files Impacted:** `backend/app/engines/house_strength_engine.py`
* **Dependencies:** None.
* **Risks:** Overly harsh bounding might flatten important astrological severity.
* **Expected Outcome:** Verified and potentially curved occupant scaling.

## P6 Malefic Aspect Scaling Review
* **Objective:** Similar to P5, review the inverted subtraction logic for malefic aspects.
* **Files Impacted:** `backend/app/engines/house_strength_engine.py`
* **Dependencies:** None.
* **Risks:** Same as P5.
* **Expected Outcome:** Verified scaling logic.

## P7 Additional Varga Integration
* **Objective:** Expand parsing to cover D2, D4, D7, D20, and D24.
* **Files Impacted:** `backend/app/parsers/*`
* **Dependencies:** P2
* **Risks:** PDF parsing complexity.
* **Expected Outcome:** Every major life domain utilizes authentic Varga validation.

## P8 Real Case Validation Expansion
* **Objective:** Test the new architecture against new real-world natal charts beyond CASE_001 (Raju).
* **Files Impacted:** `extracted_json/*`
* **Dependencies:** New canonical JSONs.
* **Risks:** New cases might expose gaps in dignity mappings or standard assumptions.
* **Expected Outcome:** Increased confidence in generalized architectural stability.
