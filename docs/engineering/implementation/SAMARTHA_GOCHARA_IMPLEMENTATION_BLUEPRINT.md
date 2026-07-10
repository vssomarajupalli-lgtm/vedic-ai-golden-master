# SAMARTHA GOCHARA IMPLEMENTATION BLUEPRINT

This blueprint defines the architecture for the proprietary Samartha Gochara system as mandated by `GOCHARA_MANDALI_GOVERNANCE_v1.md`. It outlines the exact integration points required to transform the current classical transit calculator into a True Micro Gochara Engine, without violating DR-007 (Engine Isolation).

**Authority Clarification:** Samartha Gochara is a proprietary micro-gochara system and not a standard transit engine.

---

## 1. COMPONENT AUDIT

### Existing Functionality
*   **Classical Gochara (Parashari)**: Transit quality scoring based on simple Rasi/House positions relative to the Lagna.
*   **Vedha Obstructions**: Identification of malefics blocking positive transits.
*   **Planet Activation**: Conjunction and Aspect (7th, Special) scoring between transit and natal planets.
*   **BAV Validation**: Transit validation using extracted `bav_charts` from the Ashtakavarga Engine.
*   **Dasha Sync**: Bonus multipliers generated when a transiting planet aligns with active Mahadasha/Antardasha lords.

### Reusable Functionality
The entirety of `transit_engine.py` is reusable as the foundational "Macro Transit Layer." The existing methods (`_compute_house_activation`, `_compute_bav_support`, `_compute_dasha_sync`, `_compute_vedha_layer`) will remain fully intact and execute alongside the new Micro Gochara layers.

### Missing Functionality (To Be Built)
*   **Moon Pada Anchor Layer**: Native logic to calculate the exact starting Nakshatra Pada of the natal Moon.
*   **27 Pada Belt Mapping**: Logic to map transiting planets into specific padas relative to the Moon's anchor.
*   **Elinati Shani Builder**: Explicit date-range and phase calculator for Saturn's 7.5-year transit over the natal Moon sign.
*   **Pada-Based Domain Triggers**: Specific astrological rules mapping Pada-transits to life events.

---

## 2. PROPRIETARY LAYER DEFINITIONS

### A. Moon Pada Anchor Layer
*   **Input**: `normalized_payload["planets"]["Chandra"]` (Nakshatra and Degree).
*   **Function**: Calculates the absolute Nakshatra Pada (1-108) of the natal Moon. This serves as the permanent anchor point (Pada 0) for all micro transit calculations.
*   **Output**: An integer representing the anchor Pada.

### B. 27 Pada Belt Mapping (Micro Gochara)
*   **Input**: `transit_payload` (current planetary degrees), Moon Anchor Pada.
*   **Function**: Rather than checking which *Sign* a transiting planet is in, this layer calculates which *Pada* it currently occupies relative to the Moon. The 27 Nakshatras (108 Padas) are treated as a continuous belt radiating outward from the anchor.
*   **Output**: `pada_transit_matrix` mapping each transiting planet to its relative Pada distance from the Moon.

### C. Elinati Shani Builder
*   **Input**: Natal Moon Sign, Ephemeris data for Saturn (past, present, future trajectories).
*   **Function**: Replaces the simplistic `"saturn_sadesati"` flag. It calculates the exact ephemeris ingress and egress dates for Saturn passing through the 12th, 1st, and 2nd signs from the natal Moon.
*   **Output**: `elinati_shani_report` containing: `is_active` (boolean), `current_phase` (1, 2, or 3), `phase_start_date`, and `phase_end_date`.

### D. BAV Validation Layer
*   **Integration**: Operates identically to the current implementation (`_compute_bav_support`). 
*   **Function**: Acts as a strict gatekeeper. Even if a planet occupies a highly positive Pada in the Micro Gochara belt, the positive score is throttled if the BAV bindus in that sector are critically low (< 4).

### E. Dasha Synchronization Layer
*   **Integration**: Leverages the current `_compute_dasha_sync`.
*   **Function**: Cross-references the `pada_transit_matrix` against the currently active Dasha lords.
*   **Output**: Produces printable Dasha-linked transit strings required by `GOCHARA_MANDALI_GOVERNANCE_v1.md` Section 4 (e.g., *"During Jupiter Mahadasha, Saturn transiting the 5th Pada triggers..."*).

### F. Domain Trigger Matrix
*   **Input**: The combined outputs of the Classical Layer, Pada Belt Mapping, and Dasha Sync.
*   **Function**: Expands the existing `_compute_domain_activation`. It applies proprietary Samartha rules (e.g., Transit Jupiter in Pada X triggers Marriage domain; Transit Mars in Pada Y triggers Property domain).
*   **Output**: The final weighted probability modifications fed back to the `MasterProbabilityEngine`.

---

## 3. INTEGRATION ARCHITECTURE (DR-007 COMPLIANT)

The `transit_engine.py` will be expanded structurally without violating engine isolation. No new engine-to-engine calls will be introduced.

### Updated `evaluate()` Execution Flow:

1.  **Macro (Classical) Evaluation**:
    *   Execute existing `_compute_house_activation`, `_compute_vedha_layer`, `_compute_planet_activation`.
2.  **Micro (Samartha Pada) Evaluation**:
    *   Execute new `_compute_moon_anchor(natal_payload)`.
    *   Execute new `_compute_pada_belt(transit_payload, moon_anchor)`.
3.  **Synthesis & Validation**:
    *   Execute existing `_compute_bav_support` and `_compute_dasha_sync`.
4.  **Special Event Builders**:
    *   Execute new `_build_elinati_shani(transit_payload, natal_payload)`.
5.  **Final Scoring (DR-008 Compliance)**:
    *   Merge Classical Score + Micro Pada Score into the final `activation_score`.
    *   Outputs must distinguish Potential, Activation, and Timing Window. Transit activation must not overwrite weak natal promise.
    *   Expand `confidence_flags` with the Elinati Shani phase string and Dasha-linked overlap strings.

By integrating the Micro Gochara layers directly into the `TransitEngine` namespace, we preserve the stateless, deterministic pipeline controlled entirely by the `PipelineRunner`.
