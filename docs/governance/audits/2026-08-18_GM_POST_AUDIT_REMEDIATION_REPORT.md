# 2026-08-18 GM POST-AUDIT REMEDIATION REPORT

| Field | Value |
|---|---|
| Date | 2026-08-18 |
| Base commit | `a29a38013c41ed2418d9f95d6249fedf7df25d78` (branch `main`) |
| Predecessor | `2026-08-18_GM_3FORMULA_DEEP_AUDIT_BASELINE.md` (28 sections) |
| Companion | `2026-08-18_GM_ADR004_CANONICAL_REVALIDATION.md` |
| Status | COMPLETE — verified, NOT committed, NOT pushed |

---

## Section 1 — Objective and Authority

Execute the POST-3-FORMULA AUDIT REMEDIATION mandate of 2026-08-18. Only proven
items are implemented (TR-001 traceability); SAV and DEV-002 are classified and
filed as governance/evidence items with **no code change**. Every deliverable is
backed by deterministic revalidation of Formula A/B/C against the 4 validation
charts, byte-equality proof, and the full backend test suite.

## Section 2 — Read-Only Compliance Statement (verbatim rule)

The following are frozen and were NOT modified:

- Formula A (Planet Strength) math, per-parameter weight_pct and fallback defaults.
- Formula B (Natal Promise) math, per-domain 0.35/0.30/0.20/0.15 aggregation.
- Formula C (Master Probability) math, `MASTER_WEIGHTS`
  (0.40/0.15/0.10/0.10/0.10/0.10/0.05), grades, stub 50.0, section key `probability`.
- Seven-pillar aggregation in `PipelineRunner`; engine ownership; calibration accessors.
- All calibration JSON content (`v1.0_current.json` etc.).

Changes are confined to: engine **metadata emission** (new provenance fields) and
`DisplayFormatter` **pass-through** of those fields. No engine recomputes scores;
no calibration value was edited.

## Section 3 — Git State and Change Control

- HEAD `a29a38013c41ed2418d9f95d6249fedf7df25d78`; working tree carries task files
  UNCOMMITTED. Nothing committed, nothing pushed (STOP compliance).
- Pre-existing owner WIP untouched: `frontend/src/components/GocharaTab.tsx`,
  `frontend/src/components/consultation/ConsultationWorkspace.tsx`,
  `frontend/src/components/charts/`.
- Change set (task): new `backend/app/utils/engine_provenance.py`;
  modified `backend/app/engines/{planet_strength,house_strength,master_probability,natal_promise,dasha,transit}_engine.py`;
  modified `backend/app/formatters/display_formatter.py`;
  new `backend/tests/test_engine_provenance.py`; this report + the two Part-1 audit docs.

## Section 4 — Scope

In scope: TR-001 (engine provenance / traceability), SAV classification, DEV-002
classification, Part 6 before/after proof, targeted provenance tests, dated report.

Out of scope (no change): Yoga detection blocks (binary, no score, YogaEngine is
not a Formula owner) and the Gochara Mandali block (frozen under
`GOCHARA_MANDALI_GOVERNANCE_v1.md`); both retain their existing rendering.

## Section 5 — TR-001 Disposition

**IMPLEMENTED.** Each Formula-owning score engine now emits real, deterministic
provenance into its output `metadata`, and `DisplayFormatter` renders it. The
visible defect (trace blocks labeled `Engine: Unknown (v1.0)`) is remediated for
all six in-scope engines: 33 real engine labels rendered (was 0), 5 out-of-scope
blocks remain labeled Unknown by design (see §13).

## Section 6 — TR-001 Provenance Design (`engine_provenance.py`)

Shared helper `build_engine_provenance(calibration, engine_name, formula_source)`
emits only engine-known facts, no clock-dependent fields (outputs stay
deterministic):

| key | value source |
|---|---|
| `engine` | engine display name |
| `version` | `calibration.active_profile["metadata"]["version"]` (fallback `1.0.0`) |
| `formula_source` | calibration section key passed by the engine |
| `formula_version` | `"1.0"` |
| `calibration_profile` | `active_profile["metadata"]["profile_id"]` (fallback `v1.0_default`) |
| `calibration_version` | `active_profile["metadata"]["version"]` (fallback `1.0.0`) |

`build_factor_provenance(raw, weight)` returns `{raw, weight, contribution}`
where `contribution = raw * weight` using the same operands the engine already
multiplies — nothing is re-implemented.

## Section 7 — TR-001 PlanetStrengthEngine Provenance

`metadata` now carries engine provenance plus one factor per parameter:

| factor | weight |
|---|---|
| dignity | 0.25 |
| house_placement | 0.20 |
| aspects | 0.15 |
| conjunctions | 0.10 |
| combustion | 0.10 |
| retrogression | 0.05 |
| shadbala | 0.10 |
| varga_dignity | 0.05 |

Every factor is recorded via `build_factor_provenance` from the values the engine
already computes; `contribution == breakdown` asserted by tests.

## Section 8 — TR-001 HouseStrengthEngine Provenance

| factor | weight |
|---|---|
| sav | 0.30 |
| occupants | 0.20 |
| benefic_aspects | 0.15 |
| malefic_aspects | 0.15 |
| house_type | 0.10 |
| house_yogas | 0.10 |
| lord_contribution | 0.25 |

`lord_contribution` remains breakdown-only (as before); all six scored factors
are recorded with `contribution == breakdown[key]`.

## Section 9 — TR-001 MasterProbabilityEngine Provenance

`metadata = provenance + factors[7]` mirroring `self.weights`
(0.40/0.15/0.10/0.10/0.10/0.10/0.05). Verified identity:

- `factors[k].weight == weights[k]`, `factors[k].raw == breakdown[k]`.
- `sum(factors[k].contribution) == raw_score`. Apsana TE: 21.1 + 8.766 + 4.217 +
  3.483 + 5.333 + 5.8 + 2.25 = **50.949** == raw.
- Final master score unchanged: apsana TE **51 GOOD**, raw 50.949.

## Section 10 — TR-001 NatalPromiseEngine Provenance

`__init__` now binds `self.calibration` (was missing — AttributeError fixed).
Each of the 8 domains emits provenance + 4 factors using the already-computed f
values: bhava 0.35, bhavadhipati 0.30, karaka 0.20, varga 0.15. Domain scores
unchanged (verified per-domain in revalidation).

## Section 11 — TR-001 DashaEngine Provenance

`metadata` carries provenance + 3 factors: mahadasha 0.50, antardasha 0.30,
pratyantardasha 0.20. Runtime example: MD raw 45 → 22.5, AD raw 70 → 21.0, PD raw
45 → 9.0 (contributions exactly `raw * weight`).

## Section 12 — TR-001 TransitEngine Provenance

`__init__` now binds `self.calibration`. Live path emits provenance + one factor
per breakdown weight key. Stub path (`_stub_result`) emits provenance with factors
raw 50 per `self.weights` key and activation 50. Stub behavior unchanged.

## Section 13 — TR-001 DisplayFormatter Pass-Through

`_build_explanation`: when `metadata["factors"]` is present, builds
`CalculationFactor` with the real `raw_value`, `weight`, `calibration_key`,
`calibration_value`, `contribution`. Legacy weight-1.0 fallback is preserved for
engines without provenance. Result — production HTML report `sk apsana_report.html`:

| engine | BEFORE | AFTER |
|---|---|---|
| PlanetStrengthEngine | 0 | 9 |
| HouseStrengthEngine | 0 | 12 |
| NatalPromiseEngine | 0 | 8 |
| MasterProbabilityEngine | 0 | 2 |
| DashaEngine | 0 | 1 |
| TransitEngine | 0 | 1 |
| Unknown (v1.0) | 38 | 5 |
| **Real labels** | **0** | **33** |

The 5 remaining Unknown = 4 universal yogas (Raja/Adhi/Vidya/Putra — binary
detections, no score) + 1 Gochara Mandali block (frozen) — out of scope, unchanged.
Weights render correctly end-to-end: `natal_promise raw 52.75 / weight 0.4` (2 rows),
`house sav raw 0.00 / weight 0.3` (12 rows). Timestamp row is empty in both states
(no timestamps emitted — deterministic).

## Section 14 — TR-001 Part 6 BEFORE/AFTER Byte-Equality Proof

Reproduction runner identical for both states:
`PipelineRunner().process({"canonical_content":…, "machine_index":…}, target_date_utc=2026-08-18 UTC)`.
Outputs contain no time-varying keys (only `target_date_utc: 2026-08-18T00:00:00+00:00`),
so normalized (provenance-stripped) byte comparison is valid.

| chart | master final | raw | grade | byte-identical (provenance-stripped) |
|---|---|---|---|---|
| apsana telugu | 51 | 50.949 | GOOD | PASS |
| apsana english | 52 | 51.5185 | GOOD | PASS |
| sameera telugu | 50 | 50.3915 | GOOD | PASS |
| sameera english | 51 | 51.375 | GOOD | PASS |

Formula A/B/C outputs, breakdowns, weights, and grades are byte-identical
(provenance-stripped) BEFORE vs AFTER for all 4 charts. AFTER artifacts saved as
`tr001_after_{apsana,sameera}_{telugu,english}.json`.

