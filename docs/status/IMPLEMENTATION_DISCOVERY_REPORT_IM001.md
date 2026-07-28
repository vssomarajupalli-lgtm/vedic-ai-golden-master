# Implementation Discovery Report
## GM-010 — Universal Gochara Mandali Implementation
### Phase IM-001: Repository Discovery

---

## 1. Existing Files

| File | Status | Description |
|------|--------|-------------|
| `backend/app/engines/mandali_generator.py` | **EXISTS** | Current MandaliGenerator with longitude-based pada calculation, grid generation, transit resolution, and evaluate() method |
| `backend/app/engines/transit_engine.py` | **EXISTS** | Consumes MandaliGenerator for Moon-centered Mandali resolution (lines 125-135, 683-687) |
| `backend/app/engines/question_engine.py` | **EXISTS** | Accepts `mandali_activation` parameter (line 126) |
| `backend/app/config/astrology_constants.py` | **EXISTS** | Contains SIGN_LORD_MAP, EXALTATION_MAP, DEBILITATION_MAP, OWN_SIGN_MAP, SIGNS_IN_ORDER |
| `docs/knowledge/raju_canonical_content.json` | **EXISTS** | Canonical JSON with Transit/Gochara section (pages 85-86) containing Rasi, Nakshatra, Pada, dates |
| `docs/GOCHARA_MANDALI_GOVERNANCE_v1.md` | **EXISTS** | Canonical governance document (approved) |

---

## 2. Existing Reusable Classes

| Class/Module | Reusable? | Governance Alignment | Notes |
|--------------|-----------|---------------------|-------|
| `MandaliGenerator.generate_mandali_grid(moon_pada)` | ✅ **YES** | Aligns with Capability 7.3 (MandaliGridConstruction) | Already implements MGC-01 to MGC-07 logic using absolute pada index. **Refactor**: change input from `moon_pada` (int) to accept `nakshatra, pada` via NakshatraPadaResolver. |
| `MandaliGenerator.resolve_transit_mandali(transit_longitude, moon_pada)` | ⚠️ **PARTIAL** | Aligns with Capability 7.4 (TransitMandaliResolution) | **Must refactor**: currently takes `longitude` (float). Model A requires `(nakshatra, pada)` from Canonical JSON. Core grid lookup logic reusable. |
| `MandaliGenerator.get_absolute_pada(longitude_deg)` | ❌ **NO** | Violates CGP-06 (No Astronomical Computation) | Longitude-based. **Deprecate for Model A**. Replace with `NakshatraPadaResolver.resolve(nakshatra, pada)` using Canonical Registry. |
| `MandaliGenerator.evaluate(transit_payload, natal_payload)` | ⚠️ **PARTIAL** | Aligns with Capability 7.7 (UniversalMandaliEngine) | **Must refactor**: currently expects `longitude` in payload. Model A payload has `rasi, nakshatra, pada`. Output schema differs from `mandali_advisory`. |
| `TransitEngine` Mandali integration (lines 125-135) | ✅ **YES** | Demonstrates Mandali usage pattern | Shows how MandaliGenerator is called. **Must update** to use new UniversalMandaliEngine output. |
| `astrology_constants.py` mappings | ✅ **YES** | Partial alignment with Canonical Registries | SIGN_LORD_MAP, EXALTATION_MAP, etc. exist. **Missing**: Nakshatra-Pada sequence (108 entries), Nakshatra→Rasi mapping, Rasi sequence. |

---

## 3. Missing Components

| Component | Governance Reference | Status |
|-----------|---------------------|--------|
| **Canonical Reference Data Registries** | Section 6 | **MISSING** — 3 JSON files needed: `nakshatra_pada_registry.json`, `nakshatra_rasi_registry.json`, `rasi_sequence_registry.json` |
| **NakshatraPadaResolver** | Capability 7.2 | **MISSING** — Replaces `get_absolute_pada(longitude)` |
| **CanonicalReferenceDataAccess** | Capability 7.1 | **MISSING** — Registry loader with versioning |
| **LifetimeCycleProjection** | Capability 7.5 | **MISSING** — Saturn 30-year cycle projection from Canonical JSON dates |
| **BirthPositionDetection** | Capability 7.6 | **MISSING** — BEFORE/INSIDE/AFTER classification per window |
| **UniversalMandaliEngine** | Capability 7.7 | **MISSING** — Orchestrator producing `mandali_advisory` schema |
| **CanonicalJSONLoader** | Implementation Responsibilities | **MISSING** — Load/validate Canonical JSON transit section |
| **mandali_advisory output schema** | Section 12 | **MISSING** — Versioned JSON schema for AnswerComposer |

---

## 4. Refactoring Opportunities

