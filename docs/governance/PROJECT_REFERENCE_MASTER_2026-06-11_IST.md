# PROJECT REFERENCE MASTER
**Date:** 2026-06-11 IST
**Purpose:** Permanent onboarding and project memory file.

---

## A. Project Vision
* **Deterministic astrology:** The system relies on precise mathematical boundaries and classical rules.
* **No generative predictions:** LLMs are used for synthesis and delivery, not for calculating planetary dignity, aspects, or domain strengths.
* **Extraction → Validation → Interpretation:** Prioritize extracting pre-calculated canonical data. If absent, validate constraints, and only then proceed to interpretation.

## B. Authority Hierarchy
1. **Domain Expert** (Ultimate source of truth)
2. **Authority Lock** (Overrides all assumptions)
3. **Decision Register** (Approved domain clarifications)
4. **Source of Truth** (Canonical JSON data)

## C. Final Approved Architecture
**Pipeline Flow:**
The architecture operates via isolated engines orchestrated by the `PipelineRunner` and `MasterSynthesisEngine`. Engines must NEVER call each other directly (DR-007).

* **Question Engine:** Routes user questions to domain targets.
* **Planet & House Strength Engines:** Calculates foundational dignity, shadbala, and ascendant-based functional nature.
* **Natal Promise Engine:** Synthesizes D1 foundation and Varga multipliers.
* **Dosha Engine:** Extracts and validates chart afflictions (e.g., Kuja Dosha).
* **Transit (Gochara) Engine:** Calculates active micro-gochara multipliers.
* **Dasha Engine:** Extracts temporal activation windows.
* **Remedy Engine:** Generates domain-specific mitigation suggestions based on engine outputs.

## D. Canonical Data Status
* **Present:** D1 and Varga charts, planetary degrees, basic ephemeris, Dasha timelines.
* **Partial:** BAV (Ashtakavarga) matrices, domain Phalithalu.
* **Missing:** Full dosha exceptions, specific micro-transit rules.
* **Extraction Requirements:** Always check `canonical_content.json` before building custom calculation logic (DR-003).

## E. Final Approved Decisions
* **DR-001:** Dasha Engine is strictly an extraction and activation engine. Do not recalculate dashas.
* **DR-002:** The Gochara Engine is the largest pending subsystem.
* **DR-003:** Extraction First methodology. Verify if canonical data exists before implementation.
* **DR-004:** Stop and Ask rule for conflicts.
* **DR-005:** No architectural assumptions allowed.
* **DR-006:** `canonical_content.json` is the sole knowledge authority.
* **DR-007:** Engine Isolation. Engines cannot call other engines directly.
* **DR-008:** Hybrid Probability Model. Separate Natal Promise, Dasha, Transit. Do not overwrite weak promise with strong transit.
* **DR-009:** Kuja Dosha Extraction Authority. Extract Kuja dosha from canonical data before trying to validate/recalculate.

## F. Gochara Summary
**Samartha Gochara is a proprietary micro-gochara system and not a standard transit engine.**
* **Moon Pada Anchor:** Natal Moon's precise Nakshatra Pada serves as the anchor point.
* **Pada Belt Logic:** Transiting planets are evaluated by their relative Pada distance, not just their Rasi.
* **Elinati Shani:** Exact ephemeris calculation of Saturn's 7.5-year transit.
* **BAV Validation:** Ashtakavarga points act as a gatekeeper for transit effects.
* **Dasha Synchronization:** Transits are weighted by the currently active Mahadasha/Antardasha lords.
* **Domain Trigger Layer:** Proprietary mapping of Pada transits to specific life events.

## G. Current Implementation Status
* **Question Engine:** Boundary violation needs fixing.
* **Planet Strength:** Partially complete, needs Functional Nature logic.
* **House Strength:** Mostly complete.
* **Dosha Engine:** Pending extraction and validation.
* **Dasha Engine:** Needs refactoring to pure extraction.
* **Transit Engine:** Major Gochara expansion pending.
* **Remedy Engine:** Pending implementation.

## H. Current Coding Priority
1. QuestionEngine DR-007 Fix
2. Functional Nature Engine
3. Extraction Expansion
4. Dosha Extraction Validation
5. Samartha Gochara
6. Integration
7. Remedies

## I. CRITICAL CLARIFICATIONS REQUIRED BEFORE CODING (STOP AND ASK)
*None currently actively blocking Task 1. However, if any ambiguity arises during Dosha or Gochara implementation:*
* **Why it matters:** Ensuring deterministic output aligned with domain rules.
* **Which engine is affected:** Typically Dosha, Dasha, or Transit.
* **Whether implementation must stop:** YES. Stop and consult the Domain Expert.

## J. Future Roadmap
* **V1:** Core deterministic engine, isolated architecture, hybrid probability model, pure extraction-based doshas and dashas.
* **V1.1:** Enhanced micro-gochara rules, advanced remedy mappings.
* **V1.2:** Extended Varga validation (D10, D60).
* **V1.3:** AI synthesis refinement for end-user delivery.
* **Future phases:** Independent validation engines for dosha and ephemeris fallback.

## K. Coding Agent Rules
**Before coding:**
1. Check Authority Lock
2. Check Decision Register
3. Check Canonical Data
4. Check Reference Master

**If conflict exists: STOP.**
Ask Domain Expert.
Never assume astrology rules.
