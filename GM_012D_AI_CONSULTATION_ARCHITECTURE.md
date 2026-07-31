# GM-012D AI Consultation Architecture
## AI Explanation Layer Over Deterministic Engine

**Status**: Architecture Review - Awaiting Approval  
**Version**: 1.0  
**Date**: 2026-07-29  
**Depends On**: GM-012C (Knowledge Graph Explorer) ✅ Complete

---

## 1. Executive Summary

### Purpose
Build an AI explanation layer that sits **on top** of the frozen deterministic engine (GM-007 freeze). The AI **never calculates** astrology — it only explains, traces, and contextualizes the deterministic outputs already produced by the frozen engines.

### Core Principle
> **The AI explains. The deterministic engine calculates. Never the reverse.**

---

## 2. Current Repository State (Baseline)

### Deterministic Engine Stack (GM-007 Frozen)
```
PipelineRunner → JsonNormalizer → 11 Engines → MasterProbabilityEngine → QuestionEngine
     ↓                    ↓
  11 Engines          Final Output
  - PlanetStrength     - metadata
  - HouseStrength       - master_probability
  - Varga               - engine_outputs (11 engines)
  - Dasha               - target_date_utc
  - Rasi
  - Ashtakavarga
  - NatalPromise
  - Transit
  - UniversalMandali
  - Yoga
  - FunctionalNature
  - QualityMetrics
```

### Pipeline Output (Canonical `final_output`)
```json
{
  "metadata": {...},
  "master_probability": {
    "final_score": 61,
    "grade": "MODERATE",
    "breakdown": {"natal_promise": 45, "transit": 78, "dasha": 65, ...},
    "weights": {"natal": 0.4, "transit": 0.05, "dasha": 0.1, ...}
  },
  "engine_outputs": {
    "functional_nature": {...},
    "planets": {...},
    "houses": {...},
    "vargas": {...},
    "dashas": {...},
    "rasis": {...},
    "ashtakavarga": {...},
    "doshas": {...},
    "natal_promise": {...},
    "transit": {...},
    "yogas": {...}
  },
  "target_date_utc": "2026-07-29T10:30:00+00:00"
}
```

### Knowledge Graph (GM-012C Complete)
- **79 nodes**, **206 relationships**, 12 node types, 13 relationship types
- 5 computed relationship types: `uses`, `produces`, `affects`, `weakens`, `triggered_by`, `used_in`, `appears_in_report`, `asked_by_question`, `used_by_engine`, `derived_from`, `calibrated_by`
- 5 new view modes: **Computed**, **Formulas**, **Engines**, **Questions**, **Reports**

---

## 3. AI Explanation Layer Architecture

### 3.1 Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Zero Calculation** | AI never computes; only references `final_output` |
| **Deterministic Traceability** | Every AI claim → KG node → engine output → formula → calibration |
| **Zero Hallucination** | Structured prompts with `final_output` as grounding context |
| **Audit Trail** | Every AI response includes KG node IDs and engine output paths |
| **Deterministic Replay** | Same inputs → identical AI explanation (cached prompts) |

### 3.2 AI Capabilities (What It CAN Do)
| Capability | Description | Source |
|------------|-------------|--------|
| **Explain Formula** | "TRN-HA-001 uses 5 calibrations: Own Sign=80, Friendly=60..." | Formula Registry → Calibration Registry |
| **Trace Prediction** | "61/100 comes from: Natal 45 (40%) + Transit 78 (5%) + Dasha 65 (10%)..." | `master_probability.breakdown` + weights |
| **Explain Evidence Chain** | "Transit score 78 comes from Jupiter in H9 (HA) + Saturn MD..." | KG evidence chain + engine outputs |
| **Answer Timing Questions** | "Best window: Jan 2027 - Mar 2027 (Jupiter in H9, Saturn MD/Jup AD)" | `lifetime_projection` + `mandali_activation` |
| **Trace Formula** | "TRN-HA-001 weight 30% uses 5 calibrations: Own=80, Friendly=60..." | Formula Registry → Calibration Registry |
| **Contradiction Check** | "Transit says favorable but Dasha says wait — here's why..." | Compare engine outputs |
| **Citation Generation** | "[L2 Formula: TRN-HA-001 v1.0, L3 Calibration: Own Sign=80 v1.0]" | Evidence chain levels |

### 3.3 AI Forbidden Actions (Hard Constraints)
| Forbidden | Rationale |
|-----------|-----------|
| ❌ Calculate any score | Frozen engine owns all math |
| ❌ Suggest new formulas | Governance owns formula registry |
| ❌ Override engine output | Determinism guarantee |
| ❌ Predict future not in `lifetime_projection` | Only deterministic projection allowed |
| ❌ Modify `final_output` | Immutable after pipeline run |
| ❌ Access external APIs during explanation | Air-gapped; only `final_output` + KG context |

