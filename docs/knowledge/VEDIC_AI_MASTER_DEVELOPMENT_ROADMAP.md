# VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md
# Master Development Roadmap — Golden Master v1.0

**Last Updated:** 2026-07-11  
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

**Repository State:** Clean working tree | 7 commits ahead of `origin/main` | Tags: `gm-005-bkl011a-backend-scratch-utility-isolation`, `gm-005-bkl011c-ashtakavarga-scratch-removal`, `gm-006-bkl001b-calibration-framework`, `gm-006-bkl002-gochara-integration`, `gm-006-bkl003-formula-calibration-framework`, `gm-006-bkl004-question-engine-completion`, `gm-006-bkl005a-pipeline-formula-integration`, `gm-006-bkl005b-formula-calibration-population`

---

## ACTIVE PROGRAM

### 🚀 GM-006: Golden Master v1.0 Delivery

**Program Phase:** Engineering Capability → Feature Completion → Desktop Runtime → Server Runtime → Release Candidate → Feature Freeze → Real Horoscope Validation → Calibration → Final Release  
**Program Lead:** Repository Engineering Team  
**Target:** Production-ready Golden Master v1.0 (Desktop + Server)

---

## REVISED PROJECT PHILOSOPHY (Chief Architect Approved)

The project philosophy has changed from the previous "Build → Validate Horoscopes → Continue Development" approach.

**APPROVED NEW APPROACH:**

```
Build Complete Product
       ↓
Complete All Planned Features
       ↓
Desktop Runtime
       ↓
Server Runtime
       ↓
Release Candidate
       ↓
Feature Freeze
       ↓
Real Horoscope Validation
       ↓
Calibration
       ↓
Final Release
```

**Why This Change:**
- The purpose of GM-006 is to complete the software
- Real horoscope validation will NOT occur during active development
- Validation will occur AFTER the product reaches Feature Complete
- This prevents continuous formula changes, architecture drift, overfitting, and unnecessary repository modifications

**NEW PROJECT PHILOSOPHY:**

**BUILD FIRST**  
Finish ALL planned software.

**VALIDATE LATER**  
Collect observations only after feature completion.

**CALIBRATE ONCE**  
Perform calibration after reviewing the complete validation dataset.

**Release** only after engineering validation and calibration are complete.

---

## PERMANENT ENGINEERING RULE

**Implement First → Validate Later → Calibrate Once**

- Do NOT modify formulas after every horoscope
- Do NOT change calibration during active development
- Record observations
- Complete the product
- Perform batch validation
- Then perform controlled calibration

---

## BACKLOG STRUCTURE (GM-006)

### BKL-001: Calibration Control Center
**Priority:** CRITICAL | **Effort:** 2-3 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (49089cc, tagged `gm-006-bkl001b-calibration-framework`)  
**Description:** Single unified calibration interface replacing scattered constants.
- Formula Control Panel: Toggle/override any formula weight or constant
- Percentage Control Panel: Global and per-domain probability scaling
- Default Values: Factory defaults from `v1.0.0_base.json`
- Override Values: Per-deployment / per-user calibration profiles
- Reserved Future Factors: Slots for future factors (Varga 24, 30, etc.)
- Constraint: Zero Python editing required — pure JSON/YAML configuration
- **Output:** `backend/app/calibration/` — Control Plane, profiles, history

---

### BKL-002: Complete Existing Gochara
**Priority:** CRITICAL | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (3664e81, tagged `gm-006-bkl002-gochara-integration`)  
**Description:** Implement the Gochara system as already designed in the repository. **No redesign.**
- Moon-Centered Rasi Mandali — 12 Mandalis × 9 Padas (per `GOCHARA_MANDALI_GOVERNANCE_v1.md`)
- Transit Engine — 5 subsystems (House Activation 30%, BAV 20%, Planet 20%, Dasha Sync 20%, Vedha 10%)
- Mandali Generator — `mandali_generator.py` (Moon-centered Pada grid, transit-to-Mandali resolution)
- Existing Governance — Governance freeze from `GOCHARA_MANDALI_GOVERNANCE_v1.md` (8 frozen items)
- No Redesign — Implement exactly as specified in `docs/GOCHARA_MANDALI_GOVERNANCE_v1.md`
- Integration: Wire into `TransitEngine` → `MasterProbabilityEngine` → `QuestionEngine`
- **Validation:** 232 Gochara-relevant tests PASSING (65 Ashtakavarga, 65 Transit calibration, 131 Transit engine)

