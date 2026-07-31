# GM-012A Relationship Governance v1.0

**Status**: Architecture Review Complete  
**Version**: 1.0  
**Date**: 2026-07-29  
**Based on**: v1.0.0-gm011 Released Baseline  
**Classification**: Architecture Governance — No Implementation

---

## 1. Current Repository Baseline (v1.0.0-gm011)

### 1.1 Knowledge Graph State (Released)

| Metric | Value |
|--------|-------|
| **Nodes** | 79 |
| **Relationships** | 206 |
| **Node Types** | 12 (all spec types implemented) |
| **Relationship Types** | 13 / 19 spec types |
| **Evidence Chain Types** | 14 types supported |
| **Computed Fields** | `evidence`, `references`, `relationships` on all nodes |
| **Evidence Chain** | Working for Formula, Gochara, Probability, Yoga |
| **Frontend** | Full evidence/ref/rel display implemented |

### 1.2 Implemented Relationship Types (13/19 Spec)

| Type | Direction | Present | Count |
|------|-----------|---------|-------|
| `depends_on` | Formula → Calibration | ✅ | 50 |
| `explains` | Formula → Transit/Domain | ✅ | 5 |
| `influences` | A → B (modifies score) | ✅ | 14 |
| `references` | House → Planet | ✅ | 108 |
| `activates` | Gochara → Sadesati/Ashtam | ✅ | 2 |
| `strengthens` | Yoga → Domain | ✅ | 2 |
| `references` | House → Planet | ✅ | 108 |
| `produced_by` | Yoga → Formula | ✅ | 5 |
| `supersedes` | Governance → Governance | ✅ | 1 |
| `validated_by` | Freeze → Governance | ✅ | 1 |
| `centered_on` | Moon → Gochara | ✅ | 1 |
| `contains` | Gochara → Mandali 1-12 | ✅ | 12 |
| `resolves` | Gochara → Transit | ✅ | 4 |
| `activates` | Gochara → Sadesati/Ashtam | ✅ | 2 |
| `aggregates` | Probability → Formula | ✅ | 1 |
| `produced_by` | Yoga → Formula | ✅ | 5 |

### 1.3 Missing Spec Relationship Types (11/19 Spec Missing)

| Type | Spec Section | Purpose | Status |
|------|--------------|---------|--------|
| `uses` | 3.1 | Engine → Formula | Missing |
| `produces` | 3.1 | Engine → Node | Missing |
| `affects` | 3.1 | Transit → Domain | Missing |
| `weakens` | 3.1 | A → B (decreases score) | Missing |
| `triggered_by` | 3.1 | Event → Transit | Missing |
| `used_in` | 3.1 | Formula → Engine | Missing |
| `appears_in_report` | 3.1 | Node → Report | Missing |
| `asked_by_question` | 3.1 | Question → Node | Missing |
| `used_by_engine` | 3.1 | Node → Engine | Missing |
| `derived_from` | 3.1 | Node → Formula | Missing |
| `calibrated_by` | 3.1 | Formula → Calibration | Missing |

### 1.4 Computed Fields (Already Implemented)

All nodes already have these computed fields populated via `_enrich_node()`:

- `evidence`: `{ summary, level, confidence, source, revision, traceability, chain }`
- `references`: Cross-reference list with relevance scoring
- `relationships`: Counts by relationship type

### 1.5 Evidence Chain (Implemented)

Evidence chain types supported: `depends_on`, `explains`, `influences`, `produced_by`, `contains`, `resolves`, `activates`, `centered_on`, `aggregates`, `produced_by`, `derived_from`, `validated_by`, `explains`, `strengthens`, `weakens`, `uses`, `uses` (14 types total)

---

## 2. Relationship Governance Analysis

For each missing spec relationship, governance analysis:

---

### `uses` — Engine → Formula

| Field | Value |
|-------|-------|
| **Purpose** | Engine consumes formula (TransitEngine uses TRN-HA-001) |
| **Canonical?** | Yes — represents consumption relationship |
| **Persisted?** | **NO** — Computed at runtime from engine source |
| **Computed?** | Yes — derivable from engine source code registry |
| **Runtime Only?** | Yes |
| **Source of Truth** | Engine source code (import statements) |
| **Owning Engine** | Formula Engine (registry) |
| **Duplication Risk** | LOW — not in seed data |
| **Performance Impact** | NONE — runtime lookup only |
| **Recommendation** | **COMPUTED AT RUNTIME** — Do not persist |

**Reasoning**: Engine-formula mapping is in engine source code. Persisting duplicates source-of-truth.

---

### `produces` — Engine → Node

