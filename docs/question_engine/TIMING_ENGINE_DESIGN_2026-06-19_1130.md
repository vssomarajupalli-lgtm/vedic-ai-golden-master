# TIMING ENGINE DESIGN

**Date:** 2026-06-19
**Version:** Phase 9 Step 3A Governance Package

## Architecture Note
This document outlines the architecture for the Timing Engine. **No implementation is generated in this phase.**

## Overview
The Timing Engine's sole responsibility is to answer the "When?" of a user's question. It takes the output of the Domain Resolver (which determines *if* something will happen) and projects it onto a chronological timeline.

## Current MVP (Minimum Viable Product)
The Phase 9 Timing Engine operates strictly on the Dasha System.

**Timing Logic:**
*   **Natal Promise:** The base potential exists in the D1 chart.
*   **Mahadasha (MD):** Sets the overarching theme of the 7-20 year period.
*   **Antardasha (AD):** Triggers specific events related to the MD and the AD lord's natal placement.
*   **Pratyantardasha (PD):** Provides micro-timing (weeks/months) for the event manifestation.

*Mechanism:* The engine searches the current and future Dasha timelines (from the Dasha Engine payload) to find periods where the MD/AD/PD lords are the same planets heavily involved in the domain's Promise (e.g., 7th Lord, 7th House occupants, or Venus for Marriage).

## Future Integrations

The architecture establishes interfaces for the following advanced timing modules:

### 1. Gochara (Transits)
Phase 10 integration. Gochara will act as a final filter. Even if the Dasha is favorable, the event will not manifest unless the transiting heavy planets (Saturn, Jupiter) activate the relevant natal houses.

### 2. Ashtakavarga Transits (Kakshya)
Integration of Sarvashtakavarga (SAV) and Bhinnashtakavarga (BAV) points to determine the exact month or week a transit yields results.

### 3. Mandali Transit Model
A specialized, proprietary transit intersection model to be integrated in future enterprise phases.
