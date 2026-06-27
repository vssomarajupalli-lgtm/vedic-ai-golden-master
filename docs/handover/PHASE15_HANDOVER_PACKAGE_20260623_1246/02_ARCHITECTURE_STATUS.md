---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 02_ARCHITECTURE_STATUS

The following are the immutable architectural and governance rules governing the Vedic AI System:

## 1. D1 Immutability
D1 (Rasi) charts and the physical layout of planets/houses are the supreme source of truth. They cannot be altered or reinterpreted by downstream components.

## 2. Engine Isolation Rule
Engines (e.g., `PlanetStrengthEngine`, `HouseStrengthEngine`, `NatalPromiseEngine`) must not overlap in concern. Each engine must calculate its specific scope and return a standalone 0-100 grade/score.

## 3. Dosha Preservation Routing
Doshas are computed independently and must be preserved accurately in the canonical state. They are selectively applied to the relevant domain (e.g., Mangal Dosha strictly to Marriage) and must not implicitly lower the fundamental score of unrelated domains.

## 4. Functional Nature Governance
The functional nature of a planet (benefic vs malefic) is statically defined based on the ascendant (Lagna) and must not be dynamically overwritten by contextual placement during basic strength calculations.

## 5. Dasha Timeline Contract
The timeline generation must guarantee continuity. Any dasha/bhukti periods requested must align sequentially and completely cover the native's lifespan timeline without gaps or overlaps.

## 6. Mandali Governance
The architectural decisions, documentation changes, and engine refactoring must be strictly verified against approved `PROMISE_ENGINE_FORMULA_v1.md` and reference architectures. Unauthorized heuristic magic numbers are strictly prohibited.

## 7. Question Engine Architecture
The logic used to synthesize AI responses must purely rely on the deterministic `machine_index.json` and canonical data points. It must map explicit user questions to underlying domain evaluations and dynamically inject appropriate classical rule interpretations without fabricating scores.

## 8. Four Pillar Promise Engine Architecture
A strict aggregation model used in `NatalPromiseEngine`:
- Bhava Strength (35%)
- Bhavadhipati Strength (30%)
- Karaka Strength (20%)
- Relevant Varga Validation (15%)

## 9. No Double Penalty Rule
Any astrological weakness (e.g., combustion, debilitation, malefic aspects) must be penalized strictly *once* at its lowest root calculation (within the Planet or House engines). Higher-level aggregator engines must *never* subtract heuristic penalties (e.g. "-15 for Saturn in 7th") on top of the already weighted components.
