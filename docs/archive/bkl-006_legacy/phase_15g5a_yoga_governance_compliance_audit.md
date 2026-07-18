---
archive_title: "Phase 15G.5A – Yoga Governance Compliance Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.5A – Yoga Governance Compliance Audit

## 1. Yoga Output Trace
The data flow of Yoga detections was systematically traced across the architecture:

* **YogaEngine**: Evaluates classical rules and outputs string arrays of detected yogas, grouped by house/category (e.g., `universal_yogas: ["Gaja Kesari Yoga"]`).
* **PipelineRunner**: Captures the arrays and embeds them into `engine_outputs["yogas"]`.
* **NatalPromiseEngine**: **Does not read** the yoga outputs.
* **MasterProbabilityEngine**: **Does not read** the yoga outputs. It mathematically aggregates domain, planet, house, rasi, varga, dasha, and transit scores exclusively.
* **QuestionEngine**: Reads the yoga arrays purely to pass them as text context into the LLM prompt (`compose_response`). No math is performed.
* **FormulaEvaluator**: **Does not read** the yoga outputs.
* **DisplayFormatter**: **Does not read** the yoga outputs.

## 2. Mathematical Influence
Does `YogaEngine` currently influence any of the following?

* **Planet Scores**: ❌ No. `PlanetStrengthEngine` evaluates dignity, shadbala, and BAV purely without yoga triggers.
* **House Scores**: ❌ No. `HouseStrengthEngine` calculates SAV, aspects, and occupants. (It possesses a hardcoded stub for yogas, evaluated independently below).
* **Natal Promise Scores**: ❌ No. `NatalPromiseEngine` relies on bhava, bhavadhipati, karaka, and varga pillars exclusively.
* **Question Probabilities**: ❌ No.
* **Activation Indices**: ❌ No.
* **Master Probability**: ❌ No.

## 3. Orphaned Code & Dead Weights Verification
A deep grep search of the codebase for `yoga_bonus`, `yoga_modifier`, `yoga_score`, and `yoga_weight` revealed the following:

1. **`DOMAIN_BONUSES` (astrology_constants.py):**
   A dictionary defining "Bonus additions (classical yogas)" exists. It maps things like `same_2_11_lords: {"wealth": +8}`.
   * **Status:** This dictionary is imported at the top of `NatalPromiseEngine.py` but is **never used** inside the class logic. It is dead code. No bonuses are applied to the domain score.
2. **`yogas_raw` (HouseStrengthEngine.py):**
   Line 49 declares `yogas_raw = 50.0  # Default fallback until Phase 3 integration`.
   * **Status:** This is a hardcoded stub. It forces a neutral 5.0 points to every house indiscriminately. It does not interface with `YogaEngine`.

## 4. `engine_outputs.yogas` Consumption
* **Mathematical Consumers:** Zero. No engine pulls this payload to modify a score.
* **Textual Consumers:** `QuestionEngine` (for narrative LLM grounding), `ChartProcessResponse` schema, and the frontend HTML Report Generator (`extractors.py`).

## 5. Governance Compliance Matrix

| Subsystem | Consumes `YogaEngine`? | Alters Math? | Compliance Status |
| :--- | :--- | :--- | :--- |
| **PlanetStrengthEngine** | No | No | ✅ COMPLIANT |
| **HouseStrengthEngine** | No | No | ✅ COMPLIANT |
| **NatalPromiseEngine** | No | No | ✅ COMPLIANT |
| **MasterProbabilityEngine** | No | No | ✅ COMPLIANT |
| **FormulaEvaluator** | No | No | ✅ COMPLIANT |

**Conclusion:** The Vedic-AI codebase is 100% compliant with the Phase 15 Yoga Governance mandate: "Yoga = Detection Layer Only. No bonuses. No penalties."

## 6. Implementation Readiness
**Can Yoga Trace implementation proceed safely?**
✅ **YES.**

Because Yoga detections currently carry exactly **zero mathematical weight** across all subsystems, refactoring the `YogaEngine` to emit a rich, deterministic JSON Trace Schema (instead of raw string arrays) will have absolutely **no effect** on probabilities, calculations, engine multipliers, or the overall deterministic math outputs. 

The architecture is mathematically decoupled and safe for the Trace Hydration refactor.