---

## 4. Data Flow Architecture

### 4.1 Explanation Request Flow
```
User Question
    ↓
AI Layer: "Explain why Marriage is 61/100"
    ↓
Load final_output + KG context (computed relationships)
    ↓
Structured Prompt Template (see Section 6)
    ↓
AI Response (grounded in final_output + KG)
    ↓
Return: {explanation, citations, evidence_chain, confidence}
```

### 4.2 Grounding Context Package (Sent to AI)
```json
{
  "final_output": { ... },           // Full pipeline output
  "knowledge_graph": {
    "nodes": [...],                  // Filtered to relevant domain
    "relationships": [...],          // Computed + persisted relationships
    "computed_relationships": {...}  // 11 computed types
  },
  "question": "Why is Marriage 61/100?",
  "routed_domain": "marriage",
  "evidence_chain": [...],           // From KG.build_evidence_chain()
  "cross_references": [...]          // From KG.get_cross_references()
}
```

---

## 5. Deterministic Outputs Available for AI Explanation

### 5.1 Engine Outputs (Read-Only)
| Engine | Output Keys | Explanation Value |
|--------|-------------|-------------------|
| **PlanetStrength** | `planets.{planet}.{final_score, dignity, house_type, ...}` | "Sun dignity: Exalted (80/100)" |
| **HouseStrength** | `houses.{1-12}.{final_score, lord_strength, occupants}` | "House 7 (Marriage): 72/100, Lord Venus in H12" |
| **NatalPromise** | `natal_promise.{domain}.{score, promise, factors}` | "Marriage promise: 45/100 (PRESENT)" |
| **TransitEngine** | `transit.activation_score`, `activated_domains` | "Transit 78/100: Jupiter in H9 activates Marriage" |
| **DashaEngine** | `dashas.synthesis.dasha_strength`, `timeline[]` | "Saturn MD / Jupiter AD: 65/100" |
| **Ashtakavarga** | `ashtakavarga.bav.{house}`, `sav.{house}` | "House 7 BAV: 28 (FAVORABLE)" |
| **YogaEngine** | `yogas.active_yogas[]`, `yogas.marriage_yogas` | "Gaja Kesari Yoga active (Jupiter in Kendra from Moon)" |
| **MandaliEngine** | `mandali_advisory.current_mandali`, `mandali_activations[]` | "Current Mandali 9: Jupiter in Mandali 1" |
| **MasterProbability** | `final_score`, `grade`, `breakdown`, `weights` | "61/100 = 40%×45 + 5%×78 + 10%×65 + ..." |
| **QuestionEngine** | `answer_text`, `probability`, `timing`, `formula_evaluation` | Final user-facing answer |

### 5.2 Knowledge Graph Traces
| KG Feature | AI Usage |
|------------|----------|
| `evidence_chain` | "TRN-HA-001 → Own Sign=80 → Transit 78" |
| `cross_references` | "Marriage domain ← House 7 ← Venus → Transit Jupiter" |
| `computed_relationships` | `used_in`, `produced_by`, `derived_from` |
| `evidence_chain` | 17-step chain from Formula → Calibration → Registry |

---

## 6. Prompt Engineering Framework

### 6.1 System Prompt (Fixed)
```markdown
# SYSTEM PROMPT: Vedic AI Explanation Layer

## ROLE
You are an expert Vedic astrology explainer. You NEVER calculate. You ONLY explain deterministic outputs.

## HARD CONSTRAINTS
1. NEVER calculate, predict, or compute any astrological value
2. ONLY reference values from provided `final_output` and Knowledge Graph
3. Every claim MUST cite: engine output path OR KG node ID + relationship
4. If uncertain → "The deterministic output does not specify this"
5. NEVER speculate beyond provided deterministic outputs

## RESPONSE FORMAT
{
  "explanation": "Human-readable explanation",
  "citations": [
    {"type": "engine_output", "path": "master_probability.breakdown", "value": "..."},
    {"type": "kg_node", "node_id": "...", "relationship": "used_in", "label": "..."},
    {"type": "evidence_chain", "chain": [...]}
  ],
  "confidence": "HIGH|MEDIUM|LOW",
  "deterministic_trace": "path.to.value.in.final_output"
}
```

### 6.2 Domain-Specific Prompt Templates

