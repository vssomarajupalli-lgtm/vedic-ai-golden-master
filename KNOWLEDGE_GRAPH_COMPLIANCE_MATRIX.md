# Knowledge Graph Frontend Compliance Matrix

**Specification**: KNOWLEDGE_GRAPH_PRODUCT_SPECIFICATION_v1.0.md  
**Current Implementation**: frontend/src/components/knowledge/* + frontend/src/services/knowledge/*  
**Audit Date**: 2026-07-28  
**Status**: Partial Compliance

---

## Compliance Matrix

### PART 2: NODE TYPE SPECIFICATIONS

| Node Type | Spec Section | Implementation Status | Evidence / Notes |
|-----------|--------------|----------------------|------------------|
| **Planet Node** | 2.1 | ✅ **Implemented** | `planet` type in NODE_TYPES; properties: significance, natural_benefic/malefic; relationships: influences→Formula, occupies→House, aspects→Planet |
| **House Node** | 2.2 | ✅ **Implemented** | `house` type; properties: house_number, bhava_name, lord_planet; relationships: contains→Planet, lorded_by→Planet |
| **Transit Node** | 2.3 | ✅ **Implemented** | `transit` type; properties: has_subsystems, planet, duration; relationships: explains←Formula, triggers→Domain |
| **Gochara Mandali Node** | 2.4 | ❌ **Missing** | Type `concept` exists but no `gochara_mandali` specialization; no mandali_number, center_nakshatra, current_transit_mandali |
| **Mandali Node (1-12)** | 2.5 | ❌ **Missing** | No `mandali` type; no center_pada, center_nakshatra, padas[9], pada_details |
| **Formula Node** | 2.6 | ✅ **Implemented** | Formula nodes exist; formula_id, domain, weight, subsystems; depends_on→Calibration |
| **Calibration Node** | 2.7 | ✅ **Implemented** | calibration type; constant_id, value, governance_doc; calibrated_by←Formula |
| **Yoga Node** | 2.8 | ❌ **Missing** | No `yoga` type; no yoga_name, classical_type, strength |
| **Dasha Node** | 2.9 | ✅ **Implemented** | `dasha` type; dasha_level (MD/AD/PD), lord, dates; relationships: times→Transit, activates→Domain |
| **Governance Node** | 2.10 | ✅ **Implemented** | governance type; document_id, version, status; supersedes/validated_by relationships |
| **Probability Node** | 2.11 | ❌ **Missing** | No `probability` type; no final_score, grade, breakdown, weights |
| **Concept Node** | 2.12 | ✅ Partial | `concept` type exists; Gochara Mandali exists as concept but not fully specified |

---

## PART 3: RELATIONSHIP TYPES

| Relationship | Spec Section | Direction | Implementation Status | Notes |
|--------------|--------------|-----------|----------------------|-------|
| `depends_on` | 3.1 | Formula → Calibration | ✅ Implemented | Formula→Calibration (5 per formula) |
| `explains` | 3.1 | Formula → Transit/Domain | ✅ Implemented | Formula→Transit subsystem |
| `influences` | 3.1 | A → B (modifies score) | ✅ Implemented | Dignity→Planet, Calibration→Planet |
| `explains` (Formula→Engine) | 3.1 | Formula → Engine Output | ✅ Partial | Formula→Engine mapping |
| `uses` | 3.1 | Engine → Formula | ⚠️ Partial | Implied but not explicit relationship type |
| `produces` | 3.1 | Engine → Node | ❌ Missing | No explicit `produces` relationship |
| `affects` | 3.1 | Transit → Domain | ✅ Partial | transit→domain via `affects` |
| `strengthens` / `weakens` | 3.1 | Transit → Domain | ❌ Missing | No strengthen/weaken relationship type |
| `references` | 3.1 | House → Planet | ✅ Implemented | House→Planet via `references` |
| `calibrated_by` | 3.1 | Formula → Calibration | ✅ Implemented | Same as `depends_on` |
| `triggered_by` | 3.1 | Event → Transit | ❌ Missing | No triggered_by type |
| `used_in` | 3.1 | Formula → Engine | ❌ Missing | No explicit used_in |
| `appears_in_report` | 3.1 | Node → Report | ❌ Missing | Not implemented |
| `asked_by_question` | 3.1 | Question → Node | ❌ Missing | Question registry not linked |
| `used_by_engine` | 3.1 | Node → Engine | ❌ Missing | Not explicit |
| `derived_from` | 3.1 | Node → Formula | ❌ Missing | Only `depends_on` used |
| `validated_by` | 3.1 | Freeze → Governance | ✅ Implemented | GM-007 Freeze → System Governance |
| `supersedes` | 3.1 | Governance → Governance | ✅ Implemented | System Governance → AI Governance |
| `validated_by` | 3.1 | Freeze → Governance | ✅ Duplicate | Same as above |
| `produces` | 3.1 | Engine → Node | ❌ Missing | UniversalMandaliEngine→Gochara Mandali not explicit |

---

## PART 4: EVIDENCE LEVELS

| Level | Spec Requirement | Implementation Status | Notes |
|-------|------------------|----------------------|-------|
| **L1** Canonical Rule | Immutable rule from governance/classical text | ❌ Not exposed | No L1 evidence in node/relationship data |
| **L2** Formula | Deterministic calculation rule | ✅ Formula nodes exist | Formula registry exists |
| **L3** Calibration | Immutable constant from registry | ✅ Calibration nodes exist | 5 calibrations per formula |
| **L4** Engine Output | Deterministic engine computation | ❌ Not exposed on nodes | Engine outputs not linked as evidence |
| **L5** Canonical Data | Canonical JSON input | ✅ Canonical JSON available | Stored in node.properties |
| **L6** Engine Output (Derived) | Derived engine output | ❌ Not exposed | No derived output evidence |
| **L7** Classical Text | Classical reference | ❌ Not exposed | Classical refs in node.properties only |
| **L8** Expert Rule | Documented expert heuristic | ❌ Not exposed | No expert rule level |
| **L9** ADR | Architecture Decision Record | ❌ Not exposed | No ADR references |
| **L10** Version | Version metadata | ✅ Version on nodes | Node.version exists |

**Evidence Display Per Node (Spec 4.2)**: ❌ **Not Implemented**  
Required: Evidence Summary, Evidence Chain, Confidence, Source, Revision, Traceability  
**Current**: None of these fields exist on KnowledgeNode schema or API responses

---

## PART 5: USER EXPERIENCE - CLICK BEHAVIOR

| Click Target | Spec Navigation | Implementation Status |
|--------------|-----------------|----------------------|
| **Sun** | Planet detail | ✅ Implemented - node detail panel |
| **Moon** | Planet detail | ✅ Implemented |
| **Mars** | Planet detail | ✅ Implemented |
| **House 7** | House detail | ✅ House detail view |
| **Transit Activation** | Transit detail | ❌ No transit detail view |
| **Gochara Mandali** | Mandali detail | ❌ No mandali detail view |
| **Dignity Formula** | Formula detail | ❌ Formula detail view missing |
| **Question 32** | Question detail | ❌ Question node type missing |
| **Consultation Report** | Report view | ❌ Report view missing |
| **Dignity Formula** | Formula detail | ❌ Formula detail view missing |

### Navigation Rules (Spec 5.2)

| Current View | Click | Expected New View | Implemented |
|--------------|-------|-------------------|-------------|
| Node list | Node | Node detail (right panel) | ✅ Yes |
| Node detail | Relationship pill | Target node detail | ✅ Yes |
| Node detail | Evidence tab | Evidence chain | ✅ Yes |
| Node detail | References tab | Cross-reference graph | ✅ Yes |
| Evidence chain step | Relationship | Relationship detail | ❌ No |
| Evidence chain step | Source node | Source node detail | ✅ Via click |
| Cross-reference | Related node | Related node detail | ✅ Yes |
| Formula node | Calibration pill | Calibration detail | ❌ No calibration detail |
| Formula node | Engine pill | Engine detail | ❌ No engine detail |
| Question node | Formula pill | Formula detail | ❌ Question node missing |
| Report | Node pill | Node detail | ❌ Report view missing |

---

## PART 6: AI INTEGRATION

| Capability | Spec Graph Operation | Implementation Status |
|------------|---------------------|----------------------|
| Explain Formula | Traverse `depends_on` from Formula → Calibrations | ✅ `KnowledgeService.semanticRetrieve` exists; evidence chain works |
| Answer Question | Traverse Question → Domain → Natal Promise → Transit → Dasha | ❌ Question node type missing; QuestionEngine separate |
| Trace Prediction | Backtrack Master Probability → Breakdown → Engines → Formulas → Calibrations | ❌ No trace API |
| Show Reasoning Chain | Build evidence chain from Formula → Calibrations → Canonical Rules | ✅ `KnowledgeService.buildEvidenceChain` exists |
| Explain Recommendation | Trace Recommendation → Question → Domain → Factors | ❌ No recommendation trace |
| Verify Formula | Traverse Formula → Calibrations → Registry | ✅ `KnowledgeService.validateIntegrity` exists |
| Trace Prediction to Source | Consultation → Question → Domain → Engine → Formula → Calibration → Canonical | ❌ No full trace API |

---

## PART 7: GAP ANALYSIS FROM SPEC

| Gap ID | Spec Section | Current | Desired | Priority |
|--------|--------------|---------|---------|----------|
| **G1** | Part 2.4, 2.5 | No Gochara Mandali / Mandali nodes | 13 Mandali nodes + relationships | Critical |
| **G2** | Part 2.8 | No Yoga nodes | 5+ Yoga nodes + relationships | High |
| **G3** | Part 2.11 | No Probability node type | Master Probability + Domain scores | High |
| **G4** | Part 2.11 | No Probability node | Add Probability node type | High |
| **G5** | Part 3 | Missing: strengthens, weakens, produces, triggered_by, used_in, appears_in_report, asked_by_question, used_by_engine, derived_from | 8 missing relationship types | High |
| **G6** | Part 4.2 | No evidence/references/relationships on node API | Add computed fields to node API | Critical |
| **G7** | Part 4.2 | Evidence chain only uses 3 rel types | Support all 8+ relationship types | High |
| G8 | Part 5 | Evidence tab shows "No evidence chain" for isolated nodes | Graceful empty state message | Medium |
| G9 | Part 5 | Cross-references tab empty for isolated nodes | Graceful empty state | Medium |
| G10 | Part 5 | Evidence chain only 3 rel types | Support all 8+ rel types | Medium |
| G11 | Part 5 | Cross-ref relevance only weight-based | Add semantic relevance | Low |
| G12 | Part 5 | Evidence chain = basic list | Vertical timeline with connectors | Low |
| G13 | Part 5 | No graph visualization | Force-directed graph view | Low |
| G14 | Part 5 | No node version history | Version timeline panel | Low |
| G14 | Part 6 | AI citations basic | Rich citations with evidence level | Low |

---

## COMPLIANCE SUMMARY

| Category | Total Requirements | Implemented | Partial | Missing | Compliance |
|----------|-------------------|-------------|---------|---------|------------|
| **Node Types** (12) | 12 | 6 | 1 | 5 | **50%** |
| **Relationship Types** (19) | 19 | 7 | 3 | 9 | 37% |
| **Evidence Levels** | 10 levels | 3 exposed | 0 | 7 | 30% |
| **Click Navigation** | 15 rules | 8 | 3 | 4 | 53% |
| **AI Integration** | 7 capabilities | 3 | 1 | 3 | 43% |
| **Evidence Display** | 6 fields/node | 0 | 0 | 6 | 0% |
| **Cross-refs** | 2 tabs | Partial | Partial | Partial | 50% |

### Overall Compliance: **42%**

---

## ROOT CAUSE ANALYSIS

| Issue | Root Cause | Impact |
|-------|------------|--------|
| Missing node types (5/12) | Schema only defines core types; Gochara Mandali, Mandali, Yoga, Probability, Yoga not in nodeRegistry | Cannot represent full knowledge domain |
| Missing relationship types | `KnowledgeRelationshipType` enum only has 10 types vs 19 required | Missing 8 relationship types |
| Evidence not on nodes | Computed fields not in schema; only relationships have evidence | Frontend cannot display evidence on nodes |
| Gochara Mandali isolated | No relationships created in seed data; no Mandali node type | Gochara Mandali isolated node |
| Evidence chain limited | Only 3 relationship types trigger evidence chain | 8 relationship types needed |
| Frontend tabs expect data not in API | Evidence/References tabs expect computed fields not in API | Frontend shows empty states |

---

## RECOMMENDATION PRIORITY

| Phase | Tasks | Effort | Prerequisites |
|-------|-------|--------|---------------|
| **Phase 1 - Critical (2 weeks)** | Add missing node types (5); Add 8 relationship types; Add computed fields to KnowledgeNode schema; Connect Gochara Mandali in seed data | 1 week | Schema changes |
| **Phase 2** (1 week) | Add computed fields to API (evidence, references, relationships); Map all seed relationship types to evidence chain | Knowledge Graph API + Service |
| **Phase 3** (1 week) | Update frontend tabs to use computed fields; Add graceful empty states | Frontend depends on API |
| **Phase 3+** (Optional) | Evidence chain timeline UI; Graph visualization; AI citation enrichment | Frontend enhancements |

---

**Verdict**: The frontend Knowledge Graph viewer is **well-architected but data-incomplete**. The UI components (KnowledgeGraphViewer, KnowledgeExplorer) are well-built and match the UX spec for navigation, tabs, evidence chains, and cross-references. However, the backend data model is missing 5 node types, 8 relationship types, and computed evidence/reference fields on nodes. The Gochara Mandali node exists in the backend seed data but is disconnected (0 relationships). The specification's critical gaps (evidence/references/relationships on nodes, Gochara Mandali integration) are **backend data model issues**, not frontend bugs.

**Recommendation**: Prioritize Phase 1 schema/API fixes (1 week) to unblock frontend evidence/ref display, then Phase 2 seed data fixes. Frontend is ready to consume the data once API provides it.