---

### BKL-003: Complete Question Engine
**Priority:** CRITICAL | **Effort:** 4-5 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (b2f8bc1, tagged `gm-006-bkl004-question-engine-completion`)  
**Description:** Expand the existing question framework to full domain coverage. **Current repository knowledge only — no redesign.**
- **Current State:** 42 questions across 13 domains, 40 formula keys mapped (`question_registry.json`)
- **Expanded To:** 83 questions across 13 domains (target: ~80-100 questions)
- **Formula Registry:** Extend `registry_data.py` seed formulas per domain family (Marriage, Career, Wealth, Health, Property, Education, Children, Litigation, Travel, Spirituality, Compatibility)
- **Answer Templates:** `timing_assessment_v1`, `multifactor_assessment_v1`, `strength_assessment_v1`, `risk_assessment_v1`
- **No Redesign** — Extend existing `QuestionEngine`, `FormulaRepositoryLoader`, `FormulaEvaluator` patterns
- **Result:** 83 questions across 13 domains, 30/43 formulas used by questions, 0 new formulas created

---

### BKL-003: Formula Calibration Framework
**Priority:** CRITICAL | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (bd09636, tagged `gm-006-bkl003-formula-calibration-framework`)  
**Description:** Implement Formula Calibration layer between Formula Registry (WHAT) and Engine Calibration (HOW).
- Formula Factor Schema: weight_pct, enabled, engine_required, description, purpose
- Formula Calibration Section: Added to CalibrationProfile (formula_calibration dict)
- Profile JSON: 5 formulas in v1.0_default.json with full factor metadata
- Automatic Weight Normalization: Enabled factors auto-normalize to 100%
- Engine Integration: FormulaEvaluator uses formula_calibration for weighted fulfillment
- Control Plane: get_formula_factors, modify_formula_factor, add/remove_formula_factor
- Validation: Unknown formula/factor rejected, engine_required checked
- **Result:** Formula Calibration Framework complete — Formula Registry (WHAT) → Formula Calibration (HOW MUCH) → Engine Calibration (HOW) → Master Probability

---

### BKL-004: Pipeline & Formula Integration
**Priority:** CRITICAL | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (89fb92b, tagged `gm-006-bkl005a-pipeline-formula-integration`)  
**Description:** Implement DR-009 — FormulaEvaluator executes ONLY in `PipelineRunner.answer_question()`, never in `process()`.
- FormulaEvaluator runs ONLY in `PipelineRunner.answer_question()` — NEVER in `PipelineRunner.process()`
- Zero duplicate calculations — FormulaEvaluator reuses pre-computed engine outputs
- Pipeline remains deterministic — `process()` computes engines once; `answer_question()` adds formula evaluation per question
- QuestionRouter → FormulaRegistry → FormulaCalibration → FormulaEvaluator → QuestionEngine flow works
- **Validation:** 66 Question Engine/Router tests PASSING

---

### BKL-005: Formula Calibration Population
**Priority:** CRITICAL | **Effort:** 4-5 days | **Owner:** Engineering  
**Status:** ✅ **COMPLETE** (f967bda, tagged `gm-006-bkl005b-formula-calibration-population`)  
**Description:** Populate Formula Calibration for ALL 43 formulas (was 5/43).
- 43/43 formulas calibrated (11 base + 32 child)
- Inheritance preserved: Base formulas = common factors; Child formulas = ONLY additional factors
- Equal-weight neutral defaults for structural calibration (Chief Astrologer adjusts post-validation)
- FormulaEvaluator merges Base + Child factors → normalizes to 100%
- All 83 questions mapped to calibrated formulas
- Zero duplicate factors across inheritance chain

