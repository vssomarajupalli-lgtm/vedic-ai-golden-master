# BKL-009 Documentation Taxonomy Evidence Report v1

**Date:** 2026-07-10
**Program:** GM-005 Repository Refinement
**Phase:** Discovery (BKL-009)
**Location:** `GM-005/BKL-009/architecture/BKL-009_DOCUMENTATION_TAXONOMY_EVIDENCE_REPORT_v1.md`

---

## Part 1: Directory Evidence Review

The following is an evidence-based assessment of all top-level directories currently residing under `docs/`.

### 1. `architecture/`
*   **Primary purpose:** System boundaries, design documents, and Architecture Decision Records (ADRs).
*   **Number of files:** 48
*   **Primary document types:** `.md`
*   **Current owner:** Chief Architect
*   **Overlapping directories:** `implementation/`, `question_engine/`
*   **Duplicate information risk:** Low (if strictly governed).
*   **AI retrieval impact:** Positive (high signal-to-noise for system design).
*   **Should remain independent?** Yes.

### 2. `archive/`
*   **Primary purpose:** Storage for deprecated, legacy, and superseded artifacts.
*   **Number of files:** 94
*   **Primary document types:** `.md`, `.txt`
*   **Current owner:** Repository Engineer
*   **Overlapping directories:** `handover/`, `project_handover/`, `HANDOVER_PACKAGE_2026-06-17_PHASE7_FINAL/`, `phase9/`
*   **Duplicate information risk:** Extreme (contains outdated copies of active documents).
*   **AI retrieval impact:** Highly Negative (pollutes context window with obsolete facts).
*   **Should remain independent?** Yes (but must act as the *sole* destination for all deprecated files).

### 3. `audits/`
*   **Primary purpose:** Security, compliance, and architectural audits.
*   **Number of files:** 8
*   **Primary document types:** `.md`
*   **Current owner:** Architecture Advisor
*   **Overlapping directories:** `validation/`, `governance/`
*   **Duplicate information risk:** Low.
*   **AI retrieval impact:** Neutral.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/governance/audits/`

### 4. `current/`
*   **Primary purpose:** Active project state tracking.
*   **Number of files:** 4
*   **Primary document types:** `.md`
*   **Current owner:** Unclear (Historical agents)
*   **Overlapping directories:** `status/`, `current_status/`
*   **Duplicate information risk:** High.
*   **AI retrieval impact:** Negative (conflicting state data).
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/status/`

### 5. `current_status/`
*   **Primary purpose:** Active project state tracking.
*   **Number of files:** 13
*   **Primary document types:** `.md`
*   **Current owner:** Unclear (Historical agents)
*   **Overlapping directories:** `status/`, `current/`
*   **Duplicate information risk:** High.
*   **AI retrieval impact:** Negative.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/status/`

### 6. `docs/` (nested)
*   **Primary purpose:** Contains `samartha_v2` nested documentation.
*   **Number of files:** 10
*   **Primary document types:** `.md`
*   **Current owner:** Unknown
*   **Overlapping directories:** `architecture/`, `knowledge/`
*   **Duplicate information risk:** Medium.
*   **AI retrieval impact:** Negative (redundant pathing `docs/docs/`).
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/knowledge/` or `docs/archive/`

### 7. `governance/`
*   **Primary purpose:** Constitutional rules, GOLDEN_MASTER_MANIFEST, and development standards.
*   **Number of files:** 25
*   **Primary document types:** `.md`
*   **Current owner:** Chief Architect
*   **Overlapping directories:** None logically, though historically overlapped with root.
*   **Duplicate information risk:** Low.
*   **AI retrieval impact:** Positive (essential for agent boundaries).
*   **Should remain independent?** Yes.

### 8. `handover/` & `project_handover/`
*   **Primary purpose:** Historical phase transition snapshots.
*   **Number of files:** 25 combined (14 + 11)
*   **Primary document types:** `.md`
*   **Current owner:** Legacy Phase Managers
*   **Overlapping directories:** `archive/`, `phase9/`, `HANDOVER_PACKAGE_...`
*   **Duplicate information risk:** Extreme.
*   **AI retrieval impact:** Highly Negative.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/archive/handovers/`

### 9. `HANDOVER_PACKAGE_2026-06-17_PHASE7_FINAL/`
*   **Primary purpose:** Point-in-time historical transition package.
*   **Number of files:** 12
*   **Primary document types:** `.md`
*   **Current owner:** Legacy Phase Managers
*   **Overlapping directories:** `archive/`, `handover/`
*   **Duplicate information risk:** Extreme.
*   **AI retrieval impact:** Highly Negative.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/archive/handovers/`

