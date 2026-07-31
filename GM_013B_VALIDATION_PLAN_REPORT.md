# GM-013B | Version 1.1 RC1 Real Horoscope Validation Plan

**Version:** 1.1-RC1  
**Date:** 2026-07-31  
**Status:** PLANNING — Awaiting Approval  
**Scope:** Validation ONLY — No implementation changes

---

## 1. Validation Methodology

### 1.1 Approach
- **End-to-end pipeline validation** using real canonical JSON horoscopes
- **Deterministic replay verification** — same input must produce identical output
- **Ground-truth comparison** where expert-validated reference data exists
- **AI Explanation Layer verification** — governance, citations, confidence, replay

### 1.2 Test Harness
- Backend: `python run.py <index.json> <content.json>` (deterministic CLI)
- API: `POST /api/v1/process-chart` + `POST /api/v1/explanations/generate`
- MockProvider for reproducible AI explanations
- Automated comparison scripts for regression detection

### 1.3 Execution Order
1. **Chart Processing** — `/process-chart` for each case
2. **Deterministic Replay** — Run each case twice, compare outputs
3. **Question Engine** — Query structured questions per domain
4. **AI Explanations** — Generate explanations for each question
5. **Report Generation** — HTML/PDF output verification
6. **Knowledge Graph** — Verify node/relationship integrity post-processing

---

## 2. Required Chart Diversity

### 2.1 Minimum Case Set (8 Cases)

| Case | Profile | Purpose |
|------|---------|---------|
| **CASE-001** | Male, Aries Lagna, Saturn in 7th | Marriage delay, career focus, Sadesati active |
| **CASE-002** | Female, Taurus Lagna, Jupiter in 5th | Children promise, education strength, Viparita Raja Yoga |
| **CASE-003** | Male, Gemini Lagna, Mars-Ketu in 8th | Health afflictions, longevity, sudden events |
| **CASE-004** | Female, Cancer Lagna, Moon in 10th | Career prominence, property, emotional stability |
| **CASE-005** | Male, Leo Lagna, Sun-Rahu in 1st | Leadership, fame, health vitality, ego challenges |
| **CASE-006** | Female, Virgo Lagna, Mercury in 12th | Foreign settlement, spirituality, expenses |
| **CASE-007** | Male, Libra Lagna, Venus in 4th (own sign) | Luxury, vehicles, mother relationship, comforts |
| **CASE-008** | Female, Scorpio Lagna, Mars in 3rd | Siblings, courage, initiative, communication |

### 2.2 Diversity Requirements Per Case

| Dimension | Required Coverage |
|-----------|-------------------|
| **Lagna (Ascendant)** | All 12 signs across suite |
| **Moon Sign** | All 12 signs across suite |
| **Dasha Period** | At least 3 different Mahadashas |
| **Transit Activation** | Sadesati, Ashtama Shani, Jupiter return, Rahu/Ketu transit |
| **Yoga Presence** | ≥3 major yogas per case (Raja, Dhana, Pancha Mahapurusha, Nabhasa) |
| **Ashtakavarga** | Mix of high (>28) and low (<22) bindu houses |
| **Varga Charts** | D9 (Navamsa), D10 (Dashamsa) active |
| **Natal Promise Spread** | Scores across 0-100 range in all 8 domains |

### 2.3 Input Format
Each case provides:
- `machine_index.json` — Extracted planetary positions, houses, dashas, vargas
- `canonical_content.json` — Raw text for reference
- `ground_truth.md` — Expert-validated expectations (where available)

---

## 3. Validation Checklist

### 3.1 Chart Processing (`/process-chart`)

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| HTTP 200 | All 8 cases return 200 OK | ☐ |
| Response Schema | Matches `ChartProcessResponse` exactly | ☐ |
| `final_score` | 0-100 integer, matches deterministic run | ☐ |
| `probability_grade` | One of: PRESENT/MODERATE/GOOD/VERY GOOD/EXCELLENT | ☐ |
| `master_probability` | Contains `final_score`, `grade`, `breakdown`, `weights` | ☐ |
| `engine_outputs` | All 11 engines present with scores | ☐ |
| `target_date_utc` | ISO8601 UTC string present | ☐ |
| `metadata` | Name, dob, tob, pob, ascendant_sign, ascendant_degree | ☐ |
| Yogas array | ≥1 yoga detected per case | ☐ |