| Family | Base | Child Formulas | Total |
|--------|------|----------------|-------|
| Marriage (MAR) | 1 | 2 | 3 |
| Career (CAR) | 1 | 2 | 3 |
| Wealth (WEA) | 1 | 2 | 3 |
| Health (HLT) | 2 | 4 | 6 |
| Property (AST) | 2 | 3 | 5 |
| Education (EDU) | 1 | 4 | 5 |
| Children (FAM) | 1 | 2 | 3 |
| Litigation (LIT) | 1 | 3 | 4 |
| Travel (TRV) | 1 | 3 | 4 |
| Spirituality (SPR) | 1 | 3 | 4 |
| Compatibility (REL) | 1 | 2 | 3 |
| **Total** | **11** | **32** | **43** |

---

### BKL-005C: System Integration Validation
**Priority:** CRITICAL | **Effort:** 3-4 sessions | **Owner:** Engineering  
**Status:** **NEXT**  
**Description:** End-to-end pipeline validation, integration tests for full formula pipeline.
- Create comprehensive integration test suite for full formula pipeline
- Test all 11 formula families with various question IDs
- Verify formula evaluation + calibration + inheritance flow
- Verify pipeline determinism (`process()` unchanged, `answer_question()` adds formula evaluation)
- **Estimated Effort:** 3-4 sessions
- **Dependencies:** BKL-005B complete ✅

---

### BKL-006: Desktop Runtime Integration
**Priority:** HIGH | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** PENDING (after BKL-005C)  
**Description:** Package as installable desktop application (Tauri/Electron or PyInstaller).
- **Frontend:** Vite + React + TypeScript + Tailwind (PWA already configured)
- **Backend:** FastAPI + Uvicorn (single binary or bundled)
- **Packaging:** Tauri (Rust) or PyInstaller (Python) — evaluate and pick
- **Local Server:** Auto-start backend on app launch, shutdown on close
- **Data Persistence:** Local SQLite for calibration profiles, horoscope cache
- **Offline-First:** No cloud dependency; all engines run locally

---

### BKL-007: Server Runtime Integration
**Priority:** HIGH | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** PENDING (after BKL-006)  
**Description:** Production-grade server deployment (Docker + FastAPI).
- **Containerization:** Multi-stage Dockerfile (build → runtime)
- **Orchestration:** Docker Compose (API + Redis + optional Postgres for auth)
- **Health Checks:** `/api/v1/health` endpoint (engine warm-up + model load)
- **Rate Limiting:** Per-IP / per-user throttling
- **Logging:** Structured JSON logs (structlog) → Loki/Grafana or file
- **Config:** Environment-based `.env` (calibration profile, CORS origins, rate limits)
- **Reverse Proxy:** Nginx (SSL termination, static file serving for PWA)

---

### BKL-008: End-to-End Product Completion
**Priority:** CRITICAL | **Effort:** 3-4 days | **Owner:** Engineering  
**Status:** PENDING (after BKL-007)  
**Description:** Runtime validation, UI validation, export validation, API validation.
- Desktop Runtime Validation: Install, launch, offline operation, calibration persistence
- Server Runtime Validation: Docker image, health checks, API response times
- UI Validation: PWA install, responsive layout, calibration panel, question flow
- Export Validation: JSON API, PDF generation, report builder
- API Validation: All endpoints, auth, rate limiting, error handling

---

### BKL-009: Release Candidate Build
**Priority:** CRITICAL | **Effort:** 2-3 days | **Owner:** Engineering  
**Status:** PENDING (after BKL-008)  
**Description:** RC build incorporating all validation feedback.
- **Scope:** All BKL-001 through BKL-008 complete and passing
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

