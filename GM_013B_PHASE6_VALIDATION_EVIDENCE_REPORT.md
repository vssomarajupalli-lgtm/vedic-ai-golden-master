# GM-013B | Phase 6 — CASE-001 (Raju) API Validation Evidence Report

**Version:** 1.0  
**Date:** 2026-08-15  
**Status:** COMPLETE — ALL CHECKS PASS  
**Scope:** Read-only API validation of CASE-001 (Raju) against the live backend. No implementation changes.

---

## 1. Executive Summary

The Phase 6 API validation gate for CASE-001 (Raju) is **COMPLETE and PASS**. All six API paths return valid, deterministic, person-specific results. No P0/P1 defects found via API evidence. The GM-013B release gate is **not blocked** by any API-level defect.

**Key Metrics:**
- HTTP 200 on every endpoint exercised (`/process-chart`, `/generate-report?format=json|html|pdf`, `/explanations/generate`, `/knowledge/integrity`)
- Deterministic replay: **byte-identical** after excluding only the runtime-resolved `target_date_utc`
- `final_score`: **49.0 / WEAK** (consistent across runs and report)
- HTML report: **PASS** (all three charts, person-specific values)
- PDF report: **PASS** (93 pages, all charts and values)
- AI Explanations: **PASS** with MockProvider caveat (`provider=mock`, no OpenAI key)
- Knowledge Graph: **79 nodes / 206 relationships / 0 issues**

---

## 2. Test Harness & Inputs

| Item | Value |
|------|-------|
| Base URL | `http://localhost:8000/api/v1` |
| Backend HEAD (protected baseline) | `e68d952` |
| Case inputs | `extracted_json/raju_machine_index.json` (44,036 B), `extracted_json/raju_canonical_content.json` (810,015 B) — GPU MANAGEMENT upstream, unchanged |
| Request payload | `phase6_process_req.json` (593,828 B), `phase6_report_req.json` (593,868 B, `question_ids: ["10.1","2.1","7.1"]`) |
| Rate limiter | 60/min burst 10 — respected, requests spaced |

---

## 3. Chart Processing — `/process-chart`

### 3.1 Results

| Run | HTTP | Latency | Response Size | `final_score` | Grade |
|-----|------|---------|---------------|---------------|-------|
| Run-1 | 200 | 1.63 s | 743,633 B | 49.0 | WEAK |
| Run-2 | 200 | 1.61 s | 743,633 B | 49.0 | WEAK |

### 3.2 Deterministic Replay Diff

| Differing path | Detail | Classification |
|----------------|--------|----------------|
| `root/target_date_utc` | 2026-08-15T09:31:10 vs 09:31:18 (wall-clock run time) | Runtime field — excluded |
| `root/breakdown/target_date_utc` | same wall-clock difference | Runtime field — excluded |
| All other fields | **byte-identical** | Deterministic |

After stripping `target_date_utc`, the full 700 KB+ payload is **byte-identical** across runs. This satisfies GM-013B §3.2 / §8.1 replay criteria (identical output excluding timestamps/request_ids).

### 3.3 Person-Specific Verification

| Value | Observed |
|-------|----------|
| Name | raju svsn |
| `final_score` (breakdown + master_exit) | 49 / WEAK |
| `metadata.ascendant_sign` | Mesha (canonical default — see §8 Caveats) |
| Authoritative `natal_lagna` (report) | **Simha** (matches `vargas.D1.planets.Lagna.sign`) |
| reference_moon | **Makara / Dhanishta / Pada 2 / absolute 90** |
| Mandali 1 centre | Dhanishta |
| Yogas present | Yes |

---

## 4. Report Generation (JSON replay) — `/generate-report?format=json`

| Run | HTTP | Latency | Response Size |
|-----|------|---------|---------------|
| Run-1 | 200 | 1.73 s | 823,753 B |
| Run-2 | 200 | 1.69 s | 823,753 B |

**Deterministic diff:** exactly 3 differing leaf paths — all legitimate runtime fields:
- `formula_verification/target_date_utc`
- `client_profile/generated_at`
- `metadata/generated_at`

**0 non-time diffs.** Top-level keys identical.

### 4.1 South Indian Chart Data (protected feature)

| Check | Result |
|-------|--------|
| Grid shape | 4 × 4, **Meena top-left** |
| Lagna house map | Simha=1, Mesha=9, Makara=6, Meena=8 |
| Moon house map | Makara=1 |
| reference_moon | Makara / Dhanishta / Pada 2 |
| natal_lagna | Simha |
| natal_planets | 9 (Jupiter JU 19:19:21 in Kanya/Hasta P3 H2) |

---

## 5. HTML Verification — `/generate-report?format=html`

HTTP 200, 1,147,747 B.

| Section | Present |
|---------|---------|
| Chart 1 · Natal / Lagna (D1) | ✅ |
| Chart 2 · Moon-centred Mandali, Mandali 1 on natal Moon Makara Dhanishta Pada 2 | ✅ |
| Chart 3 · Rāśi Gochara (Transit), Natal Moon Makara = House 1 | ✅ |
| Dhanishta Pada references | ✅ (14) |
| Simha / Makara references | ✅ (33 / 26) |
| Saturn lifetime cycles | ✅ (344 occurrences) |
| MASTER PROBABILITY SCORE | ✅ |
| No fabricated Raphael values | ✅ |

---

## 6. PDF Verification — `/generate-report?format=pdf`

HTTP 200, 4,664,691 B, **93 pages**, 100,838 extracted chars (pypdf).

