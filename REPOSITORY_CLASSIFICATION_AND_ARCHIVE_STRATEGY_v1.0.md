# REPOSITORY CLASSIFICATION AND ARCHIVE STRATEGY

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Repository classification must occur strictly before any repository refinement begins. To guarantee that no critical deterministic logic, governance rules, or historical context is lost, every repository asset must be categorically identified prior to modification.

Every single repository asset (file, document, engine, or directory) belongs to exactly one official classification. This strategy dictates how each classification is handled, preserved, or archived throughout the Golden Master Program.

---

## SECTION 3: Repository Classification Model

The Golden Master repository strictly enforces the following classification classes:

* **Canonical**: The absolute, unbreakable source of truth for the current architecture, governance, and active deterministic logic.
* **Supporting**: Assets that aid, catalog, or facilitate the use of Canonical assets without defining new rules themselves.
* **Reference**: Historical reports, audits, and completion summaries that provide immutable context for how decisions were made.
* **Legacy**: Older implementations or frameworks that are no longer the primary architectural foundation but must be preserved for exact deterministic reproduction.
* **Archive Candidate**: Files that are superseded, duplicated, obsolete, or temporary, which clutter the repository and should be moved out of the active root.
* **Future**: Assets defining architectures, pipelines, or engines slated for future milestones, not to be implemented or fully integrated currently.
* **Temporary**: Ephemeral working files, scratchpads, or unapproved drafts.

---

## SECTION 4: Classification Rules

| Classification | Purpose | Authority | Modification Policy | Retention Policy | Examples |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Canonical** | Defines the Golden Master. | Absolute Authority | Requires ADR and rigorous review. | Permanent. Never archived. | `GOLDEN_MASTER_MANIFEST.md`, Knowledge Packages, Core Engines |
| **Supporting** | Aids organization and coverage tracking. | Organizational | Writable as active development occurs. | Permanent while relevant. | `FORMULA_CATEGORY_CATALOG_v1.md`, `QUESTION_COVERAGE_MATRIX_v1.md` |
| **Reference** | Provides historical proof of work and audits. | Historical Context | Strictly Read-Only. Never modified. | Permanent. May be moved to `/docs/reference`. | `PHASE14G_ARCHITECTURE_REVIEW.md`, `PROGRAM_A_COMPLETION_REPORT.md` |
| **Legacy** | Preserves older logic for reference and reuse. | Historical Logic | Strictly Read-Only. Never modified. | Permanent. Never deleted. | Transit Engine, Version 1 Codebase |
| **Archive Candidate** | Identifies clutter targeted for clean-up. | None | Read-Only until archived. | Moved to `/docs/archive`. Never outright deleted. | Historical drafts, step-by-step interim phase reports |
| **Future** | Defines upcoming roadmap features. | Roadmap Placeholder | Writable until its milestone is active. | Preserved for future phases. | Moon Mandali, Gochara Engine plans |
| **Temporary** | Facilitates immediate work. | None | Unrestricted. | Delete upon completion of immediate task. | `scratch.py`, test dumps |

---

## SECTION 5: Canonical Preservation Policy

Canonical assets represent the irrefutable Constitution of the Golden Master and **MUST** always remain active and highly visible within the repository structure.

**Examples:**
* Architecture Constitution
* Approved Architecture Decision Records (ADRs)
* Domain Knowledge Packages
* Canonical Formula Definitions
* Engine Governance Registries
* Data Contracts
* Approved Validation Contracts
* Calibration Profiles
* Core deterministic engines (Planet, House, Dasha, etc.)
* Canonical documentation

**Why they are never archived:** 
Archiving canonical assets breaks the active dependency chain, obscures the rules of the system, and introduces severe architectural drift. They must remain actively maintained and permanently accessible in the repository root or primary `/docs` hierarchy.

---

## SECTION 6: Archive Candidate Policy

Assets classified as Archive Candidates are targeted for relocation to reduce repository noise and improve clarity. 

**Examples:**
* Superseded architectural drafts
* Duplicate documentation identified in the Refinement Master Inventory
* Obsolete planning notes from Phase 8-16
* Historical step-by-step implementation notes (e.g., `PHASE9_STEP1_REPORT_PROFILE_FIX.md`)
* Temporary working files left behind
* Old review and audit documents that have been finalized into Completion Reports

**Crucial Restriction:** Archive classification does **NOT** authorize deletion. An asset marked for archiving is formally relocated to an `/archive` folder structure, preserving its git history and historical value while removing it from the active developer view.

---

## SECTION 7: Legacy Preservation Policy

Legacy material is formally preserved to ensure that older iterations of the system can be referenced or reconstructed exactly as they existed.

**Examples:**
* Version 1 reference implementations
* The Transit Engine (retained for reusable deterministic spatial logic, not Version 2 architecture)
* Historical handover documents
* Migration references and diffs

**Crucial Restriction:** Legacy assets remain permanently available for historical and deterministic reference. They are not subjected to modern refactoring, nor are they deleted. They are strictly preserved.

---

## SECTION 8: Future Classification

Assets detailing systems not slated for the current milestone are classified as Future.

**Examples:**
* Moon Mandali integration blueprints
* Gochara Engine architectural drafts
* AI Narrative / Answer Composer templates
* Question Expansion plans
* Future validation assets for unbuilt engines

**Crucial Restriction:** Future assets remain firmly outside the current implementation scope. They exist as planning artifacts only and must not influence current deterministic execution until their specific milestone is activated.

---

## SECTION 9: Repository Preservation Rules

The following constitutional rules strictly govern repository preservation:

* **No canonical asset may be archived**: The source of truth must always remain actively visible.
* **No archive without approved decision**: Relocating a file to the archive requires a formal entry in the Repository Refinement Decision Register.
* **No deletion without documentation**: Deletion is forbidden unless mathematical/identical duplication is proven and recorded.
* **No knowledge loss**: Archiving or merging must never result in the loss of domain expertise or rules.
* **No deterministic logic loss**: Engine logic, even if Legacy, must be preserved.
* **No governance loss**: The Constitution must remain intact throughout all cleanup.
* **Knowledge preservation before repository cleanup**: Classification and inventory always precede any physical repository modifications.

---

## SECTION 10: Illustrative Classification Examples

*(Note: These example entries are illustrative only and do not authorize immediate implementation).*

* `PROJECT_CONTEXT.md` → **Canonical**
* `ASTROLOGICAL_PREDICTION_GOVERNANCE_v1.md` → **Canonical**
* Historical draft (`PHASE9_STEP1_REPORT_PROFILE_FIX.md`) → **Archive Candidate**
* Transit Engine (`transit_engine.py`) → **Legacy**
* Moon Mandali implementation plans → **Future**

---

## SECTION 11: Governance Freeze

This Repository Classification and Archive Strategy is hereby declared part of the permanent Golden Master Constitution.

All repository assets must be classified according to these rules before any refinement decision is approved. Future classification changes or modifications to this strategy require a rigorous formal process:

* **Architecture Decision Record (ADR)**
* **Architecture Review**
* **Repository Decision Register Entry**
* **Documentation Update**
* **Version Increment**
