# GM-013E — Frontend Mandali Acceptance Report

## Environment
- **System:** Windows (win32) / PowerShell CLI (headless; no browser automation tooling available)
- **Backend:** FastAPI (Vite dev, pyswisseph fallback synthetic ephemeris)
- **Frontend:** React 19 + Vite 8 + TypeScript 6 + Tailwind 4 + PWA
- **Backend SHA:** `0a7b9e9` (GM-013C.1 tracker commit)
- **Frontend SHA:** `0a7b9e9` (working tree; GM-013E + GM-013E.2 Phase 1 applied)
- **Server URLs:** Backend http://localhost:8000 · Swagger http://localhost:8000/docs · Health http://localhost:8000/api/v1/health/ · Frontend http://localhost:5173
- **Real horoscope:** `extracted_json/raju_canonical_content.json` (Moon nakshatra/pada injected for the Mandali path)

## Backend test baseline
739 PASS / 1 SKIP / 0 FAIL

## What was verified
- **Backend healthy:** `GET /api/v1/health/` → HTTP 200 `{"status":"online"}`.
- **Swagger reachable:** `GET /docs` → HTTP 200.
- **Frontend serving:** `GET :5173/` → HTTP 200 (React app boots).
- **Live API — `/process-chart`:** HTTP 200, `final_score=49`, `grade=WEAK`, `engine_outputs.mandali_advisory` present, `engine_outputs.transit` present.
- **Live API — `/generate-report?format=json`:** HTTP 200; top-level keys = `metadata, master_summary, mandali_analysis, natal_promise, dasha_periods, active_yogas, strength_scores, structured_questions`; `mandali_analysis` present with `natal_chart.grid=12`, `current_chart.grid=12`, `transition_summary.summary_items=9`, `natal placements=1`, `current placements=9`.
- **DTO contract (STOP-gate):** backend `mandali_analysis` + `mandali_advisory` shapes match the frontend `types/mandali.ts` exactly (verified field-by-field).
- **Build:** `npm run build` (tsc -b && vite build) → XML 0 errors.

## Browser Console / Runtime
**Not executable in this environment** — no Playwright/Puppeteer/Comative-managed browser. Live React console, runtime exceptions, network failure capture, and visual screenshots cannot be captured here. The code path compiled clean; no `undefined` DTO access patterns in the rendered components (all guarded with conditional rendering).

## Screen resolutions
Responsive grids use Tailwind `sm/md/lg` breakpoints; verified **code-level** for 1920/1440/1024/768/mobile (CSS grid 1→2→3 columns). Live visual sweep at 1366/1600/768/viewport not executed.

## Known limitations
1. Screenshots (7 requested) not capturable in headless CLI — run `start.bat` on a GUI machine to capture.
2. `pyswisseph` not installed → synthetic ephemeris fallback used for transit/advisory values (affects absolute dates, not schema/structure).
3. Natal chart carries a single Moon placement (backed by the runtime canonical build); grid still renders all 12 Mandali cells.
4. A benign Vite chunk-size (>500 kB) advisory prints during build (non-fatal).

## Acceptance decision
- DTO contract, system health, live API data flow, and production build: **PASS**.
- Browser-only visual/console/responsive/screenshot items: **not executable** in this headless environment (no browser automation present). These require a GUI run of `start.bat` for final sign-off.
- **No verified frontend defect** was found; therefore nothing required fixing during this validation.