| Field | Value |
|-------|-------|
| **Purpose** | Engine generates node (UniversalMandaliEngine produces Gochara Mandali) |
| **Canonical?** | Yes — engine output ownership |
| **Persisted?** | **NO** — Determined by engine execution |
| **Computed?** | Yes — derivable from engine output schema |
| **Runtime Only?** | Yes |
| **Source of Truth** | Engine output + node `source: "engine"` |
| **Owning Engine** | Each engine owns its outputs |
| **Duplication Risk** | LOW — already in node `source` field |
| **Performance Impact** | NONE |
| **Recommendation** | **COMPUTED AT RUNTIME** — Query nodes by `source: "engine"` |

**Reasoning**: Node already has `source: "engine"` field. Engine ownership is derivable.

---

### `affects` — Transit → Domain

| Field | Value |
|-------|-------|
| **Purpose** | Transit activates domain (Saturn transit → Marriage domain) |
| **Canonical?** | Yes — transit-domain activation |
| **Persisted?** | **PARTIAL** — Already exists as `explains` (Formula → Transit) + `influences` (Planet → Domain) |
| **Computed?** | Yes — derivable from transit engine output |
| **Runtime Only?** | Partially |
| **Source of Truth** | TransitEngine output + NatalPromise domain scores |
| **Owning Engine** | TransitEngine |
| **Duplication Risk** | MEDIUM — Overlaps with `explains` + `influences` |
| **Performance Impact** | LOW |
| **Recommendation** | **DO NOT ADD** — Use existing `explains` + `influences` + TransitEngine output |

**Reasoning**: Already covered by `explains` (Formula→Transit) + `influences` (Planet→Domain). TransitEngine output has `activated_domains`.

---

### `weakens` — A → B (decreases score)

| Field | Value |
|-------|-------|
| **Purpose** | A decreases B's score (Saturn transit weakens Marriage) |
| **Canonical?** | Yes — inverse of `strengthens` |
| **Persisted?** | **NO** — Not in seed data |
| **Computed?** | Yes — from transit quality matrix |
| **Runtime Only?** | Yes |
| **Source of Truth** | TransitEngine quality matrix (negative weights) |
| **Owning Engine** | TransitEngine |
| **Duplication Risk** | LOW |
| **Performance Impact** | LOW — computed from transit quality |
| **Recommendation** | **PERSIST** — Add to seed data where transit quality < 0 |

**Reasoning**: Not computable from existing relationships. Transit quality matrix has negative values that need explicit representation.

---

### `triggered_by` — Event → Transit

| Field | Value |
|-------|-------|
| **Purpose** | Transit triggers event (Saturn transit → Sadesati) |
| **Canonical?** | Yes — event causation |
| **Persisted?** | **PARTIAL** — `activates` (Gochara→Sadesati) exists |
| **Computed?** | Yes — from Gochara Mandali cycles |
| **Runtime Only?** | Partially |
| **Source of Truth** | GocharaMandaliEngine cycle detection |
| **Owning Engine** | UniversalMandaliEngine |
| **Duplication Risk** | LOW — `activates` covers it |
| **Performance Impact** | NONE |
| **Recommendation** | **DO NOT ADD** — Use existing `activates` |

**Reasoning**: `activates` (Gochara→Sadesati) already represents this. `triggered_by` is inverse direction, not needed.

---

### `used_in` — Formula → Engine

| Field | Value |
|-------|-------|
| **Purpose** | Formula used in engine (PRB-AG-001 → MasterProbabilityEngine) |
| **Canonical?** | Yes — formula consumption |
| **Persisted?** | **NO** — Computed from formula registry |
| **Computed?** | Yes — from formula registry `used_by_engine` field |
| **Runtime Only?** | Yes |
| **Source of Truth** | Formula registry YAML (`used_by_engine` array) |
| **Owning Engine** | Formula Engine |
| **Duplication Risk** | LOW |
| **Performance Impact** | NONE |
| **Recommendation** | **COMPUTED AT RUNTIME** — from formula registry |

**Reasoning**: Formula registry already has `used_by_engine` array. No persistence needed.

---

### `appears_in_report` — Node → Report

| Field | Value |
|-------|-------|
| **Purpose** | Node appears in report (Saturn → Sadesati Report) |
| **Canonical?** | Yes — report inclusion |
| **Persisted?** | **NO** — Report templates define this |
| **Computed?** | Yes — from report template definitions |
| **Runtime Only?** | Yes |
| **Source of Truth** | Report templates (HTMLGenerator, schemas) |
| **Owning Engine** | Report Builder |
| **Duplication Risk** | LOW |
| **Performance Impact** | NONE |
| **Recommendation** | **COMPUTED AT RUNTIME** — from report templates |

**Reasoning**: Report templates explicitly list node types to include. Not a graph relationship.

---

### `asked_by_question` — Question → Node

