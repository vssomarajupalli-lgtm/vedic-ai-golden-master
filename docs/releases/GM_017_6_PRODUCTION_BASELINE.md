# Samartha Vedic AI System

## Golden Master

### GM-017.6

### Production Baseline

---

## 1. Release Information

| Field | Value |
|-------|-------|
| Release Name | GM-017.6 — Print/Export Unification & Gochara Mandali Production Baseline |
| Version | GM-017.6 (Golden Master) |
| Date | 2026-08-14 |
| Branch | `main` |
| Commit SHA | `3648766127c0963bd3daab6fca2e93aab62511cf` |
| Git Tag | `GM-017.6` (annotated, re-pointed to this commit) |

---

## 2. Engineering Summary

GM-017.6 completes the Print/Export Unification and the Rāśi-Mandali / Gochara
integration for the Samartha Vedic AI Golden Master. The release establishes the
Gochara/Mandali reporting surface introduced across GM-017.6 Phases 1–4 as part of
the official production baseline, alongside the printing/export refinements that
unify the generated report document.

The work is divided into four phases culminating in a Phase 4 production-safety
pass. Phase 4 tightened report correctness and governance without touching any
engine, formula, or Golden Master calculation: it removed hardcoded/horoscope-specific
fallback behavior, made upcoming-event selection deterministic under a governed
consultation date, corrected strength-grade presentation to use the authoritative
threshold vocabulary, fixed navigation completeness/ordering, normalized Saturn
period terminology, removed duplicate Elinati presentation, and wired the
report-level Gochara Mandali block to real pipeline output.

---

## 3. Completed Milestones

### GM-017.6 Phases 1–4

The GM-017.6 feature branch (`gm-017.6-print-export-unification`) delivered the
following milestones on top of the GM-017.4 baseline (`1729f34`):

- **Print/Export Unification** — completed in commit `43d7b07`
  (`feat: complete GM-017.6 print export unification`).
- **Gochara/Mandali integration checkpoint** — `fc67326`
  (`chore: checkpoint current Gochara Mandali implementation before audit changes`).
- **Gochara Phase 2 reporting/print refinements** — `6acb1df`
  (`feat: Gochara Phase 2 reporting/print refinements (R1, R2, R3, R4, R6)`).
- **Duplicate Elinati presentation removal** — `738cdfa`
  (`fix: remove duplicate Elinati Shani presentation`).
- **MD/AD/PD ↔ Saturn Mandali cross-reference** — `474f019`
  (`feat: add MD AD PD Saturn Mandali cross-reference`).
- **Phase 4 production-safety fixes** — `3648766`
  (`Phase 4 (GM-017.6): Report production-safety fixes`), the final baseline commit.

All phases are complete. Phases 1–3 introduced the Gochara/Mandali report surface
and its print/export presentation; Phase 4 applied the production-safety fixes
described in Section 4.

---

## 4. Major Completed Work

- **Print/export unification** — single shared report presentation path for the
  Gochara/Mandali content consistent with the Print & Export Framework
  established in GM-017.4.
- **Gochara/Mandali integration** — Rāśi-Mandali and Gochara content integrated
  into the report pipeline and report templates, including new report-level and
  Mandali-period presentation components.
- **Rāśi-Mandali Gochar Report B** — report B builder
  (`backend/app/builders/mandali_gochar_builder.py`) plus its schemas
  (`backend/app/schemas/mandali_gochar.py`) and frontend consumers
  (`frontend/src/components/gochara/*`).
- **Saturn resolver-driven Sade Sati** — Sade Sati status and window
  presentation driven by the resolver-based Saturn period data (source of
  truth: `engine_outputs["mandali"]` Saturn periods from the Mandali
  resolver path).
- **Ardha Ashtama Shani** — presented as a discrete Shani period state
  (terminology correction: `Ardha Ashtama Shani`, see R-6 below).
