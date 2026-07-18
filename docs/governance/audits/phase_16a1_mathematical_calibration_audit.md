# Phase 16A.1 – Mathematical Calibration Audit

```text
Created : 2026-06-25
Time    : 10:25 AM IST
Phase   : Phase 16A.1
Type    : Mathematical Calibration Audit
Status  : PERMANENT RECORD
```

## Executive Summary

*Cross-References:*
- Preceded by: [Phase 15 Final Regression Evidence](phase_15_final_regression_evidence.md)
- Followed by: [Phase 16 Architecture Revision Review](phase_16_architecture_review.md)

**Objective**: Perform a complete audit of every mathematical formula, weight, grade, threshold, modifier, and fallback currently used by the Vedic-AI engine. This document serves as the definitive mathematical specification before calibration. 

*No implementation, formula changes, or redesigns are introduced here. This represents the current state of the codebase.*

---

## 1. Planet Strength Engine

**Current Formula**:
Total Score = Dignity (25%) + House (20%) + Aspects (15%) + Conjunctions (10%) + Combustion (10%) + Retrogression (5%) + Shadbala (10%) + Varga Dignity (5%)

**Final Normalization**: `clamp_score(total_score)` ensures the score remains strictly within `[0, 100]`.

| Item | Current Formula / Logic | Source Constant | Mathematical Range | Consumers | Calibration Priority |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dignity** | Dictionary lookup | `PLANET_SCORING_MATRIX["dignity"]` | `0` to `100` | Internal calculation | Tier 1 |
| **House Placement**| Dictionary lookup | `PLANET_SCORING_MATRIX["house_placement"]`| `10` to `100` | Internal calculation | Tier 1 |
| **Aspects** | `50.0 + (B * 25) + (M * -25)` | `PLANET_SCORING_MATRIX["aspects"]` | `0` to `100` (clamped) | Internal calculation | Tier 1 |
| **Conjunctions**| `50.0 + (B * 25) + (M * -25)` | `PLANET_SCORING_MATRIX["conjunctions"]` | `0` to `100` (clamped) | Internal calculation | Tier 1 |
| **Combustion** | `0` if combust, else `100` | `PLANET_SCORING_MATRIX["state_modifiers"]`| `0` or `100` | Internal calculation | Tier 1 |
| **Retrogression**| `100` if retro, else `50` | `PLANET_SCORING_MATRIX["state_modifiers"]`| `50` or `100` | Internal calculation | Tier 1 |
| **Shadbala** | Piecewise interpolation of `req_pct` | Anchors in Engine (`_map_shadbala_to_score`)| `0` to `100` | Internal calculation | Tier 2 |
| **Functional Nature**| *Not actively adjusting base strengths directly in this engine* | N/A | N/A | N/A | Tier 1 (Missing) |
| **Varga Bonus** | Hardcoded stub: `50.0` | In Engine | `50.0` fixed | Internal calculation | Tier 1 |
| **Grades** | *(Does not assign grades natively, outputs raw & final scores)* | N/A | N/A | Other engines | N/A |

---

## 2. House Strength Engine

**Current Formula**:
Total Score = SAV (30%) + Occupants (20%) + Benefic Aspects (15%) + Malefic Aspects (15%) + House Type (10%) + House Yogas (10%)

**Final Normalization**: `clamp_score(total_score)` `[0, 100]`.

| Item | Current Formula / Logic | Source Constant | Mathematical Range |
| :--- | :--- | :--- | :--- |
| **SAV Contribution** | Piecewise linear mapping | In Engine (`anchors`) | `0` to `100` |
| **Lord Contribution**| *Not calculated natively in this engine (done in Natal Promise instead)* | N/A | N/A |
| **Occupants** | `50.0 + (B * 25) + (M * -25)` | `HOUSE_SCORING_MATRIX["occupants"]` | `0` to `100` (clamped) |
| **Benefic Aspects** | `50.0 + (count * 25)` | `HOUSE_SCORING_MATRIX["aspects"]` | `50` to `100` (clamped) |
| **Malefic Aspects** | `100.0 - (count * 50)` | `HOUSE_SCORING_MATRIX["aspects"]` | `0` to `100` (clamped) |
| **House Type** | Dictionary lookup | `HOUSE_SCORING_MATRIX["house_type"]` | `10` to `100` |
| **House Yogas** | Hardcoded stub: `50.0` | In Engine | `50.0` fixed |
| **Grades** | `PROBABILITY_GRADES` | Constants (`PROBABILITY_GRADES`) | `TOO WEAK` to `EXCELLENT`|

---

## 3. Varga Strength Engine (Inventory Only)

