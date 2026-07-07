# REPOSITORY REFINEMENT DECISION REGISTER

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Version**: v1.1
* **Status**: ACTIVE
* **Author**: Coding Engine

---

## SECTION 2: Purpose

Repository refinement requires a permanent decision register to ensure strict governance and traceability. Because the Golden Master repository is the definitive source of truth, no files may be arbitrarily removed or altered. 

All repository modifications—including merges, archives, renames, relocations, consolidations, or deletions—must be traceable, justified, and fully reversible through meticulous documentation. This register serves as the permanent constitutional audit trail for all refinement executed during Milestone GM-005 and beyond.

---

## SECTION 3: Decision Register Structure

Every approved repository refinement decision must be recorded using the following standard record format:

* **Decision ID**: Unique identifier (e.g., `REF-001`).
* **Date**: The date the decision was logged.
* **Category**: The type of refinement (see Section 4).
* **Component**: The specific file(s), folder(s), or asset(s) impacted.
* **Current Location**: The absolute or relative path prior to refinement.
* **Proposed Action**: The specific action to be taken (e.g., move, merge, archive).
* **Architectural Reason**: The justification for the refinement.
* **Supporting Evidence**: Links to the Master Inventory or duplicates identified.
* **Impact Assessment**: Evaluation of downstream effects on dependencies or other documents.
* **Approval Status**: Current state of governance approval.
* **Implementation Status**: Current state of execution.
* **Notes**: Any additional context or caveats.

---

## SECTION 4: Decision Categories

Decisions must be strictly classified into one of the following authorized categories:

* **Document Merge**: Combining two or more documents that share identical architectural scope.
* **Document Archive**: Moving superseded or historical phase reports to the archive structure.
* **File Rename**: Standardizing file names to meet constitutional conventions.
* **Folder Rename**: Standardizing directory names for clarity.
* **Folder Merge**: Consolidating directories with overlapping purposes.
* **File Relocation**: Moving a file into its appropriate canonical directory.
* **Duplicate Removal**: Removing identical files (requires rigorous evidence).
* **Knowledge Consolidation**: Centralizing domain knowledge into a singular Knowledge Package.
* **Formula Consolidation Reference**: Organizing formula catalogs (without altering the formulas themselves).
* **Legacy Preservation**: Explicitly protecting legacy code or documentation for reference.
* **Repository Organization**: Creating new foundational folders (e.g., `/docs/archive/`).

---

## SECTION 5: Approval Rules

Every refinement decision is strictly governed. No implementation may occur before formal approval. Every decision requires:

1. **Architectural Review**: Assessment by the architecture board or governing engine.
2. **Evidence**: Proof of duplication, obsolescence, or necessity.
3. **Impact Assessment**: A clear understanding that no canonical logic or knowledge is destroyed.
4. **Approval**: Formal sign-off resulting in an "Approved" status.
5. **Documentation**: An entry in this register.

---

## SECTION 6: Implementation Rules

Implementation of a refinement decision occurs **only after**:

1. **Approved Decision**: The register entry must officially be marked "Approved".
2. **Repository Backup**: The current state of the repository must be secure.
3. **Git Checkpoint**: A formal commit or branch must be created prior to the change.
4. **Verification**: Post-implementation verification to ensure the change executed exactly as documented.
5. **Documentation Update**: The register entry's Implementation Status is updated to "Implemented".

---

## SECTION 7: Decision Status Definitions

A decision record flows through the following states:

* **Proposed**: The refinement action is suggested but has not yet been reviewed.
* **Under Review**: The action is actively being evaluated for impact and evidence.
* **Approved**: The action is authorized for execution.
* **Implemented**: The action has been successfully executed and verified in the repository.
* **Rejected**: The action was denied due to architectural conflicts or lack of evidence.
* **Deferred**: The action is valid but postponed to a future milestone.
* **Archived**: The decision record itself is closed and preserved for historical auditing.

---

## SECTION 8: Governance Rules

The following constitutional rules strictly govern repository refinement:

* **No undocumented repository changes**: Every single modification requires a register entry.
* **No direct deletion**: Assets are archived, not deleted, unless mathematically proven to be 100% exact duplicates.
* **No duplicate removal without evidence**: The exact nature of the duplication must be proven in the register.
* **No document merge without preserving knowledge**: No context, rule, or architectural decision may be lost during a merge.
* **No formula movement without traceability**: Astrological formulas must maintain strict lineage.
* **No architectural modification during refinement**: Refinement is strictly structural cleanup; it never alters deterministic logic, system architecture, or engine ownership.

---

## SECTION 9: Illustrative Examples

*(Note: These examples are illustrative only and do not authorize implementation).*

### Example 1: Document Archive
* **Decision ID**: REF-001
* **Category**: Document Archive
* **Component**: `PHASE9_STEP1_REPORT_PROFILE_FIX.md`
* **Proposed Action**: Move to `/docs/archive/phase_reports/`
* **Architectural Reason**: Document is a historical implementation artifact superseded by the `Master Probability Knowledge Package`.
* **Approval Status**: Approved

### Example 2: Folder Merge
* **Decision ID**: REF-002
* **Category**: Folder Merge
* **Component**: `/docs/formulas/` and `/formulas/`
* **Proposed Action**: Consolidate all contents into `/docs/formulas/` and remove the redundant root folder.
* **Architectural Reason**: Reduces root-level clutter and unifies formula documentation.
* **Approval Status**: Under Review

