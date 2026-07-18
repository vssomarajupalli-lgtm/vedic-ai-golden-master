# GM-008 | AP-001 — CHIEF ARCHITECT REVIEW BRIEF
**Prepared: 2026-07-16 | For Review Decision Only**

---

## 1. MILESTONE HIERARCHY

```
                    ┌─────────────────────────┐
                    │  M1: FOUNDATION (W1-4)  │ ← NON-NEGOTIABLE: Must be first
                    │  API Gateway, Auth,     │
                    │  Audit, Config, Schema  │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
   ┌────────┴────────┐  ┌──────┴──────┐            │
   │ M2: CLIENT MGMT │  │ M3: AI ASST │  PARALLEL  │
   │   (W5-8)        │  │  (W5-12)    │  TRACKS    │
   │                 │  │             │            │
   │ Profiles,       │  │ Q&A, Draft, │            │
   │ History, Birth  │  │ Explain,    │            │
   │ Data, Linking   │  │ Pattern     │            │
   └────────┬────────┘  └──────┬──────┘            │
            │                   │                   │
            └───────────┬───────┘                   │
                        │                           │
                ┌───────┴────────┐                  │
                │ M4: KNOWLEDGE  │  (W9-12)         │
                │ Graph, Library,│                  │
                │ Evidence, KB   │                  │
                └───────┬────────┘                  │
                        │                           │
                        ├──────────────────┐        │
                        │                  │        │
                ┌───────┴────────┐  ┌─────┴──────┐ │
                │ M5: PRACTICE   │  │ M7: SNAP-  │ │
                │   (W13-16)     │  │ SHOT INTEL │ │
                │                │  │  (W17-20)  │ │
                │ Dash, Schedule,│  │ Compare,   │ │
                │ Billing, Multi │  │ Trend,     │ │
                └───────┬────────┘  │ Predict    │ │
                        │           └─────┬──────┘ │
                        │                 │        │
                        └────────┬────────┘        │
                                 │                 │
                        ┌────────┴─────────┐       │
                        │ M6: REPORTING &  │       │
                        │    ANALYTICS     │       │
                        │    (W17-20)      │       │
                        └────────┬─────────┘       │
                                 │                 │
                        ┌────────┴─────────┐       │
                        │ M8: ENTERPRISE & │       │
                        │    INTEGRATION   │       │
                        │    (W21-24)      │       │
                        │ API Docs, Export,│       │
                        │ Backup, Security │       │
                        └──────────────────┘       │
```

**Total: 8 milestones, 24 weeks, 2 parallel tracks (M2/M3, M6/M7)**

---

## 2. COMPLETE BACKLOG HIERARCHY

