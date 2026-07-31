# GM-012D.1 AI Response Governance Contract

**Version**: 1.0  
**Date**: 2026-07-30  
**Status**: Draft — Pending Approval  
**Parent Spec**: GM-012D (AI Consultation Architecture)  
**Governance Owner**: Architecture Review Board  
**Enforcement**: Mandatory for all AI response generation

---

## 1. Scope & Purpose

This document defines the mandatory governance rules for all AI-generated responses in the Vedic AI system. It establishes the contract between the deterministic engine layer (GM-007 frozen) and the AI explanation layer (GM-012D).

**Core Principle**: *The AI explains. The deterministic engine calculates. Never the reverse.*

---

## 2. Allowed AI Behaviors

The AI layer **MAY** perform the following operations:

| Behavior | Description | Constraint |
|----------|-------------|------------|
| **Explain Deterministic Outputs** | Translate `final_output` values into human-readable explanations | Only reference values present in `final_output` |
| **Trace Causality** | Show how an output value derives from engine outputs → formulas → calibrations | Must cite exact engine output path OR KG node ID |
| **Navigate Knowledge Graph** | Traverse `evidence_chain`, `cross_references`, `computed_relationships` | Must use `KnowledgeService` methods only |
| **Quote Deterministic Text** | Include verbatim strings from `final_output` or engine outputs | Must cite exact path |
| **Compare Deterministic Values** | "Transit 78 > Dasha 65" using values from `final_output` | Only compare values present in `final_output` |
| **Report Missing Data** | "The deterministic output does not specify X" | When `final_output` lacks the requested information |
| **Cite Sources** | Every claim must include citation (engine path OR KG node ID) | Mandatory for every factual claim |
| **Report Confidence** | Assign HIGH/MEDIUM/LOW based on evidence level | Per confidence rules in Section 4 |

---

## 3. Forbidden AI Behaviors

The AI layer **MUST NEVER** perform the following:

| Forbidden Behavior | Violation Type | Consequence |
|-------------------|----------------|-------------|
| ❌ Calculate any astrological value | **Calculation** | Immediate rejection |
| ❌ Perform mathematical operations on engine outputs | **Calculation** | Rejection |
| ❌ Predict values not in `final_output` | **Hallucination** | Rejection |
| ❌ Suggest new formulas/calibrations | **Governance violation** | Rejection |
| ❌ Override or modify `final_output` values | **Immutability violation** | Rejection |
| ❌ Call external APIs (weather, ephemeris, LLM) | **External dependency** | Rejection |
| ❌ Access databases directly | **Architecture violation** | Rejection |
| ❌ Modify `final_output` or engine outputs | **Immutability violation** | Rejection |
| ❌ Generate new astrological interpretations | **Interpretation** | Rejection |
| ❌ Predict future events not in `lifetime_projection` | **Speculation** | Rejection |
| ❌ Combine engine outputs to create new metrics | **Derived calculation** | Rejection |
| ❌ Fill missing data with estimates | **Fabrication** | Rejection |
| ❌ Use external knowledge (Wikipedia, ephemeris) | **External knowledge** | Rejection |
| ❌ Modify `final_output` structure | **Schema violation** | Rejection |
| ❌ Access external APIs during explanation | **External dependency** | Rejection |

---

## 3. Citation Rules

Every factual claim in an AI response **MUST** include a citation.

### Citation Types

| Citation Type | Format | Example |
|---------------|--------|---------|
| **Engine Output** | `{"type": "engine_output", "path": "master_probability.breakdown.natal_promise", "value": "45"}` | Engine output path + value |
| **KG Node** | `{"type": "kg_node", "node_id": "n123", "relationship": "used_in", "label": "TRN-HA-001"}` | KG node ID + relationship |
| **Evidence Chain** | `{"type": "evidence_chain", "chain": ["TRN-HA-001 → Own Sign=80", "PLN-DG-001 → Sun=80"]}` | Chain of KG relationships |
| **Formula Registry** | `{"type": "formula_registry", "formula_id": "TRN-HA-001", "field": "weight", "value": "0.30"}` | Formula registry reference |
| **Calibration Registry** | `{"type": "calibration_registry", "constant_id": "own_sign", "value": "80"}` | Calibration registry reference |
| **Report Template** | `{"type": "report_template", "template": "transit_report", "section": "transit_activation"}` | Report template reference |