### 3.2 Deterministic Replay

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Run 1 vs Run 2 | Identical JSON output (byte-for-byte) | ☐ |
| Master score | Same `final_score` ±0 | ☐ |
| All engine scores | Same values ±0 | ☐ |
| Yoga list | Same yogas, same order | ☐ |
| Timing | `target_date_utc` identical | ☐ |

### 3.3 Question Engine (`/ask-question` / `/ask-structured-question`)

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Domain routing | Correct domain for each question | ☐ |
| `probability.score` | 0-100, matches master_probability domain breakdown | ☐ |
| `probability.grade` | Consistent with score | ☐ |
| `natal_promise` | Score matches natal_promise engine output | ☐ |
| `timing` | Contains mahadasha, antardasha, activation_level | ☐ |
| `formula_verification` | Present, references formula IDs | ☐ |
| `confidence` | HIGH/MEDIUM/LOW based on evidence level | ☐ |

### 3.4 Report Generation

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| HTML generated | File >50KB, valid HTML structure | ☐ |
| PDF generated | File >100KB, valid PDF (Playwright) | ☐ |
| Deterministic schema | Contains all engine outputs, citations, traceability | ☐ |
| Formula trace | Each score links to formula ID + calibration | ☐ |
| Evidence chain | ≥1 step per major factor | ☐ |

### 3.5 Knowledge Graph Integrity

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| Node count | ≥79 nodes (baseline) + new case nodes | ☐ |
| Relationship count | ≥206 + new case relationships | ☐ |
| Evidence chains | Computed for Formula, Gochara, Probability, Yoga | ☐ |
| Computed fields | `evidence`, `references`, `relationships` populated | ☐ |
| No orphan nodes | All nodes connected to at least 1 relationship | ☐ |

---

## 4. Expected Deterministic Outputs

### 4.1 Master Probability Score Ranges (Per Profile)

| Case | Expected Range | Key Drivers |
|------|----------------|-------------|
| CASE-001 (Aries) | 40-65 | Saturn 7th delays, strong career |
| CASE-002 (Taurus) | 55-75 | Jupiter 5th children, education |
| CASE-003 (Gemini) | 30-55 | 8th house afflictions, health |
| CASE-004 (Cancer) | 60-80 | Moon 10th career, property |
| CASE-005 (Leo) | 50-70 | Sun-Rahu 1st fame/health mix |
| CASE-006 (Virgo) | 45-65 | 12th Mercury foreign/spiritual |
| CASE-007 (Libra) | 65-85 | Venus 4th own sign luxury |
| CASE-008 (Scorpio) | 55-75 | Mars 3rd courage/siblings |

### 4.2 Domain Score Expectations (Per Case)

Each case must produce scores in all 8 domains:
- Marriage, Career, Wealth, Education, Children, Property, Health, Spirituality

Scores must be **consistent with natal promise engine** (no divergence >15 points between natal promise and final probability for same domain).

### 4.3 Transit Activation Levels

| Transit | Expected Activation Level |
|---------|---------------------------|
| Sadesati (Saturn over Moon) | ACTIVE if Saturn in 12th/1st/2nd from Moon |
| Ashtama Shani (Saturn 8th from Moon) | ACTIVE if Saturn in 8th from Moon |
| Jupiter Return | ACTIVE if Jupiter within 5° of natal |
| Rahu/Ketu Transit | ACTIVE if within 10° of natal planet/house |

---

## 5. AI Explanation Verification

### 5.1 Endpoint: `POST /api/v1/explanations/generate`

**Test Input:** GroundingPackage from each case's pipeline output + structured question

### 5.2 Validation Checks

| Check | Criteria | Pass/Fail |
|-------|----------|-----------|
| HTTP 200 | All questions return 200 OK | ☐ |
| Response Schema | Matches `ExplanationResponse` | ☐ |
| `explanation` | Non-empty string, references deterministic values | ☐ |
| `citations` | Array with ≥1 citation per 2 sentences | ☐ |
| Citation types | Only: `engine_output`, `kg_node`, `evidence_chain`, `formula_registry`, `calibration_registry`, `report_template` | ☐ |
| Citation fields | `type`, `path`, `value`, `evidence_level` present | ☐ |
| `confidence` | HIGH/MEDIUM/LOW — must match highest evidence_level | ☐ |
| `evidence_summary` | Contains `total_steps`, `highest_evidence_level`, `summary` | ☐ |
| `processing_time_ms` | >0, <5000 (MockProvider) | ☐ |
| `deterministic_trace` | References `master_probability.final_score` or engine output path | ☐ |