**Implemented Vargas**: D9, D10.
*(D2, D3, D4, D7, D12, D16, D20, D24, D27, D30, D40, D45, D60 are configured in Natal Promise via references but not explicitly evaluated natively inside Varga Engine's `evaluate` method for modifiers yet).*

**Calculation (per planet)**:
*   D9: Looks up `dignity` in `D9_SCORES`. Applies `VARGOTTAMA_BONUS` if applicable. Recalculates `PlanetStrengthEngine` on D9 data, assigns as D9 final score.
*   D10: Looks up `dignity` in `D10_SCORES`. Recalculates `PlanetStrengthEngine` on D10 data, assigns as D10 final score.

**Inputs**: Normalized `planets`, `vargas`, and `dependency_scores`.
**Outputs**: `results["D9"]["planets"]`, `results["D10"]["planets"]` with `final_score`, `breakdown`, `modifiers`, `confidence_flags`.
**Current Weaknesses**: Evaluates by overwriting D1 scores completely via sub-engine call instead of purely applying modifiers. Only D9/D10 are active in the engine loop.
**Missing Contributors**: Functional Nature impacts in vargas, explicit definitions for all higher harmonic charts.

---

## 4. Natal Promise

**Four Pillars & Weights**:
1.  **Bhava (35%)**: Averages `final_score` of `primary_house`.
2.  **Bhavadhipati (30%)**: Planet strength of the primary house's lord.
3.  **Karaka (20%)**: Primary/Secondary Karaka blended score.
4.  **Varga (15%)**: Varga domain specific chart planet score.

| Domain | Primary House | Support Houses | Varga | Primary Karaka | Secondary Karaka |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Marriage** | 7 | 2, 11 | D9 | Venus | Jupiter |
| **Career** | 10 | 6, 11 | D10 | Saturn | Sun |
| **Wealth** | 2, 11 | 5, 9 | D2 | Jupiter | Venus |
| **Education** | 5 | 4, 9 | D24 | Mercury | Jupiter |
| **Children** | 5 | 9, 11 | D7 | Jupiter | Moon |
| **Property** | 4 | 2, 11 | D4 | Mars | Moon |
| **Health** | 1 | 6, 8, 12 (Inv) | D6 | Sun | Moon |
| **Spirituality**| 9, 12 | 5 | D20 | Jupiter | Ketu |

**Grade Boundaries**:
*   `>=70`: STRONG
*   `>=50`: MODERATE
*   `>=30`: WEAK
*   `<30`: PRESENT

---

## 5. Master Probability

**Engine Weights**:
*   `natal_promise`: 0.40
*   `planet_strength`: 0.15
*   `house_strength`: 0.10
*   `rasi_strength`: 0.10
*   `varga_validation`: 0.10
*   `dasha_activation`: 0.10
*   `transit_trigger`: 0.05

**Aggregation & Normalization**:
Computes weighted sum of the factor averages. Missing components default to a `50.0` neutral stub. Result is clamped to `[0, 100]` and graded using `PROBABILITY_GRADES`.

---

## 6. Rasi Strength

**Factors & Weights**:
*   **A. SAV Environment (35%)**: Piecewise map of SAV bindus.
*   **B. Sign Lord Strength (25%)**: Score of ruling lord. Defaults to `50`.
*   **C. Occupant Quality (20%)**: Avg of (Benefic score) & (100 - Malefic score). Empty sign defaults to `50`.
*   **D. Balance (10%)**: `50 + (+15 B / -15 M occupants) + (±5 aspects capped at ±10)`.
*   **E. Dignity Impact (5%)**: Avg occupant dignity mod (`Exalted +30` to `Deb -20`). +10 bonus if lord in own sign.
*   **F. Varga Validation (5%)**: Avg D9/D10 occupant dignity (`Exalted +10` to `Deb -8` + Vargottama `+15`).

---

## 7. Dasha Strength

**Current Formula**:
*   **Timing Multipliers**: Uses the astrological axis (e.g., `1_1`, `6_8`) between Mahadasha (MD) and Antardasha (AD) lords to look up `DASHA_SCORING_MATRIX["relationship_scalars"]`.
*   **MD/AD/PD Activation (DashaEngine)**: `(MD base * 0.50) + (AD base * 0.30) + (PD base * 0.20)`.
*   **Master Probability Aggregation**: Uses a slightly different formula: `(0.60 * (MD * multiplier)) + (0.40 * (AD * multiplier))`.

---

## 8. Ashtakavarga

**Thresholds and Boundaries**:
*   **BAV Grades**: 7 (EXCELLENT), 6 (STRONG), 5 (GOOD), 4 (AVERAGE), 3 (BELOW_AVG), 2 (WEAK), 0 (CRITICAL).
*   **SAV Grades**: >=30 (STRONG), >=28 (FAVORABLE), >=22 (AVERAGE), >0 (WEAK), 0 (CRITICAL).
*   **BAV Planet Modifiers**: >=5 bindus (`+5`), 4 bindus (`0`), <=3 bindus (`-5`).

---

## 9. Global Mathematical Constants

| Constant | Current Value | Used By | Candidate for Calibration |
| :--- | :--- | :--- | :--- |
| `PLANET_SCORING_MATRIX` | Nested dict (dignity, state, house) | PlanetStrengthEngine | Tier 1 |
| `HOUSE_SCORING_MATRIX` | Nested dict (type, aspects, occupants) | HouseStrengthEngine | Tier 1 |
| `D9_SCORES`, `D10_SCORES` | `[-10, 15]` and `[-5, 10]` scale | VargaEngine, RasiStrengthEngine | Tier 1 |
| `VARGOTTAMA_BONUS` | `15.0` | VargaEngine, RasiStrengthEngine | Tier 1 |
| `DASHA_SCORING_MATRIX` | `[0.75, 1.25]` relationship scalars | DashaEngine | Tier 2 |
| `SAV_BINDU_SCALE` | `[(0,0), (20,30), (25,50), (40,100)]` | HouseStrength, RasiStrength, Ashtakavarga | Tier 1 |
| `RASI_SCORING_MATRIX` | Nested dict (weights, dignities) | RasiStrengthEngine | Tier 2 |
| `PROBABILITY_GRADES` | `[80, 65, 50, 35, 0]` thresholds | Planet, House, Master, Rasi | Tier 1 |
| `NATAL_PROMISE_GRADES` | `[70, 50, 30, 0]` thresholds | NatalPromiseEngine | Tier 1 |
| `DOMAIN_CONFIG` | `0.35/0.30/0.20/0.15` per domain | NatalPromiseEngine | Tier 2 |
| `BAV_GRADE_THRESHOLDS` | `[7, 6, 5, 4, 3, 2, 0]` scale | AshtakavargaEngine | Tier 2 |
| `BAV_PLANET_MODIFIER` | `+5, 0, -5` | AshtakavargaEngine | Tier 2 |
| `SAV_FAVORABLE_THRESHOLD`| `28` | AshtakavargaEngine | Tier 3 |
| `MASTER_WEIGHTS` | `0.4/0.15/0.1/0.1/0.1/0.1/0.05` | MasterProbabilityEngine | Tier 2 |

---

## 10. Grade System

| Grade Scale | Categories & Numeric Ranges | Consumers |
| :--- | :--- | :--- |
| **Probability Grades** | EXCELLENT (>=80), VERY GOOD (>=65), GOOD (>=50), WEAK (>=35), TOO WEAK (<35) | Planet Strength, House Strength, Master Probability, Rasi Strength |
| **Natal Promise** | STRONG (>=70), MODERATE (>=50), WEAK (>=30), PRESENT (<30) | Natal Promise Engine |
| **BAV Grades** | EXCELLENT (7-8), STRONG (6), GOOD (5), AVERAGE (4), BELOW_AVG (3), WEAK (2), CRITICAL (0-1) | Ashtakavarga Engine |
| **SAV Grades** | STRONG (>=30), FAVORABLE (>=28), AVERAGE (>=22), WEAK (>0), CRITICAL (0) | Ashtakavarga Engine |

---

## Calibration Candidates

### Tier 1 (Must Calibrate)
*   **Planet Strength Constants**: (`PLANET_SCORING_MATRIX`, Combust/Retro logic, Aspect weights). Crucial mathematical core.
*   **House Strength Constants**: (`HOUSE_SCORING_MATRIX`, Occupant/Aspect weighting).
*   **Varga Strength Logic**: Reverting overwrite behavior to strict fractional modification. Calibrating `D9_SCORES` and `VARGOTTAMA_BONUS`.
*   **Grade Boundaries**: Evaluating `PROBABILITY_GRADES` and `NATAL_PROMISE_GRADES` for realistic statistical distributions.

### Tier 2 (Review Later)
*   **Master Probability**: `MASTER_WEIGHTS` distribution.
*   **Rasi Strength Weights**: `RASI_SCORING_MATRIX` sub-factor weighting.
*   **Dasha Activation Scalars**: `DASHA_SCORING_MATRIX` multipliers.
*   **Ashtakavarga Modifiers**: `BAV_PLANET_MODIFIER`.
*   **Natal Promise Weights**: Domain internal 4-pillar configurations (`DOMAIN_CONFIG`).

### Tier 3 (Keep Fixed)
*   Canonical JSON mappings.
*   Bhava Madhya as the fundamental house foundation.
*   Four Pillar Architecture.
*   Yoga Governance rules.
*   SAV Classical Thresholds (e.g., Average = 28 bindus).
*   Zero Astrological Recalculation architecture standard.