#### Template: Explain Probability Score
```markdown
User: "Why is Marriage 61/100?"

AI Response Structure:
{
  "explanation": "Marriage probability 61/100 (MODERATE) comes from weighted synthesis...",
  "citations": [
    {"type": "engine_output", "path": "master_probability.breakdown", "value": "natal=45, transit=78, dasha=65"},
    {"type": "engine_output", "path": "master_probability.weights", "value": "natal=0.40, transit=0.05..."},
    {"type": "kg_node", "node_id": "n123", "relationship": "used_in", "label": "TRN-HA-001"},
    {"type": "evidence_chain", "chain": ["TRN-HA-001 → Own Sign=80", "PLN-DG-001 → Sun dignity=80"]}
  ],
  "confidence": "HIGH",
  "deterministic_trace": "master_probability.breakdown.natal_promise"
}
```

### 6.3 Evidence Chain Template
```markdown
Evidence Chain for Transit Activation 78:
  Step 1: TRN-HA-001 (House Activation, 30%) → depends_on Calibration: Own Sign=80
  Step 2: Calibration: Own Sign=80 → Calibration Registry v1.0
  Step 3: PLN-DG-001 (Dignity Score) → Sun in Leo = Own Sign → 80/100
  Step 4: TransitEngine → House 9 (Jupiter) → Activation 78/100
```

---

## 7. Implementation Phases (Post-Approval)

### Phase 1: AI Explanation Service (Week 1-2)
- [ ] `AIExplanationService` class in `backend/app/services/`
- [ ] Prompt template registry (YAML)
- [ ] `POST /api/v1/ai/explain` endpoint
- [ ] Grounding context builder: `build_explanation_context(final_output, kg)`
- [ ] Citation formatter: `format_citations(citations)`

### Phase 2: Frontend Integration (Week 2)
- [ ] "Ask AI" button in `KnowledgeGraphViewer` and `Results` page
- [ ] Streaming response UI with citation chips
- [ ] Evidence chain visualization (vertical timeline)
- [ ] Citation chips linking to KG nodes

### Phase 3: Advanced Features (Week 3-4)
- [ ] Comparison mode: "Compare Transit vs Dasha"
- [ ] Contradiction detector: "Transit favorable but Dasha says wait"
- [ ] Formula deep-dive modal: "Show me TRN-HA-001 calibration trace"
- [ ] Export explanation as PDF/Markdown

---

## 8. Deterministic Data Catalog (AI Can Reference)

### Engine Output Paths (Read-Only)
```
engine_outputs.functional_nature
engine_outputs.planets.{planet}.{final_score, dignity, house_type, house, retrograde}
engine_outputs.houses.{1-12}.{final_score, lord_strength, occupants}
engine_outputs.natal_promise.{domain}.{score, promise, karaka, afflictions}
engine_outputs.transit.{activation_score, activated_domains, breakdown}
engine_outputs.dashas.synthesis.dasha_strength
engine_outputs.dashas.timeline[]
engine_outputs.ashtakavarga.bav.{house}, sav.{house}
engine_outputs.yogas.active_yogas[]
engine_outputs.mandali_advisory.current_mandali
engine_outputs.mandali_advisory.mandali_activations[]
engine_outputs.yogas.active_yogas[]
engine_outputs.yogas.marriage_yogas
```

### Knowledge Graph Query Patterns
```python
# Get evidence chain for node
kg.build_evidence_chain(node_id) → List[EvidenceStep]

# Get cross-references
kg.get_cross_references(node_id) → List[CrossReference]

# Get computed relationships (runtime)
kg.get_all_computed_relationships(node_id) → Dict[str, List[ComputedRelationship]]

# Get node with computed relationships
kg.get_node(node_id, enrich=True) → KnowledgeNode + computed_relationships
```

---

## 8. Compliance Checklist (Pre-Approval)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No engine modifications | ✅ | Only new service + UI |
| AI never calculates | ✅ | Prompt forbids calculation |
| Deterministic replay | ✅ | Cached prompts + frozen outputs |
| Audit trail | ✅ | Citations include KG node IDs |
| No external API calls | ✅ | Air-gapped; only `final_output` + KG |
| Deterministic replay | ✅ | Same input → identical AI output |
| Zero engine modifications | ✅ | Read-only engine outputs |

---

## 9. Approval Request

**Requesting Approval For:**
1. Architecture approach (AI explains, deterministic engine calculates)
2. Prompt engineering framework (Section 6)
2. Implementation phases (Section 7)
4. Data catalog (Section 8)

**Deliverable:** `GM_012D_AI_CONSULTATION_ARCHITECTURE.md` (this document)

**Decision Required:** Approve / Request Changes / Reject

---

*End of GM-012D Architecture Document*