# BKL_009 Knowledge Graph Product Completion Plan

**Version**: 1.0  
**Date**: 2026-07-28  
**Status**: Active  
**Based on**: KNOWLEDGE_GRAPH_PRODUCT_SPECIFICATION_v1.0.md, KNOWLEDGE_GRAPH_COMPLIANCE_MATRIX.md, GM_011_ENGINEERING_CHANGE_SUMMARY.md

---

## REPOSITORY VERIFICATION SUMMARY

### What Already Exists (Verified)

#### Backend (Complete & Operational)
- ✅ `app/schemas/knowledge.py` — Pydantic models for nodes, relationships, evidence chains, cross-references, insights, integrity
- ✅ `app/core/knowledge_store.py` — Full CRUD, search, evidence chains, cross-references, domain insights, integrity validation, seed data (53 nodes, 179 relationships)
- ✅ `app/api/v1/endpoints/knowledge.py` — All 8 endpoints: `/state`, `/nodes`, `/nodes/{id}`, `/relationships`, `/evidence-chain/{id}`, `/cross-references/{id}`, `/insights/{domain}`, `/insights`, `/integrity`, `/search`, `/seed`
- ✅ `backend/app/database/knowledge_graph.json` — Persisted data (53 nodes, 179 relationships)
- ✅ Router registration: `GET /api/v1/knowledge/*`

#### Frontend (Complete & Operational)
- ✅ `frontend/src/services/knowledge/nodeRegistry.ts` — 11 node types, 11 relationship types, 14 domains
- ✅ `frontend/src/services/knowledge/knowledgeRepository.ts` — Zustand store with persistence, search, indexing, integrity
- ✅ `frontend/src/services/knowledge/knowledgeService.ts` — Semantic retrieval, evidence chain, cross-references, citations, audit
- ✅ `frontend/src/components/knowledge/KnowledgeGraphViewer.tsx` — Full UI: browse, detail, evidence chain, cross-references, insights, integrity tabs
- ✅ `frontend/src/components/knowledge/KnowledgeExplorer.tsx` — Graph overview, relationship explorer, formula evidence, integrity

#### Seed Data (Exists but Incomplete)
- ✅ 53 nodes: 9 planets, 12 houses, 10 formulas, 5 calibrations, 4 transit, 9 dasha, 3 governance, 1 concept (Gochara Mandali)
- ✅ 179 relationships: depends_on, explains, influences, references, supersedes, validated_by
- ✅ Integrity: VALID (0 issues)
- ⚠️ **Gochara Mandali node is ISOLATED (0 relationships)** — Root cause confirmed

---

### What Is PARTIALLY Implemented (Per Compliance Matrix & Spec)

| Spec Requirement | Current State | Gap |
|------------------|---------------|-----|
| **Node Types (12 spec)** | 6/12 implemented | Missing: `gochara_mandali`, `mandali`, `yoga`, `probability`, `question` (specialized) |
| **Relationship Types (19 spec)** | 7/19 implemented | Missing: `produces`, `uses`, `strengthens`, `weakens`, `triggered_by`, `used_in`, `appears_in_report`, `asked_by_question`, `used_by_engine`, `derived_from` (8 of 19) |
| **Evidence Levels (10)** | 3 exposed (L2, L3, L10) | L1, L4, L5, L6, L7, L8, L9 not on nodes |
| **Evidence Display on Nodes** | 0/6 fields | Missing: evidence_summary, evidence_chain, confidence, source, revision, traceability |
| **Gochara Mandali Connections** | 0 relationships | Must connect to Moon, Mandali 1-12, Transits, Sadesati/Elinati/Ashtama |
| **Mandali 1-12 Nodes** | 0 nodes | 12 mandali nodes needed with pada details |
| **Formula→Calibration Evidence Chain** | Only `depends_on` | Need `derived_from`/`validated_by` mapping |
| **Cross-Reference Relevance** | Weight-only | Need semantic relevance (domain/formula/planet overlap) |
| **AI Integration Capabilities** | 3/7 | Missing: Answer Question, Trace Prediction, Explain Recommendation, Trace to Source |

---

### What Is GENUINELY MISSING (Version 1.0 Mandatory)

| Category | Missing Items | Spec Section |
|----------|---------------|--------------|
| **Node Types** | `gochara_mandali` (specialized concept), `mandali` (1-12), `yoga`, `probability` | 2.4, 2.5, 2.8, 2.11 |
| **Relationship Types** | `produces`, `uses`, `strengthens`, `weakens`, `triggered_by`, `used_in`, `appears_in_report`, `asked_by_question`, `used_by_engine` | 3.1 |
| **Computed Fields on Nodes** | `evidence`, `references`, `relationships` fields in API response | 4.2, 5.1, 5.2, BL-001, BL-003, BL-005 |
| **Gochara Mandali Seed Relationships** | Connect to Moon, 12 Mandalis, Transits, Sadesati/Elinati/Ashtama | 2.4, BL-002 |
| **Evidence Chain Type Mapping** | Support `depends_on`, `explains`, `influences` → evidence chain | 3.1, 4.1, BL-004, BL-007 |
| **Evidence Levels on Nodes** | L1-L10 evidence display per node | 4.1, 4.2 |