---

## SECTION 10: Governance Freeze

This Repository Refinement Decision Register is hereby declared part of the permanent Golden Master Constitution.

All future refinement decisions must be permanently recorded here before any implementation occurs. Changes to the structure, rules, or authority of this register require a rigorous formal process:

* **Architecture Decision Record (ADR)**
* **Architecture Review**
* **Documentation Update**
* **Version Increment**

---

## SECTION 11: Approved Decisions

### REF-BKL-001
* **Decision ID**: REF-BKL-001
* **Date**: 2026-07-04
* **Category**: Knowledge Consolidation
* **Component**: `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md`, `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md`, `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md`
* **Current Location**: Root directory
* **Proposed Action**: Create `PIPELINE_RUNNER_KNOWLEDGE_PACKAGE.md`. Extract pipeline orchestration logic from Question Engine and Master Probability packages into this new canonical source.
* **Architectural Reason**: Resolves CON-001. Establishes the Pipeline Runner as the canonical owner of the DAG execution sequence, enforcing the Single Responsibility Principle.
* **Supporting Evidence**: BKL-001 Execution Package and Final Canonical Ownership Verification (Option B).
* **Impact Assessment**: Decouples orchestration from engine logic. Question and Master Probability engines become completely isolated from execution DAG mechanics.
* **Approval Status**: Approved
* **Implementation Status**: Implemented
* **Notes**: Creation of new canonical source architecturally justified.

### REF-BKL-002
* **Decision ID**: REF-BKL-002
* **Date**: 2026-07-04
* **Category**: Knowledge Consolidation
* **Component**: `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md`, `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md`
* **Current Location**: Root directory
* **Proposed Action**: Remove 60/40 probability synthesis math from Question Engine and establish canonical ownership inside Master Probability Engine.
* **Architectural Reason**: Restores the Question Engine as a pure Orchestrator. Defends the Master Probability Engine as the sole canonical owner of mathematical synthesis, resolving CON-002.
* **Supporting Evidence**: BKL-002 Execution Package and Architectural Evaluation (Option B).
* **Impact Assessment**: Eradicates mathematical calculations from the routing layer, enforcing Single Responsibility and One Formula One Owner.
* **Approval Status**: Approved
* **Implementation Status**: Implemented
* **Notes**: Resolves formula ownership conflict.

### REF-BKL-003
* **Decision ID**: REF-BKL-003
* **Date**: 2026-07-05
* **Category**: Knowledge Consolidation
* **Component**: `FORMULA_GENERATION_GOVERNANCE_v1.md`, `FORMULA_REPOSITORY_GOVERNANCE_v1.md`, `FORMULA_LIBRARY_SCALING_GOVERNANCE_v1.md`
* **Current Location**: Root directory
* **Proposed Action**: Merge into a single Canonical Governance document `FORMULA_GOVERNANCE_v1.0.md` and archive the original three documents to `docs/archive/formulas/`.
* **Architectural Reason**: Resolves governance contradiction regarding formula lifecycle processes by establishing one unambiguous constitutional rulebook, in compliance with "One Canonical Source Per Concept" rule.
* **Supporting Evidence**: BKL-003 Execution Package, Architectural Evaluation (Option B), Canonical Source Mapping.
* **Impact Assessment**: Eliminates contradictory developer instructions. Formula ownership unchanged. Enforces strict inheritance and template reuse.
* **Approval Status**: Approved
* **Implementation Status**: Implemented
* **Notes**: All unique architectural constraints from the original three documents were physically preserved in the new canonical source.

### REF-BKL-004
* **Decision ID**: REF-BKL-004
* **Date**: 2026-07-05
* **Category**: Knowledge Consolidation
* **Component**: `FORMULA_REPOSITORY_DATA_MODEL_v1.md`, `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md`
* **Current Location**: Root directory
* **Proposed Action**: Transfer duplicate Yoga Data Model knowledge (Yoga Support definitions) into the canonical Yoga Intelligence Knowledge Package. Replace the section in the Data Model with a reference.
* **Architectural Reason**: Resolves CON-004 by affirming the Yoga Engine as the sole canonical owner of Yoga Data Models, complying with the "One Canonical Source Per Concept" rule.
* **Supporting Evidence**: BKL-004 Execution Package, Architectural Evaluation (Option B).
* **Impact Assessment**: Eradicates duplication and calculation drift. Yoga knowledge and formula ownership are unchanged.
* **Approval Status**: Approved
* **Implementation Status**: Implemented
* **Notes**: Yoga knowledge safely preserved without altering Yoga Engine behavior.

### REF-BKL-005
* **Decision ID**: REF-BKL-005
* **Date**: 2026-07-07
* **Category**: Knowledge Consolidation
* **Component**: Phase 8-16 Readouts
* **Current Location**: Root directory
* **Proposed Action**: Extract hidden architectural constraints and rules from legacy Phase 8-16 reports and convert them into formal ADRs.
* **Architectural Reason**: Resolves undocumented architectural rules and protects repository governance from drift by formalizing constraints as Architecture Decision Records.
* **Supporting Evidence**: ADR_INVENTORY_v1.0.md
* **Impact Assessment**: No logic or governance changes. Explicitly preserves architectural intent securely in ADR format.
* **Approval Status**: Approved
* **Implementation Status**: Implemented
* **Notes**: 16 ADRs successfully recovered. Final Constitutional Audit passed.