| Target | Action | Governance Driver |
|--------|--------|-------------------|
| `MandaliGenerator` | **Refactor, not deprecate** | Section 9: Legacy longitude methods deprecated; Pada-based methods retained for Model B appendix |
| `MandaliGenerator.generate_mandali_grid` | Extract to `MandaliGridConstruction` capability | Capability 7.3 ownership |
| `MandaliGenerator.resolve_transit_mandali` | Extract to `TransitMandaliResolution` capability | Capability 7.4 ownership; change signature to `(nakshatra, pada)` |
| `TransitEngine` | Update to consume `UniversalMandaliEngine.mandali_advisory` | CGP-05, CGP-07: No hidden integration |
| `PipelineRunner` | Wire `UniversalMandaliEngine` | Section 13: New capability in pipeline |
| `AnswerComposer` | Accept `mandali_advisory` parameter | Section 15.2: Independent advisory block |

---

## 5. Files to Modify

| File | Modification Type | Description |
|------|-------------------|-------------|
| `backend/app/engines/mandali_generator.py` | **REFACTOR** | Deprecate `get_absolute_pada(longitude)`, `resolve_transit_mandali(longitude, moon_pada)`, `evaluate(payload, payload)`. Retain `generate_mandali_grid(moon_pada)` as core grid logic. Add `resolve_transit_mandali_by_pada(nakshatra, pada, mandali_grid)`. |
| `backend/app/engines/transit_engine.py` | **MODIFY** | Remove direct MandaliGenerator calls. Consume `UniversalMandaliEngine` output. Remove legacy fallback `t_houses[p] = int(v.get("house", 0))`. |
| `backend/app/pipeline_runner.py` | **MODIFY** | Add `UniversalMandaliEngine` to engine execution sequence. Pass `mandali_advisory` to AnswerComposer. |
| `backend/app/reports/consultation_summary_generator.py` | **MODIFY** | Accept `mandali_advisory` parameter. Render standalone "GOCHARA MANDALI ADVISORY" section per Section 14. |
| `backend/app/config/astrology_constants.py` | **EXTEND** | Add Nakshatra-Pada sequence, Nakshatra→Rasi mapping, Rasi sequence as module-level constants (or move to JSON registries). |

---

## 6. Files to Create

| File | Purpose | Governance Reference |
|------|---------|---------------------|
| `backend/app/config/nakshatra_pada_registry.json` | 108-entry Nakshatra-Pada sequence | Section 6.1 |
| `backend/app/config/nakshatra_rasi_registry.json` | Nakshatra→Rasi mapping (with pada granularity) | Section 6.2 |
| `backend/app/config/rasi_sequence_registry.json` | 12-Rasi zodiacal order | Section 6.3 |
| `backend/app/engines/canonical_reference_data.py` | Capability 7.1: Registry loader with versioning | Capability 7.1 |
| `backend/app/engines/nakshatra_pada_resolver.py` | Capability 7.2: (nakshatra, pada) → absolute pada | Capability 7.2 |
| `backend/app/engines/mandali_grid_construction.py` | Capability 7.3: Grid construction from Moon pada | Capability 7.3 |
| `backend/app/engines/transit_mandali_resolution.py` | Capability 7.4: Transit → Mandali via pada | Capability 7.4 |
| `backend/app/engines/lifetime_cycle_projection.py` | Capability 7.5: Saturn 30-year cycles | Capability 7.5 |
| `backend/app/engines/birth_position_detection.py` | Capability 7.6: BEFORE/INSIDE/AFTER classification | Capability 7.6 |
| `backend/app/engines/universal_mandali_engine.py` | Capability 7.7: Orchestrator → `mandali_advisory` | Capability 7.7 |
| `backend/app/core/canonical_json_loader.py` | Load/validate Canonical JSON transit section | Implementation Responsibilities |
| `backend/app/schemas/mandali_advisory_schema.json` | Versioned output schema | Section 12, CGP-10 |

---

## 7. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **MandaliGenerator refactor breaks TransitEngine** | HIGH | TransitEngine tests must pass after refactor. Run `test_transit_engine.py` after each change. |
| **Canonical JSON schema mismatch** | HIGH | Implement `CanonicalJSONLoader` with strict validation against Section 5 schema. |
| **Registry version drift** | MEDIUM | Enforce CRD-03: fail-fast on version mismatch. Engine declares required version. |
| **Duplicate Nakshatra-Pada data** | MEDIUM | Single source: `nakshatra_pada_registry.json`. All engines import from there. |
| **AnswerComposer integration** | MEDIUM | Add `mandali_advisory` as optional parameter; default to empty for backward compatibility. |
| **Model B appendix contamination** | LOW | Keep deprecated methods in MandaliGenerator but mark clearly; no Model A code path uses them. |

---

## 8. Recommendation

**Proceed with STEP 2: Implement first missing component — Canonical Reference Data Registries.**

Rationale:
1. **Foundation**: All capabilities (7.1–7.7) depend on the three registries.
2. **Zero risk**: Pure data files; no code execution; no existing tests affected.
3. **Validation**: Registries can be validated against Canonical JSON content (Raju chart pages 85-86).
4. **Unblocks**: NakshatraPadaResolver, MandaliGridConstruction, TransitMandaliResolution all require registries.

**Next Phase Deliverable**: Three registry JSON files + `canonical_reference_data.py` loader with versioning.

---

*End of Implementation Discovery Report — Phase IM-001*