# CODING AGENT MEMORY
**Date:** 2026-06-11 IST

## 1. Project Objective
Build a strictly deterministic, classical Vedic Astrology calculation and interpretation engine. **Generative LLMs are NOT to be used for astrological math or logic prediction**; they are exclusively for final natural language synthesis. The pipeline relies heavily on extraction of pre-calculated canonical data.

## 2. Current Status
* **Architecture:** The core pipeline is established. Engines are strictly isolated.
* **Pending Major Components:** Dosha Engine, Samartha Gochara (Micro-Transit) Engine, Dasha Engine refactor to pure extraction, Remedy Engine.
* **Immediate Issue:** The `QuestionEngine` has an architectural boundary violation that needs fixing.

## 3. Active Priorities
1. **QuestionEngine DR-007 Fix:** Prevent it from directly importing other engines.
2. **Functional Nature Engine:** Add ascendant-based benefic/malefic logic.
3. **Extraction Expansion:** Enhance `canonical_content.json` usage.
4. **Dosha Extraction Validation:** Implement Kuja Dosha, Kala Sarpa, etc., strictly via extraction (DR-009).
5. **Samartha Gochara:** Implement proprietary micro-gochara (Pada belt) logic.
6. **Integration:** Hook up all engines to `PipelineRunner`.
7. **Remedies:** Generate remedies based on final probability scores.

## 4. Locked Decisions (Do Not Violate)
* **DR-003 (Extraction First):** Check canonical data before building logic.
* **DR-006 (Canonical Source Authority):** `canonical_content.json` is the sole knowledge base.
* **DR-007 (Engine Isolation):** Engines cannot communicate directly; they return state to the pipeline.
* **DR-008 (Hybrid Probability):** Natal Promise + Dasha + Transit. They are distinct. A weak natal promise cannot be overridden by transits.
* **DR-009 (Dosha Extraction):** Do not recreate Kuja Dosha math. Extract and validate first.

## 5. Critical Warnings
* **STOP AND ASK:** If there is any contradiction, ambiguity, or missing canonical data for a required astrological rule, **STOP IMPLEMENTATION**. Do not make assumptions. Ask the Domain Expert.
* **Gochara is Proprietary:** Samartha Gochara is not a standard transit engine. It uses Moon Pada anchoring and micro-belt mapping.

## 6. Files That Must Be Read First
* `docs/governance/AUTHORITY_LOCK_2026-06-11_18-15_IST.md`
* `docs/governance/PROJECT_REFERENCE_MASTER_2026-06-11_IST.md`
* `docs/governance/DECISION_REGISTER.md`
* `docs/engineering/implementation/SAMARTHA_GOCHARA_IMPLEMENTATION_BLUEPRINT.md`
* `docs/engineering/implementation/NEXT_IMPLEMENTATION_PLAN.md`
