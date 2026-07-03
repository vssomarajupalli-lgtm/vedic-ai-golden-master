# VALIDATION FRAMEWORK KNOWLEDGE PACKAGE

## 1. Executive Summary
The Validation Framework is the observability and diagnostic layer of the Golden Master. Primarily surfaced through the `VerificationConsole.tsx` in the frontend, it exposes the raw mathematical trace of every deterministic calculation performed by the backend engines.

## 2. Purpose
To guarantee absolute explainability. The platform rejects "black box" AI. If a user asks "Will I be wealthy?" and receives a score of 72%, the Validation Framework provides the exact mathematical lineage proving exactly how that 72% was computed down to the tenth of a decimal point.

## 3. Responsibilities
- Extract the `breakdown` dictionaries from every major pipeline engine (Planet, House, Dasha, Master Probability).
- Present the structural math in organized, collapsible UI sections.
- Display the lifetime Dasha timeline projection and highlight active periods.
- Surface "Confidence Flags" (e.g., `varga_contradicted`, `zero_sav`) to identify weak or anomalous data.

## 4. Architecture
- **Data Layer (Backend):** Every engine adheres to the standard JSON payload contract, returning a `breakdown` dictionary of its internal formula factors.
- **Presentation Layer (Frontend):** `VerificationConsole.tsx` consumes the global `rawOutputs` store and maps the backend dictionaries to Tailwind-styled data tables and metric cards.

## 5. Major Verification Consoles
- **A. Domain Formula Trace:** Shows the exact 4-pillar scores (Bhava, Lord, Karaka, Varga) for the Natal Promise domains.
- **B. Planet Strength Breakdown:** Shows Dignity, Aspects, Conjunctions, Shadbala, etc., for all 9 planets.
- **C. House Strength Breakdown:** Shows SAV, Aspects, and Occupant scores for all 12 houses.
- **D. Dasha Formula Console:** Shows the temporal multipliers for the active MD, AD, and PD lords.
- **E. Signal Trace Console:** Shows the targeted factors used by the `QuestionEngine` for a specific user query.
- **F. Yoga Trace Console:** Shows the boolean `PASSED`/`FAILED` trace and specific failure reasons for classical yogas.
- **H. Master Probability Trace:** Shows the final aggregation weights of the 7-pillar Master formula.

## 6. Implementation Files
- `frontend/src/pages/VerificationConsole.tsx`

## 7. Technical Debt & Recommendations
- The UI handles missing data gracefully using optional chaining (`?.`), but the backend occasionally outputs strings like `"Data Unavailable"` instead of zeroes or neuter scores, which breaks some mathematical rendering. Standardize all backend missing-data fallbacks to `50.0` or `null`.
- Add a "Dosha Trace Console" to visualize afflictions and penalties once Phase 10C is implemented.