### 5.3 Governance Compliance

| Rule | Verification |
|------|--------------|
| No external knowledge | Explanation contains no values not in grounding package |
| No astrological calculation | All numbers trace to engine outputs |
| Citations traceable | Each citation path resolvable in pipeline output |
| Confidence propagation | L1/L2 → HIGH, L3 → MEDIUM, L4+ → based on chain |
| Structured output | JSON parseable, citations array valid |

---

## 6. Citation Verification

### 6.1 Citation Coverage Matrix

| Evidence Level | Source | Minimum Per Explanation |
|----------------|--------|-------------------------|
| L1 (Canonical Rule) | Classical text reference | 0 (optional) |
| L2 (Formula) | Formula registry (e.g., `PRB-NP-001`) | ≥1 |
| L3 (Calibration) | Calibration registry (weights, thresholds) | ≥1 |
| L4 (Engine Output) | Pipeline engine outputs | ≥2 |
| L5 (Canonical Data) | Raw planetary positions | ≥1 |
| L6 (Derived Engine) | Computed scores (dasha, transit) | ≥1 |
| L7 (Classical Text) | Shastra reference | 0 (optional) |
| L8 (Expert Rule) | ADR/governance decision | 0 (optional) |
| L9 (ADR) | Architecture decision record | 0 (optional) |
| L10 (Version) | Schema/engine version | 0 (optional) |

### 6.2 Citation Accuracy

| Check | Criteria |
|-------|----------|
| Citation path resolves | `engine_outputs.planet_strength.mars.final_score` exists |
| Citation value matches | Value in citation equals value in pipeline output |
| Evidence level correct | L4 for engine outputs, L2 for formulas, L3 for calibrations |
| No hallucinated citations | All cited paths exist in grounding package |

---

## 7. Confidence Verification

### 7.1 Confidence Level Rules

| Highest Evidence Level | Expected Confidence |
|------------------------|---------------------|
| L1-L2 (Canonical/Formula) | HIGH |
| L3 (Calibration) | HIGH |
| L4 (Engine Output) | HIGH |
| L5 (Canonical Data) | MEDIUM |
| L6 (Derived) | MEDIUM |
| L7-L10 only | LOW |

### 7.2 Validation

| Check | Criteria |
|-------|----------|
| Confidence ≥ evidence | HIGH confidence only if L1-L4 present |
| Consistency | Same evidence profile → same confidence across cases |
| Explicit in response | `confidence` field populated and accurate |

---

## 8. Replay Verification

### 8.1 Deterministic Replay Test

**Procedure:**
1. Run `python run.py case_X_index.json case_X_content.json` → Capture output A
2. Run again with same inputs → Capture output B
3. Compare: `diff <(echo A | jq -S .) <(echo B | jq -S .)` — must be empty

**API Replay:**
1. POST `/process-chart` with canonical JSON → Capture response A
2. POST identical request → Capture response B
3. Compare: Must be identical (excluding timestamps, request_ids)

### 8.2 AI Explanation Replay

**Procedure:**
1. POST `/explanations/generate` with identical GroundingPackage + question → Response A
2. Repeat → Response B
3. MockProvider must return identical `content` (JSON string)
4. Citations, confidence, deterministic_trace must match

### 8.3 Replay Pass Criteria

| Component | Match Requirement |
|-----------|-------------------|
| Pipeline output | 100% identical (byte-for-byte JSON) |
| Question engine | 100% identical |
| AI Explanation (MockProvider) | 100% identical content string |
| Citations | Identical array, order, values |
| Report HTML/PDF | Identical content (timestamps excluded) |

---

## 9. Bug Classification Rules

### 9.1 Severity Levels