- **Ashtama Shani** — canonical Ashtama Shani event presentation retained.
- **MD/AD/PD ↔ Saturn cross-reference** — Maha Dasha / Antar Dasha / Pratyantar
  Dasha lord alignment with the Saturn period windows
  (`backend/app/builders/dasha_saturn_crossref.py`).
- **Duplicate Elinati presentation/event removal** — Elinati Shani is no longer
  emitted as a duplicate upcoming Mandali event or displayed as a separate
  Saturn period header; only the canonical Ashtama Shani presentation remains
  (R-7 / `738cdfa`).
- **Horoscope-independent DOB handling** — a missing or unparseable DOB produces
  no fabricated Mandali/lifetime advisory; no Raju-specific fallback date exists
  in production code (C-1).
- **Governed target-date determinism** — identical governed consultation date
  yields identical upcoming Mandali events; the governed date is used as the
  anchor and is a real parameter of `UniversalMandaliEngine.generate_mandali_advisory`
  (C-2).
- **Report grade corrections** — house strength grades come from the real engine
  `grade` (no `strength_category`), display labels derive from the single
  authoritative `PROBABILITY_GRADES` vocabulary, and `format_percentage` follows
  the same thresholds (R-1 / R-2).
- **Navigation corrections** — report sidebar navigation entries are present,
  resolve to their section ids, and match document order (R-4).
- **HTML/PDF parity** — report templates render the corrected grades, status
  dots, terminology, and navigation uniformly for HTML and PDF export; the
  shared generated document remains the source of truth for both.

---

## 5. Governance Protections Preserved

| Protection | Status |
|-----------|--------|
| No engine/formula/Golden Master calculation changes for Phase 4 | PRESERVED — Phase 4 (`3648766`) modified presentation, formatting, schemas, templates, pipeline wiring, and tests only |
| Saturn period dates sourced from Mandali resolver | PRESERVED — `engine_outputs["mandali"]` (built in `pipeline_runner.py`) is the resolver-sourced authoritative Saturn period data consumed by `format_gochara_report` |
| No Raju-specific production fallback | PRESERVED — no `14.05.1980` fallback in `pipeline_runner.py`; asserted by `test_no_raju_fallback_in_production_code` |
| Deterministic target-date handling | PRESERVED — governed `target_date_utc` anchor for Upcoming Mandali Events; missing/unparseable DOB yields no fabricated advisory |
| Multi-horoscope independence | PRESERVED — C-1 tests exercise missing/unparseable/unknown DOB against a real fixture without injecting personal data |

---

## 6. Verification Summary

| Area | Status |
|------|--------|
| GM-017.6 targeted suites | PASS — **55 passed** (Phase 4 fixes, Rāśi-Mandali Gochar Report B, MD/AD/PD Saturn cross-reference, frozen transit golden master) |
| Full backend suite | **793 passed / 1 failed / 1 skipped / 217 subtests** |
| Pre-existing failure | PRESERVED, non-blocking — `test_report_builder.py::TestReportBuilder::test_extracts_correct_data` (outdated `client_info` assertion) |
| TypeScript build | PASS — `npx tsc --noEmit` / `tsc -b` (0 errors) |
| Vite build | PASS — `npm run build` (`tsc -b && vite build`) succeeds |
| HTML/PDF validation | PASS — corrected grades, status dots, terminology, and navigation render identically in the shared generated report document |
| Run-time values | Deterministic — governed target date produces identical Upcoming Mandali Events |

---

## 7. Regression Status

Regression verification **passed** (with the single known pre-existing failure
explicitly preserved).

- **GM-017.6 targeted suites (55 passed):**
  - `test_phase4_report_fixes.py` — C-1 DOB fallback removal, C-2 target-date
    determinism, R-1/R-2 grade source/vocabulary, R-3 status dot parsing,
    R-4 navigation completeness/order, R-6 Sani→Shani terminology,
    R-7 Elinati dedup.
  - `test_mandali_gochar_report.py` — Rāśi-Mandali Gochar Report B.
  - `test_dasha_saturn_crossref.py` — MD/AD/PD ↔ Saturn cross-reference.
  - `test_transit_golden_master.py` — frozen Swiss-Ephemeris transit golden
    master (unchanged by this release).
