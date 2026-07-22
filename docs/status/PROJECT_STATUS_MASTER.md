# Project Status Master

**Last Updated:** 2026-07-22 (GM-007 Phase 2 Deterministic Temporal Propagation)

## Executive Summary
The Vedic AI System has successfully completed:
- **GM-007 Phase 2 (R-1B & R-1C)** — Unified deterministic date propagation across PipelineRunner and JsonNormalizer. Canonical consultation_date now flows through Raw Input → JsonNormalizer → PipelineRunner → QuestionEngine → top_opportunities without dependency on server time.
- **BKL-005B: Formula Calibration Population** — 43/43 formulas calibrated (11 base + 32 child)
- **BKL-005A: Pipeline & Formula Integration** — FormulaEvaluator wired into answer_question()
- **BKL-004: Complete Question Engine** — 83 questions across 13 domains, all 43 formulas reused
- **Formula Calibration Framework** — New calibration layer between Formula Registry (WHAT) and Engine Calibration (HOW)
- **BKL-002: Gochara Integration Verification** — All existing Gochara components verified working (232 tests passing)
- **BKL-001B: Calibration Control Center** — Complete calibration subsystem with Control Plane, profiles, and history

## Revised Project Philosophy (Chief Architect Approved)

**NEW APPROACH: Build First, Validate Later, Calibrate Once**

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
- Validation occurs AFTER the product reaches Feature Complete
- This prevents continuous formula changes, architecture drift, overfitting, and unnecessary repository modifications

## Permanent Engineering Rule
- Implement First → Validate Later → Calibrate Once
- Do NOT modify formulas after every horoscope
- Do NOT change calibration during active development
- Record observations → Complete the product → Batch validation → Controlled calibration

---

## PARAMETER-DRIVEN EVOLUTION (Permanent Engineering Principle)

The deterministic Python engine shall remain stable after Feature Complete.

Future astrological refinement shall be performed through centralized parameter/configuration files wherever technically feasible.

The parameter system should support configuration of:

- Planet Strength factors and weights
- Bhava Strength factors and weights
- Gochara weights
- Formula percentages
- Thresholds
- Enable/Disable
- Add configurable factors
- Remove configurable factors
- Parameter redistribution
- Versioning
- Snapshots
- Restore
- Compare

Default parameter files shall be supplied with the software.

If the user makes no changes, the software shall execute using default values.

If parameter values are modified, the deterministic engine shall automatically use the new values throughout the system, without requiring Python source modifications.

**Engineering Philosophy:**

Build the engine once.
Freeze deterministic logic.
Future research should refine configuration, not implementation.

Validation may continue for months or years.
During that period, knowledge evolves, while the deterministic engine remains stable.

---

## YOGA GOVERNANCE (Final Chief Architect Decision)

**Yoga SHALL NOT participate in deterministic strength calculations.**

Yoga SHALL NOT contribute to:

- Planet Strength
- Bhava Strength
- House Strength
- Rasi Strength
- Dasha
- Gochara
- Ashtakavarga
- Natal Promise
- Master Probability
- Formula Evaluation
- Question Probability

or any deterministic scoring engine.

Yoga SHALL NOT require:

- weights
- percentages
- calibration
- parameter configuration
- future Parameter-Driven Evolution
- or engineering tuning.

---

## NEW ROLE OF YOGA

Yoga becomes an **INFORMATION LAYER ONLY**.

Yoga exists **to inform**, not **to calculate**.

---

## DISPLAY GOVERNANCE

Display ONLY the Yogas that actually exist in the canonical JSON.

Example:

Canonical JSON contains:
- Gaja Kesari Yoga
- Neecha Bhanga Raja Yoga

Display:
Detected Yogas:
- Gaja Kesari Yoga
- Neecha Bhanga Raja Yoga

Do NOT display:
- hundreds of absent Yogas
- False
- No
- Not Present
- Empty
- Cross marks
- Long checklists

If no Yoga exists, display: "No classical Yoga detected." Nothing more.

---

## PARAMETER-DRIVEN EVOLUTION

The following deterministic subsystems remain part of the Parameter-Driven Evolution philosophy:

✓ Planet Strength
✓ Bhava Strength
✓ House Strength
✓ Rasi Strength
✓ Gochara
✓ Dasha
✓ Ashtakavarga
✓ Natal Promise
✓ Master Probability
✓ Formula Calibration
✓ Question Engine

Yoga is intentionally excluded. Yoga is NOT part of Parameter-Driven Evolution.

---

## CONFIGURATION OWNERSHIP PRINCIPLE

Deterministic Python engines own calculations.

Configuration files own parameters.

Configuration SHALL NEVER contain business logic.

Yoga owns neither deterministic calculations nor configurable parameters.

Yoga remains a descriptive information layer.

---

## Phase Status

* **GM-001 through GM-005:** COMPLETE & FROZEN
* **GM-006:** COMPLETE
* **GM-007 (Temporal Determinism): ✅ ALL ITEMS COMPLETE**
  * R-1A (Display Formatter Deterministic Date Architecture): ✅ COMPLETE — NameError resolved, `datetime.now()` fallback removed, canonical `target_date_utc` propagation enforced end-to-end across `format_question_result`, `reports.py`, and `queries.py`.
  * R-1B (Question Engine Deterministic Propagation): ✅ COMPLETE
  * R-1C (JsonNormalizer Consultation Date Preservation): ✅ COMPLETE
