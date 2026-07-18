# GM-008 PLATFORM ARCHITECTURE BLUEPRINT
**Samartha Vedic AI — Golden Master Program**
**Version 1.0.0 — Architect Package AP-004**

---

## EXECUTIVE SUMMARY

This blueprint defines the complete GM-008 platform architecture — the system that extends the frozen GM-007 deterministic core into a full professional astrological practice platform. It is a **platform architecture**, not a feature list. Every component, service, data flow, and integration point is described from the perspective of system design, not feature implementation.

GM-008 adds four new architectural layers on top of GM-007: Knowledge, Intelligence, Practice, and Enterprise. Each layer is additive — it consumes GM-007 read-only and never modifies the deterministic foundation.

---

## 1. OVERALL PLATFORM ARCHITECTURE

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        GM-008 PLATFORM ARCHITECTURE                          ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    ENTERPRISE LAYER (GM-008)                            │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │API       │ │Auth &    │ │Audit     │ │Backup &  │ │Deployment    │ │║
║  │  │Gateway   │ │RBAC      │ │Logging   │ │Restore   │ │Config        │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                    │                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    PRACTICE LAYER (GM-008)                              │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │Practice  │ │Client    │ │Scheduling│ │Billing   │ │Document      │ │║
║  │  │Dashboard │ │Mgmt      │ │          │ │          │ │Storage       │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                    │                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    INTELLIGENCE LAYER (GM-008)                          │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │AI        │ │Knowledge │ │Snapshot  │ │Reporting │ │Analytics     │ │║
║  │  │Assistant │ │Graph     │ │Intel     │ │Engine    │ │Engine        │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                    │                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    KNOWLEDGE LAYER (GM-008)                             │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │Knowledge │ │Domain    │ │Formula   │ │Evidence  │ │Recommendation│ │║
║  │  │Graph DB  │ │Library   │ │Index     │ │Chains    │ │Engine        │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                    │                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    APPLICATION LAYER (GM-007) — FROZEN                  │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │Consult.  │ │Timeline  │ │Gochara   │ │Comparison│ │Print         │ │║
║  │  │Workspace │ │          │ │          │ │Workspace │ │Framework     │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │Repository│ │Search    │ │Grid/List │ │Details   │ │Create/Edit   │ │║
║  │  │(BKL-007B)│ │Filter    │ │          │ │Drawer    │ │Modals        │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                    │                                         ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    DETERMINISTIC CORE (GM-001–007) — PERMANENTLY FROZEN │║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │║
║  │  │Engines   │ │Formula   │ │Calibration│ │Question  │ │Pipeline      │ │║
║  │  │(5 engines)│ │Registry  │ │Manager   │ │Catalog   │ │Runner        │ │║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Layer Summary

| Layer | GM | Status | Purpose |
|-------|-----|--------|---------|
| **Enterprise** | GM-008 | New | API gateway, auth, audit, backup, deployment |
| **Practice** | GM-008 | New | Client management, scheduling, billing, documents |
| **Intelligence** | GM-008 | New | AI assistant, knowledge graph, snapshot intelligence, reporting, analytics |
| **Knowledge** | GM-008 | New | Knowledge graph DB, domain library, formula index, evidence chains |
| **Application** | GM-007 | FROZEN | Consultation workspace, repository, timeline, gochara, comparison, print |
| **Deterministic Core** | GM-001–007 | PERMANENTLY FROZEN | Engines, formulas, calibration, question catalog, pipeline |

---