### 10. `implementation/`
*   **Primary purpose:** Active build specifications and execution plans.
*   **Number of files:** 8
*   **Primary document types:** `.md`
*   **Current owner:** Engineering / Implementation Agents
*   **Overlapping directories:** `architecture/`, `validation/`, `question_engine/`
*   **Duplicate information risk:** Medium.
*   **AI retrieval impact:** Positive (if active), Negative (if stale).
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/engineering/implementation/`

### 11. `knowledge/`
*   **Primary purpose:** Astrological and domain-specific knowledge bases.
*   **Number of files:** 18
*   **Primary document types:** `.md`
*   **Current owner:** Subject Matter Experts
*   **Overlapping directories:** `reference/`
*   **Duplicate information risk:** Medium.
*   **AI retrieval impact:** Positive (crucial for engine logic).
*   **Should remain independent?** Yes.

### 12. `phase9/`
*   **Primary purpose:** Point-in-time phase artifact.
*   **Number of files:** 1
*   **Primary document types:** `.md`
*   **Current owner:** Legacy Phase Manager
*   **Overlapping directories:** `archive/`
*   **Duplicate information risk:** High.
*   **AI retrieval impact:** Negative.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/archive/handovers/`

### 13. `question_engine/`
*   **Primary purpose:** Granular architectural blueprints and timestamped snapshots for the Question Engine.
*   **Number of files:** 14
*   **Primary document types:** `.md`
*   **Current owner:** Engine Lead
*   **Overlapping directories:** `implementation/`, `architecture/`
*   **Duplicate information risk:** High (due to snapshot naming).
*   **AI retrieval impact:** Negative (fragmented snapshot files).
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/engineering/question_engine/`

### 14. `reference/`
*   **Primary purpose:** Reference manuals and lookups.
*   **Number of files:** 9
*   **Primary document types:** `.md`
*   **Current owner:** Subject Matter Experts
*   **Overlapping directories:** `knowledge/`
*   **Duplicate information risk:** Medium.
*   **AI retrieval impact:** Positive.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/knowledge/`

### 15. `status/`
*   **Primary purpose:** Active project tracking and task lists.
*   **Number of files:** 66
*   **Primary document types:** `.md`
*   **Current owner:** Repository Engineer / Project Manager
*   **Overlapping directories:** `current/`, `current_status/`
*   **Duplicate information risk:** High (currently).
*   **AI retrieval impact:** Mixed (valuable if clean, highly negative if sprawling).
*   **Should remain independent?** Yes (as the sole consolidated status domain).

### 16. `validation/`
*   **Primary purpose:** Test strategies and verification outcomes.
*   **Number of files:** 6
*   **Primary document types:** `.md`
*   **Current owner:** QA / Validation Agents
*   **Overlapping directories:** `implementation/`, `audits/`
*   **Duplicate information risk:** Low.
*   **AI retrieval impact:** Positive.
*   **Should remain independent?** No.
*   **Recommended permanent destination:** `docs/engineering/validation/`

---

## Part A. Documentation Dependency Matrix

| Domain | Depends On | Provides Input To |
| :--- | :--- | :--- |
| **Architecture** | Governance, Knowledge | Engineering, Status |
| **Governance** | (Self-standing, Supreme) | Architecture, Engineering, Audits |
| **Engineering** | Architecture, Governance | Status, Validation |
| **Knowledge** | (External domain facts) | Architecture, Engineering |
| **Status** | Architecture, Engineering | (Human coordination) |
| **Archive** | (None) | (None - excluded from RAG) |

---

## Part B. Canonical Ownership Matrix

| Knowledge Domain | Authoritative Location | Owner |
| :--- | :--- | :--- |
| **Constitutional Rules** | `docs/governance/GOLDEN_MASTER_MANIFEST.md` | Chief Architect |
| **System Architecture** | `docs/architecture/` | Chief Architect |
| **Technical Implementation**| `docs/engineering/` | Implementation Lead |
| **Astrological Domain** | `docs/knowledge/` | Subject Matter Expert |
| **Project Tracking** | `docs/status/` | Repository Engineer |
| **Historical Records** | `docs/archive/` | Repository Engineer |

---

## Part C. Consolidation Candidates

| Source | Destination | Est. Files Affected | Risk | Complexity | Expected Benefit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `current/`, `current_status/` | `docs/status/` | ~17 files | Low | Low | Unifies project state, reduces AI hallucinations regarding current progress. |
| `handover/`, `project_handover/`, `phase9/`, `HANDOVER_PACKAGE_...` | `docs/archive/handovers/` | ~38 files | Low | Medium (link updates) | Eliminates massive legacy RAG pollution. |
| `reference/`, `docs/docs/` | `docs/knowledge/` | ~19 files | Low | Low | Centralizes domain facts. |
| `implementation/`, `validation/`, `question_engine/` | `docs/engineering/` | ~28 files | Medium | Medium | Organizes active build logic away from theoretical architecture. |
| `audits/` | `docs/governance/audits/` | ~8 files | Low | Low | Properly aligns compliance tracking with governance. |

---

## Part D. Proposed Final Documentation Hierarchy

**Canonical Documentation Taxonomy v1.0**

```text
docs/
├── architecture/       # System design, interfaces, and ADRs
│   └── decisions/      # Architecture Decision Records
├── archive/            # STRICTLY for deprecated files, legacy code, and historical handovers
│   └── handovers/      # Isolated historical transitions
├── engineering/        # Active implementation specs, component designs, and QA
│   ├── implementation/
│   ├── validation/
│   └── question_engine/
├── governance/         # Manifest, coding standards, and constitutional rules
│   └── audits/         # Compliance and security audit logs
├── knowledge/          # Domain reference (astrological facts, formulas, external system docs)
└── status/             # Active project tracking, backlogs, and current state
```

*(End of Report - No implementation has been executed)*
