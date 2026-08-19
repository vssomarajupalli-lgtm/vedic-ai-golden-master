# ADR-004 / FORMULA C GOVERNANCE RECONCILIATION + LATEST CANONICAL HOROSCOPE REVALIDATION

**Report ID:** GM-AUDIT-2026-08-18-ADR004-REVALIDATE
**Mode:** READ-ONLY (no file/formula/calibration/ADR/frontend modifications; no commit/push/reset/cleanup)
**Validity inputs:** Latest `HoroscopeCleaner_Final` outputs — SK Apsana & SK Sameera (Telugu + English)
**Outcome:** Investigation complete. No modifications made.

---

## 1. Git State

- Branch `main`, HEAD `a29a38013c41ed2418d9f95d6249fedf7df25d78` — "feat: add single-click batch horoscope report launcher".
- Log-8: a29a380, 89cead8, e68d952, 1a61255, a934204, b46e752, f44f569, 3648766.
- Pre-existing owner WIP only: `M frontend/src/components/GocharaTab.tsx`, `M frontend/src/components/consultation/ConsultationWorkspace.tsx`, `?? frontend/src/components/charts/`.
- Nothing staged/committed/pushed by this investigation.

## 2. Governance Documents Inspected

| Document | Path | Version/Status | Classification |
|---|---|---|---|
| ADR-004 | `docs/architecture/decisions/ADR-004.md` | Accepted | Architecture Rule (rank 6 in DR-012) |
| ADR-003 | `docs/architecture/decisions/ADR-003.md` | Accepted | Architecture Rule (no hardcoded astrological rules) |
| Decision Register | `docs/governance/DECISION_REGISTER.md` | DR-001..DR-012+ | Approved Decision Register (rank 2) |
| Astrological Prediction Governance | `docs/governance/ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` | v1 | Source-of-Truth (rank 5); 3-layer separation authority |
| Formula Governance | `docs/governance/FORMULA_GOVERNANCE_v1.0.md` | v1.0 | Governance doc (formula sourcing) |
| Formula Repo/Data Model | `docs/governance/FORMULA_REPOSITORY_DATA_MODEL_v1.md` | v1 | Governance doc |
| Formula Ownership Mapping | `docs/governance/FORMULA_OWNERSHIP_MAPPING_v1.0.md` | DRAFT | Reference doc (rank 7) |
| Engine Ownership/Contract Registry | `docs/governance/ENGINE_OWNERSHIP_AND_DATA_CONTRACT_REGISTRY_v1.0.md` | v1.0 | Governance doc |
| Refinement Decision Register | `docs/governance/REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md` | v1.0 | Decision record |
| Master Probability Knowledge Package | `docs/knowledge/MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | — | Source-of-Truth (synthesis boundary) |
| Vedic AI Master Architecture | `docs/knowledge/VEDIC_AI_MASTER_ARCHITECTURE.md` | — | Reference/architecture list |
| Master Formula Audit (+ verification gate) | `docs/governance/audits/2026-08-18_GM_3FORMULA_DEEP_AUDIT_BASELINE.md` | 2026-08-18 | Historical audit baseline |

## 3. ADR-004 Exact Interpretation

**Decision (verbatim):** *"The system shall explicitly forbid flattening or mathematically aggregating Natal Promise (static potential), Dasha (timing activation), and Transit (current sky) values into one unified score."*

- **Prohibits:** collapsing semantically distinct layers (natal potential, temporal dasha, ephemeral transit) into one undifferentiated number that erases layer identity.
- **Does NOT prohibit:** weighted, additive synthesis where each layer retains its own score/identity (Potential, Activation, Timing Window as distinct outputs) and is combined with explicit governed weights.
- Governance foundation: `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` — "An event can only occur if the natal chart contains the promise."

## 4. Formula C Historical Evolution Table

| Date | Artifact | Weight set (7 pillars: Nat/Plan/House/Rasi/Varga/Dasha/Transit) | Source | Status |
|---|---|---|---|---|
| 2026-06-11 | DR-011 (Decision Register) | "additive weighted synthesis ... Natal + Planet + House + Rasi + Varga + Dasha + Transit" | Domain Expert / Phase-1 Clarification | **Governing (rank 2)** |
| 2026-06-27 | Initial GM commit `f6bb238` — `MASTER_WEIGHTS` literal 40/15/10/10/10/10/5 + `transit_trigger`/`dasha_activation` present | 40/15/10/10/10/10/5 | Code (calibration-backed runtime read + literal) | **Current** |
| 2026-07-24 | Commit `855dd8f` "GM-014A-GM-018 ... Calibration Framework" | 40/15/10/10/10/10/5 (via calibration read; `engine.weights == calibration` True) | Calibration | **Current** |

*Evidence gap:* `git log --all` on `master_probability_engine.py` shows only `f6bb238` and `855dd8f`; intermediate evolution not visible in this snapshot. Transit/dasha were **never added later** — present from initial GM commit and endorsed before it by DR-011.

## 5. Transit Introduction History

- `transit_trigger` exists at initial GM commit `f6bb238` (2026-06-27) — not a later add-on.
- DR-011 (2026-06-11) explicitly names Transit as one of the seven additive master-probability pillars.
- DR-008 requires Transit Activation as a separately distinguishable output (Timing Window). Formula C keeps `transit_trigger = activation_score` as a distinct 5% factor with its own breakdown — layer identity preserved.

## 6. ADR-004 Classification

**B. HISTORICAL RULE SUPERSEDED** — by DR-011 (Event Probability Philosophy, 2026-06-11) adopting additive weight composite synthesis of all seven pillars including Dasha and Transit, under DR-012 (2026-06-11) conflict hierarchy where Approved Decision Register (rank 2) outranks ADRs/Architecture Rules (rank 6). ADR-004's anti-pattern (opaque single flattening) is not what Formula C does. **Classification NOT D** — current implementation is compliant with higher-priority governance and preserves layer identity.

## 7. Recommendation (ONE)

**KEEP CURRENT FORMULA C** — no engine, weight, calibration, dasha, transit, or score change. Separate consistency follow-ups: refresh ADR-004 with DR-011/DR-012 supersession cross-reference (doc-maintenance only), resolve TR-001 provenance labels, register DEV-002 karaka intent.

## 8. Latest Canonical Files Used

Path `D:\HoroscopeCleaner_Final\output\` (outside repo):

| File | SHA-256 (canonical / machine index) | Pages |
|---|---|---|
| `sk apsana_canonical_content.json` | E7845B3BA812E46F / 7A3DE13421846E0E | 88 |
| `sk apsana english_canonical_content.json` | D06A26BDAEA0352C / 24EF6955B325334E | 91 |
| `sk sameera_canonical_content.json` | 18E5DF8D6877A917 / 3C8D5311BC3A397C | 87 |
| `sk sameera english_canonical_content.json` | D40B5164C1460F37 / 8B81B4BA9A8F526C | 88 |

All four: 9 planets, 12 houses, 16 vargas, 7 shadbala, 12 bhava-bala, dasha timeline, SAV (12 rasi-keyed) + BAV (7 planets), doshas.

## 9. Apsana Validation

- DOB 19/10/1986, TOB 22:20, Naidupet/Tirupati/AP, 13.93063N 79.9107E, Asia/Kolkata +5.5, Lagna Gemini 12:12.
- **Formula A:** TE final sun 40(-5) moon 64(+5) mars 71(0) mercury 52(-5) jupiter 62(+5) venus 65(-5) saturn 56(0) rahu 58(0) ketu 58(0); raw [44.94/58.62/70.80/56.51/57.29/69.87/56.09/57.5/57.5]. EN adds mars 66(-5), saturn 51(-5) (pada change). **EXACT.**
- **Formula B:** TE wealth 54.85->55, marriage 54.55->55, spirituality 52.45->52, career 51.35->51, education 55->55; EN career 50.35->50, spirituality 50.95->51, property 49.44->49. **EXACT (all 8 x 2).**
- **Formula C:** TE **51 GOOD** (raw 50.949); EN **52 GOOD** (raw 51.5185). **EXACT, deterministic** (two runs deep-equal).

## 10. Sameera Validation

- **Formula A:** TE sun 60 moon 56 mars 63(-5) mercury 35 jupiter 58 venus 60 saturn 57 rahu 58 ketu 58. EN sun 55(-5) moon 61(+5) mars 73(+5) venus 65(+5). **EXACT.**
- **Formula B:** TE wealth 43.6->44, marriage 52.05->52, spirituality 52.7->53, career 52.65->53, education 48.44->48, children 51.08->51, property 53.14->53, health 51.88->52; EN marriage 53.05->53, spirituality 55.7->56, career 53.85->54, property 57.74->58, health 50.18->50. **EXACT.**
- **Formula C:** TE **50 GOOD** (raw 50.3915); EN **51 GOOD** (raw 51.375). **EXACT** and deterministic (fresh run reproduced saved output).

## 11. Telugu vs English Comparison

All birth/position values identical; only language-label fields differ. **Apsana nakshatra_pada:** TE all 0 vs EN sun=3/moon=4/rahu=4/ketu=2 -> English is MORE complete (template difference, not conflict); sameera no pada difference. Cross-language Formula C deltas are pada-driven + dasha/transit deltas.

## 12. Machine-Index Comparison

Apsana TE 161 vs EN 174 blocks; Sameera TE 160 vs EN 185. All `{title, page_from, page_to}` dicts; family headers present in both. **No relative sequence inversions** on shared normalized titles; page spans consistent. Topology preserved.

## 13. Planet Strength Revalidation

Nine planets sun..ketu consistent with engine iteration. raw = sum of 8 factor contributions; base = round(raw); final = base + BAV (pipeline Step 7.5; BAV absent from planet output modifiers). Rahu/Ketu base=None (nodal standard 57.5/58). All verified.

## 14. Natal Promise Revalidation

Eight-domain engine; `0.35*bhava + 0.30*bhavadhipati + 0.20*karaka + 0.15*varga` reproduces every raw_score to <0.01 across all 32 domain records. Natal factor = unweighted mean of 8 domain finals (52.75 TE / 52.38 EN apsana; 50.75 TE / 51.75 EN sameera).

## 15. Master Probability Revalidation

| Chart | raw | final | Grade | Nat | Plan | House | Rasi | Varga | Dasha | Transit |
|---|---|---|---|---|---|---|---|---|---|---|
| Apsana TE | 50.9490 | 51 | GOOD | 52.75 | 58.44 | 42.17 | 34.83 | 53.33 | 58 | 45 |
| Apsana EN | 51.5185 | 52 | GOOD | 52.38 | 57.33 | 42.17 | 34.83 | 56.67 | 60 | 52 |
| Sameera TE | 50.3915 | 50 | GOOD | 50.75 | 56.11 | 41.67 | 33.58 | 50.00 | 62 | 59 |
| Sameera EN | 51.3750 | 51 | GOOD | 51.75 | 57.78 | 41.67 | 33.58 | 53.33 | 61 | 61 |

`sum(weight x factor)` matches raw_score exactly for every chart.

## 16. Calibration Verification

- `master_probability.weights` = calibration `probability.parameters.weights` (0.4/0.15/0.1/0.1/0.1/0.1/0.05); `engine.weights == calibration` True.
- Factor sources verified: natal = mean 8 domains; planet = mean 9 finals; house = mean 12 houses; rasi = mean 12 rasi finals; varga = 50 + net D9 modifiers clamped per planet then meaned; dasha = 0.60*MD + 0.40*AD; transit = float(activation_score).

## 17. Deployment Verification

Batch reports generated from Telugu runs: `sk apsana_report.html` -> **51% Good**, `sk sameera_report.html` -> **50% Good**, both Trend Stable. Frontend consumes `breakdown.master_probability` display-only (ActivationTimeline, ComparisonWorkspace, VerificationConsole, GocharaPresentation — no recomputation).

## 18. Traceability Status (TR-001 STILL PRESENT)

77 traceability blocks in apsana HTML, 75 in sameera HTML. First block: `Engine: Unknown (v1.0)`, empty Timestamp, `Formula: Executive Synthesis`, `Formula Source: Unknown (v1.0)`, `Calibration: Unknown (v1.0)`, factor row `natal_promise 52.75 | 1.0 | 52.75` (weight 1.0, contribution=raw). Pre-existing provenance defect.

## 19. Karaka Status (DEV-002 Implementation Gap)

`DOMAIN_KARAKA` declares secondary for all 8 domains; `_karaka_score` blends only education/children/property/health (0.60/0.40; children 0.70/0.30). Wealth/marriage/spirituality primary-only. Example deltas (apsana TE): wealth jupiter 62 (blend 63.2); marriage venus 65 (blend 63.8); spirituality jupiter 62 (blend 60.4). **No rounded final score change** in any of the 4 new charts.

## 20. Source Completeness Findings

- New canonicals have all 12 houses (Raju legacy only 9). EN apsana fills padas; TE leaves 0.
- **SAV mapping gap (pre-existing):** SAV rasi-keyed under `ashtakavarga.sav_chart`; houses carry no `sav_points`; `json_normalizer._normalize_houses` defaults `sav_points=0` -> house/rasi sav contribution 0.0 for ALL charts including legacy Raju (re-verified). Source-shape/enrichment limitation, not a formula defect. House factor ~42, rasi ~34 depressed uniformly.
- Doshas present (kala_sarpa + kuja). Dasha timeline 632 entries (apsana TE).

## 21. Raju vs Apsana vs Sameera Comparison Table

| Aspect | Raju (legacy) | Apsana | Sameera |
|---|---|---|---|
| Houses | 9 (no 1,5,7) | 12 | 12 |
| nakshatra_pada | n/a | TE 0 / EN filled | n/a |
| sav_points/house | 0 (none) | 0 (SAV rasi-keyed) | 0 (SAV rasi-keyed) |
| Master (2026-08-18) | historical only | 51/52 GOOD | 50/51 GOOD |
| Batch reports | n/a | 51% Good | 50% Good |

## 22. Deviations

1. TR-001 traceability provenance (Unknown/1.0) — pre-existing, reproduced.
2. DEV-002 karaka secondary blend gap — pre-existing; no rounded-score impact.
3. SAV-to-house enrichment gap — pre-existing (Raju included); systematic; not a formula defect.
4. Earlier sameera milestone notes (51/53) superseded by deterministic re-runs; authoritative saved/fresh values are TE 50 (50.3915), EN 51 (51.375).

## 23. Recommendations

1. KEEP CURRENT FORMULA C (DR-011/DR-008 compliant; deterministic; exact on 4 fresh canonicals).
2. Refresh ADR-004 with DR-011/DR-012 supersession cross-reference (doc-only).
3. Fix TR-001 provenance labels at next batch release.
4. Record DEV-002 karaka secondary decision (use declared blends or formally drop).
5. Register SAV->house mapping as backlog enrichment item (independent of Formula C).

## 24. Exact Next Action

Deliver this report as final outcome; STOP. Recommended downstream (separate authorization): doc-only ADR-004 supersession cross-reference + TR-001/DEV-002/SAV dockets. No Formula C / engine / weight / calibration / dasha / transit / source / frontend changes.

## 25. Final Report (Verbatim Summary)

Formula C revalidation on latest canonicals (Apsana & Sameera, TE+EN): Formulas A, B, C reproduce exactly and deterministically. Weight chain governance->calibration->engine->runtime verified (`engine.weights == calibration`). Formula C compliant with DR-011/DR-008 under DR-012; ADR-004 is a historical rule superseded by the decision register. SAV/house enrichment, TR-001, DEV-002 are pre-existing independent findings, not formula defects.

## 26. Mandatory Final Decision Table

| # | Decision / Fact | YES | NO |
|---|---|---|---|
| 1 | Formula C weights match governance (DR-011) seven-pillar synthesis | YES | |
| 2 | Runtime `engine.weights` == calibration values | YES | |
| 3 | Formula A reproduces exactly on all 4 new canonicals | YES | |
| 4 | Formula B reproduces exactly (all 8 domains x 2 languages) | YES | |
| 5 | Formula C reproduces exactly (master raw/final x 4) | YES | |
| 6 | Formula C deterministic across runs | YES | |
| 7 | ADR-004 classification = B (Historical Rule Superseded) | YES | |
| 8 | ADR-004 classification = D (governance violation) | | NO |
| 9 | Transit/dasha present from initial GM commit `f6bb238` | YES | |
| 10 | SAV->house enrichment gap pre-existing (present on Raju too) | YES | |
| 11 | TR-001 proven-defect present on new batch reports | YES | |
| 12 | DEV-002 karaka blend gap present (no rounded-score impact) | YES | |
| 13 | Any file/formula/commit modified by this investigation | | NO |

## 27. STOP Statement

Investigation complete. **No modifications made** — no files, formulas, calibrations, ADRs, tests, or frontend changed; no commits/pushes/cleanup executed. This is the final outcome.

---

**End of preservation artifact.** Original evidence retained in `C:\Users\vssom\AppData\Local\Temp\opencode\` (audit scripts + 4 revalid_* json outputs + GM_3FORMULA_DEEP_AUDIT_2026-08-18.md). Nothing in this preservation step modified formula behavior.