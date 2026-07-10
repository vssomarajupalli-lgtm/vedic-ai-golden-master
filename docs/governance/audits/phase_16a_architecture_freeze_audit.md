# Phase 16A – Architecture Freeze & Mathematical Ownership Audit

```text
Created : 2026-06-25
Time    : 10:25 AM IST
Phase   : Phase 16A
Type    : Freeze Audit
Status  : PERMANENT RECORD
```

## Executive Summary

*Cross-References:*
- Preceded by: [Phase 16 Architecture Revision Review](file:///d:/vedic-ai-system/docs/governance/audits/phase_16_architecture_review.md)
- Followed by: [Phase 16A Architecture Constitution Review](file:///d:/vedic-ai-system/docs/governance/audits/phase_16a_architecture_constitution_review.md)

**Objective:** This document serves to permanently freeze architectural ownership before any mathematical calibration begins. Every mathematical concept is assigned to a single owner to prevent duplication, double-counting, and scattered logic. 

*Note: No code has been modified during this audit. This is a purely architectural evaluation.*

---

## 1. Complete Ownership Matrix

The following matrix assigns a single definitive owner to every mathematical factor and astrological concept.

| Astrological Concept | Permanent Owning Engine |
| :--- | :--- |
| **Planet Dignity (D1)** | `PlanetStrengthEngine` |
| **Combustion & Retrogression** | `PlanetStrengthEngine` |
| **Bhavadhipati (Lord) Strength** | `PlanetStrengthEngine` (evaluated via lord's planet score) |
| **Karaka Strength** | `PlanetStrengthEngine` (evaluated via karaka's planet score) |
| **House Occupants** | `HouseStrengthEngine` |
| **House Aspects** | `HouseStrengthEngine` |
| **Bhava Madhya** | Canonical JSON / Base Logic (House boundaries) |
| **Sign Environment (Zodiac traits)** | `RasiStrengthEngine` |
| **Sign Lord Quality** | `RasiStrengthEngine` (derived from `PlanetStrengthEngine` output) |
| **SAV Bindu Evaluation** | `RasiStrengthEngine` (using extraction from `AshtakavargaEngine`) |
| **BAV Chart Generation** | `AshtakavargaEngine` |
| **BAV Planet Modifiers** | `AshtakavargaEngine` |
| **Vargottama Bonus** | `VargaEngine` |
| **Varga (D9, D10) Dignity** | `VargaEngine` |
| **Functional Nature (Benefic/Malefic)** | `FunctionalNatureEngine` |
| **Yoga Detection & Logic** | `YogaEngine` |
| **Dasha Timing Multipliers** | `DashaEngine` |
| **Transit / Gochara Activations** | `TransitEngine` |
| **Confidence Flags** | Generated natively by each owning engine |
| **Final Grade Translation** | Engine-specific mappers referencing Central Calibration Layer |
| **Master Probability Synthesis** | `MasterProbabilityEngine` |

---

## 2. Duplicate Calculation Report

**Identified Duplication:** **Occupant Quality & Aspect Balances**
*   **Where it occurs:** 
    *   `HouseStrengthEngine._evaluate_influences()` and `_evaluate_specific_aspects()`
    *   `RasiStrengthEngine._factor_occupant_quality()` and `_factor_balance()`
*   **Why it happens:** Because the system defaults to the Whole Sign House system, a Sign (Rasi) and a House (Bhava) occupy the exact same spatial coordinates. Both engines were programmed to evaluate the impact of planets sitting in that space, and planets aspecting that space.
*   **The Risk:** `MasterProbabilityEngine` weights House Strength at 10% and Rasi Strength at 10%. A malefic planet residing in Aries (if Aries is the 1st House) applies a numerical penalty in the House Engine *and* the Rasi Engine, violating the **No Double Penalty Rule**.
*   **Permanent Owner:** `HouseStrengthEngine`. Occupants and aspectual rays are spatial (Bhava) properties.

**Identified Duplication:** **SAV Contribution**
*   **Where it occurs:**
    *   `HouseStrengthEngine._evaluate_sav_support()`
    *   `RasiStrengthEngine._factor_sav()`
*   **Why it happens:** SAV is mapped to signs but operates as general environmental support for the houses residing in those signs.
*   **Permanent Owner:** `RasiStrengthEngine`. Ashtakavarga bindus are inextricably linked to zodiacal signs.

---

## 3. House vs Rasi Ownership Recommendation

To completely eliminate double counting and adhere to the Single Producer Principle, the responsibilities of House and Rasi must be strictly bifurcated.

**HouseStrengthEngine Owns (Spatial & Ray Properties):**
*   House Occupants (Benefic/Malefic impacts)
*   House Aspects (Angular rays)
*   House Activation
*   House-specific Yogas (stubbed)
*   House Type (Kendra, Trikona, Dusthana)

**RasiStrengthEngine Owns (Environmental & Zodiacal Properties):**
*   Sign Lord Strength
*   SAV Environment (Bindus)
*   Sign Dignity Impact (e.g., is this sign naturally hostile to its occupants?)

*Conclusion:* The `RasiStrengthEngine` **must remain an independent engine**, but during calibration, its formulas must be stripped of all occupant and aspect counting logic.

---

## 4. Calibration Layer Inventory

Every mathematical constant must be moved from scattered engine files into a unified Calibration Layer.

**Hardcoded Defaults & Stubs to Extract:**
*   `50.0` default fallback in `MasterProbabilityEngine` (`_STUB_SCORE`).
*   `50.0` default fallback in `NatalPromiseEngine` (`_NEUTRAL`).
*   `50.0` fallback in `PlanetStrengthEngine` for missing Shadbala/Varga data.
*   `50.0` fallback in `HouseStrengthEngine` for Yogas.
*   `4` bindu fallback in `AshtakavargaEngine` for missing BAV data.

**Constants to Extract (Currently in `astrology_constants.py`):**
*   `PLANET_SCORING_MATRIX` (dignity, state, house values).
*   `HOUSE_SCORING_MATRIX` (type, aspects, occupants values).
*   `RASI_SCORING_MATRIX` (sign environment weights).
*   `DASHA_SCORING_MATRIX` (relationship scalars).
*   `D9_SCORES`, `D10_SCORES`, `VARGOTTAMA_BONUS`.
*   `SAV_BINDU_SCALE` anchors.
*   `PROBABILITY_GRADES`, `NATAL_PROMISE_GRADES`, `BAV_GRADE_THRESHOLDS`.
*   `MASTER_WEIGHTS` and `DOMAIN_CONFIG` percentages.

---

## 5. Hidden Risk Report

1.  **Varga Overwrite Risk:** As identified in Phase 15, `VargaEngine` explicitly overwrites D1 scores by internally calling `PlanetStrengthEngine` again. This is a mathematical leakage risk. The Varga Engine must be refactored to calculate and return only additive/subtractive modifiers (`+X` or `-X`).
2.  **Hardcoded Module Imports:** Engines currently import matrices directly (e.g., `from app.config.astrology_constants import ...`). This prevents hot-swapping calibration profiles.
3.  **Dasha vs. Master Aggregation Mismatch:** The `DashaEngine` currently aggregates timelines using `(MD * 0.50) + (AD * 0.30) + (PD * 0.20)`, while `MasterProbabilityEngine` evaluates `(MD * 0.60) + (AD * 0.40)`. This logic must be centralized so there is only one mathematical owner of the aggregate dasha score.

---

## 6. Final Architecture Recommendation

1.  **Calibration Profile Injection:** Build a `CalibrationManager` that loads a `CalibrationProfile` (JSON/YAML/DB) and passes it to engines via the PipelineRunner. Engines will read `profile.planet.combust_score` instead of static constants.
2.  **Strict Boundary Enforcement:** Implement the House vs. Rasi ownership split strictly. Remove overlapping logic from the Rasi engine.
3.  **Modifier-Only Varga:** Refactor Varga Engine to conform to the Single Producer Principle—it produces modifiers, not base planet scores.

---

## 7. Recommended Phase 16 Execution Order

The safest path forward to enable future mathematical calibration without breaking governance:

*   **Phase 16A.2:** Varga Architecture Review (No Code).
*   **Phase 16A.3:** Calibration Architecture (Implement Dependency Injected Profiles; remove all constants and 50.0 stubs from engines).
*   **Phase 16B:** Mathematical Calibration Round 1 (Apply the mathematical separation of House/Rasi, fix Varga overwrite, tune weights using horoscopes).
*   **Phase 16C:** Question Engine Expansion.
*   **Phase 16D:** Client Intelligence Dashboard.
*   **Phase 16E:** Adrishta Vishayalu.
*   **Phase 16F:** Complete Dasha Intelligence.
*   **Phase 16G:** Functional Nature Transparency.
*   **Phase 16H:** Moon-Centered Mandali Gochara.