---

## VERSION CLASSIFICATION

### ✅ VERSION 1.0 MANDATORY (Release Blockers)

| ID | Task | Priority | Effort | Classification |
|----|------|----------|--------|----------------|
| **V1-01** | Add missing node types to backend schema: `gochara_mandali`, `mandali`, `yoga`, `probability` | Critical | 2 days | **V1.0** |
| **V1-02** | Add missing node types to frontend nodeRegistry.ts | Critical | 1 day | **V1.0** |
| **V1-03** | Add missing relationship types to backend schema & store | Critical | 2 days | **V1.0** |
| **V1-04** | Add missing relationship types to frontend nodeRegistry.ts | Critical | 1 day | **V1.0** |
| **V1-05** | Add computed fields to KnowledgeNode schema: `evidence`, `references`, `relationships` | Critical | 2 days | **V1.0** |
| **V1-06** | Implement computed fields in KnowledgeStore: `get_node_evidence()`, `get_node_references()`, `get_node_relationships()` | Critical | 3 days | **V1.0** |
| **V1-07** | Serialize computed fields in API responses (`/nodes`, `/nodes/{id}`, `/state`) | Critical | 1 day | **V1.0** |
| **V1-08** | Connect Gochara Mandali in seed data: relationships to Moon, Mandali 1-12, Transits, Sadesati/Elinati/Ashtama | Critical | 2 days | **V1.0** |
| **V1-09** | Add Mandali 1-12 nodes with properties (center_nakshatra, padas[9], pada_details) | Critical | 2 days | **V1.0** |
| **V1-10** | Map seed relationship types to evidence chain: `depends_on`, `explains`, `influences` → evidence chain | High | 2 days | **V1.0** |
| **V1-11** | Update frontend to display computed fields (evidence/ref/rel counts on nodes) | Critical | 2 days | **V1.0** |
| **V1-12** | Add evidence levels (L1-L10) computation and display per node | High | 3 days | **V1.0** |

**V1.0 Total: 23 days**

---

### ⏭️ VERSION 1.1 (Post-Release Enhancements)

| ID | Task | Priority | Effort | Classification |
|----|------|----------|--------|----------------|
| V1.1-01 | Cross-reference semantic relevance (domain/formula/planet overlap) | Medium | 3 days | V1.1 |
| V1.1-02 | Evidence chain visual timeline (vertical connectors, step markers) | Low | 3 days | V1.1 |
| V1.1-03 | Graph visualization view (force-directed D3/Cytoscape) | Low | 5 days | V1.1 |
| V1.1-04 | Node version history UI panel | Low | 2 days | V1.1 |
| V1.1-05 | AI citation enhancement (rich citations with evidence level) | Low | 1 day | V1.1 |
| V1.1-06 | AI Integration: Answer Question, Trace Prediction, Explain Recommendation, Trace to Source | Medium | 8 days | V1.1 |
| V1.1-07 | Question node type + Question Engine integration | Medium | 3 days | V1.1 |
| V1.1-08 | Report view + appears_in_report relationships | Low | 3 days | V1.1 |
| V1.1-09 | `strengthens`/`weakens` transit→domain relationships from TransitEngine | Medium | 2 days | V1.1 |
| V1.1-10 | Yoga nodes from YogaEngine output | Medium | 2 days | V1.1 |

**V1.1 Total: 32 days** — **DEFERRED**

---

## DEPENDENCIES & IMPLEMENTATION ORDER

```
Phase 1: Schema & Types (Days 1-4)
  V1-01 (Backend schema) ──► V1-02 (Frontend registry)
  V1-03 (Backend rel types) ──► V1-04 (Frontend registry)
  
Phase 2: Computed Fields & API (Days 5-9)
  V1-05 (Schema fields) ──► V1-06 (Store computation) ──► V1-07 (API serialization)
  
Phase 3: Seed Data & Evidence Chain (Days 10-14)
  V1-08 (Gochara Mandali connections) + V1-09 (Mandali 1-12 nodes)
  V1-10 (Evidence chain type mapping)
  
Phase 4: Frontend Integration (Days 15-17)
  V1-11 (Display computed fields)
  
Phase 5: Evidence Levels (Days 18-20)
  V1-12 (L1-L10 per node)
```

---

## AFFECTED FILES