## 2. LAYERED ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         ENTERPRISE LAYER                             │   │
│  │                                                                      │   │
│  │   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐    │   │
│  │   │ REST API │   │ Auth     │   │ Audit    │   │ Deployment   │    │   │
│  │   │ Gateway  │   │ Service  │   │ Service  │   │ Manager      │    │   │
│  │   │ (v1/v2)  │   │ (JWT)    │   │ (Immutable)│  │ (Config)     │    │   │
│  │   └────┬─────┘   └────┬─────┘   └────┬─────┘   └──────┬───────┘    │   │
│  │        │              │              │                │            │   │
│  └────────┼──────────────┼──────────────┼────────────────┼────────────┘   │
│           │              │              │                │                │
│  ┌────────┼──────────────┼──────────────┼────────────────┼────────────┐   │
│  │        │         PRACTICE LAYER      │                │            │   │
│  │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌─────┴───────┐   │   │
│  │   │ Practice │   │ Client   │   │Schedule  │   │ Document    │   │   │
│  │   │ Service  │   │ Service  │   │ Service  │   │ Service     │   │   │
│  │   └────┬─────┘   └────┬─────┘   └────┬─────┘   └─────┬───────┘   │   │
│  │        │              │              │                │           │   │
│  └────────┼──────────────┼──────────────┼────────────────┼───────────┘   │
│           │              │              │                │               │
│  ┌────────┼──────────────┼──────────────┼────────────────┼────────────┐   │
│  │        │       INTELLIGENCE LAYER    │                │            │   │
│  │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌─────┴───────┐   │   │
│  │   │ AI       │   │ Knowledge│   │ Snapshot │   │ Analytics   │   │   │
│  │   │ Engine   │   │ Engine   │   │ Engine   │   │ Engine      │   │   │
│  │   └────┬─────┘   └────┬─────┘   └────┬─────┘   └─────┬───────┘   │   │
│  │        │              │              │                │           │   │
│  └────────┼──────────────┼──────────────┼────────────────┼───────────┘   │
│           │              │              │                │               │
│  ┌────────┼──────────────┼──────────────┼────────────────┼────────────┐   │
│  │        │        KNOWLEDGE LAYER      │                │            │   │
│  │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌─────┴───────┐   │   │
│  │   │ Graph    │   │ Domain   │   │ Formula  │   │ Evidence   │   │   │
│  │   │ Database │   │ Library  │   │ Index    │   │ Chains     │   │   │
│  │   └────┬─────┘   └────┬─────┘   └────┬─────┘   └─────┬───────┘   │   │
│  │        │              │              │                │           │   │
│  └────────┼──────────────┼──────────────┼────────────────┼───────────┘   │
│           │              │              │                │               │
│  ╔════════╧══════════════╧══════════════╧════════════════╧═══════════════╗ │
│  ║                    READ-ONLY BRIDGE (IMMUTABLE)                      ║ │
│  ╚════════╤══════════════╤══════════════╤════════════════╤═══════════════╝ │
│           │              │              │                │               │
│  ┌────────┼──────────────┼──────────────┼────────────────┼────────────┐   │
│  │        │       APPLICATION LAYER (GM-007 FROZEN)       │            │   │
│  │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌─────┴───────┐   │   │
│  │   │ Repo-    │   │ Timeline │   │ Print    │   │ Comparison │   │   │
│  │   │ sitory   │   │ Gochara  │   │ Framework│   │ Workspace  │   │   │
│  │   └────┬─────┘   └────┬─────┘   └────┬─────┘   └─────┬───────┘   │   │
│  │        │              │              │                │           │   │
│  └────────┼──────────────┼──────────────┼────────────────┼───────────┘   │
│           │              │              │                │               │
│  ┌────────┼──────────────┼──────────────┼────────────────┼────────────┐   │
│  │        │     DETERMINISTIC CORE (PERMANENTLY FROZEN)   │            │   │
│  │   ┌────┴─────┐   ┌────┴─────┐   ┌────┴─────┐   ┌─────┴───────┐   │   │
│  │   │ Planet   │   │ Transit  │   │ Formula  │   │Calibration │   │   │
│  │   │ Engine   │   │ Engine   │   │ Registry │   │ Manager    │   │   │
│  │   └──────────┘   └──────────┘   └──────────┘   └────────────┘   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. MODULE DEPENDENCY MAP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODULE DEPENDENCY MAP                               │
│                                                                             │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐               │
│  │ Auth    │────▶│ API     │◀────│ Rate    │     │ Audit   │               │
│  │ Service │     │ Gateway │     │ Limiter │     │ Service │               │
│  └────┬────┘     └────┬────┘     └─────────┘     └────▲────┘               │
│       │               │                               │                     │
│       │     ┌─────────┼───────────────────────────────┘                     │
│       │     │         │                                                     │
│       ▼     ▼         ▼                                                     │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    PRACTICE LAYER                             │          │
│  │                                                                │          │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │          │
│  │  │Practice  │───▶│ Client   │───▶│ Document │                 │          │
│  │  │Dashboard │    │ Service  │    │ Service  │                 │          │
│  │  └────┬─────┘    └────┬─────┘    └──────────┘                 │          │
│  │       │               │                                       │          │
│  └───────┼───────────────┼───────────────────────────────────────┘          │
│          │               │                                                  │
│          ▼               ▼                                                  │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    INTELLIGENCE LAYER                          │          │
│  │                                                                │          │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │          │
│  │  │ AI       │───▶│ Knowledge│───▶│ Snapshot │                 │          │
│  │  │ Engine   │    │ Engine   │    │ Engine   │                 │          │
│  │  └────┬─────┘    └────┬─────┘    └────┬─────┘                 │          │
│  │       │               │               │                        │          │
│  │  ┌────┴───────────────┴───────────────┴─────┐                  │          │
│  │  │              Analytics Engine             │                  │          │
│  │  └────────────────────┬─────────────────────┘                  │          │
│  └───────────────────────┼────────────────────────────────────────┘          │
│                          │                                                   │
│                          ▼                                                   │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │                    KNOWLEDGE LAYER                             │          │
│  │                                                                │          │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │          │
│  │  │ Graph    │───▶│ Domain   │───▶│ Evidence │                 │          │
│  │  │ Database │    │ Library  │    │ Chains   │                 │          │
│  │  └────┬─────┘    └──────────┘    └──────────┘                 │          │
│  │       │                                                        │          │
│  │  ┌────┴──────────────┐                                         │          │
│  │  │ Formula Index     │                                         │          │
│  │  └───────────────────┘                                         │          │
│  └────────────────────────────────────────────────────────────────┘          │
│                          │                                                   │
│          ╔═══════════════╧═══════════════╗                                   │
│          ║    READ-ONLY BRIDGE           ║                                   │
│          ╚═══════════════╤═══════════════╝                                   │
│                          │                                                   │
│  ┌───────────────────────┴──────────────────────────────────────┐          │
│  │                    GM-007 APPLICATION (FROZEN)                │          │
│  │                                                                │          │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │          │
│  │  │Repository│───▶│ Workspace│───▶│ Print    │                 │          │
│  │  │          │    │          │    │ Framework│                 │          │
│  │  └──────────┘    └──────────┘    └──────────┘                 │          │
│  └────────────────────────────────────────────────────────────────┘          │
│                          │                                                   │
│          ╔═══════════════╧═══════════════╗                                   │
│          ║    PERMANENT FREEZE           ║                                   │
│          ╚═══════════════╤═══════════════╝                                   │
│                          │                                                   │
│  ┌───────────────────────┴──────────────────────────────────────┐          │
│  │               DETERMINISTIC CORE                              │          │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │          │
│  │  │ Engines  │ │ Formulas │ │Calibrat. │ │ Question │        │          │
│  │  │ (5)      │ │ Registry │ │ Manager  │ │ Catalog  │        │          │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │          │
│  └────────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. DATA FLOW ARCHITECTURE