| Field | Value |
|-------|-------|
| **Purpose** | Question queries node ("Will I marry?" → Marriage domain) |
| **Canonical?** | Yes — question-to-node mapping |
| **Persisted?** | **NO** — Question Router handles this |
| **Computed?** | Yes — from Question Registry mapping |
| **Runtime Only?** | Yes |
| **Source of Truth** | Question Registry (`domain` field) |
| **Owning Engine** | Question Engine |
| **Duplication Risk** | LOW |
| **Performance Impact** | NONE |
| **Recommendation** | **COMPUTED AT RUNTIME** — from Question Registry |

**Reasoning**: Question Registry already maps question_id → domain. No graph edge needed.

---

### `used_by_engine` — Node → Engine

| Field | Value |
|-------|-------|
| **Purpose** | Node consumed by engine (Sun → PlanetStrengthEngine) |
| **Canonical?** | Yes — inverse of `produces` |
| **Persisted?** | **NO** — derivable from engine input schemas |
| **Computed?** | Yes — from engine input schema validation |
| **Runtime Only?** | Yes |
| **Source of Truth** | Engine input schemas (Pydantic models) |
| **Owning Engine** | Each engine |
| **Duplication Risk** | LOW |
| **Performance Impact** | NONE |
| **Recommendation** | **COMPUTED AT RUNTIME** — from engine input schemas |

**Reasoning**: Engine input Pydantic models declare required node types. Inverse of `produces`.

---

### `derived_from` — Node → Formula

| Field | Value |
|-------|-------|
| **Purpose** | Node derived from formula (Transit Activation → TRN-HA-001) |
| **Canonical?** | Yes — derivation lineage |
| **Persisted?** | **PARTIAL** — `depends_on` (Formula→Calibration) exists |
| **Computed?** | Yes — from formula registry `output_node` field |
| **Runtime Only?** | Partially |
| **Source of Truth** | Formula registry (`output_node` field) |
| **Owning Engine** | Formula Engine |
| **Duplication Risk** | LOW |
| **Performance Impact** | LOW |
| **Recommendation** | **PERSIST** — Add to formula registry output_node, seed in KG |

**Reasoning**: Critical for evidence chain. Formula registry has `output_node`. Should be seeded as `derived_from` relationship.

---

### `calibrated_by` — Formula → Calibration

| Field | Value |
|-------|-------|
| **Purpose** | Formula uses calibration (Dignity Score → Own Sign) |
| **Canonical?** | Yes — inverse of `depends_on` |
| **Persisted?** | **PARTIAL** — `depends_on` (Formula→Calibration) exists |
| **Computed?** | Yes — inverse of `depends_on` |
| **Runtime Only?** | No — should be seeded |
| **Source of Truth** | Formula registry (5 calibrations per formula) |
| **Owning Engine** | Formula Engine |
| **Duplication Risk** | MEDIUM — inverse of `depends_on` |
| **Performance Impact** | LOW |
| **Recommendation** | **SEED AS INVERSE** — Auto-generate from `depends_on` at seed time |

**Reasoning**: `depends_on` already seeded (50 relationships). `calibrated_by` is exact inverse. Auto-generate at seed time, no manual maintenance.

---

## 3. Persisted vs Computed Decision Matrix

| Relationship | Persist in KG | Compute at Runtime | Notes |
|--------------|---------------|-------------------|-------|
| `depends_on` | ✅ SEED | — | Core evidence chain |
| `explains` | ✅ SEED | — | Core evidence chain |
| `influences` | ✅ SEED | — | Core evidence chain |
| `references` | ✅ SEED | — | House→Planet |
| `activates` | ✅ SEED | — | Gochara→Sadesati |
| `strengthens` | ✅ SEED | — | Yoga→Domain |
| `contains` | ✅ SEED | — | Gochara→Mandali |
| `resolves` | ✅ SEED | — | Gochara→Transit |
| `activates` | ✅ SEED | — | Gochara→Sadesati |
| `aggregates` | ✅ SEED | — | Probability→Formula |
| `produced_by` | ✅ SEED | — | Yoga→Formula |
| `supersedes` | ✅ SEED | — | Governance |
| `validated_by` | ✅ SEED | — | Governance |
| `centered_on` | ✅ SEED | — | Moon→Gochara |
| `contains` | ✅ SEED | — | Gochara→Mandali |
| `resolves` | ✅ SEED | — | Gochara→Transit |
| `aggregates` | ✅ SEED | — | Probability→Formula |
| `produced_by` | ✅ SEED | — | Yoga→Formula |
| **`weakens`** | ✅ **SEED** | — | **ADD: Transit quality < 0** |
| **`derived_from`** | ✅ **SEED** | — | **ADD: Formula→Output node** |
| **`calibrated_by`** | ✅ **AUTO-SEED** | — | **AUTO from `depends_on` inverse** |
| `uses` | — | ✅ COMPUTE | Engine→Formula (from registry) |
| `produces` | — | ✅ COMPUTE | Engine→Node (from node.source) |
| `affects` | — | ✅ COMPUTE | Use `explains`+`influences`+Transit output |
| `triggered_by` | — | ✅ COMPUTE | Use `activates` inverse |
| `used_in` | — | ✅ COMPUTE | From formula registry `used_by_engine` |
| `appears_in_report` | — | ✅ COMPUTE | From report templates |
| `asked_by_question` | — | ✅ COMPUTE | From Question Registry domain |
| `used_by_engine` | — | ✅ COMPUTE | From engine input schemas |
| `calibrated_by` | — | ✅ AUTO-SEED | Inverse of `depends_on` |