### Citation Rules

| Rule | Requirement |
|------|-------------|
| **Mandatory** | Every factual claim MUST have ≥1 citation |
| **Specificity** | Citation must point to exact value, not general section |
| **Verifiability** | Citation path must be resolvable in `final_output` or KG |
| **No Orphan Claims** | No factual statement without citation |
| **Citation Density** | Minimum 1 citation per 2 sentences of factual content |

### Citation Format (AI Response)
```json
{
  "explanation": "Marriage probability is 61/100...",
  "citations": [
    {"type": "engine_output", "path": "master_probability.breakdown.natal_promise", "value": "45"},
    {"type": "kg_node", "node_id": "n123", "relationship": "used_in", "label": "TRN-HA-001"},
    {"type": "evidence_chain", "chain": ["TRN-HA-001 → Own Sign=80", "PLN-DG-001 → Sun=80"]}
  ]
}
```

---

## 4. Confidence Rules

Every AI response **MUST** include a confidence level.

### 4.1 Confidence Levels

| Level | Criteria | Display |
|-------|----------|---------|
| **HIGH** | All claims cite L1-L3 evidence (Canonical Rule, Formula, Calibration) | 🟢 HIGH |
| **MEDIUM** | Claims cite L4-L6 evidence (Engine Output, Canonical Data, Derived Engine) | 🟡 MEDIUM |
| **LOW** | Claims cite L7-L10 evidence (Classical Text, Expert Rule, ADR, Version) | 🔴 LOW |

### Evidence Level Mapping

| Level | Type | Confidence | Description |
|-------|-------|------------|-------------|
| L1 | Canonical Rule | 100% | Immutable governance/classical text |
| L2 | Formula | 90% | Deterministic calculation rule |
| L3 | Calibration | 80% | Immutable constant from registry |
| L4 | Engine Output | 70% | Deterministic engine computation |
| L5 | Canonical Data | 60% | Canonical JSON input |
| L6 | Derived Engine | 50% | Derived engine output |
| L7 | Classical Text | 40% | Classical reference |
| L8 | Expert Rule | 30% | Documented expert heuristic |
| L9 | ADR | 20% | Architecture Decision Record |
| L10 | Version | 10% | Version metadata |

### Confidence Aggregation Rules

| Rule | Formula |
|------|---------|
| **Overall** | Minimum of all claim confidences |
| **Minimum** | If any claim is LOW → overall LOW |
| **No Evidence** | Claim without citation = LOW |
| **Mixed** | Overall = min(all claim confidences) |

---

## 5. Prompt Governance

### 5.1 System Prompt (Immutable)

The system prompt **must** be exactly as specified in GM-012D Section 6.1. No modifications allowed without Architecture Review Board approval.

**Required Elements (Immutable):**
1. Role definition: "You are an expert Vedic astrology explainer. You NEVER calculate."
2. Hard constraints (7 forbidden actions)
5. Response format specification (JSON with citations)
5. No modifications without Architecture Review Board approval

### 5.2 Prompt Versioning

| Version | Date | Changes | Approved By |
|---------|------|---------|-------------|
| v1.0 | 2026-07-29 | Initial release | Architecture Review Board |

### 5.3 Prompt Template Registry

| Template ID | Purpose | Version | Status |
|-------------|---------|---------|--------|
| `explain_probability` | Explain probability score | v1.0 | Active |
| `explain_evidence_chain` | Trace evidence chain | v1.0 | Active |
| `explain_formula` | Explain formula + calibrations | v1.0 | Active |
| `explain_timing` | Explain dasha/transit timing | v1.0 | Active |
| `compare_factors` | Compare transit vs dasha | v1.0 | Active |
| `trace_prediction` | Full prediction trace | v1.0 | Planned |

### 5.4 Prompt Change Control

| Change Type | Required Approval |
|-------------|-------------------|
| New template | Architecture Review Board |
| Template modification | Architecture Review Board |
| System prompt change | Architecture Review Board + CTO |
| Template deprecation | Architecture Review Board |