### Primary Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW ARCHITECTURE                            │
│                                                                             │
│  ┌──────────────────┐                                                       │
│  │  Birth Data      │                                                       │
│  │  (User Input)    │                                                       │
│  └────────┬─────────┘                                                       │
│           │                                                                 │
│           ▼                                                                 │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐    │
│  │  Canonical       │────▶│  Engine          │────▶│  Engine          │    │
│  │  Content         │     │  Pipeline        │     │  Outputs         │    │
│  │  (JSON)          │     │  (PipelineRunner) │     │  (Deterministic) │    │
│  └──────────────────┘     └──────────────────┘     └────────┬─────────┘    │
│                                                             │              │
│                                           ┌─────────────────┘              │
│                                           │                                │
│                                           ▼                                │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        STORE CONTRACTS                                │  │
│  │                                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │  │
│  │  │ ChartStore   │  │ Repository   │  │ PrintStore   │                 │  │
│  │  │ (Zustand)    │  │ (Zustand)    │  │ (Zustand)    │                 │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │  │
│  └─────────┼─────────────────┼─────────────────┼─────────────────────────┘  │
│            │                 │                 │                            │
│            ▼                 ▼                 ▼                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     GM-007 APPLICATION LAYER                          │  │
│  │                                                                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │Workspace │ │Timeline  │ │Gochara   │ │Comparison│ │Print     │    │  │
│  │  │          │ │          │ │          │ │          │ │Framework │    │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                                                                │
│            │ (read-only access for GM-008 layers)                           │
│            ▼                                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     GM-008 UPPER LAYERS                               │  │
│  │                                                                       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │  │
│  │  │Knowledge │ │AI        │ │Practice  │ │Analytics │ │Reporting │    │  │
│  │  │Graph     │ │Assistant │ │Services  │ │Engine    │ │Engine    │    │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow Rules

| Rule | Description |
|------|-------------|
| **DF-01** | All data flows from deterministic core upward — never downward |
| **DF-02** | Upper layers read lower layers through store contracts |
| **DF-03** | Upper layers write to their own stores, never to lower layer stores |
| **DF-04** | AI reads engine outputs through the read-only bridge |
| **DF-05** | AI writes to AI output store, never to engine output store |
| **DF-06** | Client data flows through Practice layer, referencing engine outputs by hash |

---

## 5. REPOSITORY ARCHITECTURE

