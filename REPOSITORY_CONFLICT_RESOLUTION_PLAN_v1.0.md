# REPOSITORY CONFLICT RESOLUTION PLAN

## SECTION 1: Document Information

* **Date**: 2026-06-29
* **Repository**: D:\vedic-ai-golden-master
* **Project**: SVAI-GM
* **Program**: Program B
* **Milestone**: GM-005
* **Phase**: Canonical Knowledge Mapping
* **Version**: v1.0
* **Status**: DRAFT
* **Author**: Coding Engine

---

## SECTION 2: Purpose

The Repository Analysis Foundation has identified numerous architectural, governance, and documentation conflicts stemming from iterative legacy phases. These conflicts threaten the integrity of the Golden Master. 

However, conflicts must be resolved through rigorous evidence rather than opinion. This document establishes the constitutional framework for evaluating and approving conflict resolutions. It mandates that **knowledge preservation always has priority over repository simplification**, ensuring no foundational logic is lost during cleanup.

---

## SECTION 3: Conflict Classification Model

Conflicts must be categorized to determine the correct resolution workflow:

* **Architectural Conflict**: Disagreement over system boundaries, engine orchestration, or data flow between two or more design documents.
* **Governance Conflict**: Overlapping, redundant, or contradictory rules governing compliance, ownership, or lifecycle management.
* **Documentation Conflict**: Misaligned descriptions, definitions, or instructions between manuals or readmes.
* **Formula Conflict**: Discrepancies in astrological mathematics, variables, or formula definitions across multiple sources.
* **Ownership Conflict**: Multiple engines or modules claiming responsibility for generating the same output contract.
* **Dependency Conflict**: Circular references or impossible dependency chains defined in architecture plans.
* **Historical Conflict**: Legacy phase reports that contradict current canonical reality.
* **Terminology Conflict**: Inconsistent naming conventions for astrological or system concepts.

---

## SECTION 4: Conflict Register

The following conflicts were formally identified during the Canonical Knowledge Mapping phase.

| Conflict ID | Repository Concept | Conflicting Documents | Conflict Type | Evidence | Architectural Risk | Proposed Resolution Strategy | Decision Register Reference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CON-001** | Pipeline Orchestration | `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` vs `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` | Architectural Conflict | Both documents claim to define the execution sequence of `PipelineRunner`. | Execution drift, broken routing | Extract orchestration to a dedicated Canonical Pipeline package | Pending | Identified |
| **CON-002** | Formula Governance | `FORMULA_GENERATION_GOVERNANCE_v1.md`, `FORMULA_REPOSITORY_GOVERNANCE_v1.md`, `FORMULA_LIBRARY_SCALING_GOVERNANCE_v1.md` | Governance Conflict | Three separate `v1` files dictate overlapping formula lifecycle rules. | Compliance failure | Consolidate into a single Canonical Formula Governance document | Pending | Identified |
| **CON-003** | ADR Collection | `PHASE15_MANDALI_DECOUPLING_DECISION_RECORD.md` vs legacy `PHASE*_REPORT.md` files | Documentation Conflict | Phase 15 uses ADRs, while Phase 8-14 embeds decisions in readouts. | Loss of historical context | Establish formal ADR directory; extract key decisions from phase reports | Pending | Identified |
| **CON-004** | Yoga Formulas | `YOGA_INTELLIGENCE_KNOWLEDGE_PACKAGE.md` vs `FORMULA_REPOSITORY_DATA_MODEL_v1.md` | Formula Conflict | Both attempt to define the mathematical structure for Yogas. | Calculation drift | Affirm Knowledge Package as canonical; update Data Model to reference it | Pending | Identified |
| **CON-005** | Question Formulas | `QUESTION_REGISTRY_MASTER_v1.md` vs `PHASE11` reports | Formula Conflict | Phase 11 hardcodes definitions that contradict the Master Registry. | API contract failure | Archive Phase 11 readouts; enforce Master Registry as canonical | Pending | Identified |
| **CON-006** | Probability Formulas | `MASTER_PROBABILITY_KNOWLEDGE_PACKAGE.md` vs `QUESTION_ENGINE_KNOWLEDGE_PACKAGE.md` | Formula Conflict | Question engine hardcodes 60/40 weighting contrary to Master Probability. | Mathematical inconsistency | Remove deterministic math from Question Engine (Orchestrator Only) | Pending | Identified |