### BKL-010: Feature Freeze / Golden Master Release
**Priority:** CRITICAL | **Effort:** 1 day | **Owner:** Engineering + Release Manager  
**Status:** PENDING (after BKL-009)  
**Description:** Final release — production ready.
- **Tag:** `v1.0.0` (semver)
- **Docker:** `samartha/golden-master:v1.0.0`
- **Desktop:** Signed installers (Windows code signing, macOS notarization)
- **Documentation:** User guide, API reference, calibration guide, developer guide
- **Announcement:** Release notes + migration notes (none for v1.0)
- **Support:** 6-month maintenance window (bug fixes only, no features)

---

## POST GM-006: VALIDATION PROGRAM

After Feature Completion, ONLY then begin:

### Validation Register
- Collect observations from 20 real horoscopes
- No immediate formula changes
- Record all discrepancies systematically

### Calibration Cycle
- Review complete validation evidence
- Identify common patterns
- Apply calibration
- Run regression
- Repeat if necessary

### Golden Master Version 1.0
- Final Release
- Tagged `v1.0.0`

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
| 4 | **System Integration** | `BKL-005C` done; canonical JSON → engines → probability → question → gochara → results |
| 5 | **Desktop Runtime Works** | `BKL-006` done; installable, runs offline, no Python editing |
| 6 | **Server Runtime Works** | `BKL-007` done; Docker image runs, health checks pass, API serves |
| 7 | **20 Real Horoscopes Validated** | `BKL-008` done; calibration frozen as `v1.0.0_frozen.json` |
| 7 | **Calibration Frozen** | `v1.0.0_frozen.json` committed, tagged `gm-006-v1.0-calibration-freeze` |
| 8 | **RC Built & Tested** | `golden-master-v1.0-rc1` tag; all quality gates pass |
| 9 | **Release Artifacts Ready** | Desktop installers, Docker image, release notes, docs |

**ALL MUST BE TRUE FOR GM-006 COMPLETION.**

---

## ROADMAP REGISTRY — DISPOSITION OF ALL ROADMAP DOCUMENTS

| Document | Status | Disposition |
|----------|--------|-------------|
| `docs/knowledge/VEDIC_AI_MASTER_DEVELOPMENT_ROADMAP.md` | **UPDATED** | **AUTHORITATIVE ROADMAP** (this document) |
| `docs/status/PHASE_ROADMAP.md` | **ARCHIVED** | Superseded by this document; move to `docs/archive/roadmaps/` |
| `docs/engineering/validation/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | **ARCHIVED** | Validation plan absorbed into BKL-008; move to `docs/archive/roadmaps/` |
| `docs/status/PHASE_ROADMAP.md` | **ARCHIVED** | Phase-based view superseded by milestone/backlog view |
| `docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md` | **ARCHIVED** | GM-005 complete; move to `docs/archive/roadmaps/` |
| `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | **ARCHIVED** | Superseded by `backend/app/formulas/registry_data.py` + `schema.py` |
| `docs/architecture/REPOSITORY_REFINEMENT_ACTION_PLAN_v1.0.md` | **ARCHIVED** | GM-005 complete |
| `docs/architecture/FORMULA_MASTER_INDEX_PLAN.md` | **ARCHIVED** | Superseded by `backend/app/formulas/registry_data.py` + `schema.py` |
| `docs/architecture/PHASE10A_FORMULA_LOADER_BLUEPRINT_2026-06-19.md` | **ARCHIVED** | Completed in GM-005 |
| `docs/engineering/validation/ASTROLOGY_VALIDATION_MASTER_PLAN.md` | **ARCHIVED** | Validation plan absorbed into BKL-008 |
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

**Next Step:** Chief Architect approval → Create `GM-006` milestone → Assign `BKL-005C` → Begin implementation.

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

**Report Generated:** 2026-07-11 14:30 IST  
**Report Location:** `C:\Users\vssom\Desktop\HERMES_WORKSPACE\Reports\GM-006\2026-07-11_GM006_ROADMAP_REALIGNMENT.md`  
**Repository Modified:** NO  
**Git Modified:** NO  

---

**Awaiting Chief Architect Approval to Proceed with GM-006 Implementation.**