---
archive_title: "ARCHITECTURE CONTRADICTIONS AND CLARIFICATIONS"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive"
archive_reason: "Superseded by current documentation architecture"
original_version: "Unknown (historical)"
replacement_document: "docs/ARCHITECTURE_RULES.md, docs/engineering/validation/PROJECT_MILESTONE_v1_RUNTIME_VALIDATION.md"
---

# ARCHITECTURE CONTRADICTIONS AND CLARIFICATIONS

## 1. Rule Conflicts

**Conflict ID: AC-001 (D1 Immutability vs Varga Override)**
*   **Document A**: `docs/ARCHITECTURE_RULES.md` (Rule 3) - "D1 must remain foundational... Vargas must NOT overwrite D1".
*   **Document B**: `docs/engineering/validation/PROJECT_MILESTONE_v1_RUNTIME_VALIDATION.md` - Implementation shows Varga adjustments (e.g., Venus D9 Navamsha support of 100.0) significantly altering domain grades (e.g., Marriage 19 -> 22).
*   **Reason for conflict**: Varga modifiers are actively changing the fundamental scores, which pushes the boundaries of "supporting" vs "overwriting" the D1 foundation.
*   **Recommended clarification required**: Define the mathematical threshold (e.g., max 10% variance) where Varga support officially becomes an "overwrite" of D1 logic.

**Conflict ID: AC-002 (Engine Development Priorities)**
*   **Document A**: `docs/ARCHITECTURE_RULES.md` (Rule 13) - "The following remain FUTURE roadmap phases: Dasha systems... Transit systems".
*   **Document B**: `docs/status/PROJECT_HANDOVER_MASTER_2026-06-09_13-45_IST.md` - Lists `DashaEngine` under "Current working engines" but later states "V1.3 MD/AD/PD STRENGTH ENGINE Next major milestone."
*   **Reason for conflict**: The Dasha system is simultaneously categorized as an active, completed engine, a pending V1.3 milestone, and a future roadmap phase.
*   **Recommended clarification required**: Explicitly declare the current production status of `DashaEngine` and whether V1 is considered stable without it.

**Conflict ID: AC-003 (Kuja Dosha Evaluation Rules)**
*   **Document A**: `docs/engineering/validation/NATAL_PROMISE_VALIDATION_AUDIT.md` - Criticizes missing Kuja Dosha checks (Mars in 1, 2, 4, 8, 12).
*   **Document B**: `docs/engineering/validation/VEDIC_RULE_VALIDATION_REVIEW.md` - Recommends Kuja Dosha for V1, but warns "cancellation rules must be coded precisely" to avoid false alarms.
*   **Reason for conflict**: Implementing Kuja Dosha immediately without complex cancellation logic will produce false predictions, violating the "Deterministic Astrology Calculation" rule.
*   **Recommended clarification required**: Should Kuja Dosha be delayed to V2, or should a simplified version be released in V1 accepting the false-alarm risks?

---

## 2. Formula Conflicts

| Conflict ID | Formula | File A | File B | Clarification Needed |
| ----------- | ------- | ------ | ------ | -------------------- |
| FC-001 | Health Score Support Houses | `NATAL_PROMISE_VALIDATION_AUDIT.md` (avg(6, 8, 12)_INVERTED) | `VEDIC_RULE_VALIDATION_REVIEW.md` (Maraka 2 & 7, Trimshamsha D30) | Should the 8th house be inverted (penalizing longevity) or should it be treated as a Maraka/Longevity house? |
| FC-002 | Event Probability Calculation | `PROJECT_HANDOVER_MASTER_2026-06-09_13-45_IST.md` (Event = Natal * Dasha * Transit) | `VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` (Score = Marriage + Dasha + Transit) | Is the final event probability additive (+) or multiplicative (*)? |
| FC-003 | Varga Domain Mapping | `NATAL_PROMISE_VALIDATION_AUDIT.md` (Health uses D6) | `VEDIC_RULE_VALIDATION_REVIEW.md` (Health uses D30 Trimshamsha) | Which divisional chart is correct for Health domain calculations? |
| FC-004 | Dasha Probability Math | `VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` (Notation shows `*` but math equates to `+`) | N/A | Should Dasha sub-period strengths (MD, AD, PD) be added or multiplied to get the final score? |

---

## 3. Engine Boundary Conflicts