- **Full backend suite:** 793 passed / 1 failed / 1 skipped / 217 subtests.
- **Known pre-existing failure (not part of this release, left untouched):**
  `test_report_builder.py::TestReportBuilder::test_extracts_correct_data` — the
  assertion still expects the outdated `client_info` shape.
- **Frontend:** TypeScript PASS, Vite build PASS.
- **Governance:** no engine, formula, canonical JSON, registry, or Golden Master
  calculation was modified in Phase 4.

---

## 8. Repository Status

| Item | Status |
|------|--------|
| Working Tree | Clean — only this release document (`docs/releases/GM_017_6_PRODUCTION_BASELINE.md`) is untracked, pending the separate documentation commit |
| Branch | `main` |
| Baseline Commit | `3648766127c0963bd3daab6fca2e93aab62511cf` |
| Tag | `GM-017.6` (annotated, re-pointed to `3648766`, pushed to origin) |
| Remote | `origin` — `main` and feature branch synchronized at `3648766`; tag present via `git ls-remote --tags origin` |
| Merge | Clean fast-forward `1729f34..3648766` — no squash, no rewrite; all GM-017.6 commits preserved |

---

## 9. Known Limitations

- **Pre-existing test failure** — `test_report_builder.py::test_extracts_correct_data`
  still asserts the outdated `client_info` shape. It is prior to and unrelated to
  this release, is tracked separately, and was intentionally **not** fixed here.
- **RHVP (Reported-Horoscope Verification Pair)** — future/deferred work. It is
  blocked on owner-provided data: `validation_data/CASE-001` requires a
  `ground_truth.md`, and `validation_data/CASE-002` exists only as an empty
  shell. No RHVP calibration or validation was performed in GM-017.6.
- **Deferred roadmap / optional items (not part of this baseline)** — Model B
  (ephemeris-based Saturn cycle projection), Knowledge Graph platform work
  (BKL-009), the extraction/calibration plan (Shadbala / Bhava Bala / D2–D60),
  and the remaining GM-008 M2–M8 roadmap items. These are not blocked by, and
  were not addressed in, GM-017.6.

---

## 10. Work Status Distinctions

| Category | Scope |
|----------|-------|
| **Completed (GM-017.6)** | Print/export unification; Gochara/Mandali integration; Rāśi-Mandali Gochar Report B; resolver-driven Sade Sati; Ardha Ashtama Shani; Ashtama Shani; MD/AD/PD ↔ Saturn cross-reference; duplicate Elinati removal; horoscope-independent DOB handling; governed target-date determinism; report grade corrections; navigation corrections; HTML/PDF parity (Sections 3–4) |
| **Known pre-existing failure** | `test_report_builder.py::TestReportBuilder::test_extracts_correct_data` — single failing test, preserved, non-blocking, tracked separately |
| **Future / deferred (RHVP)** | `validation_data/CASE-001` ground truth and CASE-002 chart — blocked on owner-provided data; not part of this release |
| **Optional / deferred roadmap** | Model B, KG platform (BKL-009), extraction/calibration plan (Shadbala/Bhava Bala/D2–D60), GM-008 M2–M8 (Section 9) |

---

## 11. Production Baseline Decision

GM-017.6 is hereby declared the **authoritative production baseline** for the
Samartha Vedic AI System Golden Master.

The tag `GM-017.6` (now re-pointed to commit
`3648766127c0963bd3daab6fca2e93aab62511cf`) becomes the official recovery point.
`main` and `origin/main` are synchronized at `3648766`, the working tree is clean,
and the Gochara/Mandali reporting surface delivered across GM-017.6 Phases 1–4 is
part of the frozen baseline. Protected calculation components remain frozen per
the Golden Master governance model; subsequent work proceeds from this baseline
and must not alter frozen components without an approved engineering change.

Golden Master remains deterministic.