## Section 15 — TR-001 Test Evidence

- Full backend suite: **827 passed / 1 skipped** (baseline) → **835 passed / 1
  skipped** after adding `test_engine_provenance.py` (8 tests). Only warning:
  starlette formparsers PendingDeprecation (pre-existing).
- New tests assert: provenance key presence; weight values (0.25/0.20/…; sav 0.30;
  natal 0.35/0.30/0.20/0.15; dasha 0.50/0.30/0.20; transit per `self.weights`);
  `raw * weight == contribution`; `contribution == breakdown`; master
  `sum(contributions) == raw_score` (final 50 stub); DisplayFormatter renders real
  weights (natal_promise 0.40, planet_strength 0.15 — never 1.0) and legacy
  fallback unchanged.

## Section 16 — SAV-001 Classification

**C — DOCUMENTATION GAP (with D — INSUFFICIENT EVIDENCE).** No code change.

- Governance scans complete: `DECISION_REGISTER.md` (3,694 bytes) and
  `ARCHITECTURE_DECISION_LOG_v1.0.md` (3,330 bytes) contain **zero** karaka-blend
  or sav-chart→house mapping entries. No governed primary-only rule and no
  governed mapping rule exist.
- Evidence the house `sav_points` value is EXPECTED: engine contract
  (`house_strength_engine` weight 0.30; `rasi_strength_engine` weight 0.35 reads
  the rasi sav_chart), canonical inventory, and the `HOME_CANONICAL_JSON` fixture.
- Runtime fact: the loader/normalizer never delivers `sav_points` into
  `house_data`; house SAV is 0.0 for all real canonicals. This is a pre-existing
  source-shape gap, NOT a formula defect. No mapping rule found → classification
  C/D, deferred for governance decision; no code change.

## Section 17 — DEV-002 Classification

**B — GOVERNANCE-DOC MISMATCH.** No code change.

- `DOMAIN_KARAKA` declares secondary karakas for all 8 domains; the engine blends
  the secondary karaka only in education/children/property/health.
- Score impact proven zero: wealth example — karaka jupiter 60 (primary-only) vs
  60.4 had venus 61 blended 0.6/0.4 → raw 56.55 vs 56.63 → **same rounded 57**,
  different raw only. Registered; governance-doc correction deferred; no code change.

## Section 18 — Governance Evidence Base

- Part 1 artifacts preserved verbatim under `docs/governance/audits/`:
  `2026-08-18_GM_3FORMULA_DEEP_AUDIT_BASELINE.md` (37,796 bytes) and
  `2026-08-18_GM_ADR004_CANONICAL_REVALIDATION.md` (15,123 bytes).
- Formula mapping confirmed: Formula A = PlanetStrengthEngine, Formula B =
  NatalPromiseEngine, Formula C = MasterProbabilityEngine; calibration chains
  verified (A: `planet_strength`; B: per-domain; C: `probability` section,
  `engine.weights == calibration.master_probability['MASTER_WEIGHTS']`).
- SAV/DEV-002 classification evidence: §16–§17; scans listed in §16.

## Section 19 — Risk Register / Out-of-Scope Items

| item | state | rationale |
|---|---|---|
| 4 yoga trace blocks (`Unknown (v1.0)`) | unchanged | binary detection, no score; YogaEngine not a Formula owner; fabricating a score trace would violate no-invented-values |
| Gochara Mandali trace block | unchanged | behavior frozen under `GOCHARA_MANDALI_GOVERNANCE_v1.md` |
| `FORMULA_REPOSITORY_DATA_MODEL` gap | open | GOV-003 from baseline §23; parameter-governance file still absent — awaiting approval, out of scope now |
| house SAV source-shape gap | open | SAV-001 C/D (§16); no mapping rule governed |

## Section 20 — Final Decision Table

| item | classification | code change | proof |
|---|---|---|---|
| TR-001 traceability | IMPLEMENTED | provenance metadata + formatter pass-through only; zero formula edits | §6–§15: byte-equal 4-chart revalidation; 835 tests; 33 real HTML engine labels (was 0) |
| SAV-001 | C / D | none | §16: no governed rule; canonical/house contract gap; 0.0 SAV for all real charts |
| DEV-002 | B | none | §17: doc mismatch only; zero score impact |

## Section 21 — Certification and STOP Compliance

All in-scope items are implemented and verified; every mandated proof is captured
above; the full suite is green (835 passed / 1 skipped); Formula A/B/C math is
byte-unchanged; no out-of-scope changes were made. Per the STOP rule the working
tree is intentionally left UNCOMMITTED and UNPUSHED — commit/push only upon
explicit authorization.

**Status: COMPLETE — STOP (no commit, no push).**