### Backend Files (Modified)
| File | Changes Required |
|------|------------------|
| `app/schemas/knowledge.py` | Add `gochara_mandali`, `mandali`, `yoga`, `probability` to node types; add 9 missing relationship types; add computed fields `evidence`, `references`, `relationships` to `KnowledgeNode` |
| `app/core/knowledge_store.py` | Add `get_node_evidence()`, `get_node_references()`, `get_node_relationships()`; update `seed_default_data()` with Gochara Mandali connections + 12 Mandali nodes; update `build_evidence_chain()` to support `depends_on`, `explains`, `influences` |
| `app/api/v1/endpoints/knowledge.py` | Ensure computed fields serialize in responses (Pydantic handles if in schema) |

### Frontend Files (Modified)
| File | Changes Required |
|------|------------------|
| `frontend/src/services/knowledge/nodeRegistry.ts` | Add 4 node types + 9 relationship types to enums/catalogs |
| `frontend/src/components/knowledge/KnowledgeGraphViewer.tsx` | Display `evidence`, `references`, `relationships` counts on node list/detail; show evidence levels |
| `frontend/src/components/knowledge/KnowledgeExplorer.tsx` | Update relationship type breakdown to include new types |

### Data Files (Modified)
| File | Changes Required |
|------|------------------|
| `backend/app/database/knowledge_graph.json` | Will be regenerated by updated `seed_default_data()` on next backend start |

---

## VERSION 1.0 REMAINING BLOCKERS

| Blocker | Status | Resolution |
|---------|--------|------------|
| Gochara Mandali isolated (0 relationships) | **OPEN** | V1-08 + V1-09 (seed data fix) |
| 5 missing node types in schema/registry | **OPEN** | V1-01, V1-02 |
| 9 missing relationship types in schema/registry | **OPEN** | V1-03, V1-04 |
| Computed fields not on nodes (evidence/ref/rel) | **OPEN** | V1-05, V1-06, V1-07 |
| Evidence chain only supports 3 rel types | **OPEN** | V1-10 |
| No Mandali 1-12 nodes in seed data | **OPEN** | V1-09 |
| No evidence levels (L1-L10) on node display | **OPEN** | V1-12 |
| PDF generation (WeasyPrint OS deps) | **OPEN** | DevOps task (outside KG scope) |
| Tauri sidecar rebuild | **OPEN** | Frontend task (outside KG scope) |

---

## COMPLEXITY ESTIMATES

| Component | Files | Lines Changed | Complexity |
|-----------|-------|---------------|------------|
| Backend Schema | 1 | ~50 | Low |
| Knowledge Store | 1 | ~150 | Medium |
| API Endpoints | 1 | ~20 | Low |
| Frontend Registry | 1 | ~80 | Low |
| Frontend Viewer | 1 | ~100 | Medium |
| Frontend Explorer | 1 | ~50 | Low |
| Seed Data Logic | 1 | ~200 | Medium |
| **Total** | **7** | **~650** | **Medium** |

---

## IMPLEMENTATION RULES (Per Session Protocol)

1. **One Formula → One Owner**: Each new node/relationship type has single definition location
2. **One Feature → One Implementation**: Evidence chain logic only in `knowledge_store.py`; frontend consumes API
3. **One Source of Truth**: Node types in `schemas/knowledge.py` + `nodeRegistry.ts` (kept in sync)
4. **Parameter Driven**: No hardcoded node IDs in seed data; use lookup by label/type
5. **No Duplicate Logic**: Evidence chain computation stays in backend; frontend only displays

---

## SUCCESS CRITERIA FOR VERSION 1.0 COMPLETION

| Metric | Current | Target V1.0 |
|--------|---------|-------------|
| Overall Compliance | 42% | ≥90% |
| Node Types Implemented | 6/12 | 11/12* |
| Relationship Types | 7/19 | 16/19* |
| Evidence Levels on Nodes | 0/10 | 10/10 |
| Computed Fields on Nodes | 0/3 | 3/3 |
| Gochara Mandali Connected | No | Yes (5+ relationships) |
| Mandali 1-12 Nodes | 0 | 12 |
| Evidence Chain Coverage | 3 rel types | 6+ rel types |
| API Returns Computed Fields | No | Yes |

*Missing 1 node type (`concept` already exists; `question` deferred to V1.1), 3 relationship types (`supersedes`, `validated_by` exist; `derived_from` added; remaining 3 deferred to V1.1)

---

## NEXT STEPS

1. **Begin Phase 1**: Modify `app/schemas/knowledge.py` to add missing node types, relationship types, and computed fields
2. **Update `nodeRegistry.ts`** to match backend types
3. **Enhance `knowledge_store.py`** with computed field methods and updated seed data
4. **Regenerate seed data** by restarting backend (auto-seeds on empty)
5. **Verify API responses** include computed fields
6. **Update frontend components** to display new fields
7. **Test evidence chain** with new relationship type mappings
8. **Validate compliance** against matrix

---

*End of Plan. Ready for Phase 1 implementation.*