```
GM-008
├── BKL-008A: AI ASSISTANT (7 items)
│   ├── AI-001: NL Q&A about consultations .............. P0
│   ├── AI-002: Report section drafting ................. P0
│   ├── AI-003: Formula evidence explanation ............ P1
│   ├── AI-004: Pattern detection across history ........ P1
│   ├── AI-005: Domain-specific insight generation ...... P2
│   ├── AI-006: AI interaction audit trail .............. P0
│   └── AI-007: Multi-consultation cross-referencing .... P2
│
├── BKL-008B: KNOWLEDGE GRAPH (6 items)
│   ├── KG-001: Domain-Formula-House-Planet graph ....... P0
│   ├── KG-002: Domain-specific insights library ........ P1
│   ├── KG-003: Formula-to-outcome evidence mapping ..... P1
│   ├── KG-004: Searchable knowledge base ............... P1
│   ├── KG-005: Personalized recommendations ............ P2
│   └── KG-006: Evidence chain visualization ............ P2
│
├── BKL-008C: CLIENT MANAGEMENT (7 items)
│   ├── CL-001: Client Profile CRUD + versioning ........ P0
│   ├── CL-002: Client ↔ Consultation linking ........... P0
│   ├── CL-003: Client history dashboard ................ P0
│   ├── CL-004: Client categorization (tags/groups) ..... P1
│   ├── CL-005: Birth data management + validation ...... P0
│   ├── CL-006: Client search and filtering ............. P0
│   └── CL-007: Relationship mapping (family/couple) .... P2
│
├── BKL-008D: PRACTICE MANAGEMENT (6 items)
│   ├── PM-001: Practice dashboard ...................... P0
│   ├── PM-002: Consultation scheduling ................. P1
│   ├── PM-003: Client communication templates .......... P2
│   ├── PM-004: Billing and invoicing ................... P2
│   ├── PM-005: Document storage ........................ P1
│   └── PM-006: Multi-practitioner support .............. P0
│
├── BKL-008E: REPORTING (4 items)
│   ├── RP-001: Professional report templates ........... P0
│   ├── RP-002: Batch report generation ................. P2
│   ├── RP-003: Report version comparison ............... P2
│   └── RP-004: Client-facing personalization ........... P1
│
├── BKL-008F: ANALYTICS (5 items)
│   ├── AN-001: Practice analytics dashboard ............ P1
│   ├── AN-002: Consultation trend analysis ............. P2
│   ├── AN-003: Domain coverage analysis ................ P2
│   ├── AN-004: Client engagement metrics ............... P2
│   └── AN-005: Formula usage statistics ................ P2
│
├── BKL-008G: SNAPSHOT INTELLIGENCE (5 items)
│   ├── SI-001: Automated multi-snapshot comparison ..... P0
│   ├── SI-002: Trend detection (transit impact) ........ P1
│   ├── SI-003: Predictive pattern recognition .......... P2
│   ├── SI-004: Timeline-based dasha/transit correlation  P1
│   └── SI-005: Domain-specific impact assessment ....... P2
│
└── BKL-008H: ENTERPRISE (6 items)
    ├── EN-001: API documentation (OpenAPI) .............. P0
    ├── EN-002: Data export/import ....................... P0
    ├── EN-003: Backup and restore ....................... P0
    ├── EN-004: Performance optimization ................. P1
    ├── EN-005: Deployment guide ......................... P1
    └── EN-006: Security hardening ....................... P0

TOTAL: 46 backlog items across 8 groups
P0 (Critical): 19 items | P1 (High): 13 items | P2 (Medium): 14 items
```

---

## 3. DEPENDENCY GRAPH

```
                    ┌──────────┐
                    │  GM-007  │ ← FROZEN: Consumed read-only by all GM-008
                    │ (Core)   │
                    └────┬─────┘
                         │
                    ┌────┴─────┐
                    │  M1:     │
                    │  FOUND.  │
                    └─┬──┬──┬──┘
                      │  │  │
         ┌────────────┘  │  └────────────┐
         │               │               │
    ┌────┴────┐    ┌─────┴─────┐         │
    │ M2:     │    │ M3: AI    │         │
    │ CLIENTS │    │ ASSISTANT │         │
    └─┬──┬─┬──┘    └─────┬─────┘         │
      │  │ │             │               │
      │  │ └─────────────┼───────┐       │
      │  └───────┐       │       │       │
      │          │  ┌────┴────┐  │       │
      │          │  │ M4:     │  │       │
      │          │  │ KNOWL.  │  │       │
      │          │  └────┬────┘  │       │
      │          │       │       │       │
 ┌────┴────┐     │  ┌────┴────┐  │       │
 │ M5:     │     │  │ M7:     │  │       │
 │ PRACTICE│     │  │ SNAP.   │  │       │
 └────┬────┘     │  │ INTEL   │  │       │
      │          │  └────┬────┘  │       │
      └────┬─────┘       │       │       │
           │             │       │       │
      ┌────┴─────────────┴───────┘       │
      │ M6: REPORTING & ANALYTICS        │
      └────────────┬─────────────────────┘
                   │
              ┌────┴─────┐
              │ M8:      │
              │ ENTERPR. │
              └──────────┘
```

**Critical Path**: M1 → M2 → M4 → M6 → M8 (foundation → clients → knowledge → reporting → enterprise)

**Parallelizable**: M2/M3 (clients and AI are independent), M6/M7 (reporting and snapshot intelligence are independent)

---

## 4. CRITICAL ARCHITECTURAL ASSUMPTIONS

These assumptions underpin the entire roadmap. If any are invalid, the roadmap must be revised.