*(Note: No conflicts are resolved by this document. This register merely catalogs them for future refinement.)*

---

## SECTION 5: Conflict Evaluation Process

Every conflict must traverse the following strict evaluation workflow before repository refinement is permitted:

1. **Evidence Collection**: Gather all conflicting documents and cross-reference with Golden Master source code.
2. **Dependency Review**: Assess what breaks if Document A is chosen over Document B.
3. **Architectural Review**: Determine which document aligns with the Golden Master Constitution.
4. **Knowledge Preservation Review**: Identify unique caveats in the "losing" document that must be ported to the canonical source.
5. **Decision Register Entry**: Formally propose the resolution in the `REPOSITORY_REFINEMENT_DECISION_REGISTER_v1.0.md`.
6. **Approval**: Obtain architectural sign-off.
7. **Controlled Refinement**: Execute the file changes (merge, delete, update).
8. **Validation**: Test the repository to ensure the conflict is eliminated without regressions.

---

## SECTION 6: Resolution Principles

All conflict resolutions are bound by the following constitutional principles:

* **Evidence Before Decision**: Resolutions must be based on actual code and architectural intent, not arbitrary preference.
* **Single Canonical Owner**: Every conflict must end with exactly one canonical source of truth.
* **Knowledge Preservation**: Context, definitions, and domain nuances must not be lost during consolidation.
* **No Hidden Assumptions**: If evidence is missing, the conflict is paused until evidence is discovered.
* **No Formula Changes During GM-005**: Resolving formula documentation conflicts does not authorize altering the underlying astrological math.
* **No Architectural Changes Without ADR**: If resolving a conflict changes the system's design, an Architecture Decision Record must be authored.

---

## SECTION 7: Conflict Priority Model

Conflicts are triaged using the following priority model:

* **Critical**: Imminent threat to deterministic math or engine boundaries (e.g., Formula or Architectural Conflicts). *Requires immediate action before any other refinement.*
* **High**: Threat to compliance or data contracts (e.g., Governance or Ownership Conflicts). *Action required in current milestone.*
* **Medium**: Threat to maintainability (e.g., Dependency Conflicts). *Action required before GM-008 Foundation phase.*
* **Low**: Formatting or minor legacy naming issues (e.g., Documentation or Terminology Conflicts). *Actioned as bandwidth permits.*
* **Informational**: Historical inaccuracies in archived phase reports (e.g., Historical Conflicts). *No action required; flag for archive.*

---

## SECTION 8: Repository Risk Assessment

If the conflicts cataloged in Section 4 remain unresolved, the Golden Master faces the following systemic risks:

* **Architecture Drift**: Developers may build against the wrong orchestration rules (e.g., Pipeline conflict).
* **Conflicting Documentation**: Future agents will hallucinate rules based on contradictory readouts.
* **Duplicate Governance**: Governance audits will fail because evaluators check different rulesets.
* **Formula Ambiguity**: Engines will drift mathematically if they source logic from differing Markdown catalogs.
* **Incorrect Repository Refinement**: Attempting to clean the repository without resolving these conflicts guarantees that critical knowledge will be accidentally deleted.
* **Knowledge Fragmentation**: Astrological definitions remain scattered, preventing the creation of a unified AI Assistant knowledge base.

---

## SECTION 9: Out of Scope

This document explicitly does **NOT**:

* Resolve conflicts
* Rename files
* Delete files
* Merge documents
* Modify formulas
* Modify architecture
* Implement repository refinement

---

## SECTION 10: Summary

The Repository Conflict Resolution Plan establishes the exact constitutional framework necessary to cure the Golden Master of its historical contradictions. 

By categorizing conflicts by type and priority, and enforcing a strict evidence-based evaluation process, this plan guarantees that the repository will emerge from GM-005 cleaner, mathematically purer, and architecturally unified. Every future repository refinement decision must reference this plan and the Repository Refinement Decision Register before implementation.
