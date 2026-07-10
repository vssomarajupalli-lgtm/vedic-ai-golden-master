# BKL-009 Documentation Taxonomy Constitution v1

**Date:** 2026-07-10
**Program:** GM-005 Repository Refinement
**Phase:** Discovery (BKL-009)
**Location:** `GM-005/BKL-009/architecture/BKL-009_DOCUMENTATION_TAXONOMY_CONSTITUTION_v1.md`

---

## Part 1: The Six Pillars of Documentation

The repository shall strictly adhere to a 6-pillar documentation taxonomy. No top-level directories outside these six are permitted within the `docs/` root.

### 1. `docs/architecture/`
1.  **Purpose:** Defines system boundaries, high-level structural designs, and formal technical decisions.
2.  **Constitutional role:** The single source of truth for "How the system is designed."
3.  **Allowed document types:** Architecture Decision Records (ADRs), system design blueprints, component dependency graphs, UML/Mermaid diagrams (`.md`, `.svg`, `.png`).
4.  **Prohibited document types:** Ephemeral status logs, active implementation checklists, handover snapshots, granular code logic.
5.  **Ownership:** Chief Architect.
6.  **Lifecycle:** Canonical designs are updated iteratively; ADRs are immutable and append-only.
7.  **Review authority:** Chief Architect.
8.  **Relationship:** Governed by `governance/`. Guides `engineering/`.
9.  **Examples:** `ADR-010.md`, `ADR-011.md`.
10. **Migration principles:** All high-level system designs migrate here. Implementation details must be stripped and moved to `engineering/`.

### 2. `docs/archive/`
1.  **Purpose:** Permanent cold storage for deprecated, legacy, and superseded artifacts.
2.  **Constitutional role:** The single sink for all expired truth. Excludes obsolete context from AI retrieval.
3.  **Allowed document types:** Deprecated `.md` and `.txt` files, legacy reports, past handover packages.
4.  **Prohibited document types:** Active code, current status docs, canonical knowledge bases.
5.  **Ownership:** Repository Engineer.
6.  **Lifecycle:** Permanent cold storage. Immutable.
7.  **Review authority:** Repository Engineer.
8.  **Relationship:** The terminal state for documents from all other pillars.
9.  **Examples:** `docs/handover/`, `PHASE15_HANDOVER_PACKAGE_20260623_1246/`, `docs/archive/bkl-006_legacy/`.
10. **Migration principles:** Bulk relocate all `handover`, `phase9`, and `project_handover` directories here to clear the root `docs/` namespace.

### 3. `docs/engineering/`
1.  **Purpose:** Active implementation specifications, granular component designs, and QA/validation test strategies.
2.  **Constitutional role:** The bridge translating theoretical architecture into executable code.
3.  **Allowed document types:** Component blueprints, test strategies, algorithm logic, implementation checklists (`.md`).
4.  **Prohibited document types:** System-wide ADRs, constitutional rules, general astrological facts.
5.  **Ownership:** Implementation Lead / Engineering Agents.
6.  **Lifecycle:** Highly mutable during build phases.
7.  **Review authority:** Implementation Lead / QA.
8.  **Relationship:** Implements `architecture/`. Depends on `knowledge/`. Provides validation proof to `status/`.
9.  **Examples:** Files currently in `docs/engineering/implementation/`, `docs/engineering/validation/`, and `docs/engineering/question_engine/`.
10. **Migration principles:** Consolidate active build directories into logical subfolders (e.g., `engineering/question_engine/`, `engineering/validation/`).

### 4. `docs/governance/`
1.  **Purpose:** Constitutional rules, overarching coding standards, and project guardrails.
2.  **Constitutional role:** The supreme law of the repository. Overrides all other documentation.
3.  **Allowed document types:** Manifests, governance rules, compliance checklists, security/audit reports (`.md`).
4.  **Prohibited document types:** Code snippets, status logs, system architectures, mathematical algorithms.
5.  **Ownership:** Chief Architect / Project Lead.
6.  **Lifecycle:** Canonical and strictly controlled. Requires extreme consensus and formal audits to change.
7.  **Review authority:** Chief Architect.
8.  **Relationship:** Governs all other pillars.
9.  **Examples:** `GOLDEN_MASTER_MANIFEST.md`, `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md`, files in `docs/governance/audits/`.
10. **Migration principles:** Protect the existing `docs/governance/` folder structure. Merge `docs/governance/audits/` into it as a subfolder.