### Repository Extension for GM-008

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CONSULTATION REPOSITORY (GM-007 + GM-008)               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         GM-007 CORE (FROZEN)                          │ │
│  │                                                                        │ │
│  │  Consultation {                                                       │ │
│  │    id: UUID                                                           │ │
│  │    version: number                                                    │ │
│  │    status: 'active' | 'archived' | 'recycle_bin' | 'permanent_delete' │ │
│  │    metadata: { title, clientName, birthDataHash, tags, isFavorite }   │ │
│  │    structure: { questionPackageId, selectedQuestionIds, refs }         │ │
│  │    snapshots: Snapshot[]                                              │ │
│  │    outputs: ConsultationOutput[]                                      │ │
│  │    notes: { general, questions, chart, timing, recommendations }       │ │
│  │    audit: { createdAt, updatedAt, gitCommit, gitTag }                  │ │
│  │  }                                                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│                          (GM-008 EXTENSIONS)                                │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                        GM-008 EXTENSIONS                              │ │
│  │                                                                        │ │
│  │  ClientProfile {                                                      │ │
│  │    id: UUID                                                           │ │
│  │    name: string                                                       │ │
│  │    birthDataHash: string        ← Link to consultation                 │ │
│  │    birthData: { date, time, place, lat, lon, tz }                     │ │
│  │    tags: string[]                                                     │ │
│  │    groups: string[]                                                   │ │
│  │    relationships: Relationship[]                                      │ │
│  │    consultationIds: string[]    ← Reverse lookup                      │ │
│  │    version: number                                                    │ │
│  │    audit: AuditTrail                                                   │ │
│  │  }                                                                    │ │
│  │                                                                        │ │
│  │  PracticeProfile {                                                    │ │
│  │    id: UUID                                                           │ │
│  │    name: string                                                       │ │
│  │    practitioners: Practitioner[]                                      │ │
│  │    settings: PracticeSettings                                          │ │
│  │    clientIds: string[]                                                │ │
│  │    version: number                                                    │ │
│  │  }                                                                    │ │
│  │                                                                        │ │
│  │  AIInteraction {                                                      │ │
│  │    id: UUID                                                           │ │
│  │    consultationId: string                                             │ │
│  │    type: 'q&a' | 'draft' | 'explain' | 'pattern'                     │ │
│  │    prompt: string                                                     │ │
│  │    response: string                                                   │ │
│  │    confidence: 'high' | 'medium' | 'low' | 'uncertain'                │ │
│  │    sources: SourceAttribution[]                                       │ │
│  │    audit: AuditTrail                                                   │ │
│  │  }                                                                    │ │
│  │                                                                        │ │
│  │  KnowledgeNode {                                                      │ │
│  │    id: string                                                         │ │
│  │    type: 'domain' | 'formula' | 'house' | 'planet' | 'concept'        │ │
│  │    label: string                                                      │ │
│  │    description: string                                                │ │
│  │    source: 'engine' | 'formula' | 'calibration' | 'derived'            │ │
│  │    edges: KnowledgeEdge[]                                             │ │
│  │    version: number                                                    │ │
│  │  }                                                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Repository Rules

| Rule | Description |
|------|-------------|
| **RE-01** | GM-007 core schema is never modified — only extended |
| **RE-02** | GM-008 extensions add fields, never remove or change existing fields |
| **RE-03** | Client ↔ Consultation link is via `birthDataHash` (deterministic) |
| **RE-04** | All extensions are versioned independently |
| **RE-05** | Repository is the single source of truth for all persisted data |

---

## 6. AI INTEGRATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI INTEGRATION ARCHITECTURE                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         AI GOVERNANCE LAYER                           │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Prompt   │  │ Model    │  │ Validation│  │ Hallucination        │  │ │
│  │  │ Manager  │  │ Registry │  │ Engine    │  │ Detector             │  │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘  │ │
│  └───────┼─────────────┼─────────────┼───────────────────┼──────────────┘ │
│          │             │             │                   │                │
│  ┌───────┼─────────────┼─────────────┼───────────────────┼──────────────┐ │
│  │       │        AI ENGINE LAYER    │                   │              │ │
│  │  ┌────┴──────────────────────────┴────────────────────┴─────┐        │ │
│  │  │                    AI Orchestrator                        │        │ │
│  │  └──┬──────────┬──────────┬──────────┬──────────────────────┘        │ │
│  │     │          │          │          │                                │ │
│  │  ┌──┴───┐  ┌───┴───┐  ┌───┴───┐  ┌───┴───────┐                        │ │
│  │  │ Q&A  │  │ Draft │  │Explain│  │ Pattern   │                        │ │
│  │  │Handler│  │Handler│  │Handler│  │ Handler   │                        │ │
│  │  └──┬───┘  └───┬───┘  └───┬───┘  └───┬───────┘                        │ │
│  └─────┼──────────┼──────────┼──────────┼────────────────────────────────┘ │
│        │          │          │          │                                  │
│  ┌─────┼──────────┼──────────┼──────────┼────────────────────────────────┐ │
│  │     │     AI PROVIDER LAYER    │          │                            │ │
│  │  ┌──┴──────────┴──────────┴────────────┴──┐                            │ │
│  │  │           Provider Adapter              │                            │ │
│  │  └──┬──────────────────┬──────────────────┘                            │ │
│  │     │                  │                                               │ │
│  │  ┌──┴──────┐     ┌─────┴──────┐                                        │ │
│  │  │ Cloud   │     │ Self-Hosted│                                        │ │
│  │  │ API     │     │ LLM        │                                        │ │
│  │  │(OpenAI) │     │(Llama/etc) │                                        │ │
│  │  └─────────┘     └────────────┘                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### AI Integration Rules

| Rule | Description |
|------|-------------|
| **AI-01** | AI engine reads engine outputs through read-only store contracts |
| **AI-02** | AI engine writes to AI output store, never to engine output store |
| **AI-03** | Every AI interaction is audited (prompt, response, sources, confidence) |
| **AI-04** | AI outputs are validated before presentation to astrologer |
| **AI-05** | AI outputs are clearly marked as "AI-assisted" |
| **AI-06** | Provider abstraction enables switching between cloud and self-hosted |
| **AI-07** | Prompt templates are versioned and stored in the repository |

