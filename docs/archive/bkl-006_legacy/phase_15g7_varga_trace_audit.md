---
archive_title: "Phase 15G.7: Varga Transparency Trace Audit"
archive_status: "ARCHIVED"
archive_date: "2026-07-18"
archive_category: "archive\bkl-006_legacy"
archive_reason: "Classified as CP-001 (Zero Dependency Historical Artifact) per BKL-006 Chief Architect Decision Register"
original_version: "Unknown (historical)"
replacement_document: "Not specified (see docs/INDEX.md for current canonical documents)"
---

# Phase 15G.7: Varga Transparency Trace Audit

## 1. Audit of Current VargaEngine Outputs

**JSON Paths:**
- `breakdown.engine_outputs.vargas.D9.planets.<planet>`
- `breakdown.engine_outputs.vargas.D10.planets.<planet>`

**Existing Structures:**
- `final_score`: Simply echoes the D1 `base_score` from `PlanetStrengthEngine`. Does not represent the true Varga structural score.
- `modifiers`: Captures `D9_dignity_modifier`, `D10_dignity_modifier`, and `D9_vargottama_bonus`.
- `confidence_flags`: Captures contradictions like `varga_contradicted` or `neecha_bhanga_varga`.
- `breakdown`: Hardcoded to `{}`. Contains zero structural contributors.

## 2. Why Breakdown Dictionaries Are Empty

There is an architectural disconnect between how Varga data is scored versus how it is stored:
1. **Scoring happens outside VargaEngine:** `NatalPromiseEngine._varga_score()` calculates the 15% Varga pillar for a domain (e.g., D9 Venus for Marriage). To do this, it dynamically passes `normalized_vargas` (raw data) directly into `PlanetStrengthEngine.calculate_strength()`.
2. **Contributors are discarded:** `PlanetStrengthEngine` successfully calculates the Varga planet's structural strength (Dignity, House, Aspects) and returns a rich object with a full `breakdown`. However, `NatalPromiseEngine` executes `return float(result.get("final_score", _NEUTRAL))`, permanently discarding the breakdown payload.
3. **VargaEngine is ignorant of scores:** `VargaEngine` only computes top-level modifiers (like Vargottama) and has no knowledge of the deep structural evaluation performed by `NatalPromiseEngine`, leaving its own `breakdown` dictionary empty.

## 3. Contributor Inventory

For any given Varga evaluation (e.g., D9 Venus for Marriage), the following contributors exist during runtime but suffer different fates:

| Contributor | Status | Current Location |
| :--- | :--- | :--- |
| **Dignity Base Score** | Discarded | Evaluated in PlanetStrengthEngine, dropped by NatalPromiseEngine |
| **House Placement** | Discarded | Evaluated in PlanetStrengthEngine, dropped by NatalPromiseEngine |
| **Benefic Support** | Discarded | Evaluated in PlanetStrengthEngine, dropped by NatalPromiseEngine |
| **Malefic Affliction** | Discarded | Evaluated in PlanetStrengthEngine, dropped by NatalPromiseEngine |
| **Vargottama Bonus** | Preserved | Evaluated and stored in `VargaEngine` (`modifiers`) |
| **Varga Dignity Modifier** | Preserved | Evaluated and stored in `VargaEngine` (`modifiers`) |
| **Contradiction Flags** | Preserved | Evaluated and stored in `VargaEngine` (`confidence_flags`) |

## 4. Transparency Matrix

| Varga Layer Component | Availability |
| :--- | :--- |
| D9/D10 Dignity Modifiers | **READY** |
| Vargottama Identification | **READY** |
| Contradiction Flags | **READY** |
| Base Dignity Values | **MISSING** |
| House Placement Modifiers | **MISSING** |
| Conjunctions & Aspects | **MISSING** |
| Final Synthesized Varga Score | **MISSING** |

## 5. Verification Console Design

### I. Varga Trace Console

Example structural render for the UI once hydrated:

```text
▾ D9 Navamsha - Venus

  Final Varga Score: 58
  
  Contributors:
  Dignity Base                 +25
  House Placement              +10
  Benefic Support               +8
  Malefic Affliction            -5
  Vargottama Bonus             +20
  
  Conclusion:
  Final Score                   58
```

## 6. Governance Review

- **VargaEngine Modification of D1:** Clean. `VargaEngine` does not alter D1 base scores. It merely echoes the D1 `final_score` and outputs isolated modifiers.
- **D1 Immutability:** Fully intact.
- **Varga Refinement Principle:** Intact. `VargaEngine` acts strictly as an additive/refinement layer as per the phase definitions.

## 7. Recommended Implementation Plan (Hydration)

### Backend Gaps
The primary gap is the "lost" breakdown payload from `NatalPromiseEngine`. The secondary gap is that `VargaEngine` doesn't currently store the true domain-level structural score.

### Proposed Fix
1. **Refactor `VargaEngine` to run the structural calculations:** Instead of `NatalPromiseEngine` calling `PlanetStrengthEngine` on the fly and throwing away the data, `VargaEngine.evaluate()` should itself instantiate `PlanetStrengthEngine` to pre-calculate the full scores and breakdowns for D9/D10 planets.
2. **Store Breakdowns Natively:** `VargaEngine` will inject these full breakdown objects directly into `results["D9"]["planets"][planet_name]["breakdown"]`.
3. **Refactor `NatalPromiseEngine` to consume:** `NatalPromiseEngine` will stop performing recalculations and simply read `varga_results["D9"]["planets"][karaka]["final_score"]` per the "Zero astrological recalculation" architectural rule.

### Risk Assessment
- **Low Risk:** Relocating the `PlanetStrengthEngine` call from `NatalPromiseEngine` to `VargaEngine` enforces existing governance rules ("Consumes pre-computed scores only").
- **Mathematical Drift:** If implemented correctly, this is a pure refactor. The final math will be identical, but the intermediate breakdown payloads will be successfully trapped and exposed to the frontend.