| # | Assumption | Impact if Wrong | Verification |
|---|-----------|-----------------|--------------|
| A1 | **GM-007 engines are permanently frozen** — no changes to formulas, calibration, or question catalog ever needed | All GM-008 work assumes a stable API contract; engine changes would force redesign of AI assistant, knowledge graph, and reporting | Confirmed by Chief Architect: GM-007 freeze is permanent |
| A2 | **AI assistant reads deterministic outputs read-only** — never modifies, never recalculates, never reinterprets | Hallucination risk; the entire AI trust model depends on this | Must be enforced by architecture: AI has no write access to engine outputs |
| A3 | **Client identity is linked to birth data hash** — not name, not arbitrary ID | Name changes, typos, or duplicate clients would break the client↔consultation link | Birth data hash is deterministic and unique; client profiles can be merged |
| A4 | **Multi-practitioner data isolation is at repository level** — not application level | Accidental data leakage between practices would be a critical privacy violation | Requires per-practice data partitioning in the repository design |
| A5 | **All AI outputs are clearly marked "assistance only"** — astrologer retains full authority | Regulatory and professional liability if AI is perceived as authoritative | Must be enforced in UI: AI sections are visually distinct from deterministic outputs |
| A6 | **Knowledge graph is derived from deterministic data** — not from AI training or external sources | Knowledge graph contamination would compromise the Golden Master's evidence-based foundation | Every graph edge must be traceable to a formula or engine output |
| A7 | **The repository is the single source of truth** — no external databases for client or practice data | Data fragmentation would create inconsistency and make export/backup impossible | All data must flow through the repository; no side channels |
| A8 | **24-week timeline with parallel tracks assumes 2 independent teams** | Single-team execution would double the timeline to ~48 weeks | Milestones M2/M3 and M6/M7 are designed for parallel execution |

---

## 5. RISKS

### Critical Risks (Probability × Impact ≥ 8)

| Risk | P | I | Score | Mitigation |
|------|---|---|-------|------------|
| AI hallucination misrepresenting deterministic data | 4 | 5 | 20 | Read-only AI interface; all AI outputs validated against source; AI sections visually distinct |
| Client data isolation breach (multi-practitioner) | 2 | 5 | 10 | Repository-level data partitioning; role-based access; audit logging of all access |
| Repository schema change breaking GM-007 consultations | 2 | 5 | 10 | Versioned migrations; full backward compat; GM-007 schema unchanged |
| Birth data hash collision causing client merge errors | 1 | 5 | 5 | Extremely unlikely with SHA-256; additional validation on birth data fields |

### High Risks (Probability × Impact ≥ 6)

