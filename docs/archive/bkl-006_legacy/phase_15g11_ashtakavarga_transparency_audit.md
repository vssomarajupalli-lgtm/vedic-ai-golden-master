---
archive_title: "Phase 15G.11: Ashtakavarga Transparency Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.11: Ashtakavarga Transparency Audit

## Executive Summary
This audit reviews the transparency readiness of the Ashtakavarga Engine (`AshtakavargaEngine`). The engine calculates both Bhinnashtakavarga (BAV - individual planet matrices) and Sarvashtakavarga (SAV - cumulative house totals). Currently, these matrices exist in the backend runtime but are largely invisible to the end user.

---

## 1. Exact Backend JSON Paths
The primary payload is housed under:
`breakdown.engine_outputs.ashtakavarga`

It contains six primary sub-objects:
1. `bav_charts`
2. `sav_chart`
3. `planet_bav_support`
4. `dasha_bav_support`
5. `sav_analytics`
6. `engine_modifiers`

---

## 2. Existing SAV/BAV Payload Structures

**SAV Chart Example (`sav_chart`):**
```json
"1": {
  "bindus": 28,
  "score": 50.0,
  "grade": "AVERAGE",
  "is_favorable": false,
  "is_strong": false,
  "is_weak": false
}
```

**BAV Charts Example (`bav_charts.sun`):**
```json
"1": {
  "bindus": 4,
  "grade": "AVERAGE"
},
"2": {
  "bindus": 5,
  "grade": "GOOD"
}
```

**SAV Analytics Example (`sav_analytics`):**
```json
"sav_analytics": {
  "total_bindus": 337,
  "average_per_house": 28.08,
  "peak_house": "11",
  "weakest_house": "12",
  "favorable_houses": ["11", "2", "9"],
  "unfavorable_houses": ["12", "6", "8"],
  "bav_consistency_check": true
}
```

---

## 3. What is Already Exposed
- The final **BAV Modifier** per planet is exposed inside `B. Planet Strength Breakdown` (e.g., `BAV Modifier: 0`).
- The final **SAV Score** per house is exposed inside `C. House Strength Breakdown` (e.g., `SAV: 50.0`).

---

## 4. What is Hidden
- The **BAV Matrices**: The 7x12 grid showing how many bindus each planet contributes to every house.
- The **SAV Matrix**: The 1x12 total sum grid showing the cumulative bindus across all houses.
- The **SAV Analytics**: The metadata declaring which houses are mathematical "peaks" and "valleys", and the mathematical consistency check ensuring `sum(BAV) == SAV`.
- The **Dasha Support**: The modifier determining if the current Dasha Lord is sitting in a high-bindu house.

---

## 5. Trace Design Proposal
The Ashtakavarga Trace should be built to expose the raw data tables.
1. **SAV Summary Table:** A horizontal display of Houses 1-12 showing total bindus (typically 20-40) with color coding (e.g., `< 25` = Red, `> 30` = Green).
2. **BAV Matrix Grid:** A classic Ashtakavarga table. Rows = Planets (Sun -> Saturn). Columns = Houses (1 -> 12). Cells = Bindus (0 -> 8).
3. **Analytics Summary:** A small card showing `Peak House`, `Weakest House`, and the `BAV Consistency Check` boolean flag.

---

## 6. Verification Console Design
- **Location:** Insert as `K. Ashtakavarga Trace Console`. (Shift `Engine Output Snapshot` to `L`).
- **UI Components:** Utilizes standard HTML `<table className="min-w-full ...">` structures already established in the Domain Formula Trace.

---

## 7. Governance Review
**PASS.** 
Exposing these matrices does not alter any formulas. It simply visualizes the existing outputs of `AshtakavargaEngine`. The engine already runs fully deterministically and pushes `planet_score_adjustments` and `dasha_bav_confidence_multiplier` to the pipeline cleanly.

---

## 8. Implementation Readiness
**READY.** 
The backend JSON payload is exceptionally well-structured and exhaustive. No backend modifications are required. The payload is perfectly shaped for a 2D React mapping loop.

---

## 9. Risk Assessment
**LOW.**
This is a pure frontend rendering task. The only complexity is designing a responsive 12-column data table that does not break CSS styling on mobile devices, necessitating a scrolling `overflow-x-auto` container.