* **Backlog Items:**
  * BKL-001A (Calibration Discovery): ✅ COMPLETE
  * BKL-001B (Calibration Control Center): ✅ COMPLETE (49089cc)
  * BKL-002 (Gochara Integration Verification): ✅ COMPLETE (3664e81)
  * BKL-003 (Formula Calibration Framework): ✅ COMPLETE (bd09636)
  * BKL-004 (Complete Question Engine): ✅ COMPLETE (b2f8bc1)
  * BKL-005A (Pipeline & Formula Integration): ✅ COMPLETE (89fb92b)
  * BKL-005B (Formula Calibration Population): ✅ COMPLETE (f967bda)
  * **BKL-005C (System Integration Validation): NEXT**
  * BKL-006 (Desktop Runtime Integration): PENDING
  * BKL-007 (Server Runtime Integration): PENDING
  * BKL-008 (End-to-End Product Completion): PENDING
  * BKL-009 (Release Candidate Build): PENDING
  * BKL-010 (Feature Freeze / Golden Master): PENDING


## Formula Calibration Framework (Architectural Extension)

**Added as calibrated extension to existing Calibration Framework:**

| Component | Status | Details |
|-----------|--------|---------|
| Formula Factor Schema | ✅ | Pydantic model with weight_pct, enabled, engine_required |
| Formula Calibration Section | ✅ | Added to CalibrationProfile (formula_calibration dict) |
| Profile JSON | ✅ | 43 formulas in v1.0_default.json with full factor metadata |
| Automatic Weight Normalization | ✅ | Enabled factors auto-normalize to 100% |
| Engine Integration | ✅ | FormulaEvaluator uses formula_calibration for weighted fulfillment |
| Control Plane | ✅ | get_formula_factors, modify_formula_factor, add/remove_formula_factor |
| Validation | ✅ | Unknown formula/factor rejected, engine_required checked |

**Formulas Implemented (43 of 43 — 100%):**
- 11 Base Formulas (common factors per family)
- 32 Child Formulas (additional factors only — no duplication)
- All weights auto-normalize to 100%

## Question Engine Completion (BKL-004)

**Expanded from 42 to 83 questions across all 13 domains:**

| Domain | Before | After | Life Events Added |
|--------|--------|-------|-------------------|
| Marriage | 3 | 8 | Love Marriage, Arranged Marriage, Second Marriage, Spouse Nature, Married Life |
| Career | 2 | 8 | Government Job, Private Job, Business, Career Change, Foreign Job, Retirement |
| Wealth | 2 | 8 | Investment Timing, Debt Resolution, Loan Recovery, Inheritance, Windfall, Financial Loss |
| Property | 6 | 11 | Land, Apartment, Vehicle, Sale, Inheritance |
| Health | 5 | 8 | Mental Health, Surgery Timing, Specific Disease Risk |
| Children | 3 | 7 | Number of Children, Delay, Child Health, Child Education |
| Education | 6 | 8 | Scholarship, Competitive Exams |
| Litigation | 4 | 6 | Property Litigation, Conflict Resolution Timing |
| Travel | 4 | 6 | Pilgrimage Timing, Business Travel |
| Spirituality | 4 | 7 | Guru/Diksha, Temple Service, Meditation Progress |
| Compatibility | 3 | 6 | Business Partnership, Friendship, Relationship Stability |

**Formula Reuse:** 30/43 leaf formulas used by questions, 0 new formulas created

## Formula Calibration Population (BKL-005B)

**43/43 formulas calibrated (100%) — was 5/43**

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

**Inheritance Verified:** Base formulas contain common factors; Child formulas contain ONLY additional factors — merged and normalized to 100% in FormulaEvaluator.

## Current System State

* **Backend:** Stable. All calibration frameworks, Gochara integration, formula calibration, question engine verified.
* **Test Coverage:** 214 core tests passing (Question Engine + Gochara/Ashtakavarga/Transit), 1 skipped, zero new regressions.
* **Architecture:** FROZEN — No changes without Architecture Review Board approval.
* **Formula Registry:** 43 unique formulas, 11 base + 32 child
* **Question Registry:** 83 questions, all mapped to calibrated formulas
* **Calibration Profiles:** v1.0_default (IMMUTABLE), v1.0_current (mutable), v1.0_frozen (production)

## GM-007 Phase 2 Engineering Handover

**Root Cause Discovered:** During the independent audit, it was discovered that `JsonNormalizer._normalize_metadata()` was actively dropping the canonical `consultation_date`, which starved `PipelineRunner._resolve_target_date_utc()` of the temporal truth and forced an unconditional fallback to the server's physical system clock.

**Verification Process:** A full execution trace confirmed the vulnerability. Verified that restoring the key in `JsonNormalizer` allowed proper propagation to `PipelineRunner` and subsequently to `QuestionEngine.compose_response()`.

**Architecture Decisions:** 
- Unified date extraction into a single `_resolve_target_date_utc()` helper.
- `JsonNormalizer` now acts as a transparent conduit, preserving `consultation_date`.
- `QuestionEngine` is dynamically injected with `target_date_utc`, making `top_opportunities` projections mathematically deterministic and completely independent of the server's execution time.

**Test Results:** 654 tests collected, 653 passed, 0 failed, 1 skipped. No architectural regressions.

**Final Approval & Push Confirmation:** The independent architectural audit issued an APPROVED FOR PUSH verdict. The implementation has been successfully pushed to the remote `main` branch across commits `2aad681a` and `d9d62bc5`. The repository state remains completely clean.

## Next Immediate Goal

**BKL-005C: System Integration Validation** — End-to-end pipeline validation, integration tests for full formula pipeline, prepare for end-to-end product completion (BKL-008).