---

## 4. Architecture Compliance Check

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **One Source of Truth** | ✅ | Each relationship has single owner |
| **Deterministic** | ✅ | All computed relationships are deterministic |
| **No Duplicate Logic** | ✅ | Inverse relationships auto-generated |
| **Engine Ownership** | ✅ | Each relationship has owning engine |
| **Parameter-Driven** | ✅ | Seed data driven by registries |
| **No Stored Derived Values** | ✅ | Computed fields not persisted |

---

## 5. Final Approved Relationship Contract

### 5.1 Persisted (Seed Data) — 18 Types

| Type | Seed Source | Owner |
|------|-------------|-------|
| `depends_on` | Formula Registry | Formula Engine |
| `explains` | Formula Registry | Formula Engine |
| `influences` | Formula Registry | Formula Engine |
| `references` | House-Planet matrix | House Engine |
| `activates` | Gochara Engine | UniversalMandaliEngine |
| `strengthens` | Yoga Engine | Yoga Engine |
| `contains` | Gochara Engine | UniversalMandaliEngine |
| `resolves` | Gochara Engine | UniversalMandaliEngine |
| `activates` | Gochara Engine | UniversalMandaliEngine |
| `aggregates` | MasterProbabilityEngine | MasterProbabilityEngine |
| `produced_by` | Yoga Engine | Yoga Engine |
| `supersedes` | Governance docs | Governance |
| `validated_by` | Governance docs | Governance |
| `centered_on` | Gochara Engine | UniversalMandaliEngine |
| `contains` | Gochara Engine | UniversalMandaliEngine |
| `resolves` | Gochara Engine | UniversalMandaliEngine |
| `aggregates` | MasterProbabilityEngine | MasterProbabilityEngine |
| `produced_by` | Yoga Engine | Yoga Engine |
| `weakens` | **NEW** TransitEngine | TransitEngine |
| `derived_from` | **NEW** Formula Registry | Formula Engine |
| `calibrated_by` | **AUTO from `depends_on`** | Formula Engine |

---

### 5.2 Computed at Runtime — 11 Types

| Type | Computed From | Owner |
|------|---------------|-------|
| `uses` | Engine source imports | Formula Engine |
| `produces` | Node `source` field | Each Engine |
| `affects` | TransitEngine output | Transit Engine |
| `triggered_by` | `activates` inverse | UniversalMandaliEngine |
| `used_in` | Formula Registry `used_by_engine` | Formula Engine |
| `appears_in_report` | Report templates | Report Builder |
| `asked_by_question` | Question Registry domain | Question Engine |
| `used_by_engine` | Engine input schemas | Each Engine |
| `calibrated_by` | Inverse of `depends_on` | Formula Engine |
| `derived_from` | Formula Registry `output_node` | Formula Engine |
| `calibrated_by` | Inverse of `depends_on` | Formula Engine |

---

## 6. Implementation Recommendations for GM-012B

### 6.1 Phase 1: Seed Data Updates (Week 1)

```python
# 1. Add `weakens` relationships for negative transit quality
# 2. Add `derived_from` from formula_registry.output_node
# 3. Auto-generate `calibrated_by` from `depends_on` inverse
# 4. Seed `weakens` for transit quality < 0
```

### 6.2 Phase 2: Runtime Computed Properties (Week 2)

```python
# Add to KnowledgeStore:
def get_node_uses(self, node_id):        # from engine imports
def get_node_produces(self, node_id):    # from node.source
def get_node_affects(self, node_id):     # from TransitEngine output
def get_node_calibrated_by(self, node_id): # inverse of depends_on
# ... etc for all 11 computed types
```

### 6.3 Phase 3: API Serialization (Week 3)

```python
# Update knowledge.py endpoints to include computed relationships
# Update frontend nodeRegistry.ts with new types (already done)
# Update KnowledgeGraphViewer to display computed relationships
```

---

## 7. Approval Record

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Chief Architect |  |  |  |
| Product Owner |  |  |  |
| Engineering Lead |  |  |  |

---

**Document Control**: This document governs all Knowledge Graph relationship decisions for v1.1+. No implementation may proceed without compliance.

---

*End of GM-012A Relationship Governance v1.0*