# SAMARTHA VEDIC AI GOLDEN MASTER — 3-FORMULA DEEP AUDIT REPORT
**Report ID:** GM-AUDIT-2026-08-18-3FMLA
**Mode:** READ-ONLY (no files modified, no staging, no commits, no push)
**Authority:** VEDIC_AI_MASTER_ARCHITECTURE.md · FORMULA_GOVERNANCE_v1.0.md · v1.0_current.json · canonical Raju horoscope · current test suite
**Outcome:** AUDIT COMPLETE / EVIDENCE RECORDED / IMPLEMENTATION PENDING APPROVAL

---

## Section 1 — Audit Objective and Authority
Verify Formulas A (Planet Strength), B (Natal Promise), C (Master Probability) end-to-end — governance → calibration → engine → report → frontend — against current code, current tests, current calibration profile, and the canonical Raju horoscope. Only the three governed formulas and their deployment path are in scope. Findings are proven from current artifacts, never assumed from old documents. Ambiguities are recorded as "GOVERNANCE DECISION REQUIRED".

## Section 2 — Read-Only Compliance Statement (verbatim rule)
No file modifications; no staging; no commits; no push; no reset; no checkout; no cleanup of unrelated work. Defects are registered, never fixed. Final outcome must be AUDIT COMPLETE / EVIDENCE RECORDED / IMPLEMENTATION PENDING APPROVAL, with "Implementation required — awaiting user approval." for any defect. All evidence scripts were written outside the repo (`C:\Users\vssom\AppData\Local\Temp\opencode\`). No repo file was touched.

## Section 3 — Git State and Change Control
- Branch: `main`
- HEAD: `a29a38013c41ed2418d9f95d6249fedf7df25d78` — "feat: add single-click batch horoscope report launcher"
- Log-5: `a29a380` (current HEAD), `89cead8` (GM-013B phase 6 validation evidence), `e68d952` (South Indian charts), `1a61255` (restore explanations endpoint runtime), `a934204` (GM-017.6 Saturn lifetime)
- Pre-existing owner WIP (present at audit start, untouched by audit): `M frontend/src/components/GocharaTab.tsx`, `M frontend/src/components/consultation/ConsultationWorkspace.tsx`, `?? frontend/src/components/charts/`
- Audit introduced zero changes: `git status` delta attributable to this audit = none.

## Section 4 — Governance Document Inventory and Current-Version Rationale
| Document | Version/Status | Role in this audit | Current-version rationale |
|---|---|---|---|
| `docs/knowledge/VEDIC_AI_MASTER_ARCHITECTURE.md` | current (58 lines) | Source reference for Master weights 40/15/10/10/10/10/5 | Cited by Formula C docstring as the weight authority |
| `docs/governance/FORMULA_GOVERNANCE_v1.0.md` | v1.0 | Evaluate-once/consume-many; strict reuse; no semantic formulas | Governing constitution for formula deployment |
| `docs/architecture/FORMULA_REPOSITORY_DATA_MODEL_v1.md` | v1 | Data model for formula repository | Structural authority |
| `docs/architecture/FORMULA_OWNERSHIP_MAPPING_v1.0.md` | DRAFT | One formula, one owner registry: Planet Strength → Planet Engine (consumers House/Yoga/Varga/Dosha) | Status DRAFT noted — ownership mapping not finalized |
| `docs/status/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | v1.0 | Engine ownership + data contracts | Registry authority |
| `docs/architecture/decisions/ADR-001..016` | mixed (Accepted + Proposed) | ADR-003 (no hardcoded rules), ADR-004 (no Promise+Dasha+Transit aggregation), ADR-008 (evaluate once) bind the formulas | ADR-004/Accepted directly tensions Formula C aggregation; no superseding ADR found (see §17) |
| `backend/app/calibration/profiles/v1.0_current.json` | v1.0.0, IMMUTABLE, profile_id v1.0_default | The live calibration used by all engines at runtime | Only profile with status IMMUTABLE selected as current by CalibrationManager |
| `docs/governance/CALIBRATION_DEPENDENCY_MAP_v1.md`, `CALIBRATION_CONSTANT_INVENTORY_v1.md`, `docs/knowledge/CALIBRATION_FRAMEWORK_KNOWLEDGE_PACKAGE.md` | current | Calibration governance cross-reference | Calibration constants authoritative |
| `docs/rhvp/CALIBRATION_CANDIDATE_REGISTER.md`, `GOLDEN_MASTER_V1.0_HANDOVER.md`, `VERSION_1_0_RELEASE_ACCEPTANCE_REPORT.md`, `GM_013_RELEASE_CANDIDATE_READINESS_REPORT.md` | current | Release/handover context | Context only; not used to prove pass/fail |
| **No `FORMULA_REPOSITORY_DATA_MODEL`/`*PARAMETER*` governance md exists** | — | Absence registered — parameter-driven governance file is missing | The mandated data model doc reference gap |

## Section 5 — Scope
**In scope:** Formula A (Planet Strength), Formula B (Natal Promise), Formula C (Master Probability); deployment path proving them (charts endpoint, reports builder, HTML/PDF generators, frontend display).
**Out of scope (verified absent from this audit):** Gochara/Mandali, frontend redesign, formula enhancement, calibration change, HoroscopeCleaner extraction, SAV extraction, English template work, START.bat, Knowledge Graph, AI explanation layer, deployment backlog. No analysis or changes applied to these.

## Section 6 — Evidence Base
- Audit scripts (outside repo): `audit_verify.py`, `audit_determinism.py`, `audit_planets.py`, `audit_calib_runtime.py`, `audit_domains.py`.
- Canonical input: `extracted_json/raju_canonical_content.json` (houses 2,3,4,6,8,9,10,11,12 — **missing 1,5,7**; planets sun..ketu) + `raju_machine_index.json`.
- Test baseline: 826 passed, 1 skipped, 217 subtests (recorded). Focus suites re-run this audit: 81 passed (planet 36+?; natal + master) in 1.26s — see per-formula sections.
- All JSON/calibration reads executed with `backend/venv/Scripts/python.exe` (PowerShell `ConvertFrom-Json` is broken on duplicated `vedha_pairs`/`VEDHA_PAIRS` keys).

---

# FORMULA A — PLANET STRENGTH (sections A.1–A.20)

## Section 7 — Formula A Governance and Ownership
- Owner per FORMULA_OWNERSHIP_MAPPING_v1.0.md (DRAFT): Planet Engine → `backend/app/engines/planet_strength_engine.py`; consumers House/Yoga/Varga/Dosha.
- Calibration source: `calibration.planet_strength.get('PLANET_SCORING_MATRIX')`; per-parameter weight_pct from `active_profile["sections"]["planet_strength"]["parameters"][param]["weight_pct"]/100`; fallback defaults `_get_weight(param, 0.25/0.20/0.15/0.10/0.10/0.05/0.10/0.05)`.

## Section 8 — Formula A Calibration → Engine → Runtime Chain
Verified at runtime (audit_calib_runtime.py): JSON `weight_pct` = dignity 25.0, house_placement 20.0, aspects 15.0, conjunctions 10.0, combustion 10.0, retrogression 5.0, shadbala 10.0, varga_dignity 5.0 (total 100.0). Engaged `_get_weight('dignity',0.25)=0.25`; `('house_placement',0.20)=0.20`; `('varga_dignity',0.05)=0.05`. Engine weights dict keys include PLANET_SCORING_MATRIX, NATURAL_BENEFICS, NATURAL_MALEFICS. Calibration is the runtime source of truth; fallback defaults are never reached under v1.0_current.

## Section 9 — Formula A Deep Verification (A.1–A.20)
- **A.1 Governed weight set:** CALIBRATION_CONSTANT_INVENTORY_v1.md governs the 8-factor weight set (25/20/15/10/10/5/10/5). Exact.
- **A.2 Calibration stores the set:** `v1.0_current.json` section `planet_strength` — `total_weight_pct: 100.0`; parameters per above. Exact.
- **A.3 Engine consumes the set:** `_get_weight` reads `weight_pct/100` from active profile. Exact.
- **A.4 Runtime consumes the set:** proven live values above. Exact (i.e., Governed == Calibration == Engine == Runtime for all 8 factors).
- **A.5 Matrix dignity (governed):** exalted=100/own_sign=80/friendly=60/neutral=50/enemy=20/debilitated=0 in `PLANET_SCORING_MATRIX.dignity`. Exact.
- **A.6 Matrix house_placement:** trikona=100/kendra=90/upachaya=70/neutral=50/dusthana=10. Exact.
- **A.7 Matrix state_modifiers:** combust_score=0 when combust (else 100); retrograde_score=100 when retro (else 50). Exact.
- **A.8 Matrix aspects:** benefic +25, malefic −25 anchored at 50. Exact.
- **A.9 Matrix conjunctions:** benefic +25, malefic −25. Exact.
- **A.10 Aggregation math:** `score = Σ weight_f × factor_f`; `base_score = round(score)`; BAV modifier applied at pipeline Step 7.5; `final_score = clamp(base_score + bav, 0, 100)`; `clamp_score` returns int. Exact.
- **A.11 Real-chart weight contribution (Raju jupiter):** dignity 12.5 (score 50), house 10.0 (50), aspects 7.5 (50), conjunctions 5.0 (50), combustion 10.0 (100/not combust), retrogression 2.5 (50/not retro), shadbala 5.2385 (score 52.385), varga_dignity 2.5 (50). Raw = 55.2385 → base 55 → BAV +5 → final 60. Independent recomputation matches. Exact.
- **A.12 Real-chart mercury:** raw 70.81975 → 71, BAV 0; saturn raw 45.213 → 45, BAV −5 → 40. Matches.
- **A.13 Grade/clamp:** final bounded 0..100 integer. Exact.
- **A.14 Duplicate implementation:** factor names + weight literals appear only in the canonical engine + calibration accessor; no duplicate. Exact.
- **A.15 Test coverage:** `test_planet_strength_engine.py` (181L) asserts exact dignity/house/aspect contributions and missing-data neutral=55. Caveat found: stale comments cite kendra=100 while matrix says 90 — comment-only drift (registered, no math impact).
- **A.16 Test result:** formula suites re-run — all pass (see §11 for tallies).
- **A.17 Traceability provenance:** engine emits only `{"entity_id","entity_type"}`; DisplayFormatter defaults engine_name="Unknown" → report trace shows Unknown (v1.0), weight 1.0, contribution=raw_value (defect TR-001, display-only).
- **A.18 Frontend value used:** final_score and breakdown (display-only; Math.round only for % rendering). No recomputation. Exact.
- **A.19 ADR-003 (no hardcoded rules):** matrix and weights are calibration-driven; fallback literal constants remain in code (deviation PARAM-001 driver, see §24). Partial.
- **A.20 Maturity:** Formula A math = PASS; provenance/display fidelity = DEFECT; parameter-readiness = YES (§25).

## Section 10 — Formula A Real-Chart Verification
Verified against canonical Raju horoscope. All 9 planets' final scores reproduced via independent recomputation (jupiter 60, mercury 71, saturn 40, venus 61, sun 49, ketu 58, mars 55 — plus internal fuel for B/C). Matched.

## Section 11 — Formula A Test Evidence
`tests/test_planet_strength_engine.py` included in the 81-test focused run; all passed. Full suite baseline per governance log: 826 passed / 1 skipped / 217 subtests.

## Section 12–13 reserved (Formula A roll-up):
Formula A status: **PASS (math)** + defects DM-001 (data source, see §23), TR-001 (traceability, §32). No formula deviation found.

---

# FORMULA B — NATAL PROMISE (sections B.1–B.20)

## Section 14 — Formula B Governance and Ownership
- Owner: `backend/app/engines/natal_promise_engine.py`. Calibration: loads `DOMAIN_CONFIG`, `DOMAIN_KARAKA`, `NATAL_PROMISE_GRADES`, `DOMAIN_BONUSES` (from calibration.natal_promise) and `SIGN_LORD_MAP` (from calibration.rasi_strength).
- Governed weights: `PROMISE_ENGINE_FORMULA_v1.md` OUTER WEIGHTS = 35/30/20/15 (bhava/bhavadhipati/karaka/varga). Grade ladder: STRONG ≥70, MODERATE ≥50, WEAK ≥30, PRESENT ≥0.

## Section 15 — Formula B Calibration → Engine → Runtime Chain
Runtime proof (audit_calib_runtime.py): DOMAIN_CONFIG wealth weights = {"bhava":0.35,"bhavadhipati":0.3,"karaka":0.2,"varga":0.15}; engine config identical. DOMAIN_KARAKA wealth {primary jupiter, secondary venus}; marriage {primary venus, secondary jupiter}; spirituality {primary jupiter, secondary ketu}. `engine.config[n]["weights"] == calibration` — True. NATAL_PROMISE_GRADES = [[70,STRONG],[50,MODERATE],[30,WEAK],[0,PRESENT]].

## Section 16 — Formula B Deep Verification (B.1–B.20)
- **B.1 Governed outer weights:** 35/30/20/15 (PROMISE_ENGINE_FORMULA_v1.md). Exact.
- **B.2 Calibration stores them:** `natal_promise.DOMAIN_CONFIG[*].weights`. Exact.
- **B.3 Engine consumes them:** `npe.config`. Exact.
- **B.4 Runtime consumes them:** live proof above. Exact (Governed == Calibration == Engine == Runtime).
- **B.5 Bhava score:** mean of primary-house final_scores (present houses only; absent → neutral 50.0). Weight 0.35. Exact.
- **B.6 Bhavadhipati score:** lord planet final of primary house (house absent → neutral 50.0). Weight 0.30. Exact.
- **B.7 Karaka score:** primary karaka planet final; secondary blended ONLY for education (0.60/0.40), children (0.70/0.30), property (0.60/0.40), health (0.60/0.40). Weight 0.20. ← See DEV-002.
- **B.8 Varga score:** final_score of the domain varga chart planet (absent → neutral 50.0). Weight 0.15. Exact.
- **B.9 Aggregation:** `raw = 0.35·bhava + 0.30·bhavadhipati + 0.20·karaka + 0.15·varga`; `score = round(raw)`; grade via ladder from calibration. Exact.
- **B.10 Wealth trace (Raju):** bhava = (H2 48 + H11 42)/2 = 45.0; bhavadhipati = mercury 71 (lord of H2); karaka = jupiter 60 (primary-only — wealth blend NOT applied); varga = D2 jupiter 50.0. raw = 15.75+21.30+12.00+7.50 = 56.55 → round 57 → MODERATE. Independent recomputation exact-match, including the blend question (if secondary venus 61 had applied 0.6/0.4, karaka would be 60.4 → raw 56.63 → still 57; **same rounded score, different raw** — registered).
- **B.11 Marriage trace (Raju):** H7 absent in canonical source → bhava neutral 50.0; bhavadhipati neutral 50.0 (lord unresolved); karaka = venus 61 (primary-only); varga = D9 venus 55.0. raw = 17.50+15.00+12.20+8.25 = 52.95 → round 53 → MODERATE. Exact-match (aggregate). Blend deviation registered: DOMAIN_KARAKA declares secondary jupiter but marriage is primary-only; secondary blend would give karaka 60.6 → raw 52.92 → still 53 (same rounded score).
- **B.12 Spirituality trace (Raju):** bhava = (H9 38 + H12 42)/2 = 40.0; bhavadhipati = mars 55 (lord of H9 = mars — verified raw H9 lord mars, mars final 55); karaka = jupiter 60 (primary-only); varga = D20 jupiter 50.0. raw = 14.00+16.50+12.00+7.50 = 50.00 → round 50 → MODERATE. Exact-match. Blend deviation: secondary ketu declared; primary-only → 60 (blend would be jupiter 60.0/ketu 58 → 59.2 → raw 49.8 → still 50).
- **B.13 Exhaustive wealth/marriage/spirituality reconciliation:** All three domains recomputed exactly from current code; aggregate scores match the engine; the only divergence is the karaka secondary blend, which changes raw by <0.2 and never the rounded score for this chart. Registered as DEV-002 (governance/declarative-intent mismatch, zero math impact on current canonical input).
- **B.14 Missing-house data coupling:** bhava/bhavadhipati neutral fallback for health/marriage/children occurs because the canonical Raju source lacks houses 1,5,7 — same phenomenon as Formula A/Formula C house population. Registered as DM-001/DM-002 (data-source, see §23).
- **B.15 Test coverage:** `test_natal_promise_engine.py` (347L) covers primary houses/karaka blends/lord read/varga charts/contribution deltas (tolerance 2.0)/grade thresholds.
- **B.16 Test result:** passed in focused 81-test run.
- **B.17 Traceability provenance:** natal-promise report traces also render Unknown (v1.0), weight 1.0 (defect TR-001).
- **B.18 Frontend/report value:** `report["natal_promise"]` and breakdowns rendered; no recomputation. Exact.
- **B.19 ADR-003:** weights/blends live in calibration; the blend-map for the four blended domains is engine logic (deviation PARAM-001 driver, §24). Partial.
- **B.20 Maturity:** Formula B math = PASS; karaka-blend governance mismatch = DEFECT (DEV-002); parameter-readiness = YES (§25).

## Section 17 — Formula C (ADR-004 governance note shared): see Formula C sections.

---

# FORMULA C — MASTER PROBABILITY (sections C.1–C.20)

## Section 18 — Formula C Governance and Ownership
- Owner: `backend/app/engines/master_probability_engine.py`. `MASTER_WEIGHTS` constant = natal_promise 0.40, planet_strength 0.15, house_strength 0.10, rasi_strength 0.10, varga_validation 0.10, dasha_activation 0.10, transit_trigger 0.05 (docstring cites VEDIC_AI_MASTER_ARCHITECTURE.md). `_STUB_SCORE = 50.0`. Dasha factor = 0.60×MD + 0.40×AD.
- **ADR-004 tension (accepted, not superseded):** ADR-004 (Accepted) forbids flattening Promise + Dasha + Transit into one score; Formula C aggregates natal_promise (0.40) + dasha_activation (0.10) + transit_trigger (0.05). MASTER_PROBABILITY_KNOWLEDGE_PACKAGE §11 documents the master engine as the sole canonical synthesis boundary — a plausible sanctioned exception — but NO ADR amendment/supersession exists. **Determination: GOVERNANCE DECISION REQUIRED** (reconcile ADR-004 vs sanctioned master synthesis; amend ADR-004 or scope the exception explicitly). Recommendation: formally register the master engine as the ADR-004-recognized single synthesis owner.

## Section 19 — Formula C Calibration → Engine → Runtime Chain
Runtime proof: `calibration.master_probability.get('MASTER_WEIGHTS')` = {"natal_promise":0.4,"planet_strength":0.15,"house_strength":0.1,"rasi_strength":0.1,"varga_validation":0.1,"dasha_activation":0.1,"transit_trigger":0.05}; `engine.weights == calibration.master_probability['MASTER_WEIGHTS']` — **True**. `engine.weights` is populated from the calibration accessor (`self.weights = calibration.master_probability.get('MASTER_WEIGHTS', {})`), NOT from the module constant; `self.stub = _STUB_SCORE` (50.0). PROBABILITY_GRADES = [[80,EXCELLENT],[65,VERY GOOD],[50,GOOD],[35,WEAK],[0,TOO WEAK]]. Section key is `probability` (not `master_probability`).

## Section 20 — Formula C Deep Verification (C.1–C.20)
- **C.1 Governed weight set:** VEDIC_AI_MASTER_ARCHITECTURE.md 40/15/10/10/10/10/5 (percent) = 0.40/0.15/0.10/0.10/0.10/0.10/0.05. Exact.
- **C.2 Calibration stores them:** `probability.parameters.weights` current_value = EXACTLY 0.4/0.15/0.1/0.1/0.1/0.1/0.05; grades EXCELLENT 80 / VERY_GOOD 65 / GOOD 50 / WEAK 35 / TOO_WEAK 0; stub_score 50.0. Exact.
- **C.3 Calibration accessor maps:** `CalibrationManager.master_probability` (lines 432–439) returns `MASTER_WEIGHTS` from `sections["probability"]["parameters"]["weights"]`. Exact.
- **C.4 Engine consumes accessor:** `self.weights = calibration.master_probability.get('MASTER_WEIGHTS', {})` at __init__ (line 50). Exact.
- **C.5 Runtime consumes accessor:** `engine.weights == calibration` — True (proven). Exact.
- **C.6 Hardcoded constant role:** module-level `MASTER_WEIGHTS` constant is documentation/fallback only; runtime uses calibration. ADR-003 partial compliance (constant literal persists) — registered PARAM-001.
- **C.7 Aggregation math:** `raw = Σ weight_i × factor_i`; `final = round(raw)`; grade from calibration PROBABILITY_GRADES; clamp 0..100. Exact.
- **C.8 Factor — natal_promise:** weighted mean of the 8 domain scores = 51.88 (Raju). ×0.40 → 20.752. Exact (matches audit_verify independent recomputation).
- **C.9 Factor — planet_strength:** mean of 9 planet final_scores = 56.56. ×0.15 → 8.484. Exact.
- **C.10 Factor — house_strength:** mean of 9 present houses = 42.89. ×0.10 → 4.289. Exact.
- **C.11 Factor — rasi_strength:** mean of 12 rasi scores = 34.17. ×0.10 → 3.417. Exact.
- **C.12 Factor — varga_validation:** 50.0 (no net modifiers). ×0.10 → 5.000. Exact.
- **C.13 Factor — dasha_activation:** 41 = round(0.60×MD + 0.40×AD) with MD=AD fallback when AD absent. ×0.10 → 4.100. Exact.
- **C.14 Factor — transit_trigger:** 59.0. ×0.05 → 2.950. Exact.
- **C.15 Total:** 20.752+8.484+4.289+3.417+5.000+4.100+2.950 = 48.992 → round 49 → grade WEAK. Independent Σ contribution×weight exact-match. Equal-weight mean 47.93→48 is NOT the governing formula. Exact.
- **C.16 Determinism:** two PipelineRunner runs on identical Raju payload + fixed target_date_utc → `engine_outputs` deep-identical; master 49/48.992/WEAK both runs. Exact.
- **C.17 Test coverage:** `test_master_probability_engine.py` (375L) — output schema, weights, weighted-sum exact, round, grade, clamp, MD-AD 60/40. Exact.
- **C.18 Test result:** passed in focused 81-test run.
- **C.19 Deployment parity:** `charts.py` places `master_probability` + nested `engine_outputs` into `breakdown`; `reports/builder.py` builds `master_summary={final_score,grade}`; raw/breakdown/weights retained under `formula_verification=pipeline_outputs` but NOT in `master_summary` (raw/breakdown/weights intentionally omitted). No downstream recomputation. Frontend reads `rawOutputs.breakdown.master_probability.{final_score,breakdown,grade}` display-only. Exact.
- **C.20 Maturity:** Formula C math = PASS; ADR-004 reconciliation = GOVERNANCE DECISION REQUIRED; traceability = DEFECT TR-001; parameter-readiness (natal_promise weight) = YES (§25).

## Section 21 — Formula C (and B/A) Deployment Path Proof
PipelineRunner → charts.py builds ChartProcessResponse (breakdown=outputs, master_probability, nested engine_outputs) → reports/builder.py (master_summary final_score/grade + natal_promise + strength_scores; formula_verification holds pipeline outputs) → reports.py endpoint `_filter_report_sections` removes only top-level presentation keys → HTML/PDF via HTMLGenerator/PDFGenerator with DeterministicExplanation. Frontend: `rawOutputs.breakdown.*` display-only; Math.round reserved for % presentation. No recomputation anywhere downstream. Exact.

---

## Section 22 — MASTER FORMULA WEIGHT TABLE (mandated)
| Formula | Component | Governed Weight | Calibration Weight | Engine Weight | Actual Runtime Weight | Strength Source | Contribution (Raju) | Total | Rounding | Clamp | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A Planet Strength | dignity | 25% | 25.0 | 0.25 | 0.25 | jupiter dignity 50 | 12.5 | 55.2385 raw | base 55 | 0..100 | PASS |
| A | house_placement | 20% | 20.0 | 0.20 | 0.20 | 50 | 10.0 | | | | PASS |
| A | aspects | 15% | 15.0 | 0.15 | 0.15 | 50 | 7.5 | | | | PASS |
| A | conjunctions | 10% | 10.0 | 0.10 | 0.10 | 50 | 5.0 | | | | PASS |
| A | combustion | 10% | 10.0 | 0.10 | 0.10 | 100 (not combust) | 10.0 | | | | PASS |
| A | retrogression | 5% | 5.0 | 0.05 | 0.05 | 50 (not retro) | 2.5 | | | | PASS |
| A | shadbala | 10% | 10.0 | 0.10 | 0.10 | 52.385 | 5.2385 | | | | PASS |
| A | varga_dignity | 5% | 5.0 | 0.05 | 0.05 | 50 | 2.5 | | | | PASS |
| **A jupiter final** | BAV +5 | — | — | — | — | 55→60 (25/20/15/10/10/5/10/5 of 100) | Σ=55.2385 | 55→60 | round | clamp int | **PASS** |
| B Natal Promise | bhava | 35% | 0.35 | 0.35 | 0.35 | wealth bhava 45.0 | 15.75 | 56.55 raw | round 57 | ladder | PASS |
| B | bhavadhipati | 30% | 0.30 | 0.30 | 0.30 | mercury 71 | 21.30 | | | | PASS |
| B | karaka | 20% | 0.20 | 0.20 | 0.20 | jupiter 60 (primary-only) | 12.00 | | | | PASS (blend DEV-002) |
| B | varga | 15% | 0.15 | 0.15 | 0.15 | D2 jupiter 50 | 7.50 | | | | PASS |
| **B wealth final** | grade | — | — | — | — | 57 (MODERATE) | Σ=56.55 | 57 | round | ladder | **PASS** |
| C Master | natal_promise | 40% | 0.40 | 0.40 | 0.40 | 51.88 | 20.752 | 48.992 raw | round 49 | 0..100 | PASS |
| C | planet_strength | 15% | 0.15 | 0.15 | 0.15 | 56.56 | 8.484 | | | | PASS |
| C | house_strength | 10% | 0.10 | 0.10 | 0.10 | 42.89 | 4.289 | | | | PASS |
| C | rasi_strength | 10% | 0.10 | 0.10 | 0.10 | 34.17 | 3.417 | | | | PASS |
| C | varga_validation | 10% | 0.10 | 0.10 | 0.10 | 50.0 | 5.000 | | | | PASS |
| C | dasha_activation | 10% | 0.10 | 0.10 | 0.10 | 41 (60/40 MD/AD) | 4.100 | | | | PASS |
| C | transit_trigger | 5% | 0.05 | 0.05 | 0.05 | 59.0 | 2.950 | | | | PASS |
| **C master final** | grade | — | — | — | — | 49 (WEAK) | Σ=48.992 | 49 | round | clamp | **PASS** |

---

## Section 23 — DEVIATION REGISTER (mandated)
| DEV-ID | Formula | Severity | Location | Expected | Existing | Evidence | Math Impact | Display Impact | Governance Impact | Recommendation | Implementation Required? | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DM-001 | A,B,C | Medium | `raju_canonical_content.json` (9 houses; missing 1,5,7) | 12-house canonical | 9 houses | §6; §10; §16 B.14; §20 C.10 (mean over 9) | Real: house-strength mean 42.89 over 9 vs over 12; B bhava neutral 50 for H1/H5/H7 domains. Audit fixture has all 12 → production/test divergence | Altered per-domain certainty labels in production vs fixture | Data-source governance; pipeline must not shrink canonical | Re-extract full 12-house canonical (out of scope here) | YES — implementation required, awaiting approval | High |
| DM-002 | A,B,C | Medium | Pipeline output house population | Reuses canonical houses as-is | Mirrors 9-house source | §10/§20 | Same as DM-001 aggregate for C | None | Pipeline source-of-truth contract | Approve 12-house canonical re-extraction path | YES — awaiting approval | High |
| DEV-002 | B | Low-Med | natal_promise `_karaka_score` blend map | DOMAIN_KARAKA declares secondary for all 8 domains | Blend honored only for education/children/property/health; wealth/marriage/spirituality primary-only | Runtime proof §15; traces B.10–B.13 | Wealth raw 56.55 vs 56.63 (same round 57); marriage 53 unchanged; spirituality 50 unchanged — zero rounded-score impact on canonical chart | None (aggregate identical for this chart) | Declarative-intent mismatch; calibration declares a blend the engine does not implement for 3 domains | Apply declared blends for wealth/marriage/spirituality OR scope DOMAIN_KARAKA secondary intent | YES — implementation required, awaiting approval (or governance clarification) | Medium |
| PARAM-001 | A,B,C | Low-Med | Codes: `MASTER_WEIGHTS` const, `_STUB_SCORE`, `_get_weight` fallbacks, blend map literals, `varga_raw=50` stub | ADR-003: no hardcoded astrological rules | Runtime is calibration-driven; literals persist as fallback/documentation | §19; §20 C.6; §8 A.19; B.19 | None at runtime under v1.0_current | None | ADR-003 tension | Migrate remaining literals into calibration or document explicit fallback contract; give PARAM governance file | YES — implementation required, awaiting approval | Low |
| TR-001 | A,B,C | Low-Med | `display_formatter.py` `_build_explanation` (≈161–167) → reports macros | Provenance: engine_name, version, formula_source, calibration_profile, timestamp, true weight/contribution | Emits Unknown/v1.0/Empty timestamp; factor weight 1.0; contribution=raw_value; label "Formula: Executive Synthesis" | `outputs/deterministic_report.html` 64 "Engineering Traceability" blocks all Unknown (v1.0); natal traces same | None (display-only) | All trace blocks show Unknown; weight/contribution misrepresented | Engines emit provenance metadata; formatter consumes it | YES — implementation required, awaiting approval | Low-Med |
| GOV-001 | C | High | ADR-004 (Accepted) vs Formula C aggregation | Layers evaluated as distinct gates; no Promise+Dasha+Transit flattening | Master engine aggregates exactly those three + four others into one score | ADR-004 §16–38; MASTER_PROBABILITY_KNOWLEDGE_PACKAGE §11; §18 | None (math governed) | None | Direct conflict on the record | Approve ADR-004 amendment or formally register master engine as sole sanctioned synthesis owner | YES — governance decision required + implementation | High |
| GOV-002 | A | Low | FORMULA_OWNERSHIP_MAPPING_v1.0.md status DRAFT | Finalized one-formula-one-owner register | DRAFT; Planet→Planet Engine mapping only | §4 | None | None | Ownership map not ratified | Ratify v1.0 ownership mapping | YES — awaiting approval | Low |
| GOV-003 | All | Low | Missing `FORMULA_REPOSITORY_DATA_MODEL` / `*PARAMETER*` governance md | Parameter-driven governance file exists | Absent | §4 | None | None | Referenced data model doc not present | Create parameter-change governance file per mandate (out of scope now) | YES — awaiting approval | Low |
| DOC-001 | A | Trivial | `tests/test_planet_strength_engine.py` comments | kendra=100 per test comments | Matrix kendra=90 | §9 A.15 | None (comments only) | None | Doc drift | Correct stale comments | YES — awaiting approval | Low |

---

## Section 24 — WHAT WE GOVERNED vs WHAT CALIBRATION CONTAINS vs WHAT CODE IMPLEMENTS vs WHAT RUNTIME EXECUTES vs WHAT REPORT SHOWS vs WHAT FRONTEND SHOWS vs WHAT IS MISSING vs WHAT IS DIFFERENT (mandated)
**A. Planet Strength**
- Governed: 8 factors 25/20/15/10/10/5/10/5, matrix scales, round, BAV, clamp. Calibration contains: identical parameters + matrix (incl. duplicated `vedha_pairs`/`VEDHA_PAIRS` keys). Code implements: identical via `_get_weight` read. Runtime executes: identical (proven). Report shows: final/breakdown present; trace provenance Unknown/1.0. Frontend shows: final_score/breakdown display-only.
- What is MISSING: full 12-house canonical; provenance metadata emission; stale comment fix.
- What is DIFFERENT: none in math.

**B. Natal Promise**
- Governed: 35/30/20/15, grade ladder. Calibration contains: DOMAIN_CONFIG/DOMAIN_KARAKA (secondary declared for all 8 domains)/grades/bonuses. Code implements: 35/30/20/15 correctly; karaka secondary blend for only 4 domains. Runtime executes: identical to code. Report shows: natal_promise blocks; trace Unknown/1.0. Frontend shows: display-only.
- What is MISSING: wealth/marriage/spirituality secondary blend; 12-house canonical.
- What is DIFFERENT: declarative secondary karaka vs implemented blend (DEV-002) — aggregate impact nil on canonical chart.

**C. Master Probability**
- Governed: docs 40/15/10/10/10/10/5; ADR-004 forbids Promise+Dasha+Transit flattening. Calibration contains: same weights under section `probability` (not `master_probability`), grades, stub 50.0. Code implements: `MASTER_WEIGHTS` const + **reads calibration accessor at runtime**. Runtime executes: calibration values (proven `weights == calibration`). Report shows: `master_summary` final_score/grade; raw/breakdown/weights kept under formula_verification but intentionally absent from `master_summary`. Frontend shows: final/breakdown/grade display-only.
- What is MISSING: ADR-004 amendment/exception registration; parameter-change governance file.
- What is DIFFERENT: documentation constant vs calibrated runtime (identical values); ADR-004 letter vs master synthesis.

---

## Section 25 — PARAMETER-CHANGE READINESS (mandated)
Question: "If governance changes a governed weight, what is required downstream?"
| Formula | Changed Parameter | Engine reads from calibration? | Fallback literal in code? | New profile requires code change? | Classify |
|---|---|---|---|---|---|
| A | dignity weight | Yes (`_get_weight` → weight_pct/100) | Yes (0.25 etc.) | No — code change NOT required if a new profile ships; fallback only if profile lacks param | **YES** |
| A | (house_placement etc. same path) | Yes | Yes (same pattern) | No | **YES** |
| B | bhava weight | Yes (`npe.config[n]["weights"]` from calibration) | No | No | **YES** |
| B | karaka blend coefficients | Blend map in engine code for 4 domains | Yes (literals 0.60/0.40, 0.70/0.30) | YES — code change required to honor declared secondaries for wealth/marriage/spirituality | **PARTIAL** |
| C | master natal_promise weight | Yes (`master_probability` accessor → `self.weights`) | Yes (`MASTER_WEIGHTS` const kept as fallback/doc) | No — runtime follows calibration; const must be re-synced as documentation or will drift | **YES** (with PARAM-001 doc-drift risk on the constant) |
Notes: profile status IMMUTABLE → parameter change means a NEW profile version selected via CalibrationManager; engines are constructed per request and read the active profile at `__init__`/call time — mechanism-ready. ADR-003 partial-compliance (PARAM-001) is the only gate requiring code action for the instrumented weights.

---

## Section 26 — ONE-PAGE FORMULA CHECKPOINT (mandated)
| Formula | Owner engine | Governed weights | Calibration | Engine | Runtime | Independent recompute | Tests | Report | Frontend | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| A Planet Strength | planet_strength_engine.py | 25/20/15/10/10/5/10/5 | exact | exact | exact | jupiter 55.2385→60 ✓ | all pass | score present, trace Unknown | display-only ✓ | **PASS (math); DA defects** |
| B Natal Promise | natal_promise_engine.py | 35/30/20/15 | exact | exact | exact | wealth 56.55→57 ✓ marriage 52.95→53 ✓ spirit 50→50 ✓ | all pass | blocks present, trace Unknown | display-only ✓ | **PASS (math); DEV-002 blend** |
| C Master Probe | master_probability_engine.py | 40/15/10/10/10/10/5 | exact | exact | exact | 48.992→49→WEAK ✓ | all pass | master_summary final/grade only | display-only ✓ | **PASS (math); ADR-004 + TR-001** |
| Cross-cut | — | ADR-003 ≠ literals | vedha dup keys | — | deterministic ✓ | — | 81 ✔ focused | 64 trace blocks Unknown | Math.round only | Deviation register §23 |

**Bottom line:** all three formulas are mathematically correct as implemented and match canonical calibration and real-chart recomputation. The deployment path carries identical values to report and frontend with zero recomputation. Enabled defects are provenance/display fidelity (TR-001), karaka-blend declarative mismatch (DEV-002, zero canonical impact), canonical 9-house data source (DM-001/DM-002), ADR-004 conflict (GOV-001), and ADR-003 literal residue (PARAM-001) — plus missing governance artifacts (GOV-002/GOV-003) and doc drift (DOC-001).

---

## Section 27 — FINAL CERTIFICATION (A–N, mandated)
- **A. Formula A math: CORRECT** — every factor, weight, round, BAV, clamp reproduced exactly.
- **B. Formula B math: CORRECT** — 35/30/20/15 exact; wealth/marriage/spirituality independently reproduced; secondary-blend deviation documented with zero rounded-score impact on canonical chart.
- **C. Formula C math: CORRECT** — 40/15/10/10/10/10/5 exact; 48.992→49→WEAK reproduced; dasha 60/40 MD/AD exact; equal-weight mean disproven as governing formula.
- **D. Calibration ↔ code ↔ runtime parity: VERIFIED** — runtime weights == calibration values for all three formulas (proven live).
- **E. Determinism: VERIFIED** — two-run deep-identical engine_outputs and master probability.
- **F. Deployment parity (report): VERIFIED** — no recomputation downstream; raw/breakdown retained under formula_verification; master_summary intentionally final/grade only.
- **G. Deployment parity (frontend): VERIFIED** — display-only consumption; Math.round presentation-only.
- **H. Duplicate formula / ownership: NONE FOUND** — single canonical owners; no parallel implementations.
- **I. Test integrity: PASS** — focused formula suites re-run green (81 passed); baseline recorded 826 passed/1 skipped.
- **J. Traceability/provenance: DEFECT** (TR-001): 64 blocks Unknown (v1.0), weight 1.0, contribution=raw. Display-only; math unaffected.
- **K. Data-source governance: DEFECT** (DM-001/DM-002): canonical Raju carries 9 houses; production behavior differs from test fixture for house-strength mean and H1/H5/H7 domains.
- **L. Governance consistency: DEFECT** (GOV-001 ADR-004; GOV-002 draft ownership; GOV-003 missing parameter-governance file; PARAM-001 ADR-003 residue). ADR-004 is the highest-severity item → GOVERNANCE DECISION REQUIRED.
- **M. Read-only integrity: MAINTAINED** — zero repo changes; no staging/commits/push; git state unchanged from §3.
- **N. Next implementation task (exact):** Register the master engine as the sole ADR-004-sanctioned synthesis boundary (or amend ADR-004) via an owner-approved ADR amendment, and implement TR-001 engine→reports provenance emission — as the highest-priority governed implementations — followed by 12-house canonical re-extraction (DM-001).

---

## Section 28 — AUDIT OUTCOME AND BINDING LANGUAGE
**AUDIT COMPLETE — EVIDENCE RECORDED — IMPLEMENTATION PENDING APPROVAL.**

Formula-level verdicts: A = PASS (math) / B = PASS (math) / C = PASS (math), each carrying registered non-math defects (see §23). For every defect: **Implementation required — awaiting user approval.** No code, calibration, docs, governance, staging, or commits were modified by this audit.

---

## Appendices
- **§29 A. ADR register (relevant):** ADR-003 Accepted (no hardcoded rules), ADR-004 Accepted (no aggregate), ADR-008 Accepted (evaluate once); ADR-001/2/5–16 noted (formats, Mandali overlay, expansion, routing matrix, scaling, moon-exclusion, non-numeric confidence, tone-locking, composer firewall, MIXED capping, system warnings). No ADR supersedes ADR-004.
- **§30 B. Calibration profile:** `v1.0_current.json` — profile_id v1.0_default, version 1.0.0, status IMMUTABLE; metadata validation_horoscopes_completed 0; duplicated `vedha_pairs`/`VEDHA_PAIRS` keys break PowerShell JSON parsing (Python reads authoritative).
- **§31 C. Source-shape detail (DM-001):** canonical 9 houses (2,3,4,6,8,9,10,11,12); missing 1,5,7; planets sun..ketu. Test fixture `test_real_charts.py` has all 12 → divergence between production house-strength mean (42.89 over 9) and fixture-derived expectations.
- **§32 D. Traceability defect detail (TR-001):** `DisplayFormatter._build_explanation` defaults engine_name="Unknown", engine_version="1.0", formula_source="Unknown", formula_version="1.0", calibration_profile="Unknown", calibration_version="1.0", execution_timestamp=""; factor weight 1.0/contribution=raw_value; template label "Formula: Executive Synthesis". `outputs/deterministic_report.html` ≈1,075,962 bytes; 64 blocks ALL Unknown (v1.0) + empty timestamps; natal-promise blocks same.
- **§33 E. Test inventory note:** exact assertions present in planet/master suites; natal uses delta=2.0 tolerances; gaps: no HTML-trace-content test, no two-run determinism test, no exact-master-output contract test (each proposed as future implementation beyond this audit's scope).
- **§34 F. Formula owners (current):** A→Planet Strength Engine; B→Natal Promise Engine; C→Master Probability Engine; consumers House/Yoga/Varga/Dosha (Planet); report/formatters/frontend are consumers-only.