*   **Overlap 1: YogaEngine vs PlanetStrengthEngine Dignity Lookup**:
    *   `PROJECT_HANDOVER_MASTER` noted `YogaEngine` previously attempted to read dignity from `PlanetStrengthEngine`, violating `ARCHITECTURE_RULES.md` Rule 4 (Engines must NEVER directly call other engines). While fixed by reading from the raw payload, this exposes a risk of engines performing duplicate baseline calculations instead of centralizing them.
*   **Overlap 2: Varga Calculation Responsibilities**:
    *   `NatalPromiseEngine` calculates a flat `0.05 * D9` modifier internally for Marriage, but there is also a dedicated `VargaEngine`. Does `NatalPromiseEngine` calculate Varga modifiers independently (violating single responsibility), or does it consume `VargaEngine`'s output (potentially violating engine isolation)?
*   **Overlap 3: Dasha vs Master Probability / Event Probability**:
    *   `PROJECT_HANDOVER_MASTER` says the Dasha engine computes "Activation % Not event prediction." However, `VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE` assigns "Dasha Probability Engine" to measure Dasha strength and a "Timing Engine" to measure windows. It is unclear which engine holds the boundary responsibility for aggregating Dasha into the final Master Probability.

---

## 4. Terminology Conflicts

*   **"Strength" vs "Probability"**:
    *   `VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` interchangeably uses "Marriage Strength", "Marriage Potential", and "Event Probability".
*   **"Natal Promise"**:
    *   In some files, this refers to the base static calculation of the birth chart.
    *   In `PROJECT_HANDOVER_MASTER`, it acts as a variable multiplier within the Event Probability equation.
*   **"Master Probability" vs "Event Probability"**:
    *   `MasterProbabilityEngine` generates a "Master Probability" (e.g., Score 55).
    *   Future architecture references an "Event Probability Engine" calculating probabilities for specific domains. Are these the same engine, or is Master Probability a chart-wide average?
*   **"Functional Benefic"**:
    *   Referred to both as a static Lagna-based dignity and an active runtime score modifier.

---

## 5. Source Of Truth Validation

*   **Primary Source**: `docs/VEDIC_AI_SOURCE_OF_TRUTH.md` is designated as the master schema definition.
*   **Rule Master**: `docs/ARCHITECTURE_RULES.md` defines the strict deterministic laws.
*   **Status Master**: `docs/status/PROJECT_HANDOVER_MASTER_2026-06-09_13-45_IST.md` establishes the immediate action items.
*   **The Conflict**:
    *   `PROJECT_HANDOVER_MASTER` explicitly states that `docs/knowledge/` files are "Used for design guidance only. Not implementation authority."
    *   However, highly detailed formulas exist in `docs/knowledge/VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` that contradict the `HANDOVER_MASTER`.
    *   Additionally, the `validation` audit files propose highly complex additions (Atmakaraka, Upapada Lagna) that directly conflict with the "Overengineering Prevention Rule" (Rule 8) in `ARCHITECTURE_RULES.md`.
*   **Flagged For Resolution**: Multiple documents claim ultimate authority. The exact formula hierarchy must be strictly defined before coding resumes.

---

## 6. Questions for Domain Expert

*   **Q1**: Should the 8th House be inverted for Health calculations (penalizing longevity), or should it be treated as a Maraka/Longevity house per classical Vedic rules?
*   **Q2**: Is the final Event Probability derived additively (Sum of strengths) or multiplicatively (Product of activations)?
*   **Q3**: Should Dasha and Transit engines be considered active V1 modules, V1.3 milestones, or purely Future V2 Roadmap, given their contradictory statuses across the documentation?
*   **Q4**: When Varga results conflict with D1 calculations, does the D1 Immutability Rule prevent Vargas from overriding the final grade, or is the current 5-10% modification weight mathematically acceptable?
*   **Q5**: Do we immediately implement Kuja Dosha for V1 despite the lack of cancellation rules, risking false divorce/delay alarms, or do we push it to V2?
*   **Q6**: Should the `NatalPromiseEngine` query the `VargaEngine` for its D9/D10/D6 multipliers, or should it calculate them independently? If it queries `VargaEngine`, does that violate the Engine Isolation Rule?
*   **Q7**: Are the mathematical formulas inside `VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` to be considered authoritative despite the file being located in the `reference` folder?
*   **Q8**: Which divisional chart is correct for Health domain calculations: D6 or D30?