---

## 7. KNOWLEDGE GRAPH ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE GRAPH ARCHITECTURE                            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         GRAPH DATABASE                                │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                        NODE TYPES                                │ │ │
│  │  │                                                                   │ │ │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │ │ │
│  │  │  │ DOMAIN  │  │ FORMULA │  │ HOUSE   │  │ PLANET  │             │ │ │
│  │  │  │         │  │         │  │         │  │         │             │ │ │
│  │  │  │ Marriage│  │MAR-DEL  │  │ 7th     │  │ Saturn  │             │ │ │
│  │  │  │ Career  │  │CAR-PRO  │  │ 10th    │  │ Jupiter │             │ │ │
│  │  │  │ Health  │  │HLT-VIT  │  │ 6th     │  │ Mars    │             │ │ │
│  │  │  │ Wealth  │  │WTH-ACC  │  │ 2nd     │  │ Venus   │             │ │ │
│  │  │  │ ...     │  │ ...     │  │ ...     │  │ ...     │             │ │ │
│  │  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘             │ │ │
│  │  └───────┼────────────┼────────────┼────────────┼──────────────────┘ │ │
│  │          │            │            │            │                     │ │
│  │  ┌───────┴────────────┴────────────┴────────────┴──────────────────┐ │ │
│  │  │                        EDGE TYPES                               │ │ │
│  │  │                                                                  │ │ │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │ │ │
│  │  │  │ ACTIVATES    │  │ DEPENDS_ON   │  │ CALIBRATED_BY        │   │ │ │
│  │  │  │ (Formula →   │  │ (Formula →   │  │ (Formula →           │   │ │ │
│  │  │  │  Domain)     │  │  Formula)    │  │  Calibration)        │   │ │ │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │ │ │
│  │  │                                                                  │ │ │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │ │ │
│  │  │  │ OCCUPIES     │  │ ASPECTS      │  │ EVIDENCE_FOR         │   │ │ │
│  │  │  │ (Planet →    │  │ (Planet →    │  │ (Formula →           │   │ │ │
│  │  │  │  House)      │  │  Planet)     │  │  Consultation)       │   │ │ │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         GRAPH SERVICES                                │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Graph    │  │ Domain   │  │ Evidence │  │ Recommendation        │  │ │
│  │  │ Query    │  │ Library  │  │ Chains   │  │ Engine                │  │ │
│  │  │ API      │  │ API      │  │ API      │  │                       │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Knowledge Graph Rules

| Rule | Description |
|------|-------------|
| **KG-01** | Graph is derived from deterministic data (engines, formulas, calibration) |
| **KG-02** | Every node is traceable to a deterministic source |
| **KG-03** | Every edge is traceable to a formula relationship |
| **KG-04** | Graph is versioned; old versions preserved for consultation history |
| **KG-05** | Graph is queried by AI but never modified by AI |
| **KG-06** | Graph modifications require Chief Architect approval |

---