---

## 6. Grounding Requirements

### 7.1 Grounding Package (Sent to AI)

Every AI request **must** include a grounding package:

```json
{
  "final_output": { ... },                    // Full pipeline output
  "knowledge_graph": {                        // Filtered KG context
    "nodes": [...],                           // Relevant nodes only
    "relationships": [...],                   // Relevant relationships
    "computed_relationships": {...}           // 11 computed types
  },
  "question": "Why is Marriage 61/100?",
  "routed_domain": "marriage",
  "evidence_chain": [...],                    // From KG.build_evidence_chain()
  "cross_references": [...]                   // From KG.get_cross_references()
}
```

### 7.2 Grounding Rules

| Rule | Enforcement |
|-------|-------------|
| **No External Knowledge** | AI prompt explicitly forbids external knowledge |
| **Grounding Package Required** | Request rejected without grounding package |
| **KG Filtering** | Only relevant nodes/relationships included |
| **Deterministic Serialization** | Grounding package serialized deterministically |
| **Version Pinning** | KG version + `final_output` hash included |

### 7.3 Grounding Validation

| Check | Validation |
|-------|------------|
| Grounding package present | Required in request |
| `final_output` hash matches | Must match pipeline run |
| KG version matches | Must match current KG version |
| No extra fields | Only allowed fields present |

---

## 7. Deterministic Replay Requirements

### 8.1 Replay Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Same Input → Same Output** | Identical grounding package → identical AI response |
| **Prompt Caching** | System prompt + grounding package hash → cached response |
| **Cache Key** | `SHA256(system_prompt + grounding_package_json)` |
| **Cache TTL** | 24 hours (configurable) |
| **Cache Invalidation** | On `final_output` change or KG version change |
| **Replay Verification** | Automated test: same input → byte-identical response |

### 8.2 Replay Validation

| Check | Method |
|-------|----------|
| **Determinism Test** | Run same grounding package 10× → identical responses |
| **Cache Hit Rate** | Target >90% for repeated questions |
| **Cache Miss Logging** | Log cache misses for analysis |
| **Cache Invalidation Test** | Modify `final_output` → cache invalidated |

---

## 8. Audit Trail Requirements

### 9.1 Audit Log Format

Every AI interaction **must** produce an audit log entry:

```json
{
  "audit_id": "uuid",
  "timestamp": "2026-07-29T10:30:00Z",
  "user_id": "user_123",
  "question": "Why is Marriage 61/100?",
  "routed_domain": "marriage",
  "grounding_package_hash": "sha256:abc123...",
  "ai_response": { ... },
  "citations": [...],
  "confidence": "HIGH",
  "deterministic_trace": "master_probability.breakdown.natal_promise",
  "processing_time_ms": 1245,
  "cache_hit": true,
  "cache_key": "sha256:abc123...",
  "ai_model": "gpt-4o-v2024-08-06",
  "prompt_version": "v1.0"
}
```

### 9.2 Audit Requirements

| Requirement | Specification |
|-------------|---------------|
| **Immutability** | Append-only; never modified |
| **Retention** | 7 years minimum |
| **Queryable** | By user_id, question, domain, date range |
| **Tamper-Evident** | Hash chain (each entry includes prev_hash) |
| **Exportable** | JSON/CSV export for compliance |
| **PII Protection** | User IDs hashed; questions sanitized |

### 9.3 Audit Log Storage

| Requirement | Specification |
|-------------|---------------|
| **Storage** | Append-only log (PostgreSQL or CloudWatch) |
| **Retention** | 7 years minimum |
| **Encryption** | At-rest AES-256; in-transit TLS 1.3 |
| **Access Control** | Admin only; audit log access logged |
| **Exportable** | JSON/CSV export for compliance |

---

## 9. Versioning Strategy

### 10.1 Versioning Scheme