| Risk | P | I | Score | Mitigation |
|------|---|---|-------|------------|
| Scope creep into GM-009 territory (engine changes, ML) | 4 | 3 | 12 | Strict milestone gates; public OUT OF SCOPE list; freeze at each milestone |
| Performance degradation with large client bases | 3 | 3 | 9 | Horizontal scaling design from M1; pagination-first; benchmarks in M8 |
| AI assistant adoption resistance (astrologers distrust AI) | 3 | 3 | 9 | AI outputs clearly marked as assistance; astrologer always has final authority; transparent evidence chains |
| Team scaling bottleneck (can't parallelize M2/M3) | 3 | 3 | 9 | Clear interface contracts; independent codebases for M2 and M3 |

### Medium Risks (Probability × Impact ≥ 4)

| Risk | P | I | Score | Mitigation |
|------|---|---|-------|------------|
| Knowledge graph becomes stale without update mechanism | 3 | 2 | 6 | Versioned graph; update triggers on formula/calibration changes |
| Timelines slip due to underestimated complexity | 3 | 2 | 6 | Milestone gates with buffer; early risk identification; phased delivery |
| Reporting template complexity exceeds estimate | 2 | 2 | 4 | Start with minimal templates; iterate based on usage; leverage existing PrintFramework |

---

## 6. DESIGN DECISIONS MADE WITHOUT REQUIREMENTS

The following decisions were made during roadmap creation based on architectural judgment, not explicit requirements. Each requires Chief Architect confirmation.

| # | Decision | Rationale | Discussion Required |
|---|----------|-----------|---------------------|
| D1 | **Client identity = birth data hash** | Birth data is the only immutable, deterministic identifier across consultations. Names change, IDs are arbitrary, but birth data is unique to the astrological chart. | Should clients be allowed to have multiple birth data sets (e.g., rectified vs. reported)? |
| D2 | **AI reads engine outputs, never recalculates** | This is the only way to guarantee AI doesn't hallucinate astrological values. If AI needs to understand a formula, it reads the formula's evidence, not the formula's implementation. | Should AI have access to intermediate engine outputs (e.g., individual subsystem scores) or only final outputs? |
| D3 | **Repository-level multi-tenancy** | Each practice's data is isolated at the repository layer, not the application layer. This is the strongest isolation guarantee. | Is this acceptable for a single-practitioner deployment where simplicity is preferred? |
| D4 | **Knowledge graph is derived, not curated** | The graph is built automatically from formula relationships and consultation patterns, not manually curated by domain experts. | Should there be a manual curation layer for astrological accuracy? |
| D5 | **M2 (Clients) and M3 (AI) are parallel, independent tracks** | They share no dependencies — clients don't need AI, AI can work on sample data. Parallel execution halves the timeline. | Is the team size sufficient for two parallel tracks? |
| D6 | **Reporting is last before Enterprise** | Reports consume data from every other system. Building them early means constant rewrites as other systems evolve. | Should a minimal reporting milestone be inserted earlier for early adopter feedback? |
| D7 | **No new backend calculations** | All GM-008 features are presentation layer. The backend serves as a data API and gateway, never as a calculation engine. | Should the knowledge graph or analytics engine have any server-side computation? |
| D8 | **24-week timeline assumes no engine changes** | If any GM-007 engine requires modification during GM-008, the timeline is invalid. | Confirm: is the GM-007 freeze truly permanent for the duration of GM-008? |

---

## 7. SECTIONS REQUIRING FURTHER DISCUSSION

| Section | Issue | Recommendation |
|---------|-------|----------------|
| **M3: AI Assistant scope** | The boundary between "AI assistance" and "AI authority" is not defined. What happens when AI and astrologer disagree? | Define an AI Governance Policy before M3 begins: AI is advisory only; astrologer always has final authority; all AI outputs are discardable. |
| **M4: Knowledge Graph** | Derived vs. curated knowledge. A purely derived graph may miss astrological nuance; a curated graph requires domain expert time. | Propose a hybrid: graph is derived automatically, then reviewed/curated by domain experts in a separate pass. |
| **M5: Practice Management** | Billing and invoicing are listed as P2 but may be critical for professional adoption. | Survey target users: is billing a "nice to have" or a "must have" for initial adoption? |
| **M8: Enterprise** | "Enterprise" is a broad term. Does it mean multi-tenant SaaS, self-hosted deployment, or both? | Define the deployment model: SaaS-first or self-hosted-first? This affects the entire architecture. |
| **API Gateway** | The roadmap assumes a REST API gateway. WebSocket or GraphQL may be needed for real-time features. | Confirm: REST-only for GM-008, or plan for real-time in GM-009? |
| **Client Data Privacy** | Birth data is personal and culturally sensitive. GDPR/India DPDP Act compliance is not addressed. | Add a privacy and compliance milestone or integrate privacy requirements into M1 Foundation. |
| **AI Model Selection** | The roadmap assumes AI assistance is feasible. No specific model or provider is named. | Define AI provider strategy before M3: local LLM, cloud API, or hybrid? This affects cost, latency, and data privacy. |
| **GM-007 Backlog** | 4 pre-existing TypeScript errors in BKL-007A files (`QuestionSelectionPanel`, `ReportStructurePanel`) are not addressed. | Decide: fix in GM-008 Foundation milestone, or defer to a dedicated GM-007 cleanup sprint? |

---

## REVIEW DECISION REQUIRED

The Chief Architect is asked to:

1. **Confirm** the 8 critical architectural assumptions (A1-A8)
2. **Resolve** the 8 design decisions made without requirements (D1-D8)
3. **Address** the 8 sections requiring further discussion
4. **Approve** the milestone hierarchy and dependency graph
5. **Authorize** M1: Foundation to begin upon approval

---

*Prepared for Chief Architect Review — No roadmap modifications made*  
*AP-001 Review Brief | 2026-07-16*