## 8. CLIENT MANAGEMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLIENT MANAGEMENT ARCHITECTURE                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         CLIENT PROFILE                                │ │
│  │                                                                        │ │
│  │  ClientProfile {                                                      │ │
│  │    id: UUID                                                           │ │
│  │    name: string                                                       │ │
│  │    birthDataHash: string          ← Link to consultations             │ │
│  │    birthData: {                                                       │ │
│  │      date: string                                                     │ │
│  │      time: string                                                     │ │
│  │      place: string                                                    │ │
│  │      latitude: number                                                 │ │
│  │      longitude: number                                                │ │
│  │      timezone: string                                                 │ │
│  │    }                                                                  │ │
│  │    tags: string[]                                                     │ │
│  │    groups: string[]                                                   │ │
│  │    relationships: [                                                   │ │
│  │      { type: 'spouse' | 'child' | 'parent', targetClientId: UUID }    │ │
│  │    ]                                                                  │ │
│  │    consultationIds: UUID[]                                             │ │
│  │    notes: string                                                      │ │
│  │    version: number                                                    │ │
│  │    audit: { createdAt, updatedAt, createdBy }                          │ │
│  │  }                                                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         CLIENT SERVICES                               │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Profile  │  │ History  │  │ Search   │  │ Relationship          │  │ │
│  │  │ CRUD     │  │ View     │  │ & Filter │  │ Manager               │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         LINK TO CONSULTATIONS                         │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  ClientProfile.birthDataHash ────▶ Consultation.metadata.        │ │ │
│  │  │                                    birthDataHash                  │ │ │
│  │  │                                                                   │ │ │
│  │  │  ClientProfile.consultationIds ◀──── Consultation.id (reverse)    │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. PRACTICE MANAGEMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PRACTICE MANAGEMENT ARCHITECTURE                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         PRACTICE PROFILE                              │ │
│  │                                                                        │ │
│  │  PracticeProfile {                                                    │ │
│  │    id: UUID                                                           │ │
│  │    name: string                                                       │ │
│  │    practitioners: [                                                   │ │
│  │      { id: UUID, name: string, role: 'owner' | 'practitioner' }       │ │
│  │    ]                                                                  │ │
│  │    settings: {                                                        │ │
│  │      branding: { primaryColor, secondaryColor, logo }                  │ │
│  │      reportDefaults: { profile, format, sections }                    │ │
│  │      aiDefaults: { provider, model, privacyMode }                      │ │
│  │    }                                                                  │ │
│  │    clientIds: UUID[]                                                  │ │
│  │    subscription: { tier, status, expiry }                              │ │
│  │    version: number                                                    │ │
│  │  }                                                                    │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         PRACTICE SERVICES                             │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │Dashboard │  │Scheduling│  │Billing   │  │ Document              │  │ │
│  │  │          │  │          │  │          │  │ Storage               │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         MULTI-TENANCY                                 │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Practice A                    Practice B                        │ │ │
│  │  │  ├── Clients (isolated)        ├── Clients (isolated)            │ │ │
│  │  │  ├── Consultations (isolated)  ├── Consultations (isolated)       │ │ │
│  │  │  ├── Settings (isolated)       ├── Settings (isolated)            │ │ │
│  │  │  └── AI History (isolated)     └── AI History (isolated)          │ │ │
│  │  │                                                                   │ │ │
│  │  │  SHARED: Deterministic Engines, Formula Registry, Calibration     │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. REPORTING ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        REPORTING ARCHITECTURE                               │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         REPORT TEMPLATE SYSTEM                        │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Template │  │ Section  │  │ Variable │  │ Personalization       │  │ │
│  │  │ Registry │  │ Library  │  │ Engine   │  │ Engine                │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         REPORT GENERATION PIPELINE                    │ │
│  │                                                                        │ │
│  │  Template ──▶ Variables ──▶ Sections ──▶ Assembly ──▶ PrintFramework  │ │
│  │  Selection    Resolved     Assembled    (PDF/HTML)   (Single Gateway)  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         OUTPUT RECORDING                              │ │
│  │                                                                        │ │
│  │  Every output:                                                         │ │
│  │  • Output ID (UUID)                                                   │ │
│  │  • Profile (quick/standard/professional/research/book)                 │ │
│  │  • Format (pdf/html/json)                                             │ │
│  │  • Generated timestamp                                                │ │
│  │  • Checksum (SHA-256)                                                 │ │
│  │  • Sections included                                                  │ │
│  │  • Repository version                                                 │ │
│  │  • Git commit + tag                                                   │ │
│  │  • Immutable (append-only)                                            │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. SNAPSHOT INTELLIGENCE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   SNAPSHOT INTELLIGENCE ARCHITECTURE                        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         COMPARISON ENGINE                             │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Snapshot A ──┐                                                  │ │ │
│  │  │               ├──▶ Diff Engine ──▶ Comparison Report             │ │ │
│  │  │  Snapshot B ──┘                                                  │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         TREND DETECTION                               │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Snapshots[0..N] ──▶ Time Series ──▶ Pattern Detection           │ │ │
│  │  │                                                                    │ │ │
│  │  │  Detected Patterns:                                               │ │ │
│  │  │  • Transit activation trends (rising/falling/cyclical)            │ │ │
│  │  │  • Dasha period correlations                                      │ │ │
│  │  │  • Domain-specific impact patterns                                 │ │ │
│  │  │  • Planet strength trajectories                                   │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         PREDICTIVE LAYER                              │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Historical Patterns ──▶ Projection Model ──▶ Forecast            │ │ │
│  │  │                                                                    │ │ │
│  │  │  ⚠️ ALL FORECASTS ARE AI-ASSISTED, NOT DETERMINISTIC              │ │ │
│  │  │  ⚠️ Clearly labeled as "Projection" not "Prediction"              │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. ENTERPRISE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENTERPRISE ARCHITECTURE                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         API GATEWAY                                   │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Rate     │  │ Auth     │  │ Version  │  │ Request              │  │ │
│  │  │ Limiting │  │ (JWT)    │  │ Routing  │  │ Logging              │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         SECURITY LAYER                                │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ RBAC     │  │ Data     │  │ Audit    │  │ Encryption            │  │ │
│  │  │ (Roles)  │  │ Isolation│  │ Trail    │  │ (TLS + at-rest)       │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         DEPLOYMENT                                    │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    DEPLOYMENT OPTIONS                            │ │ │
│  │  │                                                                   │ │ │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │ │ │
│  │  │  │ Self-Hosted  │  │ Cloud        │  │ Hybrid               │   │ │ │
│  │  │  │ (Docker)     │  │ (SaaS)       │  │ (Self-hosted +       │   │ │ │
│  │  │  │              │  │              │  │  Cloud AI)           │   │ │ │
│  │  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 13. SECURITY ARCHITECTURE