| Severity | Definition | Examples |
|----------|------------|----------|
| **P0 — Release Blocker** | Incorrect deterministic output, governance violation, crash | Wrong master score, missing citations, confidence mismatch, 500 error |
| **P1 — Critical** | Functional failure in non-deterministic path | Report generation fails, KG query error, frontend console error |
| **P2 — Major** | Deviation from expected output within tolerance | Score difference >5 pts from ground truth, missing yoga |
| **P3 — Minor** | Cosmetic, documentation, non-functional | UI alignment, typo in explanation, missing optional field |
| **P4 — Enhancement** | Improvement, not a bug | Performance, UX polish, additional yoga detection |

### 9.2 Classification Decision Tree

```
Is output deterministic?
├── NO → P0 (architecture violation)
├── YES → Does it match ground truth?
│   ├── NO → Deviation >15 pts? → P0
│   ├── NO → Deviation 5-15 pts? → P1
│   ├── NO → Deviation <5 pts? → P2
│   └── YES → Governance compliant?
│       ├── NO (missing citations, wrong confidence) → P0
│       └── YES → Cosmetic only? → P3/P4
```

### 9.3 Regression Detection

| Check | Baseline | Threshold |
|-------|----------|-----------|
| Test suite | 739 passed | Any new failure = P0 |
| Master score (per case) | v1.0 baseline | Δ >3 pts = P1 |
| Citation count | ≥1 per 2 sentences | <1 per 2 = P0 |
| Confidence accuracy | 100% | Any mismatch = P0 |

---

## 10. Release Acceptance Criteria

### 10.1 Mandatory (All Must Pass)

| Criterion | Target |
|-----------|--------|
| **All 8 cases process** | 8/8 HTTP 200 on `/process-chart` |
| **Deterministic replay** | 100% identical output (pipeline + API + AI) |
| **All 739 tests pass** | 0 new failures, 0 new flaky |
| **AI Explanation governance** | 100% citation coverage, 100% confidence accuracy |
| **Citation verification** | All citations resolve, values match, levels correct |
| **Report generation** | 8/8 HTML + PDF generated successfully |
| **Knowledge Graph** | No integrity violations, computed fields populated |
| **No P0/P1 bugs** | 0 open P0, 0 open P1 |

### 10.2 Target Metrics

| Metric | Target |
|--------|--------|
| Master score accuracy vs ground truth | ≤5 pts average deviation |
| Citation coverage | ≥1.5 per 2 sentences |
| Confidence accuracy | 100% |
| Replay success rate | 100% (8/8 cases) |
| API latency (p50) | <500ms `/process-chart`, <800ms `/explanations/generate` |
| Frontend build | 0 TypeScript errors, <600kB gzipped |

### 10.3 Conditional Release

| Scenario | Decision |
|----------|----------|
| All mandatory pass, 0 P0/P1 | **READY FOR RC1 TAG** |
| All mandatory pass, 1-2 P2 | **READY AFTER P2 FIXES** (24hr window) |
| Any P0/P1 open | **NOT READY** — block release |
| >3 P2 open | **NOT READY** — consolidate fixes |

---

## 11. Execution Plan

| Phase | Activity | Duration | Owner |
|-------|----------|----------|-------|
| **Prep** | Collect 8 canonical JSON cases, verify ground truth | 2 hours | QA |
| **Execute** | Run pipeline on all 8 cases (CLI + API) | 1 hour | Engineer |
| **Replay** | Double-run each case, diff outputs | 30 min | Engineer |
| **AI Layer** | Generate explanations for 20 questions across cases | 1 hour | Engineer |
| **Reports** | Generate HTML/PDF for all 8 cases | 30 min | Engineer |
| **Analysis** | Score comparison, citation audit, confidence check | 2 hours | QA + Engineer |
| **Bug Triage** | Classify, prioritize, assign | 1 hour | Lead |
| **Fix/Verify** | Address P0/P1, re-run affected cases | Variable | Engineer |
| **Sign-off** | Final report, acceptance decision | 30 min | Lead |

**Total Estimated: 8-10 hours**

---

## 12. Approval Gates

| Gate | Required Approval |
|------|-------------------|
| **Plan Approval** | Lead Engineer + Product Owner |
| **Execution Start** | Lead Engineer |
| **P0/P1 Triage** | Lead Engineer (mandatory) |
| **Release Decision** | Lead Engineer + Product Owner (unanimous) |

---

*Generated by GM-013B — Validation Plan Only. No code changes.*