| Component | Versioning Scheme |
|-----------|-------------------|
| **AI Response Governance** | `MAJOR.MINOR.PATCH` (SemVer) |
| **Prompt Templates** | `v{MAJOR}.{MINOR}` (e.g., `v1.0`, `v1.1`) |
| **System Prompt** | `v{MAJOR}.{MINOR}` (tied to governance version) |
| **AI Model** | Provider version string (e.g., `gpt-4o-v2024-08-06`) |
| **Grounding Package Schema** | `v{MAJOR}.{MINOR}` (JSON Schema version) |

### 10.2 Version Compatibility

| Component | Compatibility Rule |
|-----------|-------------------|
| **Governance v1.x** | Compatible with AI Model v1.x, Grounding Schema v1.x |
| **Governance v2.x** | Breaking changes; requires full revalidation |
| **Prompt Template v1.x** | Compatible with Governance v1.x |
| **Grounding Schema v1.x** | Compatible with Governance v1.x |

### 10.3 Release Process

| Step | Action | Gate |
|------|--------|------|
| 1 | Create release branch | Architecture Review |
| 2 | Run full test suite | 739 tests pass |
| 3 | Deterministic replay test | 10/10 identical responses |
| 4 | Tag release | `git tag governance-v1.x.x` |
| 5 | Deploy to staging | Smoke test |
| 6 | Production deploy | Blue-green deploy |

---

## 10. Compliance Checklist

### 10.1 Pre-Deployment Checklist

| # | Check | Status | Evidence |
|---|-------|--------|----------|
| 1 | No engine modifications | ✅ | Code review |
| 2 | AI never calculates | ✅ | Prompt forbids calculation |
| 3 | Deterministic replay | ✅ | 739 tests passing |
| 4 | No temporary files | ✅ | No temp files created |
| 6 | Citation coverage ≥1/2 sentences | ✅ | Automated citation check |
| 7 | Confidence levels assigned | ✅ | All responses have confidence |
| 8 | No secrets in logs | ✅ | Log sanitization verified |
| 9 | No temporary files | ✅ | No temp files created |
| 10 | Deterministic replay | ✅ | 10/10 identical responses |

### 10.2 Post-Deployment Monitoring

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Cache hit rate | >90% | <80% |
| Deterministic replay pass rate | 100% | <100% |
| Citation coverage | ≥1 per 2 sentences | <50% |
| Avg confidence | HIGH | <MEDIUM |
| Audit log write latency | <100ms | >500ms |
| Error rate | <0.1% | >1% |

---

## 12. Appendices

### Appendix A: Citation Type Registry

| Type ID | Name | Required Fields | Example |
|---------|------|-----------------|---------|
| `engine_output` | Engine Output | path, value | `{"path": "master_probability.breakdown", "value": "45"}` |
| `kg_node` | KG Node | node_id, relationship, label | `{"node_id": "n123", "relationship": "used_in"}` |
| `evidence_chain` | Evidence Chain | chain[] | `{"chain": ["A→B", "B→C"]}` |
| `formula_registry` | Formula Registry | formula_id, field, value | `{"formula_id": "TRN-HA-001", "field": "weight"}` |
| `calibration_registry` | Calibration Registry | constant_id, value | `{"constant_id": "own_sign", "value": "80"}` |
| `report_template` | Report Template | template, section | `{"template": "transit_report", "section": "activation"}` |

### Appendix B: Confidence Level Quick Reference

| Evidence in Citation | Min Confidence |
|---------------------|----------------|
| Canonical Rule (L1) | HIGH |
| Formula (L2) | HIGH |
| Calibration (L3) | HIGH |
| Engine Output (L4) | MEDIUM |
| Canonical Data (L5) | MEDIUM |
| Derived Engine (L6) | MEDIUM |
| Classical Text (L7) | LOW |
| Expert Rule (L8) | LOW |
| ADR (L9) | LOW |
| Version (L10) | LOW |

---

## 14. Approval Record

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Chief Architect | | | |
| Product Owner | | | |
| Engineering Lead | | | |
| QA Lead | | |
| Security Officer | | |

---

## 14. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-30 | Architecture Team | Initial release |

---

## 14. End of Document

*This document governs all AI response behaviour in the Vedic AI system. No AI response may be deployed without compliance to this governance contract.*

---

**END OF DOCUMENT**