| Layer | Security Control | Implementation |
|-------|-----------------|----------------|
| **Network** | TLS 1.3 for all API calls | Enforced at API Gateway |
| **Authentication** | JWT with refresh tokens | Auth Service |
| **Authorization** | Role-based (Owner, Practitioner, Viewer) | RBAC middleware |
| **Data Isolation** | Practice-level data partitioning | Repository layer |
| **Audit** | Immutable audit trail for all operations | Audit Service |
| **Encryption** | AES-256 at rest; TLS in transit | Infrastructure |
| **API Security** | Rate limiting, input validation, CORS | API Gateway |
| **AI Security** | Prompt injection defense, data minimization | AI Governance layer |
| **Secrets** | Environment variables, never in code | Deployment config |

---

## 14. EXTENSION / PLUGIN ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EXTENSION ARCHITECTURE (GM-009+)                      │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         EXTENSION POINTS                              │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Report   │  │ UI       │  │ Knowledge│  │ Workflow              │  │ │
│  │  │ Templates│  │ Components│ │ Graph    │  │ Hooks                │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         EXTENSION CONTRACT                            │ │
│  │                                                                        │ │
│  │  Extensions:                                                           │ │
│  │  • Read deterministic outputs through store contracts                  │ │
│  │  • Never modify engine outputs or formulas                            │ │
│  │  • Register at defined extension points                               │ │
│  │  • Are isolated from each other                                       │ │
│  │  • Are versioned and tested independently                             │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 15. API ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API ARCHITECTURE                                  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         API VERSIONS                                  │ │
│  │                                                                        │ │
│  │  /api/v1/  ──── GM-007 endpoints (FROZEN)                             │ │
│  │  /api/v2/  ──── GM-008 endpoints (NEW)                                │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  v1 Endpoints (GM-007):                                          │ │ │
│  │  │  /api/v1/upload          — Chart upload                          │ │ │
│  │  │  /api/v1/pipeline        — Run deterministic pipeline            │ │ │
│  │  │  /api/v1/report          — Generate report                       │ │ │
│  │  │  /api/v1/questions       — Question catalog                      │ │ │
│  │  │  /api/v1/verify          — Verification console                  │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  v2 Endpoints (GM-008):                                          │ │ │
│  │  │  /api/v2/clients         — Client CRUD                           │ │ │
│  │  │  /api/v2/practice        — Practice management                   │ │ │
│  │  │  /api/v2/ai              — AI assistant interactions             │ │ │
│  │  │  /api/v2/knowledge       — Knowledge graph queries               │ │ │
│  │  │  /api/v2/analytics       — Practice analytics                    │ │ │
│  │  │  /api/v2/snapshots       — Snapshot intelligence                 │ │ │
│  │  │  /api/v2/export          — Data export/import                    │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 16. EVENT FLOW ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EVENT FLOW ARCHITECTURE                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         EVENT TYPES                                   │ │
│  │                                                                        │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐    │ │
│  │  │ Consultation │  │ Snapshot     │  │ Output                    │    │ │
│  │  │ Created      │  │ Created      │  │ Generated                 │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘    │ │
│  └─────────┼─────────────────┼───────────────────────┼──────────────────┘ │
│            │                 │                       │                     │
│            ▼                 ▼                       ▼                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         EVENT BUS                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│            │                 │                       │                     │
│            ▼                 ▼                       ▼                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐        │
│  │ Audit        │  │ Knowledge    │  │ Analytics                │        │
│  │ Logger       │  │ Graph Update │  │ Engine Update            │        │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 17. VERSION INTERACTION MAP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      VERSION INTERACTION MAP                                │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │  Consultation v1 ──── References ────▶ Calibration v1.0.0             │ │
│  │       │                                Formula Registry v1.0.0        │ │
│  │       │                                Question Catalog v1.0.0        │ │
│  │       │                                Architecture v1.2.0            │ │
│  │       │                                                               │ │
│  │       ▼                                                               │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Version Compatibility Rule:                                     │ │ │
│  │  │                                                                  │ │ │
│  │  │  A consultation created with version X of a component ALWAYS     │ │ │
│  │  │  produces the same output, regardless of later version changes.  │ │ │
│  │  │                                                                  │ │ │
│  │  │  New consultations use the latest versions.                      │ │ │
│  │  │  Existing consultations retain their creation versions.          │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 18. DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DEPLOYMENT ARCHITECTURE                              │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                         DOCKER COMPOSE                                │ │
│  │                                                                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │ │
│  │  │ Frontend │  │ Backend  │  │ AI       │  │ Knowledge             │  │ │
│  │  │ (Vite +  │  │ (FastAPI)│  │ Service  │  │ Graph DB              │  │ │
│  │  │  React)  │  │          │  │          │  │ (optional)            │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│  ┌─────────────────────────────────┴─────────────────────────────────────┐ │
│  │                         DEPLOYMENT MODES                              │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  MODE          │  Components              │  AI Provider          │ │ │
│  │  │  ──────────────┼──────────────────────────┼────────────────────── │ │ │
│  │  │  Self-Hosted   │  All local (Docker)      │  Self-hosted LLM      │ │ │
│  │  │  Cloud (SaaS)  │  Hosted platform         │  Cloud API or local   │ │ │
│  │  │  Hybrid        │  Local app + Cloud AI    │  Cloud API            │ │ │
│  │  │  Desktop       │  Tauri app + local API   │  None or local LLM    │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 19. SCALABILITY STRATEGY