### 5. `docs/knowledge/`
1.  **Purpose:** Astrological domain facts, mathematical formulas, and external system reference manuals.
2.  **Constitutional role:** The undisputed dictionary and factual reference base for the system.
3.  **Allowed document types:** Domain rules, mathematical formulas, API references, educational guides (`.md`).
4.  **Prohibited document types:** System architecture, active project status, implementation code.
5.  **Ownership:** Subject Matter Expert (SME).
6.  **Lifecycle:** Canonical. Updated only when external facts, formulas, or scholarly interpretations change.
7.  **Review authority:** Subject Matter Expert.
8.  **Relationship:** Provides factual grounding for `architecture/` and `engineering/`.
9.  **Examples:** Files currently in `docs/knowledge/`, `docs/knowledge/`, and `docs/knowledge/`.
10. **Migration principles:** Absorb `docs/knowledge/` and `docs/knowledge/` completely to form a single unified factual library.

### 6. `docs/status/`
1.  **Purpose:** Active project tracking, milestone backlogs, discovery reports, and current state representations.
2.  **Constitutional role:** The operational heartbeat and state machine of the project.
3.  **Allowed document types:** Backlogs, task lists, current state reports, discovery reports (`.md`, `.txt`).
4.  **Prohibited document types:** Permanent architecture designs, domain knowledge, constitutional rules.
5.  **Ownership:** Repository Engineer / Project Manager.
6.  **Lifecycle:** Ephemeral and rapidly updated. Frequently deprecated and rotated to `archive/`.
7.  **Review authority:** Repository Engineer.
8.  **Relationship:** Consumes updates from all pillars to track project velocity.
9.  **Examples:** Files currently in `docs/status/`, `docs/status/`, and `docs/status/`.
10. **Migration principles:** Consolidate all tracking into one unified folder. Eliminate conflicting state files.

---

## Part 2: Governance and Execution Rules

### A. Repository Documentation Constitution
The `docs/` hierarchy is a managed graph, not a filesystem dump. The six root pillars (`architecture`, `archive`, `engineering`, `governance`, `knowledge`, `status`) represent the absolute entirety of permitted top-level taxonomy. No script, agent, or engineer shall create a 7th pillar without a formal Constitutional Amendment.

### B. Documentation Placement Rules
Placement is determined by intent:
*   *Is it a rule?* -> `governance/`
*   *Is it a design?* -> `architecture/`
*   *Is it a build spec?* -> `engineering/`
*   *Is it a fact?* -> `knowledge/`
*   *Is it a state?* -> `status/`
*   *Is it dead?* -> `archive/`

### C. File Naming Standards
*   **Canonical Documents:** Must use `UPPER_SNAKE_CASE.md` (e.g., `QUESTION_ENGINE_ARCHITECTURE.md`).
*   **Timestamp Prohibition:** Active, canonical documents must **never** contain a timestamp or date in the filename. Version control is the strict responsibility of Git.
*   **Exceptions:** Phase logs, handover packages, and archival dumps may retain timestamps to denote their frozen historical state.

### D. Canonical Ownership Rules
Every knowledge domain has exactly ONE authoritative location and ONE designated owner. In the event of conflicting information across the repository, the document residing within the domain's authoritative pillar (as defined in Part 1) supersedes all others.

### E. Archive Governance
The `docs/archive/` pillar is the repository's graveyard. Files placed here are considered permanently retired. AI tooling and RAG (Retrieval-Augmented Generation) systems must be configured to explicitly exclude `docs/archive/` from their context windows to prevent hallucination based on deprecated facts.

### F. Status Document Governance
Status documents are living entities. Creating a new status snapshot (e.g., `STATUS_JULY_10.md`) is prohibited. The designated status file (e.g., `CURRENT_SYSTEM_STATE.md`) must be overwritten and updated in place. Old states are tracked via Git history.

### G. Knowledge Governance
The `knowledge/` pillar must remain completely decoupled from implementation details. It defines *what* the facts are (e.g., Vedic formulas, astronomical calculations), not *how* they are implemented in Python.

### H. Future Expansion Rules
Expansion of the documentation footprint is explicitly restricted to subdirectories *within* the six established pillars. For example, `engineering/frontend_tests/` is permitted; `docs/frontend_tests/` is strictly prohibited.

---

## Part 3: Implementation Readiness Assessment

**Status: READY FOR MIGRATION**

The repository is fully ready for documentation migration. 
*   The Evidence Report (BKL-009) has identified all current fragmentation and mapped all source targets.
*   This Constitution explicitly defines all valid destinations, boundaries, and migration principles.
*   Zero missing architectural prerequisites exist.

The system is prepared to proceed to the BKL-009 Execution Phase to physically enforce this taxonomy via Git operations.
