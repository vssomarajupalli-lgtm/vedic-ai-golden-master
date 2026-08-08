# Samartha Vedic AI System

## Golden Master

### GM-017.4

### Production Baseline

---

## 1. Release Information

| Field | Value |
|-------|-------|
| Release Name | GM-017.4 — Complete Print & Export Framework |
| Version | GM-017.4 (Golden Master v1.2) |
| Date | 2026-08-08 |
| Branch | `main` |
| Commit SHA | `5a0e5883f07f2e8fb54e7167fec2a265d9463c18` |
| Git Tag | `GM-017.4` (annotated) |

---

## 2. Engineering Summary

GM-017.4 completes the Print & Export Framework for the Samartha Vedic AI Golden Master. It establishes a single, canonical generated HTML document as the source of truth for **Preview**, **Download HTML**, **Download PDF**, and **Print Direct**, eliminating the previous divergence where browser Print operated on the live React page and Preview was unimplemented.

The framework now produces a print-optimized A4 document with page breaks between all major report sections, repeatable table headers, non-splitting Mandali/activation/timeline tables, and a running header plus "Page X of Y" footer delivered through the active PDF renderer (Playwright/Chromium; WeasyPrint CSS margin-box fallback retained).

The remaining PDF HTTP 500 was diagnosed as environmental (the server was previously launched under a bare uv Python interpreter without Playwright/WeasyPrint site-packages) and is resolved by running the backend under the `backend\venv` interpreter, which exposes Playwright to the report pipeline.

---

## 3. Completed Milestones

### GM-017 Recovery

Restored the report export path after the report pipeline began returning plain dictionaries instead of Pydantic models. Fixed the `AttributeError: 'dict' object has no attribute 'dict'` failure in the HTML generator and re-established live JSON/HTML/PDF generation.

### GM-017.2

Rate-limiting middleware hardened: the 10th+ request now returns a clean `JSONResponse(429)` with `Access-Control-Allow-Origin: *` and a JSON body instead of raising an uncaught `HTTPException`. Recovery after the 60-second window verified.

### GM-017.3

Diagnosed the layered failures in the export pipeline:
- PDF/HTML 500 root cause (`html_generator.py` `.dict()` call on a dict).
- Question Engine section template crash against `StructuredQuestionResult` shape.
- Knowledge Graph "412 Issues" caused by the frontend reading camelCase fields off the raw snake_case API payload.

Applied targeted fixes (GM-017.3A): the HTML generator renders dicts directly, the Question Engine section renders the real `StructuredQuestionResult` keys defensively, and the Knowledge Graph viewer applies the existing `mapGraphState()` mapper.

### GM-017.4

Completed the Print & Export Framework:
- Single shared generated HTML document for Preview / Download HTML / Download PDF / Print.
- Print Framework now prints the generated document (iframe `contentWindow.print()`), not the live React page.
- A4 print CSS: margins, page breaks between major sections, non-splitting Mandali/planet/house/gochara tables, flowable lifetime timeline with repeating headers.
- PDF running header (client name + report title) and footer (Page X of Y) via Playwright header/footer templates; WeasyPrint `@page` margin-box fallback retained.
- Verified PDF/HTML/JSON all HTTP 200 live; JSON report content byte-identical to pre-release baseline.

---

## 4. Protected Modules

The following modules are frozen (engineering freeze) and must not be modified:

- Astrology Engines
- Pipeline Runner
- Formula Registry
- Formula Verification
- Results Calculations
- Consultation Calculations
- Current Gochara
- Planet Strength
- House Strength
- MD / AD / PD
- Swiss Ephemeris
- Calibration
- Knowledge Store (backend)
- Backend Report JSON Schema
- Report DTOs

---

## 5. Verification Summary

| Area | Status |
|------|--------|
| Results | UNCHANGED — byte-identical to pre-release baseline |
| Questionnaire | UNCHANGED — `structured_questions` section hash-MATCH |
| Formula Verification | UNCHANGED — hash-MATCH; only per-run `target_date_utc` timestamp differs |
| Consultation | UNCHANGED — consultation/engagement calculations untouched |
| Current Gochara | UNCHANGED — `gochara_report` section hash-MATCH |
| Knowledge Graph | PASS — viewer applies `mapGraphState()`; "79 nodes · 206 relationships ✓ Integrity Valid", 0 issues |
| Print Framework | PASS — Preview/Print use the shared generated HTML document |
| PDF Export | PASS — HTTP 200, 55 pages, running header + Page X of Y footer confirmed |
| HTML Export | PASS — HTTP 200, single canonical document |

---

## 6. Regression Status

Regression verification **passed**.

- JSON report generated after release is byte-identical to the captured baseline when run-time values are masked (masked diff fields: **0**; all 11 mandatory sections hash-MATCH).
- Backend test suite: **748 passed / 1 skipped / 1 pre-existing fail** (`tests/test_report_builder.py::test_extracts_correct_data` — outdated `client_info` assertion, pre-existing, not part of this release).
- Frontend: **TypeScript PASS**, **Vite build PASS**.
- No protected module was modified in GM-017.4.

---

## 7. Repository Status

| Item | Status |
|------|--------|
| Working Tree | Clean (no staged/untracked files) |
| Branch | `main` |
| Tag | `GM-017.4` (annotated, pushed to origin) |
| Remote | `origin` — up to date; tag present via `git ls-remote --tags origin` |

---

## 8. Known Limitations

- WeasyPrint is not usable on this Windows box (missing `gobject-2.0-0` / GTK-Pango DLLs); the PDF path therefore always uses the Playwright/Chromium renderer, which provides header/footer/page numbers via Playwright templates. The WeasyPrint CSS `@page` margin-box fallback remains in the template for platforms where WeasyPrint is available.
- The backend must be launched under the `backend\venv` interpreter (or an environment with Playwright installed) for PDF export; launching under a bare Python without Playwright/WeasyPrint causes PDF generation to fail with a clear runtime error.
- Only one real horoscope is currently available for end-to-end validation.
- Pre-existing test `test_report_builder.py::test_extracts_correct_data` still asserts the outdated `client_info` shape (known, tracked separately).

No production blockers.

---

## 9. Engineering Freeze Declaration

GM-017.4 is hereby declared the **production baseline** for the Samartha Vedic AI System Golden Master.

The tag `GM-017.4` (commit `5a0e5883f07f2e8fb54e7167fec2a265d9463c18`) becomes the official recovery point. All protected modules listed in Section 4 are frozen. Subsequent work proceeds from this baseline and must not alter frozen components without an approved engineering change.

Golden Master remains deterministic.