| Component | Scaling Strategy | Rationale |
|-----------|-----------------|-----------|
| **Deterministic Engines** | Vertical scaling (CPU-bound) | Engine computation is CPU-intensive; not easily distributed |
| **API Gateway** | Horizontal scaling (stateless) | Standard load-balanced HTTP |
| **AI Service** | Horizontal + provider scaling | Queue-based with multiple provider adapters |
| **Knowledge Graph** | Read replicas | Read-heavy; write operations are rare |
| **Repository** | LocalStorage (single-user) → IndexedDB (multi-user) → Backend DB (enterprise) | Progressive enhancement based on deployment mode |
| **Reporting** | Async queue with workers | PDF generation is CPU-intensive; batch via queue |

---

## 20. FUTURE EVOLUTION STRATEGY

```
GM-008 (Current)               GM-009 (Next)               GM-010 (Future)
─────────────────              ─────────────               ──────────────
Platform Foundation            Learning System              Marketplace
                               
• AI Assistant                 • Feedback loops            • Plugin marketplace
• Knowledge Graph              • Model improvement          • White-label
• Client Management            • New domains (Muhurta,     • Mobile apps
• Practice Management           Prashna, Horary)           • Real-time collab
• Reporting & Analytics        • Guru-Shishya mode         • API ecosystem
• Snapshot Intelligence        • Continuous calibration    • Third-party integrations
• Enterprise Foundation         refinement                 • Enterprise SSO
```

---

## CROSS-CUTTING CONCERNS

### Shared Services

| Service | Consumers | Description |
|---------|-----------|-------------|
| **Auth Service** | All layers | JWT authentication, RBAC, session management |
| **Audit Service** | All layers | Immutable audit trail for all operations |
| **Config Service** | All layers | Centralized configuration management |
| **Logging Service** | All layers | Structured logging with correlation IDs |
| **Event Bus** | All layers | Pub/sub for cross-module communication |

### Common Infrastructure

| Component | Description |
|-----------|-------------|
| **Store Contracts** | Zustand stores with read/write contracts per layer |
| **API Gateway** | Single entry point with versioning, auth, rate limiting |
| **Repository** | Single source of truth for all persisted data |
| **PrintFramework** | Single gateway for all file generation |

### Reusable UI Components

| Component | Used By |
|-----------|---------|
| **ConsultationCard** | Client history, search results, dashboard |
| **MetricCard** | Dashboard, analytics, snapshot comparison |
| **DetailCard** | Client profile, consultation details, practice settings |
| **TagManager** | Client tags, consultation tags, knowledge tags |
| **SearchBar** | Client search, consultation search, knowledge search |
| **ConfidenceBadge** | AI outputs, snapshot integrity, formula evidence |
| **AuditTrailViewer** | AI history, consultation history, practice audit |

### Architectural Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AI hallucination contaminating knowledge graph** | Critical | AI reads knowledge graph but never writes; graph modifications require Chief Architect |
| **Client data isolation breach** | Critical | Repository-level partitioning; RBAC; audit logging |
| **Performance degradation with scale** | High | Horizontal scaling design; pagination; async processing |
| **Repository schema complexity** | Medium | Versioned extensions; backward compatibility; migration scripts |
| **AI provider lock-in** | Medium | Provider abstraction layer; self-hosted option |

### Recommended Implementation Sequence

```
M1: Foundation (API Gateway, Auth, Audit, Config)
    │
    ├── M2: Client Management (parallel with M3)
    │
    ├── M3: AI Assistant (parallel with M2)
    │
    ├── M4: Knowledge Graph (depends on M3 for usage patterns)
    │
    ├── M5: Practice Management (depends on M2)
    │
    ├── M6: Reporting & Analytics (depends on M2, M3, M4, M5)
    │
    ├── M7: Snapshot Intelligence (parallel with M6)
    │
    └── M8: Enterprise (depends on all prior)
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                         AP-004 COMPLETE                                      ║
║                                                                              ║
║    Document: GM-008_PLATFORM_ARCHITECTURE_BLUEPRINT.md                      ║
║    Version: 1.0.0                                                            ║
║                                                                              ║
║    Sections: 20 (Overall through Future Evolution)                          ║
║    Cross-cutting: Shared services, infrastructure, risks, sequence          ║
║                                                                              ║
║    Complete platform architecture from system perspective.                  ║
║    No code generated. No repository modified.                               ║
║                                                                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```