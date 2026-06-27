# Phase 15G: Final Transparency Audit

## Executive Summary
This audit reviews the absolute state of the Vedic-AI Formula Verification Console and its synchronization with the backend mathematical pipeline following the execution of Phase 15G.11A. 

Significant progress has been made. Over 10 deterministic subsystems are now fully exposed, proving the math live to the user. However, a few peripheral subsystems and global mapping modules remain hidden.

**Transparency Completion Percentage:** ~77% (10 out of 13 major calculation modules are fully transparent).

---

## 1. Currently Exposed Trace Sections
The Verification Console currently renders exactly 11 coherent traces (A through K):

- **A.** Domain Formula Trace (`engine_outputs.natal_promise`)
- **B.** Planet Strength Breakdown (`engine_outputs.planets`)
- **C.** House Strength Breakdown (`engine_outputs.houses`)
- **D.** Dasha Formula Console (`engine_outputs.dashas`)
- **E.** Signal Trace Console (`isolated_signals`)
- **F.** Yoga Trace Console (`engine_outputs.yogas`)
- **G.** Varga Trace Console (`engine_outputs.vargas`)
- **H.** Master Probability Trace (`master_probability`)
- **I.** Rasi Trace Console (`engine_outputs.rasis`)
- **J.** Engine Output Snapshot (Raw `breakdown` JSON)
- **K.** Ashtakavarga Trace Console (`engine_outputs.ashtakavarga`)

---

## 2. Remaining Hidden Backend Payloads
The following payloads are actively computed in the backend but remain unmapped to the frontend UI:

1. `breakdown.engine_outputs.transit` (Gochara Activation Trigger)
2. `breakdown.engine_outputs.functional_nature` (Benefic/Malefic roles for Ascendant)
3. `breakdown.engine_outputs.doshas` (Kuja Dosha, etc. - currently emitting `{}`)
4. **Global Confidence Flags** (Present inside nested modules, but no aggregated array exists)
5. **Calibration Constants** (Hardcoded in Python `astrology_constants.py`, no HTTP transport)

---

## 3. Subsystem Classification Matrix

| Subsystem / Payload | Frontend Status | Backend Status | Classification |
| :--- | :--- | :--- | :--- |
| **Domain Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Planet Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **House Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Dasha Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Signal Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Yoga Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Varga Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Master Prob** | Exposed | Fully Calculated | **COMPLETE** |
| **Rasi Trace** | Exposed | Fully Calculated | **COMPLETE** |
| **Ashtakavarga**| Exposed | Fully Calculated | **COMPLETE** |
| **Transit** | Hidden | Partial (Stub) | **PARTIAL** |
| **Functional Nature**| Hidden | Fully Calculated | **PARTIAL** |
| **Doshas** | Hidden | Missing (`{}`) | **NOT EXPOSED** |
| **Global Flags**| Hidden | Nested Only | **PARTIAL** |
| **Calibration** | Hidden | Missing API | **NOT EXPOSED** |

---

## 4. Missing Consoles & UI Elements
To achieve 100% UI Transparency, the following sections must be added to `VerificationConsole.tsx`:
- **L. Transit Trace Console:** To map Gochara activation logic.
- **M. Functional Nature Trace Console:** To prove why a planet is acting destructively or constructively.
- **N. Dosha Trace Console:** To list structural chart flaws.
- **O. Global Flags Summary:** A top-level tag cloud of all `confidence_flags`.
- **P. Calibration Console:** A standalone React page or modal exposing immutable engine weights.

---

## 5. Missing API Hydration
- **Calibration Route:** The frontend has absolutely no access to `astrology_constants.py`. A new FastAPI endpoint (e.g., `GET /api/v1/calibration`) must be created to hydrate the Calibration Console.

---

## 6. Missing Backend Trace Generation
- **Transit Engine:** Currently relies on stub logic (`stub_factors`). Needs dynamic calculation.
- **Dosha Engine:** Currently returns an empty dictionary `{}`. Needs trace scaffolding.
- **Pipeline Runner:** Needs a small aggregation function to scrape all `confidence_flags` from the 10 nested engines and expose them as a flat `global_flags` array at the top of the response.

---

## 7. Recommended Final Phase 15 Roadmap
The transparency initiative can be closed out in three final sprint phases:

1. **Phase 15G.12 – Secondary Math Traces:** Implement the Transit Trace (L) and Functional Nature Trace (M) in the UI.
2. **Phase 15G.13 – Flaws & Flags:** Build out the Dosha Engine backend payload and implement the Dosha Trace (N). Create the Global Flag aggregator in `PipelineRunner` and expose the Global Flags Summary (O).
3. **Phase 15G.14 – Calibration Transport:** Build `GET /api/v1/calibration` and design the standalone Calibration Console UI (P), officially closing out Phase 15.
