# TRANSIT ENGINE KNOWLEDGE PACKAGE

## 1. Executive Summary
The `TransitEngine` evaluates current planetary transits (Gochara) against a natal chart to produce an `activation_score` representing the temporal triggering of the natal promise. It relies on the `MandaliGenerator` to resolve transit positions relative to the Natal Moon and evaluates five mathematical sub-systems: House Activation, BAV Support, Vedha Obstruction, Planet Activation, and Dasha-Transit Synchronization.

## 2. Purpose
To calculate the short-term probability fluctuations (transits) that act upon the long-term probabilities (Natal Promise). It overrides the initial `transit_trigger` stub in the `MasterProbabilityEngine`.

## 3. Responsibilities
- Resolve transit longitudes into Moon-centered Mandalis.
- Calculate 5 separate mathematical layers of Gochara influence.
- Generate confidence flags (e.g., "saturn_sadesati").
- Provide a graceful stub fallback if transit data is not provided in the payload.

## 4. Architecture
- **Stateless & Deterministic:** Follows Rule 4 (Zero recalculation) and Rule 2 (No AI).
- **Sub-systems:**
  1. **House Activation (30%):** Static quality score of planet occupying a specific house relative to the moon.
  2. **BAV Support (20%):** Validates transit strength using Ashtakavarga bindus (score = bindus / 8).
  3. **Vedha Obstruction (10%):** Subtracts points if a malefic occupies a specific paired house (blocking a positive transit).
  4. **Planet Activation (20%):** Scores conjunctions and classical aspects (7th, plus special 3/10, 5/9, 4/8) onto natal planets.
  5. **Dasha-Transit Sync (20%):** Applies massive multipliers if the transiting planet is the active MD or AD lord, or aspects/occupies the natal position of the active lords.

## 5. Inputs
- `transit_payload` (Current transits)
- `natal_payload` (Base chart)
- `dasha_results` (Active temporal lords)
- `av_results` (BAV charts)
- `natal_promise_results` (Domain scores)

## 6. Outputs
- `activation_score`: Float [0, 100]
- `grade`: String (e.g., "GOOD")
- `activated_domains`: Domain-specific transit scores
- `breakdown`: Scores of the 5 sub-systems

## 7. Data Contracts
- Outputs cleanly integrate into the Master Probability Engine, which expects an `activation_score`.

## 8. Formula & Engine Dependencies
- Heavily dependent on `MandaliGenerator` for spatial resolution.
- Dependent on `CalibrationManager` for `TRANSIT_WEIGHTS`, `VEDHA_PAIRS`, and `TRANSIT_DASHA_SYNC_BONUSES`.

## 9. Business Rules & Deterministic Rules
- **Rule of Clamping:** Every output boundary is rigidly clamped between `[0, 100]` using `clamp_score()`.
- **Vedha Cap:** Vedha penalties cannot exceed `TRANSIT_VEDHA_CAP`.
- **Sade Sati Rule:** Flagged if Saturn transits Mandalis 12, 1, or 2 relative to the Moon.

## 10. Execution Flow
1. Receives payload. Returns stub if empty.
2. Extracts Natal Moon longitude, resolves transit houses via `MandaliGenerator`.
3. Sequentially executes the 5 sub-system formulas.
4. Performs a master weighted sum.
5. Computes domain-specific activations.
6. Returns the standardized dictionary.

## 11. Implementation Files
- `backend/app/engines/transit_engine.py`

## 12. Supporting Documents
- `GOCHARA_MANDALI_GOVERNANCE_v1.md`

## 13. Governance References
- Ashtakavarga transit rules (BAV bindu transit logic).

## 14. Special Requirements Breakdown

### Current Implementation
Fully implemented Gochara engine evaluating House, BAV, Vedha, Planet, and Dasha-Sync layers. Translates transit longitude to Moon-centered Mandalis for accuracy.

### Placeholder Logic
The `_stub_result()` method acts as a massive placeholder when no `transit_payload` is supplied, hardcoding the score to exactly `50` and returning a `transit_stub_no_input` confidence flag.

### Deprecated Logic
The legacy fallback in `t_houses[p] = int(v.get("house", 0))` is used when the natal Moon's longitude is missing, effectively bypassing the `MandaliGenerator` and using naive house boundaries. This contradicts the new Mandali governance.

### Reusable Deterministic Logic
- The `_compute_bav_support` (bindu transit mapping) is highly accurate and reusable.
- The `_compute_vedha_layer` logic correctly implements classical obstruction.
- The `_compute_dasha_sync` effectively multiplies temporal importance.

### Components for Future Gochara Engine
- `MandaliGenerator` spatial arithmetic.
- The Ashtakavarga BAV intersection layer.
- The Vedha obstruction pairs and penalty caps.

### Components NOT to Reuse
- The `_compute_planet_activation` is fundamentally naive. It uses strict house-based aspect checks (e.g., 7th house) without calculating exact planetary orb overlap.
- The hardcoded `_BENEFIC_PLANETS` and `_MALEFIC_PLANETS` sets bypass the `FunctionalNatureEngine`, resulting in inaccurate transit strength depending on the chart's Ascendant.

## 15. Technical Debt
- Bypasses `FunctionalNatureEngine`.
- Naive aspect calculations.
- Contains legacy fallbacks to static house assignments.

## 16. Future Roadmap
- Strip out static Rasi aspects in favor of exact longitudinal orb aspects.
- Inject `FunctionalNatureEngine` output to override natural benefic/malefic transit logic.
