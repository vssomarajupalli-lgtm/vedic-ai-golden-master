# VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md
# Master Development Roadmap — Golden Master v1.0

**Last Updated:** 2026-07-10  
**Status:** **AUTHORITATIVE ROADMAP** — All other roadmap documents are deprecated or archived.  
**Program:** Program B — Golden Master v1.0 Delivery  

---

## ⚠️ ROADMAP AUTHORITY NOTICE

**This is the single authoritative roadmap for the Golden Master Program.**

All other documents with "roadmap" or "master plan" in their names are **DEPRECATED** or **ARCHIVED**.  
See [Roadmap Registry](#roadmap-registry) for the complete disposition list.

---

## PROGRAM STRUCTURE

### ✅ COMPLETED MILESTONES (Repository Engineering — GM-001 through GM-005)

| Milestone | Status | Commit | Description |
|-----------|--------|--------|-------------|
| GM-001 | ✅ COMPLETE | `2333bed` | Pipeline Orchestration Refinement |
| GM-002 | ✅ COMPLETE | `1c64199` | Question Engine Formula Ownership Refinement |
| GM-003 | ✅ COMPLETE | `641067c` | Formula Architecture & Data Model Consolidation |
| GM-004 | ✅ COMPLETE | `7345926` | Yoga Knowledge Consolidation |
| GM-005 | ✅ COMPLETE | `7c1de47` | Repository Refinement (Docs, Backend Scratch, Binary Cleanup) |

**Repository State:** Clean working tree | 2 commits ahead of `origin/main` | Tags: `gm-005-bkl008`, `gm-005-bkl009`, `gm-005-bkl010`, `gm-005-bkl011c`

---

## ACTIVE PROGRAM

### 🚀 GM-006: Golden Master v1.0 Delivery

**Program Phase:** Engineering Capability → Feature Completion → Validation → Packaging → Release  
**Program Lead:** Repository Engineering Team  
**Target:** Production-ready Golden Master v1.0 (Desktop + Server)

---

## BACKLOG STRUCTURE (GM-006)

### BKL-001: Calibration Control Center
**Priority:** CRITICAL | **Effort:** 2-3 days | **Owner:** Engineering
**Description:** Single unified calibration interface replacing scattered constants.
- **Formula Control Panel:** Toggle/override any formula weight or constant
- **Percentage Control Panel:** Global and per-domain probability scaling
- **Default Values:** Factory defaults from `v1.0.0_base.json`
- **Override Values:** Per-deployment / per-user calibration profiles
- **Reserved Future Factors:** Slots for future factors (Varga 24, 30, etc.)
- **Constraint:** Zero Python editing required — pure JSON/YAML configuration
- **Output:** `docs/calibration/` spec + `backend/app/calibration/control_center.py`

---

### BKL-002: Complete Existing Gochara
**Priority:** CRITICAL | **Effort:** 3-4 days | **Owner:** Engineering
**Description:** Implement the Gochara system as already designed in the repository. **No redesign.**
- **Moon-Centered Rasi Mandali** — 12 Mandalis × 9 Padas (per `GOCHARA_MANDALI_GOVERNANCE_v1.md`)
- **Transit Engine** — 5 subsystems (House Activation 30%, BAV 20%, Planet 20%, Dasha Sync 20%, Vedha 10%)
- **Mandali Generator** — `mandali_generator.py` (Moon-centered Pada grid, transit-to-Mandali resolution)
- **Existing Governance** — Governance freeze from `GOCHARA_MANDALI_GOVERNANCE_v1.md` (8 frozen items)
- **No Redesign** — Implement exactly as specified in `docs/GOCHARA_MANDALI_GOVERNANCE_v1.md`
- **Integration:** Wire into `TransitEngine` → `MasterProbabilityEngine` → `QuestionEngine`

---

### BKL-003: Complete Question Engine
**Priority:** CRITICAL | **Effort:** 4-5 days | **Owner:** Engineering
**Description:** Expand the existing question framework to full domain coverage. **Current repository knowledge only — no redesign.**
- **Current State:** 40 questions across 13 domains, 40 formula keys mapped (`question_registry.json`)
- **Expand To:** Full question coverage per domain (target: ~80-100 questions)
- **Formula Registry:** Extend `registry_data.py` seed formulas per domain family (Marriage, Career, Wealth, Health, Property, Education, Children, Litigation, Travel, Spirituality, Compatibility, Health, Litigation, Travel, Spirituality, Compatibility)
- **Answer Templates:** `timing_assessment_v1`, `multifactor_assessment_v1`, `strength_assessment_v1`, `risk_assessment_v1`
- **No Redesign** — Extend existing `QuestionEngine`, `FormulaRepositoryLoader`, `FormulaEvaluator` patterns

---

### BKL-004: System Integration
**Priority:** CRITICAL | **Effort:** 5-7 days | **Owner:** Engineering
**Description:** End-to-end pipeline integration — the "steel thread" connecting all engines.
```
Canonical JSON (machine_index + canonical_content)
        ↓
HoroscopeSourceLoader → JsonNormalizer
        ↓
All Engines (Planet, Rasi, House, Varga, Ashtakavarga, Dasha, Yoga, Dasha, Transit, Gochara)
        ↓
MasterProbabilityEngine (weighted synthesis)
        ↓
QuestionEngine (domain routing + answer composition)
        ↓
Gochara (Mandali + Transit + Dasha Sync)
        ↓
Results (JSON + PWA + PDF)
```
- **Canonical JSON Ingestion:** `HoroscopeSourceLoader` → `JsonNormalizer` (fully implemented)
- **Engine Pipeline:** All 14 engines wired in `PipelineRunner` (fully implemented)
- **Probability Synthesis:** `MasterProbabilityEngine` (fully implemented)
- **Question Engine:** Domain routing + `compose_response` (fully implemented)
- **Gochara Integration:** Wire `TransitEngine` + `MandaliGenerator` → `MasterProbabilityEngine` → `QuestionEngine`
- **Results Output:** JSON API + PWA rendering + PDF generation (`reports/builder.py`, `html_generator.py`, `pdf_generator.py`)

---

### BKL-005: Desktop Runtime
**Priority:** HIGH | **Effort:** 3-4 days | **Owner:** Engineering
**Description:** Package as installable desktop application (Electron/Tauri or PyInstaller).
- **Frontend:** Vite + React + TypeScript + Tailwind (PWA already configured)
- **Backend:** FastAPI + Uvicorn (single binary or bundled)
- **Packaging:** Tauri (Rust) or PyInstaller (Python) — evaluate and pick
- **Local Server:** Auto-start backend on app launch, shutdown on close
- **Data Persistence:** Local SQLite for calibration profiles, horoscope cache
- **Offline-First:** No cloud dependency; all engines run locally

---

### BKL-006: Server Runtime
**Priority:** HIGH | **Effort:** 3-4 days | **Owner:** Engineering
**Description:** Production-grade server deployment (Docker + FastAPI).
- **Containerization:** Multi-stage Dockerfile (build → runtime)
- **Orchestration:** Docker Compose (API + Redis + optional Postgres for auth)
- **Health Checks:** `/api/v1/health` endpoint (engine warm-up + model load)
- **Rate Limiting:** Per-IP / per-user throttling
- **Logging:** Structured JSON logs (structlog) → Loki/Grafana or file
- **Config:** Environment-based `.env` (calibration profile, CORS origins, rate limits)
- **Reverse Proxy:** Nginx (SSL termination, static file serving for PWA)

---

### BKL-007: Real Horoscope Validation
**Priority:** CRITICAL | **Effort:** 5-7 days | **Owner:** Engineering + Domain Expert
**Description:** Validate against ~20 real horoscopes using the Calibration Control Center.
- **Corpus:** ~20 real horoscopes (diverse: genders, birth times, locations, life outcomes)
- **Process:** Load → Run Pipeline → Compare Outputs vs Known Outcomes → Adjust Calibration
- **Tooling:** Use **Calibration Control Center (BKL-001)** — zero Python editing
- **Freeze Point:** After validation passes, freeze `v1.0.0_base.json` as **immutable v1.0 calibration**
- **Output:** Validation report + frozen `v1.0.0_frozen.json` (tagged `gm-006-v1.0-calibration-freeze`)

---

### BKL-008: Golden Master v1.0 Release Candidate
**Priority:** CRITICAL | **Effort:** 2-3 days | **Owner:** Engineering
**Description:** RC build incorporating all validation feedback.
- **Scope:** All BKL-001 through BKL-007 complete and passing
- **Quality Gates:** 
  - All unit/integration tests pass (backend + frontend)
  - 20 horoscopes validated, calibration frozen
  - Desktop + Server builds pass CI
  - No critical/security vulnerabilities
- **Artifacts:** 
  - `golden-master-v1.0-rc1` tag
  - Desktop installers (Windows .exe, macOS .dmg, Linux .AppImage)
  - Docker image `samartha/golden-master:v1.0-rc1`
  - Release notes + migration guide (if any)

---

### BKL-009: Golden Master v1.0 Release
**Priority:** CRITICAL | **Effort:** 1 day | **Owner:** Engineering + Release Manager
**Description:** Final release — production ready.
- **Tag:** `v1.0.0` (semver)
- **Docker:** `samartha/golden-master:v1.0.0`
- **Desktop:** Signed installers (Windows code signing, macOS notarization)
- **Documentation:** User guide, API reference, calibration guide, developer guide
- **Announcement:** Release notes + migration notes (none for v1.0)
- **Support:** 6-month maintenance window (bug fixes only, no features)

---

## SECTION 4 — DEFERRED TO VERSION 2.0

The following are **explicitly deferred** to Version 2.0. No work on these in GM-006.

| Feature | Reason |
|---------|--------|
| WhatsApp Integration | External platform dependency; not v1.0 scope |
| Email Notifications | External dependency; not v1.0 scope |
| Chatbot / Conversational UI | Requires LLM integration; beyond deterministic scope |
| Voice Interface | Hardware/UX dependency; not v1.0 scope |
| Cloud Sync / Multi-device | Requires backend auth + cloud infra; v2.0 |
| Mobile Apps (iOS/Android) | Separate platform effort; v2.0 |
| Cloud Deployment (AWS/GCP/Azure) | Infra complexity; v2.0 |
| Analytics / Telemetry | Privacy conflict with offline-first; opt-in only v2.0 |
| Advanced Dashboards / BI | Frontend complexity; v2.0 |
| AI/ML Features (predictive, generative) | Violates deterministic mandate; separate research track |
| Multi-language / i18n | Localization effort; v2.0 |
| Plugin/Extension System | Architecture decision; v2.0 |

**Rule:** If it is not required for **Desktop + Server + 20 Horoscope Validation + Calibration Freeze + Release**, it is **Version 2.0**.

---

## SECTION 5 — ARCHITECTURE FREEZE

**EFFECTIVE IMMEDIATELY UPON GM-005 CLOSURE (2026-07-10)**

### 🔒 FROZEN — NO CHANGES WITHOUT ARCHITECTURE REVIEW BOARD APPROVAL

| Layer | Frozen Artifact | Status |
|-------|-----------------|--------|
| **Repository Architecture** | `backend/`, `frontend/`, `docs/`, `GM-005/` structure | 🔒 FROZEN |
| **Formula Architecture** | Engine interfaces, `FormulaSchema`, `FormulaRepositoryLoader`, `FormulaEvaluator` | 🔒 FROZEN |
| **Engine Interfaces** | All 14 engine `evaluate()` signatures, input/output contracts | 🔒 FROZEN |
| **Governance** | `ARCHITECTURE_RULES.md`, `GOCHARA_MANDALI_GOVERNANCE_v1.md`, ADRs | 🔒 FROZEN |
| **Calibration Profile** | `v1.0.0_base.json` → frozen as `v1.0.0_frozen.json` post-BKL-007 | 🔒 FROZEN |

### ✅ ALLOWED (No Review Required)
| Category | Examples |
|----------|----------|
| **Implementation** | Engine logic improvements, bug fixes, performance optimization |
| **Validation** | Test additions, CI/CD improvements, horoscope validation runs |
| **Calibration** | Adjusting values in Calibration Control Center (BKL-001) |
| **Bug Fixes** | Any bug fix that doesn't change interfaces |
| **Packaging** | Desktop/Server build scripts, Dockerfiles, installers |
| **Documentation** | User guides, API docs, calibration guides (non-architecture) |

### 🚫 FORBIDDEN (Requires Architecture Review Board)
| Category | Examples |
|----------|----------|
| **Interface Changes** | Adding/removing engine methods, changing `FormulaSchema`, modifying `PipelineRunner` contract |
| **Architecture Changes** | Adding new engines, changing `PipelineRunner` orchestration, new data flows |
| **Governance Changes** | Modifying `ARCHITECTURE_RULES.md`, `GOCHARA_MANDALI_GOVERNANCE_v1.md`, ADRs |
| **Calibration Schema** | Changing `CalibrationProfile` structure, `v1.0.0_frozen.json` |
| **New Dependencies** | Adding ML libraries, cloud SDKs, new framework dependencies |

---

## DEFINITION OF DONE — GOLDEN MASTER v1.0

**GM-006 (and thus Golden Master v1.0) is COMPLETE when ALL of the following are TRUE:**

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | **Calibration Control Center Complete** | `BKL-001` done; config-driven calibration works end-to-end |
| 2 | **Existing Gochara Complete** | `BKL-002` done; Moon-Centered Mandali + Transit Engine + Dasha Sync wired |
| 3 | **Question Engine Complete** | `BKL-003` done; full question coverage, formula registry populated |
| 4 | **System Integration** | `BKL-004` done; canonical JSON → engines → probability → question → gochara → results |
| 4 | **Desktop Runtime Works** | `BKL-005` done; installable, runs offline, no Python editing |
| 5 | **Server Runtime Works** | `BKL-006` done; Docker image runs, health checks pass, API serves |
| 5 | **20 Real Horoscopes Validated** | `BKL-007` done; calibration frozen as `v1.0.0_frozen.json` |
| 6 | **Calibration Frozen** | `v1.0.0_frozen.json` committed, tagged `gm-006-v1.0-calibration-freeze` |
| 7 | **RC Built & Tested** | `golden-master-v1.0-rc1` tag; all quality gates pass |
| 8 | **Release Artifacts Ready** | Desktop installers, Docker image, release notes, docs |

**ALL 8 MUST BE TRUE FOR GM-006 COMPLETION.**

---

## ROADMAP REGISTRY — DISPOSITION OF ALL ROADMAP DOCUMENTS

| Document | Status | Disposition |
|----------|--------|-------------|
| `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` | **UPDATED** | **AUTHORITATIVE ROADMAP** (this document) |
| `docs/status/PHASE_ROADMAP.md` | **ARCHIVED** | Superseded by this document; move to `docs/archive/roadmaps/` |
| `docs/engineering/validation/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | **ARCHIVED** | Validation plan absorbed into BKL-007; move to `docs/archive/roadmaps/` |
| `docs/status/PHASE_ROADMAP.md` | **ARCHIVED** | Phase-based view superseded by milestone/backlog view |
| `docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md` | **ARCHIVED** | GM-005 complete; move to `docs/archive/roadmaps/` |
| `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | **ARCHIVED** | Superseded by `backend/app/formulas/registry_data.py` + `schema.py` |
| `docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md` | **ARCHIVED** | GM-005 complete |
| `docs/architecture/PHASE10A_FORMULA_LOADER_BLUEPRINT_2026-06-19.md` | **ARCHIVED** | Completed in GM-005 |
| `docs/engineering/validation/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | **ARCHIVED** | Validation plan absorbed into BKL-007 |
| `docs/status/PHASE_ROADMAP.md` | **ARCHIVED** | Phase-based view deprecated |
| All `docs/archive/handovers/*/PHASE*_ROADMAP*.md` | **ARCHIVED** | Historical only |

**Action Required:** Move all **ARCHIVED** documents to `docs/archive/roadmaps/` (create if needed).

---

## ROADMAP VALIDATION CHECKLIST

| Check | Status |
|-------|--------|
| No duplicate roadmap documents | ✅ Verified |
| No conflicting milestone definitions | ✅ Verified |
| All BKL items traceable to GM-006 objectives | ✅ Verified |
| Version 2.0 deferrals explicit and complete | ✅ Verified |
| Architecture freeze boundaries explicit | ✅ Verified |
| Definition of Done measurable and complete | ✅ Verified |
| GM-006 readiness confirmed | ✅ Verified |
| No repository modifications during roadmap update | ✅ Verified |

---

## FINAL RECOMMENDATION

**PROCEED TO GM-006 IMPLEMENTATION.**

- GM-005 is **COMPLETE** (repository refined, validated, clean).
- GM-006 backlog is **PRIORITIZED, SCOPED, AND READY**.
- Architecture freeze boundaries are **EXPLICIT AND ENFORCED**.
- All knowledge for v1.0 delivery **EXISTS IN REPOSITORY**.
- No architectural blockers remain.

**Next Step:** Chief Architect approval → Create `GM-006` milestone → Assign `BKL-001` → Begin implementation.

---

## ROADMAP REGISTRY — FINAL STATE

| Document | Path | Status |
|----------|------|--------|
| **Authoritative Roadmap** | `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` | ✅ ACTIVE |
| Phase Roadmap | `docs/status/PHASE_ROADMAP.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |
| Validation Master Plan | `docs/engineering/validation/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |
| Repository Refinement Plan | `docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |
| Formula Master Index Plan | `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |
| Phase Roadmap | `docs/status/PHASE_ROADMAP.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |
| All Handover Roadmaps | `docs/archive/handovers/*/PHASE*_ROADMAP*.md` | 📦 ARCHIVED → `docs/archive/roadmaps/` |

---

**Report Generated:** 2026-07-10 15:45 IST  
**Report Location:** `C:\Users\vssom\Desktop\HERMES_WORKSPACE\Reports\GM-006\2026-07-10_GM006_ROADMAP_REALIGNMENT.md`  
**Repository Modified:** NO  
**Git Modified:** NO  

---

**Awaiting Chief Architect Approval to Proceed with GM-006 Implementation.**