| Check | Present |
|-------|---------|
| Valid PDF | ✅ |
| Chart 1 / Chart 2 / Chart 3 labels | ✅ (1 each) |
| Lagna (Simha) | ✅ (33) |
| Makara (Moon) | ✅ (26) |
| Dhanishta / Pada 2 | ✅ (13 / 11) |
| Mandali / Gochara | ✅ (541 / 13) |
| Saturn / lifetime | ✅ (374 / SATURN LIFETIME present) |

---

## 7. AI Explanations — `/explanations/generate`

HTTP 200 (0.25 s), 1,005 B.

| Field | Value |
|-------|-------|
| question | Marriage Prospects (7.1) |
| domain | marriage |
| `routed` | true |
| `confidence` | HIGH |
| `deterministic_trace` | `"master_probability.final_score"` |
| `citations` | 3 (all `type=engine_output`, highest level L4) |
| `evidence_summary` | complete (`by_type`, `total_citations`, `highest_evidence_level`) |
| `metadata.provider` | **mock** / `model=mock-model` |
| `grounding_package_hash` | empty |

**Caveat (non-blocking):** the AI provider is **MockProvider** — no OpenAI API key is wired, so the explanation is a templated mock, not a live LLM call. The endpoint contract, governance shape (citations, confidence, deterministic_trace) is valid. This is a deployed-environment finding, not a Phase 6 failure.

---

## 8. Knowledge Graph Integrity — `/knowledge/integrity`

HTTP 200, 109 B.

```json
{ "valid": true, "issues": [], "node_count": 79, "relationship_count": 206, "checked_at": "2026-08-15T09:36:54" }
```

Meets GM-013B §3.5 baseline (≥79 nodes, ≥206 relationships, 0 issues).

---

## 9. Protected-Feature Regression (Step 8)

| Protected feature | Status |
|-------------------|--------|
| South Indian 4×4 geometry, Meena top-left | ✅ unchanged |
| Lagna house numbering (Simha=1) | ✅ unchanged |
| Moon-centred Mandali allocation (Makara, Dhanishta P2) | ✅ unchanged |
| Traditional Rāśi Gochara (Moon Makara = H1) | ✅ unchanged |
| Nakshatra / Pada references | ✅ unchanged |
| Dasha (MD Saturn, AD Jupiter, PD Sun, 17 days remaining) | ✅ unchanged |
| Saturn lifetime cycles | ✅ unchanged |
| Deterministic trace | ✅ unchanged |
| HTML/PDF generation | ✅ unchanged |

---

## 10. Caveats & Findings

| # | Finding | Severity | Blocking? |
|---|---------|----------|-----------|
| F-6.1 | `run.py` CLI report path fails: `base.html:1053` `q.executive_summary` missing (legacy `compose_response` dicts). API path unaffected. | P1 | **No** — deferred |
| F-6.2 | `process-chart` `metadata.ascendant_sign=Mesha` is the canonical default (metadata lacks a `lagna` field). Authoritative `natal_lagna=Simha` (from `vargas.D1.planets.Lagna.sign`) is correct. | P3 (canonical-data note) | No |
| F-6.3 | Explanations use `provider=mock` — no OpenAI key wired at runtime; `grounding_package_hash` empty. | P3 (env) | No |

---

## 11. Conclusion & Next Action

**No API-level defect blocks GM-013B.** All six API paths return valid, deterministic, person-specific results for CASE-001. The prior blocker ("obtain GM-013B approval evidence + build add-only harness") is unblocked from an API standpoint.

- ✅ **Record complete.** Raw artifacts retained in `C:\Users\vssom\AppData\Local\Temp\opencode\` (see §12 provenance).
- ⏭ **Not performed (out of scope):** CASE-002…008 collection, multi-case harness creation, any protected-feature modification.

---

## 12. Evidence Artifact Provenance (SHA-256)

| Artifact | Size | SHA-256 |
|----------|------|---------|
| `phase6_process_run1.json` | 743,633 | `1E9889D4336B6CFCC1704A348042F46D491EA4350062A86B89347E37EFEFB4A8` |
| `phase6_process_run2.json` | 743,633 | `B3A9565388C16B59F6C8B93FFC11A884E25B9DBB9C5AD50ADB72B06E52460DD8` |
| `phase6_reportjson_run1.json` | 823,753 | `24EB5F224B54AD329D90A77D5B7F778984A298F856FE446749CB3073F7BE4448` |
| `phase6_reportjson_run2.json` | 823,753 | `04D5FFCD097D2ED58E280F6577E8523A3666A622401084FBD53FA40892F575DE` |
| `phase6_report.html` | 1,147,747 | `05DF89BF0BC04BB8642C435D3F9A522D37148D1BAF98904F648F0841CDC6D9AB` |
| `phase6_report.pdf` | 4,664,691 | `D5A5A3A441C4285E18D7168DC2B758F609706E77CAAA4EA6EBB674305A335F82` |
| `phase6_expl1.json` | 1,005 | `71D44AED70CC73B373A0A215B25B5CC4796C313F56BD09BE165024EE8CCE603E` |
| `phase6_knowledge.json` | 109 | `133E26308A6D35F7DF293C3AFDC7E4E7167A35C8C37722D723C4589D3CD80D79` |

Raw replay artifacts are intentionally **not committed** to the repository (they are validation intermediates, not tracked assets), consistent with the existing convention where the repository tracks only validation Markdown reports and ground-truth data. Provenance hashes above preserve the record.

---

*Deferred (not fixed — out of task scope): `backend/app/reports/templates/base.html:1053` — `q.executive_summary` missing when `run.py` passes legacy `compose_response()` results.*