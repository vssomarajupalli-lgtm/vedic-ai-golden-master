---
Generated Date & Time: 2026-06-23T12:46:10+05:30
Current Project Phase: Phase 15 (Promise Engine Validation)
Latest Git Commit Hash: d8a09355ae980b69be448fe4dfeaf0f23e7f3bea
Current Branch: main
Current Runtime Status: Validation Stable
---

# 06_PROMISE_ENGINE_ARCHITECTURE

## Final Approved Architecture
The Promise Engine uses a rigid "Four Pillar" model based on classical Vedic logic, designed to ensure explainability and prevent mathematical overlap or compounding penalties.

### Outer Formula (NatalPromiseEngine)
- **Bhava Strength:** 35% (The house environment)
- **Bhavadhipati Strength:** 30% (The strength of the house lord)
- **Karaka Strength:** 20% (The natural significator of the domain)
- **Relevant Varga Validation:** 15% (The divisional chart score)

### Inner Formulas
#### House Strength (Bhava)
Calculates a 0-100 base score based purely on the physical environment of the house:
- SAV Bindus: 30%
- Occupants: 20%
- Benefic Aspects: 15%
- Malefic Aspects: 15%
- House Type (Kendra/Trikona/Dusthana): 10%
- House Specific Yogas: 10%

#### Planet Strength (Bhavadhipati & Karaka)
Calculates a 0-100 base score based purely on the planet's dignity and state:
- Dignity (Exalted/Moolatrikona/Debilitated): 25%
- House Placement: 20%
- Aspects Received: 15%
- Conjunctions: 10%
- Combustion: 10%
- Retrogression: 5%
- Shadbala: 10%
- Varga Dignity (D9): 5%

## No Double Penalty Rule
Any astrological weakness (e.g., combustion, debilitation, malefic aspects) must be penalized strictly *once* at its lowest root calculation (within the Planet or House engines). Higher-level aggregator engines must *never* subtract heuristic penalties (e.g., "-15 for Saturn in 7th") on top of the already weighted components.

## Planet vs Bhava Separation Logic
The strength of the House (Bhava) and the strength of its Lord (Bhavadhipati) are calculated completely independently. `HouseStrengthEngine` evaluates physical environment, while `PlanetStrengthEngine` evaluates the lord's inherent planetary dignity.

## Governance Decisions
- The formula enforces a `[0, 100]` bound for all calculations.
- Missing data (such as missing D9 Varga charts) gracefully fallback to a neutral `50` rather than punishing the score with a `0`.
- All legacy additive heuristics and magic numbers have been stripped from the system.