---

## 8. Gochara (Transit) Engine Conflicts

**Conflict ID: GC-001 (Recalculation vs Extraction Rule)**
*   **Document A**: `docs/samartha_v2/GOCHARA_ENGINE_MASTER.md` - Mandates building a "Saturn transit resolver", "Elinati Shani builder", and performing extensive calculation of Moon nakshatra pada-based zones.
*   **Document B**: Decision Register (DR-003) - "Before implementing any module, first verify whether the calculation already exists in the canonical source data. Prefer extraction and interpretation over recalculation."
*   **Reason for conflict**: It is highly likely the source PDF already contains Gochara and Elinati Shani predictions (potentially under `phalithalu` pages 85-87 in `machine_index.json`). Rebuilding a full transit calculator violates the new extraction-first mandate.
*   **Recommended clarification required**: Please confirm if the `canonical_content.json` output will eventually include extracted Gochara results. If yes, `GOCHARA_ENGINE_MASTER.md` must be deprecated or severely reduced in scope.

**Conflict ID: GC-002 (Engine Boundary Overlap - Strength Recalculation)**
*   **Document A**: `docs/samartha_v2/GOCHARA_ENGINE_MASTER.md` (Section 5) - Demands the Gochara engine must include "planet strength and bhava strength calculations."
*   **Document B**: `docs/ARCHITECTURE_RULES.md` and `PROJECT_HANDOVER_MASTER_2026-06-09_13-45_IST.md` - These strengths are already calculated by `PlanetStrengthEngine` and `HouseStrengthEngine` in Phase 1.
*   **Reason for conflict**: Recalculating fundamental strengths inside the Gochara Engine violates the DRY principle and the Engine Isolation rule.
*   **Recommended clarification required**: Confirm that the Gochara Engine must strictly consume the outputs of `PlanetStrengthEngine` and `HouseStrengthEngine` rather than recalculating Exaltation, Own sign, Moolatrikona, etc., natively.

**Conflict ID: GC-003 (Conflicting Scoring Weights)**
*   **Document A**: `docs/samartha_v2/GOCHARA_ENGINE_MASTER.md` (Section 6) - Defines a rigid universal scoring formula: `(0.40 × S_lord) + (0.30 × S_karaka) + (0.15 × S_D9) + (0.10 × S_varga) + (0.05 × 20) + Bonus`.
*   **Document B**: `docs/knowledge/VEDIC_AI_PROBABILITY_ENGINE_ARCHITECTURE.md` - Uses domain-specific weights (e.g., Marriage uses 25% House, 25% Lord, 20% Karaka, 20% D9, 10% Vargas).
*   **Reason for conflict**: The Gochara Engine Master attempts to override the global domain probability formulas with a generalized 40/30/15/10/5 split.
*   **Recommended clarification required**: Does the Gochara Engine override the core Event Probability scoring framework, or should Section 6 of `GOCHARA_ENGINE_MASTER.md` be discarded in favor of domain-specific weighting?

---

## 9. Recommended Resolutions

1.  **Freeze Reference Documents**: Officially label all documents in `docs/knowledge/` as deprecated or strictly illustrative, moving all active mathematical formulas into `VEDIC_AI_SOURCE_OF_TRUTH.md`.
2.  **Define Pipeline Aggregator**: Clarify that individual Engines (Planet, House, Varga, NatalPromise) remain strictly isolated, and only the `PipelineRunner` or a specialized `SynthesisEngine` (like `MasterProbabilityEngine`) can read from multiple engine outputs to compute the final formulas. This resolves the engine boundary conflicts.
3.  **Standardize Lexicon**: Enforce "Strength" for static chart calculations (e.g., Planet Strength, House Strength) and "Probability" strictly for final predictive event outcomes (e.g., Marriage Event Probability).
4.  **Health Formula Override**: Immediately pause the inversion of the 8th house in the Health domain calculation until the Domain Expert clarifies the longevity rules.
5.  **Varga Override Cap**: Enforce a strict mathematical cap on Varga influence (e.g., max 15%) at the `MasterProbabilityEngine` level to satisfy the D1 Immutability Rule.
6.  **Gochara Extraction Priority**: Wait for `HoroscopeCleaner_Final` output for Gochara sections before writing calculation logic, converting Gochara to an extraction/evaluation engine rather than a raw calculation engine.
