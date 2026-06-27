# PROJECT_STATUS_MASTER.md
**Last Updated:** 2026-06-25

## Project State: Phase 16A.3 Calibration Layer Freeze
The Vedic AI System has completed Phase 16A.3. The mathematical Calibration Layer has been successfully implemented across all 12 engines. The `CalibrationManager` completely isolates all tuning weights. Numerical parity has been rigorously verified, and the tuple-key deserialization issue resolved. The current commit is `ecaf976`. The next immediate objective is Phase 16B - Mathematical Calibration Round 1.

## Phase Completion Status
- **Phase 1: Foundation** — **COMPLETE**
- **Phase 2: Strength Engines** — **COMPLETE**
- **Phase 3: Varga Integration** — **COMPLETE**
- **Phase 4: Ashtakavarga** — **COMPLETE**
- **Phase 5: Question Engine** — **COMPLETE**
- **Phase 6: Dasha Integration** — **COMPLETE**
- **Phase 7: Mandali Gochara** — **COMPLETE**
- **Phase 15: Transparency & Verification Console** — **COMPLETE**
- **Phase 16A: Architecture Constitution Freeze** — **COMPLETE**
- **Phase 16A.3: Calibration Architecture** — **COMPLETE**
- **Phase 16B: Mathematical Calibration Round 1** — **NEXT IMMEDIATE OBJECTIVE**

## Key Achievements & Locks
- **Architecture Constitution:** **APPROVED**
- **Governance:** **FROZEN**
- **Ownership Matrix:** **FINALIZED**
- **Formula Ownership Register:** **FINALIZED**
- **Engine Dependency Hierarchy:** **FROZEN**
- **Engine Output Contracts:** **FROZEN**
- **Calibration Version Governance:** **FROZEN**
- **Calibration Migration Strategy:** **FROZEN**
- **Moon-Centered Nine-Pada Mandali Governance:** **FROZEN**
- **Four Pillar Promise Architecture:** **COMPLETE** (Strict 35/30/20/15 percent logic enforced).
- **No Double Penalty Rule:** **COMPLETE** (Afflictions calculated at root engines only, preventing double counting).
- **Yoga Governance:** **COMPLETE** (Yoga is strictly detection, classification, and explanation. Yoga score modification permanently removed).
- **Bhava Bala Override Removal:** **COMPLETE** (House Strength formula explicitly adheres to foundational rules, bypassing Bhava Bala payload injection).
- **Dosha Routing:** **COMPLETE** (Preservation schema applied and verified).
- **Functional Nature Governance Lock:** **COMPLETE** (Math remains completely deterministic).

## Testing Status
- **Status:** GREEN
- **Passed:** 613
- **Failed:** 0
- **Errors:** 0
- **Coverage:** 100% of defined architectural mathematical schemas.

## Legacy Historical Context
The following sections document the critical historical debugging state prior to the Phase 7 release.

## Project Goal
*   **Final intended Vedic AI architecture:** A robust, pipeline-driven engine combining Python/FastAPI backend with a React/Vite frontend. The architecture is fully deterministic, calculating exact scores based on astrological rules without generative AI interpolation.
*   **HoroscopeCleaner integration goals:** Consume static pre-extracted JSON (`canonical_content.json`) natively, bypassing the need for an active PDF parsing layer in the main runtime pipeline.
*   **Deterministic calculation goals:** 100% math-based scoring.
*   **Question engine goals:** Provide precise astrological answers mapped directly to derived domain scores.
*   **Transit/Gochara goals:** Project dynamic effects of current/future transits over the base natal promise.

## Current Implementation Status
### Backend
*   **JsonNormalizer:** **COMPLETED**
*   **PipelineRunner:** **COMPLETED**
*   **PlanetStrengthEngine:** **COMPLETED**
*   **HouseStrengthEngine:** **COMPLETED** (Formula: SAV, Occupants, Benefic/Malefic Aspects, Type, Yogas)
*   **NatalPromiseEngine:** **COMPLETED** (Four Pillar Architecture. Support Houses are deferred/dead configuration)
*   **YogaEngine:** **COMPLETED** (Detection only. No scoring output)
*   **AshtakavargaEngine:** **COMPLETED**
*   **DashaEngine:** **COMPLETED**
*   **TransitEngine:** **COMPLETED** (Mandali Gochara)
*   **MasterProbabilityEngine:** **COMPLETED** (Yoga modifiers explicitly removed)
*   **ReportBuilder:** **COMPLETED**

### Frontend
*   **Upload page:** **COMPLETED** (Verified hitting `http://localhost:8000`).
*   **Results page:** **COMPLETED** (UI components exist, renders data directly from backend payload).
*   **Question Engine page:** **PARTIALLY IMPLEMENTED**
*   **Export Report page:** **PARTIALLY IMPLEMENTED** (Fails due to missing `WeasyPrint` OS dependency).

## Files Modified During Current Debugging Cycle
1.  `backend/app/parsers/json_normalizer.py`: Added fallback logic to gracefully handle `"planets"`, `"houses"`, and `"birth_data"` keys without demanding the legacy `"raw_"` prefixes.
2.  `backend/app/reports/sections/extractors.py`: Updated dictionary extraction to use `"promise"` key instead of `"grade"` key, perfectly matching the `NatalPromiseEngine` schema.

## Confirmed Fixes
*   `master_synthesis` renamed to `master_probability` in schema to match actual logic.
*   `grade` fallback fixed to `promise` extractor alignment in `ReportBuilder`.
*   Fixed `JsonNormalizer` natively bypassing the `canonical_content.json` input failure that orphaned planets and houses.

## Open Problems
*   **Frontend Phantom Cache:** The frontend application seamlessly connects to any process on port 8000. Ghost instances (like older Docker containers running unpatched backend code) will silently intercept requests, causing "fixed" bugs to continuously appear unfixed to the user.
*   **Extraneous `machine_index` Schema:** The API enforces a strict `machine_index: List[Dict]` payload shape via Pydantic. Passing an empty or malformed index throws a fatal `422 Unprocessable Entity`, despite the fact that `machine_index` has exactly zero impact on any astrological calculations.

## Current Runtime Symptoms
*   **Life domains showing 48:** Conclusively proven to be caused by `JsonNormalizer` rejecting `canonical_content.json` legacy keys in unpatched instances. It silently passes `0` planets and `0` houses to the mathematical engines, which triggers their respective fail-safe defaults (50 strength, 0 SAV) and mathematically resolves to exactly `48`.
*   **Missing meaningful question engine output:** Incomplete implementation.
*   **Missing/unfinished transit/gochara output:** Transit engine logic is not fully integrated into the pipeline flow.

## Critical Contradictions Found
*   **CONTRADICTION 1:** Previous audits incorrectly claimed the system was fully functional and mathematically flawless because 619 tests passed. They failed to test the *exact* input schema of the final production `canonical_content.json`.
*   **CONTRADICTION 2:** Earlier audits incorrectly stated `JsonNormalizer` was broken. Its python execution was sound, but it strictly expected legacy prefixes (`"raw_planets"`) instead of the final extracted keys (`"planets"`).

## Next Investigation Plan
1.  **Stop blindly rewriting engine math:** The fallback value of `48` is ultimate runtime proof that the `NatalPromiseEngine` math is working flawlessly under fallback/empty payload conditions.
2.  **Verify Yoga Engine Math:** Trace `YogaEngine` using actual runtime data to identify why rules do not trigger.
3.  **Refactor `machine_index` Schema:** Deprecate its strict Pydantic requirements in `ChartProcessRequest` since it is entirely cosmetic and causes `422` crashes.